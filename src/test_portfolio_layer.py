from __future__ import annotations

import pandas as pd

import build_portfolio_layer as portfolio


GENERATED_JST = "2026-06-09 12:00:00 JST"
GENERATED_UTC = "2026-06-09 03:00:00 UTC"


def test_normal_inputs_generate_portfolio_candidates():
    signals = pd.DataFrame(
        [
            {"asset": "WTI", "rank": "A", "side": "LONG", "signal_strength": 80, "date": "2026-06-09"},
            {"asset": "GOLD", "rank": "B", "side": "LONG", "signal_strength": 60, "date": "2026-06-09"},
        ]
    )
    evaluations = pd.DataFrame(
        [
            {"asset": "WTI", "r_multiple": 1.2, "outcome": "win_tp1"},
            {"asset": "WTI", "r_multiple": -1.0, "outcome": "loss_sl"},
            {"asset": "GOLD", "r_multiple": 0.5, "outcome": "win_tp1"},
        ]
    )
    candidates = portfolio.build_portfolio_candidates(
        pd.DataFrame(),
        signals,
        evaluations,
        pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
        GENERATED_JST,
    )
    wti = candidates[candidates["asset"] == "WTI"].iloc[0]
    assert len(candidates) == len(portfolio.ASSETS)
    assert wti["allocation_score"] > 40
    assert wti["portfolio_weight_candidate"] > 0
    assert candidates["portfolio_weight_candidate"].sum() <= 1.0
    assert bool(wti["requires_human_approval"]) is True
    assert bool(wti["weights_json_updated"]) is False
    assert bool(wti["orders_created"]) is False


def test_empty_inputs_fallback_does_not_fail():
    candidates = portfolio.build_portfolio_candidates(
        pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
        GENERATED_JST,
    )
    summary = portfolio.summary_from(
        candidates,
        {
            "market_snapshot_available": False,
            "signals_available": False,
            "latest_evaluations_available": False,
            "meta_learning_available": False,
            "auto_calibration_candidates_available": False,
            "human_override_analytics_available": False,
            "proposal_impact_available": False,
        },
        GENERATED_JST,
        GENERATED_UTC,
    )
    assert len(candidates) == len(portfolio.ASSETS)
    assert summary["portfolio_status"] == "active"
    assert summary["recommended_next_action"] == "generate_upstream_analysis"
    assert summary["requires_human_approval"] is True
    assert summary["patch_applied"] is False


def test_auto_calibration_and_human_override_affect_scores():
    auto = pd.DataFrame([{"asset": "BTC", "classification": "decrease", "confidence": 0.8}])
    overrides = pd.DataFrame([{"asset": "BTC", "override_type": "blocked", "impact_status": "negative", "impact_score": -1.0}])
    candidates = portfolio.build_portfolio_candidates(
        pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
        auto,
        overrides,
        pd.DataFrame(),
        GENERATED_JST,
    )
    btc = candidates[candidates["asset"] == "BTC"].iloc[0]
    assert btc["auto_calibration_score"] < 0
    assert btc["human_override_score"] < 0
    assert btc["risk_class"] == "high"


def test_summary_counts_are_consistent():
    candidates = pd.DataFrame(
        [
            {"asset": "BTC", "portfolio_weight_candidate": 0.25, "confidence": 0.7, "risk_class": "high", "risk_role": "offensive"},
            {"asset": "GOLD", "portfolio_weight_candidate": 0.20, "confidence": 0.6, "risk_class": "defensive", "risk_role": "defensive"},
            {"asset": "USDJPY", "portfolio_weight_candidate": 0.0, "confidence": 0.4, "risk_class": "medium", "risk_role": "balanced"},
        ]
    )
    summary = portfolio.summary_from(candidates, {"signals_available": True}, GENERATED_JST, GENERATED_UTC)
    assert summary["candidate_assets"] == 2
    assert summary["defensive_assets"] == 1
    assert summary["offensive_assets"] == 1
    assert summary["risk_concentration"] == 0.25
    assert summary["portfolio_concentration"] == 0.25
    assert summary["cash_candidate"] == 0.55


def test_proposal_impact_fallback_is_optional():
    impact = pd.DataFrame([{"asset": "NASDAQ", "impact_score": 0.8}])
    candidates = portfolio.build_portfolio_candidates(
        pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
        impact,
        GENERATED_JST,
    )
    nasdaq = candidates[candidates["asset"] == "NASDAQ"].iloc[0]
    assert nasdaq["proposal_impact_score"] > 0


def test_risk_concentration_tracks_high_risk_weight():
    candidates = pd.DataFrame(
        [
            {"asset": "BTC", "portfolio_weight_candidate": 0.20, "confidence": 0.7, "risk_class": "high", "risk_role": "offensive"},
            {"asset": "WTI", "portfolio_weight_candidate": 0.10, "confidence": 0.6, "risk_class": "high", "risk_role": "offensive"},
            {"asset": "GOLD", "portfolio_weight_candidate": 0.15, "confidence": 0.5, "risk_class": "defensive", "risk_role": "defensive"},
        ]
    )
    summary = portfolio.summary_from(candidates, {"signals_available": True}, GENERATED_JST, GENERATED_UTC)
    assert summary["risk_concentration"] == 0.30
