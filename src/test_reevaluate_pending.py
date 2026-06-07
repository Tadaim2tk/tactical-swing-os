from __future__ import annotations

import pandas as pd

import reevaluate_pending_signals as rps


def signal_rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"signal_id": "pending-1", "date": "2026-06-01", "asset": "BTC", "side": "LONG", "rank": "B"},
            {"signal_id": "closed-1", "date": "2026-06-01", "asset": "GOLD", "side": "LONG", "rank": "A"},
            {"signal_id": "missing-eval", "date": "2026-06-01", "asset": "WTI", "side": "SHORT", "rank": "B"},
            {"signal_id": "no-trade-1", "date": "2026-06-01", "asset": "SPX", "side": "NONE", "rank": "NO_TRADE"},
        ]
    )


def evaluation_rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"signal_id": "pending-1", "evaluation_date": "2026-06-02", "status": "open", "evaluation_status": "pending", "outcome": "open_unresolved", "r_multiple": "0.1"},
            {"signal_id": "pending-1", "evaluation_date": "2026-06-03", "status": "no_entry", "evaluation_status": "pending", "outcome": "no_entry", "r_multiple": "0"},
            {"signal_id": "closed-1", "evaluation_date": "2026-06-02", "status": "closed", "evaluation_status": "closed", "outcome": "win_tp1", "r_multiple": "1.2"},
            {"signal_id": "no-trade-1", "evaluation_date": "2026-06-02", "status": "no_trade", "evaluation_status": "skipped", "outcome": "no_trade_correct", "r_multiple": "0"},
        ]
    )


def test_selects_open_and_missing_evaluations_only_by_default():
    targets, latest = rps.select_reevaluation_targets(
        signal_rows(),
        evaluation_rows(),
        lookback_days=30,
        include_no_trade=False,
    )

    assert set(targets["signal_id"]) == {"pending-1", "missing-eval"}
    assert len(latest) == 3
    latest_pending = latest[latest["signal_id"] == "pending-1"].iloc[0]
    assert latest_pending["outcome"] == "no_entry"


def test_include_no_trade_allows_unseen_no_trade_signal():
    signals = pd.concat(
        [
            signal_rows(),
            pd.DataFrame([{"signal_id": "no-trade-new", "date": "2026-06-01", "asset": "SPX", "side": "NONE", "rank": "NO_TRADE"}]),
        ],
        ignore_index=True,
    )
    targets, _ = rps.select_reevaluation_targets(
        signals,
        evaluation_rows(),
        lookback_days=30,
        include_no_trade=True,
    )

    assert "no-trade-new" in set(targets["signal_id"])
    assert "no-trade-1" not in set(targets["signal_id"])


def test_changed_outcome_flag_uses_latest_previous_row():
    base = pd.DataFrame(
        [
            {
                "signal_id": "pending-1",
                "status": "closed",
                "evaluation_status": "closed",
                "outcome": "win_tp1",
                "r_multiple": 1.0,
            }
        ]
    ).reindex(columns=rps.EVALUATION_COLUMNS)
    _, latest = rps.select_reevaluation_targets(
        signal_rows(),
        evaluation_rows(),
        lookback_days=30,
        include_no_trade=False,
    )

    annotated = rps.annotate_reevaluations(
        base,
        latest,
        source="local_csv",
        run_id="test-run",
        generated_at_utc=pd.Timestamp("2026-06-08T00:00:00Z").to_pydatetime(),
    )

    row = annotated.iloc[0]
    assert row["previous_outcome"] == "no_entry"
    assert bool(row["changed_outcome"]) is True
    assert bool(row["changed_status"]) is True
    assert bool(row["is_latest_evaluation"]) is True
