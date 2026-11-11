"""tools/ledger_freshness.py — 取込が止まったら夜間ジョブが気付くこと。

2026-11-03〜11/09 は取込が止まっていたのに daily_cycle は緑だった（売買頻度の監視は台帳の最終日を
基準に数えるので、台帳と一緒に止まる）。ここは「今日」から数える。"""
from __future__ import annotations

import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import ledger_freshness as lf  # noqa: E402

HEADER = "date,signal_id,asset,side,rank,type\n"


def _ledger(tmp_path: Path, dates) -> Path:
    p = tmp_path / "signal_log.csv"
    p.write_text(HEADER + "".join(f"{d},{d.replace('-', '')}_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE\n" for d in dates),
                 encoding="utf-8")
    return p


def test_previous_day_is_normal_at_the_nightly_run():
    # 06:55 JST の時点では、当日の出力（07:00）はまだ無い。前日分まで入っていれば正常。
    r = lf.evaluate(date(2026, 11, 11), date(2026, 11, 12))
    assert r["status"] == "OK" and r["lag_days"] == 1


def test_same_day_and_future_dated_rows_are_ok():
    assert lf.evaluate(date(2026, 11, 12), date(2026, 11, 12))["status"] == "OK"
    assert lf.evaluate(date(2026, 11, 13), date(2026, 11, 12))["status"] == "OK"


def test_one_missed_day_warns_two_missed_days_alert():
    assert lf.evaluate(date(2026, 11, 10), date(2026, 11, 12))["status"] == "WARN"
    r = lf.evaluate(date(2026, 11, 9), date(2026, 11, 12))
    assert r["status"] == "ALERT" and r["lag_days"] == 3 and "2 日ぶん" in r["reason"]


def test_the_october_break_would_have_alerted_on_the_second_missed_morning():
    # 10/28 のレポートから Codex は本文を読めなくなった。10/27 で止まった台帳は 10/30 朝に赤になる。
    assert lf.evaluate(date(2026, 10, 27), date(2026, 10, 29))["status"] == "WARN"
    assert lf.evaluate(date(2026, 10, 27), date(2026, 10, 30))["status"] == "ALERT"


def test_unreadable_or_empty_ledger_alerts(tmp_path):
    assert lf.last_ledger_date(tmp_path / "nope.csv") is None
    empty = tmp_path / "signal_log.csv"
    empty.write_text(HEADER, encoding="utf-8")
    assert lf.last_ledger_date(empty) is None
    r = lf.evaluate(None, date(2026, 11, 12))
    assert r["status"] == "ALERT" and r["lag_days"] is None


def test_last_date_is_the_max_and_ignores_broken_rows(tmp_path):
    p = _ledger(tmp_path, ["2026-11-09", "2026-11-11", "2026-11-10"])
    with p.open("a", encoding="utf-8") as fh:
        fh.write("not-a-date,x\n\n2026-13-45,y\n")
    assert lf.last_ledger_date(p) == date(2026, 11, 11)


def test_today_is_the_jst_calendar_day():
    # 夜間ジョブは 21:55 UTC（= 翌日 06:55 JST）に走る。UTC の日付で数えると1日ずれる。
    assert lf.jst_today(datetime(2026, 11, 11, 21, 55, tzinfo=timezone.utc)) == date(2026, 11, 12)
    assert lf.jst_today(datetime(2026, 11, 11, 14, 59, tzinfo=timezone.utc)) == date(2026, 11, 11)


def test_cli_exit_codes(tmp_path, capsys):
    p = _ledger(tmp_path, ["2026-11-08", "2026-11-09"])
    assert lf.main(["--ledger", str(p), "--today", "2026-11-10", "--fail-on-alert"]) == 0
    assert capsys.readouterr().out.startswith("status=OK last_date=2026-11-09 today=2026-11-10 lag_days=1")
    assert lf.main(["--ledger", str(p), "--today", "2026-11-11", "--fail-on-alert"]) == 0     # WARN は落とさない
    assert capsys.readouterr().out.startswith("status=WARN ")
    assert lf.main(["--ledger", str(p), "--today", "2026-11-12", "--fail-on-alert"]) == 2
    out = capsys.readouterr().out
    assert out.startswith("status=ALERT last_date=2026-11-09 today=2026-11-12 lag_days=3") and "定期タスク" in out
    assert lf.main(["--ledger", str(p), "--today", "2026-11-12"]) == 0                        # 旗が無ければ落とさない
    assert lf.main(["--ledger", str(tmp_path / "missing.csv"), "--today", "2026-11-12", "--fail-on-alert"]) == 2
