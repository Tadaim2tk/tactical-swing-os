from __future__ import annotations

import pandas as pd

import classify_news_narratives as cnn
import fetch_news


def classify_one(title: str):
    df = pd.DataFrame([{"title": title, "summary": "", "matched_assets": fetch_news.matched_assets_for(title, "")}])
    return cnn.classify_rows(df)


def test_bitcoin_etf_inflows_maps_to_btc_and_crypto_liquidity():
    title = "bitcoin ETF inflows boost crypto rally"
    scores, drivers = classify_one(title)
    assert "BTC" in fetch_news.matched_assets_for(title, "")
    assert scores["crypto_liquidity_news_score"] > 0
    assert drivers


def test_gold_geopolitical_tensions_maps_to_gold_and_risk():
    title = "gold rises as geopolitical tensions intensify"
    scores, _ = classify_one(title)
    assert "GOLD" in fetch_news.matched_assets_for(title, "")
    assert scores["gold_safe_haven_news_score"] > 0
    assert scores["geopolitical_risk_news_score"] > 0


def test_oil_opec_supply_disruption_maps_to_wti():
    title = "oil jumps after OPEC supply disruption"
    scores, _ = classify_one(title)
    assert "WTI" in fetch_news.matched_assets_for(title, "")
    assert scores["oil_supply_risk_news_score"] > 0


def test_dollar_yields_headline_scores_dollar_and_rates():
    title = "dollar strengthens as yields rise"
    scores, _ = classify_one(title)
    assets = fetch_news.matched_assets_for(title, "")
    assert "DXY" in assets
    assert "USDJPY" in assets
    assert scores["dollar_strength_news_score"] > 0
    assert scores["rate_pressure_news_score"] > 0


def test_empty_news_produces_zero_scores():
    scores, drivers = cnn.classify_rows(pd.DataFrame())
    assert scores["news_confidence"] == 0
    assert drivers == []
