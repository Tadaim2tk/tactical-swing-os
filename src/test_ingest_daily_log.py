"""Daily log ingestion (Phase 29.7) の単体テスト。

固定する原則:
1. 3形式(markdownのcsvブロック/生CSV/JSON)の自動判別
2. 黙って捨てない — 全行に verdict(append/skip_duplicate/reject) が付く
3. 桁違い水準(QQQ事故クラス)は取込時に警告(記録は許可・採点側が隔離)
4. 既定 dry-run(書かない)・--apply でのみ追記・origin 列の冪等な拡張
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import ingest_daily_log as idl

HEADER = ("date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,"
          "expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,"
          "invalidation,verification_target,verified_status")


def _ledger(tmp_path: Path) -> Path:
    p = tmp_path / "signal_log.csv"
    p.write_text(HEADER + "\n" + "2026-07-09,EXIST-001,WTI,BUY,B,MONITOR,72.0,73.0,69.5,77.0,80.0,2.1,60,0.38,,,,0.25,RISK_OFF,64,,,,73,,x,y,verified\n", encoding="utf-8")
    return p


def _raw(tmp_path: Path, asset="WTI", close=73.0) -> Path:
    d = tmp_path / "raw"
    d.mkdir(exist_ok=True)
    (d / f"{asset}.csv").write_text(f"date,open,high,low,close\n2026-07-09,{close},{close},{close},{close}\n", encoding="utf-8")
    return d


def test_markdown_csv_block_extraction(tmp_path):
    ledger, raw = _ledger(tmp_path), _raw(tmp_path)
    text = f"""# 日次レポート\n本文いろいろ\n```csv\n{HEADER}\n2026-07-10,TSO-20260710-001,WTI,BUY,B,MONITOR,72.5,73.5,70.0,78.0,81.0,2.0,58,0.35,,,,0.25,NEUTRAL,60,,,,70,,inv,vt,verified\n```\n後書き"""
    r = idl.ingest(text, origin="chatgpt_app", apply=False, run_score=False, ledger_path=ledger, raw_dir=raw)
    assert r["format"] == "markdown_csv_block"
    assert r["parsed"] == 1 and r["would_append"] == 1
    # dry-run では書かれない
    assert "TSO-20260710-001" not in ledger.read_text(encoding="utf-8")


def test_apply_appends_with_origin_and_extends_header(tmp_path):
    ledger, raw = _ledger(tmp_path), _raw(tmp_path)
    text = f"{HEADER}\n2026-07-10,TSO-20260710-001,WTI,BUY,B,M,72.5,73.5,70.0,78.0,81.0,2.0,58,0.35,,,,0.25,N,60,,,,70,,i,v,verified"
    r = idl.ingest(text, origin="gpt_terminal", apply=True, run_score=False, ledger_path=ledger, raw_dir=raw)
    assert r["format"] == "raw_csv" and r["appended"] == 1
    df = pd.read_csv(ledger, keep_default_na=False)
    assert "origin" in df.columns
    assert df[df["signal_id"] == "TSO-20260710-001"].iloc[0]["origin"] == "gpt_terminal"
    assert df[df["signal_id"] == "EXIST-001"].iloc[0]["origin"] == ""  # 既存行は空でパディング


def test_json_array_input(tmp_path):
    ledger, raw = _ledger(tmp_path), _raw(tmp_path)
    text = '[{"date":"2026-07-10","signal_id":"TSO-20260710-002","asset":"WTI","side":"BUY","rank":"B","entry_low":"72","entry_high":"73","sl":"70"}]'
    r = idl.ingest(text, origin="gpt_terminal", apply=True, run_score=False, ledger_path=ledger, raw_dir=raw)
    assert r["format"] == "json" and r["appended"] == 1


def test_duplicate_skipped_not_duplicated(tmp_path):
    ledger, raw = _ledger(tmp_path), _raw(tmp_path)
    text = f"{HEADER}\n2026-07-09,EXIST-001,WTI,BUY,B,M,72.0,73.0,69.5,77.0,80.0,2.1,60,0.38,,,,0.25,R,64,,,,73,,x,y,verified"
    r = idl.ingest(text, origin="manual", apply=True, run_score=False, ledger_path=ledger, raw_dir=raw)
    assert r["skipped_duplicate"] == 1 and r["appended"] == 0
    df = pd.read_csv(ledger, keep_default_na=False)
    assert (df["signal_id"] == "EXIST-001").sum() == 1


def test_scale_mismatch_warned_at_ingest(tmp_path):
    # QQQ水準(704)をNASDAQ指数(23600)へ -> 取込時に桁違い警告(記録は許可)
    ledger = _ledger(tmp_path)
    raw = _raw(tmp_path, asset="NASDAQ", close=23600.0)
    text = f"{HEADER}\n2026-07-10,TSO-X,NASDAQ,BUY,B,M,704.0,710.0,696.0,724.0,730.0,2.0,55,0.3,,,,0.25,N,60,,,,70,,i,v,verified"
    r = idl.ingest(text, origin="chatgpt_app", apply=False, run_score=False, ledger_path=ledger, raw_dir=raw)
    d = r["details"][0]
    assert d["verdict"] == "append"
    assert any("桁違い" in w for w in d["warnings"])


def test_reject_only_unparseable_rows(tmp_path):
    ledger, raw = _ledger(tmp_path), _raw(tmp_path)
    text = f"{HEADER}\n2026-07-10,,WTI,BUY,B,M,72,73,70,78,81,2,58,0.35,,,,0.25,N,60,,,,70,,i,v,verified\nbad-date,TSO-Y,WTI,NONE,NO_TRADE,,,,,,,,,,,,,,,,,,,,,,,"
    r = idl.ingest(text, origin="manual", apply=False, run_score=False, ledger_path=ledger, raw_dir=raw)
    assert r["rejected"] == 2  # 空ID と 不正date — どちらも理由つきで可視化
    assert all(d["verdict"] == "reject" for d in r["details"])


def test_unrecognized_input_is_honest_error(tmp_path):
    ledger, raw = _ledger(tmp_path), _raw(tmp_path)
    r = idl.ingest("ただの文章で表なし", origin="manual", apply=False, run_score=False, ledger_path=ledger, raw_dir=raw)
    assert r.get("error")
    assert r["parsed"] == 0


def test_ensure_origin_idempotent(tmp_path):
    ledger = _ledger(tmp_path)
    cols1 = idl.ensure_origin_column(ledger)
    cols2 = idl.ensure_origin_column(ledger)
    assert cols1 == cols2
    assert ledger.read_text(encoding="utf-8").splitlines()[0].count("origin") == 1
