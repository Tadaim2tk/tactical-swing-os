from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from time_utils import format_jst, format_utc, now_utc


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/model_state")
META_LEARNING_JSON = RESULTS_DIR / "meta_learning.json"
META_LEARNING_CSV = RESULTS_DIR / "meta_learning.csv"
PROPOSAL_IMPACT_JSON = RESULTS_DIR / "proposal_impact.json"
PROPOSAL_IMPACT_CSV = RESULTS_DIR / "proposal_impact.csv"
ADOPTION_JSON = RESULTS_DIR / "proposal_adoption_tracking.json"
ADOPTION_CSV = RESULTS_DIR / "proposal_adoption_tracking.csv"
WEIGHT_HISTORY_JSON = RESULTS_DIR / "weight_version_history.json"
WEIGHT_HISTORY_CSV = RESULTS_DIR / "weight_version_history.csv"

VALUE_MIN = 0.50
VALUE_MAX = 1.50
CANDIDATE_COLUMNS = [
    "generated_at_jst",
    "candidate_id",
    "proposal_id",
    "asset",
    "category",
    "target",
    "factor",
    "current_value",
    "suggested_delta",
    "suggested_value",
    "confidence",
    "confidence_level",
    "sample_size",
    "source",
    "classification",
    "recommended_next_action",
    "rationale",
    "requires_human_approval",
    "patch_applied",
    "weights_json_updated",
    "generate_signal_updated",
    "apply_automatically",
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


def load_meta_learning() -> tuple[pd.DataFrame, dict[str, Any]]:
    payload = read_json(META_LEARNING_JSON, {})
    rows = rows_from_payload(payload, ["meta_learning_candidates", "candidates", "rows"]) if payload else []
    if rows:
        return normalize_headers(pd.DataFrame(rows)), payload if isinstance(payload, dict) else {}
    return read_csv(META_LEARNING_CSV), payload if isinstance(payload, dict) else {}


def load_proposal_impact() -> tuple[pd.DataFrame, dict[str, Any]]:
    payload = read_json(PROPOSAL_IMPACT_JSON, {})
    rows = rows_from_payload(payload, ["proposal_impacts", "impacts", "proposal_impact", "impact_rows"]) if payload else []
    if rows:
        return normalize_headers(pd.DataFrame(rows)), payload if isinstance(payload, dict) else {}
    return read_csv(PROPOSAL_IMPACT_CSV), payload if isinstance(payload, dict) else {}


def load_adoptions() -> tuple[pd.DataFrame, dict[str, Any]]:
    payload = read_json(ADOPTION_JSON, {})
    rows = rows_from_payload(payload, ["adoptions", "proposal_adoptions", "rows"]) if payload else []
    if rows:
        return normalize_headers(pd.DataFrame(rows)), payload if isinstance(payload, dict) else {}
    return read_csv(ADOPTION_CSV), payload if isinstance(payload, dict) else {}


def load_weight_history() -> tuple[pd.DataFrame, dict[str, Any]]:
    payload = read_json(WEIGHT_HISTORY_JSON, {})
    rows = rows_from_payload(payload, ["proposals", "versions", "history", "rows"]) if payload else []
    if rows:
        return normalize_headers(pd.DataFrame(rows)), payload if isinstance(payload, dict) else {}
    return read_csv(WEIGHT_HISTORY_CSV), payload if isinstance(payload, dict) else {}


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


def first_present(row: pd.Series, columns: list[str], default: Any = "") -> Any:
    for col in columns:
        if col in row.index:
            value = row.get(col)
            if clean_text(value):
                return value
    return default


def factor_for(category: str, target: str) -> str:
    category = clean_text(category) or "general"
    mapping = {
        "asset": "asset_weight",
        "side": "side_weight",
        "rank": "rank_weight",
        "type": "setup_type_weight",
        "reason_code": "reason_code_weight",
        "narrative": "narrative_weight",
    }
    if category in mapping:
        return mapping[category]
    if target:
        return f"{category}_weight"
    return "general_weight"


def confidence_score(confidence_level: str, sample_size: int, magnitude: float) -> float:
    base = {
        "high": 0.78,
        "medium": 0.62,
        "low": 0.46,
        "insufficient_data": 0.20,
    }.get(clean_text(confidence_level), 0.40)
    sample_boost = min(max(sample_size, 0), 40) / 200.0
    magnitude_boost = min(abs(magnitude), 1.0) * 0.10
    return round(min(0.95, max(0.0, base + sample_boost + magnitude_boost)), 4)


def classification_from_meta(pattern_type: str, impact_direction: str, confidence_level: str, sample_size: int) -> str:
    if clean_text(confidence_level) == "insufficient_data" or sample_size < 5:
        return "insufficient_data"
    pattern_type = clean_text(pattern_type)
    impact_direction = clean_text(impact_direction)
    if pattern_type == "success_pattern" and impact_direction == "positive":
        return "increase"
    if pattern_type == "failure_pattern" and impact_direction == "negative":
        return "decrease"
    return "hold"


def classification_from_impact(impact: float, confidence_level: str, sample_size: int) -> str:
    if clean_text(confidence_level) == "insufficient_data" or sample_size < 5:
        return "insufficient_data"
    if impact >= 0.5:
        return "increase"
    if impact <= -0.5:
        return "decrease"
    return "hold"


def suggested_delta(classification: str, confidence: float, impact: float) -> float:
    if classification == "increase":
        return round(min(0.10, max(0.01, confidence * 0.08 + max(impact, 0.0) * 0.02)), 4)
    if classification == "decrease":
        return round(max(-0.10, min(-0.01, -(confidence * 0.08 + abs(min(impact, 0.0)) * 0.02))), 4)
    return 0.0


def candidate_row_from_meta(row: pd.Series, generated_at_jst: str, sequence: int) -> dict[str, Any]:
    proposal_id = clean_text(first_present(row, ["proposal_id", "meta_learning_id"], f"meta_{sequence}"))
    category = clean_text(first_present(row, ["category", "target_type", "proposal_type"], "general"))
    target = clean_text(first_present(row, ["target", "target_name", "asset"], ""))
    asset = target if category == "asset" else clean_text(first_present(row, ["asset"], ""))
    sample_size = integer(first_present(row, ["sample_count", "sample_size", "evaluated_count"], 0), 0)
    confidence_level = clean_text(first_present(row, ["confidence_level"], "low")) or "low"
    impact = numeric(first_present(row, ["impact_score", "impact_r_delta", "total_r_delta"], 0.0), 0.0)
    classification = classification_from_meta(
        clean_text(row.get("pattern_type", "")),
        clean_text(row.get("impact_direction", "")),
        confidence_level,
        sample_size,
    )
    confidence = confidence_score(confidence_level, sample_size, impact)
    delta = suggested_delta(classification, confidence, impact)
    current_value = 1.0
    unclipped = current_value + delta
    suggested = min(VALUE_MAX, max(VALUE_MIN, unclipped))
    return {
        "generated_at_jst": generated_at_jst,
        "candidate_id": f"AC_{sequence:04d}_{proposal_id}",
        "proposal_id": proposal_id,
        "asset": asset,
        "category": category,
        "target": target,
        "factor": factor_for(category, target),
        "current_value": current_value,
        "suggested_delta": delta,
        "suggested_value": round(suggested, 4),
        "confidence": confidence,
        "confidence_level": confidence_level,
        "sample_size": sample_size,
        "source": "meta_learning",
        "classification": classification,
        "recommended_next_action": "human_review" if classification in {"increase", "decrease"} else "wait_for_more_data",
        "rationale": clean_text(first_present(row, ["learning_hypothesis", "evidence_summary", "rationale"], "Meta Learning result converted to calibration candidate.")),
        "requires_human_approval": True,
        "patch_applied": False,
        "weights_json_updated": False,
        "generate_signal_updated": False,
        "apply_automatically": False,
    }


def candidate_row_from_impact(row: pd.Series, generated_at_jst: str, sequence: int) -> dict[str, Any]:
    proposal_id = clean_text(first_present(row, ["proposal_id", "patch_id"], f"impact_{sequence}"))
    category = clean_text(first_present(row, ["category", "target_type", "proposal_type"], "general"))
    target = clean_text(first_present(row, ["target", "target_name", "asset"], ""))
    asset = target if category == "asset" else clean_text(first_present(row, ["asset"], ""))
    sample_size = integer(first_present(row, ["sample_count", "post_sample_count", "evaluated_count", "sample_size"], 0), 0)
    impact = numeric(first_present(row, ["impact_score", "impact_r_delta", "total_r_delta", "r_delta", "delta_r"], 0.0), 0.0)
    confidence_level = clean_text(first_present(row, ["confidence_level"], "medium" if sample_size >= 10 else "low")) or "low"
    classification = classification_from_impact(impact, confidence_level, sample_size)
    confidence = confidence_score(confidence_level, sample_size, impact)
    delta = suggested_delta(classification, confidence, impact)
    current_value = 1.0
    return {
        "generated_at_jst": generated_at_jst,
        "candidate_id": f"AC_{sequence:04d}_{proposal_id}",
        "proposal_id": proposal_id,
        "asset": asset,
        "category": category,
        "target": target,
        "factor": factor_for(category, target),
        "current_value": current_value,
        "suggested_delta": delta,
        "suggested_value": round(min(VALUE_MAX, max(VALUE_MIN, current_value + delta)), 4),
        "confidence": confidence,
        "confidence_level": confidence_level,
        "sample_size": sample_size,
        "source": "proposal_impact",
        "classification": classification,
        "recommended_next_action": "human_review" if classification in {"increase", "decrease"} else "wait_for_more_data",
        "rationale": f"Proposal Impact fallback: impact_score={impact:.2f}, sample_size={sample_size}.",
        "requires_human_approval": True,
        "patch_applied": False,
        "weights_json_updated": False,
        "generate_signal_updated": False,
        "apply_automatically": False,
    }


def fallback_candidate(row: pd.Series, generated_at_jst: str, sequence: int, source: str) -> dict[str, Any]:
    proposal_id = clean_text(first_present(row, ["proposal_id", "patch_id", "version_id"], f"{source}_{sequence}"))
    status = clean_text(first_present(row, ["adoption_status", "review_decision"], "tracked"))
    classification = "blocked" if status == "blocked" else "hold"
    return {
        "generated_at_jst": generated_at_jst,
        "candidate_id": f"AC_{sequence:04d}_{proposal_id}",
        "proposal_id": proposal_id,
        "asset": clean_text(row.get("asset", "")),
        "category": clean_text(first_present(row, ["category", "target_type"], "general")),
        "target": clean_text(first_present(row, ["target", "target_name", "weight_path"], "")),
        "factor": factor_for(clean_text(first_present(row, ["category", "target_type"], "general")), clean_text(first_present(row, ["target", "target_name", "weight_path"], ""))),
        "current_value": 1.0,
        "suggested_delta": 0.0,
        "suggested_value": 1.0,
        "confidence": 0.20,
        "confidence_level": "insufficient_data",
        "sample_size": integer(first_present(row, ["sample_count", "sample_size"], 0), 0),
        "source": source,
        "classification": classification,
        "recommended_next_action": "wait_for_more_data",
        "rationale": "Fallback tracking row; no calibration change is suggested.",
        "requires_human_approval": True,
        "patch_applied": False,
        "weights_json_updated": False,
        "generate_signal_updated": False,
        "apply_automatically": False,
    }


def build_candidates(
    meta: pd.DataFrame,
    impact: pd.DataFrame,
    adoptions: pd.DataFrame,
    weight_history: pd.DataFrame,
    generated_at_jst: str,
) -> pd.DataFrame:
    if not meta.empty:
        rows = [candidate_row_from_meta(row, generated_at_jst, idx + 1) for idx, (_, row) in enumerate(meta.iterrows())]
    elif not impact.empty:
        rows = [candidate_row_from_impact(row, generated_at_jst, idx + 1) for idx, (_, row) in enumerate(impact.iterrows())]
    elif not adoptions.empty:
        rows = [fallback_candidate(row, generated_at_jst, idx + 1, "proposal_adoption_tracking") for idx, (_, row) in enumerate(adoptions.iterrows())]
    elif not weight_history.empty:
        rows = [fallback_candidate(row, generated_at_jst, idx + 1, "weight_version_history") for idx, (_, row) in enumerate(weight_history.iterrows())]
    else:
        rows = []
    return pd.DataFrame(rows, columns=CANDIDATE_COLUMNS)


def summary_from(candidates: pd.DataFrame, input_status: dict[str, bool], generated_at_jst: str, generated_at_utc: str) -> dict[str, Any]:
    classification = candidates.get("classification", pd.Series(dtype=str)).fillna("").astype(str) if not candidates.empty else pd.Series(dtype=str)
    recommended = "human_review" if classification.isin(["increase", "decrease"]).any() else "wait_for_more_data"
    if candidates.empty and not any(input_status.values()):
        recommended = "generate_meta_learning_or_proposal_impact"
    return {
        "generated_at_jst": generated_at_jst,
        "generated_at_utc": generated_at_utc,
        "candidate_status": "unavailable" if candidates.empty else "active",
        "candidate_count": int(len(candidates)),
        "increase_count": int((classification == "increase").sum()),
        "decrease_count": int((classification == "decrease").sum()),
        "hold_count": int((classification == "hold").sum()),
        "insufficient_data_count": int((classification == "insufficient_data").sum()),
        "blocked_count": int((classification == "blocked").sum()),
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


def render_markdown(summary: dict[str, Any], candidates: pd.DataFrame) -> str:
    top = candidates.sort_values("confidence", ascending=False).head(10) if not candidates.empty and "confidence" in candidates.columns else candidates
    blocked = candidates[candidates["classification"] == "blocked"] if not candidates.empty else pd.DataFrame()
    cols = ["candidate_id", "asset", "category", "target", "factor", "classification", "current_value", "suggested_delta", "suggested_value", "confidence", "sample_size", "source", "rationale"]
    return f"""# Auto Calibration Candidates

## 1. 概要

- 生成日時JST: {summary["generated_at_jst"]}
- candidate_status: {summary["candidate_status"]}
- candidate_count: {summary["candidate_count"]}
- increase_count: {summary["increase_count"]}
- decrease_count: {summary["decrease_count"]}
- hold_count: {summary["hold_count"]}
- insufficient_data_count: {summary["insufficient_data_count"]}
- blocked_count: {summary["blocked_count"]}
- recommended_next_action: {summary["recommended_next_action"]}
- requires_human_approval: true
- patch_applied: false
- weights_json_updated: false
- generate_signal_updated: false
- apply_automatically: false

## 2. 候補一覧

{markdown_table(top[cols] if not top.empty else top)}

## 3. ブロック/保留候補

{markdown_table(blocked[cols] if not blocked.empty else blocked)}

## 4. 注意事項

- Auto Calibration Candidatesは将来の重み変更候補を作るだけです
- weights.jsonは更新しません
- patchは適用しません
- generate_signal.pyは変更しません
- Google Sheetsへの書き込みは行いません
- 実売買・発注・XM操作は行いません
- すべての候補は人間承認が必須です
"""


def build_auto_calibration_candidates() -> tuple[pd.DataFrame, dict[str, Any], str]:
    generated_dt_utc = now_utc()
    generated_at_jst = format_jst(generated_dt_utc)
    generated_at_utc = format_utc(generated_dt_utc)
    meta, meta_payload = load_meta_learning()
    impact, impact_payload = load_proposal_impact()
    adoptions, adoption_payload = load_adoptions()
    weight_history, weight_history_payload = load_weight_history()
    input_status = {
        "meta_learning_available": bool(meta_payload) or not meta.empty,
        "proposal_impact_available": bool(impact_payload) or not impact.empty,
        "proposal_adoption_tracking_available": bool(adoption_payload) or not adoptions.empty,
        "weight_version_history_available": bool(weight_history_payload) or not weight_history.empty,
    }
    candidates = build_candidates(meta, impact, adoptions, weight_history, generated_at_jst)
    summary = summary_from(candidates, input_status, generated_at_jst, generated_at_utc)
    payload = {
        **summary,
        "source": {
            "meta_learning": "results/meta_learning.json",
            "proposal_impact": "results/proposal_impact.json",
            "proposal_adoption_tracking": "results/proposal_adoption_tracking.json",
            "weight_version_history": "results/weight_version_history.json",
        },
        "input_status": input_status,
        "safety": {
            "weights_json_updated": False,
            "patch_applied": False,
            "requires_human_approval": True,
            "apply_automatically": False,
            "generate_signal_updated": False,
        },
        "candidates": candidates.to_dict(orient="records"),
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_date = generated_at_jst[:10]
    csv_path = RESULTS_DIR / "auto_calibration_candidates.csv"
    json_path = RESULTS_DIR / "auto_calibration_candidates.json"
    summary_path = RESULTS_DIR / "auto_calibration_candidates_summary.json"
    report_path = REPORTS_DIR / f"{report_date}_auto_calibration_candidates.md"
    candidates.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    report_path.write_text(render_markdown(summary, candidates), encoding="utf-8")
    print(f"auto calibration candidates generated: {report_path}")
    print(f"auto calibration candidate rows: {len(candidates)}")
    return candidates, summary, str(report_path)


def main() -> int:
    build_auto_calibration_candidates()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
