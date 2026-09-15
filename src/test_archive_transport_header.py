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
