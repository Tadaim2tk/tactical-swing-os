from __future__ import annotations

from datetime import datetime
import json

import numpy as np
import pandas as pd

import build_ai_feedback
import score_narratives as narratives
from time_utils import UTC, format_jst, format_utc


def market(rows):
    return pd.DataFrame(rows)


def signals(asset: str, side: str):
    return pd.DataFrame(
        [
            {
                "signal_id": f"test_{asset}_{side}",
                "asset": asset,
                "side": side,
                "rank": "B",
                "recommended_action": "TRADE",
                "reason_codes": "test",
            }
        ]
    )


def alignment_for(market_rows, asset, side):
    scores = narratives.score_market_narratives(market(market_rows))
    aligned = narratives.evaluate_signal_alignment(signals(asset, side), scores)
    return aligned.iloc[0].to_dict()


def test_btc_long_risk_on_aligned():
    row = alignment_for(
        [
            {"asset": "BTC", "open": 100, "close": 110},
            {"asset": "NASDAQ", "open": 100, "close": 104},
            {"asset": "DXY", "open": 100, "close": 96},
            {"asset": "VIX", "open": 20, "close": 17},
            {"asset": "SPX", "open": 100, "close": 103},
            {"asset": "GOLD", "open": 100, "close": 99},
            {"asset": "USDJPY", "open": 100, "close": 99},
            {"asset": "US10Y", "open": 4, "close": 3.9},
            {"asset": "WTI", "open": 70, "close": 71},
        ],
        "BTC",
        "LONG",
    )
    assert row["narrative_alignment"] == "aligned"


def test_btc_long_risk_off_conflicted():
    row = alignment_for(
        [
            {"asset": "BTC", "open": 100, "close": 90},
            {"asset": "NASDAQ", "open": 100, "close": 95},
            {"asset": "DXY", "open": 100, "close": 104},
            {"asset": "VIX", "open": 20, "close": 25},
            {"asset": "SPX", "open": 100, "close": 96},
            {"asset": "GOLD", "open": 100, "close": 103},
            {"asset": "USDJPY", "open": 100, "close": 102},
            {"asset": "US10Y", "open": 4, "close": 4.2},
            {"asset": "WTI", "open": 70, "close": 69},
        ],
        "BTC",
        "LONG",
    )
    assert row["narrative_alignment"] == "conflicted"


def test_gold_long_risk_off_aligned():
    row = alignment_for(
        [
            {"asset": "GOLD", "open": 100, "close": 106},
            {"asset": "VIX", "open": 20, "close": 24},
            {"asset": "SPX", "open": 100, "close": 96},
            {"asset": "NASDAQ", "open": 100, "close": 95},
            {"asset": "DXY", "open": 100, "close": 99},
            {"asset": "BTC", "open": 100, "close": 97},
            {"asset": "USDJPY", "open": 100, "close": 99},
            {"asset": "US10Y", "open": 4, "close": 3.9},
            {"asset": "WTI", "open": 70, "close": 69},
        ],
        "GOLD",
        "LONG",
    )
    assert row["narrative_alignment"] == "aligned"


def test_gold_long_rate_and_dollar_conflicted():
    row = alignment_for(
        [
            {"asset": "GOLD", "open": 100, "close": 96},
            {"asset": "DXY", "open": 100, "close": 106},
            {"asset": "US10Y", "open": 4, "close": 4.4},
            {"asset": "VIX", "open": 20, "close": 19},
            {"asset": "SPX", "open": 100, "close": 101},
            {"asset": "NASDAQ", "open": 100, "close": 99},
            {"asset": "BTC", "open": 100, "close": 99},
            {"asset": "USDJPY", "open": 100, "close": 103},
            {"asset": "WTI", "open": 70, "close": 69},
        ],
        "GOLD",
        "LONG",
    )
    assert row["narrative_alignment"] == "conflicted"


def test_insufficient_data_and_no_auto_apply():
    scores = narratives.score_market_narratives(pd.DataFrame())
    aligned = narratives.evaluate_signal_alignment(signals("BTC", "LONG"), scores)
    assert aligned.iloc[0]["narrative_alignment"] == "insufficient_data"


def test_jst_time_display_is_utc_plus_nine_hours():
    utc_dt = datetime(2026, 6, 7, 11, 49, 53, tzinfo=UTC)

    assert format_utc(utc_dt) == "2026-06-07 11:49:53 UTC"
    assert format_jst(utc_dt) == "2026-06-07 20:49:53 JST"
    assert "JST" in format_jst(utc_dt)


def test_safe_json_dumps_handles_pandas_numpy_datetime_and_nan():
    payload = {
        "timestamp": pd.Timestamp("2026-06-07 07:00:00"),
        "datetime": datetime(2026, 6, 7, 7, 0, 0),
        "np_float": np.float64(1.25),
        "np_int": np.int64(7),
        "np_bool": np.bool_(True),
        "nan": np.nan,
        "nat": pd.NaT,
        "series": pd.Series({"a": np.float64(2.5), "b": np.nan}),
    }
    dumped = build_ai_feedback.safe_json_dumps(payload)
    loaded = json.loads(dumped)
    assert loaded["timestamp"] == "2026-06-07T07:00:00"
    assert loaded["datetime"] == "2026-06-07T07:00:00"
    assert loaded["np_float"] == 1.25
    assert loaded["np_int"] == 7
    assert loaded["np_bool"] is True
    assert loaded["nan"] is None
    assert loaded["nat"] is None
    assert loaded["series"]["b"] is None


def test_build_report_handles_non_json_values_in_payload_sections():
    scores = pd.DataFrame(
        [
            {
                "asset": "GLOBAL",
                "risk_on_score": np.float64(60.0),
                "risk_off_score": np.float64(40.0),
                "dollar_strength_score": np.float64(45.0),
                "rate_pressure_score": np.float64(50.0),
                "gold_safe_haven_score": np.float64(42.0),
                "crypto_liquidity_score": np.float64(61.0),
                "volatility_stress_score": np.float64(38.0),
                "narrative_confidence": np.float64(95.0),
            }
        ]
    )
    alignment = pd.DataFrame(
        [
            {
                "signal_id": "x",
                "asset": "BTC",
                "side": "LONG",
                "rank": "B",
                "recommended_action": "TRADE",
                "reason_codes": "test",
                "narrative_alignment": "aligned",
                "narrative_alignment_score": np.int64(31),
                "narrative_comment": "テスト",
            }
        ]
    )
    feedback_rows = pd.DataFrame(
        [
            {
                "generated_at": pd.Timestamp("2026-06-07"),
                "date": "2026-06-07",
                "asset": "BTC",
                "signal_id": "x",
                "apply_automatically": np.bool_(False),
            }
        ]
    )
    markdown = build_ai_feedback.build_report(
        "2026-06-07T07:00:00",
        "2026-06-07",
        "Google Sheets",
        scores,
        alignment,
        feedback_rows,
        [{"signal_id": "x", "r_multiple": np.float64(1.0), "checked_at": pd.Timestamp("2026-06-07")}],
        ["BTCのLONGはリスクオン時に監視強化。"],
        [{"proposal_id": "p", "apply_automatically": np.bool_(False)}],
    )
    assert "AI_FEEDBACK_LOG JSON" in markdown
    assert "2026-06-07T00:00:00" in markdown


def test_recent_evaluation_reflection_dedupes_alignment_signal_id_by_latest_date():
    evaluations = pd.DataFrame(
        [
            {
                "signal_id": "dup-signal",
                "asset": "BTC",
                "outcome": "win_tp1",
                "r_multiple": 1.2,
                "evaluation_date": "2026-06-07",
            }
        ]
    )
    alignment = pd.DataFrame(
        [
            {
                "signal_id": "",
                "evaluation_date": "2026-06-09",
                "narrative_alignment": "conflicted",
            },
            {
                "signal_id": "dup-signal",
                "evaluation_date": "2026-06-06",
                "narrative_alignment": "conflicted",
            },
            {
                "signal_id": "dup-signal",
                "evaluation_date": "2026-06-08",
                "narrative_alignment": "aligned",
            },
        ]
    )

    reflections = build_ai_feedback.recent_evaluation_reflection(evaluations, alignment)

    assert reflections[0]["signal_id"] == "dup-signal"
    assert reflections[0]["narrative_alignment"] == "aligned"


def test_dedupe_by_signal_id_uses_row_order_when_date_columns_are_missing():
    duplicated = pd.DataFrame(
        [
            {"signal_id": "x", "narrative_alignment": "conflicted"},
            {"signal_id": " ", "narrative_alignment": "neutral"},
            {"signal_id": "x", "narrative_alignment": "aligned"},
        ]
    )

    deduped = build_ai_feedback.dedupe_by_signal_id(duplicated, "alignment")

    assert len(deduped) == 1
    assert deduped.iloc[0]["signal_id"] == "x"
    assert deduped.iloc[0]["narrative_alignment"] == "aligned"
