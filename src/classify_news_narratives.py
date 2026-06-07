from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from time_utils import JST, format_jst, format_utc, now_utc


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/news")
HEADLINES_PATH = RESULTS_DIR / "news_headlines.csv"
SCORES_CSV = RESULTS_DIR / "news_narrative_scores.csv"
SCORES_JSON = RESULTS_DIR / "news_narrative_scores.json"
SCORE_COLUMNS = [
    "risk_on_news_score",
    "risk_off_news_score",
    "dollar_strength_news_score",
    "rate_pressure_news_score",
    "gold_safe_haven_news_score",
    "oil_supply_risk_news_score",
    "crypto_liquidity_news_score",
    "equity_momentum_news_score",
    "geopolitical_risk_news_score",
    "inflation_pressure_news_score",
    "recession_risk_news_score",
    "central_bank_hawkish_score",
    "central_bank_dovish_score",
    "news_confidence",
]
THEME_SCORE_COLUMNS = [col for col in SCORE_COLUMNS if col != "news_confidence"]
THEME_LABELS = {
    "risk_on_news_score": "risk_on",
    "risk_off_news_score": "risk_off",
    "dollar_strength_news_score": "dollar_strength",
    "rate_pressure_news_score": "rate_pressure",
    "gold_safe_haven_news_score": "gold_safe_haven",
    "oil_supply_risk_news_score": "oil_supply_risk",
    "crypto_liquidity_news_score": "crypto_liquidity",
    "equity_momentum_news_score": "equity_momentum",
    "geopolitical_risk_news_score": "geopolitical_risk",
    "inflation_pressure_news_score": "inflation_pressure",
    "recession_risk_news_score": "recession_risk",
    "central_bank_hawkish_score": "central_bank_hawkish",
    "central_bank_dovish_score": "central_bank_dovish",
}
TAG_LABELS_JA = {
    "risk_on": "リスクオン要因",
    "risk_off": "リスクオフ要因",
    "dollar_strength": "ドル高要因",
    "rate_pressure": "金利圧力候補",
    "gold_safe_haven": "金安全資産需要",
    "oil_supply_risk": "原油供給リスク",
    "crypto_liquidity": "暗号資産流動性",
    "equity_momentum": "株式モメンタム",
    "geopolitical_risk": "地政学リスク",
    "inflation_pressure": "インフレ圧力",
    "recession_risk": "景気後退リスク",
    "central_bank_hawkish": "中銀タカ派",
    "central_bank_dovish": "中銀ハト派",
}
TAG_PRIORITY = [
    "geopolitical_risk",
    "inflation_pressure",
    "oil_supply_risk",
    "rate_pressure",
    "dollar_strength",
    "risk_off",
    "risk_on",
    "equity_momentum",
    "crypto_liquidity",
    "gold_safe_haven",
    "recession_risk",
    "central_bank_hawkish",
    "central_bank_dovish",
]
KEYWORDS = {
    "risk_on_news_score": ["rally", "rebound", "risk-on", "optimism", "soft landing", "rate cut hopes", "earnings beat", "tech gains", "stocks rise"],
    "risk_off_news_score": ["selloff", "slump", "risk-off", "fear", "uncertainty", "recession", "crisis", "safe haven", "stocks fall"],
    "dollar_strength_news_score": ["dollar rises", "dollar strengthens", "greenback gains", "yen weakens", "usd/jpy rises", "stronger dollar"],
    "rate_pressure_news_score": ["yields rise", "treasury yields climb", "hawkish fed", "sticky inflation", "higher for longer", "rate hike", "bond yields"],
    "gold_safe_haven_news_score": ["gold rises", "safe haven", "geopolitical tensions", "war", "conflict", "central bank buying", "inflation hedge"],
    "oil_supply_risk_news_score": ["oil rises", "crude jumps", "supply disruption", "opec", "middle east", "sanctions", "tanker", "inventory draw", "refinery outage"],
    "crypto_liquidity_news_score": ["bitcoin rises", "crypto rally", "etf inflows", "risk appetite", "liquidity", "rate cut", "dollar falls", "bitcoin etf"],
    "equity_momentum_news_score": ["stocks rise", "s&p gains", "nasdaq climbs", "tech gains", "earnings beat", "wall street rises"],
    "geopolitical_risk_news_score": ["war", "missile", "attack", "sanctions", "middle east", "russia", "ukraine", "taiwan", "china tensions", "geopolitical tensions"],
    "inflation_pressure_news_score": ["inflation", "cpi", "pce", "prices rise", "tariff", "wages", "energy prices"],
    "recession_risk_news_score": ["recession", "slowdown", "contraction", "jobless", "defaults", "weak demand"],
    "central_bank_hawkish_score": ["fed hawkish", "rate hike", "higher for longer", "boj hike", "ecb hawkish", "powell warns"],
    "central_bank_dovish_score": ["rate cut", "dovish", "easing", "stimulus", "pivot", "fed cuts"],
}


def normalize_headers(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    out = df.copy()
    out.columns = [str(col).strip().lower().replace("-", "_").replace(" ", "_") for col in out.columns]
    return out


def clamp(value: float) -> float:
    return round(max(0.0, min(100.0, float(value))), 2)


def read_headlines(path: Path = HEADLINES_PATH) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return normalize_headers(pd.read_csv(path))
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def keyword_hits(text: str, keywords: list[str]) -> list[str]:
    lower = text.lower()
    return [keyword for keyword in keywords if keyword in lower]


def score_from_hits(count: int, total_rows: int) -> float:
    if total_rows <= 0:
        return 0.0
    return clamp(min(100.0, count * 18.0 + (count / total_rows) * 35.0))


def score_value(scores: dict, key: str) -> float:
    value = pd.to_numeric(scores.get(key, 0), errors="coerce")
    return float(value) if not pd.isna(value) else 0.0


def clean_value(value) -> str:
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value or "")


def news_market_bias(scores: dict, headline_count: int) -> str:
    if headline_count < 5:
        return "insufficient_data"
    risk_on = score_value(scores, "risk_on_news_score")
    risk_off = score_value(scores, "risk_off_news_score")
    if risk_on >= 60 and risk_off >= 60:
        return "mixed"
    if risk_on >= 65 and risk_off < 45:
        return "risk_on"
    if risk_off >= 65 and risk_on < 45:
        return "risk_off"
    if risk_on < 40 and risk_off < 40:
        return "neutral"
    return "mixed" if min(risk_on, risk_off) >= 45 else "neutral"


def news_conflict_score(scores: dict, headline_count: int) -> float:
    base = min(score_value(scores, "risk_on_news_score"), score_value(scores, "risk_off_news_score"))
    if headline_count < 5:
        base *= max(0.0, headline_count / 5.0)
    return clamp(base)


def dominant_news_themes(scores: dict, limit: int = 5) -> list[str]:
    ranked = sorted(
        ((THEME_LABELS[col], score_value(scores, col)) for col in THEME_SCORE_COLUMNS),
        key=lambda item: item[1],
        reverse=True,
    )
    return [label for label, value in ranked if value >= 60][:limit]


def driver_tags_from_rules(matched_rules: list[str]) -> list[str]:
    tags = []
    for rule in matched_rules:
        score_col = rule.split(":", 1)[0]
        label = THEME_LABELS.get(score_col)
        if label and label not in tags:
            tags.append(label)
    return tags


def driver_summary_ja(tags: list[str]) -> str:
    if not tags:
        return "分類未確定"
    ordered = sorted(tags, key=lambda tag: TAG_PRIORITY.index(tag) if tag in TAG_PRIORITY else len(TAG_PRIORITY))
    labels = [TAG_LABELS_JA.get(tag, tag) for tag in ordered[:3]]
    if "geopolitical_risk" in tags and "risk_off" not in tags:
        labels.append("リスクオフ要因")
    if "inflation_pressure" in tags and "rate_pressure" not in tags:
        labels.append("金利圧力候補")
    return " / ".join(dict.fromkeys(labels))


def news_summary_ja(scores: dict, headline_count: int) -> str:
    bias = news_market_bias(scores, headline_count)
    conflict = news_conflict_score(scores, headline_count)
    themes = dominant_news_themes(scores)
    theme_text = "、".join(TAG_LABELS_JA.get(theme, theme) for theme in themes[:3])
    if bias == "insufficient_data":
        return "ニュース件数が少ないため、ナラティブ判定は保留です。"
    if bias == "mixed":
        suffix = "方向感は一方向ではなく、ボラティリティ上昇に注意が必要です。" if conflict >= 60 else "強弱材料が混在しており、方向感は限定的です。"
        return f"{theme_text or '複数テーマ'}が目立ち、リスクオン材料とリスクオフ材料が混在しています。{suffix}"
    if bias == "risk_on":
        return f"{theme_text or 'リスクオン材料'}が優勢で、ニュース面ではリスク選好がやや強い状態です。"
    if bias == "risk_off":
        return f"{theme_text or 'リスクオフ材料'}が優勢で、ニュース面では慎重姿勢が強い状態です。"
    return f"{theme_text or '主要テーマ'}はありますが、ニュース面の方向感は中立です。"


def classify_rows(headlines: pd.DataFrame) -> tuple[dict, list[dict]]:
    if headlines.empty:
        scores = {col: 0.0 for col in SCORE_COLUMNS}
        scores["news_confidence"] = 0.0
        return scores, []

    drivers = []
    counts = {col: 0 for col in SCORE_COLUMNS if col != "news_confidence"}
    for _, row in headlines.iterrows():
        title = str(row.get("title", "") or "")
        summary = str(row.get("summary", "") or "")
        text = f"{title} {summary}".lower()
        row_hits = []
        for score_col, keywords in KEYWORDS.items():
            hits = keyword_hits(text, keywords)
            if hits:
                counts[score_col] += len(hits)
                row_hits.extend([f"{score_col}:{hit}" for hit in hits])
        if row_hits:
            tags = driver_tags_from_rules(row_hits)
            drivers.append(
                {
                    "title": title,
                    "source": clean_value(row.get("source", "")),
                    "matched_assets": clean_value(row.get("matched_assets", "")),
                    "matched_rules": "|".join(row_hits[:8]),
                    "driver_tags": "|".join(tags),
                    "driver_summary_ja": driver_summary_ja(tags),
                    "link": clean_value(row.get("link", "")),
                }
            )

    total = len(headlines)
    scores = {col: score_from_hits(counts.get(col, 0), total) for col in counts}
    scores["news_confidence"] = clamp(min(100.0, 20.0 + total * 2.0 + len(drivers) * 6.0))
    return scores, drivers


def news_mode_summary(scores: dict) -> str:
    if not scores or scores.get("news_confidence", 0) <= 0:
        return "ニュースナラティブ未取得"
    parts = []
    bias = str(scores.get("news_market_bias", ""))
    if bias == "mixed":
        parts.append("ニュースは混在")
    elif bias == "neutral":
        parts.append("ニュースのリスク方向は中立")
    elif bias == "insufficient_data":
        parts.append("ニュース件数不足")
    elif bias == "risk_on":
        parts.append("ニュースはリスクオン寄り")
    elif bias == "risk_off":
        parts.append("ニュースはリスクオフ寄り")
    elif scores.get("risk_on_news_score", 0) >= scores.get("risk_off_news_score", 0) + 10:
        parts.append("ニュースはリスクオン寄り")
    elif scores.get("risk_off_news_score", 0) >= scores.get("risk_on_news_score", 0) + 10:
        parts.append("ニュースはリスクオフ寄り")
    else:
        parts.append("ニュースのリスク方向は中立")
    if scores.get("dollar_strength_news_score", 0) >= 35:
        parts.append("ドル高材料あり")
    if scores.get("rate_pressure_news_score", 0) >= 35:
        parts.append("金利圧力材料あり")
    if scores.get("geopolitical_risk_news_score", 0) >= 35:
        parts.append("地政学リスク材料あり")
    if scores.get("oil_supply_risk_news_score", 0) >= 35:
        parts.append("原油供給リスク材料あり")
    return " / ".join(parts)


def write_outputs(scores: dict, drivers: list[dict], headlines: pd.DataFrame) -> dict:
    generated_at = now_utc()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    enriched_scores = {
        **scores,
        "news_market_bias": news_market_bias(scores, len(headlines)),
        "news_conflict_score": news_conflict_score(scores, len(headlines)),
        "dominant_news_themes": dominant_news_themes(scores),
        "news_summary_ja": news_summary_ja(scores, len(headlines)),
    }
    row = {
        "generated_at_jst": format_jst(generated_at),
        "generated_at_utc": format_utc(generated_at),
        "headline_count": int(len(headlines)),
        **enriched_scores,
        "news_mode_summary": news_mode_summary(enriched_scores),
        "top_news_drivers": drivers[:10],
    }
    flat = row.copy()
    flat["dominant_news_themes"] = "|".join(row["dominant_news_themes"])
    flat["top_news_drivers"] = json.dumps(drivers[:10], ensure_ascii=False)
    pd.DataFrame([flat]).to_csv(SCORES_CSV, index=False)
    SCORES_JSON.write_text(json.dumps(row, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

    report = [
        "# Tactical Swing OS News Narrative Report",
        "",
        f"生成日時（JST）: {row['generated_at_jst']}",
        f"生成日時（UTC）: {row['generated_at_utc']}",
        f"headline件数: {row['headline_count']}",
        f"ニュース市場バイアス: {row['news_market_bias']}",
        f"ニュース矛盾スコア: {row['news_conflict_score']}",
        f"主要テーマ: {', '.join(row['dominant_news_themes']) or 'なし'}",
        f"日本語要約: {row['news_summary_ja']}",
        f"ニュースモード: {row['news_mode_summary']}",
        "",
        "## スコア",
        "",
    ]
    for col in SCORE_COLUMNS:
        report.append(f"- {col}: {row.get(col, 0)}")
    report.extend(["", "## Top News Drivers", ""])
    if drivers:
        for driver in drivers[:10]:
            report.append(f"- {driver.get('title', '')} ({driver.get('driver_summary_ja', '')})")
    else:
        report.append("ニュースドライバーは検出されませんでした。")
    report_path = REPORTS_DIR / f"{generated_at.astimezone(JST).strftime('%Y-%m-%d')}_news_narrative_report.md"
    report_path.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"news narrative scores csv generated: {SCORES_CSV}")
    print(f"news narrative scores json generated: {SCORES_JSON}")
    print(f"news narrative report generated: {report_path}")
    return row


def classify_news_narratives() -> dict:
    headlines = read_headlines()
    scores, drivers = classify_rows(headlines)
    return write_outputs(scores, drivers, headlines)


def main() -> int:
    classify_news_narratives()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
