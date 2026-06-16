from __future__ import annotations

"""Adversarial Review Agent (Phase 23) — ルールベースの横断監査。

AI Feedback / Rule Proposal / Model State Proposal / Weights Patch /
Auto Calibration など、蓄積済みの「提案・要約」を横断レビューし、
危険な兆候を検出する。新しい予測ロジックではなく、既存の安全思想
(憲章「AIは監査される対象」「過剰最適化への自動ブレーキ」)の上に載る
"敵対的レビュー層"である。

検出観点:
1. サンプル不足なのに強い提案 (insufficient_sample_strong)
2. 自動適用・weights更新の危険 (auto_apply_violation / weights_update_violation)
3. 過剰最適化リスク (overfitting_risk)
4. 未来情報混入の波及 (lookahead_contamination)
5. 過信表現 (overconfidence_language)
6. レイヤー間の矛盾 (cross_layer_contradiction)

絶対条件:
- 監査結果は提案・警告のみ。weights.json / generate_signal.py は一切変更しない。
- LLM API・有料APIは新規利用しない(蓄積済みCSV/JSONのみ)。
- requires_human_approval は常に true。
"""

import argparse
import json
import math
from pathlib import Path

import pandas as pd

import stat_guards
from time_utils import format_jst, format_utc, now_utc

RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/audit")

REVIEW_COLUMNS = [
    "generated_at_jst",
    "review_id",
    "source_type",
    "target",
    "finding_category",
    "severity",
    "evidence",
    "recommended_action",
    "requires_human_approval",
    "weights_json_updated",
    "generate_signal_updated",
    "notes",
]

SEVERITY_ORDER = {"info": 0, "warning": 1, "high_risk": 2, "blocked": 3}

STRONG_VALUES = {"high", "strong", "adopt", "increase_strong"}
LOW_CONFIDENCE = {"low", "insufficient_data", "none", "weak"}

OVERCONFIDENCE_TERMS = [
    # 日本語
    "確実", "必ず", "絶対", "間違いない", "リスクなし", "リスクゼロ", "鉄板", "100%", "確実に儲か",
    # 英語
    "guaranteed", "certain win", "no risk", "risk-free", "riskless", "always wins", "surefire", "can't lose", "100% sure",
]

MIN_SAMPLES = stat_guards.MIN_SAMPLES_WEIGHT_CHANGE  # 30


# === 低レベルヘルパー (純粋) ===

def truthy(value) -> bool:
    """'true'/'1'/'yes'/True/1 を True とみなす。"""
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    s = str(value).strip().lower()
    return s in {"true", "1", "yes", "y", "applied"}


def num(value, default: float = 0.0) -> float:
    try:
        f = float(value)
    except (TypeError, ValueError):
        return default
    if pd.isna(f) or math.isinf(f):
        return default
    return f


# auto_calibration の classification は STRONG_VALUES 語彙ではなく方向値を取る。
# 方向性のある提案(increase/decrease)はサンプル不足チェックの対象とみなす。
DIRECTIONAL_VALUES = {"increase", "decrease", "up", "down", "raise", "lower"}


def is_strong(value) -> bool:
    return str(value).strip().lower() in STRONG_VALUES


def is_directional(value) -> bool:
    return str(value).strip().lower() in DIRECTIONAL_VALUES


def is_low_confidence(value) -> bool:
    return str(value).strip().lower() in LOW_CONFIDENCE


def detect_overconfidence(text) -> list[str]:
    if text is None:
        return []
    low = str(text).lower()
    found = [t for t in OVERCONFIDENCE_TERMS if t.lower() in low]
    return sorted(set(found))


def _finding(
    *,
    source_type: str,
    target: str,
    category: str,
    severity: str,
    evidence: str,
    recommended_action: str,
    notes: str = "",
) -> dict:
    return {
        "review_id": "",  # main() で連番付与
        "source_type": source_type,
        "target": str(target),
        "finding_category": category,
        "severity": severity,
        "evidence": evidence,
        "recommended_action": recommended_action,
        "requires_human_approval": True,
        "weights_json_updated": False,
        "generate_signal_updated": False,
        "notes": notes,
    }


# === 検出ディメンション (各々 df -> findings list) ===

def check_auto_apply_and_weight_updates(df: pd.DataFrame, source_type: str, target_col: str) -> list[dict]:
    """憲章違反の最重要検出: 自動適用 / weights更新 / patch適用 / generate_signal変更。"""
    if df.empty:
        return []
    out = []
    for _, r in df.iterrows():
        target = r.get(target_col, "")
        if "apply_automatically" in df.columns and truthy(r.get("apply_automatically")):
            out.append(_finding(
                source_type=source_type, target=target, category="auto_apply_violation", severity="high_risk",
                evidence="apply_automatically=true", recommended_action="apply_automatically を false に戻し、人間承認を必須化する",
            ))
        if "weights_json_updated" in df.columns and truthy(r.get("weights_json_updated")):
            out.append(_finding(
                source_type=source_type, target=target, category="weights_update_violation", severity="blocked",
                evidence="weights_json_updated=true", recommended_action="weights.jsonの自動更新を即時停止し、変更を巻き戻す",
            ))
        if "patch_applied" in df.columns and truthy(r.get("patch_applied")):
            out.append(_finding(
                source_type=source_type, target=target, category="weights_update_violation", severity="blocked",
                evidence="patch_applied=true", recommended_action="patch自動適用を停止し、適用済み変更を監査する",
            ))
        if "generate_signal_updated" in df.columns and truthy(r.get("generate_signal_updated")):
            out.append(_finding(
                source_type=source_type, target=target, category="generate_signal_violation", severity="blocked",
                evidence="generate_signal_updated=true", recommended_action="generate_signal.pyの自動変更を停止する",
            ))
    return out


def check_insufficient_sample_strong(df: pd.DataFrame, source_type: str, target_col: str, strength_col: str, sample_col: str, predicate=is_strong) -> list[dict]:
    """サンプル不足(<30)なのに強い/方向性のある提案。

    predicate で「強い提案」の判定方法を差し替えられる。proposal_strength 系は
    is_strong、auto_calibration の classification(increase/decrease) は is_directional。
    """
    if df.empty or strength_col not in df.columns or sample_col not in df.columns:
        return []
    out = []
    for _, r in df.iterrows():
        n = num(r.get(sample_col))
        if predicate(r.get(strength_col)) and n < MIN_SAMPLES:
            sev = "high_risk" if n < MIN_SAMPLES / 2 else "warning"
            out.append(_finding(
                source_type=source_type, target=r.get(target_col, ""), category="insufficient_sample_strong", severity=sev,
                evidence=f"{strength_col}={r.get(strength_col)} だが {sample_col}={int(n)} < {MIN_SAMPLES}",
                recommended_action=f"サンプルが{MIN_SAMPLES}件に達するまで強い提案を保留(Watching固定)",
            ))
    return out


def check_overfitting_risk(df: pd.DataFrame, source_type: str, target_col: str) -> list[dict]:
    """増加方向の提案が低サンプル/低信頼で出ている過剰最適化リスク。"""
    if df.empty:
        return []
    out = []
    direction_col = next((c for c in ["proposal_direction"] if c in df.columns), None)
    delta_col = next((c for c in ["proposed_delta", "suggested_delta"] if c in df.columns), None)
    sample_col = next((c for c in ["sample_count", "evidence_count", "sample_size"] if c in df.columns), None)
    conf_col = next((c for c in ["confidence_level", "confidence"] if c in df.columns), None)
    for _, r in df.iterrows():
        increasing = (direction_col and str(r.get(direction_col)).lower() in {"increase", "up", "raise"}) or (
            delta_col and num(r.get(delta_col)) > 0
        )
        if not increasing:
            continue
        n = num(r.get(sample_col)) if sample_col else 0.0
        low_conf = is_low_confidence(r.get(conf_col)) if conf_col else False
        if (sample_col and n < MIN_SAMPLES) or low_conf:
            out.append(_finding(
                source_type=source_type, target=r.get(target_col, ""), category="overfitting_risk", severity="warning",
                evidence=f"増加提案だが n={int(n)} / confidence={r.get(conf_col) if conf_col else 'NA'}",
                recommended_action="直近相場への過剰最適化の可能性。統計的優位性(DSR/Sharpe)の確認を人間に求める",
            ))
    return out


def check_evidence_quality(review_df: pd.DataFrame) -> list[dict]:
    """weights_patch_review: 最低条件未達なのに強い、または高リスク。"""
    if review_df.empty:
        return []
    out = []
    for _, r in review_df.iterrows():
        target = r.get("target", "")
        mcm = r.get("minimum_conditions_met")
        if "minimum_conditions_met" in review_df.columns and pd.notna(mcm) and not truthy(mcm) and is_strong(r.get("proposal_strength")):
            out.append(_finding(
                source_type="weights_patch_review", target=target, category="weak_evidence_strong_claim", severity="warning",
                evidence=f"minimum_conditions_met=false かつ proposal_strength={r.get('proposal_strength')}",
                recommended_action="不足条件(missing_conditions)を満たすまで採用判断を保留",
                notes=str(r.get("missing_conditions", "")),
            ))
        if str(r.get("patch_risk_level", "")).strip().lower() in {"high", "severe"}:
            out.append(_finding(
                source_type="weights_patch_review", target=target, category="high_patch_risk", severity="high_risk",
                evidence=f"patch_risk_level={r.get('patch_risk_level')}",
                recommended_action="高リスクpatchは人間が個別精査するまで適用しない",
            ))
    return out


def check_overconfidence(frames: list[tuple[str, pd.DataFrame, str, list[str]]]) -> list[dict]:
    """テキスト列の過信表現を検出。frames: (source_type, df, target_col, text_cols)。"""
    out = []
    for source_type, df, target_col, text_cols in frames:
        if df.empty:
            continue
        for _, r in df.iterrows():
            text = " ".join(str(r.get(c, "")) for c in text_cols if c in df.columns)
            terms = detect_overconfidence(text)
            if terms:
                out.append(_finding(
                    source_type=source_type, target=r.get(target_col, ""), category="overconfidence_language", severity="warning",
                    evidence="過信表現: " + ", ".join(terms),
                    recommended_action="断定的表現を確率的表現へ修正し、不確実性を明示する",
                ))
    return out


def check_lookahead_contamination(lookahead_summary: dict | None) -> list[dict]:
    """Narrative Lookahead Audit が warning以上なら、ナラティブ由来提案への波及を警告。"""
    if not isinstance(lookahead_summary, dict) or not lookahead_summary:
        return []
    status = str(lookahead_summary.get("audit_status", "")).lower()
    sev_map = {"warning": "warning", "high_risk": "high_risk", "blocked": "blocked"}
    if status in sev_map:
        return [_finding(
            source_type="narrative_lookahead_audit", target="narrative_derived_proposals",
            category="lookahead_contamination", severity=sev_map[status],
            evidence=f"narrative_lookahead audit_status={status} (high_risk={lookahead_summary.get('high_risk_count')}, blocked={lookahead_summary.get('blocked_count')})",
            recommended_action="ナラティブ/AIフィードバックに依存する提案は、未来情報混入が解消されるまで採用しない",
        )]
    return []


def check_cross_layer_contradiction(model_state: pd.DataFrame, auto_calib: pd.DataFrame) -> list[dict]:
    """同一targetに対して、あるレイヤーは増加・別レイヤーは減少を提案している矛盾。"""
    def signed(df, target_col, delta_col):
        m = {}
        if df.empty or delta_col not in df.columns or target_col not in df.columns:
            return m
        for _, r in df.iterrows():
            d = num(r.get(delta_col))
            if d == 0:
                continue
            m[str(r.get(target_col))] = m.get(str(r.get(target_col)), 0.0) + d
        return m

    ms = signed(model_state, "target", "proposed_delta")
    ac = signed(auto_calib, "target", "suggested_delta")
    out = []
    for target in sorted(set(ms) & set(ac)):
        if ms[target] * ac[target] < 0:
            out.append(_finding(
                source_type="cross_layer", target=target, category="cross_layer_contradiction", severity="warning",
                evidence=f"model_state delta={ms[target]:+.3f} と auto_calibration delta={ac[target]:+.3f} が逆方向",
                recommended_action="矛盾する提案は採用せず、どちらが正しいか人間が判断する",
            ))
    return out


# === I/O ===

def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except (pd.errors.EmptyDataError, OSError):
        return pd.DataFrame()


def read_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def build_findings(sources: dict) -> list[dict]:
    """全ディメンションを実行して findings を集める。"""
    rule = sources.get("rule_update_proposals", pd.DataFrame())
    model_state = sources.get("model_state_update_proposals", pd.DataFrame())
    patch = sources.get("weights_patch_proposal", pd.DataFrame())
    review = sources.get("weights_patch_review", pd.DataFrame())
    auto_calib = sources.get("auto_calibration_candidates", pd.DataFrame())
    ai_feedback = sources.get("ai_feedback", pd.DataFrame())
    lookahead_summary = sources.get("narrative_lookahead_audit_summary", None)

    findings: list[dict] = []
    # 2. 自動適用 / weights更新の危険 (全提案系)
    findings += check_auto_apply_and_weight_updates(rule, "rule_update_proposal", "target_name")
    findings += check_auto_apply_and_weight_updates(model_state, "model_state_proposal", "target")
    findings += check_auto_apply_and_weight_updates(patch, "weights_patch_proposal", "target")
    findings += check_auto_apply_and_weight_updates(review, "weights_patch_review", "target")
    findings += check_auto_apply_and_weight_updates(auto_calib, "auto_calibration", "target")
    # 1. サンプル不足なのに強い提案
    findings += check_insufficient_sample_strong(rule, "rule_update_proposal", "target_name", "proposal_strength", "evidence_count")
    findings += check_insufficient_sample_strong(model_state, "model_state_proposal", "target", "proposal_strength", "sample_count")
    findings += check_insufficient_sample_strong(patch, "weights_patch_proposal", "target", "proposal_strength", "sample_count")
    findings += check_insufficient_sample_strong(auto_calib, "auto_calibration", "target", "classification", "sample_size", predicate=is_directional)
    # 3. 過剰最適化リスク
    findings += check_overfitting_risk(model_state, "model_state_proposal", "target")
    findings += check_overfitting_risk(patch, "weights_patch_proposal", "target")
    findings += check_overfitting_risk(auto_calib, "auto_calibration", "target")
    # 3b. 証拠品質
    findings += check_evidence_quality(review)
    # 4. 未来情報混入の波及
    findings += check_lookahead_contamination(lookahead_summary)
    # 5. 過信表現
    findings += check_overconfidence([
        ("rule_update_proposal", rule, "target_name", ["proposed_change", "expected_effect", "risk_note", "notes"]),
        ("model_state_proposal", model_state, "target", ["rationale"]),
        ("ai_feedback", ai_feedback, "asset", ["feedback_summary", "proposed_next_action"]),
    ])
    # 6. レイヤー間の矛盾
    findings += check_cross_layer_contradiction(model_state, auto_calib)
    return findings


def summarize(findings: list[dict], sources_present: int, generated_at_jst: str, generated_at_utc: str) -> dict:
    def count(sev: str) -> int:
        return sum(1 for f in findings if f["severity"] == sev)

    blocked, high, warn, info = count("blocked"), count("high_risk"), count("warning"), count("info")
    contradictions = sum(1 for f in findings if f["finding_category"] == "cross_layer_contradiction")
    auto_apply = sum(1 for f in findings if f["finding_category"] == "auto_apply_violation")
    weights_viol = sum(1 for f in findings if f["finding_category"] in ("weights_update_violation", "generate_signal_violation"))

    if sources_present == 0:
        status = "unavailable"
    elif blocked > 0:
        status = "blocked"
    elif high > 0:
        status = "high_risk"
    elif warn > 0:
        status = "warning"
    else:
        status = "passed"

    max_severity = "none"
    for sev in ("blocked", "high_risk", "warning", "info"):
        if count(sev) > 0:
            max_severity = sev
            break

    action = {
        "blocked": "重大な安全違反あり。人間が即時に確認し、自動適用を停止すること",
        "high_risk": "高リスク提案あり。人間の精査が必要",
        "warning": "警告あり。人間が時間軸・サンプル・矛盾を確認",
        "passed": "continue_monitoring",
        "unavailable": "提案データ蓄積後に再レビュー",
    }[status]

    return {
        "generated_at_jst": generated_at_jst,
        "generated_at_utc": generated_at_utc,
        "review_status": status,
        "total_sources_checked": sources_present,
        "total_findings": len(findings),
        "info_count": info,
        "warning_count": warn,
        "high_risk_count": high,
        "blocked_count": blocked,
        "contradiction_count": contradictions,
        "auto_apply_violation_count": auto_apply,
        "weights_update_violation_count": weights_viol,
        "max_severity": max_severity,
        "recommended_next_action": action,
        "requires_human_approval": True,
        "weights_json_updated": False,
        "generate_signal_updated": False,
    }


def render_markdown(summary: dict, findings: list[dict]) -> str:
    severe = [f for f in findings if f["severity"] in ("blocked", "high_risk")]
    warns = [f for f in findings if f["severity"] == "warning"]
    cat_counts: dict[str, int] = {}
    for f in findings:
        cat_counts[f["finding_category"]] = cat_counts.get(f["finding_category"], 0) + 1

    def table(items: list[dict]) -> str:
        if not items:
            return "_該当なし_"
        lines = ["| source | target | category | severity | evidence | action |", "| --- | --- | --- | --- | --- | --- |"]
        for f in items[:30]:
            lines.append(
                "| {source_type} | {target} | {finding_category} | {severity} | {ev} | {ac} |".format(
                    ev=str(f["evidence"]).replace("|", "\\|")[:80], ac=str(f["recommended_action"]).replace("|", "\\|")[:60], **f
                )
            )
        return "\n".join(lines)

    cat_lines = "\n".join(f"- {k}: {v}" for k, v in sorted(cat_counts.items())) or "- なし"
    return f"""# Adversarial Review

## 1. 概要

提案・要約レイヤー(Rule/Model State/Weights Patch/Auto Calibration/AI Feedback)を
横断レビューし、危険な兆候を検出する敵対的監査です。自動適用はせず、警告のみ提示します。

## 2. レビューステータス

- review_status: **{summary['review_status']}**
- max_severity: {summary['max_severity']}
- recommended_next_action: {summary['recommended_next_action']}
- requires_human_approval: {summary['requires_human_approval']} / weights_json_updated: {summary['weights_json_updated']} / generate_signal_updated: {summary['generate_signal_updated']}

## 3. 件数

- total_sources_checked: {summary['total_sources_checked']} / total_findings: {summary['total_findings']}
- blocked: {summary['blocked_count']} / high_risk: {summary['high_risk_count']} / warning: {summary['warning_count']} / info: {summary['info_count']}
- 自動適用違反: {summary['auto_apply_violation_count']} / weights更新違反: {summary['weights_update_violation_count']} / 矛盾: {summary['contradiction_count']}

## 4. blocked / high_risk 詳細

{table(severe)}

## 5. warning 詳細

{table(warns)}

## 6. finding_category 別集計

{cat_lines}

## 7. 注意事項

- この監査は自動売買判断ではありません。提案の危険兆候を人間に提示する補助です。
- weights.json / generate_signal.py は一切変更しません。
- 最終判断は人間が行います。
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Adversarial review of accumulated proposals/summaries.")
    parser.parse_args()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    now = now_utc()
    generated_at_jst = format_jst(now)
    generated_at_utc = format_utc(now)

    csv_sources = {
        "rule_update_proposals": "rule_update_proposals.csv",
        "model_state_update_proposals": "model_state_update_proposals.csv",
        "weights_patch_proposal": "weights_patch_proposal.csv",
        "weights_patch_review": "weights_patch_review.csv",
        "auto_calibration_candidates": "auto_calibration_candidates.csv",
        "ai_feedback": "ai_feedback.csv",
    }
    sources: dict = {}
    sources_present = 0
    for key, fname in csv_sources.items():
        df = read_csv(RESULTS_DIR / fname)
        sources[key] = df
        if not df.empty:
            sources_present += 1
    sources["narrative_lookahead_audit_summary"] = read_json(RESULTS_DIR / "narrative_lookahead_audit_summary.json")
    if sources["narrative_lookahead_audit_summary"]:
        sources_present += 1

    findings = build_findings(sources)
    for i, f in enumerate(findings):
        f["review_id"] = f"adv_{i}"
        f["generated_at_jst"] = generated_at_jst

    summary = summarize(findings, sources_present, generated_at_jst, generated_at_utc)

    review_df = pd.DataFrame(findings, columns=REVIEW_COLUMNS)
    review_df.to_csv(RESULTS_DIR / "adversarial_review.csv", index=False)
    (RESULTS_DIR / "adversarial_review.json").write_text(json.dumps(findings, ensure_ascii=False, indent=2), encoding="utf-8")
    (RESULTS_DIR / "adversarial_review_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    report_date = generated_at_jst[:10]
    (REPORTS_DIR / f"{report_date}_adversarial_review.md").write_text(render_markdown(summary, findings), encoding="utf-8")

    print(f"adversarial review: status={summary['review_status']} findings={summary['total_findings']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
