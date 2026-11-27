# -*- coding: utf-8 -*-
"""週末の読み: その週の擬似執行の結果を、確定ぶんと進行中の含みを分けて一度に読む。

ダッシュボードと週次レビューは決着した擬似取引だけを数えていたので、含み損を抱えた週が良く見えた
（2026-11-23 の週: 決着 +2.8R・進行中 34 件の含み −11.5R）。数え方は src/open_book.py に固定してある。

    python src/fetch_market.py                    # 価格(data/raw は git 管理外)を先に取る
    python tools/analysis/weekly_readout.py       # 直近4週
    python tools/analysis/weekly_readout.py --weeks 8 --context-assets DXY,US10Y

読み方
------
* 週 = 月曜〜日曜。進行中の週は、価格のある最新の日まで。
* 確定＋含み = その日までに決着した行の r_result の合計 ＋ その日に建玉だった行の含みR（定義は src/open_book.py）。
  含みR は確定した結果ではない。
* 文脈用の資産 = 取引しない資産（既定は DXY と US10Y。tools/analysis/intervention_review.py と同じ）。分けて数える。
* 行を全部足した数字。同じ見立てを毎日出し直した日数ぶん重なる（見立て単位の読みは intervention_review.py）。

観測だけ。採点・提案・配分に入る数は変えない。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import open_book as ob  # noqa: E402

DEFAULT_CONTEXT = ("DXY", "US10Y")
STATUS_JA = {"filled_sl": "SL", "filled_tp1": "TP1", "filled_time_exit": "時間決済"}


def _r(v) -> str:
    return "—" if v is None or v != v else f"{v:+.2f}R"


def week_table(d: pd.DataFrame, marks: pd.Series) -> pd.DataFrame:
    """判断した週ごとの注文の内訳。d は ob.prepare の結果、marks は行ごとの含みR（測れない行は欠損）。"""
    if d.empty:
        return pd.DataFrame()
    x = d.assign(mark=marks.reindex(d.index), day=pd.to_datetime(d["date"], errors="coerce"))
    x = x[x["day"].notna()]
    x["week"] = x["day"].dt.to_period("W-SUN")
    rows = []
    for wk, g in x.groupby("week"):
        done = g[g["status"].isin(ob.SETTLED)]
        held = g[(g["status"] == "open") & g["fill_price"].notna()]
        rows.append({
            "週(月曜)": wk.start_time.strftime("%m/%d"), "注文": len(g), "未約定(確定)": int((g["status"] == "no_fill").sum()),
            "決着": len(done), "SL": int((done["status"] == "filled_sl").sum()), "TP1": int((done["status"] == "filled_tp1").sum()),
            "時間決済": int((done["status"] == "filled_time_exit").sum()), "確定R": round(float(done["r"].sum()), 2),
            "進行中(約定済み)": len(held), "含みR": round(float(held["mark"].sum()), 2),
            "測れない": int(held["mark"].isna().sum()), "まだ約定していない": int(((g["status"] == "open") & g["fill_price"].isna()).sum()),
        })
    return pd.DataFrame(rows)


def readout(sim: pd.DataFrame, frames: dict, weeks: int, context: set) -> str:
    out = []
    book = ob.summary(sim, frames, weeks=weeks)
    if not book["available"]:
        return f"読めなかった: {book['reason']}（先に python src/fetch_market.py）"
    as_of = pd.Timestamp(book["as_of"])
    start = as_of.to_period("W-SUN").start_time.normalize() - pd.Timedelta(days=7 * weeks)
    out.append(f"# 週末の読み（{book['as_of']} までの値。週は月曜〜日曜。文脈用の資産: {', '.join(sorted(context)) or 'なし'}）")
    groups = [("全資産", sim)]
    if context:
        asset = sim["asset"].astype(str).str.strip().str.upper()
        groups += [("取引する資産", sim[~asset.isin(context)]), ("文脈用の資産", sim[asset.isin(context)])]

    out.append("\n## 1. 週ごとの「確定＋含み」の変化（擬似執行。行を全部足した数字）")
    for name, part in groups:
        wk = ob.weekly_changes(ob.equity_curve(part, frames, start, as_of)).tail(weeks)
        out.append(f"\n{name}")
        if wk.empty:
            out.append("  該当なし")
            continue
        for _, r in wk.iterrows():
            if r["incomplete"]:
                out.append(f"  {r['week_start']:%m/%d} の週（{pd.Timestamp(r['last_day']):%m/%d} まで）: 変化は出せない"
                           f"（測れない建玉が、前の週の終わりに {int(r['prev_unmeasured'])} 件・この週の終わりに {int(r['unmeasured'])} 件）"
                           f" / 確定ぶんの変化 {_r(r['realized_change_r'])}")
                continue
            out.append(f"  {r['week_start']:%m/%d} の週（{pd.Timestamp(r['last_day']):%m/%d} まで）: 変化 {_r(r['change_r'])}"
                       f"（うち確定 {_r(r['realized_change_r'])}） / 週の終わりの含み {_r(r['mark_r'])} / 確定＋含み（記録の最初からの通算） {_r(r['equity_r'])}")

    out.append("\n## 2. 判断した週ごとの注文")
    for name, part in groups[:2]:
        d = ob.prepare(part)
        pos = ob.positions(part, frames)
        marks = pd.Series(pos["mark_r"].values, index=pos["row"].values, dtype=float)
        t = week_table(d, marks).tail(weeks + 1)
        out.append(f"\n{name}")
        out.append(t.to_string(index=False) if not t.empty else "  該当なし")

    out.append(f"\n## 3. いまの建玉（約定済み・未決着。{book['as_of']} までの値）")
    out.append(f"全資産: {book['positions']} 件 / 含み {_r(book['mark_r'])} / 決着の合計 {_r(book['realized_r'])} / 確定＋含み {_r(book['equity_r'])}"
               f" / まだ約定していない {book['unfilled_open']} 件 / 測れない {book['unmeasured']} 件")
    for r in book["by_asset"]:
        tag = "（文脈用）" if r["asset"] in context else ""
        out.append(f"  {r['asset']}{tag}: {r['positions']} 件 / 含み {_r(r['mark_r'])} / 評価に使った足 {r['mark_date']}")

    d = ob.prepare(sim)
    wk_start = as_of.to_period("W-SUN").start_time.normalize()
    this_week = d[d["status"].isin(ob.SETTLED) & (d["exit_date"] >= wk_start) & (d["exit_date"] <= as_of)].sort_values(["exit_date", "asset"])
    out.append(f"\n## 4. 今週（{wk_start:%m/%d}〜）に決着した行: {len(this_week)} 件 / 合計 {_r(float(this_week['r'].sum()) if len(this_week) else 0.0)}")
    for _, r in this_week.iterrows():
        tag = "（文脈用）" if r["asset"] in context else ""
        out.append(f"  判断 {str(r['date'])[5:].replace('-', '/')} {r['asset']}{tag} {r['side']} → {r['exit_date']:%m/%d} {STATUS_JA.get(r['status'], r['status'])} {_r(r['r'])}")

    out.append("\n## 5. 日ごと（直近14日。全資産）")
    c = ob.equity_curve(sim, frames, as_of - pd.Timedelta(days=13), as_of)
    c = c.assign(day=c["day"].dt.strftime("%m/%d(%a)")).rename(columns={
        "day": "日", "realized_r": "確定R累計", "positions": "建玉", "mark_r": "含みR", "equity_r": "確定＋含み", "unmeasured": "測れない"})
    out.append(c.round(2).to_string(index=False))
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--weeks", type=int, default=4, help="さかのぼる週の数（既定 4）")
    ap.add_argument("--context-assets", default=",".join(DEFAULT_CONTEXT), help="取引しない資産（カンマ区切り。空なら分けない）")
    ap.add_argument("--sim", default="data/execution_simulation.csv", help="執行シミュレーションの表")
    ap.add_argument("--raw-dir", default="data/raw", help="日足の置き場")
    args = ap.parse_args(argv)
    if args.weeks < 1:
        ap.error("--weeks は 1 以上")
    sim_path = Path(args.sim)
    if not sim_path.exists():
        print(f"読めなかった: {sim_path} が無い")
        return 1
    sim = pd.read_csv(sim_path)
    context = {a.strip().upper() for a in args.context_assets.split(",") if a.strip()}
    frames = ob.load_frames(sim["asset"].unique(), Path(args.raw_dir)) if "asset" in sim.columns else {}
    text = readout(sim, frames, args.weeks, context)
    print(text)
    return 1 if text.startswith("読めなかった") else 0


if __name__ == "__main__":
    raise SystemExit(main())
