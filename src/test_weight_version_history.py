from __future__ import annotations

import pandas as pd

import build_weight_version_history as history


def adoption_row(**overrides):
    base = {
        "proposal_id": "p1",
        "review_decision": "candidate",
        "adoption_status": "pending_review",
        "tracking_reason": "candidate requires human adoption decision",
        "weights_json_updated": False,
        "patch_applied": False,
    }
    base.update(overrides)
    return base


def test_build_history_rows_from_adoption_tracking():
    adoptions = pd.DataFrame(
        [
            adoption_row(proposal_id="p1", adoption_status="pending_review"),
            adoption_row(proposal_id="p2", adoption_status="held"),
            adoption_row(proposal_id="p3", adoption_status="accepted"),
            adoption_row(proposal_id="p4", adoption_status="rejected"),
            adoption_row(proposal_id="p5", adoption_status="blocked"),
        ]
    )
    rows = history.build_history_rows(adoptions, pd.DataFrame(), pd.DataFrame(), "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC")
    assert list(rows["adoption_status"]) == ["candidate", "held", "approved", "rejected", "blocked"]
    assert set(rows["version_id"]) == {"v1"}
    assert rows["weights_json_updated"].eq(False).all()
    assert rows["patch_applied"].eq(False).all()
    assert rows["requires_human_approval"].eq(True).all()


def test_missing_inputs_create_empty_history_and_unavailable_summary():
    rows = history.build_history_rows(pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC")
    summary = history.summary_from(rows, {}, {}, {}, "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC")
    assert rows.empty
    assert summary["current_version"] == "v1"
    assert summary["version_count"] == 1
    assert summary["review_status"] == "unavailable"
    assert summary["history_status"] == "unavailable"
    assert summary["weights_json_updated"] is False
    assert summary["patch_applied"] is False
    assert summary["requires_human_approval"] is True


def test_review_unavailable_status_is_preserved():
    rows = history.build_history_rows(pd.DataFrame([adoption_row()]), pd.DataFrame(), pd.DataFrame(), "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC")
    summary = history.summary_from(rows, {"review_status": "unavailable"}, {}, {}, "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC")
    assert summary["review_status"] == "unavailable"
    assert summary["candidate_count"] == 1


def test_summary_counts_match_history_rows():
    rows = pd.DataFrame(
        [
            history.history_row(pd.Series(adoption_row(proposal_id="p1", adoption_status="pending_review")), "proposal_adoption_tracking", "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC"),
            history.history_row(pd.Series(adoption_row(proposal_id="p2", adoption_status="held")), "proposal_adoption_tracking", "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC"),
            history.history_row(pd.Series(adoption_row(proposal_id="p3", adoption_status="accepted")), "proposal_adoption_tracking", "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC"),
            history.history_row(pd.Series(adoption_row(proposal_id="p4", adoption_status="rejected")), "proposal_adoption_tracking", "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC"),
            history.history_row(pd.Series(adoption_row(proposal_id="p5", adoption_status="blocked")), "proposal_adoption_tracking", "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC"),
            history.history_row(pd.Series(adoption_row(proposal_id="p6", adoption_status="superseded")), "proposal_adoption_tracking", "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC"),
        ]
    )
    summary = history.summary_from(rows, {}, {"review_status": "passed"}, {}, "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC")
    assert summary["tracked_count"] == 1
    assert summary["held_count"] == 1
    assert summary["candidate_count"] == 1
    assert summary["approved_count"] == 1
    assert summary["rejected_count"] == 1
    assert summary["blocked_count"] == 1
    assert summary["total_history_records"] == 6


def test_review_and_model_state_fallbacks():
    review = pd.DataFrame([{"proposal_id": "review-1", "review_decision": "hold", "review_reason": "needs more evidence"}])
    review_rows = history.build_history_rows(pd.DataFrame(), review, pd.DataFrame(), "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC")
    assert review_rows.iloc[0]["source"] == "weights_patch_review"
    assert review_rows.iloc[0]["adoption_status"] == "held"

    proposals = pd.DataFrame([{"proposal_id": "model-1", "proposal_direction": "increase", "confidence_level": "medium"}])
    proposal_rows = history.build_history_rows(pd.DataFrame(), pd.DataFrame(), proposals, "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC")
    assert proposal_rows.iloc[0]["source"] == "model_state_update_proposals"
    assert proposal_rows.iloc[0]["adoption_status"] == "tracked"
