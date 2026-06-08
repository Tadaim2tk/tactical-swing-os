from __future__ import annotations

import pandas as pd

import propose_model_state_updates as msu


def test_sample_count_under_5_holds():
    direction, delta, limit, strength = msu.proposed_delta(sample_count=4, avg_r=1.0, win_rate=1.0)
    assert direction == "hold"
    assert delta == 0
    assert limit == 0
    assert strength == "none"


def test_good_performance_increases_after_10_samples():
    direction, delta, limit, strength = msu.proposed_delta(sample_count=10, avg_r=0.4, win_rate=0.7)
    assert direction == "increase"
    assert 0 < delta <= limit
    assert limit == 0.05
    assert strength in {"weak", "moderate", "strong"}


def test_bad_performance_decreases():
    direction, delta, limit, strength = msu.proposed_delta(sample_count=20, avg_r=-0.3, win_rate=0.35)
    assert direction == "decrease"
    assert -limit <= delta < 0
    assert limit == 0.08
    assert strength in {"weak", "moderate", "strong"}


def test_delta_never_exceeds_max_allowed_delta():
    for sample_count in [5, 9, 10, 19, 20, 50]:
        _, delta, limit, _ = msu.proposed_delta(sample_count=sample_count, avg_r=2.0, win_rate=1.0)
        assert abs(delta) <= limit


def test_missing_weight_defaults_to_one():
    current_weight, missing = msu.weight_lookup({}, "asset", "BTC")
    assert current_weight == 1.0
    assert missing is True


def test_make_proposal_never_applies_automatically():
    frame = pd.DataFrame(
        [
            {"outcome": "win_tp1", "r_multiple": 1.2, "missed_opportunity": False},
            {"outcome": "loss_sl", "r_multiple": -1.0, "missed_opportunity": False},
            {"outcome": "win_tp2", "r_multiple": 2.0, "missed_opportunity": False},
            {"outcome": "win_tp1", "r_multiple": 1.0, "missed_opportunity": False},
            {"outcome": "win_tp1", "r_multiple": 1.0, "missed_opportunity": False},
        ]
    )
    proposal = msu.make_proposal(
        generated_at_jst="2026-06-08 12:00:00 JST",
        category="asset",
        target="BTC",
        metric_group="asset",
        metrics=msu.metrics_from_frame(frame),
        weights={"asset_weights": {"BTC": 1.0}},
        evidence_source="test",
        proposal_type="asset_weight_adjustment",
    )
    assert proposal["apply_automatically"] is False
    assert proposal["missing_current_weight"] is False
