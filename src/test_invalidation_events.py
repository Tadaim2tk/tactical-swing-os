# -*- coding: utf-8 -*-
"""発動日と「聞いた日」を分けて読む。**架空データだけで試す。**

#162 の再現: 5営業日ぶんをまとめて聞き直して回収した `fired` を、
`check_date` の日に発動したものとして較正に渡さない。
"""
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from invalidation_events import fired_events, load_checks, undated_fired   # noqa: E402

HEAD = ("check_date,signal_id,invalidation_fired,source,recorded_at,"
        "fired_on,retrospective\n")


def _write(tmp_path, rows, corrections=None):
    inval = tmp_path / "invalidation_checks.csv"
    inval.write_text(HEAD + "".join(rows), encoding="utf-8")
    corr = tmp_path / "invalidation_corrections.csv"
    corr.write_text("check_date,signal_id,field,value,reason,recorded_at\n"
                    + "".join(corrections or []), encoding="utf-8")
    return {"inval_path": inval, "corrections_path": corr}


def test_daily_fired_with_known_date_is_used(tmp_path):
    kw = _write(tmp_path, [
        "2026-01-06,20260105_EXAMPLE_BUY,fired,example,2026-01-06T00:00:00Z,2026-01-06,no\n"])
    got = fired_events(**kw)
    assert len(got) == 1 and got[0]["fired_on"] == "2026-01-06"


def test_retrospective_fired_is_excluded(tmp_path):
    """**聞いた日を発動日にしない。** 日付が空なら較正に渡さない。"""
    kw = _write(tmp_path, [
        "2026-01-12,20260105_EXAMPLE_BUY,fired,example,2026-01-12T00:00:00Z,,yes\n"])
    assert fired_events(**kw) == []
    assert len(undated_fired(**kw)) == 1


def test_legacy_row_without_columns_is_excluded(tmp_path):
    """列が無かった時代の行は空＝不明。**不明を「その日に発動」に読み替えない。**"""
    inval = tmp_path / "invalidation_checks.csv"
    inval.write_text("check_date,signal_id,invalidation_fired,source,recorded_at\n"
                     "2026-01-12,20260105_EXAMPLE_BUY,fired,example,2026-01-12T00:00:00Z\n",
                     encoding="utf-8")
    corr = tmp_path / "invalidation_corrections.csv"
    kw = {"inval_path": inval, "corrections_path": corr}
    assert fired_events(**kw) == []
    assert len(undated_fired(**kw)) == 1


def test_not_fired_never_counted(tmp_path):
    kw = _write(tmp_path, [
        "2026-01-06,20260105_EXAMPLE_BUY,not_fired,example,2026-01-06T00:00:00Z,,no\n"])
    assert fired_events(**kw) == [] and undated_fired(**kw) == []


def test_correction_layers_without_overwriting_the_observation(tmp_path):
    """訂正は重ねるだけ。**元の観測値を消さない。**"""
    kw = _write(tmp_path,
                ["2026-01-12,20260105_EXAMPLE_BUY,fired,example,2026-01-12T00:00:00Z,2026-01-12,no\n"],
                ["2026-01-12,20260105_EXAMPLE_BUY,fired_on,,後日回収と判明。発動日は不明,"
                 "2026-01-13T00:00:00Z\n",
                 "2026-01-12,20260105_EXAMPLE_BUY,retrospective,yes,後日回収と判明,"
                 "2026-01-13T00:00:00Z\n"])
    row = load_checks(**kw)[0]
    assert row["fired_on"] == "" and row["retrospective"] == "yes"
    assert row["observed_fired_on"] == "2026-01-12"      # 元の値が残っている
    assert fired_events(**kw) == []


def test_later_correction_wins(tmp_path):
    kw = _write(tmp_path,
                ["2026-01-12,20260105_EXAMPLE_BUY,fired,example,2026-01-12T00:00:00Z,,yes\n"],
                ["2026-01-12,20260105_EXAMPLE_BUY,fired_on,2026-01-07,一次訂正,2026-01-13T00:00:00Z\n",
                 "2026-01-12,20260105_EXAMPLE_BUY,fired_on,2026-01-08,再訂正,2026-01-14T00:00:00Z\n"])
    assert fired_events(**kw)[0]["fired_on"] == "2026-01-08"


def test_unknown_correction_field_is_ignored(tmp_path):
    kw = _write(tmp_path,
                ["2026-01-06,20260105_EXAMPLE_BUY,fired,example,2026-01-06T00:00:00Z,2026-01-06,no\n"],
                ["2026-01-06,20260105_EXAMPLE_BUY,invalidation_fired,not_fired,取り消し,"
                 "2026-01-07T00:00:00Z\n"])
    # 判定そのものを訂正で塗り替えられない（塗り替えたいなら台帳の設計から見直すこと）
    assert load_checks(**kw)[0]["invalidation_fired"] == "fired"


def test_writer_marks_retrospective_rows(tmp_path):
    """書く側: 前回から間が空いていれば fired_on を空にする。"""
    repo = Path(__file__).resolve().parents[1]
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "signal_log.csv").write_text(
        "date,signal_id,side\n2026-01-05,20260105_EXAMPLE_BUY,BUY\n", encoding="utf-8")
    (tmp_path / "data" / "invalidation_checks.csv").write_text(HEAD, encoding="utf-8")
    r = subprocess.run([sys.executable, str(repo / "tools" / "record_signal_extras.py"),
                        "invalidation", "2026-01-12", "20260105_EXAMPLE_BUY=fired"],
                       cwd=tmp_path, capture_output=True, text=True)
    body = (tmp_path / "data" / "invalidation_checks.csv").read_text(encoding="utf-8")
    assert "fired" in body and r.returncode == 0, r.stderr
    last = body.strip().splitlines()[-1].split(",")
    assert last[5] == "" and last[6] == "yes"          # fired_on 空 / 後日回収


def test_daily_reconfirmation_does_not_create_a_new_firing(tmp_path):
    """**毎日聞いたことは、当日発動した証拠にならない。** 再確認で発動を増やさない。"""
    kw = _write(tmp_path, [
        "2026-01-06,20260105_EXAMPLE_BUY,fired,example,2026-01-06T00:00:00Z,2026-01-06,no\n",
        "2026-01-07,20260105_EXAMPLE_BUY,fired,example,2026-01-07T00:00:00Z,2026-01-06,no\n",
        "2026-01-08,20260105_EXAMPLE_BUY,fired,example,2026-01-08T00:00:00Z,2026-01-06,no\n"])
    got = fired_events(**kw)
    assert len(got) == 1
    assert got[0]["fired_on"] == "2026-01-06" and got[0]["check_date"] == "2026-01-06"


def test_writer_does_not_invent_a_firing_date(tmp_path):
    """日次で聞いても、回答に発動日が無ければ fired_on は空のまま。"""
    repo = Path(__file__).resolve().parents[1]
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "signal_log.csv").write_text(
        "date,signal_id,side\n2026-01-05,20260105_EXAMPLE_BUY,BUY\n", encoding="utf-8")
    (tmp_path / "data" / "invalidation_checks.csv").write_text(HEAD, encoding="utf-8")
    tool = str(repo / "tools" / "record_signal_extras.py")
    for day in ("2026-01-06", "2026-01-07"):
        r = subprocess.run([sys.executable, tool, "invalidation", day,
                            "20260105_EXAMPLE_BUY=fired"], cwd=tmp_path,
                           capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
    body = (tmp_path / "data" / "invalidation_checks.csv").read_text(encoding="utf-8")
    for line in body.strip().splitlines()[1:]:
        cols = line.split(",")
        assert cols[5] == "", "翌日の再確認に新しい発動日が付いた: " + line
    kw = {"inval_path": tmp_path / "data" / "invalidation_checks.csv",
          "corrections_path": tmp_path / "data" / "nonexistent.csv"}
    assert fired_events(**kw) == []
    assert len(undated_fired(**kw)) == 1          # 判断ごとに1件


def test_writer_accepts_an_explicit_firing_date(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "signal_log.csv").write_text(
        "date,signal_id,side\n2026-01-05,20260105_EXAMPLE_BUY,BUY\n", encoding="utf-8")
    (tmp_path / "data" / "invalidation_checks.csv").write_text(HEAD, encoding="utf-8")
    tool = str(repo / "tools" / "record_signal_extras.py")
    r = subprocess.run([sys.executable, tool, "invalidation", "2026-01-12",
                        "20260105_EXAMPLE_BUY=fired@2026-01-07"], cwd=tmp_path,
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    cols = (tmp_path / "data" / "invalidation_checks.csv").read_text(
        encoding="utf-8").strip().splitlines()[-1].split(",")
    assert cols[5] == "2026-01-07" and cols[6] == "yes"


def test_writer_rejects_impossible_or_conflicting_firing_dates(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "signal_log.csv").write_text(
        "date,signal_id,side\n2026-01-05,20260105_EXAMPLE_BUY,BUY\n", encoding="utf-8")
    (tmp_path / "data" / "invalidation_checks.csv").write_text(
        HEAD + "2026-01-08,20260105_EXAMPLE_BUY,fired,example,"
               "2026-01-08T00:00:00Z,2026-01-07,no\n", encoding="utf-8")
    tool = str(repo / "tools" / "record_signal_extras.py")
    for arg in ("20260105_EXAMPLE_BUY=fired@2026-01-20",      # 確認日より後
                "20260105_EXAMPLE_BUY=fired@2026-01-01",      # 判断が出る前
                "20260105_EXAMPLE_BUY=fired@2026-01-09",      # 既存の発動日と食い違う
                "20260105_EXAMPLE_BUY=not_fired@2026-01-07"):  # fired 以外に付けた
        r = subprocess.run([sys.executable, tool, "invalidation", "2026-01-12", arg],
                           cwd=tmp_path, capture_output=True, text=True)
        assert r.returncode != 0, "通ってしまった: " + arg
