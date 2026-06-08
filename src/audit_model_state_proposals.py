from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from time_utils import format_jst, format_utc, now_utc


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/model_state")
PROPOSAL_JSON = RESULTS_DIR / "model_state_update_proposals.json"
PROPOSAL_CSV = RESULTS_DIR / "model_state_update_proposals.csv"
AUDIT_COLUMNS = [
    "proposal_id",
    "category",
    "target",
    "audit_result",
    "severity",
    "reason",
    "sample_count",
    "confidence_level",
    "proposed_delta",
    "max_allowed_delta",
    "apply_automatically",
    "recommended_action",
]
SEVERITY_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}


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


def read_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return normalize_headers(pd.read_csv(path))
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def load_proposals() -> tuple[pd.DataFrame, str]:
    payload = read_json(PROPOSAL_JSON)
    if isinstance(payload, dict):
        rows = payload.get("proposals", [])
        if isinstance(rows, list):
            return normalize_headers(pd.DataFrame(rows)), "json"
    csv = read_csv(PROPOSAL_CSV)
    if not csv.empty:
        return csv, "csv"
    return pd.DataFrame(), "missing"


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


def stronger_severity(current: str, candidate: str) -> str:
    return candidate if SEVERITY_ORDER[candidate] > SEVERITY_ORDER[current] else current


def audit_one(row: pd.Series) -> dict[str, Any]:
    proposal_id = str(row.get("proposal_id", ""))
    category = str(row.get("category", ""))
    target = str(row.get("target", ""))
    sample_count = parse_int(row.get("sample_count", 0))
    confidence = str(row.get("confidence_level", ""))
    direction = str(row.get("proposal_direction", ""))
    strength = str(row.get("proposal_strength", ""))
    proposed_delta = parse_float(row.get("proposed_delta", 0))
    max_allowed_delta = parse_float(row.get("max_allowed_delta", 0))
    apply_automatically = parse_bool(row.get("apply_automatically", False))

    audit_result = "passed"
    severity = "low"
    reasons: list[str] = []
    action = "human_review_required"

    if apply_automatically:
        audit_result = "blocked"
        severity = "critical"
        reasons.append("automatic_application_not_allowed")
        action = "block_proposal"

    if abs(proposed_delta) > max_allowed_delta:
        audit_result = "blocked"
        severity = stronger_severity(severity, "high")
        reasons.append("delta_exceeds_max_allowed")
        action = "block_proposal"

    if confidence == "insufficient_data" and (direction != "hold" or proposed_delta != 0):
        audit_result = "blocked"
        severity = stronger_severity(severity, "high")
        reasons.append("insufficient_data_with_non_hold_proposal")
        action = "block_proposal"

    if sample_count < 5 and direction != "hold" and "insufficient_data_with_non_hold_proposal" not in reasons:
        audit_result = "warning" if audit_result == "passed" else audit_result
        severity = stronger_severity(severity, "medium")
        reasons.append("low_sample_non_hold_proposal")
        if action != "block_proposal":
            action = "review_before_any_change"

    if strength == "strong":
        strong_ok = sample_count >= 10 and confidence in {"medium", "high"} and abs(proposed_delta) > 0 and not apply_automatically
        if not strong_ok:
            audit_result = "warning" if audit_result == "passed" else audit_result
            severity = stronger_severity(severity, "medium")
            reasons.append("weak_evidence_marked_strong")
            if action != "block_proposal":
                action = "review_before_any_change"

    if not reasons:
        reasons.append("safe_proposal")
        action = "human_review_required"

    return {
        "proposal_id": proposal_id,
        "category": category,
        "target": target,
        "audit_result": audit_result,
        "severity": severity,
        "reason": "|".join(reasons),
        "sample_count": sample_count,
        "confidence_level": confidence,
        "proposed_delta": proposed_delta,
        "max_allowed_delta": max_allowed_delta,
        "apply_automatically": bool(apply_automatically),
        "recommended_action": action,
    }


def audit_proposals(proposals: pd.DataFrame) -> pd.DataFrame:
    if proposals.empty:
        return pd.DataFrame(columns=AUDIT_COLUMNS)
    rows = [audit_one(row) for _, row in normalize_headers(proposals).iterrows()]
    return pd.DataFrame(rows, columns=AUDIT_COLUMNS)


def audit_status(audit: pd.DataFrame, source: str) -> str:
    if source == "missing":
        return "unavailable"
    if audit.empty:
        return "unavailable"
    if (audit["audit_result"] == "blocked").any():
        return "blocked"
    if (audit["audit_result"] == "warning").any():
        return "warning"
    return "passed"


def build_payload(audit: pd.DataFrame, source: str, generated_at_jst: str, generated_at_utc: str) -> dict[str, Any]:
    status = audit_status(audit, source)
    result = audit.get("audit_result", pd.Series(dtype=str))
    severity = audit.get("severity", pd.Series(dtype=str))
    apply_auto = audit.get("apply_automatically", pd.Series(dtype=bool)).astype(str).str.lower().isin(["true", "1", "yes"])
    return {
        "generated_at_jst": generated_at_jst,
        "generated_at_utc": generated_at_utc,
        "audit_status": status,
        "total_proposals": int(len(audit)),
        "passed_count": int((result == "passed").sum()) if not audit.empty else 0,
        "warning_count": int((result == "warning").sum()) if not audit.empty else 0,
        "blocked_count": int((result == "blocked").sum()) if not audit.empty else 0,
        "critical_count": int((severity == "critical").sum()) if not audit.empty else 0,
        "weights_json_updated": False,
        "apply_automatically_detected": bool(apply_auto.any()) if not audit.empty else False,
        "requires_human_review": True,
        "proposal_source": source,
        "audit_items": audit.to_dict(orient="records"),
    }


def markdown_table(df: pd.DataFrame, empty: str = "該当なし") -> str:
    if df.empty:
        return empty
    view = df.copy()
    cols = [str(col) for col in view.columns]
    lines = [
        "| " + " | ".join(cols) + " |",
        "| " + " | ".join(["---"] * len(cols)) + " |",
    ]
    for _, row in view.iterrows():
        values = []
        for col in view.columns:
            value = str(row.get(col, ""))
            values.append(value.replace("\n", " ").replace("|", "/"))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def render_markdown(payload: dict[str, Any], audit: pd.DataFrame) -> str:
    blocked = audit[audit["audit_result"] == "blocked"] if not audit.empty else pd.DataFrame()
    warnings = audit[audit["audit_result"] == "warning"] if not audit.empty else pd.DataFrame()
    passed = audit[audit["audit_result"] == "passed"] if not audit.empty else pd.DataFrame()
    return f"""# Model State Proposal Safety Audit

## 1. 概要

- 生成日時JST: {payload["generated_at_jst"]}
- audit_status: {payload["audit_status"]}
- total_proposals: {payload["total_proposals"]}
- warning_count: {payload["warning_count"]}
- blocked_count: {payload["blocked_count"]}
- critical_count: {payload["critical_count"]}
- weights_json_updated: false
- requires_human_review: true

## 2. ブロック対象

{markdown_table(blocked)}

## 3. 警告対象

{markdown_table(warnings)}

## 4. 通過対象

{markdown_table(passed.head(50))}

## 5. 注意

- この監査は自動反映を許可するものではない
- weights.jsonは更新していない
- 人間確認が必須
- 実売買・発注は行わない
"""


def build_audit() -> tuple[pd.DataFrame, dict[str, Any], str]:
    generated_dt_utc = now_utc()
    generated_at_jst = format_jst(generated_dt_utc)
    generated_at_utc = format_utc(generated_dt_utc)
    report_date = generated_at_jst[:10]
    proposals, source = load_proposals()
    audit = audit_proposals(proposals)
    payload = build_payload(audit, source, generated_at_jst, generated_at_utc)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = RESULTS_DIR / "model_state_proposal_audit.csv"
    json_path = RESULTS_DIR / "model_state_proposal_audit.json"
    report_path = REPORTS_DIR / f"{report_date}_model_state_proposal_audit.md"

    audit.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    report_path.write_text(render_markdown(payload, audit), encoding="utf-8")
    print(f"model state proposal audit generated: {report_path}")
    print(f"model state proposal audit status: {payload['audit_status']}")
    return audit, payload, str(report_path)


def main() -> int:
    build_audit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
