from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import audit_narrative_lookahead as nl


JST = "2026-06-16 08:00:00 JST"


def _rec(**kw):
    base = dict(
        audit_id="t", source_type="news_headline", source_file="f",
        text="", narrative_ts=None, signal_date=None, evaluation_date=None,
        generated_at_jst=JST,
    )
    base.update(kw)
    return nl.audit_text_record(**base)


# === 空入力でも落ちない ===

def test_build_rows_empty_inputs():
    rows = nl.build_audit_rows(pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), None, None, JST)
    assert rows == []
    summary = nl.summarize(rows, JST, JST)
    assert summary["audit_status"] == "unavailable"
    assert summary["total_checked"] == 0


# === 未来日付参照 → high_risk ===

def test_future_dated_news_is_high_risk():
    r = _rec(
        source_type="news_headline",
        text="Gold rallied on rate fears",
        narrative_ts=nl.parse_ts("2026-06-12T00:00:00Z"),
        signal_date=nl.parse_ts("2026-06-10T00:00:00Z"),
    )
    assert r["lookahead_risk_level"] == "high_risk"
    assert r["issue_type"] == "future_dated_reference"
    assert r["source_timing_class"] == "post_signal_news"


# === 未来情報キーワード → warning以上 ===

def test_future_keyword_is_warning_or_higher():
    r = _rec(
        source_type="news_narrative",
        text="株は引け後に急伸した",  # 「引け後」
        narrative_ts=nl.parse_ts("2026-06-10T00:00:00Z"),
        signal_date=nl.parse_ts("2026-06-10T00:00:00Z"),
    )
    assert r["lookahead_risk_level"] in ("warning", "high_risk", "blocked")
    assert "引け後" in r["detected_terms"]


def test_future_keyword_english():
    assert "after the close" in nl.detect_terms("Stocks jumped after the close today", nl.FUTURE_KEYWORDS)


# === 評価結果語の事前材料混入 → warning ===

def test_outcome_terms_in_pre_signal_news_is_warning():
    r = _rec(
        source_type="news_headline",
        text="analysis references loss_sl and r_multiple of the setup",
        narrative_ts=nl.parse_ts("2026-06-10T00:00:00Z"),
        signal_date=nl.parse_ts("2026-06-10T00:00:00Z"),
    )
    assert r["lookahead_risk_level"] == "warning"
    assert "loss_sl" in r["detected_terms"]


def test_outcome_terms_in_ai_feedback_is_allowed():
    # AIフィードバックは振り返りとして評価結果を使ってよい → passed / evaluation_feedback
    r = _rec(
        source_type="ai_feedback",
        text="loss_sl だったため次回はSL設計を見直す",
        narrative_ts=nl.parse_ts("2026-06-12T00:00:00Z"),
        signal_date=nl.parse_ts("2026-06-10T00:00:00Z"),
    )
    assert r["source_timing_class"] == "evaluation_feedback"
    assert r["lookahead_risk_level"] == "passed"


# === blocked: 複数の重大混入 ===

def test_multiple_contamination_is_blocked():
    r = _rec(
        source_type="news_headline",
        text="market reacted after the loss_sl was confirmed",  # future kw + outcome term
        narrative_ts=nl.parse_ts("2026-06-12T00:00:00Z"),  # future-dated
        signal_date=nl.parse_ts("2026-06-10T00:00:00Z"),
    )
    assert r["lookahead_risk_level"] == "blocked"


# === source_timing_class 分類 ===

def test_timing_pre_signal():
    assert nl.classify_source_timing("news_headline", nl.parse_ts("2026-06-09"), nl.parse_ts("2026-06-10"), False) == "pre_signal_news"

def test_timing_post_signal():
    assert nl.classify_source_timing("news_headline", nl.parse_ts("2026-06-11"), nl.parse_ts("2026-06-10"), False) == "post_signal_news"

def test_timing_unknown_when_no_dates():
    assert nl.classify_source_timing("news_headline", None, None, False) == "unknown_timing"

def test_timing_retrospective_narrative():
    assert nl.classify_source_timing("news_narrative", nl.parse_ts("2026-06-10"), nl.parse_ts("2026-06-10"), True) == "retrospective_analysis"


# === summary counts と audit_status ===

def test_summary_counts_and_status_high_risk():
    rows = [
        _rec(source_type="news_headline", text="x", narrative_ts=nl.parse_ts("2026-06-12"), signal_date=nl.parse_ts("2026-06-10")),  # high_risk
        _rec(source_type="news_headline", text="loss_sl", narrative_ts=nl.parse_ts("2026-06-10"), signal_date=nl.parse_ts("2026-06-10")),  # warning
        _rec(source_type="ai_feedback", text="ok", narrative_ts=nl.parse_ts("2026-06-10"), signal_date=nl.parse_ts("2026-06-10")),  # passed
    ]
    s = nl.summarize(rows, JST, JST)
    assert s["total_checked"] == 3
    assert s["high_risk_count"] == 1
    assert s["warning_count"] == 1
    assert s["passed_count"] == 1
    assert s["audit_status"] == "high_risk"  # high_risk が最優先


def test_summary_status_blocked_precedence():
    rows = [_rec(source_type="news_headline", text="after the close loss_sl", narrative_ts=nl.parse_ts("2026-06-12"), signal_date=nl.parse_ts("2026-06-10"))]
    s = nl.summarize(rows, JST, JST)
    assert s["audit_status"] == "blocked"


# === safety flags が固定される ===

def test_safety_flags_fixed():
    r = _rec(text="anything")
    assert r["requires_human_approval"] is True
    assert r["weights_json_updated"] is False
    assert r["generate_signal_updated"] is False
    s = nl.summarize([r], JST, JST)
    assert s["requires_human_approval"] is True
    assert s["weights_json_updated"] is False
    assert s["generate_signal_updated"] is False


# === detect_terms 安全性 ===

def test_detect_terms_handles_none_and_empty():
    assert nl.detect_terms(None, nl.FUTURE_KEYWORDS) == []
    assert nl.detect_terms("", nl.OUTCOME_TERMS) == []
    assert nl.parse_ts("not a date") is None
