"""監査F9 (2026-09-06) の再現テスト: 未決着件数だけで成績の確信度を上げない。

監査の実測: BTC の open_unresolved / R欠損 30件だけで confidence が 0.35 → 0.86。
allocation_score は 40 のままなので、この入力単独で配分が起きるわけではないが、
他のスコアが有効になると配分の重みへ流入する。
"""
import pandas as pd
import pytest

import build_portfolio_layer as pl


def _unresolved(n, asset="BTC"):
    return [{"asset": asset, "outcome": "open_unresolved", "status": "pending",
             "r_multiple": 0.0, "missed_opportunity": False} for _ in range(n)]


def _decided(n, asset="BTC", win=True):
    return [{"asset": asset, "outcome": "win_tp1" if win else "loss_sl", "status": "closed",
             "r_multiple": 1.0 if win else -1.0, "missed_opportunity": False} for _ in range(n)]


def test_unresolved_rows_do_not_raise_confidence():
    score, conf, note = pl.evaluation_component(pd.DataFrame(_unresolved(30)), "BTC")
    assert conf == pytest.approx(0.30), "未決着30件だけで確信度が上がってはいけない"
    assert "decided=0/30" in note, "決着数と行数を並べて出す"


def test_confidence_tracks_decided_rows_only():
    df = pd.DataFrame(_decided(6) + _unresolved(30))
    _, conf, note = pl.evaluation_component(df, "BTC")
    _, conf_alone, _ = pl.evaluation_component(pd.DataFrame(_decided(6)), "BTC")
    assert conf == conf_alone, "未決着行を足しても確信度は動かない"
    assert "decided=6/36" in note


def test_avg_r_is_not_diluted_by_unresolved_zeros():
    """未決着行の r_multiple=0.0 が平均Rを薄めない。"""
    score_clean, _, _ = pl.evaluation_component(pd.DataFrame(_decided(4)), "BTC")
    score_padded, _, _ = pl.evaluation_component(pd.DataFrame(_decided(4) + _unresolved(20)), "BTC")
    assert score_clean == pytest.approx(score_padded)


def test_confidence_still_grows_with_real_results():
    """機能を殺していないこと: 決着が増えれば確信度は上がる。"""
    confs = [pl.evaluation_component(pd.DataFrame(_decided(n)), "BTC")[1] for n in (3, 12, 30, 60)]
    assert confs == sorted(confs)
    assert confs[0] < confs[-1]
    assert confs[-1] == pytest.approx(0.80)


def test_losses_count_as_decided():
    _, conf, note = pl.evaluation_component(pd.DataFrame(_decided(10, win=False)), "BTC")
    assert "decided=10/10" in note
    assert conf > 0.30, "負けも決着であり確信度に寄与する"


def test_empty_and_missing_asset_keep_low_confidence():
    assert pl.evaluation_component(pd.DataFrame(), "BTC")[1] == 0.35
    assert pl.evaluation_component(pd.DataFrame(_decided(5, asset="GOLD")), "BTC")[1] == 0.35
