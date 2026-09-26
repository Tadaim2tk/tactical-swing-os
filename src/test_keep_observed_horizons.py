"""append_scores: 観測済みの horizon を、価格窓の短い再採点で空白に戻さない（#173 Codex P1）。

main は夜間ワークフローが毎日自分で価格を取って採点するため、手元より先まで埋まっている
ことがある。手元で再採点すると status は同格のままセルだけ空白になり、確定していた
result_5d が awaiting に戻っていた（2026-09-26: 5d が54行、3d が36行消えた）。
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import score_prediction_log as sp


def _row(**kw):
    base = {c: float("nan") for c in sp.SCORE_COLUMNS}
    base.update({"date": "2026-09-19", "signal_id": "S", "status": "awaiting_horizon"})
    base.update(kw)
    return base


def test_blank_rerun_does_not_erase_observed_cells(tmp_path):
    path = tmp_path / "scores.csv"
    pd.DataFrame([_row(fwd_return_5d=0.012, r_close_5d=0.8905, result_5d="success")]).to_csv(path, index=False)
    out = sp.append_scores(pd.DataFrame([_row(result_5d="awaiting")]), path)
    r = out.set_index("signal_id").loc["S"]
    assert abs(r["fwd_return_5d"] - 0.012) < 1e-9 and abs(r["r_close_5d"] - 0.8905) < 1e-9
    assert r["result_5d"] == "success", "確定を awaiting に戻さない"


def test_newer_observation_still_replaces(tmp_path):
    """空白ではない新しい観測は普通に採る。保護は『空白での上書き』だけ。"""
    path = tmp_path / "scores.csv"
    pd.DataFrame([_row(fwd_return_5d=0.012, result_5d="success")]).to_csv(path, index=False)
    out = sp.append_scores(pd.DataFrame([_row(fwd_return_5d=0.020, result_5d="success", status="scored")]), path)
    assert abs(out.set_index("signal_id").loc["S", "fwd_return_5d"] - 0.020) < 1e-9


def test_first_time_rows_are_unaffected(tmp_path):
    path = tmp_path / "scores.csv"
    out = sp.append_scores(pd.DataFrame([_row(fwd_return_1d=0.001)]), path)
    assert len(out) == 1
