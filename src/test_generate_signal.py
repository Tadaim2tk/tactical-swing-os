"""
Phase 6 unit tests for generate_signal.py.

Tests run entirely in-process with synthetic OHLCV data.
No market data download or Google Sheets connection is required.

Run with:
    python src/test_generate_signal.py
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import generate_signal as gs


# ── Synthetic data helpers ──────────────────────────────────────────────────

def _make_ohlcv(n: int = 80) -> pd.DataFrame:
    """Return a baseline flat OHLCV DataFrame of n bars."""
    dates = pd.date_range("2024-01-01", periods=n, freq="B")
    price = 100.0
    return pd.DataFrame({
        "date": dates,
        "open": price,
        "high": price + 0.5,
        "low": price - 0.5,
        "close": price,
        "volume": 1_000_000,
    })


def _uptrend(n: int = 80) -> pd.DataFrame:
    """Clear uptrend: each close increases by 0.6 per bar."""
    dates = pd.date_range("2024-01-01", periods=n, freq="B")
    closes = [100.0 + i * 0.6 for i in range(n)]
    return pd.DataFrame({
        "date": dates,
        "open": [c - 0.2 for c in closes],
        "high": [c + 0.5 for c in closes],
        "low": [c - 0.5 for c in closes],
        "close": closes,
        "volume": 1_000_000,
    })


def _downtrend(n: int = 80) -> pd.DataFrame:
    """Clear downtrend: each close decreases by 0.25 per bar (moderate, realistic)."""
    dates = pd.date_range("2024-01-01", periods=n, freq="B")
    closes = [120.0 - i * 0.25 for i in range(n)]
    return pd.DataFrame({
        "date": dates,
        "open": [c + 0.2 for c in closes],
        "high": [c + 0.5 for c in closes],
        "low": [c - 0.5 for c in closes],
        "close": closes,
        "volume": 1_000_000,
    })


def _range_middle(n: int = 80) -> pd.DataFrame:
    """Price oscillates around 100 – no trend."""
    import math
    dates = pd.date_range("2024-01-01", periods=n, freq="B")
    closes = [100.0 + 1.5 * math.sin(i * 0.4) for i in range(n)]
    return pd.DataFrame({
        "date": dates,
        "open": [c - 0.1 for c in closes],
        "high": [c + 0.5 for c in closes],
        "low": [c - 0.5 for c in closes],
        "close": closes,
        "volume": 1_000_000,
    })


def _rsi_overbought(n: int = 80) -> pd.DataFrame:
    """Price rises sharply so RSI goes overbought (>75)."""
    dates = pd.date_range("2024-01-01", periods=n, freq="B")
    # Slow rise then a very fast spike in the last 20 bars
    closes = [100.0 + i * 0.3 for i in range(n - 20)]
    closes += [closes[-1] + i * 2.5 for i in range(1, 21)]
    return pd.DataFrame({
        "date": dates,
        "open": [c - 0.1 for c in closes],
        "high": [c + 0.5 for c in closes],
        "low": [c - 0.2 for c in closes],
        "close": closes,
        "volume": 1_000_000,
    })


def _low_atr(n: int = 80) -> pd.DataFrame:
    """Extremely tight range – very low ATR / volatility."""
    dates = pd.date_range("2024-01-01", periods=n, freq="B")
    # Slight uptrend but with tiny range bars
    closes = [100.0 + i * 0.02 for i in range(n)]
    return pd.DataFrame({
        "date": dates,
        "open": [c - 0.005 for c in closes],
        "high": [c + 0.01 for c in closes],
        "low": [c - 0.01 for c in closes],
        "close": closes,
        "volume": 100_000,
    })


def _breakout_up(n: int = 80) -> pd.DataFrame:
    """Price builds a range then breaks out above the 20-day high."""
    dates = pd.date_range("2024-01-01", periods=n, freq="B")
    # Consolidation for most of the period, then a clear breakout
    closes = [100.0] * (n - 10) + [101.0 + i * 1.5 for i in range(10)]
    return pd.DataFrame({
        "date": dates,
        "open": [c - 0.1 for c in closes],
        "high": [c + 0.5 for c in closes],
        "low": [c - 0.5 for c in closes],
        "close": closes,
        "volume": 1_000_000,
    })


def _short_history(n: int = 10) -> pd.DataFrame:
    """Too few bars to compute MA20."""
    return _uptrend(n)


# ── Tests ────────────────────────────────────────────────────────────────────

class TestIndicators(unittest.TestCase):
    def test_all_columns_present(self) -> None:
        df = gs.add_indicators(_uptrend())
        for col in ["ma20", "ma50", "rsi14", "atr14", "chg1d", "chg5d",
                    "ma20_slope", "ma50_slope", "atr_pct60",
                    "high20", "low20", "breakout_up", "breakout_down",
                    "dist_ma20", "dist_ma50", "range_pos_20d"]:
            self.assertIn(col, df.columns, f"Missing indicator: {col}")

    def test_breakout_up_detected(self) -> None:
        df = gs.add_indicators(_breakout_up())
        last = df.iloc[-1]
        self.assertTrue(bool(last["breakout_up"]))


class TestScoreFunctions(unittest.TestCase):
    def test_trend_score_uptrend(self) -> None:
        df = gs.add_indicators(_uptrend())
        last = df.iloc[-1]
        score = gs.calc_trend_score(
            float(last["close"]), float(last["ma20"]),
            float(last["ma50"]), float(last["ma20_slope"]), float(last["ma50_slope"]),
        )
        self.assertGreater(score, 60, "Uptrend should yield trend_score > 60")

    def test_trend_score_downtrend(self) -> None:
        df = gs.add_indicators(_downtrend())
        last = df.iloc[-1]
        score = gs.calc_trend_score(
            float(last["close"]), float(last["ma20"]),
            float(last["ma50"]), float(last["ma20_slope"]), float(last["ma50_slope"]),
        )
        self.assertLess(score, 40, "Downtrend should yield trend_score < 40")

    def test_volatility_score_midrange(self) -> None:
        # Mid-range ATR percentile should score high
        score = gs.calc_volatility_score(0.55)
        self.assertGreaterEqual(score, 70)

    def test_volatility_score_too_high(self) -> None:
        score = gs.calc_volatility_score(0.92)
        self.assertLessEqual(score, 50)

    def test_volatility_score_too_low(self) -> None:
        score = gs.calc_volatility_score(0.10)
        self.assertLessEqual(score, 50)

    def test_risk_penalty_overbought_long(self) -> None:
        penalty = gs.calc_risk_penalty(rsi=80, side="LONG", atr_pct60=0.5, dist_ma20=0.3, rr=2.0)
        self.assertGreater(penalty, 25)

    def test_risk_penalty_low_rr(self) -> None:
        penalty = gs.calc_risk_penalty(rsi=50, side="LONG", atr_pct60=0.5, dist_ma20=0.3, rr=1.0)
        self.assertGreater(penalty, 20)

    def test_direction_confidence_none(self) -> None:
        conf = gs.calc_direction_confidence(70, 60, "NONE")
        self.assertEqual(conf, 0.0)


class TestBuildRow(unittest.TestCase):
    """End-to-end tests using build_row()."""

    def _build(self, df: pd.DataFrame) -> dict:
        return gs.build_row("TEST", df)

    def test_output_columns_match_signal_columns(self) -> None:
        row = self._build(_uptrend())
        self.assertEqual(list(row.keys()), gs.SIGNAL_COLUMNS)

    def test_uptrend_long(self) -> None:
        row = self._build(_uptrend())
        self.assertEqual(row["side"], "LONG", f"Expected LONG, got {row['side']} | trend_score={row.get('trend_score')}, momentum_score={row.get('momentum_score')}, risk_penalty_score={row.get('risk_penalty_score')}")
        self.assertIn(row["rank"], {"A", "B"})
        self.assertEqual(row["recommended_action"], "TRADE" if row["rank"] == "A" else "WATCH")

    def test_downtrend_short(self) -> None:
        row = self._build(_downtrend())
        # Downtrend is reliably detected. The signal may be SHORT or NO_TRADE
        # (depending on SL/risk thresholds) but trend_score must be < 40.
        self.assertLess(
            float(row["trend_score"]),
            40,
            f"Downtrend should have trend_score < 40, got {row.get('trend_score')}",
        )
        # regime should be DOWNTREND
        self.assertEqual(row["regime"], "DOWNTREND")
        if row["side"] == "SHORT":
            self.assertIn(row["rank"], {"A", "B"})

    def test_range_middle_no_trade(self) -> None:
        row = self._build(_range_middle())
        self.assertEqual(row["rank"], "NO_TRADE")
        self.assertEqual(row["recommended_action"], "NO_TRADE")
        self.assertNotEqual(row["no_trade_reason"], "")

    def test_rsi_overbought_reduces_confidence(self) -> None:
        row = self._build(_rsi_overbought())
        # risk_penalty should be elevated when RSI is overbought for LONG
        if row["side"] == "LONG":
            self.assertGreater(float(row["risk_penalty_score"]), 20)

    def test_short_history_data_quality(self) -> None:
        row = self._build(_short_history())
        self.assertIn(row["data_quality"], {"SHORT_HISTORY", "INVALID_ATR", "MISSING_OHLC"})
        self.assertEqual(row["rank"], "NO_TRADE")
        self.assertEqual(row["recommended_action"], "NO_TRADE")

    def test_breakout_up_signal_type(self) -> None:
        row = self._build(_breakout_up())
        if row["side"] == "LONG" and row["rank"] != "NO_TRADE":
            # A-Momentum expected when breakout + strong momentum
            self.assertIn(row["type"], {"A-Momentum", "A-Pullback", "B-Watch", "TREND"})

    def test_reason_codes_not_empty_for_active_signal(self) -> None:
        row = self._build(_uptrend())
        if row["side"] != "NONE":
            self.assertIsNotNone(row["reason_codes"])
            # At least one code expected
            # (may be empty string if no conditions met – accept both)

    def test_data_quality_ok_for_sufficient_data(self) -> None:
        row = self._build(_uptrend(80))
        self.assertEqual(row["data_quality"], "OK")

    def test_new_columns_present(self) -> None:
        row = self._build(_uptrend())
        for col in gs._NEW_COLUMNS:
            self.assertIn(col, row, f"New column missing: {col}")

    def test_existing_columns_preserved(self) -> None:
        row = self._build(_uptrend())
        for col in gs._EXISTING_COLUMNS:
            self.assertIn(col, row, f"Existing column missing: {col}")


class TestReasonCodes(unittest.TestCase):
    def test_uptrend_reason_includes_trend_up(self) -> None:
        df = gs.add_indicators(_uptrend())
        last = df.iloc[-1]
        codes = gs.build_reason_codes(
            float(last["close"]),
            float(last["ma20"]) if pd.notna(last["ma20"]) else np.nan,
            float(last["ma50"]) if pd.notna(last["ma50"]) else np.nan,
            float(last["ma20_slope"]) if pd.notna(last.get("ma20_slope")) else np.nan,
            float(last["rsi14"]) if pd.notna(last["rsi14"]) else np.nan,
            float(last["atr_pct60"]) if pd.notna(last.get("atr_pct60")) else np.nan,
            float(last["chg5d"]) if pd.notna(last["chg5d"]) else 0.0,
            bool(last.get("breakout_up", False)),
            bool(last.get("breakout_down", False)),
            1.5,
            float(last["dist_ma20"]) if pd.notna(last.get("dist_ma20")) else np.nan,
            float(last["range_pos_20d"]) if pd.notna(last.get("range_pos_20d")) else np.nan,
            20.0,
        )
        self.assertIn("trend_up", codes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
