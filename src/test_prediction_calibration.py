from __future__ import annotations

import pandas as pd

import build_prediction_calibration as pc


def make_signals(ranks):
    return pd.DataFrame([{"signal_id": f"s{i}", "rank": r} for i, r in enumerate(ranks)])


def make_evaluations(hits):
    return pd.DataFrame([
        {"signal_id": f"s{i}", "evaluation_status": "closed", "r_result": (1.0 if h else -1.0)}
        for i, h in enumerate(hits)
    ])


def run(ranks, hits, implied=None):
    implied = implied or {"A": 0.55, "B": 0.45}
    table_hits = pc.closed_hits_by_rank(make_signals(ranks), make_evaluations(hits))
    return pc.build_calibration_rows(table_hits, implied, "2026-06-11 12:00:00 JST"), table_hits, implied


def test_overconfident_detected():
    # Rank A (implied 0.55) で n=40, 的中12/40=30% -> 有意に過信
    ranks = ["A"] * 40
    hits = [1] * 12 + [0] * 28
    table, _, _ = run(ranks, hits)
    row = table[table["rank"] == "A"].iloc[0]
    assert row["closed_count"] == 40
    assert row["calibration_gap"] < 0
    assert row["calibration_verdict"] == "overconfident"
    assert row["significant"] == True  # noqa: E712


def test_well_calibrated_when_gap_small():
    # implied 0.55 で 的中 22/40 = 55% -> well_calibrated
    ranks = ["A"] * 40
    hits = [1] * 22 + [0] * 18
    table, _, _ = run(ranks, hits)
    assert table.iloc[0]["calibration_verdict"] == "well_calibrated"


def test_underconfident_detected():
    # implied 0.45 (Rank B) で 的中 32/40 = 80% -> 有意に過小評価
    ranks = ["B"] * 40
    hits = [1] * 32 + [0] * 8
    table, _, _ = run(ranks, hits)
    row = table[table["rank"] == "B"].iloc[0]
    assert row["calibration_verdict"] == "underconfident"


def test_below_30_is_insufficient():
    ranks = ["A"] * 29
    hits = [0] * 29  # 大外れでもn<30なら保留
    table, _, _ = run(ranks, hits)
    assert table.iloc[0]["calibration_verdict"] == "insufficient_data"


def test_brier_skill_score_positive_when_ranks_informative():
    # Aは高的中(0.8)、Bは低的中(0.2): implied {A:0.8, B:0.2} が完璧なら BSS > 0
    ranks = ["A"] * 30 + ["B"] * 30
    hits = [1] * 24 + [0] * 6 + [1] * 6 + [0] * 24
    _, table_hits, _ = run(ranks, hits)
    skill = pc.brier_skill_score(table_hits, {"A": 0.8, "B": 0.2})
    assert skill["scored_n"] == 60
    assert skill["brier_skill_score"] > 0.3


def test_brier_skill_score_zero_when_uninformative():
    # 両Rankとも同じ的中率なら、implied差は情報を持たずBSS <= 0
    ranks = ["A"] * 30 + ["B"] * 30
    hits = ([1] * 15 + [0] * 15) * 2
    _, table_hits, _ = run(ranks, hits)
    skill = pc.brier_skill_score(table_hits, {"A": 0.55, "B": 0.45})
    assert skill["brier_skill_score"] <= 0.0


def test_default_implied_probabilities():
    implied, source = pc.load_implied_probabilities()
    assert implied == {"A": 0.55, "B": 0.45}
    assert "default" in source


def test_missing_inputs_graceful():
    table = pc.build_calibration_rows(pd.DataFrame(), {"A": 0.55}, "2026-06-11 12:00:00 JST")
    assert table.empty
    summary = pc.summary_from(table, {"overall_brier": 0.0, "reference_brier": 0.0, "brier_skill_score": 0.0, "scored_n": 0}, "default", "j", "u")
    assert summary["calibration_status"] == "unavailable"
    assert summary["requires_human_approval"] is True
