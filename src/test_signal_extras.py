"""tools/record_signal_extras.py のガード（#157 Codex P2 対応を含む）。"""
import subprocess
import sys
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parents[1] / "tools" / "record_signal_extras.py"


def run(args, cwd):
    return subprocess.run([sys.executable, str(TOOL), *args], cwd=cwd,
                          capture_output=True, text=True)


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "expected_r_basis.csv").write_text(
        "date,expected_r_basis,source,recorded_at\n", encoding="utf-8")
    (tmp_path / "data" / "invalidation_checks.csv").write_text(
        "check_date,signal_id,invalidation_fired,source,recorded_at\n", encoding="utf-8")
    return tmp_path


def _rows(repo, name):
    import csv
    return list(csv.DictReader((repo / "data" / name).open(encoding="utf-8")))


def test_contradictory_duplicate_in_one_batch_is_rejected(repo):
    """矛盾する重複を先勝ちで黙って通さない。

    通すと (check_date, signal_id) が矛盾したまま append-only 台帳に入り、
    再実行しても両方「既存」になって通常の手順では直せなくなる。
    """
    r = run(["invalidation", "2026-09-09", "S1=fired,S1=not_fired"], repo)
    assert r.returncode != 0
    assert "矛盾" in r.stdout + r.stderr
    assert _rows(repo, "invalidation_checks.csv") == [], "1行も書かない"


def test_identical_duplicate_in_one_batch_writes_once(repo):
    r = run(["invalidation", "2026-09-09", "S1=fired,S1=fired"], repo)
    assert r.returncode == 0
    assert len(_rows(repo, "invalidation_checks.csv")) == 1


def test_source_is_recorded_and_validated(repo):
    """経路を決め打ちしない。同じプロンプトをターミナル経路でも使うため。"""
    assert run(["basis", "2026-09-09", "two_point", "bogus"], repo).returncode != 0
    assert run(["basis", "2026-09-09", "two_point", "gpt_terminal"], repo).returncode == 0
    assert _rows(repo, "expected_r_basis.csv")[0]["source"] == "gpt_terminal"


def test_source_defaults_to_chatgpt_app(repo):
    run(["basis", "2026-09-09", "subjective"], repo)
    assert _rows(repo, "expected_r_basis.csv")[0]["source"] == "chatgpt_app"


@pytest.mark.parametrize("bad", ["S1=maybe", "S1", "=fired"])
def test_bad_invalidation_syntax_is_rejected(repo, bad):
    assert run(["invalidation", "2026-09-09", bad], repo).returncode != 0
    assert _rows(repo, "invalidation_checks.csv") == []


def test_append_only_across_runs(repo):
    run(["invalidation", "2026-09-09", "S1=not_fired"], repo)
    run(["invalidation", "2026-09-09", "S1=fired"], repo)   # 2回目は無視される
    rows = _rows(repo, "invalidation_checks.csv")
    assert len(rows) == 1 and rows[0]["invalidation_fired"] == "not_fired"
