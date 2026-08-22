"""Tests for automated generated-signal ledger persistence."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import append_generated_signals as ags


LEDGER_HEADER = (
    "date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,"
    "expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,"
    "invalidation,verification_target,verified_status,origin"
)


def test_append_generated_signals_dedupes_and_preserves_phase6_columns(tmp_path: Path):
    signals_path = tmp_path / "results" / "signals.csv"
    ledger_path = tmp_path / "data" / "signal_log.csv"
    summary_path = tmp_path / "results" / "signal_ledger_append_summary.json"
    signals_path.parent.mkdir(parents=True)
    ledger_path.parent.mkdir(parents=True)

    ledger_path.write_text(
        LEDGER_HEADER
        + "\n2026-08-16,EXISTING,GOLD,LONG,B,A-Pullback,4320,4380,4220,4560,,1.5,0.60,0.50,70,40,20,0.5,UPTREND,70,70,70,70,70,70,inv,vt,verified,manual\n",
        encoding="utf-8",
    )
    signals_path.write_text(
        "date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,"
        "tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,"
        "trend_score,momentum_score,data_quality\n"
        "2026-08-16,EXISTING,GOLD,LONG,B,A-Pullback,4320,4380,4220,4560,,1.5,0.60,0.50,70,40,20,0.5,UPTREND,70,70,70,70,70,70,inv,vt,88,77,OK\n"
        "2026-08-17,NEW-SIGNAL,NASDAQ,LONG,A,A-Pullback,29850,30100,29150,31250,,1.5,0.64,0.56,82,20,10,1.0,UPTREND,80,80,80,80,80,80,inv,vt,91,85,OK\n",
        encoding="utf-8",
    )

    result = ags.append_generated_signals(signals_path, ledger_path, summary_path, origin="daily_cycle")

    assert result["status"] == "success"
    assert result["appended_rows"] == 1
    assert result["skipped_duplicates"] == 1
    assert result["latest_signal_date"] == "2026-08-17"

    out = pd.read_csv(ledger_path, dtype=str, keep_default_na=False)
    assert list(out["signal_id"]) == ["EXISTING", "NEW-SIGNAL"]
    assert "trend_score" in out.columns
    assert "momentum_score" in out.columns
    assert "data_quality" in out.columns
    new = out[out["signal_id"] == "NEW-SIGNAL"].iloc[0]
    assert new["origin"] == "daily_cycle"
    assert new["verified_status"] == "unverified"
    assert new["trend_score"] == "91"

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["appended_rows"] == 1
    assert summary["ledger_rows_after"] == 2


def test_append_generated_signals_skips_empty_signal_file(tmp_path: Path):
    signals_path = tmp_path / "results" / "signals.csv"
    ledger_path = tmp_path / "data" / "signal_log.csv"
    summary_path = tmp_path / "results" / "signal_ledger_append_summary.json"

    result = ags.append_generated_signals(signals_path, ledger_path, summary_path)

    assert result["status"] == "skipped"
    assert "missing or empty" in result["error"]
    assert json.loads(summary_path.read_text(encoding="utf-8"))["status"] == "skipped"


def test_append_generated_signals_fails_when_no_valid_rows(tmp_path: Path):
    signals_path = tmp_path / "results" / "signals.csv"
    ledger_path = tmp_path / "data" / "signal_log.csv"
    summary_path = tmp_path / "results" / "signal_ledger_append_summary.json"
    signals_path.parent.mkdir(parents=True)
    signals_path.write_text("date,signal_id,asset\n,,GOLD\n", encoding="utf-8")

    result = ags.append_generated_signals(signals_path, ledger_path, summary_path)

    assert result["status"] == "failed"
    assert result["rejected_rows"] == 1
    assert "no valid" in result["error"]
