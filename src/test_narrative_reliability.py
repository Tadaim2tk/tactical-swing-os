from __future__ import annotations

import pandas as pd

import build_narrative_reliability as nr


def make_signals():
    rows = []
    for i in range(40):
        rows.append({"signal_id": f"s{i}", "asset": "BTC", "date": f"2026-05-{(i % 28) + 1:02d}"})
    return pd.DataFrame(rows)


def make_narratives_with_signal_id(n=40, narrative="risk_on"):
    return pd.DataFrame([{"narrative": narrative, "signal_id": f"s{i}"} for i in range(n)])


def make_evaluations(values):
    rows = []
    for i, v in enumerate(values):
        rows.append({
            "signal_id": f"s{i}",
            "evaluation_status": "closed",
            "r_result": v,
            "evaluation_date": f"2026-06-{(i % 9) + 1:02d}",
        })
    return pd.DataFrame(rows)


def run(narratives, signals, evaluations):
    links = nr.link_narratives_to_signals(narratives, signals)
    closed = nr.closed_r_by_signal(evaluations)
    return nr.build_reliability_rows(links, closed, "2026-06-11 12:00:00 JST", as_of=pd.Timestamp("2026-06-11"))


def test_signal_id_link_strong_positive():
    # n=30, 20勝(+1.0)/10敗(-0.5): sharpe≈0.70, p≈0.0007 -> strong_positive
    values = [1.0] * 20 + [-0.5] * 10
    table = run(make_narratives_with_signal_id(30), make_signals(), make_evaluations(values))
    assert len(table) == 1
    row = table.iloc[0]
    assert row["closed_count"] == 30
    assert row["reliability_label"] == "strong_positive"
    assert row["significant"] == True  # noqa: E712
    assert "p=" in row["evidence_note"]


def test_below_30_is_insufficient_data():
    values = [1.0] * 29
    table = run(make_narratives_with_signal_id(29), make_signals(), make_evaluations(values))
    assert table.iloc[0]["reliability_label"] == "insufficient_data"


def test_not_significant_is_unproven():
    values = [1.0, -1.0] * 15
    table = run(make_narratives_with_signal_id(30), make_signals(), make_evaluations(values))
    assert table.iloc[0]["reliability_label"] == "unproven"


def test_significant_loss_is_strong_negative():
    values = [0.5] * 10 + [-1.0] * 20
    table = run(make_narratives_with_signal_id(30), make_signals(), make_evaluations(values))
    row = table.iloc[0]
    assert row["reliability_label"] == "strong_negative"
    assert row["recommended_action"] == "human_review_for_suppression"


def test_asset_date_join_fallback():
    # signal_id列が無いナラティブは (asset, date) で結合される
    narratives = pd.DataFrame([
        {"narrative_category": "inflation_fear", "asset": "btc", "date": "2026-05-03"},
    ])
    signals = make_signals()
    evaluations = make_evaluations([2.0] * 5)
    links = nr.link_narratives_to_signals(narratives, signals)
    assert not links.empty
    assert set(links["narrative"]) == {"inflation_fear"}
    # 2026-05-03 のシグナルは s2 (date=05-03)
    assert "s2" in set(links["signal_id"])


def test_missing_inputs_return_empty_and_unavailable():
    table = nr.build_reliability_rows(pd.DataFrame(), pd.DataFrame(), "2026-06-11 12:00:00 JST")
    assert table.empty
    summary = nr.summary_from(table, "missing", "2026-06-11 12:00:00 JST", "2026-06-11 03:00:00 UTC")
    assert summary["narrative_reliability_status"] == "unavailable"
    assert summary["weights_json_updated"] is False
    assert summary["requires_human_approval"] is True


def test_safety_flags_in_rows():
    values = [1.0] * 30
    table = run(make_narratives_with_signal_id(30), make_signals(), make_evaluations(values))
    row = table.iloc[0]
    assert row["requires_human_approval"] == True  # noqa: E712
    assert row["weights_json_updated"] == False  # noqa: E712
