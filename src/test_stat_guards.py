from __future__ import annotations

import math

import stat_guards
from build_monthly_calibration import proposed_change


# === t検定の数値的正確性 ===

def test_t_test_known_value():
    # [1,2,3,4,5]: mean=3, sd=1.5811, t=4.2426, df=4 -> 両側p ≈ 0.0132 (scipy基準値)
    t_stat, p_value = stat_guards.t_test_one_sample([1, 2, 3, 4, 5])
    assert abs(t_stat - 4.2426) < 0.001
    assert abs(p_value - 0.0132) < 0.001


def test_t_test_zero_mean_is_not_significant():
    values = [1.0, -1.0] * 15
    _, p_value = stat_guards.t_test_one_sample(values)
    assert p_value > 0.9


def test_t_test_constant_nonzero_series():
    t_stat, p_value = stat_guards.t_test_one_sample([0.5] * 10)
    assert math.isinf(t_stat)
    assert p_value == 0.0


def test_t_test_insufficient_n():
    assert stat_guards.t_test_one_sample([1.0]) == (0.0, 1.0)
    assert stat_guards.t_test_one_sample([]) == (0.0, 1.0)


def test_nan_and_none_are_ignored():
    report = stat_guards.significance_report([1.0, None, float("nan"), 2.0, 3.0])
    assert report["n"] == 3


def test_sharpe_ratio():
    # mean=0.5, sd≈0.7187 -> sharpe≈0.6957
    values = [1.0] * 20 + [-0.5] * 10
    assert abs(stat_guards.sharpe_ratio(values) - 0.6957) < 0.01
    assert stat_guards.sharpe_ratio([0.5] * 5) == 0.0
    assert stat_guards.sharpe_ratio([]) == 0.0


# === proposed_change ゲート挙動 ===

def metrics_of(values):
    n = len(values)
    wins = sum(1 for v in values if v > 0)
    return n, (wins / n if n else 0.0), (sum(values) / n if n else 0.0)


def test_below_30_samples_is_rejected():
    values = [1.0] * 29
    n, win, avg = metrics_of(values)
    change, reason = proposed_change(n, win, avg, values)
    assert change == 0.0
    assert "データ不足" in reason


def test_strong_significant_performance_proposes_increase():
    # n=30, avg_r=0.5, win=0.667, sharpe≈0.70, p≈0.0007
    values = [1.0] * 20 + [-0.5] * 10
    n, win, avg = metrics_of(values)
    change, reason = proposed_change(n, win, avg, values)
    assert change == 0.05
    assert "sharpe=" in reason and "p=" in reason


def test_significant_loss_proposes_decrease_without_sharpe_gate():
    # n=30, avg_r=-0.5: 損失が有意ならSharpe閾値なしで減少(Ruin回避優先)
    values = [0.5] * 10 + [-1.0] * 20
    n, win, avg = metrics_of(values)
    change, reason = proposed_change(n, win, avg, values)
    assert change == -0.05


def test_not_significant_is_rejected_even_with_30_samples():
    values = [1.0, -1.0] * 15
    n, win, avg = metrics_of(values)
    change, reason = proposed_change(n, win, avg, values)
    assert change == 0.0
    assert "統計的有意性なし" in reason


def test_significant_but_low_sharpe_blocks_increase():
    # mean=0.45, sd≈1.017 -> sharpe≈0.443 (有意だがSharpe<=0.5)
    values = [1.45] * 15 + [-0.55] * 15
    n, win, avg = metrics_of(values)
    change, reason = proposed_change(n, win, avg, values)
    assert change == 0.0
    assert "Sharpe" in reason


# === SPEC-RD-001: time decay ===

def test_decay_weight_half_life():
    assert stat_guards.decay_weight(0) == 1.0
    assert abs(stat_guards.decay_weight(90) - 0.5) < 1e-12
    assert abs(stat_guards.decay_weight(180) - 0.25) < 1e-12
    assert stat_guards.decay_weight(-10) == 1.0  # 未来日付は重み1に丸める


def test_decayed_mean_recent_dominates():
    # 直近+1.0(重み1.0) vs 360日前-1.0(重み0.0625) -> 正側に寄る
    result = stat_guards.decayed_mean([1.0, -1.0], [0, 360])
    assert result["decayed_mean"] > 0.8
    assert abs(result["effective_n"] - 1.0625) < 1e-9


def test_decayed_mean_handles_bad_input():
    assert stat_guards.decayed_mean([], []) == {"decayed_mean": 0.0, "effective_n": 0.0}
    assert stat_guards.decayed_mean(None, None) == {"decayed_mean": 0.0, "effective_n": 0.0}
    result = stat_guards.decayed_mean([1.0, float("nan"), 2.0], [0, 0, "bad"])
    assert result["effective_n"] == 1.0  # 有効ペアは(1.0, 0)のみ


# === SPEC-NQ-001: Welch二標本t検定 ===

def test_welch_known_value():
    # a=[1..5], b=[2..6]: t=-1.0, df=8, 両側p≈0.3466 (scipy基準値)
    t, p, df = stat_guards.t_test_welch([1, 2, 3, 4, 5], [2, 3, 4, 5, 6])
    assert abs(t + 1.0) < 1e-9
    assert abs(df - 8.0) < 1e-9
    assert abs(p - 0.3466) < 0.002


def test_welch_clear_difference_is_significant():
    a = [1.0, 1.1, 0.9, 1.2, 0.8] * 6   # mean=1.0, n=30
    b = [-1.0, -0.9, -1.1, -0.8, -1.2] * 6  # mean=-1.0, n=30
    t, p, _ = stat_guards.t_test_welch(a, b)
    assert t > 10
    assert p < 0.001


def test_welch_insufficient_n():
    assert stat_guards.t_test_welch([1.0], [1.0, 2.0]) == (0.0, 1.0, 0.0)
    assert stat_guards.t_test_welch([], []) == (0.0, 1.0, 0.0)


# === SPEC-DSR-001: Deflated Sharpe Ratio (多重検定補正) ===

def test_norm_cdf_known_values():
    assert abs(stat_guards.norm_cdf(0.0) - 0.5) < 1e-12
    assert abs(stat_guards.norm_cdf(1.959963985) - 0.975) < 1e-6
    assert abs(stat_guards.norm_cdf(-1.959963985) - 0.025) < 1e-6


def test_norm_ppf_known_values():
    assert abs(stat_guards.norm_ppf(0.975) - 1.959963985) < 1e-6
    assert abs(stat_guards.norm_ppf(0.5)) < 1e-9


def test_norm_ppf_roundtrip():
    for p in [0.01, 0.1, 0.5, 0.9, 0.99]:
        assert abs(stat_guards.norm_cdf(stat_guards.norm_ppf(p)) - p) < 1e-7


def test_norm_ppf_edges():
    assert stat_guards.norm_ppf(0.0) == float("-inf")
    assert stat_guards.norm_ppf(1.0) == float("inf")


def test_psr_strong_positive_high():
    strong = [0.5] * 40 + [0.4] * 40  # 高い平均・低い分散
    assert stat_guards.probabilistic_sharpe_ratio(strong, 0.0) > 0.99


def test_psr_insufficient_or_zero_std():
    assert stat_guards.probabilistic_sharpe_ratio([1.0], 0.0) == 0.0
    assert stat_guards.probabilistic_sharpe_ratio([2.0, 2.0, 2.0], 0.0) == 0.0


def test_expected_max_sharpe_grows_with_trials():
    e10 = stat_guards.expected_max_sharpe(10, 0.25)
    e360 = stat_guards.expected_max_sharpe(360, 0.25)
    assert e360 > e10 > 0.0


def test_expected_max_sharpe_degenerate():
    assert stat_guards.expected_max_sharpe(1, 0.25) == 0.0
    assert stat_guards.expected_max_sharpe(360, 0.0) == 0.0


def test_dsr_deflation_rejects_lucky_cell():
    # 単独t検定は通るが多重検定では偽陽性になる中程度のセル
    import random
    random.seed(1)
    moderate = [random.gauss(0.15, 0.5) for _ in range(40)]
    assert stat_guards.significance_report(moderate)["significant"]  # 単独検定は通過
    dsr_single = stat_guards.deflated_sharpe_ratio(moderate, 1, 0.0)
    dsr_multi = stat_guards.deflated_sharpe_ratio(moderate, 360, 0.25)
    assert dsr_multi < dsr_single
    assert dsr_multi < stat_guards.DEFLATED_SHARPE_CONFIDENCE  # 多重検定後は棄却


def test_dsr_strong_cell_survives_deflation():
    strong = [0.5] * 40 + [0.4] * 40
    assert stat_guards.deflated_sharpe_ratio(strong, 360, 0.25) > stat_guards.DEFLATED_SHARPE_CONFIDENCE
