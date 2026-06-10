from __future__ import annotations

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


def main() -> int:
    signals = read_csv(RESULTS_DIR / "signals.csv")
    evaluations = read_csv(RESULTS_DIR / "evaluations.csv")

    status = "PASS"
    reasons: list[str] = []

    signal_dups = 0
    eval_dups = 0
    reason_count: int | str = "N/A"

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

    if not evaluations.empty:
        reason_col = next((col for col in ["reason_code", "trigger_name"] if col in evaluations.columns), None)
        if reason_col:
            values = evaluations[reason_col].dropna().astype(str).str.strip()
            values = values[values != ""]
            reason_count = int(values.nunique())
            if reason_count > 20:
                status = "WARNING"
                reasons.append(f"reason_code count exceeds 20: {reason_count}")

    if not reasons:
        reasons.append("No data integrity anomalies detected.")

    today = datetime.utcnow().strftime("%Y-%m-%d")
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    status_label = "✅ PASS" if status == "PASS" else "⚠️ WARNING"
    reason_lines = "\n".join(f"- {reason}" for reason in reasons)

    report = f"""# Tactical Swing OS Audit Report v0.1

**Date:** {today}

## Data Integrity Score

**Status:** {status_label}

## Reasons

{reason_lines}

## Metrics

| item | value |
|---|---:|
| SIGNALS duplicate signal_id | {signal_dups} |
| EVALUATIONS duplicate signal_id | {eval_dups} |
| Unique reason codes | {reason_count} |
"""

    (REPORTS_DIR / f"{today}_audit_report.md").write_text(report, encoding="utf-8")
    (RESULTS_DIR / "latest_audit_status.txt").write_text(status, encoding="utf-8")

    print(f"audit report generated: {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
