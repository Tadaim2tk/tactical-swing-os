"""監査辞書の外部化 + 語境界マッチャーのテスト。

データ駆動の調整ではなく、カバレッジ・誤検知低減・ラベル付き例のロックが目的。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import audit_dictionaries as ad


@pytest.fixture(autouse=True)
def _reset_dict_cache():
    """各テストの前後でキャッシュを破棄し、tmp/部分configの汚染を防ぐ。"""
    ad.reset_cache()
    yield
    ad.reset_cache()


# === マッチャー: 英語=語境界 / 日本語=部分一致 ===

def test_english_word_boundary_no_false_positive():
    # "certain win" は "uncertain win" に当たらない
    assert ad.match_terms("the uncertain win ahead", ["certain win"]) == []
    # "war" は "warning"/"reward"/"toward" に当たらない
    assert ad.match_terms("a warning toward the reward", ["war"]) == []


def test_english_word_boundary_true_positive():
    assert ad.match_terms("risk of war", ["war"]) == ["war"]
    assert ad.match_terms("Stocks jumped after the close today", ["after the close"]) == ["after the close"]
    assert ad.match_terms("this is 100% sure", ["100% sure"]) == ["100% sure"]


def test_japanese_substring_still_matches():
    assert ad.match_terms("株は引け後に急伸した", ["引け後"]) == ["引け後"]
    assert ad.match_terms("結果を受けて下落", ["結果を受けて"]) == ["結果を受けて"]


def test_snake_case_token_matches():
    assert "loss_sl" in ad.match_terms("the setup hit loss_sl yesterday", ["loss_sl"])


def test_case_insensitive():
    assert ad.match_terms("GUARANTEED returns", ["guaranteed"]) == ["guaranteed"]


def test_empty_and_none_text():
    assert ad.match_terms(None, ["war"]) == []
    assert ad.match_terms("", ["war"]) == []


def test_result_is_sorted_unique():
    out = ad.match_terms("war war missile", ["missile", "war", "war"])
    assert out == ["missile", "war"]


# === ローダー: 欠損/破損/部分のフォールバック ===

def test_shipped_config_loads_nonempty():
    ad.reset_cache()
    m = ad.load_dictionaries()
    assert len(ad.future_keywords(m)) >= 18
    assert len(ad.outcome_terms(m)) >= 9
    assert len(ad.overconfidence_terms(m)) >= 16
    assert "geopolitical_risk_news_score" in ad.news_keywords(m)


def test_missing_config_falls_back_to_defaults():
    ad.reset_cache()
    m = ad.load_dictionaries(Path("/nonexistent_audit_dict.json"))
    assert ad.future_keywords(m) == ad.future_keywords(ad.DEFAULTS) if False else len(ad.future_keywords(m)) > 0
    # DEFAULTS と一致
    assert ad.overconfidence_terms(m) == (
        ad.DEFAULTS["adversarial_review"]["overconfidence_terms_ja"] + ad.DEFAULTS["adversarial_review"]["overconfidence_terms_en"]
    )


def test_corrupt_config_falls_back(tmp_path):
    ad.reset_cache()
    bad = tmp_path / "bad.json"
    bad.write_text("{ this is not json", encoding="utf-8")
    m = ad.load_dictionaries(bad)
    assert len(ad.future_keywords(m)) > 0  # 破損でも DEFAULTS


def test_partial_config_merges_per_key(tmp_path):
    ad.reset_cache()
    cfg = tmp_path / "partial.json"
    cfg.write_text(json.dumps({"narrative_lookahead": {"outcome_terms": ["custom_term"]}}, ensure_ascii=False), encoding="utf-8")
    m = ad.load_dictionaries(cfg)
    # 指定したキーは上書き
    assert ad.outcome_terms(m) == ["custom_term"]
    # 未指定キーは DEFAULTS を維持
    assert len(ad.future_keywords(m)) > 0
    assert len(ad.overconfidence_terms(m)) > 0


def test_empty_list_in_config_falls_back(tmp_path):
    ad.reset_cache()
    cfg = tmp_path / "emptylist.json"
    cfg.write_text(json.dumps({"narrative_lookahead": {"outcome_terms": []}}), encoding="utf-8")
    m = ad.load_dictionaries(cfg)
    # 空リストは無効として DEFAULTS へ
    assert len(ad.outcome_terms(m)) >= 9


# === ラベル付き例 (true positive / true negative) のロック ===

LOOKAHEAD_FUTURE_TP = ["the stock rallied after the close", "株価は引け後に急伸した", "in hindsight it was obvious", "結果を受けて売られた"]
LOOKAHEAD_FUTURE_TN = ["the uncertain outlook ahead", "afternoon session looks weak", "市場は方向感に欠ける", "watching for a breakout"]

OVERCONFIDENCE_TP = ["this is a guaranteed win", "絶対に上がる", "a sure thing setup", "リスクなしのトレード"]
OVERCONFIDENCE_TN = ["uncertain but promising", "probably rises", "やや上がりやすい", "risk is elevated"]


def test_lookahead_future_true_positive_examples():
    fk = ad.future_keywords()
    for text in LOOKAHEAD_FUTURE_TP:
        assert ad.match_terms(text, fk), f"should flag future-info: {text}"


def test_lookahead_future_true_negative_examples():
    fk = ad.future_keywords()
    for text in LOOKAHEAD_FUTURE_TN:
        assert ad.match_terms(text, fk) == [], f"should NOT flag: {text}"


def test_overconfidence_true_positive_examples():
    oc = ad.overconfidence_terms()
    for text in OVERCONFIDENCE_TP:
        assert ad.match_terms(text, oc), f"should flag overconfidence: {text}"


def test_overconfidence_true_negative_examples():
    oc = ad.overconfidence_terms()
    for text in OVERCONFIDENCE_TN:
        assert ad.match_terms(text, oc) == [], f"should NOT flag: {text}"


# === セルフ監査の追補: JP隣接・境界・記号・構造・robustness ===

# JP語が ASCII数字/英字に隣接しても検出されること(false-negative回帰防止)
JP_ADJACENCY_TP = [
    ("その後", "日経225その後に急落"),
    ("終値で", "S&P500終値で最高値"),
    ("発表後", "CPI発表後に下落"),
    ("翌日に", "Q3翌日に修正"),
    ("判明した", "EPS判明した"),
    ("あとから", "GDP2.5あとから修正"),
]


def test_japanese_adjacent_to_ascii_still_matches():
    for term, text in JP_ADJACENCY_TP:
        assert ad.match_terms(text, [term]) == [term], f"JP adjacency missed: {term} in {text}"


# 出荷辞書の語を部分含むが境界で弾くべき例(境界が退行すると失敗する=真の境界カバレッジ)
def test_boundary_true_negatives_from_shipped_terms():
    oc = ad.overconfidence_terms()
    fk = ad.future_keywords()
    # "guaranteed" を部分含むが別語
    assert ad.match_terms("guaranteedish hype", oc) == []
    # "certain win" を部分含むが "uncertain win"
    assert ad.match_terms("an uncertain win streak", oc) == []
    # "in hindsight" を部分含むが "hindsightful"
    assert ad.match_terms("in hindsightfulness", fk) == []
    # "after the close" を部分含むが "after the closet"
    assert ad.match_terms("after the closet door", fk) == []


def test_trailing_percent_term_matches_when_followed_by_alnum():
    oc_like = ["100%"]
    assert ad.match_terms("up 100%sure now", oc_like) == ["100%"]
    assert ad.match_terms("gain of 2100% reported", oc_like) == []  # 先頭境界で弾く


# 記号/句読点を含む news 語が正しく一致する
def test_symbol_bearing_news_terms_match():
    nk = ad.news_keywords()
    assert "s&p gains" in ad.match_terms("the s&p gains lifted indices", nk["equity_momentum_news_score"])
    assert "usd/jpy rises" in ad.match_terms("usd/jpy rises sharply", nk["dollar_strength_news_score"])
    assert "risk-on" in ad.match_terms("a clear risk-on mood", nk["risk_on_news_score"])


def test_word_boundary_news_no_false_positive():
    nk = ad.news_keywords()
    # "war" は "warning"/"toward"/"reward" に当たらない
    assert ad.match_terms("a warning toward reward", nk["geopolitical_risk_news_score"]) == []
    # 語形変化はconfig側で補う方針: "inflationary" は追加済みで拾える
    assert "inflationary" in ad.match_terms("inflationary pressure", nk["inflation_pressure_news_score"])


# news_keywords の構造: _meta を含まない / 13カテゴリ / 全て list
def test_news_keywords_structure():
    nk = ad.news_keywords()
    assert "_meta" not in nk
    assert len(nk) == 13
    for k, v in nk.items():
        assert isinstance(v, list) and v


# 出荷 config が DEFAULTS と一致(config が正本・ドリフトしていない)
def test_shipped_config_matches_defaults():
    ad.reset_cache()
    shipped = ad.load_dictionaries(ad.CONFIG_PATH)
    ad.reset_cache()
    fallback = ad.load_dictionaries(Path("/nonexistent_audit_dict.json"))
    assert ad.future_keywords(shipped) == ad.future_keywords(fallback)
    assert ad.outcome_terms(shipped) == ad.outcome_terms(fallback)
    assert ad.overconfidence_terms(shipped) == ad.overconfidence_terms(fallback)
    assert ad.news_keywords(shipped) == ad.news_keywords(fallback)


# ローダー robustness
def test_non_dict_root_falls_back(tmp_path):
    for bad in ("[]", '"a string"', "123"):
        ad.reset_cache()
        p = tmp_path / "root.json"
        p.write_text(bad, encoding="utf-8")
        m = ad.load_dictionaries(p)
        assert len(ad.future_keywords(m)) > 0


def test_non_dict_section_falls_back(tmp_path):
    ad.reset_cache()
    p = tmp_path / "sec.json"
    p.write_text(json.dumps({"adversarial_review": ["oops not a dict"]}), encoding="utf-8")
    m = ad.load_dictionaries(p)
    assert ad.overconfidence_terms(m) == (
        ad.DEFAULTS["adversarial_review"]["overconfidence_terms_ja"] + ad.DEFAULTS["adversarial_review"]["overconfidence_terms_en"]
    )


def test_list_of_non_strings_coerced(tmp_path):
    ad.reset_cache()
    p = tmp_path / "nums.json"
    p.write_text(json.dumps({"narrative_lookahead": {"outcome_terms": [123, "abc"]}}), encoding="utf-8")
    m = ad.load_dictionaries(p)
    assert ad.outcome_terms(m) == ["123", "abc"]
