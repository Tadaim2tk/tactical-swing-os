from __future__ import annotations

from pathlib import Path

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


def test_default_sheets_result_skips_when_not_requested():
    result = rps.default_sheets_result(False)

    assert result["write_sheets_requested"] is False
    assert result["write_sheets_status"] == "skipped"
    assert result["sheets_appended_rows"] == 0


def test_write_sheets_missing_secrets_skips_without_error(monkeypatch, tmp_path):
    monkeypatch.delenv("GOOGLE_SERVICE_ACCOUNT_JSON", raising=False)
    monkeypatch.delenv("GOOGLE_SHEET_ID", raising=False)
    csv_path = tmp_path / "pending_reevaluations.csv"
    pd.DataFrame([{"reevaluation_run_id": "run-1", "signal_id": "S001"}]).to_csv(csv_path, index=False)

    result = rps.append_pending_reevaluations_to_sheets(csv_path)

    assert result["write_sheets_requested"] is True
    assert result["write_sheets_status"] == "skipped"
    assert result["sheets_appended_rows"] == 0
    assert "missing" in result["sheets_error"]


def test_summary_payload_includes_sheets_metadata():
    rows = pd.DataFrame([{"signal_id": "S001", "outcome": "win_tp1", "evaluation_status": "closed", "missed_opportunity": False}])
    sheets = rps.default_sheets_result(True)
    sheets.update({"write_sheets_status": "success", "sheets_appended_rows": 1, "sheets_skipped_duplicates": 2})

    payload = rps.build_summary_payload(
        rows,
        generated_at_utc=pd.Timestamp("2026-06-08T00:00:00Z").to_pydatetime(),
        source="local_csv",
        total_signals=3,
        target_count=1,
        run_id="run-1",
        sheets_result=sheets,
    )

    assert payload["write_sheets_requested"] is True
    assert payload["write_sheets_status"] == "success"
    assert payload["sheets_appended_rows"] == 1
    assert payload["sheets_skipped_duplicates"] == 2


def test_dashboard_workflow_does_not_write_sheets():
    workflow = Path(".github/workflows/dashboard.yml").read_text(encoding="utf-8")
    reevaluate_lines = [line for line in workflow.splitlines() if "reevaluate_pending_signals.py" in line]

    assert reevaluate_lines, "dashboard workflow should run pending reevaluation for display"
    assert all("--write-sheets" not in line for line in reevaluate_lines)


# === 2026-07-09 サンプル廃棄監査の回帰テスト(設計書§6) ===

def _sig(sid, date, side="LONG", rank="B"):
    return {"signal_id": sid, "date": date, "asset": "WTI", "side": side, "rank": rank,
            "entry_low": 70.0, "entry_high": 71.0, "sl": 68.0, "tp1": 75.0, "tp2": 78.0}


def _open_eval(sid):
    return {"signal_id": sid, "outcome": "open_unresolved", "status": "pending",
            "evaluation_status": "pending", "reevaluation_count": 0}


def _closed_eval(sid):
    return {"signal_id": sid, "outcome": "win_tp1", "status": "closed",
            "evaluation_status": "closed", "reevaluation_count": 1}


def test_aged_open_rows_are_kept_not_discarded():
    # 最新シグナルから30日超の古い行でも、評価が未確定なら対象に残る
    signals = pd.DataFrame([_sig("old1", "2026-05-01"), _sig("new1", "2026-07-01")])
    evaluations = pd.DataFrame([_open_eval("old1"), _open_eval("new1")])
    targets, _ = rps.select_reevaluation_targets(signals, evaluations, lookback_days=30, include_no_trade=True)
    ids = set(targets["signal_id"])
    assert "old1" in ids  # 廃棄されない
    assert "new1" in ids
    assert targets.attrs.get("aged_open_kept", 0) == 1  # 窓外救済を可視化


def test_closed_old_rows_are_skipped_not_reevaluated():
    signals = pd.DataFrame([_sig("old2", "2026-05-01")])
    evaluations = pd.DataFrame([_closed_eval("old2")])
    targets, _ = rps.select_reevaluation_targets(signals, evaluations, lookback_days=30, include_no_trade=True)
    assert targets.empty  # 確定済みは再評価不要(これは廃棄ではない)


def test_no_trade_included_by_default_argparse():
    # 既定で NO_TRADE も再評価対象(見送り判断の no_trade_correct/missed を確定させる)
    import sys
    argv = sys.argv
    try:
        sys.argv = ["reevaluate_pending_signals.py"]
        args = rps.parse_args()
        assert args.include_no_trade is True
        sys.argv = ["reevaluate_pending_signals.py", "--no-include-no-trade"]
        assert rps.parse_args().include_no_trade is False
    finally:
        sys.argv = argv


def test_no_trade_rows_selected_when_included():
    signals = pd.DataFrame([_sig("nt1", "2026-07-01", side="NONE", rank="NO_TRADE")])
    evaluations = pd.DataFrame([_open_eval("nt1")])
    targets, _ = rps.select_reevaluation_targets(signals, evaluations, lookback_days=30, include_no_trade=True)
    assert "nt1" in set(targets["signal_id"])
