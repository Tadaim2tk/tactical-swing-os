"""jp_calendar.py のユニットテスト。"""

from __future__ import annotations

from datetime import date

import jp_calendar as cal


# ── is_market_holiday ────────────────────────────────────────────

def test_saturday_is_holiday():
    assert cal.is_market_holiday(date(2026, 6, 13))  # 土曜

def test_sunday_is_holiday():
    assert cal.is_market_holiday(date(2026, 6, 14))  # 日曜

def test_weekday_is_not_holiday():
    assert not cal.is_market_holiday(date(2026, 6, 16))  # 月曜

def test_jan1_is_holiday():
    assert cal.is_market_holiday(date(2026, 1, 1))

def test_jan2_is_holiday():
    assert cal.is_market_holiday(date(2026, 1, 2))  # 年始

def test_jan3_is_holiday():
    assert cal.is_market_holiday(date(2026, 1, 3))  # 年始

def test_dec31_is_holiday():
    assert cal.is_market_holiday(date(2025, 12, 31))  # 大晦日

def test_constitution_day_may3():
    assert cal.is_market_holiday(date(2026, 5, 3))  # 憲法記念日

def test_childrens_day_may5():
    assert cal.is_market_holiday(date(2026, 5, 5))  # こどもの日

def test_showa_day_apr29():
    assert cal.is_market_holiday(date(2026, 4, 29))  # 昭和の日

def test_culture_day_nov3():
    assert cal.is_market_holiday(date(2026, 11, 3))  # 文化の日

def test_labor_day_nov23():
    assert cal.is_market_holiday(date(2026, 11, 23))  # 勤労感謝の日

def test_foundation_day_feb11():
    assert cal.is_market_holiday(date(2026, 2, 11))  # 建国記念日

def test_emperors_birthday_feb23():
    assert cal.is_market_holiday(date(2026, 2, 23))  # 天皇誕生日

def test_mountain_day_aug11():
    assert cal.is_market_holiday(date(2026, 8, 11))  # 山の日


# ── next_business_day ─────────────────────────────────────────────

def test_next_business_day_from_friday():
    # 金曜から1営業日後 = 月曜（土日スキップ）
    assert cal.next_business_day(date(2026, 6, 12)) == date(2026, 6, 15)

def test_next_business_day_from_saturday():
    # 土曜から1営業日後 = 月曜
    assert cal.next_business_day(date(2026, 6, 13)) == date(2026, 6, 15)

def test_next_business_day_n2_from_friday():
    # 金曜から2営業日後 = 火曜
    assert cal.next_business_day(date(2026, 6, 12), 2) == date(2026, 6, 16)

def test_next_business_day_skips_holiday():
    # 4/29(昭和の日・祝)前の木曜から1営業日後 = 4/30 (金)
    assert cal.next_business_day(date(2026, 4, 28)) == date(2026, 4, 30)

def test_next_business_day_year_end_skip():
    # 12/30(火)から1営業日後 = 1/4（大晦日・元旦・1/2・1/3 をスキップ）
    result = cal.next_business_day(date(2025, 12, 30))
    assert result == date(2026, 1, 5)

def test_next_business_day_n0_weekday_is_same():
    d = date(2026, 6, 16)  # 月曜
    assert cal.next_business_day(d, 0) == d

def test_next_business_day_n0_holiday_advances():
    d = date(2026, 1, 1)  # 元旦
    result = cal.next_business_day(d, 0)
    assert not cal.is_market_holiday(result)


# ── intended_order_date / assumed_execution_date ─────────────────

def test_intended_order_date_from_monday():
    # 月曜判断 → 注文日 = 火曜
    assert cal.intended_order_date(date(2026, 6, 15)) == date(2026, 6, 16)

def test_assumed_execution_date_from_monday():
    # 月曜判断 → 想定約定日 = 水曜
    assert cal.assumed_execution_date(date(2026, 6, 15)) == date(2026, 6, 17)

def test_intended_order_date_from_friday():
    # 金曜判断 → 注文日 = 月曜
    assert cal.intended_order_date(date(2026, 6, 12)) == date(2026, 6, 15)

def test_assumed_execution_date_from_friday():
    # 金曜判断 → 想定約定日 = 火曜
    assert cal.assumed_execution_date(date(2026, 6, 12)) == date(2026, 6, 16)

def test_assumed_execution_date_skips_golden_week():
    # GW前 4/28(火) 判断 → 注文日 4/30(木)、約定日 5/1(金)
    # ※ 4/29(水)=昭和の日
    intended = cal.intended_order_date(date(2026, 4, 28))
    assumed = cal.assumed_execution_date(date(2026, 4, 28))
    assert not cal.is_market_holiday(intended)
    assert not cal.is_market_holiday(assumed)
    assert assumed > intended


# ── business_days_between ─────────────────────────────────────────

def test_business_days_same_day_is_zero():
    d = date(2026, 6, 16)
    assert cal.business_days_between(d, d) == 0

def test_business_days_mon_to_fri():
    # 月〜金 = 4営業日（火水木金）
    assert cal.business_days_between(date(2026, 6, 15), date(2026, 6, 19)) == 4

def test_business_days_over_weekend():
    # 金〜月 = 1営業日（月のみ）
    assert cal.business_days_between(date(2026, 6, 12), date(2026, 6, 15)) == 1


# ── vernal / autumnal equinox ────────────────────────────────────

def test_vernal_equinox_2026_is_march():
    d = cal._vernal_equinox(2026)
    assert d.month == 3
    assert 19 <= d.day <= 22

def test_autumnal_equinox_2026_is_september():
    d = cal._autumnal_equinox(2026)
    assert d.month == 9
    assert 21 <= d.day <= 24


# ── substitute holiday ────────────────────────────────────────────

def test_substitute_holiday_when_holiday_on_sunday():
    # 2026年 元旦 = 木曜なので振替なし
    # 天皇誕生日(2/23)が日曜の年があれば振替月曜が休みになる
    # 2025年 2/23 は日曜 → 2/24(月)が振替
    holidays_2025 = cal._get_holidays(2025)
    feb23_2025 = date(2025, 2, 23)
    feb24_2025 = date(2025, 2, 24)
    if feb23_2025.weekday() == 6:  # 日曜なら
        assert feb24_2025 in holidays_2025
