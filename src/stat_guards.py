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


def t_two_sided_p_value(t_stat: float, df: float) -> float:
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


# === SPEC-DSR-001: Deflated Sharpe Ratio (多重検定補正) ===
# 月次較正は asset/rank/side/regime/narrative にわたり多数のセルを同時に検定する。
# 純粋な偶然でも一部のセルは p<0.05 を満たす(選択バイアス)。
# Deflated Sharpe Ratio (Bailey & Lopez de Prado, 2014) は「N回の試行のうち
# 期待される最大Sharpe」を基準に観測Sharpeを割り引き、偶然の好成績を排除する。
# これは憲章「過学習への冷徹なブレーキ」「後知恵バイアス排除」の統計的実装。

# DSRがこの確信度以上のときのみ「多重検定後も有意」と判定する。
DEFLATED_SHARPE_CONFIDENCE = 0.95
# オイラー＝マスケローニ定数(期待最大Sharpeの推定に使う)。
_EULER_MASCHERONI = 0.5772156649015329


def norm_cdf(x: float) -> float:
    """標準正規分布の累積分布関数 Φ(x)。標準ライブラリのerfで計算。"""
    return 0.5 * math.erfc(-float(x) / math.sqrt(2.0))


def norm_ppf(p: float) -> float:
    """標準正規分布の逆累積分布関数(probit)。Acklamの有理近似。

    p<=0 で -inf、p>=1 で +inf。相対誤差は約1.15e-9。
    """
    if p <= 0.0:
        return -math.inf
    if p >= 1.0:
        return math.inf
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    p_low = 0.02425
    p_high = 1.0 - p_low
    if p < p_low:
        q = math.sqrt(-2.0 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
               ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0)
    if p <= p_high:
        q = p - 0.5
        r = q * q
        return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
               (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1.0)
    q = math.sqrt(-2.0 * math.log(1.0 - p))
    return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0)


def _moments(clean: list[float]) -> tuple[float, float, float, float]:
    """(mean, std(標本/n-1), skewness, kurtosis(正規=3)) を返す。"""
    n = len(clean)
    mean = sum(clean) / n
    var_sample = sum((v - mean) ** 2 for v in clean) / (n - 1)
    std = math.sqrt(var_sample) if var_sample > 0 else 0.0
    if std <= 0.0:
        return mean, 0.0, 0.0, 3.0
    m2 = sum((v - mean) ** 2 for v in clean) / n
    m3 = sum((v - mean) ** 3 for v in clean) / n
    m4 = sum((v - mean) ** 4 for v in clean) / n
    skew = m3 / (m2 ** 1.5) if m2 > 0 else 0.0
    kurt = m4 / (m2 ** 2) if m2 > 0 else 3.0
    return mean, std, skew, kurt


def probabilistic_sharpe_ratio(values: Iterable[Any] | None, sr_benchmark: float = 0.0) -> float:
    """確率的Sharpe比(PSR): 真のSharpeが sr_benchmark を超える確率。

    歪度・尖度(非正規性)を補正する。n<2 や std=0 では 0.0。
    Sharpeは1トレードあたり(非年率)で観測系列と同一単位。
    """
    clean = _clean_values(values)
    n = len(clean)
    if n < 2:
        return 0.0
    mean, std, skew, kurt = _moments(clean)
    if std <= 0.0:
        return 0.0
    sr_hat = mean / std
    denom = 1.0 - skew * sr_hat + ((kurt - 1.0) / 4.0) * sr_hat * sr_hat
    if denom <= 0.0:
        return 0.0
    z = (sr_hat - sr_benchmark) * math.sqrt(n - 1) / math.sqrt(denom)
    return norm_cdf(z)


def expected_max_sharpe(n_trials: int, sharpe_variance: float) -> float:
    """N回の独立試行で期待される最大Sharpe比(帰無仮説の基準値)。

    Bailey & Lopez de Prado (2014) 式。sharpe_variance は試行間のSharpeの分散。
    n_trials<=1 または分散<=0 のとき 0.0(=多重検定補正なし)。
    """
    if n_trials <= 1 or sharpe_variance <= 0.0:
        return 0.0
    sigma = math.sqrt(sharpe_variance)
    e = math.e
    z1 = norm_ppf(1.0 - 1.0 / n_trials)
    z2 = norm_ppf(1.0 - 1.0 / (n_trials * e))
    return sigma * ((1.0 - _EULER_MASCHERONI) * z1 + _EULER_MASCHERONI * z2)


def deflated_sharpe_ratio(
    values: Iterable[Any] | None,
    n_trials: int,
    sharpe_variance: float,
) -> float:
    """Deflated Sharpe Ratio: 多重検定(N試行)を考慮しても観測Sharpeが
    偶然の最大値を超える確率。1.0に近いほど本物の優位性。

    n_trials<=1 のときは単一検定とみなし PSR(vs 0) に一致する。
    """
    sr_star = expected_max_sharpe(n_trials, sharpe_variance)
    return probabilistic_sharpe_ratio(values, sr_star)


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


# === SPEC-NQ-001: ナラティブ×クオンツ ===

def t_test_welch(
    values_a: Iterable[Any] | None,
    values_b: Iterable[Any] | None,
) -> tuple[float, float, float]:
    """Welchの二標本t検定(両側、等分散を仮定しない)。(t統計量, p値, 自由度)を返す。

    どちらかの群が n < 2 の場合は検定不能として (0.0, 1.0, 0.0)。
    自由度はWelch-Satterthwaite近似(非整数)。p値は正確なt分布から計算。
    """
    a = _clean_values(values_a)
    b = _clean_values(values_b)
    n_a, n_b = len(a), len(b)
    if n_a < 2 or n_b < 2:
        return 0.0, 1.0, 0.0
    mean_a = sum(a) / n_a
    mean_b = sum(b) / n_b
    var_a = sum((v - mean_a) ** 2 for v in a) / (n_a - 1)
    var_b = sum((v - mean_b) ** 2 for v in b) / (n_b - 1)
    se_sq = var_a / n_a + var_b / n_b
    if se_sq <= 0.0:
        if mean_a != mean_b:
            return math.copysign(math.inf, mean_a - mean_b), 0.0, float(n_a + n_b - 2)
        return 0.0, 1.0, float(n_a + n_b - 2)
    t_stat = (mean_a - mean_b) / math.sqrt(se_sq)
    df = (se_sq ** 2) / (
        (var_a / n_a) ** 2 / (n_a - 1) + (var_b / n_b) ** 2 / (n_b - 1)
    )
    return t_stat, t_two_sided_p_value(t_stat, df), df
