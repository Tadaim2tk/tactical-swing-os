"""最小観測ループ (Phase 29.4) の単体テスト。

検証の柱:
1. 候補選定: 適格イベント(CBS>=80 & EMS>=70)優先、無ければ直近A-rankをdry-run
2. 反後知恵: R は当時の reference/risk から計算。元記録不足は invalid_data(推定しない)
3. 結果窓未確定は pending の正直表示、再実行で確定に更新(重複しない)
4. 1周の成果物: observation_log.csv + OBS md が生成される
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import run_observation_loop as ol


def _ledger_row(**over) -> dict:
    base = dict(
        date="2026-06-08", signal_id="20260608_WTI_LONG_A-MOMENTUM", asset="WTI",
        side="LONG", rank="A", type="A-Momentum",
        entry_low=95.5, entry_high=97.0, sl=92.0, tp1=102.0, tp2=105.0,
        rr=1.5, win_prob=0.6, expected_r=0.5, tq_score=70,
        regime="oil_supply_shock", ems=84, ffs=60, cds=55, ias=50, cbs=76, mes=65,
        invalidation="Close below SL", verification_target="TP1 then TP2",
    )
    base.update(over)
    return base


def _prices(tmp_path: Path, asset="WTI", n=30, start="2026-06-01", step=0.5, base=95.0):
    dates = pd.bdate_range(start, periods=n)
    close = base + step * np.arange(n)
    df = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "open": close, "high": close + 0.5,
                       "low": close - 0.5, "close": close, "volume": 100})
    (tmp_path / f"{asset}.csv").write_text(df.to_csv(index=False), encoding="utf-8")
    return dates, close


# === 1. 候補選定 ===

def test_qualifying_event_preferred_over_dry_run():
    ledger = pd.DataFrame([
        _ledger_row(),  # CBS 76 -> 非適格
        _ledger_row(date="2026-06-09", signal_id="q1", cbs=85, ems=75),  # 適格
    ])
    row, run_type = ol.select_candidate(ledger)
    assert run_type == "qualifying" and row["signal_id"] == "q1"


def test_dry_run_when_no_qualifying():
    row, run_type = ol.select_candidate(pd.DataFrame([_ledger_row()]))
    assert run_type == "non_qualifying_dry_run"
    assert row["signal_id"] == "20260608_WTI_LONG_A-MOMENTUM"


def test_no_candidate_when_no_a_rank():
    row, run_type = ol.select_candidate(pd.DataFrame([_ledger_row(rank="B")]))
    assert row is None and run_type == "no_candidate"


# === 2/3. 評価の反後知恵と正直表示 ===

def test_evaluate_uses_recorded_reference_and_risk(tmp_path):
    dates, close = _prices(tmp_path)
    closes = pd.Series(close, index=dates)
    out = ol.evaluate_outcome(pd.Series(_ledger_row()), closes)
    # reference = (95.5+97)/2 = 96.25, risk = 96.25-92 = 4.25 (当時の記録値)
    assert abs(out["reference_price"] - 96.25) < 1e-9
    assert abs(out["risk_unit"] - 4.25) < 1e-9
    # 6/8(=index[5]) の +5営業日 = index[10] close = 95+0.5*10 = 100.0
    expected_r = (100.0 - 96.25) / 4.25
    assert abs(out["realized_r_5d"] - round(expected_r, 4)) < 1e-9
    assert out["result"] == "success"


def test_invalid_data_when_sl_missing(tmp_path):
    dates, close = _prices(tmp_path)
    closes = pd.Series(close, index=dates)
    out = ol.evaluate_outcome(pd.Series(_ledger_row(sl=np.nan)), closes)
    assert out["result"] == "invalid_data"
    assert np.isnan(out["realized_r_5d"])


def test_pending_when_window_not_closed(tmp_path):
    dates, close = _prices(tmp_path, n=8)  # 6/8 の +5営業日が存在しない
    closes = pd.Series(close, index=dates)
    out = ol.evaluate_outcome(pd.Series(_ledger_row()), closes)
    assert out["result"] == "pending"


def test_failure_when_price_falls(tmp_path):
    dates, close = _prices(tmp_path, step=-0.5, base=100.0)
    closes = pd.Series(close, index=dates)
    out = ol.evaluate_outcome(pd.Series(_ledger_row()), closes)
    assert out["result"] == "failure"
    assert out["realized_r_5d"] < 0


# === 4. 1周の成果物 ===

def test_run_writes_log_and_observation_md(tmp_path, monkeypatch):
    _prices(tmp_path)
    ledger_path = tmp_path / "signal_log.csv"
    pd.DataFrame([_ledger_row()]).to_csv(ledger_path, index=False)
    monkeypatch.setattr(ol, "RESULTS_DIR", tmp_path / "results")
    (tmp_path / "results").mkdir()

    summary = ol.run(
        ledger_path=ledger_path,
        obs_log_path=tmp_path / "observation_log.csv",
        obs_dir=tmp_path / "observations",
        raw_dir=tmp_path,
        memory_path=tmp_path / "no_memory.csv",
    )
    assert summary["status"] == "recorded"
    assert summary["run_type"] == "non_qualifying_dry_run"
    log = pd.read_csv(tmp_path / "observation_log.csv")
    assert len(log) == 1
    md = (tmp_path / "observations" / f"{summary['event_id']}.md").read_text(encoding="utf-8")
    assert "反後知恵" in md and "dry-run" in md or "dry_run" in md

    # 再実行 -> 重複せず最新で上書き
    ol.run(ledger_path=ledger_path, obs_log_path=tmp_path / "observation_log.csv",
           obs_dir=tmp_path / "observations", raw_dir=tmp_path, memory_path=tmp_path / "no_memory.csv")
    log2 = pd.read_csv(tmp_path / "observation_log.csv")
    assert len(log2) == 1


def test_safety_fields():
    assert ol.SAFETY_FIELDS["connected_to_signal_score"] is False
    assert ol.SAFETY_FIELDS["weights_json_updated"] is False
