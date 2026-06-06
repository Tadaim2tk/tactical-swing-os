"""generate_signal.py – Phase 6 multi-score swing signal generator.

All existing columns in SIGNAL_COLUMNS are preserved for backward
compatibility with evaluate_signal.py / sync_to_sheets.py / weekly &
monthly review scripts.  New scoring columns are appended after the
existing ones in SIGNAL_COLUMNS.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


RAW_DIR = Path("data/raw")
RESULTS_DIR = Path("results")

# ── Existing columns (MUST remain unchanged) ──────────────────────────────────
_EXISTING_COLUMNS: list[str] = [
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

# ── New Phase-6 columns ────────────────────────────────────────────────────────
_NEW_COLUMNS: list[str] = [
    "trend_score",
    "momentum_score",
    "volatility_score",
    "risk_penalty_score",
    "setup_quality_score",
    "entry_quality_score",
    "direction_confidence",
    "reason_codes",
    "no_trade_reason",
    "signal_strength",
    "recommended_action",
    "data_quality",
]

SIGNAL_COLUMNS: list[str] = _EXISTING_COLUMNS + _NEW_COLUMNS


# ── Utilities ─────────────────────────────────────────────────────────────────

def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    if pd.isna(value):
        return 0.0
    return float(max(low, min(high, value)))


def _safe(series: pd.Series, default: float = np.nan) -> float:
    val = series.iloc[-1] if len(series) else default
    return float(val) if pd.notna(val) else default


# ── Data loading ──────────────────────────────────────────────────────────────

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


# ── Indicator computation ─────────────────────────────────────────────────────

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    close = out["close"]
    high = out["high"]
    low = out["low"]
    prev_close = close.shift(1)

    # True Range / ATR14
    tr = pd.concat(
        [(high - low), (high - prev_close).abs(), (low - prev_close).abs()],
        axis=1,
    ).max(axis=1)

    # RSI14
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14, min_periods=14).mean()
    avg_loss = loss.rolling(14, min_periods=14).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)

    # Core indicators
    out["ma20"] = close.rolling(20, min_periods=20).mean()
    out["ma50"] = close.rolling(50, min_periods=50).mean()
    out["rsi14"] = 100 - (100 / (1 + rs))
    out["atr14"] = tr.rolling(14, min_periods=14).mean()
    out["chg1d"] = close.pct_change(1)
    out["chg5d"] = close.pct_change(5)

    # Phase-6 additions
    out["ma20_slope"] = out["ma20"].diff(3) / out["ma20"].shift(3)   # 3-bar slope ratio
    out["ma50_slope"] = out["ma50"].diff(3) / out["ma50"].shift(3)
    out["atr_pct60"] = out["atr14"].rank(pct=True, method="average").rolling(60, min_periods=20).apply(
        lambda x: x.iloc[-1], raw=False
    )
    out["high20"] = high.rolling(20, min_periods=5).max()
    out["low20"] = low.rolling(20, min_periods=5).min()
    out["breakout_up"] = close > out["high20"].shift(1)
    out["breakout_down"] = close < out["low20"].shift(1)
    out["dist_ma20"] = (close - out["ma20"]) / out["atr14"]
    out["dist_ma50"] = (close - out["ma50"]) / out["atr14"]
    rng20 = (out["high20"] - out["low20"]).replace(0, np.nan)
    out["range_pos_20d"] = ((close - out["low20"]) / rng20).clip(0, 1)

    return out


# ── Score functions (all return 0-100 float) ──────────────────────────────────

def calc_trend_score(
    close: float,
    ma20: float,
    ma50: float,
    ma20_slope: float,
    ma50_slope: float,
) -> float:
    """Higher = stronger bull trend; lower = stronger bear trend; ~50 = unclear."""
    score = 50.0
    if np.isnan(ma20) or np.isnan(ma50):
        return score

    # Price alignment
    if close > ma20 > ma50:
        score += 25
    elif close < ma20 < ma50:
        score -= 25

    # MA order partial credit
    if ma20 > ma50:
        score += 8
    elif ma20 < ma50:
        score -= 8

    # MA slope
    if not np.isnan(ma20_slope):
        score += clamp(ma20_slope * 2000, -12, 12)
    if not np.isnan(ma50_slope):
        score += clamp(ma50_slope * 2000, -8, 8)

    return clamp(score)


def calc_momentum_score(
    chg1d: float,
    chg5d: float,
    breakout_up: bool,
    breakout_down: bool,
) -> float:
    score = 50.0

    # 1-day change
    score += clamp(chg1d * 500, -10, 10)
    # 5-day change
    score += clamp(chg5d * 300, -15, 15)

    # Breakout bonus
    if breakout_up:
        score += 15
    if breakout_down:
        score -= 15

    # Over-extension penalty (excessive one-sided move increases reversal risk)
    if abs(chg5d) > 0.07:
        score -= 5

    return clamp(score)


def calc_volatility_score(atr_pct60: float) -> float:
    """Middle ATR percentile is best (40-70); extremes are penalized."""
    if np.isnan(atr_pct60):
        return 40.0
    p = atr_pct60  # 0-1
    if 0.40 <= p <= 0.70:
        return 80.0
    if 0.25 <= p < 0.40 or 0.70 < p <= 0.80:
        return 65.0
    if p > 0.85:
        return 40.0  # too volatile
    if p < 0.20:
        return 35.0  # not enough volatility
    return 55.0


def calc_risk_penalty(
    rsi: float,
    side: str,
    atr_pct60: float,
    dist_ma20: float,
    rr: float,
) -> float:
    """Higher = more dangerous. Not clipped here – caller clips to 0-100."""
    penalty = 0.0

    if not np.isnan(rsi):
        if side == "LONG" and rsi > 75:
            penalty += 30 + (rsi - 75) * 1.5
        if side == "SHORT" and rsi < 25:
            penalty += 30 + (25 - rsi) * 1.5

    if not np.isnan(atr_pct60) and atr_pct60 > 0.85:
        penalty += 20

    # Entry far from MA20 (overextended)
    if not np.isnan(dist_ma20) and abs(dist_ma20) > 2.5:
        penalty += 15

    # RR too low
    if rr < 1.5:
        penalty += 25

    return clamp(penalty)


def calc_setup_quality(
    trend: float,
    momentum: float,
    volatility: float,
    risk_penalty: float,
) -> float:
    raw = 0.35 * trend + 0.35 * momentum + 0.20 * volatility - 0.20 * risk_penalty + 10
    return clamp(raw)


def calc_entry_quality(
    atr: float,
    sl_dist: float,
    rr: float,
    dist_ma20: float,
) -> float:
    """Ideal SL is 0.8-2.5 ATR away; RR >= 1.5 is required."""
    score = 55.0

    # SL distance check
    sl_atr = sl_dist / atr if atr > 0 else np.nan
    if not np.isnan(sl_atr):
        if 0.8 <= sl_atr <= 2.5:
            score += 25
        elif sl_atr < 0.5:
            score -= 20  # too tight
        elif sl_atr > 3.5:
            score -= 15  # too wide

    # RR
    if rr >= 1.5:
        score += 20
    else:
        score -= 25

    # Entry near MA20 (pullback bonus)
    if not np.isnan(dist_ma20) and abs(dist_ma20) < 0.5:
        score += 10

    return clamp(score)


def calc_direction_confidence(
    trend_score: float,
    momentum_score: float,
    side: str,
) -> float:
    """High when trend & momentum both agree with the chosen side."""
    if side == "LONG":
        t = trend_score          # high trend_score = bullish
        m = momentum_score       # high momentum_score = bullish
    elif side == "SHORT":
        t = 100 - trend_score    # invert: low trend_score = bearish = high short confidence
        m = 100 - momentum_score
    else:
        return 0.0

    # If both point the same direction, confidence is high
    agreement = 1 - abs(t - m) / 100
    base = (t + m) / 2
    return clamp(base * agreement * 1.1)


# ── Reason code builder ───────────────────────────────────────────────────────

def build_reason_codes(
    close: float,
    ma20: float,
    ma50: float,
    ma20_slope: float,
    rsi: float,
    atr_pct60: float,
    chg5d: float,
    breakout_up: bool,
    breakout_down: bool,
    rr: float,
    dist_ma20: float,
    rng_pos: float,
    risk_penalty: float,
) -> list[str]:
    codes: list[str] = []

    if not np.isnan(ma20) and not np.isnan(ma50):
        if close > ma20 > ma50:
            codes += ["trend_up", "ma_alignment_bull"]
        elif close < ma20 < ma50:
            codes += ["trend_down", "ma_alignment_bear"]

    if not np.isnan(ma20_slope):
        if ma20_slope > 0.001:
            codes.append("momentum_positive")
        elif ma20_slope < -0.001:
            codes.append("momentum_negative")

    if breakout_up:
        codes.append("breakout_up")
    if breakout_down:
        codes.append("breakout_down")

    if not np.isnan(rsi):
        if rsi > 70:
            codes.append("rsi_overbought")
        elif rsi < 30:
            codes.append("rsi_oversold")

    if not np.isnan(atr_pct60):
        if atr_pct60 > 0.85:
            codes.append("atr_too_high")
        elif atr_pct60 < 0.20:
            codes.append("atr_too_low")

    if rr < 1.5:
        codes.append("rr_too_low")

    if not np.isnan(rng_pos) and 0.4 <= rng_pos <= 0.6:
        codes.append("range_middle")

    if not np.isnan(dist_ma20) and abs(dist_ma20) < 0.4:
        codes.append("pullback_to_ma20")

    if risk_penalty >= 70:
        codes.append("risk_penalty_high")

    if abs(chg5d) > 0.07:
        codes.append("overextended")

    return codes


def build_no_trade_reason(
    trend_score: float,
    risk_penalty: float,
    atr_pct60: float,
    rr: float,
    rng_pos: float,
    rsi: float,
    side: str,
    data_quality: str,
) -> str:
    if data_quality != "OK":
        return "data_insufficient"
    if risk_penalty >= 80:
        return "risk_penalty_high"
    if not np.isnan(atr_pct60) and atr_pct60 < 0.20:
        return "low_volatility"
    if rr < 1.5:
        return "rr_too_low"
    if 45 <= trend_score <= 55:
        return "trend_unclear"
    if not np.isnan(rng_pos) and 0.4 <= rng_pos <= 0.6:
        return "range_middle"
    if not np.isnan(rsi):
        if side in {"LONG", "NONE"} and rsi > 75:
            return "overextended"
        if side in {"SHORT", "NONE"} and rsi < 25:
            return "overextended"
    return ""


# ── Signal type detection ─────────────────────────────────────────────────────

def decide_signal_type(
    side: str,
    rank: str,
    trend_score: float,
    momentum_score: float,
    breakout_up: bool,
    breakout_down: bool,
    dist_ma20: float,
) -> str:
    if side == "NONE" or rank == "NO_TRADE":
        return "NO_TRADE"
    bo = (side == "LONG" and breakout_up) or (side == "SHORT" and breakout_down)
    if bo and momentum_score >= 70:
        return "A-Momentum"
    if not np.isnan(dist_ma20) and abs(dist_ma20) < 0.5 and trend_score >= 60:
        return "A-Pullback"
    if rank == "B":
        return "B-Watch"
    return "TREND"


# ── Core signal builder ───────────────────────────────────────────────────────

def build_row(asset: str, df: pd.DataFrame) -> dict[str, Any]:  # noqa: C901
    enriched = add_indicators(df)
    n = len(enriched)
    last = enriched.iloc[-1]

    latest_date = pd.Timestamp(last["date"]).strftime("%Y-%m-%d")
    date_id = pd.Timestamp(last["date"]).strftime("%Y%m%d")
    close = float(last["close"])

    # ── Data quality gate ───────────────────────────────────────────────────
    data_quality = "OK"
    if n < 20:
        data_quality = "SHORT_HISTORY"
    atr = float(last["atr14"]) if pd.notna(last["atr14"]) else np.nan
    if data_quality == "OK" and (np.isnan(atr) or atr <= 0):
        data_quality = "INVALID_ATR"
    ma20 = float(last["ma20"]) if pd.notna(last["ma20"]) else np.nan
    ma50 = float(last["ma50"]) if pd.notna(last["ma50"]) else np.nan
    rsi = float(last["rsi14"]) if pd.notna(last["rsi14"]) else np.nan
    if data_quality == "OK" and any(np.isnan(v) for v in [ma20]):
        data_quality = "SHORT_HISTORY"

    # ── Indicator extraction ────────────────────────────────────────────────
    ma20_slope = float(last["ma20_slope"]) if pd.notna(last.get("ma20_slope")) else np.nan
    ma50_slope = float(last["ma50_slope"]) if pd.notna(last.get("ma50_slope")) else np.nan
    atr_pct60 = float(last["atr_pct60"]) if pd.notna(last.get("atr_pct60")) else np.nan
    high20 = float(last["high20"]) if pd.notna(last.get("high20")) else np.nan
    low20 = float(last["low20"]) if pd.notna(last.get("low20")) else np.nan
    breakout_up = bool(last.get("breakout_up", False))
    breakout_down = bool(last.get("breakout_down", False))
    dist_ma20 = float(last["dist_ma20"]) if pd.notna(last.get("dist_ma20")) else np.nan
    dist_ma50 = float(last["dist_ma50"]) if pd.notna(last.get("dist_ma50")) else np.nan
    rng_pos = float(last["range_pos_20d"]) if pd.notna(last.get("range_pos_20d")) else np.nan
    chg1d = float(last["chg1d"]) if pd.notna(last["chg1d"]) else 0.0
    chg5d = float(last["chg5d"]) if pd.notna(last["chg5d"]) else 0.0

    # ── Insufficient data fallback ─────────────────────────────────────────
    if data_quality != "OK":
        empty: dict[str, Any] = {col: np.nan for col in SIGNAL_COLUMNS}
        empty.update({
            "date": latest_date,
            "signal_id": f"{date_id}_{asset}_NONE_NO_TRADE",
            "asset": asset,
            "side": "NONE",
            "rank": "NO_TRADE",
            "type": "NO_TRADE",
            "regime": "INSUFFICIENT_DATA",
            "ems": 0, "ffs": 0, "cds": 0, "ias": 0, "cbs": 0, "mes": 0,
            "tq_score": 0, "opp_score": 0, "no_trade_score": 100,
            "rr": 0, "win_prob": 0, "expected_r": 0, "risk_pct": 0,
            "invalidation": "No actionable setup",
            "verification_target": "Wait for sufficient data",
            "trend_score": 0, "momentum_score": 0, "volatility_score": 0,
            "risk_penalty_score": 100, "setup_quality_score": 0,
            "entry_quality_score": 0, "direction_confidence": 0,
            "reason_codes": "data_insufficient",
            "no_trade_reason": "data_insufficient",
            "signal_strength": 0,
            "recommended_action": "NO_TRADE",
            "data_quality": data_quality,
        })
        return {col: empty.get(col) for col in SIGNAL_COLUMNS}

    # ── Phase-6 scores (side-agnostic first pass) ───────────────────────────
    trend_score = calc_trend_score(close, ma20, ma50, ma20_slope, ma50_slope)
    momentum_score = calc_momentum_score(chg1d, chg5d, breakout_up, breakout_down)
    volatility_score = calc_volatility_score(atr_pct60)

    # ── Preliminary side determination (needed for risk_penalty) ───────────
    # momentum_score is bullish-biased (high = bullish momentum).
    # For SHORT we use the bear-momentum equivalent: 100 - momentum_score.
    bear_momentum = 100 - momentum_score

    # LONG conditions
    long_ok = (
        close > ma20
        and (ma20 >= ma50 or (not np.isnan(ma20_slope) and ma20_slope > 0))
        and momentum_score >= 55
    )
    # SHORT conditions
    short_ok = (
        close < ma20
        and (ma20 <= ma50 or (not np.isnan(ma20_slope) and ma20_slope < 0))
        and bear_momentum >= 55
    )

    if long_ok and not short_ok:
        prelim_side = "LONG"
    elif short_ok and not long_ok:
        prelim_side = "SHORT"
    elif long_ok and short_ok:
        # Both pass; pick by trend strength
        prelim_side = "LONG" if trend_score > 55 else "SHORT" if trend_score < 45 else "NONE"
    else:
        prelim_side = "NONE"

    # ── Entry / SL / TP (preliminary, for scoring) ─────────────────────────
    if prelim_side == "LONG":
        entry_low = close - 0.30 * atr
        entry_high = close + 0.10 * atr
        sl_base = close - 1.2 * atr
        sl_candidate_low20 = (low20 - 0.1 * atr) if not np.isnan(low20) else sl_base
        sl = min(sl_base, sl_candidate_low20)  # more conservative (lower)
        entry_mid = (entry_low + entry_high) / 2
        risk = abs(entry_mid - sl)
        tp1 = entry_mid + 1.5 * risk if risk > 0 else np.nan
        tp2 = entry_mid + 2.5 * risk if risk > 0 else np.nan
    elif prelim_side == "SHORT":
        entry_low = close - 0.10 * atr
        entry_high = close + 0.30 * atr
        sl_base = close + 1.2 * atr
        sl_candidate_high20 = (high20 + 0.1 * atr) if not np.isnan(high20) else sl_base
        sl = max(sl_base, sl_candidate_high20)  # more conservative (higher)
        entry_mid = (entry_low + entry_high) / 2
        risk = abs(sl - entry_mid)
        tp1 = entry_mid - 1.5 * risk if risk > 0 else np.nan
        tp2 = entry_mid - 2.5 * risk if risk > 0 else np.nan
    else:
        entry_low = entry_high = sl = tp1 = tp2 = np.nan
        entry_mid = close
        risk = 0.0

    rr = round((1.5 * risk) / risk, 4) if risk > 0 else 0.0  # always 1.5 by construction; recalc properly below
    # Actual RR = distance to TP1 / distance to SL
    if prelim_side in {"LONG", "SHORT"} and risk > 0 and not np.isnan(tp1):
        rr = round(abs(tp1 - entry_mid) / risk, 4)
    else:
        rr = 0.0

    sl_dist = abs(close - sl) if not np.isnan(sl) else np.nan

    # ── Phase-6 scores (side-aware) ────────────────────────────────────────
    # trend_score and momentum_score are bull-biased (high = bullish).
    # For SHORT evaluation we invert them so 100 = strong bearish.
    directional_trend = trend_score if prelim_side != "SHORT" else (100 - trend_score)
    directional_momentum = momentum_score if prelim_side != "SHORT" else bear_momentum
    risk_penalty_score = calc_risk_penalty(rsi, prelim_side, atr_pct60, dist_ma20, rr)
    setup_quality_score = calc_setup_quality(directional_trend, directional_momentum, volatility_score, risk_penalty_score)
    entry_quality_score = calc_entry_quality(atr, sl_dist if not np.isnan(sl_dist) else 0, rr, dist_ma20)
    direction_confidence = calc_direction_confidence(trend_score, momentum_score, prelim_side)

    # ── Final side / rank arbitration ──────────────────────────────────────
    # Reject if risk_penalty is too high
    if risk_penalty_score >= 80:
        prelim_side = "NONE"

    # Regime / trend clarity gate
    unclear_trend = 45 <= trend_score <= 55
    if unclear_trend and prelim_side in {"LONG", "SHORT"}:
        prelim_side = "NONE"

    # ATR insufficiency gate (very low volatility)
    if not np.isnan(atr_pct60) and atr_pct60 < 0.15:
        prelim_side = "NONE"

    side = prelim_side

    # Rank (use prelim scores before final side override)
    if side != "NONE":
        if (
            setup_quality_score >= 75
            and entry_quality_score >= 65
            and direction_confidence >= 65
            and risk_penalty_score < 60
            and rr >= 1.5
        ):
            rank = "A"
        elif (
            setup_quality_score >= 60
            and entry_quality_score >= 50
            and direction_confidence >= 50
            and rr >= 1.5
        ):
            rank = "B"
        else:
            side = "NONE"
            rank = "NO_TRADE"
    else:
        rank = "NO_TRADE"

    # Re-compute entry/sl/tp with final side
    if side == "LONG":
        entry_low = round(close - 0.30 * atr, 5)
        entry_high = round(close + 0.10 * atr, 5)
        sl_base = close - 1.2 * atr
        sl_candidate = (low20 - 0.1 * atr) if not np.isnan(low20) else sl_base
        sl = round(min(sl_base, sl_candidate), 5)
        entry_mid = (entry_low + entry_high) / 2
        risk = abs(entry_mid - sl)
        tp1 = round(entry_mid + 1.5 * risk, 5) if risk > 0 else np.nan
        tp2 = round(entry_mid + 2.5 * risk, 5) if risk > 0 else np.nan
        rr = round(1.5, 2)  # by design
        invalidation = "Close below SL or loss of MA20 support"
        verification_target = "TP1 then TP2 from next sessions"
    elif side == "SHORT":
        entry_low = round(close - 0.10 * atr, 5)
        entry_high = round(close + 0.30 * atr, 5)
        sl_base = close + 1.2 * atr
        sl_candidate = (high20 + 0.1 * atr) if not np.isnan(high20) else sl_base
        sl = round(max(sl_base, sl_candidate), 5)
        entry_mid = (entry_low + entry_high) / 2
        risk = abs(sl - entry_mid)
        tp1 = round(entry_mid - 1.5 * risk, 5) if risk > 0 else np.nan
        tp2 = round(entry_mid - 2.5 * risk, 5) if risk > 0 else np.nan
        rr = round(1.5, 2)
        invalidation = "Close above SL or recovery above MA20"
        verification_target = "TP1 then TP2 from next sessions"
    else:
        entry_low = entry_high = sl = tp1 = tp2 = np.nan
        entry_mid = close
        risk = 0.0
        rr = 0.0
        invalidation = "No actionable setup"
        verification_target = "Wait for trend and risk conditions to align"

    sl_dist = abs(close - sl) if not np.isnan(sl) else 0.0

    # Recalc quality scores with final side
    # Use the original prelim_side direction for confidence even if rank degraded to NO_TRADE.
    _effective_side = side if side != "NONE" else prelim_side
    risk_penalty_score = calc_risk_penalty(rsi, side, atr_pct60, dist_ma20, rr)
    entry_quality_score = calc_entry_quality(atr, sl_dist, rr, dist_ma20)
    direction_confidence = calc_direction_confidence(trend_score, momentum_score, _effective_side)

    # ── Regime ─────────────────────────────────────────────────────────────
    if not np.isnan(ma20) and not np.isnan(ma50):
        if close > ma20 > ma50:
            regime = "UPTREND"
        elif close < ma20 < ma50:
            regime = "DOWNTREND"
        else:
            regime = "RANGE"
    else:
        regime = "UNKNOWN"

    # ── Reason codes / no-trade reason ────────────────────────────────────
    reason_codes_list = build_reason_codes(
        close, ma20, ma50, ma20_slope, rsi, atr_pct60,
        chg5d, breakout_up, breakout_down, rr, dist_ma20, rng_pos,
        risk_penalty_score,
    )
    reason_codes_str = "|".join(reason_codes_list) if reason_codes_list else ""

    no_trade_reason = ""
    if side == "NONE" or rank == "NO_TRADE":
        no_trade_reason = build_no_trade_reason(
            trend_score, risk_penalty_score, atr_pct60, rr, rng_pos, rsi,
            side, data_quality,
        )

    # ── Signal type ────────────────────────────────────────────────────────
    signal_type = decide_signal_type(
        side, rank, trend_score, momentum_score,
        breakout_up, breakout_down, dist_ma20,
    )

    # ── Recommended action ────────────────────────────────────────────────
    if rank == "A":
        recommended_action = "TRADE"
    elif rank == "B":
        recommended_action = "WATCH"
    else:
        recommended_action = "NO_TRADE"

    # ── signal_strength ──────────────────────────────────────────────────
    signal_strength = round(
        (setup_quality_score * 0.5 + direction_confidence * 0.3 + entry_quality_score * 0.2),
        2,
    ) if side != "NONE" else 0.0

    # ── Legacy score fields (maintained for backward compat) ──────────────
    extension = abs(close - ma20) / atr if not np.isnan(ma20) else 1.0
    volatility_raw = atr / close
    ems = clamp(50 + dist_ma50 * 8) if not np.isnan(dist_ma50) else 50.0
    ffs = clamp(50 + abs(chg5d) * 500)
    cds = clamp(100 - extension * 18)
    ias = clamp(70 - abs(rsi - 50) * 1.2) if not np.isnan(rsi) else 50.0
    cbs = clamp(65 if ((side == "LONG" and chg1d > 0) or (side == "SHORT" and chg1d < 0)) else 45)
    mes = clamp(75 - volatility_raw * 1200)
    tq_score = round((ems * 0.25) + (ffs * 0.15) + (cds * 0.2) + (ias * 0.15) + (cbs * 0.1) + (mes * 0.15), 2)
    no_trade_score = round(clamp(100 - tq_score + (25 if side == "NONE" else 0)), 2)
    opp_score = round(50 - abs(trend_score - 50), 2)  # how much opportunity the 'other side' shows

    win_prob = 0.0 if side == "NONE" else round(min(0.68, max(0.42, 0.42 + tq_score / 400)), 3)
    expected_r = round((win_prob * rr) - (1 - win_prob), 3) if side != "NONE" else 0.0
    risk_pct = 1.0 if rank == "A" else 0.5 if rank == "B" else 0.0

    # ── signal_id ─────────────────────────────────────────────────────────
    signal_id = f"{date_id}_{asset}_{side}_{signal_type}"

    # ── Assemble final row ────────────────────────────────────────────────
    row: dict[str, Any] = {
        "date": latest_date,
        "signal_id": signal_id,
        "asset": asset,
        "side": side,
        "rank": rank,
        "type": signal_type,
        "entry_low": entry_low,
        "entry_high": entry_high,
        "sl": sl,
        "tp1": tp1,
        "tp2": tp2,
        "rr": rr,
        "win_prob": win_prob,
        "expected_r": expected_r,
        "tq_score": tq_score,
        "opp_score": opp_score,
        "no_trade_score": no_trade_score,
        "risk_pct": risk_pct,
        "regime": regime,
        "ems": round(ems, 2),
        "ffs": round(ffs, 2),
        "cds": round(cds, 2),
        "ias": round(ias, 2),
        "cbs": round(cbs, 2),
        "mes": round(mes, 2),
        "invalidation": invalidation,
        "verification_target": verification_target,
        # Phase-6
        "trend_score": round(trend_score, 2),
        "momentum_score": round(momentum_score, 2),
        "volatility_score": round(volatility_score, 2),
        "risk_penalty_score": round(risk_penalty_score, 2),
        "setup_quality_score": round(setup_quality_score, 2),
        "entry_quality_score": round(entry_quality_score, 2),
        "direction_confidence": round(direction_confidence, 2),
        "reason_codes": reason_codes_str,
        "no_trade_reason": no_trade_reason,
        "signal_strength": signal_strength,
        "recommended_action": recommended_action,
        "data_quality": data_quality,
    }
    return {col: row.get(col) for col in SIGNAL_COLUMNS}


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []

    for path in sorted(RAW_DIR.glob("*.csv")):
        try:
            df = load_ohlcv(path)
            if df.empty:
                continue
            rows.append(build_row(path.stem, df))
        except Exception as exc:  # noqa: BLE001 - one bad asset should not stop others.
            print(f"signal error: {path.name} {exc}")

    signals = pd.DataFrame(rows, columns=SIGNAL_COLUMNS)
    signals.to_csv(RESULTS_DIR / "signals.csv", index=False)
    signals.to_json(RESULTS_DIR / "signals.json", orient="records", indent=2, force_ascii=False)
    print(f"signals generated: {len(signals)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
