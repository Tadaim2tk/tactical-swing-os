from __future__ import annotations

import pandas as pd

import track_proposal_adoption as adoption


def review_row(**overrides):
    base = {
        "proposal_id": "p1",
        "patch_id": "patch-1",
        "category": "asset",
        "target": "BTC",
        "weight_path": "asset_weights.BTC",
        "review_decision": "candidate",
        "sample_count": 12,
        "confidence_level": "medium",
        "proposal_strength": "moderate",
        "proposal_direction": "increase",
        "proposed_delta": 0.03,
        "patch_risk_level": "low",
        "evidence_quality": "moderate",
        "rationale": "test rationale",
    }
    base.update(overrides)
    return base


def test_candidate_review_becomes_pending_review_without_manual_decision():
    row = adoption.adoption_row(pd.Series(review_row()), pd.DataFrame(), "2026-06-09 12:00:00 JST")
    assert row["adoption_status"] == "pending_review"
    assert row["adoption_source"] == "derived_from_review"
    assert row["recommended_next_action"] == "manual_review"
    assert row["patch_applied"] is False
    assert row["weights_json_updated"] is False


def test_hold_review_becomes_held():
    row = adoption.adoption_row(pd.Series(review_row(review_decision="hold")), pd.DataFrame(), "2026-06-09 12:00:00 JST")
    assert row["adoption_status"] == "held"
    assert row["recommended_next_action"] == "wait_for_more_data"


def test_reject_and_blocked_reviews_become_terminal_states():
    rejected = adoption.adoption_row(pd.Series(review_row(review_decision="reject")), pd.DataFrame(), "2026-06-09 12:00:00 JST")
    blocked = adoption.adoption_row(pd.Series(review_row(review_decision="blocked")), pd.DataFrame(), "2026-06-09 12:00:00 JST")
    assert rejected["adoption_status"] == "rejected"
    assert blocked["adoption_status"] == "blocked"
    assert rejected["recommended_next_action"] == "no_action"
    assert blocked["recommended_next_action"] == "no_action"


def test_manual_decision_overrides_derived_status():
    decisions = pd.DataFrame(
        [
            {
                "proposal_id": "p1",
                "human_decision": "accepted",
                "human_decision_date": "2026-06-09",
                "decision_reason": "approved after review",
            }
        ]
    )
    row = adoption.adoption_row(pd.Series(review_row()), decisions, "2026-06-09 12:00:00 JST")
    assert row["adoption_status"] == "accepted"
    assert row["adoption_source"] == "manual"
    assert row["human_decision_recorded"] is True
    assert row["human_decision_date"] == "2026-06-09"


def test_summary_counts_are_correct():
    tracking = pd.DataFrame(
        [
            adoption.adoption_row(pd.Series(review_row(proposal_id="p1", review_decision="candidate")), pd.DataFrame(), "2026-06-09 12:00:00 JST"),
            adoption.adoption_row(pd.Series(review_row(proposal_id="p2", review_decision="hold")), pd.DataFrame(), "2026-06-09 12:00:00 JST"),
            adoption.adoption_row(pd.Series(review_row(proposal_id="p3", review_decision="reject")), pd.DataFrame(), "2026-06-09 12:00:00 JST"),
            adoption.adoption_row(pd.Series(review_row(proposal_id="p4", review_decision="blocked")), pd.DataFrame(), "2026-06-09 12:00:00 JST"),
        ]
    )
    summary = adoption.summary_from(tracking, {"review_status": "warning"}, "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC")
    assert summary["total_tracked_proposals"] == 4
    assert summary["pending_review_count"] == 1
    assert summary["held_count"] == 1
    assert summary["rejected_count"] == 1
    assert summary["blocked_count"] == 1
    assert summary["recommended_next_action"] == "manual_review"
    assert summary["requires_human_approval"] is True
    assert summary["weights_json_updated"] is False
    assert summary["patch_applied"] is False


def test_empty_tracking_is_unavailable():
    summary = adoption.summary_from(pd.DataFrame(columns=adoption.TRACKING_COLUMNS), {}, "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC")
    assert summary["tracking_status"] == "unavailable"
    assert summary["recommended_next_action"] == "no_action"
