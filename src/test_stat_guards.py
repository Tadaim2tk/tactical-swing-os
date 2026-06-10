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
