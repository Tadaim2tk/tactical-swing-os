from __future__ import annotations

from pathlib import Path

import pandas as pd

import audit_datetime_consistency as audit


def write_tmp(tmp_path: Path, name: str, text: str) -> Path:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_normal_file_has_no_warning(tmp_path):
    path = write_tmp(tmp_path, "normal.py", "from time_utils import now_utc\nvalue = now_utc()\n")
    rows = audit.run_audit([path], "2026-06-09 12:00:00 JST")
    summary = audit.summary_from(rows, "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC")
    assert summary["audit_status"] == "passed"
    assert summary["timestamp_mismatch"] == 0
    assert summary["naive_datetime"] == 0


def test_date_vs_timestamp_is_detected(tmp_path):
    path = write_tmp(tmp_path, "date_vs_ts.py", 'mask = df["_d"].dt.date >= start.date()\n')
    rows = audit.run_audit([path], "2026-06-09 12:00:00 JST")
    summary = audit.summary_from(rows, "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC")
    assert summary["audit_status"] == "warning"
    assert summary["timestamp_mismatch"] >= 1
    assert summary["recommended_action"] == "normalize_to_timestamp"


def test_jst_utc_and_timezone_boundaries_are_detected_as_info(tmp_path):
    path = write_tmp(tmp_path, "tz.py", 'x = pd.to_datetime(col, utc=True).dt.tz_localize(None)\nlabel = "JST UTC"\n')
    rows = audit.run_audit([path], "2026-06-09 12:00:00 JST")
    summary = audit.summary_from(rows, "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC")
    assert summary["audit_status"] == "passed"
    assert summary["timezone_mismatch"] >= 1
    assert summary["string_date_count"] >= 1


def test_empty_data_summary_is_consistent():
    rows = pd.DataFrame(columns=audit.AUDIT_COLUMNS)
    summary = audit.summary_from(rows, "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC")
    assert summary["audit_status"] == "passed"
    assert summary["issues_found"] == 0
    assert summary["recommended_action"] == "monitor"


def test_missing_target_is_non_blocking_info(tmp_path):
    missing = tmp_path / "missing.py"
    rows = audit.run_audit([missing], "2026-06-09 12:00:00 JST")
    summary = audit.summary_from(rows, "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC")
    assert summary["audit_status"] == "passed"
    assert summary["missing_target_count"] == 1
    assert rows.iloc[0]["issue_type"] == "missing_target"


def test_summary_counts_match_rows(tmp_path):
    path = write_tmp(
        tmp_path,
        "mixed.py",
        "\n".join(
            [
                "now = datetime.now()",
                'mask = df["_d"].dt.date <= end.date()',
                "x = pd.to_datetime(col, utc=True).dt.tz_localize(None)",
            ]
        ),
    )
    rows = audit.run_audit([path], "2026-06-09 12:00:00 JST")
    summary = audit.summary_from(rows, "2026-06-09 12:00:00 JST", "2026-06-09 03:00:00 UTC")
    assert summary["issues_found"] == len(rows)
    assert summary["naive_datetime"] == 1
    assert summary["timestamp_mismatch"] >= 1
    assert summary["timezone_mismatch"] >= 1
