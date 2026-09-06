from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from time_utils import format_jst, format_utc, now_utc


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/portfolio")

ASSETS = ["WTI", "BTC", "NASDAQ", "USDJPY", "GOLD", "ETH", "SPX", "VIX", "DXY", "US10Y"]
HIGH_RISK_ASSETS = {"BTC", "ETH", "NASDAQ", "WTI", "VIX"}
DEFENSIVE_ASSETS = {"GOLD", "DXY", "US10Y", "VIX"}
OFFENSIVE_ASSETS = {"BTC", "ETH", "NASDAQ", "SPX", "WTI"}

PORTFOLIO_COLUMNS = [
    "generated_at_jst",
    "asset",
    "allocation_score",
    "portfolio_weight_candidate",
    "confidence",
    "risk_class",
    "risk_role",
    "recommended_exposure",
    "cash_ratio_candidate",
    "latest_rank",
    "latest_side",
    "signal_score",
    "evaluation_score",
    "meta_learning_score",
    "auto_calibration_score",
    "human_override_score",
    "proposal_impact_score",
    "rationale",
    "requires_human_approval",
    "weights_json_updated",
    "patch_applied",
    "generate_signal_updated",
    "orders_created",
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


def load_table(csv_path: Path, json_path: Path, keys: list[str]) -> tuple[pd.DataFrame, bool]:
    payload = read_json(json_path, {})
    rows = rows_from_payload(payload, keys) if payload else []
    if rows:
        return normalize_headers(pd.DataFrame(rows)), True
    csv = read_csv(csv_path)
    return csv, not csv.empty or bool(payload)


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


def first_present(row: pd.Series, columns: list[str], default: Any = "") -> Any:
    for col in columns:
        if col in row.index and clean_text(row.get(col)):
            return row.get(col)
    return default


def asset_mask(df: pd.DataFrame, asset: str) -> pd.Series:
    if df.empty:
        return pd.Series(dtype=bool)
    candidates = [col for col in ["asset", "target", "target_name"] if col in df.columns]
    if not candidates:
        return pd.Series([False] * len(df), index=df.index)
    mask = pd.Series([False] * len(df), index=df.index)
    for col in candidates:
        mask = mask | (df[col].fillna("").astype(str).str.upper() == asset.upper())
    return mask


def latest_for_asset(df: pd.DataFrame, asset: str) -> pd.Series | None:
    if df.empty:
        return None
    rows = df[asset_mask(df, asset)]
    if rows.empty:
        return None
    for col in ["date", "signal_date", "evaluation_date", "generated_at_jst", "generated_at"]:
        if col in rows.columns:
            sortable = rows.copy()
            sortable["_sort_key"] = pd.to_datetime(sortable[col], errors="coerce")
            rows = sortable.sort_values("_sort_key").drop(columns=["_sort_key"])
            break
    return rows.iloc[-1]


def risk_class(asset: str) -> str:
    if asset in HIGH_RISK_ASSETS:
        return "high"
    if asset in DEFENSIVE_ASSETS:
        return "defensive"
    return "medium"


def risk_role(asset: str) -> str:
    if asset in DEFENSIVE_ASSETS:
        return "defensive"
    if asset in OFFENSIVE_ASSETS:
        return "offensive"
    return "balanced"


def signal_component(signals: pd.DataFrame, asset: str) -> tuple[float, str, str, str]:
    row = latest_for_asset(signals, asset)
    if row is None:
        return 0.0, "", "", "signal data unavailable"
    rank = clean_text(first_present(row, ["rank"], ""))
    side = clean_text(first_present(row, ["side"], ""))
    rank_score = {"A": 18.0, "B": 10.0, "NO_TRADE": -8.0}.get(rank.upper(), 0.0)
    side_score = -5.0 if side.upper() in {"NONE", "NO_TRADE"} else 5.0 if side else 0.0
    quality = max(
        numeric(first_present(row, ["signal_strength", "tq_score", "setup_quality_score", "entry_quality_score"], 0.0), 0.0),
        0.0,
    )
    quality_score = min(15.0, quality / 100.0 * 15.0 if quality > 1 else quality * 15.0)
    score = rank_score + side_score + quality_score
    return score, rank, side, f"signal rank={rank or 'n/a'} side={side or 'n/a'}"


def evaluation_component(evaluations: pd.DataFrame, asset: str) -> tuple[float, float, str]:
    if evaluations.empty:
        return 0.0, 0.35, "evaluation data unavailable"
    rows = evaluations[asset_mask(evaluations, asset)]
    if rows.empty:
        return 0.0, 0.35, "evaluation rows unavailable"
    r = pd.to_numeric(rows.get("r_multiple", pd.Series(dtype=float)), errors="coerce")
    closed = rows.get("outcome", rows.get("status", pd.Series(dtype=str))).fillna("").astype(str)
    wins = closed.str.contains("win|tp", case=False, regex=True, na=False)
    losses = closed.str.contains("loss|sl", case=False, regex=True, na=False)
    decided = wins | losses
    decided_count = int(decided.sum())
    win_rate = float(wins.sum() / decided_count) if decided_count else 0.0
    # 監査F9 (2026-09-06): avg_r も confidence も**決着した行**で測る。
    # 未決着行(open_unresolved 等)は r_multiple=0.0 を持つため、
    # 全行平均だと 0 が平均を薄め、件数だけが confidence を押し上げる。
    # 実測: BTC の未決着30件だけで confidence が 0.35 → 0.86 になっていた。
    r_decided = r[decided].dropna()
    avg_r = float(r_decided.mean()) if not r_decided.empty else 0.0
    missed = rows.get("missed_opportunity", pd.Series([False] * len(rows))).fillna(False).astype(str).str.lower().isin(["true", "1", "yes"]).sum()
    score = avg_r * 8.0 + win_rate * 12.0 - min(10.0, missed * 2.0)
    # 「入力があること」と「成績が確からしいこと」は別物。confidence は後者のみを表す。
    confidence = min(0.85, 0.30 + min(decided_count, 30) / 60.0)
    return score, confidence, (
        f"evaluation avg_r={avg_r:.2f} win_rate={win_rate:.2f} "
        f"decided={decided_count}/{len(rows)}"
    )


def meta_component(meta: pd.DataFrame, asset: str) -> tuple[float, str]:
    if meta.empty:
        return 0.0, "meta learning unavailable"
    rows = meta[asset_mask(meta, asset)]
    score = 0.0
    for _, row in rows.iterrows():
        pattern = clean_text(first_present(row, ["pattern_type"], "")).lower()
        direction = clean_text(first_present(row, ["impact_direction"], "")).lower()
        impact = numeric(first_present(row, ["impact_score", "total_r_delta"], 0.0), 0.0)
        if "success" in pattern or direction == "positive" or impact > 0:
            score += 6.0 + min(4.0, abs(impact) * 2.0)
        elif "failure" in pattern or direction == "negative" or impact < 0:
            score -= 6.0 + min(4.0, abs(impact) * 2.0)
    return score, f"meta rows={len(rows)}"


def auto_calibration_component(candidates: pd.DataFrame, asset: str) -> tuple[float, str]:
    if candidates.empty:
        return 0.0, "auto calibration unavailable"
    rows = candidates[asset_mask(candidates, asset)]
    score = 0.0
    for _, row in rows.iterrows():
        classification = clean_text(first_present(row, ["classification"], "")).lower()
        confidence = numeric(first_present(row, ["confidence"], 0.35), 0.35)
        if classification == "increase":
            score += 5.0 + confidence * 3.0
        elif classification == "decrease":
            score -= 5.0 + confidence * 3.0
        elif classification == "blocked":
            score -= 10.0
        elif classification == "insufficient_data":
            score -= 2.0
    return score, f"auto calibration rows={len(rows)}"


def human_override_component(overrides: pd.DataFrame, asset: str) -> tuple[float, str]:
    if overrides.empty:
        return 0.0, "human override unavailable"
    rows = overrides[asset_mask(overrides, asset)]
    score = 0.0
    for _, row in rows.iterrows():
        override_type = clean_text(first_present(row, ["override_type"], "")).lower()
        impact_status = clean_text(first_present(row, ["impact_status"], "")).lower()
        impact_score = numeric(first_present(row, ["impact_score"], 0.0), 0.0)
        if impact_status == "positive":
            score += 5.0 + max(0.0, impact_score)
        elif impact_status == "negative":
            score -= 5.0 + abs(min(0.0, impact_score))
        if override_type == "blocked":
            score -= 6.0
        elif override_type == "rejected":
            score -= 3.0
    return score, f"human override rows={len(rows)}"


def proposal_impact_component(impact: pd.DataFrame, asset: str) -> tuple[float, str]:
    if impact.empty:
        return 0.0, "proposal impact unavailable"
    rows = impact[asset_mask(impact, asset)]
    values = pd.to_numeric(rows.get("impact_score", pd.Series(dtype=float)), errors="coerce").dropna()
    score = float(values.mean() * 5.0) if not values.empty else 0.0
    return score, f"proposal impact rows={len(rows)}"


def market_component(snapshot: pd.DataFrame, asset: str) -> tuple[float, str]:
    row = latest_for_asset(snapshot, asset)
    if row is None:
        return 0.0, "market snapshot unavailable"
    one_day = numeric(first_present(row, ["change_1d", "change_pct_1d", "pct_change_1d", "one_day_change"], 0.0), 0.0)
    five_day = numeric(first_present(row, ["change_5d", "change_pct_5d", "pct_change_5d", "five_day_change"], 0.0), 0.0)
    score = max(-5.0, min(5.0, one_day * 1.5 + five_day * 0.6))
    return score, f"market momentum 1d={one_day:.2f} 5d={five_day:.2f}"


def compute_raw_rows(
    market_snapshot: pd.DataFrame,
    signals: pd.DataFrame,
    latest_evaluations: pd.DataFrame,
    meta_learning: pd.DataFrame,
    auto_calibration: pd.DataFrame,
    human_override: pd.DataFrame,
    proposal_impact: pd.DataFrame,
    generated_at_jst: str,
) -> list[dict[str, Any]]:
    rows = []
    for asset in ASSETS:
        sig_score, rank, side, sig_note = signal_component(signals, asset)
        ev_score, ev_conf, ev_note = evaluation_component(latest_evaluations, asset)
        meta_score, meta_note = meta_component(meta_learning, asset)
        auto_score, auto_note = auto_calibration_component(auto_calibration, asset)
        override_score, override_note = human_override_component(human_override, asset)
        impact_score, impact_note = proposal_impact_component(proposal_impact, asset)
        market_score, market_note = market_component(market_snapshot, asset)
        allocation_score = max(
            0.0,
            min(100.0, 40.0 + sig_score + ev_score + meta_score + auto_score + override_score + impact_score + market_score),
        )
        available_sources = sum(
            [
                not signals[asset_mask(signals, asset)].empty if not signals.empty else False,
                not latest_evaluations[asset_mask(latest_evaluations, asset)].empty if not latest_evaluations.empty else False,
                not meta_learning[asset_mask(meta_learning, asset)].empty if not meta_learning.empty else False,
                not auto_calibration[asset_mask(auto_calibration, asset)].empty if not auto_calibration.empty else False,
                not human_override[asset_mask(human_override, asset)].empty if not human_override.empty else False,
                not proposal_impact[asset_mask(proposal_impact, asset)].empty if not proposal_impact.empty else False,
            ]
        )
        confidence = min(0.90, max(0.20, ev_conf + available_sources * 0.06))
        rows.append(
            {
                "generated_at_jst": generated_at_jst,
                "asset": asset,
                "allocation_score": round(allocation_score, 2),
                "portfolio_weight_candidate": 0.0,
                "confidence": round(confidence, 4),
                "risk_class": risk_class(asset),
                "risk_role": risk_role(asset),
                "recommended_exposure": 0.0,
                "cash_ratio_candidate": 1.0,
                "latest_rank": rank,
                "latest_side": side,
                "signal_score": round(sig_score, 4),
                "evaluation_score": round(ev_score, 4),
                "meta_learning_score": round(meta_score, 4),
                "auto_calibration_score": round(auto_score, 4),
                "human_override_score": round(override_score, 4),
                "proposal_impact_score": round(impact_score, 4),
                "rationale": "; ".join([sig_note, ev_note, meta_note, auto_note, override_note, impact_note, market_note]),
                "requires_human_approval": True,
                "weights_json_updated": False,
                "patch_applied": False,
                "generate_signal_updated": False,
                "orders_created": False,
            }
        )
    return rows


def allocate_weights(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, float]]:
    active = [max(0.0, (row["allocation_score"] - 45.0) * row["confidence"]) for row in rows]
    total_active = sum(active)
    avg_score = sum(row["allocation_score"] for row in rows) / len(rows) if rows else 0.0
    avg_confidence = sum(row["confidence"] for row in rows) / len(rows) if rows else 0.0
    if total_active <= 0:
        exposure = 0.0
    else:
        exposure = min(0.90, max(0.10, 0.45 + (avg_score - 50.0) / 100.0 + avg_confidence * 0.25))
    cash = round(1.0 - exposure, 4)
    caps = {"high": 0.28, "medium": 0.24, "defensive": 0.30}
    weights = []
    for row, active_score in zip(rows, active):
        raw_weight = exposure * active_score / total_active if total_active > 0 else 0.0
        weights.append(min(caps.get(row["risk_class"], 0.24), raw_weight))
    capped_total = sum(weights)
    if 0 < capped_total < exposure:
        scale = min(1.0, exposure / capped_total)
        weights = [min(caps.get(row["risk_class"], 0.24), weight * scale) for row, weight in zip(rows, weights)]
    final_exposure = min(exposure, sum(weights))
    final_cash = round(max(0.0, 1.0 - final_exposure), 4)
    for row, weight in zip(rows, weights):
        row["portfolio_weight_candidate"] = round(weight, 4)
        row["recommended_exposure"] = round(final_exposure, 4)
        row["cash_ratio_candidate"] = final_cash
    return rows, {"recommended_exposure": round(final_exposure, 4), "cash_ratio_candidate": final_cash}


def build_portfolio_candidates(
    market_snapshot: pd.DataFrame,
    signals: pd.DataFrame,
    latest_evaluations: pd.DataFrame,
    meta_learning: pd.DataFrame,
    auto_calibration: pd.DataFrame,
    human_override: pd.DataFrame,
    proposal_impact: pd.DataFrame,
    generated_at_jst: str,
) -> pd.DataFrame:
    rows = compute_raw_rows(
        market_snapshot,
        signals,
        latest_evaluations,
        meta_learning,
        auto_calibration,
        human_override,
        proposal_impact,
        generated_at_jst,
    )
    rows, _ = allocate_weights(rows)
    return pd.DataFrame(rows, columns=PORTFOLIO_COLUMNS)


def summary_from(candidates: pd.DataFrame, input_status: dict[str, bool], generated_at_jst: str, generated_at_utc: str) -> dict[str, Any]:
    if candidates.empty:
        weights = pd.Series(dtype=float)
        confidence = pd.Series(dtype=float)
        risk_class_values = pd.Series(dtype=str)
        risk_role_values = pd.Series(dtype=str)
    else:
        weights = pd.to_numeric(candidates["portfolio_weight_candidate"], errors="coerce").fillna(0.0)
        confidence = pd.to_numeric(candidates["confidence"], errors="coerce").fillna(0.0)
        risk_class_values = candidates["risk_class"].fillna("").astype(str)
        risk_role_values = candidates["risk_role"].fillna("").astype(str)
    candidate_mask = weights > 0
    high_risk_weight = float(weights[risk_class_values == "high"].sum()) if not candidates.empty else 0.0
    concentration = float(weights.max()) if not weights.empty else 0.0
    recommended_exposure = float(weights.sum()) if not weights.empty else 0.0
    cash_candidate = max(0.0, 1.0 - recommended_exposure)
    if candidates.empty or not any(input_status.values()):
        next_action = "generate_upstream_analysis"
    elif candidate_mask.sum() == 0:
        next_action = "hold_cash_and_review_inputs"
    else:
        next_action = "human_review_allocations"
    return {
        "generated_at_jst": generated_at_jst,
        "generated_at_utc": generated_at_utc,
        "portfolio_status": "unavailable" if candidates.empty and not any(input_status.values()) else "active",
        "candidate_assets": int(candidate_mask.sum()),
        "defensive_assets": int(((risk_role_values == "defensive") & candidate_mask).sum()) if not candidates.empty else 0,
        "offensive_assets": int(((risk_role_values == "offensive") & candidate_mask).sum()) if not candidates.empty else 0,
        "cash_candidate": round(cash_candidate, 4),
        "cash_ratio_candidate": round(cash_candidate, 4),
        "average_confidence": round(float(confidence.mean()) if not confidence.empty else 0.0, 4),
        "portfolio_concentration": round(concentration, 4),
        "risk_concentration": round(high_risk_weight, 4),
        "recommended_exposure": round(recommended_exposure, 4),
        "top_allocation_asset": clean_text(candidates.sort_values("portfolio_weight_candidate", ascending=False).iloc[0]["asset"]) if not candidates.empty else "",
        "requires_human_approval": True,
        "weights_json_updated": False,
        "patch_applied": False,
        "generate_signal_updated": False,
        "orders_created": False,
        "recommended_next_action": next_action,
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
    top = candidates.sort_values("portfolio_weight_candidate", ascending=False).head(10) if not candidates.empty else candidates
    cols = ["asset", "allocation_score", "portfolio_weight_candidate", "confidence", "risk_class", "risk_role", "latest_rank", "latest_side", "rationale"]
    return f"""# Portfolio Layer

## 1. 概要

- 生成日時JST: {summary["generated_at_jst"]}
- portfolio_status: {summary["portfolio_status"]}
- candidate assets: {summary["candidate_assets"]}
- defensive assets: {summary["defensive_assets"]}
- offensive assets: {summary["offensive_assets"]}
- cash candidate: {summary["cash_candidate"]}
- average confidence: {summary["average_confidence"]}
- portfolio concentration: {summary["portfolio_concentration"]}
- risk concentration: {summary["risk_concentration"]}
- recommended exposure: {summary["recommended_exposure"]}
- recommended next action: {summary["recommended_next_action"]}
- requires_human_approval: true
- weights_json_updated: false
- patch_applied: false
- generate_signal_updated: false
- orders_created: false

## 2. Top Allocation Candidates

{markdown_table(top[cols] if not top.empty else top)}

## 3. Risk Concentration

- high risk weight candidate: {summary["risk_concentration"]}
- portfolio concentration: {summary["portfolio_concentration"]}
- cash ratio candidate: {summary["cash_ratio_candidate"]}

## 4. 注意事項

- Portfolio Layerは配分候補を生成するだけです
- 自動売買・自動発注・自動リバランスは行いません
- weights.jsonは更新しません
- generate_signal.pyは変更しません
- Google Sheetsへの書き込みは行いません
- すべての候補は人間承認が必須です
"""


def build_portfolio_layer() -> tuple[pd.DataFrame, dict[str, Any], str]:
    generated_dt_utc = now_utc()
    generated_at_jst = format_jst(generated_dt_utc)
    generated_at_utc = format_utc(generated_dt_utc)
    market_snapshot, market_available = load_table(RESULTS_DIR / "market_snapshot.csv", RESULTS_DIR / "market_snapshot.json", ["rows", "market_snapshot"])
    signals, signals_available = load_table(RESULTS_DIR / "signals.csv", RESULTS_DIR / "signals.json", ["signals", "rows"])
    latest_evaluations, latest_available = load_table(
        RESULTS_DIR / "latest_evaluations.csv",
        RESULTS_DIR / "latest_evaluations.json",
        ["latest_evaluations", "evaluations", "rows"],
    )
    meta_learning, meta_available = load_table(RESULTS_DIR / "meta_learning.csv", RESULTS_DIR / "meta_learning.json", ["meta_learning_candidates", "candidates", "rows"])
    auto_calibration, auto_available = load_table(
        RESULTS_DIR / "auto_calibration_candidates.csv",
        RESULTS_DIR / "auto_calibration_candidates.json",
        ["candidates", "auto_calibration_candidates", "rows"],
    )
    human_override, override_available = load_table(
        RESULTS_DIR / "human_override_analytics.csv",
        RESULTS_DIR / "human_override_analytics.json",
        ["overrides", "analytics", "human_override_analytics", "rows"],
    )
    proposal_impact, impact_available = load_table(RESULTS_DIR / "proposal_impact.csv", RESULTS_DIR / "proposal_impact.json", ["proposal_impacts", "impacts", "rows"])
    input_status = {
        "market_snapshot_available": market_available,
        "signals_available": signals_available,
        "latest_evaluations_available": latest_available,
        "meta_learning_available": meta_available,
        "auto_calibration_candidates_available": auto_available,
        "human_override_analytics_available": override_available,
        "proposal_impact_available": impact_available,
    }
    candidates = build_portfolio_candidates(
        market_snapshot,
        signals,
        latest_evaluations,
        meta_learning,
        auto_calibration,
        human_override,
        proposal_impact,
        generated_at_jst,
    )
    summary = summary_from(candidates, input_status, generated_at_jst, generated_at_utc)
    payload = {
        **summary,
        "source": {
            "market_snapshot": "results/market_snapshot.json",
            "signals": "results/signals.json",
            "latest_evaluations": "results/latest_evaluations.json",
            "meta_learning": "results/meta_learning.json",
            "auto_calibration_candidates": "results/auto_calibration_candidates.json",
            "human_override_analytics": "results/human_override_analytics.json",
            "proposal_impact": "results/proposal_impact.json",
        },
        "input_status": input_status,
        "safety": {
            "requires_human_approval": True,
            "weights_json_updated": False,
            "patch_applied": False,
            "generate_signal_updated": False,
            "orders_created": False,
            "google_sheets_written": False,
        },
        "portfolio_candidates": candidates.to_dict(orient="records"),
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_date = generated_at_jst[:10]
    csv_path = RESULTS_DIR / "portfolio_layer.csv"
    json_path = RESULTS_DIR / "portfolio_layer.json"
    summary_path = RESULTS_DIR / "portfolio_layer_summary.json"
    report_path = REPORTS_DIR / f"{report_date}_portfolio_layer.md"
    candidates.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    report_path.write_text(render_markdown(summary, candidates), encoding="utf-8")
    print(f"portfolio layer generated: {report_path}")
    print(f"portfolio candidate rows: {len(candidates)}")
    return candidates, summary, str(report_path)


def main() -> int:
    build_portfolio_layer()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
