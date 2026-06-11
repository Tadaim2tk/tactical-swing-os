from __future__ import annotations

import pandas as pd

import build_meta_learning as meta


def impact_row(**overrides):
    base = {
        "proposal_id": "p1",
        "category": "asset",
        "target": "BTC",
        "adoption_status": "approved",
        "impact_score": 0.8,
        "win_rate_delta": 0.05,
        "sample_count": 12,
    }
    base.update(overrides)
    return base


def test_success_pattern_from_positive_impact():
    rows = meta.build_meta_rows(pd.DataFrame([impact_row()]), "2026-06-09 12:00:00 JST")
    assert rows.iloc[0]["pattern_type"] == "success_pattern"
    assert rows.iloc[0]["impact_direction"] == "positive"
    assert bool(rows.iloc[0]["apply_automatically"]) is False
    assert bool(rows.iloc[0]["weights_json_updated"]) is False
    assert bool(rows.iloc[0]["patch_applied"]) is False
    assert bool(rows.iloc[0]["requires_human_approval"]) is True


def test_failure_pattern_from_negative_impact():
    rows = meta.build_meta_rows(pd.DataFrame([impact_row(impact_score=-0.9, win_rate_delta=-0.1)]), "2026-06-09 12:00:00 JST")
    assert rows.iloc[0]["pattern_type"] == "failure_pattern"
    assert rows.iloc[0]["impact_direction"] == "negative"
    assert rows.iloc[0]["recommended_action"] == "avoid_or_review_pattern"


def test_insufficient_data_pattern():
    rows = meta.build_meta_rows(pd.DataFrame([impact_row(impact_score=2.0, sample_count=2)]), "2026-06-09 12:00:00 JST")
    assert rows.iloc[0]["pattern_type"] == "insufficient_data"
    assert rows.iloc[0]["confidence_level"] == "insufficient_data"


def test_missing_input_summary_is_unavailable_and_safe():
    rows = meta.build_meta_rows(pd.DataFrame(), "2026-06-09 12:00:00 JST")
    summary = meta.summary_from(rows, {}, "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC")
    assert summary["meta_learning_status"] == "unavailable"
    assert summary["proposal_impact_status"] == "unavailable"
    assert summary["total_candidates"] == 0
    assert summary["apply_automatically"] is False
    assert summary["weights_json_updated"] is False
    assert summary["patch_applied"] is False
    assert summary["requires_human_approval"] is True


def test_summary_payload_can_mark_proposal_impact_status():
    rows = meta.build_meta_rows(pd.DataFrame(), "2026-06-09 12:00:00 JST")
    summary = meta.summary_from(rows, {"impact_status": "unavailable"}, "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC")
    assert summary["proposal_impact_status"] == "unavailable"


def test_summary_counts_are_correct():
    rows = meta.build_meta_rows(
        pd.DataFrame(
            [
                impact_row(proposal_id="p1", impact_score=0.8, win_rate_delta=0.04, sample_count=12),
                impact_row(proposal_id="p2", impact_score=-0.8, win_rate_delta=-0.04, sample_count=12),
                impact_row(proposal_id="p3", impact_score=0.1, win_rate_delta=0.0, sample_count=12),
                impact_row(proposal_id="p4", impact_score=1.0, win_rate_delta=0.2, sample_count=2),
            ]
        ),
        "2026-06-09 12:00:00 JST",
    )
    summary = meta.summary_from(rows, {"impact_status": "active"}, "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC")
    assert summary["meta_learning_status"] == "active"
    assert summary["success_pattern_count"] == 1
    assert summary["failure_pattern_count"] == 1
    assert summary["neutral_pattern_count"] == 1
    assert summary["insufficient_data_count"] >= 1
    assert summary["recommended_next_action"] == "human_review"
