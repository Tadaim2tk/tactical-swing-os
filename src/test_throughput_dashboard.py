"""Dashboard の売買頻度カード(2026-11-03)。判定は data/throughput_watch.csv の最終行をそのまま見せ、
週表は台帳から tools/throughput_watch.py と同じ定義で数える。"""
from __future__ import annotations

import pandas as pd

import dashboard_render as dr
import dashboard_summaries as ds
import throughput_metrics as tm


def _ledger(days=21):
    rows = []
    for i, d in enumerate(pd.date_range("2026-09-01", periods=days, freq="D")):
        ds_ = d.strftime("%Y-%m-%d")
        for a in ["GOLD", "WTI", "BTC"]:
            if a == "WTI" and d.weekday() == 0:  # 毎週月曜に WTI BUY(単発) → 週1本の見立て
                rows.append([ds_, f"x_{ds_}_{a}", a, "BUY", "B", "PULLBACK"])
            else:
                rows.append([ds_, f"x_{ds_}_{a}", a, "NONE", "NO_TRADE", "NO_TRADE"])
    return pd.DataFrame(rows, columns=["date", "signal_id", "asset", "side", "rank", "type"])


def test_summary_unavailable_without_csv_but_weekly_from_ledger():
    out = ds.throughput_summary(pd.DataFrame(), _ledger())
    assert out["available"] is False and out["tone"] == "neutral"
    assert out["weekly"] and all(set(r) >= {"week", "orders", "ideas"} for r in out["weekly"])
    assert sum(r["ideas"] for r in out["weekly"]) == 3  # 3 週 × 月曜1本


def test_summary_reads_latest_row_and_tone():
    watch = pd.DataFrame([
        {"as_of": "2026-09-20", "status": "WARN", "orders_window": "3", "ideas_window": "3", "orders_baseline": "20", "ideas_baseline": "8", "orders_ratio": "0.6", "ideas_ratio": "1.5", "window_days": "14", "baseline_days": "56", "note": ""},
        {"as_of": "2026-09-21", "status": "ALERT", "orders_window": "2", "ideas_window": "2", "orders_baseline": "20", "ideas_baseline": "8", "orders_ratio": "0.4", "ideas_ratio": "", "window_days": "14", "baseline_days": "56", "note": "見立てが14日で2本"},
    ])
    out = ds.throughput_summary(watch, _ledger())
    assert out["available"] and out["status"] == "ALERT" and out["tone"] == "bad"
    assert out["ideas_window"] == 2 and out["orders_ratio"] == 0.4 and out["ideas_ratio"] is None
    assert out["stale"] is False


def test_summary_marks_stale_when_watch_lags_ledger():
    watch = pd.DataFrame([{"as_of": "2026-09-10", "status": "OK", "orders_window": "6", "ideas_window": "5", "orders_baseline": "20", "ideas_baseline": "8", "orders_ratio": "1.0", "ideas_ratio": "1.0", "window_days": "14", "baseline_days": "56", "note": ""}])
    out = ds.throughput_summary(watch, _ledger())  # 台帳は 9/21 まで
    assert out["stale"] is True and out["tone"] == "warn"


def test_block_renders_status_and_weekly_table():
    tp = ds.throughput_summary(pd.DataFrame([{"as_of": "2026-09-21", "status": "ALERT", "orders_window": "2", "ideas_window": "2", "orders_baseline": "20", "ideas_baseline": "8", "orders_ratio": "0.4", "ideas_ratio": "0.5", "window_days": "14", "baseline_days": "56", "note": "見立てが14日で2本"}]), _ledger())
    html_text = dr.throughput_block(tp)
    assert "ALERT" in html_text and "pill-bad" in html_text and "見立て 2 本" in html_text and "<table" in html_text
    assert "売買頻度 未取得" in dr.throughput_block({})


def test_metrics_module_is_the_single_definition():
    # CLI(tools/throughput_watch.py) は src/throughput_metrics.py の関数をそのまま使う
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location("tw_cli", Path(__file__).resolve().parents[1] / "tools" / "throughput_watch.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.evaluate is tm.evaluate and mod.weekly_table is tm.weekly_table and mod.mark_runs is tm.mark_runs


def test_health_layer_uses_recording_time_not_ledger_date():
    """監視が毎日走っていれば、台帳が遅れていても throughput_watch 層は fresh(#202 Codex P2)。"""
    import dashboard_io as dio
    watch = pd.DataFrame([
        {"as_of": "2026-10-28", "status": "ALERT", "recorded_at": "2026-11-02T13:01:58Z"},
        {"as_of": "2026-10-29", "status": "ALERT", "recorded_at": "2026-11-03T21:56:10Z"},
    ])
    ts = dio.latest_timestamp(watch, "recorded_at")
    assert ts == "2026-11-03 21:56:10 UTC"
    assert dio.latest_timestamp(pd.DataFrame(), "recorded_at") == ""
    spec = next(s for s in ds.LAYER_HEALTH_REGISTRY if s["label"] == "throughput_watch")
    assert spec["ts"] == ("date", "latest_throughput_watch_recorded_at")
    layer = ds.assess_layer("throughput_watch", ts, 2, pd.Timestamp("2026-11-04T06:00:00"), 36, cadence="daily")
    assert layer["status"] == "fresh"
    # as_of(10/29)で測っていたら 6日以上前で stale になっていたはず
    stale = ds.assess_layer("throughput_watch", "2026-10-29", 2, pd.Timestamp("2026-11-04T06:00:00"), 36, cadence="daily")
    assert stale["status"] == "stale"

