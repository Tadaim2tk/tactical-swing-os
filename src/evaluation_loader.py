from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd


RESULTS_DIR = Path("results")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


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


def metadata(source: str, rows: int, latest_available: bool, fallback_used: bool) -> dict:
    return {
        "evaluation_source": source,
        "evaluation_rows": int(rows),
        "latest_evaluations_available": bool(latest_available),
        "fallback_used": bool(fallback_used),
    }


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


def load_sheets_evaluations() -> pd.DataFrame:
    try:
        client = get_sheets_client()
        if client is None:
            return pd.DataFrame()
        spreadsheet = client.open_by_key(os.environ["GOOGLE_SHEET_ID"])
        df = worksheet_to_dataframe(spreadsheet.worksheet("EVALUATIONS"))
        print(f"ok: loaded {len(df)} rows from Google Sheets EVALUATIONS for evaluation fallback")
        return df
    except Exception as exc:  # noqa: BLE001 - fallback metadata captures missing sheets.
        print(f"warning: Google Sheets EVALUATIONS fallback unavailable: {exc}")
        return pd.DataFrame()


def load_evaluations_prefer_latest(local_only: bool = False) -> tuple[pd.DataFrame, dict]:
    latest = read_csv(RESULTS_DIR / "latest_evaluations.csv")
    if not latest.empty:
        return latest, metadata("latest_evaluations", len(latest), True, False)

    pending = read_csv(RESULTS_DIR / "pending_reevaluations.csv")
    if not pending.empty:
        return pending, metadata("pending_reevaluations", len(pending), False, True)

    evaluations = read_csv(RESULTS_DIR / "evaluations.csv")
    if not evaluations.empty:
        return evaluations, metadata("evaluations", len(evaluations), False, True)

    if not local_only:
        sheets = load_sheets_evaluations()
        if not sheets.empty:
            return sheets, metadata("sheets_evaluations", len(sheets), False, True)

    return pd.DataFrame(), metadata("none", 0, False, True)
