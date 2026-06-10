from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/audit")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    out.columns = [str(col).strip().lower().replace("-", "_") for col in out.columns]
    return out


def unique_reason_count(signals: pd.DataFrame) -> int | str:
    """Count reason-code vocabulary from signal-time locked labels.

    Evaluations intentionally do not own reason labels. The locked labels live in
    results/signals.csv as reason_codes / no_trade_reason.
    """
    if signals.empty:
        return "N/A"

    values: list[str] = []
    if "reason_codes" in signals.columns:
        for raw in signals["reason_codes"].dropna().astype(str):
            for code in raw.replace(",", "|").split("|"):
                code = code.strip()
                if code:
                    values.append(code)

    if "no_trade_reason" in signals.columns:
        for code in signals["no_trade_reason"].dropna().astype(str).str.strip():
            if code:
                values.append(code)

    if not values:
        return "N/A"
    return len(set(values))


def status_counts(df: pd.DataFrame) -> dict[str, int]:
    if df.empty or "evaluation_status" not in df.columns:
        return {}
    series = df["evaluation_status"].fillna("").astype(str).str.strip().str.lower()
    return {key: int((series == key).sum()) for key in sorted(series.unique()) if key}


def main() -> int:
    signals = normalize_columns(read_csv(RESULTS_DIR / "signals.csv"))
    evaluations = normalize_columns(read_csv(RESULTS_DIR / "evaluations.csv"))
    latest = normalize_columns(read_csv(RESULTS_DIR / "latest_evaluations.csv"))
    pending = normalize_columns(read_csv(RESULTS_DIR / "pending_reevaluations.csv"))
    latest_summary = read_json(RESULTS_DIR / "latest_evaluations_summary.json")

    status = "PASS"
    reasons: list[str] = []

    signal_dups = 0
    eval_dups = 0
    latest_dups = 0
    reason_count = unique_reason_count(signals)

    if not signals.empty and "signal_id" in signals.columns:
        signal_dups = int(signals["signal_id"].duplicated().sum())
        if signal_dups > 0:
            status = "WARNING"
            reasons.append(f"SIGNALS duplicate signal_id: {signal_dups}")

    if not evaluations.empty and "signal_id" in evaluations.columns:
        eval_dups = int(evaluations["signal_id"].duplicated().sum())
        if eval_dups > 0:
            status = "WARNING"
            reasons.append(f"EVALUATIONS duplicate signal_id: {eval_dups}")

    if not latest.empty and "signal_id" in latest.columns:
        latest_dups = int(latest["signal_id"].duplicated().sum())
        if latest_dups > 0:
            status = "WARNING"
            reasons.append(f"LATEST_EVALUATIONS duplicate signal_id: {latest_dups}")

    if isinstance(reason_count, int) and reason_count > 20:
        status = "WARNING"
        reasons.append(f"reason_code count exceeds 20: {reason_count}")

    if not reasons:
        reasons.append("No data integrity anomalies detected.")

    today = datetime.utcnow().strftime("%Y-%m-%d")
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    status_label = "✅ PASS" if status == "PASS" else "⚠️ WARNING"
    reason_lines = "\n".join(f"- {reason}" for reason in reasons)

    eval_status_counts = status_counts(evaluations)
    latest_status_counts = status_counts(latest)
    eval_status_text = ", ".join(f"{k}: {v}" for k, v in eval_status_counts.items()) or "N/A"
    latest_status_text = ", ".join(f"{k}: {v}" for k, v in latest_status_counts.items()) or "N/A"

    report = f"""# Tactical Swing OS Audit Report v0.1

**Date:** {today}

## Data Integrity Score

**Status:** {status_label}

## Reasons

{reason_lines}

## Input Coverage

| item | value |
|---|---:|
| SIGNALS rows | {len(signals)} |
| EVALUATIONS rows | {len(evaluations)} |
| PENDING_REEVALUATIONS rows | {len(pending)} |
| LATEST_EVALUATIONS rows | {len(latest)} |
| latest summary input rows | {latest_summary.get('total_input_rows', 'N/A')} |
| latest summary unique signals | {latest_summary.get('unique_signal_count', 'N/A')} |

## Duplicate Metrics

| item | value |
|---|---:|
| SIGNALS duplicate signal_id | {signal_dups} |
| EVALUATIONS duplicate signal_id | {eval_dups} |
| LATEST_EVALUATIONS duplicate signal_id | {latest_dups} |

## Label Metrics

| item | value |
|---|---:|
| Unique reason codes from SIGNALS | {reason_count} |

## Status Metrics

| item | value |
|---|---|
| EVALUATIONS evaluation_status counts | {eval_status_text} |
| LATEST_EVALUATIONS evaluation_status counts | {latest_status_text} |
"""

    (REPORTS_DIR / f"{today}_audit_report.md").write_text(report, encoding="utf-8")
    (RESULTS_DIR / "latest_audit_status.txt").write_text(status, encoding="utf-8")

    print(f"audit report generated: {status}")
    print(f"audit rows: signals={len(signals)} evaluations={len(evaluations)} pending={len(pending)} latest={len(latest)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
