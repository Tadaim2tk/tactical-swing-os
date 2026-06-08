from __future__ import annotations

import argparse
import json
import math
import os
from datetime import datetime
from pathlib import Path

import pandas as pd

import evaluation_loader


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/reason_codes")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_MAPPINGS = {
    "signals": ("SIGNALS", RESULTS_DIR / "signals.csv"),
    "evaluations": ("EVALUATIONS", RESULTS_DIR / "evaluations.csv"),
}
DATE_COLUMNS = ["signal_date", "date", "evaluation_date"]
SIGNAL_COLUMNS = [
    "signal_id",
    "date",
    "asset",
    "side",
    "rank",
    "type",
    "reason_codes",
    "no_trade_reason",
    "recommended_action",
    "setup_quality_score",
    "entry_quality_score",
    "direction_confidence",
    "signal_strength",
    "data_quality",
]
EVALUATION_COLUMNS = [
    "signal_id",
    "outcome",
    "error_type",
    "r_multiple",
    "mfe_r",
    "mae_r",
    "missed_opportunity",
    "status",
    "evaluation_status",
    "evaluation_date",
]
REASON_COLUMNS = [
    "reason_code",
    "signals_count",
    "evaluated_count",
    "win_count",
    "loss_count",
    "no_entry_count",
    "missed_opportunity_count",
    "win_rate",
    "total_r",
    "average_r",
    "median_r",
    "best_r",
    "worst_r",
    "average_mfe_r",
    "average_mae_r",
    "rank_a_count",
    "rank_b_count",
    "no_trade_count",
    "recommended_action_trade_count",
    "recommended_action_watch_count",
    "recommended_action_no_trade_count",
    "reliability_label",
]
NO_TRADE_COLUMNS = [
    "no_trade_reason",
    "count",
    "no_trade_correct_count",
    "no_trade_missed_count",
    "missed_opportunity_count",
    "average_mfe_r",
    "average_r",
    "assessment",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze Tactical Swing OS reason code performance.")
    parser.add_argument("--start", help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end", help="End date in YYYY-MM-DD format")
    parser.add_argument("--period", choices=["weekly", "monthly"], default="monthly", help="Default period when start/end are omitted")
    return parser.parse_args()


def default_period(period: str) -> tuple[pd.Timestamp, pd.Timestamp]:
    end = pd.Timestamp(datetime.now().date())
    days = 6 if period == "weekly" else 29
    return end - pd.Timedelta(days=days), end


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
        print("Google Sheets env not set; using local CSV fallback")
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


def load_from_sheets() -> dict[str, pd.DataFrame] | None:
    try:
        client = get_sheets_client()
        if client is None:
            return None
        spreadsheet = client.open_by_key(os.environ["GOOGLE_SHEET_ID"])
        data: dict[str, pd.DataFrame] = {}
        for key, (sheet_name, _) in SHEET_MAPPINGS.items():
            try:
                worksheet = spreadsheet.worksheet(sheet_name)
            except Exception as exc:  # noqa: BLE001 - missing sheet should not stop fallback.
                print(f"warning: Google Sheets worksheet {sheet_name} not found or unreadable: {exc}")
                data[key] = pd.DataFrame()
                continue
            df = worksheet_to_dataframe(worksheet)
            data[key] = df
            print(f"ok: loaded {len(df)} rows from Google Sheets {sheet_name}")
        return data
    except Exception as exc:  # noqa: BLE001 - fallback to local CSV is intentional.
        print(f"warning: Google Sheets read failed; falling back to local CSV: {exc}")
        return None


def load_from_local_csv() -> dict[str, pd.DataFrame]:
    data = {}
    for key, (_, path) in SHEET_MAPPINGS.items():
        df = read_csv(path)
        data[key] = df
        print(f"ok: loaded {len(df)} rows from local CSV {path}")
    return data


def load_input_data() -> dict[str, pd.DataFrame]:
    sheets_data = load_from_sheets()
    if sheets_data is not None:
        return sheets_data
    return load_from_local_csv()


def ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = normalize_headers(df)
    for col in columns:
        if col not in out.columns:
            out[col] = ""
    return out[columns].copy()


def find_date_column(df: pd.DataFrame) -> str | None:
    for col in DATE_COLUMNS:
        if col in df.columns:
            return col
    return None


def filter_period(df: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    date_col = find_date_column(df)
    if not date_col:
        return df.copy()
    out = df.copy()
    out["_analysis_date"] = pd.to_datetime(out[date_col], errors="coerce", utc=True).dt.tz_localize(None)
    mask = (out["_analysis_date"].dt.date >= start.date()) & (out["_analysis_date"].dt.date <= end.date())
    return out[mask].drop(columns=["_analysis_date"])


def to_bool(series: pd.Series) -> pd.Series:
    return series.fillna("").astype(str).str.lower().isin(["true", "1", "yes"])


def numeric_series(df: pd.DataFrame, column: str) -> pd.Series:
    if df.empty or column not in df.columns:
        return pd.Series(dtype=float)
    return pd.to_numeric(df[column], errors="coerce").dropna()


def combine_signals_evaluations(signals: pd.DataFrame, evaluations: pd.DataFrame) -> pd.DataFrame:
    signals = ensure_columns(signals, SIGNAL_COLUMNS)
    evaluations = ensure_columns(evaluations, EVALUATION_COLUMNS)
    if signals.empty:
        return signals
    if evaluations.empty:
        merged = signals.copy()
        for col in EVALUATION_COLUMNS:
            if col != "signal_id":
                merged[col] = ""
        return merged
    return signals.merge(evaluations, on="signal_id", how="left", suffixes=("", "_eval"))


def split_reason_codes(value) -> list[str]:
    if pd.isna(value):
        return []
    codes = [code.strip() for code in str(value).split("|")]
    return [code for code in codes if code]


def explode_reason_codes(merged: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in merged.iterrows():
        for code in split_reason_codes(row.get("reason_codes", "")):
            record = row.to_dict()
            record["reason_code"] = code
            rows.append(record)
    if not rows:
        return pd.DataFrame(columns=list(merged.columns) + ["reason_code"])
    return pd.DataFrame(rows)


def evaluated_mask(df: pd.DataFrame) -> pd.Series:
    if df.empty:
        return pd.Series(dtype=bool)
    r = pd.to_numeric(df.get("r_multiple", pd.Series(index=df.index, dtype=float)), errors="coerce")
    outcome = df.get("outcome", pd.Series(index=df.index, dtype=str)).fillna("").astype(str)
    error_type = df.get("error_type", pd.Series(index=df.index, dtype=str)).fillna("").astype(str)
    status = df.get("status", df.get("evaluation_status", pd.Series(index=df.index, dtype=str))).fillna("").astype(str)
    return r.notna() | outcome.ne("") | error_type.ne("") | status.ne("")


def reliability_label(evaluated_count: int, average_r: float, win_rate: float) -> str:
    if evaluated_count < 5:
        return "insufficient_data"
    if average_r > 0.3 and win_rate >= 0.5:
        return "strong_positive"
    if average_r > 0.1 and win_rate >= 0.45:
        return "positive"
    if average_r < -0.3:
        return "strong_negative"
    if average_r < -0.1:
        return "negative"
    return "neutral"


def reason_summary(exploded: pd.DataFrame) -> pd.DataFrame:
    if exploded.empty:
        return pd.DataFrame(columns=REASON_COLUMNS)

    rows = []
    for code, part in exploded.groupby("reason_code", dropna=False):
        r = numeric_series(part, "r_multiple")
        eval_part = part[evaluated_mask(part)]
        outcome = part.get("outcome", pd.Series(index=part.index, dtype=str)).fillna("").astype(str)
        rec = part.get("recommended_action", pd.Series(index=part.index, dtype=str)).fillna("").astype(str).str.upper()
        rank = part.get("rank", pd.Series(index=part.index, dtype=str)).fillna("").astype(str).str.upper()
        missed = to_bool(part["missed_opportunity"]) if "missed_opportunity" in part.columns else pd.Series([False] * len(part))
        win_count = int(outcome.isin(["win_tp1", "win_tp2"]).sum())
        loss_count = int((outcome == "loss_sl").sum())
        no_entry_count = int((outcome == "no_entry").sum())
        win_rate = win_count / len(eval_part) if len(eval_part) else 0.0
        average_r = float(r.mean()) if not r.empty else 0.0
        rows.append(
            {
                "reason_code": code,
                "signals_count": len(part),
                "evaluated_count": len(eval_part),
                "win_count": win_count,
                "loss_count": loss_count,
                "no_entry_count": no_entry_count,
                "missed_opportunity_count": int(missed.sum()),
                "win_rate": round(win_rate, 4),
                "total_r": round(float(r.sum()) if not r.empty else 0.0, 4),
                "average_r": round(average_r, 4),
                "median_r": round(float(r.median()) if not r.empty else 0.0, 4),
                "best_r": round(float(r.max()) if not r.empty else 0.0, 4),
                "worst_r": round(float(r.min()) if not r.empty else 0.0, 4),
                "average_mfe_r": round(float(numeric_series(part, "mfe_r").mean()) if not numeric_series(part, "mfe_r").empty else 0.0, 4),
                "average_mae_r": round(float(numeric_series(part, "mae_r").mean()) if not numeric_series(part, "mae_r").empty else 0.0, 4),
                "rank_a_count": int((rank == "A").sum()),
                "rank_b_count": int((rank == "B").sum()),
                "no_trade_count": int((rank == "NO_TRADE").sum()),
                "recommended_action_trade_count": int((rec == "TRADE").sum()),
                "recommended_action_watch_count": int((rec == "WATCH").sum()),
                "recommended_action_no_trade_count": int((rec == "NO_TRADE").sum()),
                "reliability_label": reliability_label(len(eval_part), average_r, win_rate),
            }
        )
    return pd.DataFrame(rows, columns=REASON_COLUMNS).sort_values(["average_r", "signals_count"], ascending=[False, False])


def no_trade_assessment(count: int, correct: int, missed: int, missed_opportunity: int) -> str:
    if count < 5:
        return "insufficient_data"
    if missed > 0 or missed_opportunity > 0:
        return "over_filtering_risk"
    if correct >= max(1, count * 0.6):
        return "effective_filter"
    return "neutral"


def no_trade_summary(merged: pd.DataFrame) -> pd.DataFrame:
    if merged.empty or "no_trade_reason" not in merged.columns:
        return pd.DataFrame(columns=NO_TRADE_COLUMNS)
    data = merged.copy()
    data["no_trade_reason"] = data["no_trade_reason"].fillna("").astype(str).str.strip()
    data = data[data["no_trade_reason"] != ""]
    if data.empty:
        return pd.DataFrame(columns=NO_TRADE_COLUMNS)

    rows = []
    for reason, part in data.groupby("no_trade_reason", dropna=False):
        outcome = part.get("outcome", pd.Series(index=part.index, dtype=str)).fillna("").astype(str)
        missed = to_bool(part["missed_opportunity"]) if "missed_opportunity" in part.columns else pd.Series([False] * len(part))
        correct_count = int((outcome == "no_trade_correct").sum())
        missed_count = int((outcome == "no_trade_missed").sum())
        missed_opp = int(missed.sum())
        rows.append(
            {
                "no_trade_reason": reason,
                "count": len(part),
                "no_trade_correct_count": correct_count,
                "no_trade_missed_count": missed_count,
                "missed_opportunity_count": missed_opp,
                "average_mfe_r": round(float(numeric_series(part, "mfe_r").mean()) if not numeric_series(part, "mfe_r").empty else 0.0, 4),
                "average_r": round(float(numeric_series(part, "r_multiple").mean()) if not numeric_series(part, "r_multiple").empty else 0.0, 4),
                "assessment": no_trade_assessment(len(part), correct_count, missed_count, missed_opp),
            }
        )
    return pd.DataFrame(rows, columns=NO_TRADE_COLUMNS).sort_values(["missed_opportunity_count", "no_trade_missed_count", "count"], ascending=[False, False, False])


def markdown_table(df: pd.DataFrame, empty: str = "_該当なし_") -> str:
    if df.empty:
        return empty
    view = df.fillna("").astype(str)
    headers = list(view.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in view.iterrows():
        lines.append("| " + " | ".join(str(row[col]).replace("|", "\\|") for col in headers) + " |")
    return "\n".join(lines)


def json_safe(value):
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def records(df: pd.DataFrame) -> list[dict]:
    if df.empty:
        return []
    return [{key: json_safe(value) for key, value in row.items()} for row in df.to_dict(orient="records")]


def build_analysis(start: pd.Timestamp, end: pd.Timestamp) -> tuple[pd.DataFrame, str]:
    input_data = load_input_data()
    preferred_evaluations, evaluation_meta = evaluation_loader.load_evaluations_prefer_latest()
    if not preferred_evaluations.empty or evaluation_meta.get("evaluation_source") != "none":
        input_data["evaluations"] = preferred_evaluations
    signals = filter_period(input_data["signals"], start, end)
    evaluations = filter_period(input_data["evaluations"], start, end)
    merged = combine_signals_evaluations(signals, evaluations)
    exploded = explode_reason_codes(merged)
    reason_table = reason_summary(exploded)
    no_trade_table = no_trade_summary(merged)

    top_positive = reason_table[reason_table["reliability_label"].isin(["strong_positive", "positive"])].head(10) if not reason_table.empty else pd.DataFrame()
    top_negative = reason_table[reason_table["reliability_label"].isin(["strong_negative", "negative"])].sort_values("average_r").head(10) if not reason_table.empty else pd.DataFrame()
    over_filtering = no_trade_table[no_trade_table["assessment"] == "over_filtering_risk"].head(10) if not no_trade_table.empty else pd.DataFrame()
    insufficient_count = int((reason_table["reliability_label"] == "insufficient_data").sum()) if not reason_table.empty else 0
    notes = [
        "reason_code単位のweights自動更新はまだ行いません。",
        f"insufficient_data reason_codes: {insufficient_count}",
    ]
    if reason_table.empty:
        notes.append("reason_codes列が空、または期間内に対象データがありません。")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_csv = RESULTS_DIR / "reason_code_analysis.csv"
    output_json = RESULTS_DIR / "reason_code_analysis.json"
    report_path = REPORTS_DIR / f"{end.strftime('%Y-%m-%d')}_reason_code_analysis.md"

    reason_table.to_csv(output_csv, index=False)
    payload = {
        "start_date": start.strftime("%Y-%m-%d"),
        "end_date": end.strftime("%Y-%m-%d"),
        "reason_code_summary": records(reason_table),
        "no_trade_reason_summary": records(no_trade_table),
        "top_positive_reasons": records(top_positive),
        "top_negative_reasons": records(top_negative),
        "over_filtering_candidates": records(over_filtering),
        **evaluation_meta,
        "notes": notes,
    }
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    conclusion = "reason_codesの有効性を集計しました。"
    if reason_table.empty:
        conclusion = "期間内にreason_codes分析対象がありません。Phase 6以降のSIGNALS蓄積後に再確認してください。"
    elif not top_positive.empty:
        conclusion = f"上位プラス要因は {top_positive.iloc[0]['reason_code']} です。"
    report = f"""# Tactical Swing OS Reason Code Analysis

## 1. 結論

{conclusion}

対象期間: {start.strftime('%Y-%m-%d')} - {end.strftime('%Y-%m-%d')}

評価データソース: {evaluation_meta["evaluation_source"]} / latest_evaluations_available: {evaluation_meta["latest_evaluations_available"]} / fallback_used: {evaluation_meta["fallback_used"]}

## 2. reason_codes 上位プラス要因

{markdown_table(top_positive.head(10))}

## 3. reason_codes 上位マイナス要因

{markdown_table(top_negative.head(10))}

## 4. no_trade_reason 分析

{markdown_table(no_trade_table)}

## 5. 取り逃し候補

{markdown_table(over_filtering)}

## 6. 改善候補

{markdown_table(reason_table[reason_table["reliability_label"].isin(["strong_negative", "negative", "strong_positive", "positive"])].head(20) if not reason_table.empty else pd.DataFrame())}

## 7. データ不足の注意

reason_codeごとの評価件数が5件未満の場合は `insufficient_data` とし、weights.jsonは自動更新しません。

## 8. REASON_CODE_ANALYSIS CSV

```csv
{reason_table.to_csv(index=False).strip()}
```

## 9. REASON_CODE_ANALYSIS JSON

```json
{json.dumps(payload, ensure_ascii=False, indent=2)}
```
"""
    report_path.write_text(report, encoding="utf-8")
    print(f"reason code analysis generated: {report_path}")
    print(f"reason code rows: {len(reason_table)}")
    print(f"no_trade_reason rows: {len(no_trade_table)}")
    return reason_table, str(report_path)


def main() -> int:
    args = parse_args()
    if args.start and args.end:
        start = pd.Timestamp(args.start)
        end = pd.Timestamp(args.end)
    else:
        start, end = default_period(args.period)
    if start > end:
        raise ValueError("--start must be before or equal to --end")
    build_analysis(start, end)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
