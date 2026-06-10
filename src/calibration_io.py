from __future__ import annotations

"""月次較正の入力IO層 (Google Sheets / ローカルCSV)。

build_monthly_calibration.py から抽出(SPEC-RD-001適用時のモジュール分割)。
挙動は分割前と同一。
"""

import json
import os
from pathlib import Path

import pandas as pd


RESULTS_DIR = Path("results")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_MAPPINGS = {
    "market_snapshot": ("MARKET_SNAPSHOT", RESULTS_DIR / "market_snapshot.csv"),
    "signals": ("SIGNALS", RESULTS_DIR / "signals.csv"),
    "evaluations": ("EVALUATIONS", RESULTS_DIR / "evaluations.csv"),
}


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
