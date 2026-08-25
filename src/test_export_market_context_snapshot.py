"""market context snapshot (Phase 27.3-a / SPEC-JMCB-001) の単体テスト。

検証の柱:
1. usable_from_utc が生成時刻と一致する(lookahead 判定の根拠になる列)
2. 保存は多め — 10 スコアだけでなく主要資産の生値も列として残る
3. データ不足 / 鮮度切れは status で正直に表す(捏造しない)
4. append-only — 既存行を書き換えない / 同一 run の二重記録もしない
5. 空データでも例外で落ちない(日次サイクルを止めない)
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import export_market_context_snapshot as mcs


GENERATED = datetime(2026, 8, 26, 21, 55, 0, tzinfo=timezone.utc)


def market_frame(context_date: str = "2026-08-26", assets: list[str] | None = None) -> pd.DataFrame:
    assets = assets if assets is not None else list(mcs.KEY_ASSETS)
    rows = []
    for index, asset in enumerate(assets):
        open_ = 100.0 + index
        rows.append(
            {
                "run_ts": "2026-08-26T21:55:00+00:00",
                "asset": asset,
                "ticker": f"{asset}-X",
                "status": "ok",
                "message": "",
                "date": context_date,
                "open": open_,
                "high": open_ * 1.02,
                "low": open_ * 0.98,
                "close": open_ * 1.01,
                "volume": 1000,
                "rows": 240,
            }
        )
    return pd.DataFrame(rows)


def test_usable_from_matches_generation_time():
    """判断可能時刻は生成時刻。ここがズレると lookahead 判定が壊れる。"""
    row = mcs.build_snapshot_row(market_frame(), generated_dt=GENERATED)
    assert row["usable_from_utc"] == row["generated_at_utc"]
    assert row["generated_at_utc"].startswith("2026-08-26")
    assert row["snapshot_id"] == "MCTX-20260826T215500Z"


def test_saves_raw_asset_values_not_only_scores():
    """保存は多め。後から別の変数が効くと分かっても取り返せるようにする。"""
    row = mcs.build_snapshot_row(market_frame(), generated_dt=GENERATED)
    for asset in mcs.KEY_ASSETS:
        assert row[f"close_{asset}"] != "", f"close_{asset} が保存されていない"
        assert row[f"chg_pct_{asset}"] != "", f"chg_pct_{asset} が保存されていない"
    for column in mcs.SCORE_COLUMNS:
        assert row[column] != "", f"{column} が保存されていない"


def test_status_ok_on_full_fresh_data():
    row = mcs.build_snapshot_row(market_frame(), generated_dt=GENERATED)
    assert row["status"] == "ok"
    assert row["status_reason"] == ""
    assert row["input_assets_available"] == len(mcs.KEY_ASSETS)
    assert row["staleness_days"] == 0
    assert row["context_date"] == "2026-08-26"


def test_missing_assets_reported_as_insufficient_data():
    """資産が揃わなければ推測で埋めず insufficient_data。"""
    row = mcs.build_snapshot_row(
        market_frame(assets=["BTC", "GOLD", "SPX"]), generated_dt=GENERATED
    )
    assert row["status"] == "insufficient_data"
    assert "3/9" in row["status_reason"]
    assert row["input_assets_available"] == 3


def test_weekend_gap_is_not_stale_but_long_gap_is():
    """通常の週末・3連休は正常。4日以上空いたら取得停止を疑い stale。"""
    weekend = mcs.build_snapshot_row(
        market_frame(context_date="2026-08-23"), generated_dt=GENERATED
    )
    assert weekend["staleness_days"] == 3
    assert weekend["status"] == "ok"

    long_gap = mcs.build_snapshot_row(
        market_frame(context_date="2026-08-20"), generated_dt=GENERATED
    )
    assert long_gap["staleness_days"] == 6
    assert long_gap["status"] == "stale"
    assert "6 日前" in long_gap["status_reason"]


def test_non_ok_market_rows_are_ignored():
    """fetch 失敗行を有効データとして数えない。"""
    frame = market_frame()
    frame.loc[frame["asset"].isin(["BTC", "GOLD", "WTI"]), "status"] = "error"
    row = mcs.build_snapshot_row(frame, generated_dt=GENERATED)
    assert row["input_assets_available"] == len(mcs.KEY_ASSETS) - 3


def test_empty_market_does_not_raise():
    """空入力でも例外で日次サイクルを止めない。"""
    row = mcs.build_snapshot_row(pd.DataFrame(), generated_dt=GENERATED)
    assert row["status"] == "insufficient_data"
    assert row["input_assets_available"] == 0
    assert row["context_date"] == ""


def test_append_is_idempotent_for_same_run():
    row = mcs.build_snapshot_row(market_frame(), generated_dt=GENERATED)
    empty = pd.DataFrame(columns=mcs.SNAPSHOT_COLUMNS)

    first, appended_first = mcs.append_snapshot(row, empty)
    assert appended_first is True
    assert len(first) == 1

    second, appended_second = mcs.append_snapshot(row, first)
    assert appended_second is False
    assert len(second) == 1


def test_append_never_rewrites_existing_rows():
    """append-only。過去に記録した値は後から書き換えない。"""
    first_row = mcs.build_snapshot_row(market_frame(), generated_dt=GENERATED)
    ledger, _ = mcs.append_snapshot(first_row, pd.DataFrame(columns=mcs.SNAPSHOT_COLUMNS))

    later = GENERATED + timedelta(days=1)
    second_row = mcs.build_snapshot_row(
        market_frame(context_date="2026-08-27"), generated_dt=later
    )
    ledger, appended = mcs.append_snapshot(second_row, ledger)

    assert appended is True
    assert len(ledger) == 2
    assert ledger.iloc[0]["snapshot_id"] == first_row["snapshot_id"]
    assert ledger.iloc[0]["context_date"] == "2026-08-26"
    assert ledger.iloc[1]["context_date"] == "2026-08-27"


def test_column_order_is_stable():
    """消費側が列順に依存できるよう、スキーマ順を固定する。"""
    row = mcs.build_snapshot_row(market_frame(), generated_dt=GENERATED)
    ledger, _ = mcs.append_snapshot(row, pd.DataFrame(columns=mcs.SNAPSHOT_COLUMNS))
    assert list(ledger.columns) == mcs.SNAPSHOT_COLUMNS
    assert mcs.SNAPSHOT_COLUMNS[0] == "snapshot_id"
    assert "usable_from_utc" in mcs.SNAPSHOT_COLUMNS


def test_divergent_asset_dates_do_not_hide_a_stale_feed():
    """一部の資産だけ古い状態を、全体の最新日で隠さない(false-green 防止)。

    実データで確認された事象: 2026-08-25 の snapshot は US10Y だけ 1 日古く、
    2026-06-10 の記録では DXY が 1 日古い一方 USDJPY は 1 日進んでいた。
    """
    frame = market_frame()
    frame.loc[frame["asset"] == "US10Y", "date"] = "2026-08-20"
    row = mcs.build_snapshot_row(frame, generated_dt=GENERATED)

    # 最新バーは当日なので context_date と staleness_days は 0 のまま
    assert row["context_date"] == "2026-08-26"
    assert row["staleness_days"] == 0
    # だが最古資産は 6 日前。ここが隠れないこと
    assert row["oldest_asset_date"] == "2026-08-20"
    assert row["max_asset_staleness_days"] == 6
    assert row["asset_date_spread_days"] == 6
    assert row["status"] == "stale"
    assert "最も古い資産" in row["status_reason"]


def test_asset_dated_ahead_does_not_break_freshness():
    """FX が米株より 1 日先の日付を持つのは正常。これで stale にしない。"""
    frame = market_frame()
    frame.loc[frame["asset"] == "USDJPY", "date"] = "2026-08-27"
    row = mcs.build_snapshot_row(frame, generated_dt=GENERATED)
    assert row["context_date"] == "2026-08-27"
    assert row["staleness_days"] == -1
    assert row["max_asset_staleness_days"] == 0
    assert row["asset_date_spread_days"] == 1
    assert row["status"] == "ok"
