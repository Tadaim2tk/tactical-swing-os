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
    # 古い+1.5(40日前) と 新しい-0.5(19日前): 単純平均は+0.5だが減衰平均はより負側へ寄る
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


# === SPEC-DSR-001: Deflated Sharpe Ratio (多重検定補正) ===

def test_single_trial_increase_still_passes():
    # n_trials=1(デフォルト)なら多重検定補正なし=従来通り増加提案が出る
    import random
    random.seed(2)
    strong = [random.gauss(0.5, 0.4) for _ in range(40)]
    avg = sum(strong) / len(strong)
    change, reason = cal.proposed_change(40, 0.6, avg, strong, n_trials=1, sharpe_variance=0.0)
    assert change > 0.0
    assert "DSR=" in reason


def test_dsr_blocks_lucky_increase_under_many_trials():
    # 単独検定は通る中程度セルが、多数試行(N=360)では偽陽性として保留される
    import random
    random.seed(7)
    moderate = [random.gauss(0.32, 0.5) for _ in range(40)]
    avg = sum(moderate) / len(moderate)
    rep = cal.stat_guards.significance_report(moderate)
    # 前提: Sharpe>0.5 を通過する(=DSRゲートまで到達する)セルであること
    assert rep["sharpe"] > cal.stat_guards.MIN_SHARPE_FOR_INCREASE
    change, reason = cal.proposed_change(40, 0.6, avg, moderate, n_trials=360, sharpe_variance=0.25)
    assert change == 0.0
    assert "Deflated Sharpe" in reason


def test_dsr_does_not_block_decrease():
    # 減少提案はリスク優先でDSRゲートを課さない
    losers = [-0.5] * 40
    change, reason = cal.proposed_change(40, 0.1, -0.5, losers, n_trials=360, sharpe_variance=0.25)
    assert change < 0.0


def test_gather_trial_context_counts_eligible_cells():
    signals = pd.DataFrame({"asset": ["X"] * 40 + ["Y"] * 10})
    evals = pd.DataFrame({
        "asset": ["X"] * 40 + ["Y"] * 10,
        "evaluation_status": ["closed"] * 50,
        "r_result": [0.3] * 40 + [0.1] * 10,
    })
    n_trials, variance = cal.gather_trial_context([(signals, evals, "asset", None)])
    # Xは40件(>=30)で1試行、Yは10件で対象外 → N=1
    assert n_trials == 1
    assert variance == 0.0


# === SPEC-NQ-001: ナラティブ信頼性 ===

def make_alignment():
    return pd.DataFrame(
        [
            {"signal_id": "s1", "narrative_alignment": "aligned", "narrative_alignment_score": 40},
            {"signal_id": "s2", "narrative_alignment": "conflicted", "narrative_alignment_score": -30},
            # s1の重複記録(後から来たもの)は無視されるべき
            {"signal_id": "s1", "narrative_alignment": "conflicted", "narrative_alignment_score": -99},
        ]
    )


def test_merge_narrative_alignment_first_record_wins():
    evals = cal.enrich_evaluations(make_evaluations(), make_signals())
    alignment = make_alignment().drop_duplicates(subset=["signal_id"], keep="first")
    merged = cal.merge_narrative_alignment(evals, alignment)
    s1 = merged[merged["signal_id"] == "s1"].iloc[0]
    assert s1["narrative_alignment"] == "aligned"


def test_narrative_calibration_table():
    evals = cal.enrich_evaluations(make_evaluations(), make_signals())
    alignment = make_alignment().drop_duplicates(subset=["signal_id"], keep="first")
    merged = cal.merge_narrative_alignment(evals, alignment)
    table = cal.calibration_table(
        cal.merge_narrative_alignment(make_signals(), alignment),
        merged,
        "narrative_alignment",
        cal.NARRATIVE_CATEGORIES,
        as_of=pd.Timestamp("2026-06-10"),
    )
    assert list(table["narrative_alignment"]) == ["aligned", "conflicted", "neutral", "insufficient_data"]
    aligned = table[table["narrative_alignment"] == "aligned"].iloc[0]
    assert aligned["closed"] == 1
    assert "データ不足" in aligned["reason"]


def test_narrative_edge_gated_below_30():
    note, edge = cal.narrative_edge_note([1.0] * 29, [-1.0] * 50)
    assert edge["verdict"] == "insufficient_data"
    assert "データ不足" in note


def test_narrative_edge_confirmed():
    aligned = [1.0, 1.2, 0.8] * 10      # n=30, mean=1.0
    conflicted = [-0.5, -0.7, -0.3] * 10  # n=30, mean=-0.5
    note, edge = cal.narrative_edge_note(aligned, conflicted)
    assert edge["verdict"] == "narrative_edge_confirmed"
    assert edge["p_value"] < 0.05


def test_narrative_inverse_warning():
    aligned = [-0.8, -1.0, -1.2] * 10
    conflicted = [0.9, 1.1, 1.0] * 10
    note, edge = cal.narrative_edge_note(aligned, conflicted)
    assert edge["verdict"] == "narrative_inverse"
    assert "逆ナラティブ" in note


def test_no_alignment_file_is_graceful():
    # 整合CSVが無い環境でもテーブルは全カテゴリゼロで生成される
    empty = cal.merge_narrative_alignment(make_signals(), pd.DataFrame())
    assert "narrative_alignment" in empty.columns
