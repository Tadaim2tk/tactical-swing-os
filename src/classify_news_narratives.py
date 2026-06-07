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
            drivers.append(
                {
                    "title": title,
                    "source": row.get("source", ""),
                    "matched_assets": row.get("matched_assets", ""),
                    "matched_rules": "|".join(row_hits[:8]),
                    "link": row.get("link", ""),
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
    if scores.get("risk_on_news_score", 0) >= scores.get("risk_off_news_score", 0) + 10:
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
    row = {
        "generated_at_jst": format_jst(generated_at),
        "generated_at_utc": format_utc(generated_at),
        "headline_count": int(len(headlines)),
        **scores,
        "news_mode_summary": news_mode_summary(scores),
        "top_news_drivers": drivers[:10],
    }
    flat = row.copy()
    flat["top_news_drivers"] = json.dumps(drivers[:10], ensure_ascii=False)
    pd.DataFrame([flat]).to_csv(SCORES_CSV, index=False)
    SCORES_JSON.write_text(json.dumps(row, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

    report = [
        "# Tactical Swing OS News Narrative Report",
        "",
        f"生成日時（JST）: {row['generated_at_jst']}",
        f"生成日時（UTC）: {row['generated_at_utc']}",
        f"headline件数: {row['headline_count']}",
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
            report.append(f"- {driver.get('title', '')} ({driver.get('matched_assets', '')})")
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
