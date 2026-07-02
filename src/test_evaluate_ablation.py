"""Ablation evaluation frame (Phase 29.3) の単体テスト。

検証の柱:
1. 同一cohort: 3系統が同じ (日,資産,ホライズン) 行で比較される
2. テキスト系統の as-of 徹底（結果窓が基準日までに閉じた類似日のみ使用）
3. 合成armの決定的ルール（テキスト強不一致で見送り / 合意で確率平均）
4. データ不足時は insufficient_data の正直表示（捏造しない）
5. 指標計算（hit / R / Brier / calibration slope / net==gross when unconfigured）
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import build_narrative_memory as bnm
import evaluate_ablation as ea


# === フィクスチャ ===

def _trend_prices(tmp_path: Path, asset="SPX", n=160, start="2026-01-01", drift=0.01):
    """滑らかな上昇トレンドの合成OHLCV。"""
    dates = pd.bdate_range(start, periods=n)
    close = 100.0 * (1 + drift) ** np.arange(n)
    df = pd.DataFrame({
        "date": dates.strftime("%Y-%m-%d"),
        "open": close * 0.999, "high": close * 1.005, "low": close * 0.995,
        "close": close, "volume": 1000,
    })
    (tmp_path / f"{asset}.csv").write_text(df.to_csv(index=False), encoding="utf-8")
    return dates


def _memory(n_days: int, dates) -> pd.DataFrame:
    """価格日付に整合する n_days 分の allowed 局面record。"""
    rows = []
    for i in range(n_days):
        d = pd.Timestamp(dates[i]).strftime("%Y-%m-%d")
        rows.append({
            "record_id": f"r{i}", "memory_date": d, "asset_tags": "", "source": "t",
            "source_category": "macro", "text": f"risk on rally day{i} inflation cool",
            "link": f"https://x/{i}",
            "observed_at_utc": f"{d} 21:50:00 UTC", "source_published_at_utc": f"{d} 20:00:00 UTC",
            "ingested_at_utc": f"{d} 21:52:00 UTC", "signal_cutoff_utc": f"{d} 21:55:00 UTC",
            "allowed_for_signal": True, "cutoff_violation": False, "exclusion_reason": "",
        })
    return pd.DataFrame(rows, columns=bnm.MEMORY_COLUMNS)


# === 1/4. cohort とデータ不足 ===

def test_empty_when_insufficient_memory(tmp_path, monkeypatch):
    dates = _trend_prices(tmp_path)
    monkeypatch.setattr(ea, "RAW_DIR", tmp_path)
    cohort = ea.build_cohort(_memory(3, dates), raw_dir=tmp_path)
    assert cohort.empty


def test_empty_when_no_prices(tmp_path):
    dates = pd.bdate_range("2026-01-01", periods=30)
    cohort = ea.build_cohort(_memory(20, dates), raw_dir=tmp_path)  # 価格ファイルなし
    assert cohort.empty


def test_cohort_symmetric_across_arms(tmp_path):
    dates = _trend_prices(tmp_path, n=200)
    # memory は価格履歴が十分溜まった後半の日付に置く(テクニカル再構成に60バー必要)
    mem_dates = dates[100:130]
    cohort = ea.build_cohort(_memory(30, mem_dates), raw_dir=tmp_path)
    assert not cohort.empty
    # 同一cohort: (date,asset,horizon) 毎に必ず3arm揃う
    counts = cohort.groupby(["date", "asset", "horizon_days"])["arm"].nunique()
    assert (counts == len(ea.ARMS)).all()


def test_technical_arm_long_in_uptrend(tmp_path):
    dates = _trend_prices(tmp_path, n=200)
    cohort = ea.build_cohort(_memory(30, dates[100:130]), raw_dir=tmp_path)
    tech = cohort[(cohort["arm"] == "technical_only") & cohort["actionable"]]
    assert not tech.empty
    assert (tech["side"] == "LONG").all()          # 強い上昇トレンドでSHORTは出ない
    assert (tech["r"].dropna() > 0).mean() > 0.9   # 上昇継続なのでほぼ勝つ


# === 2. テキスト系統の as-of ===

def test_text_prediction_ignores_unclosed_windows(tmp_path):
    dates = _trend_prices(tmp_path, n=100)
    df = ea.load_ohlcv_frame("SPX", tmp_path)
    d_idx = 50
    # 類似日 = d の3バー前 -> +5d の結果窓は d 時点で未確定 -> 使えない
    recent = dates[d_idx - 3].strftime("%Y-%m-%d")
    out = ea.text_prediction([(recent, 0.9)], df, d_idx, horizon=5)
    assert out["side"] == "NONE" and out["n_cases"] == 0
    # 類似日 = d の10バー前 -> +5d は確定済み -> 使える(上昇トレンドなのでLONG)
    old = dates[d_idx - 10].strftime("%Y-%m-%d")
    out2 = ea.text_prediction([(old, 0.9)], df, d_idx, horizon=5)
    assert out2["side"] == "LONG" and out2["n_cases"] == 1


# === 3. 合成ルール ===

def test_combined_veto_on_strong_disagreement():
    tech = {"side": "LONG", "prob": 0.6}
    text = {"side": "SHORT", "prob": 0.9}  # LONG方向確率 0.1 < 0.35 -> 見送り
    assert ea.combined_prediction(tech, text)["side"] == "NONE"


def test_combined_agreement_averages_prob():
    tech = {"side": "LONG", "prob": 0.6}
    text = {"side": "LONG", "prob": 0.8}
    out = ea.combined_prediction(tech, text)
    assert out["side"] == "LONG"
    assert abs(out["prob"] - 0.7) < 1e-9


def test_combined_neutral_text_keeps_technical():
    tech = {"side": "SHORT", "prob": 0.55}
    text = {"side": "NONE", "prob": 0.5}
    out = ea.combined_prediction(tech, text)
    assert out["side"] == "SHORT"
    assert abs(out["prob"] - 0.525) < 1e-9


def test_combined_none_when_technical_none():
    assert ea.combined_prediction({"side": "NONE", "prob": 0.5}, {"side": "LONG", "prob": 0.9})["side"] == "NONE"


# === 5. 指標 ===

def _cohort_rows(arm: str, n: int, r=1.0, hit=1.0, prob=0.6, h=5) -> list[dict]:
    return [{
        "date": f"2026-01-{i+1:02d}", "asset": "SPX", "horizon_days": h, "arm": arm,
        "side": "LONG", "prob": prob, "actionable": True,
        "r": r, "hit": hit, "mfe_r": r + 0.5, "mae_r": -0.3, "risk_per_unit": 2.0,
    } for i in range(n)]


def test_metrics_insufficient_below_min_samples():
    cohort = pd.DataFrame(
        _cohort_rows("technical_only", 10)
        + _cohort_rows("text_narrative_only", 10)
        + _cohort_rows("technical_plus_text", 10)
    )
    table = ea.summarize_metrics(cohort)
    row = table[(table["arm"] == "technical_only") & (table["horizon_days"] == 5)].iloc[0]
    assert row["status"] == "insufficient_data"   # n=10 < 30
    assert row["n_actionable"] == 10
    assert row["hit_rate"] == 1.0


def test_metrics_ok_at_min_samples_and_net_equals_gross_unconfigured():
    import cost_model
    cost_model.reset_cache()
    cohort = pd.DataFrame(
        _cohort_rows("technical_only", 30)
        + _cohort_rows("text_narrative_only", 30, r=-0.5, hit=0.0, prob=0.4)
        + _cohort_rows("technical_plus_text", 30)
    )
    table = ea.summarize_metrics(cohort)
    tech = table[(table["arm"] == "technical_only") & (table["horizon_days"] == 5)].iloc[0]
    assert tech["status"] == "ok"
    assert tech["avg_r"] == 1.0
    # cost 未設定 -> net==gross を正直表示
    assert tech["net_avg_r"] == tech["avg_r"]
    assert tech["cost_source"] == "unconfigured"
    # Brier: prob=0.6, hit=1 -> (0.6-1)^2 = 0.16
    assert abs(tech["brier"] - 0.16) < 1e-9
    text = table[(table["arm"] == "text_narrative_only") & (table["horizon_days"] == 5)].iloc[0]
    assert text["hit_rate"] == 0.0 and text["avg_r"] == -0.5


def test_calibration_slope_positive_when_prob_tracks_hits():
    rows = []
    for i in range(40):
        good = i % 2 == 0
        rows += [{
            "date": f"2026-02-{(i % 28) + 1:02d}", "asset": "SPX", "horizon_days": 5,
            "arm": "technical_only", "side": "LONG",
            "prob": 0.8 if good else 0.3, "actionable": True,
            "r": 1.0 if good else -1.0, "hit": 1.0 if good else 0.0,
            "mfe_r": 1.0, "mae_r": -0.5, "risk_per_unit": 2.0,
        }]
    table = ea.summarize_metrics(pd.DataFrame(rows))
    row = table.iloc[0]
    assert row["calibration_slope"] > 0.5  # 確率が結果を追っている


def test_safety_fields_and_arm_list():
    assert ea.SAFETY_FIELDS["connected_to_signal_score"] is False
    assert ea.SAFETY_FIELDS["weights_json_updated"] is False
    assert set(ea.ARMS) == {"technical_only", "text_narrative_only", "technical_plus_text"}
