#!/usr/bin/env python3
"""月次較正の実測パート（毎月同じ物差しで出す。2026-10 の手書き版 monthly_calib_2026_10.py を一般化）。

    python tools/analysis/monthly_calib.py --month 2026-10                     # 標準出力
    python tools/analysis/monthly_calib.py --month 2026-10 --write docs/x.md   # 草稿を書く

出すもの（節番号は 2026-10 の文書と同じ並び）:
  0 売買頻度（月別の注文・見立て、ALERT 区間）
  1 SL: 月別の SL率と合計R、申告SL幅÷ATR10 の月別中央値、併走 atr_floor の差
  2 regime 6語の遵守率と月別分布
  3 主役の申告 vs 機械判定 LEADER_V1、申告主役への判断の成績
  4 週次 crypto 予測の検算（期日終値、予測時の価格は実行前に閉じた土曜終値）
  5 invalidation fired の時系列（手遅れ / 降りられた / 未約定）
  6 併走観測 chase / half_exit / forgone（2026-09-09 以降）
  7 win_prob の較正（月別）
  8 対象月の介入の前後14日
数値の採否・ルール変更は書かない。それは人間の仕事（文書末尾の「決定待ち」）。
価格系列(data/raw)が無い環境では ATR を使う節を「計算できず」と書いて続行する。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[2] / "src"))
import throughput_metrics as tm  # noqa: E402

ASSETS = ["GOLD", "BTC", "ETH", "WTI", "USDJPY", "SPX", "NASDAQ", "DXY", "US10Y", "VIX"]
FINAL = {"filled_sl", "filled_tp1", "filled_time_exit"}
VOC = {"RISK_ON", "RISK_OFF", "NEUTRAL", "MIXED", "EVENT", "UNKNOWN"}
TRACK_START = pd.Timestamp("2026-09-09")


def _read(root: Path, rel: str, parse_dates=None) -> pd.DataFrame:
    p = root / rel
    if not p.exists() or p.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(p, parse_dates=parse_dates)
    except Exception:
        return pd.DataFrame()


def _num(df: pd.DataFrame, cols) -> pd.DataFrame:
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def _md(df: pd.DataFrame, empty: str = "_該当なし_") -> str:
    if df is None or len(df) == 0:
        return empty
    df = df.copy()
    if isinstance(df.index, pd.MultiIndex) or df.index.name is not None or not isinstance(df.index, pd.RangeIndex):
        df = df.reset_index()
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        cells = []
        for v in r.tolist():
            if isinstance(v, float):
                cells.append("" if np.isnan(v) else f"{v:.3g}" if abs(v) < 1 and v != 0 else f"{v:.2f}".rstrip("0").rstrip("."))
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


class Prices:
    def __init__(self, root: Path):
        self.root = root
        self.cache: dict[str, pd.DataFrame | None] = {}

    def get(self, asset: str) -> pd.DataFrame | None:
        if asset in self.cache:
            return self.cache[asset]
        p = self.root / "data" / "raw" / f"{asset}.csv"
        if not p.exists():
            self.cache[asset] = None
            return None
        df = pd.read_csv(p)
        df.columns = [c.lower() for c in df.columns]
        dc = [c for c in df.columns if "date" in c or "time" in c]
        if not dc or not {"open", "high", "low", "close"}.issubset(df.columns):
            self.cache[asset] = None
            return None
        df["date"] = pd.to_datetime(df[dc[0]], errors="coerce").dt.tz_localize(None).dt.normalize()
        df = df.dropna(subset=["date"]).sort_values("date").drop_duplicates("date")
        if asset not in ("BTC", "ETH"):
            df = df[df["date"].dt.weekday < 5]
        self.cache[asset] = df.set_index("date")[["open", "high", "low", "close"]]
        return self.cache[asset]

    def atr10_before(self, asset: str, day: pd.Timestamp) -> float:
        p = self.get(asset)
        if p is None:
            return np.nan
        d = p[p.index < day]
        if len(d) < 11:
            return np.nan
        h, l, c = d["high"], d["low"], d["close"]
        pc = c.shift(1)
        tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
        return float(tr.tail(10).mean())


def build(root: Path, month: str) -> tuple[str, dict]:
    """対象月 (YYYY-MM) の草稿 markdown と、節ごとの数値 dict を返す。"""
    target = pd.Period(month, freq="M")
    led = _read(root, "data/signal_log.csv")
    sim = _read(root, "data/execution_simulation.csv")
    sc = _read(root, "data/prediction_log_scores.csv")
    R: dict = {"month": month}
    out: list[str] = [f"# 月次較正 {month}（草稿・機械生成 {date.today().isoformat()}）", "",
                      "数値は `tools/analysis/monthly_calib.py` が台帳・サイドカー・執行シミュレーション・遡及コーパスから出したもの。",
                      "**採否と結論は人間が書く**（末尾「決定待ち」）。節の並びは docs/monthly_calibration_2026-10.md と同じ。", ""]

    def section(title: str, fn):
        out.append(f"## {title}")
        out.append("")
        try:
            fn()
        except Exception as e:  # 節ごとに隔離。草稿は必ず出す
            out.append(f"_計算できず: {type(e).__name__}: {e}_")
            R.setdefault("errors", []).append(f"{title}: {e}")
        out.append("")

    if led.empty:
        out.append("_台帳 data/signal_log.csv が空。何も計算できない。_")
        return "\n".join(out), R
    led["date"] = pd.to_datetime(led["date"], errors="coerce")
    led = led.dropna(subset=["date"])
    _num(led, ["entry_low", "entry_high", "sl", "tp1", "rr", "win_prob", "expected_r", "risk_pct"])
    led["side_n"] = led["side"].astype(str).replace({"LONG": "BUY", "SHORT": "SELL"})
    led["order"] = led["rank"].isin(["A", "B"]) & led["side_n"].isin(["BUY", "SELL"])
    led["month"] = led["date"].dt.to_period("M")
    if not sim.empty:
        sim["date"] = pd.to_datetime(sim["date"], errors="coerce")
        sim["month"] = sim["date"].dt.to_period("M")
    if not sc.empty:
        sc["date"] = pd.to_datetime(sc["date"], errors="coerce")
    prices = Prices(root)

    # ---------------------------------------------------------------- 0
    def s0():
        lg = tm.ledger_frame(led.astype(str))
        orders = tm.mark_runs(lg)
        lg["month"] = lg["date"].dt.to_period("M")
        orders["month"] = orders["date"].dt.to_period("M")
        t = pd.DataFrame({"ledger_days": lg.groupby("month")["date"].nunique(),
                          "orders": orders.groupby("month").size(),
                          "ideas": orders[orders["run_start"]].groupby("month").size()}).fillna(0).astype(int)
        t["ideas_per_week"] = (t["ideas"] / t["ledger_days"].replace(0, np.nan) * 7).round(2)
        t.index = t.index.astype(str)
        t.index.name = "month"
        out.append(_md(t))
        eps = tm.alert_episodes(tm.history(lg))
        out.append("")
        out.append("ALERT 区間: " + ("、".join(f"{a}〜{b}" for a, b in eps) if eps else "なし"))
        R["throughput"] = t.reset_index().astype(str).to_dict("records")
        R["alert_episodes"] = eps
    section("0. 売買頻度（注文 = rank A/B 行、見立て = 資産×方向の並びの始まり）", s0)

    # ---------------------------------------------------------------- 1
    def s1():
        if sim.empty:
            out.append("_執行シミュレーションが無い（SL率・併走は出せない）_")
        else:
            f = sim[sim["status"].isin(FINAL)]
            t = f.groupby("month").agg(n=("r_result", "size"), sl=("status", lambda s: (s == "filled_sl").sum()),
                                       tp1=("status", lambda s: (s == "filled_tp1").sum()),
                                       time=("status", lambda s: (s == "filled_time_exit").sum()),
                                       r_sum=("r_result", "sum"))
            t["sl_rate"] = (t["sl"] / t["n"]).round(2)
            t["no_fill"] = sim[sim["status"] == "no_fill"].groupby("month").size()
            t = t.fillna(0)
            t.index = t.index.astype(str)
            out.append("月別（確定行のみ）:")
            out.append("")
            out.append(_md(t.round(2)))
            R["sl_by_month"] = t.round(3).reset_index().astype(str).to_dict("records")
        b = led[led["order"] & (led["risk_pct"] > 0)].copy()
        b["mid"] = (b["entry_low"] + b["entry_high"]) / 2
        b["sl_w"] = (b["mid"] - b["sl"]).abs()
        b["atr10"] = [prices.atr10_before(a, d) for a, d in zip(b["asset"], b["date"])]
        b["sl_atr"] = b["sl_w"] / b["atr10"]
        if b["atr10"].notna().any():
            t2 = b.groupby("month").agg(n=("sl_atr", "size"), sl_atr_med=("sl_atr", "median"),
                                        below_1atr=("sl_atr", lambda s: int((s < 1.0).sum()))).round(2)
            t2.index = t2.index.astype(str)
            out.append("")
            out.append("申告SL幅÷ATR10（判断日の前日までの10本）の月別中央値と、1.0 未満の件数:")
            out.append("")
            out.append(_md(t2))
            R["sl_atr_by_month"] = t2.reset_index().astype(str).to_dict("records")
        else:
            out.append("")
            out.append("_価格系列(data/raw)が無いので SL幅÷ATR10 は計算できず_")
        if not sim.empty and "atr_floor_r" in sim.columns:
            a = sim[sim["atr_floor_r"].notna()]
            tgt = a[a["month"] == target]
            out.append("")
            out.append(f"併走 atr_floor（SL幅 = max(申告, 1×ATR10)）: 全期間 n={len(a)} atr_floor={a['atr_floor_r'].sum():.2f}R / 既定={a['r_result'].sum():.2f}R / 差={a['atr_floor_r'].sum() - a['r_result'].sum():+.2f}R"
                       f"；対象月 n={len(tgt)} 差={tgt['atr_floor_r'].sum() - tgt['r_result'].sum():+.2f}R")
            if "atr_floor_widened" in sim.columns:
                w = sim[(sim["month"] == target) & sim["atr_floor_widened"].notna()]
                if len(w):
                    out.append(f"対象月に SL を広げる必要があった行（atr_floor_widened=True）: {int(w['atr_floor_widened'].astype(str).eq('True').sum())}/{len(w)}")
    section("1. SL — SL率・実損・申告SL幅÷ATR10・併走 atr_floor", s1)

    # ---------------------------------------------------------------- 2
    def s2():
        r = led[led["date"] >= "2026-09-01"]
        comp = float(r["regime"].isin(VOC).mean()) if len(r) else float("nan")
        out.append(f"6語の遵守率（2026-09-01 以降、n={len(r)}）: {comp:.3f}")
        ct = pd.crosstab(r["month"].astype(str), r["regime"], normalize="index").round(2)
        out.append("")
        out.append(_md(ct))
        R["regime_compliance"] = comp
    section("2. regime 6語の遵守率と月別分布", s2)

    # ---------------------------------------------------------------- 3
    def s3():
        lo = _read(root, "data/leader_observations.csv")
        mk = _read(root, "data/retro/market_daily.csv", parse_dates=["date"])
        if lo.empty:
            out.append("_主役の申告が無い_")
            return
        lo["date"] = pd.to_datetime(lo["date"])
        if not mk.empty and "leader_asset" in mk.columns:
            ctx = mk[["date", "leader_asset"]].sort_values("date")
            j = pd.merge_asof(lo.sort_values("date"), ctx, on="date", direction="backward", allow_exact_matches=False)
            m1 = float((j["leader_claimed"] == j["leader_asset"]).mean())
            out.append(f"申告 n={len(lo)}、機械判定 LEADER_V1 との一致率（as-of D−1）: {m1:.3f}。コーパス最終日 {mk['date'].max().date()}"
                       + ("（**対象月の末まで延長されていない。`tools/retro_build_market.py --extend` を回すこと**）" if mk["date"].max() < target.end_time.normalize() - pd.Timedelta(days=3) else ""))
            out.append("")
            out.append(_md(pd.crosstab(j["leader_claimed"], j["leader_asset"])))
            R["leader_match_asof"] = m1
        else:
            out.append("_遡及コーパス data/retro/market_daily.csv が無い_")
        if not sc.empty:
            act = sc[(sc["actionable"] == True) & sc["result_5d"].isin(["success", "failure"])].copy()  # noqa: E712
            act = act.merge(lo[["date", "leader_claimed"]], on="date", how="left")
            sub = act[act["leader_claimed"].notna()].copy()
            if len(sub):
                sub["on_claimed_leader"] = sub["asset"] == sub["leader_claimed"]
                g = sub.groupby("on_claimed_leader").agg(n=("signal_id", "size"), win=("result_5d", lambda s: (s == "success").mean()), r5=("r_close_5d", "mean")).round(3)
                out.append("")
                out.append("申告主役と同じ資産への判断（5日決着、累積）:")
                out.append("")
                out.append(_md(g))
                R["on_claimed_leader"] = g.reset_index().astype(str).to_dict("records")
    section("3. 主役の申告 vs 機械判定、申告主役への判断の成績", s3)

    # ---------------------------------------------------------------- 4
    def s4():
        cp = _read(root, "data/crypto_predictions_weekly.csv")
        cc = _read(root, "data/crypto_context_weekly.csv")
        if cp.empty:
            out.append("_週次 crypto 予測が記録されていない（日曜20:30 の出力を tools/record_crypto_context.py で記録する）_")
            return
        btc = prices.get("BTC")
        rows = []
        for _, p in cp.iterrows():
            ws = pd.Timestamp(p["week_start"])
            pred_day = ws + pd.Timedelta(days=6)
            deadline = pd.Timestamp(p["deadline"])
            level = float(p["level"])
            direction = str(p["direction"]).upper()
            at_pred = dl_close = np.nan
            hit = "価格なし"
            if btc is not None:
                ap = btc[btc.index < pred_day]["close"]
                at_pred = float(ap.iloc[-1]) if len(ap) else np.nan
                upto = btc[(btc.index > pred_day) & (btc.index <= deadline)]["close"]
                if len(upto) and deadline <= btc.index.max():
                    dl_close = float(upto.iloc[-1])
                    hit = ("HIT" if dl_close >= level else "MISS") if direction == "ABOVE" else ("HIT" if dl_close <= level else "MISS")
                else:
                    hit = "pending"
            nxt = cc[cc["week_start"] == (ws + pd.Timedelta(days=7)).strftime("%Y-%m-%d")] if not cc.empty else pd.DataFrame()
            rows.append({"week_start": p["week_start"], "pred": f"{p['asset']} {direction} {level:.0f} by {p['deadline']}",
                         "px_at_pred(土曜終値)": round(at_pred) if not np.isnan(at_pred) else "",
                         "level_vs_px_%": round((level / at_pred - 1) * 100, 1) if at_pred and not np.isnan(at_pred) else "",
                         "deadline_close": round(dl_close) if not np.isnan(dl_close) else "", "machine": hit,
                         "gpt_prev_result": str(nxt["prev_result"].iloc[0]) if len(nxt) else ""})
        t = pd.DataFrame(rows)
        out.append(_md(t))
        dec = t[t["machine"].isin(["HIT", "MISS"])]
        if len(dec):
            out.append("")
            out.append(f"決着 {len(dec)} 件: 機械 HIT {int((dec['machine'] == 'HIT').sum())} / GPT自己採点 HIT {int((dec['gpt_prev_result'] == 'HIT').sum())} / 一致 {int((dec['machine'] == dec['gpt_prev_result']).sum())}")
        R["crypto_pred"] = t.astype(str).to_dict("records")
    section("4. 週次 crypto 予測の検算（期日終値で判定。予測時の価格は実行前に閉じた土曜終値）", s4)

    # ---------------------------------------------------------------- 5
    def s5():
        ic = _read(root, "data/invalidation_checks.csv")
        if ic.empty:
            out.append("_invalidation_check が記録されていない_")
            return
        ic["check_date"] = pd.to_datetime(ic["check_date"])
        out.append(f"verdicts: {ic['invalidation_fired'].value_counts().to_dict()}")
        rows = []
        for _, fr in ic[ic["invalidation_fired"] == "fired"].iterrows():
            sid = fr["signal_id"]
            L = led[led["signal_id"] == sid]
            S = sim[sim["signal_id"] == sid] if not sim.empty else pd.DataFrame()
            if L.empty:
                rows.append({"signal_id": sid, "check": fr["check_date"].date(), "kind": "台帳に無い"})
                continue
            L = L.iloc[0]
            S = S.iloc[0] if len(S) else None
            p = prices.get(L["asset"])
            if p is None or S is None:
                rows.append({"signal_id": sid, "check": fr["check_date"].date(), "kind": "価格かsimが無い"})
                continue
            sign = 1 if L["side_n"] == "BUY" else -1
            before = p[p.index < fr["check_date"]]
            after = p[p.index >= fr["check_date"]]
            obs_bar = before.index[-1] if len(before) else pd.NaT
            exit_px = float(after["open"].iloc[0]) if len(after) else np.nan
            fill_date = pd.to_datetime(S["fill_date"]) if isinstance(S["fill_date"], str) and S["fill_date"] else pd.NaT
            exit_date = pd.to_datetime(S["exit_date"]) if isinstance(S["exit_date"], str) and S["exit_date"] else pd.NaT
            sim_r = float(S["r_result"]) if pd.notna(S["r_result"]) else np.nan
            if S["status"] == "no_fill" or pd.isna(fill_date) or (pd.notna(obs_bar) and fill_date > obs_bar):
                kind, r_on = "未約定(注文取消で済む)", 0.0
            elif pd.notna(exit_date) and pd.notna(obs_bar) and exit_date <= obs_bar:
                kind, r_on = f"手遅れ(既に {S['status']})", sim_r
            else:
                kind = "降りられた"
                r_on = sign * (exit_px - float(S["fill_price"])) / float(S["risk_unit"]) if not np.isnan(exit_px) else np.nan
            rows.append({"signal_id": sid, "check": fr["check_date"].date(), "sim_status": S["status"],
                         "sim_r": round(sim_r, 2) if not np.isnan(sim_r) else "", "kind": kind,
                         "r_if_exit_on_fired": round(r_on, 2) if not (isinstance(r_on, float) and np.isnan(r_on)) else ""})
        t = pd.DataFrame(rows)
        out.append("")
        out.append(_md(t))
        if len(t) and "kind" in t:
            kinds = t["kind"].str.split("(").str[0].value_counts().to_dict()
            out.append("")
            out.append(f"内訳: {kinds}")
            ok = t[t["kind"] == "降りられた"]
            if len(ok):
                out.append(f"降りられた {len(ok)} 件: 既定 {pd.to_numeric(ok['sim_r'], errors='coerce').sum():.2f}R vs 発動で降りる {pd.to_numeric(ok['r_if_exit_on_fired'], errors='coerce').sum():.2f}R")
            R["fired_kinds"] = kinds
    section("5. invalidation が fired になった判断 — 報告は決着の前か後か", s5)

    # ---------------------------------------------------------------- 6
    def s6():
        if sim.empty:
            out.append("_執行シミュレーションが無い_")
            return
        s9 = sim[sim["date"] >= TRACK_START]
        rows = []
        for c in ["chase_r", "half_exit_r", "half_exit_be_r", "atr_floor_r", "forgone_r"]:
            if c in s9.columns:
                sub = s9[s9[c].notna()]
                rows.append({"track": c, "n": len(sub), "track_sum": round(float(sub[c].sum()), 2), "baseline_same_rows": round(float(sub["r_result"].sum()), 2)})
        out.append(_md(pd.DataFrame(rows)))
        R["tracks"] = rows
    section("6. 併走観測（2026-09-09 以降の確定行。同じ行の既定 r_result と並べる）", s6)

    # ---------------------------------------------------------------- 7
    def s7():
        if sc.empty:
            out.append("_採点が無い_")
            return
        act = sc[(sc["actionable"] == True) & sc["result_5d"].isin(["success", "failure"])].merge(  # noqa: E712
            led[["signal_id", "win_prob"]], on="signal_id", how="left")
        if act.empty:
            out.append("_5日決着の判断が無い_")
            return
        act["month"] = act["date"].dt.to_period("M").astype(str)
        g = act.groupby("month").agg(n=("signal_id", "size"), wp=("win_prob", "mean"),
                                     realized=("result_5d", lambda s: (s == "success").mean()), r5=("r_close_5d", "mean"))
        g["err"] = g["realized"] - g["wp"]
        out.append(_md(g.round(3)))
        R["calibration"] = g.round(3).reset_index().astype(str).to_dict("records")
    section("7. win_prob の較正（actionable・5日決着、月別）", s7)

    # ---------------------------------------------------------------- 8
    def s8():
        path = root / "config" / "interventions.json"
        lg = tm.ledger_frame(led.astype(str))
        t = tm.intervention_table(lg, path)
        if len(t):
            t["date"] = pd.to_datetime(t["date"])
            # 対象月の14日前から対象月の末まで。上限を切らないと過去月の草稿に後の月の介入が混ざる(#206 Codex P2)
            lo, hi = target.start_time - pd.Timedelta(days=14), target.end_time.normalize()
            t = t[(t["date"] >= lo) & (t["date"] <= hi)]
            t["date"] = t["date"].dt.date
        out.append(_md(t, "_対象月に介入なし（config/interventions.json）_"))
    section("8. 対象月とその直前の介入の前後14日（注文・見立ての実数）", s8)

    out += ["## 決定待ち（人間が書く）", "", "- （数値の採否・プロンプト変更・観察継続の判断をここに。空のまま提出してよい）", "",
            f"*機械生成 {date.today().isoformat()}。再現: `python tools/analysis/monthly_calib.py --month {month}`*"]
    return "\n".join(out), R


def default_month() -> str:
    today = date.today()
    y, m = (today.year, today.month - 1) if today.month > 1 else (today.year - 1, 12)
    return f"{y:04d}-{m:02d}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--month", default=default_month(), help="対象月 YYYY-MM（既定: 先月）")
    ap.add_argument("--root", type=Path, default=HERE.parents[2])
    ap.add_argument("--write", type=Path, help="草稿 markdown の出力先")
    ap.add_argument("--json", type=Path)
    args = ap.parse_args(argv)
    md, R = build(args.root, args.month)
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(md + "\n", encoding="utf-8")
        print(f"wrote {args.write}")
    else:
        print(md)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(R, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
