from __future__ import annotations

import pandas as pd

import build_auto_calibration_candidates as auto


GENERATED_JST = "2026-06-09 12:00:00 JST"
GENERATED_UTC = "2026-06-09 03:00:00 UTC"


def meta_row(**overrides):
    base = {
        "meta_learning_id": "ml1",
        "proposal_id": "p1",
        "pattern_type": "success_pattern",
        "category": "asset",
        "target": "WTI",
        "impact_score": 0.8,
        "impact_direction": "positive",
        "sample_count": 18,
        "confidence_level": "medium",
        "learning_hypothesis": "WTI positive pattern",
    }
    base.update(overrides)
    return base


def test_meta_learning_success_generates_increase_candidate():
    candidates = auto.build_candidates(pd.DataFrame([meta_row()]), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), GENERATED_JST)
    row = candidates.iloc[0]
    assert row["asset"] == "WTI"
    assert row["factor"] == "asset_weight"
    assert row["classification"] == "increase"
    assert row["suggested_value"] > row["current_value"]
    assert row["confidence"] > 0
    assert bool(row["requires_human_approval"]) is True
    assert bool(row["patch_applied"]) is False
    assert bool(row["weights_json_updated"]) is False
    assert bool(row["generate_signal_updated"]) is False


def test_meta_learning_failure_generates_decrease_candidate():
    candidates = auto.build_candidates(
        pd.DataFrame([meta_row(pattern_type="failure_pattern", impact_direction="negative", impact_score=-0.9)]),
        pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
        GENERATED_JST,
    )
    row = candidates.iloc[0]
    assert row["classification"] == "decrease"
    assert row["suggested_value"] < row["current_value"]


def test_empty_inputs_generate_unavailable_summary():
    candidates = auto.build_candidates(pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), GENERATED_JST)
    summary = auto.summary_from(
        candidates,
        {
            "meta_learning_available": False,
            "proposal_impact_available": False,
            "proposal_adoption_tracking_available": False,
            "weight_version_history_available": False,
        },
        GENERATED_JST,
        GENERATED_UTC,
    )
    assert candidates.empty
    assert summary["candidate_status"] == "unavailable"
    assert summary["candidate_count"] == 0
    assert summary["recommended_next_action"] == "generate_meta_learning_or_proposal_impact"
    assert summary["requires_human_approval"] is True
    assert summary["patch_applied"] is False


def test_missing_meta_uses_proposal_impact_fallback():
    impact = pd.DataFrame(
        [
            {
                "proposal_id": "impact-1",
                "category": "rank",
                "target": "A",
                "impact_score": 0.7,
                "sample_count": 12,
            }
        ]
    )
    candidates = auto.build_candidates(pd.DataFrame(), impact, pd.DataFrame(), pd.DataFrame(), GENERATED_JST)
    row = candidates.iloc[0]
    assert row["source"] == "proposal_impact"
    assert row["factor"] == "rank_weight"
    assert row["classification"] == "increase"


def test_missing_impact_uses_adoption_hold_fallback():
    adoptions = pd.DataFrame([{"proposal_id": "adopt-1", "adoption_status": "held"}])
    candidates = auto.build_candidates(pd.DataFrame(), pd.DataFrame(), adoptions, pd.DataFrame(), GENERATED_JST)
    row = candidates.iloc[0]
    assert row["source"] == "proposal_adoption_tracking"
    assert row["classification"] == "hold"
    assert row["suggested_delta"] == 0.0


def test_blocked_fallback_classification():
    history = pd.DataFrame([{"proposal_id": "hist-1", "adoption_status": "blocked"}])
    candidates = auto.build_candidates(pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), history, GENERATED_JST)
    assert candidates.iloc[0]["classification"] == "blocked"


def test_insufficient_data_classification():
    candidates = auto.build_candidates(pd.DataFrame([meta_row(sample_count=2)]), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), GENERATED_JST)
    row = candidates.iloc[0]
    assert row["classification"] == "insufficient_data"
    assert row["suggested_value"] == 1.0


def test_summary_counts_match_candidates():
    candidates = pd.DataFrame(
        [
            {"classification": "increase"},
            {"classification": "decrease"},
            {"classification": "hold"},
            {"classification": "insufficient_data"},
            {"classification": "blocked"},
        ]
    )
    summary = auto.summary_from(
        candidates,
        {
            "meta_learning_available": True,
            "proposal_impact_available": False,
            "proposal_adoption_tracking_available": False,
            "weight_version_history_available": False,
        },
        GENERATED_JST,
        GENERATED_UTC,
    )
    assert summary["candidate_count"] == 5
    assert summary["increase_count"] == 1
    assert summary["decrease_count"] == 1
    assert summary["hold_count"] == 1
    assert summary["insufficient_data_count"] == 1
    assert summary["blocked_count"] == 1
    assert summary["recommended_next_action"] == "human_review"


def test_suggested_value_is_clipped():
    assert auto.suggested_delta("increase", 10.0, 10.0) <= 0.10
    row = auto.candidate_row_from_meta(pd.Series(meta_row(impact_score=100.0, confidence_level="high", sample_count=100)), GENERATED_JST, 1)
    assert 0.50 <= row["suggested_value"] <= 1.50
