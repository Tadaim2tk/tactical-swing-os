"""evaluate_signal の正直な評価状態の単体テスト (Phase 27.2)。

第1コホートが評価へ変換される瞬間を正しく観測できることを保証する。特に
「価格データが本当に無い(data_missing)」と「signal_date 以降のバーがまだ無い
= ホライズン未到達(awaiting_horizon, 若い/蓄積中)」を取り違えないことを検証する。
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import evaluate_signal as ev


def _ohlcv(rows: list[tuple[float, float, float, float]], start: str = "2026-01-02") -> pd.DataFrame:
    out = []
    for i, (o, h, l, c) in enumerate(rows):
        out.append({"date": pd.Timestamp(start) + pd.Timedelta(days=i), "open": o, "high": h, "low": l, "close": c})
    return ev.add_atr(pd.DataFrame(out))


def _trade_signal(date: str, asset: str = "WTI") -> pd.Series:
    return pd.Series(
        {
            "signal_id": "s",
            "asset": asset,
            "side": "LONG",
            "rank": "A",
            "type": "T",
            "date": date,
            "entry_low": 100,
            "entry_high": 100,
            "sl": 95,
            "tp1": 110,
            "tp2": 120,
        }
    )


def _no_trade_signal(date: str, asset: str = "GOLD") -> pd.Series:
    return pd.Series({"signal_id": "n", "asset": asset, "side": "NONE", "rank": "NO_TRADE", "type": "T", "date": date})


# === 決着: データが揃った due シグナルは closed になる ===

def test_trade_closes_when_data_present():
    sig = _trade_signal("2026-01-01")
    # 01-02 entryタッチ(100), 01-03 で tp1(110) 到達
    df = _ohlcv([(100, 101, 99, 100), (105, 111, 100, 110)])
    res = ev.evaluate_trade(sig, df, horizon=10)
    assert res["evaluation_status"] == "closed"
    assert res["outcome"] in {"win_tp1", "win_tp2"}
    assert res["error_type"] != "awaiting_horizon"
    assert res["error_type"] != "data_missing"


# === ホライズン未到達: OHLCはあるが将来バーが無い -> awaiting_horizon ===

def test_trade_awaiting_horizon_when_signal_newer_than_data():
    sig = _trade_signal("2026-01-31")  # df の最終バー(01-03)より新しい
    df = _ohlcv([(100, 101, 99, 100), (105, 111, 100, 110)])
    res = ev.evaluate_trade(sig, df, horizon=10)
    assert res["error_type"] == "awaiting_horizon"
    assert res["status"] == "pending"
    assert res["evaluation_status"] == "pending"
    assert res["outcome"] == "open_unresolved"


# === 欠損: OHLC が一切無い -> data_missing(awaiting_horizon と区別) ===

def test_trade_data_missing_when_no_ohlc():
    sig = _trade_signal("2026-01-01")
    res = ev.evaluate_trade(sig, pd.DataFrame(), horizon=10)
    assert res["error_type"] == "data_missing"
    assert res["status"] == "pending"
    assert res["evaluation_status"] == "pending"


def test_evaluate_one_data_missing_for_asset_without_raw(monkeypatch):
    # 実raw不在 -> load_ohlcv が空 -> data_missing(awaiting_horizon ではない)
    monkeypatch.setattr(ev, "load_ohlcv", lambda asset: pd.DataFrame())
    res = ev.evaluate_one(_trade_signal("2026-01-01", asset="NOPE"), horizon=10)
    assert res["error_type"] == "data_missing"


# === no_trade も同じ区別を行う ===

def test_no_trade_awaiting_horizon_when_signal_newer_than_data():
    # このテストが本来守っていたのは awaiting_horizon と data_missing の区別であり、
    # そこは不変。outcome/evaluation_status の期待値は監査F2 (2026-09-06) で変更した:
    # 旧値 outcome="no_trade" / evaluation_status="skipped" は FINAL_OUTCOMES にも
    # OPEN_OUTCOMES/OPEN_STATUSES にも属さず、has_open_latest_evaluation が False を
    # 返すため、バーが届いても永久に再評価されない行になっていた。
    sig = _no_trade_signal("2026-01-31")
    df = _ohlcv([(100, 101, 99, 100), (105, 106, 100, 104)])
    res = ev.no_trade_result(sig, df, horizon=10)
    assert res["error_type"] == "awaiting_horizon"
    assert res["outcome"] == "open_unresolved"
    assert res["evaluation_status"] == "pending"


def test_no_trade_data_missing_when_no_ohlc():
    sig = _no_trade_signal("2026-01-01")
    res = ev.no_trade_result(sig, pd.DataFrame(), horizon=10)
    assert res["error_type"] == "data_missing"
    assert res["outcome"] == "no_trade"


# === 入力不正: signal_date が不正/欠損は awaiting_horizon ではなく invalid_signal_date ===
# (Codex review P2: future_bars は signal_date=None でも空になり、誤って「若い」に分類されていた)

def test_trade_invalid_signal_date_not_awaiting_horizon():
    df = _ohlcv([(100, 101, 99, 100), (105, 111, 100, 110)])
    for bad in ["not-a-date", "", None]:
        res = ev.evaluate_trade(_trade_signal(bad), df, horizon=10)
        assert res["error_type"] == "invalid_signal_date", bad
        assert res["error_type"] != "awaiting_horizon"
        assert res["status"] == "invalid"
        assert res["evaluation_status"] == "skipped"
        assert res["outcome"] == "invalid"


def test_no_trade_invalid_signal_date_not_awaiting_horizon():
    df = _ohlcv([(100, 101, 99, 100), (105, 106, 100, 104)])
    for bad in ["not-a-date", "", None]:
        res = ev.no_trade_result(_no_trade_signal(bad), df, horizon=10)
        assert res["error_type"] == "invalid_signal_date", bad
        assert res["error_type"] != "awaiting_horizon"
        assert res["status"] == "invalid"
        assert res["evaluation_status"] == "skipped"
        assert res["outcome"] == "invalid"


def test_evaluate_one_invalid_signal_date_for_both_paths(monkeypatch):
    # evaluate_one 経由(trade / no_trade)でも、OHLCがあっても invalid_signal_date になる
    df = _ohlcv([(100, 101, 99, 100), (105, 111, 100, 110)])
    monkeypatch.setattr(ev, "load_ohlcv", lambda asset: df)
    assert ev.evaluate_one(_trade_signal("bad"), horizon=10)["error_type"] == "invalid_signal_date"
    assert ev.evaluate_one(_no_trade_signal(""), horizon=10)["error_type"] == "invalid_signal_date"


# === コホート(複数件)が混在しても各状態が正しく付く ===

def test_cohort_mixed_states_via_dataframe(monkeypatch):
    df = _ohlcv([(100, 101, 99, 100), (105, 111, 100, 110)])
    monkeypatch.setattr(ev, "load_ohlcv", lambda asset: df if asset == "WTI" else pd.DataFrame())
    signals = pd.DataFrame(
        [
            _trade_signal("2026-01-01", asset="WTI").to_dict(),   # closed
            _trade_signal("2026-01-31", asset="WTI").to_dict(),   # awaiting_horizon
            _trade_signal("2026-01-01", asset="NOPE").to_dict(),  # data_missing
        ]
    )
    out = ev.evaluate_signals_dataframe(signals, horizon=10)
    errs = out["error_type"].fillna("").astype(str).tolist()
    assert "awaiting_horizon" in errs
    assert "data_missing" in errs
    assert (out["evaluation_status"] == "closed").sum() == 1
