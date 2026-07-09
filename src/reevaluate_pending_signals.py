from __future__ import annotations

import argparse
import json
import os
import re
import uuid
from pathlib import Path

import pandas as pd

from evaluate_signal import EVALUATION_COLUMNS, evaluate_signals_dataframe, normalize_column_name
from time_utils import JST, format_jst, format_utc, now_utc


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/reevaluation")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_NAMES = {"signals": "SIGNALS", "evaluations": "EVALUATIONS"}
LOCAL_PATHS = {"signals": RESULTS_DIR / "signals.csv", "evaluations": RESULTS_DIR / "evaluations.csv"}
FINAL_OUTCOMES = {"win_tp1", "win_tp2", "loss_sl", "no_trade_correct", "no_trade_missed", "invalid"}
OPEN_OUTCOMES = {"", "open_unresolved", "no_entry", "nan", "none", "null"}
OPEN_STATUSES = {"", "pending", "open", "unresolved", "no_entry", "nan", "none", "null"}
EXTRA_COLUMNS = [
    "reevaluation_at_jst",
    "reevaluation_at_utc",
    "reevaluation_run_id",
    "previous_status",
    "previous_evaluation_status",
    "previous_outcome",
    "previous_r_multiple",
    "changed_status",
    "changed_outcome",
    "changed_r_multiple",
    "is_latest_evaluation",
    "source",
]
OUTPUT_COLUMNS = EVALUATION_COLUMNS + EXTRA_COLUMNS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reevaluate unresolved Tactical Swing OS signals.")
    parser.add_argument("--lookback-days", type=int, default=30, help="Signal lookback window in days")
    parser.add_argument("--horizon", type=int, default=10, help="Future bars to evaluate")
    # 2026-07-09 人間指示(設計書§6 全判断採点の原則): NO_TRADE の見送り判断も採点対象が既定。
    # 旧: store_true(既定False) -> NO_TRADE の no_trade_correct/missed が永久に確定しなかった。
    parser.add_argument("--include-no-trade", dest="include_no_trade", action="store_true", default=True,
                        help="NO_TRADEシグナルも再評価する(既定: 有効)")
    parser.add_argument("--no-include-no-trade", dest="include_no_trade", action="store_false",
                        help="NO_TRADEシグナルを再評価から除外する(非推奨: 見送り判断も学習サンプル)")
    parser.add_argument("--write-sheets", action="store_true", help="Append reevaluations to Google Sheets PENDING_REEVALUATIONS")
    return parser.parse_args()


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


def load_from_sheets() -> tuple[pd.DataFrame, pd.DataFrame] | None:
    try:
        client = get_sheets_client()
        if client is None:
            return None
        spreadsheet = client.open_by_key(os.environ["GOOGLE_SHEET_ID"])
        frames = {}
        for key, sheet_name in SHEET_NAMES.items():
            try:
                frames[key] = worksheet_to_dataframe(spreadsheet.worksheet(sheet_name))
                print(f"ok: loaded {len(frames[key])} rows from Google Sheets {sheet_name}")
            except Exception as exc:  # noqa: BLE001 - fallback handles missing worksheets.
                print(f"warning: Google Sheets worksheet {sheet_name} unavailable: {exc}")
                frames[key] = pd.DataFrame()
        return frames["signals"], frames["evaluations"]
    except Exception as exc:  # noqa: BLE001 - local fallback is intentional.
        print(f"warning: Google Sheets read failed; falling back to local CSV: {exc}")
        return None


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, str]:
    sheet_data = load_from_sheets()
    if sheet_data is not None:
        return sheet_data[0], sheet_data[1], "sheets"
    return read_csv(LOCAL_PATHS["signals"]), read_csv(LOCAL_PATHS["evaluations"]), "local_csv"


def clean_text(value) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()


def lower_text(value) -> str:
    return clean_text(value).lower()


def best_date_column(df: pd.DataFrame, candidates: list[str]) -> str:
    for col in candidates:
        if col in df.columns:
            return col
    return ""


def apply_lookback(signals: pd.DataFrame, lookback_days: int) -> pd.DataFrame:
    if signals.empty or lookback_days <= 0:
        return signals
    date_col = best_date_column(signals, ["signal_date", "date", "generated_at", "created_at"])
    if not date_col:
        return signals
    out = signals.copy()
    parsed = pd.to_datetime(out[date_col], errors="coerce", utc=True).dt.tz_localize(None)
    if parsed.dropna().empty:
        return signals
    cutoff = parsed.max() - pd.Timedelta(days=lookback_days - 1)
    return out[(parsed.isna()) | (parsed >= cutoff)]


def dedupe_latest_evaluations(evaluations: pd.DataFrame) -> pd.DataFrame:
    if evaluations.empty or "signal_id" not in evaluations.columns:
        return pd.DataFrame()
    out = evaluations.copy()
    out["_row_order"] = range(len(out))
    out["signal_id"] = out["signal_id"].map(clean_text)
    out = out[out["signal_id"] != ""].copy()
    if out.empty:
        return out.drop(columns=["_row_order"], errors="ignore")
    date_col = best_date_column(out, ["reevaluation_at_utc", "evaluation_date", "date", "generated_at", "reevaluation_at_jst"])
    if date_col:
        out["_sort_key"] = pd.to_datetime(out[date_col], errors="coerce", utc=True).dt.tz_localize(None)
    else:
        out["_sort_key"] = pd.NaT
    before = len(out)
    out = out.sort_values(["_sort_key", "_row_order"], na_position="first").drop_duplicates("signal_id", keep="last")
    if before != len(out):
        print(f"warning: duplicate EVALUATIONS signal_id rows detected; using latest rows ({before} -> {len(out)})")
    return out.drop(columns=["_sort_key", "_row_order"], errors="ignore")


def has_open_latest_evaluation(row: pd.Series) -> bool:
    outcome = lower_text(row.get("outcome", ""))
    status = lower_text(row.get("status", ""))
    evaluation_status = lower_text(row.get("evaluation_status", ""))
    if outcome in FINAL_OUTCOMES or status == "closed" or evaluation_status == "closed":
        return False
    return outcome in OPEN_OUTCOMES or status in OPEN_STATUSES or evaluation_status in OPEN_STATUSES


def select_reevaluation_targets(
    signals: pd.DataFrame,
    evaluations: pd.DataFrame,
    *,
    lookback_days: int,
    include_no_trade: bool,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if signals.empty:
        return pd.DataFrame(), dedupe_latest_evaluations(evaluations)

    sig = normalize_headers(signals)
    if "signal_id" not in sig.columns:
        sig["signal_id"] = ""
    sig["signal_id"] = sig["signal_id"].map(clean_text)
    # lookback は計算量の目安であって「未確定行の廃棄」ではない(設計書§6 サンプル廃棄禁止)。
    # 窓は「窓内 or 評価が未確定」の union に緩め、窓外の未確定行は aged_open として可視化する。
    in_window_ids: set[str] | None = None
    if lookback_days > 0 and not sig.empty:
        in_window_ids = set(apply_lookback(sig, lookback_days)["signal_id"].map(clean_text))

    if not include_no_trade:
        side = sig.get("side", pd.Series("", index=sig.index)).fillna("").astype(str).str.upper()
        rank = sig.get("rank", pd.Series("", index=sig.index)).fillna("").astype(str).str.upper()
        sig = sig[(side != "NONE") & (rank != "NO_TRADE")].copy()

    latest_eval = dedupe_latest_evaluations(normalize_headers(evaluations))
    latest_by_signal = {}
    if not latest_eval.empty and "signal_id" in latest_eval.columns:
        latest_by_signal = {clean_text(row["signal_id"]): row for _, row in latest_eval.iterrows()}

    rows = []
    aged_open_kept = 0
    for _, signal in sig.iterrows():
        signal_id = clean_text(signal.get("signal_id", ""))
        latest = latest_by_signal.get(signal_id)
        is_open = latest is None or has_open_latest_evaluation(latest)
        if not is_open:
            continue  # 確定済みは再評価不要(廃棄ではない)
        if in_window_ids is not None and signal_id not in in_window_ids:
            aged_open_kept += 1  # 窓外だが未確定 -> 廃棄せず対象に残す
        rows.append(signal)
    targets = pd.DataFrame(rows).reset_index(drop=True)
    targets = normalize_headers(targets)
    targets.attrs["aged_open_kept"] = aged_open_kept
    return targets, latest_eval


def bool_changed(previous, current) -> bool:
    prev = clean_text(previous)
    cur = clean_text(current)
    if prev == "" and cur == "":
        return False
    prev_num = pd.to_numeric(prev, errors="coerce")
    cur_num = pd.to_numeric(cur, errors="coerce")
    if not pd.isna(prev_num) and not pd.isna(cur_num):
        return round(float(prev_num), 6) != round(float(cur_num), 6)
    return prev != cur


def annotate_reevaluations(
    reevaluations: pd.DataFrame,
    latest_eval: pd.DataFrame,
    *,
    source: str,
    run_id: str,
    generated_at_utc,
) -> pd.DataFrame:
    if reevaluations.empty:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)
    latest_by_signal = {}
    if not latest_eval.empty and "signal_id" in latest_eval.columns:
        latest_by_signal = {clean_text(row["signal_id"]): row for _, row in latest_eval.iterrows()}

    out = reevaluations.copy()
    out["reevaluation_at_jst"] = format_jst(generated_at_utc)
    out["reevaluation_at_utc"] = format_utc(generated_at_utc)
    out["reevaluation_run_id"] = run_id
    out["source"] = source
    out["is_latest_evaluation"] = True
    previous_rows = []
    for _, row in out.iterrows():
        prev = latest_by_signal.get(clean_text(row.get("signal_id", "")), pd.Series(dtype=object))
        previous_rows.append(
            {
                "previous_status": prev.get("status", ""),
                "previous_evaluation_status": prev.get("evaluation_status", ""),
                "previous_outcome": prev.get("outcome", ""),
                "previous_r_multiple": prev.get("r_multiple", prev.get("r_result", "")),
                "changed_status": bool_changed(prev.get("status", ""), row.get("status", "")),
                "changed_outcome": bool_changed(prev.get("outcome", ""), row.get("outcome", "")),
                "changed_r_multiple": bool_changed(prev.get("r_multiple", prev.get("r_result", "")), row.get("r_multiple", row.get("r_result", ""))),
            }
        )
    previous_df = pd.DataFrame(previous_rows, index=out.index)
    out = pd.concat([out, previous_df], axis=1)
    return out.reindex(columns=OUTPUT_COLUMNS)


def is_closed_row(row: pd.Series) -> bool:
    return lower_text(row.get("evaluation_status", row.get("status", ""))) == "closed" or lower_text(row.get("outcome", "")) in {"win_tp1", "win_tp2", "loss_sl"}


def truthy_series(df: pd.DataFrame, column: str) -> pd.Series:
    if column not in df.columns:
        return pd.Series(False, index=df.index)
    return df[column].fillna("").astype(str).str.lower().isin(["true", "1", "yes"])


def markdown_table(df: pd.DataFrame, columns: list[str], empty: str) -> str:
    if df.empty:
        return empty
    view = df.copy()
    for col in columns:
        if col not in view.columns:
            view[col] = ""
    view = view[columns].head(20)
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    rows = []
    for _, row in view.iterrows():
        cells = [clean_text(row.get(col, "")).replace("|", "\\|") for col in columns]
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *rows])


def build_report(
    reevaluations: pd.DataFrame,
    *,
    generated_at_utc,
    source: str,
    total_signals: int,
    target_count: int,
    include_no_trade: bool,
    sheets_result: dict,
) -> str:
    closed_count = int(reevaluations.apply(is_closed_row, axis=1).sum()) if not reevaluations.empty else 0
    outcome = reevaluations.get("outcome", pd.Series(dtype=str)).fillna("").astype(str).str.lower() if not reevaluations.empty else pd.Series(dtype=str)
    no_entry_count = int((outcome == "no_entry").sum())
    open_count = int((outcome == "open_unresolved").sum())
    missed_count = int(truthy_series(reevaluations, "missed_opportunity").sum()) if not reevaluations.empty else 0
    closed = reevaluations[reevaluations.apply(is_closed_row, axis=1)] if not reevaluations.empty else pd.DataFrame()
    unresolved = reevaluations[outcome.isin(["open_unresolved", "no_entry"])] if not reevaluations.empty else pd.DataFrame()
    missed = reevaluations[truthy_series(reevaluations, "missed_opportunity")] if not reevaluations.empty else pd.DataFrame()
    no_trade = reevaluations[reevaluations.get("side", pd.Series(dtype=str)).fillna("").astype(str).str.upper() == "NONE"] if not reevaluations.empty and "side" in reevaluations.columns else pd.DataFrame()

    lines = [
        "# Pending Signal Re-evaluation Report",
        "",
        "## 1. 概要",
        "",
        f"* 生成日時JST: {format_jst(generated_at_utc)}",
        f"* データソース: {source}",
        f"* 対象SIGNALS件数: {total_signals}",
        f"* 再評価対象件数: {target_count}",
        f"* closed化した件数: {closed_count}",
        f"* no_entry継続件数: {no_entry_count}",
        f"* open継続件数: {open_count}",
        f"* missed_opportunity件数: {missed_count}",
        f"* Sheets保存: {sheets_result.get('requested_label', '未実行')}",
        f"* Sheets保存成功件数: {sheets_result.get('appended_rows', 0)}",
        f"* Sheets重複スキップ件数: {sheets_result.get('skipped_duplicates', 0)}",
        f"* Sheets保存warning: {sheets_result.get('error', '') or 'なし'}",
        "",
        "## 2. 決着したシグナル",
        "",
        markdown_table(closed, ["signal_id", "asset", "side", "rank", "previous_outcome", "outcome", "r_multiple", "error_type"], "決着したシグナルはありません。"),
        "",
        "## 3. 未決着継続",
        "",
        markdown_table(unresolved, ["signal_id", "asset", "side", "rank", "outcome", "mfe_r", "mae_r", "bars_checked"], "未決着継続のシグナルはありません。"),
        "",
        "## 4. 取り逃し候補",
        "",
        markdown_table(missed, ["signal_id", "asset", "side", "rank", "outcome", "mfe_r", "mae_r", "notes"], "取り逃し候補はありません。"),
        "",
        "## 5. No Trade再評価",
        "",
        markdown_table(no_trade, ["signal_id", "asset", "side", "rank", "outcome", "error_type"], "No Trade再評価は実行していません。" if not include_no_trade else "No Trade再評価対象はありません。"),
        "",
        "## 6. 注意",
        "",
        "* このレポートは実売買ではありません。",
        "* Tactical Swing OS が過去に出した判断の仮想評価です。",
        "* 価格データの欠損や市場休場により、評価が遅れる場合があります。",
        "* append-only運用でEVALUATIONSへ追記する場合、分析側では最新評価行を採用する必要があります。",
    ]
    return "\n".join(lines) + "\n"


def safe_json_records(df: pd.DataFrame) -> list[dict]:
    if df.empty:
        return []
    clean = df.where(pd.notna(df), None)
    return clean.to_dict(orient="records")


def default_sheets_result(write_requested: bool) -> dict:
    return {
        "write_sheets_requested": bool(write_requested),
        "write_sheets_status": "skipped",
        "requested_label": "未実行" if not write_requested else "実行",
        "sheets_appended_rows": 0,
        "sheets_skipped_duplicates": 0,
        "sheets_error": "",
        "appended_rows": 0,
        "skipped_duplicates": 0,
        "error": "",
        "sheet_name": "PENDING_REEVALUATIONS",
    }


def append_pending_reevaluations_to_sheets(csv_path: Path) -> dict:
    result = default_sheets_result(True)
    try:
        from sync_to_sheets import append_csv_with_result, get_client, open_spreadsheet

        client = get_client()
        if client is None:
            result.update(
                {
                    "write_sheets_status": "skipped",
                    "sheets_error": "GOOGLE_SERVICE_ACCOUNT_JSON or GOOGLE_SHEET_ID is missing",
                    "error": "GOOGLE_SERVICE_ACCOUNT_JSON or GOOGLE_SHEET_ID is missing",
                }
            )
            print("warning: pending reevaluation Sheets append skipped; credentials are missing")
            return result

        spreadsheet = open_spreadsheet(client)
        sync_result = append_csv_with_result(spreadsheet, csv_path, "PENDING_REEVALUATIONS")
        status = sync_result.get("status", "failed")
        if status == "success":
            write_status = "success"
        elif sync_result.get("appended_rows", 0) > 0:
            write_status = "partial"
        elif status == "skipped":
            write_status = "skipped"
        else:
            write_status = "failed"
        result.update(
            {
                "write_sheets_status": write_status,
                "sheets_appended_rows": int(sync_result.get("appended_rows", 0)),
                "sheets_skipped_duplicates": int(sync_result.get("skipped_duplicates", 0)),
                "sheets_error": sync_result.get("error", ""),
                "appended_rows": int(sync_result.get("appended_rows", 0)),
                "skipped_duplicates": int(sync_result.get("skipped_duplicates", 0)),
                "error": sync_result.get("error", ""),
                "key_columns": sync_result.get("key_columns", []),
            }
        )
        return result
    except Exception as exc:  # noqa: BLE001 - artifacts should survive Sheets failures.
        message = str(exc)
        print(f"warning: pending reevaluation Sheets append failed; artifacts kept: {message}")
        result.update({"write_sheets_status": "failed", "sheets_error": message, "error": message})
        return result


def build_summary_payload(
    reevaluations: pd.DataFrame,
    *,
    generated_at_utc,
    source: str,
    total_signals: int,
    target_count: int,
    run_id: str,
    sheets_result: dict,
    aged_open_kept: int = 0,
) -> dict:
    outcome = reevaluations.get("outcome", pd.Series(dtype=str)).fillna("").astype(str).str.lower() if not reevaluations.empty else pd.Series(dtype=str)
    closed_count = int(reevaluations.apply(is_closed_row, axis=1).sum()) if not reevaluations.empty else 0
    return {
        "generated_at_jst": format_jst(generated_at_utc),
        "generated_at_utc": format_utc(generated_at_utc),
        "reevaluation_run_id": run_id,
        "source": source,
        "total_signals": int(total_signals),
        "target_signals": int(target_count),
        "reevaluated_rows": int(len(reevaluations)),
        # lookback窓外だが未確定のため対象に残した行数(サンプル廃棄禁止の可視化・設計書§6)
        "aged_open_kept": int(aged_open_kept),
        "closed_count": closed_count,
        "open_count": int((outcome == "open_unresolved").sum()),
        "no_entry_count": int((outcome == "no_entry").sum()),
        "missed_opportunity_count": int(truthy_series(reevaluations, "missed_opportunity").sum()) if not reevaluations.empty else 0,
        "write_sheets_requested": bool(sheets_result.get("write_sheets_requested", False)),
        "write_sheets_status": sheets_result.get("write_sheets_status", "skipped"),
        "sheets_appended_rows": int(sheets_result.get("sheets_appended_rows", 0)),
        "sheets_skipped_duplicates": int(sheets_result.get("sheets_skipped_duplicates", 0)),
        "sheets_error": sheets_result.get("sheets_error", ""),
        "sheets_key_columns": sheets_result.get("key_columns", []),
    }


def main() -> int:
    args = parse_args()
    generated_at_utc = now_utc()
    run_id = f"reeval_{generated_at_utc.strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:8]}"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    signals, evaluations, source = load_inputs()
    signals = normalize_headers(signals)
    evaluations = normalize_headers(evaluations)
    targets, latest_eval = select_reevaluation_targets(
        signals,
        evaluations,
        lookback_days=args.lookback_days,
        include_no_trade=args.include_no_trade,
    )
    print(f"ok: source={source} signals={len(signals)} evaluations={len(evaluations)} targets={len(targets)}")

    base = evaluate_signals_dataframe(targets, args.horizon)
    reevaluations = annotate_reevaluations(base, latest_eval, source=source, run_id=run_id, generated_at_utc=generated_at_utc)

    csv_path = RESULTS_DIR / "pending_reevaluations.csv"
    json_path = RESULTS_DIR / "pending_reevaluations.json"
    summary_path = RESULTS_DIR / "pending_reevaluation_summary.json"
    report_path = REPORTS_DIR / f"{generated_at_utc.astimezone(JST).strftime('%Y-%m-%d')}_pending_reevaluation.md"

    reevaluations.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(safe_json_records(reevaluations), ensure_ascii=False, indent=2), encoding="utf-8")
    sheets_result = default_sheets_result(args.write_sheets)
    if args.write_sheets:
        sheets_result = append_pending_reevaluations_to_sheets(csv_path)
    else:
        print("ok: Google Sheets write skipped; --write-sheets was not set")
    summary_path.write_text(
        json.dumps(
            build_summary_payload(
                reevaluations,
                generated_at_utc=generated_at_utc,
                source=source,
                total_signals=len(signals),
                target_count=len(targets),
                run_id=run_id,
                sheets_result=sheets_result,
                aged_open_kept=int(targets.attrs.get("aged_open_kept", 0)),
            ),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    report_path.write_text(
        build_report(
            reevaluations,
            generated_at_utc=generated_at_utc,
            source=source,
            total_signals=len(signals),
            target_count=len(targets),
            include_no_trade=args.include_no_trade,
            sheets_result=sheets_result,
        ),
        encoding="utf-8",
    )
    print(f"pending reevaluations generated: {len(reevaluations)}")
    print(f"pending reevaluation summary generated: {summary_path}")
    print(f"pending reevaluations report generated: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
