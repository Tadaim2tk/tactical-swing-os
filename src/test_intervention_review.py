"""tools/analysis/intervention_review.py — 介入後の期間の読み方を固定する。

数え方を言葉どおりにする: 見立ては資産×向きの並び（向きが行き来しても、同じ向きが3日以内に続けば1本）、
成績は並びの最初の注文、入れ替わりは期間の中だけ、賭けの本数は行数で頭打ち。"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "analysis"))
sys.path.insert(0, str(ROOT / "src"))
import intervention_review as ir  # noqa: E402
import throughput_metrics as tm  # noqa: E402


def _ledger(rows):
    df = pd.DataFrame(rows, columns=["date", "asset", "side", "rank"])
    return tm.ledger_frame(df)


def _orders(rows, results):
    """rows: 台帳の行。results: (date, asset) -> (status, r_result)。"""
    orders = ir.attach_runs(tm.mark_runs(_ledger(rows)))
    orders["status"] = [results.get((d.strftime("%Y-%m-%d"), a), ("open", np.nan))[0] for d, a in zip(orders["date"], orders["asset"])]
    orders["r_result"] = [results.get((d.strftime("%Y-%m-%d"), a), ("open", np.nan))[1] for d, a in zip(orders["date"], orders["asset"])]
    return orders


def test_an_idea_is_a_run_of_the_same_asset_and_side_and_is_scored_by_its_first_order():
    rows = [
        ("2026-11-04", "ETH", "SELL", "B"), ("2026-11-05", "ETH", "BUY", "B"), ("2026-11-06", "ETH", "SELL", "B"),
        ("2026-11-07", "ETH", "SELL", "B"), ("2026-11-05", "GOLD", "BUY", "B"), ("2026-11-06", "GOLD", "BUY", "B"),
        ("2026-11-05", "VIX", "NONE", "NO_TRADE"),
    ]
    results = {("2026-11-04", "ETH"): ("filled_sl", -1.0), ("2026-11-05", "ETH"): ("filled_sl", -1.0),
               ("2026-11-06", "ETH"): ("filled_tp1", 1.5), ("2026-11-07", "ETH"): ("open", np.nan),
               ("2026-11-05", "GOLD"): ("filled_sl", -1.0), ("2026-11-06", "GOLD"): ("filled_sl", -1.0)}
    ideas = ir.idea_table(_orders(rows, results), pd.Timestamp("2026-11-04"), pd.Timestamp("2026-11-17"))
    # ETH の売りは 11/4・11/6・11/7 で1本（間に買いが挟まっても、同じ向きが3日以内に続く）
    got = {(r.asset, r.side): (r.rows, r.first_r, r.sum_r, r.settled_rows) for r in ideas.itertuples()}
    assert got == {("ETH", "SELL"): (3, -1.0, 0.5, 2), ("ETH", "BUY"): (1, -1.0, -1.0, 1), ("GOLD", "BUY"): (2, -1.0, -2.0, 2)}
    s = ir.idea_summary(ideas)
    assert (s["ideas"], s["first_settled"], s["wins"], s["losses"], s["total_r"], s["all_rows_r"]) == (3, 3, 0, 3, -3.0, -2.5)


def test_ideas_that_began_before_the_period_are_left_out_and_rows_after_it_are_not_added():
    rows = [("2026-11-02", "WTI", "SELL", "B"), ("2026-11-04", "WTI", "SELL", "B"),      # 期間より前から続く並び
            ("2026-11-10", "BTC", "SELL", "B"), ("2026-11-12", "BTC", "SELL", "B")]      # 11/12 は期間の外
    results = {("2026-11-04", "WTI"): ("filled_tp1", 1.2), ("2026-11-10", "BTC"): ("no_fill", np.nan), ("2026-11-12", "BTC"): ("filled_tp1", 2.0)}
    ideas = ir.idea_table(_orders(rows, results), pd.Timestamp("2026-11-04"), pd.Timestamp("2026-11-11"))
    assert list(ideas["asset"]) == ["BTC"]
    row = ideas.iloc[0]
    assert (row["rows"], row["first_status"], row["settled_rows"], row["sum_r"]) == (1, "no_fill", 0, 0.0) and np.isnan(row["first_r"])
    s = ir.idea_summary(ideas)
    assert (s["first_settled"], s["first_no_fill"], s["mean_r"]) == (0, 1, None)


def test_row_summary_counts_only_settled_rows_in_the_result():
    rows = pd.DataFrame({"status": ["filled_sl", "filled_tp1", "filled_time_exit", "no_fill", "open", ""],
                         "r_result": [-1.0, 1.5, 0.2, np.nan, np.nan, np.nan]})
    s = ir.row_summary(rows)
    assert (s["orders"], s["settled"], s["sl"], s["tp1"], s["time_exit"], s["no_fill"], s["open"], s["wins"]) == (6, 3, 1, 1, 1, 1, 1, 2)
    assert s["total_r"] == 0.7 and s["mean_r"] == pytest.approx(0.233, abs=1e-3)
    empty = ir.row_summary(rows[rows["status"] == "open"])
    assert (empty["settled"], empty["total_r"], empty["mean_r"]) == (0, 0.0, None)


def test_flips_are_counted_inside_the_period_only_and_skip_no_trade_days():
    led = _ledger([
        ("2026-10-20", "NASDAQ", "BUY", "B"),                                   # 期間より前。比べない
        ("2026-11-04", "NASDAQ", "SELL", "B"), ("2026-11-05", "NASDAQ", "BUY", "B"),
        ("2026-11-06", "NASDAQ", "NONE", "NO_TRADE"), ("2026-11-07", "NASDAQ", "SELL", "B"),
        ("2026-11-08", "NASDAQ", "SELL", "B"),
        ("2026-11-04", "WTI", "SELL", "B"), ("2026-11-09", "WTI", "SELL", "B"),
        ("2026-11-04", "VIX", "NONE", "NO_TRADE"),
    ])
    assert ir.count_flips(led, pd.Timestamp("2026-11-04"), pd.Timestamp("2026-11-17")) == {"NASDAQ": 2, "WTI": 0}


def test_effective_bets_is_one_for_identical_moves_and_n_for_unrelated_ones():
    rng = np.random.RandomState(0)
    base = rng.normal(size=300)
    other = rng.normal(size=300)
    returns = pd.DataFrame({"A": base, "B": base, "C": other, "D": -base})
    assert ir.effective_bets({"A": "BUY", "B": "BUY"}, returns) == pytest.approx(1.0)
    assert ir.effective_bets({"A": "BUY", "D": "SELL"}, returns) == pytest.approx(1.0)     # 逆に動く資産の逆向き = 同じ賭け
    assert ir.effective_bets({"A": "BUY", "C": "BUY"}, returns) == pytest.approx(2.0, abs=0.15)
    # 打ち消し合う組（同じ動きの資産を買いと売り）は式の値が行数を超える。行数で頭打ち
    assert ir.effective_bets({"A": "BUY", "B": "SELL"}, returns) == 2.0
    assert ir.effective_bets({"A": "BUY"}, returns) == 1.0
    assert np.isnan(ir.effective_bets({}, returns))


def test_effective_bets_is_unknown_without_enough_price_history():
    """測れない日を「全部が無関係 = 行数ぶん」と数えない（#219 Codex P2）。"""
    rng = np.random.RandomState(3)
    returns = pd.DataFrame({"A": rng.normal(size=100), "B": rng.normal(size=100), "FLAT": np.zeros(100)})
    two = {"A": "BUY", "B": "BUY"}
    assert np.isnan(ir.effective_bets(two, returns.iloc[0:0]))                 # 判断日が価格の履歴より前
    assert np.isnan(ir.effective_bets(two, returns.head(ir.MIN_HISTORY - 1)))  # 履歴が足りない
    assert not np.isnan(ir.effective_bets(two, returns.head(ir.MIN_HISTORY)))
    assert np.isnan(ir.effective_bets({"A": "BUY", "Z": "BUY"}, returns))      # 価格の無い資産が混じる
    assert np.isnan(ir.effective_bets({"A": "BUY", "FLAT": "BUY"}, returns))   # 相関が出ない
    assert ir.effective_bets({"Z": "BUY"}, returns.iloc[0:0]) == 1.0           # 1行の日は相関が要らない


def _frame(dates, returns):
    """日次リターンの列から日足を作る（open/high/low は close と同じ。ここでは終値しか使わない）。"""
    close = 100.0 * np.cumprod(1.0 + 0.01 * np.asarray(returns, dtype=float))
    return pd.DataFrame({"date": pd.DatetimeIndex(dates), "open": close, "high": close, "low": close, "close": close})


def _orders_on(day, sides):
    return ir.attach_runs(tm.mark_runs(_ledger([(day.strftime("%Y-%m-%d"), a, s, "B") for a, s in sides])))


def test_daily_bets_uses_only_bars_closed_at_decision_time_and_splits_context_assets():
    idx = pd.bdate_range("2026-07-01", periods=100)
    rng = np.random.RandomState(1)
    base = rng.normal(size=100)
    frames = {"GOLD": _frame(idx, base), "DXY": _frame(idx, -base), "WTI": _frame(idx, rng.normal(size=100))}
    day = idx[80]
    orders = _orders_on(day, [("GOLD", "BUY"), ("DXY", "SELL"), ("WTI", "BUY")])
    got = ir.daily_bets(orders, frames, {"DXY"}).iloc[0]
    assert (got["orders"], got["orders_tradable"]) == (3, 2)
    assert got["bets"] < 2.4                     # GOLD 買いと DXY 売りは同じ賭け。3行でも2本ぶんに近い
    # 判断日以降の足を壊しても結果は変わらない（先を見ていない）
    broken = {a: df.copy() for a, df in frames.items()}
    for df in broken.values():
        df.loc[df["date"] >= day, "close"] = 1e9
    assert ir.daily_bets(orders, broken, {"DXY"}).iloc[0]["bets"] == pytest.approx(got["bets"])
    # 週5日の資産は、前日ラベルの足が判断時に閉まっているので使う（壊すと結果が変わる）
    assert ir.history_cutoff(day, ["GOLD", "WTI"], frames) == idx[79]
    used = {a: df.copy() for a, df in frames.items()}
    used["WTI"].loc[used["WTI"]["date"] == idx[79], "close"] *= 3.0
    assert ir.daily_bets(orders, used, {"DXY"}).iloc[0]["bets"] != pytest.approx(got["bets"])


def test_a_crypto_order_moves_the_cutoff_one_bar_earlier_for_the_whole_day():
    """暗号資産の日足は判断の2時間後（09:00 JST）に閉まる。前日ラベルの足は使わない（#219 Codex P2）。

    切る日は src/score_prediction_log.py の decision_time_anchor で決める。その日の注文に暗号資産があれば、
    いちばん早く切れる資産に全体をそろえる。"""
    all_days = pd.date_range("2026-07-01", periods=140)                       # 暗号資産は土日も足がある
    weekdays = all_days[all_days.dayofweek < 5]
    rng = np.random.RandomState(4)
    frames = {"BTC": _frame(all_days, rng.normal(size=len(all_days))),
              "GOLD": _frame(weekdays, rng.normal(size=len(weekdays))),
              "WTI": _frame(weekdays, rng.normal(size=len(weekdays)))}
    day = pd.Timestamp("2026-11-10")                                          # 火曜
    assert ir.history_cutoff(day, ["GOLD", "WTI"], frames) == pd.Timestamp("2026-11-09")
    assert ir.history_cutoff(day, ["BTC"], frames) == pd.Timestamp("2026-11-08")
    assert ir.history_cutoff(day, ["BTC", "GOLD"], frames) == pd.Timestamp("2026-11-08")
    orders = _orders_on(day, [("BTC", "SELL"), ("GOLD", "BUY")])
    got = ir.daily_bets(orders, frames, set()).iloc[0]["bets"]
    assert not np.isnan(got)
    # 11/9 ラベルの足（BTC は判断時にまだ閉まっていない）を壊しても、結果は変わらない
    broken = {a: df.copy() for a, df in frames.items()}
    for df in broken.values():
        df.loc[df["date"] >= pd.Timestamp("2026-11-09"), "close"] *= 5.0
    assert ir.daily_bets(orders, broken, set()).iloc[0]["bets"] == pytest.approx(got)
    # 価格の無い資産が混じる日、判断日より前の足が無い日は、切る日を決められない
    assert ir.history_cutoff(day, ["BTC", "ZZZ"], frames) is None
    assert ir.history_cutoff(pd.Timestamp("2026-07-01"), ["BTC"], frames) is None


def test_an_asset_outside_the_order_group_cannot_remove_history_from_it():
    """GOLD と WTI の日を測るのに、VIX の履歴の短さは関係ない（#219 Codex P2）。"""
    idx = pd.bdate_range("2026-07-01", periods=100)
    rng = np.random.RandomState(6)
    frames = {"GOLD": _frame(idx, rng.normal(size=100)), "WTI": _frame(idx, rng.normal(size=100))}
    day = idx[80]
    orders = _orders_on(day, [("GOLD", "BUY"), ("WTI", "BUY")])
    alone = ir.daily_bets(orders, frames, set()).iloc[0]["bets"]
    assert not np.isnan(alone)
    # 履歴が20日しかない VIX、途中の日が抜けた DXY を足しても、GOLD と WTI の結果は同じ
    with_others = dict(frames)
    with_others["VIX"] = _frame(idx[60:80], rng.normal(size=20))
    with_others["DXY"] = _frame(idx[::3], rng.normal(size=len(idx[::3])))
    assert ir.daily_bets(orders, with_others, set()).iloc[0]["bets"] == pytest.approx(alone)
    # 組に入っている資産の履歴が短ければ、その組は測れない
    short = dict(frames)
    short["WTI"] = _frame(idx[60:80], rng.normal(size=20))
    assert np.isnan(ir.daily_bets(orders, short, set()).iloc[0]["bets"])
    # そろえるのは組の資産に終値がある日だけ。行は cutoff までの直近 lookback 本
    got = ir.group_returns(with_others, ["GOLD", "WTI"], idx[79], lookback=60)
    assert list(got.columns) == ["GOLD", "WTI"] and len(got) == 60 and got.index.max() == idx[79]
    assert ir.group_returns(with_others, ["GOLD", "ZZZ"], idx[79]).empty


def test_days_without_orders_count_as_zero_in_the_daily_average():
    """14日のうち2日しか注文が無い期間を「1日 1.0 行」と読まない（#219 Codex P2）。"""
    idx = pd.bdate_range("2026-07-01", periods=100)
    rng = np.random.RandomState(2)
    frames = {a: _frame(idx, rng.normal(size=100)) for a in ("GOLD", "WTI", "DXY")}
    days = list(idx[80:94])                                            # 台帳の14日
    orders = ir.attach_runs(tm.mark_runs(_ledger([(days[0].strftime("%Y-%m-%d"), "GOLD", "BUY", "B"),
                                                  (days[5].strftime("%Y-%m-%d"), "DXY", "BUY", "B")])))
    bets = ir.daily_bets(orders, frames, {"DXY"}, days=days)
    assert len(bets) == 14 and int((bets["orders"] == 0).sum()) == 12
    assert bets["orders"].mean() == pytest.approx(2 / 14)
    assert bets["bets"].mean() == pytest.approx(2 / 14)               # 1行の日は 1 本
    # 文脈用の資産しか無い日は、取引する資産の側を 0 行・0 本にする（平均から抜け落ちない）
    assert bets["orders_tradable"].sum() == 1 and bets["bets_tradable"].mean() == pytest.approx(1 / 14)
    assert not bets[["bets", "bets_tradable"]].isna().any().any()
    # 注文が1つも無い期間でも落ちない
    none = ir.daily_bets(orders.iloc[0:0], frames, {"DXY"}, days=days)
    assert len(none) == 14 and none["orders"].sum() == 0 and none["bets"].mean() == 0.0
    assert list(ir.daily_bets(orders.iloc[0:0], frames, {"DXY"}).columns) == ["date", "orders", "bets", "orders_tradable", "bets_tradable"]


def test_a_day_without_enough_history_stays_unknown_in_the_daily_table():
    """日ごとの表でも NaN のまま残り、0 や行数に化けない（#219 Codex P2）。"""
    idx = pd.bdate_range("2026-07-01", periods=100)
    rng = np.random.RandomState(5)
    frames = {"GOLD": _frame(idx, rng.normal(size=100)), "WTI": _frame(idx, rng.normal(size=100))}
    early = idx[5]
    got = ir.daily_bets(_orders_on(early, [("GOLD", "BUY"), ("WTI", "BUY")]), frames, set(), days=[early]).iloc[0]
    assert got["orders"] == 2 and np.isnan(got["bets"]) and np.isnan(got["bets_tradable"])
    # 価格が1つも無いときも測れない（1行の日だけは 1）
    none = ir.daily_bets(_orders_on(early, [("GOLD", "BUY"), ("WTI", "BUY")]), {}, set(), days=[early]).iloc[0]
    assert np.isnan(none["bets"])
    assert ir.daily_bets(_orders_on(early, [("GOLD", "BUY")]), {}, set(), days=[early]).iloc[0]["bets"] == 1.0
