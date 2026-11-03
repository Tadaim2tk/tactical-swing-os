"""売買頻度の監視の中身（tools/throughput_watch.py の CLI と dashboard が共有する）。

定義・判定規則・報告の描画はここに一つだけ置く。CLI は tools/throughput_watch.py、
Dashboard は dashboard_summaries.throughput_summary から呼ぶ。二か所に書くと定義がずれる
（label-vs-measure）。規則の説明は tools/throughput_watch.py の docstring。
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

LEDGER_PATH = Path("data/signal_log.csv")
OUT_CSV = Path("data/throughput_watch.csv")
REPORT_PATH = Path("reports/throughput_watch.md")
INTERVENTIONS_PATH = Path("config/interventions.json")

ORDER_RANKS = {"A", "B"}
SIDE_NORMALIZE = {"LONG": "BUY", "SHORT": "SELL", "BUY": "BUY", "SELL": "SELL"}
RUN_GAP_DAYS = 3  # 金→月 は 3 日。これ以内なら同じ見立ての再発行
CSV_COLUMNS = [
    "as_of", "window_days", "baseline_days", "ledger_days_window", "orders_window", "ideas_window",
    "ledger_days_baseline", "orders_baseline", "ideas_baseline", "orders_ratio", "ideas_ratio",
    "status", "note", "ledger_last_date", "recorded_at",
]
STATUS_ORDER = {"OK": 0, "WARN": 1, "ALERT": 2, "INSUFFICIENT_DATA": 1}


# --------------------------------------------------------------------------- 読み込み
def load_ledger(path: Path = LEDGER_PATH) -> pd.DataFrame:
    return ledger_frame(pd.read_csv(path, dtype=str, keep_default_na=False))


def ledger_frame(df: pd.DataFrame) -> pd.DataFrame:
    """既に読み込んだ台帳(文字列の DataFrame)を監視用の形にする。dashboard から使う。"""
    if df is None or df.empty or not {"date", "asset", "side", "rank"}.issubset(df.columns):
        return pd.DataFrame(columns=["date", "asset", "side_n", "rank", "is_order"])
    df = df.astype(str)
    out = pd.DataFrame({
        "date": pd.to_datetime(df["date"], errors="coerce").dt.normalize(),
        "asset": df["asset"].str.strip().str.upper(),
        "rank": df["rank"].str.strip().str.upper(),
    })
    out["side_n"] = df["side"].str.strip().str.upper().map(SIDE_NORMALIZE).fillna("NONE")
    out = out.dropna(subset=["date"])
    out["is_order"] = out["rank"].isin(ORDER_RANKS) & out["side_n"].isin({"BUY", "SELL"})
    return out.sort_values("date").reset_index(drop=True)


def mark_runs(ledger: pd.DataFrame) -> pd.DataFrame:
    """注文行に run_start（見立ての始まり）を立てる。"""
    orders = ledger[ledger["is_order"]].copy()
    if orders.empty:
        orders["run_start"] = pd.Series(dtype=bool)
        return orders
    orders = orders.sort_values(["asset", "side_n", "date"])
    gap = orders.groupby(["asset", "side_n"])["date"].diff().dt.days
    orders["run_start"] = gap.isna() | (gap > RUN_GAP_DAYS)
    return orders.sort_values("date")


# --------------------------------------------------------------------------- 集計
def window_stats(ledger: pd.DataFrame, orders: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> dict:
    in_l = ledger[(ledger["date"] >= start) & (ledger["date"] <= end)]
    in_o = orders[(orders["date"] >= start) & (orders["date"] <= end)]
    ideas = in_o[in_o["run_start"]]
    return {
        "start": start.date(), "end": end.date(),
        "ledger_days": int(in_l["date"].nunique()),
        "orders": int(len(in_o)),
        "ideas": int(len(ideas)),
        "ideas_by_asset": ideas.groupby("asset").size().to_dict(),
        "orders_by_asset": in_o.groupby("asset").size().to_dict(),
    }


def _ratio(num_rate: float, den_rate: float) -> float | None:
    if den_rate is None or den_rate <= 0:
        return None
    return round(num_rate / den_rate, 3)


def evaluate(ledger: pd.DataFrame, as_of: pd.Timestamp, window: int = 14, baseline: int = 56,
             alert_ideas: int = 3, warn_ideas: int = 4, orders: pd.DataFrame | None = None) -> dict:
    """as_of を含む直近 window 日を、その前 baseline 日と比べて判定する。"""
    if orders is None:
        orders = mark_runs(ledger)
    as_of = pd.Timestamp(as_of).normalize()
    w_start = as_of - pd.Timedelta(days=window - 1)
    b_end = w_start - pd.Timedelta(days=1)
    b_start = b_end - pd.Timedelta(days=baseline - 1)
    w = window_stats(ledger, orders, w_start, as_of)
    b = window_stats(ledger, orders, b_start, b_end)
    res = {
        "as_of": as_of.date(), "window_days": window, "baseline_days": baseline,
        "window": w, "baseline": b, "orders_ratio": None, "ideas_ratio": None, "notes": [],
    }
    if w["ledger_days"] < math.ceil(window / 2):
        res["status"] = "INSUFFICIENT_DATA"
        res["notes"].append(f"窓{window}日のうち台帳の日付が{w['ledger_days']}日しか無い（取込が止まっていないか）")
        return res
    w_orders_rate = w["orders"] / w["ledger_days"]
    w_ideas_rate = w["ideas"] / w["ledger_days"]
    if b["ledger_days"] < window:
        res["notes"].append("no_baseline")
        if w["ideas"] < alert_ideas:
            res["status"] = "ALERT"
        elif w["ideas"] < warn_ideas:
            res["status"] = "WARN"
        else:
            res["status"] = "OK"
        return res
    b_orders_rate = b["orders"] / b["ledger_days"]
    b_ideas_rate = b["ideas"] / b["ledger_days"]
    o_ratio = _ratio(w_orders_rate, b_orders_rate)
    i_ratio = _ratio(w_ideas_rate, b_ideas_rate)
    res["orders_ratio"], res["ideas_ratio"] = o_ratio, i_ratio
    o_half = o_ratio is not None and o_ratio <= 0.5
    i_half = i_ratio is not None and i_ratio <= 0.5
    if w["ideas"] < alert_ideas:
        res["status"] = "ALERT"
        res["notes"].append(f"見立てが{window}日で{w['ideas']}本（床 {alert_ideas} 本未満＝週1本以下）")
    elif o_half and i_half:
        res["status"] = "ALERT"
        res["notes"].append("注文も見立ても基準の半分以下")
    elif o_half or i_half or w["ideas"] < warn_ideas:
        res["status"] = "WARN"
        if o_half and (i_ratio is None or i_ratio > 0.75):
            res["notes"].append("注文は半分以下だが見立ては減っていない（同じ見立ての再発行が減っただけ＝記帳の仕方の変化）")
        elif i_half and not o_half:
            res["notes"].append("見立ては半分以下だが注文は減っていない（少ない見立てを毎日書き直している）")
        elif o_half or i_half:
            res["notes"].append("注文か見立てのどちらかが基準の半分以下")
        else:
            res["notes"].append(f"見立てが{window}日で{w['ideas']}本（{warn_ideas} 本未満）")
    else:
        res["status"] = "OK"
    return res


ESCALATE_AFTER_DAYS = 14  # WARN がこれだけ続いたら ALERT に上げる（9/16 の WARN を放置しないため）


def history(ledger: pd.DataFrame, window: int = 14, baseline: int = 56, alert_ideas: int = 3,
            warn_ideas: int = 4, step_days: int = 1, until: pd.Timestamp | None = None,
            escalate_after: int = ESCALATE_AFTER_DAYS) -> pd.DataFrame:
    """台帳の各日を as_of として判定を並べる（遡って「いつ気づけたか」を見る）。

    WARN が ``escalate_after`` 日以上続いた日は ALERT に上げる（note に ``escalated``）。
    """
    cols = ["as_of", "status", "orders_window", "ideas_window", "orders_ratio", "ideas_ratio", "note"]
    if ledger.empty:
        return pd.DataFrame(columns=cols)
    orders = mark_runs(ledger)
    first = ledger["date"].min() + pd.Timedelta(days=window + baseline - 1)
    last = ledger["date"].max() if until is None else min(pd.Timestamp(until).normalize(), ledger["date"].max())
    rows = []
    d = first
    streak = 0  # OK でない日の連続
    while d <= last:
        r = evaluate(ledger, d, window, baseline, alert_ideas, warn_ideas, orders=orders)
        status, notes = r["status"], list(r["notes"])
        streak = streak + 1 if status in ("WARN", "ALERT") else 0
        if status == "WARN" and escalate_after and streak >= escalate_after:
            status = "ALERT"
            notes.append(f"escalated: WARN が{streak}日続いた")
        rows.append({"as_of": r["as_of"], "status": status, "orders_window": r["window"]["orders"],
                     "ideas_window": r["window"]["ideas"], "orders_ratio": r["orders_ratio"], "ideas_ratio": r["ideas_ratio"],
                     "note": "; ".join(notes)})
        d += pd.Timedelta(days=step_days)
    return pd.DataFrame(rows, columns=cols)


def alert_episodes(hist: pd.DataFrame) -> list[tuple[str, str]]:
    """history の ALERT が続いた区間 [(start, end), ...]。"""
    out: list[tuple[str, str]] = []
    start = prev = None
    for _, r in hist.iterrows():
        if r["status"] == "ALERT":
            if start is None:
                start = r["as_of"]
            prev = r["as_of"]
        elif start is not None:
            out.append((str(start), str(prev)))
            start = prev = None
    if start is not None:
        out.append((str(start), str(prev)))
    return out


def intervention_table(ledger: pd.DataFrame, path: Path = INTERVENTIONS_PATH, span: int = 14) -> pd.DataFrame:
    """介入日の前後 span 日で、台帳日あたりの注文と見立てを並べる。"""
    cols = ["date", "label", "orders_before", "orders_after", "ideas_before", "ideas_after", "days_before", "days_after"]
    if not path.exists() or ledger.empty:
        return pd.DataFrame(columns=cols)
    items = json.loads(path.read_text(encoding="utf-8")).get("interventions", [])
    orders = mark_runs(ledger)
    last = ledger["date"].max()
    rows = []
    for it in items:
        d = pd.Timestamp(it["date"]).normalize()
        before = window_stats(ledger, orders, d - pd.Timedelta(days=span), d - pd.Timedelta(days=1))
        after = window_stats(ledger, orders, d, min(d + pd.Timedelta(days=span - 1), last))
        rows.append({"date": d.date(), "label": it.get("label", ""),
                     "orders_before": before["orders"], "orders_after": after["orders"],
                     "ideas_before": before["ideas"], "ideas_after": after["ideas"],
                     "days_before": before["ledger_days"], "days_after": after["ledger_days"]})
    return pd.DataFrame(rows, columns=cols)


def weekly_table(ledger: pd.DataFrame, weeks: int = 10) -> pd.DataFrame:
    orders = mark_runs(ledger)
    if ledger.empty:
        return pd.DataFrame(columns=["week", "ledger_days", "orders", "ideas"])
    l = ledger.assign(week=ledger["date"].dt.to_period("W-SUN"))
    o = orders.assign(week=orders["date"].dt.to_period("W-SUN"))
    t = pd.DataFrame({
        "ledger_days": l.groupby("week")["date"].nunique(),
        "orders": o.groupby("week").size(),
        "ideas": o[o["run_start"]].groupby("week").size(),
    }).fillna(0).astype(int)
    t.index = [f"{p.start_time.date()}" for p in t.index]
    t.index.name = "week"
    return t.tail(weeks).reset_index()


# --------------------------------------------------------------------------- 出力
def _md_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_該当なし_"
    cols = list(df.columns)
    lines = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join("" if (isinstance(v, float) and math.isnan(v)) else str(v) for v in r.tolist()) + " |")
    return "\n".join(lines)


def render_report(res: dict, ledger: pd.DataFrame, episodes: list[tuple[str, str]], interventions: pd.DataFrame,
                  weekly: pd.DataFrame) -> str:
    w, b = res["window"], res["baseline"]
    last_date = ledger["date"].max().date() if not ledger.empty else None
    lines = [
        f"# 売買頻度の監視 — {res['status']}",
        "",
        f"- 基準日(as_of): **{res['as_of']}**（台帳の最終日: {last_date}）",
        f"- 直近{res['window_days']}日 {w['start']}〜{w['end']}: 台帳日 {w['ledger_days']}、注文 **{w['orders']}** 行、見立て **{w['ideas']}** 本",
        f"- 基準{res['baseline_days']}日 {b['start']}〜{b['end']}: 台帳日 {b['ledger_days']}、注文 {b['orders']} 行、見立て {b['ideas']} 本",
        f"- 台帳日あたりの比（直近/基準）: 注文 {res['orders_ratio']}、見立て {res['ideas_ratio']}",
    ]
    if res["notes"]:
        lines.append("- 注記: " + "；".join(res["notes"]))
    if episodes:
        lines.append("- この規則で遡ったときの ALERT 区間: " + "、".join(f"**{a}〜{b}**" for a, b in episodes))
    else:
        lines.append("- この規則で遡っても ALERT になった日は無い")
    lines += ["", "## 判定の規則", "",
              "- 注文 = rank A/B の行。見立て = 資産×方向の並びの始まり（3日以内に同じ資産・方向が続けば再発行として1本に数える）。",
              "- ALERT: 見立てが窓で3本未満（14日で2本以下＝週1本以下）、または注文・見立てとも基準の半分以下、または WARN が14日続いた。WARN: どちらかが半分以下、または見立てが4本未満。",
              "- 観測だけ。提案・配分・採用に入る数は変えない。",
              "", "## 窓の中の資産別", "",
              "| 資産 | 見立て(直近) | 注文(直近) | 見立て(基準) | 注文(基準) |", "|---|---|---|---|---|"]
    assets = sorted(set(w["ideas_by_asset"]) | set(w["orders_by_asset"]) | set(b["ideas_by_asset"]) | set(b["orders_by_asset"]))
    for a in assets:
        lines.append(f"| {a} | {w['ideas_by_asset'].get(a, 0)} | {w['orders_by_asset'].get(a, 0)} | {b['ideas_by_asset'].get(a, 0)} | {b['orders_by_asset'].get(a, 0)} |")
    if not assets:
        lines.append("| (なし) | 0 | 0 | 0 | 0 |")
    lines += ["", "## 週ごと（直近）", "", _md_table(weekly),
              "", "## 介入の前後14日（台帳日あたりではなく実数）", "",
              "介入が頻度を変えたかを、月次較正を待たずに見るための表。after は介入日を含む。", "",
              _md_table(interventions), ""]
    return "\n".join(lines)


def append_csv(res: dict, ledger: pd.DataFrame, path: Path = OUT_CSV) -> None:
    """as_of ごとに1行。同じ as_of があれば置き換える。"""
    w, b = res["window"], res["baseline"]
    row = {
        "as_of": str(res["as_of"]), "window_days": res["window_days"], "baseline_days": res["baseline_days"],
        "ledger_days_window": w["ledger_days"], "orders_window": w["orders"], "ideas_window": w["ideas"],
        "ledger_days_baseline": b["ledger_days"], "orders_baseline": b["orders"], "ideas_baseline": b["ideas"],
        "orders_ratio": "" if res["orders_ratio"] is None else res["orders_ratio"],
        "ideas_ratio": "" if res["ideas_ratio"] is None else res["ideas_ratio"],
        "status": res["status"], "note": "; ".join(res["notes"]),
        "ledger_last_date": str(ledger["date"].max().date()) if not ledger.empty else "",
        "recorded_at": pd.Timestamp.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    rows = []
    if path.exists():
        with path.open(encoding="utf-8", newline="") as f:
            rows = [r for r in csv.DictReader(f) if r.get("as_of") != row["as_of"]]
    rows.append(row)
    rows.sort(key=lambda r: r["as_of"])
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        wri = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        wri.writeheader()
        for r in rows:
            wri.writerow({c: r.get(c, "") for c in CSV_COLUMNS})


def previous_status(path: Path, as_of: date) -> str | None:
    """CSV にある、as_of より前で最新の判定。"""
    if not path.exists():
        return None
    with path.open(encoding="utf-8", newline="") as f:
        prev = [r for r in csv.DictReader(f) if r.get("as_of") and r["as_of"] < str(as_of)]
    return prev[-1]["status"] if prev else None


