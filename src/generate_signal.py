from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


RAW_DIR = Path("data/raw")
RESULTS_DIR = Path("results")
SIGNAL_COLUMNS = [
    "date",
    "signal_id",
    "asset",
    "side",
    "rank",
    "type",
    "entry_low",
    "entry_high",
    "sl",
    "tp1",
    "tp2",
    "rr",
    "win_prob",
    "expected_r",
    "tq_score",
    "opp_score",
    "no_trade_score",
    "risk_pct",
    "regime",
    "ems",
    "ffs",
    "cds",
    "ias",
    "cbs",
    "mes",
    "invalidation",
    "verification_target",
]


def load_ohlcv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]
    if "date" not in df.columns:
        raise ValueError(f"{path} has no date column")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in ["open", "high", "low", "close", "volume"]:
        if col not in df.columns:
            df[col] = np.nan
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["date", "open", "high", "low", "close"])
    return df.sort_values("date").drop_duplicates(subset=["date"], keep="last").reset_index(drop=True)


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    close = out["close"]
    high = out["high"]
    low = out["low"]
    prev_close = close.shift(1)
    tr = pd.concat([(high - low), (high - prev_close).abs(), (low - prev_close).abs()], axis=1).max(axis=1)

    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14, min_periods=14).mean()
    avg_loss = loss.rolling(14, min_periods=14).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)

    out["ma20"] = close.rolling(20, min_periods=20).mean()
    out["ma50"] = close.rolling(50, min_periods=50).mean()
    out["rsi14"] = 100 - (100 / (1 + rs))
    out["atr14"] = tr.rolling(14, min_periods=14).mean()
    out["chg1d"] = close.pct_change(1)
    out["chg5d"] = close.pct_change(5)
    return out


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    if pd.isna(value):
        return 0.0
    return float(max(low, min(high, value)))


def score_signal(last: pd.Series) -> dict:
    close = float(last["close"])
    ma20 = float(last["ma20"]) if pd.notna(last["ma20"]) else np.nan
    ma50 = float(last["ma50"]) if pd.notna(last["ma50"]) else np.nan
    rsi = float(last["rsi14"]) if pd.notna(last["rsi14"]) else np.nan
    atr = float(last["atr14"]) if pd.notna(last["atr14"]) else np.nan
    chg1d = float(last["chg1d"]) if pd.notna(last["chg1d"]) else 0.0
    chg5d = float(last["chg5d"]) if pd.notna(last["chg5d"]) else 0.0

    if any(pd.isna(v) for v in [close, ma20, ma50, rsi, atr]) or atr <= 0:
        return {
            "side": "NONE",
            "rank": "NO_TRADE",
            "type": "NO_TRADE",
            "regime": "INSUFFICIENT_DATA",
            "ems": 0,
            "ffs": 0,
            "cds": 0,
            "ias": 0,
            "cbs": 0,
            "mes": 0,
            "tq_score": 0,
            "opp_score": 0,
            "no_trade_score": 100,
        }

    trend_long = close > ma20 > ma50
    trend_short = close < ma20 < ma50
    extension = abs(close - ma20) / atr
    volatility = atr / close

    long_points = 0
    short_points = 0
    long_points += 28 if trend_long else 0
    short_points += 28 if trend_short else 0
    long_points += 18 if chg5d > 0 else 0
    short_points += 18 if chg5d < 0 else 0
    long_points += 14 if 45 <= rsi <= 68 else 0
    short_points += 14 if 32 <= rsi <= 55 else 0
    long_points += 10 if chg1d > -0.015 else 0
    short_points += 10 if chg1d < 0.015 else 0

    if long_points >= short_points and long_points >= 46:
        side = "LONG"
        opp_score = short_points
    elif short_points > long_points and short_points >= 46:
        side = "SHORT"
        opp_score = long_points
    else:
        side = "NONE"
        opp_score = max(long_points, short_points)

    ems = clamp(50 + (close - ma50) / atr * 8) if side == "LONG" else clamp(50 + (ma50 - close) / atr * 8)
    ffs = clamp(50 + abs(chg5d) * 500)
    cds = clamp(100 - extension * 18)
    ias = clamp(70 - abs(rsi - 50) * 1.2)
    cbs = clamp(65 if ((side == "LONG" and chg1d > 0) or (side == "SHORT" and chg1d < 0)) else 45)
    mes = clamp(75 - volatility * 1200)
    tq_score = round((ems * 0.25) + (ffs * 0.15) + (cds * 0.2) + (ias * 0.15) + (cbs * 0.1) + (mes * 0.15), 2)
    no_trade_score = round(clamp(100 - tq_score + (25 if side == "NONE" else 0)), 2)

    if side == "NONE":
        rank = "NO_TRADE"
        signal_type = "NO_TRADE"
    elif tq_score >= 70 and no_trade_score < 40:
        rank = "A"
        signal_type = "TREND"
    elif tq_score >= 55:
        rank = "B"
        signal_type = "TREND"
    else:
        side = "NONE"
        rank = "NO_TRADE"
        signal_type = "NO_TRADE"

    if trend_long:
        regime = "UPTREND"
    elif trend_short:
        regime = "DOWNTREND"
    else:
        regime = "RANGE"

    return {
        "side": side,
        "rank": rank,
        "type": signal_type,
        "regime": regime,
        "ems": round(ems, 2),
        "ffs": round(ffs, 2),
        "cds": round(cds, 2),
        "ias": round(ias, 2),
        "cbs": round(cbs, 2),
        "mes": round(mes, 2),
        "tq_score": tq_score,
        "opp_score": round(float(opp_score), 2),
        "no_trade_score": no_trade_score,
    }


def build_row(asset: str, df: pd.DataFrame) -> dict:
    enriched = add_indicators(df)
    last = enriched.iloc[-1]
    latest_date = pd.Timestamp(last["date"]).strftime("%Y-%m-%d")
    date_id = pd.Timestamp(last["date"]).strftime("%Y%m%d")
    close = float(last["close"])
    atr = float(last["atr14"]) if pd.notna(last["atr14"]) else np.nan
    score = score_signal(last)
    side = score["side"]
    signal_type = score["type"]

    if side == "LONG":
        entry_low = close - atr * 0.25
        entry_high = close + atr * 0.15
        sl = close - atr * 1.2
        tp1 = close + atr * 1.2
        tp2 = close + atr * 2.4
        invalidation = "Close below SL or loss of MA20 support"
        verification_target = "TP1 then TP2 from next sessions"
    elif side == "SHORT":
        entry_low = close - atr * 0.15
        entry_high = close + atr * 0.25
        sl = close + atr * 1.2
        tp1 = close - atr * 1.2
        tp2 = close - atr * 2.4
        invalidation = "Close above SL or recovery above MA20"
        verification_target = "TP1 then TP2 from next sessions"
    else:
        entry_low = entry_high = sl = tp1 = tp2 = np.nan
        invalidation = "No actionable setup"
        verification_target = "Wait for trend and risk conditions to align"

    rr = 2.0 if side in {"LONG", "SHORT"} else 0.0
    win_prob = 0.0 if side == "NONE" else round(min(0.68, max(0.42, 0.42 + score["tq_score"] / 400)), 3)
    expected_r = round((win_prob * rr) - (1 - win_prob), 3) if side != "NONE" else 0.0
    risk_pct = 1.0 if score["rank"] == "A" else 0.5 if score["rank"] == "B" else 0.0
    signal_id = f"{date_id}_{asset}_{side}_{signal_type}"

    row = {
        "date": latest_date,
        "signal_id": signal_id,
        "asset": asset,
        "side": side,
        "rank": score["rank"],
        "type": signal_type,
        "entry_low": entry_low,
        "entry_high": entry_high,
        "sl": sl,
        "tp1": tp1,
        "tp2": tp2,
        "rr": rr,
        "win_prob": win_prob,
        "expected_r": expected_r,
        "risk_pct": risk_pct,
        "invalidation": invalidation,
        "verification_target": verification_target,
        **score,
    }
    return {col: row.get(col) for col in SIGNAL_COLUMNS}


def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    rows = []

    for path in sorted(RAW_DIR.glob("*.csv")):
        try:
            df = load_ohlcv(path)
            if df.empty:
                continue
            rows.append(build_row(path.stem, df))
        except Exception as exc:  # noqa: BLE001 - one bad input should not stop other assets.
            print(f"signal error: {path.name} {exc}")

    signals = pd.DataFrame(rows, columns=SIGNAL_COLUMNS)
    signals.to_csv(RESULTS_DIR / "signals.csv", index=False)
    signals.to_json(RESULTS_DIR / "signals.json", orient="records", indent=2, force_ascii=False)
    print(f"signals generated: {len(signals)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
