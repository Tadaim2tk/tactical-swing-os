from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from stat_guards import MIN_SAMPLES_WEIGHT_CHANGE
from time_utils import format_jst, format_utc, now_utc


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/model_state")
WEIGHTS_PATH = Path("models/weights.json")
PROPOSAL_JSON = RESULTS_DIR / "model_state_update_proposals.json"
PROPOSAL_CSV = RESULTS_DIR / "model_state_update_proposals.csv"
AUDIT_JSON = RESULTS_DIR / "model_state_proposal_audit.json"
AUDIT_CSV = RESULTS_DIR / "model_state_proposal_audit.csv"
MIN_WEIGHT = 0.50
MAX_WEIGHT = 1.50
CSV_COLUMNS = [
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
    "unclipped_proposed_value",
    "clipped",
    "sample_count",
    "confidence_level",
    "proposal_strength",
    "proposal_direction",
    "rationale",
    "audit_result",
    "requires_human_approval",
    "apply_automatically",
    "weights_json_updated",
]


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


def load_weights(path: Path = WEIGHTS_PATH) -> dict[str, Any]:
    weights = read_json(path, {})
    return weights if isinstance(weights, dict) else {}


def load_proposals() -> pd.DataFrame:
    payload = read_json(PROPOSAL_JSON, {})
    if isinstance(payload, dict):
        rows = payload.get("proposals", [])
        if isinstance(rows, list):
            df = normalize_headers(pd.DataFrame(rows))
            if not df.empty:
                return df
    return read_csv(PROPOSAL_CSV)


def load_audit() -> tuple[dict[str, Any], pd.DataFrame]:
    payload = read_json(AUDIT_JSON, {})
    audit_json = payload if isinstance(payload, dict) else {}
    rows = audit_json.get("audit_items", []) if audit_json else []
    if isinstance(rows, list) and rows:
        audit_csv = normalize_headers(pd.DataFrame(rows))
    else:
        audit_csv = read_csv(AUDIT_CSV)
    return audit_json, audit_csv


def weight_path(category: str, target: str) -> str:
    roots = {
        "asset": "asset_weights",
        "side": "side_weights",
        "rank": "rank_weights",
        "type": "setup_type_weights",
        "reason_code": "reason_code_weights",
        "narrative": "narrative_weights",
    }
    return f"{roots.get(category, f'{category}_weights')}.{target}"


def current_weight_for(weights: dict[str, Any], category: str, target: str) -> tuple[float, bool]:
    path = weight_path(category, target)
    root = path.split(".", 1)[0]
    table = weights.get(root, {})
    if isinstance(table, dict) and target in table:
        return parse_float(table[target], 1.0), False
    # Phase 13 used a couple of historical aliases; keep read-only compatibility.
    aliases = {
        "type": ["type_weights", "setup_types"],
        "reason_code": ["reason_codes"],
        "narrative": ["narratives"],
    }
    for alias in aliases.get(category, []):
        table = weights.get(alias, {})
        if isinstance(table, dict) and target in table:
            return parse_float(table[target], 1.0), False
    return 1.0, True


def clip_weight(value: float) -> tuple[float, bool]:
    clipped = min(MAX_WEIGHT, max(MIN_WEIGHT, value))
    return clipped, clipped != value


def audit_lookup(audit: pd.DataFrame) -> dict[str, str]:
    if audit.empty or "proposal_id" not in audit.columns:
        return {}
    lookup = {}
    for _, row in audit.iterrows():
        lookup[str(row.get("proposal_id", ""))] = str(row.get("audit_result", ""))
    return lookup


def exclusion_reason(row: pd.Series, audit_result: str, audit_status: str) -> str:
    if audit_status == "blocked":
        return "audit_status_blocked"
    if audit_result != "passed":
        return f"audit_result_{audit_result or 'missing'}"
    if parse_bool(row.get("apply_automatically", False)):
        return "apply_automatically_true"
    if str(row.get("confidence_level", "")) == "insufficient_data":
        return "insufficient_data"
    if parse_int(row.get("sample_count", 0)) < MIN_SAMPLES_WEIGHT_CHANGE:
        return "sample_count_below_30"
    if str(row.get("proposal_direction", "")) not in {"increase", "decrease"}:
        return "proposal_direction_not_increase_or_decrease"
    if parse_float(row.get("proposed_delta", 0)) == 0:
        return "proposed_delta_zero"
    if abs(parse_float(row.get("proposed_delta", 0))) > parse_float(row.get("max_allowed_delta", 0)):
        return "delta_exceeds_max_allowed"
    return ""


def eligible(row: pd.Series, audit_result: str, audit_status: str) -> bool:
    return exclusion_reason(row, audit_result, audit_status) == ""


def make_patch(row: pd.Series, weights: dict[str, Any], generated_at_jst: str, audit_result: str) -> dict[str, Any]:
    category = str(row.get("category", ""))
    target = str(row.get("target", ""))
    proposal_id = str(row.get("proposal_id", ""))
    current_weight, missing = current_weight_for(weights, category, target)
    delta = parse_float(row.get("proposed_delta", 0))
    unclipped = current_weight + delta
    proposed_value, clipped = clip_weight(unclipped)
    return {
        "generated_at_jst": generated_at_jst,
        "patch_id": f"{generated_at_jst[:10].replace('-', '')}_{proposal_id}_weights_patch",
        "proposal_id": proposal_id,
        "category": category,
        "target": target,
        "weight_path": weight_path(category, target),
        "patch_action": "add_key_proposal" if missing else "update_key_proposal",
        "current_weight": round(current_weight, 4),
        "proposed_delta": round(delta, 4),
        "proposed_value": round(proposed_value, 4),
        "unclipped_proposed_value": round(unclipped, 4),
        "clipped": bool(clipped),
        "sample_count": parse_int(row.get("sample_count", 0)),
        "confidence_level": str(row.get("confidence_level", "")),
        "proposal_strength": str(row.get("proposal_strength", "")),
        "proposal_direction": str(row.get("proposal_direction", "")),
        "rationale": str(row.get("rationale", "")),
        "audit_result": audit_result,
        "requires_human_approval": True,
        "apply_automatically": False,
        "weights_json_updated": False,
    }


def build_patch_rows(proposals: pd.DataFrame, audit: pd.DataFrame, weights: dict[str, Any], generated_at_jst: str, audit_status: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    if proposals.empty:
        return pd.DataFrame(columns=CSV_COLUMNS), pd.DataFrame()
    lookup = audit_lookup(audit)
    patches = []
    excluded = []
    for _, row in normalize_headers(proposals).iterrows():
        proposal_id = str(row.get("proposal_id", ""))
        audit_result = lookup.get(proposal_id, "")
        reason = exclusion_reason(row, audit_result, audit_status)
        if eligible(row, audit_result, audit_status):
            patches.append(make_patch(row, weights, generated_at_jst, audit_result))
        else:
            excluded.append(
                {
                    "proposal_id": proposal_id,
                    "category": row.get("category", ""),
                    "target": row.get("target", ""),
                    "exclusion_reason": reason,
                    "audit_result": audit_result,
                    "sample_count": row.get("sample_count", 0),
                    "confidence_level": row.get("confidence_level", ""),
                    "proposal_direction": row.get("proposal_direction", ""),
                    "proposed_delta": row.get("proposed_delta", 0),
                }
            )
    patch_df = pd.DataFrame(patches, columns=CSV_COLUMNS)
    excluded_df = pd.DataFrame(excluded)
    return patch_df, excluded_df


def summary_from(patches: pd.DataFrame, excluded: pd.DataFrame, total_input: int) -> dict[str, int]:
    direction = patches.get("proposal_direction", pd.Series(dtype=str))
    action = patches.get("patch_action", pd.Series(dtype=str))
    return {
        "total_input_proposals": int(total_input),
        "eligible_patch_count": int(len(patches)),
        "excluded_count": int(len(excluded)),
        "increase_count": int((direction == "increase").sum()) if not patches.empty else 0,
        "decrease_count": int((direction == "decrease").sum()) if not patches.empty else 0,
        "add_key_count": int((action == "add_key_proposal").sum()) if not patches.empty else 0,
        "update_key_count": int((action == "update_key_proposal").sum()) if not patches.empty else 0,
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


def render_markdown(payload: dict[str, Any], patches: pd.DataFrame, excluded: pd.DataFrame) -> str:
    summary = payload["summary"]
    audit_gate = payload["audit_gate"]
    patch_cols = ["weight_path", "current_weight", "proposed_delta", "proposed_value", "rationale"]
    excluded_cols = ["proposal_id", "category", "target", "exclusion_reason", "audit_result", "sample_count", "confidence_level", "proposal_direction", "proposed_delta"]
    return f"""# Weights Patch Proposal

## 1. 概要

- 生成日時JST: {payload["generated_at_jst"]}
- audit_status: {audit_gate["audit_status"]}
- 入力提案件数: {summary["total_input_proposals"]}
- patch候補数: {summary["eligible_patch_count"]}
- 除外件数: {summary["excluded_count"]}
- increase件数: {summary["increase_count"]}
- decrease件数: {summary["decrease_count"]}
- add件数: {summary["add_key_count"]}
- update件数: {summary["update_key_count"]}
- weights.json更新: false
- patch適用: false
- 人間承認: 必須

## 2. patch候補

{markdown_table(patches[patch_cols] if not patches.empty else patches)}

## 3. 除外された提案

{markdown_table(excluded[excluded_cols] if not excluded.empty else excluded)}

## 4. 注意

- このファイルは適用候補であり、weights.jsonを更新しない
- 自動適用は禁止
- 人間確認後、別フェーズで明示的に適用する
- 実売買・発注は行わない
"""


def build_weights_patch() -> tuple[pd.DataFrame, dict[str, Any], str]:
    generated_dt_utc = now_utc()
    generated_at_jst = format_jst(generated_dt_utc)
    generated_at_utc = format_utc(generated_dt_utc)
    report_date = generated_at_jst[:10]
    weights = load_weights()
    proposals = load_proposals()
    audit_json, audit = load_audit()
    audit_status = str(audit_json.get("audit_status", "unavailable") if audit_json else "unavailable")
    if audit_status not in {"passed", "warning", "blocked"}:
        audit_status = "unavailable"
    patches, excluded = build_patch_rows(proposals, audit, weights, generated_at_jst, audit_status)
    summary = summary_from(patches, excluded, len(proposals))
    audit_gate = {
        "audit_status": audit_status,
        "blocked_count": parse_int(audit_json.get("blocked_count", 0) if audit_json else 0),
        "warning_count": parse_int(audit_json.get("warning_count", 0) if audit_json else 0),
        "critical_count": parse_int(audit_json.get("critical_count", 0) if audit_json else 0),
    }
    payload = {
        "generated_at_jst": generated_at_jst,
        "generated_at_utc": generated_at_utc,
        "source": {
            "weights": "models/weights.json",
            "model_state_update_proposals": "results/model_state_update_proposals.json",
            "audit": "results/model_state_proposal_audit.json",
        },
        "safety": {
            "weights_json_updated": False,
            "patch_applied": False,
            "requires_human_approval": True,
            "apply_automatically": False,
        },
        "audit_gate": audit_gate,
        "summary": summary,
        "patches": patches.to_dict(orient="records"),
        "excluded_proposals": excluded.to_dict(orient="records"),
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = RESULTS_DIR / "weights_patch_proposal.csv"
    json_path = RESULTS_DIR / "weights_patch_proposal.json"
    summary_path = RESULTS_DIR / "weights_patch_summary.json"
    report_path = REPORTS_DIR / f"{report_date}_weights_patch_proposal.md"
    patches.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    summary_path.write_text(
        json.dumps({"generated_at_jst": generated_at_jst, **summary, "audit_gate": audit_gate, "safety": payload["safety"]}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    report_path.write_text(render_markdown(payload, patches, excluded), encoding="utf-8")
    print(f"weights patch proposal generated: {report_path}")
    print(f"weights patch proposal rows: {len(patches)}")
    return patches, payload, str(report_path)


def main() -> int:
    build_weights_patch()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
