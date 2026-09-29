"""週5日資産の暦は、取得した曜日で変わらない（2026-09-30、#174/#175 Codex）。

yfinance は週末に取得すると「当日」の行を末尾に付ける。decision_time_anchor は週末の行が
1本でもあると週7日資産と判定するため、JPY=X の土曜の1行で USDJPY の全アンカーが
k-1 → k-2 にずれ、採点が取得曜日に依存していた。
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import score_prediction_log as sp


def _write(tmp, asset, dates):
    rows = [{"date": d, "open": 150 + i, "high": 151 + i, "low": 149 + i, "close": 150.5 + i}
            for i, d in enumerate(dates)]
    pd.DataFrame(rows).to_csv(tmp / f"{asset}.csv", index=False)


WEEK = ["2026-09-21", "2026-09-22", "2026-09-23", "2026-09-24", "2026-09-25", "2026-09-28", "2026-09-29"]


def test_fx_weekend_today_row_is_dropped(tmp_path):
    _write(tmp_path, "USDJPY", WEEK[:5] + ["2026-09-26"])          # 土曜に取得した場合
    df = sp.load_ohlcv_frame("USDJPY", tmp_path)
    assert (df["date"].dt.dayofweek < 5).all()
    assert df.attrs.get("dropped_weekend_bars") == 1


def test_fx_anchor_does_not_depend_on_fetch_weekday(tmp_path):
    """同じ週の系列に、週末取得の当日行が付いていても付いていなくてもアンカーは同じ。"""
    a, b = tmp_path / "a", tmp_path / "b"; a.mkdir(); b.mkdir()
    _write(a, "USDJPY", WEEK)
    _write(b, "USDJPY", WEEK[:5] + ["2026-09-26"] + WEEK[5:])
    fa, fb = sp.load_ohlcv_frame("USDJPY", a), sp.load_ohlcv_frame("USDJPY", b)
    for d in ["2026-09-22", "2026-09-25", "2026-09-28", "2026-09-29"]:
        ka, ia = sp.decision_time_anchor(fa, d); kb, ib = sp.decision_time_anchor(fb, d)
        assert fa["date"].iloc[ia] == fb["date"].iloc[ib], d


def test_monday_fx_signal_anchors_on_friday(tmp_path):
    """月曜 07:00 JST の判断が知っている最後の終値は金曜。k-1。"""
    _write(tmp_path, "USDJPY", WEEK[:5] + ["2026-09-26"] + WEEK[5:])
    df = sp.load_ohlcv_frame("USDJPY", tmp_path)
    k, i = sp.decision_time_anchor(df, "2026-09-28")
    assert df["date"].iloc[i] == pd.Timestamp("2026-09-25")


def test_crypto_keeps_weekend_bars_and_k_minus_2(tmp_path):
    days = pd.date_range("2026-09-21", "2026-09-29").strftime("%Y-%m-%d").tolist()
    _write(tmp_path, "BTC", days)
    df = sp.load_ohlcv_frame("BTC", tmp_path)
    assert (df["date"].dt.dayofweek >= 5).sum() == 2
    k, i = sp.decision_time_anchor(df, "2026-09-28")
    assert df["date"].iloc[i] == pd.Timestamp("2026-09-26"), "UTC日足の前日ラベルはまだ閉じていない → k-2"
