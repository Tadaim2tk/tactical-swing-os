from __future__ import annotations

from unittest.mock import patch

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


def test_markdown_table_returns_string_for_dataframe():
    table = msu.markdown_table(pd.DataFrame([{"asset": "BTC", "avg_r": 0.5}]))
    assert isinstance(table, str)
    assert "BTC" in table


def test_markdown_table_falls_back_without_tabulate():
    frame = pd.DataFrame([{"note": "alpha|beta\nnext", "avg_r": 0.5}])
    with patch.object(pd.DataFrame, "to_markdown", side_effect=ImportError("tabulate missing")):
        table = msu.markdown_table(frame)
    assert "| note | avg_r |" in table
    assert "alpha/beta next" in table


def test_markdown_table_empty_dataframe_returns_data_missing():
    assert msu.markdown_table(pd.DataFrame()) == "データなし"


def test_render_markdown_survives_without_tabulate():
    proposals = pd.DataFrame(
        [
            {
                "generated_at_jst": "2026-06-08 12:00:00 JST",
                "proposal_id": "p1",
                "category": "asset",
                "target": "BTC",
                "metric_group": "asset",
                "sample_count": 10,
                "win_rate": 0.7,
                "avg_r": 0.4,
                "total_r": 4.0,
                "missed_opportunity_rate": 0.0,
                "no_entry_rate": 0.0,
                "confidence_level": "medium",
                "current_weight": 1.0,
                "proposed_weight": 1.03,
                "proposed_delta": 0.03,
                "max_allowed_delta": 0.05,
                "proposal_direction": "increase",
                "proposal_strength": "moderate",
                "rationale": "test rationale",
                "evidence_source": "test",
                "apply_automatically": False,
                "missing_current_weight": False,
            }
        ]
    )
    payload = {
        "generated_at_jst": "2026-06-08 12:00:00 JST",
        "data_source": {"evaluations": "latest_evaluations"},
        "summary": {
            "total_proposals": 1,
            "increase_count": 1,
            "decrease_count": 0,
            "hold_count": 0,
            "insufficient_data_count": 0,
        },
    }
    with patch.object(pd.DataFrame, "to_markdown", side_effect=ImportError("tabulate missing")):
        report = msu.render_markdown(payload, proposals)
    assert "# Model State Update Proposals" in report
    assert "test rationale" in report
