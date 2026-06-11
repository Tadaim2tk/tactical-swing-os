from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from time_utils import format_jst, format_utc, now_utc


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/model_state")
CONFIG_DIR = Path("config")
REVIEW_JSON = RESULTS_DIR / "weights_patch_review.json"
REVIEW_CSV = RESULTS_DIR / "weights_patch_review.csv"
PATCH_JSON = RESULTS_DIR / "weights_patch_proposal.json"
PATCH_CSV = RESULTS_DIR / "weights_patch_proposal.csv"
MODEL_STATE_JSON = RESULTS_DIR / "model_state_update_proposals.json"
MODEL_STATE_CSV = RESULTS_DIR / "model_state_update_proposals.csv"
AUDIT_JSON = RESULTS_DIR / "model_state_proposal_audit.json"
MANUAL_DECISION_JSON = CONFIG_DIR / "proposal_adoption_decisions.json"
MANUAL_DECISION_CSV = CONFIG_DIR / "proposal_adoption_decisions.csv"
TRACKING_COLUMNS = [
    "generated_at_jst",
    "proposal_id",
    "patch_id",
    "category",
    "target",
    "weight_path",
    "review_decision",
    "adoption_status",
    "adoption_source",
    "human_decision",
    "human_decision_recorded",
    "human_decision_date",
    "recommended_next_action",
    "tracking_reason",
    "sample_count",
    "confidence_level",
    "proposal_strength",
    "proposal_direction",
    "proposed_delta",
    "patch_risk_level",
    "evidence_quality",
    "requires_human_approval",
    "patch_applied",
    "weights_json_updated",
    "rationale",
]
ALLOWED_MANUAL_DECISIONS = {
    "accepted",
    "held",
    "rejected",
    "superseded",
    "pending_review",
    "blocked",
}


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


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return normalize_headers(pd.read_csv(path))
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def parse_float(value: Any, default: float = 0.0) -> float:
    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number):
        return default
    return float(number)


def parse_int(value: Any, default: int = 0) -> int:
    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number):
        return default
    return int(number)


def load_review() -> tuple[pd.DataFrame, dict[str, Any]]:
    payload = read_json(REVIEW_JSON, {})
    if isinstance(payload, dict):
        rows = payload.get("patch_review", [])
        if isinstance(rows, list):
            return normalize_headers(pd.DataFrame(rows)), payload
    return read_csv(REVIEW_CSV), {}


def load_patch_rows() -> pd.DataFrame:
    payload = read_json(PATCH_JSON, {})
    if isinstance(payload, dict):
        rows = payload.get("patches", [])
        if isinstance(rows, list) and rows:
            return normalize_headers(pd.DataFrame(rows))
    return read_csv(PATCH_CSV)


def load_model_state_rows() -> pd.DataFrame:
    payload = read_json(MODEL_STATE_JSON, {})
    if isinstance(payload, dict):
        rows = payload.get("proposals", [])
        if isinstance(rows, list) and rows:
            return normalize_headers(pd.DataFrame(rows))
    return read_csv(MODEL_STATE_CSV)


def load_manual_decisions() -> pd.DataFrame:
    payload = read_json(MANUAL_DECISION_JSON, {})
    if isinstance(payload, dict):
        rows = payload.get("decisions", [])
        if isinstance(rows, list) and rows:
            return normalize_headers(pd.DataFrame(rows))
    elif isinstance(payload, list):
        return normalize_headers(pd.DataFrame(payload))
    return read_csv(MANUAL_DECISION_CSV)


def keyed_lookup(df: pd.DataFrame) -> dict[str, dict[str, Any]]:
    if df.empty:
        return {}
    out: dict[str, dict[str, Any]] = {}
    for _, row in df.iterrows():
        data = row.to_dict()
        for key_col in ("proposal_id", "patch_id"):
            key = str(row.get(key_col, "")).strip()
            if key:
                out[key] = data
    return out


def merge_rows(primary: pd.DataFrame, *fallbacks: pd.DataFrame) -> pd.DataFrame:
    if primary.empty:
        for fallback in fallbacks:
            if not fallback.empty:
                primary = fallback.copy()
                break
    if primary.empty:
        return pd.DataFrame()
    merged = normalize_headers(primary).copy()
    lookups = [keyed_lookup(normalize_headers(df)) for df in fallbacks if not df.empty]
    for idx, row in merged.iterrows():
        for lookup in lookups:
            extras = lookup.get(str(row.get("proposal_id", "")).strip()) or lookup.get(str(row.get("patch_id", "")).strip()) or {}
            for key, value in extras.items():
                if key not in merged.columns:
                    merged[key] = ""
                current = merged.at[idx, key]
                if current in {"", None} or (isinstance(current, float) and pd.isna(current)):
                    merged.at[idx, key] = value
    return merged


def manual_decision_for(row: pd.Series, decisions: pd.DataFrame) -> dict[str, Any]:
    if decisions.empty:
        return {}
    for key_col in ("proposal_id", "patch_id"):
        key = str(row.get(key_col, "")).strip()
        if not key or key_col not in decisions.columns:
            continue
        matched = decisions[decisions[key_col].fillna("").astype(str) == key]
        if not matched.empty:
            return matched.iloc[-1].to_dict()
    return {}


def derived_status(review_decision: str) -> tuple[str, str, str]:
    if review_decision == "candidate":
        return "pending_review", "manual_review", "candidate requires human adoption decision"
    if review_decision == "hold":
        return "held", "wait_for_more_data", "held by review decision; more data required"
    if review_decision == "reject":
        return "rejected", "no_action", "rejected by review decision"
    if review_decision == "blocked":
        return "blocked", "no_action", "blocked by safety review"
    return "unreviewed", "manual_review", "no review decision available"


def adoption_row(row: pd.Series, decisions: pd.DataFrame, generated_at_jst: str) -> dict[str, Any]:
    review_decision = str(row.get("review_decision", "")).strip()
    manual = manual_decision_for(row, decisions)
    manual_decision = str(manual.get("human_decision", manual.get("adoption_status", ""))).strip()
    manual_decision = manual_decision if manual_decision in ALLOWED_MANUAL_DECISIONS else ""
    if manual_decision:
        adoption_status = manual_decision
        adoption_source = "manual"
        human_recorded = True
        action = "no_action" if manual_decision in {"rejected", "blocked", "superseded"} else "manual_review"
        reason = str(manual.get("decision_reason", manual.get("notes", "manual decision recorded")))
    else:
        adoption_status, action, reason = derived_status(review_decision)
        adoption_source = "derived_from_review"
        human_recorded = False

    return {
        "generated_at_jst": generated_at_jst,
        "proposal_id": str(row.get("proposal_id", "")),
        "patch_id": str(row.get("patch_id", "")),
        "category": str(row.get("category", "")),
        "target": str(row.get("target", "")),
        "weight_path": str(row.get("weight_path", "")),
        "review_decision": review_decision,
        "adoption_status": adoption_status,
        "adoption_source": adoption_source,
        "human_decision": manual_decision,
        "human_decision_recorded": human_recorded,
        "human_decision_date": str(manual.get("human_decision_date", manual.get("decision_date", ""))) if manual else "",
        "recommended_next_action": action,
        "tracking_reason": reason,
        "sample_count": parse_int(row.get("sample_count", 0)),
        "confidence_level": str(row.get("confidence_level", "")),
        "proposal_strength": str(row.get("proposal_strength", "")),
        "proposal_direction": str(row.get("proposal_direction", "")),
        "proposed_delta": parse_float(row.get("proposed_delta", 0)),
        "patch_risk_level": str(row.get("patch_risk_level", "")),
        "evidence_quality": str(row.get("evidence_quality", "")),
        "requires_human_approval": True,
        "patch_applied": False,
        "weights_json_updated": False,
        "rationale": str(row.get("rationale", "")),
    }


def build_tracking_rows(review: pd.DataFrame, patches: pd.DataFrame, proposals: pd.DataFrame, decisions: pd.DataFrame, generated_at_jst: str) -> pd.DataFrame:
    source = merge_rows(review, patches, proposals)
    if source.empty:
        return pd.DataFrame(columns=TRACKING_COLUMNS)
    rows = [adoption_row(row, decisions, generated_at_jst) for _, row in source.iterrows()]
    return pd.DataFrame(rows, columns=TRACKING_COLUMNS)


def summary_from(tracking: pd.DataFrame, review_payload: dict[str, Any], generated_at_jst: str, generated_at_utc: str) -> dict[str, Any]:
    status = tracking.get("adoption_status", pd.Series(dtype=str))
    source = tracking.get("adoption_source", pd.Series(dtype=str))
    total = int(len(tracking))
    accepted = int((status == "accepted").sum()) if total else 0
    pending = int((status == "pending_review").sum()) if total else 0
    held = int((status == "held").sum()) if total else 0
    rejected = int((status == "rejected").sum()) if total else 0
    blocked = int((status == "blocked").sum()) if total else 0
    superseded = int((status == "superseded").sum()) if total else 0
    if pending:
        next_action = "manual_review"
    elif held:
        next_action = "wait_for_more_data"
    else:
        next_action = "no_action"
    return {
        "generated_at_jst": generated_at_jst,
        "generated_at_utc": generated_at_utc,
        "tracking_status": "unavailable" if total == 0 else "active",
        "total_tracked_proposals": total,
        "accepted_count": accepted,
        "pending_review_count": pending,
        "held_count": held,
        "rejected_count": rejected,
        "blocked_count": blocked,
        "superseded_count": superseded,
        "manual_decision_count": int((source == "manual").sum()) if total else 0,
        "derived_decision_count": int((source == "derived_from_review").sum()) if total else 0,
        "requires_human_approval": True,
        "weights_json_updated": False,
        "patch_applied": False,
        "recommended_next_action": next_action,
        "review_status": review_payload.get("review_status", "unavailable") if isinstance(review_payload, dict) else "unavailable",
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


def render_markdown(summary: dict[str, Any], tracking: pd.DataFrame) -> str:
    pending = tracking[tracking["adoption_status"] == "pending_review"] if not tracking.empty else pd.DataFrame()
    held = tracking[tracking["adoption_status"] == "held"] if not tracking.empty else pd.DataFrame()
    final = tracking[tracking["adoption_status"].isin(["accepted", "rejected", "blocked", "superseded"])] if not tracking.empty else pd.DataFrame()
    cols = ["proposal_id", "weight_path", "review_decision", "adoption_status", "adoption_source", "recommended_next_action", "sample_count", "confidence_level", "proposal_strength", "tracking_reason"]
    return f"""# Proposal Adoption Tracking

## 1. 概要

- 生成日時JST: {summary["generated_at_jst"]}
- tracking_status: {summary["tracking_status"]}
- review_status: {summary["review_status"]}
- total_tracked_proposals: {summary["total_tracked_proposals"]}
- accepted_count: {summary["accepted_count"]}
- pending_review_count: {summary["pending_review_count"]}
- held_count: {summary["held_count"]}
- rejected_count: {summary["rejected_count"]}
- blocked_count: {summary["blocked_count"]}
- superseded_count: {summary["superseded_count"]}
- manual_decision_count: {summary["manual_decision_count"]}
- derived_decision_count: {summary["derived_decision_count"]}
- recommended_next_action: {summary["recommended_next_action"]}
- requires_human_approval: true
- patch_applied: false
- weights_json_updated: false

## 2. 承認判断待ち

{markdown_table(pending[cols] if not pending.empty else pending)}

## 3. 保留中

{markdown_table(held[cols] if not held.empty else held)}

## 4. 確定済みまたはブロック済み

{markdown_table(final[cols] if not final.empty else final)}

## 5. 注意

- このレポートは提案の採用状態を追跡するだけです
- weights.jsonは更新しません
- patchは適用しません
- 実売買・発注・XM操作は行いません
- 手動判断ファイルがない場合はWeights Patch Reviewから状態を自動導出します
"""


def build_adoption_tracking() -> tuple[pd.DataFrame, dict[str, Any], str]:
    generated_dt_utc = now_utc()
    generated_at_jst = format_jst(generated_dt_utc)
    generated_at_utc = format_utc(generated_dt_utc)
    review, review_payload = load_review()
    patches = load_patch_rows()
    proposals = load_model_state_rows()
    decisions = load_manual_decisions()
    tracking = build_tracking_rows(review, patches, proposals, decisions, generated_at_jst)
    summary = summary_from(tracking, review_payload, generated_at_jst, generated_at_utc)
    payload = {
        **summary,
        "source": {
            "weights_patch_review": "results/weights_patch_review.json",
            "weights_patch_proposal": "results/weights_patch_proposal.json",
            "model_state_update_proposals": "results/model_state_update_proposals.json",
            "manual_decisions_json": "config/proposal_adoption_decisions.json",
            "manual_decisions_csv": "config/proposal_adoption_decisions.csv",
        },
        "safety": {
            "weights_json_updated": False,
            "patch_applied": False,
            "requires_human_approval": True,
            "apply_automatically": False,
        },
        "adoptions": tracking.to_dict(orient="records"),
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_date = generated_at_jst[:10]
    csv_path = RESULTS_DIR / "proposal_adoption_tracking.csv"
    json_path = RESULTS_DIR / "proposal_adoption_tracking.json"
    summary_path = RESULTS_DIR / "proposal_adoption_tracking_summary.json"
    report_path = REPORTS_DIR / f"{report_date}_proposal_adoption_tracking.md"
    tracking.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    report_path.write_text(render_markdown(summary, tracking), encoding="utf-8")
    print(f"proposal adoption tracking generated: {report_path}")
    print(f"proposal adoption tracking rows: {len(tracking)}")
    return tracking, summary, str(report_path)


def main() -> int:
    build_adoption_tracking()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
