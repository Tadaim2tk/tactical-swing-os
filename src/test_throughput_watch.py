"""tools/throughput_watch.py — 売買頻度の監視（2026-11-02）。

8月は78行の注文が8本の見立てだった。注文の数だけ見ると記帳の仕方の変化で崖に見え、
見立ての数だけ見ると再発行の多さが隠れる。両方を数え、床と比で判定することを確かめる。
"""
from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import throughput_watch as tw  # noqa: E402

TOOL = ROOT / "tools" / "throughput_watch.py"
ASSETS = ["GOLD", "BTC", "ETH", "WTI", "USDJPY", "SPX", "NASDAQ", "DXY", "US10Y", "VIX"]
COLS = ["date", "signal_id", "asset", "side", "rank", "type", "risk_pct"]


def make_ledger(start: str, days: int, orders: dict[str, list[tuple[str, str]]]) -> pd.DataFrame:
    """毎日10資産。orders[date] = [(asset, side), ...] を A/B 行にする。"""
    rows = []
    for d in pd.date_range(start, periods=days, freq="D"):
        ds = d.strftime("%Y-%m-%d")
        todays = dict(orders.get(ds, []))
        for a in ASSETS:
            if a in todays:
                rows.append([ds, f"{ds.replace('-', '')}_{a}_{todays[a]}_PULLBACK", a, todays[a], "B", "PULLBACK", "0.25"])
            else:
                rows.append([ds, f"{ds.replace('-', '')}_{a}_NONE_NO_TRADE", a, "NONE", "NO_TRADE", "NO_TRADE", ""])
    return pd.DataFrame(rows, columns=COLS)


def write(df: pd.DataFrame, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


def steady(start, days, per_week=2, assets=("GOLD", "WTI", "BTC", "NASDAQ")):
    """週に per_week 本、別々の資産で単発の見立てを置く。"""
    orders = {}
    i = 0
    for d in pd.date_range(start, periods=days, freq="D"):
        if d.weekday() in (0, 3)[:per_week]:
            orders[d.strftime("%Y-%m-%d")] = [(assets[i % len(assets)], "BUY" if i % 2 == 0 else "SELL")]
            i += 1
    return orders


def test_runs_count_reissues_as_one_idea():
    # WTI BUY を10日続ける(土日含む) → 注文10行、見立て1本
    orders = {d.strftime("%Y-%m-%d"): [("WTI", "BUY")] for d in pd.date_range("2026-08-01", periods=10)}
    led = tw.load_ledger(write(make_ledger("2026-08-01", 10, orders), Path("/tmp/_tw_runs.csv")))
    o = tw.mark_runs(led)
    assert len(o) == 10 and int(o["run_start"].sum()) == 1


def test_gap_over_three_days_starts_new_idea():
    orders = {"2026-08-03": [("GOLD", "BUY")], "2026-08-06": [("GOLD", "BUY")], "2026-08-11": [("GOLD", "BUY")]}
    led = tw.load_ledger(write(make_ledger("2026-08-01", 14, orders), Path("/tmp/_tw_gap.csv")))
    o = tw.mark_runs(led)
    # 8/3→8/6 は3日(金→月相当)で同じ見立て、8/6→8/11 は5日で新しい見立て
    assert int(o["run_start"].sum()) == 2


def test_long_short_normalized_to_buy_sell():
    orders = {"2026-08-03": [("GOLD", "LONG")], "2026-08-04": [("GOLD", "BUY")], "2026-08-05": [("GOLD", "SHORT")]}
    led = tw.load_ledger(write(make_ledger("2026-08-01", 7, orders), Path("/tmp/_tw_side.csv")))
    o = tw.mark_runs(led)
    assert sorted(o["side_n"].unique()) == ["BUY", "SELL"] and int(o["run_start"].sum()) == 2


def test_ok_when_steady():
    days = 70
    led = tw.load_ledger(write(make_ledger("2026-06-01", days, steady("2026-06-01", days)), Path("/tmp/_tw_ok.csv")))
    res = tw.evaluate(led, led["date"].max())
    assert res["status"] == "OK", res


def test_alert_when_window_is_empty():
    days = 70
    orders = steady("2026-06-01", days)
    cutoff = pd.Timestamp("2026-06-01") + pd.Timedelta(days=56)
    orders = {d: v for d, v in orders.items() if pd.Timestamp(d) < cutoff}
    led = tw.load_ledger(write(make_ledger("2026-06-01", days, orders), Path("/tmp/_tw_alert.csv")))
    res = tw.evaluate(led, led["date"].max())
    assert res["status"] == "ALERT" and res["window"]["ideas"] == 0


def test_accounting_change_is_warn_not_alert():
    """基準期間は同じ2本の見立てを毎日書き直す(注文多)、窓は同じ2本/週を単発で書く(注文少)。
    注文は半分以下に落ちるが見立ては落ちていない → WARN と「記帳の仕方の変化」の注記。"""
    days = 70
    orders = {}
    for d in pd.date_range("2026-06-01", periods=56):
        orders[d.strftime("%Y-%m-%d")] = [("WTI", "BUY"), ("GOLD", "SELL")] if d.weekday() < 5 else []
    # 基準56日で WTI BUY / GOLD SELL は連続 → 見立て 2本、注文 80行
    # 窓14日: 週2本の単発を別資産で
    orders.update(steady("2026-07-27", 14, assets=("BTC", "NASDAQ", "USDJPY", "SPX")))
    led = tw.load_ledger(write(make_ledger("2026-06-01", days, orders), Path("/tmp/_tw_acct.csv")))
    res = tw.evaluate(led, led["date"].max())
    assert res["orders_ratio"] is not None and res["orders_ratio"] <= 0.5
    assert res["ideas_ratio"] is not None and res["ideas_ratio"] > 1.0  # 見立ては増えている
    assert res["status"] == "WARN"
    assert any("記帳の仕方" in n for n in res["notes"])


def test_insufficient_data_when_ledger_has_gaps():
    led = tw.load_ledger(write(make_ledger("2026-06-01", 60, steady("2026-06-01", 60)), Path("/tmp/_tw_gap2.csv")))
    # 窓の最後の14日のうち台帳があるのは2日だけ、という状況を as_of を未来にずらして作る
    res = tw.evaluate(led, led["date"].max() + pd.Timedelta(days=12))
    assert res["status"] == "INSUFFICIENT_DATA"


def test_no_baseline_uses_floor_only():
    led = tw.load_ledger(write(make_ledger("2026-06-01", 20, steady("2026-06-01", 20)), Path("/tmp/_tw_nobase.csv")))
    res = tw.evaluate(led, led["date"].max())
    assert "no_baseline" in res["notes"] and res["status"] in ("OK", "WARN")
    led2 = tw.load_ledger(write(make_ledger("2026-06-01", 20, {}), Path("/tmp/_tw_nobase2.csv")))
    assert tw.evaluate(led2, led2["date"].max())["status"] == "ALERT"


def test_history_escalates_long_warn_to_alert():
    """見立て3本/14日(=WARN帯)が続く台帳。WARN が14日続いた日から ALERT。"""
    days = 120
    orders = steady("2026-06-01", 70)  # 基準は 2本/週
    # 7/11 以降は 1.5本/週 相当: 月曜だけ、ただし2週に1回は木曜も
    k = 0
    for d in pd.date_range("2026-07-11", periods=50):
        if d.weekday() == 0 or (d.weekday() == 3 and (d.isocalendar()[1] % 2 == 0)):
            orders[d.strftime("%Y-%m-%d")] = [(ASSETS[k % 4], "BUY")]
            k += 1
    led = tw.load_ledger(write(make_ledger("2026-06-01", days, orders), Path("/tmp/_tw_hist.csv")))
    h = tw.history(led)
    assert set(h["status"]) & {"WARN", "ALERT"}
    esc = h[h["note"].str.contains("escalated")]
    raw_alert = h[(h["status"] == "ALERT") & ~h["note"].str.contains("escalated")]
    # 昇格した日が存在し、その直前14日はすべて OK でない
    if not esc.empty:
        first = esc.iloc[0]
        idx = h.index[h["as_of"] == first["as_of"]][0]
        assert all(s != "OK" for s in h.loc[idx - 13:idx, "status"])
    else:
        assert not raw_alert.empty  # 昇格の前に生の ALERT が出た


def test_alert_episodes_groups_consecutive_days():
    h = pd.DataFrame({"as_of": pd.date_range("2026-09-01", periods=6).date,
                      "status": ["OK", "ALERT", "ALERT", "WARN", "ALERT", "OK"]})
    assert tw.alert_episodes(h) == [("2026-09-02", "2026-09-03"), ("2026-09-05", "2026-09-05")]


def test_cli_writes_csv_idempotently_and_exit_code(tmp_path):
    days = 70
    orders = steady("2026-06-01", days)
    cutoff = pd.Timestamp("2026-06-01") + pd.Timedelta(days=56)
    orders = {d: v for d, v in orders.items() if pd.Timestamp(d) < cutoff}
    ledger = write(make_ledger("2026-06-01", days, orders), tmp_path / "data" / "signal_log.csv")
    out_csv = tmp_path / "data" / "throughput_watch.csv"
    report = tmp_path / "reports" / "throughput_watch.md"
    trans = tmp_path / "results" / ".throughput_alert_new"
    args = [sys.executable, str(TOOL), "--ledger", str(ledger), "--out-csv", str(out_csv), "--report", str(report),
            "--interventions", str(tmp_path / "none.json"), "--transition-file", str(trans), "--fail-on-alert"]
    r1 = subprocess.run(args, cwd=tmp_path, capture_output=True, text=True)
    assert r1.returncode == 2, r1.stdout + r1.stderr
    assert trans.exists()  # 前回が無い → 新規 ALERT
    rows = list(csv.DictReader(out_csv.open(encoding="utf-8")))
    assert len(rows) == 1 and rows[0]["status"] == "ALERT"
    assert "売買頻度の監視 — ALERT" in report.read_text(encoding="utf-8")
    trans.unlink()
    r2 = subprocess.run(args, cwd=tmp_path, capture_output=True, text=True)
    assert r2.returncode == 2
    rows = list(csv.DictReader(out_csv.open(encoding="utf-8")))
    assert len(rows) == 1  # 同じ as_of は置き換え
    # 同じ日の再実行は「前の日の判定」が無いので、やはり新規 ALERT 扱い(前日行は同日行で置き換わる)
    assert trans.exists()
    # 前日に ALERT の行があれば遷移ではない
    trans.unlink()
    with out_csv.open("a", encoding="utf-8", newline="") as f:
        prev_day = (led_max := pd.to_datetime(rows[0]["as_of"])) - pd.Timedelta(days=1)
        f.write(",".join([prev_day.strftime("%Y-%m-%d"), "14", "56", "14", "0", "0", "56", "16", "16", "0", "0", "ALERT", "", str(led_max.date()), "x"]) + "\n")
    r3 = subprocess.run(args, cwd=tmp_path, capture_output=True, text=True)
    assert r3.returncode == 2 and not trans.exists(), r3.stdout


def test_cli_check_only_writes_nothing(tmp_path):
    ledger = write(make_ledger("2026-06-01", 70, steady("2026-06-01", 70)), tmp_path / "data" / "signal_log.csv")
    out_csv = tmp_path / "data" / "throughput_watch.csv"
    report = tmp_path / "reports" / "throughput_watch.md"
    r = subprocess.run([sys.executable, str(TOOL), "--ledger", str(ledger), "--out-csv", str(out_csv), "--report", str(report),
                        "--interventions", str(tmp_path / "none.json"), "--check-only"], cwd=tmp_path, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert not out_csv.exists() and not report.exists()
    assert "status=OK" in r.stdout


def test_cli_report_only_skips_csv(tmp_path):
    ledger = write(make_ledger("2026-06-01", 70, steady("2026-06-01", 70)), tmp_path / "data" / "signal_log.csv")
    out_csv = tmp_path / "data" / "throughput_watch.csv"
    report = tmp_path / "reports" / "throughput_watch.md"
    r = subprocess.run([sys.executable, str(TOOL), "--ledger", str(ledger), "--out-csv", str(out_csv), "--report", str(report),
                        "--interventions", str(tmp_path / "none.json"), "--report-only"], cwd=tmp_path, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert report.exists() and not out_csv.exists()


def test_intervention_table_before_after(tmp_path):
    days = 60
    orders = steady("2026-06-01", 30)  # 前半だけ注文がある
    led = tw.load_ledger(write(make_ledger("2026-06-01", days, orders), tmp_path / "l.csv"))
    inter = tmp_path / "interventions.json"
    inter.write_text('{"interventions":[{"date":"2026-07-01","label":"x"}]}', encoding="utf-8")
    t = tw.intervention_table(led, inter)
    assert len(t) == 1 and t.loc[0, "orders_before"] > 0 and t.loc[0, "orders_after"] == 0
    assert t.loc[0, "days_before"] == 14 and t.loc[0, "days_after"] == 14
