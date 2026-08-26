"""コミット済み台帳ファイルそのものの不変条件テスト。

既存テストは全てコードを検証し、コミット済みの台帳ファイルを1件も見ていなかった。
これが 2026-08-25 の事故2種(列和集合の自己増殖 close_btc/close_BTC・#117 ブランチ内
再生成による MCTX-20260825T144243Z の行消失)を素通りさせた穴。governance の
「append-only」を規律から機構にする。

- ヘッダは SNAPSHOT_COLUMNS と完全一致(列の schema enforcement)
- HEAD~ に存在した snapshot_id は全部残っている(行の append-only)
- 既存行の値は変わっていない(不変性)

注: HEAD~ 比較は git 履歴が必要。fetch-depth=1 の CI checkout では skip される
(ローカル実行と PR 前の手元 pytest が防衛線。CI でも効かせるには対象 workflow の
checkout に fetch-depth: 2 を足す)。親コミットのヘッダが契約と不一致の場合は
移行境界として免除する(スキーマ移行コミット自体を弾かないため)。
"""
from __future__ import annotations

import io
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent))
from export_market_context_snapshot import SNAPSHOT_COLUMNS  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
LEDGER = REPO_ROOT / "data" / "market_context_daily.csv"


def _parent_ledger_text() -> str | None:
    try:
        out = subprocess.run(
            ["git", "show", "HEAD~:data/market_context_daily.csv"],
            capture_output=True, text=True, cwd=REPO_ROOT, timeout=30,
        )
    except Exception:  # noqa: BLE001 - git 不在等は「比較不能」として扱う
        return None
    if out.returncode != 0:
        return None
    return out.stdout


def test_snapshot_header_matches_contract():
    if not LEDGER.exists():
        pytest.skip("台帳未作成")
    df = pd.read_csv(LEDGER, dtype=str, keep_default_na=False)
    assert list(df.columns) == list(SNAPSHOT_COLUMNS), (
        "market_context_daily.csv のヘッダが契約と不一致。"
        "列を変えるときは明示的な移行コミットで一致させる"
    )


def test_snapshot_append_only_vs_parent_commit():
    if not LEDGER.exists():
        pytest.skip("台帳未作成")
    prev_text = _parent_ledger_text()
    if prev_text is None or not prev_text.strip():
        pytest.skip("HEAD~ に台帳が無い(浅いcheckout・初回コミット・git不在)")
    prev = pd.read_csv(io.StringIO(prev_text), dtype=str, keep_default_na=False)
    if list(prev.columns) != list(SNAPSHOT_COLUMNS):
        pytest.skip("親コミットはスキーマ移行境界のため免除")
    cur = pd.read_csv(LEDGER, dtype=str, keep_default_na=False)

    prev_ids = list(prev["snapshot_id"])
    cur_ids = set(cur["snapshot_id"])
    missing = [i for i in prev_ids if i not in cur_ids]
    assert not missing, f"append-only違反: 行が消えた {missing}"

    p = prev.set_index("snapshot_id").loc[prev_ids]
    c = cur.set_index("snapshot_id").loc[prev_ids]
    pd.testing.assert_frame_equal(p, c, check_like=True, obj="既存行の値")
