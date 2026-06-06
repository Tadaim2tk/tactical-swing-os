from __future__ import annotations

import argparse
import json
import math
import os
from datetime import datetime
from pathlib import Path

import pandas as pd


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/monthly")
WEIGHTS_PATH = Path("models/weights.json")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
DATE_COLUMNS = ["date", "signal_date", "evaluation_date", "hit_date", "run_ts"]
SHEET_MAPPINGS = {
    "market_snapshot": ("MARKET_SNAPSHOT", RESULTS_DIR / "market_snapshot.csv"),
    "signals": ("SIGNALS", RESULTS_DIR / "signals.csv"),
    "evaluations": ("EVALUATIONS", RESULTS_DIR / "evaluations.csv"),
}
LOG_COLUMNS = [
    "month_start",
    "month_end",
    "total_signals",
    "closed_signals",
    "pending_signals",
    "skipped_signals",
    "win_rate",
    "profit_factor",
    "total_r",
    "average_r",
    "max_win_r",
    "max_loss_r",
    "best_asset",
    "worst_asset",
    "best_rank",
    "worst_rank",
    "best_side",
    "worst_side",
    "next_month_mode",
    "max_daily_risk_pct",
    "weight_change_summary",
    "rule_change_1",
    "rule_change_2",
    "rule_change_3",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Tactical Swing OS monthly calibration.")
    parser.add_argument("--start", help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end", help="End date in YYYY-MM-DD format")
    return parser.parse_args()


def default_period() -> tuple[pd.Timestamp, pd.Timestamp]:
    end = pd.Timestamp(datetime.now().date())
    start = end - pd.Timedelta(days=29)
    return start, end


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
            except Exception as exc:  # noqa: BLE001 - missing sheet should not stop the review.
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
    out["_calibration_date"] = pd.to_datetime(out[date_col], errors="coerce", utc=True).dt.tz_localize(None)
    mask = (out["_calibration_date"].dt.date >= start.date()) & (out["_calibration_date"].dt.date <= end.date())
    return out[mask].drop(columns=["_calibration_date"])


def enrich_evaluations(evaluations: pd.DataFrame, signals: pd.DataFrame) -> pd.DataFrame:
    if evaluations.empty or signals.empty or "signal_id" not in evaluations.columns or "signal_id" not in signals.columns:
        return evaluations.copy()
    cols = [col for col in ["signal_id", "asset", "side", "rank", "date"] if col in signals.columns]
    lookup = signals[cols].drop_duplicates(subset=["signal_id"], keep="last")
    out = evaluations.merge(lookup, on="signal_id", how="left", suffixes=("", "_signal"))
    for col in ["asset", "side", "rank"]:
        signal_col = f"{col}_signal"
        if signal_col in out.columns:
            if col in out.columns:
                out[col] = out[col].fillna(out[signal_col])
            else:
                out[col] = out[signal_col]
            out = out.drop(columns=[signal_col])
    return out.drop(columns=[col for col in ["date_signal"] if col in out.columns])


def closed_df(evaluations: pd.DataFrame) -> pd.DataFrame:
    if evaluations.empty or "evaluation_status" not in evaluations.columns:
        return pd.DataFrame()
    return evaluations[evaluations["evaluation_status"].astype(str).str.lower() == "closed"].copy()


def numeric_r(df: pd.DataFrame) -> pd.Series:
    if df.empty or "r_result" not in df.columns:
        return pd.Series(dtype=float)
    return pd.to_numeric(df["r_result"], errors="coerce").dropna()


def r_metrics(evaluations: pd.DataFrame) -> dict:
    closed = closed_df(evaluations)
    r = numeric_r(closed)
    wins = r[r > 0]
    losses = r[r < 0]
    closed_count = len(closed)
    gross_profit = float(wins.sum()) if not wins.empty else 0.0
    gross_loss = abs(float(losses.sum())) if not losses.empty else 0.0
    if gross_loss > 0:
        profit_factor = gross_profit / gross_loss
    elif gross_profit > 0:
        profit_factor = math.inf
    else:
        profit_factor = 0.0
    return {
        "closed_count": closed_count,
        "win_rate": float(len(wins) / closed_count) if closed_count else 0.0,
        "profit_factor": profit_factor,
        "total_r": float(r.sum()) if not r.empty else 0.0,
        "average_r": float(r.mean()) if not r.empty else 0.0,
        "max_win_r": float(r.max()) if not r.empty else 0.0,
        "max_loss_r": float(r.min()) if not r.empty else 0.0,
    }


def count_status(evaluations: pd.DataFrame, status: str) -> int:
    if evaluations.empty or "evaluation_status" not in evaluations.columns:
        return 0
    return int((evaluations["evaluation_status"].astype(str).str.lower() == status).sum())


def proposed_change(closed_count: int, win_rate: float, average_r: float) -> tuple[float, str]:
    if closed_count < 5:
        return 0.0, "データ不足"
    if average_r > 0.3 and win_rate >= 0.5:
        return 0.05, "average_r > 0.3 and win_rate >= 0.5"
    if average_r > 0.1 and win_rate >= 0.45:
        return 0.03, "average_r > 0.1 and win_rate >= 0.45"
    if average_r < -0.3:
        return -0.05, "average_r < -0.3"
    if average_r < -0.1:
        return -0.03, "average_r < -0.1"
    return 0.0, "変更なし"


def calibration_table(signals: pd.DataFrame, evaluations: pd.DataFrame, column: str, values: list[str] | None = None) -> pd.DataFrame:
    if values is None:
        observed = set(signals[column].dropna().astype(str)) if column in signals.columns and not signals.empty else set()
        observed |= set(evaluations[column].dropna().astype(str)) if column in evaluations.columns and not evaluations.empty else set()
        values = sorted(observed)
    rows = []
    for value in values:
        sig_part = signals[signals[column].astype(str) == value] if column in signals.columns and not signals.empty else pd.DataFrame()
        eval_part = evaluations[evaluations[column].astype(str) == value] if column in evaluations.columns and not evaluations.empty else pd.DataFrame()
        metrics = r_metrics(eval_part)
        change, reason = proposed_change(metrics["closed_count"], metrics["win_rate"], metrics["average_r"])
        rows.append(
            {
                column: value,
                "signals": len(sig_part),
                "closed": metrics["closed_count"],
                "win_rate": round(metrics["win_rate"], 4),
                "total_r": round(metrics["total_r"], 4),
                "average_r": round(metrics["average_r"], 4),
                "best_r": round(metrics["max_win_r"], 4),
                "worst_r": round(metrics["max_loss_r"], 4),
                "proposed_weight_change": change,
                "reason": reason,
            }
        )
    return pd.DataFrame(rows)


def best_worst(table: pd.DataFrame, label_col: str) -> tuple[str, str]:
    if table.empty or "total_r" not in table.columns:
        return "", ""
    scored = table.copy()
    scored["total_r"] = pd.to_numeric(scored["total_r"], errors="coerce")
    scored = scored.dropna(subset=["total_r"])
    if scored.empty:
        return "", ""
    best = str(scored.sort_values("total_r", ascending=False).iloc[0][label_col])
    worst = str(scored.sort_values("total_r", ascending=True).iloc[0][label_col])
    return best, worst


def next_month_decision(metrics: dict) -> tuple[str, float, list[str]]:
    total_r = metrics["total_r"]
    win_rate = metrics["win_rate"]
    closed_count = metrics["closed_count"]
    notes = []
    if total_r > 3.0 and win_rate >= 0.5:
        mode = "攻撃"
    elif total_r >= 0 and win_rate >= 0.4:
        mode = "通常"
    else:
        mode = "防御"
    if closed_count < 10:
        mode = "通常"
        notes.append("データ不足")
    risk = {"攻撃": 1.0, "通常": 0.5, "防御": 0.25}[mode]
    return mode, risk, notes


def weight_change_summary(*tables: pd.DataFrame) -> str:
    changes = []
    for table in tables:
        if table.empty or "proposed_weight_change" not in table.columns:
            continue
        label_col = table.columns[0]
        for _, row in table.iterrows():
            change = float(row["proposed_weight_change"])
            if change:
                changes.append(f"{label_col}:{row[label_col]} {change:+.2f}")
    return "; ".join(changes) if changes else "変更提案なし"


def rule_changes(metrics: dict, mode_notes: list[str], summary: str) -> list[str]:
    changes = []
    if metrics["closed_count"] < 10:
        changes.append("closed評価10件未満のため自動適用しない")
    if summary != "変更提案なし":
        changes.append("提案のみ。weights.jsonは更新しない")
    if metrics["total_r"] < 0:
        changes.append("Entry/SL/Rank判定の見直し")
    elif metrics["total_r"] > 0 and metrics["win_rate"] >= 0.45:
        changes.append("現行ルール維持")
    changes.extend(mode_notes)
    while len(changes) < 3:
        changes.append("")
    return changes[:3]


def markdown_table(df: pd.DataFrame, empty: str = "_該当なし_") -> str:
    if df.empty:
        return empty
    view = df.fillna("").astype(str)
    headers = list(view.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in view.iterrows():
        lines.append("| " + " | ".join(str(row[col]).replace("|", "\\|") for col in headers) + " |")
    return "\n".join(lines)


def build_monthly_calibration(start: pd.Timestamp, end: pd.Timestamp) -> tuple[pd.DataFrame, str]:
    input_data = load_input_data()
    signals = filter_period(input_data["signals"], start, end)
    evaluations = filter_period(input_data["evaluations"], start, end)
    market_snapshot = filter_period(input_data["market_snapshot"], start, end)
    evaluations = enrich_evaluations(evaluations, signals)

    metrics = r_metrics(evaluations)
    pending_count = count_status(evaluations, "pending")
    skipped_count = count_status(evaluations, "skipped")
    asset_table = calibration_table(signals, evaluations, "asset")
    rank_table = calibration_table(signals, evaluations, "rank", ["A", "B", "NO_TRADE"])
    side_table = calibration_table(signals, evaluations, "side", ["LONG", "SHORT", "NONE"])
    best_asset, worst_asset = best_worst(asset_table, "asset")
    best_rank, worst_rank = best_worst(rank_table, "rank")
    best_side, worst_side = best_worst(side_table, "side")
    mode, risk, mode_notes = next_month_decision(metrics)
    summary = weight_change_summary(asset_table, rank_table, side_table)
    changes = rule_changes(metrics, mode_notes, summary)

    row = {
        "month_start": start.strftime("%Y-%m-%d"),
        "month_end": end.strftime("%Y-%m-%d"),
        "total_signals": len(signals),
        "closed_signals": metrics["closed_count"],
        "pending_signals": pending_count,
        "skipped_signals": skipped_count,
        "win_rate": round(metrics["win_rate"], 4),
        "profit_factor": "inf" if math.isinf(metrics["profit_factor"]) else round(metrics["profit_factor"], 4),
        "total_r": round(metrics["total_r"], 4),
        "average_r": round(metrics["average_r"], 4),
        "max_win_r": round(metrics["max_win_r"], 4),
        "max_loss_r": round(metrics["max_loss_r"], 4),
        "best_asset": best_asset,
        "worst_asset": worst_asset,
        "best_rank": best_rank,
        "worst_rank": worst_rank,
        "best_side": best_side,
        "worst_side": worst_side,
        "next_month_mode": mode,
        "max_daily_risk_pct": risk,
        "weight_change_summary": summary,
        "rule_change_1": changes[0],
        "rule_change_2": changes[1],
        "rule_change_3": changes[2],
    }
    log = pd.DataFrame([row], columns=LOG_COLUMNS)

    proposed_weight_changes = {
        "asset": asset_table[["asset", "proposed_weight_change", "reason"]].to_dict(orient="records") if not asset_table.empty else [],
        "rank": rank_table[["rank", "proposed_weight_change", "reason"]].to_dict(orient="records") if not rank_table.empty else [],
        "side": side_table[["side", "proposed_weight_change", "reason"]].to_dict(orient="records") if not side_table.empty else [],
    }
    payload = {
        **row,
        "asset_calibration": asset_table.to_dict(orient="records"),
        "rank_calibration": rank_table.to_dict(orient="records"),
        "side_calibration": side_table.to_dict(orient="records"),
        "proposed_weight_changes": proposed_weight_changes,
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"{end.strftime('%Y-%m-%d')}_monthly_calibration.md"
    data_warning = "closed評価が30〜50件以上たまるまでは、変更案を自動適用しません。"
    conclusion = f"翌月モードは「{mode}」、最大日次リスクは {risk}% です。{(' / '.join(mode_notes) + '。') if mode_notes else ''}"
    report = f"""# Tactical Swing OS Monthly Calibration

## 1. 月次結論

{conclusion}

## 2. 月次サマリー

{markdown_table(log)}

## 3. 資産別較正

{markdown_table(asset_table)}

## 4. Rank別較正

{markdown_table(rank_table)}

## 5. Side別較正

{markdown_table(side_table)}

## 6. 翌月の暫定モード

- next_month_mode: {mode}
- max_daily_risk_pct: {risk}

## 7. 重み変更案

{summary}

## 8. 据え置き理由

weights.jsonは初期値のまま据え置きます。今回の出力は提案のみで、自動更新は行いません。

## 9. データ不足の注意

{data_warning}

## 10. MONTHLY_CALIBRATION_LOG CSV

```csv
{log.to_csv(index=False).strip()}
```

## 11. MONTHLY_CALIBRATION_LOG JSON

```json
{json.dumps([payload], ensure_ascii=False, indent=2)}
```
"""
    report_path.write_text(report, encoding="utf-8")
    log.to_csv(RESULTS_DIR / "monthly_calibration.csv", index=False)
    (RESULTS_DIR / "monthly_calibration.json").write_text(json.dumps([payload], ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"monthly calibration generated: {report_path}")
    print(f"market snapshot rows in period: {len(market_snapshot)}")
    print(f"weights reference: {WEIGHTS_PATH}")
    return log, str(report_path)


def main() -> int:
    args = parse_args()
    if args.start and args.end:
        start = pd.Timestamp(args.start)
        end = pd.Timestamp(args.end)
    else:
        start, end = default_period()
    if start > end:
        raise ValueError("--start must be before or equal to --end")
    build_monthly_calibration(start, end)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
