from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from time_utils import format_jst, format_utc, now_utc


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/model_state")
IMPACT_JSON = RESULTS_DIR / "proposal_impact.json"
IMPACT_CSV = RESULTS_DIR / "proposal_impact.csv"
IMPACT_SUMMARY_JSON = RESULTS_DIR / "proposal_impact_summary.json"
ADOPTION_JSON = RESULTS_DIR / "proposal_adoption_tracking.json"
WEIGHT_HISTORY_JSON = RESULTS_DIR / "weight_version_history.json"
META_COLUMNS = [
    "generated_at_jst",
    "meta_learning_id",
    "source",
    "pattern_type",
    "category",
    "target",
    "proposal_id",
    "adoption_status",
    "impact_score",
    "impact_direction",
    "sample_count",
    "confidence_level",
    "recommended_action",
    "learning_hypothesis",
    "evidence_summary",
    "apply_automatically",
    "requires_human_approval",
    "weights_json_updated",
    "patch_applied",
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


def load_proposal_impact() -> tuple[pd.DataFrame, dict[str, Any]]:
    payload = read_json(IMPACT_JSON, {})
    if isinstance(payload, dict):
        for key in ("proposal_impacts", "impacts", "proposal_impact", "impact_rows"):
            rows = payload.get(key, [])
            if isinstance(rows, list):
                return normalize_headers(pd.DataFrame(rows)), payload
    if isinstance(payload, list):
        return normalize_headers(pd.DataFrame(payload)), {"proposal_impacts": payload}
    return read_csv(IMPACT_CSV), {}


def load_adoption_payload() -> dict[str, Any]:
    payload = read_json(ADOPTION_JSON, {})
    return payload if isinstance(payload, dict) else {}


def load_weight_history_payload() -> dict[str, Any]:
    payload = read_json(WEIGHT_HISTORY_JSON, {})
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


def impact_delta(row: pd.Series) -> float:
    explicit = first_present(row, ["impact_score", "impact_r_delta", "total_r_delta", "r_delta", "delta_r"], None)
    if explicit is not None and clean_text(explicit):
        return numeric(explicit, 0.0)
    after = first_present(row, ["post_total_r", "after_total_r", "post_avg_r", "after_avg_r"], None)
    before = first_present(row, ["pre_total_r", "before_total_r", "pre_avg_r", "before_avg_r"], None)
    if after is not None and before is not None and clean_text(after) and clean_text(before):
        return numeric(after, 0.0) - numeric(before, 0.0)
    return 0.0


def win_rate_delta(row: pd.Series) -> float:
    explicit = first_present(row, ["win_rate_delta", "delta_win_rate"], None)
    if explicit is not None and clean_text(explicit):
        return numeric(explicit, 0.0)
    after = first_present(row, ["post_win_rate", "after_win_rate"], None)
    before = first_present(row, ["pre_win_rate", "before_win_rate"], None)
    if after is not None and before is not None and clean_text(after) and clean_text(before):
        return numeric(after, 0.0) - numeric(before, 0.0)
    return 0.0


def confidence_from(sample_count: int, impact: float, win_delta: float) -> str:
    if sample_count < 5:
        return "insufficient_data"
    magnitude = abs(impact) + abs(win_delta)
    if sample_count >= 20 and magnitude >= 1.0:
        return "high"
    if sample_count >= 10 and magnitude >= 0.35:
        return "medium"
    return "low"


def classify_pattern(impact: float, win_delta: float, sample_count: int) -> tuple[str, str, str]:
    if sample_count < 3:
        return "insufficient_data", "neutral", "wait_for_more_data"
    if impact >= 0.5 or (impact > 0 and win_delta >= 0.03):
        return "success_pattern", "positive", "monitor_for_repeatability"
    if impact <= -0.5 or (impact < 0 and win_delta <= -0.03):
        return "failure_pattern", "negative", "avoid_or_review_pattern"
    return "neutral_pattern", "neutral", "wait_for_more_data"


def hypothesis_for(row: pd.Series, pattern_type: str, category: str, target: str, impact: float, win_delta: float) -> str:
    label = f"{category}:{target}" if category or target else clean_text(row.get("proposal_id", "unknown_proposal"))
    if pattern_type == "success_pattern":
        return f"{label} は採用後の成績改善候補です。再現性が確認できれば将来の承認判断で優先候補になります。"
    if pattern_type == "failure_pattern":
        return f"{label} は採用後の悪化候補です。次回提案では条件緩和よりも抑制・見直しを優先します。"
    if pattern_type == "insufficient_data":
        return f"{label} はデータ不足です。追加評価が出るまでMeta Learning判断を保留します。"
    return f"{label} は明確な成功/失敗パターンではありません。impact={impact:.2f}, win_rate_delta={win_delta:.2f} を継続監視します。"


def evidence_for(row: pd.Series, impact: float, win_delta: float, sample_count: int) -> str:
    proposal_id = clean_text(row.get("proposal_id", ""))
    return f"proposal_id={proposal_id or 'unknown'}, impact_score={impact:.2f}, win_rate_delta={win_delta:.2f}, sample_count={sample_count}"


def meta_row(row: pd.Series, generated_at_jst: str, sequence: int) -> dict[str, Any]:
    category = clean_text(first_present(row, ["category", "target_type", "proposal_type"], ""))
    target = clean_text(first_present(row, ["target", "target_name", "weight_path"], ""))
    proposal_id = clean_text(first_present(row, ["proposal_id", "patch_id"], f"impact_{sequence}"))
    adoption_status = clean_text(first_present(row, ["adoption_status", "review_decision"], "tracked"))
    sample_count = integer(first_present(row, ["sample_count", "post_sample_count", "evaluated_count"], 0), 0)
    impact = impact_delta(row)
    win_delta = win_rate_delta(row)
    pattern_type, direction, action = classify_pattern(impact, win_delta, sample_count)
    confidence = confidence_from(sample_count, impact, win_delta)
    return {
        "generated_at_jst": generated_at_jst,
        "meta_learning_id": f"ML_{sequence:04d}_{proposal_id}",
        "source": "proposal_impact",
        "pattern_type": pattern_type,
        "category": category,
        "target": target,
        "proposal_id": proposal_id,
        "adoption_status": adoption_status,
        "impact_score": impact,
        "impact_direction": direction,
        "sample_count": sample_count,
        "confidence_level": confidence,
        "recommended_action": action,
        "learning_hypothesis": hypothesis_for(row, pattern_type, category, target, impact, win_delta),
        "evidence_summary": evidence_for(row, impact, win_delta, sample_count),
        "apply_automatically": False,
        "requires_human_approval": True,
        "weights_json_updated": False,
        "patch_applied": False,
    }


def build_meta_rows(impact: pd.DataFrame, generated_at_jst: str) -> pd.DataFrame:
    if impact.empty:
        return pd.DataFrame(columns=META_COLUMNS)
    rows = [meta_row(row, generated_at_jst, idx + 1) for idx, (_, row) in enumerate(impact.iterrows())]
    return pd.DataFrame(rows, columns=META_COLUMNS)


def summary_from(meta: pd.DataFrame, impact_payload: dict[str, Any], generated_at_jst: str, generated_at_utc: str) -> dict[str, Any]:
    pattern = meta.get("pattern_type", pd.Series(dtype=str)).fillna("").astype(str) if not meta.empty else pd.Series(dtype=str)
    direction = meta.get("impact_direction", pd.Series(dtype=str)).fillna("").astype(str) if not meta.empty else pd.Series(dtype=str)
    confidence = meta.get("confidence_level", pd.Series(dtype=str)).fillna("").astype(str) if not meta.empty else pd.Series(dtype=str)
    return {
        "generated_at_jst": generated_at_jst,
        "generated_at_utc": generated_at_utc,
        "meta_learning_status": "unavailable" if meta.empty else "active",
        "proposal_impact_status": impact_payload.get("impact_status", "unavailable") if isinstance(impact_payload, dict) and impact_payload else "unavailable",
        "total_candidates": int(len(meta)),
        "success_pattern_count": int((pattern == "success_pattern").sum()),
        "failure_pattern_count": int((pattern == "failure_pattern").sum()),
        "neutral_pattern_count": int((pattern == "neutral_pattern").sum()),
        "insufficient_data_count": int((pattern == "insufficient_data").sum()) + int((confidence == "insufficient_data").sum()),
        "positive_count": int((direction == "positive").sum()),
        "negative_count": int((direction == "negative").sum()),
        "requires_human_approval": True,
        "apply_automatically": False,
        "weights_json_updated": False,
        "patch_applied": False,
        "recommended_next_action": "human_review" if (pattern.isin(["success_pattern", "failure_pattern"]).any() if not meta.empty else False) else "wait_for_more_data",
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
            values.append(clean_text(row.get(col, "")).replace("\n", " ").replace("|", "/"))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def render_markdown(summary: dict[str, Any], meta: pd.DataFrame) -> str:
    success = meta[meta["pattern_type"] == "success_pattern"] if not meta.empty else pd.DataFrame()
    failure = meta[meta["pattern_type"] == "failure_pattern"] if not meta.empty else pd.DataFrame()
    neutral = meta[~meta["pattern_type"].isin(["success_pattern", "failure_pattern"])] if not meta.empty else pd.DataFrame()
    cols = ["meta_learning_id", "pattern_type", "category", "target", "proposal_id", "impact_score", "sample_count", "confidence_level", "recommended_action", "learning_hypothesis"]
    return f"""# Meta Learning Layer

## 1. 概要

- 生成日時JST: {summary["generated_at_jst"]}
- meta_learning_status: {summary["meta_learning_status"]}
- proposal_impact_status: {summary["proposal_impact_status"]}
- total_candidates: {summary["total_candidates"]}
- success_pattern_count: {summary["success_pattern_count"]}
- failure_pattern_count: {summary["failure_pattern_count"]}
- neutral_pattern_count: {summary["neutral_pattern_count"]}
- insufficient_data_count: {summary["insufficient_data_count"]}
- recommended_next_action: {summary["recommended_next_action"]}
- apply_automatically: false
- weights_json_updated: false
- patch_applied: false
- requires_human_approval: true

## 2. 成功パターン候補

{markdown_table(success[cols] if not success.empty else success)}

## 3. 失敗パターン候補

{markdown_table(failure[cols] if not failure.empty else failure)}

## 4. 保留・中立候補

{markdown_table(neutral[cols] if not neutral.empty else neutral)}

## 5. 注意事項

- Meta Learningは提案のみです
- weights.jsonは更新しません
- patchは適用しません
- 自動適用は禁止です
- 実売買・発注・XM操作は行いません
- Proposal Impactが未取得の場合は、未取得summaryのみ生成します
"""


def build_meta_learning() -> tuple[pd.DataFrame, dict[str, Any], str]:
    generated_dt_utc = now_utc()
    generated_at_jst = format_jst(generated_dt_utc)
    generated_at_utc = format_utc(generated_dt_utc)
    impact, impact_payload = load_proposal_impact()
    adoption_payload = load_adoption_payload()
    weight_history_payload = load_weight_history_payload()
    meta = build_meta_rows(impact, generated_at_jst)
    summary = summary_from(meta, impact_payload, generated_at_jst, generated_at_utc)
    payload = {
        **summary,
        "source": {
            "proposal_impact": "results/proposal_impact.json",
            "proposal_adoption_tracking": "results/proposal_adoption_tracking.json",
            "weight_version_history": "results/weight_version_history.json",
        },
        "safety": {
            "weights_json_updated": False,
            "patch_applied": False,
            "requires_human_approval": True,
            "apply_automatically": False,
        },
        "input_status": {
            "proposal_impact_available": bool(impact_payload) or not impact.empty,
            "proposal_adoption_tracking_available": bool(adoption_payload),
            "weight_version_history_available": bool(weight_history_payload),
        },
        "meta_learning_candidates": meta.to_dict(orient="records"),
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_date = generated_at_jst[:10]
    csv_path = RESULTS_DIR / "meta_learning.csv"
    json_path = RESULTS_DIR / "meta_learning.json"
    summary_path = RESULTS_DIR / "meta_learning_summary.json"
    report_path = REPORTS_DIR / f"{report_date}_meta_learning.md"
    meta.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    report_path.write_text(render_markdown(summary, meta), encoding="utf-8")
    print(f"meta learning generated: {report_path}")
    print(f"meta learning rows: {len(meta)}")
    return meta, summary, str(report_path)


def main() -> int:
    build_meta_learning()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
