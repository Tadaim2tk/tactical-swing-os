"""trim_sheets_grid の純関数テスト (非破壊保証の固定)。"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from trim_sheets_grid import MARGIN_ROWS, MIN_ROWS, data_extent, plan_resize


def test_data_extent():
    assert data_extent([]) == (0, 0)
    assert data_extent([["a", "b"], ["c"]]) == (2, 2)


def test_plan_trims_giant_empty_grid():
    # 100万行×26列の空グリッド + データ30行×10列 -> 50行(MIN)×10列へ
    plan = plan_resize(1_000_000, 26, 30, 10)
    assert plan == (max(30 + MARGIN_ROWS, MIN_ROWS), 10)


def test_plan_never_shrinks_below_data():
    tr, tc = plan_resize(5000, 50, 4000, 40)
    assert tr >= 4000 and tc >= 40


def test_plan_never_grows():
    # 既にタイトなグリッドは触らない(拡大しない)
    assert plan_resize(40, 5, 35, 5) == None or plan_resize(40, 5, 35, 5)[0] <= 40
    assert plan_resize(30, 3, 30, 3) is None


def test_no_trim_when_already_tight():
    assert plan_resize(60, 10, 45, 10) is None  # 45+20=65 > 60 -> 縮小余地なし
