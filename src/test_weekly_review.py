from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import build_weekly_review as weekly


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_weekly_review_prefers_prediction_log_over_stale_latest(monkeypatch, tmp_path: Path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("GOOGLE_SERVICE_ACCOUNT_JSON", raising=False)
    monkeypatch.delenv("GOOGLE_SHEET_ID", raising=False)

    write(
        tmp_path / "results" / "signals.csv",
        "date,signal_id,asset,side,rank\n"
        "2026-07-08,STALE-SIGNAL,BTC,NONE,NO_TRADE\n",
    )
    write(
        tmp_path / "results" / "evaluations.csv",
        "signal_id,signal_date,evaluation_status,r_result,asset,side,rank\n"
        "STALE-SIGNAL,2026-07-08,skipped,0,BTC,NONE,NO_TRADE\n",
    )
    write(
        tmp_path / "results" / "latest_evaluations.csv",
        "signal_id,signal_date,evaluation_status,r_result,asset,side,rank\n"
        "STALE-SIGNAL,2026-07-08,skipped,0,BTC,NONE,NO_TRADE\n",
    )
    write(tmp_path / "results" / "market_snapshot.csv", "date,asset,close\n2026-08-28,BTC,100\n")
    write(
        tmp_path / "data" / "signal_log.csv",
        "date,signal_id,asset,side,rank,origin\n"
        "2026-08-28,LOG-BTC,BTC,BUY,B,chatgpt_app\n"
        "2026-08-28,LOG-DXY,DXY,NONE,NO_TRADE,chatgpt_app\n"
        "2026-08-28,LOG-WTI,WTI,NONE,NO_TRADE,chatgpt_app\n",
    )
    write(
        tmp_path / "data" / "prediction_log_scores.csv",
        "date,signal_id,asset,side,rank,status,result_5d,result_10d,r_close_5d\n"
        "2026-08-28,LOG-BTC,BTC,LONG,B,awaiting_horizon,awaiting,awaiting,\n"
        "2026-08-28,LOG-DXY,DXY,NONE,NO_TRADE,awaiting_horizon,not_applicable,not_applicable,\n"
        "2026-08-28,LOG-WTI,WTI,NONE,NO_TRADE,awaiting_horizon,not_applicable,not_applicable,\n",
    )

    review, report_path = weekly.build_review(pd.Timestamp("2026-08-24"), pd.Timestamp("2026-08-30"))

    row = review.iloc[0]
    assert int(row["total_signals"]) == 3
    assert int(row["b_signals"]) == 1
    assert int(row["no_trade_signals"]) == 2
    assert int(row["pending_signals"]) == 3
    assert row["signal_source"] == "prediction_log"
    assert row["evaluation_source"] == "prediction_log_scores"
    assert not bool(row["latest_evaluations_available"])
    assert int(row["prediction_awaiting_rows"]) == 3
    assert row["rule_change_1"] == "予測ログは評価期間中（awaiting_horizon）"
    assert row["best_asset"] == ""
    assert row["worst_asset"] == ""
    assert "シグナル集計ソース: prediction_log" in Path(report_path).read_text(encoding="utf-8")


def test_weekly_review_uses_live_signals_when_prediction_log_missing(monkeypatch, tmp_path: Path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("GOOGLE_SERVICE_ACCOUNT_JSON", raising=False)
    monkeypatch.delenv("GOOGLE_SHEET_ID", raising=False)

    write(
        tmp_path / "results" / "signals.csv",
        "date,signal_id,asset,side,rank\n"
        "2026-08-28,LIVE-GOLD,GOLD,LONG,A\n",
    )
    write(
        tmp_path / "results" / "evaluations.csv",
        "signal_id,signal_date,evaluation_status,r_result,asset,side,rank\n"
        "LIVE-GOLD,2026-08-28,closed,1.2,GOLD,LONG,A\n",
    )
    write(tmp_path / "results" / "market_snapshot.csv", "date,asset,close\n2026-08-28,GOLD,100\n")

    review, _ = weekly.build_review(pd.Timestamp("2026-08-24"), pd.Timestamp("2026-08-30"))

    row = review.iloc[0]
    assert int(row["total_signals"]) == 1
    assert int(row["a_signals"]) == 1
    assert int(row["closed_signals"]) == 1
    assert row["signal_source"] == "signals"
    assert row["evaluation_source"] == "evaluations"
    assert float(row["total_r"]) == 1.2


def test_best_worst_asset_ignores_assets_without_closed_results():
    table = pd.DataFrame(
        [
            {"asset": "BTC", "closed": 0, "total_r": 0.0},
            {"asset": "GOLD", "closed": 0, "total_r": 0.0},
        ]
    )

    assert weekly.best_worst_asset(table) == ("", "")


def test_prediction_scores_non_actionable_rows_do_not_enter_closed_metrics():
    # #125 Codex P2: NO_TRADE等もstatus=scoredになるため、空白Rのままclosedに写すと
    # 勝率の分母が薄まる。closed=scoredかつ数値Rの行のみ。
    scores = pd.DataFrame([
        {"signal_id": "A", "status": "scored", "r_close_5d": 0.5},
        {"signal_id": "B", "status": "scored", "r_close_5d": ""},        # NO_TRADE行
        {"signal_id": "C", "status": "awaiting_horizon", "r_close_5d": ""},
        {"signal_id": "D", "status": "invalid_data", "r_close_5d": ""},
    ])
    ev = weekly.prediction_scores_to_evaluations(scores)
    m = weekly.r_metrics(ev)
    assert m["closed_count"] == 1
    assert m["win_rate"] == 1.0
    by_id = ev.set_index("signal_id")["evaluation_status"]
    assert by_id["B"] == "not_applicable"
    assert by_id["C"] == "pending"
    assert by_id["D"] == "skipped"


def test_ledger_sides_normalized_before_side_table():
    # #125 Codex P2: 台帳はBUY/SELL表記、集計表はLONG/SHORT/NONEを要求。
    # 正規化せずに渡すとactionableな判断がside別集計で全て0件になる。
    ledger = pd.DataFrame([
        {"signal_id": "A", "side": "BUY"},
        {"signal_id": "B", "side": "SELL"},
        {"signal_id": "C", "side": "NONE"},
    ])
    out_sig, _, meta = weekly.select_weekly_inputs(
        pd.DataFrame(), pd.DataFrame(), ledger, pd.DataFrame())
    assert meta["signal_source"] == "prediction_log"
    assert list(out_sig["side"]) == ["LONG", "SHORT", "NONE"]
