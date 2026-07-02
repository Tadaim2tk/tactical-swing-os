from __future__ import annotations

"""Dashboard データ入出力と低レベルヘルパー (機能変更なし・build_dashboardから分離)。

Google Sheetsは読み込みのみ。書き込みは一切行わない。Secrets値も出力しない。
"""

import json
import math
import os
from datetime import datetime
from pathlib import Path

import pandas as pd


RESULTS_DIR = Path("results")


REPORTS_DIR = Path("reports/dashboard")


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


def read_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError:
        return ""


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
        "model_state_update_proposals": read_csv(RESULTS_DIR / "model_state_update_proposals.csv"),
        "ai_feedback": read_csv(RESULTS_DIR / "ai_feedback.csv"),
        "news_narrative_scores": read_csv(RESULTS_DIR / "news_narrative_scores.csv"),
        "pending_reevaluations": read_csv(RESULTS_DIR / "pending_reevaluations.csv"),
        "latest_evaluations": read_csv(RESULTS_DIR / "latest_evaluations.csv"),
        "weekly_review_json": read_json(RESULTS_DIR / "weekly_review.json"),
        "monthly_calibration_json": read_json(RESULTS_DIR / "monthly_calibration.json"),
        "reason_code_analysis_json": read_json(RESULTS_DIR / "reason_code_analysis.json"),
        "rule_update_proposals_json": read_json(RESULTS_DIR / "rule_update_proposals.json"),
        "model_state_update_proposals_json": read_json(RESULTS_DIR / "model_state_update_proposals.json"),
        "model_state_update_summary_json": read_json(RESULTS_DIR / "model_state_update_summary.json"),
        "model_state_proposal_audit": read_csv(RESULTS_DIR / "model_state_proposal_audit.csv"),
        "model_state_proposal_audit_json": read_json(RESULTS_DIR / "model_state_proposal_audit.json"),
        "weights_patch_proposal": read_csv(RESULTS_DIR / "weights_patch_proposal.csv"),
        "weights_patch_proposal_json": read_json(RESULTS_DIR / "weights_patch_proposal.json"),
        "weights_patch_summary_json": read_json(RESULTS_DIR / "weights_patch_summary.json"),
        "weights_patch_review": read_csv(RESULTS_DIR / "weights_patch_review.csv"),
        "weights_patch_review_json": read_json(RESULTS_DIR / "weights_patch_review.json"),
        "weights_patch_review_summary_json": read_json(RESULTS_DIR / "weights_patch_review_summary.json"),
        "proposal_adoption_tracking": read_csv(RESULTS_DIR / "proposal_adoption_tracking.csv"),
        "proposal_adoption_tracking_json": read_json(RESULTS_DIR / "proposal_adoption_tracking.json"),
        "proposal_adoption_tracking_summary_json": read_json(RESULTS_DIR / "proposal_adoption_tracking_summary.json"),
        "weight_version_history": read_csv(RESULTS_DIR / "weight_version_history.csv"),
        "weight_version_history_json": read_json(RESULTS_DIR / "weight_version_history.json"),
        "weight_version_history_summary_json": read_json(RESULTS_DIR / "weight_version_history_summary.json"),
        "meta_learning": read_csv(RESULTS_DIR / "meta_learning.csv"),
        "meta_learning_json": read_json(RESULTS_DIR / "meta_learning.json"),
        "meta_learning_summary_json": read_json(RESULTS_DIR / "meta_learning_summary.json"),
        "auto_calibration_candidates": read_csv(RESULTS_DIR / "auto_calibration_candidates.csv"),
        "auto_calibration_candidates_json": read_json(RESULTS_DIR / "auto_calibration_candidates.json"),
        "auto_calibration_candidates_summary_json": read_json(RESULTS_DIR / "auto_calibration_candidates_summary.json"),
        "human_override_analytics": read_csv(RESULTS_DIR / "human_override_analytics.csv"),
        "human_override_analytics_json": read_json(RESULTS_DIR / "human_override_analytics.json"),
        "human_override_analytics_summary_json": read_json(RESULTS_DIR / "human_override_analytics_summary.json"),
        "portfolio_layer": read_csv(RESULTS_DIR / "portfolio_layer.csv"),
        "portfolio_layer_json": read_json(RESULTS_DIR / "portfolio_layer.json"),
        "portfolio_layer_summary_json": read_json(RESULTS_DIR / "portfolio_layer_summary.json"),
        "datetime_audit": read_csv(RESULTS_DIR / "datetime_audit.csv"),
        "datetime_audit_json": read_json(RESULTS_DIR / "datetime_audit.json"),
        "datetime_audit_summary_json": read_json(RESULTS_DIR / "datetime_audit_summary.json"),
        "ai_feedback_json": read_json(RESULTS_DIR / "ai_feedback.json"),
        "news_narrative_scores_json": read_json(RESULTS_DIR / "news_narrative_scores.json"),
        "latest_evaluations_summary_json": read_json(RESULTS_DIR / "latest_evaluations_summary.json"),
        "prediction_calibration": read_csv(RESULTS_DIR / "prediction_calibration.csv"),
        "prediction_calibration_json": read_json(RESULTS_DIR / "prediction_calibration.json"),
        "narrative_reliability": read_csv(RESULTS_DIR / "narrative_reliability.csv"),
        "narrative_reliability_json": read_json(RESULTS_DIR / "narrative_reliability.json"),
        "cost_model_json": read_json(Path("config/cost_model.json")),
        "latest_audit_status": read_text(RESULTS_DIR / "latest_audit_status.txt"),
        "narrative_lookahead_audit": read_csv(RESULTS_DIR / "narrative_lookahead_audit.csv"),
        "narrative_lookahead_audit_summary_json": read_json(RESULTS_DIR / "narrative_lookahead_audit_summary.json"),
        "adversarial_review": read_csv(RESULTS_DIR / "adversarial_review.csv"),
        "adversarial_review_summary_json": read_json(RESULTS_DIR / "adversarial_review_summary.json"),
        "similar_narrative_cases": read_csv(RESULTS_DIR / "similar_narrative_cases.csv"),
        "similar_narrative_summary_json": read_json(RESULTS_DIR / "similar_narrative_summary.json"),
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


def numeric_or(value, default: float = 0.0) -> float:
    number = pd.to_numeric(value, errors="coerce")
    return float(number) if not pd.isna(number) else default


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
