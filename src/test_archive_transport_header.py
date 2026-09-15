"""tools/archive_gpt_prose.py のヘッダは実際の取得経路を言う（#170 Codex P2）。

経路をモードで決め打ちしていたため、会話APIから取った本文にも
「DOM innerText -> Blob download」と書いていた。DOMの innerText と raw markdown
では ```csv フェンスや ** の有無が違い、同じ本文でも抽出の意味が変わる。
"""
import json
import subprocess
import sys
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "tools" / "archive_gpt_prose.py"


def run(args, cwd):
    return subprocess.run([sys.executable, str(TOOL), *args], cwd=cwd, capture_output=True, text=True)


def _header(repo, day):
    return (repo / "data" / "prediction_log_archive" / f"{day}_tso-daily-signal-log.md").read_text(encoding="utf-8").splitlines()[1]


def test_blob_mode_says_dom(tmp_path):
    body = "TSO Daily Signal Log v2 — 2026-08-01\nx\n"
    src = tmp_path / "b.txt"
    src.write_text(f"===== TSO_DAILY 2026-08-01 ({len(body.rstrip(chr(10)))} chars) =====\n{body}", encoding="utf-8")
    assert run([str(src), "--apply"], tmp_path).returncode == 0
    assert "DOM innerText -> Blob download" in _header(tmp_path, "2026-08-01")


def test_export_mode_says_conversation_json(tmp_path):
    conv = [{"title": "TSO(日次)", "mapping": {"n1": {"message": {"author": {"role": "assistant"},
             "content": {"parts": ["TSO Daily Signal Log v2 — 2026-08-02\nbody"]}}}}}]
    src = tmp_path / "c.json"; src.write_text(json.dumps(conv), encoding="utf-8")
    assert run([str(src), "--from-chatgpt-export", "--title", "TSO", "--apply"], tmp_path).returncode == 0
    h = _header(tmp_path, "2026-08-02")
    assert "conversation JSON" in h and "DOM innerText" not in h


def test_explicit_transport_overrides(tmp_path):
    body = "TSO Daily Signal Log v2 — 2026-08-03\nx\n"
    src = tmp_path / "b.txt"
    src.write_text(f"===== TSO_DAILY 2026-08-03 ({len(body.rstrip(chr(10)))} chars) =====\n{body}", encoding="utf-8")
    r = run([str(src), "--apply", "--transport", "/backend-api/conversation -> Blob file"], tmp_path)
    assert r.returncode == 0
    assert "/backend-api/conversation -> Blob file" in _header(tmp_path, "2026-08-03")


# --- detect_day: 前置きの後に来る実行日を拾う（#171 Codex P2） ---
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("archive_gpt_prose", TOOL)
_mod = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_mod)


def test_detect_day_finds_run_date_after_a_long_preamble():
    """7/27 の形: 300字超の前置き → 「**実行日：2026年7月27日**」。台帳には10行あるのに落ちていた。"""
    text = "タスクのプロンプトを修正しました。" * 30 + "\n# TSO Daily Signal Log v2\n**実行日：2026年7月27日**\n本文"
    assert len(text.split("\n")[0]) > 300
    assert _mod.detect_day(text) == "2026-07-27"


def test_detect_day_does_not_take_a_body_date_when_header_is_absent():
    """見出し語彙が無ければ本文中の日付で決めない。「7月28日の終値」は実行日ではない。"""
    text = "前置き。" * 60 + "\n利用価格は主に7月28日の米国市場終値です。\n"
    assert _mod.detect_day(text) is None


def test_detect_day_prefers_the_head_when_present():
    """先頭300字に日付があれば従来どおりそれを使う（後方の実行日より優先）。"""
    text = "# TSO Daily Signal Log v2 — 2026年7月28日\n利用価格は主に7月27日の終値。\n実行日：2026年7月27日\n"
    assert _mod.detect_day(text) == "2026-07-28"
