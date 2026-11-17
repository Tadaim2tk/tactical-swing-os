# -*- coding: utf-8 -*-
"""介入（プロンプトの貼り替え）の後の期間を、決めた項目で一度に読む。

changelog (20) は「貼った日の14日後に、頻度・SL幅・成績を見る」と決めた。月次較正を待つと評価が宙に浮く
（2026-10 は月次が行われず、(13)〜(17) の評価が残らなかった）。次の介入でも同じ読み方ができるよう、
数え方をここに固定する。

    python src/fetch_market.py                                   # 価格(data/raw は git 管理外)を先に取る
    python tools/analysis/intervention_review.py --start 2026-11-04 --end 2026-11-17

数え方（言葉と計算を一致させるための定義）
------------------------------------------
* 注文 = 台帳の rank A/B で向きのある行。1資産1日1行。
* 決着 = 執行シミュレーション(data/execution_simulation.csv)の status が filled_sl / filled_tp1 /
  filled_time_exit の行。R は同じ表の r_result。open は5営業日の窓がまだ閉じていない行。
* 見立て = 同じ資産・同じ向きの注文が3日以内に続く並び（src/throughput_metrics.py の mark_runs と同じ）。
  見立ての成績は「並びの最初の日の注文」で数える。行を全部足した合計は、同じ見立てを毎日出し直した
  日数ぶん重なるので、別に出す。
* 文脈用の資産 = 取引しない資産（既定は DXY と US10Y）。分けて数える。
* 向きの入れ替わり = 資産ごとに、期間の中の向きのある判断を日付順に並べて BUY⇔SELL が変わった回数。
  見送りの日は飛ばす。期間より前の判断とは比べない（何週間も前の見立てとの違いは「入れ替わり」ではない）。
* 連動を差し引いた賭けの本数 = n² ÷ Σρ。ρ は、その日の注文どうしの、向きをそろえた日次終値リターンの
  相関（判断日より前の60営業日。全資産に値がある日だけ）。互いに打ち消す組が多い日は式の値が行数 n を
  超えるので、n で頭打ちにする。全部が同じ動きなら 1、無関係なら n。
  1日あたりの平均は、**期間の中の台帳の日すべて**で割る。注文が無い日は 0 行・0 本として数える
  （注文のある日だけで割ると、14日のうち2日しか注文が無い期間が「1日 1.0 行」に見える。#219 Codex P2）。
* SL の後で戻ったか = SL になった注文のうち、判断後5本目の終値が予測方向の側にあった件数
  （tools/analysis/sl_width_vs_atr.py の close5_R > 0）。5本目がまだ無い注文は分母に入れない。

観測だけ。提案・配分・採用に入る数は変えない。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import throughput_metrics as tm  # noqa: E402

SETTLED = ("filled_sl", "filled_tp1", "filled_time_exit")
DEFAULT_CONTEXT = ("DXY", "US10Y")
ASSETS = ["GOLD", "BTC", "ETH", "WTI", "USDJPY", "SPX", "NASDAQ", "DXY", "US10Y", "VIX"]
LOOKBACK = 60


def attach_runs(orders: pd.DataFrame) -> pd.DataFrame:
    """mark_runs の結果に、見立ての通し番号 run_id（資産×向きごと）を付ける。"""
    out = orders.sort_values(["asset", "side_n", "date"]).copy()
    out["run_id"] = out.groupby(["asset", "side_n"])["run_start"].cumsum().astype(int)
    return out


def row_summary(rows: pd.DataFrame) -> dict:
    """行（注文）単位の集計。rows は status と r_result を持つ。"""
    done = rows[rows["status"].isin(SETTLED)]
    r = pd.to_numeric(done["r_result"], errors="coerce")
    return {
        "orders": int(len(rows)),
        "settled": int(len(done)),
        "sl": int((done["status"] == "filled_sl").sum()),
        "tp1": int((done["status"] == "filled_tp1").sum()),
        "time_exit": int((done["status"] == "filled_time_exit").sum()),
        "no_fill": int((rows["status"] == "no_fill").sum()),
        "open": int((rows["status"] == "open").sum()),
        "total_r": round(float(r.sum()), 2) if len(done) else 0.0,
        "mean_r": round(float(r.mean()), 3) if len(done) else None,
        "wins": int((r > 0).sum()),
    }


def idea_table(orders: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    """期間の中で始まった見立てを1行ずつ。orders は run_id・status・r_result を持つ注文行。

    並びが期間より前から続いているものは「期間の中で始まった」に入れない。期間より後の行は足さない。"""
    out = []
    for (asset, side, _), x in orders.groupby(["asset", "side_n", "run_id"]):
        x = x.sort_values("date")
        first = x.iloc[0]
        if not (start <= first["date"] <= end):
            continue
        inside = x[x["date"] <= end]
        done = inside[inside["status"].isin(SETTLED)]
        first_done = first["status"] in SETTLED
        out.append({
            "asset": asset, "side": side, "start": first["date"], "last": inside["date"].max(),
            "rows": int(len(inside)), "first_status": first["status"],
            "first_r": float(first["r_result"]) if first_done else np.nan,
            "settled_rows": int(len(done)),
            "sum_r": round(float(pd.to_numeric(done["r_result"], errors="coerce").sum()), 2),
        })
    cols = ["asset", "side", "start", "last", "rows", "first_status", "first_r", "settled_rows", "sum_r"]
    return pd.DataFrame(out, columns=cols).sort_values(["start", "asset"]).reset_index(drop=True)


def idea_summary(ideas: pd.DataFrame) -> dict:
    done = ideas.dropna(subset=["first_r"])
    return {
        "ideas": int(len(ideas)),
        "first_settled": int(len(done)),
        "first_no_fill": int((ideas["first_status"] == "no_fill").sum()),
        "first_open": int((ideas["first_status"] == "open").sum()),
        "wins": int((done["first_r"] > 0).sum()),
        "losses": int((done["first_r"] <= 0).sum()),
        "total_r": round(float(done["first_r"].sum()), 2),
        "mean_r": round(float(done["first_r"].mean()), 3) if len(done) else None,
        "all_rows_r": round(float(ideas["sum_r"].sum()), 2),
    }


def count_flips(ledger: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> dict:
    """資産ごとの向きの入れ替わり回数。ledger は tm.load_ledger() の形（date, asset, side_n）。"""
    out = {}
    directional = ledger[ledger["side_n"].isin(["BUY", "SELL"]) & (ledger["date"] >= start) & (ledger["date"] <= end)]
    for asset, x in directional.sort_values("date").groupby("asset"):
        sides = list(x["side_n"])
        out[asset] = sum(1 for a, b in zip(sides, sides[1:]) if a != b)
    return out


def effective_bets(sides: dict, returns: pd.DataFrame) -> float:
    """その日の注文（資産→BUY/SELL）が、連動を差し引いて何本ぶんか。returns は日次リターンの表。"""
    assets = [a for a in sides if a in returns.columns]
    n = len(assets)
    if n == 0:
        return float("nan")
    if n == 1:
        return 1.0
    sign = np.array([1.0 if sides[a] == "BUY" else -1.0 for a in assets])
    corr = returns[assets].corr().values * np.outer(sign, sign)
    total = float(np.nansum(corr))
    if total <= 0:
        return float(n)                  # 打ち消し合いが勝っている。行数で頭打ち
    return float(min(n, n * n / total))


def load_returns(raw_dir: Path = Path("data/raw")) -> pd.DataFrame:
    closes = {}
    for asset in ASSETS:
        path = raw_dir / f"{asset}.csv"
        if not path.exists():
            continue
        df = pd.read_csv(path)
        df.columns = [c.lower() for c in df.columns]
        closes[asset] = pd.Series(pd.to_numeric(df["close"], errors="coerce").values, index=pd.to_datetime(df["date"]))
    return pd.DataFrame(closes).dropna().pct_change().dropna()


def daily_bets(orders: pd.DataFrame, returns: pd.DataFrame, context: set, lookback: int = LOOKBACK,
               days=None) -> pd.DataFrame:
    """日ごとの注文の行数と、連動を差し引いた本数。days は期間の中の台帳の日（注文が無い日も含む）。

    days を渡すと、注文が無い日は 0 行・0 本の行として入る。渡さなければ注文のある日だけ（従来の形）。
    注文はあるが取引する資産が1つも無い日は、取引する資産の側を 0 行・0 本にする。"""
    cols = ["date", "orders", "bets", "orders_tradable", "bets_tradable"]
    by_day = {day: x for day, x in orders.groupby("date")}
    all_days = sorted(set(by_day) | {pd.Timestamp(d) for d in (days if days is not None else [])})
    out = []
    for day in all_days:
        x = by_day.get(day)
        if x is None:
            out.append({"date": day, "orders": 0, "bets": 0.0, "orders_tradable": 0, "bets_tradable": 0.0})
            continue
        hist = returns[returns.index < day].tail(lookback)
        sides = dict(zip(x["asset"], x["side_n"]))
        tradable = {a: s for a, s in sides.items() if a not in context}
        out.append({"date": day, "orders": len(sides), "bets": effective_bets(sides, hist),
                    "orders_tradable": len(tradable),
                    "bets_tradable": effective_bets(tradable, hist) if tradable else 0.0})
    return pd.DataFrame(out, columns=cols)


def sl_readout(start: pd.Timestamp, end: pd.Timestamp, ledger_raw: pd.DataFrame, sim: pd.DataFrame) -> dict:
    import sl_width_vs_atr as sw
    built = sw.build(ledger_raw, sim)
    if built.empty:
        return {}
    built["date"] = pd.to_datetime(built["date"])
    x = built[(built["date"] >= start) & (built["date"] <= end)]
    sl = x[x["status"] == "filled_sl"]
    judged = sl.dropna(subset=["close5_R"])
    return {
        "orders": int(len(x)),
        "risk_atr_median": round(float(x["risk_atr"].median()), 2) if len(x) else None,
        "risk_atr_min": round(float(x["risk_atr"].min()), 2) if len(x) else None,
        "below_1atr": int((x["risk_atr"] < 1.0).sum()),
        "sl": int(len(sl)),
        "sl_judged": int(len(judged)),
        "sl_came_back": int((judged["close5_R"] > 0).sum()),
    }


def _fmt_rows(name: str, s: dict) -> str:
    if not s["settled"]:
        return f"{name}: 注文 {s['orders']} / 決着 0（未約定 {s['no_fill']}・未決着 {s['open']}）"
    return (f"{name}: 注文 {s['orders']} / 決着 {s['settled']}（SL {s['sl']}・TP1 {s['tp1']}・時間決済 {s['time_exit']}）"
            f" / 未約定 {s['no_fill']} / 未決着 {s['open']} | 合計 {s['total_r']:+.2f}R 平均 {s['mean_r']:+.3f}R"
            f" 勝ち {s['wins']} 行（{s['wins'] / s['settled'] * 100:.0f}%）")


def _fmt_ideas(name: str, s: dict) -> str:
    if not s["first_settled"]:
        return f"{name}: 見立て {s['ideas']} 本 / 初日の注文が決着したもの 0"
    return (f"{name}: 見立て {s['ideas']} 本 / 初日の注文が決着 {s['first_settled']} 本（未約定 {s['first_no_fill']}・未決着 {s['first_open']}）"
            f" | {s['wins']} 勝 {s['losses']} 敗 合計 {s['total_r']:+.2f}R 平均 {s['mean_r']:+.3f}R | 行を全部足すと {s['all_rows_r']:+.2f}R")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--start", required=True, help="介入境界（最初に効いた定時実行の日）YYYY-MM-DD")
    ap.add_argument("--end", required=True, help="読む期間の最後の日 YYYY-MM-DD")
    ap.add_argument("--context-assets", default=",".join(DEFAULT_CONTEXT), help="取引しない資産（カンマ区切り）")
    args = ap.parse_args(argv)
    start, end = pd.Timestamp(args.start), pd.Timestamp(args.end)
    context = {a.strip().upper() for a in args.context_assets.split(",") if a.strip()}

    ledger = tm.load_ledger()
    sim = pd.read_csv("data/execution_simulation.csv")
    sim["date"] = pd.to_datetime(sim["date"])
    sim["asset"] = sim["asset"].astype(str).str.upper()
    orders = attach_runs(tm.mark_runs(ledger)).merge(sim[["date", "asset", "status", "r_result"]], on=["date", "asset"], how="left")
    orders["status"] = orders["status"].fillna("")
    inside = orders[(orders["date"] >= start) & (orders["date"] <= end)]
    days = int(ledger[(ledger["date"] >= start) & (ledger["date"] <= end)]["date"].nunique())

    print(f"# 介入後の読み {args.start}〜{args.end}（台帳 {days} 日ぶん。文脈用の資産: {', '.join(sorted(context)) or 'なし'}）\n")
    print("## 1. 行（注文）単位")
    print(_fmt_rows("全資産", row_summary(inside)))
    print(_fmt_rows("取引する資産", row_summary(inside[~inside["asset"].isin(context)])))
    print(_fmt_rows("文脈用の資産", row_summary(inside[inside["asset"].isin(context)])))
    for asset, x in inside.groupby("asset"):
        print("  " + _fmt_rows(asset, row_summary(x)))

    print("\n## 2. 見立て単位（期間の中で始まったもの）")
    ideas = idea_table(orders, start, end)
    print(_fmt_ideas("全資産", idea_summary(ideas)))
    print(_fmt_ideas("取引する資産", idea_summary(ideas[~ideas["asset"].isin(context)])))
    if len(ideas):
        show = ideas.copy()
        show["start"] = show["start"].dt.strftime("%m/%d")
        show["last"] = show["last"].dt.strftime("%m/%d")
        print(show.to_string(index=False, float_format=lambda v: "%+.2f" % v))

    print("\n## 3. SL幅と、SL の後で戻ったか")
    ledger_raw = pd.read_csv("data/signal_log.csv")
    s = sl_readout(start, end, ledger_raw, pd.read_csv("data/execution_simulation.csv"))
    if s:
        print(f"SL幅÷ATR10: 中央値 {s['risk_atr_median']} 最小 {s['risk_atr_min']} / 1.0 未満 {s['below_1atr']} 行（対象 {s['orders']} 行）")
        print(f"SL {s['sl']} 件のうち、5本目が出そろった {s['sl_judged']} 件 → 予測方向の側に戻っていた {s['sl_came_back']} 件")

    print("\n## 4. 向きの入れ替わり")
    flips = count_flips(ledger, start, end)
    print("合計 %d 回: " % sum(flips.values()) + "、".join(f"{a} {n}" for a, n in sorted(flips.items(), key=lambda kv: -kv[1]) if n))

    print("\n## 5. 1日の注文は、連動を差し引いて何本ぶんか")
    returns = load_returns()
    if returns.empty:
        print("価格が無い（先に python src/fetch_market.py）")
    else:
        ledger_days = sorted(ledger[(ledger["date"] >= start) & (ledger["date"] <= end)]["date"].unique())
        bets = daily_bets(inside, returns, context, days=ledger_days)
        if bets.empty:
            print("期間の中に台帳の日が無い")
        else:
            print("1日あたり平均（台帳 %d 日で割る。注文の無い日 %d 日を含む）: 注文 %.1f 行 → %.1f 本ぶん（取引する資産だけ: %.1f 行 → %.1f 本ぶん）" % (
                len(bets), int((bets["orders"] == 0).sum()),
                bets["orders"].mean(), bets["bets"].mean(), bets["orders_tradable"].mean(), bets["bets_tradable"].mean()))
            show = bets.copy()
            show["date"] = show["date"].dt.strftime("%m/%d")
            print(show.to_string(index=False, float_format=lambda v: "%.1f" % v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
