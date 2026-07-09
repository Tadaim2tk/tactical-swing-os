"""sync_to_sheets の exit code 規約テスト (2026-07-09 実障害の回帰防止)。

実障害: EVALUATIONS がセル上限(10M)で毎回失敗しても他タブ成功で exit 0
= false green のまま蓄積停止。部分失敗は正直な赤にする。
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sync_to_sheets import overall_exit_code


def test_partial_failure_is_red():
    results = [
        {"sheet_name": "SIGNALS", "status": "success"},
        {"sheet_name": "EVALUATIONS", "status": "failed", "error": "cell limit"},
    ]
    assert overall_exit_code(results) == 1


def test_all_success_is_green():
    assert overall_exit_code([{"status": "success"}, {"status": "success"}]) == 0


def test_success_with_skips_is_green():
    # skipped(ファイル無し/空)は失敗ではない
    assert overall_exit_code([{"status": "success"}, {"status": "skipped"}]) == 0


def test_nothing_synced_is_red():
    assert overall_exit_code([{"status": "skipped"}]) == 1
    assert overall_exit_code([]) == 1
