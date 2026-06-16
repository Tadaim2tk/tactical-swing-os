from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import pandas as pd

import cost_model


RAW_DIR = Path("data/raw")
RESULTS_DIR = Path("results")
EVALUATION_COLUMNS = [
    "signal_id",
    "asset",
    "side",
    "rank",
    "type",
    "signal_date",
    "evaluation_date",
    "status",
    "evaluation_status",
    "entry_low",
    "entry_high",
    "entry_hit",
    "entry_hit_date",
    "entry_price",
    "sl",
    "tp1",
    "tp2",
    "sl_hit",
    "sl_hit_date",
    "tp1_hit",
    "tp1_hit_date",
    "tp2_hit",
    "tp2_hit_date",
    "mfe",
    "mae",
    "mfe_r",
    "mae_r",
    "r_multiple",
    "r_result",
    "cost_r",
    "r_result_net",
    "cost_source",
    "outcome",
    "error_type",
    "missed_opportunity",
    "hit_date",
    "hit_level",
    "bars_checked",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate Tactical Swing OS signals.")
    parser.add_argument("--horizon", type=int, default=5, help="Maximum number of future bars to evaluate")
    return parser.parse_args()


def normalize_column_name(column: str) -> str:
    normalized = str(column).strip().lower().replace("-", "_")
    normalized = "_".join(normalized.split())
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    return normalized


def load_ohlcv(asset: str) -> pd.DataFrame:
    path = RAW_DIR / f"{asset}.csv"
    if not path.exists():
        return pd.DataFrame()
    try:
        df = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()
    df.columns = [normalize_column_name(col) for col in df.columns]
    if "date" not in df.columns:
        return pd.DataFrame()
    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True).dt.tz_localize(None)
    for col in ["open", "high", "low", "close"]:
        if col not in df.columns:
            df[col] = np.nan
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["date", "open", "high", "low", "close"]).sort_values("date")
    return add_atr(df)


def add_atr(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    prev_close = out["close"].shift(1)
    ranges = pd.concat(
        [
            out["high"] - out["low"],
            (out["high"] - prev_close).abs(),
            (out["low"] - prev_close).abs(),
        ],
        axis=1,
    )
    out["atr14"] = ranges.max(axis=1).rolling(14, min_periods=1).mean()
    return out


def safe_float(value) -> float | None:
    value = pd.to_numeric(value, errors="coerce")
    if pd.isna(value):
        return None
    return float(value)


def safe_date(value) -> pd.Timestamp | None:
    date = pd.to_datetime(value, errors="coerce", utc=True)
    if pd.isna(date):
        return None
    return pd.Timestamp(date).tz_localize(None)


def date_str(value) -> str | None:
    if value is None or pd.isna(value):
        return None
    return pd.Timestamp(value).strftime("%Y-%m-%d")


def base_result(signal: pd.Series) -> dict:
    return {
        "signal_id": signal.get("signal_id"),
        "asset": signal.get("asset"),
        "side": str(signal.get("side", "NONE")).upper(),
        "rank": signal.get("rank"),
        "type": signal.get("type"),
        "signal_date": signal.get("date"),
        "evaluation_date": None,
        "status": "pending",
        "evaluation_status": "pending",
        "entry_low": signal.get("entry_low"),
        "entry_high": signal.get("entry_high"),
        "entry_hit": False,
        "entry_hit_date": None,
        "entry_price": None,
        "sl": signal.get("sl"),
        "tp1": signal.get("tp1"),
        "tp2": signal.get("tp2"),
        "sl_hit": False,
        "sl_hit_date": None,
        "tp1_hit": False,
        "tp1_hit_date": None,
        "tp2_hit": False,
        "tp2_hit_date": None,
        "mfe": None,
        "mae": None,
        "mfe_r": None,
        "mae_r": None,
        "r_multiple": None,
        "r_result": None,
        "cost_r": 0.0,
        "r_result_net": None,
        "cost_source": "unconfigured",
        "outcome": "open_unresolved",
        "error_type": "",
        "missed_opportunity": False,
        "hit_date": None,
        "hit_level": None,
        "bars_checked": 0,
        "notes": "",
    }


def finish(result: dict, *, status: str, evaluation_status: str, outcome: str, error_type: str, note: str = "") -> dict:
    result["status"] = status
    result["evaluation_status"] = evaluation_status
    result["outcome"] = outcome
    result["error_type"] = error_type
    if note:
        result["notes"] = append_note(result["notes"], note)
    # コスト未適用の経路(no_trade/no_entry/open等)はネット=グロスで埋める(SPEC-TC-001)
    if result.get("r_result_net") is None:
        result["r_result_net"] = result.get("r_result")
    return result


def apply_cost(result: dict, asset: str, risk_per_unit: float, bars_held: float) -> None:
    """closed評価のグロスRへ取引コストを適用し、ネットRを記録する (SPEC-TC-001)。"""
    gross = result.get("r_result")
    if gross is None:
        return
    cost = cost_model.asset_cost(asset)
    c_r = cost_model.cost_r(asset, risk_per_unit, bars_held)
    result["cost_r"] = round(c_r, 4)
    result["r_result_net"] = round(float(gross) - c_r, 4)
    result["cost_source"] = cost["source"]


def append_note(notes: str | None, note: str) -> str:
    if not notes:
        return note
    if note in notes.split(";"):
        return notes
    return f"{notes};{note}"


def future_bars(df: pd.DataFrame, signal_date: pd.Timestamp | None, horizon: int) -> pd.DataFrame:
    if signal_date is None or df.empty:
        return pd.DataFrame()
    future = df[df["date"] > signal_date].copy()
    if horizon > 0:
        future = future.head(horizon)
    return future


def range_touches_entry(bar: pd.Series, entry_low: float, entry_high: float) -> bool:
    return float(bar["high"]) >= entry_low and float(bar["low"]) <= entry_high


def no_trade_result(signal: pd.Series, df: pd.DataFrame, horizon: int) -> dict:
    result = base_result(signal)
    signal_date = safe_date(signal.get("date"))
    if signal_date is None:
        # 日付が不正/欠損 = 評価位置を決められない入力不正。若さ(awaiting_horizon)ではない。
        result["r_multiple"] = 0.0
        result["r_result"] = 0.0
        return finish(result, status="invalid", evaluation_status="skipped", outcome="invalid", error_type="invalid_signal_date", note="Invalid or missing signal date")
    future = future_bars(df, signal_date, horizon)
    result["bars_checked"] = len(future)
    if not future.empty:
        result["evaluation_date"] = date_str(future.iloc[-1]["date"])
    if df.empty:
        result["r_multiple"] = 0.0
        result["r_result"] = 0.0
        return finish(result, status="no_trade", evaluation_status="skipped", outcome="no_trade", error_type="data_missing", note="No OHLC data for no-trade evaluation")
    if future.empty:
        # OHLCはあるが signal_date 以降のバーがまだ無い = ホライズン未到達。
        # no_trade の正否(correct/missed)はまだ判定不能。欠損(data_missing)とは区別する。
        result["r_multiple"] = 0.0
        result["r_result"] = 0.0
        return finish(result, status="no_trade", evaluation_status="skipped", outcome="no_trade", error_type="awaiting_horizon", note="No-trade signal newer than latest OHLC bar; correctness not yet assessable")

    price_range = float(future["high"].max() - future["low"].min())
    atr_series = df[df["date"] <= future.iloc[0]["date"]]["atr14"].dropna()
    atr14 = float(atr_series.iloc[-1]) if not atr_series.empty else math.nan
    result["mfe"] = round(price_range, 4)
    result["mae"] = 0.0
    result["r_multiple"] = 0.0
    result["r_result"] = 0.0
    if math.isfinite(atr14) and price_range < atr14 * 2:
        outcome = "no_trade_correct"
    else:
        outcome = "no_trade_missed"
    result["hit_level"] = "NO_TRADE"
    return finish(result, status="no_trade", evaluation_status="skipped", outcome=outcome, error_type="no_trade", note="No trade signal")


def direction_r(side: str, price: float, entry: float, risk: float) -> float:
    if side == "LONG":
        return (price - entry) / risk
    return (entry - price) / risk


def evaluate_trade(signal: pd.Series, df: pd.DataFrame, horizon: int) -> dict:
    result = base_result(signal)
    side = result["side"]
    signal_date = safe_date(signal.get("date"))
    if signal_date is None:
        # 日付が不正/欠損 = 評価位置を決められない入力不正。若さ(awaiting_horizon)ではない。
        return finish(result, status="invalid", evaluation_status="skipped", outcome="invalid", error_type="invalid_signal_date", note="Invalid or missing signal date")
    future = future_bars(df, signal_date, horizon)
    result["bars_checked"] = len(future)
    if not future.empty:
        result["evaluation_date"] = date_str(future.iloc[-1]["date"])

    if df.empty:
        return finish(result, status="pending", evaluation_status="pending", outcome="open_unresolved", error_type="data_missing", note="No OHLC data available for asset")
    if future.empty:
        # OHLCはあるが signal_date 以降のバーがまだ無い = ホライズン未到達(若い/蓄積中)。
        # 「価格データが本当に無い(data_missing)」と区別し、誤った赤(欠損)を出さない。
        return finish(result, status="pending", evaluation_status="pending", outcome="open_unresolved", error_type="awaiting_horizon", note="Signal newer than latest OHLC bar; horizon not yet elapsed")

    entry_low = safe_float(signal.get("entry_low"))
    entry_high = safe_float(signal.get("entry_high"))
    sl = safe_float(signal.get("sl"))
    tp1 = safe_float(signal.get("tp1"))
    tp2 = safe_float(signal.get("tp2"))
    if None in [entry_low, entry_high, sl, tp1, tp2]:
        return finish(result, status="invalid", evaluation_status="skipped", outcome="invalid", error_type="data_missing", note="Missing trade levels")
    if entry_low > entry_high:
        entry_low, entry_high = entry_high, entry_low

    entry_price = (entry_low + entry_high) / 2
    result.update(
        {
            "entry_low": entry_low,
            "entry_high": entry_high,
            "entry_price": round(entry_price, 8),
            "sl": sl,
            "tp1": tp1,
            "tp2": tp2,
        }
    )
    risk = (entry_price - sl) if side == "LONG" else (sl - entry_price)
    if risk <= 0:
        result["r_multiple"] = 0.0
        result["r_result"] = 0.0
        return finish(result, status="invalid", evaluation_status="skipped", outcome="invalid", error_type="invalid_risk", note="Invalid risk distance")

    entry_index = None
    for idx, bar in future.iterrows():
        if range_touches_entry(bar, entry_low, entry_high):
            entry_index = idx
            result["entry_hit"] = True
            result["entry_hit_date"] = date_str(bar["date"])
            break

    if entry_index is None:
        high_max = float(future["high"].max())
        low_min = float(future["low"].min())
        missed = (side == "LONG" and high_max >= entry_high + risk) or (side == "SHORT" and low_min <= entry_low - risk)
        result["mfe"] = round(high_max - entry_price, 4) if side == "LONG" else round(entry_price - low_min, 4)
        result["mae"] = round(low_min - entry_price, 4) if side == "LONG" else round(entry_price - high_max, 4)
        result["mfe_r"] = round(float(result["mfe"]) / risk, 4)
        result["mae_r"] = round(float(result["mae"]) / risk, 4)
        result["r_multiple"] = 0.0
        result["r_result"] = 0.0
        result["hit_level"] = "NO_ENTRY"
        if missed:
            result["missed_opportunity"] = True
            return finish(result, status="no_entry", evaluation_status="pending", outcome="no_entry", error_type="missed_entry", note="missed_after_no_entry")
        return finish(result, status="no_entry", evaluation_status="pending", outcome="no_entry", error_type="no_entry", note="Entry not reached")

    after_entry = future.loc[entry_index:].copy()
    high_max = float(after_entry["high"].max())
    low_min = float(after_entry["low"].min())
    if side == "LONG":
        mfe = high_max - entry_price
        mae = low_min - entry_price
    else:
        mfe = entry_price - low_min
        mae = entry_price - high_max
    result["mfe"] = round(float(mfe), 4)
    result["mae"] = round(float(mae), 4)
    result["mfe_r"] = round(float(mfe / risk), 4)
    result["mae_r"] = round(float(mae / risk), 4)

    for bars_held, (_, bar) in enumerate(after_entry.iterrows(), start=1):
        bar_date = date_str(bar["date"])
        high = float(bar["high"])
        low = float(bar["low"])
        if side == "LONG":
            sl_hit = low <= sl
            tp1_hit = high >= tp1
            tp2_hit = high >= tp2
            tp_r = direction_r(side, tp2 if tp2_hit else tp1, entry_price, risk)
        else:
            sl_hit = high >= sl
            tp1_hit = low <= tp1
            tp2_hit = low <= tp2
            tp_r = direction_r(side, tp2 if tp2_hit else tp1, entry_price, risk)

        if sl_hit and (tp1_hit or tp2_hit):
            result["notes"] = append_note(result["notes"], "same_bar_sl_tp_conservative_sl")
        if sl_hit:
            result.update({"sl_hit": True, "sl_hit_date": bar_date, "hit_date": bar_date, "hit_level": "SL", "r_multiple": -1.0, "r_result": -1.0})
            apply_cost(result, result["asset"], risk, bars_held)
            return finish(result, status="closed", evaluation_status="closed", outcome="loss_sl", error_type="stop_loss", note="Virtual evaluation only")
        if tp2_hit:
            r_multiple = round(float(tp_r), 4)
            result.update({"tp1_hit": True, "tp1_hit_date": bar_date, "tp2_hit": True, "tp2_hit_date": bar_date, "hit_date": bar_date, "hit_level": "TP2", "r_multiple": r_multiple, "r_result": r_multiple})
            apply_cost(result, result["asset"], risk, bars_held)
            return finish(result, status="closed", evaluation_status="closed", outcome="win_tp2", error_type="target_reached", note="Virtual evaluation only")
        if tp1_hit:
            r_multiple = round(float(tp_r), 4)
            result.update({"tp1_hit": True, "tp1_hit_date": bar_date, "hit_date": bar_date, "hit_level": "TP1", "r_multiple": r_multiple, "r_result": r_multiple})
            apply_cost(result, result["asset"], risk, bars_held)
            return finish(result, status="closed", evaluation_status="closed", outcome="win_tp1", error_type="target_reached", note="Virtual evaluation only")

    last_close = float(after_entry.iloc[-1]["close"])
    r_multiple = round(float(direction_r(side, last_close, entry_price, risk)), 4)
    result.update({"hit_level": "UNREACHED", "r_multiple": r_multiple, "r_result": r_multiple})
    return finish(result, status="open", evaluation_status="pending", outcome="open_unresolved", error_type="unresolved", note="Evaluation horizon ended without SL/TP")


def evaluate_one(signal: pd.Series, horizon: int) -> dict:
    side = str(signal.get("side", "NONE")).upper()
    rank = str(signal.get("rank", "")).upper()
    asset = str(signal.get("asset", "")).strip()
    df = load_ohlcv(asset) if asset else pd.DataFrame()
    if side == "NONE" or rank == "NO_TRADE":
        return no_trade_result(signal, df, horizon)
    if side not in {"LONG", "SHORT"}:
        result = base_result(signal)
        result["r_multiple"] = 0.0
        result["r_result"] = 0.0
        return finish(result, status="invalid", evaluation_status="skipped", outcome="invalid", error_type="data_missing", note="Unsupported side")
    return evaluate_trade(signal, df, horizon)


def evaluate_signals_dataframe(signals: pd.DataFrame, horizon: int) -> pd.DataFrame:
    if signals.empty:
        return pd.DataFrame(columns=EVALUATION_COLUMNS)

    normalized = signals.copy()
    normalized.columns = [normalize_column_name(col) for col in normalized.columns]
    rows = [evaluate_one(row, horizon) for _, row in normalized.iterrows()]
    return pd.DataFrame(rows).reindex(columns=EVALUATION_COLUMNS)


def main() -> int:
    args = parse_args()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    signals_path = RESULTS_DIR / "signals.csv"
    if not signals_path.exists():
        evaluations = pd.DataFrame(columns=EVALUATION_COLUMNS)
    else:
        signals = pd.read_csv(signals_path)
        evaluations = evaluate_signals_dataframe(signals, args.horizon)

    evaluations.to_csv(RESULTS_DIR / "evaluations.csv", index=False)
    evaluations.to_json(RESULTS_DIR / "evaluations.json", orient="records", indent=2, force_ascii=False)
    print(f"evaluations generated: {len(evaluations)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
