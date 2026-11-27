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


def test_sections_are_the_six_named_in_the_document():
    assert list(_mod().SECTIONS) == ["geometry", "flips", "direction", "rows", "chase", "weekend"]


def test_stops_without_prices_instead_of_printing_empty_tables(tmp_path, monkeypatch, capsys):
    (tmp_path / "data" / "raw").mkdir(parents=True)
    for name in ("signal_log.csv", "execution_simulation.csv"):
        shutil.copy(ROOT / "data" / name, tmp_path / "data" / name)
    monkeypatch.chdir(tmp_path)
    assert _mod().main([]) == 1
    assert "価格が無い" in capsys.readouterr().out
