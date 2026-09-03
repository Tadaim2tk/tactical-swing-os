"""遡及市場コーパス: 価格層の一括構築 (SPEC-RNC-001)。

5年の日次OHLCVを一度きり取得し、監査の教訓に従って
- リターンは資産固有カレンダー上の close-to-close (fill_method=None)
- wide表での一括pct_change禁止 (資産別に計算してから日付で結合)
- FXはopenを使わない / 各資産のbar_dateを明示列で持つ
- 先行遅行は merge_asof(backward, allow_exact_matches=False)
を実装する。ラベル語彙は閉じた集合・閾値は事前宣言(層別用・未検証)。

出力: data/retro/prices_long.csv, data/retro/market_daily.csv
retrospective_derived — point-in-time台帳(market_context_daily.csv)とは別物。併合禁止。
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

OUT_DIR = Path("data/retro")
TICKERS = {
    "GOLD": "GC=F", "BTC": "BTC-USD", "ETH": "ETH-USD", "WTI": "CL=F",
    "USDJPY": "JPY=X", "SPX": "ES=F", "NASDAQ": "NQ=F", "DXY": "DX-Y.NYB",
    "US10Y": "^TNX", "VIX": "^VIX",
}
PERIOD = "5y"

# 層別用・未検証のv1閾値(事前宣言。当てはめで選んでいない。変更時はTHRESHOLDS版を上げる)
THRESHOLDS_V1 = {
    "risk_ret": 0.003,     # SPXリターンの有意とみなす下限(±0.3%)
    "risk_vix": 0.03,      # VIX変化率の有意下限(±3%)
    "flat_band": 0.0015,   # up/down/flat の flat 帯(±0.15%)
    "flat_band_yield": 0.02,  # US10Yは水準変化(pt)で判定(±0.02pt)
    "vol_calm": 16.0, "vol_stressed": 24.0,
}

# 主役アセット判定 v1 (2026-08-31 人間発案「その時市場の主役だったアセットを切り替えながら
# 見る」。式は事前宣言・層別用・未検証。当てはめ探索で選んでいない):
#   dominance = (直近W日の他資産との|相関|平均) × (直近W日の自身の活発度 / 直近BASE日の平常活発度)
#   leader = dominance 最大の資産。相関は両資産にバーがある日だけで計算(埋めない)。
LEADER_V1 = {"window": 20, "min_periods": 12, "activity_base": 120}


def fetch_asset(asset: str, ticker: str) -> pd.DataFrame:
    df = yf.download(ticker, period=PERIOD, interval="1d", auto_adjust=False, progress=False)
    if df.empty:
        return pd.DataFrame()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]
    df = df.reset_index()
    df.columns = [str(c).strip().lower() for c in df.columns]
    df["date"] = pd.to_datetime(df["date"], utc=True).dt.tz_localize(None).dt.normalize()
    df = df.dropna(subset=["date", "close"]).sort_values("date").reset_index(drop=True)
    out = pd.DataFrame({
        "asset": asset,
        "date": df["date"],
        "close": pd.to_numeric(df["close"], errors="coerce"),
        "high": pd.to_numeric(df.get("high"), errors="coerce"),
        "low": pd.to_numeric(df.get("low"), errors="coerce"),
    })
    out = out.dropna(subset=["close"]).reset_index(drop=True)
    # 資産固有カレンダー上の close-to-close (ERS#1: pad埋め禁止を明示)
    out["ret_cc"] = out["close"].pct_change(fill_method=None)
    # 20日実現ボラ(層別用)
    out["vol20"] = out["ret_cc"].rolling(20, min_periods=10).std() * np.sqrt(252)
    return out


def _move(x: float, band: float) -> str:
    if pd.isna(x):
        return "unknown"
    if x > band:
        return "up"
    if x < -band:
        return "down"
    return "flat"


def build_daily(prices: pd.DataFrame) -> pd.DataFrame:
    t = THRESHOLDS_V1
    frames = {}
    for asset, g in prices.groupby("asset"):
        g = g.sort_values("date").reset_index(drop=True)
        frames[asset] = g
    # 全観測日(いずれかの資産にバーがある日)を行にする。埋めない(ERS流: 空欄は空欄)。
    all_dates = sorted(prices["date"].unique())
    rows = []
    for d in all_dates:
        row: dict = {"date": pd.Timestamp(d)}
        for asset, g in frames.items():
            hit = g[g["date"] == d]
            if len(hit):
                r = hit.iloc[0]
                row[f"ret_{asset}"] = round(float(r["ret_cc"]), 6) if pd.notna(r["ret_cc"]) else np.nan
                row[f"close_{asset}"] = float(r["close"])
                row[f"bar_date_{asset}"] = str(pd.Timestamp(d).date())
        rows.append(row)
    daily = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)

    # US10Yはリターンでなく水準変化(pt)も持つ
    if "close_US10Y" in daily.columns:
        daily["chg_US10Y_pt"] = daily["close_US10Y"].diff().round(4)

    # 先行遅行(ERS#2): 各行に「その日より前で直近の」米株セッションを当てる。
    # 同日は当てない(allow_exact_matches=False相当)。休み跨ぎはSPXの累積リターン。
    spx = frames.get("SPX", pd.DataFrame())
    if not spx.empty:
        spx_l = spx[["date", "ret_cc", "close"]].rename(
            columns={"ret_cc": "prev_us_ret", "close": "prev_us_close"})
        spx_l["cum_log"] = np.log1p(spx_l["prev_us_ret"].fillna(0)).cumsum()
        merged = pd.merge_asof(
            daily[["date"]], spx_l, on="date", direction="backward",
            allow_exact_matches=False)
        daily["prev_us_bar_date"] = merged["date"].where(merged["prev_us_close"].notna())
        # 前回この結合が当てたバーから今回のバーまでの累積(休み跨ぎを取りこぼさない)
        cum = merged["cum_log"]
        daily["prev_us_ret_cum"] = (np.exp(cum - cum.shift(1)) - 1).round(6)
        daily["prev_us_ret_1bar"] = merged["prev_us_ret"].round(6)

    # ラベル(閉じた語彙・ルール計算のみ)
    def risk_state(r):
        s, v = r.get("ret_SPX"), r.get("ret_VIX")
        if pd.isna(s) or pd.isna(v):
            return "unknown"
        if s > t["risk_ret"] and v < -t["risk_vix"]:
            return "risk_on"
        if s < -t["risk_ret"] and v > t["risk_vix"]:
            return "risk_off"
        if (s > t["risk_ret"] and v > t["risk_vix"]) or (s < -t["risk_ret"] and v < -t["risk_vix"]):
            return "mixed"
        return "neutral"

    def vol_state(r):
        v = r.get("close_VIX")
        if pd.isna(v):
            return "unknown"
        if v < t["vol_calm"]:
            return "calm"
        if v > t["vol_stressed"]:
            return "stressed"
        return "elevated"

    # 主役アセット(LEADER_V1)。wide表はリターン計算には使わない(ERS#1) — 相関の観測にだけ使う。
    # pandas rolling corr は「両方に観測がある日」だけで計算する(min_periods未満はNaN)。
    lw, lmp, lbase = LEADER_V1["window"], LEADER_V1["min_periods"], LEADER_V1["activity_base"]
    wide = daily.set_index("date")[[f"ret_{a}" for a in frames]].rename(
        columns=lambda c: c.replace("ret_", ""))
    abs_ret = wide.abs()
    activity = abs_ret.rolling(lw, min_periods=lmp).mean() / abs_ret.rolling(
        lbase, min_periods=lw * 2).mean()
    corr_sum = pd.DataFrame(0.0, index=wide.index, columns=wide.columns)
    corr_n = pd.DataFrame(0, index=wide.index, columns=wide.columns)
    cols = list(wide.columns)
    for i, a in enumerate(cols):
        for b in cols[i + 1:]:
            c = wide[a].rolling(lw, min_periods=lmp).corr(wide[b]).abs()
            corr_sum[a] = corr_sum[a] + c.fillna(0)
            corr_sum[b] = corr_sum[b] + c.fillna(0)
            corr_n[a] = corr_n[a] + c.notna().astype(int)
            corr_n[b] = corr_n[b] + c.notna().astype(int)
    mean_corr = corr_sum / corr_n.replace(0, np.nan)
    dominance = (mean_corr * activity).round(4)
    valid_cnt = dominance.notna().sum(axis=1)
    leader = dominance.idxmax(axis=1, skipna=True)
    leader[valid_cnt < 3] = "none"
    daily["leader_asset"] = leader.fillna("none").values
    dmax = dominance.max(axis=1)
    d2nd = dominance.apply(lambda r: r.nlargest(2).iloc[-1] if r.notna().sum() >= 2 else np.nan, axis=1)
    daily["leader_score"] = dmax.round(4).values
    daily["leader_margin"] = (dmax - d2nd).round(4).values  # 2位との差=主役の明確さ

    daily["risk_state"] = daily.apply(risk_state, axis=1)
    daily["vol_state"] = daily.apply(vol_state, axis=1)
    daily["yield_move"] = daily.get("chg_US10Y_pt", pd.Series(np.nan, index=daily.index)).apply(
        lambda x: _move(x, t["flat_band_yield"]))
    daily["usd_move"] = daily.get("ret_DXY", pd.Series(np.nan, index=daily.index)).apply(
        lambda x: _move(x, t["flat_band"]))
    daily["crypto_move"] = daily.get("ret_BTC", pd.Series(np.nan, index=daily.index)).apply(
        lambda x: _move(x, t["flat_band"]))
    daily["provenance"] = "retrospective_derived"
    return daily


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # 取得は一度きり(SPEC-RNC-001): 既に取得済みなら再フェッチせず、派生の再計算だけ行う
    cached = OUT_DIR / "prices_long.csv"
    if cached.exists() and "--extend" in sys.argv:
        # 主役判定の継続比較のため、既存の一度きり取得へ最新分だけ足す(全取得はしない)。
        # 既存行は書き換えず、新しい日付のバーだけ追記して派生を作り直す。
        old = pd.read_csv(cached, parse_dates=["date"])
        # 資産ごとに cutoff を持つ(#138 Codex P1: 全体の最大日で切ると、週7日の暗号資産が
        # 先に進んだ分だけ週5日資産の新しいバーが落ちる)。
        cutoffs = old.groupby("asset")["date"].max().to_dict()
        # 形成途中のバーを凍結しない(#138 Codex P1): ラベル日がUTCで過ぎたバーだけ確定として
        # 保存し、当日ラベルは保存しない。前回入った未確定バーは捨てて取り直す。
        today_utc = pd.Timestamp(datetime.now(timezone.utc).date())
        fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        old = old[old["date"] < today_utc]
        parts = [old]
        for asset, ticker in TICKERS.items():
            df = fetch_asset(asset, ticker)
            if df.empty:
                continue
            cut = cutoffs.get(asset, pd.Timestamp.min)
            add = df[(df["date"] > cut) & (df["date"] < today_utc)].copy()
            if not add.empty:
                add["fetched_at"] = fetched_at
                add["provenance"] = "retrospective_derived"
                parts.append(add)
        prices = pd.concat(parts, ignore_index=True).drop_duplicates(
            subset=["asset", "date"], keep="last").sort_values(["asset", "date"])
        prices.to_csv(cached, index=False)
        daily = build_daily(prices)
        daily["fetched_at"] = fetched_at
        daily.to_csv(OUT_DIR / "market_daily.csv", index=False)
        print(f"extended: prices {len(old)}→{len(prices)} rows, daily {len(daily)} rows "
              f"(資産別cutoff: {min(cutoffs.values()).date()}..{max(cutoffs.values()).date()})")
        return 0
    if cached.exists():
        prices = pd.read_csv(cached, parse_dates=["date"])
        fetched_at = str(prices["fetched_at"].iloc[0]) if "fetched_at" in prices.columns else "unknown"
        print(f"using cached prices_long.csv ({len(prices)} rows, fetched_at={fetched_at})")
        daily = build_daily(prices)
        daily["fetched_at"] = fetched_at
        daily.to_csv(OUT_DIR / "market_daily.csv", index=False)
        print(f"daily: {len(daily)} rows -> {OUT_DIR/'market_daily.csv'}")
        print("thresholds_v1:", THRESHOLDS_V1, "| leader_v1:", LEADER_V1)
        return 0
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    parts = []
    for asset, ticker in TICKERS.items():
        df = fetch_asset(asset, ticker)
        if df.empty:
            print(f"warn: {asset} ({ticker}) empty", file=sys.stderr)
            continue
        print(f"{asset}: {len(df)} bars {df['date'].min().date()}..{df['date'].max().date()}")
        parts.append(df)
    prices = pd.concat(parts, ignore_index=True)
    prices["fetched_at"] = fetched_at
    prices["provenance"] = "retrospective_derived"
    prices.to_csv(OUT_DIR / "prices_long.csv", index=False)

    daily = build_daily(prices)
    daily["fetched_at"] = fetched_at
    daily.to_csv(OUT_DIR / "market_daily.csv", index=False)
    print(f"daily: {len(daily)} rows -> {OUT_DIR/'market_daily.csv'}")
    print("thresholds_v1:", THRESHOLDS_V1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
