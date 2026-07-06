"""Shadow outcome linkage (Phase 29.5) の単体テスト。

設計書 docs/phase29_design_reasoning.md §1 の統計判断を固定する:
1. 4分類ペアの diff（同一/skip/追加/両NO_TRADE）
2. ゼロ込みペア（除外しない・選択バイアス防止）と divergent の併記
3. 未確定は awaiting、反実仮想不能は uncomputable として除外+計数（0と置かない）
4. 版フィルタと再実行の冪等性（awaiting→確定の上書き）
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import link_shadow_outcomes as lo


def _shadow_row(sid="s1", base_rank="A", weighted_rank="A", side="LONG", asset="SPX", version="v1"):
    return {"signal_id": sid, "asset": asset, "side": side, "date": "2026-06-01",
            "base_rank": base_rank, "weighted_rank": weighted_rank, "weights_version": version}


def _eval_row(sid="s1", r_result=1.5, entry_hit=True, bars=10, asset="SPX"):
    return {"signal_id": sid, "asset": asset, "signal_date": "2026-06-01", "type": "T",
            "entry_low": 100.0, "entry_high": 102.0, "sl": 95.0, "tp1": 110.0, "tp2": 115.0,
            "r_result": r_result, "entry_hit": entry_hit, "bars_checked": bars}


def _pairs(shadow_rows, eval_rows, loader=None):
    return lo.build_pairs(
        pd.DataFrame(shadow_rows), pd.DataFrame(eval_rows),
        horizon=10, ohlcv_loader=loader or (lambda a: pd.DataFrame()), linked_at="t",
    )


# === 1. 4分類 ===

def test_same_action_diff_zero():
    rows, counts = _pairs([_shadow_row()], [_eval_row(r_result=2.0)])
    assert counts["pairs_linked"] == 1
    r = rows.iloc[0]
    assert r["pair_type"] == "same_action"
    assert r["base_r"] == 2.0 and r["weighted_r"] == 2.0 and r["diff"] == 0.0


def test_weighted_skipped_is_minus_base_r():
    rows, _ = _pairs([_shadow_row(weighted_rank="NO_TRADE")], [_eval_row(r_result=-1.0)])
    r = rows.iloc[0]
    assert r["pair_type"] == "weighted_skipped"
    assert r["diff"] == 1.0  # 負けトレードを見送った -> +1.0 の改善


def test_both_no_trade_zero_included():
    # side=NONE でも base_rank/weighted_rank 両方非actionableなら 0 ペアとして「含める」
    rows, counts = _pairs([_shadow_row(base_rank="NO_TRADE", weighted_rank="NO_TRADE")], [_eval_row()])
    assert counts["pairs_linked"] == 1
    assert rows.iloc[0]["pair_type"] == "both_no_trade"
    assert rows.iloc[0]["diff"] == 0.0


def test_weighted_added_uses_hypothetical_r(tmp_path):
    # 上昇して TP1 に到達する合成価格 -> 反実仮想Rが正になる
    dates = pd.bdate_range("2026-06-01", periods=15)
    close = np.linspace(101, 112, 15)
    df = pd.DataFrame({"date": dates, "open": close, "high": close + 1, "low": close - 1,
                       "close": close, "volume": 100})
    p = tmp_path / "SPX.csv"
    p.write_text(df.to_csv(index=False), encoding="utf-8")

    from evaluate_signal import load_ohlcv as _  # 実loaderは使わずローカル読み込み
    def loader(asset):
        raw = pd.read_csv(p)
        raw["date"] = pd.to_datetime(raw["date"])
        return raw

    rows, counts = _pairs(
        [_shadow_row(base_rank="NO_TRADE", weighted_rank="A")],
        [_eval_row(r_result=None, entry_hit=False)],
        loader=loader,
    )
    assert counts["pairs_linked"] == 1
    r = rows.iloc[0]
    assert r["pair_type"] == "weighted_added"
    assert r["base_r"] == 0.0
    assert r["diff"] == r["weighted_r"]  # base=0 なので diff=仮想R
    assert pd.notna(r["weighted_r"])


# === 3. 正直な除外 ===

def test_awaiting_excluded_and_counted():
    rows, counts = _pairs([_shadow_row()], [_eval_row(r_result=None, entry_hit=True, bars=3)])
    assert rows.empty
    assert counts["awaiting"] == 1


def test_no_fill_closed_window_is_zero_not_awaiting():
    rows, counts = _pairs([_shadow_row()], [_eval_row(r_result=None, entry_hit=False, bars=10)])
    assert counts["pairs_linked"] == 1
    assert rows.iloc[0]["base_r"] == 0.0  # 窓が閉じてentry不成立 = 正当なゼロ


def test_uncomputable_counterfactual_excluded_and_counted():
    rows, counts = _pairs(
        [_shadow_row(base_rank="NO_TRADE", weighted_rank="A")],
        [_eval_row(r_result=None, entry_hit=False)],
        loader=lambda a: pd.DataFrame(),  # 価格が読めない -> uncomputable
    )
    assert rows.empty
    assert counts["uncomputable_counterfactual"] == 1


def test_missing_evaluation_counted():
    rows, counts = _pairs([_shadow_row(sid="sX")], [_eval_row(sid="sY")])
    assert rows.empty
    assert counts["missing_evaluation"] == 1


# === 4. 台帳と版フィルタ ===

def test_append_dedupe_and_version_filter(tmp_path):
    path = tmp_path / "diffs.csv"
    a = pd.DataFrame([{**{c: "" for c in lo.DIFF_COLUMNS},
                       "signal_id": "s1", "weights_version": "v1", "diff": 0.0, "date": "2026-06-01"}])
    b = pd.DataFrame([{**{c: "" for c in lo.DIFF_COLUMNS},
                       "signal_id": "s1", "weights_version": "v1", "diff": 0.5, "date": "2026-06-01"},
                      {**{c: "" for c in lo.DIFF_COLUMNS},
                       "signal_id": "s2", "weights_version": "v2", "diff": -0.3, "date": "2026-06-02"}])
    lo.append_diffs(a, path)
    merged = lo.append_diffs(b, path)
    assert len(merged) == 2  # s1/v1 は最新(0.5)で上書き
    diffs_v1, div_v1 = lo.diffs_for_version("v1", path)
    assert diffs_v1 == [0.5] and div_v1 == 1
    diffs_v2, div_v2 = lo.diffs_for_version("v2", path)
    assert diffs_v2 == [-0.3] and div_v2 == 1
    assert lo.diffs_for_version("v9", path) == ([], 0)


def test_divergent_counts_only_nonzero(tmp_path):
    path = tmp_path / "diffs.csv"
    rows = pd.DataFrame([{**{c: "" for c in lo.DIFF_COLUMNS},
                          "signal_id": f"s{i}", "weights_version": "v1",
                          "diff": 0.0 if i < 8 else 0.7, "date": "2026-06-01"} for i in range(10)])
    lo.append_diffs(rows, path)
    diffs, divergent = lo.diffs_for_version("v1", path)
    assert len(diffs) == 10   # ゼロ込みで系列に含める(設計書 §1.2)
    assert divergent == 2     # 決定が変わったのは2件、と必ず併記


# === ゲート統合: identity なら全ゼロ -> zero_difference で blocked ===

def test_gate_receives_zero_series_and_blocks():
    import shadow_weights as sw
    gate = sw.evaluate_promotion_gate([0.0] * 40, comparisons_accumulated=40)
    assert gate["decision"] == "blocked"
    assert any(r.startswith("zero_difference") for r in gate["blocked_reasons"])


def test_safety_fields():
    assert lo.SAFETY_FIELDS["shadow_mode"] is True
    assert lo.SAFETY_FIELDS["affects_live_recommendation"] is False
    assert lo.SAFETY_FIELDS["weights_json_updated"] is False
