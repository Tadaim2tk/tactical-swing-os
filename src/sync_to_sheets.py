from __future__ import annotations

import json
import os
import re
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


def normalize_column_name(column: str) -> str:
    normalized = str(column).strip().lower()
    normalized = normalized.replace("-", "_")
    normalized = re.sub(r"\s+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized)
    return normalized


def normalized_column_map(columns: list[str]) -> dict[str, str]:
    mapping = {}
    for column in columns:
        normalized = normalize_column_name(column)
        if normalized and normalized not in mapping:
            mapping[normalized] = column
    return mapping


def read_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df.fillna("")


def key_candidates_for(sheet_name: str) -> list[list[str]]:
    if sheet_name == "MARKET_SNAPSHOT":
        return [
            ["date", "asset"],
            ["timestamp", "asset"],
            ["run_ts", "asset"],
            ["run_timestamp", "asset"],
            ["fetched_at", "asset"],
            ["created_at", "asset"],
            ["retrieved_at", "asset"],
        ]
    if sheet_name == "SIGNALS":
        return [
            ["signal_id"],
            ["date", "asset", "side", "type"],
        ]
    if sheet_name == "EVALUATIONS":
        return [
            ["signal_id"],
            ["date", "asset", "side"],
            ["evaluation_date", "asset", "side"],
        ]
    return []


def choose_key_columns(sheet_name: str, csv_columns: list[str], sheet_header: list[str]) -> list[str]:
    csv_map = normalized_column_map(csv_columns)
    sheet_map = normalized_column_map(sheet_header)
    for candidate in key_candidates_for(sheet_name):
        if all(column in csv_map and column in sheet_map for column in candidate):
            return candidate
    return []


def has_valid_header(sheet_name: str, header: list[str]) -> bool:
    header_map = normalized_column_map(header)
    if sheet_name == "MARKET_SNAPSHOT":
        return ("date" in header_map and "asset" in header_map) or ("run_ts" in header_map and "asset" in header_map)
    if sheet_name in {"SIGNALS", "EVALUATIONS"}:
        return "signal_id" in header_map
    return bool(header)


def existing_keys(worksheet, key_columns: list[str]) -> set[tuple[str, ...]]:
    values = worksheet.get_all_values()
    if not values:
        return set()

    header = values[0]
    header_map = normalized_column_map(header)
    indexes = [header.index(header_map[col]) for col in key_columns]
    keys = set()
    for row in values[1:]:
        key = tuple(row[idx] if idx < len(row) else "" for idx in indexes)
        if any(key):
            keys.add(key)
    return keys


def expand_header(
    worksheet,
    csv_columns: list[str],
    sheet_header: list[str],
    sheet_name: str,
) -> list[str]:
    """Return the updated sheet header, appending any new CSV columns to the end.

    Only the header row in the sheet is modified; existing data rows are untouched.
    Returns the new (possibly expanded) header.
    """
    sheet_norm_map = normalized_column_map(sheet_header)
    csv_norm_map = normalized_column_map(csv_columns)

    missing_norms = [n for n in csv_norm_map if n not in sheet_norm_map]
    if not missing_norms:
        print(f"ok: {sheet_name} header already up to date")
        return sheet_header

    # Preserve original CSV column names for the missing columns.
    new_columns = [csv_norm_map[n] for n in missing_norms]
    updated_header = sheet_header + new_columns

    # Overwrite only cell A1:Z1 (extend to however many columns are needed).
    col_count = len(updated_header)
    import gspread.utils as _gsu
    end_col = _gsu.rowcol_to_a1(1, col_count)[:-1]  # strip row digit -> column letter(s)
    worksheet.update(f"A1:{end_col}1", [updated_header], value_input_option="RAW")
    print(f"ok: {sheet_name} added {len(new_columns)} new columns: {new_columns}")
    return updated_header


def ensure_header(worksheet, header: list[str], sheet_name: str) -> list[str]:
    """Ensure the sheet has a valid header and expand it with any new CSV columns.

    Three cases are handled:
    1. Empty sheet  -> write the CSV header as the first row.
    2. Invalid/missing header -> insert CSV header at row 1 (push data down).
    3. Valid header but missing columns -> append new columns to the right.

    Returns the final (possibly expanded) sheet header.
    """
    values = worksheet.get_all_values()

    # Case 1: sheet is empty.
    if not values:
        worksheet.append_row(header, value_input_option="RAW")
        print(f"ok: {sheet_name} header created (new sheet)")
        return header

    # Case 2: header exists but is invalid.
    if not has_valid_header(sheet_name, values[0]):
        worksheet.insert_row(header, index=1, value_input_option="RAW")
        print(f"warning: {sheet_name} header is missing or invalid; inserted CSV header at row 1")
        return header

    # Case 3: valid header – expand with any new CSV columns.
    return expand_header(worksheet, header, values[0], sheet_name)


def current_header(worksheet) -> list[str]:
    values = worksheet.get_all_values()
    if not values:
        return []
    return values[0]


def row_key(record: pd.Series, csv_map: dict[str, str], key_columns: list[str]) -> tuple[str, ...]:
    return tuple(normalize_value(record[csv_map[col]]) for col in key_columns)


def append_csv(spreadsheet, csv_path: Path, sheet_name: str) -> bool:
    if not csv_path.exists():
        print(f"warning: {csv_path} not found; skipped")
        return False

    df = read_csv(csv_path)
    if df.empty:
        print(f"warning: {csv_path} is empty; skipped")
        return False

    worksheet = get_or_create_worksheet(spreadsheet, sheet_name)
    csv_columns = list(df.columns)
    # ensure_header returns the final (possibly expanded) sheet header.
    sheet_header = ensure_header(worksheet, csv_columns, sheet_name)

    key_columns = choose_key_columns(sheet_name, csv_columns, sheet_header)
    csv_map = normalized_column_map(csv_columns)
    sheet_norm_map = normalized_column_map(sheet_header)
    known_keys = existing_keys(worksheet, key_columns) if key_columns else set()
    if key_columns:
        print(f"ok: {sheet_name} using key columns {key_columns}")
    else:
        print(f"warning: {sheet_name} has no usable dedup key columns; appending all rows")

    rows = []
    duplicate_count = 0
    for _, record in df.iterrows():
        key = row_key(record, csv_map, key_columns) if key_columns else tuple()
        if key_columns and key in known_keys:
            duplicate_count += 1
            continue
        # Align row data to the current sheet header order.
        # If a sheet column is not in the CSV, insert an empty string.
        row = []
        for col in sheet_header:
            norm = normalize_column_name(col)
            if norm in csv_map:
                row.append(normalize_value(record[csv_map[norm]]))
            else:
                row.append("")
        rows.append(row)
        if key_columns:
            known_keys.add(key)

    if key_columns:
        print(f"ok: {sheet_name} skipped {duplicate_count} duplicate rows")

    if rows:
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
