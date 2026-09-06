from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import pandas as pd

from time_utils import format_jst, format_utc, now_utc


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/model_state")
WEIGHTS_PATH = Path("models/weights.json")
KNOWN_ASSETS = ["BTC", "GOLD", "WTI", "USDJPY", "SPX", "NASDAQ", "DXY", "VIX", "US10Y"]
KNOWN_SIDES = ["LONG", "SHORT", "NONE", "NO_TRADE"]
KNOWN_RANKS = ["A", "B", "NO_TRADE"]
KNOWN_TYPES = ["A-Momentum", "A-Pullback", "B-Watch", "NO_TRADE"]
KNOWN_REASON_CODES = [
    "trend_up",
    "trend_down",
    "momentum_positive",
    "momentum_negative",
    "ma_alignment_bull",
    "ma_alignment_bear",
    "breakout_up",
    "breakout_down",
    "rsi_overbought",
    "rsi_oversold",
    "rr_too_low",
    "low_volatility",
]
NARRATIVE_SCORE_KEYS = {
    "risk_on": "risk_on_news_score",
    "risk_off": "risk_off_news_score",
    "dollar_strength": "dollar_strength_news_score",
    "rate_pressure": "rate_pressure_news_score",
    "geopolitical_risk": "geopolitical_risk_news_score",
    "oil_supply_risk": "oil_supply_risk_news_score",
    "crypto_liquidity": "crypto_liquidity_news_score",
}
CSV_COLUMNS = [
    "generated_at_jst",
    "proposal_id",
    "category",
    "target",
    "metric_group",
    "sample_count",
    "win_rate",
    "avg_r",
    "total_r",
    "missed_opportunity_rate",
    "no_entry_rate",
    "confidence_level",
    "current_weight",
    "proposed_weight",
    "proposed_delta",
    "max_allowed_delta",
    "proposal_direction",
    "proposal_strength",
    "rationale",
    "evidence_source",
    "apply_automatically",
    "missing_current_weight",
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


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return normalize_headers(pd.read_csv(path))
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [json_safe(v) for v in value]
    if isinstance(value, tuple):
        return [json_safe(v) for v in value]
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if not isinstance(value, (dict, list, tuple)):
        try:
            if pd.isna(value):
                return None
        except (TypeError, ValueError):
            pass
    if hasattr(value, "item"):
        try:
            return value.item()
        except (TypeError, ValueError):
            pass
    return value


def bool_series(df: pd.DataFrame, column: str) -> pd.Series:
    if df.empty or column not in df.columns:
        return pd.Series([False] * len(df), index=df.index)
    return df[column].fillna("").astype(str).str.lower().isin(["true", "1", "yes"])


def numeric_series(df: pd.DataFrame, column: str) -> pd.Series:
    if df.empty or column not in df.columns:
        return pd.Series(dtype=float)
    return pd.to_numeric(df[column], errors="coerce")


def scalar_float(value: Any, default: float = 0.0) -> float:
    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number):
        return default
    return float(number)


def scalar_int(value: Any, default: int = 0) -> int:
    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number):
        return default
    return int(number)


def load_weights(path: Path = WEIGHTS_PATH) -> dict[str, Any]:
    weights = read_json(path, {})
    return weights if isinstance(weights, dict) else {}


def weight_lookup(weights: dict[str, Any], category: str, target: str) -> tuple[float, bool]:
    category_keys = {
        "asset": ["asset_weights", "assets"],
        "side": ["side_weights", "sides"],
        "rank": ["rank_weights", "ranks"],
        "type": ["type_weights", "setup_type_weights", "setup_types"],
        "reason_code": ["reason_code_weights", "reason_codes"],
        "narrative": ["narrative_weights", "narratives"],
    }
    for key in category_keys.get(category, []):
        table = weights.get(key, {})
        if isinstance(table, dict) and target in table:
            return scalar_float(table[target], 1.0), False
    global_weights = weights.get("global", {})
    global_key = f"{target}_weight"
    if isinstance(global_weights, dict) and global_key in global_weights:
        return scalar_float(global_weights[global_key], 1.0), False
    return 1.0, True


# 正否を測れなかった行の error_type (監査F1, 2026-09-06)。
# evaluate_signal はこれらにも r_multiple=0.0 を入れるが、その 0 は「損益ゼロ」ではなく
# 「測れなかった」である。0R を実績として集計に入れると、負けと同じ働きをして
# 勝率を薄め、平均Rを引き下げ、標本数と信頼度だけを膨らませる。
# 実測(合成再現): 正常5件(全て+1R)なら n=5 勝率100% 平均+1R confidence=low
# 提案 increase +0.03。同じ5件に評価不能20件を足すと n=25 勝率20% 平均+0.2R
# confidence=high 提案 decrease -0.0507 で、**提案の向きが反転する**。
UNEVALUABLE_ERROR_TYPES = {"invalid_signal_date", "data_missing", "awaiting_horizon"}

# 確定した見送り評価。no_trade_result はこれらにも evaluation_status="skipped" を付けるため、
# skipped を一律に評価不能とすると**正しく採点できた見送りまで母集団から消える**
# (#145 Codex P1)。その場合 NONE/NO_TRADE の side・rank・type 提案が
# insufficient_samples になり、観測された結果がモデル更新に届かなくなる。
FINALIZED_NO_TRADE_OUTCOMES = {"no_trade_correct", "no_trade_missed"}

# まだ決着していない行。測れなかったのではなく「これから測る」。
UNRESOLVED_OUTCOMES = {"open_unresolved", "no_trade"}


def _lower_col(df: pd.DataFrame, name: str) -> pd.Series:
    return df.get(name, pd.Series("", index=df.index)).fillna("").astype(str).str.lower()


def unevaluable_mask(df: pd.DataFrame) -> pd.Series:
    """正否を測れなかった行 = 入力不正・データ欠損・ホライズン未到達・skipped。

    「全判断を記録する」と「全行を売買勝率の分母にする」は別の要件である。
    記録は残したまま、測れた集合だけを成績の母集団にする。
    """
    if df.empty:
        return pd.Series(dtype=bool)
    err = _lower_col(df, "error_type")
    st = _lower_col(df, "status")
    outcome = _lower_col(df, "outcome")
    # evaluation_status=="skipped" を単独の条件にしない(#145 Codex P1)。
    # 確定した no_trade_correct / no_trade_missed も skipped を持つため、
    # 一律に外すと正しく採点できた見送りが母集団から消える。
    # 評価不能かどうかは error_type と outcome/status の組み合わせで判定する。
    return (
        err.isin(UNEVALUABLE_ERROR_TYPES)
        | (st == "invalid")
        | (outcome == "invalid")
        | (outcome.isin(UNRESOLVED_OUTCOMES) & ~outcome.isin(FINALIZED_NO_TRADE_OUTCOMES))
        | (st.isin({"pending", "open", "unresolved"}))
    )


def measurable_mask(df: pd.DataFrame) -> pd.Series:
    """成績の母集団。勝率の分母・R集計・標本数・信頼度はすべてこの集合を使う。"""
    if df.empty:
        return pd.Series(dtype=bool)
    return ~unevaluable_mask(df)


def closed_mask(df: pd.DataFrame) -> pd.Series:
    if df.empty:
        return pd.Series(dtype=bool)
    outcome = _lower_col(df, "outcome")
    status = df.get("evaluation_status", df.get("status", pd.Series("", index=df.index))).fillna("").astype(str).str.lower()
    r = numeric_series(df, "r_multiple")
    resolved = outcome.isin(["win_tp1", "win_tp2", "loss_sl"])
    # 評価不能行は r_multiple=0.0 を持つため r.notna() で closed に混入する。除く。
    return (resolved | (status == "closed") | r.notna()) & measurable_mask(df)


_EMPTY_METRICS = {
    "sample_count": 0, "recorded_count": 0, "unevaluable_count": 0,
    "win_rate": 0.0, "avg_r": 0.0, "total_r": 0.0, "median_r": 0.0,
    "loss_rate": 0.0, "missed_opportunity_rate": 0.0, "no_entry_rate": 0.0, "closed_rate": 0.0,
}


def metrics_from_frame(df: pd.DataFrame) -> dict[str, float | int]:
    """成績指標。分母はすべて「測れた行」で揃える（監査F1）。

    sample_count は測れた行数であり、記録総数ではない。記録総数は recorded_count、
    測れなかった行数は unevaluable_count に別途残す（記録は捨てない）。
    """
    recorded_count = int(len(df))
    if recorded_count == 0:
        return dict(_EMPTY_METRICS)
    measurable = measurable_mask(df)
    sample_count = int(measurable.sum())
    unevaluable_count = recorded_count - sample_count
    if sample_count == 0:
        out = dict(_EMPTY_METRICS)
        out["recorded_count"] = recorded_count
        out["unevaluable_count"] = unevaluable_count
        return out

    sub = df[measurable]
    outcome = _lower_col(sub, "outcome")
    r = numeric_series(sub, "r_multiple")
    closed_count = int(closed_mask(df)[measurable].sum())
    wins = int(outcome.isin(["win_tp1", "win_tp2"]).sum())
    losses = int(outcome.isin(["loss_sl"]).sum())
    missed = int(bool_series(sub, "missed_opportunity").sum())
    no_entry = int((outcome == "no_entry").sum())
    r_values = r.dropna()
    return {
        "sample_count": sample_count,
        "recorded_count": recorded_count,
        "unevaluable_count": unevaluable_count,
        "win_rate": wins / closed_count if closed_count else 0.0,
        "avg_r": float(r_values.mean()) if not r_values.empty else 0.0,
        "total_r": float(r_values.sum()) if not r_values.empty else 0.0,
        "median_r": float(r_values.median()) if not r_values.empty else 0.0,
        "loss_rate": losses / closed_count if closed_count else 0.0,
        "missed_opportunity_rate": missed / sample_count,
        "no_entry_rate": no_entry / sample_count,
        "closed_rate": closed_count / sample_count,
    }


def confidence_level(sample_count: int) -> str:
    if sample_count < 5:
        return "insufficient_data"
    if sample_count < 10:
        return "low"
    if sample_count < 20:
        return "medium"
    return "high"


def max_allowed_delta(sample_count: int) -> float:
    if sample_count < 5:
        return 0.0
    if sample_count < 10:
        return 0.03
    if sample_count < 20:
        return 0.05
    return 0.08


def direction_from_metrics(sample_count: int, avg_r: float, win_rate: float) -> str:
    if sample_count < 5:
        return "hold"
    if avg_r > 0.25 and win_rate > 0.55:
        return "increase"
    if avg_r < -0.15 or win_rate < 0.40:
        return "decrease"
    return "hold"


def proposed_delta(sample_count: int, avg_r: float, win_rate: float) -> tuple[str, float, float, str]:
    limit = max_allowed_delta(sample_count)
    direction = direction_from_metrics(sample_count, avg_r, win_rate)
    if direction == "hold" or limit <= 0:
        return direction, 0.0, limit, "none"

    quality = min(1.0, abs(avg_r) / 0.75)
    win_component = min(1.0, abs(win_rate - 0.50) / 0.30)
    raw_delta = limit * max(0.45, min(1.0, (quality + win_component) / 2))
    delta = min(limit, raw_delta)
    if direction == "decrease":
        delta = -delta

    abs_delta = abs(delta)
    if abs_delta >= 0.06:
        strength = "strong"
    elif abs_delta >= 0.03:
        strength = "moderate"
    else:
        strength = "weak"
    return direction, round(delta, 4), limit, strength


def proposal_rationale(category: str, target: str, metrics: dict[str, float | int], direction: str) -> str:
    sample_count = int(metrics["sample_count"])
    if sample_count < 5:
        return f"{category}={target} はsample_count={sample_count}で、統計的に不足しているため保留します。"
    return (
        f"{category}={target} はsample_count={sample_count}, "
        f"win_rate={float(metrics['win_rate']):.2f}, avg_r={float(metrics['avg_r']):.2f}。"
        f" 判定は {direction} です。"
    )


def make_proposal(
    *,
    generated_at_jst: str,
    category: str,
    target: str,
    metric_group: str,
    metrics: dict[str, float | int],
    weights: dict[str, Any],
    evidence_source: str,
    proposal_type: str,
    rationale_extra: str = "",
) -> dict[str, Any]:
    current_weight, missing = weight_lookup(weights, category, target)
    direction, delta, limit, strength = proposed_delta(
        int(metrics["sample_count"]),
        float(metrics["avg_r"]),
        float(metrics["win_rate"]),
    )
    proposed_weight = max(0.0, current_weight + delta)
    proposal_id = f"{generated_at_jst[:10].replace('-', '')}_{category}_{target}_{proposal_type}".replace(" ", "_").replace("/", "_")
    rationale = proposal_rationale(category, target, metrics, direction)
    if rationale_extra:
        rationale = f"{rationale} {rationale_extra}"
    return {
        "generated_at_jst": generated_at_jst,
        "proposal_id": proposal_id,
        "proposal_type": proposal_type,
        "category": category,
        "target": target,
        "metric_group": metric_group,
        "sample_count": int(metrics["sample_count"]),
        "win_rate": round(float(metrics["win_rate"]), 4),
        "avg_r": round(float(metrics["avg_r"]), 4),
        "total_r": round(float(metrics["total_r"]), 4),
        "median_r": round(float(metrics["median_r"]), 4),
        "loss_rate": round(float(metrics["loss_rate"]), 4),
        "missed_opportunity_rate": round(float(metrics["missed_opportunity_rate"]), 4),
        "no_entry_rate": round(float(metrics["no_entry_rate"]), 4),
        "closed_rate": round(float(metrics["closed_rate"]), 4),
        "confidence_level": confidence_level(int(metrics["sample_count"])),
        "current_weight": round(float(current_weight), 4),
        "proposed_weight": round(float(proposed_weight), 4),
        "proposed_delta": round(float(delta), 4),
        "max_allowed_delta": round(float(limit), 4),
        "proposal_direction": direction,
        "proposal_strength": strength,
        "rationale": rationale,
        "evidence_source": evidence_source,
        "apply_automatically": False,
        "missing_current_weight": bool(missing),
    }


def group_metric_proposals(
    evaluations: pd.DataFrame,
    weights: dict[str, Any],
    generated_at_jst: str,
    category: str,
    column: str,
    targets: list[str],
    proposal_type: str,
    evidence_source: str = "latest_evaluations",
) -> list[dict[str, Any]]:
    proposals = []
    values = set(targets)
    if not evaluations.empty and column in evaluations.columns:
        values.update(v for v in evaluations[column].dropna().astype(str).unique() if v)
    for target in sorted(values):
        if not evaluations.empty and column in evaluations.columns:
            part = evaluations[evaluations[column].fillna("").astype(str) == target]
        else:
            part = pd.DataFrame()
        proposals.append(
            make_proposal(
                generated_at_jst=generated_at_jst,
                category=category,
                target=target,
                metric_group=column,
                metrics=metrics_from_frame(part),
                weights=weights,
                evidence_source=evidence_source,
                proposal_type=proposal_type,
            )
        )
    return proposals


def parse_reason_code_metrics(reason_json: Any) -> list[dict[str, Any]]:
    if not isinstance(reason_json, dict):
        return []
    rows = reason_json.get("reason_code_summary", [])
    return rows if isinstance(rows, list) else []


def reason_metrics_from_evaluations(evaluations: pd.DataFrame) -> pd.DataFrame:
    if evaluations.empty or "reason_codes" not in evaluations.columns:
        return pd.DataFrame()
    rows = []
    for _, row in evaluations.iterrows():
        codes = str(row.get("reason_codes", "") or "").replace(";", "|").replace(",", "|").split("|")
        for code in [c.strip() for c in codes if c.strip()]:
            item = row.to_dict()
            item["reason_code"] = code
            rows.append(item)
    return pd.DataFrame(rows)


def reason_code_proposals(evaluations: pd.DataFrame, reason_json: Any, weights: dict[str, Any], generated_at_jst: str) -> list[dict[str, Any]]:
    proposals = []
    reason_rows = parse_reason_code_metrics(reason_json)
    used = set()
    for row in reason_rows:
        code = str(row.get("reason_code", "") or "")
        if not code:
            continue
        used.add(code)
        sample_count = scalar_int(row.get("evaluated_count", row.get("signals_count", 0)), 0)
        metrics = {
            "sample_count": sample_count,
            "win_rate": scalar_float(row.get("win_rate", 0)),
            "avg_r": scalar_float(row.get("average_r", row.get("avg_r", 0))),
            "total_r": scalar_float(row.get("total_r", 0)),
            "median_r": scalar_float(row.get("median_r", 0)),
            "loss_rate": scalar_float(row.get("loss_rate", 0)),
            "missed_opportunity_rate": scalar_float(row.get("missed_opportunity_count", 0)) / sample_count if sample_count else 0.0,
            "no_entry_rate": scalar_float(row.get("no_entry_count", 0)) / sample_count if sample_count else 0.0,
            "closed_rate": 1.0 if sample_count else 0.0,
        }
        proposals.append(
            make_proposal(
                generated_at_jst=generated_at_jst,
                category="reason_code",
                target=code,
                metric_group="reason_code",
                metrics=metrics,
                weights=weights,
                evidence_source="reason_code_analysis",
                proposal_type="reason_code_weight_adjustment",
                rationale_extra=f"reliability_label={row.get('reliability_label', 'unknown')}",
            )
        )

    exploded = reason_metrics_from_evaluations(evaluations)
    for code in sorted(set(KNOWN_REASON_CODES) - used):
        part = exploded[exploded["reason_code"] == code] if not exploded.empty else pd.DataFrame()
        proposals.append(
            make_proposal(
                generated_at_jst=generated_at_jst,
                category="reason_code",
                target=code,
                metric_group="reason_code",
                metrics=metrics_from_frame(part),
                weights=weights,
                evidence_source="latest_evaluations",
                proposal_type="reason_code_weight_adjustment",
            )
        )
    return proposals


def narrative_proposals(evaluations: pd.DataFrame, ai_json: Any, weights: dict[str, Any], generated_at_jst: str) -> list[dict[str, Any]]:
    if not isinstance(ai_json, dict):
        ai_json = {}
    scores = ai_json.get("narrative_scores", {})
    if not isinstance(scores, dict):
        scores = {}
    alignment = pd.DataFrame(ai_json.get("signal_alignment", []) or [])
    base_metrics = metrics_from_frame(evaluations)
    proposals = []
    for target, score_key in NARRATIVE_SCORE_KEYS.items():
        part = pd.DataFrame()
        if not alignment.empty:
            alignment_norm = normalize_headers(alignment)
            text_cols = [col for col in ["narrative_alignment", "market_mode_summary", "notes", "asset"] if col in alignment_norm.columns]
            if text_cols:
                mask = pd.Series(False, index=alignment_norm.index)
                for col in text_cols:
                    mask = mask | alignment_norm[col].fillna("").astype(str).str.lower().str.contains(target.replace("_", " "), regex=False)
                    mask = mask | alignment_norm[col].fillna("").astype(str).str.lower().str.contains(target, regex=False)
                part = alignment_norm[mask]
        metrics = metrics_from_frame(part) if not part.empty else base_metrics
        score = scalar_float(scores.get(score_key, ai_json.get(score_key, 0)), 0.0)
        rationale_extra = f"narrative_score={score:.2f}。AI Feedback由来の補助指標として扱います。"
        proposals.append(
            make_proposal(
                generated_at_jst=generated_at_jst,
                category="narrative",
                target=target,
                metric_group="narrative_alignment",
                metrics=metrics,
                weights=weights,
                evidence_source="ai_feedback",
                proposal_type="narrative_weight_adjustment",
                rationale_extra=rationale_extra,
            )
        )
    return proposals


def load_inputs() -> dict[str, Any]:
    return {
        "weights": load_weights(),
        "evaluations": read_csv(RESULTS_DIR / "latest_evaluations.csv"),
        "reason_code_analysis": read_json(RESULTS_DIR / "reason_code_analysis.json", {}),
        "rule_update_proposals": read_json(RESULTS_DIR / "rule_update_proposals.json", {}),
        "monthly_calibration": read_json(RESULTS_DIR / "monthly_calibration.json", {}),
        "ai_feedback": read_json(RESULTS_DIR / "ai_feedback.json", {}),
    }


def data_source_status(inputs: dict[str, Any]) -> dict[str, str]:
    return {
        "evaluations": "latest_evaluations" if not inputs["evaluations"].empty else "missing",
        "reason_code_analysis": "available" if bool(inputs["reason_code_analysis"]) else "missing",
        "rule_update_proposals": "available" if bool(inputs["rule_update_proposals"]) else "missing",
        "monthly_calibration": "available" if bool(inputs["monthly_calibration"]) else "missing",
        "ai_feedback": "available" if bool(inputs["ai_feedback"]) else "missing",
    }


def build_model_state_update_proposals() -> tuple[pd.DataFrame, dict[str, Any], str]:
    generated_dt_utc = now_utc()
    generated_at_jst = format_jst(generated_dt_utc)
    generated_at_utc = format_utc(generated_dt_utc)
    report_date = generated_at_jst[:10]
    inputs = load_inputs()
    evaluations = inputs["evaluations"]
    weights = inputs["weights"]

    proposals: list[dict[str, Any]] = []
    proposals.extend(group_metric_proposals(evaluations, weights, generated_at_jst, "asset", "asset", KNOWN_ASSETS, "asset_weight_adjustment"))
    proposals.extend(group_metric_proposals(evaluations, weights, generated_at_jst, "side", "side", KNOWN_SIDES, "side_bias_adjustment"))
    proposals.extend(group_metric_proposals(evaluations, weights, generated_at_jst, "rank", "rank", KNOWN_RANKS, "rank_confidence_adjustment"))
    proposals.extend(group_metric_proposals(evaluations, weights, generated_at_jst, "type", "type", KNOWN_TYPES, "setup_type_weight_adjustment"))
    proposals.extend(reason_code_proposals(evaluations, inputs["reason_code_analysis"], weights, generated_at_jst))
    proposals.extend(narrative_proposals(evaluations, inputs["ai_feedback"], weights, generated_at_jst))

    df = pd.DataFrame(proposals)
    if df.empty:
        df = pd.DataFrame(columns=CSV_COLUMNS)
    else:
        df = df.sort_values(["proposal_strength", "category", "target"], key=lambda col: col.map({"strong": 0, "moderate": 1, "weak": 2, "none": 3}).fillna(col) if col.name == "proposal_strength" else col)

    csv_df = df.copy()
    for col in CSV_COLUMNS:
        if col not in csv_df.columns:
            csv_df[col] = ""
    csv_df = csv_df[CSV_COLUMNS]

    summary = {
        "total_proposals": int(len(df)),
        "increase_count": int((df.get("proposal_direction", pd.Series(dtype=str)) == "increase").sum()) if not df.empty else 0,
        "decrease_count": int((df.get("proposal_direction", pd.Series(dtype=str)) == "decrease").sum()) if not df.empty else 0,
        "hold_count": int((df.get("proposal_direction", pd.Series(dtype=str)) == "hold").sum()) if not df.empty else 0,
        "insufficient_data_count": int((df.get("confidence_level", pd.Series(dtype=str)) == "insufficient_data").sum()) if not df.empty else 0,
    }
    payload = {
        "generated_at_jst": generated_at_jst,
        "generated_at_utc": generated_at_utc,
        "timezone": "Asia/Tokyo",
        "data_source": data_source_status(inputs),
        "safety": {
            "apply_automatically": False,
            "weights_json_updated": False,
            "requires_human_review": True,
        },
        "summary": summary,
        "proposals": json_safe(df.to_dict(orient="records")),
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = RESULTS_DIR / "model_state_update_proposals.csv"
    json_path = RESULTS_DIR / "model_state_update_proposals.json"
    summary_path = RESULTS_DIR / "model_state_update_summary.json"
    report_path = REPORTS_DIR / f"{report_date}_model_state_update_proposals.md"
    csv_df.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    summary_path.write_text(json.dumps({"generated_at_jst": generated_at_jst, **summary, "safety": payload["safety"]}, ensure_ascii=False, indent=2), encoding="utf-8")
    report_path.write_text(render_markdown(payload, csv_df), encoding="utf-8")
    print(f"model state update proposals generated: {report_path}")
    print(f"model state proposal rows: {len(csv_df)}")
    return csv_df, payload, str(report_path)


def markdown_table(df: pd.DataFrame, empty: str = "データなし") -> str:
    if df is None or df.empty:
        return empty
    try:
        return df.to_markdown(index=False)
    except ImportError:
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


def render_markdown(payload: dict[str, Any], proposals: pd.DataFrame) -> str:
    summary = payload["summary"]
    strong = proposals[proposals["proposal_strength"] == "strong"] if not proposals.empty else pd.DataFrame()
    moderate = proposals[proposals["proposal_strength"] == "moderate"] if not proposals.empty else pd.DataFrame()
    hold = proposals[(proposals["proposal_direction"] == "hold") | (proposals["confidence_level"] == "insufficient_data")] if not proposals.empty else pd.DataFrame()
    asset = proposals[proposals["category"] == "asset"] if not proposals.empty else pd.DataFrame()
    reason = proposals[proposals["category"] == "reason_code"] if not proposals.empty else pd.DataFrame()
    narrative = proposals[proposals["category"] == "narrative"] if not proposals.empty else pd.DataFrame()
    cols = [
        "proposal_id",
        "category",
        "target",
        "sample_count",
        "win_rate",
        "avg_r",
        "proposal_direction",
        "proposal_strength",
        "proposed_delta",
        "rationale",
    ]
    return f"""# Model State Update Proposals

## 1. 概要

- 生成日時JST: {payload["generated_at_jst"]}
- latest_evaluations使用有無: {payload["data_source"]["evaluations"]}
- 提案件数: {summary["total_proposals"]}
- increase件数: {summary["increase_count"]}
- decrease件数: {summary["decrease_count"]}
- hold件数: {summary["hold_count"]}
- insufficient_data件数: {summary["insufficient_data_count"]}
- 自動適用: false

## 2. 強い更新候補

{markdown_table(strong[cols] if not strong.empty else strong)}

## 3. 中程度の更新候補

{markdown_table(moderate[cols] if not moderate.empty else moderate)}

## 4. 保留候補

{markdown_table(hold[cols].head(25) if not hold.empty else hold)}

## 5. asset別提案

{markdown_table(asset[cols] if not asset.empty else asset)}

## 6. reason_code別提案

{markdown_table(reason[cols].head(25) if not reason.empty else reason)}

## 7. narrative別提案

{markdown_table(narrative[cols] if not narrative.empty else narrative)}

## 8. 注意

- weights.jsonは自動更新していない
- 提案は統計的にまだ不安定な可能性がある
- 実売買・自動発注には使わない
- 人間確認後に別フェーズで反映を検討する

## 9. MODEL_STATE_UPDATE_PROPOSALS JSON

```json
{json.dumps(payload, ensure_ascii=False, indent=2)}
```
"""


def main() -> int:
    build_model_state_update_proposals()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
