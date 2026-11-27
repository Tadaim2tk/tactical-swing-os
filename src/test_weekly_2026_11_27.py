"""一度きりの測定スクリプト tools/analysis/weekly_2026_11_27.py が、読み込めて、入力が無いときに正直に止まること。

数字の再現は実データと価格（git 管理外）が要るので、ここでは確かめない。
"""
from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _mod():
    spec = importlib.util.spec_from_file_location("weekly_2026_11_27", ROOT / "tools" / "analysis" / "weekly_2026_11_27.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_unknown_section_name_is_rejected(capsys):
    assert _mod().main(["nope"]) == 2
    assert "知らない名前" in capsys.readouterr().out


def test_sections_are_the_ones_named_in_the_document():
    # 最初の6つが §3 の切り口。follow と notes は同じ日の夕方の追記（§7）
    assert list(_mod().SECTIONS) == ["geometry", "flips", "direction", "rows", "chase", "weekend", "follow", "notes"]


def test_notes_counts_days_by_wording_in_the_archived_write_ups(tmp_path, monkeypatch, capsys):
    arch = tmp_path / "data" / "prediction_log_archive"
    arch.mkdir(parents=True)
    (arch / "2026-11-01_tso-daily-signal-log.md").write_text("SL距離は暫定値。ATR10 の実測は未完了。\nA級は該当なし\n", encoding="utf-8")
    (arch / "2026-11-02_tso-daily-signal-log.md").write_text("ATR10実測値との比較が未完了のためA級にしない\n", encoding="utf-8")
    (arch / "2026-11-03_tso-daily-signal-log.md").write_text("ATR10 は 120。SL は 1.5 倍。\nA級は条件を満たさず見送り\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    _mod().notes(None, None)
    out = capsys.readouterr().out
    assert "11月で (1) に当たる日: 01 02" in out      # 同じ行に ATR10 と、計算できなかった旨の語
    assert "11月で (2) に当たる日: 02" in out          # A級にしない理由として ATR10 を挙げた行


def test_stops_without_prices_instead_of_printing_empty_tables(tmp_path, monkeypatch, capsys):
    (tmp_path / "data" / "raw").mkdir(parents=True)
    for name in ("signal_log.csv", "execution_simulation.csv"):
        shutil.copy(ROOT / "data" / name, tmp_path / "data" / name)
    monkeypatch.chdir(tmp_path)
    assert _mod().main([]) == 1
    assert "価格が無い" in capsys.readouterr().out
