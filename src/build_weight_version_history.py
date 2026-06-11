from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from time_utils import format_jst, format_utc, now_utc


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/model_state")
WEIGHTS_PATH = Path("models/weights.json")
ADOPTION_JSON = RESULTS_DIR / "proposal_adoption_tracking.json"
ADOPTION_CSV = RESULTS_DIR / "proposal_adoption_tracking.csv"
REVIEW_JSON = RESULTS_DIR / "weights_patch_review.json"
REVIEW_CSV = RESULTS_DIR / "weights_patch_review.csv"
MODEL_STATE_JSON = RESULTS_DIR / "model_state_update_proposals.json"
MODEL_STATE_CSV = RESULTS_DIR / "model_state_update_proposals.csv"
HISTORY_COLUMNS = [
    "version_id",
    "created_at_jst",
    "created_at_utc",
    "source",
    "proposal_id",
    "review_decision",
    "adoption_status",
    "description",
    "weights_json_updated",
    "patch_applied",
    "requires_human_approval",
    "notes",
]
ALLOWED_HISTORY_STATUSES = {"tracked", "held", "candidate", "approved", "rejected", "blocked"}


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


def load_adoptions() -> tuple[pd.DataFrame, dict[str, Any]]:
    payload = read_json(ADOPTION_JSON, {})
    if isinstance(payload, dict):
        rows = payload.get("adoptions", [])
        if isinstance(rows, list):
            return normalize_headers(pd.DataFrame(rows)), payload
    return read_csv(ADOPTION_CSV), {}


def load_review() -> tuple[pd.DataFrame, dict[str, Any]]:
    payload = read_json(REVIEW_JSON, {})
    if isinstance(payload, dict):
        rows = payload.get("patch_review", [])
        if isinstance(rows, list):
            return normalize_headers(pd.DataFrame(rows)), payload
    return read_csv(REVIEW_CSV), {}


def load_model_state_proposals() -> tuple[pd.DataFrame, dict[str, Any]]:
    payload = read_json(MODEL_STATE_JSON, {})
    if isinstance(payload, dict):
        rows = payload.get("proposals", [])
        if isinstance(rows, list):
            return normalize_headers(pd.DataFrame(rows)), payload
    return read_csv(MODEL_STATE_CSV), {}


def load_weights() -> dict[str, Any]:
    payload = read_json(WEIGHTS_PATH, {})
    return payload if isinstance(payload, dict) else {}


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()


def adoption_to_history_status(status: str, review_decision: str = "") -> str:
    status = clean_text(status)
    review_decision = clean_text(review_decision)
    mapping = {
        "accepted": "approved",
        "approved": "approved",
        "pending_review": "candidate",
        "candidate": "candidate",
        "held": "held",
        "hold": "held",
        "rejected": "rejected",
        "reject": "rejected",
        "blocked": "blocked",
        "superseded": "tracked",
        "tracked": "tracked",
        "unreviewed": "tracked",
    }
    if status in mapping:
        return mapping[status]
    if review_decision in mapping:
        return mapping[review_decision]
    return "tracked"


def review_to_history_status(review_decision: str) -> str:
    return adoption_to_history_status("", review_decision)


def proposal_to_history_status(row: pd.Series) -> str:
    direction = clean_text(row.get("proposal_direction", ""))
    confidence = clean_text(row.get("confidence_level", ""))
    if confidence == "insufficient_data" or direction == "hold":
        return "held"
    if direction in {"increase", "decrease"}:
        return "tracked"
    return "tracked"


def pick_description(row: pd.Series) -> str:
    for col in ("tracking_reason", "review_reason", "rationale", "description", "proposed_change"):
        value = clean_text(row.get(col, ""))
        if value:
            return value
    proposal_id = clean_text(row.get("proposal_id", ""))
    return f"history tracking for {proposal_id}" if proposal_id else "history tracking placeholder"


def history_row(row: pd.Series, source: str, generated_at_jst: str, generated_at_utc: str, status: str | None = None) -> dict[str, Any]:
    review_decision = clean_text(row.get("review_decision", ""))
    proposal_id = clean_text(row.get("proposal_id", row.get("patch_id", "")))
    adoption_status = status or adoption_to_history_status(clean_text(row.get("adoption_status", "")), review_decision)
    if adoption_status not in ALLOWED_HISTORY_STATUSES:
        adoption_status = "tracked"
    return {
        "version_id": "v1",
        "created_at_jst": generated_at_jst,
        "created_at_utc": generated_at_utc,
        "source": source,
        "proposal_id": proposal_id,
        "review_decision": review_decision,
        "adoption_status": adoption_status,
        "description": pick_description(row),
        "weights_json_updated": False,
        "patch_applied": False,
        "requires_human_approval": True,
        "notes": "history_only_no_weight_change",
    }


def build_history_rows(adoptions: pd.DataFrame, review: pd.DataFrame, proposals: pd.DataFrame, generated_at_jst: str, generated_at_utc: str) -> pd.DataFrame:
    if not adoptions.empty:
        rows = [history_row(row, "proposal_adoption_tracking", generated_at_jst, generated_at_utc) for _, row in adoptions.iterrows()]
        return pd.DataFrame(rows, columns=HISTORY_COLUMNS)
    if not review.empty:
        rows = [
            history_row(row, "weights_patch_review", generated_at_jst, generated_at_utc, review_to_history_status(clean_text(row.get("review_decision", ""))))
            for _, row in review.iterrows()
        ]
        return pd.DataFrame(rows, columns=HISTORY_COLUMNS)
    if not proposals.empty:
        rows = [history_row(row, "model_state_update_proposals", generated_at_jst, generated_at_utc, proposal_to_history_status(row)) for _, row in proposals.iterrows()]
        return pd.DataFrame(rows, columns=HISTORY_COLUMNS)
    return pd.DataFrame(columns=HISTORY_COLUMNS)


def summary_from(history: pd.DataFrame, adoption_payload: dict[str, Any], review_payload: dict[str, Any], weights: dict[str, Any], generated_at_jst: str, generated_at_utc: str) -> dict[str, Any]:
    status = history.get("adoption_status", pd.Series(dtype=str)).fillna("").astype(str) if not history.empty else pd.Series(dtype=str)
    review_status = "unavailable"
    if isinstance(review_payload, dict) and review_payload:
        review_status = clean_text(review_payload.get("review_status", "unavailable")) or "unavailable"
    elif isinstance(adoption_payload, dict) and adoption_payload:
        review_status = clean_text(adoption_payload.get("review_status", "unavailable")) or "unavailable"
    current_version = clean_text(weights.get("current_version", "v1")) or "v1"
    return {
        "generated_at_jst": generated_at_jst,
        "generated_at_utc": generated_at_utc,
        "current_version": current_version,
        "version_count": 1,
        "tracked_count": int((status == "tracked").sum()),
        "held_count": int((status == "held").sum()),
        "candidate_count": int((status == "candidate").sum()),
        "approved_count": int((status == "approved").sum()),
        "rejected_count": int((status == "rejected").sum()),
        "blocked_count": int((status == "blocked").sum()),
        "weights_json_updated": False,
        "patch_applied": False,
        "requires_human_approval": True,
        "review_status": review_status,
        "history_status": "unavailable" if history.empty else "tracked",
        "total_history_records": int(len(history)),
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
            value = clean_text(row.get(col, ""))
            values.append(value.replace("\n", " ").replace("|", "/"))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def render_markdown(summary: dict[str, Any], history: pd.DataFrame) -> str:
    version_view = pd.DataFrame(
        [
            {
                "version_id": summary["current_version"],
                "version_count": summary["version_count"],
                "weights_json_updated": summary["weights_json_updated"],
                "patch_applied": summary["patch_applied"],
                "requires_human_approval": summary["requires_human_approval"],
            }
        ]
    )
    proposal_cols = [
        "version_id",
        "source",
        "proposal_id",
        "review_decision",
        "adoption_status",
        "description",
        "weights_json_updated",
        "patch_applied",
        "requires_human_approval",
        "notes",
    ]
    return f"""# Weight Version History

## 1. 概要

- 生成日時JST: {summary["generated_at_jst"]}
- 現在Version: {summary["current_version"]}
- Version数: {summary["version_count"]}
- review_status: {summary["review_status"]}
- history_status: {summary["history_status"]}
- tracked_count: {summary["tracked_count"]}
- held_count: {summary["held_count"]}
- candidate_count: {summary["candidate_count"]}
- approved_count: {summary["approved_count"]}
- rejected_count: {summary["rejected_count"]}
- blocked_count: {summary["blocked_count"]}
- weights_json_updated: false
- patch_applied: false
- requires_human_approval: true

## 2. Version一覧

{markdown_table(version_view)}

## 3. Proposal一覧

{markdown_table(history[proposal_cols] if not history.empty else history)}

## 4. 注意事項

- 実際のweight変更はしていません
- weights.jsonは更新しません
- patchは適用しません
- 人間承認が必要です
- 実売買・発注・XM操作は行いません
- この履歴はProposal/Review/Adoption Trackingを長期追跡するための研究用ビューです
"""


def build_weight_version_history() -> tuple[pd.DataFrame, dict[str, Any], str]:
    generated_dt_utc = now_utc()
    generated_at_jst = format_jst(generated_dt_utc)
    generated_at_utc = format_utc(generated_dt_utc)
    adoptions, adoption_payload = load_adoptions()
    review, review_payload = load_review()
    proposals, model_state_payload = load_model_state_proposals()
    weights = load_weights()
    history = build_history_rows(adoptions, review, proposals, generated_at_jst, generated_at_utc)
    summary = summary_from(history, adoption_payload, review_payload, weights, generated_at_jst, generated_at_utc)
    payload = {
        **summary,
        "source": {
            "proposal_adoption_tracking": "results/proposal_adoption_tracking.json",
            "weights_patch_review": "results/weights_patch_review.json",
            "model_state_update_proposals": "results/model_state_update_proposals.json",
            "weights": "models/weights.json",
        },
        "safety": {
            "weights_json_updated": False,
            "patch_applied": False,
            "requires_human_approval": True,
            "apply_automatically": False,
        },
        "input_status": {
            "proposal_adoption_tracking_available": bool(adoption_payload) or not adoptions.empty,
            "weights_patch_review_available": bool(review_payload) or not review.empty,
            "model_state_update_proposals_available": bool(model_state_payload) or not proposals.empty,
            "weights_available": bool(weights),
        },
        "versions": [
            {
                "version_id": summary["current_version"],
                "created_at_jst": generated_at_jst,
                "created_at_utc": generated_at_utc,
                "description": "Initial fixed version for history tracking; weights.json is not updated in this phase.",
                "weights_json_updated": False,
                "patch_applied": False,
                "requires_human_approval": True,
            }
        ],
        "proposals": history.to_dict(orient="records"),
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_date = generated_at_jst[:10]
    csv_path = RESULTS_DIR / "weight_version_history.csv"
    json_path = RESULTS_DIR / "weight_version_history.json"
    summary_path = RESULTS_DIR / "weight_version_history_summary.json"
    report_path = REPORTS_DIR / f"{report_date}_weight_version_history.md"
    history.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    report_path.write_text(render_markdown(summary, history), encoding="utf-8")
    print(f"weight version history generated: {report_path}")
    print(f"weight version history rows: {len(history)}")
    return history, summary, str(report_path)


def main() -> int:
    build_weight_version_history()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
