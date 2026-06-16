from __future__ import annotations

"""Narrative Lookahead Audit (研究プロセスの汚染防止レイヤー)。

ニュースナラティブやAIフィードバックなどの文章系分析に、未来情報・評価後情報・
結果情報が混入していないかを監査する。これは新しい予測ロジックではなく、憲章
「後知恵バイアスこそ最大の敵」「AIは監査される対象」の実装である。

絶対条件:
- 監査結果は提案・警告のみ。weights.json/generate_signal.pyは一切変更しない。
- LLM API・有料ニュースAPIは新規利用しない(蓄積済みCSV/JSONのみ読む)。
- requires_human_approval は常に true。
"""

import argparse
import json
import re
from pathlib import Path

import pandas as pd

import audit_dictionaries
from time_utils import format_jst, format_utc, now_utc

RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/narrative")

AUDIT_COLUMNS = [
    "generated_at_jst",
    "audit_id",
    "source_type",
    "source_file",
    "source_timing_class",
    "reference_date",
    "narrative_timestamp",
    "signal_date",
    "evaluation_date",
    "text_excerpt",
    "detected_terms",
    "lookahead_risk_level",
    "lookahead_score",
    "issue_type",
    "recommended_action",
    "requires_human_approval",
    "weights_json_updated",
    "generate_signal_updated",
    "notes",
]

# --- 辞書は config/audit_dictionaries.json へ外部化 (欠損時は DEFAULTS へ安全fallback) ---
FUTURE_KEYWORDS = audit_dictionaries.future_keywords()
OUTCOME_TERMS = audit_dictionaries.outcome_terms()

# 事前材料として扱うソース (ここに評価結果や未来日付が混入すると危険)
PRE_SIGNAL_SOURCES = {"news_headline", "news_narrative"}

SOURCE_TIMING_CLASSES = {
    "pre_signal_news",
    "post_signal_news",
    "evaluation_feedback",
    "retrospective_analysis",
    "unknown_timing",
}

RISK_LEVELS = {"passed", "warning", "high_risk", "blocked", "unavailable"}


# === 純粋関数 (単体テスト対象) ===

def detect_terms(text: str | None, terms: list[str]) -> list[str]:
    """text に含まれる terms を返す (大文字小文字無視・英語は語境界マッチ)。"""
    return audit_dictionaries.match_terms(text, terms)


def parse_ts(value) -> pd.Timestamp | None:
    """日時文字列を naive(UTC) Timestamp へ。失敗時 None。"""
    if value is None:
        return None
    ts = pd.to_datetime(value, errors="coerce", utc=True)
    if pd.isna(ts):
        return None
    return pd.Timestamp(ts).tz_localize(None)


def classify_source_timing(
    source_type: str,
    narrative_ts: pd.Timestamp | None,
    signal_date: pd.Timestamp | None,
    has_outcome_terms: bool,
    feedback_type: str | None = None,
) -> str:
    """ソースの時間的位置づけを分類する。"""
    if source_type == "ai_feedback":
        return "evaluation_feedback"
    if has_outcome_terms and source_type == "news_narrative":
        return "retrospective_analysis"
    if narrative_ts is None or signal_date is None:
        return "unknown_timing"
    if narrative_ts.date() <= signal_date.date():
        return "pre_signal_news"
    return "post_signal_news"


def assess_risk(
    source_type: str,
    narrative_ts: pd.Timestamp | None,
    signal_date: pd.Timestamp | None,
    future_terms: list[str],
    outcome_terms: list[str],
    has_text: bool,
) -> dict:
    """未来情報混入のリスク判定。(level, score, issue_type, recommended_action) を返す。

    判定方針:
    - 事前材料ソースで narrative日時 > signal日時 → 未来日付参照 (high_risk以上)
    - 未来情報キーワード → warning以上
    - 事前材料ソースに評価結果語が混入 → warning以上
    - 上記が複数重なる → blocked
    - 比較材料が無い → unavailable
    """
    is_pre_signal = source_type in PRE_SIGNAL_SOURCES
    future_dated = bool(
        is_pre_signal
        and narrative_ts is not None
        and signal_date is not None
        and narrative_ts.date() > signal_date.date()
    )
    has_future_kw = bool(future_terms)
    outcome_in_pre_signal = bool(is_pre_signal and outcome_terms)

    score = 0
    issues: list[str] = []
    if future_dated:
        score += 50
        issues.append("future_dated_reference")
    if has_future_kw:
        score += min(30, 10 * len(future_terms))
        issues.append("future_keyword")
    if outcome_in_pre_signal:
        score += 15
        issues.append("evaluation_result_in_pre_signal")

    severe_count = sum([future_dated, has_future_kw, outcome_in_pre_signal])

    if future_dated and severe_count >= 2:
        level = "blocked"
    elif future_dated:
        level = "high_risk"
    elif has_future_kw or outcome_in_pre_signal:
        level = "warning"
    elif not has_text and narrative_ts is None:
        level = "unavailable"
    else:
        level = "passed"

    issue_type = issues[0] if issues else ("no_data" if level == "unavailable" else "none")
    action = {
        "blocked": "人間が当該ナラティブを除外し、時系列を再構成すること",
        "high_risk": "未来日付の材料を事前ナラティブから除外する",
        "warning": "時間軸を人間が確認し、振り返り材料か事前材料かを明示する",
        "unavailable": "入力データが揃ってから再監査する",
        "passed": "継続監視",
    }[level]
    return {"lookahead_risk_level": level, "lookahead_score": score, "issue_type": issue_type, "recommended_action": action}


def excerpt(text: str | None, limit: int = 160) -> str:
    if not text:
        return ""
    cleaned = re.sub(r"\s+", " ", str(text)).strip()
    return cleaned[:limit]


# === I/O (蓄積済みCSVのみ・Sheets書き込みなし) ===

def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except (pd.errors.EmptyDataError, OSError):
        return pd.DataFrame()


def latest_date_in(df: pd.DataFrame, columns: list[str]) -> pd.Timestamp | None:
    if df.empty:
        return None
    for col in columns:
        if col in df.columns:
            parsed = pd.to_datetime(df[col], errors="coerce", utc=True).dt.tz_localize(None)
            if parsed.notna().any():
                return pd.Timestamp(parsed.max())
    return None


# === 監査行の構築 ===

def _base_row(audit_id: str, source_type: str, source_file: str, generated_at_jst: str) -> dict:
    return {
        "generated_at_jst": generated_at_jst,
        "audit_id": audit_id,
        "source_type": source_type,
        "source_file": source_file,
        "source_timing_class": "unknown_timing",
        "reference_date": "",
        "narrative_timestamp": "",
        "signal_date": "",
        "evaluation_date": "",
        "text_excerpt": "",
        "detected_terms": "",
        "lookahead_risk_level": "unavailable",
        "lookahead_score": 0,
        "issue_type": "no_data",
        "recommended_action": "入力データが揃ってから再監査する",
        "requires_human_approval": True,
        "weights_json_updated": False,
        "generate_signal_updated": False,
        "notes": "",
    }


def audit_text_record(
    *,
    audit_id: str,
    source_type: str,
    source_file: str,
    text: str | None,
    narrative_ts: pd.Timestamp | None,
    signal_date: pd.Timestamp | None,
    evaluation_date: pd.Timestamp | None,
    generated_at_jst: str,
    feedback_type: str | None = None,
) -> dict:
    """1つの文章レコードを監査して1行を返す。"""
    row = _base_row(audit_id, source_type, source_file, generated_at_jst)
    future_terms = detect_terms(text, FUTURE_KEYWORDS)
    outcome_terms = detect_terms(text, OUTCOME_TERMS)
    has_outcome = bool(outcome_terms)
    timing = classify_source_timing(source_type, narrative_ts, signal_date, has_outcome, feedback_type)
    risk = assess_risk(source_type, narrative_ts, signal_date, future_terms, outcome_terms, bool(text))
    row.update(
        {
            "source_timing_class": timing,
            "reference_date": signal_date.strftime("%Y-%m-%d") if signal_date is not None else "",
            "narrative_timestamp": narrative_ts.strftime("%Y-%m-%d %H:%M") if narrative_ts is not None else "",
            "signal_date": signal_date.strftime("%Y-%m-%d") if signal_date is not None else "",
            "evaluation_date": evaluation_date.strftime("%Y-%m-%d") if evaluation_date is not None else "",
            "text_excerpt": excerpt(text),
            "detected_terms": ";".join(future_terms + outcome_terms),
            **risk,
        }
    )
    return row


def build_audit_rows(
    headlines: pd.DataFrame,
    narrative_scores: pd.DataFrame,
    ai_feedback: pd.DataFrame,
    signal_date: pd.Timestamp | None,
    evaluation_date: pd.Timestamp | None,
    generated_at_jst: str,
) -> list[dict]:
    rows: list[dict] = []

    # 1) ニュース見出し
    for i, r in headlines.iterrows():
        text = " ".join(str(r.get(c, "")) for c in ["title", "summary"] if c in headlines.columns)
        pub = parse_ts(r.get("published_utc") or r.get("published"))
        rows.append(
            audit_text_record(
                audit_id=f"news_headline_{i}",
                source_type="news_headline",
                source_file="results/news_headlines.csv",
                text=text,
                narrative_ts=pub,
                signal_date=signal_date,
                evaluation_date=evaluation_date,
                generated_at_jst=generated_at_jst,
            )
        )

    # 2) ニュースナラティブ要約 (集計1件)
    for i, r in narrative_scores.iterrows():
        text = " ".join(
            str(r.get(c, "")) for c in ["news_summary_ja", "news_mode_summary", "top_news_drivers"] if c in narrative_scores.columns
        )
        gen = parse_ts(r.get("generated_at_utc") or r.get("generated_at_jst"))
        rows.append(
            audit_text_record(
                audit_id=f"news_narrative_{i}",
                source_type="news_narrative",
                source_file="results/news_narrative_scores.csv",
                text=text,
                narrative_ts=gen,
                signal_date=signal_date,
                evaluation_date=evaluation_date,
                generated_at_jst=generated_at_jst,
            )
        )

    # 3) AIフィードバック (評価結果の振り返りはOKだが分類して記録)
    for i, r in ai_feedback.iterrows():
        text = " ".join(str(r.get(c, "")) for c in ["feedback_summary", "proposed_next_action"] if c in ai_feedback.columns)
        gen = parse_ts(r.get("generated_at_utc") or r.get("generated_at"))
        row_signal_date = parse_ts(r.get("date")) or signal_date
        rows.append(
            audit_text_record(
                audit_id=f"ai_feedback_{i}",
                source_type="ai_feedback",
                source_file="results/ai_feedback.csv",
                text=text,
                narrative_ts=gen,
                signal_date=row_signal_date,
                evaluation_date=evaluation_date,
                generated_at_jst=generated_at_jst,
                feedback_type=str(r.get("feedback_type", "")),
            )
        )

    return rows


# === 集計 ===

def summarize(rows: list[dict], generated_at_jst: str, generated_at_utc: str) -> dict:
    def count(level: str) -> int:
        return sum(1 for r in rows if r["lookahead_risk_level"] == level)

    total = len(rows)
    blocked = count("blocked")
    high = count("high_risk")
    warn = count("warning")
    unavailable = count("unavailable")
    unknown_timing = sum(1 for r in rows if r["source_timing_class"] == "unknown_timing")
    max_score = max((int(r["lookahead_score"]) for r in rows), default=0)

    if blocked > 0:
        status = "blocked"
    elif high > 0:
        status = "high_risk"
    elif warn > 0:
        status = "warning"
    elif total == 0:
        status = "unavailable"
    else:
        status = "passed"

    action = {
        "blocked": "人間によるナラティブ除外と時系列再構成が必要",
        "high_risk": "未来日付材料の除外を人間が確認",
        "warning": "時間軸の人間確認を推奨",
        "unavailable": "入力データ蓄積後に再監査",
        "passed": "continue_monitoring",
    }[status]

    return {
        "generated_at_jst": generated_at_jst,
        "generated_at_utc": generated_at_utc,
        "audit_status": status,
        "total_checked": total,
        "passed_count": count("passed"),
        "warning_count": warn,
        "high_risk_count": high,
        "blocked_count": blocked,
        "unavailable_count": unavailable,
        "unknown_timing_count": unknown_timing,
        "max_lookahead_score": max_score,
        "requires_human_approval": True,
        "weights_json_updated": False,
        "generate_signal_updated": False,
        "recommended_next_action": action,
    }


def render_markdown(summary: dict, rows: list[dict]) -> str:
    high_blocked = [r for r in rows if r["lookahead_risk_level"] in ("high_risk", "blocked")]
    warnings = [r for r in rows if r["lookahead_risk_level"] == "warning"]
    timing_counts: dict[str, int] = {}
    for r in rows:
        timing_counts[r["source_timing_class"]] = timing_counts.get(r["source_timing_class"], 0) + 1

    def table(items: list[dict]) -> str:
        if not items:
            return "_該当なし_"
        lines = ["| source_type | timing | risk | score | issue | terms | excerpt |", "| --- | --- | --- | --- | --- | --- | --- |"]
        for r in items[:20]:
            lines.append(
                "| {source_type} | {source_timing_class} | {lookahead_risk_level} | {lookahead_score} | {issue_type} | {detected_terms} | {ex} |".format(
                    ex=str(r["text_excerpt"]).replace("|", "\\|")[:80], **r
                )
            )
        return "\n".join(lines)

    timing_lines = "\n".join(f"- {k}: {v}" for k, v in sorted(timing_counts.items())) or "- なし"
    return f"""# Narrative Lookahead Audit

## 1. 概要

外部ニュースやAI要約に「未来情報・評価結果」が混入していないかを監査する補助レイヤーです。
自動売買判断ではなく、研究プロセスの時間軸汚染を検出します。最終判断は人間が行います。

## 2. 監査ステータス

- audit_status: **{summary['audit_status']}**
- recommended_next_action: {summary['recommended_next_action']}
- requires_human_approval: {summary['requires_human_approval']}
- weights_json_updated: {summary['weights_json_updated']} / generate_signal_updated: {summary['generate_signal_updated']}

## 3. 件数

- total_checked: {summary['total_checked']}
- passed: {summary['passed_count']} / warning: {summary['warning_count']} / high_risk: {summary['high_risk_count']} / blocked: {summary['blocked_count']}
- unavailable: {summary['unavailable_count']} / unknown_timing: {summary['unknown_timing_count']}
- max_lookahead_score: {summary['max_lookahead_score']}

## 4. high_risk / blocked の詳細

{table(high_blocked)}

## 5. warning の詳細

{table(warnings)}

## 6. source_timing_class 別集計

{timing_lines}

## 7. 注意事項

- この監査は自動売買判断ではありません。
- LLMやニュース要約への未来情報混入を検出する補助です。
- 評価結果を「振り返り」として使うのは許可されます。問題は「事前材料」と混同する場合です。
- 最終判断は人間が行います。
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit narratives for lookahead/contamination.")
    parser.parse_args()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    now = now_utc()
    generated_at_jst = format_jst(now)
    generated_at_utc = format_utc(now)

    headlines = read_csv(RESULTS_DIR / "news_headlines.csv")
    narrative_scores = read_csv(RESULTS_DIR / "news_narrative_scores.csv")
    ai_feedback = read_csv(RESULTS_DIR / "ai_feedback.csv")
    signals = read_csv(RESULTS_DIR / "signals.csv")
    evaluations = read_csv(RESULTS_DIR / "evaluations.csv")
    latest_evaluations = read_csv(RESULTS_DIR / "latest_evaluations.csv")

    signal_date = latest_date_in(signals, ["date", "signal_date"])
    evaluation_date = latest_date_in(latest_evaluations, ["evaluation_date", "hit_date"]) or latest_date_in(
        evaluations, ["evaluation_date", "hit_date"]
    )

    rows = build_audit_rows(headlines, narrative_scores, ai_feedback, signal_date, evaluation_date, generated_at_jst)
    summary = summarize(rows, generated_at_jst, generated_at_utc)

    audit_df = pd.DataFrame(rows, columns=AUDIT_COLUMNS)
    audit_df.to_csv(RESULTS_DIR / "narrative_lookahead_audit.csv", index=False)
    (RESULTS_DIR / "narrative_lookahead_audit.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (RESULTS_DIR / "narrative_lookahead_audit_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    report_date = now.astimezone().strftime("%Y-%m-%d") if now.tzinfo else now.strftime("%Y-%m-%d")
    report_date = format_jst(now)[:10]
    (REPORTS_DIR / f"{report_date}_narrative_lookahead_audit.md").write_text(
        render_markdown(summary, rows), encoding="utf-8"
    )

    print(f"narrative lookahead audit: status={summary['audit_status']} total={summary['total_checked']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
