#!/usr/bin/env python3
"""月次較正 2026-10 の実測パート（2026-11-03 実行。10/1 に行われなかった月次の代替）。

changelog (13)〜(18) が「10月月次で測る」と予告した項目を、台帳・サイドカー・執行シミュレーション・
遡及コーパスから一度に出す。数値の採否は人間（docs/monthly_calibration_2026-10.md §決定）。

    python tools/analysis/monthly_calib_2026_10.py            # 標準出力に全節
    python tools/analysis/monthly_calib_2026_10.py --json results/monthly_calib_2026_10.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import throughput_watch as tw  # noqa: E402

pd.set_option("display.width", 220)
pd.set_option("display.max_rows", 400)
pd.set_option("display.max_columns", 60)

ASSETS = ["GOLD", "BTC", "ETH", "WTI", "USDJPY", "SPX", "NASDAQ", "DXY", "US10Y", "VIX"]
FINAL = {"filled_sl", "filled_tp1", "filled_time_exit"}
R: dict = {}


def say(title: str) -> None:
    print(f"\n## {title}\n")


def num(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def px(asset: str) -> pd.DataFrame:
    df = pd.read_csv(ROOT / "data" / "raw" / f"{asset}.csv")
    df.columns = [c.lower() for c in df.columns]
    dc = [c for c in df.columns if "date" in c or "time" in c][0]
    df["date"] = pd.to_datetime(df[dc]).dt.tz_localize(None).dt.normalize()
    df = df.sort_values("date").drop_duplicates("date")
    if asset not in ("BTC", "ETH"):
        df = df[df["date"].dt.weekday < 5]
    return df.set_index("date")[["open", "high", "low", "close"]]


def atr10_before(p: pd.DataFrame, day: pd.Timestamp) -> float:
    d = p[p.index < day]
    if len(d) < 11:
        return np.nan
    h, l, c = d["high"], d["low"], d["close"]
    pc = c.shift(1)
    tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    return float(tr.tail(10).mean())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()

    led = pd.read_csv(ROOT / "data/signal_log.csv")
    led["date"] = pd.to_datetime(led["date"])
    num(led, ["entry_low", "entry_high", "sl", "tp1", "rr", "win_prob", "expected_r", "risk_pct"])
    led["side_n"] = led["side"].replace({"LONG": "BUY", "SHORT": "SELL"})
    led["order"] = led["rank"].isin(["A", "B"]) & led["side_n"].isin(["BUY", "SELL"])
    sim = pd.read_csv(ROOT / "data/execution_simulation.csv")
    sim["date"] = pd.to_datetime(sim["date"])
    sc = pd.read_csv(ROOT / "data/prediction_log_scores.csv")
    sc["date"] = pd.to_datetime(sc["date"])
    prices = {a: px(a) for a in ASSETS}

    # ------------------------------------------------------------------ 0. 頻度
    say("0. 売買頻度（docs/signal_drought_2026-11-02.md の要約。tools/throughput_watch.py と同じ定義）")
    lg = tw.load_ledger(ROOT / "data/signal_log.csv")
    orders = tw.mark_runs(lg)
    lg["month"] = lg["date"].dt.to_period("M")
    orders["month"] = orders["date"].dt.to_period("M")
    t0 = pd.DataFrame({
        "ledger_days": lg.groupby("month")["date"].nunique(),
        "orders": orders.groupby("month").size(),
        "ideas": orders[orders["run_start"]].groupby("month").size(),
    }).fillna(0).astype(int)
    t0["ideas_per_week"] = (t0["ideas"] / t0["ledger_days"] * 7).round(2)
    print(t0.to_string())
    R["throughput_monthly"] = t0.reset_index().astype(str).to_dict("records")
    h = tw.history(lg)
    R["throughput_alert_episodes"] = tw.alert_episodes(h)
    print("ALERT 区間:", R["throughput_alert_episodes"])

    # ------------------------------------------------------------------ 1. SL幅
    say("1. (13) SL幅を通常へ戻した後の SL率・実損 — 執行シミュレーション（確定行のみ）")
    bins = [pd.Timestamp("2026-01-01"), pd.Timestamp("2026-07-16"), pd.Timestamp("2026-08-31"),
            pd.Timestamp("2026-09-15"), pd.Timestamp("2026-12-31")]
    labels = ["~7/15", "7/16-8/31(SL2倍)", "9/1-9/15", "9/16-"]
    sim["period"] = pd.cut(sim["date"], bins, labels=labels)
    f = sim[sim["status"].isin(FINAL)]
    t1 = f.groupby("period").agg(n=("r_result", "size"), sl=("status", lambda s: (s == "filled_sl").sum()),
                                 tp1=("status", lambda s: (s == "filled_tp1").sum()),
                                 time=("status", lambda s: (s == "filled_time_exit").sum()),
                                 r_sum=("r_result", "sum"), r_mean=("r_result", "mean"))
    t1["sl_rate"] = (t1["sl"] / t1["n"]).round(2)
    t1["no_fill"] = sim[sim["status"] == "no_fill"].groupby("period").size()
    print(t1.round(2).to_string())
    R["sl_by_period"] = t1.round(3).reset_index().astype(str).to_dict("records")

    say("1b. 申告 SL 幅 ÷ ATR10（判断日の前日まで）— 資産×期間の中央値")
    b = led[led["order"] & (led["risk_pct"] > 0)].copy()
    b["mid"] = (b["entry_low"] + b["entry_high"]) / 2
    b["sl_w"] = (b["mid"] - b["sl"]).abs()
    b["atr10"] = [atr10_before(prices[a], d) if a in prices else np.nan for a, d in zip(b["asset"], b["date"])]
    b["sl_atr"] = b["sl_w"] / b["atr10"]
    b["period"] = np.where(b["date"] < "2026-07-16", "~7/15", np.where(b["date"] < "2026-09-01", "7/16-8/31", np.where(b["date"] < "2026-09-16", "9/1-9/15", "9/16-")))
    t1b = b.groupby(["period"]).agg(n=("sl_atr", "size"), sl_atr_med=("sl_atr", "median")).round(2)
    print(t1b.to_string())
    t1c = b[b["date"] >= "2026-09-16"].groupby("asset").agg(n=("sl_atr", "size"), sl_atr_med=("sl_atr", "median")).round(2)
    print("\n9/16以降 資産別:\n" + t1c.to_string())
    R["sl_atr_by_period"] = t1b.reset_index().astype(str).to_dict("records")

    say("1c. 併走観測 atr_floor（SL幅 = max(申告, 1×ATR10)）— 同じ行の既定 r_result と並べる")
    a = sim[sim["atr_floor_r"].notna()]
    for lab, sub in [("全期間", a), ("9/16以降", a[a["date"] >= "2026-09-16"])]:
        print(f"{lab}: n={len(sub)} atr_floor={sub['atr_floor_r'].sum():.2f}R / 既定={sub['r_result'].sum():.2f}R / 差={sub['atr_floor_r'].sum() - sub['r_result'].sum():+.2f}R")
        R[f"atr_floor_{lab}"] = {"n": int(len(sub)), "atr_floor": round(float(sub["atr_floor_r"].sum()), 2), "baseline": round(float(sub["r_result"].sum()), 2)}
    ta = a.groupby("asset").agg(n=("atr_floor_r", "size"), atr_floor=("atr_floor_r", "sum"), baseline=("r_result", "sum")).round(2)
    ta["diff"] = (ta["atr_floor"] - ta["baseline"]).round(2)
    print(ta.to_string())
    print("status(全期間):", a["atr_floor_status"].value_counts().to_dict(), "| 既定:", a["status"].value_counts().to_dict())

    # ------------------------------------------------------------------ 2. regime
    say("2. (13) regime 6語の遵守率と分布（2026-09-01 以降）")
    VOC = {"RISK_ON", "RISK_OFF", "NEUTRAL", "MIXED", "EVENT", "UNKNOWN"}
    r = led[led["date"] >= "2026-09-01"].copy()
    r["month"] = r["date"].dt.to_period("M")
    print("遵守率:", round(float(r["regime"].isin(VOC).mean()), 3), "n=", len(r))
    print(pd.crosstab(r["month"], r["regime"], normalize="index").round(2).to_string())
    R["regime_compliance"] = round(float(r["regime"].isin(VOC).mean()), 3)

    # ------------------------------------------------------------------ 3. 主役
    say("3. (13) 主役の申告 vs 機械判定 LEADER_V1（遡及コーパス、as-of D-1）")
    lo = pd.read_csv(ROOT / "data/leader_observations.csv")
    lo["date"] = pd.to_datetime(lo["date"])
    mk = pd.read_csv(ROOT / "data/retro/market_daily.csv", parse_dates=["date"])
    ctx = mk[["date", "leader_asset", "leader_margin"]].sort_values("date")
    j = pd.merge_asof(lo.sort_values("date"), ctx, on="date", direction="backward", allow_exact_matches=False)
    j2 = lo.merge(ctx, on="date", how="left")
    m1 = round(float((j["leader_claimed"] == j["leader_asset"]).mean()), 3)
    m2 = round(float((j2["leader_claimed"] == j2["leader_asset"]).mean()), 3)
    print(f"n={len(lo)} 一致率 as-of D-1: {m1} / 同日: {m2}  コーパス最終日: {mk['date'].max().date()}")
    print(pd.crosstab(j["leader_claimed"], j["leader_asset"]).to_string())
    R["leader_match"] = {"n": int(len(lo)), "asof": m1, "same_day": m2}
    # 申告主役と同じ資産への判断の成績
    act = sc[(sc["actionable"] == True) & sc["result_5d"].isin(["success", "failure"])].copy()  # noqa: E712
    act = act.merge(lo[["date", "leader_claimed"]], on="date", how="left")
    act["on_claimed_leader"] = act["asset"] == act["leader_claimed"]
    sub = act[act["leader_claimed"].notna()]
    if len(sub):
        g = sub.groupby("on_claimed_leader").agg(n=("signal_id", "size"), win=("result_5d", lambda s: (s == "success").mean()), r5=("r_close_5d", "mean")).round(3)
        print("\n申告主役と同じ資産への判断（5日決着）:\n" + g.to_string())
        R["on_claimed_leader"] = g.reset_index().astype(str).to_dict("records")

    # ------------------------------------------------------------------ 4. crypto
    say("4. (14) crypto_grounds と BTC/ETH の見送り率")
    cg = pd.read_csv(ROOT / "data/crypto_grounds_observations.csv")
    cg["date"] = pd.to_datetime(cg["date"])
    m = led[led["asset"].isin(["BTC", "ETH"])].merge(cg[["date", "etf_grounds", "cme_grounds"]], on="date", how="inner")
    print(m.groupby(["asset", "etf_grounds", "cme_grounds"]).agg(n=("rank", "size"), no_trade=("rank", lambda s: (s == "NO_TRADE").mean())).round(2).to_string())
    print("etf_grounds:", cg["etf_grounds"].value_counts().to_dict(), "cme_grounds:", cg["cme_grounds"].value_counts().to_dict())

    say("4b. (14) 週次 crypto 予測の検算（CRYPTO_PRED: 期日の終値で判定。GPT の自己採点 prev_result と並べる）")
    cp_path = ROOT / "data/crypto_predictions_weekly.csv"
    cc_path = ROOT / "data/crypto_context_weekly.csv"
    if cp_path.exists() and cp_path.stat().st_size > 60:
        cp = pd.read_csv(cp_path)
        cc = pd.read_csv(cc_path) if cc_path.exists() else pd.DataFrame()
        btc = prices["BTC"]
        rows = []
        for _, p in cp.iterrows():
            ws = pd.Timestamp(p["week_start"])
            pred_day = ws + pd.Timedelta(days=6)  # 日曜の実行日
            deadline = pd.Timestamp(p["deadline"])
            level = float(p["level"])
            at_pred = btc[btc.index <= pred_day]["close"]
            at_pred = float(at_pred.iloc[-1]) if len(at_pred) else np.nan
            upto = btc[(btc.index > pred_day) & (btc.index <= deadline)]["close"]
            dl_close = float(upto.iloc[-1]) if len(upto) and deadline <= btc.index.max() else np.nan
            direction = str(p["direction"]).upper()
            if np.isnan(dl_close):
                hit = "pending"
            elif direction == "ABOVE":
                hit = "HIT" if dl_close >= level else "MISS"
            else:
                hit = "HIT" if dl_close <= level else "MISS"
            # 「触れた」判定: 期日までのどこかで条件を満たした終値があるか
            if len(upto):
                touched = bool((upto >= level).any()) if direction == "ABOVE" else bool((upto <= level).any())
            else:
                touched = None
            # 翌週の自己採点
            nxt = cc[cc["week_start"] == (ws + pd.Timedelta(days=7)).strftime("%Y-%m-%d")] if len(cc) else pd.DataFrame()
            self_grade = str(nxt["prev_result"].iloc[0]) if len(nxt) else ""
            rows.append({"week_start": p["week_start"], "pred": f"{p['asset']} {direction} {level:.0f} by {p['deadline']}",
                         "px_at_pred": round(at_pred, 0), "level_vs_px_%": round((level / at_pred - 1) * 100, 1) if at_pred else np.nan,
                         "deadline_close": round(dl_close, 0) if not np.isnan(dl_close) else "", "machine": hit, "touched": touched, "gpt_prev_result(next week)": self_grade})
        t4 = pd.DataFrame(rows)
        print(t4.to_string(index=False))
        dec = t4[t4["machine"].isin(["HIT", "MISS"])]
        print(f"\n決着 {len(dec)} 件: 機械 HIT {int((dec['machine'] == 'HIT').sum())} / GPT自己採点 HIT {int((dec['gpt_prev_result(next week)'] == 'HIT').sum())}"
              f" / 一致 {int((dec['machine'] == dec['gpt_prev_result(next week)']).sum())}")
        R["crypto_pred"] = t4.astype(str).to_dict("records")
    else:
        print("data/crypto_predictions_weekly.csv が空。週次タスクの出力が記録されていない。")

    # ------------------------------------------------------------------ 5. expected_r_basis / invalidation
    say("5. (15) expected_r_basis の分布")
    eb = pd.read_csv(ROOT / "data/expected_r_basis.csv")
    print(eb["expected_r_basis"].value_counts().to_dict(), f"({eb['date'].min()}〜{eb['date'].max()}, n={len(eb)})")
    R["expected_r_basis"] = eb["expected_r_basis"].value_counts().to_dict()

    say("5b. (15) invalidation が fired になった判断 — 発動の報告は SL/TP の後だったか、前なら降りた方が良かったか")
    ic = pd.read_csv(ROOT / "data/invalidation_checks.csv")
    ic["check_date"] = pd.to_datetime(ic["check_date"])
    print("verdicts:", ic["invalidation_fired"].value_counts().to_dict())
    rows = []
    for _, fr in ic[ic["invalidation_fired"] == "fired"].iterrows():
        sid = fr["signal_id"]
        L = led[led["signal_id"] == sid]
        S = sim[sim["signal_id"] == sid]
        if L.empty:
            rows.append({"signal_id": sid, "note": "台帳に無い"})
            continue
        L = L.iloc[0]
        S = S.iloc[0] if not S.empty else None
        p = prices[L["asset"]]
        sign = 1 if L["side_n"] == "BUY" else -1
        before = p[p.index < fr["check_date"]]
        after = p[p.index >= fr["check_date"]]
        obs_bar = before.index[-1] if len(before) else pd.NaT  # 報告の朝に見えていた最後のバー
        exit_px = float(after["open"].iloc[0]) if len(after) else np.nan  # 降りられる最初の値
        fill_date = pd.to_datetime(S["fill_date"]) if S is not None and isinstance(S["fill_date"], str) else pd.NaT
        exit_date = pd.to_datetime(S["exit_date"]) if S is not None and isinstance(S["exit_date"], str) else pd.NaT
        status = S["status"] if S is not None else ""
        sim_r = float(S["r_result"]) if S is not None and pd.notna(S["r_result"]) else np.nan
        if S is None or status == "no_fill" or pd.isna(fill_date) or fill_date > obs_bar:
            kind = "未約定(注文取消で済む)"
            r_on_fired = 0.0
        elif pd.notna(exit_date) and exit_date <= obs_bar:
            kind = f"手遅れ(既に {status} で決着済み)"
            r_on_fired = sim_r
        else:
            kind = "降りられた"
            r_on_fired = sign * (exit_px - float(S["fill_price"])) / float(S["risk_unit"])
        rows.append({"signal_id": sid, "check": fr["check_date"].date(), "obs_bar": obs_bar.date() if pd.notna(obs_bar) else "",
                     "fill": fill_date.date() if pd.notna(fill_date) else "", "sim_exit": exit_date.date() if pd.notna(exit_date) else "",
                     "sim_status": status, "sim_r": round(sim_r, 2) if not np.isnan(sim_r) else "", "kind": kind,
                     "r_if_exit_on_fired": round(r_on_fired, 2) if not np.isnan(r_on_fired) else ""})
    t5 = pd.DataFrame(rows)
    print(t5.to_string(index=False))
    kinds = t5["kind"].str.split("(").str[0].value_counts().to_dict() if "kind" in t5 else {}
    print("内訳:", kinds)
    ok = t5[t5["kind"] == "降りられた"] if "kind" in t5 else pd.DataFrame()
    if len(ok):
        print(f"降りられた {len(ok)} 件: 既定 {pd.to_numeric(ok['sim_r']).sum():.2f}R vs 発動で降りる {pd.to_numeric(ok['r_if_exit_on_fired']).sum():.2f}R")
    R["fired_kinds"] = kinds

    # ------------------------------------------------------------------ 6. chase / half_exit
    say("6. (16)(17) 成行参加 chase_r と TP1半分 half_exit_r — 2026-09-09 以降の確定行、同じ行の既定と並べる")
    s9 = sim[(sim["date"] >= "2026-09-09")]
    for c in ["chase_r", "half_exit_r", "half_exit_be_r", "forgone_r"]:
        sub = s9[s9[c].notna()]
        print(f"{c}: n={len(sub)} 合計={sub[c].sum():.2f}R / 同じ行の既定={sub['r_result'].sum():.2f}R")
        R[c] = {"n": int(len(sub)), "sum": round(float(sub[c].sum()), 2), "baseline": round(float(sub["r_result"].sum()), 2)}
    print("chase_status:", s9["chase_status"].value_counts(dropna=False).to_dict())
    print("half_exit_status:", s9["half_exit_status"].value_counts(dropna=False).to_dict())
    ch = sim[(sim["asset"].isin(["NASDAQ", "BTC", "USDJPY"])) & sim["chase_r"].notna()]
    print(f"chase 3資産 全期間: n={len(ch)} chase={ch['chase_r'].sum():.2f}R / 既定={ch['r_result'].sum():.2f}R")

    # ------------------------------------------------------------------ 7. 較正
    say("7. win_prob の較正（actionable・5日決着）— 月別")
    act = sc[(sc["actionable"] == True) & sc["result_5d"].isin(["success", "failure"])].merge(  # noqa: E712
        led[["signal_id", "win_prob"]], on="signal_id", how="left")
    act["month"] = act["date"].dt.to_period("M")
    g = act.groupby("month").agg(n=("signal_id", "size"), wp=("win_prob", "mean"), realized=("result_5d", lambda s: (s == "success").mean()),
                                 r5=("r_close_5d", "mean"), touched=("entry_touched_5d", "mean"))
    g["err"] = g["realized"] - g["wp"]
    print(g.round(3).to_string())
    late = act[act["date"] >= "2026-09-16"]
    print(f"9/16以降: n={len(late)} wp={late['win_prob'].mean():.3f} realized={(late['result_5d'] == 'success').mean():.3f} r5={late['r_close_5d'].mean():.2f}")
    R["calibration_monthly"] = g.round(3).reset_index().astype(str).to_dict("records")

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(R, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
        print(f"\njson -> {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
