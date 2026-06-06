from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd


CONFIG_PATH = Path("config/sheets_schema.json")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
FUTURE_SHEETS = ["WEEKLY_REVIEW", "MONTHLY_CALIBRATION", "PARAMETERS"]


def load_schema() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"missing schema: {CONFIG_PATH}")
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def get_client():
    service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not service_account_json or not sheet_id:
        print("Sheets sync skipped: GOOGLE_SERVICE_ACCOUNT_JSON and GOOGLE_SHEET_ID are required")
        return None

    import gspread
    from google.oauth2.service_account import Credentials

    try:
        account_info = json.loads(service_account_json)
    except json.JSONDecodeError as exc:
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON is not valid JSON") from exc

    credentials = Credentials.from_service_account_info(account_info, scopes=SCOPES)
    return gspread.authorize(credentials)


def open_spreadsheet(client):
    sheet_id = os.environ["GOOGLE_SHEET_ID"]
    return client.open_by_key(sheet_id)


def get_or_create_worksheet(spreadsheet, title: str):
    import gspread

    try:
        return spreadsheet.worksheet(title)
    except gspread.WorksheetNotFound:
        return spreadsheet.add_worksheet(title=title, rows=1000, cols=50)


def ensure_future_sheets(spreadsheet) -> None:
    for title in FUTURE_SHEETS:
        get_or_create_worksheet(spreadsheet, title)


def normalize_value(value) -> str:
    if pd.isna(value):
        return ""
    return str(value)


def read_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df.fillna("")


def existing_keys(worksheet, key_columns: list[str]) -> set[tuple[str, ...]]:
    values = worksheet.get_all_values()
    if not values:
        return set()

    header = values[0]
    missing = [col for col in key_columns if col not in header]
    if missing:
        print(f"warning: {worksheet.title} has no key columns {missing}; appending all rows")
        return set()

    indexes = [header.index(col) for col in key_columns]
    keys = set()
    for row in values[1:]:
        key = tuple(row[idx] if idx < len(row) else "" for idx in indexes)
        if any(key):
            keys.add(key)
    return keys


def ensure_header(worksheet, header: list[str]) -> None:
    values = worksheet.get_all_values()
    if values:
        return
    worksheet.append_row(header, value_input_option="RAW")


def key_columns_for(sheet_name: str) -> list[str]:
    if sheet_name == "MARKET_SNAPSHOT":
        return ["date", "asset"]
    if sheet_name in {"SIGNALS", "EVALUATIONS"}:
        return ["signal_id"]
    return []


def append_csv(spreadsheet, csv_path: Path, sheet_name: str) -> bool:
    if not csv_path.exists():
        print(f"warning: {csv_path} not found; skipped")
        return False

    df = read_csv(csv_path)
    if df.empty:
        print(f"warning: {csv_path} is empty; skipped")
        return False

    worksheet = get_or_create_worksheet(spreadsheet, sheet_name)
    header = list(df.columns)
    ensure_header(worksheet, header)

    key_columns = key_columns_for(sheet_name)
    known_keys = existing_keys(worksheet, key_columns) if key_columns else set()

    rows = []
    for _, record in df.iterrows():
        key = tuple(normalize_value(record[col]) for col in key_columns) if key_columns else tuple()
        if key_columns and key in known_keys:
            continue
        rows.append([normalize_value(record[col]) for col in header])

    if not rows:
        print(f"ok: {sheet_name} no new rows")
        return True

    worksheet.append_rows(rows, value_input_option="RAW")
    print(f"ok: {sheet_name} appended {len(rows)} rows")
    return True


def main() -> int:
    client = get_client()
    if client is None:
        return 0

    schema = load_schema()
    mappings = schema.get("mappings", [])
    spreadsheet = open_spreadsheet(client)
    ensure_future_sheets(spreadsheet)

    success_count = 0
    for mapping in mappings:
        csv_path = Path(mapping["csv_path"])
        sheet_name = mapping["sheet_name"]
        try:
            if append_csv(spreadsheet, csv_path, sheet_name):
                success_count += 1
        except Exception as exc:  # noqa: BLE001 - keep other sheet syncs running.
            print(f"error: failed to sync {csv_path} to {sheet_name}: {exc}")

    if success_count == 0:
        print("Sheets sync failed: no CSV was synced")
        return 1

    print(f"Sheets sync completed: {success_count}/{len(mappings)} targets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
