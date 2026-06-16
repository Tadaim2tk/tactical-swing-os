"""jp_swing_evaluate.py のユニットテスト (JP-EVAL-001 rev2)。

設計仕様の確認事項:
  1. actual_execution_date フィールド名（旧 actual_entry_date / order_date は使わない）
  2. thesis_hit / timing_hit / execution_hurt フィールド名（旧 *_correct / execution_degraded）
  3. net_pnl = gross_pnl - fees のみ（execution_lag_cost は含まない）
  4. execution_lag_cost_jpy は attribution 専用フィールドとして別途計算
  5. 評価開始は actual_execution_date の翌日（同日バーは除外）
  6. ohlcv 空 → status=open のまま返す（エラーにならない）
  7. source=unconfigured でもコスト計算は動く（fee=0 でなく unconfigured 扱い）
"""

from __future__ import annotations

import math
import pandas as pd
import pytest

import jp_swing_evaluate as ev
import jp_one_share_cost as cost_lib
import jp_swing_ledger as ledger


# ── テスト用ヘルパー ──────────────────────────────────────────────

def _make_ohlcv(dates: list[str], opens=None, highs=None, lows=None, closes=None) -> pd.DataFrame:
    n = len(dates)
    opens = opens or [1000.0] * n
    highs = highs or [1100.0] * n
    lows = lows or [950.0] * n
    closes = closes or [1050.0] * n
    return pd.DataFrame({
        "date": pd.to_datetime(dates),
        "open": opens,
        "high": highs,
        "low": lows,
        "close": closes,
    })


def _base_row(**kwargs) -> dict:
    """評価可能な最小限の仮説行（約定済み状態）。"""
    row = {
        "hypothesis_id": "JP-TEST-001",
        "decision_date": "2026-06-10",
        "intended_order_date": "2026-06-11",
        "assumed_execution_date": "2026-06-12",
        "actual_execution_date": "2026-06-12",
        "ticker": "7203.T",
        "company_name": "トヨタ自動車",
        "sector": "輸送用機器",
        "narrative": "テスト仮説",
        "falsifier": "来期ガイダンスが市場予想を下回る",
        "horizon_days": 20,
        "confidence_pct": 65,
        "status": "pending",
        "actual_entry_price": 2000.0,
        "expected_entry_price": 1980.0,
        "sl_price": 1900.0,
        "tp1_price": 2200.0,
        "tp2_price": 2400.0,
        "shares": 1,
    }
    row.update(kwargs)
    return row


def _cfg_sourced() -> dict:
    """ソース付きコスト設定（テスト用）。"""
    return {
        "source": "test",
        "buy_rate": 0.005,
        "sell_rate": 0.005,
        "buy_min_fee": 52.0,
        "sell_min_fee": 52.0,
    }


# ── フィールド名 rev2 確認 ─────────────────────────────────────────

def test_evaluate_uses_actual_execution_date_not_old_names():
    """旧フィールド名 actual_entry_date / order_date を渡しても評価できない（スルーされる）。"""
    ohlcv = _make_ohlcv(
        ["2026-06-13", "2026-06-14", "2026-06-15"],
        highs=[2500.0, 2500.0, 2500.0],
        lows=[1950.0, 1950.0, 1950.0],
        closes=[2300.0, 2300.0, 2300.0],
    )
    # actual_execution_date を省略し、旧名フィールドのみ提供 → 評価されない
    row = _base_row()
    row.pop("actual_execution_date", None)
    row["actual_entry_date"] = "2026-06-12"  # 旧フィールド名
    row["order_date"] = "2026-06-11"          # 旧フィールド名
    result = ev.evaluate_signal(row, ohlcv=ohlcv, cost_cfg=_cfg_sourced())
    # 旧フィールドが評価に使われないので pending or open だが closed にはならない
    assert result["status"] != "closed"


def test_evaluate_reads_actual_execution_date():
    """actual_execution_date が正しく使われる → closed になる。"""
    ohlcv = _make_ohlcv(
        ["2026-06-13", "2026-06-14", "2026-06-15"],
        highs=[2500.0, 2500.0, 2500.0],
        lows=[1800.0, 1800.0, 1800.0],
        closes=[2300.0, 2300.0, 2300.0],
    )
    row = _base_row()  # actual_execution_date="2026-06-12" を含む
    result = ev.evaluate_signal(row, ohlcv=ohlcv, cost_cfg=_cfg_sourced())
    assert result["status"] == "closed"


# ── 評価除外: 約定日同日バー ───────────────────────────────────────

def test_evaluation_excludes_execution_date_bar():
    """約定日(2026-06-12)のバーは評価対象外。翌日(06-13)から始まる。"""
    # 約定日のバーのみ SL を下回る → 除外されるので SL にならない
    ohlcv = _make_ohlcv(
        ["2026-06-12", "2026-06-13", "2026-06-14"],
        highs=[2500.0, 2100.0, 2100.0],
        lows=[1800.0, 1950.0, 1950.0],  # 約定日のみ SL(1900) を下回る
        closes=[2000.0, 2050.0, 2050.0],
    )
    row = _base_row()
    result = ev.evaluate_signal(row, ohlcv=ohlcv, cost_cfg=_cfg_sourced())
    # 約定日バーが除外されているので sl_hit にならない
    assert result.get("exit_reason") != "sl_hit"


def test_execution_date_bar_included_would_hit_sl():
    """除外しなければ SL になる状況を確認（設計の意図テスト）。"""
    ohlcv = _make_ohlcv(
        ["2026-06-13", "2026-06-14", "2026-06-15"],
        highs=[2500.0, 2500.0, 2500.0],
        lows=[1800.0, 1800.0, 1800.0],  # SL(1900) を全日下回る → SL ヒット
        closes=[1850.0, 1850.0, 1850.0],
    )
    row = _base_row()
    result = ev.evaluate_signal(row, ohlcv=ohlcv, cost_cfg=_cfg_sourced())
    assert result.get("exit_reason") == "sl_hit"


# ── コスト分離: net_pnl と execution_lag_cost ─────────────────────

def test_net_pnl_excludes_lag_cost():
    """net_pnl = gross_pnl - buy_fee - sell_fee（ラグコスト含まない）。"""
    ohlcv = _make_ohlcv(
        ["2026-06-13"],
        highs=[2200.0],
        lows=[1950.0],
        closes=[2100.0],
    )
    # horizon=20 でも ohlcv に1本しかないので time_exit
    row = _base_row(horizon_days=20)
    cfg = _cfg_sourced()
    result = ev.evaluate_signal(row, ohlcv=ohlcv, cost_cfg=cfg)
    assert result["status"] == "closed"
    entry = 2000.0
    exit_price = result["exit_price"]
    expected_gross = (exit_price - entry) * 1
    buy_fee = cost_lib.buy_commission(entry, 1, cfg)
    sell_fee = cost_lib.sell_commission(exit_price, 1, cfg)
    expected_net = expected_gross - buy_fee - sell_fee
    assert abs(result["gross_pnl_jpy"] - round(expected_gross, 0)) < 1
    assert abs(result["net_pnl_jpy"] - round(expected_net, 0)) < 1


def test_execution_lag_cost_is_separate_attribution():
    """execution_lag_cost_jpy は net_pnl と独立したフィールド。"""
    ohlcv = _make_ohlcv(["2026-06-13"], highs=[2100.0], lows=[1950.0], closes=[2100.0])
    row = _base_row(
        actual_entry_price=2000.0,
        expected_entry_price=1980.0,  # ラグで 20 円不利
        shares=2,
    )
    result = ev.evaluate_signal(row, ohlcv=ohlcv, cost_cfg=_cfg_sourced())
    assert "execution_lag_cost_jpy" in result
    # ラグコスト = (actual - expected) × shares = (2000-1980) × 2 = 40 → 正値（不利）
    assert result["execution_lag_cost_jpy"] == 40.0


def test_execution_lag_cost_negative_when_favorable():
    """ラグが有利に働いた場合（安く約定）→ 負値。"""
    ohlcv = _make_ohlcv(["2026-06-13"], highs=[2100.0], lows=[1950.0], closes=[2100.0])
    row = _base_row(
        actual_entry_price=1960.0,   # 想定より安く約定
        expected_entry_price=1980.0,
        shares=1,
    )
    result = ev.evaluate_signal(row, ohlcv=ohlcv, cost_cfg=_cfg_sourced())
    # (1960 - 1980) × 1 = -20
    assert result["execution_lag_cost_jpy"] == -20.0


def test_lag_cost_not_in_net_pnl():
    """net_pnl に execution_lag_cost を加算しないことを明示的に検証。"""
    ohlcv = _make_ohlcv(["2026-06-13"], highs=[2100.0], lows=[1950.0], closes=[2100.0])
    cfg = _cfg_sourced()
    row = _base_row(
        actual_entry_price=2000.0,
        expected_entry_price=1980.0,
        shares=1,
    )
    result = ev.evaluate_signal(row, ohlcv=ohlcv, cost_cfg=cfg)
    exit_p = result["exit_price"]
    buy_fee = cost_lib.buy_commission(2000.0, 1, cfg)
    sell_fee = cost_lib.sell_commission(exit_p, 1, cfg)
    expected_net = (exit_p - 2000.0) - buy_fee - sell_fee
    lag_cost = result["execution_lag_cost_jpy"]
    # net_pnl が lag_cost を含まないことを確認（含むと値がずれる）
    assert abs(result["net_pnl_jpy"] - round(expected_net, 0)) < 1
    assert result["net_pnl_jpy"] != round(expected_net - lag_cost, 0) or lag_cost == 0


# ── SL / TP / time_exit ───────────────────────────────────────────

def test_sl_exit():
    ohlcv = _make_ohlcv(
        ["2026-06-13", "2026-06-14"],
        highs=[2100.0, 2100.0],
        lows=[1850.0, 1850.0],  # SL=1900 を下回る
        closes=[2000.0, 2000.0],
    )
    row = _base_row()
    result = ev.evaluate_signal(row, ohlcv=ohlcv, cost_cfg=_cfg_sourced())
    assert result["exit_reason"] == "sl_hit"
    assert result["exit_price"] == 1900.0
    assert result["status"] == "closed"


def test_tp1_exit_without_tp2():
    ohlcv = _make_ohlcv(
        ["2026-06-13"],
        highs=[2300.0],  # tp1=2200 を超える、tp2=2400 は超えない
        lows=[1950.0],
        closes=[2250.0],
    )
    row = _base_row(tp2_price=float("nan"))  # tp2 なし
    result = ev.evaluate_signal(row, ohlcv=ohlcv, cost_cfg=_cfg_sourced())
    assert result["exit_reason"] == "tp1_hit"
    assert result["exit_price"] == 2200.0


def test_tp2_exit():
    ohlcv = _make_ohlcv(
        ["2026-06-13"],
        highs=[2500.0],  # tp2=2400 を超える
        lows=[1950.0],
        closes=[2450.0],
    )
    row = _base_row()
    result = ev.evaluate_signal(row, ohlcv=ohlcv, cost_cfg=_cfg_sourced())
    assert result["exit_reason"] == "tp2_hit"
    assert result["exit_price"] == 2400.0


def test_time_exit():
    """horizon 満了 → 最終足の終値で time_exit。"""
    # horizon=10、10本のバーを用意（SL/TP 到達なし）
    dates = [f"2026-06-{13+i:02d}" for i in range(10)]
    ohlcv = _make_ohlcv(dates, highs=[2100.0] * 10, lows=[1950.0] * 10, closes=[2050.0] * 10)
    row = _base_row(horizon_days=10)
    result = ev.evaluate_signal(row, ohlcv=ohlcv, cost_cfg=_cfg_sourced())
    assert result["exit_reason"] == "time_exit"
    assert result["exit_price"] == 2050.0
    assert result["status"] == "closed"


def test_sl_takes_priority_over_tp_in_same_bar():
    """同バー内で SL と TP 両方触れる → SL が優先（不利側を保守的に評価）。"""
    ohlcv = _make_ohlcv(
        ["2026-06-13"],
        highs=[2500.0],  # tp2 を超える
        lows=[1800.0],   # SL を下回る
        closes=[2200.0],
    )
    row = _base_row()
    result = ev.evaluate_signal(row, ohlcv=ohlcv, cost_cfg=_cfg_sourced())
    assert result["exit_reason"] == "sl_hit"


# ── 未約定 / データ欠落 ───────────────────────────────────────────

def test_pending_without_execution_date_returns_pending():
    """actual_execution_date が空 → pending のまま。"""
    row = _base_row()
    row["actual_execution_date"] = ""
    result = ev.evaluate_signal(row, ohlcv=pd.DataFrame(), cost_cfg=_cfg_sourced())
    assert result["status"] in {"pending", "open"}


def test_empty_ohlcv_returns_open():
    """ohlcv が空 → status=open（評価不能だがエラーにならない）。"""
    row = _base_row()
    result = ev.evaluate_signal(row, ohlcv=pd.DataFrame(), cost_cfg=_cfg_sourced())
    assert result["status"] == "open"


def test_already_closed_row_returned_as_is():
    """status=closed の行はそのまま返す（再評価しない）。"""
    row = _base_row(status="closed")
    result = ev.evaluate_signal(row, ohlcv=pd.DataFrame(), cost_cfg=_cfg_sourced())
    assert result["status"] == "closed"


def test_missing_entry_price_returns_pending():
    row = _base_row()
    row["actual_entry_price"] = ""
    result = ev.evaluate_signal(row, ohlcv=pd.DataFrame(), cost_cfg=_cfg_sourced())
    assert result["status"] in {"pending", "open"}


def test_zero_shares_returns_pending():
    row = _base_row(shares=0)
    result = ev.evaluate_signal(row, ohlcv=pd.DataFrame(), cost_cfg=_cfg_sourced())
    assert result["status"] in {"pending", "open"}


# ── _suggest_outcome と execution_hurt フラグ ──────────────────────

def test_suggest_outcome_A_when_thesis_timing_win():
    """thesis_hit=true, timing_hit=true, tp ヒット → outcome A。"""
    ohlcv = _make_ohlcv(["2026-06-13"], highs=[2500.0], lows=[1950.0], closes=[2450.0])
    row = _base_row(thesis_hit="true", timing_hit="true")
    result = ev.evaluate_signal(row, ohlcv=ohlcv, cost_cfg=_cfg_sourced())
    assert result["outcome_type"] == "A"


def test_suggest_outcome_D_when_thesis_false_loss():
    """thesis_hit=false, SL ヒット → outcome D。"""
    ohlcv = _make_ohlcv(
        ["2026-06-13"],
        highs=[2100.0],
        lows=[1800.0],  # SL ヒット
        closes=[1850.0],
    )
    row = _base_row(thesis_hit="false")
    result = ev.evaluate_signal(row, ohlcv=ohlcv, cost_cfg=_cfg_sourced())
    assert result["outcome_type"] == "D"


def test_suggest_outcome_B_timing_miss():
    """thesis_hit=true, timing_hit=false → outcome B。"""
    ohlcv = _make_ohlcv(["2026-06-13"], highs=[2100.0], lows=[1950.0], closes=[2050.0])
    row = _base_row(thesis_hit="true", timing_hit="false")
    result = ev.evaluate_signal(row, ohlcv=ohlcv, cost_cfg=_cfg_sourced())
    assert result["outcome_type"] == "B"


def test_suggest_outcome_F_lucky_win():
    """thesis_hit=false でも tp ヒット → Lucky win (F)。"""
    ohlcv = _make_ohlcv(["2026-06-13"], highs=[2500.0], lows=[1950.0], closes=[2450.0])
    row = _base_row(thesis_hit="false")
    result = ev.evaluate_signal(row, ohlcv=ohlcv, cost_cfg=_cfg_sourced())
    assert result["outcome_type"] == "F"


def test_human_input_outcome_type_takes_precedence():
    """人間入力の outcome_type がある → 機械推定を上書きしない。"""
    ohlcv = _make_ohlcv(["2026-06-13"], highs=[2500.0], lows=[1950.0], closes=[2450.0])
    row = _base_row(outcome_type="E")  # 人間が記入済み
    result = ev.evaluate_signal(row, ohlcv=ohlcv, cost_cfg=_cfg_sourced())
    assert result["outcome_type"] == "E"


def test_execution_hurt_not_overwritten_when_human_provided():
    """人間が execution_hurt=false と記入済み → 自動フラグで上書きしない。"""
    ohlcv = _make_ohlcv(["2026-06-13"], highs=[2100.0], lows=[1950.0], closes=[2050.0])
    row = _base_row(execution_hurt="false")
    result = ev.evaluate_signal(row, ohlcv=ohlcv, cost_cfg=_cfg_sourced())
    # 人間入力を尊重（自動計算が true でも false が残る）
    assert str(result.get("execution_hurt", "")).strip().lower() in {"false", "0", "no", False}


# ── summarize() ─────────────────────────────────────────────────

def test_summarize_empty_df_has_insufficient_data():
    df = pd.DataFrame(columns=ledger.JP_SIGNAL_COLUMNS)
    summary = ev.summarize(df)
    assert summary["insufficient_data"] is True
    assert summary["total_hypotheses"] == 0


def test_summarize_counts_status():
    rows = []
    for status in ["pending", "open", "closed", "closed"]:
        row = {col: "" for col in ledger.JP_SIGNAL_COLUMNS}
        row.update(_base_row(status=status))
        rows.append(row)
    df = pd.DataFrame(rows)
    summary = ev.summarize(df)
    assert summary["total_hypotheses"] == 4
    assert summary["closed"] == 2
    assert summary["open"] == 1
    assert summary["pending"] == 1


def test_summarize_win_rate():
    rows = []
    for net_r, status in [(1.0, "closed"), (-0.5, "closed"), (0.5, "closed")]:
        row = {col: "" for col in ledger.JP_SIGNAL_COLUMNS}
        row.update(_base_row(status=status))
        row["net_r"] = net_r
        row["gross_r"] = net_r
        row["net_pnl_jpy"] = net_r * 1000
        row["execution_lag_cost_jpy"] = 0
        rows.append(row)
    df = pd.DataFrame(rows)
    summary = ev.summarize(df)
    # 2勝1敗 → 0.667
    assert abs(summary["win_rate"] - 2 / 3) < 0.01


def test_summarize_total_lag_cost():
    rows = []
    for lag in [40.0, -20.0, 10.0]:
        row = {col: "" for col in ledger.JP_SIGNAL_COLUMNS}
        row.update(_base_row(status="closed"))
        row["net_r"] = 0.0
        row["gross_r"] = 0.0
        row["net_pnl_jpy"] = 0
        row["execution_lag_cost_jpy"] = lag
        rows.append(row)
    df = pd.DataFrame(rows)
    summary = ev.summarize(df)
    assert summary["total_lag_cost_jpy"] == 30  # 40 - 20 + 10


def test_summarize_outcome_distribution():
    rows = []
    for ot in ["A", "B", "D", "A"]:
        row = {col: "" for col in ledger.JP_SIGNAL_COLUMNS}
        row.update(_base_row(status="closed"))
        row["net_r"] = 0.0
        row["gross_r"] = 0.0
        row["net_pnl_jpy"] = 0
        row["execution_lag_cost_jpy"] = 0
        row["outcome_type"] = ot
        rows.append(row)
    df = pd.DataFrame(rows)
    summary = ev.summarize(df)
    dist = summary["outcome_distribution"]
    assert dist["A"] == 2
    assert dist["B"] == 1
    assert dist["D"] == 1
    assert dist["C"] == 0


def test_summarize_calibration_insufficient_when_less_than_5():
    rows = []
    for _ in range(3):
        row = {col: "" for col in ledger.JP_SIGNAL_COLUMNS}
        row.update(_base_row(status="closed"))
        row["net_r"] = 1.0
        row["gross_r"] = 1.0
        row["net_pnl_jpy"] = 1000
        row["execution_lag_cost_jpy"] = 0
        row["confidence_pct"] = 70.0
        rows.append(row)
    df = pd.DataFrame(rows)
    summary = ev.summarize(df)
    assert summary["calibration"].get("insufficient_data") is True


# ── _coerce ───────────────────────────────────────────────────────

def test_coerce_valid_float():
    assert ev._coerce("1234.5") == 1234.5


def test_coerce_none_returns_nan():
    assert math.isnan(ev._coerce(None))


def test_coerce_empty_string_returns_nan():
    assert math.isnan(ev._coerce(""))


def test_coerce_inf_returns_fallback():
    assert math.isnan(ev._coerce(float("inf")))


def test_coerce_custom_fallback():
    assert ev._coerce(None, fallback=0.0) == 0.0
