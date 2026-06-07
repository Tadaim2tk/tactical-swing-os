from __future__ import annotations

import json

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


def test_news_market_bias_risk_on_risk_off_mixed_and_insufficient():
    assert cnn.news_market_bias({"risk_on_news_score": 70, "risk_off_news_score": 20}, 10) == "risk_on"
    assert cnn.news_market_bias({"risk_on_news_score": 20, "risk_off_news_score": 70}, 10) == "risk_off"
    assert cnn.news_market_bias({"risk_on_news_score": 70, "risk_off_news_score": 65}, 10) == "mixed"
    assert cnn.news_market_bias({"risk_on_news_score": 70, "risk_off_news_score": 20}, 3) == "insufficient_data"


def test_driver_tags_for_iran_war_and_inflation_headlines():
    iran_scores, iran_drivers = classify_one("Iran war raises fears of wider Middle East conflict")
    assert iran_scores["geopolitical_risk_news_score"] > 0
    assert "geopolitical_risk" in iran_drivers[0]["driver_tags"]
    assert "地政学リスク" in iran_drivers[0]["driver_summary_ja"]

    inflation_scores, inflation_drivers = classify_one("Inflation inside electronics supply chains keeps prices high")
    assert inflation_scores["inflation_pressure_news_score"] > 0
    assert "inflation_pressure" in inflation_drivers[0]["driver_tags"]
    assert "インフレ圧力" in inflation_drivers[0]["driver_summary_ja"]


def test_fetch_status_metadata_for_partial_failure():
    metadata = {
        "source_total_count": 3,
        "source_success_count": 2,
        "source_failed_count": 1,
        "source_skipped_count": 0,
    }
    assert fetch_news.fetch_status(metadata) == "partial"


def test_fetch_news_global_timeout_skips_remaining_sources(monkeypatch, tmp_path):
    sources = [
        fetch_news.NewsSource("Slow Source", "https://example.com/slow.xml", "macro"),
        fetch_news.NewsSource("Skipped Source", "https://example.com/skipped.xml", "macro"),
    ]

    def fake_load_sources():
        return sources

    def fake_parse_feed(source, fetched_at, hours, timeout_seconds):
        return [], {"source": source.name, "status": "failed", "item_count": 0, "elapsed_seconds": 2.0, "reason": "timeout"}

    monkeypatch.setattr(fetch_news, "load_sources", fake_load_sources)
    monkeypatch.setattr(fetch_news, "parse_feed", fake_parse_feed)
    monkeypatch.setattr(fetch_news, "RESULTS_DIR", tmp_path)
    monkeypatch.setattr(fetch_news, "REPORTS_DIR", tmp_path)
    monkeypatch.setattr(fetch_news.time, "monotonic", iter([0.0, 0.0, 2.0, 2.0]).__next__)

    fetch_news.fetch_news(hours=24, max_items=10, timeout_seconds=1, global_timeout_seconds=1)
    metadata = json.loads((tmp_path / "news_headlines.json").read_text(encoding="utf-8"))["metadata"]

    assert metadata["source_failed_count"] == 1
    assert metadata["source_skipped_count"] == 1
    assert metadata["fetch_status"] == "failed"
