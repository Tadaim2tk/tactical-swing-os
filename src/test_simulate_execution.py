"""SL/TP執行シミュレーション(保守的)の単体テスト。

固定する原則:
1. 曖昧さは常に不利側 — worst-in-zone約定 / 約定足のSL成立 / TP1は翌足以降 / SL優先
2. 判定不能は捏造しない — バー不足は open、未到達は no_fill
3. 採点系と同じ±10%水準ガードで系列取り違えを隔離
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import simulate_execution as se


def _ohlcv(bars):
    """bars: list of (date, open, high, low, close)"""
    df = pd.DataFrame(bars, columns=["date", "open", "high", "low", "close"])
    df["date"] = pd.to_datetime(df["date"])
    return df


def _row(**over):
    base = dict(date="2026-07-01", signal_id="X", asset="WTI", side="BUY", rank="B",
                risk_pct="0.25", entry_low="72.0", entry_high="73.0", sl="70.0", tp1="76.0")
    base.update(over)
    return pd.Series(base)


def test_long_fill_then_tp1_next_bar():
    bars = _ohlcv([
        ("2026-07-01", 74, 74.5, 72.5, 74.0),   # 約定(low<=73) SLなし TP同足でも翌足まで持ち越し
        ("2026-07-02", 74, 76.5, 73.5, 76.0),   # TP1 76 到達
    ])
    r = se.simulate_row(_row(), bars, "t")
    assert r["status"] == "filled_tp1"
    assert r["fill_price"] == 73.0            # worst-in-zone (BUY=entry_high)
    assert abs(r["r_result"] - 1.0) < 1e-9    # (76-73)/(73-70)=1.0R


def test_same_bar_sl_is_conservative_loss():
    bars = _ohlcv([("2026-07-01", 74, 74.5, 69.5, 74.0)])  # 約定もSL(70)も同足 → 不利側
    r = se.simulate_row(_row(), bars, "t")
    assert r["status"] == "filled_sl"
    assert r["r_result"] == -1.0


def test_sl_priority_when_same_later_bar():
    bars = _ohlcv([
        ("2026-07-01", 74, 74.5, 72.9, 74.0),            # 約定のみ
        ("2026-07-02", 74, 77.0, 69.5, 75.0),            # SLもTP1も同足 → SL優先
    ])
    r = se.simulate_row(_row(), bars, "t")
    assert r["status"] == "filled_sl" and r["r_result"] == -1.0


def test_tp1_not_credited_on_fill_bar_then_time_exit():
    bars = _ohlcv([
        ("2026-07-01", 74, 76.5, 72.9, 74.0),  # 約定足でTP1タッチ → 持ち越し(不利側)
        ("2026-07-02", 74, 75.0, 73.5, 74.5),
        ("2026-07-03", 74, 75.0, 73.5, 74.5),
        ("2026-07-06", 74, 75.0, 73.5, 74.5),
        ("2026-07-07", 74, 75.0, 73.5, 74.5),
        ("2026-07-08", 74, 75.0, 73.5, 74.2),  # 期限バー(判断日+5) 終値決済
    ])
    r = se.simulate_row(_row(), bars, "t")
    assert r["status"] == "filled_time_exit"
    assert abs(r["r_result"] - (74.2 - 73.0) / 3.0) < 1e-3


def test_no_fill_and_open():
    far = [("2026-07-0%d" % d, 80, 81, 78, 80) for d in range(1, 6)]
    r = se.simulate_row(_row(), _ohlcv(far), "t")
    assert r["status"] == "no_fill"
    r2 = se.simulate_row(_row(), _ohlcv(far[:2]), "t")   # 約定待ち窓が未完
    assert r2["status"] == "open"


def test_short_direction_mirrors():
    row = _row(side="SELL", entry_low="76.0", entry_high="77.0", sl="79.0", tp1="72.0")
    bars = _ohlcv([
        ("2026-07-01", 75, 76.5, 74.5, 75.0),  # SELL約定(worst=entry_low=76) SL(79)未達
        ("2026-07-02", 75, 75.5, 71.5, 72.5),  # TP1 72 到達
    ])
    r = se.simulate_row(row, bars, "t")
    assert r["status"] == "filled_tp1"
    assert r["fill_price"] == 76.0
    assert abs(r["r_result"] - (76 - 72) / 3.0) < 1e-3  # r_resultは4桁丸め


def test_scale_mismatch_excluded():
    r = se.simulate_row(_row(entry_low="720", entry_high="730", sl="700", tp1="760"),
                        _ohlcv([("2026-07-01", 74, 75, 73, 74)]), "t")
    assert r["status"] == "excluded_scale"


def test_signal_before_price_window_gets_typed_status_not_fake_fill():
    # 2026-08-31監査P1-4a: rawは直近240日で上書きされるため、信号日が窓外に落ちた行を
    # 窓先頭のバーへ静かにアンカーすると「6月の判断が8月のバーで約定」する(符号反転の
    # 実例を確認済み)。typed status で正直に返し、偽の約定を作らない。
    bars = _ohlcv([("2026-08-0%d" % d, 74, 76.5, 72.5, 74.0) for d in range(3, 8)])
    r = se.simulate_row(_row(date="2026-07-01"), bars, "t")  # 窓は8/3開始、信号は7/1
    assert r["status"] == "data_window_expired"
    assert r["fill_date"] == "" and pd.isna(r["r_result"])


def test_ledger_filter_only_priced_orders(tmp_path):
    led = pd.DataFrame([
        _row().to_dict(),
        _row(signal_id="W", risk_pct="0.00").to_dict(),          # 監視のみ → 対象外
        _row(signal_id="N", side="NONE", rank="NO_TRADE").to_dict(),
        _row(signal_id="A0", rank="C").to_dict(),                 # 未知rank → 対象外
    ])
    raw = tmp_path
    _ohlcv([("2026-07-01", 74, 74.5, 72.5, 74.0), ("2026-07-02", 74, 76.5, 73.5, 76.0)]).assign(
        date=lambda d: d["date"].dt.strftime("%Y-%m-%d")
    ).to_csv(raw / "WTI.csv", index=False)
    sim = se.simulate_ledger(led, raw_dir=raw)
    assert len(sim) == 1 and sim.iloc[0]["signal_id"] == "X"


def test_summarize_counts_and_cost_sensitivity():
    sim = pd.DataFrame([
        {"status": "filled_tp1", "r_result": 1.0, "capital_pct": 0.25, "rank": "B"},
        {"status": "filled_sl", "r_result": -1.0, "capital_pct": -0.25, "rank": "B"},
        {"status": "no_fill", "r_result": float("nan"), "capital_pct": float("nan"), "rank": "B"},
    ], columns=se.COLUMNS[:0].tolist() + ["status", "r_result", "capital_pct", "rank"]) if False else pd.DataFrame([
        {"status": "filled_tp1", "r_result": 1.0, "capital_pct": 0.25},
        {"status": "filled_sl", "r_result": -1.0, "capital_pct": -0.25},
        {"status": "no_fill", "r_result": float("nan"), "capital_pct": float("nan")},
    ])
    s = se.summarize(sim)
    assert s["fills_resolved"] == 2 and s["no_fill"] == 1
    assert s["gross_total_r"] == 0.0
    assert abs(s["cost_sensitivity_r"]["0.05R"] - (0.0 - 0.1)) < 1e-9
