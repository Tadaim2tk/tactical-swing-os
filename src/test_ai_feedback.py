from __future__ import annotations

import pandas as pd

import score_narratives as narratives


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
