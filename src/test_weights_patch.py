from __future__ import annotations

import pandas as pd

import build_weights_patch as wp


def proposal(**overrides):
    base = {
        "proposal_id": "p1",
        "category": "asset",
        "target": "BTC",
        "sample_count": 10,
        "confidence_level": "medium",
        "proposal_direction": "increase",
        "proposal_strength": "moderate",
        "proposed_delta": 0.03,
        "max_allowed_delta": 0.05,
        "apply_automatically": False,
        "rationale": "test rationale",
    }
    base.update(overrides)
    return base


def audit_item(proposal_id="p1", result="passed"):
    return {"proposal_id": proposal_id, "audit_result": result}


def test_audit_status_blocked_generates_no_patches():
    patches, excluded = wp.build_patch_rows(
        pd.DataFrame([proposal()]),
        pd.DataFrame([audit_item()]),
        {"asset_weights": {"BTC": 1.0}},
        "2026-06-08 12:00:00 JST",
        "blocked",
    )
    assert patches.empty
    assert excluded.iloc[0]["exclusion_reason"] == "audit_status_blocked"


def test_apply_automatically_true_is_excluded():
    row = pd.Series(proposal(apply_automatically=True))
    assert wp.exclusion_reason(row, "passed", "passed") == "apply_automatically_true"


def test_insufficient_data_is_excluded():
    row = pd.Series(proposal(confidence_level="insufficient_data"))
    assert wp.exclusion_reason(row, "passed", "passed") == "insufficient_data"


def test_hold_proposal_is_excluded():
    row = pd.Series(proposal(proposal_direction="hold"))
    assert wp.exclusion_reason(row, "passed", "passed") == "proposal_direction_not_increase_or_decrease"


def test_low_sample_is_excluded():
    row = pd.Series(proposal(sample_count=4))
    assert wp.exclusion_reason(row, "passed", "passed") == "sample_count_under_5"


def test_eligible_increase_decrease_only_become_patches():
    proposals = pd.DataFrame(
        [
            proposal(proposal_id="p1", proposal_direction="increase", proposed_delta=0.03),
            proposal(proposal_id="p2", proposal_direction="decrease", proposed_delta=-0.03),
            proposal(proposal_id="p3", proposal_direction="hold", proposed_delta=0.0),
        ]
    )
    audit = pd.DataFrame([audit_item("p1"), audit_item("p2"), audit_item("p3")])
    patches, excluded = wp.build_patch_rows(proposals, audit, {"asset_weights": {"BTC": 1.0}}, "2026-06-08 12:00:00 JST", "passed")
    assert len(patches) == 2
    assert len(excluded) == 1
    assert set(patches["proposal_direction"]) == {"increase", "decrease"}


def test_proposed_value_is_clipped_between_point_5_and_1_point_5():
    patch = wp.make_patch(
        pd.Series(proposal(proposed_delta=0.8, max_allowed_delta=1.0)),
        {"asset_weights": {"BTC": 1.0}},
        "2026-06-08 12:00:00 JST",
        "passed",
    )
    assert patch["proposed_value"] == 1.5
    assert patch["unclipped_proposed_value"] == 1.8
    assert patch["clipped"] is True


def test_missing_weight_adds_key_proposal():
    patch = wp.make_patch(pd.Series(proposal(target="GOLD")), {}, "2026-06-08 12:00:00 JST", "passed")
    assert patch["current_weight"] == 1.0
    assert patch["patch_action"] == "add_key_proposal"


def test_safety_flags_are_always_false_or_human_required():
    patches, payload, _ = wp.build_weights_patch()
    assert payload["safety"]["weights_json_updated"] is False
    assert payload["safety"]["patch_applied"] is False
    assert payload["safety"]["requires_human_approval"] is True
    assert payload["safety"]["apply_automatically"] is False
