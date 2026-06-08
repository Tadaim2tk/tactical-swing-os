from __future__ import annotations

import pandas as pd

import build_human_override_analytics as hoa


GENERATED_JST = "2026-06-09 12:00:00 JST"
GENERATED_UTC = "2026-06-09 03:00:00 UTC"


def adoption_row(**overrides):
    base = {
        "proposal_id": "p1",
        "review_decision": "hold",
        "adoption_status": "held",
        "tracking_reason": "held by review decision",
        "sample_count": 12,
        "confidence_level": "low",
    }
    base.update(overrides)
    return base


def impact_row(**overrides):
    base = {
        "proposal_id": "p1",
        "impact_score": 0.8,
        "sample_count": 12,
        "confidence_level": "medium",
    }
    base.update(overrides)
    return base


def test_override_type_mapping():
    assert hoa.override_type_from("", "accepted") == "accepted"
    assert hoa.override_type_from("candidate", "pending_review") == "held"
    assert hoa.override_type_from("reject", "") == "rejected"
    assert hoa.override_type_from("", "blocked") == "blocked"
    assert hoa.override_type_from("", "") == "unknown"


def test_normal_case_joins_adoption_and_impact():
    analytics = hoa.build_analytics_rows(
        pd.DataFrame([adoption_row(adoption_status="accepted", review_decision="candidate")]),
        pd.DataFrame(),
        pd.DataFrame([impact_row(impact_score=0.6)]),
        pd.DataFrame(),
        pd.DataFrame(),
        GENERATED_JST,
    )
    row = analytics.iloc[0]
    assert row["proposal_id"] == "p1"
    assert row["override_type"] == "accepted"
    assert row["impact_status"] == "positive"
    assert row["impact_score"] == 0.6
    assert bool(row["requires_human_approval"]) is True
    assert bool(row["patch_applied"]) is False
    assert bool(row["weights_json_updated"]) is False


def test_empty_inputs_summary_is_unavailable():
    analytics = hoa.build_analytics_rows(pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), GENERATED_JST)
    summary = hoa.summary_from(
        analytics,
        {
            "proposal_adoption_tracking_available": False,
            "weight_version_history_available": False,
            "proposal_impact_available": False,
            "meta_learning_available": False,
            "auto_calibration_candidates_available": False,
        },
        GENERATED_JST,
        GENERATED_UTC,
    )
    assert analytics.empty
    assert summary["analytics_status"] == "unavailable"
    assert summary["total_overrides"] == 0
    assert summary["recommended_next_action"] == "generate_adoption_tracking"
    assert summary["requires_human_approval"] is True


def test_missing_impact_marks_unknown_outcome():
    analytics = hoa.build_analytics_rows(
        pd.DataFrame([adoption_row(proposal_id="p2")]),
        pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
        GENERATED_JST,
    )
    row = analytics.iloc[0]
    assert row["impact_status"] == "unknown"
    assert row["impact_score"] == 0.0
    summary = hoa.summary_from(
        analytics,
        {
            "proposal_adoption_tracking_available": True,
            "weight_version_history_available": False,
            "proposal_impact_available": False,
            "meta_learning_available": False,
            "auto_calibration_candidates_available": False,
        },
        GENERATED_JST,
        GENERATED_UTC,
    )
    assert summary["unknown_outcome_count"] == 1
    assert summary["recommended_next_action"] == "wait_for_proposal_impact"


def test_missing_adoption_uses_weight_history_fallback():
    history = pd.DataFrame([{"proposal_id": "p3", "adoption_status": "blocked", "description": "blocked by review"}])
    analytics = hoa.build_analytics_rows(pd.DataFrame(), history, pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), GENERATED_JST)
    assert analytics.iloc[0]["source"] == "weight_version_history"
    assert analytics.iloc[0]["override_type"] == "blocked"


def test_missing_meta_learning_does_not_block_auto_fallback():
    auto = pd.DataFrame([{"proposal_id": "p4", "classification": "increase", "suggested_delta": 0.04}])
    analytics = hoa.build_analytics_rows(pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), auto, GENERATED_JST)
    row = analytics.iloc[0]
    assert row["source"] == "auto_calibration_candidates"
    assert row["override_type"] == "unknown"
    assert row["impact_status"] == "unknown"


def test_summary_counts_are_consistent():
    analytics = pd.DataFrame(
        [
            {"override_type": "accepted", "impact_status": "positive", "impact_score": 0.5},
            {"override_type": "held", "impact_status": "negative", "impact_score": -0.3},
            {"override_type": "rejected", "impact_status": "unknown", "impact_score": 0.0},
            {"override_type": "blocked", "impact_status": "unknown", "impact_score": 0.0},
        ]
    )
    summary = hoa.summary_from(
        analytics,
        {
            "proposal_adoption_tracking_available": True,
            "weight_version_history_available": False,
            "proposal_impact_available": True,
            "meta_learning_available": False,
            "auto_calibration_candidates_available": False,
        },
        GENERATED_JST,
        GENERATED_UTC,
    )
    assert summary["total_overrides"] == 4
    assert summary["accepted_count"] == 1
    assert summary["held_count"] == 1
    assert summary["rejected_count"] == 1
    assert summary["blocked_count"] == 1
    assert summary["positive_override_count"] == 1
    assert summary["negative_override_count"] == 1
    assert summary["unknown_outcome_count"] == 2
    assert summary["human_acceptance_rate"] == 0.25


def test_negative_impact_status():
    analytics = hoa.build_analytics_rows(
        pd.DataFrame([adoption_row(proposal_id="p5", adoption_status="held")]),
        pd.DataFrame(),
        pd.DataFrame([impact_row(proposal_id="p5", impact_score=-0.7)]),
        pd.DataFrame(),
        pd.DataFrame(),
        GENERATED_JST,
    )
    row = analytics.iloc[0]
    assert row["impact_status"] == "negative"
    assert row["override_type"] == "held"
