"""進行中の擬似取引（建玉）の含みR と、週の「確定＋含み」の変化（src/open_book.py。2026-11-27）。

決着ぶんだけを画面に出していたので、含み損を抱えた週が良く見えていた（2026-11-23 の週: 決着 +2.8R・進行中 34 件の含み −11.5R）。
"""
from __future__ import annotations

import math

import pandas as pd
import pytest

import dashboard_render as dr
import dashboard_summaries as ds
import open_book as ob

COLS = ["date", "signal_id", "asset", "side", "status", "fill_date", "fill_price", "risk_unit", "exit_date", "r_result"]


def _frame(closes: dict) -> pd.DataFrame:
    """{"2026-11-20": 100.0, ...} → 日足（終値だけが意味を持つ）。"""
    d = pd.DataFrame({"date": pd.to_datetime(list(closes)), "close": list(closes.values())})
    d["open"] = d["high"] = d["low"] = d["close"]
    return d


def _sim(rows: list) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=COLS)


# 週5日の資産 AAA（土日の足が無い）と、週7日の資産 CCC
AAA = _frame({"2026-11-19": 100.0, "2026-11-20": 104.0, "2026-11-23": 110.0, "2026-11-24": 108.0, "2026-11-25": 101.0})
CCC = _frame({"2026-11-19": 50.0, "2026-11-20": 50.0, "2026-11-21": 52.0, "2026-11-22": 48.0, "2026-11-23": 47.0,
              "2026-11-24": 49.0, "2026-11-25": 46.0})
FRAMES = {"AAA": AAA, "CCC": CCC}


def test_positions_are_marked_with_the_latest_close_in_units_of_risk():
    sim = _sim([
        ["2026-11-20", "a", "AAA", "LONG", "open", "2026-11-20", 105.0, 10.0, "", ""],   # (101-105)/10 = -0.4
        ["2026-11-20", "c", "CCC", "SHORT", "open", "2026-11-20", 50.0, 8.0, "", ""],    # -(46-50)/8 = +0.5
    ])
    pos = ob.positions(sim, FRAMES).set_index("signal_id")
    assert pos.loc["a", "mark_r"] == pytest.approx(-0.4) and pos.loc["c", "mark_r"] == pytest.approx(0.5)
    assert pos.loc["a", "mark_date"] == pd.Timestamp("2026-11-25")


def test_an_open_order_that_never_filled_is_not_a_position():
    sim = _sim([
        ["2026-11-24", "wait", "AAA", "LONG", "open", "", "", 10.0, "", ""],
        ["2026-11-20", "held", "AAA", "LONG", "open", "2026-11-20", 105.0, 10.0, "", ""],
    ])
    pos = ob.positions(sim, FRAMES)
    assert list(pos["signal_id"]) == ["held"] and list(pos["row"]) == [1]     # row は元の表の行番号
    s = ob.summary(sim, FRAMES)
    assert s["positions"] == 1 and s["unfilled_open"] == 1


def test_settled_and_excluded_rows_are_not_positions():
    sim = _sim([
        ["2026-11-19", "done", "AAA", "LONG", "filled_tp1", "2026-11-19", 100.0, 10.0, "2026-11-23", "1.0"],
        ["2026-11-19", "miss", "AAA", "LONG", "no_fill", "", "", "", "", ""],
        ["2026-11-19", "bad", "AAA", "LONG", "excluded_scale", "", "", "", "", ""],
    ])
    assert ob.positions(sim, FRAMES).empty
    s = ob.summary(sim, FRAMES)
    assert s["available"] and s["positions"] == 0 and s["mark_r"] == 0.0 and s["realized_r"] == 1.0 and s["equity_r"] == 1.0


def test_positions_that_cannot_be_measured_are_counted_and_left_out_of_the_mark():
    sim = _sim([
        ["2026-11-20", "ok", "AAA", "LONG", "open", "2026-11-20", 105.0, 10.0, "", ""],
        ["2026-11-20", "zero_risk", "AAA", "LONG", "open", "2026-11-20", 105.0, 0.0, "", ""],
        ["2026-11-20", "no_risk", "AAA", "LONG", "open", "2026-11-20", 105.0, "", "", ""],
        ["2026-11-20", "no_price", "ZZZ", "LONG", "open", "2026-11-20", 105.0, 10.0, "", ""],
        ["2026-11-20", "no_side", "AAA", "NONE", "open", "2026-11-20", 105.0, 10.0, "", ""],
    ])
    s = ob.summary(sim, FRAMES)
    assert s["positions"] == 1 and s["unmeasured"] == 4 and s["mark_r"] == pytest.approx(-0.4)
    assert [r["asset"] for r in s["by_asset"]] == ["AAA"]


def test_the_curve_moves_a_row_from_unrealized_to_realized_on_its_exit_day():
    sim = _sim([["2026-11-19", "t", "AAA", "LONG", "filled_tp1", "2026-11-20", 100.0, 10.0, "2026-11-24", "1.5"]])
    c = ob.equity_curve(sim, FRAMES, "2026-11-19", "2026-11-25").set_index("day")
    d = pd.Timestamp
    assert c.loc[d("2026-11-19"), ["positions", "equity_r"]].tolist() == [0, 0.0]          # まだ約定していない
    assert c.loc[d("2026-11-20"), "mark_r"] == pytest.approx(0.4)                           # (104-100)/10
    assert c.loc[d("2026-11-23"), "mark_r"] == pytest.approx(1.0)                           # (110-100)/10
    assert c.loc[d("2026-11-24"), ["realized_r", "positions", "mark_r"]].tolist() == [1.5, 0, 0.0]   # 決着した日は確定側
    assert c.loc[d("2026-11-25"), "equity_r"] == pytest.approx(1.5)


def test_a_weekday_asset_keeps_fridays_close_over_the_weekend():
    sim = _sim([
        ["2026-11-20", "a", "AAA", "LONG", "open", "2026-11-20", 100.0, 10.0, "", ""],
        ["2026-11-20", "c", "CCC", "LONG", "open", "2026-11-20", 50.0, 10.0, "", ""],
    ])
    c = ob.equity_curve(sim, FRAMES, "2026-11-20", "2026-11-23").set_index("day")
    d = pd.Timestamp
    # AAA は金曜の 104 のまま（+0.4）。CCC は土日も動く（52 → +0.2、48 → −0.2）
    assert c.loc[d("2026-11-21"), "mark_r"] == pytest.approx(0.4 + 0.2)
    assert c.loc[d("2026-11-22"), "mark_r"] == pytest.approx(0.4 - 0.2)
    assert c.loc[d("2026-11-23"), "mark_r"] == pytest.approx(1.0 - 0.3)


def test_a_position_opened_before_the_price_window_is_unmeasured_until_a_price_exists():
    sim = _sim([["2026-11-10", "old", "AAA", "LONG", "open", "2026-11-10", 100.0, 10.0, "", ""]])
    c = ob.equity_curve(sim, FRAMES, "2026-11-18", "2026-11-19").set_index("day")
    assert c.loc[pd.Timestamp("2026-11-18"), ["positions", "unmeasured"]].tolist() == [0, 1]
    assert c.loc[pd.Timestamp("2026-11-19"), ["positions", "unmeasured"]].tolist() == [1, 0]


def test_weekly_changes_compare_the_last_day_of_each_monday_to_sunday_week():
    curve = pd.DataFrame({
        "day": pd.to_datetime(["2026-11-15", "2026-11-20", "2026-11-22", "2026-11-23", "2026-11-25"]),
        "realized_r": [1.0, 2.0, 5.0, 5.0, 6.0], "positions": [0, 0, 0, 0, 0],
        "mark_r": [0.0, 1.0, 0.5, -1.0, -4.0], "equity_r": [1.0, 3.0, 5.5, 4.0, 2.0], "unmeasured": [0, 0, 0, 0, 0],
    })
    wk = ob.weekly_changes(curve)
    assert wk["week_start"].dt.strftime("%Y-%m-%d").tolist() == ["2026-11-16", "2026-11-23"]
    assert wk["last_day"].dt.strftime("%Y-%m-%d").tolist() == ["2026-11-22", "2026-11-25"]   # 進行中の週は最新の日まで
    assert wk["change_r"].tolist() == [4.5, -3.5] and wk["realized_change_r"].tolist() == [4.0, 1.0]
    assert wk["mark_r"].tolist() == [0.5, -4.0]


def test_weekly_changes_do_not_bridge_a_missing_week():
    curve = pd.DataFrame({
        "day": pd.to_datetime(["2026-11-08", "2026-11-22"]), "realized_r": [1.0, 2.0], "positions": [0, 0],
        "mark_r": [0.0, 0.0], "equity_r": [1.0, 2.0], "unmeasured": [0, 0],
    })
    assert ob.weekly_changes(curve).empty


def test_summary_adds_the_unrealized_to_the_realized_and_reads_the_two_latest_weeks():
    sim = _sim([
        ["2026-11-10", "old_win", "AAA", "LONG", "filled_tp1", "2026-11-10", 90.0, 10.0, "2026-11-12", "1.2"],
        ["2026-11-19", "last_week", "AAA", "LONG", "filled_time_exit", "2026-11-19", 100.0, 10.0, "2026-11-20", "0.4"],
        ["2026-11-20", "held", "AAA", "SHORT", "open", "2026-11-20", 104.0, 10.0, "", ""],      # -(101-104)/10 = +0.3
        ["2026-11-23", "this_week", "CCC", "LONG", "filled_sl", "2026-11-23", 47.0, 2.0, "2026-11-25", "-1.0"],
        ["2026-11-24", "held2", "CCC", "LONG", "open", "2026-11-24", 49.0, 2.0, "", ""],        # (46-49)/2 = -1.5
    ])
    s = ob.summary(sim, FRAMES)
    assert s["available"] and s["as_of"] == "2026-11-25"
    assert s["realized_r"] == pytest.approx(0.6) and s["mark_r"] == pytest.approx(-1.2) and s["equity_r"] == pytest.approx(-0.6)
    assert [(r["asset"], r["positions"], r["mark_r"]) for r in s["by_asset"]] == [("CCC", 1, -1.5), ("AAA", 1, 0.3)]   # 悪い順
    this_week = s["weeks"][-1]
    assert this_week["week_start"] == "2026-11-23" and this_week["last_day"] == "2026-11-25"
    # 前の週の最後の日（11/22・日）: 確定 1.6、建玉は held だけ（金曜の 104 → 0.0）
    assert this_week["change_r"] == pytest.approx(-0.6 - 1.6) and this_week["realized_change_r"] == pytest.approx(-1.0)
    assert s["weeks"][-2]["week_start"] == "2026-11-16" and len(s["weeks"]) == 2


def test_summary_says_unavailable_instead_of_zero_when_no_price_can_be_read(tmp_path):
    sim = _sim([["2026-11-20", "held", "AAA", "LONG", "open", "2026-11-20", 105.0, 10.0, "", ""]])
    s = ob.summary(sim, frames=None, raw_dir=tmp_path)     # 価格の置き場が空
    assert s["available"] is False and s["mark_r"] is None and s["equity_r"] is None and "価格" in s["reason"]
    assert ob.summary(sim, frames={})["available"] is False


def test_summary_handles_an_empty_table_and_a_table_without_the_needed_columns():
    assert ob.summary(pd.DataFrame(), FRAMES)["available"] is False
    assert ob.summary(pd.DataFrame({"asset": ["AAA"], "status": ["open"]}), FRAMES)["available"] is False
    assert ob.equity_curve(pd.DataFrame(), FRAMES, "2026-11-20", "2026-11-21").empty
    assert ob.positions(pd.DataFrame(), FRAMES).empty and ob.weekly_changes(pd.DataFrame()).empty


def test_values_read_as_text_by_the_dashboard_are_handled():
    # dashboard_io.read_csv は型を決めずに読む。空欄は NaN、数字は文字列のことがある
    sim = _sim([["2026-11-20", "held", "aaa ", " long", "open", "2026-11-20", "105.0", "10", float("nan"), float("nan")]])
    s = ob.summary(sim, FRAMES)
    assert s["positions"] == 1 and s["mark_r"] == pytest.approx(-0.4)


def test_a_mark_can_be_worse_than_minus_one_r_while_the_simulator_has_not_settled_the_row():
    # 最新の足が SL を越えていても、執行シミュレーションは形成途中の足では決着させない。含みはそのまま出す
    sim = _sim([["2026-11-24", "held", "AAA", "LONG", "open", "2026-11-24", 108.0, 5.0, "", ""]])   # (101-108)/5 = -1.4
    assert ob.summary(sim, FRAMES)["mark_r"] == pytest.approx(-1.4)


# --------------------------------------------------------------------------- ダッシュボード
def _dash_sim() -> pd.DataFrame:
    cols = COLS + ["rank", "risk_pct", "capital_pct"]
    rows = [
        ["2026-11-19", "w", "AAA", "LONG", "filled_tp1", "2026-11-19", 100.0, 10.0, "2026-11-20", "0.4", "B", 0.25, 0.1],
        ["2026-11-20", "h", "AAA", "LONG", "open", "2026-11-20", 105.0, 10.0, "", "", "B", 0.25, ""],
        ["2026-11-24", "u", "CCC", "LONG", "open", "", "", 2.0, "", "", "B", 0.25, ""],
    ]
    return pd.DataFrame(rows, columns=cols)


def _tile(k, v, sub="", cls=""):
    return f"[{k}|{v}|{sub}|{cls}]"


def test_dashboard_summary_carries_the_open_book():
    es = ds.execution_sim_summary(_dash_sim(), FRAMES)
    assert es["available"] and es["open_book"]["available"]
    assert es["open_book"]["positions"] == 1 and es["open_book"]["mark_r"] == pytest.approx(-0.4)
    assert es["open_book"]["unfilled_open"] == 1 and es["gross_total_r"] == pytest.approx(0.4)


def test_dashboard_block_shows_unrealized_total_and_the_weeks_change():
    book = ds.execution_sim_summary(_dash_sim(), FRAMES)["open_book"]
    text = dr.open_book_block(book, _tile)
    assert "[進行中の含み(未確定)|-0.4R|約定済み 1件・2026-11-25 までの値|negative]" in text
    assert "[確定＋含み|+0.0R|決着の合計 +0.4R に含みを足した値|]" in text
    # 前の週の最後の日（11/22）: 確定 +0.4、建玉 h は金曜の 104 で −0.1 → +0.3。今週は 11/25 の 101 で −0.4 → 0.0
    assert "[今週の変化(確定＋含み)|-0.3R|2026-11-23 の週・2026-11-25 まで／前の週 +0.3R|negative]" in text
    assert "確定した結果ではありません" in text and "まだ約定していない注文 1件" in text
    assert "<td>AAA</td><td>1</td><td>-0.4R</td><td>2026-11-25</td>" in text


def test_dashboard_block_says_not_computed_instead_of_showing_zero():
    for book in (None, {}, {"available": False, "reason": "価格（data/raw）を読めなかった"}):
        text = dr.open_book_block(book, _tile)
        assert "未計算" in text and "進行中の損益は入っていません" in text and "0.0R" not in text


def test_dashboard_block_reports_positions_that_could_not_be_measured():
    sim = _dash_sim()
    sim.loc[len(sim)] = ["2026-11-20", "z", "ZZZ", "LONG", "open", "2026-11-20", 10.0, 1.0, "", "", "B", 0.25, ""]
    text = dr.open_book_block(ds.execution_sim_summary(sim, FRAMES)["open_book"], _tile)
    assert "測れなかった建玉が 1件" in text


def test_dashboard_summary_survives_a_failure_inside_the_open_book(monkeypatch):
    def boom(*a, **k):
        raise RuntimeError("x")
    monkeypatch.setattr(ob, "summary", boom)
    es = ds.execution_sim_summary(_dash_sim(), FRAMES)
    assert es["available"] and es["open_book"] == {"available": False, "reason": "計算できなかった: RuntimeError"}
    assert math.isclose(es["gross_total_r"], 0.4)


def test_header_pill_shows_this_weeks_change_and_the_unrealized_total():
    es = ds.execution_sim_summary(_dash_sim(), FRAMES)
    pill = dr.week_change_pill(es)
    assert "今週の変化(擬似執行・確定＋含み)" in pill and "-0.3R／含み -0.4R" in pill and "pill-warn" in pill
    es["open_book"]["weeks"][-1]["change_r"] = 1.25
    assert "+1.2R／含み -0.4R" in dr.week_change_pill(es) and "pill-good" in dr.week_change_pill(es)


def test_header_pill_says_not_computed_when_the_open_book_is_unavailable():
    for es in (None, {}, {"open_book": {"available": False}}, {"open_book": {"available": True, "weeks": []}}):
        pill = dr.week_change_pill(es)
        assert "未計算" in pill and "pill-neutral" in pill


# --------------------------------------------------------------------------- 週末の読み（CLI）
def _cli():
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location("weekly_readout", Path(__file__).resolve().parents[1] / "tools" / "analysis" / "weekly_readout.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _write_inputs(tmp_path, rows):
    raw = tmp_path / "raw"
    raw.mkdir()
    for name, frame in (("AAA", AAA), ("CCC", CCC), ("DXY", AAA)):
        frame.assign(date=frame["date"].dt.strftime("%Y-%m-%d")).to_csv(raw / f"{name}.csv", index=False)
    sim_path = tmp_path / "sim.csv"
    _sim(rows).to_csv(sim_path, index=False)
    return sim_path, raw


CLI_ROWS = [
    ["2026-11-19", "last_week", "AAA", "LONG", "filled_time_exit", "2026-11-19", 100.0, 10.0, "2026-11-20", "0.4"],
    ["2026-11-20", "held", "AAA", "SHORT", "open", "2026-11-20", 104.0, 10.0, "", ""],          # +0.3
    ["2026-11-23", "this_week", "CCC", "LONG", "filled_sl", "2026-11-23", 47.0, 2.0, "2026-11-25", "-1.0"],
    ["2026-11-24", "held2", "CCC", "LONG", "open", "2026-11-24", 49.0, 2.0, "", ""],            # -1.5
    ["2026-11-24", "ctx", "DXY", "LONG", "open", "2026-11-24", 108.0, 10.0, "", ""],            # (101-108)/10 = -0.7
    ["2026-11-25", "wait", "AAA", "LONG", "open", "", "", 10.0, "", ""],
]


def test_cli_prints_the_weeks_change_split_into_realized_and_unrealized(tmp_path, capsys):
    sim_path, raw = _write_inputs(tmp_path, CLI_ROWS)
    assert _cli().main(["--weeks", "1", "--sim", str(sim_path), "--raw-dir", str(raw)]) == 0
    out = capsys.readouterr().out
    assert "# 週末の読み（2026-11-25 までの値。週は月曜〜日曜。文脈用の資産: DXY, US10Y）" in out
    # 取引する資産: 前の週の最後（11/22）は 確定 +0.4・含み 0.0。今週は 確定 −0.6・含み +0.3−1.5 → −1.8。変化 −2.2
    block = out.split("取引する資産")[1].split("文脈用の資産")[0]
    assert "11/23 の週（11/25 まで）: 変化 -2.20R（うち確定 -1.00R） / 週の終わりの含み -1.20R" in block
    assert "全資産: 3 件 / 含み -1.90R / 決着の合計 -0.60R / 確定＋含み -2.50R / まだ約定していない 1 件 / 測れない 0 件" in out
    assert "DXY（文脈用）: 1 件 / 含み -0.70R" in out
    assert "今週（11/23〜）に決着した行: 1 件 / 合計 -1.00R" in out and "判断 11/23 CCC LONG → 11/25 SL -1.00R" in out


def test_cli_week_table_counts_each_status_of_the_orders_decided_that_week(tmp_path, capsys):
    sim_path, raw = _write_inputs(tmp_path, CLI_ROWS)
    cli = _cli()
    sim = pd.read_csv(sim_path)
    frames = ob.load_frames(sim["asset"].unique(), raw)
    pos = ob.positions(sim, frames)
    t = cli.week_table(ob.prepare(sim), pd.Series(pos["mark_r"].values, index=pos["row"].values, dtype=float)).set_index("週(月曜)")
    assert t.loc["11/16", ["注文", "決着", "時間決済", "確定R", "進行中(約定済み)", "含みR"]].tolist() == [2, 1, 1, 0.4, 1, 0.3]
    assert t.loc["11/23", ["注文", "決着", "SL", "確定R", "進行中(約定済み)", "含みR", "まだ約定していない"]].tolist() == [4, 1, 1, -1.0, 2, -2.2, 1]


def test_cli_fails_clearly_without_prices_or_without_the_table(tmp_path, capsys):
    sim_path, raw = _write_inputs(tmp_path, CLI_ROWS)
    empty = tmp_path / "empty"
    empty.mkdir()
    assert _cli().main(["--sim", str(sim_path), "--raw-dir", str(empty)]) == 1
    assert "読めなかった" in capsys.readouterr().out
    assert _cli().main(["--sim", str(tmp_path / "nope.csv"), "--raw-dir", str(raw)]) == 1
    assert "が無い" in capsys.readouterr().out


# --------------------------------------------------------------------------- 測れない建玉がある週（#241 Codex P2）
def _two_asset_sim():
    # ZZZ は価格が無い。先週は建玉、今週 +1.0R で決着。AAA は先週から建玉のまま
    return _sim([
        ["2026-11-19", "z", "ZZZ", "LONG", "filled_time_exit", "2026-11-19", 10.0, 1.0, "2026-11-24", "1.0"],
        ["2026-11-20", "a", "AAA", "LONG", "open", "2026-11-20", 105.0, 10.0, "", ""],
    ])


def test_weekly_change_is_withheld_when_an_endpoint_has_unmeasured_positions():
    # 先週の終わり（11/22）に ZZZ が測れない。ZZZ の含みが +2R だったなら本当の変化は −1R 側で、出てくる数字と符号が逆になりうる
    wk = ob.weekly_changes(ob.equity_curve(_two_asset_sim(), FRAMES, "2026-11-09", "2026-11-25")).iloc[-1]
    assert bool(wk["incomplete"]) and wk["prev_unmeasured"] == 1 and wk["unmeasured"] == 0
    assert math.isnan(wk["change_r"])
    assert wk["realized_change_r"] == pytest.approx(1.0)      # 確定ぶんは価格に依らないので出す
    assert wk["equity_r"] == pytest.approx(1.0 - 0.4)         # 最新の日は全部測れている


def test_weekly_change_is_withheld_when_the_latest_day_has_unmeasured_positions():
    sim = _sim([
        ["2026-11-24", "z", "ZZZ", "LONG", "open", "2026-11-24", 10.0, 1.0, "", ""],
        ["2026-11-20", "a", "AAA", "LONG", "open", "2026-11-20", 105.0, 10.0, "", ""],
    ])
    wk = ob.weekly_changes(ob.equity_curve(sim, FRAMES, "2026-11-09", "2026-11-25")).iloc[-1]
    assert bool(wk["incomplete"]) and wk["unmeasured"] == 1 and wk["prev_unmeasured"] == 0
    assert math.isnan(wk["change_r"]) and math.isnan(wk["equity_r"]) and math.isnan(wk["mark_r"])


def test_summary_and_dashboard_do_not_name_a_change_for_an_incomplete_week():
    es = ds.execution_sim_summary(_two_asset_sim().assign(rank="B", risk_pct=0.25, capital_pct=""), FRAMES)
    week = es["open_book"]["weeks"][-1]
    assert week["incomplete"] is True and week["change_r"] is None and week["realized_change_r"] == pytest.approx(1.0)
    # いまの建玉は全部測れているので、建玉の注意書きには何も出ない。週のほうで知らせる
    assert es["open_book"]["unmeasured"] == 0
    text = dr.open_book_block(es["open_book"], _tile)
    assert "[今週の変化(確定＋含み)|—|2026-11-23 の週・2026-11-25 まで／測れない建玉があり比べられません（前の週の終わり 1件・最新 0件）。確定ぶんの変化は +1.0R|]" in text
    pill = dr.week_change_pill(es)
    assert "比べられない(測れない建玉あり)" in pill and "pill-neutral" in pill and "+1.0R" not in pill


def test_a_complete_week_after_an_incomplete_one_is_reported_normally():
    # ZZZ が 11/13 に決着して以後は全部測れる。11/16 の週は 11/15 と 11/22 を比べるので、変化を出してよい
    sim = _sim([
        ["2026-11-10", "z", "ZZZ", "LONG", "filled_time_exit", "2026-11-10", 10.0, 1.0, "2026-11-13", "1.0"],
        ["2026-11-20", "a", "AAA", "LONG", "open", "2026-11-20", 105.0, 10.0, "", ""],
    ])
    wk = ob.weekly_changes(ob.equity_curve(sim, FRAMES, "2026-11-02", "2026-11-25")).set_index("week_start")
    assert bool(wk.loc[pd.Timestamp("2026-11-09"), "incomplete"]) is False      # 11/08 は建玉なし、11/15 は決着済み
    assert wk.loc[pd.Timestamp("2026-11-09"), "change_r"] == pytest.approx(1.0)
    assert bool(wk.loc[pd.Timestamp("2026-11-16"), "incomplete"]) is False
    assert wk.loc[pd.Timestamp("2026-11-16"), "change_r"] == pytest.approx(-0.1)


def test_cli_says_the_change_cannot_be_given_for_an_incomplete_week(tmp_path, capsys):
    sim_path, raw = _write_inputs(tmp_path, _two_asset_sim().values.tolist())
    assert _cli().main(["--weeks", "1", "--context-assets", "", "--sim", str(sim_path), "--raw-dir", str(raw)]) == 0
    out = capsys.readouterr().out
    assert "11/23 の週（11/25 まで）: 変化は出せない（測れない建玉が、前の週の終わりに 1 件・この週の終わりに 0 件） / 確定ぶんの変化 +1.00R" in out
