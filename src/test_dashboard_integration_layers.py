"""統合フェーズで追加した4レイヤーのDashboardサマリー関数の単体テスト。

分析・表示専用であり、実売買/発注/weights更新は一切しないことを併せて検証する。
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import build_dashboard as bd


# === Prediction Calibration ===

def test_prediction_calibration_summary_from_json():
    payload = {
        "calibration_status": "tracking",
        "implied_probability_source": "frozen_default",
        "ranks_tracked": 3,
        "overconfident_count": 1,
        "underconfident_count": 0,
        "well_calibrated_count": 2,
        "insufficient_data_count": 0,
        "overall_brier": 0.21,
        "reference_brier": 0.25,
        "brier_skill_score": 0.16,
        "scored_n": 42,
        "requires_human_approval": True,
        "weights_json_updated": False,
    }
    s = bd.prediction_calibration_summary(payload, pd.DataFrame())
    assert s["available"] is True
    assert s["calibration_status"] == "tracking"
    assert s["scored_n"] == 42
    assert s["weights_json_updated"] is False  # 安全条件: weights更新なし


def test_prediction_calibration_summary_unavailable():
    s = bd.prediction_calibration_summary(None, pd.DataFrame())
    assert s["available"] is False
    assert s["calibration_status"] == "unavailable"


# === Narrative Reliability ===

def test_narrative_reliability_summary_from_json():
    payload = {
        "narrative_reliability_status": "tracking",
        "narrative_source": "signal_narrative_alignment",
        "total_narratives": 4,
        "strong_positive_count": 1,
        "strong_negative_count": 0,
        "unproven_count": 3,
        "insufficient_data_count": 0,
        "decay_divergence_count": 1,
        "requires_human_approval": True,
        "weights_json_updated": False,
    }
    s = bd.narrative_reliability_summary(payload, pd.DataFrame())
    assert s["available"] is True
    assert s["total_narratives"] == 4
    assert s["weights_json_updated"] is False


def test_narrative_reliability_summary_unavailable():
    s = bd.narrative_reliability_summary({}, pd.DataFrame())
    assert s["available"] is False


# === Transaction Cost ===

def test_transaction_cost_summary_unconfigured_warns():
    cost_model_json = {
        "_meta": {"status": "unconfigured"},
        "default": {"source": "unconfigured"},
        "assets": {"BTC": {"source": "unconfigured"}},
    }
    evals = pd.DataFrame({
        "r_result": [1.0, -1.0],
        "r_result_net": [1.0, -1.0],
        "cost_r": [0.0, 0.0],
        "cost_source": ["unconfigured", "unconfigured"],
    })
    s = bd.transaction_cost_summary(evals, cost_model_json)
    assert s["cost_model_status"] == "unconfigured"
    assert s["net_r_available"] is True
    assert s["gross_r_available"] is True
    assert s["cost_adjusted_rows"] == 0
    assert s["configured_asset_count"] == 0
    assert s["warning"]  # 未設定の警告が出る


def test_transaction_cost_summary_configured():
    cost_model_json = {
        "_meta": {"status": "configured"},
        "default": {"source": "broker_x"},
        "assets": {"BTC": {"source": "broker_x"}, "WTI": {"source": "unconfigured"}},
    }
    evals = pd.DataFrame({
        "r_result": [1.0, -1.0],
        "r_result_net": [0.8, -1.2],
        "cost_r": [0.2, 0.2],
        "cost_source": ["broker_x", "broker_x"],
    })
    s = bd.transaction_cost_summary(evals, cost_model_json)
    assert s["configured_asset_count"] == 1
    assert s["cost_adjusted_rows"] == 2
    assert s["warning"] == ""  # 設定済みなら警告なし


def test_transaction_cost_summary_empty_evaluations():
    s = bd.transaction_cost_summary(pd.DataFrame(), {"_meta": {"status": "unconfigured"}})
    assert s["available"] is True
    assert s["net_r_available"] is False


# === Audit Report ===

def test_audit_report_summary_pass():
    s = bd.audit_report_summary("PASS")
    assert s["available"] is True
    assert s["latest_audit_status"] == "PASS"
    assert s["audit_report_available"] is True


def test_audit_report_summary_empty():
    s = bd.audit_report_summary("")
    assert s["available"] is False
    assert s["latest_audit_status"] == "unavailable"


# === Narrative Lookahead Audit ===

def test_narrative_lookahead_summary_from_json():
    payload = {
        "audit_status": "warning",
        "total_checked": 10,
        "passed_count": 7,
        "warning_count": 2,
        "high_risk_count": 1,
        "blocked_count": 0,
        "unavailable_count": 0,
        "unknown_timing_count": 3,
        "max_lookahead_score": 50,
        "recommended_next_action": "時間軸の人間確認を推奨",
        "requires_human_approval": True,
        "weights_json_updated": False,
        "generate_signal_updated": False,
    }
    s = bd.narrative_lookahead_summary(payload, pd.DataFrame())
    assert s["available"] is True
    assert s["audit_status"] == "warning"
    assert s["high_risk_count"] == 1
    assert s["weights_json_updated"] is False
    assert s["generate_signal_updated"] is False


def test_narrative_lookahead_summary_unavailable():
    s = bd.narrative_lookahead_summary(None, pd.DataFrame())
    assert s["available"] is False
    assert s["audit_status"] == "unavailable"


# === Adversarial Review ===

def test_adversarial_review_summary_from_json():
    payload = {
        "review_status": "high_risk",
        "total_sources_checked": 5,
        "total_findings": 3,
        "warning_count": 1,
        "high_risk_count": 2,
        "blocked_count": 0,
        "contradiction_count": 1,
        "auto_apply_violation_count": 2,
        "weights_update_violation_count": 0,
        "max_severity": "high_risk",
        "recommended_next_action": "高リスク提案あり",
        "requires_human_approval": True,
        "weights_json_updated": False,
        "generate_signal_updated": False,
    }
    s = bd.adversarial_review_summary(payload, pd.DataFrame())
    assert s["available"] is True
    assert s["review_status"] == "high_risk"
    assert s["auto_apply_violation_count"] == 2
    assert s["weights_json_updated"] is False
    assert s["generate_signal_updated"] is False


def test_adversarial_review_summary_unavailable():
    s = bd.adversarial_review_summary(None, pd.DataFrame())
    assert s["available"] is False
    assert s["review_status"] == "unavailable"


# === Phase 26: Transaction Cost 証拠フレーム表示 ===

def test_transaction_cost_summary_unsourced_nonzero_flagged():
    cost_model_json = {
        "_meta": {"status": "unconfigured"},
        "default": {"source": "unconfigured"},
        "assets": {
            "BTC": {"spread": 200.0, "commission_round_turn": 0.0, "swap_per_bar": 0.0, "source": "unconfigured"},  # unsourced non-zero
            "GOLD": {"spread": 0.0, "commission_round_turn": 0.0, "swap_per_bar": 0.0, "source": "unconfigured"},
        },
    }
    s = bd.transaction_cost_summary(pd.DataFrame(), cost_model_json)
    assert s["unsourced_nonzero_count"] == 1
    assert "証拠主義違反" in s["warning"]
    assert s["configured_asset_count"] == 0


def test_transaction_cost_summary_configured_sources_listed():
    cost_model_json = {
        "_meta": {"status": "configured"},
        "default": {"source": "unconfigured"},
        "assets": {
            "BTC": {"spread": 200.0, "commission_round_turn": 0.0, "swap_per_bar": 0.0,
                    "source": "XM spec", "source_date": "2026-06-16", "responsibility": "maru"},
        },
    }
    s = bd.transaction_cost_summary(pd.DataFrame(), cost_model_json)
    assert s["configured_asset_count"] == 1
    assert s["unsourced_nonzero_count"] == 0
    assert s["missing_provenance_count"] == 0
    assert any("XM spec" in src and "2026-06-16" in src for src in s["configured_sources"])


def test_transaction_cost_summary_missing_provenance_counted():
    cost_model_json = {
        "_meta": {"status": "configured"},
        "default": {"source": "unconfigured"},
        "assets": {
            "BTC": {"spread": 1.0, "commission_round_turn": 0.0, "swap_per_bar": 0.0, "source": "XM spec"},  # no date/responsibility
        },
    }
    s = bd.transaction_cost_summary(pd.DataFrame(), cost_model_json)
    assert s["configured_asset_count"] == 1
    assert s["missing_provenance_count"] == 1


# === セルフ監査(major/minor)の追補: 語彙一致・provenance ===

def test_transaction_cost_summary_placeholder_source_is_unsourced():
    j = {"_meta": {"status": "unconfigured"}, "default": {"source": "unconfigured"},
         "assets": {"BTC": {"spread": 5.0, "source": "placeholder"}}}  # placeholder=未出典
    s = bd.transaction_cost_summary(pd.DataFrame(), j)
    assert s["configured_asset_count"] == 0
    assert s["unsourced_nonzero_count"] == 1


def test_transaction_cost_summary_whitespace_mixedcase_source_is_configured():
    j = {"_meta": {"status": "configured"}, "default": {"source": "unconfigured"},
         "assets": {"BTC": {"spread": 5.0, "source": "  XM Spec  ", "source_date": "2026-06-16", "responsibility": "tk"}}}
    s = bd.transaction_cost_summary(pd.DataFrame(), j)
    assert s["configured_asset_count"] == 1
    assert s["unsourced_nonzero_count"] == 0
    assert s["missing_provenance_count"] == 0


def test_transaction_cost_summary_missing_responsibility_only_counts():
    j = {"_meta": {"status": "configured"}, "default": {"source": "unconfigured"},
         "assets": {"BTC": {"spread": 1.0, "source": "XM spec", "source_date": "2026-06-16", "responsibility": ""}}}
    s = bd.transaction_cost_summary(pd.DataFrame(), j)
    assert s["missing_provenance_count"] == 1


def test_transaction_cost_summary_default_source_normalized():
    # 未出典の default(placeholder)は "unconfigured" として表示
    j = {"_meta": {"status": "unconfigured"}, "default": {"source": "placeholder"}, "assets": {}}
    s = bd.transaction_cost_summary(pd.DataFrame(), j)
    assert s["default_source"] == "unconfigured"


def test_transaction_cost_summary_unsourced_asset_not_counted_as_configured():
    # ダッシュボードも cost_model と同じく、自前sourceの無いアセットは configured にしない
    j = {"_meta": {"status": "configured"},
         "default": {"source": "XM_house", "source_date": "2026-01-01", "responsibility": "tk"},
         "assets": {"USDJPY": {"spread": 0.015}}}  # 自前sourceなし
    s = bd.transaction_cost_summary(pd.DataFrame(), j)
    assert s["configured_asset_count"] == 0
    assert s["unsourced_nonzero_count"] == 1
