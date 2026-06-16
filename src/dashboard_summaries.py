from __future__ import annotations

"""Dashboard サマリー関数群 (機能変更なし・build_dashboardから分離)。

DataFrame/JSON/textを受け取りdictを返す純粋関数。数値・分類ロジックは変更しない。
"""

import pandas as pd

import analyze_reason_codes as arc

from dashboard_io import *  # noqa: F401,F403 - 低レベルヘルパーの再利用
from dashboard_io import latest_date, latest_file_date, normalize_headers, numeric_or


# === Data Health / Freshness (古い・空のデータを正常と誤読しないためのガード) ===
# 各レイヤーの想定更新間隔(時間)。これを超えたら stale とみなす。
# daily=36h, weekly≈8.5日=204h, monthly≈35日=840h。
LAYER_HEALTH_REGISTRY = [
    {"label": "signals", "ts": ("date", "latest_signal_date"), "rows": "signals", "threshold_hours": 36, "cadence": "daily"},
    {"label": "evaluations", "ts": ("date", "latest_evaluation_date"), "rows": "evaluations", "threshold_hours": 48, "cadence": "daily"},
    {"label": "latest_evaluations", "ts": ("json", "latest_evaluations_summary_json", "generated_at_utc"), "rows": "latest_evaluations", "threshold_hours": 36, "cadence": "daily"},
    {"label": "weekly_review", "ts": ("date", "latest_weekly_review_date"), "rows": "weekly_review", "threshold_hours": 204, "cadence": "weekly"},
    {"label": "monthly_calibration", "ts": ("date", "latest_monthly_calibration_date"), "rows": "monthly_calibration", "threshold_hours": 840, "cadence": "monthly"},
    {"label": "prediction_calibration", "ts": ("json", "prediction_calibration_json", "generated_at_utc"), "rows": "prediction_calibration", "threshold_hours": 36, "cadence": "daily"},
    {"label": "narrative_reliability", "ts": ("json", "narrative_reliability_json", "generated_at_utc"), "rows": "narrative_reliability", "threshold_hours": 36, "cadence": "daily"},
    {"label": "narrative_lookahead_audit", "ts": ("json", "narrative_lookahead_audit_summary_json", "generated_at_utc"), "rows": "narrative_lookahead_audit", "threshold_hours": 36, "cadence": "daily"},
    {"label": "adversarial_review", "ts": ("json", "adversarial_review_summary_json", "generated_at_utc"), "rows": "adversarial_review", "threshold_hours": 36, "cadence": "daily", "allow_empty": True},
    {"label": "news_narrative", "ts": ("json", "news_narrative_scores_json", "generated_at_utc"), "rows": "news_narrative_scores", "threshold_hours": 36, "cadence": "daily"},
    {"label": "ai_feedback", "ts": ("json", "ai_feedback_json", "generated_at_utc"), "rows": "ai_feedback", "threshold_hours": 36, "cadence": "daily"},
    {"label": "portfolio_layer", "ts": ("json", "portfolio_layer_summary_json", "generated_at_utc"), "rows": "portfolio_layer", "threshold_hours": 204, "cadence": "weekly"},
    {"label": "datetime_audit", "ts": ("json", "datetime_audit_summary_json", "generated_at_utc"), "rows": "datetime_audit", "threshold_hours": 36, "cadence": "daily"},
    {"label": "model_state_proposals", "ts": ("json", "model_state_update_summary_json", "generated_at_jst"), "rows": "model_state_update_proposals", "threshold_hours": 36, "cadence": "daily"},
]

# 健全性の重大度(高いほど悪い)
_HEALTH_RANK = {"fresh": 0, "unknown_age": 1, "empty": 2, "stale": 3, "unavailable": 4, "missing": 5}


def parse_generated_at(value):
    """'YYYY-MM-DD HH:MM:SS UTC' / '... JST' / 'YYYY-MM-DD' を naive(UTC) Timestamp へ。"""
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    s = str(value).strip()
    if not s:
        return None
    is_jst = s.endswith("JST")
    s2 = s.replace(" UTC", "").replace(" JST", "").strip()
    ts = pd.to_datetime(s2, errors="coerce")
    if pd.isna(ts):
        return None
    ts = pd.Timestamp(ts)
    if ts.tzinfo is not None:
        ts = ts.tz_convert("UTC").tz_localize(None)
    if is_jst:
        ts = ts - pd.Timedelta(hours=9)  # JST -> UTC
    return ts


def _now_naive_utc(now):
    ts = pd.Timestamp(now)
    if ts.tzinfo is not None:
        ts = ts.tz_convert("UTC").tz_localize(None)
    return ts


def assess_layer(label, ts_value, row_count, now, threshold_hours, unavailable=False, cadence="", allow_empty=False) -> dict:
    """1レイヤーの鮮度・有無を判定する純粋関数。

    status: fresh / stale / empty / missing / unavailable / unknown_age

    allow_empty=True のレイヤー(監査系: 0件=「異常なし」が正常)では、
    生成時刻があれば row_count=0 でも empty にせず鮮度で判定する。
    """
    ts = parse_generated_at(ts_value)
    now_ts = _now_naive_utc(now)
    raw_age = None
    age_hours = None
    if ts is not None:
        raw_age = (now_ts - ts).total_seconds() / 3600.0
        age_hours = round(raw_age, 1)  # 表示用のみ。判定は raw_age で行う(丸めによる false-fresh 防止)

    if unavailable:
        status = "unavailable"
    elif ts is None and row_count <= 0:
        status = "missing"
    elif row_count <= 0 and not allow_empty:
        status = "empty"
    elif ts is None:
        status = "unknown_age"
    elif raw_age is not None and raw_age > threshold_hours:
        status = "stale"
    else:
        status = "fresh"

    return {
        "layer": label,
        "status": status,
        "last_generated": ts.strftime("%Y-%m-%d %H:%M") if ts is not None else "",
        "age_hours": age_hours if age_hours is not None else "",
        "row_count": int(row_count),
        "threshold_hours": threshold_hours,
        "cadence": cadence,
    }


def _resolve_ts(spec, extras, latest_dates):
    kind = spec[0]
    if kind == "date":
        return (latest_dates or {}).get(spec[1], "")
    if kind == "json":
        payload = (extras or {}).get(spec[1])
        if isinstance(payload, list) and payload and isinstance(payload[0], dict):
            payload = payload[0]
        if isinstance(payload, dict):
            return payload.get(spec[2]) or payload.get("generated_at_jst")
    return None


def _layer_unavailable(label, extras) -> bool:
    """summaryが明示的に unavailable を示す場合に True。"""
    checks = {
        "narrative_reliability": ("narrative_reliability_json", "narrative_reliability_status"),
        "prediction_calibration": ("prediction_calibration_json", "calibration_status"),
        "narrative_lookahead_audit": ("narrative_lookahead_audit_summary_json", "audit_status"),
        "adversarial_review": ("adversarial_review_summary_json", "review_status"),
    }
    if label not in checks:
        return False
    key, field = checks[label]
    payload = (extras or {}).get(key)
    if isinstance(payload, dict):
        return str(payload.get(field, "")).strip().lower() == "unavailable"
    return False


def data_health_summary(extras, row_counts, latest_dates, now) -> dict:
    """全レイヤーの鮮度・有無を一覧化する (Phase 24)。

    「古い/空のデータを正常と誤読しない」ためのDashboard freshness guard。
    分析・表示専用であり、weights.json等は一切変更しない。
    """
    layers = []
    for spec in LAYER_HEALTH_REGISTRY:
        ts_value = _resolve_ts(spec["ts"], extras, latest_dates)
        row_count = int((row_counts or {}).get(spec["rows"], 0)) if spec.get("rows") else 0
        unavailable = _layer_unavailable(spec["label"], extras)
        layers.append(assess_layer(
            spec["label"], ts_value, row_count, now, spec["threshold_hours"],
            unavailable=unavailable, cadence=spec.get("cadence", ""), allow_empty=spec.get("allow_empty", False),
        ))

    counts = {k: 0 for k in _HEALTH_RANK}
    for layer in layers:
        counts[layer["status"]] = counts.get(layer["status"], 0) + 1

    if counts["missing"] > 0 or counts["unavailable"] > 0:
        health_status = "critical"
    elif counts["stale"] > 0 or counts["empty"] > 0:
        health_status = "degraded"
    elif counts["unknown_age"] > 0:
        health_status = "watch"
    else:
        health_status = "healthy"

    worst = max(layers, key=lambda x: _HEALTH_RANK.get(x["status"], 0)) if layers else None
    attention = [l for l in layers if l["status"] in ("stale", "empty", "missing", "unavailable")]

    return {
        "available": True,
        "health_status": health_status,
        "total_layers": len(layers),
        "fresh_count": counts["fresh"],
        "stale_count": counts["stale"],
        "empty_count": counts["empty"],
        "missing_count": counts["missing"],
        "unavailable_count": counts["unavailable"],
        "unknown_age_count": counts["unknown_age"],
        "worst_layer": worst["layer"] if worst else "",
        "worst_status": worst["status"] if worst else "",
        "attention_layers": [l["layer"] for l in attention],
        "layers": layers,
        "requires_human_approval": True,
        "weights_json_updated": False,
        "generate_signal_updated": False,
    }


def latest_signals(signals: pd.DataFrame) -> pd.DataFrame:
    date_col = "date" if "date" in signals.columns else "signal_date" if "signal_date" in signals.columns else ""
    if signals.empty or not date_col:
        return pd.DataFrame()
    out = signals.copy()
    out["_date"] = pd.to_datetime(out[date_col], errors="coerce", utc=True).dt.tz_localize(None)
    if out["_date"].dropna().empty:
        return signals
    latest = out["_date"].max()
    return out[out["_date"] == latest].drop(columns=["_date"])


def signal_summary(signals: pd.DataFrame) -> dict:
    if signals.empty or "rank" not in signals.columns:
        return {"A": 0, "B": 0, "NO_TRADE": 0}
    rank = signals["rank"].fillna("").astype(str).str.upper()
    return {
        "A": int((rank == "A").sum()),
        "B": int((rank == "B").sum()),
        "NO_TRADE": int((rank == "NO_TRADE").sum()),
    }


def evaluation_summary(evaluations: pd.DataFrame) -> dict:
    if evaluations.empty:
        return {
            "total_evaluated": 0,
            "closed": 0,
            "pending": 0,
            "skipped": 0,
            "no_entry": 0,
            "no_trade": 0,
            "win_rate": 0.0,
            "total_r": 0.0,
            "average_r": 0.0,
            "best_r": 0.0,
            "worst_r": 0.0,
            "missed_opportunity_count": 0,
        }
    out = evaluations.copy()
    if "evaluation_date" in out.columns:
        out["_date"] = pd.to_datetime(out["evaluation_date"], errors="coerce", utc=True).dt.tz_localize(None)
        cutoff = pd.Timestamp(datetime.now().date()) - pd.Timedelta(days=29)
        if not out["_date"].dropna().empty:
            out = out[(out["_date"].isna()) | (out["_date"] >= cutoff)]
    status = out.get("evaluation_status", out.get("status", pd.Series(index=out.index, dtype=str))).fillna("").astype(str).str.lower()
    outcome = out.get("outcome", pd.Series(index=out.index, dtype=str)).fillna("").astype(str)
    r = pd.to_numeric(out.get("r_multiple", out.get("r_result", pd.Series(index=out.index, dtype=float))), errors="coerce")
    wins = outcome.isin(["win_tp1", "win_tp2"]) | (r > 0)
    evaluated_count = int(r.notna().sum())
    return {
        "total_evaluated": evaluated_count,
        "closed": int((status == "closed").sum()),
        "pending": int((status == "pending").sum()),
        "skipped": int((status == "skipped").sum()),
        "no_entry": int((outcome == "no_entry").sum()),
        "no_trade": int((outcome.astype(str).str.startswith("no_trade")).sum()),
        "win_rate": float(wins.sum() / evaluated_count) if evaluated_count else 0.0,
        "total_r": float(r.dropna().sum()) if evaluated_count else 0.0,
        "average_r": float(r.dropna().mean()) if evaluated_count else 0.0,
        "best_r": float(r.dropna().max()) if evaluated_count else 0.0,
        "worst_r": float(r.dropna().min()) if evaluated_count else 0.0,
        "missed_opportunity_count": int(out.get("missed_opportunity", pd.Series(index=out.index, dtype=str)).fillna("").astype(str).str.lower().isin(["true", "1", "yes"]).sum()),
    }


def asset_performance(signals: pd.DataFrame, evaluations: pd.DataFrame) -> pd.DataFrame:
    assets = set()
    if not signals.empty and "asset" in signals.columns:
        assets |= set(signals["asset"].dropna().astype(str))
    if not evaluations.empty and "asset" in evaluations.columns:
        assets |= set(evaluations["asset"].dropna().astype(str))
    rows = []
    for asset in sorted(assets):
        sig = signals[signals["asset"].astype(str) == asset] if "asset" in signals.columns and not signals.empty else pd.DataFrame()
        ev = evaluations[evaluations["asset"].astype(str) == asset] if "asset" in evaluations.columns and not evaluations.empty else pd.DataFrame()
        metrics = evaluation_summary(ev)
        rows.append(
            {
                "asset": asset,
                "signals": len(sig),
                "evaluations": len(ev),
                "win_rate": metrics["win_rate"],
                "total_r": metrics["total_r"],
                "average_r": metrics["average_r"],
                "missed_opportunity_count": metrics["missed_opportunity_count"],
            }
        )
    return pd.DataFrame(rows)


def reason_code_data(signals: pd.DataFrame, evaluations: pd.DataFrame, reason_csv: pd.DataFrame, reason_json) -> tuple[pd.DataFrame, pd.DataFrame]:
    reason_table = reason_csv.copy()
    no_trade_table = pd.DataFrame()
    if reason_json:
        no_trade_table = pd.DataFrame(reason_json.get("no_trade_reason_summary", []))
        no_trade_table = normalize_headers(no_trade_table)
    if reason_table.empty:
        merged = arc.combine_signals_evaluations(signals, evaluations)
        reason_table = arc.reason_summary(arc.explode_reason_codes(merged))
        if no_trade_table.empty:
            no_trade_table = arc.no_trade_summary(merged)
    return normalize_headers(reason_table), normalize_headers(no_trade_table)


def weekly_monthly_mode(weekly: pd.DataFrame, monthly: pd.DataFrame) -> dict:
    row_w = weekly.iloc[-1].to_dict() if not weekly.empty else {}
    row_m = monthly.iloc[-1].to_dict() if not monthly.empty else {}
    return {
        "next_week_mode": row_w.get("next_week_mode", "not available"),
        "next_month_mode": row_m.get("next_month_mode", "not available"),
        "max_daily_risk_pct": row_m.get("max_daily_risk_pct", row_w.get("max_daily_risk_pct", "not available")),
        "best_asset": row_m.get("best_asset", row_w.get("best_asset", "not available")),
        "worst_asset": row_m.get("worst_asset", row_w.get("worst_asset", "not available")),
        "best_rank": row_m.get("best_rank", "not available"),
        "worst_rank": row_m.get("worst_rank", "not available"),
    }


def ai_feedback_summary(ai_feedback: pd.DataFrame, ai_feedback_json) -> dict:
    if not ai_feedback_json and ai_feedback.empty:
        return {
            "available": False,
            "latest_date": "",
            "market_mode_summary": "AIフィードバック未取得",
            "alignment_counts": {"aligned": 0, "conflicted": 0, "neutral": 0, "insufficient_data": 0},
            "improvement_hypotheses": [],
        }
    counts = {"aligned": 0, "conflicted": 0, "neutral": 0, "insufficient_data": 0}
    if not ai_feedback.empty and "narrative_alignment" in ai_feedback.columns:
        raw_counts = ai_feedback["narrative_alignment"].fillna("neutral").astype(str).value_counts().to_dict()
        counts = {key: int(raw_counts.get(key, 0)) for key in counts}
    latest = ""
    market_mode = "データなし"
    hypotheses = []
    if ai_feedback_json:
        latest = str(ai_feedback_json.get("date", "") or "")
        market_mode = str(ai_feedback_json.get("market_mode_summary", "データなし"))
        hypotheses = list(ai_feedback_json.get("improvement_hypotheses", []) or [])
        if not any(counts.values()):
            for row in ai_feedback_json.get("signal_alignment", []) or []:
                key = str(row.get("narrative_alignment", "neutral"))
                if key in counts:
                    counts[key] += 1
    elif not ai_feedback.empty:
        latest = latest_date(ai_feedback, ["date"])
    return {
        "available": True,
        "latest_date": latest,
        "market_mode_summary": market_mode,
        "alignment_counts": counts,
        "improvement_hypotheses": hypotheses[:3],
    }


def news_narrative_summary(news_csv: pd.DataFrame, news_json) -> dict:
    if isinstance(news_json, dict) and news_json:
        return {
            "available": True,
            "latest_news_fetched_at": news_json.get("generated_at_jst", ""),
            "news_fetch_status": news_json.get("news_fetch_status", "unavailable"),
            "news_fetch_success_source_count": int(numeric_or(news_json.get("news_fetch_success_source_count", 0), 0)),
            "news_fetch_failed_source_count": int(numeric_or(news_json.get("news_fetch_failed_source_count", 0), 0)),
            "news_fetch_elapsed_seconds": numeric_or(news_json.get("news_fetch_elapsed_seconds", 0), 0.0),
            "headline_count": int(numeric_or(news_json.get("headline_count", 0), 0)),
            "news_market_bias": news_json.get("news_market_bias", "insufficient_data"),
            "news_conflict_score": numeric_or(news_json.get("news_conflict_score", 0), 0.0),
            "dominant_news_themes": list(news_json.get("dominant_news_themes", []) or []),
            "news_summary_ja": news_json.get("news_summary_ja", "ニュースナラティブ未取得"),
            "news_confidence": numeric_or(news_json.get("news_confidence", 0), 0.0),
            "risk_on_news_score": numeric_or(news_json.get("risk_on_news_score", 0), 0.0),
            "risk_off_news_score": numeric_or(news_json.get("risk_off_news_score", 0), 0.0),
            "dollar_strength_news_score": numeric_or(news_json.get("dollar_strength_news_score", 0), 0.0),
            "rate_pressure_news_score": numeric_or(news_json.get("rate_pressure_news_score", 0), 0.0),
            "geopolitical_risk_news_score": numeric_or(news_json.get("geopolitical_risk_news_score", 0), 0.0),
            "oil_supply_risk_news_score": numeric_or(news_json.get("oil_supply_risk_news_score", 0), 0.0),
            "crypto_liquidity_news_score": numeric_or(news_json.get("crypto_liquidity_news_score", 0), 0.0),
            "top_news_drivers": list(news_json.get("top_news_drivers", []) or [])[:5],
        }
    if not news_csv.empty:
        row = news_csv.iloc[-1].to_dict()
        drivers = row.get("top_news_drivers", [])
        if isinstance(drivers, str):
            try:
                drivers = json.loads(drivers)
            except json.JSONDecodeError:
                drivers = []
        return {
            "available": True,
            "latest_news_fetched_at": row.get("generated_at_jst", ""),
            "news_fetch_status": row.get("news_fetch_status", "unavailable"),
            "news_fetch_success_source_count": int(numeric_or(row.get("news_fetch_success_source_count", 0), 0)),
            "news_fetch_failed_source_count": int(numeric_or(row.get("news_fetch_failed_source_count", 0), 0)),
            "news_fetch_elapsed_seconds": numeric_or(row.get("news_fetch_elapsed_seconds", 0), 0.0),
            "headline_count": int(numeric_or(row.get("headline_count", 0), 0)),
            "news_market_bias": row.get("news_market_bias", "insufficient_data"),
            "news_conflict_score": numeric_or(row.get("news_conflict_score", 0), 0.0),
            "dominant_news_themes": str(row.get("dominant_news_themes", "") or "").split("|") if row.get("dominant_news_themes", "") else [],
            "news_summary_ja": row.get("news_summary_ja", "ニュースナラティブ未取得"),
            "news_confidence": numeric_or(row.get("news_confidence", 0), 0.0),
            "risk_on_news_score": numeric_or(row.get("risk_on_news_score", 0), 0.0),
            "risk_off_news_score": numeric_or(row.get("risk_off_news_score", 0), 0.0),
            "dollar_strength_news_score": numeric_or(row.get("dollar_strength_news_score", 0), 0.0),
            "rate_pressure_news_score": numeric_or(row.get("rate_pressure_news_score", 0), 0.0),
            "geopolitical_risk_news_score": numeric_or(row.get("geopolitical_risk_news_score", 0), 0.0),
            "oil_supply_risk_news_score": numeric_or(row.get("oil_supply_risk_news_score", 0), 0.0),
            "crypto_liquidity_news_score": numeric_or(row.get("crypto_liquidity_news_score", 0), 0.0),
            "top_news_drivers": drivers[:5] if isinstance(drivers, list) else [],
        }
    return {
        "available": False,
        "latest_news_fetched_at": "",
        "news_fetch_status": "unavailable",
        "news_fetch_success_source_count": 0,
        "news_fetch_failed_source_count": 0,
        "news_fetch_elapsed_seconds": 0.0,
        "headline_count": 0,
        "news_market_bias": "insufficient_data",
        "news_conflict_score": 0.0,
        "dominant_news_themes": [],
        "news_summary_ja": "ニュースナラティブ未取得",
        "news_confidence": 0.0,
        "risk_on_news_score": 0.0,
        "risk_off_news_score": 0.0,
        "dollar_strength_news_score": 0.0,
        "rate_pressure_news_score": 0.0,
        "geopolitical_risk_news_score": 0.0,
        "oil_supply_risk_news_score": 0.0,
        "crypto_liquidity_news_score": 0.0,
        "top_news_drivers": [],
    }


def model_state_update_summary(proposals: pd.DataFrame, proposals_json, summary_json) -> dict:
    if isinstance(summary_json, dict) and summary_json:
        strong = proposals[proposals["proposal_strength"].astype(str) == "strong"] if not proposals.empty and "proposal_strength" in proposals.columns else pd.DataFrame()
        return {
            "available": True,
            "model_state_total_proposals": int(numeric_or(summary_json.get("total_proposals", len(proposals)), 0)),
            "model_state_increase_count": int(numeric_or(summary_json.get("increase_count", 0), 0)),
            "model_state_decrease_count": int(numeric_or(summary_json.get("decrease_count", 0), 0)),
            "model_state_hold_count": int(numeric_or(summary_json.get("hold_count", 0), 0)),
            "model_state_insufficient_data_count": int(numeric_or(summary_json.get("insufficient_data_count", 0), 0)),
            "model_state_apply_automatically": str((summary_json.get("safety", {}) or {}).get("apply_automatically", False)).lower(),
            "strong_candidates": strong.head(5).to_dict(orient="records"),
        }
    if isinstance(proposals_json, dict) and proposals_json:
        summary = proposals_json.get("summary", {}) or {}
        rows = proposals_json.get("proposals", []) or []
        table = normalize_headers(pd.DataFrame(rows))
        strong = table[table["proposal_strength"].astype(str) == "strong"] if not table.empty and "proposal_strength" in table.columns else pd.DataFrame()
        return {
            "available": True,
            "model_state_total_proposals": int(numeric_or(summary.get("total_proposals", len(rows)), 0)),
            "model_state_increase_count": int(numeric_or(summary.get("increase_count", 0), 0)),
            "model_state_decrease_count": int(numeric_or(summary.get("decrease_count", 0), 0)),
            "model_state_hold_count": int(numeric_or(summary.get("hold_count", 0), 0)),
            "model_state_insufficient_data_count": int(numeric_or(summary.get("insufficient_data_count", 0), 0)),
            "model_state_apply_automatically": str((proposals_json.get("safety", {}) or {}).get("apply_automatically", False)).lower(),
            "strong_candidates": strong.head(5).to_dict(orient="records"),
        }
    if not proposals.empty:
        strong = proposals[proposals["proposal_strength"].astype(str) == "strong"] if "proposal_strength" in proposals.columns else pd.DataFrame()
        direction = proposals.get("proposal_direction", pd.Series("", index=proposals.index)).fillna("").astype(str)
        confidence = proposals.get("confidence_level", pd.Series("", index=proposals.index)).fillna("").astype(str)
        return {
            "available": True,
            "model_state_total_proposals": int(len(proposals)),
            "model_state_increase_count": int((direction == "increase").sum()),
            "model_state_decrease_count": int((direction == "decrease").sum()),
            "model_state_hold_count": int((direction == "hold").sum()),
            "model_state_insufficient_data_count": int((confidence == "insufficient_data").sum()),
            "model_state_apply_automatically": "false",
            "strong_candidates": strong.head(5).to_dict(orient="records"),
        }
    return {
        "available": False,
        "model_state_total_proposals": 0,
        "model_state_increase_count": 0,
        "model_state_decrease_count": 0,
        "model_state_hold_count": 0,
        "model_state_insufficient_data_count": 0,
        "model_state_apply_automatically": "false",
        "strong_candidates": [],
    }


def model_state_audit_summary(audit_json, audit_csv: pd.DataFrame) -> dict:
    if isinstance(audit_json, dict) and audit_json:
        return {
            "model_state_audit_status": audit_json.get("audit_status", "unavailable"),
            "model_state_audit_warning_count": int(numeric_or(audit_json.get("warning_count", 0), 0)),
            "model_state_audit_blocked_count": int(numeric_or(audit_json.get("blocked_count", 0), 0)),
            "model_state_audit_critical_count": int(numeric_or(audit_json.get("critical_count", 0), 0)),
            "model_state_requires_human_review": "必須" if audit_json.get("requires_human_review", True) else "不要",
            "model_state_weights_json_updated": str(audit_json.get("weights_json_updated", False)).lower(),
        }
    if not audit_csv.empty:
        result = audit_csv.get("audit_result", pd.Series("", index=audit_csv.index)).fillna("").astype(str)
        severity = audit_csv.get("severity", pd.Series("", index=audit_csv.index)).fillna("").astype(str)
        status = "blocked" if (result == "blocked").any() else "warning" if (result == "warning").any() else "passed"
        return {
            "model_state_audit_status": status,
            "model_state_audit_warning_count": int((result == "warning").sum()),
            "model_state_audit_blocked_count": int((result == "blocked").sum()),
            "model_state_audit_critical_count": int((severity == "critical").sum()),
            "model_state_requires_human_review": "必須",
            "model_state_weights_json_updated": "false",
        }
    return {
        "model_state_audit_status": "unavailable",
        "model_state_audit_warning_count": 0,
        "model_state_audit_blocked_count": 0,
        "model_state_audit_critical_count": 0,
        "model_state_requires_human_review": "必須",
        "model_state_weights_json_updated": "false",
    }


def weights_patch_summary(patch_csv: pd.DataFrame, patch_json, summary_json) -> dict:
    if isinstance(patch_json, dict) and patch_json:
        summary = patch_json.get("summary", {}) or {}
        safety = patch_json.get("safety", {}) or {}
        rows = patch_json.get("patches", []) or []
        return {
            "available": True,
            "weights_patch_count": int(numeric_or(summary.get("eligible_patch_count", len(rows)), 0)),
            "weights_patch_excluded_count": int(numeric_or(summary.get("excluded_count", 0), 0)),
            "weights_patch_increase_count": int(numeric_or(summary.get("increase_count", 0), 0)),
            "weights_patch_decrease_count": int(numeric_or(summary.get("decrease_count", 0), 0)),
            "weights_patch_requires_human_approval": "必須" if safety.get("requires_human_approval", True) else "不要",
            "weights_patch_applied": str(safety.get("patch_applied", False)).lower(),
            "weights_patch_weights_json_updated": str(safety.get("weights_json_updated", False)).lower(),
            "patch_candidates": rows[:5],
        }
    if isinstance(summary_json, dict) and summary_json:
        safety = summary_json.get("safety", {}) or {}
        return {
            "available": True,
            "weights_patch_count": int(numeric_or(summary_json.get("eligible_patch_count", len(patch_csv)), 0)),
            "weights_patch_excluded_count": int(numeric_or(summary_json.get("excluded_count", 0), 0)),
            "weights_patch_increase_count": int(numeric_or(summary_json.get("increase_count", 0), 0)),
            "weights_patch_decrease_count": int(numeric_or(summary_json.get("decrease_count", 0), 0)),
            "weights_patch_requires_human_approval": "必須" if safety.get("requires_human_approval", True) else "不要",
            "weights_patch_applied": str(safety.get("patch_applied", False)).lower(),
            "weights_patch_weights_json_updated": str(safety.get("weights_json_updated", False)).lower(),
            "patch_candidates": patch_csv.head(5).to_dict(orient="records"),
        }
    if not patch_csv.empty:
        direction = patch_csv.get("proposal_direction", pd.Series("", index=patch_csv.index)).fillna("").astype(str)
        return {
            "available": True,
            "weights_patch_count": int(len(patch_csv)),
            "weights_patch_excluded_count": 0,
            "weights_patch_increase_count": int((direction == "increase").sum()),
            "weights_patch_decrease_count": int((direction == "decrease").sum()),
            "weights_patch_requires_human_approval": "必須",
            "weights_patch_applied": "false",
            "weights_patch_weights_json_updated": "false",
            "patch_candidates": patch_csv.head(5).to_dict(orient="records"),
        }
    return {
        "available": False,
        "weights_patch_count": 0,
        "weights_patch_excluded_count": 0,
        "weights_patch_increase_count": 0,
        "weights_patch_decrease_count": 0,
        "weights_patch_requires_human_approval": "必須",
        "weights_patch_applied": "false",
        "weights_patch_weights_json_updated": "false",
        "patch_candidates": [],
    }


def weights_patch_review_summary(review_csv: pd.DataFrame, review_json, summary_json) -> dict:
    if isinstance(review_json, dict) and review_json:
        rows = review_json.get("patch_review", []) or []
        return {
            "available": True,
            "weights_patch_review_status": review_json.get("review_status", "unavailable"),
            "weights_patch_review_candidate_count": int(numeric_or(review_json.get("candidate_count", 0), 0)),
            "weights_patch_review_hold_count": int(numeric_or(review_json.get("hold_count", 0), 0)),
            "weights_patch_review_reject_count": int(numeric_or(review_json.get("reject_count", 0), 0)),
            "weights_patch_review_blocked_count": int(numeric_or(review_json.get("blocked_count", 0), 0)),
            "weights_patch_review_recommended_next_action": review_json.get("recommended_next_action", "no_action"),
            "weights_patch_review_requires_human_approval": "必須" if review_json.get("requires_human_approval", True) else "不要",
            "weights_patch_review_patch_applied": str(review_json.get("patch_applied", False)).lower(),
            "weights_patch_review_weights_json_updated": str(review_json.get("weights_json_updated", False)).lower(),
            "candidate_rows": [row for row in rows if str(row.get("review_decision", "")) == "candidate"][:5],
            "hold_rows": [row for row in rows if str(row.get("review_decision", "")) == "hold"][:5],
        }
    if isinstance(summary_json, dict) and summary_json:
        candidates = review_csv[review_csv["review_decision"].astype(str) == "candidate"].head(5) if not review_csv.empty and "review_decision" in review_csv.columns else pd.DataFrame()
        holds = review_csv[review_csv["review_decision"].astype(str) == "hold"].head(5) if not review_csv.empty and "review_decision" in review_csv.columns else pd.DataFrame()
        return {
            "available": True,
            "weights_patch_review_status": summary_json.get("review_status", "unavailable"),
            "weights_patch_review_candidate_count": int(numeric_or(summary_json.get("candidate_count", 0), 0)),
            "weights_patch_review_hold_count": int(numeric_or(summary_json.get("hold_count", 0), 0)),
            "weights_patch_review_reject_count": int(numeric_or(summary_json.get("reject_count", 0), 0)),
            "weights_patch_review_blocked_count": int(numeric_or(summary_json.get("blocked_count", 0), 0)),
            "weights_patch_review_recommended_next_action": summary_json.get("recommended_next_action", "no_action"),
            "weights_patch_review_requires_human_approval": "必須" if summary_json.get("requires_human_approval", True) else "不要",
            "weights_patch_review_patch_applied": str(summary_json.get("patch_applied", False)).lower(),
            "weights_patch_review_weights_json_updated": str(summary_json.get("weights_json_updated", False)).lower(),
            "candidate_rows": candidates.to_dict(orient="records"),
            "hold_rows": holds.to_dict(orient="records"),
        }
    if not review_csv.empty and "review_decision" in review_csv.columns:
        decision = review_csv["review_decision"].fillna("").astype(str)
        risk = review_csv.get("patch_risk_level", pd.Series("", index=review_csv.index)).fillna("").astype(str)
        return {
            "available": True,
            "weights_patch_review_status": "blocked" if (decision == "blocked").any() else "warning" if decision.isin(["hold", "reject"]).any() else "passed",
            "weights_patch_review_candidate_count": int((decision == "candidate").sum()),
            "weights_patch_review_hold_count": int((decision == "hold").sum()),
            "weights_patch_review_reject_count": int((decision == "reject").sum()),
            "weights_patch_review_blocked_count": int((decision == "blocked").sum()),
            "weights_patch_review_recommended_next_action": "manual_review" if (decision == "candidate").any() else "wait_for_more_data" if (decision == "hold").any() else "no_action",
            "weights_patch_review_requires_human_approval": "必須",
            "weights_patch_review_patch_applied": "false",
            "weights_patch_review_weights_json_updated": "false",
            "weights_patch_review_low_risk_count": int((risk == "low").sum()),
            "weights_patch_review_medium_risk_count": int((risk == "medium").sum()),
            "weights_patch_review_high_risk_count": int((risk == "high").sum()),
            "candidate_rows": review_csv[decision == "candidate"].head(5).to_dict(orient="records"),
            "hold_rows": review_csv[decision == "hold"].head(5).to_dict(orient="records"),
        }
    return {
        "available": False,
        "weights_patch_review_status": "unavailable",
        "weights_patch_review_candidate_count": 0,
        "weights_patch_review_hold_count": 0,
        "weights_patch_review_reject_count": 0,
        "weights_patch_review_blocked_count": 0,
        "weights_patch_review_recommended_next_action": "no_action",
        "weights_patch_review_requires_human_approval": "必須",
        "weights_patch_review_patch_applied": "false",
        "weights_patch_review_weights_json_updated": "false",
        "candidate_rows": [],
        "hold_rows": [],
    }


def proposal_adoption_summary(adoption_csv: pd.DataFrame, adoption_json, summary_json) -> dict:
    payload = adoption_json if isinstance(adoption_json, dict) and adoption_json else summary_json if isinstance(summary_json, dict) else {}
    if payload:
        rows = adoption_json.get("adoptions", []) if isinstance(adoption_json, dict) else []
        if not rows and not adoption_csv.empty:
            rows = adoption_csv.to_dict(orient="records")
        return {
            "available": True,
            "proposal_adoption_tracking_status": payload.get("tracking_status", "unavailable"),
            "proposal_adoption_total_count": int(numeric_or(payload.get("total_tracked_proposals", len(rows)), 0)),
            "proposal_adoption_accepted_count": int(numeric_or(payload.get("accepted_count", 0), 0)),
            "proposal_adoption_pending_review_count": int(numeric_or(payload.get("pending_review_count", 0), 0)),
            "proposal_adoption_held_count": int(numeric_or(payload.get("held_count", 0), 0)),
            "proposal_adoption_rejected_count": int(numeric_or(payload.get("rejected_count", 0), 0)),
            "proposal_adoption_blocked_count": int(numeric_or(payload.get("blocked_count", 0), 0)),
            "proposal_adoption_superseded_count": int(numeric_or(payload.get("superseded_count", 0), 0)),
            "proposal_adoption_manual_decision_count": int(numeric_or(payload.get("manual_decision_count", 0), 0)),
            "proposal_adoption_derived_decision_count": int(numeric_or(payload.get("derived_decision_count", 0), 0)),
            "proposal_adoption_recommended_next_action": payload.get("recommended_next_action", "no_action"),
            "pending_rows": [row for row in rows if str(row.get("adoption_status", "")) == "pending_review"][:5],
            "held_rows": [row for row in rows if str(row.get("adoption_status", "")) == "held"][:5],
        }
    if not adoption_csv.empty and "adoption_status" in adoption_csv.columns:
        status = adoption_csv["adoption_status"].fillna("").astype(str)
        source = adoption_csv.get("adoption_source", pd.Series("", index=adoption_csv.index)).fillna("").astype(str)
        return {
            "available": True,
            "proposal_adoption_tracking_status": "active",
            "proposal_adoption_total_count": int(len(adoption_csv)),
            "proposal_adoption_accepted_count": int((status == "accepted").sum()),
            "proposal_adoption_pending_review_count": int((status == "pending_review").sum()),
            "proposal_adoption_held_count": int((status == "held").sum()),
            "proposal_adoption_rejected_count": int((status == "rejected").sum()),
            "proposal_adoption_blocked_count": int((status == "blocked").sum()),
            "proposal_adoption_superseded_count": int((status == "superseded").sum()),
            "proposal_adoption_manual_decision_count": int((source == "manual").sum()),
            "proposal_adoption_derived_decision_count": int((source == "derived_from_review").sum()),
            "proposal_adoption_recommended_next_action": "manual_review" if (status == "pending_review").any() else "wait_for_more_data" if (status == "held").any() else "no_action",
            "pending_rows": adoption_csv[status == "pending_review"].head(5).to_dict(orient="records"),
            "held_rows": adoption_csv[status == "held"].head(5).to_dict(orient="records"),
        }
    return {
        "available": False,
        "proposal_adoption_tracking_status": "unavailable",
        "proposal_adoption_total_count": 0,
        "proposal_adoption_accepted_count": 0,
        "proposal_adoption_pending_review_count": 0,
        "proposal_adoption_held_count": 0,
        "proposal_adoption_rejected_count": 0,
        "proposal_adoption_blocked_count": 0,
        "proposal_adoption_superseded_count": 0,
        "proposal_adoption_manual_decision_count": 0,
        "proposal_adoption_derived_decision_count": 0,
        "proposal_adoption_recommended_next_action": "no_action",
        "pending_rows": [],
        "held_rows": [],
    }


def weight_version_history_summary(history_csv: pd.DataFrame, history_json, summary_json) -> dict:
    payload = history_json if isinstance(history_json, dict) and history_json else summary_json if isinstance(summary_json, dict) else {}
    if payload:
        rows = history_json.get("proposals", []) if isinstance(history_json, dict) else []
        if not rows and not history_csv.empty:
            rows = history_csv.to_dict(orient="records")
        return {
            "available": True,
            "weight_history_current_version": payload.get("current_version", "v1"),
            "weight_history_version_count": int(numeric_or(payload.get("version_count", 1), 1)),
            "weight_history_tracked_count": int(numeric_or(payload.get("tracked_count", 0), 0)),
            "weight_history_held_count": int(numeric_or(payload.get("held_count", 0), 0)),
            "weight_history_candidate_count": int(numeric_or(payload.get("candidate_count", 0), 0)),
            "weight_history_approved_count": int(numeric_or(payload.get("approved_count", 0), 0)),
            "weight_history_rejected_count": int(numeric_or(payload.get("rejected_count", 0), 0)),
            "weight_history_blocked_count": int(numeric_or(payload.get("blocked_count", 0), 0)),
            "weight_history_weights_json_updated": str(payload.get("weights_json_updated", False)).lower(),
            "weight_history_patch_applied": str(payload.get("patch_applied", False)).lower(),
            "weight_history_requires_human_approval": "必須" if payload.get("requires_human_approval", True) else "不要",
            "proposal_rows": rows[:5],
        }
    if not history_csv.empty and "adoption_status" in history_csv.columns:
        status = history_csv["adoption_status"].fillna("").astype(str)
        return {
            "available": True,
            "weight_history_current_version": "v1",
            "weight_history_version_count": 1,
            "weight_history_tracked_count": int((status == "tracked").sum()),
            "weight_history_held_count": int((status == "held").sum()),
            "weight_history_candidate_count": int((status == "candidate").sum()),
            "weight_history_approved_count": int((status == "approved").sum()),
            "weight_history_rejected_count": int((status == "rejected").sum()),
            "weight_history_blocked_count": int((status == "blocked").sum()),
            "weight_history_weights_json_updated": "false",
            "weight_history_patch_applied": "false",
            "weight_history_requires_human_approval": "必須",
            "proposal_rows": history_csv.head(5).to_dict(orient="records"),
        }
    return {
        "available": False,
        "weight_history_current_version": "v1",
        "weight_history_version_count": 1,
        "weight_history_tracked_count": 0,
        "weight_history_held_count": 0,
        "weight_history_candidate_count": 0,
        "weight_history_approved_count": 0,
        "weight_history_rejected_count": 0,
        "weight_history_blocked_count": 0,
        "weight_history_weights_json_updated": "false",
        "weight_history_patch_applied": "false",
        "weight_history_requires_human_approval": "必須",
        "proposal_rows": [],
    }


def meta_learning_summary(meta_csv: pd.DataFrame, meta_json, summary_json) -> dict:
    payload = meta_json if isinstance(meta_json, dict) and meta_json else summary_json if isinstance(summary_json, dict) else {}
    if payload:
        rows = meta_json.get("meta_learning_candidates", []) if isinstance(meta_json, dict) else []
        if not rows and not meta_csv.empty:
            rows = meta_csv.to_dict(orient="records")
        return {
            "available": True,
            "meta_learning_status": payload.get("meta_learning_status", "unavailable"),
            "meta_learning_total_candidates": int(numeric_or(payload.get("total_candidates", len(rows)), 0)),
            "meta_learning_success_pattern_count": int(numeric_or(payload.get("success_pattern_count", 0), 0)),
            "meta_learning_failure_pattern_count": int(numeric_or(payload.get("failure_pattern_count", 0), 0)),
            "meta_learning_neutral_pattern_count": int(numeric_or(payload.get("neutral_pattern_count", 0), 0)),
            "meta_learning_insufficient_data_count": int(numeric_or(payload.get("insufficient_data_count", 0), 0)),
            "meta_learning_recommended_next_action": payload.get("recommended_next_action", "wait_for_more_data"),
            "meta_learning_apply_automatically": str(payload.get("apply_automatically", False)).lower(),
            "meta_learning_weights_json_updated": str(payload.get("weights_json_updated", False)).lower(),
            "meta_learning_patch_applied": str(payload.get("patch_applied", False)).lower(),
            "meta_learning_requires_human_approval": "必須" if payload.get("requires_human_approval", True) else "不要",
            "success_rows": [row for row in rows if str(row.get("pattern_type", "")) == "success_pattern"][:5],
            "failure_rows": [row for row in rows if str(row.get("pattern_type", "")) == "failure_pattern"][:5],
        }
    if not meta_csv.empty and "pattern_type" in meta_csv.columns:
        pattern = meta_csv["pattern_type"].fillna("").astype(str)
        return {
            "available": True,
            "meta_learning_status": "active",
            "meta_learning_total_candidates": int(len(meta_csv)),
            "meta_learning_success_pattern_count": int((pattern == "success_pattern").sum()),
            "meta_learning_failure_pattern_count": int((pattern == "failure_pattern").sum()),
            "meta_learning_neutral_pattern_count": int((pattern == "neutral_pattern").sum()),
            "meta_learning_insufficient_data_count": int((pattern == "insufficient_data").sum()),
            "meta_learning_recommended_next_action": "human_review" if pattern.isin(["success_pattern", "failure_pattern"]).any() else "wait_for_more_data",
            "meta_learning_apply_automatically": "false",
            "meta_learning_weights_json_updated": "false",
            "meta_learning_patch_applied": "false",
            "meta_learning_requires_human_approval": "必須",
            "success_rows": meta_csv[pattern == "success_pattern"].head(5).to_dict(orient="records"),
            "failure_rows": meta_csv[pattern == "failure_pattern"].head(5).to_dict(orient="records"),
        }
    return {
        "available": False,
        "meta_learning_status": "unavailable",
        "meta_learning_total_candidates": 0,
        "meta_learning_success_pattern_count": 0,
        "meta_learning_failure_pattern_count": 0,
        "meta_learning_neutral_pattern_count": 0,
        "meta_learning_insufficient_data_count": 0,
        "meta_learning_recommended_next_action": "wait_for_more_data",
        "meta_learning_apply_automatically": "false",
        "meta_learning_weights_json_updated": "false",
        "meta_learning_patch_applied": "false",
        "meta_learning_requires_human_approval": "必須",
        "success_rows": [],
        "failure_rows": [],
    }


def auto_calibration_summary(candidate_csv: pd.DataFrame, candidate_json, summary_json) -> dict:
    payload = candidate_json if isinstance(candidate_json, dict) and candidate_json else summary_json if isinstance(summary_json, dict) else {}
    if payload:
        rows = candidate_json.get("candidates", []) if isinstance(candidate_json, dict) else []
        if not rows and not candidate_csv.empty:
            rows = candidate_csv.to_dict(orient="records")
        sorted_rows = sorted(rows, key=lambda row: numeric_or(row.get("confidence", 0), 0), reverse=True)
        return {
            "available": True,
            "auto_calibration_status": payload.get("candidate_status", "unavailable"),
            "auto_calibration_candidate_count": int(numeric_or(payload.get("candidate_count", len(rows)), 0)),
            "auto_calibration_increase_count": int(numeric_or(payload.get("increase_count", 0), 0)),
            "auto_calibration_decrease_count": int(numeric_or(payload.get("decrease_count", 0), 0)),
            "auto_calibration_hold_count": int(numeric_or(payload.get("hold_count", 0), 0)),
            "auto_calibration_blocked_count": int(numeric_or(payload.get("blocked_count", 0), 0)),
            "auto_calibration_insufficient_data_count": int(numeric_or(payload.get("insufficient_data_count", 0), 0)),
            "auto_calibration_recommended_next_action": payload.get("recommended_next_action", "wait_for_more_data"),
            "auto_calibration_requires_human_approval": "必須" if payload.get("requires_human_approval", True) else "不要",
            "auto_calibration_patch_applied": str(payload.get("patch_applied", False)).lower(),
            "auto_calibration_weights_json_updated": str(payload.get("weights_json_updated", False)).lower(),
            "top_candidates": sorted_rows[:5],
        }
    if not candidate_csv.empty and "classification" in candidate_csv.columns:
        classification = candidate_csv["classification"].fillna("").astype(str)
        top = candidate_csv.sort_values("confidence", ascending=False).head(5) if "confidence" in candidate_csv.columns else candidate_csv.head(5)
        return {
            "available": True,
            "auto_calibration_status": "active",
            "auto_calibration_candidate_count": int(len(candidate_csv)),
            "auto_calibration_increase_count": int((classification == "increase").sum()),
            "auto_calibration_decrease_count": int((classification == "decrease").sum()),
            "auto_calibration_hold_count": int((classification == "hold").sum()),
            "auto_calibration_blocked_count": int((classification == "blocked").sum()),
            "auto_calibration_insufficient_data_count": int((classification == "insufficient_data").sum()),
            "auto_calibration_recommended_next_action": "human_review" if classification.isin(["increase", "decrease"]).any() else "wait_for_more_data",
            "auto_calibration_requires_human_approval": "必須",
            "auto_calibration_patch_applied": "false",
            "auto_calibration_weights_json_updated": "false",
            "top_candidates": top.to_dict(orient="records"),
        }
    return {
        "available": False,
        "auto_calibration_status": "unavailable",
        "auto_calibration_candidate_count": 0,
        "auto_calibration_increase_count": 0,
        "auto_calibration_decrease_count": 0,
        "auto_calibration_hold_count": 0,
        "auto_calibration_blocked_count": 0,
        "auto_calibration_insufficient_data_count": 0,
        "auto_calibration_recommended_next_action": "wait_for_more_data",
        "auto_calibration_requires_human_approval": "必須",
        "auto_calibration_patch_applied": "false",
        "auto_calibration_weights_json_updated": "false",
        "top_candidates": [],
    }


def human_override_summary(override_csv: pd.DataFrame, override_json, summary_json) -> dict:
    payload = override_json if isinstance(override_json, dict) and override_json else summary_json if isinstance(summary_json, dict) else {}
    if payload:
        rows = override_json.get("overrides", []) if isinstance(override_json, dict) else []
        if not rows and not override_csv.empty:
            rows = override_csv.to_dict(orient="records")
        top_rows = sorted(rows, key=lambda row: abs(numeric_or(row.get("impact_score", 0), 0)), reverse=True)
        return {
            "available": True,
            "human_override_status": payload.get("analytics_status", "unavailable"),
            "human_override_total_overrides": int(numeric_or(payload.get("total_overrides", len(rows)), 0)),
            "human_override_accepted_count": int(numeric_or(payload.get("accepted_count", 0), 0)),
            "human_override_held_count": int(numeric_or(payload.get("held_count", 0), 0)),
            "human_override_rejected_count": int(numeric_or(payload.get("rejected_count", 0), 0)),
            "human_override_blocked_count": int(numeric_or(payload.get("blocked_count", 0), 0)),
            "human_override_positive_count": int(numeric_or(payload.get("positive_override_count", 0), 0)),
            "human_override_negative_count": int(numeric_or(payload.get("negative_override_count", 0), 0)),
            "human_override_unknown_count": int(numeric_or(payload.get("unknown_outcome_count", 0), 0)),
            "human_override_recommended_next_action": payload.get("recommended_next_action", "wait_for_more_data"),
            "human_override_requires_human_approval": "必須" if payload.get("requires_human_approval", True) else "不要",
            "top_rows": top_rows[:5],
        }
    if not override_csv.empty and "override_type" in override_csv.columns:
        override_type = override_csv["override_type"].fillna("").astype(str)
        impact_status = override_csv.get("impact_status", pd.Series("", index=override_csv.index)).fillna("").astype(str)
        impact_score = pd.to_numeric(override_csv.get("impact_score", pd.Series(0, index=override_csv.index)), errors="coerce").fillna(0)
        top = override_csv.reindex(impact_score.abs().sort_values(ascending=False).index).head(5) if "impact_score" in override_csv.columns else override_csv.head(5)
        return {
            "available": True,
            "human_override_status": "active",
            "human_override_total_overrides": int(len(override_csv)),
            "human_override_accepted_count": int((override_type == "accepted").sum()),
            "human_override_held_count": int((override_type == "held").sum()),
            "human_override_rejected_count": int((override_type == "rejected").sum()),
            "human_override_blocked_count": int((override_type == "blocked").sum()),
            "human_override_positive_count": int((impact_status == "positive").sum()),
            "human_override_negative_count": int((impact_status == "negative").sum()),
            "human_override_unknown_count": int((impact_status == "unknown").sum()),
            "human_override_recommended_next_action": "wait_for_proposal_impact" if (impact_status == "unknown").any() else "review_successful_overrides",
            "human_override_requires_human_approval": "必須",
            "top_rows": top.to_dict(orient="records"),
        }
    return {
        "available": False,
        "human_override_status": "unavailable",
        "human_override_total_overrides": 0,
        "human_override_accepted_count": 0,
        "human_override_held_count": 0,
        "human_override_rejected_count": 0,
        "human_override_blocked_count": 0,
        "human_override_positive_count": 0,
        "human_override_negative_count": 0,
        "human_override_unknown_count": 0,
        "human_override_recommended_next_action": "wait_for_more_data",
        "human_override_requires_human_approval": "必須",
        "top_rows": [],
    }


def portfolio_layer_summary(portfolio_csv: pd.DataFrame, portfolio_json, summary_json) -> dict:
    payload = summary_json if isinstance(summary_json, dict) and summary_json else portfolio_json if isinstance(portfolio_json, dict) else {}
    rows = portfolio_json.get("portfolio_candidates", []) if isinstance(portfolio_json, dict) else []
    if payload:
        if not rows and not portfolio_csv.empty:
            rows = portfolio_csv.to_dict(orient="records")
        top_rows = sorted(rows, key=lambda row: numeric_or(row.get("portfolio_weight_candidate", 0), 0), reverse=True)[:5]
        return {
            "available": True,
            "portfolio_status": payload.get("portfolio_status", "active"),
            "portfolio_candidate_assets": int(numeric_or(payload.get("candidate_assets", len(top_rows)), 0)),
            "portfolio_defensive_assets": int(numeric_or(payload.get("defensive_assets", 0), 0)),
            "portfolio_offensive_assets": int(numeric_or(payload.get("offensive_assets", 0), 0)),
            "portfolio_cash_candidate": numeric_or(payload.get("cash_candidate", payload.get("cash_ratio_candidate", 0)), 0),
            "portfolio_average_confidence": numeric_or(payload.get("average_confidence", 0), 0),
            "portfolio_concentration": numeric_or(payload.get("portfolio_concentration", 0), 0),
            "portfolio_risk_concentration": numeric_or(payload.get("risk_concentration", 0), 0),
            "portfolio_recommended_exposure": numeric_or(payload.get("recommended_exposure", 0), 0),
            "portfolio_recommended_next_action": payload.get("recommended_next_action", "human_review_allocations"),
            "portfolio_requires_human_approval": "必須" if payload.get("requires_human_approval", True) else "不要",
            "top_rows": top_rows,
        }
    if not portfolio_csv.empty:
        weights = pd.to_numeric(portfolio_csv.get("portfolio_weight_candidate", pd.Series(dtype=float)), errors="coerce").fillna(0)
        confidence = pd.to_numeric(portfolio_csv.get("confidence", pd.Series(dtype=float)), errors="coerce").fillna(0)
        risk_class = portfolio_csv.get("risk_class", pd.Series(dtype=str)).fillna("").astype(str)
        risk_role = portfolio_csv.get("risk_role", pd.Series(dtype=str)).fillna("").astype(str)
        candidate_mask = weights > 0
        top = portfolio_csv.sort_values("portfolio_weight_candidate", ascending=False).head(5) if "portfolio_weight_candidate" in portfolio_csv.columns else portfolio_csv.head(5)
        return {
            "available": True,
            "portfolio_status": "active",
            "portfolio_candidate_assets": int(candidate_mask.sum()),
            "portfolio_defensive_assets": int(((risk_role == "defensive") & candidate_mask).sum()),
            "portfolio_offensive_assets": int(((risk_role == "offensive") & candidate_mask).sum()),
            "portfolio_cash_candidate": max(0.0, 1.0 - float(weights.sum())),
            "portfolio_average_confidence": float(confidence.mean()) if not confidence.empty else 0,
            "portfolio_concentration": float(weights.max()) if not weights.empty else 0,
            "portfolio_risk_concentration": float(weights[risk_class == "high"].sum()) if not weights.empty else 0,
            "portfolio_recommended_exposure": float(weights.sum()),
            "portfolio_recommended_next_action": "human_review_allocations",
            "portfolio_requires_human_approval": "必須",
            "top_rows": top.to_dict(orient="records"),
        }
    return {
        "available": False,
        "portfolio_status": "unavailable",
        "portfolio_candidate_assets": 0,
        "portfolio_defensive_assets": 0,
        "portfolio_offensive_assets": 0,
        "portfolio_cash_candidate": 0,
        "portfolio_average_confidence": 0,
        "portfolio_concentration": 0,
        "portfolio_risk_concentration": 0,
        "portfolio_recommended_exposure": 0,
        "portfolio_recommended_next_action": "generate_upstream_analysis",
        "portfolio_requires_human_approval": "必須",
        "top_rows": [],
    }


def datetime_audit_summary(audit_json, summary_json, audit_csv: pd.DataFrame) -> dict:
    payload = audit_json if isinstance(audit_json, dict) and audit_json else summary_json if isinstance(summary_json, dict) else {}
    if payload:
        return {
            "available": True,
            "datetime_audit_status": payload.get("audit_status", "unavailable"),
            "datetime_issues_found": int(numeric_or(payload.get("issues_found", len(audit_csv)), 0)),
            "datetime_timezone_mismatch": int(numeric_or(payload.get("timezone_mismatch", 0), 0)),
            "datetime_naive_datetime": int(numeric_or(payload.get("naive_datetime", 0), 0)),
            "datetime_timestamp_mismatch": int(numeric_or(payload.get("timestamp_mismatch", 0), 0)),
            "datetime_recommended_action": payload.get("recommended_action", "monitor"),
        }
    if not audit_csv.empty:
        issue_type = audit_csv.get("issue_type", pd.Series("", index=audit_csv.index)).fillna("").astype(str)
        severity = audit_csv.get("severity", pd.Series("", index=audit_csv.index)).fillna("").astype(str)
        return {
            "available": True,
            "datetime_audit_status": "warning" if (severity == "warning").any() else "passed",
            "datetime_issues_found": int(len(audit_csv)),
            "datetime_timezone_mismatch": int((issue_type == "timezone_mismatch").sum()),
            "datetime_naive_datetime": int((issue_type == "naive_datetime").sum()),
            "datetime_timestamp_mismatch": int((issue_type == "timestamp_mismatch").sum()),
            "datetime_recommended_action": "normalize_to_timestamp" if (issue_type == "timestamp_mismatch").any() else "monitor",
        }
    return {
        "available": False,
        "datetime_audit_status": "unavailable",
        "datetime_issues_found": 0,
        "datetime_timezone_mismatch": 0,
        "datetime_naive_datetime": 0,
        "datetime_timestamp_mismatch": 0,
        "datetime_recommended_action": "monitor",
    }


def prediction_calibration_summary(calibration_json, calibration_csv: pd.DataFrame) -> dict:
    """予測キャリブレーション層 (SPEC-BC-001) のDashboard表示用サマリー。分析専用。"""
    payload = calibration_json if isinstance(calibration_json, dict) and calibration_json else {}
    if not payload:
        return {"available": False, "calibration_status": "unavailable"}
    return {
        "available": True,
        "calibration_status": payload.get("calibration_status", "unavailable"),
        "implied_probability_source": payload.get("implied_probability_source", "frozen_default"),
        "ranks_tracked": int(numeric_or(payload.get("ranks_tracked", 0), 0)),
        "overconfident_count": int(numeric_or(payload.get("overconfident_count", 0), 0)),
        "underconfident_count": int(numeric_or(payload.get("underconfident_count", 0), 0)),
        "well_calibrated_count": int(numeric_or(payload.get("well_calibrated_count", 0), 0)),
        "insufficient_data_count": int(numeric_or(payload.get("insufficient_data_count", 0), 0)),
        "overall_brier": numeric_or(payload.get("overall_brier", 0.0), 0.0),
        "reference_brier": numeric_or(payload.get("reference_brier", 0.0), 0.0),
        "brier_skill_score": numeric_or(payload.get("brier_skill_score", 0.0), 0.0),
        "scored_n": int(numeric_or(payload.get("scored_n", 0), 0)),
        "requires_human_approval": bool(payload.get("requires_human_approval", True)),
        "weights_json_updated": bool(payload.get("weights_json_updated", False)),
    }


def narrative_reliability_summary(reliability_json, reliability_csv: pd.DataFrame) -> dict:
    """ナラティブ信頼性ゲート (SPEC-NQ-001) のDashboard表示用サマリー。分析専用。"""
    payload = reliability_json if isinstance(reliability_json, dict) and reliability_json else {}
    if not payload:
        return {"available": False, "narrative_reliability_status": "unavailable"}
    return {
        "available": True,
        "narrative_reliability_status": payload.get("narrative_reliability_status", "unavailable"),
        "narrative_source": payload.get("narrative_source", "unavailable"),
        "total_narratives": int(numeric_or(payload.get("total_narratives", 0), 0)),
        "strong_positive_count": int(numeric_or(payload.get("strong_positive_count", 0), 0)),
        "strong_negative_count": int(numeric_or(payload.get("strong_negative_count", 0), 0)),
        "unproven_count": int(numeric_or(payload.get("unproven_count", 0), 0)),
        "insufficient_data_count": int(numeric_or(payload.get("insufficient_data_count", 0), 0)),
        "decay_divergence_count": int(numeric_or(payload.get("decay_divergence_count", 0), 0)),
        "requires_human_approval": bool(payload.get("requires_human_approval", True)),
        "weights_json_updated": bool(payload.get("weights_json_updated", False)),
    }


def transaction_cost_summary(evaluations: pd.DataFrame, cost_model_json) -> dict:
    """取引コストモデル (SPEC-TC-001) の表示用サマリー。分析専用・実売買なし。

    evaluations の net R / cost R 列の有無と、config/cost_model.json の設定状態を要約する。
    """
    meta = (cost_model_json or {}).get("_meta", {}) if isinstance(cost_model_json, dict) else {}
    assets = (cost_model_json or {}).get("assets", {}) if isinstance(cost_model_json, dict) else {}
    default_source = ((cost_model_json or {}).get("default", {}) or {}).get("source", "unconfigured") if isinstance(cost_model_json, dict) else "unconfigured"
    configured_assets = 0
    for cfg in (assets.values() if isinstance(assets, dict) else []):
        if isinstance(cfg, dict) and str(cfg.get("source", "unconfigured")) not in ("", "unconfigured"):
            configured_assets += 1

    cols = set(evaluations.columns) if not evaluations.empty else set()
    net_available = "r_result_net" in cols
    gross_available = "r_result" in cols
    cost_col = "cost_r" in cols
    cost_adjusted_rows = 0
    all_costs_zero = True
    if not evaluations.empty and cost_col:
        cost_series = pd.to_numeric(evaluations["cost_r"], errors="coerce").fillna(0.0)
        cost_adjusted_rows = int((cost_series.abs() > 0).sum())
        all_costs_zero = bool((cost_series.abs() == 0).all())
    cost_source_unconfigured = True
    if not evaluations.empty and "cost_source" in cols:
        sources = evaluations["cost_source"].fillna("unconfigured").astype(str)
        cost_source_unconfigured = bool((sources.isin(["", "unconfigured"])).all())

    status = str(meta.get("status", "unconfigured")) if meta else "unconfigured"
    warning = ""
    if status == "unconfigured" or (all_costs_zero and cost_source_unconfigured):
        warning = "コスト未設定: 全コスト0のためネットR=グロスR。XMTrading実測値をsource付きで記入するまで分析は理論値です。"
    return {
        "available": True,
        "cost_model_status": status,
        "configured_asset_count": int(configured_assets),
        "default_source": str(default_source),
        "net_r_available": bool(net_available),
        "gross_r_available": bool(gross_available),
        "cost_adjusted_rows": int(cost_adjusted_rows),
        "all_costs_zero_or_unconfigured": bool(all_costs_zero and cost_source_unconfigured),
        "warning": warning,
    }


def audit_report_summary(audit_status_text: str) -> dict:
    """統合状態確認用 Audit Report (SPEC) のサマリー。statusのみ表示。"""
    status = str(audit_status_text or "").strip()
    available = bool(status)
    return {
        "available": available,
        "latest_audit_status": status or "unavailable",
        "latest_audit_report_date": latest_file_date("reports/audit/*_audit_report.md"),
        "audit_report_available": available,
    }


def narrative_lookahead_summary(audit_json, audit_csv: pd.DataFrame) -> dict:
    """Narrative Lookahead Audit の表示用サマリー (SPEC)。分析・警告専用。

    ニュース/AIフィードバックへの未来情報・評価結果混入を監査する。
    weights.json/generate_signal.py は一切変更しない。
    """
    payload = audit_json if isinstance(audit_json, dict) and audit_json else {}
    if not payload:
        return {"available": False, "audit_status": "unavailable"}
    return {
        "available": True,
        "audit_status": payload.get("audit_status", "unavailable"),
        "total_checked": int(numeric_or(payload.get("total_checked", 0), 0)),
        "passed_count": int(numeric_or(payload.get("passed_count", 0), 0)),
        "warning_count": int(numeric_or(payload.get("warning_count", 0), 0)),
        "high_risk_count": int(numeric_or(payload.get("high_risk_count", 0), 0)),
        "blocked_count": int(numeric_or(payload.get("blocked_count", 0), 0)),
        "unavailable_count": int(numeric_or(payload.get("unavailable_count", 0), 0)),
        "unknown_timing_count": int(numeric_or(payload.get("unknown_timing_count", 0), 0)),
        "max_lookahead_score": int(numeric_or(payload.get("max_lookahead_score", 0), 0)),
        "recommended_next_action": payload.get("recommended_next_action", "continue_monitoring"),
        "requires_human_approval": bool(payload.get("requires_human_approval", True)),
        "weights_json_updated": bool(payload.get("weights_json_updated", False)),
        "generate_signal_updated": bool(payload.get("generate_signal_updated", False)),
    }


def adversarial_review_summary(review_json, review_csv: pd.DataFrame) -> dict:
    """Adversarial Review Agent (Phase 23) の表示用サマリー。分析・警告専用。

    提案レイヤーを横断レビューし危険兆候を検出する。weights.json/generate_signal.py
    は一切変更しない。
    """
    payload = review_json if isinstance(review_json, dict) and review_json else {}
    if not payload:
        return {"available": False, "review_status": "unavailable"}
    return {
        "available": True,
        "review_status": payload.get("review_status", "unavailable"),
        "total_sources_checked": int(numeric_or(payload.get("total_sources_checked", 0), 0)),
        "total_findings": int(numeric_or(payload.get("total_findings", 0), 0)),
        "warning_count": int(numeric_or(payload.get("warning_count", 0), 0)),
        "high_risk_count": int(numeric_or(payload.get("high_risk_count", 0), 0)),
        "blocked_count": int(numeric_or(payload.get("blocked_count", 0), 0)),
        "contradiction_count": int(numeric_or(payload.get("contradiction_count", 0), 0)),
        "auto_apply_violation_count": int(numeric_or(payload.get("auto_apply_violation_count", 0), 0)),
        "weights_update_violation_count": int(numeric_or(payload.get("weights_update_violation_count", 0), 0)),
        "max_severity": payload.get("max_severity", "none"),
        "recommended_next_action": payload.get("recommended_next_action", "continue_monitoring"),
        "requires_human_approval": bool(payload.get("requires_human_approval", True)),
        "weights_json_updated": bool(payload.get("weights_json_updated", False)),
        "generate_signal_updated": bool(payload.get("generate_signal_updated", False)),
    }


def pending_reevaluation_summary(pending: pd.DataFrame) -> dict:
    if pending.empty:
        return {
            "available": False,
            "pending_reevaluation_count": 0,
            "pending_reevaluation_closed_count": 0,
            "pending_reevaluation_open_count": 0,
            "pending_reevaluation_no_entry_count": 0,
            "pending_reevaluation_missed_count": 0,
            "recent_closed": [],
        }
    out = pending.copy()
    status = out.get("evaluation_status", out.get("status", pd.Series("", index=out.index))).fillna("").astype(str).str.lower()
    outcome = out.get("outcome", pd.Series("", index=out.index)).fillna("").astype(str).str.lower()
    missed = out.get("missed_opportunity", pd.Series("", index=out.index)).fillna("").astype(str).str.lower().isin(["true", "1", "yes"])
    closed_mask = (status == "closed") | outcome.isin(["win_tp1", "win_tp2", "loss_sl"])
    recent_closed = out[closed_mask].tail(5)
    return {
        "available": True,
        "pending_reevaluation_count": int(len(out)),
        "pending_reevaluation_closed_count": int(closed_mask.sum()),
        "pending_reevaluation_open_count": int((outcome == "open_unresolved").sum()),
        "pending_reevaluation_no_entry_count": int((outcome == "no_entry").sum()),
        "pending_reevaluation_missed_count": int(missed.sum()),
        "recent_closed": recent_closed.to_dict(orient="records"),
    }


def choose_evaluations_for_dashboard(data_evaluations: pd.DataFrame, extras: dict[str, object]) -> tuple[pd.DataFrame, str]:
    latest = extras.get("latest_evaluations", pd.DataFrame())
    pending = extras.get("pending_reevaluations", pd.DataFrame())
    if isinstance(latest, pd.DataFrame) and not latest.empty:
        return latest, "latest_evaluations"
    if isinstance(pending, pd.DataFrame) and not pending.empty:
        return pending, "pending_reevaluations"
    return data_evaluations, "evaluations"


def latest_evaluation_view_summary(latest: pd.DataFrame, summary_json) -> dict:
    if isinstance(summary_json, dict) and summary_json:
        return {
            "available": True,
            "latest_evaluation_unique_signal_count": int(numeric_or(summary_json.get("unique_signal_count", 0), 0)),
            "latest_evaluation_rows": int(numeric_or(summary_json.get("latest_rows", 0), 0)),
            "latest_from_pending_reevaluations": int(numeric_or(summary_json.get("latest_from_pending_reevaluations", 0), 0)),
            "latest_from_evaluations": int(numeric_or(summary_json.get("latest_from_evaluations", 0), 0)),
            "latest_evaluation_closed_count": int(numeric_or(summary_json.get("closed_count", 0), 0)),
            "latest_evaluation_pending_count": int(numeric_or(summary_json.get("pending_count", 0), 0)),
            "latest_evaluation_open_count": int(numeric_or(summary_json.get("open_count", 0), 0)),
            "latest_evaluation_no_entry_count": int(numeric_or(summary_json.get("no_entry_count", 0), 0)),
            "latest_evaluation_missed_count": int(numeric_or(summary_json.get("missed_opportunity_count", 0), 0)),
        }
    if latest.empty:
        return {
            "available": False,
            "latest_evaluation_unique_signal_count": 0,
            "latest_evaluation_rows": 0,
            "latest_from_pending_reevaluations": 0,
            "latest_from_evaluations": 0,
            "latest_evaluation_closed_count": 0,
            "latest_evaluation_pending_count": 0,
            "latest_evaluation_open_count": 0,
            "latest_evaluation_no_entry_count": 0,
            "latest_evaluation_missed_count": 0,
        }
    status = latest.get("evaluation_status", latest.get("status", pd.Series("", index=latest.index))).fillna("").astype(str).str.lower()
    outcome = latest.get("outcome", pd.Series("", index=latest.index)).fillna("").astype(str).str.lower()
    latest_source = latest.get("latest_source", pd.Series("", index=latest.index)).fillna("").astype(str)
    missed = latest.get("missed_opportunity", pd.Series("", index=latest.index)).fillna("").astype(str).str.lower().isin(["true", "1", "yes"])
    return {
        "available": True,
        "latest_evaluation_unique_signal_count": int(latest["signal_id"].nunique()) if "signal_id" in latest.columns else len(latest),
        "latest_evaluation_rows": int(len(latest)),
        "latest_from_pending_reevaluations": int((latest_source == "pending_reevaluations").sum()),
        "latest_from_evaluations": int((latest_source == "evaluations").sum()),
        "latest_evaluation_closed_count": int((status == "closed").sum()),
        "latest_evaluation_pending_count": int((status == "pending").sum()),
        "latest_evaluation_open_count": int(((status == "open") | (outcome == "open_unresolved")).sum()),
        "latest_evaluation_no_entry_count": int((outcome == "no_entry").sum()),
        "latest_evaluation_missed_count": int(missed.sum()),
    }


def top_reason_codes(reason_table: pd.DataFrame) -> dict:
    if reason_table.empty:
        return {"positive": [], "negative": [], "insufficient": []}
    positive = reason_table[reason_table["reliability_label"].isin(["strong_positive", "positive"])].head(5) if "reliability_label" in reason_table.columns else pd.DataFrame()
    negative = (
        reason_table[reason_table["reliability_label"].isin(["strong_negative", "negative"])].sort_values("average_r").head(5)
        if {"reliability_label", "average_r"}.issubset(reason_table.columns)
        else pd.DataFrame()
    )
    insufficient = reason_table[reason_table["reliability_label"].astype(str) == "insufficient_data"].head(5) if "reliability_label" in reason_table.columns else pd.DataFrame()
    return {
        "positive": positive.to_dict(orient="records"),
        "negative": negative.to_dict(orient="records"),
        "insufficient": insufficient.to_dict(orient="records"),
    }
