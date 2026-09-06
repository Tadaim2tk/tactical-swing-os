"""監査F6 (2026-09-06) の再現テスト: 5日成績の分母は5日の確定条件で決める。

旧実装は値に r_close_5d を採る一方、採否条件に status=scored(全horizon完了=10日まで確定)
を使っていた。そのため「5日は確定しているのに週次では pending」という行が出ていた。
実データ702行中13件が status=awaiting_horizon かつ result_5d ∈ {success, failure}。
"""
import pandas as pd

import build_weekly_review as w


def _scores(rows):
    return pd.DataFrame([{
        "date": "2026-09-01", "signal_id": r["sid"], "asset": "GOLD",
        "side": r.get("side", "LONG"), "rank": r.get("rank", "B"),
        "status": r["status"], "result_5d": r["result_5d"],
        "result_10d": r.get("result_10d", "awaiting"), "r_close_5d": r.get("r5", ""),
    } for r in rows])


def test_five_day_result_closes_without_waiting_for_ten_day():
    """監査の中心的所見: 10日の確定を待たない。"""
    ev = w.prediction_scores_to_evaluations(_scores([
        {"sid": "a", "status": "awaiting_horizon", "result_5d": "success", "r5": 1.2},
        {"sid": "b", "status": "awaiting_horizon", "result_5d": "failure", "r5": -0.8},
    ]))
    assert list(ev["evaluation_status"]) == ["closed", "closed"]


def test_awaiting_five_day_stays_pending():
    ev = w.prediction_scores_to_evaluations(_scores([
        {"sid": "a", "status": "awaiting_horizon", "result_5d": "awaiting", "r5": ""},
    ]))
    assert ev["evaluation_status"].iloc[0] == "pending"


def test_not_applicable_is_not_pending():
    """方向Rを持ちようがない行を「これから決着する」と数えない。"""
    ev = w.prediction_scores_to_evaluations(_scores([
        {"sid": "n1", "status": "awaiting_horizon", "result_5d": "not_applicable",
         "side": "NONE", "rank": "NO_TRADE"},
        {"sid": "n2", "status": "scored", "result_5d": "not_applicable",
         "side": "NONE", "rank": "NO_TRADE"},
    ]))
    assert list(ev["evaluation_status"]) == ["not_applicable", "not_applicable"]


def test_suspect_data_is_skipped_not_closed():
    """水準取り違えの隔離行を成績に混ぜない。"""
    ev = w.prediction_scores_to_evaluations(_scores([
        {"sid": "s", "status": "scored", "result_5d": "suspect_data", "r5": 12.0},
    ]))
    assert ev["evaluation_status"].iloc[0] == "skipped"


def test_horizon_is_recorded_on_the_frame():
    """どのhorizonのRを採ったかを行に残す(同名の数字が同じ量とは限らないため)。"""
    ev = w.prediction_scores_to_evaluations(_scores([
        {"sid": "a", "status": "scored", "result_5d": "success", "r5": 1.0},
    ]))
    assert ev["r_horizon"].iloc[0] == "5d"


def test_invalid_status_still_skipped():
    ev = w.prediction_scores_to_evaluations(_scores([
        {"sid": "i", "status": "invalid_data", "result_5d": "success", "r5": 1.0},
    ]))
    assert ev["evaluation_status"].iloc[0] == "skipped"
