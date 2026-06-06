from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


RAW_DIR = Path("data/raw")
RESULTS_DIR = Path("results")
EVALUATION_COLUMNS = [
    "signal_id",
    "asset",
    "side",
    "rank",
    "signal_date",
    "evaluation_status",
    "hit_date",
    "hit_level",
    "mfe",
    "mae",
    "r_result",
    "bars_checked",
    "notes",
]


def load_ohlcv(asset: str) -> pd.DataFrame:
    path = RAW_DIR / f"{asset}.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]
    if "date" not in df.columns:
        return pd.DataFrame()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in ["open", "high", "low", "close"]:
        if col not in df.columns:
            df[col] = np.nan
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["date", "open", "high", "low", "close"]).sort_values("date")


def first_hit(side: str, future: pd.DataFrame, sl: float, tp1: float, tp2: float) -> tuple[str, str | None, str | None]:
    for _, bar in future.iterrows():
        date = pd.Timestamp(bar["date"]).strftime("%Y-%m-%d")
        high = float(bar["high"])
        low = float(bar["low"])
        if side == "LONG":
            sl_hit = low <= sl
            tp2_hit = high >= tp2
            tp1_hit = high >= tp1
        else:
            sl_hit = high >= sl
            tp2_hit = low <= tp2
            tp1_hit = low <= tp1

        if sl_hit:
            return "closed", date, "SL"
        if tp2_hit:
            return "closed", date, "TP2"
        if tp1_hit:
            return "closed", date, "TP1"
    return "open", None, "UNREACHED"


def evaluate_one(signal: pd.Series) -> dict:
    base = {
        "signal_id": signal.get("signal_id"),
        "asset": signal.get("asset"),
        "side": signal.get("side"),
        "rank": signal.get("rank"),
        "signal_date": signal.get("date"),
        "evaluation_status": "pending",
        "hit_date": None,
        "hit_level": None,
        "mfe": None,
        "mae": None,
        "r_result": None,
        "bars_checked": 0,
        "notes": "",
    }

    side = str(signal.get("side", "NONE"))
    if side not in {"LONG", "SHORT"}:
        base.update({"evaluation_status": "skipped", "hit_level": "NO_TRADE", "notes": "No trade signal"})
        return base

    needed = ["entry_low", "entry_high", "sl", "tp1", "tp2"]
    if any(pd.isna(signal.get(col)) for col in needed):
        base.update({"evaluation_status": "skipped", "notes": "Missing trade levels"})
        return base

    df = load_ohlcv(str(signal.get("asset")))
    if df.empty:
        base.update({"notes": "No OHLC data for asset"})
        return base

    signal_date = pd.to_datetime(signal.get("date"), errors="coerce")
    future = df[df["date"] > signal_date].copy()
    if future.empty:
        base.update({"notes": "No next-day data yet"})
        return base

    entry = (float(signal["entry_low"]) + float(signal["entry_high"])) / 2
    sl = float(signal["sl"])
    tp1 = float(signal["tp1"])
    tp2 = float(signal["tp2"])
    risk = abs(entry - sl)
    if risk <= 0:
        base.update({"evaluation_status": "skipped", "notes": "Invalid risk distance"})
        return base

    if side == "LONG":
        mfe = (future["high"].max() - entry) / risk
        mae = (future["low"].min() - entry) / risk
    else:
        mfe = (entry - future["low"].min()) / risk
        mae = (entry - future["high"].max()) / risk

    status, hit_date, hit_level = first_hit(side, future, sl, tp1, tp2)
    if hit_level == "SL":
        r_result = -1.0
    elif hit_level == "TP1":
        r_result = 1.0
    elif hit_level == "TP2":
        r_result = 2.0
    else:
        last_close = float(future.iloc[-1]["close"])
        r_result = ((last_close - entry) / risk) if side == "LONG" else ((entry - last_close) / risk)

    base.update(
        {
            "evaluation_status": status,
            "hit_date": hit_date,
            "hit_level": hit_level,
            "mfe": round(float(mfe), 4),
            "mae": round(float(mae), 4),
            "r_result": round(float(r_result), 4),
            "bars_checked": len(future),
            "notes": "Virtual evaluation only",
        }
    )
    return base


def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    signals_path = RESULTS_DIR / "signals.csv"
    if not signals_path.exists():
        evaluations = pd.DataFrame(columns=EVALUATION_COLUMNS)
    else:
        signals = pd.read_csv(signals_path)
        evaluations = pd.DataFrame([evaluate_one(row) for _, row in signals.iterrows()], columns=EVALUATION_COLUMNS)

    evaluations.to_csv(RESULTS_DIR / "evaluations.csv", index=False)
    evaluations.to_json(RESULTS_DIR / "evaluations.json", orient="records", indent=2, force_ascii=False)
    print(f"evaluations generated: {len(evaluations)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
