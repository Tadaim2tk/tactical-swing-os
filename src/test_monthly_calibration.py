from __future__ import annotations

import pandas as pd

import build_monthly_calibration as cal


def make_signals():
    return pd.DataFrame(
        [
            {"signal_id": "s1", "asset": "BTC", "side": "LONG", "rank": "A", "regime": "UPTREND", "date": "2026-05-01"},
            {"signal_id": "s2", "asset": "BTC", "side": "LONG", "rank": "A", "regime": "UPTREND", "date": "2026-05-15"},
            {"signal_id": "s3", "asset": "GOLD", "side": "SHORT", "rank": "B", "regime": "DOWNTREND", "date": "2026-06-01"},
        ]
    )


def make_evaluations():
    return pd.DataFrame(
        [
            {"signal_id": "s1", "evaluation_status": "closed", "r_result": 1.5, "evaluation_date": "2026-05-08"},
            {"signal_id": "s2", "evaluation_status": "closed", "r_result": -0.5, "evaluation_date": "2026-05-22"},
            {"signal_id": "s3", "evaluation_status": "pending", "r_result": None, "evaluation_date": "2026-06-08"},
        ]
    )


def test_enrich_merges_regime():
    enriched = cal.enrich_evaluations(make_evaluations(), make_signals())
    assert "regime" in enriched.columns
    assert set(enriched["regime"].dropna()) == {"UPTREND", "DOWNTREND"}


def test_regime_calibration_table():
    enriched = cal.enrich_evaluations(make_evaluations(), make_signals())
    table = cal.calibration_table(
        make_signals(), enriched, "regime",
        ["UPTREND", "DOWNTREND", "RANGE", "UNKNOWN"],
        as_of=pd.Timestamp("2026-06-10"),
    )
    assert list(table["regime"]) == ["UPTREND", "DOWNTREND", "RANGE", "UNKNOWN"]
    up = table[table["regime"] == "UPTREND"].iloc[0]
    assert up["closed"] == 2
    assert "decayed_avg_r" in table.columns
    assert "effective_n" in table.columns
    assert "decay_divergence" in table.columns
    # n=2 < 30 なのでゲートは当然データ不足
    assert "データ不足" in up["reason"]


def test_decayed_avg_weights_recent_more():
    # 古い+1.5(33日前) と 新しい-0.5(19日前): 単純平均は+0.5だが減衰平均はより負側へ寄る
    enriched = cal.enrich_evaluations(make_evaluations(), make_signals())
    table = cal.calibration_table(
        make_signals(), enriched, "asset", as_of=pd.Timestamp("2026-06-10"),
    )
    btc = table[table["asset"] == "BTC"].iloc[0]
    assert btc["average_r"] == 0.5
    assert btc["decayed_avg_r"] < btc["average_r"]


def test_decay_divergence_flag():
    # 古い大勝ち + 直近の負け -> 全期間平均は正、減衰平均は負 -> divergence
    signals = pd.DataFrame(
        [{"signal_id": f"x{i}", "asset": "FX", "side": "LONG", "rank": "A", "regime": "RANGE", "date": "2026-01-01"} for i in range(4)]
    )
    evals = pd.DataFrame(
        [
            {"signal_id": "x0", "evaluation_status": "closed", "r_result": 3.0, "evaluation_date": "2025-09-01"},
            {"signal_id": "x1", "evaluation_status": "closed", "r_result": -0.8, "evaluation_date": "2026-06-01"},
            {"signal_id": "x2", "evaluation_status": "closed", "r_result": -0.8, "evaluation_date": "2026-06-05"},
            {"signal_id": "x3", "evaluation_status": "closed", "r_result": -0.8, "evaluation_date": "2026-06-08"},
        ]
    )
    enriched = cal.enrich_evaluations(evals, signals)
    table = cal.calibration_table(signals, enriched, "asset", as_of=pd.Timestamp("2026-06-10"))
    fx = table[table["asset"] == "FX"].iloc[0]
    assert fx["average_r"] > 0  # 全期間では勝っているように見える
    assert fx["decayed_avg_r"] < 0  # 直近は負けている
    assert bool(fx["decay_divergence"]) is True


def test_gate_unchanged_by_decay():
    # SPEC-SG-001のゲートはdecayの影響を受けない(n<30なら常にデータ不足)
    change, reason = cal.proposed_change(29, 0.9, 1.0, [1.0] * 29)
    assert change == 0.0 and "データ不足" in reason
