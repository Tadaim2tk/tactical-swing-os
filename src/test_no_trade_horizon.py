"""監査F2 (2026-09-06) の再現テスト: 見送り評価を1バーで確定させないこと。

監査の実測: horizon=10・実取得=1バー・値幅2・ATR14=2 → no_trade_correct。
その結果は FINAL_OUTCOMES に入るため has_open_latest_evaluation が再評価対象から外し、
残り9バーで大きく動いても見送りの採点は二度と検証されない。
"""
import pandas as pd
import pytest

import evaluate_signal as es
import reevaluate_pending_signals as rp


def _ohlc(n_bars, start="2026-07-01", high=101.0, low=99.0):
    dates = pd.date_range(start, periods=n_bars, freq="D")
    return pd.DataFrame({
        "date": dates,
        "open": [100.0] * n_bars,
        "high": [high] * n_bars,
        "low": [low] * n_bars,
        "close": [100.0] * n_bars,
        "atr14": [2.0] * n_bars,
    })


def _signal(date="2026-06-30"):
    return pd.Series({"signal_id": "s1", "date": date, "asset": "GOLD", "side": "NONE",
                      "rank": "NO_TRADE", "type": "NO_TRADE"})


def test_partial_horizon_is_held_pending():
    """1バーしか無い状態で no_trade_correct/missed に確定しない。"""
    r = es.no_trade_result(_signal(), _ohlc(1), horizon=10)
    assert r["outcome"] == "open_unresolved"
    assert r["status"] == "pending"
    assert r["error_type"] == "awaiting_horizon"
    assert "1/10" in r["notes"]


@pytest.mark.parametrize("bars", [1, 2, 5, 9])
def test_any_partial_horizon_is_not_final(bars):
    r = es.no_trade_result(_signal(), _ohlc(bars), horizon=10)
    assert r["outcome"] not in rp.FINAL_OUTCOMES, f"{bars}バーで確定してはいけない"
    assert rp.has_open_latest_evaluation(pd.Series(r)), "再評価対象から外れてはいけない"


def test_full_horizon_still_classifies():
    """ホライズンを満たせば従来どおり分類する（機能を止めていないこと）。"""
    r = es.no_trade_result(_signal(), _ohlc(10), horizon=10)
    assert r["outcome"] in ("no_trade_correct", "no_trade_missed")
    assert r["outcome"] in rp.FINAL_OUTCOMES
    assert not rp.has_open_latest_evaluation(pd.Series(r))


def test_full_horizon_quiet_market_is_correct():
    # 値幅2 < ATR14(2)*2=4 → 見送りは妥当
    r = es.no_trade_result(_signal(), _ohlc(10, high=101.0, low=99.0), horizon=10)
    assert r["outcome"] == "no_trade_correct"


def test_full_horizon_big_move_is_missed():
    # 値幅20 > ATR14(2)*2=4 → 見送りは機会損失
    r = es.no_trade_result(_signal(), _ohlc(10, high=110.0, low=90.0), horizon=10)
    assert r["outcome"] == "no_trade_missed"


def test_late_bars_can_flip_the_verdict():
    """監査の懸念そのもの: 静かな1バーで確定していたら、後の大きな動きを見逃していた。"""
    quiet_then_big = _ohlc(10)
    quiet_then_big.loc[9, "high"] = 130.0
    quiet_then_big.loc[9, "low"] = 70.0
    early = es.no_trade_result(_signal(), quiet_then_big.head(1), horizon=10)
    full = es.no_trade_result(_signal(), quiet_then_big, horizon=10)
    assert early["outcome"] == "open_unresolved"
    assert full["outcome"] == "no_trade_missed"


def test_no_bars_at_all_is_still_awaiting_not_pending_regression():
    """future が空のときの既存の扱い(no_trade/skipped/awaiting_horizon)は変えていない。"""
    r = es.no_trade_result(_signal("2026-12-31"), _ohlc(10), horizon=10)
    assert r["error_type"] == "awaiting_horizon"
    assert rp.has_open_latest_evaluation(pd.Series(r))


def test_empty_future_is_reevaluable():
    """同型の欠陥: バーが1本も無い見送りは outcome="no_trade" で、FINALにもOPENにも
    属さないため has_open_latest_evaluation が False を返し、後でバーが届いても
    永久に再評価されなかった。"""
    r = es.no_trade_result(_signal("2026-12-31"), _ohlc(10), horizon=10)
    assert r["outcome"] == "open_unresolved"
    assert r["status"] == "pending"
    assert rp.has_open_latest_evaluation(pd.Series(r)), "バーが届いても再評価されない行を作らない"
