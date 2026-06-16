from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import audit_adversarial_review as ar


JST = "2026-06-16 10:00:00 JST"


# === 低レベルヘルパー ===

def test_truthy():
    for v in [True, "true", "True", "1", 1, "yes", "applied"]:
        assert ar.truthy(v) is True
    for v in [False, "false", "0", 0, "no", None, "", "hold"]:
        assert ar.truthy(v) is False


def test_detect_overconfidence_ja_en():
    assert "必ず" in ar.detect_overconfidence("これは必ず上がる")
    assert "guaranteed" in ar.detect_overconfidence("a guaranteed win")
    assert ar.detect_overconfidence("通常の見通し") == []


# === 1. サンプル不足なのに強い提案 ===

def test_insufficient_sample_strong():
    df = pd.DataFrame([
        {"target": "BTC", "proposal_strength": "strong", "sample_count": 12},   # < 15 -> high_risk
        {"target": "GOLD", "proposal_strength": "strong", "sample_count": 25},  # 15..30 -> warning
        {"target": "WTI", "proposal_strength": "strong", "sample_count": 40},   # >=30 -> none
        {"target": "SPX", "proposal_strength": "none", "sample_count": 5},      # not strong -> none
    ])
    out = ar.check_insufficient_sample_strong(df, "model_state_proposal", "target", "proposal_strength", "sample_count")
    cats = {f["target"]: f["severity"] for f in out}
    assert cats == {"BTC": "high_risk", "GOLD": "warning"}


# === 2. 自動適用 / weights更新の危険 ===

def test_auto_apply_violation_high_risk():
    df = pd.DataFrame([{"target": "BTC", "apply_automatically": True}])
    out = ar.check_auto_apply_and_weight_updates(df, "model_state_proposal", "target")
    assert len(out) == 1
    assert out[0]["finding_category"] == "auto_apply_violation"
    assert out[0]["severity"] == "high_risk"


def test_weights_update_violation_blocked():
    df = pd.DataFrame([{"target": "BTC", "weights_json_updated": True, "patch_applied": True, "generate_signal_updated": True}])
    out = ar.check_auto_apply_and_weight_updates(df, "weights_patch_review", "target")
    sevs = {f["finding_category"] for f in out}
    assert "weights_update_violation" in sevs
    assert "generate_signal_violation" in sevs
    assert all(f["severity"] == "blocked" for f in out)


def test_clean_rows_no_violation():
    df = pd.DataFrame([{"target": "BTC", "apply_automatically": False, "weights_json_updated": False}])
    assert ar.check_auto_apply_and_weight_updates(df, "x", "target") == []


# === 3. 過剰最適化リスク ===

def test_overfitting_risk_increase_low_sample():
    df = pd.DataFrame([
        {"target": "BTC", "proposal_direction": "increase", "proposed_delta": 0.05, "sample_count": 10, "confidence_level": "low"},
        {"target": "GOLD", "proposal_direction": "decrease", "proposed_delta": -0.05, "sample_count": 5, "confidence_level": "low"},  # 減少は対象外
    ])
    out = ar.check_overfitting_risk(df, "model_state_proposal", "target")
    assert len(out) == 1
    assert out[0]["target"] == "BTC"
    assert out[0]["finding_category"] == "overfitting_risk"


# === 3b. 証拠品質 ===

def test_evidence_quality_weak_strong_and_high_risk():
    df = pd.DataFrame([
        {"target": "BTC", "minimum_conditions_met": False, "proposal_strength": "strong", "missing_conditions": "n>=30", "patch_risk_level": "low"},
        {"target": "GOLD", "minimum_conditions_met": True, "proposal_strength": "strong", "patch_risk_level": "high"},
    ])
    out = ar.check_evidence_quality(df)
    cats = {(f["target"], f["finding_category"]) for f in out}
    assert ("BTC", "weak_evidence_strong_claim") in cats
    assert ("GOLD", "high_patch_risk") in cats


# === 4. 未来情報混入の波及 ===

def test_lookahead_contamination_propagates():
    assert ar.check_lookahead_contamination({"audit_status": "high_risk", "high_risk_count": 2, "blocked_count": 0})[0]["severity"] == "high_risk"
    assert ar.check_lookahead_contamination({"audit_status": "blocked"})[0]["severity"] == "blocked"
    assert ar.check_lookahead_contamination({"audit_status": "passed"}) == []
    assert ar.check_lookahead_contamination(None) == []


# === 5. 過信表現 ===

def test_overconfidence_finding():
    df = pd.DataFrame([{"target": "BTC", "rationale": "これは絶対に勝てる"}])
    out = ar.check_overconfidence([("model_state_proposal", df, "target", ["rationale"])])
    assert len(out) == 1
    assert out[0]["finding_category"] == "overconfidence_language"


# === 6. レイヤー間の矛盾 ===

def test_cross_layer_contradiction():
    model = pd.DataFrame([{"target": "BTC", "proposed_delta": 0.05}, {"target": "GOLD", "proposed_delta": 0.03}])
    auto = pd.DataFrame([{"target": "BTC", "suggested_delta": -0.04}, {"target": "GOLD", "suggested_delta": 0.02}])
    out = ar.check_cross_layer_contradiction(model, auto)
    assert len(out) == 1
    assert out[0]["target"] == "BTC"  # 逆方向のみ
    assert out[0]["finding_category"] == "cross_layer_contradiction"


# === 集計 / status ===

def test_summary_status_precedence_blocked():
    findings = [
        ar._finding(source_type="x", target="t", category="weights_update_violation", severity="blocked", evidence="e", recommended_action="a"),
        ar._finding(source_type="x", target="t", category="insufficient_sample_strong", severity="warning", evidence="e", recommended_action="a"),
    ]
    s = ar.summarize(findings, sources_present=3, generated_at_jst=JST, generated_at_utc=JST)
    assert s["review_status"] == "blocked"
    assert s["blocked_count"] == 1 and s["warning_count"] == 1
    assert s["max_severity"] == "blocked"


def test_summary_unavailable_when_no_sources():
    s = ar.summarize([], sources_present=0, generated_at_jst=JST, generated_at_utc=JST)
    assert s["review_status"] == "unavailable"


def test_summary_passed_when_sources_no_findings():
    s = ar.summarize([], sources_present=4, generated_at_jst=JST, generated_at_utc=JST)
    assert s["review_status"] == "passed"


# === safety flags 固定 ===

def test_safety_flags_fixed():
    f = ar._finding(source_type="x", target="t", category="overfitting_risk", severity="warning", evidence="e", recommended_action="a")
    assert f["requires_human_approval"] is True
    assert f["weights_json_updated"] is False
    assert f["generate_signal_updated"] is False
    s = ar.summarize([f], 1, JST, JST)
    assert s["requires_human_approval"] is True
    assert s["weights_json_updated"] is False
    assert s["generate_signal_updated"] is False


# === build_findings 空入力で落ちない ===

def test_build_findings_empty():
    assert ar.build_findings({}) == []


# === build_findings 統合: 違反提案を検出 ===

def test_build_findings_detects_violation():
    sources = {
        "model_state_update_proposals": pd.DataFrame([
            {"target": "BTC", "proposal_strength": "strong", "sample_count": 8, "apply_automatically": True,
             "proposal_direction": "increase", "proposed_delta": 0.05, "confidence_level": "low", "rationale": "必ず上がる"},
        ]),
    }
    findings = ar.build_findings(sources)
    cats = {f["finding_category"] for f in findings}
    assert "auto_apply_violation" in cats
    assert "insufficient_sample_strong" in cats
    assert "overfitting_risk" in cats
    assert "overconfidence_language" in cats


# === セルフ監査で指摘されたギャップの追補 ===

# auto_calibration: 方向性ありの低サンプル候補が検出される(旧デッドルールの修正確認)
def test_auto_calibration_directional_low_sample_detected():
    df = pd.DataFrame([
        {"target": "BTC", "classification": "decrease", "sample_size": 8, "suggested_delta": -0.05},
        {"target": "GOLD", "classification": "increase", "sample_size": 25, "suggested_delta": 0.05},
        {"target": "WTI", "classification": "hold", "sample_size": 5, "suggested_delta": 0.0},   # holdは対象外
        {"target": "SPX", "classification": "increase", "sample_size": 40, "suggested_delta": 0.05},  # 十分
    ])
    out = ar.check_insufficient_sample_strong(df, "auto_calibration", "target", "classification", "sample_size", predicate=ar.is_directional)
    sev = {f["target"]: f["severity"] for f in out}
    assert sev == {"BTC": "high_risk", "GOLD": "warning"}


def test_is_directional_vocabulary():
    assert ar.is_directional("increase") and ar.is_directional("decrease")
    assert not ar.is_directional("hold") and not ar.is_directional("insufficient_data")


# summarize: high_risk / warning 分岐 + action 文言
def test_summary_status_high_risk_branch():
    findings = [
        ar._finding(source_type="x", target="t", category="high_patch_risk", severity="high_risk", evidence="e", recommended_action="a"),
        ar._finding(source_type="x", target="t", category="overfitting_risk", severity="warning", evidence="e", recommended_action="a"),
    ]
    s = ar.summarize(findings, 3, JST, JST)
    assert s["review_status"] == "high_risk"
    assert s["max_severity"] == "high_risk"
    assert "高リスク" in s["recommended_next_action"]


def test_summary_status_warning_only_branch():
    s = ar.summarize([ar._finding(source_type="x", target="t", category="overfitting_risk", severity="warning", evidence="e", recommended_action="a")], 3, JST, JST)
    assert s["review_status"] == "warning"
    assert s["max_severity"] == "warning"


# summarize: 違反/矛盾の集計(generate_signal_violation も weights_update に合算)
def test_summary_violation_rollups():
    findings = [
        ar._finding(source_type="x", target="t", category="auto_apply_violation", severity="high_risk", evidence="e", recommended_action="a"),
        ar._finding(source_type="x", target="t", category="weights_update_violation", severity="blocked", evidence="e", recommended_action="a"),
        ar._finding(source_type="x", target="t", category="generate_signal_violation", severity="blocked", evidence="e", recommended_action="a"),
        ar._finding(source_type="x", target="t", category="cross_layer_contradiction", severity="warning", evidence="e", recommended_action="a"),
    ]
    s = ar.summarize(findings, 3, JST, JST)
    assert s["auto_apply_violation_count"] == 1
    assert s["weights_update_violation_count"] == 2  # weights_update + generate_signal
    assert s["contradiction_count"] == 1
    assert s["review_status"] == "blocked"


# num(): NaN/None/garbage/inf を default に落とす
def test_num_handles_nan_none_garbage_inf():
    assert ar.num(float("nan")) == 0.0
    assert ar.num(None) == 0.0
    assert ar.num("abc") == 0.0
    assert ar.num(float("inf")) == 0.0
    assert ar.num("3.5") == 3.5
    assert ar.num(2, default=9) == 2.0


def test_insufficient_sample_nan_treated_as_zero():
    # サンプル数がNaN(欠損)でも強い提案なら high_risk(0扱い)
    df = pd.DataFrame([{"target": "BTC", "proposal_strength": "strong", "sample_count": float("nan")}])
    out = ar.check_insufficient_sample_strong(df, "model_state_proposal", "target", "proposal_strength", "sample_count")
    assert len(out) == 1 and out[0]["severity"] == "high_risk"


# insufficient_sample 境界値
def test_insufficient_sample_boundaries():
    df = pd.DataFrame([
        {"target": "a", "proposal_strength": "strong", "sample_count": 14},  # < 15 -> high_risk
        {"target": "b", "proposal_strength": "strong", "sample_count": 15},  # == 15 -> warning
        {"target": "c", "proposal_strength": "strong", "sample_count": 29},  # < 30 -> warning
        {"target": "d", "proposal_strength": "strong", "sample_count": 30},  # == 30 -> none
    ])
    out = {f["target"]: f["severity"] for f in ar.check_insufficient_sample_strong(df, "m", "target", "proposal_strength", "sample_count")}
    assert out == {"a": "high_risk", "b": "warning", "c": "warning"}


# overfitting: direction列なしでも正のdeltaで発火、負deltaは非発火
def test_overfitting_delta_only_path():
    df = pd.DataFrame([
        {"target": "BTC", "suggested_delta": 0.05, "sample_size": 5},
        {"target": "GOLD", "suggested_delta": -0.05, "sample_size": 5},
    ])
    out = ar.check_overfitting_risk(df, "auto_calibration", "target")
    assert [f["target"] for f in out] == ["BTC"]


# evidence_quality: minimum_conditions_met が欠損(NaN)なら誤検出しない
def test_evidence_quality_nan_not_flagged():
    df = pd.DataFrame([{"target": "BTC", "minimum_conditions_met": float("nan"), "proposal_strength": "strong", "patch_risk_level": "low"}])
    out = ar.check_evidence_quality(df)
    assert all(f["finding_category"] != "weak_evidence_strong_claim" for f in out)


# lookahead: 大文字statusの畳み込みと未知status
def test_lookahead_case_and_unknown():
    assert ar.check_lookahead_contamination({"audit_status": "WARNING"})[0]["severity"] == "warning"
    assert ar.check_lookahead_contamination({"audit_status": "unknown_xyz"}) == []
    assert ar.check_lookahead_contamination({}) == []


# cross_layer: 同一レイヤー内で相殺(net-zero)は矛盾としない
def test_cross_layer_netting_no_false_contradiction():
    model = pd.DataFrame([{"target": "BTC", "proposed_delta": 0.05}, {"target": "BTC", "proposed_delta": -0.05}])  # nets to 0
    auto = pd.DataFrame([{"target": "BTC", "suggested_delta": -0.04}])
    assert ar.check_cross_layer_contradiction(model, auto) == []


# === Codex P2: 偽passed防止 (sources有効性) ===

def test_lookahead_unavailable_not_counted_as_source():
    # lookahead が unavailable のときは有効ソースに数えない
    assert ar.lookahead_counts_as_source({"audit_status": "unavailable"}) is False
    assert ar.lookahead_counts_as_source({}) is False
    assert ar.lookahead_counts_as_source(None) is False
    assert ar.lookahead_counts_as_source({"audit_status": ""}) is False


def test_lookahead_checked_statuses_counted_as_source():
    for st in ["passed", "warning", "high_risk", "blocked", "PASSED", "Blocked"]:
        assert ar.lookahead_counts_as_source({"audit_status": st}) is True


def test_count_sources_present_ignores_empty_and_unavailable():
    sources = {
        "rule_update_proposals": pd.DataFrame(),
        "model_state_update_proposals": pd.DataFrame(),
        "weights_patch_proposal": pd.DataFrame(),
        "weights_patch_review": pd.DataFrame(),
        "auto_calibration_candidates": pd.DataFrame(),
        "ai_feedback": pd.DataFrame(),
        "narrative_lookahead_audit_summary": {"audit_status": "unavailable"},
    }
    # 全CSV空 + lookahead unavailable -> 0
    assert ar.count_sources_present(sources) == 0


def test_count_sources_present_counts_real_sources():
    sources = {
        "rule_update_proposals": pd.DataFrame([{"x": 1}]),
        "narrative_lookahead_audit_summary": {"audit_status": "passed"},
    }
    # 中身のあるCSV1件 + 実チェック済みlookahead1件 -> 2
    assert ar.count_sources_present(sources) == 2


def test_no_false_passed_when_nothing_reviewed():
    # 提案CSVが全部空、lookaheadもunavailable -> review_status は unavailable (passedではない)
    sources = {k: pd.DataFrame() for k in ar.CSV_SOURCE_KEYS}
    sources["narrative_lookahead_audit_summary"] = {"audit_status": "unavailable"}
    findings = ar.build_findings(sources)
    s = ar.summarize(findings, ar.count_sources_present(sources), JST, JST)
    assert findings == []
    assert s["review_status"] == "unavailable"  # 偽passedにしない


def test_passed_only_when_real_sources_present():
    sources = {k: pd.DataFrame() for k in ar.CSV_SOURCE_KEYS}
    sources["narrative_lookahead_audit_summary"] = {"audit_status": "passed"}  # 実チェック済み
    s = ar.summarize(ar.build_findings(sources), ar.count_sources_present(sources), JST, JST)
    assert s["review_status"] == "passed"
