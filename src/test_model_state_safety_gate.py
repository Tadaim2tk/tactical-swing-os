from __future__ import annotations

import pandas as pd

import audit_model_state_proposals as audit


def proposal(**overrides):
    base = {
        "proposal_id": "p1",
        "category": "asset",
        "target": "BTC",
        "sample_count": 20,
        "confidence_level": "high",
        "proposal_direction": "hold",
        "proposal_strength": "none",
        "proposed_delta": 0.0,
        "max_allowed_delta": 0.08,
        "apply_automatically": False,
    }
    base.update(overrides)
    return base


def test_apply_automatically_true_is_critical_blocked():
    result = audit.audit_one(pd.Series(proposal(apply_automatically=True)))
    assert result["audit_result"] == "blocked"
    assert result["severity"] == "critical"
    assert "automatic_application_not_allowed" in result["reason"]


def test_delta_exceeds_max_allowed_is_blocked():
    result = audit.audit_one(pd.Series(proposal(proposed_delta=0.2, max_allowed_delta=0.08)))
    assert result["audit_result"] == "blocked"
    assert result["severity"] == "high"
    assert "delta_exceeds_max_allowed" in result["reason"]


def test_insufficient_data_with_non_hold_is_blocked():
    result = audit.audit_one(
        pd.Series(
            proposal(
                sample_count=3,
                confidence_level="insufficient_data",
                proposal_direction="increase",
                proposed_delta=0.01,
                max_allowed_delta=0.03,
            )
        )
    )
    assert result["audit_result"] == "blocked"
    assert "insufficient_data_with_non_hold_proposal" in result["reason"]


def test_strong_with_low_sample_is_warning():
    result = audit.audit_one(
        pd.Series(
            proposal(
                sample_count=6,
                confidence_level="low",
                proposal_direction="increase",
                proposal_strength="strong",
                proposed_delta=0.02,
                max_allowed_delta=0.03,
            )
        )
    )
    assert result["audit_result"] == "warning"
    assert "weak_evidence_marked_strong" in result["reason"]


def test_safe_proposal_passes():
    result = audit.audit_one(pd.Series(proposal()))
    assert result["audit_result"] == "passed"
    assert result["severity"] == "low"
    assert result["reason"] == "safe_proposal"


def test_payload_never_updates_weights_json():
    audited = audit.audit_proposals(pd.DataFrame([proposal()]))
    payload = audit.build_payload(audited, "json", "2026-06-08 12:00:00 JST", "2026-06-08 03:00:00 UTC")
    assert payload["weights_json_updated"] is False
    assert payload["requires_human_review"] is True
