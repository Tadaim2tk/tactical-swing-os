"""jp_one_share_cost.py のユニットテスト。"""

from __future__ import annotations

import jp_one_share_cost as cost


def _unsourced_cfg() -> dict:
    return {
        "buy_rate": 0.0055,
        "buy_min_fee": 52.0,
        "sell_rate": 0.0055,
        "sell_min_fee": 52.0,
        "tax_rate": 0.0,
        "execution_lag_days": 1,
        "source": "unconfigured",
        "source_date": "",
        "source_type": "unconfigured",
        "responsibility": "",
        "sourced": False,
    }


def _sourced_cfg() -> dict:
    return {
        "buy_rate": 0.0055,
        "buy_min_fee": 52.0,
        "sell_rate": 0.0055,
        "sell_min_fee": 52.0,
        "tax_rate": 0.0,
        "execution_lag_days": 1,
        "source": "https://example.com/wankabu_fee",
        "source_date": "2026-06-01",
        "source_type": "published_spec",
        "responsibility": "test_user",
        "sourced": True,
    }


# ── is_sourced ──────────────────────────────────────────────────

def test_is_sourced_rejects_empty():
    assert not cost.is_sourced("")

def test_is_sourced_rejects_unconfigured():
    assert not cost.is_sourced("unconfigured")

def test_is_sourced_accepts_url():
    assert cost.is_sourced("https://example.com/fee")


# ── buy_commission ───────────────────────────────────────────────

def test_buy_commission_unsourced_returns_zero():
    cfg = _unsourced_cfg()
    assert cost.buy_commission(10000.0, 10, cfg) == 0.0

def test_buy_commission_rate_exceeds_min():
    # 10000 * 10 * 0.0055 = 550 > 52
    cfg = _sourced_cfg()
    assert cost.buy_commission(10000.0, 10, cfg) == 550.0

def test_buy_commission_min_fee_binding():
    # 3000 * 1 * 0.0055 = 16.5 < 52 → min fee 52
    cfg = _sourced_cfg()
    assert cost.buy_commission(3000.0, 1, cfg) == 52.0

def test_buy_commission_zero_shares():
    cfg = _sourced_cfg()
    assert cost.buy_commission(10000.0, 0, cfg) == 52.0  # min_fee applies even for 0 shares


# ── sell_commission ──────────────────────────────────────────────

def test_sell_commission_unsourced_returns_zero():
    cfg = _unsourced_cfg()
    assert cost.sell_commission(9000.0, 5, cfg) == 0.0

def test_sell_commission_rate_exceeds_min():
    cfg = _sourced_cfg()
    # 9000 * 5 * 0.0055 = 247.5 > 52
    assert abs(cost.sell_commission(9000.0, 5, cfg) - 247.5) < 1e-9

def test_sell_commission_min_fee_binding():
    # 2000 * 1 * 0.0055 = 11 < 52
    cfg = _sourced_cfg()
    assert cost.sell_commission(2000.0, 1, cfg) == 52.0


# ── min_fee_dominates ────────────────────────────────────────────

def test_min_fee_dominates_true_for_low_price():
    # 3000 * 0.0055 = 16.5 < 52
    cfg = _sourced_cfg()
    assert cost.min_fee_dominates(3000.0, cfg) is True

def test_min_fee_dominates_false_for_high_price():
    # 20000 * 0.0055 = 110 > 52
    cfg = _sourced_cfg()
    assert cost.min_fee_dominates(20000.0, cfg) is False

def test_min_fee_dominates_unsourced_returns_false():
    cfg = _unsourced_cfg()
    assert cost.min_fee_dominates(1000.0, cfg) is False


# ── net_r ────────────────────────────────────────────────────────

def test_net_r_unsourced_equals_gross():
    cfg = _unsourced_cfg()
    # risk = (5000-4500)*10 = 5000, gross = (5500-5000)*10 = 5000 → gross_r = 1.0
    g = cost.gross_r(5000.0, 5500.0, 4500.0, 10)
    n = cost.net_r(5000.0, 5500.0, 4500.0, 10, cfg)
    assert g == n == 1.0

def test_net_r_sourced_less_than_gross():
    cfg = _sourced_cfg()
    g = cost.gross_r(5000.0, 5500.0, 4500.0, 10)
    n = cost.net_r(5000.0, 5500.0, 4500.0, 10, cfg)
    assert n < g

def test_net_r_sl_equals_entry_returns_zero():
    cfg = _sourced_cfg()
    assert cost.net_r(5000.0, 5500.0, 5000.0, 10, cfg) == 0.0

def test_net_r_zero_shares_returns_zero():
    cfg = _sourced_cfg()
    assert cost.net_r(5000.0, 5500.0, 4500.0, 0, cfg) == 0.0


# ── effective_fee_rate ───────────────────────────────────────────

def test_effective_fee_rate_unsourced_returns_zero():
    cfg = _unsourced_cfg()
    assert cost.effective_fee_rate(5000.0, 10, cfg) == 0.0

def test_effective_fee_rate_high_price():
    cfg = _sourced_cfg()
    # 10000 * 10 = 100000 position, buy+sell = 550+550 = 1100 → 1.1%
    rate = cost.effective_fee_rate(10000.0, 10, cfg)
    assert abs(rate - 0.011) < 1e-6

def test_effective_fee_rate_low_price_dominated_by_min_fee():
    cfg = _sourced_cfg()
    # 2000 * 1 = 2000, buy_min=52 + sell_min=52 = 104 → 5.2%
    rate = cost.effective_fee_rate(2000.0, 1, cfg)
    assert abs(rate - 0.052) < 1e-6


# ── fee_viable ───────────────────────────────────────────────────

def test_fee_viable_unsourced_always_true():
    cfg = _unsourced_cfg()
    assert cost.fee_viable(5000.0, 1, 0.0, cfg) is True

def test_fee_viable_true_when_gain_exceeds_2x_cost():
    cfg = _sourced_cfg()
    # effective rate for 10000*10 = 1.1%, need gain_pct >= 2.2%
    assert cost.fee_viable(10000.0, 10, 5.0, cfg) is True

def test_fee_viable_false_when_gain_too_small():
    cfg = _sourced_cfg()
    # effective rate for 2000*1 = 5.2%, need >= 10.4% gain. 3% fails.
    assert cost.fee_viable(2000.0, 1, 3.0, cfg) is False


# ── lag_adjusted_edge ────────────────────────────────────────────

def test_lag_adjusted_edge_no_lag():
    r = cost.lag_adjusted_edge(5000.0, 5000.0, 5500.0, 4500.0)
    assert r["rr_now"] == r["rr_lag"]
    assert r["rr_degradation"] == 0.0
    assert r["lag_slippage_pct"] == 0.0

def test_lag_adjusted_edge_adverse_lag():
    # 仮説形成時5000、ラグ後5100に上昇してしまった（SL=4500, TP1=5500）
    r = cost.lag_adjusted_edge(5000.0, 5100.0, 5500.0, 4500.0)
    assert r["rr_lag"] < r["rr_now"]
    assert r["rr_degradation"] > 0.0
    assert r["lag_slippage_pct"] > 0.0

def test_lag_adjusted_edge_survives_marginal():
    # rr_lag < 1.5 なら edge_survives=False
    r = cost.lag_adjusted_edge(5000.0, 5300.0, 5500.0, 4500.0)
    assert not r["edge_survives"]


# ── validate_jp_cost_model ───────────────────────────────────────

def test_validate_no_issues_when_all_zero_unsourced():
    model = {
        "monex_wankabu": {
            "buy_rate": 0.0, "buy_min_fee": 0.0,
            "sell_rate": 0.0, "sell_min_fee": 0.0,
            "tax_rate": 0.0, "execution_lag_days": 1,
            "source": "unconfigured", "source_date": "", "source_type": "unconfigured",
            "responsibility": "",
        }
    }
    cost.reset_cache()
    issues = cost.validate_jp_cost_model(model)
    assert issues == []

# ── execution_lag_cost_jpy ───────────────────────────────────────

def test_execution_lag_cost_adverse():
    # 想定5000 → 実際5100、10株 → コスト = 1000円
    assert cost.execution_lag_cost_jpy(5000.0, 5100.0, 10) == 1000.0

def test_execution_lag_cost_favorable():
    # 想定5000 → 実際4950、10株 → -500円（有利方向）
    assert cost.execution_lag_cost_jpy(5000.0, 4950.0, 10) == -500.0

def test_execution_lag_cost_no_lag():
    assert cost.execution_lag_cost_jpy(5000.0, 5000.0, 10) == 0.0

def test_execution_lag_cost_zero_shares():
    assert cost.execution_lag_cost_jpy(5000.0, 5100.0, 0) == 0.0


def test_validate_flags_unsourced_nonzero():
    model = {
        "monex_wankabu": {
            "buy_rate": 0.0055, "buy_min_fee": 52.0,
            "sell_rate": 0.0055, "sell_min_fee": 52.0,
            "tax_rate": 0.0, "execution_lag_days": 1,
            "source": "unconfigured", "source_date": "", "source_type": "unconfigured",
            "responsibility": "",
        }
    }
    cost.reset_cache()
    issues = cost.validate_jp_cost_model(model)
    assert any(i["issue"] == "unsourced_nonzero_cost" for i in issues)
