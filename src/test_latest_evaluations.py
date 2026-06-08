from __future__ import annotations

import pandas as pd

import build_latest_evaluations as lev


def test_latest_row_selected_by_reevaluation_timestamp():
    evaluations = pd.DataFrame(
        [
            {
                "signal_id": "S001",
                "asset": "BTC",
                "evaluation_date": "2026-06-01",
                "outcome": "open_unresolved",
            }
        ]
    )
    pending = pd.DataFrame(
        [
            {
                "signal_id": "S001",
                "asset": "BTC",
                "reevaluation_at_jst": "2026-06-08 07:05:00 JST",
                "outcome": "win_tp1",
            }
        ]
    )

    latest = lev.build_latest_view(evaluations, pending, generated_at_utc=pd.Timestamp("2026-06-08T00:00:00Z").to_pydatetime())

    assert len(latest) == 1
    row = latest.iloc[0]
    assert row["outcome"] == "win_tp1"
    assert row["latest_source"] == "pending_reevaluations"
    assert row["latest_reason"] == "latest_by_reevaluation_at"
    assert bool(row["has_reevaluation_history"]) is True


def test_same_timestamp_prefers_pending_reevaluations():
    evaluations = pd.DataFrame(
        [
            {
                "signal_id": "S001",
                "evaluation_date": "2026-06-08",
                "outcome": "open_unresolved",
            }
        ]
    )
    pending = pd.DataFrame(
        [
            {
                "signal_id": "S001",
                "evaluation_date": "2026-06-08",
                "outcome": "loss_sl",
            }
        ]
    )

    latest = lev.build_latest_view(evaluations, pending, generated_at_utc=pd.Timestamp("2026-06-08T00:00:00Z").to_pydatetime())

    assert latest.iloc[0]["latest_source"] == "pending_reevaluations"
    assert latest.iloc[0]["outcome"] == "loss_sl"


def test_blank_signal_id_is_excluded():
    evaluations = pd.DataFrame([{"signal_id": "", "evaluation_date": "2026-06-08", "outcome": "win_tp1"}])

    latest = lev.build_latest_view(evaluations, pd.DataFrame(), generated_at_utc=pd.Timestamp("2026-06-08T00:00:00Z").to_pydatetime())

    assert latest.empty


def test_evaluations_only_and_pending_only_both_work():
    ev_only = lev.build_latest_view(
        pd.DataFrame([{"signal_id": "E1", "evaluation_date": "2026-06-08", "outcome": "win_tp2"}]),
        pd.DataFrame(),
        generated_at_utc=pd.Timestamp("2026-06-08T00:00:00Z").to_pydatetime(),
    )
    pending_only = lev.build_latest_view(
        pd.DataFrame(),
        pd.DataFrame([{"signal_id": "P1", "reevaluation_at_utc": "2026-06-08 00:00:00 UTC", "outcome": "no_entry"}]),
        generated_at_utc=pd.Timestamp("2026-06-08T00:00:00Z").to_pydatetime(),
    )

    assert ev_only.iloc[0]["latest_source"] == "evaluations"
    assert ev_only.iloc[0]["source"] == "evaluations"
    assert pending_only.iloc[0]["latest_source"] == "pending_reevaluations"
    assert pending_only.iloc[0]["source"] == "pending_reevaluations"


def test_both_inputs_empty_returns_empty_view():
    latest = lev.build_latest_view(pd.DataFrame(), pd.DataFrame(), generated_at_utc=pd.Timestamp("2026-06-08T00:00:00Z").to_pydatetime())

    assert latest.empty


def test_summary_counts_latest_rows():
    latest = pd.DataFrame(
        [
            {"signal_id": "S001", "latest_source": "pending_reevaluations", "evaluation_status": "closed", "outcome": "win_tp1", "missed_opportunity": False},
            {"signal_id": "S002", "latest_source": "evaluations", "evaluation_status": "pending", "outcome": "no_entry", "missed_opportunity": True},
        ]
    )

    summary = lev.summary_payload(
        latest,
        pd.DataFrame([{"signal_id": "S002"}]),
        pd.DataFrame([{"signal_id": "S001"}]),
        generated_at_utc=pd.Timestamp("2026-06-08T00:00:00Z").to_pydatetime(),
        source="local_csv",
    )

    assert summary["unique_signal_count"] == 2
    assert summary["latest_from_pending_reevaluations"] == 1
    assert summary["latest_from_evaluations"] == 1
    assert summary["win_tp1_count"] == 1
    assert summary["no_entry_count"] == 1
    assert summary["missed_opportunity_count"] == 1


def test_dedupe_columns_merges_duplicate_signal_id_columns():
    df = pd.DataFrame([["", "S001", "BTC"]], columns=["signal_id", "signal_id", "asset"])

    out = lev.dedupe_columns(df, "TEST")

    assert list(out.columns) == ["signal_id", "asset"]
    assert out.iloc[0]["signal_id"] == "S001"


def test_dedupe_columns_uses_leftmost_non_empty_value():
    df = pd.DataFrame([["nan", "S001"], ["S002", "S002-alt"], [None, "S003"]], columns=["signal_id", "signal_id"])

    out = lev.dedupe_columns(df, "TEST")

    assert out["signal_id"].tolist() == ["S001", "S002", "S003"]


def test_duplicate_columns_in_evaluations_do_not_break_latest_view():
    evaluations = pd.DataFrame(
        [["", "S001", "2026-06-07", "open_unresolved"]],
        columns=["signal_id", "signal_id", "evaluation_date", "outcome"],
    )
    pending = pd.DataFrame([{"signal_id": "S002", "reevaluation_at_utc": "2026-06-08 00:00:00 UTC", "outcome": "win_tp1"}])

    latest = lev.build_latest_view(evaluations, pending, generated_at_utc=pd.Timestamp("2026-06-08T00:00:00Z").to_pydatetime())

    assert set(latest["signal_id"]) == {"S001", "S002"}


def test_duplicate_columns_in_pending_reevaluations_do_not_break_latest_view():
    evaluations = pd.DataFrame([{"signal_id": "S001", "evaluation_date": "2026-06-07", "outcome": "open_unresolved"}])
    pending = pd.DataFrame(
        [["", "S001", "2026-06-08 07:05:00 JST", "win_tp2"]],
        columns=["signal_id", "signal_id", "reevaluation_at_jst", "outcome"],
    )

    latest = lev.build_latest_view(evaluations, pending, generated_at_utc=pd.Timestamp("2026-06-08T00:00:00Z").to_pydatetime())

    assert len(latest) == 1
    assert latest.iloc[0]["signal_id"] == "S001"
    assert latest.iloc[0]["outcome"] == "win_tp2"
    assert latest.iloc[0]["latest_source"] == "pending_reevaluations"
