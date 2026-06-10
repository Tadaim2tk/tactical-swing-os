from __future__ import annotations

"""統計ガード(過学習ブレーキ)の単一情報源モジュール。

Tactical Swing OS 憲章の実装:
- 7. Active昇格条件: 最低30サンプル。それ未満はWatching固定。
- 8. 最大評価指標: 勝率ではなく、MAE改善・破滅回避・Sharpe等を優先。

設計上の制約:
- scipyに依存しない(GitHub Actionsのrequirements.txtにscipyは含まれない)。
- Student's t分布の正確な両側p値を標準ライブラリ(math)のみで計算する。
  (正則化不完全ベータ関数の連分数展開による。Numerical Recipes準拠)
"""

import math
from typing import Any, Iterable

# === 仕様凍結された閾値 (docs/SPEC_STATISTICAL_GUARDS.md SPEC-SG-001) ===
# 重み変更提案に必要な最低closedサンプル数。憲章ルール「最低30サンプル」。
MIN_SAMPLES_WEIGHT_CHANGE = 30
# 増加(攻撃方向)提案に追加で要求するSharpe比の下限。
MIN_SHARPE_FOR_INCREASE = 0.5
# 統計的有意性の判定水準(両側t検定)。
SIGNIFICANCE_ALPHA = 0.05


def _clean_values(values: Iterable[Any] | None) -> list[float]:
    """None/NaN/非数値を除外したfloatリストを返す。"""
    if values is None:
        return []
    out: list[float] = []
    for value in values:
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if math.isnan(number) or math.isinf(number):
            continue
        out.append(number)
    return out


def _log_beta(a: float, b: float) -> float:
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)


def _betacf(a: float, b: float, x: float) -> float:
    """不完全ベータ関数の連分数展開(Lentz法)。"""
    max_iterations = 300
    eps = 3.0e-12
    fpmin = 1.0e-300
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, max_iterations + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def _regularized_incomplete_beta(a: float, b: float, x: float) -> float:
    """正則化不完全ベータ関数 I_x(a, b)。"""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    ln_front = -_log_beta(a, b) + a * math.log(x) + b * math.log(1.0 - x)
    front = math.exp(ln_front)
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1.0 - x) / b


def t_two_sided_p_value(t_stat: float, df: int) -> float:
    """Student's t分布の正確な両側p値。 p = I_{df/(df+t^2)}(df/2, 1/2)"""
    if df <= 0:
        return 1.0
    if math.isinf(t_stat):
        return 0.0
    x = df / (df + t_stat * t_stat)
    p = _regularized_incomplete_beta(df / 2.0, 0.5, x)
    return min(1.0, max(0.0, p))


def t_test_one_sample(values: Iterable[Any] | None, mu: float = 0.0) -> tuple[float, float]:
    """一標本t検定(両側)。 (t統計量, p値) を返す。

    n < 2 の場合は検定不能として (0.0, 1.0)。
    分散ゼロかつ mean != mu の場合は (inf符号付き, 0.0)。
    """
    clean = _clean_values(values)
    n = len(clean)
    if n < 2:
        return 0.0, 1.0
    mean = sum(clean) / n
    variance = sum((v - mean) ** 2 for v in clean) / (n - 1)
    if variance <= 0.0:
        if mean != mu:
            return math.copysign(math.inf, mean - mu), 0.0
        return 0.0, 1.0
    standard_error = math.sqrt(variance / n)
    t_stat = (mean - mu) / standard_error
    return t_stat, t_two_sided_p_value(t_stat, n - 1)


def sharpe_ratio(values: Iterable[Any] | None) -> float:
    """R系列のSharpe比 (mean / 標本標準偏差)。stdが0なら0.0。"""
    clean = _clean_values(values)
    n = len(clean)
    if n < 2:
        return 0.0
    mean = sum(clean) / n
    variance = sum((v - mean) ** 2 for v in clean) / (n - 1)
    if variance <= 0.0:
        return 0.0
    return mean / math.sqrt(variance)


def significance_report(values: Iterable[Any] | None) -> dict[str, Any]:
    """R系列の統計サマリー。重み変更ゲートが参照する唯一の判定根拠。"""
    clean = _clean_values(values)
    n = len(clean)
    if n == 0:
        return {
            "n": 0,
            "mean": 0.0,
            "std": 0.0,
            "sharpe": 0.0,
            "t_stat": 0.0,
            "p_value": 1.0,
            "significant": False,
        }
    mean = sum(clean) / n
    if n < 2:
        std = 0.0
    else:
        std = math.sqrt(sum((v - mean) ** 2 for v in clean) / (n - 1))
    t_stat, p_value = t_test_one_sample(clean)
    return {
        "n": n,
        "mean": mean,
        "std": std,
        "sharpe": (mean / std) if std > 0 else 0.0,
        "t_stat": t_stat,
        "p_value": p_value,
        "significant": p_value < SIGNIFICANCE_ALPHA,
    }


# === SPEC-RD-001: 忘却 (time decay) ===
# 指数減衰の半減期(日)。古い成績ほど重みが下がる。情報提示用であり、
# SPEC-SG-001の統計ゲート(無加重t検定)には影響しない。
DECAY_HALF_LIFE_DAYS = 90


def decay_weight(age_days: float, half_life_days: float = DECAY_HALF_LIFE_DAYS) -> float:
    """経過日数に対する指数減衰重み。age=0で1.0、半減期ごとに半分。"""
    if half_life_days <= 0:
        return 1.0
    return 0.5 ** (max(0.0, float(age_days)) / float(half_life_days))


def decayed_mean(
    values: Iterable[Any] | None,
    age_days_list: Iterable[Any] | None,
    half_life_days: float = DECAY_HALF_LIFE_DAYS,
) -> dict[str, float]:
    """減衰加重平均と実効サンプル数(重みの総和)を返す。

    values と age_days_list は同じ長さであること。不正値のペアは除外。
    """
    if values is None or age_days_list is None:
        return {"decayed_mean": 0.0, "effective_n": 0.0}
    pairs: list[tuple[float, float]] = []
    for value, age in zip(values, age_days_list):
        try:
            v = float(value)
            a = float(age)
        except (TypeError, ValueError):
            continue
        if math.isnan(v) or math.isinf(v) or math.isnan(a) or math.isinf(a):
            continue
        pairs.append((v, max(0.0, a)))
    if not pairs:
        return {"decayed_mean": 0.0, "effective_n": 0.0}
    weights = [decay_weight(a, half_life_days) for _, a in pairs]
    total = sum(weights)
    if total <= 0:
        return {"decayed_mean": 0.0, "effective_n": 0.0}
    weighted = sum(w * v for (v, _), w in zip(pairs, weights))
    return {"decayed_mean": weighted / total, "effective_n": total}
