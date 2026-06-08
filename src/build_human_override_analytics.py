from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from time_utils import format_jst, format_utc, now_utc


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/model_state")
ADOPTION_JSON = RESULTS_DIR / "proposal_adoption_tracking.json"
ADOPTION_CSV = RESULTS_DIR / "proposal_adoption_tracking.csv"
WEIGHT_HISTORY_JSON = RESULTS_DIR / "weight_version_history.json"
WEIGHT_HISTORY_CSV = RESULTS_DIR / "weight_version_history.csv"
IMPACT_JSON = RESULTS_DIR / "proposal_impact.json"
IMPACT_CSV = RESULTS_DIR / "proposal_impact.csv"
META_JSON = RESULTS_DIR / "meta_learning.json"
META_CSV = RESULTS_DIR / "meta_learning.csv"
AUTO_CALIBRATION_JSON = RESULTS_DIR / "auto_calibration_candidates.json"
AUTO_CALIBRATION_CSV = RESULTS_DIR / "auto_calibration_candidates.csv"
ANALYTICS_COLUMNS = [
    "generated_at_jst",
    "proposal_id",
    "review_decision",
    "adoption_status",
    "override_type",
    "override_reason",
    "impact_status",
    "impact_score",
    "source",
    "category",
    "target",
    "confidence_level",
    "sample_count",
    "recommended_next_action",
    "requires_human_approval",
    "patch_applied",
    "weights_json_updated",
    "generate_signal_updated",
    "apply_automatically",
]
OVERRIDE_TYPES = {"accepted", "held", "rejected", "blocked", "unknown"}


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


def rows_from_payload(payload: Any, keys: list[str]) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if not isinstance(payload, dict):
        return []
    for key in keys:
        rows = payload.get(key, [])
        if isinstance(rows, list):
            return [row for row in rows if isinstance(row, dict)]
    return []


def load_table(json_path: Path, csv_path: Path, row_keys: list[str]) -> tuple[pd.DataFrame, dict[str, Any]]:
    payload = read_json(json_path, {})
    rows = rows_from_payload(payload, row_keys) if payload else []
    if rows:
        return normalize_headers(pd.DataFrame(rows)), payload if isinstance(payload, dict) else {}
    return read_csv(csv_path), payload if isinstance(payload, dict) else {}


def load_inputs() -> dict[str, Any]:
    adoption, adoption_payload = load_table(ADOPTION_JSON, ADOPTION_CSV, ["adoptions", "proposal_adoptions", "rows"])
    history, history_payload = load_table(WEIGHT_HISTORY_JSON, WEIGHT_HISTORY_CSV, ["proposals", "history", "versions", "rows"])
    impact, impact_payload = load_table(IMPACT_JSON, IMPACT_CSV, ["proposal_impacts", "impacts", "proposal_impact", "impact_rows"])
    meta, meta_payload = load_table(META_JSON, META_CSV, ["meta_learning_candidates", "candidates", "rows"])
    auto, auto_payload = load_table(AUTO_CALIBRATION_JSON, AUTO_CALIBRATION_CSV, ["candidates", "auto_calibration_candidates", "rows"])
    return {
        "adoption": adoption,
        "adoption_payload": adoption_payload,
        "history": history,
        "history_payload": history_payload,
        "impact": impact,
        "impact_payload": impact_payload,
        "meta": meta,
        "meta_payload": meta_payload,
        "auto": auto,
        "auto_payload": auto_payload,
    }


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()


def numeric(value: Any, default: float = 0.0) -> float:
    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number):
        return default
    return float(number)


def integer(value: Any, default: int = 0) -> int:
    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number):
        return default
    return int(number)


def first_present(row: pd.Series | dict[str, Any], columns: list[str], default: Any = "") -> Any:
    for col in columns:
        if col in row:
            value = row.get(col)  # type: ignore[union-attr]
            if clean_text(value):
                return value
    return default


def row_key(row: pd.Series | dict[str, Any]) -> str:
    return clean_text(first_present(row, ["proposal_id", "patch_id", "candidate_id", "meta_learning_id", "version_id"], ""))


def keyed_lookup(df: pd.DataFrame) -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    if df.empty:
        return lookup
    for _, row in df.iterrows():
        data = row.to_dict()
        for key_col in ("proposal_id", "patch_id", "candidate_id", "meta_learning_id", "version_id"):
            key = clean_text(row.get(key_col, ""))
            if key:
                lookup[key] = data
    return lookup


def primary_rows(adoption: pd.DataFrame, history: pd.DataFrame, impact: pd.DataFrame, meta: pd.DataFrame, auto: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    if not adoption.empty:
        return adoption.copy(), "proposal_adoption_tracking"
    if not history.empty:
        return history.copy(), "weight_version_history"
    if not impact.empty:
        return impact.copy(), "proposal_impact"
    if not meta.empty:
        return meta.copy(), "meta_learning"
    if not auto.empty:
        return auto.copy(), "auto_calibration_candidates"
    return pd.DataFrame(), "unavailable"


def override_type_from(review_decision: str, adoption_status: str) -> str:
    review_decision = clean_text(review_decision).lower()
    adoption_status = clean_text(adoption_status).lower()
    text = adoption_status or review_decision
    if text in {"accepted", "approved", "approve"}:
        return "accepted"
    if text in {"held", "hold", "pending_review", "candidate", "tracked", "unreviewed", "superseded"}:
        return "held"
    if text in {"rejected", "reject"}:
        return "rejected"
    if text == "blocked":
        return "blocked"
    return "unknown"


def impact_score_from(row: dict[str, Any]) -> float:
    return numeric(first_present(row, ["impact_score", "impact_r_delta", "total_r_delta", "r_delta", "delta_r", "suggested_delta"], 0.0), 0.0)


def impact_status_from(score: float, has_impact: bool) -> str:
    if not has_impact:
        return "unknown"
    if score > 0:
        return "positive"
    if score < 0:
        return "negative"
    return "neutral"


def merged_context(row: pd.Series, source: str, lookups: list[dict[str, dict[str, Any]]]) -> dict[str, Any]:
    data = row.to_dict()
    keys = [clean_text(row.get(col, "")) for col in ("proposal_id", "patch_id", "candidate_id", "meta_learning_id", "version_id")]
    for lookup in lookups:
        for key in keys:
            if key and key in lookup:
                for col, value in lookup[key].items():
                    if not clean_text(data.get(col, "")):
                        data[col] = value
                break
    data["_source"] = source
    return data


def analytics_row(row: pd.Series, source: str, lookups: list[dict[str, dict[str, Any]]], generated_at_jst: str) -> dict[str, Any]:
    data = merged_context(row, source, lookups)
    proposal_id = row_key(data)
    review_decision = clean_text(first_present(data, ["review_decision", "human_decision", "review_status"], ""))
    adoption_status = clean_text(first_present(data, ["adoption_status", "classification", "impact_direction"], ""))
    override_type = override_type_from(review_decision, adoption_status)
    has_impact = any(clean_text(data.get(col, "")) for col in ("impact_score", "impact_r_delta", "total_r_delta", "r_delta", "delta_r"))
    score = impact_score_from(data)
    impact_status = impact_status_from(score, has_impact)
    reason = clean_text(first_present(data, ["tracking_reason", "review_reason", "rationale", "learning_hypothesis", "evidence_summary"], ""))
    if not reason:
        reason = "override source available; outcome not yet measured" if override_type != "unknown" else "human override data unavailable"
    return {
        "generated_at_jst": generated_at_jst,
        "proposal_id": proposal_id,
        "review_decision": review_decision,
        "adoption_status": adoption_status,
        "override_type": override_type if override_type in OVERRIDE_TYPES else "unknown",
        "override_reason": reason,
        "impact_status": impact_status,
        "impact_score": score,
        "source": source,
        "category": clean_text(first_present(data, ["category", "target_type", "proposal_type"], "")),
        "target": clean_text(first_present(data, ["target", "target_name", "asset", "weight_path"], "")),
        "confidence_level": clean_text(first_present(data, ["confidence_level", "proposal_strength"], "")),
        "sample_count": integer(first_present(data, ["sample_count", "sample_size", "evaluated_count"], 0), 0),
        "recommended_next_action": "human_review" if override_type == "accepted" and impact_status == "unknown" else "wait_for_more_data" if impact_status == "unknown" else "review_override_effectiveness",
        "requires_human_approval": True,
        "patch_applied": False,
        "weights_json_updated": False,
        "generate_signal_updated": False,
        "apply_automatically": False,
    }


def build_analytics_rows(
    adoption: pd.DataFrame,
    history: pd.DataFrame,
    impact: pd.DataFrame,
    meta: pd.DataFrame,
    auto: pd.DataFrame,
    generated_at_jst: str,
) -> pd.DataFrame:
    primary, source = primary_rows(adoption, history, impact, meta, auto)
    if primary.empty:
        return pd.DataFrame(columns=ANALYTICS_COLUMNS)
    lookups = [keyed_lookup(df) for df in (impact, meta, auto, history, adoption) if not df.empty]
    rows = [analytics_row(row, source, lookups, generated_at_jst) for _, row in primary.iterrows()]
    return pd.DataFrame(rows, columns=ANALYTICS_COLUMNS)


def rate(numerator: int, denominator: int) -> float:
    return round(float(numerator / denominator), 4) if denominator else 0.0


def summary_from(analytics: pd.DataFrame, input_status: dict[str, bool], generated_at_jst: str, generated_at_utc: str) -> dict[str, Any]:
    override = analytics.get("override_type", pd.Series(dtype=str)).fillna("").astype(str) if not analytics.empty else pd.Series(dtype=str)
    impact = analytics.get("impact_status", pd.Series(dtype=str)).fillna("").astype(str) if not analytics.empty else pd.Series(dtype=str)
    impact_score = pd.to_numeric(analytics.get("impact_score", pd.Series(dtype=float)), errors="coerce") if not analytics.empty else pd.Series(dtype=float)
    total = int(len(analytics))
    accepted = int((override == "accepted").sum())
    held = int((override == "held").sum())
    rejected = int((override == "rejected").sum())
    blocked = int((override == "blocked").sum())
    unknown = int((impact == "unknown").sum())
    positive = int((impact == "positive").sum())
    negative = int((impact == "negative").sum())
    accepted_known = analytics[(override == "accepted") & (impact != "unknown")] if not analytics.empty else pd.DataFrame()
    held_known = analytics[(override == "held") & (impact != "unknown")] if not analytics.empty else pd.DataFrame()
    recommended = "wait_for_proposal_impact" if unknown >= max(1, total) else "review_successful_overrides" if positive > negative else "review_negative_overrides" if negative else "monitor"
    if total == 0 and not any(input_status.values()):
        recommended = "generate_adoption_tracking"
    return {
        "generated_at_jst": generated_at_jst,
        "generated_at_utc": generated_at_utc,
        "analytics_status": "unavailable" if total == 0 else "active",
        "total_overrides": total,
        "accepted_count": accepted,
        "held_count": held,
        "rejected_count": rejected,
        "blocked_count": blocked,
        "positive_override_count": positive,
        "negative_override_count": negative,
        "unknown_outcome_count": unknown,
        "human_acceptance_rate": rate(accepted, total),
        "human_hold_rate": rate(held, total),
        "human_rejection_rate": rate(rejected, total),
        "accepted_positive_rate": rate(int((accepted_known.get("impact_status", pd.Series(dtype=str)).astype(str) == "positive").sum()) if not accepted_known.empty else 0, len(accepted_known)),
        "accepted_negative_rate": rate(int((accepted_known.get("impact_status", pd.Series(dtype=str)).astype(str) == "negative").sum()) if not accepted_known.empty else 0, len(accepted_known)),
        "held_positive_rate": rate(int((held_known.get("impact_status", pd.Series(dtype=str)).astype(str) == "positive").sum()) if not held_known.empty else 0, len(held_known)),
        "held_negative_rate": rate(int((held_known.get("impact_status", pd.Series(dtype=str)).astype(str) == "negative").sum()) if not held_known.empty else 0, len(held_known)),
        "average_impact_score": round(float(impact_score.dropna().mean()), 4) if impact_score.notna().any() else 0.0,
        "requires_human_approval": True,
        "patch_applied": False,
        "weights_json_updated": False,
        "generate_signal_updated": False,
        "apply_automatically": False,
        "recommended_next_action": recommended,
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


def render_markdown(summary: dict[str, Any], analytics: pd.DataFrame) -> str:
    cols = ["proposal_id", "review_decision", "adoption_status", "override_type", "override_reason", "impact_status", "impact_score", "source", "recommended_next_action"]
    positive = analytics[analytics["impact_status"] == "positive"] if not analytics.empty else pd.DataFrame()
    negative = analytics[analytics["impact_status"] == "negative"] if not analytics.empty else pd.DataFrame()
    unknown = analytics[analytics["impact_status"] == "unknown"] if not analytics.empty else pd.DataFrame()
    return f"""# Human Override Analytics

## 1. 概要

- 生成日時JST: {summary["generated_at_jst"]}
- analytics_status: {summary["analytics_status"]}
- total_overrides: {summary["total_overrides"]}
- accepted_count: {summary["accepted_count"]}
- held_count: {summary["held_count"]}
- rejected_count: {summary["rejected_count"]}
- blocked_count: {summary["blocked_count"]}
- positive_override_count: {summary["positive_override_count"]}
- negative_override_count: {summary["negative_override_count"]}
- unknown_outcome_count: {summary["unknown_outcome_count"]}
- recommended_next_action: {summary["recommended_next_action"]}
- requires_human_approval: true
- patch_applied: false
- weights_json_updated: false
- generate_signal_updated: false
- apply_automatically: false

## 2. Analytics

- 人間採用率: {summary["human_acceptance_rate"]}
- 人間保留率: {summary["human_hold_rate"]}
- 人間却下率: {summary["human_rejection_rate"]}
- 採用後改善率: {summary["accepted_positive_rate"]}
- 採用後悪化率: {summary["accepted_negative_rate"]}
- 保留後改善率: {summary["held_positive_rate"]}
- 保留後悪化率: {summary["held_negative_rate"]}
- 平均impact_score: {summary["average_impact_score"]}

## 3. Positive Override

{markdown_table(positive[cols] if not positive.empty else positive)}

## 4. Negative Override

{markdown_table(negative[cols] if not negative.empty else negative)}

## 5. Unknown Outcome

{markdown_table(unknown[cols].head(20) if not unknown.empty else unknown)}

## 6. 注意事項

- 人間判断を評価するだけです
- 自動修正は禁止です
- 自動適用は禁止です
- weights.jsonは更新しません
- patchは適用しません
- generate_signal.pyは変更しません
- Google Sheetsへの書き込みは行いません
- 実売買・発注・XM操作は行いません
"""


def build_human_override_analytics() -> tuple[pd.DataFrame, dict[str, Any], str]:
    generated_dt_utc = now_utc()
    generated_at_jst = format_jst(generated_dt_utc)
    generated_at_utc = format_utc(generated_dt_utc)
    inputs = load_inputs()
    adoption = inputs["adoption"]
    history = inputs["history"]
    impact = inputs["impact"]
    meta = inputs["meta"]
    auto = inputs["auto"]
    input_status = {
        "proposal_adoption_tracking_available": bool(inputs["adoption_payload"]) or not adoption.empty,
        "weight_version_history_available": bool(inputs["history_payload"]) or not history.empty,
        "proposal_impact_available": bool(inputs["impact_payload"]) or not impact.empty,
        "meta_learning_available": bool(inputs["meta_payload"]) or not meta.empty,
        "auto_calibration_candidates_available": bool(inputs["auto_payload"]) or not auto.empty,
    }
    analytics = build_analytics_rows(adoption, history, impact, meta, auto, generated_at_jst)
    summary = summary_from(analytics, input_status, generated_at_jst, generated_at_utc)
    payload = {
        **summary,
        "source": {
            "proposal_adoption_tracking": "results/proposal_adoption_tracking.json",
            "weight_version_history": "results/weight_version_history.json",
            "proposal_impact": "results/proposal_impact.json",
            "meta_learning": "results/meta_learning.json",
            "auto_calibration_candidates": "results/auto_calibration_candidates.json",
        },
        "input_status": input_status,
        "safety": {
            "weights_json_updated": False,
            "patch_applied": False,
            "requires_human_approval": True,
            "apply_automatically": False,
            "generate_signal_updated": False,
        },
        "overrides": analytics.to_dict(orient="records"),
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_date = generated_at_jst[:10]
    csv_path = RESULTS_DIR / "human_override_analytics.csv"
    json_path = RESULTS_DIR / "human_override_analytics.json"
    summary_path = RESULTS_DIR / "human_override_analytics_summary.json"
    report_path = REPORTS_DIR / f"{report_date}_human_override_analytics.md"
    analytics.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    report_path.write_text(render_markdown(summary, analytics), encoding="utf-8")
    print(f"human override analytics generated: {report_path}")
    print(f"human override analytics rows: {len(analytics)}")
    return analytics, summary, str(report_path)


def main() -> int:
    build_human_override_analytics()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
