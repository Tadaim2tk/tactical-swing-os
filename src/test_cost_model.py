from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cost_model


def _model(assets: dict, default: dict | None = None) -> dict:
    return {"default": default or {"spread": 0.0, "commission_round_turn": 0.0, "swap_per_bar": 0.0, "source": "unconfigured"}, "assets": assets}


# === デフォルト(未設定)はコスト0 = ネット=グロス ===

def test_unconfigured_zero_cost():
    model = _model({})
    assert cost_model.cost_r("BTC", risk_per_unit=1000.0, bars_held=5, model=model) == 0.0
    assert cost_model.net_r(1.5, "BTC", 1000.0, 5, model=model) == 1.5


def test_net_r_equals_gross_when_zero():
    model = _model({})
    for gross in [-1.0, 0.0, 2.3]:
        assert cost_model.net_r(gross, "WTI", 2.0, 3, model=model) == gross


# === 設定値が効く ===

def test_spread_and_commission_reduce_r():
    # risk=2.0 price, spread+commission=0.4 price -> cost_r = 0.2R
    model = _model({"WTI": {"spread": 0.3, "commission_round_turn": 0.1, "swap_per_bar": 0.0, "source": "broker_x"}})
    assert abs(cost_model.cost_r("WTI", 2.0, bars_held=4, model=model) - 0.2) < 1e-9
    assert abs(cost_model.net_r(1.0, "WTI", 2.0, 4, model=model) - 0.8) < 1e-9


def test_swap_scales_with_bars():
    model = _model({"BTC": {"spread": 0.0, "commission_round_turn": 0.0, "swap_per_bar": 10.0, "source": "broker_x"}})
    # 5バー保有, swap 10/bar = 50 price, risk=1000 -> 0.05R
    assert abs(cost_model.cost_r("BTC", 1000.0, bars_held=5, model=model) - 0.05) < 1e-9
    # 0バーならスワップ0
    assert cost_model.cost_r("BTC", 1000.0, bars_held=0, model=model) == 0.0


def test_cost_always_unfavorable():
    model = _model({"BTC": {"spread": 30.0, "commission_round_turn": 0.0, "swap_per_bar": 0.0, "source": "broker_x"}})
    # 勝ちでも負けでもコストは減算
    assert cost_model.net_r(2.0, "BTC", 1000.0, 1, model=model) < 2.0
    assert cost_model.net_r(-1.0, "BTC", 1000.0, 1, model=model) < -1.0


# === 安全側のフォールバック ===

def test_unknown_asset_falls_back_to_default():
    model = _model({}, default={"spread": 1.0, "commission_round_turn": 0.0, "swap_per_bar": 0.0, "source": "default_src"})
    # 未定義アセットXはdefault(spread=1.0)を使う。risk=2.0 -> 0.5R
    assert abs(cost_model.cost_r("UNKNOWN_ASSET", 2.0, 1, model=model) - 0.5) < 1e-9


def test_zero_or_negative_risk_no_cost():
    model = _model({"BTC": {"spread": 30.0, "commission_round_turn": 0.0, "swap_per_bar": 0.0, "source": "broker_x"}})
    assert cost_model.cost_r("BTC", 0.0, 1, model=model) == 0.0
    assert cost_model.cost_r("BTC", -5.0, 1, model=model) == 0.0


def test_bad_values_coerced_to_zero():
    model = _model({"BTC": {"spread": "abc", "commission_round_turn": None, "swap_per_bar": float("nan"), "source": "broker_x"}})
    assert cost_model.cost_r("BTC", 1000.0, 5, model=model) == 0.0


# === 実際のconfigファイルが読めて、初期状態は0コスト ===

def test_shipped_config_is_zero_cost():
    cost_model.reset_cache()
    model = cost_model.load_cost_model()
    assert model["_meta"]["status"] == "unconfigured"
    for asset in ["BTC", "USDJPY", "WTI", "GOLD"]:
        assert cost_model.cost_r(asset, 100.0, 5, model=model) == 0.0


# === evaluate_signal 統合: ネット列が末端まで流れる ===

import pandas as pd  # noqa: E402
import evaluate_signal as ev  # noqa: E402


def _ohlcv(prices):
    rows = []
    for i, (o, h, l, c) in enumerate(prices):
        rows.append({"date": pd.Timestamp("2026-01-01") + pd.Timedelta(days=i + 1),
                     "open": o, "high": h, "low": l, "close": c})
    df = pd.DataFrame(rows)
    return ev.add_atr(df)


def test_evaluate_trade_applies_cost_on_sl(monkeypatch):
    # SL到達トレード。設定コストでネットR < グロスR(-1.0)になること
    configured = {"default": {"spread": 0.0, "commission_round_turn": 0.0, "swap_per_bar": 0.0, "source": "u"},
                  "assets": {"BTC": {"spread": 200.0, "commission_round_turn": 0.0, "swap_per_bar": 0.0, "source": "broker_x"}}}
    monkeypatch.setattr(cost_model, "_cache", configured)
    signal = pd.Series({"signal_id": "t1", "asset": "BTC", "side": "LONG", "rank": "A", "type": "T",
                        "date": "2026-01-01", "entry_low": 100000, "entry_high": 100000,
                        "sl": 99000, "tp1": 102000, "tp2": 104000})
    # entry 100000, risk=1000. 翌日 entryタッチ後 SL(99000)割れ
    df = _ohlcv([(100000, 100100, 99900, 100000), (100000, 100050, 98900, 99000)])
    res = ev.evaluate_trade(signal, df, horizon=5)
    assert res["hit_level"] == "SL"
    assert res["r_result"] == -1.0
    # spread 200 / risk 1000 = 0.2R のコスト
    assert abs(res["cost_r"] - 0.2) < 1e-9
    assert abs(res["r_result_net"] - (-1.2)) < 1e-9
    assert res["cost_source"] == "broker_x"


def test_evaluate_trade_zero_cost_net_equals_gross(monkeypatch):
    monkeypatch.setattr(cost_model, "_cache", {"default": {"spread": 0.0, "commission_round_turn": 0.0, "swap_per_bar": 0.0, "source": "unconfigured"}, "assets": {}})
    signal = pd.Series({"signal_id": "t2", "asset": "BTC", "side": "LONG", "rank": "A", "type": "T",
                        "date": "2026-01-01", "entry_low": 100000, "entry_high": 100000,
                        "sl": 99000, "tp1": 102000, "tp2": 104000})
    df = _ohlcv([(100000, 100100, 99900, 100000), (100000, 102500, 99900, 102000)])
    res = ev.evaluate_trade(signal, df, horizon=5)
    assert res["hit_level"] in {"TP1", "TP2"}
    assert res["cost_r"] == 0.0
    assert res["r_result_net"] == res["r_result"]
