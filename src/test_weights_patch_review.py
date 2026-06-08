from __future__ import annotations

import pandas as pd

import review_weights_patch as review


def patch(**overrides):
    base = {
        "patch_id": "patch-1",
        "proposal_id": "p1",
        "category": "asset",
        "target": "BTC",
        "weight_path": "asset_weights.BTC",
        "patch_action": "update_key_proposal",
        "current_weight": 1.0,
        "proposed_delta": 0.03,
        "proposed_value": 1.03,
        "sample_count": 12,
        "confidence_level": "medium",
        "proposal_strength": "moderate",
        "proposal_direction": "increase",
        "max_allowed_delta": 0.05,
        "audit_result": "passed",
        "apply_automatically": False,
        "patch_applied": False,
        "rationale": "test rationale",
    }
    base.update(overrides)
    return base


def test_audit_status_blocked_marks_all_patches_blocked():
    result = review.evaluate_patch(patch(), "blocked")
    assert result["review_decision"] == "blocked"
    assert result["recommended_human_action"] == "reject"
    assert "安全監査がblocked" in result["review_reason"]


def test_weak_low_sample_patch_is_hold():
    result = review.evaluate_patch(
        patch(sample_count=6, confidence_level="low", proposal_strength="weak"),
        "passed",
    )
    assert result["review_decision"] == "hold"
    assert result["recommended_human_action"] == "wait_for_more_data"
    assert result["evidence_quality"] == "weak"


def test_moderate_sufficient_patch_is_candidate():
    result = review.evaluate_patch(patch(), "passed")
    assert result["review_decision"] == "candidate"
    assert result["recommended_human_action"] == "approve_later"
    assert result["minimum_conditions_met"] is True


def test_patch_applied_true_is_blocked():
    result = review.evaluate_patch(patch(patch_applied=True), "passed")
    assert result["review_decision"] == "blocked"
    assert result["recommended_human_action"] == "reject"
    assert result["patch_applied"] is False
    assert "patch_applied_true_is_not_allowed" in result["review_reason"]


def test_non_positive_proposed_value_is_rejected():
    result = review.evaluate_patch(patch(proposed_value=0), "passed")
    assert result["review_decision"] == "reject"
    assert result["recommended_human_action"] == "reject"
    assert "proposed_weight_or_value_invalid" in result["review_reason"]


def test_summary_counts_are_correct():
    review_df = pd.DataFrame(
        [
            review.evaluate_patch(patch(patch_id="p1"), "passed"),
            review.evaluate_patch(patch(patch_id="p2", sample_count=6, proposal_strength="weak"), "passed"),
            review.evaluate_patch(patch(patch_id="p3", proposed_delta=0), "passed"),
            review.evaluate_patch(patch(patch_id="p4"), "blocked"),
        ]
    )
    summary = review.build_summary(review_df, "passed", True, "2026-06-08 12:00:00 JST", "2026-06-08 03:00:00 UTC")
    assert summary["candidate_count"] == 1
    assert summary["hold_count"] == 1
    assert summary["reject_count"] == 1
    assert summary["blocked_count"] == 1
    assert summary["requires_human_approval"] is True
    assert summary["weights_json_updated"] is False
    assert summary["patch_applied"] is False


def test_unavailable_summary_when_inputs_missing():
    summary = review.build_summary(
        pd.DataFrame(columns=review.REVIEW_COLUMNS),
        "unavailable",
        False,
        "2026-06-08 12:00:00 JST",
        "2026-06-08 03:00:00 UTC",
    )
    assert summary["review_status"] == "unavailable"
    assert summary["recommended_next_action"] == "no_action"
