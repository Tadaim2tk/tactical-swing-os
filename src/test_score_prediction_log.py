"""Prediction log retro-scorer (Phase 29.6) の単体テスト。

固定する原則:
1. 全判断を採点する — B級・NO_TRADE・side NONE も行として残る（サンプル廃棄禁止）
2. 反後知恵 — reference/risk は記録値のみ。記録不足は invalid ではなく「方向Rなし」で
   fwd リターンだけ記録（NONE行）/ 価格が無ければ invalid_data の正直表示
3. スキーマ正規化 — BUY→LONG / SELL→SHORT / 新旧列差異(verified_status有無)を許容
4. awaiting→確定の冪等更新（signal_id 重複なし）
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import score_prediction_log as spl


def _prices(tmp_path: Path, asset="WTI", n=30, start="2026-06-01", step=1.0, base=70.0):
    dates = pd.bdate_range(start, periods=n)
    close = base + step * np.arange(n)
    df = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "open": close,
                       "high": close + 0.5, "low": close - 0.5, "close": close, "volume": 1})
    (tmp_path / f"{asset}.csv").write_text(df.to_csv(index=False), encoding="utf-8")
    return dates, close


def _row(**over):
    base = dict(date="2026-06-08", signal_id="X1", asset="WTI", side="BUY", rank="B",
                entry_low=72.0, entry_high=73.0, sl=69.5, tp1=77.0, tp2=80.0,
                verified_status="verified")
    base.update(over)
    return base


# === 1. 全判断が行として残る ===

def test_all_ranks_scored_including_no_trade(tmp_path):
    _prices(tmp_path)
    ledger = pd.DataFrame([
        _row(),
        _row(signal_id="X2", side="NONE", rank="B", entry_low=0, entry_high=0, sl=0),
        _row(signal_id="X3", side="NONE", rank="NO_TRADE", entry_low=np.nan, entry_high=np.nan, sl=np.nan),
    ])
    scores = spl.score_ledger(ledger, raw_dir=tmp_path, scored_at="t")
    assert len(scores) == 3  # 1行も捨てない
    assert set(scores["signal_id"]) == {"X1", "X2", "X3"}
    none_rows = scores[scores["side"] == "NONE"]
    assert (none_rows["actionable"] == False).all()  # noqa: E712
    # 見送り行にも「その後何が起きたか」(fwdリターン)が記録される
    assert none_rows["fwd_return_5d"].notna().all()
    assert (none_rows["result_5d"] == "not_applicable").all()


# === 2. 反後知恵の R 計算 ===

def test_actionable_r_uses_recorded_reference_and_risk(tmp_path):
    dates, close = _prices(tmp_path)  # 6/8=index5, close=75.0
    scores = spl.score_ledger(pd.DataFrame([_row()]), raw_dir=tmp_path, scored_at="t")
    r = scores.iloc[0]
    assert r["side"] == "LONG"  # BUY正規化
    assert abs(r["reference_price"] - 72.5) < 1e-9
    assert abs(r["risk_unit"] - 3.0) < 1e-9
    # +5営業日: index10 close=80.0 -> R = (80-72.5)/3
    assert abs(r["r_close_5d"] - round((80.0 - 72.5) / 3.0, 4)) < 1e-9
    assert r["result_5d"] == "success"
    assert r["status"] == "scored"
    assert r["entry_touched_5d"] in (True, False)


def test_short_direction_r(tmp_path):
    _prices(tmp_path, step=-1.0, base=100.0)  # 下落トレンド
    scores = spl.score_ledger(
        pd.DataFrame([_row(side="SELL", entry_low=94.0, entry_high=95.0, sl=97.0)]),
        raw_dir=tmp_path, scored_at="t")
    r = scores.iloc[0]
    assert r["side"] == "SHORT"
    assert r["r_close_5d"] > 0  # 下落継続なのでSHORT成功
    assert r["result_5d"] == "success"


def test_no_price_data_is_invalid_not_fabricated(tmp_path):
    scores = spl.score_ledger(pd.DataFrame([_row(asset="UNKNOWN")]), raw_dir=tmp_path, scored_at="t")
    r = scores.iloc[0]
    assert r["status"] == "invalid_data"
    assert pd.isna(r["fwd_return_5d"])


def test_awaiting_when_window_open(tmp_path):
    dates, _ = _prices(tmp_path, n=8)  # 6/8=index5, +3までしか無い
    scores = spl.score_ledger(pd.DataFrame([_row()]), raw_dir=tmp_path, scored_at="t")
    r = scores.iloc[0]
    assert r["status"] == "awaiting_horizon"
    assert pd.notna(r["fwd_return_1d"])   # 確定分は記録
    assert pd.isna(r["fwd_return_10d"])   # 未確定は捏造しない
    assert r["result_10d"] == "awaiting"


# === 3. 正規化 ===

def test_side_normalization():
    assert spl.normalize_side("BUY") == "LONG"
    assert spl.normalize_side("SELL") == "SHORT"
    assert spl.normalize_side("LONG") == "LONG"
    assert spl.normalize_side("none") == "NONE"
    assert spl.normalize_side(None) == "NONE"
    assert spl.normalize_side("MONITOR") == "NONE"  # 不明値は方向なしへ(fail-closed)


# === 4. 冪等更新 ===

def test_append_scores_updates_awaiting_to_scored(tmp_path):
    path = tmp_path / "scores.csv"
    a = pd.DataFrame([{**{c: "" for c in spl.SCORE_COLUMNS},
                       "signal_id": "X1", "date": "2026-06-08", "status": "awaiting_horizon"}])
    b = pd.DataFrame([{**{c: "" for c in spl.SCORE_COLUMNS},
                       "signal_id": "X1", "date": "2026-06-08", "status": "scored"}])
    spl.append_scores(a, path)
    merged = spl.append_scores(b, path)
    assert len(merged) == 1
    assert merged.iloc[0]["status"] == "scored"  # 最新で更新


# === 集計の正直表示 ===

def test_summary_reports_counts_but_flags_small_n(tmp_path):
    _prices(tmp_path)
    ledger = pd.DataFrame([_row(signal_id=f"S{i}") for i in range(3)])
    scores = spl.score_ledger(ledger, raw_dir=tmp_path, scored_at="t")
    s = spl.summarize(scores)
    b = s["by_rank"]["B"]
    assert b["actionable_rows"] == 3
    assert b["result_5d"]["n_closed"] == 3
    assert b["result_5d"]["win_rate"] is not None            # 件数と勝敗は出す
    assert b["result_5d"]["statistical_basis"] == "insufficient_data"  # ただし判断材料未満を明示
    assert s["min_samples_for_judgement"] == spl.MIN_SAMPLES


def test_safety_fields():
    assert spl.SAFETY_FIELDS["connected_to_signal_score"] is False
    assert spl.SAFETY_FIELDS["weights_json_updated"] is False


# === データ品質ガード(補正せず・正直に除外) ===

def test_scale_mismatch_excluded_not_repaired(tmp_path):
    # QQQ水準(704/696)を指数価格(~23600)の資産に記録 -> scale_mismatch
    _prices(tmp_path, asset="NASDAQ", base=23600.0, step=10.0)
    scores = spl.score_ledger(
        pd.DataFrame([_row(asset="NASDAQ", entry_low=704.0, entry_high=710.0, sl=696.0)]),
        raw_dir=tmp_path, scored_at="t")
    r = scores.iloc[0]
    assert r["data_quality"] == "scale_mismatch"
    assert r["actionable"] == False  # noqa: E712
    assert pd.isna(r["r_close_5d"])          # 補正して捏造しない
    assert r["result_5d"] == "suspect_data"  # 勝率集計から自動除外
    assert pd.notna(r["fwd_return_5d"])      # fwdリターン(記録水準に依存しない)は残す
    s = spl.summarize(scores)
    assert s["suspect_data_rows"] == 1
    assert s["by_rank"]["B"]["result_5d"]["n_closed"] == 0  # 集計を汚さない


def test_same_family_index_confusion_quarantined(tmp_path):
    # NASDAQ総合水準(25,900前後)をNQ先物系列(29,400)の資産に記録 -> 桁は近いが
    # (close-reference)/risk が偽の約+10Rを生むため ±10% ガードで隔離する。
    # 一方、通常の押し目entry(anchorから~1%)は隔離しない。
    _prices(tmp_path, asset="NASDAQ", base=29400.0, step=0.0)
    scores = spl.score_ledger(
        pd.DataFrame([
            _row(signal_id="FAR", asset="NASDAQ", entry_low=25820.0, entry_high=25980.0, sl=25540.0),
            _row(signal_id="NEAR", asset="NASDAQ", entry_low=29000.0, entry_high=29100.0, sl=28700.0),
        ]),
        raw_dir=tmp_path, scored_at="t")
    far = scores[scores["signal_id"] == "FAR"].iloc[0]
    assert far["data_quality"] == "scale_mismatch"
    assert pd.isna(far["r_close_5d"])
    assert far["result_5d"] == "suspect_data"
    near = scores[scores["signal_id"] == "NEAR"].iloc[0]
    assert near["data_quality"] == "ok"
    assert pd.notna(near["r_close_5d"])
