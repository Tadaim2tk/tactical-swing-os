from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from time_utils import format_jst, format_utc, now_utc


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/model_state")
WEIGHTS_PATH = Path("models/weights.json")
PATCH_JSON_CANDIDATES = [
    RESULTS_DIR / "weights_patch_proposal.json",
    RESULTS_DIR / "weights_patch_proposals.json",
]
PATCH_CSV_CANDIDATES = [
    RESULTS_DIR / "weights_patch_proposal.csv",
    RESULTS_DIR / "weights_patch_proposals.csv",
]
MODEL_STATE_JSON = RESULTS_DIR / "model_state_update_proposals.json"
MODEL_STATE_CSV = RESULTS_DIR / "model_state_update_proposals.csv"
AUDIT_JSON = RESULTS_DIR / "model_state_proposal_audit.json"
REVIEW_COLUMNS = [
    "generated_at_jst",
    "patch_id",
    "proposal_id",
    "category",
    "target",
    "weight_path",
    "patch_action",
    "current_weight",
    "proposed_delta",
    "proposed_value",
    "sample_count",
    "confidence_level",
    "proposal_strength",
    "proposal_direction",
    "audit_result",
    "review_decision",
    "human_action_required",
    "recommended_human_action",
    "review_reason",
    "minimum_conditions_met",
    "missing_conditions",
    "evidence_quality",
    "patch_risk_level",
    "requires_human_approval",
    "apply_automatically",
    "patch_applied",
    "weights_json_updated",
    "rationale",
]
RISK_ORDER = ["low", "medium", "high"]


def normalize_column_name(column: str) -> str:
    normalized = str(column).strip().lower().replace("-", "_")
    normalized = "_".join(normalized.split())
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    return normalized


def normalize_headers(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    out = df.copy()
    out.columns = [normalize_column_name(col) for col in out.columns]
    return out


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def read_first_json(paths: list[Path]) -> Any:
    for path in paths:
        payload = read_json(path)
        if payload is not None:
            return payload
    return None


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return normalize_headers(pd.read_csv(path))
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def read_first_csv(paths: list[Path]) -> pd.DataFrame:
    for path in paths:
        df = read_csv(path)
        if not df.empty:
            return df
    return pd.DataFrame()


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def parse_float(value: Any, default: float | None = 0.0) -> float | None:
    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number):
        return default
    return float(number)


def parse_int(value: Any, default: int = 0) -> int:
    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number):
        return default
    return int(number)


def load_patch_payload() -> tuple[pd.DataFrame, dict[str, Any]]:
    payload = read_first_json(PATCH_JSON_CANDIDATES)
    if isinstance(payload, dict):
        rows = payload.get("patches", [])
        if isinstance(rows, list):
            return normalize_headers(pd.DataFrame(rows)), payload
    return read_first_csv(PATCH_CSV_CANDIDATES), {}


def load_model_state_proposals() -> pd.DataFrame:
    payload = read_json(MODEL_STATE_JSON, {})
    if isinstance(payload, dict):
        rows = payload.get("proposals", [])
        if isinstance(rows, list) and rows:
            return normalize_headers(pd.DataFrame(rows))
    return read_csv(MODEL_STATE_CSV)


def load_audit_payload() -> dict[str, Any]:
    payload = read_json(AUDIT_JSON, {})
    return payload if isinstance(payload, dict) else {}


def proposal_lookup(proposals: pd.DataFrame) -> dict[str, dict[str, Any]]:
    if proposals.empty or "proposal_id" not in proposals.columns:
        return {}
    return {str(row.get("proposal_id", "")): row.to_dict() for _, row in proposals.iterrows()}


def enrich_patch_row(row: pd.Series, proposals_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    out = row.to_dict()
    proposal = proposals_by_id.get(str(row.get("proposal_id", "")), {})
    for key, value in proposal.items():
        out.setdefault(key, value)
        if out.get(key, "") in {"", None}:
            out[key] = value
    return out


def evidence_quality(sample_count: int, confidence: str, strength: str) -> str:
    if confidence == "insufficient_data" or sample_count < 5:
        return "insufficient"
    if strength == "weak" or sample_count < 10 or confidence == "low":
        return "weak"
    if strength == "strong" and sample_count >= 20 and confidence == "high":
        return "strong"
    return "moderate"


def raise_risk(level: str) -> str:
    try:
        idx = RISK_ORDER.index(level)
    except ValueError:
        return "high"
    return RISK_ORDER[min(idx + 1, len(RISK_ORDER) - 1)]


def patch_risk_level(proposed_delta: float, sample_count: int) -> str:
    magnitude = abs(proposed_delta)
    if magnitude <= 0.03:
        risk = "low"
    elif magnitude <= 0.05:
        risk = "medium"
    else:
        risk = "high"
    if sample_count < 10:
        risk = raise_risk(risk)
    return risk


def evaluate_patch(row: dict[str, Any], audit_status: str) -> dict[str, Any]:
    sample_count = parse_int(row.get("sample_count", 0))
    confidence = str(row.get("confidence_level", ""))
    strength = str(row.get("proposal_strength", ""))
    direction = str(row.get("proposal_direction", ""))
    audit_result = str(row.get("audit_result", ""))
    patch_action = str(row.get("patch_action", ""))
    category = str(row.get("category", "")).strip()
    target = str(row.get("target", "")).strip()
    proposed_delta = parse_float(row.get("proposed_delta", 0), 0.0) or 0.0
    max_allowed_delta = parse_float(row.get("max_allowed_delta", None), None)
    proposed_value = parse_float(row.get("proposed_value", row.get("proposed_weight", None)), None)
    current_weight = parse_float(row.get("current_weight", None), None)
    apply_automatically = parse_bool(row.get("apply_automatically", False))
    patch_applied = parse_bool(row.get("patch_applied", False))
    quality = evidence_quality(sample_count, confidence, strength)
    risk = patch_risk_level(proposed_delta, sample_count)
    missing_conditions: list[str] = []
    reasons: list[str] = []

    if audit_status == "blocked":
        decision = "blocked"
        action = "reject"
        reasons.append("安全監査がblockedのため承認不可")
    elif patch_applied:
        decision = "blocked"
        action = "reject"
        reasons.append("patch_applied_true_is_not_allowed")
    elif audit_result == "blocked":
        decision = "reject"
        action = "reject"
        reasons.append("proposal audit_result blocked")
    elif not category or not target:
        decision = "reject"
        action = "reject"
        reasons.append("category_or_target_missing")
    elif proposed_delta == 0:
        decision = "reject"
        action = "reject"
        reasons.append("proposed_delta_zero")
    elif max_allowed_delta is None:
        decision = "reject"
        action = "reject"
        reasons.append("max_allowed_delta_missing")
    elif proposed_value is None or proposed_value <= 0:
        decision = "reject"
        action = "reject"
        reasons.append("proposed_weight_or_value_invalid")
    elif current_weight is None and patch_action != "add_key_proposal":
        decision = "reject"
        action = "reject"
        reasons.append("current_weight_missing_without_add_key_proposal")
    else:
        if audit_status not in {"passed", "warning"}:
            missing_conditions.append("audit_status_passed_or_warning")
        if strength not in {"moderate", "strong"}:
            missing_conditions.append("proposal_strength_moderate_or_strong")
        if sample_count < 10:
            missing_conditions.append("sample_count_at_least_10")
        if confidence not in {"medium", "high"}:
            missing_conditions.append("confidence_level_medium_or_high")
        if abs(proposed_delta) > max_allowed_delta:
            missing_conditions.append("delta_within_max_allowed")
        if apply_automatically:
            missing_conditions.append("apply_automatically_false")
        if patch_applied:
            missing_conditions.append("patch_applied_false")
        if quality in {"weak", "insufficient"}:
            missing_conditions.append("evidence_quality_moderate_or_strong")

        if not missing_conditions:
            decision = "candidate"
            action = "approve_later"
            reasons.append("minimum_conditions_met")
        else:
            decision = "hold"
            action = "wait_for_more_data"
            reasons.append("データ蓄積または人間確認待ち")

    minimum_conditions_met = decision == "candidate"
    return {
        **row,
        "sample_count": sample_count,
        "confidence_level": confidence,
        "proposal_strength": strength,
        "proposal_direction": direction,
        "proposed_delta": proposed_delta,
        "max_allowed_delta": max_allowed_delta,
        "proposed_value": proposed_value,
        "audit_result": audit_result,
        "review_decision": decision,
        "human_action_required": True,
        "recommended_human_action": action,
        "review_reason": "; ".join(reasons),
        "minimum_conditions_met": minimum_conditions_met,
        "missing_conditions": "|".join(missing_conditions),
        "evidence_quality": quality,
        "patch_risk_level": risk,
        "requires_human_approval": True,
        "apply_automatically": bool(apply_automatically),
        "patch_applied": False,
        "weights_json_updated": False,
    }


def review_patches(patches: pd.DataFrame, proposals: pd.DataFrame, audit_status: str) -> pd.DataFrame:
    if patches.empty:
        return pd.DataFrame(columns=REVIEW_COLUMNS)
    proposals_by_id = proposal_lookup(proposals)
    rows = []
    for _, patch in normalize_headers(patches).iterrows():
        rows.append(evaluate_patch(enrich_patch_row(patch, proposals_by_id), audit_status))
    review = normalize_headers(pd.DataFrame(rows))
    for col in REVIEW_COLUMNS:
        if col not in review.columns:
            review[col] = ""
    return review[REVIEW_COLUMNS + [col for col in review.columns if col not in REVIEW_COLUMNS]]


def review_status_from(review: pd.DataFrame, audit_status: str, source_available: bool) -> str:
    if not source_available:
        return "unavailable"
    if audit_status == "blocked" or (not review.empty and (review["review_decision"] == "blocked").any()):
        return "blocked"
    if not review.empty and ((review["review_decision"] == "reject").any() or (review["review_decision"] == "hold").any()):
        return "warning"
    return "passed"


def recommended_next_action(review: pd.DataFrame, status: str) -> str:
    if status in {"blocked", "unavailable"}:
        return "no_action"
    if review.empty:
        return "no_action"
    if (review["review_decision"] == "candidate").any():
        return "manual_review"
    if (review["review_decision"] == "hold").any():
        return "wait_for_more_data"
    return "no_action"


def build_summary(review: pd.DataFrame, audit_status: str, source_available: bool, generated_at_jst: str, generated_at_utc: str) -> dict[str, Any]:
    status = review_status_from(review, audit_status, source_available)
    decisions = review.get("review_decision", pd.Series(dtype=str))
    risks = review.get("patch_risk_level", pd.Series(dtype=str))
    return {
        "generated_at_jst": generated_at_jst,
        "generated_at_utc": generated_at_utc,
        "review_status": status,
        "total_patch_candidates": int(len(review)),
        "candidate_count": int((decisions == "candidate").sum()) if not review.empty else 0,
        "hold_count": int((decisions == "hold").sum()) if not review.empty else 0,
        "reject_count": int((decisions == "reject").sum()) if not review.empty else 0,
        "blocked_count": int((decisions == "blocked").sum()) if not review.empty else 0,
        "low_risk_count": int((risks == "low").sum()) if not review.empty else 0,
        "medium_risk_count": int((risks == "medium").sum()) if not review.empty else 0,
        "high_risk_count": int((risks == "high").sum()) if not review.empty else 0,
        "requires_human_approval": True,
        "weights_json_updated": False,
        "patch_applied": False,
        "recommended_next_action": recommended_next_action(review, status),
    }


def markdown_table(df: pd.DataFrame, empty: str = "該当なし") -> str:
    if df.empty:
        return empty
    cols = [str(col) for col in df.columns]
    lines = [
        "| " + " | ".join(cols) + " |",
        "| " + " | ".join(["---"] * len(cols)) + " |",
    ]
    for _, row in df.iterrows():
        values = []
        for col in df.columns:
            value = str(row.get(col, ""))
            values.append(value.replace("\n", " ").replace("|", "/"))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def render_markdown(summary: dict[str, Any], review: pd.DataFrame) -> str:
    candidates = review[review["review_decision"] == "candidate"] if not review.empty else pd.DataFrame()
    holds = review[review["review_decision"] == "hold"] if not review.empty else pd.DataFrame()
    rejected = review[review["review_decision"].isin(["reject", "blocked"])] if not review.empty else pd.DataFrame()
    cols = ["weight_path", "patch_action", "current_weight", "proposed_delta", "proposed_value", "sample_count", "confidence_level", "proposal_strength", "patch_risk_level", "review_reason", "missing_conditions"]
    return f"""# Weights Patch Human Review

## 1. 概要

- 生成日時JST: {summary["generated_at_jst"]}
- review_status: {summary["review_status"]}
- patch候補数: {summary["total_patch_candidates"]}
- candidate件数: {summary["candidate_count"]}
- hold件数: {summary["hold_count"]}
- reject件数: {summary["reject_count"]}
- blocked件数: {summary["blocked_count"]}
- requires_human_approval: true
- patch_applied: false
- weights_json_updated: false

## 2. 承認候補

{markdown_table(candidates[cols] if not candidates.empty else candidates)}

## 3. 保留候補

保留候補は、データ蓄積または人間確認を待つpatchです。

{markdown_table(holds[cols] if not holds.empty else holds)}

## 4. 却下候補

{markdown_table(rejected[cols] if not rejected.empty else rejected)}

## 5. 人間チェックリスト

- 対象weight pathは妥当か
- sample_countは十分か
- avg_r / win_rate は実用的か
- 提案deltaは過大ではないか
- 直近相場の一時的偏りではないか
- 同じ方向の提案が複数重なりすぎていないか
- 実売買に使う前にバックテストまたは紙上検証するか

## 6. 注意

- このレポートは承認を補助するだけ
- weights.jsonは更新しない
- 自動売買しない
- 人間承認なしに反映しない
"""


def build_review() -> tuple[pd.DataFrame, dict[str, Any], str]:
    generated_dt_utc = now_utc()
    generated_at_jst = format_jst(generated_dt_utc)
    generated_at_utc = format_utc(generated_dt_utc)
    patches, patch_payload = load_patch_payload()
    proposals = load_model_state_proposals()
    audit_payload = load_audit_payload()
    audit_status = str(audit_payload.get("audit_status", "unavailable") if audit_payload else "unavailable")
    source_available = bool(patch_payload) or not patches.empty or bool(audit_payload)
    review = review_patches(patches, proposals, audit_status)
    summary = build_summary(review, audit_status, source_available, generated_at_jst, generated_at_utc)
    payload = {
        **summary,
        "source": {
            "weights": str(WEIGHTS_PATH),
            "weights_patch_proposal": "results/weights_patch_proposal.json",
            "model_state_update_proposals": "results/model_state_update_proposals.json",
            "audit": "results/model_state_proposal_audit.json",
        },
        "safety": {
            "weights_json_updated": False,
            "patch_applied": False,
            "requires_human_approval": True,
            "apply_automatically": False,
        },
        "patch_review": review.to_dict(orient="records"),
        "patch_summary": patch_payload.get("summary", {}) if isinstance(patch_payload, dict) else {},
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_date = generated_at_jst[:10]
    csv_path = RESULTS_DIR / "weights_patch_review.csv"
    json_path = RESULTS_DIR / "weights_patch_review.json"
    summary_path = RESULTS_DIR / "weights_patch_review_summary.json"
    report_path = REPORTS_DIR / f"{report_date}_weights_patch_review.md"
    review.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    report_path.write_text(render_markdown(summary, review), encoding="utf-8")
    print(f"weights patch review generated: {report_path}")
    print(f"weights patch review rows: {len(review)}")
    return review, summary, str(report_path)


def main() -> int:
    build_review()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
