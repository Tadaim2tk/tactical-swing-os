"""監査F1 (2026-09-06) の再現テスト: 評価不能の0Rが提案の向きを反転させないこと。

監査の実測:
  正常5件(全て+1R)          → n=5  勝率100% 平均+1R   confidence=low  提案 increase +0.03
  同じ5件 + 評価不能20件     → n=25 勝率20%  平均+0.2R confidence=high 提案 decrease -0.0507

evaluate_signal は日付不正・データ欠損・ホライズン未到達の行にも r_multiple=0.0 を入れる。
その 0 は「損益ゼロ」ではなく「測れなかった」であり、実績に混ぜると負けと同じ働きをする。
"""
import pandas as pd
import pytest

import propose_model_state_updates as ms


def _win_rows(n=5):
    return [{"outcome": "win_tp1", "evaluation_status": "closed", "status": "closed",
             "error_type": "", "r_multiple": 1.0, "missed_opportunity": False} for _ in range(n)]


def _unevaluable_rows(n=20, error_type="invalid_signal_date"):
    # evaluate_signal.no_trade_result が実際に返す形（r_multiple=0.0 が入る）
    return [{"outcome": "invalid" if error_type == "invalid_signal_date" else "no_trade",
             "evaluation_status": "skipped", "status": "invalid" if error_type == "invalid_signal_date" else "no_trade",
             "error_type": error_type, "r_multiple": 0.0, "missed_opportunity": False} for _ in range(n)]


def test_clean_wins_are_unchanged():
    m = ms.metrics_from_frame(pd.DataFrame(_win_rows(5)))
    assert m["sample_count"] == 5
    assert m["recorded_count"] == 5
    assert m["unevaluable_count"] == 0
    assert m["win_rate"] == 1.0
    assert m["avg_r"] == pytest.approx(1.0)


@pytest.mark.parametrize("error_type", sorted(ms.UNEVALUABLE_ERROR_TYPES))
def test_unevaluable_rows_do_not_dilute_win_rate(error_type):
    df = pd.DataFrame(_win_rows(5) + _unevaluable_rows(20, error_type))
    m = ms.metrics_from_frame(df)
    # 測れた集合だけが成績になる
    assert m["sample_count"] == 5, "標本数に評価不能行を数えない"
    assert m["win_rate"] == 1.0, "評価不能行が負けとして勝率を薄めない"
    assert m["avg_r"] == pytest.approx(1.0), "0R が平均を引き下げない"
    assert m["total_r"] == pytest.approx(5.0)
    # 記録は捨てない
    assert m["recorded_count"] == 25
    assert m["unevaluable_count"] == 20


def test_confidence_does_not_inflate_from_unevaluable_rows():
    """信頼度は測れた件数で決まる。評価不能行で high にならない。"""
    clean = ms.metrics_from_frame(pd.DataFrame(_win_rows(5)))
    padded = ms.metrics_from_frame(pd.DataFrame(_win_rows(5) + _unevaluable_rows(20)))
    assert ms.confidence_level(clean["sample_count"]) == ms.confidence_level(padded["sample_count"])
    assert ms.confidence_level(padded["sample_count"]) != "high"


def test_proposal_direction_does_not_flip():
    """監査の中心的な所見: 測れなかった行だけで increase → decrease に反転していた。"""
    clean = ms.metrics_from_frame(pd.DataFrame(_win_rows(5)))
    padded = ms.metrics_from_frame(pd.DataFrame(_win_rows(5) + _unevaluable_rows(20)))
    d_clean = ms.direction_from_metrics(clean["sample_count"], clean["avg_r"], clean["win_rate"])
    d_padded = ms.direction_from_metrics(padded["sample_count"], padded["avg_r"], padded["win_rate"])
    assert d_clean == d_padded, f"評価不能行だけで方向が {d_clean} → {d_padded} に変わってはいけない"
    assert ms.max_allowed_delta(padded["sample_count"]) <= ms.max_allowed_delta(5)


def test_unevaluable_rows_are_not_closed():
    df = pd.DataFrame(_win_rows(5) + _unevaluable_rows(20))
    closed = ms.closed_mask(df)
    assert int(closed.sum()) == 5, "r_multiple=0.0 だけで closed に混入しない"


def test_all_unevaluable_frame_reports_zero_sample_not_zero_performance():
    m = ms.metrics_from_frame(pd.DataFrame(_unevaluable_rows(12)))
    assert m["sample_count"] == 0
    assert m["recorded_count"] == 12
    assert m["unevaluable_count"] == 12
    assert ms.direction_from_metrics(m["sample_count"], m["avg_r"], m["win_rate"]) == "hold"


# === #145 Codex P1: 確定した見送り評価を母集団から落とさない ===================
# no_trade_result は no_trade_correct / no_trade_missed にも evaluation_status="skipped"
# を付ける(evaluate_signal.py)。skipped を一律に評価不能とすると、正しく採点できた
# 見送りまで消え、NONE/NO_TRADE の side・rank・type 提案が insufficient_samples になる。

def _finalized_no_trade_rows(n=6, outcome="no_trade_correct"):
    return [{"outcome": outcome, "evaluation_status": "skipped", "status": "no_trade",
             "error_type": "no_trade", "r_multiple": 0.0, "missed_opportunity": outcome == "no_trade_missed"}
            for _ in range(n)]


@pytest.mark.parametrize("outcome", ["no_trade_correct", "no_trade_missed"])
def test_finalized_no_trade_stays_measurable(outcome):
    df = pd.DataFrame(_finalized_no_trade_rows(6, outcome))
    assert int(ms.unevaluable_mask(df).sum()) == 0, "skipped だけを理由に落とさない"
    m = ms.metrics_from_frame(df)
    assert m["sample_count"] == 6
    assert m["unevaluable_count"] == 0


def test_finalized_no_trade_reaches_confidence_and_direction():
    """観測された見送りの結果がモデル更新に届く（提案が insufficient_data で死なない）。"""
    df = pd.DataFrame(_finalized_no_trade_rows(12))
    m = ms.metrics_from_frame(df)
    assert ms.confidence_level(m["sample_count"]) != "insufficient_data"
    assert ms.max_allowed_delta(m["sample_count"]) > 0.0


def test_unresolved_rows_are_not_measurable():
    """まだ決着していない行は「測れなかった」ではなく「これから測る」。母集団に入れない。"""
    rows = [{"outcome": "open_unresolved", "evaluation_status": "pending", "status": "pending",
             "error_type": "awaiting_horizon", "r_multiple": 0.0, "missed_opportunity": False}
            for _ in range(9)]
    df = pd.DataFrame(_win_rows(4) + rows)
    m = ms.metrics_from_frame(df)
    assert m["sample_count"] == 4
    assert m["unevaluable_count"] == 9
    assert m["win_rate"] == 1.0


def test_mixed_frame_keeps_no_trade_and_drops_only_unevaluable():
    df = pd.DataFrame(_win_rows(3) + _finalized_no_trade_rows(4) + _unevaluable_rows(5))
    m = ms.metrics_from_frame(df)
    assert m["sample_count"] == 7, "勝ち3 + 確定見送り4"
    assert m["unevaluable_count"] == 5
    assert m["recorded_count"] == 12


def test_counts_reach_the_proposal_output():
    """F1の「記録は捨てない」が出力列まで届いていること。

    sample_count だけだと「測れなかった行が何件あったか」が読み手に見えない。
    実際、初版は metrics_from_frame に3つの数を持たせながら CSV には
    sample_count しか出しておらず、BTC が sample_count=0 とだけ見えていた。
    """
    import propose_model_state_updates as m
    for col in ("recorded_count", "unevaluable_count"):
        assert col in m.CSV_COLUMNS, f"{col} が出力列に無い"
    assert m.CSV_COLUMNS.index("sample_count") < m.CSV_COLUMNS.index("recorded_count")
