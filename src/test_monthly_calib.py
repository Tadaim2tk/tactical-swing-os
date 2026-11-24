"""tools/analysis/monthly_calib.py と tools/monthly_calibration_run.py — 月次較正の草稿が毎月同じ物差しで出ること。
10月は月次が3つとも抜けた（遡及コーパスの延長・数値・文書）。草稿は入力が欠けていても必ず出る。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "analysis"))
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))
import monthly_calib as mc  # noqa: E402
import monthly_calibration_run as run  # noqa: E402

LED_COLS = ["date", "signal_id", "asset", "side", "rank", "type", "entry_low", "entry_high", "sl", "tp1", "tp2", "rr", "win_prob",
            "expected_r", "tq_score", "opp_score", "no_trade_score", "risk_pct", "regime", "ems", "ffs", "cds", "ias", "cbs", "mes",
            "invalidation", "verification_target", "verified_status", "origin"]


def _root(tmp_path: Path, with_raw: bool = False) -> Path:
    (tmp_path / "data" / "raw").mkdir(parents=True)
    (tmp_path / "data" / "retro").mkdir()
    (tmp_path / "config").mkdir()
    rows = []
    for d in pd.date_range("2026-09-01", "2026-10-31", freq="D"):
        ds = d.strftime("%Y-%m-%d")
        for a in ["GOLD", "WTI", "BTC"]:
            if a == "WTI" and d.weekday() == 0:
                rows.append([ds, f"{ds.replace('-', '')}_{a}_BUY_PULLBACK", a, "BUY", "B", "PULLBACK", 90, 91, 88, 95, 97, 1.6, 0.55, 0.3,
                             60, 60, 40, 0.25, "MIXED", 70, 70, 70, 70, 75, 60, "x", "y", "verified", "chatgpt_app"])
            else:
                rows.append([ds, f"{ds.replace('-', '')}_{a}_NONE_NO_TRADE", a, "NONE", "NO_TRADE", "NO_TRADE", "", "", "", "", "", "", "", "",
                             60, 60, 80, "", "EVENT", 60, 60, 60, 60, 60, 60, "", "", "verified", "chatgpt_app"])
    pd.DataFrame(rows, columns=LED_COLS).to_csv(tmp_path / "data" / "signal_log.csv", index=False)
    (tmp_path / "data" / "execution_simulation.csv").write_text("date,signal_id,asset,side,rank,status,fill_date,fill_price,risk_unit,exit_date,r_result,atr_floor_r,atr_floor_widened,chase_r,half_exit_r,half_exit_be_r,forgone_r\n", encoding="utf-8")
    (tmp_path / "data" / "prediction_log_scores.csv").write_text("date,signal_id,asset,side,rank,actionable,result_5d,r_close_5d\n", encoding="utf-8")
    (tmp_path / "data" / "leader_observations.csv").write_text("date,leader_claimed,source,recorded_at\n2026-10-02,WTI,chatgpt_app,x\n", encoding="utf-8")
    (tmp_path / "data" / "invalidation_checks.csv").write_text("check_date,signal_id,invalidation_fired,source,recorded_at\n", encoding="utf-8")
    (tmp_path / "data" / "crypto_predictions_weekly.csv").write_text("week_start,asset,direction,level,deadline,source,recorded_at\n", encoding="utf-8")
    (tmp_path / "data" / "crypto_context_weekly.csv").write_text("week_start,driver,etf_flow_dir,cme_basis,regulation_event,confidence,prev_result,source,recorded_at\n", encoding="utf-8")
    (tmp_path / "config" / "interventions.json").write_text(json.dumps({"interventions": [
        {"date": "2026-10-08", "label": "in_month"}, {"date": "2026-09-20", "label": "14d_before"},
        {"date": "2026-09-10", "label": "too_early"}, {"date": "2026-11-04", "label": "later_month"}]}), encoding="utf-8")
    if with_raw:
        days = pd.bdate_range("2026-08-01", "2026-10-31")
        pd.DataFrame({"date": days.strftime("%Y-%m-%d"), "open": 90.0, "high": 92.0, "low": 89.0, "close": 90.5, "adj_close": 90.5, "volume": 1}).to_csv(tmp_path / "data" / "raw" / "WTI.csv", index=False)
    return tmp_path


def test_draft_is_written_even_with_sparse_inputs(tmp_path):
    root = _root(tmp_path)
    md, R = mc.build(root, "2026-10")
    assert "# 月次較正 2026-10" in md and "## 決定待ち" in md
    for h in ["## 0.", "## 1.", "## 2.", "## 3.", "## 4.", "## 5.", "## 6.", "## 7.", "## 8."]:
        assert h in md, h
    assert not R.get("errors"), R.get("errors")  # 入力が空でも節は例外にならない(「価格系列が無い」の注記は例外ではない)
    assert R["throughput"] and any(r["month"] == "2026-10" for r in R["throughput"])
    assert "価格系列(data/raw)が無い" in md or "SL幅÷ATR10" in md


def test_sl_atr_uses_raw_prices_when_present(tmp_path):
    root = _root(tmp_path, with_raw=True)
    md, R = mc.build(root, "2026-10")
    assert "sl_atr_by_month" in R and any(r["month"] == "2026-10" for r in R["sl_atr_by_month"])
    # WTI: SL幅 = |90.5-88| = 2.5、ATR10 = 3.0（高値-安値=3、前日終値の差は 1.5/1.5） → 0.83
    row = [r for r in R["sl_atr_by_month"] if r["month"] == "2026-10"][0]
    assert abs(float(row["sl_atr_med"]) - 0.83) < 0.02 and int(float(row["below_1atr"])) > 0


def _order(ds: str, asset: str, entry_low, entry_high, sl, tp1, side: str = "BUY") -> list:
    """rank B の注文1行（LED_COLS の並び）。"""
    return [ds, f"{ds.replace('-', '')}_{asset}_{side}_PULLBACK", asset, side, "B", "PULLBACK", entry_low, entry_high, sl, tp1, "", 1.6, 0.55, 0.3,
            60, 60, 40, 0.25, "MIXED", 70, 70, 70, 70, 75, 60, "x", "y", "verified", "chatgpt_app"]


def _add_orders(root: Path, rows: list) -> None:
    led = pd.read_csv(root / "data" / "signal_log.csv")
    pd.concat([led, pd.DataFrame(rows, columns=LED_COLS)], ignore_index=True).to_csv(root / "data" / "signal_log.csv", index=False)


def _write_bars(root: Path, asset: str, days, base: float, rng: float = 100.0, ranges: dict | None = None, opens: dict | None = None) -> None:
    """終値は base で一定、値幅は rng（日付ごとに ranges で差し替え）。真の値幅 = 高値 − 安値 になる。"""
    rows = []
    for d in days:
        ds = d.strftime("%Y-%m-%d")
        r = (ranges or {}).get(ds, rng)
        rows.append({"date": ds, "open": (opens or {}).get(ds, base), "high": base + r / 2, "low": base - r / 2, "close": base, "volume": 1})
    pd.DataFrame(rows).to_csv(root / "data" / "raw" / f"{asset}.csv", index=False)


def test_atr_is_cut_at_the_bars_closed_at_decision_time_like_the_simulation(tmp_path):
    """暗号資産の前日の足は、判断(07:00 JST)の2時間後に閉じる。月次の ATR10 も、執行シミュレーションと同じく1本手前で切る。

    10/15 の BTC の注文。前日(10/14)だけ値幅が 1100、ほかは 100。SL幅は 150。
    日付が判断日より前の足で切る（初版）: ATR10 = (9×100 + 1100)/10 = 200 → 0.75（1.0 未満）
    判断時に閉まっていた足で切る:          ATR10 = 100                  → 1.5
    """
    root = _root(tmp_path, with_raw=True)
    _add_orders(root, [_order("2026-10-15", "BTC", 49950, 50050, 49850, 50400)])
    _write_bars(root, "BTC", pd.date_range("2026-09-01", "2026-10-31", freq="D"), base=50000.0, ranges={"2026-10-14": 1100.0})
    prices = mc.Prices(root)
    assert abs(prices.atr10_at_decision("BTC", pd.Timestamp("2026-10-15")) - 100.0) < 1e-9
    assert abs(prices.atr10_at_decision("WTI", pd.Timestamp("2026-10-12")) - 3.0) < 1e-9   # 週5日の資産は前日までで変わらない
    # 執行シミュレーションが atr_floor に使う値と同じであること（同じ関数を呼んでいる）
    import simulate_execution as se
    from score_prediction_log import decision_time_anchor, load_ohlcv_frame
    o = load_ohlcv_frame("BTC", raw_dir=root / "data" / "raw")
    assert prices.atr10_at_decision("BTC", pd.Timestamp("2026-10-15")) == se.atr_at_decision(o, decision_time_anchor(o, "2026-10-15")[1])
    _, R = mc.build(root, "2026-10")
    row = [r for r in R["sl_atr_by_month"] if r["month"] == "2026-10"][0]
    assert int(float(row["below_1atr"])) == 4          # 月曜の WTI 4件(0.83)だけ。BTC は 1.5 で入らない


def test_rows_and_measured_rows_are_reported_separately(tmp_path):
    """比率を測れなかった行（SL が欠けている・価格系列が無い資産）を、中央値の母数のように見せない。"""
    root = _root(tmp_path, with_raw=True)
    _add_orders(root, [_order("2026-10-14", "WTI", 90, 91, "", 95),             # SL が欠けている
                       _order("2026-10-15", "QQQ", 700, 702, 690, 720)])        # 価格系列が無い資産
    md, R = mc.build(root, "2026-10")
    row = [r for r in R["sl_atr_by_month"] if r["month"] == "2026-10"][0]
    assert "n" not in row
    assert (int(float(row["rows"])), int(float(row["measured"]))) == (6, 4)     # 月曜の WTI 4件 + 測れない2件
    assert abs(float(row["sl_atr_med"]) - 0.83) < 0.02 and int(float(row["below_1atr"])) == 4
    sec = md.split("## 1.")[1].split("## 2.")[0]
    assert "| month | rows | measured | sl_atr_med | below_1atr |" in sec


SIM_COLS = ["date", "signal_id", "asset", "side", "rank", "status", "fill_date", "fill_price", "risk_unit", "exit_date", "r_result",
            "atr_floor_r", "atr_floor_widened", "chase_r", "half_exit_r", "half_exit_be_r", "forgone_r"]


def _fired_root(tmp_path: Path) -> Path:
    """invalidation の fired を6通り置く。GOLD は終値 100 で一定、買い・建値 100・SL幅 10。"""
    root = _root(tmp_path)
    days = {"AMBIG": "2026-09-03", "LATE": "2026-09-04", "DAILY": "2026-09-22", "UNFILLED": "2026-10-06", "GAP": "2026-10-13", "OLD": "2026-07-01"}
    _add_orders(root, [_order(d, "GOLD", 99, 100, 90, 115) for d in days.values()])
    sid = {k: f"{d.replace('-', '')}_GOLD_BUY_PULLBACK" for k, d in days.items()}

    def sim(key, status, fill, exit_, r):
        return [days[key], sid[key], "GOLD", "LONG", "B", status, fill, 100.0 if fill else "", 10.0 if fill else "", exit_, r, "", "", "", "", "", ""]
    pd.DataFrame([
        sim("AMBIG", "filled_sl", "2026-09-08", "2026-09-11", -1.0),     # 3営業日後に約定、そのあと SL
        sim("LATE", "filled_sl", "2026-09-04", "2026-09-04", -1.0),      # 判断の当日に約定して SL
        sim("DAILY", "filled_sl", "2026-09-23", "2026-09-25", -1.0),
        sim("UNFILLED", "no_fill", "", "", ""),
        sim("GAP", "filled_sl", "2026-10-13", "2026-10-16", -1.0),
        sim("OLD", "filled_sl", "2026-07-01", "2026-07-06", -1.0),
    ], columns=SIM_COLS).to_csv(root / "data" / "execution_simulation.csv", index=False)
    checks = [
        ("2026-09-09", sid["AMBIG"], "fired"),                            # 最初の確認が4営業日後（まとめて聞き直した形）
        ("2026-09-09", sid["LATE"], "fired"),
        ("2026-09-22", sid["DAILY"], "not_fired"), ("2026-09-23", sid["DAILY"], "not_fired"),
        ("2026-09-24", sid["DAILY"], "fired"), ("2026-09-25", sid["DAILY"], "fired"),   # 翌日の fired は同じ発動の再確認
        ("2026-10-09", sid["UNFILLED"], "fired"),
        ("2026-10-13", sid["GAP"], "not_fired"), ("2026-10-14", sid["GAP"], "unknown"), ("2026-10-15", sid["GAP"], "fired"),
        ("2026-07-03", sid["OLD"], "fired"),                              # 価格の窓(8/17〜)より前
    ]
    pd.DataFrame([(d, s, v, "chatgpt_app", "x") for d, s, v in checks],
                 columns=["check_date", "signal_id", "invalidation_fired", "source", "recorded_at"]).to_csv(
        root / "data" / "invalidation_checks.csv", index=False)
    _write_bars(root, "GOLD", pd.bdate_range("2026-08-17", "2026-10-30"), base=100.0, rng=2.0,
                opens={"2026-09-09": 99.0, "2026-09-24": 99.5, "2026-09-25": 98.0, "2026-10-14": 98.0, "2026-10-15": 97.0})
    return root


def _fired(R: dict) -> dict:
    return {r["signal_id"][:8]: r for r in R["fired"]}


def test_a_fired_report_is_counted_as_an_exit_only_when_the_firing_day_is_known(tmp_path):
    """check_date は「聞いた日」であって「発動した日」ではない。

    前の確認(not_fired。無ければ判断日)から fired の確認までに取引が2本以上あり、最も早く知らされた場合と
    実際に知らされた日とで結論が変わる行は、「降りられた」に数えない（2026-09-09 にまとめて聞き直した GOLD の形）。
    """
    md, R = mc.build(_fired_root(tmp_path), "2026-10")
    assert not R.get("errors"), R.get("errors")
    f = _fired(R)
    # 毎日聞いていて、前日は not_fired: 発動は1本の中。発動の翌朝の寄り(99.5)で降りる = −0.05R
    assert f["20260922"]["kind"] == "降りられた" and f["20260922"]["window_bars"] == "1"
    assert abs(float(f["20260922"]["r_if_exit_on_fired"]) - (-0.05)) < 1e-9
    # 最初の確認が4営業日後。最も早い報告なら未約定(0R)、実際の報告なら寄りで降りる(−0.1R) → 数えない・Rを書かない
    assert f["20260903"]["kind"] == "発動日が幅でしか分からない(4本。最も早い報告なら未約定)"
    assert f["20260903"]["r_if_exit_on_fired"] == ""
    # 間に unknown の日がある。unknown は「まだ発動していない」の証拠にならないので幅は2本。降りる値段が変わる → 数えない
    assert f["20261013"]["kind"] == "発動日が幅でしか分からない(2本。最も早い報告なら降りられた)"
    kinds = R["fired_kinds"]
    assert kinds["降りられた"] == 1 and kinds["発動日が幅でしか分からない"] == 2
    sec = md.split("## 5.")[1].split("## 6.")[0]
    assert "降りられた 1 件: 既定 -1.00R vs 発動で降りる -0.05R" in sec
    assert "発動日が幅でしか分からない 2 件は、降りられた・手遅れ・未約定のどれにも数えていない" in sec


def test_a_wide_window_does_not_change_a_verdict_that_holds_for_every_possible_report_day(tmp_path):
    """幅が広くても、どの朝に知らされても同じ結論になる行は、そのまま数える。"""
    _, R = mc.build(_fired_root(tmp_path), "2026-10")
    f = _fired(R)
    # 判断の当日に約定して SL。最も早い報告(翌朝)でも既に決着している
    assert f["20260904"]["kind"] == "手遅れ(既に filled_sl)" and f["20260904"]["window_bars"] == "3"
    assert float(f["20260904"]["r_if_exit_on_fired"]) == -1.0
    # 約定していない注文は、いつ知らされても取り消すだけ
    assert f["20261006"]["kind"] == "未約定(注文取消で済む)" and float(f["20261006"]["r_if_exit_on_fired"]) == 0.0


def test_a_repeated_fired_answer_is_one_report_and_old_rows_are_not_priced_from_the_window_head(tmp_path):
    md, R = mc.build(_fired_root(tmp_path), "2026-10")
    assert len(R["fired"]) == 6                                   # fired は7行。同じ判断の翌日の fired は数えない
    assert "同じ判断への fired の再確認 1 行は数えていない" in md
    old = _fired(R)["20260701"]
    # 価格の窓(8/17〜)が判断日に届かない。窓の先頭の寄りで「降りられた」ことにしない
    assert old["kind"] == "価格の窓の外(測り直せない)" and old["r_if_exit_on_fired"] == "" and old["window_bars"] == ""


def test_fire_window_starts_at_the_last_not_fired_check_or_the_decision_day():
    checks = pd.DataFrame({"signal_id": ["S", "S", "S", "T"],
                           "check_date": pd.to_datetime(["2026-10-13", "2026-10-14", "2026-10-15", "2026-10-14"]),
                           "invalidation_fired": ["not_fired", "unknown", "fired", "not_fired"]})
    sig = pd.Timestamp("2026-10-10")
    assert mc.fire_window_start(checks, "S", pd.Timestamp("2026-10-15"), sig) == pd.Timestamp("2026-10-13")   # unknown は幅を縮めない
    assert mc.fire_window_start(checks, "S", pd.Timestamp("2026-10-13"), sig) == sig                          # 前の確認が無ければ判断日
    assert mc.fire_window_start(checks, "U", pd.Timestamp("2026-10-15"), sig) == sig                          # 別の判断の確認は使わない


def test_runner_writes_report_and_docs_without_overwriting(tmp_path):
    root = _root(tmp_path)
    (root / "docs").mkdir()
    (root / "docs" / "monthly_calibration_2026-10.md").write_text("手書き", encoding="utf-8")
    rc = run.main(["--root", str(root), "--month", "2026-10", "--no-extend", "--docs"])
    assert rc == 0
    assert (root / "reports" / "monthly" / "2026-10_calibration_draft.md").exists()
    assert (root / "docs" / "monthly_calibration_2026-10.md").read_text(encoding="utf-8") == "手書き"  # 既存は守る
    assert (root / "docs" / "monthly_calibration_2026-10.draft.md").exists()
    rc2 = run.main(["--root", str(root), "--month", "2026-09", "--no-extend", "--docs"])
    assert rc2 == 0 and (root / "docs" / "monthly_calibration_2026-09.md").exists()


def _capture_extend_calls(monkeypatch):
    """延長の subprocess を差し替え、呼ばれた回数だけ数える（ネットワークに出ない）。"""
    calls = []

    class _Done:
        returncode = 0
        stdout = "extended\n"
        stderr = ""

    def fake_run(cmd, **kwargs):
        calls.append([str(c) for c in cmd])
        return _Done()

    monkeypatch.setattr(run.subprocess, "run", fake_run)
    return calls


def test_runner_accepts_explicit_extend_flag(tmp_path, monkeypatch):
    """月次の自動化（Codex）の手順書は --extend --docs で呼ぶ。未定義の旗で exit 2 にならないこと。"""
    root = _root(tmp_path)
    calls = _capture_extend_calls(monkeypatch)
    rc = run.main(["--root", str(root), "--month", "2026-10", "--extend", "--docs"])
    assert rc == 0
    assert len(calls) == 1 and calls[0][-1] == "--extend" and calls[0][-2].endswith("retro_build_market.py")
    assert (root / "reports" / "monthly" / "2026-10_calibration_draft.md").exists()


def test_runner_extends_by_default_and_skips_with_no_extend(tmp_path, monkeypatch):
    root = _root(tmp_path)
    calls = _capture_extend_calls(monkeypatch)
    assert run.main(["--root", str(root), "--month", "2026-10"]) == 0
    assert len(calls) == 1
    assert run.main(["--root", str(root), "--month", "2026-10", "--no-extend"]) == 0
    assert len(calls) == 1          # --no-extend では呼ばれない


def test_runner_rejects_extend_with_no_extend(tmp_path, monkeypatch):
    root = _root(tmp_path)
    _capture_extend_calls(monkeypatch)
    with pytest.raises(SystemExit) as e:
        run.main(["--root", str(root), "--month", "2026-10", "--extend", "--no-extend"])
    assert e.value.code == 2


def test_default_month_is_previous_month(monkeypatch):
    import datetime as dt

    class D(dt.date):
        @classmethod
        def today(cls):
            return cls(2026, 11, 9)
    monkeypatch.setattr(mc, "date", D)
    assert mc.default_month() == "2026-10"


def test_intervention_table_is_bounded_by_the_target_month(tmp_path):
    """過去月の草稿に、後の月の介入を混ぜない(#206 Codex P2)。対象月の14日前〜月末だけ。"""
    root = _root(tmp_path)
    md, _ = mc.build(root, "2026-10")
    sec = md.split("## 8.")[1].split("## 決定待ち")[0]
    assert "in_month" in sec and "14d_before" in sec
    assert "too_early" not in sec and "later_month" not in sec
    assert "| index |" not in sec          # 絞ったあとの行番号を列として出さない(pandas の版で出たり出なかったりした)

