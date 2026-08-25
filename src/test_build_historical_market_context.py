"""historical market context join (Phase 27.3-b2 / SPEC-JMCB-001) の単体テスト。

固定された4条件をそのまま検証の柱にする:
1. provenance を全件に残す
2. 「寄り前の最新」を機械的に保証する
3. 週末などで数日空いても除外せず、当時利用可能だった最新記録として扱う
4. historical_artifact_join と native_point_in_time を区別する
そして、当時の記録が無い日は再構成せず unavailable にする。
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import build_historical_market_context as bh
import export_market_context_snapshot as mcs

UTC = dt.timezone.utc


def market_frame(run_ts: str, bar_date: str, assets: list[str] | None = None) -> pd.DataFrame:
    assets = assets if assets is not None else list(mcs.KEY_ASSETS)
    rows = []
    for index, asset in enumerate(assets):
        open_ = 100.0 + index
        rows.append(
            {
                "run_ts": run_ts,
                "asset": asset,
                "ticker": f"{asset}-X",
                "status": "ok",
                "message": "",
                "date": bar_date,
                "open": open_,
                "high": open_ * 1.02,
                "low": open_ * 0.98,
                "close": open_ * 1.01,
                "volume": 1000,
                "rows": 240,
            }
        )
    return pd.DataFrame(rows)


def entry(artifact_id: str, run_ts: str, bar_date: str, created_at: str) -> dict:
    return {
        "artifact_id": artifact_id,
        "artifact_name": f"tactical-swing-os-{artifact_id}999",
        "created_at": bh.parse_utc(created_at),
        "market": market_frame(run_ts, bar_date),
    }


def test_usable_from_is_artifact_time_not_run_ts():
    """保守側に倒す: 値が確実に手元にあったのはアーティファクト確定時刻。"""
    ledger = bh.build_historical_ledger(
        [entry("11", "2026-06-10T22:00:00+00:00", "2026-06-10", "2026-06-10T22:09:00Z")]
    )
    row = ledger.iloc[0]
    assert row["source_market_run_ts_utc"].startswith("2026-06-10 22:00")
    assert row["usable_from_utc"].startswith("2026-06-10 22:09")
    assert bh.parse_utc(row["usable_from_utc"]) >= bh.parse_utc(row["source_market_run_ts_utc"])


def test_provenance_is_recorded_and_distinct_from_native():
    """条件1と4。由来が残り、日次生成行と機械的に区別できる。"""
    ledger = bh.build_historical_ledger(
        [entry("11", "2026-06-10T22:00:00+00:00", "2026-06-10", "2026-06-10T22:09:00Z")]
    )
    row = ledger.iloc[0]
    assert row["provenance"] == mcs.PROVENANCE_HISTORICAL
    assert row["provenance"] != mcs.PROVENANCE_NATIVE
    assert row["source_artifact_id"] == "11"
    assert row["source_run_id"] == "11999"
    assert row["artifact_created_at_utc"] != ""

    native = mcs.build_snapshot_row(
        market_frame("2026-06-10T22:00:00+00:00", "2026-06-10"),
        generated_dt=dt.datetime(2026, 6, 10, 22, 0, tzinfo=UTC),
    )
    assert native["provenance"] == mcs.PROVENANCE_NATIVE


def test_join_picks_latest_snapshot_strictly_before_the_open():
    """条件2。寄り(09:00 JST = 00:00 UTC)より前の最新だけを採る。"""
    ledger = bh.build_historical_ledger(
        [
            entry("01", "2026-06-08T22:00:00+00:00", "2026-06-08", "2026-06-08T22:09:00Z"),
            entry("02", "2026-06-09T22:00:00+00:00", "2026-06-09", "2026-06-09T22:09:00Z"),
            # 寄りの後に出た記録。これを拾ってはいけない
            entry("03", "2026-06-10T01:00:00+00:00", "2026-06-10", "2026-06-10T01:09:00Z"),
        ]
    )
    link = bh.link_records([{"code": "1234", "name": "X", "date": "2026-06-10", "quarter": "Q1"}], ledger)
    row = link.iloc[0]
    assert row["join_status"] == "ok"
    assert row["source_artifact_id"] == "02"
    assert bh.parse_utc(row["snapshot_usable_from_utc"]) < bh.parse_utc(row["decision_cutoff_utc"])


def test_weekend_gap_is_kept_not_excluded():
    """条件3。金曜の記録しか無くても、それが当時利用可能だった最新記録。"""
    ledger = bh.build_historical_ledger(
        [entry("05", "2026-06-05T22:00:00+00:00", "2026-06-05", "2026-06-05T22:09:00Z")]
    )
    # 2026-06-08(月)の寄り前。直近の記録は金曜夜のもの
    link = bh.link_records([{"code": "1234", "name": "X", "date": "2026-06-08", "quarter": "Q1"}], ledger)
    row = link.iloc[0]
    assert row["join_status"] == "ok"
    assert row["source_artifact_id"] == "05"
    assert float(row["lag_hours"]) > 48
    assert float(row["lag_hours"]) < 96


def test_no_record_before_cutoff_is_unavailable_not_reconstructed():
    """当時の記録が無い日は再構成しない。"""
    ledger = bh.build_historical_ledger(
        [entry("09", "2026-07-01T22:00:00+00:00", "2026-07-01", "2026-07-01T22:09:00Z")]
    )
    link = bh.link_records([{"code": "1234", "name": "X", "date": "2026-06-10", "quarter": "Q1"}], ledger)
    row = link.iloc[0]
    assert row["join_status"] == "unavailable"
    assert row["snapshot_id"] == ""
    assert row["lag_hours"] == ""


def test_unparsable_date_is_unavailable():
    ledger = bh.build_historical_ledger(
        [entry("09", "2026-07-01T22:00:00+00:00", "2026-07-01", "2026-07-01T22:09:00Z")]
    )
    link = bh.link_records([{"code": "1234", "name": "X", "date": "", "quarter": ""}], ledger)
    assert link.iloc[0]["join_status"] == "unavailable"


def test_ledger_is_sorted_and_schema_stable():
    ledger = bh.build_historical_ledger(
        [
            entry("02", "2026-06-09T22:00:00+00:00", "2026-06-09", "2026-06-09T22:09:00Z"),
            entry("01", "2026-06-08T22:00:00+00:00", "2026-06-08", "2026-06-08T22:09:00Z"),
        ]
    )
    assert list(ledger.columns) == bh.HISTORICAL_COLUMNS
    assert list(ledger["source_artifact_id"]) == ["01", "02"]
    # 27.3-a のスキーマを内包し、provenance 列を追加している
    for column in mcs.SNAPSHOT_COLUMNS:
        assert column in bh.HISTORICAL_COLUMNS


def test_stale_feed_in_history_is_not_hidden():
    """過去分にも最古資産基準の鮮度判定が効く(27.3-a の監査修正の継承)。"""
    frame = market_frame("2026-06-10T22:00:00+00:00", "2026-06-10")
    frame.loc[frame["asset"] == "US10Y", "date"] = "2026-06-01"
    ledger = bh.build_historical_ledger(
        [
            {
                "artifact_id": "77",
                "artifact_name": "tactical-swing-os-77999",
                "created_at": bh.parse_utc("2026-06-10T22:09:00Z"),
                "market": frame,
            }
        ]
    )
    row = ledger.iloc[0]
    assert row["status"] == "stale"
    assert row["max_asset_staleness_days"] == 9
    assert row["asset_date_spread_days"] == 9
