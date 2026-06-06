from __future__ import annotations

import html
import json
import os
from datetime import datetime
from pathlib import Path

import pandas as pd

import analyze_reason_codes as arc


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/dashboard")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_MAPPINGS = {
    "market_snapshot": ("MARKET_SNAPSHOT", RESULTS_DIR / "market_snapshot.csv"),
    "signals": ("SIGNALS", RESULTS_DIR / "signals.csv"),
    "evaluations": ("EVALUATIONS", RESULTS_DIR / "evaluations.csv"),
}
SAFETY_NOTES = [
    "This system does not place trades.",
    "This system does not operate XM or brokers.",
    "Rule updates are proposals only.",
    "weights.json is not automatically updated.",
    "Human review is required before any live trading use.",
]


def normalize_column_name(column: str) -> str:
    normalized = str(column).strip().lower().replace("-", "_")
    normalized = "_".join(normalized.split())
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    return normalized


def normalize_headers(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
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


def read_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def get_sheets_client():
    service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not service_account_json or not sheet_id:
        return None

    import gspread
    from google.oauth2.service_account import Credentials

    account_info = json.loads(service_account_json)
    credentials = Credentials.from_service_account_info(account_info, scopes=SCOPES)
    return gspread.authorize(credentials)


def worksheet_to_dataframe(worksheet) -> pd.DataFrame:
    values = worksheet.get_all_values()
    if not values:
        return pd.DataFrame()
    header = [normalize_column_name(col) for col in values[0]]
    rows = []
    for row in values[1:]:
        padded = list(row) + [""] * max(0, len(header) - len(row))
        trimmed = padded[: len(header)]
        if any(str(cell).strip() for cell in trimmed):
            rows.append(trimmed)
    return pd.DataFrame(rows, columns=header)


def load_sheet_data() -> tuple[dict[str, pd.DataFrame] | None, str]:
    try:
        client = get_sheets_client()
        if client is None:
            return None, "local fallback"
        spreadsheet = client.open_by_key(os.environ["GOOGLE_SHEET_ID"])
        data: dict[str, pd.DataFrame] = {}
        for key, (sheet_name, _) in SHEET_MAPPINGS.items():
            try:
                data[key] = worksheet_to_dataframe(spreadsheet.worksheet(sheet_name))
                print(f"ok: loaded {len(data[key])} rows from Google Sheets {sheet_name}")
            except Exception as exc:  # noqa: BLE001 - missing worksheets should not break dashboard.
                print(f"warning: Google Sheets worksheet {sheet_name} unavailable: {exc}")
                data[key] = pd.DataFrame()
        return data, "Google Sheets"
    except Exception as exc:  # noqa: BLE001 - fallback is intentional for artifact generation.
        print(f"warning: Google Sheets read failed; using local fallback: {exc}")
        return None, "local fallback"


def load_data() -> tuple[dict[str, pd.DataFrame], dict[str, object], str]:
    sheet_data, source = load_sheet_data()
    data = sheet_data if sheet_data is not None else {
        key: read_csv(path) for key, (_, path) in SHEET_MAPPINGS.items()
    }
    extras = {
        "weekly_review": read_csv(RESULTS_DIR / "weekly_review.csv"),
        "monthly_calibration": read_csv(RESULTS_DIR / "monthly_calibration.csv"),
        "reason_code_analysis": read_csv(RESULTS_DIR / "reason_code_analysis.csv"),
        "rule_update_proposals": read_csv(RESULTS_DIR / "rule_update_proposals.csv"),
        "weekly_review_json": read_json(RESULTS_DIR / "weekly_review.json"),
        "monthly_calibration_json": read_json(RESULTS_DIR / "monthly_calibration.json"),
        "reason_code_analysis_json": read_json(RESULTS_DIR / "reason_code_analysis.json"),
        "rule_update_proposals_json": read_json(RESULTS_DIR / "rule_update_proposals.json"),
    }
    return data, extras, source


def latest_date(df: pd.DataFrame, columns: list[str]) -> str:
    dates = []
    for col in columns:
        if not df.empty and col in df.columns:
            parsed = pd.to_datetime(df[col], errors="coerce", utc=True).dt.tz_localize(None)
            dates.extend(parsed.dropna().tolist())
    if not dates:
        return ""
    return max(dates).strftime("%Y-%m-%d")


def latest_file_date(pattern: str) -> str:
    files = sorted(Path().glob(pattern))
    if not files:
        return ""
    latest = max(files, key=lambda p: p.stat().st_mtime)
    stem = latest.stem
    text = stem[:10]
    return text if len(text) == 10 else latest.name


def fmt_num(value) -> str:
    value = pd.to_numeric(value, errors="coerce")
    if pd.isna(value):
        return ""
    return f"{float(value):.2f}"


def badge(value: str) -> str:
    clean = str(value or "")
    cls = normalize_column_name(clean) or "default"
    return f'<span class="badge badge-{html.escape(cls)}">{html.escape(clean)}</span>'


def value_class(value) -> str:
    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number):
        return ""
    if number > 0:
        return "positive"
    if number < 0:
        return "negative"
    return "neutral"


def is_numeric_cell(value) -> bool:
    if isinstance(value, bool) or value == "":
        return False
    number = pd.to_numeric(value, errors="coerce")
    return not pd.isna(number)


def table_html(df: pd.DataFrame, columns: list[str], empty: str = "データなし", limit: int | None = None) -> str:
    if df.empty:
        return f'<div class="empty">{html.escape(empty)}</div>'
    view = df.copy()
    if columns:
        for col in columns:
            if col not in view.columns:
                view[col] = ""
        view = view[columns]
    if limit:
        view = view.head(limit)
    if view.empty:
        return f'<div class="empty">{html.escape(empty)}</div>'

    out = ['<div class="table-wrap"><table><thead><tr>']
    out.extend(f"<th>{html.escape(col)}</th>" for col in view.columns)
    out.append("</tr></thead><tbody>")
    for _, row in view.iterrows():
        out.append("<tr>")
        for col in view.columns:
            raw = row.get(col, "")
            if col in {"rank", "side", "recommended_action", "proposal_strength", "reliability_label", "assessment"}:
                cell = badge(raw)
            elif col in {"average_r", "total_r", "r_multiple", "win_rate", "best_r", "worst_r", "average_mfe_r"}:
                cell = f'<span class="{value_class(raw)}">{fmt_num(raw)}</span>'
            elif is_numeric_cell(raw):
                cell = fmt_num(raw)
            else:
                cell = html.escape("" if pd.isna(raw) else str(raw))
            out.append(f"<td>{cell}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def stat_card(label: str, value, css_class: str = "") -> str:
    return f'<div class="stat {css_class}"><div class="stat-label">{html.escape(label)}</div><div class="stat-value">{html.escape(str(value))}</div></div>'


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


def json_safe(value):
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
        except (ValueError, TypeError):
            pass
    return value


def build_dashboard() -> tuple[dict, str]:
    data, extras, source = load_data()
    snapshot = data["market_snapshot"]
    signals = data["signals"]
    evaluations = data["evaluations"]
    weekly = extras["weekly_review"]
    monthly = extras["monthly_calibration"]
    reason_table, no_trade_table = reason_code_data(signals, evaluations, extras["reason_code_analysis"], extras["reason_code_analysis_json"])
    rule_updates = extras["rule_update_proposals"]
    latest_sig = latest_signals(signals)
    sig_summary = signal_summary(latest_sig)
    eval_summary = evaluation_summary(evaluations)
    asset_table = asset_performance(signals, evaluations)
    mode = weekly_monthly_mode(weekly, monthly)
    reason_tops = top_reason_codes(reason_table)
    generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row_counts = {
        "market_snapshot": len(snapshot),
        "signals": len(signals),
        "evaluations": len(evaluations),
        "weekly_review": len(weekly),
        "monthly_calibration": len(monthly),
        "reason_code_analysis": len(reason_table),
        "rule_update_proposals": len(rule_updates),
    }
    latest_dates = {
        "latest_signal_date": latest_date(signals, ["signal_date", "date"]),
        "latest_evaluation_date": latest_date(evaluations, ["evaluation_date", "hit_date", "signal_date"]),
        "latest_daily_report_date": latest_file_date("reports/*.md"),
        "latest_weekly_review_date": latest_file_date("reports/weekly/*_weekly_review.md"),
        "latest_monthly_calibration_date": latest_file_date("reports/monthly/*_monthly_calibration.md"),
        "latest_reason_code_analysis_date": latest_file_date("reports/reason_codes/*_reason_code_analysis.md"),
        "latest_rule_update_proposals_date": latest_file_date("reports/rule_updates/*_rule_update_proposals.md"),
    }
    apply_false = True
    if not rule_updates.empty and "apply_automatically" in rule_updates.columns:
        apply_false = rule_updates["apply_automatically"].fillna(False).astype(str).str.lower().isin(["false", "0", "no"]).all()
    rule_update_summary = {
        "count": int(len(rule_updates)),
        "high_priority": int((rule_updates.get("proposal_strength", pd.Series(dtype=str)).astype(str) == "HIGH").sum()) if not rule_updates.empty else 0,
        "apply_automatically_all_false": bool(apply_false),
    }
    summary = json_safe({
        "generated_at": generated,
        "data_source": source,
        "row_counts": row_counts,
        "latest_dates": latest_dates,
        "daily_signal_summary": sig_summary,
        "evaluation_summary": eval_summary,
        "asset_performance": asset_table.to_dict(orient="records"),
        "top_reason_codes": reason_tops,
        "rule_update_summary": rule_update_summary,
        "safety_notes": SAFETY_NOTES,
    })

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "dashboard_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    html_text = render_html(
        generated=generated,
        source=source,
        latest_dates=latest_dates,
        row_counts=row_counts,
        signals=latest_sig,
        signal_counts=sig_summary,
        eval_summary=eval_summary,
        asset_table=asset_table,
        reason_table=reason_table,
        no_trade_table=no_trade_table,
        rule_updates=rule_updates,
        mode=mode,
        apply_false=apply_false,
        summary=summary,
    )
    html_path = REPORTS_DIR / "index.html"
    html_path.write_text(html_text, encoding="utf-8")
    print(f"dashboard generated: {html_path}")
    print(f"dashboard summary generated: {REPORTS_DIR / 'dashboard_summary.json'}")
    return summary, str(html_path)


def render_html(
    *,
    generated: str,
    source: str,
    latest_dates: dict,
    row_counts: dict,
    signals: pd.DataFrame,
    signal_counts: dict,
    eval_summary: dict,
    asset_table: pd.DataFrame,
    reason_table: pd.DataFrame,
    no_trade_table: pd.DataFrame,
    rule_updates: pd.DataFrame,
    mode: dict,
    apply_false: bool,
    summary: dict,
) -> str:
    top_positive = reason_table[reason_table["reliability_label"].isin(["strong_positive", "positive"])].head(10) if not reason_table.empty and "reliability_label" in reason_table.columns else pd.DataFrame()
    top_negative = (
        reason_table[reason_table["reliability_label"].isin(["strong_negative", "negative"])].sort_values("average_r").head(10)
        if not reason_table.empty and {"reliability_label", "average_r"}.issubset(reason_table.columns)
        else pd.DataFrame()
    )
    insufficient = reason_table[reason_table["reliability_label"].astype(str) == "insufficient_data"].head(10) if not reason_table.empty and "reliability_label" in reason_table.columns else pd.DataFrame()
    rule_view = rule_updates.sort_values("priority").head(10) if not rule_updates.empty and "priority" in rule_updates.columns else rule_updates.head(10)
    system_stats = "".join(
        [
            stat_card("market_snapshot rows", row_counts["market_snapshot"]),
            stat_card("signals rows", row_counts["signals"]),
            stat_card("evaluations rows", row_counts["evaluations"]),
            stat_card("latest daily report", latest_dates["latest_daily_report_date"] or "not available"),
            stat_card("latest weekly review", latest_dates["latest_weekly_review_date"] or "not available"),
            stat_card("latest monthly calibration", latest_dates["latest_monthly_calibration_date"] or "not available"),
            stat_card("latest reason_code_analysis", latest_dates["latest_reason_code_analysis_date"] or "not available"),
            stat_card("latest rule_update_proposals", latest_dates["latest_rule_update_proposals_date"] or "not available"),
        ]
    )
    eval_stats = "".join(stat_card(k.replace("_", " "), fmt_num(v) if isinstance(v, float) else v, value_class(v)) for k, v in eval_summary.items())
    signal_stats = "".join(stat_card(k, v) for k, v in signal_counts.items())
    mode_stats = "".join(stat_card(k.replace("_", " "), fmt_num(v) if isinstance(v, float) else v) for k, v in mode.items())
    safe = "".join(f"<li>{html.escape(note)}</li>" for note in SAFETY_NOTES)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tactical Swing OS Dashboard</title>
  <style>
    :root {{ color-scheme: dark; --bg:#0b1020; --panel:#121a2e; --panel2:#17213a; --text:#edf2ff; --muted:#98a6c7; --line:#263553; --pos:#65d98c; --neg:#ff7b86; --warn:#ffd166; --accent:#7aa2ff; }}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background:var(--bg); color:var(--text); }}
    header {{ padding:28px; background:linear-gradient(135deg, #111b35, #0c1224); border-bottom:1px solid var(--line); }}
    h1 {{ margin:0 0 10px; font-size:28px; }}
    h2 {{ margin:0 0 14px; font-size:18px; }}
    h3 {{ margin:18px 0 10px; font-size:14px; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; }}
    main {{ padding:20px; display:grid; gap:18px; }}
    .meta {{ display:flex; flex-wrap:wrap; gap:10px; color:var(--muted); font-size:13px; }}
    .card {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:16px; box-shadow:0 8px 24px rgba(0,0,0,.18); }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(160px,1fr)); gap:10px; }}
    .stat {{ background:var(--panel2); border:1px solid var(--line); border-radius:8px; padding:12px; }}
    .stat-label {{ color:var(--muted); font-size:12px; }}
    .stat-value {{ margin-top:6px; font-size:20px; font-weight:700; }}
    .table-wrap {{ overflow-x:auto; border:1px solid var(--line); border-radius:8px; }}
    table {{ width:100%; border-collapse:collapse; min-width:720px; }}
    th, td {{ padding:9px 10px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; font-size:13px; }}
    th {{ color:var(--muted); background:#10182b; position:sticky; top:0; }}
    tr:hover td {{ background:rgba(122,162,255,.05); }}
    .badge {{ display:inline-flex; align-items:center; border-radius:999px; padding:2px 8px; font-size:12px; font-weight:700; background:#273554; color:#dbe6ff; }}
    .badge-a, .badge-trade, .badge-strong_positive, .badge-positive {{ background:rgba(101,217,140,.16); color:var(--pos); }}
    .badge-b, .badge-watch, .badge-medium {{ background:rgba(255,209,102,.16); color:var(--warn); }}
    .badge-no_trade, .badge-none, .badge-data_insufficient, .badge-insufficient_data {{ background:rgba(152,166,199,.16); color:var(--muted); }}
    .badge-strong_negative, .badge-negative, .badge-high {{ background:rgba(255,123,134,.16); color:var(--neg); }}
    .positive {{ color:var(--pos); font-weight:700; }}
    .negative {{ color:var(--neg); font-weight:700; }}
    .neutral {{ color:var(--muted); }}
    .empty {{ color:var(--muted); padding:14px; border:1px dashed var(--line); border-radius:8px; }}
    .notice {{ color:var(--muted); margin:8px 0 12px; }}
    ul {{ margin:8px 0 0; padding-left:20px; color:var(--muted); }}
  </style>
</head>
<body>
  <header>
    <h1>Tactical Swing OS Dashboard</h1>
    <div class="meta">
      <span>generated_at: {html.escape(generated)}</span>
      <span>data_source: {html.escape(source)}</span>
      <span>latest_signal_date: {html.escape(latest_dates["latest_signal_date"] or "not available")}</span>
      <span>latest_evaluation_date: {html.escape(latest_dates["latest_evaluation_date"] or "not available")}</span>
    </div>
  </header>
  <main>
    <section class="card"><h2>System Status</h2><div class="grid">{system_stats}</div></section>
    <section class="card"><h2>Daily Signal Overview</h2><div class="grid">{signal_stats}</div>{table_html(signals, ["asset","side","rank","type","recommended_action","signal_strength","setup_quality_score","entry_quality_score","direction_confidence","reason_codes","no_trade_reason"])}</section>
    <section class="card"><h2>Evaluation Overview</h2><div class="grid">{eval_stats}</div></section>
    <section class="card"><h2>Asset Performance</h2>{table_html(asset_table, ["asset","signals","evaluations","win_rate","total_r","average_r","missed_opportunity_count"])}</section>
    <section class="card"><h2>Reason Code Performance</h2><h3>Top Positive</h3>{table_html(top_positive, ["reason_code","signals_count","evaluated_count","win_rate","average_r","total_r","reliability_label"])}<h3>Top Negative</h3>{table_html(top_negative, ["reason_code","signals_count","evaluated_count","win_rate","average_r","total_r","reliability_label"])}<h3>Insufficient Data</h3>{table_html(insufficient, ["reason_code","signals_count","evaluated_count","win_rate","average_r","total_r","reliability_label"])}</section>
    <section class="card"><h2>No Trade Reason Analysis</h2>{table_html(no_trade_table, ["no_trade_reason","count","missed_opportunity_count","average_mfe_r","assessment"], "no_trade_reason data not available")}</section>
    <section class="card"><h2>Rule Update Proposals</h2><p class="notice">apply_automatically is false for all proposals: <strong>{str(apply_false).lower()}</strong></p>{table_html(rule_view, ["proposal_type","target_type","target_name","proposal_strength","priority","average_r","win_rate","proposed_change","apply_automatically"])}</section>
    <section class="card"><h2>Weekly / Monthly Mode</h2><div class="grid">{mode_stats}</div></section>
    <section class="card"><h2>Safety Notes</h2><ul>{safe}</ul></section>
  </main>
  <script type="application/json" id="dashboard-summary">{html.escape(json.dumps(summary, ensure_ascii=False))}</script>
</body>
</html>
"""


def main() -> int:
    build_dashboard()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
