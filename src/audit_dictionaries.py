"""監査辞書の単一情報源 (Phase: Dictionary Externalization)。

Narrative Lookahead / Adversarial Review / News Narrative が使う語彙辞書を
config/audit_dictionaries.json へ外部化し、共通のマッチャーを提供する。

設計:
- config 欠損/破損時は組み込み DEFAULTS へ安全にフォールバック(挙動を壊さない)。
- マッチャーは英語(ASCII)語を**語境界**で照合し false positive を減らす
  ("certain win" は "uncertain win" に当たらない)。日本語は語境界が無いため
  実質的に部分一致になる(ASCII以外の前後文字は語境界条件を常に満たす)。
- データ駆動の重み調整ではない。カバレッジ拡充・誤検知低減・例ロックが目的。
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

CONFIG_PATH = Path("config/audit_dictionaries.json")

# === 組み込み DEFAULTS (config 欠損時の安全フォールバック / config の正本) ===
DEFAULTS: dict[str, Any] = {
    "narrative_lookahead": {
        # 結果判明後でないと書けない未来情報表現
        "future_keywords_en": [
            "after the close", "later today", "following the release", "confirmed after",
            "earnings beat after", "post-market", "tomorrow's data showed", "revised higher after",
            "the market reacted after", "as it turned out", "in hindsight", "in retrospect",
            "closed higher", "closed lower", "ended up", "finished the day", "later confirmed",
            "data later showed", "rallied after", "fell after",
        ],
        "future_keywords_ja": [
            "引け後", "発表後", "後に判明", "翌日に", "その後", "結果を受けて", "確定後", "改定後",
            "市場は反応した", "終値で", "結果的に", "事後的に", "後場", "判明した", "振り返ると",
            "終わってみれば", "あとから",
        ],
        # 評価結果を示す語 (事前ナラティブに混入していないか)
        "outcome_terms": [
            "outcome", "r_multiple", "r_result", "r_result_net", "net_r", "gross_r",
            "win_tp1", "win_tp2", "loss_sl", "missed_opportunity", "evaluation_status",
            "hit_level", "tp1_hit", "tp2_hit", "sl_hit", "bars_held",
        ],
    },
    "adversarial_review": {
        "overconfidence_terms_ja": [
            "確実", "必ず", "絶対", "間違いない", "リスクなし", "リスクゼロ", "鉄板", "100%",
            "確実に儲か", "勝ち確", "負けるわけがない", "ノーリスク", "確実に利益", "100%勝てる",
            "間違いなく上がる", "鉄板銘柄",
        ],
        "overconfidence_terms_en": [
            "guaranteed", "certain win", "no risk", "risk-free", "riskless", "always wins",
            "surefire", "can't lose", "100% sure", "can't miss", "cannot lose", "sure thing",
            "zero risk", "guaranteed profit", "slam dunk", "free money",
        ],
    },
    "news_narrative": {
        "risk_on_news_score": ["rally", "rebound", "risk-on", "optimism", "soft landing", "rate cut hopes", "earnings beat", "tech gains", "stocks rise"],
        "risk_off_news_score": ["selloff", "slump", "risk-off", "fear", "uncertainty", "recession", "crisis", "safe haven", "stocks fall"],
        "dollar_strength_news_score": ["dollar rises", "dollar strengthens", "greenback gains", "yen weakens", "usd/jpy rises", "stronger dollar"],
        "rate_pressure_news_score": ["yields rise", "treasury yields climb", "hawkish fed", "sticky inflation", "higher for longer", "rate hike", "bond yields"],
        "gold_safe_haven_news_score": ["gold rises", "safe haven", "geopolitical tensions", "war", "conflict", "central bank buying", "inflation hedge"],
        "oil_supply_risk_news_score": ["oil rises", "crude jumps", "supply disruption", "opec", "middle east", "sanctions", "tanker", "inventory draw", "refinery outage"],
        "crypto_liquidity_news_score": ["bitcoin rises", "crypto rally", "etf inflows", "risk appetite", "liquidity", "rate cut", "dollar falls", "bitcoin etf"],
        "equity_momentum_news_score": ["stocks rise", "s&p gains", "nasdaq climbs", "tech gains", "earnings beat", "wall street rises"],
        "geopolitical_risk_news_score": ["war", "missile", "attack", "sanctions", "middle east", "russia", "ukraine", "taiwan", "china tensions", "geopolitical tensions"],
        "inflation_pressure_news_score": ["inflation", "inflationary", "cpi", "pce", "prices rise", "tariff", "wages", "energy prices"],
        "recession_risk_news_score": ["recession", "recessionary", "slowdown", "contraction", "jobless", "defaults", "weak demand"],
        "central_bank_hawkish_score": ["fed hawkish", "rate hike", "higher for longer", "boj hike", "ecb hawkish", "powell warns"],
        "central_bank_dovish_score": ["rate cut", "dovish", "easing", "stimulus", "pivot", "fed cuts"],
    },
}

_cache: dict[str, Any] | None = None


def load_dictionaries(path: Path = CONFIG_PATH) -> dict[str, Any]:
    """辞書を読み込む。欠損/破損時は DEFAULTS。トップレベルキー単位で DEFAULTS へマージ。"""
    global _cache
    if _cache is not None:
        return _cache
    data: dict[str, Any] = {}
    if path.exists():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                data = loaded
        except (json.JSONDecodeError, OSError):
            data = {}
    merged: dict[str, Any] = {}
    for top, default_section in DEFAULTS.items():
        section = data.get(top)
        if not isinstance(section, dict):
            merged[top] = default_section
            continue
        merged_section = dict(default_section)
        for key, default_list in default_section.items():
            val = section.get(key)
            merged_section[key] = val if isinstance(val, list) and val else default_list
        merged[top] = merged_section
    _cache = merged
    return merged


def reset_cache() -> None:
    global _cache
    _cache = None


def _list(top: str, key: str, model: dict[str, Any] | None = None) -> list[str]:
    model = model or load_dictionaries()
    section = model.get(top) or {}
    val = section.get(key)
    return [str(x) for x in val] if isinstance(val, list) else []


# --- 取得API ---

def future_keywords(model: dict[str, Any] | None = None) -> list[str]:
    return _list("narrative_lookahead", "future_keywords_en", model) + _list("narrative_lookahead", "future_keywords_ja", model)


def outcome_terms(model: dict[str, Any] | None = None) -> list[str]:
    return _list("narrative_lookahead", "outcome_terms", model)


def overconfidence_terms(model: dict[str, Any] | None = None) -> list[str]:
    return _list("adversarial_review", "overconfidence_terms_ja", model) + _list("adversarial_review", "overconfidence_terms_en", model)


def news_keywords(model: dict[str, Any] | None = None) -> dict[str, list[str]]:
    model = model or load_dictionaries()
    section = model.get("news_narrative") or {}
    return {k: [str(x) for x in v] for k, v in section.items() if isinstance(v, list)}


# === マッチャー (英語=語境界 / 日本語=部分一致) ===

def _term_pattern(term: str) -> "re.Pattern[str]":
    """語の前後に英数字境界を**条件付き**で課す。

    境界は「語が ASCII英数字で始まる/終わる」端にのみ適用する。これにより:
    - 英語語は語境界マッチ("certain win" は "uncertain win" に当たらない)。
    - 日本語語(端が非ASCII)や記号終端語("100%")は ASCII隣接でも部分一致になり、
      "日経225発表後" の「発表後」のような mixed JP/EN を取りこぼさない。
    """
    tl = term.lower()
    esc = re.escape(tl)
    pre = r"(?<![a-z0-9])" if (tl[:1].isascii() and tl[:1].isalnum()) else ""
    suf = r"(?![a-z0-9])" if (tl[-1:].isascii() and tl[-1:].isalnum()) else ""
    return re.compile(pre + esc + suf)


def match_terms(text: Any, terms: list[str]) -> list[str]:
    """text に含まれる terms を返す(条件付き語境界マッチ)。大文字小文字無視。"""
    if not text:
        return []
    low = str(text).lower()
    found = [t for t in terms if t and _term_pattern(t).search(low)]
    return sorted(set(found))
