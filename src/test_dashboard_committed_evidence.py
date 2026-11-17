"""週次レビューと月次較正の層を、コミットされている記録で確かめる（2026-11-17）。

dashboard の job は results/weekly_review.csv・reports/weekly/*.md・results/monthly_calibration.csv・
reports/monthly/*.md を見ていたが、どれも git 管理外でその job には無い。2つの層は 2026-09 から毎日
missing と出続け、Data Health はずっと critical だった（11/3〜11/9 に取込が本当に止まったときも、色は変わらなかった）。"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

import dashboard_io as dio
import dashboard_summaries as ds

HEADER = "week_start,week_end,total_signals\n"


def test_weekly_evidence_is_the_last_week_end_of_the_committed_log(tmp_path):
    log = tmp_path / "weekly_review_log.csv"
    log.write_text(HEADER + "2026-11-01,2026-11-07,20\n2026-11-08,2026-11-14,70\n2026-10-25,2026-10-31,60\n", encoding="utf-8")
    assert dio.committed_weekly_review(log) == (3, "2026-11-14")


def test_weekly_evidence_is_absent_when_the_log_is_missing_empty_or_has_no_week_end(tmp_path):
    assert dio.committed_weekly_review(tmp_path / "nope.csv") == (0, "")
    empty = tmp_path / "empty.csv"
    empty.write_text(HEADER, encoding="utf-8")
    assert dio.committed_weekly_review(empty) == (0, "")
    other = tmp_path / "other.csv"
    other.write_text("week,orders\n2026-11-08,3\n", encoding="utf-8")
    assert dio.committed_weekly_review(other) == (0, "")
    broken = tmp_path / "broken.csv"
    broken.write_text(HEADER + "2026-11-08,not-a-date,1\n", encoding="utf-8")
    assert dio.committed_weekly_review(broken) == (0, "")


def test_monthly_evidence_is_the_last_day_of_the_latest_covered_month(tmp_path, monkeypatch):
    docs = tmp_path / "docs"
    docs.mkdir()
    for name in ("monthly_calibration_2026-08.md", "monthly_calibration_2026-10.md", "monthly_calibration.md",
                 "monthly_calibration_2026-11.draft.md", "monthly_calibration_2026-13.md"):
        (docs / name).write_text("x", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    # 月の無い文書・下書き・ありえない月は数えない
    assert dio.committed_monthly_calibration() == (2, "2026-10-31")
    (docs / "monthly_calibration_2028-02.md").write_text("x", encoding="utf-8")
    assert dio.committed_monthly_calibration() == (3, "2028-02-29")


def test_monthly_evidence_is_absent_without_documents(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert dio.committed_monthly_calibration() == (0, "")


def test_job_outputs_win_and_committed_records_are_the_fallback():
    assert dio.review_evidence(0, "", (11, "2026-11-14")) == (11, "2026-11-14")
    assert dio.review_evidence(4, "2026-11-21", (11, "2026-11-14")) == (4, "2026-11-21")
    assert dio.review_evidence(0, "2026-11-21", (11, "2026-11-14")) == (0, "2026-11-21")     # 片方でもあれば job の側
    assert dio.review_evidence(0, "", (0, "")) == (0, "")


def _layer(label):
    return [spec for spec in ds.LAYER_HEALTH_REGISTRY if spec["label"] == label][0]


def test_weekly_layer_is_fresh_within_a_week_and_stale_when_a_week_is_skipped():
    spec = _layer("weekly_review")
    now = pd.Timestamp("2026-11-17 04:26:00")
    assert ds.assess_layer("weekly_review", "2026-11-14", 11, now, spec["threshold_hours"])["status"] == "fresh"
    # 次の土曜の job が動く前（11/21 13時台 JST）はまだ fresh
    assert ds.assess_layer("weekly_review", "2026-11-14", 11, pd.Timestamp("2026-11-21 04:26:00"), spec["threshold_hours"])["status"] == "fresh"
    # 1週飛ぶと stale
    assert ds.assess_layer("weekly_review", "2026-11-14", 11, pd.Timestamp("2026-11-23 04:26:00"), spec["threshold_hours"])["status"] == "stale"
    # 記録が無ければ従来どおり missing
    assert ds.assess_layer("weekly_review", "", 0, now, spec["threshold_hours"])["status"] == "missing"


def test_monthly_layer_goes_stale_when_next_months_document_does_not_arrive():
    spec = _layer("monthly_calibration")
    hours = spec["threshold_hours"]
    assert ds.assess_layer("monthly_calibration", "2026-10-31", 3, pd.Timestamp("2026-11-17 04:26:00"), hours)["status"] == "fresh"
    assert ds.assess_layer("monthly_calibration", "2026-10-31", 3, pd.Timestamp("2026-12-03 04:26:00"), hours)["status"] == "fresh"
    assert ds.assess_layer("monthly_calibration", "2026-10-31", 3, pd.Timestamp("2026-12-06 04:26:00"), hours)["status"] == "stale"


def test_the_repository_has_the_committed_records_the_layers_now_read():
    root = Path(__file__).resolve().parents[1]
    rows, last_week = dio.committed_weekly_review(root / "data" / "weekly_review_log.csv")
    assert rows > 0 and last_week >= "2026-11-14"
    assert sorted(p.name for p in root.glob(dio.MONTHLY_CALIBRATION_DOC_GLOB))[-1] >= "monthly_calibration_2026-10.md"
