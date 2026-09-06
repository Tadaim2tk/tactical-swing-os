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
