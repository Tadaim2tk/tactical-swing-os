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
