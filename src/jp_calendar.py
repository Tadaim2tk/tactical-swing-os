"""日本株式市場営業日カレンダー (JP-CAL-001)。

ワン株の「注文→約定」ラグ計算に使用する。
単純な +1 day では土日祝・年末年始をまたぐ。

対象: 2000〜2099年（春分・秋分の計算式の有効範囲）
非対応: 天皇即位等の臨時休場（ただし直近の追加ルールは記載）

依存: stdlib のみ（datetime, math）
"""

from __future__ import annotations

import math
from datetime import date, timedelta


# ── 祝日計算ヘルパー ──────────────────────────────────────────────

def _nth_weekday_of_month(year: int, month: int, weekday: int, n: int) -> date:
    """第n X曜日を返す。weekday=0:月, 1:火, ..., 6:日。"""
    first = date(year, month, 1)
    delta = (weekday - first.weekday()) % 7
    return first + timedelta(days=delta + (n - 1) * 7)


def _vernal_equinox(year: int) -> date:
    """春分の日（近似）。2000〜2099年対象。"""
    day = math.floor(20.8431 + 0.242194 * (year - 1980) - math.floor((year - 1980) / 4))
    return date(year, 3, day)


def _autumnal_equinox(year: int) -> date:
    """秋分の日（近似）。2000〜2099年対象。"""
    day = math.floor(23.2488 + 0.242194 * (year - 1980) - math.floor((year - 1980) / 4))
    return date(year, 9, day)


def _public_holidays(year: int) -> set[date]:
    """その年の国民の祝日と振替休日（臨時休場含む）をまとめて返す。"""
    holidays: set[date] = set()

    # 固定日祝日
    fixed = [
        (1, 1),   # 元旦
        (2, 11),  # 建国記念日
        (2, 23),  # 天皇誕生日（2020〜）
        (4, 29),  # 昭和の日
        (5, 3),   # 憲法記念日
        (5, 4),   # みどりの日
        (5, 5),   # こどもの日
        (8, 11),  # 山の日（2016〜）
        (11, 3),  # 文化の日
        (11, 23), # 勤労感謝の日
    ]
    # 2016年より前は山の日なし
    if year < 2016:
        fixed = [(m, d) for m, d in fixed if (m, d) != (8, 11)]
    # 2020年より前は天皇誕生日 = 12/23 (平成)
    if year < 2020:
        fixed = [(m, d) for m, d in fixed if (m, d) != (2, 23)]
        if year >= 1989:  # 平成以降
            fixed.append((12, 23))

    for month, day in fixed:
        holidays.add(date(year, month, day))

    # ハッピーマンデー
    holidays.add(_nth_weekday_of_month(year, 1, 0, 2))   # 成人の日 (第2月)
    holidays.add(_nth_weekday_of_month(year, 7, 0, 3))   # 海の日 (第3月)
    holidays.add(_nth_weekday_of_month(year, 9, 0, 3))   # 敬老の日 (第3月)
    # スポーツの日: 2022〜 第2月, 2000〜2021 体育の日 (同じ第2月)
    holidays.add(_nth_weekday_of_month(year, 10, 0, 2))

    # 春分・秋分
    holidays.add(_vernal_equinox(year))
    holidays.add(_autumnal_equinox(year))

    # 振替休日: 日曜日の祝日→翌月曜日 (複数日連続もケア)
    holidays |= _substitute_holidays(holidays, year)

    # 国民の休日: 2つの祝日にはさまれた平日 (主にゴールデンウィーク5/2等)
    holidays |= _citizens_holidays(holidays, year)

    return holidays


def _substitute_holidays(base_holidays: set[date], year: int) -> set[date]:
    """振替休日を計算して返す。"""
    substitutes: set[date] = set()
    for h in sorted(base_holidays):
        if h.weekday() == 6:  # 日曜
            sub = h + timedelta(days=1)
            while sub in base_holidays or sub in substitutes:
                sub += timedelta(days=1)
            substitutes.add(sub)
    return substitutes


def _citizens_holidays(base_holidays: set[date], year: int) -> set[date]:
    """国民の休日: 前後を祝日にはさまれた平日を休日に。"""
    all_h = set(base_holidays)
    extra: set[date] = set()
    for h in sorted(all_h):
        candidate = h + timedelta(days=2)
        middle = h + timedelta(days=1)
        if candidate in all_h and middle.weekday() < 5 and middle not in all_h:
            extra.add(middle)
    return extra


# 年をまたがないようにキャッシュ
_holiday_cache: dict[int, set[date]] = {}


def _get_holidays(year: int) -> set[date]:
    if year not in _holiday_cache:
        _holiday_cache[year] = _public_holidays(year)
    return _holiday_cache[year]


# ── 株式市場休場日 ────────────────────────────────────────────────

def is_market_holiday(d: date) -> bool:
    """東京証券取引所が休場かどうかを返す。

    土日・国民の祝日・年末年始（12/31〜1/3）を対象とする。
    臨時休場（天皇即位等）は手動追加が必要。
    """
    # 土日
    if d.weekday() >= 5:
        return True
    # 年末（大晦日）
    if d.month == 12 and d.day == 31:
        return True
    # 年始（1/2, 1/3）
    if d.month == 1 and d.day in (2, 3):
        return True
    # 国民の祝日・振替
    return d in _get_holidays(d.year)


# ── 営業日計算 ────────────────────────────────────────────────────

def next_business_day(d: date, n: int = 1) -> date:
    """d の n 営業日後を返す。n >= 1 で前方、n=0 で d 自体（休場なら次の営業日）。"""
    if n < 0:
        raise ValueError(f"n は 0 以上の整数にしてください: {n}")
    result = d
    if n == 0:
        while is_market_holiday(result):
            result += timedelta(days=1)
        return result
    steps = 0
    current = d
    while steps < n:
        current += timedelta(days=1)
        if not is_market_holiday(current):
            steps += 1
    return current


def business_days_between(start: date, end: date) -> int:
    """start（含む）から end（含む）までの営業日数。end < start なら負を返す。"""
    if end == start:
        return 0 if not is_market_holiday(start) else 0
    direction = 1 if end > start else -1
    count = 0
    current = start + timedelta(days=direction)
    while (direction == 1 and current <= end) or (direction == -1 and current >= end):
        if not is_market_holiday(current):
            count += direction
        current += timedelta(days=direction)
    return count


def intended_order_date(decision_date: date) -> date:
    """判断日の翌営業日（注文予定日）を返す。"""
    return next_business_day(decision_date, 1)


def assumed_execution_date(decision_date: date) -> date:
    """判断日の翌々営業日（想定約定日 = 注文日の翌営業日）を返す。"""
    return next_business_day(decision_date, 2)
