from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd

from time_utils import JST, format_jst, format_utc, now_utc


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/evaluations")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_MAPPINGS = {
    "evaluations": ("EVALUATIONS", RESULTS_DIR / "evaluations.csv"),
    "pending_reevaluations": ("PENDING_REEVALUATIONS", RESULTS_DIR / "pending_reevaluations.csv"),
}
FINAL_OUTCOMES = {"win_tp1", "win_tp2", "loss_sl", "no_trade_correct", "no_trade_missed"}


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


def load_from_sheets() -> tuple[dict[str, pd.DataFrame] | None, str]:
    try:
        client = get_sheets_client()
        if client is None:
            return None, "local_csv"
        spreadsheet = client.open_by_key(os.environ["GOOGLE_SHEET_ID"])
        frames: dict[str, pd.DataFrame] = {}
        for key, (sheet_name, _) in SHEET_MAPPINGS.items():
            try:
                frames[key] = worksheet_to_dataframe(spreadsheet.worksheet(sheet_name))
                print(f"ok: loaded {len(frames[key])} rows from Google Sheets {sheet_name}")
            except Exception as exc:  # noqa: BLE001 - missing sheets should not break fallback behavior.
                print(f"warning: Google Sheets worksheet {sheet_name} unavailable: {exc}")
                frames[key] = pd.DataFrame()
        return frames, "sheets"
    except Exception as exc:  # noqa: BLE001 - local fallback is intentional.
        print(f"warning: Google Sheets read failed; falling back to local CSV: {exc}")
        return None, "local_csv"


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, str]:
    sheet_data, source = load_from_sheets()
    if sheet_data is not None:
        return sheet_data["evaluations"], sheet_data["pending_reevaluations"], source
    return read_csv(SHEET_MAPPINGS["evaluations"][1]), read_csv(SHEET_MAPPINGS["pending_reevaluations"][1]), "local_csv"


def clean_text(value) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()


def truthy_series(df: pd.DataFrame, column: str) -> pd.Series:
    if column not in df.columns:
        return pd.Series(False, index=df.index)
    return df[column].fillna("").astype(str).str.lower().isin(["true", "1", "yes"])


def parse_timestamp(value) -> pd.Timestamp:
    text = clean_text(value)
    if not text:
        return pd.NaT
    if text.upper().endswith("JST"):
        raw = text[:-3].strip()
        parsed = pd.to_datetime(raw, errors="coerce")
        if pd.isna(parsed):
            return pd.NaT
        return pd.Timestamp(parsed).tz_localize(JST).tz_convert(None)
    parsed = pd.to_datetime(text, errors="coerce", utc=True)
    if pd.isna(parsed):
        return pd.NaT
    return pd.Timestamp(parsed).tz_convert(None)


def best_sort_key(row: pd.Series) -> tuple[pd.Timestamp, str]:
    for col, reason in [
        ("reevaluation_at_jst", "latest_by_reevaluation_at"),
        ("reevaluation_at_utc", "latest_by_reevaluation_at"),
        ("evaluation_date", "latest_by_evaluation_date"),
        ("date", "latest_by_evaluation_date"),
    ]:
        if col in row.index:
            parsed = parse_timestamp(row.get(col))
            if not pd.isna(parsed):
                return parsed, reason
    return pd.NaT, "latest_by_row_order"


def prepare_source(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    out = normalize_headers(df)
    if out.empty:
        out = pd.DataFrame()
    out = out.copy()
    out["source"] = source_name
    out["latest_source"] = source_name
    out["_source_priority"] = 1 if source_name == "pending_reevaluations" else 0
    out["_row_order"] = range(len(out))
    if "signal_id" not in out.columns:
        out["signal_id"] = ""
    out["signal_id"] = out["signal_id"].map(clean_text)
    out = out[out["signal_id"] != ""].copy()
    if out.empty:
        return out
    sort_values = out.apply(best_sort_key, axis=1)
    out["_sort_at"] = [item[0] for item in sort_values]
    out["latest_reason"] = [item[1] for item in sort_values]
    return out


def build_latest_view(evaluations: pd.DataFrame, pending_reevaluations: pd.DataFrame, generated_at_utc=None) -> pd.DataFrame:
    generated_at_utc = generated_at_utc or now_utc()
    ev = prepare_source(evaluations, "evaluations")
    pending = prepare_source(pending_reevaluations, "pending_reevaluations")
    combined = pd.concat([ev, pending], ignore_index=True, sort=False)
    if combined.empty:
        return pd.DataFrame()

    history_counts = combined.groupby("signal_id").size().rename("previous_rows_count")
    pending_history = combined[combined["latest_source"] == "pending_reevaluations"].groupby("signal_id").size().rename("_pending_history_count")
    combined = combined.merge(history_counts, on="signal_id", how="left")
    combined = combined.merge(pending_history, on="signal_id", how="left")
    combined["_pending_history_count"] = combined["_pending_history_count"].fillna(0)
    combined["has_reevaluation_history"] = combined["_pending_history_count"] > 0

    combined = combined.sort_values(["_sort_at", "_source_priority", "_row_order"], na_position="first")
    latest = combined.drop_duplicates("signal_id", keep="last").copy()
    latest["is_latest_evaluation"] = True
    latest["latest_selected_at_jst"] = format_jst(generated_at_utc)
    latest["latest_selected_at_utc"] = format_utc(generated_at_utc)
    latest["source_priority"] = latest["_source_priority"].astype(int)
    latest = latest.drop(columns=["_source_priority", "_row_order", "_sort_at", "_pending_history_count"], errors="ignore")

    preferred = [
        "signal_id",
        "asset",
        "side",
        "rank",
        "type",
        "signal_date",
        "evaluation_date",
        "status",
        "evaluation_status",
        "outcome",
        "error_type",
        "r_multiple",
        "r_result",
        "missed_opportunity",
        "latest_selected_at_jst",
        "latest_selected_at_utc",
        "latest_source",
        "source",
        "source_priority",
        "previous_rows_count",
        "has_reevaluation_history",
        "latest_reason",
        "is_latest_evaluation",
    ]
    columns = [col for col in preferred if col in latest.columns] + [col for col in latest.columns if col not in preferred]
    return latest[columns].reset_index(drop=True)


def outcome_series(df: pd.DataFrame) -> pd.Series:
    if df.empty or "outcome" not in df.columns:
        return pd.Series(dtype=str)
    return df["outcome"].fillna("").astype(str).str.lower()


def status_series(df: pd.DataFrame) -> pd.Series:
    if df.empty:
        return pd.Series(dtype=str)
    return df.get("evaluation_status", df.get("status", pd.Series("", index=df.index))).fillna("").astype(str).str.lower()


def summary_payload(
    latest: pd.DataFrame,
    evaluations: pd.DataFrame,
    pending_reevaluations: pd.DataFrame,
    *,
    generated_at_utc,
    source: str,
) -> dict:
    outcome = outcome_series(latest)
    status = status_series(latest)
    latest_source = latest.get("latest_source", pd.Series(dtype=str)).fillna("").astype(str) if not latest.empty else pd.Series(dtype=str)
    return {
        "generated_at_jst": format_jst(generated_at_utc),
        "generated_at_utc": format_utc(generated_at_utc),
        "source": source,
        "total_input_rows": int(len(evaluations) + len(pending_reevaluations)),
        "evaluations_rows": int(len(evaluations)),
        "pending_reevaluation_rows": int(len(pending_reevaluations)),
        "unique_signal_count": int(latest["signal_id"].nunique()) if not latest.empty and "signal_id" in latest.columns else 0,
        "latest_rows": int(len(latest)),
        "latest_from_evaluations": int((latest_source == "evaluations").sum()),
        "latest_from_pending_reevaluations": int((latest_source == "pending_reevaluations").sum()),
        "closed_count": int((status == "closed").sum()),
        "pending_count": int((status == "pending").sum()),
        "open_count": int(((status == "open") | (outcome == "open_unresolved")).sum()),
        "no_entry_count": int((outcome == "no_entry").sum()),
        "missed_opportunity_count": int(truthy_series(latest, "missed_opportunity").sum()) if not latest.empty else 0,
        "win_tp1_count": int((outcome == "win_tp1").sum()),
        "win_tp2_count": int((outcome == "win_tp2").sum()),
        "loss_sl_count": int((outcome == "loss_sl").sum()),
        "no_trade_correct_count": int((outcome == "no_trade_correct").sum()),
        "no_trade_missed_count": int((outcome == "no_trade_missed").sum()),
    }


def safe_records(df: pd.DataFrame) -> list[dict]:
    if df.empty:
        return []
    return df.where(pd.notna(df), None).to_dict(orient="records")


def markdown_table(df: pd.DataFrame, columns: list[str], empty: str) -> str:
    if df.empty:
        return empty
    view = df.copy()
    for col in columns:
        if col not in view.columns:
            view[col] = ""
    view = view[columns].head(25)
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    rows = []
    for _, row in view.iterrows():
        cells = [clean_text(row.get(col, "")).replace("|", "\\|") for col in columns]
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *rows])


def build_report(latest: pd.DataFrame, summary: dict) -> str:
    outcome = outcome_series(latest)
    status = status_series(latest)
    closed = latest[outcome.isin(FINAL_OUTCOMES)] if not latest.empty else pd.DataFrame()
    unresolved = latest[(status.isin(["pending", "open"])) | outcome.isin(["no_entry", "open_unresolved"])] if not latest.empty else pd.DataFrame()
    history = latest[truthy_series(latest, "has_reevaluation_history")] if not latest.empty else pd.DataFrame()
    lines = [
        "# Latest Evaluations Report",
        "",
        "## 1. 概要",
        "",
        f"* 生成日時JST: {summary['generated_at_jst']}",
        f"* 入力行数: {summary['total_input_rows']}",
        f"* unique signal数: {summary['unique_signal_count']}",
        f"* 最新評価行数: {summary['latest_rows']}",
        f"* PENDING_REEVALUATIONS由来の最新評価数: {summary['latest_from_pending_reevaluations']}",
        f"* EVALUATIONS由来の最新評価数: {summary['latest_from_evaluations']}",
        "",
        "## 2. 決着済み",
        "",
        markdown_table(closed, ["signal_id", "asset", "side", "rank", "outcome", "r_multiple", "latest_source", "latest_reason"], "決着済みの最新評価はありません。"),
        "",
        "## 3. 未決着",
        "",
        markdown_table(unresolved, ["signal_id", "asset", "side", "rank", "status", "evaluation_status", "outcome", "latest_source", "latest_reason"], "未決着の最新評価はありません。"),
        "",
        "## 4. 再評価履歴あり",
        "",
        markdown_table(history, ["signal_id", "asset", "side", "rank", "outcome", "previous_rows_count", "latest_source", "latest_reason"], "再評価履歴ありのシグナルはありません。"),
        "",
        "## 5. 注意",
        "",
        "* append-only履歴から最新行だけを選ぶ分析用ビューです。",
        "* 元のEVALUATIONS / PENDING_REEVALUATIONSは削除しません。",
        "* この評価は実売買ではありません。",
        "* 自動発注は行いません。",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    generated_at_utc = now_utc()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    evaluations, pending_reevaluations, source = load_inputs()
    latest = build_latest_view(evaluations, pending_reevaluations, generated_at_utc=generated_at_utc)
    summary = summary_payload(latest, evaluations, pending_reevaluations, generated_at_utc=generated_at_utc, source=source)

    latest.to_csv(RESULTS_DIR / "latest_evaluations.csv", index=False)
    (RESULTS_DIR / "latest_evaluations.json").write_text(json.dumps(safe_records(latest), ensure_ascii=False, indent=2), encoding="utf-8")
    (RESULTS_DIR / "latest_evaluations_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    report_path = REPORTS_DIR / f"{generated_at_utc.astimezone(JST).strftime('%Y-%m-%d')}_latest_evaluations.md"
    report_path.write_text(build_report(latest, summary), encoding="utf-8")

    print(f"latest evaluations generated: {len(latest)}")
    print(f"latest evaluations report generated: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
