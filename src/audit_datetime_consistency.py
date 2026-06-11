from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pandas as pd

from time_utils import format_jst, format_utc, now_utc


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/system")
TARGET_FILES = [
    Path("src/build_weekly_review.py"),
    Path("src/build_monthly_calibration.py"),
    Path("src/build_ai_feedback.py"),
    Path("src/measure_proposal_impact.py"),
    Path("src/build_meta_learning.py"),
    Path("src/build_dashboard.py"),
    Path("src/evaluation_loader.py"),
]
AUDIT_COLUMNS = [
    "generated_at_jst",
    "file",
    "line",
    "issue_type",
    "severity",
    "pattern",
    "snippet",
    "recommended_action",
]
ISSUE_PATTERNS = [
    {
        "issue_type": "timestamp_mismatch",
        "severity": "warning",
        "regex": re.compile(r"\.dt\.date\s*[<>=!]=?|[<>=!]=?\s*(?:start|end|cutoff|today|current)[^#\n]*\.date\(\)"),
        "pattern": "date_vs_timestamp_comparison",
        "recommended_action": "normalize_to_timestamp",
    },
    {
        "issue_type": "naive_datetime",
        "severity": "warning",
        "regex": re.compile(r"\bdatetime\.now\(\)|\bdatetime\.today\(\)|\bpd\.Timestamp\(\s*datetime\.now\(\)\.date\(\)\s*\)"),
        "pattern": "timezone_naive_now",
        "recommended_action": "use_time_utils_now_utc_or_now_jst",
    },
    {
        "issue_type": "timezone_mismatch",
        "severity": "info",
        "regex": re.compile(r"\.dt\.tz_localize\(None\)|\.tz_localize\(None\)"),
        "pattern": "timezone_removed",
        "recommended_action": "document_timezone_boundary_or_keep_utc",
    },
    {
        "issue_type": "timezone_mismatch",
        "severity": "info",
        "regex": re.compile(r'utc=True|ZoneInfo\("Asia/Tokyo"\)|ZoneInfo\("UTC"\)|\bJST\b|\bUTC\b'),
        "pattern": "timezone_explicit_usage",
        "recommended_action": "verify_consistent_jst_utc_labeling",
    },
    {
        "issue_type": "string_date",
        "severity": "info",
        "regex": re.compile(r"strftime\(|strptime\(|pd\.to_datetime\("),
        "pattern": "string_date_conversion",
        "recommended_action": "use_errors_coerce_and_normalize",
    },
]


def scan_file(path: Path, generated_at_jst: str) -> list[dict[str, Any]]:
    if not path.exists():
        return [
            {
                "generated_at_jst": generated_at_jst,
                "file": str(path),
                "line": 0,
                "issue_type": "missing_target",
                "severity": "info",
                "pattern": "target_file_missing",
                "snippet": "",
                "recommended_action": "skip_until_phase_is_available",
            }
        ]
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        for rule in ISSUE_PATTERNS:
            if rule["regex"].search(stripped):
                rows.append(
                    {
                        "generated_at_jst": generated_at_jst,
                        "file": str(path),
                        "line": line_no,
                        "issue_type": rule["issue_type"],
                        "severity": rule["severity"],
                        "pattern": rule["pattern"],
                        "snippet": stripped[:240],
                        "recommended_action": rule["recommended_action"],
                    }
                )
    return rows


def run_audit(targets: list[Path] | None = None, generated_at_jst: str | None = None) -> pd.DataFrame:
    generated_at_jst = generated_at_jst or format_jst()
    rows: list[dict[str, Any]] = []
    for path in targets or TARGET_FILES:
        rows.extend(scan_file(path, generated_at_jst))
    return pd.DataFrame(rows, columns=AUDIT_COLUMNS)


def summary_from(audit: pd.DataFrame, generated_at_jst: str, generated_at_utc: str) -> dict[str, Any]:
    if audit.empty:
        counts = pd.Series(dtype=int)
        severities = pd.Series(dtype=int)
    else:
        counts = audit["issue_type"].value_counts()
        severities = audit["severity"].value_counts()
    warning_count = int(severities.get("warning", 0))
    timestamp_mismatch = int(counts.get("timestamp_mismatch", 0))
    naive_datetime = int(counts.get("naive_datetime", 0))
    timezone_mismatch = int(counts.get("timezone_mismatch", 0))
    recommended_action = "normalize_to_timestamp" if timestamp_mismatch else "use_time_utils_now_utc_or_now_jst" if naive_datetime else "monitor"
    return {
        "generated_at_jst": generated_at_jst,
        "generated_at_utc": generated_at_utc,
        "audit_status": "warning" if warning_count else "passed",
        "issues_found": int(len(audit)),
        "warning_count": warning_count,
        "info_count": int(severities.get("info", 0)),
        "timezone_mismatch": timezone_mismatch,
        "naive_datetime": naive_datetime,
        "timestamp_mismatch": timestamp_mismatch,
        "string_date_count": int(counts.get("string_date", 0)),
        "missing_target_count": int(counts.get("missing_target", 0)),
        "recommended_action": recommended_action,
        "weights_json_updated": False,
        "patch_applied": False,
        "requires_human_approval": True,
    }


def markdown_table(df: pd.DataFrame, empty: str = "該当なし") -> str:
    if df.empty:
        return empty
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        values = [str(row.get(col, "")).replace("\n", " ").replace("|", "/") for col in df.columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def render_markdown(summary: dict[str, Any], audit: pd.DataFrame) -> str:
    warning_rows = audit[audit["severity"] == "warning"] if not audit.empty else pd.DataFrame()
    info_rows = audit[audit["severity"] == "info"] if not audit.empty else pd.DataFrame()
    cols = ["file", "line", "issue_type", "severity", "pattern", "recommended_action", "snippet"]
    return f"""# Datetime Consistency Audit

## 1. 概要

- 生成日時JST: {summary["generated_at_jst"]}
- audit_status: {summary["audit_status"]}
- issues_found: {summary["issues_found"]}
- timezone_mismatch: {summary["timezone_mismatch"]}
- naive_datetime: {summary["naive_datetime"]}
- timestamp_mismatch: {summary["timestamp_mismatch"]}
- string_date_count: {summary["string_date_count"]}
- missing_target_count: {summary["missing_target_count"]}
- recommended_action: {summary["recommended_action"]}

## 2. Warning

{markdown_table(warning_rows[cols] if not warning_rows.empty else warning_rows)}

## 3. Info

{markdown_table(info_rows[cols] if not info_rows.empty else info_rows)}

## 4. 注意事項

- この監査は日付型・時刻型・timezone境界の不安定要素を検出するための品質確認です
- 実売買・発注・XM操作は行いません
- weights.jsonは更新しません
- patchは適用しません
- Google Sheetsへの書き込みは行いません
"""


def build_datetime_audit() -> tuple[pd.DataFrame, dict[str, Any], str]:
    generated_dt_utc = now_utc()
    generated_at_jst = format_jst(generated_dt_utc)
    generated_at_utc = format_utc(generated_dt_utc)
    audit = run_audit(generated_at_jst=generated_at_jst)
    summary = summary_from(audit, generated_at_jst, generated_at_utc)
    payload = {
        **summary,
        "targets": [str(path) for path in TARGET_FILES],
        "safety": {
            "weights_json_updated": False,
            "patch_applied": False,
            "requires_human_approval": True,
            "apply_automatically": False,
        },
        "issues": audit.to_dict(orient="records"),
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_date = generated_at_jst[:10]
    csv_path = RESULTS_DIR / "datetime_audit.csv"
    json_path = RESULTS_DIR / "datetime_audit.json"
    summary_path = RESULTS_DIR / "datetime_audit_summary.json"
    report_path = REPORTS_DIR / f"{report_date}_datetime_audit.md"
    audit.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    report_path.write_text(render_markdown(summary, audit), encoding="utf-8")
    print(f"datetime audit generated: {report_path}")
    print(f"datetime audit status: {summary['audit_status']}")
    return audit, summary, str(report_path)


def main() -> int:
    build_datetime_audit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
