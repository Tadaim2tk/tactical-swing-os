from __future__ import annotations

"""Dashboard HTML/CSS描画層 (機能変更なし・build_dashboardから分離)。

表示内容・セクション順序・デザインは一切変更しない。
"""

import html

import pandas as pd

from dashboard_io import *  # noqa: F401,F403 - 低レベルヘルパーの再利用
from dashboard_io import fmt_num, normalize_column_name, numeric_or, latest_date, latest_file_date


SAFETY_NOTES = [
    "このシステムは実売買を行いません。",
    "このシステムはXMや証券会社を操作しません。",
    "ルール改善は提案のみで、自動反映されません。",
    "weights.json は自動更新されません。",
    "実運用に使う前に必ず人間による確認が必要です。",
]


DASHBOARD_DESCRIPTION = (
    "このダッシュボードは、Tactical Swing OS が生成したシグナル、評価結果、理由コード分析、"
    "改善候補を確認するための研究用画面です。実売買や自動発注は行いません。"
)


DISPLAY_LABELS = {
    "market_snapshot rows": "市場データ行数",
    "signals rows": "シグナル行数",
    "evaluations rows": "評価行数",
    "evaluation_view_source": "評価ビュー",
    "evaluation_fallback_used": "評価fallback使用",
    "latest daily report": "最新日次レポート",
    "latest weekly review": "最新週次レビュー",
    "latest monthly calibration": "最新月次較正",
    "latest reason_code_analysis": "最新理由コード分析",
    "latest rule_update_proposals": "最新ルール改善候補",
    "latest ai feedback": "最新AIフィードバック",
    "latest_model_state_update_proposals": "最新Model State更新提案",
    "latest_news_fetched_at": "最新ニュース取得日時",
    "news_fetch_status": "ニュース取得ステータス",
    "news_fetch_success_source_count": "取得成功ソース数",
    "news_fetch_failed_source_count": "取得失敗ソース数",
    "news_fetch_elapsed_seconds": "ニュース取得所要秒数",
    "headline_count": "headline件数",
    "news_market_bias": "ニュース市場バイアス",
    "news_conflict_score": "ニュース矛盾スコア",
    "dominant_news_themes": "主要ニューステーマ",
    "news_summary_ja": "日本語ニュース要約",
    "pending_reevaluation_count": "再評価対象件数",
    "pending_reevaluation_closed_count": "決着件数",
    "pending_reevaluation_open_count": "open継続件数",
    "pending_reevaluation_no_entry_count": "no_entry継続件数",
    "pending_reevaluation_missed_count": "取り逃し候補数",
    "latest_evaluation_unique_signal_count": "unique signal数",
    "latest_evaluation_rows": "latest rows",
    "latest_from_pending_reevaluations": "pending_reevaluation由来数",
    "latest_from_evaluations": "evaluations由来数",
    "latest_evaluation_closed_count": "closed数",
    "latest_evaluation_pending_count": "pending数",
    "latest_evaluation_open_count": "open数",
    "latest_evaluation_no_entry_count": "no_entry数",
    "latest_evaluation_missed_count": "missed_opportunity数",
    "previous_outcome": "前回outcome",
    "outcome": "今回outcome",
    "r_multiple": "R倍数",
    "error_type": "エラー分類",
    "news_confidence": "ニュース信頼度",
    "risk_on_news_score": "ニュースRisk On",
    "risk_off_news_score": "ニュースRisk Off",
    "dollar_strength_news_score": "ニュースドル高",
    "rate_pressure_news_score": "ニュース金利圧力",
    "geopolitical_risk_news_score": "ニュース地政学リスク",
    "oil_supply_risk_news_score": "ニュース原油供給リスク",
    "crypto_liquidity_news_score": "ニュース暗号資産流動性",
    "A": "Aランク",
    "B": "Bランク",
    "NO_TRADE": "見送り",
    "asset": "資産",
    "side": "売買方向",
    "rank": "ランク",
    "type": "タイプ",
    "recommended_action": "推奨アクション",
    "signal_strength": "シグナル強度",
    "setup_quality_score": "セットアップ品質",
    "entry_quality_score": "エントリー品質",
    "direction_confidence": "方向信頼度",
    "reason_codes": "判断理由コード",
    "no_trade_reason": "見送り理由",
    "total_evaluated": "評価対象数",
    "closed": "決着済み",
    "pending": "評価待ち",
    "skipped": "スキップ",
    "awaiting_horizon": "ホライズン未到達",
    "data_missing": "価格データ欠損",
    "invalid_signal_date": "日付不正",
    "no_entry": "未約定",
    "no_trade": "見送り",
    "win_rate": "勝率",
    "total_r": "総R",
    "average_r": "平均R",
    "best_r": "最大R",
    "worst_r": "最小R",
    "missed_opportunity_count": "取り逃し候補数",
    "evaluation_maturity": "評価成熟度",
    "signals": "シグナル数",
    "evaluations": "評価数",
    "reason_code": "判断理由コード",
    "signals_count": "シグナル数",
    "evaluated_count": "評価数",
    "reliability_label": "信頼性ラベル",
    "count": "件数",
    "average_mfe_r": "平均最大順行R",
    "assessment": "判定",
    "proposal_type": "提案タイプ",
    "target_type": "対象タイプ",
    "target_name": "対象名",
    "proposal_strength": "提案強度",
    "priority": "優先度",
    "proposed_change": "提案内容",
    "apply_automatically": "自動適用",
    "next_week_mode": "次週モード",
    "next_month_mode": "次月モード",
    "max_daily_risk_pct": "最大日次リスク%",
    "best_asset": "最良資産",
    "worst_asset": "最悪資産",
    "best_rank": "最良ランク",
    "worst_rank": "最悪ランク",
    "aligned": "整合",
    "conflicted": "衝突",
    "insufficient_data": "データ不足",
    "market_mode_summary": "市場モード",
    "model_state_total_proposals": "総提案件数",
    "model_state_increase_count": "increase件数",
    "model_state_decrease_count": "decrease件数",
    "model_state_hold_count": "hold件数",
    "model_state_insufficient_data_count": "データ不足件数",
    "model_state_apply_automatically": "自動適用",
    "model_state_audit_status": "安全監査",
    "model_state_audit_warning_count": "警告件数",
    "model_state_audit_blocked_count": "ブロック件数",
    "model_state_audit_critical_count": "重大件数",
    "model_state_requires_human_review": "人間確認",
    "model_state_weights_json_updated": "weights.json更新",
    "category": "カテゴリ",
    "target": "対象",
    "sample_count": "サンプル数",
    "avg_r": "平均R",
    "proposed_delta": "提案delta",
    "proposed_weight": "提案weight",
    "proposal_direction": "提案方向",
    "rationale": "理由",
    "weights_patch_count": "patch候補数",
    "weights_patch_excluded_count": "除外件数",
    "weights_patch_increase_count": "increase件数",
    "weights_patch_decrease_count": "decrease件数",
    "weights_patch_requires_human_approval": "人間承認",
    "weights_patch_applied": "patch適用",
    "weights_patch_weights_json_updated": "weights.json更新",
    "weight_path": "weight path",
    "patch_action": "patch action",
    "current_weight": "現在weight",
    "proposed_value": "提案値",
    "weights_patch_review_status": "review_status",
    "weights_patch_review_candidate_count": "承認候補",
    "weights_patch_review_hold_count": "保留候補",
    "weights_patch_review_reject_count": "却下候補",
    "weights_patch_review_blocked_count": "ブロック候補",
    "weights_patch_review_recommended_next_action": "推奨次アクション",
    "weights_patch_review_requires_human_approval": "人間承認",
    "weights_patch_review_patch_applied": "patch適用",
    "weights_patch_review_weights_json_updated": "weights.json更新",
    "review_decision": "レビュー判定",
    "recommended_human_action": "推奨人間アクション",
    "review_reason": "レビュー理由",
    "evidence_quality": "根拠品質",
    "patch_risk_level": "patchリスク",
    "missing_conditions": "不足条件",
    "proposal_adoption_tracking_status": "tracking_status",
    "proposal_adoption_total_count": "追跡対象",
    "proposal_adoption_accepted_count": "採用済み",
    "proposal_adoption_pending_review_count": "承認判断待ち",
    "proposal_adoption_held_count": "保留",
    "proposal_adoption_rejected_count": "却下",
    "proposal_adoption_blocked_count": "ブロック",
    "proposal_adoption_superseded_count": "置き換え済み",
    "proposal_adoption_manual_decision_count": "手動判断",
    "proposal_adoption_derived_decision_count": "レビュー由来",
    "proposal_adoption_recommended_next_action": "推奨次アクション",
    "adoption_status": "採用状態",
    "adoption_source": "採用判断ソース",
    "human_decision_recorded": "人間判断記録",
    "tracking_reason": "追跡理由",
    "weight_history_current_version": "現在Version",
    "weight_history_version_count": "Version数",
    "weight_history_tracked_count": "tracked件数",
    "weight_history_held_count": "held件数",
    "weight_history_candidate_count": "candidate件数",
    "weight_history_approved_count": "approved件数",
    "weight_history_rejected_count": "rejected件数",
    "weight_history_blocked_count": "blocked件数",
    "weight_history_weights_json_updated": "weights.json更新",
    "weight_history_patch_applied": "patch適用",
    "weight_history_requires_human_approval": "人間承認",
    "version_id": "Version",
    "description": "説明",
    "notes": "備考",
    "meta_learning_status": "meta_learning_status",
    "meta_learning_total_candidates": "Meta Learning候補数",
    "meta_learning_success_pattern_count": "成功パターン",
    "meta_learning_failure_pattern_count": "失敗パターン",
    "meta_learning_neutral_pattern_count": "中立パターン",
    "meta_learning_insufficient_data_count": "データ不足",
    "meta_learning_recommended_next_action": "推奨次アクション",
    "meta_learning_apply_automatically": "自動適用",
    "meta_learning_weights_json_updated": "weights.json更新",
    "meta_learning_patch_applied": "patch適用",
    "meta_learning_requires_human_approval": "人間承認",
    "meta_learning_id": "Meta Learning ID",
    "pattern_type": "パターン",
    "impact_score": "impact score",
    "impact_direction": "impact方向",
    "learning_hypothesis": "学習仮説",
    "evidence_summary": "根拠要約",
    "auto_calibration_status": "auto calibration status",
    "auto_calibration_candidate_count": "candidate count",
    "auto_calibration_increase_count": "increase",
    "auto_calibration_decrease_count": "decrease",
    "auto_calibration_hold_count": "hold",
    "auto_calibration_blocked_count": "blocked",
    "auto_calibration_insufficient_data_count": "データ不足",
    "auto_calibration_recommended_next_action": "recommended next action",
    "auto_calibration_requires_human_approval": "人間承認",
    "auto_calibration_patch_applied": "patch適用",
    "auto_calibration_weights_json_updated": "weights.json更新",
    "candidate_id": "Candidate ID",
    "factor": "factor",
    "classification": "分類",
    "confidence": "confidence",
    "sample_size": "サンプル数",
    "suggested_delta": "suggested delta",
    "suggested_value": "suggested value",
    "human_override_status": "human override status",
    "human_override_total_overrides": "total overrides",
    "human_override_accepted_count": "accepted",
    "human_override_held_count": "held",
    "human_override_rejected_count": "rejected",
    "human_override_blocked_count": "blocked",
    "human_override_positive_count": "positive override",
    "human_override_negative_count": "negative override",
    "human_override_unknown_count": "unknown outcome",
    "human_override_recommended_next_action": "recommended next action",
    "human_override_requires_human_approval": "人間承認",
    "portfolio_status": "portfolio status",
    "portfolio_candidate_assets": "candidate assets",
    "portfolio_defensive_assets": "defensive assets",
    "portfolio_offensive_assets": "offensive assets",
    "portfolio_cash_candidate": "cash candidate",
    "portfolio_average_confidence": "average confidence",
    "portfolio_concentration": "portfolio concentration",
    "portfolio_risk_concentration": "risk concentration",
    "portfolio_recommended_exposure": "recommended exposure",
    "portfolio_recommended_next_action": "recommended next action",
    "portfolio_requires_human_approval": "人間承認",
    "allocation_score": "配分スコア",
    "portfolio_weight_candidate": "配分候補",
    "confidence": "信頼度",
    "risk_class": "リスク分類",
    "risk_role": "リスク役割",
    "recommended_exposure": "推奨エクスポージャー",
    "cash_ratio_candidate": "キャッシュ候補",
    "override_type": "override type",
    "override_reason": "override reason",
    "impact_status": "impact status",
    "datetime_audit_status": "datetime audit status",
    "datetime_issues_found": "issues found",
    "datetime_timezone_mismatch": "timezone mismatch",
    "datetime_naive_datetime": "naive datetime count",
    "datetime_timestamp_mismatch": "timestamp mismatch",
    "datetime_recommended_action": "recommended action",
    # --- 日本語化オーバーライド（dict は後勝ち。可視ティアの英語ラベルを上書き） ---
    "health_status": "健全性ステータス", "total_layers": "総レイヤー数",
    "fresh": "最新レイヤー数", "stale": "古いレイヤー数", "empty": "空レイヤー数",
    "missing": "欠損レイヤー数", "unavailable": "対象なしレイヤー数",
    "unknown_age": "時刻不明レイヤー数", "future_timestamp": "未来時刻レイヤー数",
    "worst_layer": "最も悪いレイヤー", "attention_layers": "要注意レイヤー",
    "datetime_audit_status": "日時監査ステータス", "datetime_issues_found": "検出された問題数",
    "datetime_timezone_mismatch": "タイムゾーン不一致", "datetime_naive_datetime": "TZ無し日時 件数",
    "datetime_timestamp_mismatch": "タイムスタンプ不一致", "datetime_recommended_action": "推奨アクション",
    "review_status": "レビュー状態", "total_sources_checked": "確認したソース数",
    "total_findings": "検出件数", "warning": "警告", "high_risk": "高リスク", "blocked": "停止",
    "auto_apply_violations": "自動適用違反", "weights_update_violations": "weights更新違反",
    "contradictions": "矛盾", "max_severity": "最大深刻度",
    "recommended_next_action": "推奨次アクション", "requires_human_approval": "人間承認",
    "audit_status": "監査ステータス", "total_checked": "確認総数", "unknown_timing": "時間軸不明",
    "max_lookahead_score": "最大lookaheadスコア", "latest_audit_status": "最新監査ステータス",
    "latest_audit_report_date": "最新監査レポート日", "audit_report_available": "監査レポート有無",
    "calibration_status": "較正ステータス", "ranks_tracked": "対象ランク数",
    "overconfident": "自信過剰", "underconfident": "自信不足", "well_calibrated": "良好な較正",
    "overall_brier": "Brier（全体）", "reference_brier": "Brier（基準）",
    "brier_skill_score": "Brier Skill Score", "scored_n": "採点サンプル数",
    "weights_json_updated": "weights.json更新", "reliability_status": "信頼性ステータス",
    "narrative_source": "ナラティブソース", "total_narratives": "ナラティブ総数",
    "strong_positive": "強いプラス", "strong_negative": "強いマイナス", "unproven": "未実証",
    "neutral": "中立", "decay_divergence": "減衰乖離", "insufficient_data": "データ不足",
    "cost_model_status": "コストモデル状態", "configured_assets": "設定済みアセット",
    "unsourced_nonzero": "出典なし非ゼロ", "missing_provenance": "出典欠落",
    "invalid_source_type": "source_type不正", "invalid_source_date": "source_date不正",
    "default_source": "デフォルトsource", "configured_sources": "設定済みsource数",
    "net_r_available": "ネットR利用可", "gross_r_available": "グロスR利用可",
    "cost_adjusted_rows": "コスト調整済み行数",
    # --- 類似局面検索 (Narrative Memory v0 / Phase 29.2) ---
    "similar_narrative_status": "検索ステータス", "similar_query_date": "基準日",
    "similar_corpus_days": "過去局面日数", "similar_memory_days_total": "局面日数(総計)",
    "similar_case_rows": "類似ケース行数", "similar_embedding_provider": "embedding provider",
    "connected_to_signal_score": "シグナルスコア接続",
    "similar_rank": "順位", "similar_date": "類似日", "similarity": "類似度",
    "fwd_return_5d": "+5営業日", "fwd_return_10d": "+10営業日", "fwd_return_20d": "+20営業日",
    "outcome_status": "結果状態",
    "prediction_total": "記録した判断の数",
    "b_rank_win_rate_5d": "B級の5日勝率",
    "prediction_awaiting": "結果待ちの判断",
    "prediction_suspect": "記録ミス隔離",
    "judgements": "判断数",
    "with_levels": "水準つき",
    "win_5d": "5日勝率",
    "win_10d": "10日勝率",
    "mean_r_5d": "平均R(5日)",
    "basis": "統計的根拠",
    "r_close_5d": "5日後R",
    "r_close_10d": "10日後R",
    "result_5d": "5日判定",
    "result_10d": "10日判定",
}


VALUE_LABELS = {
    "not available": "未取得",
    "data not available": "データなし",
    "local fallback": "ローカルCSV/JSON fallback",
    "insufficient_data": "データ不足",
    "strong_positive": "強いプラス",
    "positive": "プラス",
    "neutral": "中立",
    "negative": "マイナス",
    "strong_negative": "強いマイナス",
    "effective_filter": "有効な見送り",
    "over_filtering_risk": "見送り過剰リスク",
    "TRADE": "TRADE（取引候補）",
    "WATCH": "WATCH（監視）",
    "NO_TRADE": "NO_TRADE（見送り）",
    "LONG": "LONG（買い）",
    "SHORT": "SHORT（売り）",
    "NONE": "NONE（見送り）",
    "increase": "increase（引き上げ候補）",
    "decrease": "decrease（引き下げ候補）",
    "hold": "hold（保留）",
    "passed": "passed（通過）",
    "warning": "warning（警告）",
    "blocked": "blocked（ブロック）",
    "unavailable": "unavailable（未取得）",
    "False": "false",
    "True": "true",
    "strong": "strong（強い候補）",
    "moderate": "moderate（中程度）",
    "weak": "weak（弱い候補）",
    "none": "none（提案なし）",
    "candidate": "candidate（承認候補）",
    "reject": "reject（却下）",
    "low": "low（低）",
    "medium": "medium（中）",
    "high": "high（高）",
    "approve_later": "approve_later（後で承認検討）",
    "wait_for_more_data": "wait_for_more_data（データ蓄積待ち）",
    "manual_review": "manual_review（人間確認）",
    "no_action": "no_action（対応なし）",
    "active": "active（追跡中）",
    "pending_review": "pending_review（承認判断待ち）",
    "held": "held（保留）",
    "accepted": "accepted（採用済み）",
    "rejected": "rejected（却下）",
    "superseded": "superseded（置き換え済み）",
    "tracked": "tracked（追跡対象）",
    "approved": "approved（承認済み）",
    "success_pattern": "成功パターン",
    "failure_pattern": "失敗パターン",
    "neutral_pattern": "中立パターン",
    "positive": "プラス",
    "negative": "マイナス",
    "human_review": "human_review（人間確認）",
    "derived_from_review": "レビュー由来",
    "manual": "手動判断",
    "generate_meta_learning_or_proposal_impact": "Meta LearningまたはImpact生成待ち",
    "wait_for_proposal_impact": "Proposal Impact待ち",
    "review_successful_overrides": "有効な介入を確認",
    "review_negative_overrides": "悪化した介入を確認",
    "generate_adoption_tracking": "Adoption Tracking生成待ち",
    # --- 状態系の値を日本語化（健全性 / 鮮度 / 評価成熟度 / 評価結果 / モード） ---
    "healthy": "正常", "watch": "警戒", "degraded": "要注意", "critical": "危険",
    "fresh": "最新", "stale": "古い", "empty": "空", "missing": "欠損",
    "unknown_age": "時刻不明", "future_timestamp": "未来時刻",
    "high_risk": "高リスク",
    "no_signals": "シグナルなし", "accumulating": "蓄積中",
    "pending": "評価待ち", "closed": "決着", "skipped": "スキップ", "open": "未決着",
    "open_unresolved": "未決着", "awaiting_horizon": "ホライズン未到達",
    "data_missing": "価格データ欠損", "invalid_signal_date": "日付不正", "invalid": "無効",
    "no_trade": "見送り", "no_trade_correct": "見送り正解", "no_trade_missed": "見送り取り逃し",
    "win_tp1": "勝ち(TP1)", "win_tp2": "勝ち(TP2)", "loss_sl": "負け(SL)", "no_entry": "未約定",
    "attack": "攻撃モード", "aggressive": "攻撃モード", "normal": "通常モード",
    "defense": "防御モード", "defensive": "防御モード",
    "tracking": "追跡中", "calibrated": "較正OK", "uncalibrated": "未較正",
    "tfidf_local": "TF-IDF（ローカル）",
    "no_query_document": "本日の局面文書なし",
    "before_price_history": "価格履歴より前",
    "no_price_data": "価格データなし",
    "not_applicable": "対象外(見送り)",
    "suspect_data": "記録ミス疑い(除外)",
    "awaiting": "結果待ち",
    "success": "的中",
    "failure": "外れ",
    "scored": "採点済み",
    "none": "指摘なし",
}


def display_label(label: str) -> str:
    return DISPLAY_LABELS.get(str(label), str(label).replace("_", " "))


def display_value(value, column: str | None = None) -> str:
    if pd.isna(value):
        return ""
    raw = str(value)
    if raw == "":
        return ""
    if column == "apply_automatically":
        return "false（自動適用なし）" if raw.lower() in {"false", "0", "no"} else raw
    return VALUE_LABELS.get(raw, VALUE_LABELS.get(raw.lower(), raw))


def display_source(source: str) -> str:
    return VALUE_LABELS.get(source, source)


def display_optional(value: str, fallback: str = "未取得") -> str:
    try:
        if pd.isna(value):
            return fallback
    except (TypeError, ValueError):
        pass
    if not value or str(value) == "not available":
        return fallback
    return str(value)


def badge(value: str, column: str | None = None) -> str:
    clean = display_value(value, column)
    cls = normalize_column_name(value) or "default"
    return f'<span class="badge badge-{html.escape(cls)}">{html.escape(clean)}</span>'


def value_class(value) -> str:
    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number):
        return ""
    if number > 0:
        return "positive"
    if number < 0:
        return "negative"
    return "neutral"


def is_numeric_cell(value) -> bool:
    if isinstance(value, bool) or value == "":
        return False
    number = pd.to_numeric(value, errors="coerce")
    return not pd.isna(number)


def table_html(df: pd.DataFrame, columns: list[str], empty: str = "データなし", limit: int | None = None) -> str:
    if df.empty:
        return f'<div class="empty">{html.escape(empty)}</div>'
    view = df.copy()
    if columns:
        for col in columns:
            if col not in view.columns:
                view[col] = ""
        view = view[columns]
    if limit:
        view = view.head(limit)
    if view.empty:
        return f'<div class="empty">{html.escape(empty)}</div>'

    out = ['<div class="table-wrap"><table><thead><tr>']
    out.extend(f"<th>{html.escape(display_label(col))}</th>" for col in view.columns)
    out.append("</tr></thead><tbody>")
    for _, row in view.iterrows():
        out.append("<tr>")
        for col in view.columns:
            raw = row.get(col, "")
            if col in {"rank", "side", "recommended_action", "proposal_strength", "proposal_direction", "reliability_label", "assessment", "classification", "override_type", "impact_status"}:
                cell = badge(raw, col)
            elif col in {
                "average_r",
                "avg_r",
                "total_r",
                "r_multiple",
                "win_rate",
                "best_r",
                "worst_r",
                "average_mfe_r",
                "proposed_delta",
                "proposed_weight",
                "suggested_delta",
                "suggested_value",
                "current_value",
                "confidence",
                "impact_score",
            }:
                cell = f'<span class="{value_class(raw)}">{fmt_num(raw)}</span>'
            elif is_numeric_cell(raw):
                cell = fmt_num(raw)
            else:
                cell = html.escape(display_value(raw, col))
            out.append(f"<td>{cell}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def stat_card(label: str, value, css_class: str = "") -> str:
    return f'<div class="stat {css_class}"><div class="stat-label">{html.escape(display_label(label))}</div><div class="stat-value">{html.escape(display_value(value))}</div></div>'


# === 再設計 (2026-07-17): サービスとしての「今日の判断」ヘルパー ===
# 供給源は手動予測台帳(todays_judgements_summary)。表示のみで発注はしない。

SIDE_DISPLAY = {"BUY": ("買い", "▲", "buy"), "SELL": ("売り", "▼", "sell")}

NO_TRADE_TYPE_JA = {
    "NO_TRADE": "見送り",
    "NONE": "見送り",
    "MOMENTUM_AVOID": "追随回避",
    "EVENT_WAIT": "イベント待ち",
    "CONFIRMATION_ONLY": "確認変数",
    "DIVERGENCE_WAIT": "乖離解消待ち",
}


def fmt_price(v) -> str:
    """価格の桁に応じた表示(捏造しない: 非数値は—)。"""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return "—"
    if f != f:  # NaN
        return "—"
    if abs(f) >= 1000:
        return f"{f:,.0f}"
    if abs(f) >= 100:
        return f"{f:,.2f}".rstrip("0").rstrip(".")
    return f"{f:,.4f}".rstrip("0").rstrip(".")


def range_figure(row: dict) -> str:
    """SL〜TP の価格レンジ図。エントリー帯を面で、SL/TPを目盛で示す。"""
    pts = {k: row.get(k) for k in ("sl", "entry_low", "entry_high", "tp1", "tp2")}
    if pts["entry_low"] is None or pts["entry_high"] is None or pts["sl"] is None:
        return ""
    vals = [v for v in pts.values() if v is not None]
    lo, hi = min(vals), max(vals)
    span = hi - lo
    if span <= 0:
        return ""
    pad = span * 0.07
    lo -= pad
    hi += pad
    span = hi - lo
    W, H = 560, 66

    def x(v):
        return round((v - lo) / span * (W - 28) + 14, 1)

    e1, e2 = x(pts["entry_low"]), x(pts["entry_high"])
    parts = [f'<svg class="range" viewBox="0 0 {W} {H}" preserveAspectRatio="none" role="img" aria-label="価格レンジ">']
    parts.append(f'<line x1="14" y1="33" x2="{W - 14}" y2="33" class="rg-track"/>')
    parts.append(f'<rect x="{min(e1, e2)}" y="27" width="{max(abs(e2 - e1), 4)}" height="12" rx="3" class="rg-entry"/>')

    def tick(v, cls, label, above):
        xx = x(v)
        y1, y2 = (20, 33) if above else (33, 46)
        ty = 14 if above else 60
        parts.append(f'<line x1="{xx}" y1="{y1}" x2="{xx}" y2="{y2}" class="rg-tick {cls}"/>')
        parts.append(f'<text x="{xx}" y="{ty}" class="rg-lab {cls}">{label} {fmt_price(v)}</text>')

    tick(pts["sl"], "rg-sl", "SL", False)
    if pts.get("tp1") is not None:
        tick(pts["tp1"], "rg-tp", "TP1", True)
    if pts.get("tp2") is not None:
        tick(pts["tp2"], "rg-tp", "TP2", False)
    parts.append(
        f'<text x="{(e1 + e2) / 2:.1f}" y="14" class="rg-lab rg-entry-lab">IN {fmt_price(pts["entry_low"])}–{fmt_price(pts["entry_high"])}</text>'
    )
    parts.append("</svg>")
    return "".join(parts)


def judgement_card(row: dict) -> str:
    """当日のA/B級判断1件をカードとして描画する。"""
    ja, arrow, side_cls = SIDE_DISPLAY.get(str(row.get("side", "")), (str(row.get("side", "?")), "", "flat"))
    rank = str(row.get("rank", ""))
    stats = []

    def st(label, value):
        stats.append(f'<div class="jc-stat"><span>{html.escape(label)}</span><b>{html.escape(value)}</b></div>')

    if row.get("rr") is not None:
        st("RR", fmt_num(row["rr"]))
    if row.get("win_prob") is not None:
        st("勝率(申告)", f"{row['win_prob'] * 100:.0f}%")
    if row.get("expected_r") is not None:
        st("期待値", f"{row['expected_r']:+.2f}R")
    if row.get("risk_pct") is not None:
        st("リスク", f"{row['risk_pct']:.2f}%")
    inv = str(row.get("invalidation") or "").strip()
    inv_html = f'<p class="jc-inv"><span>無効化:</span> {html.escape(inv)}</p>' if inv else ""
    type_txt = str(row.get("type") or "").strip()
    type_chip = f'<span class="chip">{html.escape(type_txt)}</span>' if type_txt else ""
    rank_cls = " rank-a" if rank == "A" else ""
    return (
        f'<article class="jcard {side_cls}{rank_cls}">'
        f'<header><span class="jc-side {side_cls}">{arrow} {html.escape(ja)}</span>'
        f'<span class="jc-asset">{html.escape(str(row.get("asset", "")))}</span>'
        f'<span class="chip rank">{html.escape(rank)}級</span>{type_chip}</header>'
        f"{range_figure(row)}"
        f'<div class="jc-stats">{"".join(stats)}</div>'
        f"{inv_html}"
        f"</article>"
    )


def no_trade_strip(rows: list) -> str:
    if not rows:
        return '<p class="notice">見送りの記帳はありません。</p>'
    chips = []
    for r in rows:
        t = str(r.get("type") or "").strip().upper()
        label = NO_TRADE_TYPE_JA.get(t, t or "見送り")
        chips.append(f'<span class="nt-chip"><b>{html.escape(str(r.get("asset", "")))}</b><em>{html.escape(label)}</em></span>')
    return f'<div class="nt-strip">{"".join(chips)}</div>'


def prev_results_html(tj: dict) -> str:
    rows = tj.get("prev_results") or []
    prev = str(tj.get("prev_date") or "—")
    if not rows:
        return f'<p class="notice">前営業日({html.escape(prev)})に方向つきの判断はありませんでした。</p>'
    tr = []
    for r in rows:
        side_ja = {"LONG": "買い", "SHORT": "売り"}.get(str(r.get("side", "")), str(r.get("side", "")))
        v = r.get("r_close_1d")
        if str(r.get("data_quality")) == "scale_mismatch":
            verdict = '<span class="chip warn">水準取り違えのため採点隔離</span>'
        elif v is None:
            verdict = '<span class="chip">結果待ち</span>'
        else:
            tone = "positive" if v > 0 else "negative" if v < 0 else "neutral"
            verdict = f'<b class="{tone}">{v:+.2f}R</b> <span class="muted">(1日後・終値基準)</span>'
        touched = "到達" if r.get("touched") else "未到達*"
        tr.append(
            f"<tr><td><b>{html.escape(str(r.get('asset', '')))}</b></td>"
            f"<td>{html.escape(side_ja)} {html.escape(str(r.get('rank', '')))}級</td>"
            f"<td>{touched}</td><td>{verdict}</td></tr>"
        )
    note = (
        '<p class="notice">*entry到達は翌営業日以降のバーで判定しており、記帳当日中の到達はまだ拾えません'
        "(既知の測定上の注意)。Rは終値基準の方向採点で、SL/TP執行の再現ではありません。</p>"
    )
    return (
        f'<div class="table-wrap"><table class="slim"><thead><tr><th>資産</th><th>判断</th><th>entry</th><th>結果</th></tr></thead>'
        f'<tbody>{"".join(tr)}</tbody></table></div>{note}'
    )


def cum_r_chart(series: list) -> str:
    """B級判断の累積R(5日終値基準)ライン。単一系列のため凡例なし(タイトルが命名)。"""
    pts = [p for p in series if isinstance(p.get("cum"), (int, float))]
    if len(pts) < 2:
        return '<p class="notice">確定した判断が2件未満のため蓄積待ちです。</p>'
    W, H, L, R, T, B = 920, 240, 50, 16, 16, 32
    ys = [p["cum"] for p in pts] + [0.0]
    ylo, yhi = min(ys), max(ys)
    if yhi - ylo < 1e-9:
        yhi = ylo + 1.0
    pad = (yhi - ylo) * 0.10
    ylo -= pad
    yhi += pad
    n = len(pts)

    def X(i):
        return L + (W - L - R) * (i / (n - 1))

    def Y(v):
        return T + (H - T - B) * (1 - (v - ylo) / (yhi - ylo))

    path = " ".join(f"{'M' if i == 0 else 'L'}{X(i):.1f},{Y(p['cum']):.1f}" for i, p in enumerate(pts))
    area = (
        f"M{X(0):.1f},{Y(0):.1f} "
        + " ".join(f"L{X(i):.1f},{Y(p['cum']):.1f}" for i, p in enumerate(pts))
        + f" L{X(n - 1):.1f},{Y(0):.1f} Z"
    )
    dots = "".join(
        f'<circle cx="{X(i):.1f}" cy="{Y(p["cum"]):.1f}" r="10" class="hit" '
        f'data-tip="{html.escape(str(p.get("date", "")))} {html.escape(str(p.get("asset", "")))} / この判断 {p["r"]:+.2f}R / 累積 {p["cum"]:+.2f}R"/>'
        for i, p in enumerate(pts)
    )
    ticks = ""
    for tv in (round(ylo + pad, 1), 0.0, round(yhi - pad, 1)):
        zero = ' zero' if abs(tv) < 1e-9 else ""
        ticks += (
            f'<line x1="{L}" y1="{Y(tv):.1f}" x2="{W - R}" y2="{Y(tv):.1f}" class="gr{zero}"/>'
            f'<text x="{L - 8}" y="{Y(tv) + 4:.1f}" class="ax">{tv:+.1f}</text>'
        )
    last = pts[-1]
    return (
        f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="B級判断の累積R(5日終値基準)">'
        f'{ticks}<path d="{area}" class="area"/><path d="{path}" class="line"/>'
        f'<circle cx="{X(n - 1):.1f}" cy="{Y(last["cum"]):.1f}" r="4" class="dot"/>'
        f'<text x="{X(n - 1) - 4:.1f}" y="{Y(last["cum"]) - 12:.1f}" class="last">{last["cum"]:+.1f}R</text>{dots}'
        f'<text x="{L}" y="{H - 8}" class="ax x">{html.escape(str(pts[0].get("date", "")))}</text>'
        f'<text x="{W - R}" y="{H - 8}" class="ax x end">{html.escape(str(last.get("date", "")))}</text></svg>'
    )


def horizon_chart(bars: list) -> str:
    """地平線別勝率(B級)。ひとつの指標なので単色・直接ラベル。50%線を参照線に。"""
    if not bars:
        return '<p class="notice">確定した判断の蓄積待ちです。</p>'
    W, H, L, R, T, B = 560, 220, 44, 12, 18, 36
    bw = 58
    n = len(bars)
    gap = (W - L - R - bw * n) / max(n - 1, 1) if n > 1 else 0
    y0v = T + (H - T - B)

    def Y(v):
        return T + (H - T - B) * (1 - v)

    parts = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="地平線別勝率(B級・終値基準)">']
    for g in (0.0, 0.5, 1.0):
        zero = ' zero' if abs(g - 0.5) < 1e-9 else ""
        parts.append(
            f'<line x1="{L}" y1="{Y(g):.1f}" x2="{W - R}" y2="{Y(g):.1f}" class="gr{zero}"/>'
            f'<text x="{L - 8}" y="{Y(g) + 4:.1f}" class="ax">{int(g * 100)}%</text>'
        )
    for i, b in enumerate(bars):
        x0 = L + i * (bw + gap)
        yb = Y(b["rate"])
        parts.append(
            f'<rect x="{x0:.1f}" y="{yb:.1f}" width="{bw}" height="{max(y0v - yb, 2):.1f}" rx="4" class="bar" '
            f'data-tip="{html.escape(str(b["horizon"]))}後: {b["rate"] * 100:.0f}% ({b["wins"]}/{b["n"]})"/>'
        )
        parts.append(f'<text x="{x0 + bw / 2:.1f}" y="{yb - 7:.1f}" class="val">{b["rate"] * 100:.0f}%</text>')
        parts.append(f'<text x="{x0 + bw / 2:.1f}" y="{H - 10}" class="ax x mid">{html.escape(str(b["horizon"]))} (n={b["n"]})</text>')
    parts.append("</svg>")
    return "".join(parts)


def summary_pill(label: str, value: str, tone: str) -> str:
    return (
        f'<span class="summary-pill pill-{tone}">'
        f'<span class="pill-k">{html.escape(label)}</span>'
        f'<span class="pill-v">{html.escape(value)}</span></span>'
    )


PAGE_CSS = """
:root {
  --bg:#f4f6fb; --surface:#ffffff; --surface2:#eef2f9; --line:#d9e0ec; --line2:#e7ecf5;
  --text:#182233; --muted:#5b6880; --accent:#2f5fd0; --accent-soft:rgba(47,95,208,.12);
  --pos:#147a48; --pos-soft:rgba(20,122,72,.11); --neg:#c02f3c; --neg-soft:rgba(192,47,60,.10);
  --warn:#8a6100; --warn-soft:rgba(178,131,0,.14); --shadow:0 1px 2px rgba(20,30,55,.06), 0 8px 24px rgba(20,30,55,.06);
}
:root[data-theme="dark"] {
  --bg:#0e1420; --surface:#161e2e; --surface2:#1d2739; --line:#2b3852; --line2:#233047;
  --text:#e9eefb; --muted:#95a3c0; --accent:#729dff; --accent-soft:rgba(114,157,255,.16);
  --pos:#3ec39b; --pos-soft:rgba(62,195,155,.14); --neg:#f2808f; --neg-soft:rgba(242,128,143,.12);
  --warn:#e0b356; --warn-soft:rgba(224,179,86,.15); --shadow:0 1px 2px rgba(0,0,0,.35), 0 10px 30px rgba(0,0,0,.30);
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg:#0e1420; --surface:#161e2e; --surface2:#1d2739; --line:#2b3852; --line2:#233047;
    --text:#e9eefb; --muted:#95a3c0; --accent:#729dff; --accent-soft:rgba(114,157,255,.16);
    --pos:#3ec39b; --pos-soft:rgba(62,195,155,.14); --neg:#f2808f; --neg-soft:rgba(242,128,143,.12);
    --warn:#e0b356; --warn-soft:rgba(224,179,86,.15); --shadow:0 1px 2px rgba(0,0,0,.35), 0 10px 30px rgba(0,0,0,.30);
  }
}
* { box-sizing:border-box; }
html { scroll-behavior:smooth; scroll-padding-top:64px; }
body { margin:0; background:var(--bg); color:var(--text);
  font-family:system-ui, -apple-system, "Hiragino Sans", "Yu Gothic UI", "Segoe UI", sans-serif;
  font-size:14px; line-height:1.65; -webkit-font-smoothing:antialiased; }
a { color:var(--accent); text-decoration:none; }
.wrap { max-width:1160px; margin:0 auto; padding:0 20px 56px; }
.topbar { position:sticky; top:0; z-index:30; background:color-mix(in srgb, var(--bg) 88%, transparent);
  backdrop-filter:blur(10px); border-bottom:1px solid var(--line2); }
.topbar-in { max-width:1160px; margin:0 auto; padding:10px 20px; display:flex; align-items:center; gap:16px; }
.brand { font-weight:800; font-size:15px; letter-spacing:.01em; white-space:nowrap; }
.brand small { color:var(--muted); font-weight:600; margin-left:8px; }
nav.jump { display:flex; gap:2px; flex:1; overflow-x:auto; }
nav.jump a { padding:6px 11px; border-radius:999px; color:var(--muted); font-weight:600; font-size:13px; white-space:nowrap; }
nav.jump a:hover { background:var(--accent-soft); color:var(--accent); }
#theme-toggle { border:1px solid var(--line); background:var(--surface); color:var(--muted);
  border-radius:999px; padding:5px 12px; cursor:pointer; font-size:12px; }
.gen { color:var(--muted); font-size:12px; white-space:nowrap; }
h1 { font-size:22px; margin:26px 0 4px; }
.lead { color:var(--muted); margin:0 0 18px; max-width:860px; }
h2.sec { font-size:17px; margin:34px 0 4px; display:flex; align-items:baseline; gap:10px; }
h2.sec .n { color:var(--accent); font-weight:800; }
p.sec-sub { color:var(--muted); margin:0 0 14px; font-size:13px; }
section.card { background:var(--surface); border:1px solid var(--line2); border-radius:14px;
  padding:18px 20px; box-shadow:var(--shadow); margin-bottom:14px; }
section.card > h2 { margin:0 0 6px; font-size:15px; }
section.card > h3 { margin:18px 0 8px; font-size:12.5px; color:var(--muted); letter-spacing:.05em; }
.notice { color:var(--muted); font-size:12.5px; margin:8px 0 4px; }
.muted { color:var(--muted); }
.pills { display:flex; flex-wrap:wrap; gap:10px; margin:16px 0 6px; }
.summary-pill { display:flex; flex-direction:column; gap:2px; padding:10px 16px; border-radius:12px;
  border:1px solid var(--line); background:var(--surface); box-shadow:var(--shadow); min-width:150px; }
.summary-pill .pill-k { font-size:11px; color:var(--muted); letter-spacing:.03em; }
.summary-pill .pill-v { font-size:16px; font-weight:800; }
.pill-good { border-color:color-mix(in srgb, var(--pos) 45%, var(--line)); } .pill-good .pill-v { color:var(--pos); }
.pill-warn { border-color:color-mix(in srgb, var(--warn) 55%, var(--line)); } .pill-warn .pill-v { color:var(--warn); }
.pill-bad { border-color:color-mix(in srgb, var(--neg) 55%, var(--line)); } .pill-bad .pill-v { color:var(--neg); }
.jgrid { display:grid; grid-template-columns:repeat(auto-fill, minmax(330px, 1fr)); gap:14px; }
.jcard { background:var(--surface); border:1px solid var(--line2); border-left:4px solid var(--line);
  border-radius:14px; padding:14px 16px 12px; box-shadow:var(--shadow); }
.jcard.buy { border-left-color:var(--pos); }
.jcard.sell { border-left-color:var(--neg); }
.jcard.rank-a { outline:2px solid var(--accent); outline-offset:-1px; }
.jcard header { display:flex; align-items:center; gap:9px; flex-wrap:wrap; margin-bottom:4px; }
.jc-side { font-weight:800; font-size:13px; padding:3px 10px; border-radius:999px; }
.jc-side.buy { color:var(--pos); background:var(--pos-soft); }
.jc-side.sell { color:var(--neg); background:var(--neg-soft); }
.jc-asset { font-size:19px; font-weight:800; letter-spacing:.01em; }
.chip { font-size:11px; font-weight:700; color:var(--muted); background:var(--surface2);
  border:1px solid var(--line2); padding:2px 9px; border-radius:999px; }
.chip.rank { color:var(--accent); background:var(--accent-soft); border-color:transparent; }
.chip.warn { color:var(--warn); background:var(--warn-soft); border-color:transparent; }
.jc-stats { display:flex; gap:8px; flex-wrap:wrap; margin-top:8px; }
.jc-stat { background:var(--surface2); border-radius:9px; padding:6px 11px; display:flex; flex-direction:column; min-width:78px; }
.jc-stat span { font-size:10.5px; color:var(--muted); }
.jc-stat b { font-size:14.5px; }
.jc-inv { margin:10px 0 0; font-size:12px; color:var(--muted); border-top:1px dashed var(--line2); padding-top:8px; }
.jc-inv span { font-weight:700; }
svg.range { width:100%; height:66px; display:block; margin-top:8px; }
.rg-track { stroke:var(--line); stroke-width:2; }
.rg-entry { fill:var(--accent); opacity:.75; }
.rg-tick { stroke-width:2; } .rg-tick.rg-sl { stroke:var(--neg); } .rg-tick.rg-tp { stroke:var(--pos); }
.rg-lab { font-size:10.5px; fill:var(--muted); text-anchor:middle; font-weight:600; }
.rg-lab.rg-sl { fill:var(--neg); } .rg-lab.rg-tp { fill:var(--pos); } .rg-lab.rg-entry-lab { fill:var(--accent); font-weight:700; }
.nt-strip { display:flex; flex-wrap:wrap; gap:8px; margin-top:6px; }
.nt-chip { display:inline-flex; align-items:center; gap:7px; border:1px solid var(--line2); background:var(--surface2);
  border-radius:999px; padding:5px 12px; font-size:12px; }
.nt-chip b { font-size:12.5px; } .nt-chip em { font-style:normal; color:var(--muted); }
.grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(170px, 1fr)); gap:9px; margin-top:8px; }
.stat { background:var(--surface2); border:1px solid var(--line2); border-radius:10px; padding:10px 12px; }
.stat-label { color:var(--muted); font-size:11px; overflow-wrap:anywhere; }
.stat-value { margin-top:4px; font-size:16px; font-weight:750; overflow-wrap:anywhere; }
.tiles { display:grid; grid-template-columns:repeat(auto-fit, minmax(150px, 1fr)); gap:10px; margin:4px 0 14px; }
.tile { background:var(--surface); border:1px solid var(--line2); border-radius:12px; padding:12px 14px; box-shadow:var(--shadow); }
.tile .t-k { font-size:11px; color:var(--muted); }
.tile .t-v { font-size:22px; font-weight:800; margin-top:2px; }
.tile .t-s { font-size:11px; color:var(--muted); margin-top:2px; }
.tile .t-v.positive { color:var(--pos); } .tile .t-v.negative { color:var(--neg); } .tile .t-v.accent { color:var(--accent); }
.charts { display:grid; grid-template-columns:1.6fr 1fr; gap:14px; }
@media (max-width:900px) { .charts { grid-template-columns:1fr; } }
svg.chart { width:100%; height:auto; display:block; }
svg.chart .gr { stroke:var(--line2); stroke-width:1; }
svg.chart .gr.zero { stroke:var(--muted); stroke-dasharray:4 4; }
svg.chart .ax { font-size:11px; fill:var(--muted); text-anchor:end; }
svg.chart .ax.x { text-anchor:start; } svg.chart .ax.x.end { text-anchor:end; } svg.chart .ax.x.mid { text-anchor:middle; }
svg.chart .line { fill:none; stroke:var(--accent); stroke-width:2.25; stroke-linejoin:round; }
svg.chart .area { fill:var(--accent); opacity:.10; }
svg.chart .dot { fill:var(--accent); }
svg.chart .last { font-size:12.5px; font-weight:800; fill:var(--accent); text-anchor:end; }
svg.chart .bar { fill:var(--accent); opacity:.85; }
svg.chart .bar:hover { opacity:1; }
svg.chart .val { font-size:12px; font-weight:750; fill:var(--text); text-anchor:middle; }
svg.chart .hit { fill:transparent; cursor:crosshair; }
svg.chart .hit:hover { fill:var(--accent); opacity:.25; }
.table-wrap { overflow-x:auto; border:1px solid var(--line2); border-radius:10px; margin-top:8px; }
table { width:100%; border-collapse:collapse; min-width:680px; }
table.slim { min-width:0; }
th, td { padding:8px 11px; border-bottom:1px solid var(--line2); text-align:left; vertical-align:top; font-size:13px; }
tbody tr:last-child td { border-bottom:none; }
th { color:var(--muted); background:var(--surface2); font-size:11.5px; letter-spacing:.03em; position:sticky; top:0; }
tr:hover td { background:var(--accent-soft); }
.badge { display:inline-flex; align-items:center; border-radius:999px; padding:2px 8px; font-size:11.5px; font-weight:700; background:var(--surface2); color:var(--muted); }
.badge-a, .badge-trade, .badge-strong_positive, .badge-positive { background:var(--pos-soft); color:var(--pos); }
.badge-b, .badge-watch, .badge-medium { background:var(--warn-soft); color:var(--warn); }
.badge-no_trade, .badge-none, .badge-data_insufficient, .badge-insufficient_data { background:var(--surface2); color:var(--muted); }
.badge-strong_negative, .badge-negative, .badge-high { background:var(--neg-soft); color:var(--neg); }
.positive { color:var(--pos); font-weight:700; }
.negative { color:var(--neg); font-weight:700; }
.neutral { color:var(--muted); }
.empty { color:var(--muted); padding:12px 14px; border:1px dashed var(--line); border-radius:10px; font-size:13px; }
ul { margin:8px 0 0; padding-left:20px; color:var(--muted); }
details.group { margin:10px 0 14px; }
details.group > summary { cursor:pointer; list-style:none; display:flex; align-items:center; gap:10px;
  padding:13px 16px; background:var(--surface); border:1px solid var(--line2); border-radius:12px;
  font-weight:750; font-size:14px; box-shadow:var(--shadow); user-select:none; }
details.group > summary::-webkit-details-marker { display:none; }
details.group > summary::after { content:"開く"; margin-left:auto; font-size:11.5px; color:var(--accent); font-weight:600; }
details.group[open] > summary::after { content:"閉じる"; }
details.group > summary .g-sub { color:var(--muted); font-weight:500; font-size:12px; }
details.group > .g-body { padding-top:12px; }
#tooltip { position:fixed; z-index:99; pointer-events:none; background:var(--text); color:var(--bg);
  font-size:12px; font-weight:600; padding:6px 10px; border-radius:8px; opacity:0; transition:opacity .08s; max-width:320px; }
footer.foot { color:var(--muted); font-size:12px; margin-top:26px; border-top:1px solid var(--line2); padding-top:14px; }
"""

PAGE_JS = """
(function () {
  var KEY = "tso-theme";
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  if (saved === "light" || saved === "dark") document.documentElement.setAttribute("data-theme", saved);
  var btn = document.getElementById("theme-toggle");
  function label() {
    var t = document.documentElement.getAttribute("data-theme");
    if (!t) t = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    btn.textContent = t === "dark" ? "ライト表示" : "ダーク表示";
  }
  btn.addEventListener("click", function () {
    var cur = document.documentElement.getAttribute("data-theme");
    if (!cur) cur = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    var next = cur === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    try { localStorage.setItem(KEY, next); } catch (e) {}
    label();
  });
  label();

  var tip = document.getElementById("tooltip");
  document.addEventListener("mousemove", function (ev) {
    var t = ev.target && ev.target.closest ? ev.target.closest("[data-tip]") : null;
    if (t) {
      tip.textContent = t.getAttribute("data-tip");
      tip.style.opacity = "1";
      var x = Math.min(ev.clientX + 14, window.innerWidth - tip.offsetWidth - 8);
      var y = Math.max(ev.clientY - tip.offsetHeight - 12, 8);
      tip.style.left = x + "px";
      tip.style.top = y + "px";
    } else {
      tip.style.opacity = "0";
    }
  }, { passive: true });
})();
"""


def render_html(
    *,
    generated: str,
    generated_at_jst: str,
    generated_at_utc: str,
    data_reference_date: str,
    source: str,
    latest_dates: dict,
    row_counts: dict,
    signals: pd.DataFrame,
    signal_counts: dict,
    eval_summary: dict,
    asset_table: pd.DataFrame,
    reason_table: pd.DataFrame,
    no_trade_table: pd.DataFrame,
    rule_updates: pd.DataFrame,
    model_state_updates: pd.DataFrame,
    model_state_summary: dict,
    weights_patch: dict,
    weights_patch_review: dict,
    proposal_adoption: dict,
    weight_history: dict,
    meta_learning: dict,
    auto_calibration: dict,
    human_override: dict,
    portfolio_layer: dict,
    datetime_health: dict,
    prediction_calibration: dict,
    prediction_calibration_table: pd.DataFrame,
    narrative_reliability: dict,
    narrative_reliability_table: pd.DataFrame,
    transaction_cost: dict,
    audit_report: dict,
    narrative_lookahead: dict,
    narrative_lookahead_table: pd.DataFrame,
    adversarial_review: dict,
    adversarial_review_table: pd.DataFrame,
    data_health: dict,
    mode: dict,
    ai_summary: dict,
    news_summary: dict,
    pending_summary: dict,
    latest_eval_summary: dict,
    evaluation_view_source: str,
    evaluation_fallback_used: bool,
    similar_narrative: dict,
    similar_table: pd.DataFrame,
    prediction_log: dict,
    apply_false: bool,
    todays_judgements: dict,
    performance_series: dict,
    execution_view: dict,
    summary: dict,
) -> str:
    top_positive = reason_table[reason_table["reliability_label"].isin(["strong_positive", "positive"])].head(10) if not reason_table.empty and "reliability_label" in reason_table.columns else pd.DataFrame()
    top_negative = (
        reason_table[reason_table["reliability_label"].isin(["strong_negative", "negative"])].sort_values("average_r").head(10)
        if not reason_table.empty and {"reliability_label", "average_r"}.issubset(reason_table.columns)
        else pd.DataFrame()
    )
    insufficient = reason_table[reason_table["reliability_label"].astype(str) == "insufficient_data"].head(10) if not reason_table.empty and "reliability_label" in reason_table.columns else pd.DataFrame()
    rule_view = rule_updates.sort_values("priority").head(10) if not rule_updates.empty and "priority" in rule_updates.columns else rule_updates.head(10)
    system_stats = "".join(
        [
            stat_card("market_snapshot rows", row_counts["market_snapshot"]),
            stat_card("signals rows", row_counts["signals"]),
            stat_card("evaluations rows", row_counts["evaluations"]),
            stat_card("evaluation_view_source", evaluation_view_source),
            stat_card("evaluation_fallback_used", str(evaluation_fallback_used).lower()),
            stat_card("latest daily report", latest_dates["latest_daily_report_date"] or "未取得"),
            stat_card("latest weekly review", latest_dates["latest_weekly_review_date"] or "未取得"),
            stat_card("latest monthly calibration", latest_dates["latest_monthly_calibration_date"] or "未取得"),
            stat_card("latest reason_code_analysis", latest_dates["latest_reason_code_analysis_date"] or "未取得"),
            stat_card("latest rule_update_proposals", latest_dates["latest_rule_update_proposals_date"] or "未取得"),
            stat_card("latest_model_state_update_proposals", latest_dates["latest_model_state_update_proposals_date"] or "未取得"),
            stat_card("latest ai feedback", latest_dates["latest_ai_feedback_date"] or "未取得"),
        ]
    )
    datetime_stats = "".join(
        [
            stat_card("datetime_audit_status", datetime_health.get("datetime_audit_status", "unavailable")),
            stat_card("datetime_issues_found", datetime_health.get("datetime_issues_found", 0)),
            stat_card("datetime_timezone_mismatch", datetime_health.get("datetime_timezone_mismatch", 0)),
            stat_card("datetime_naive_datetime", datetime_health.get("datetime_naive_datetime", 0)),
            stat_card("datetime_timestamp_mismatch", datetime_health.get("datetime_timestamp_mismatch", 0)),
            stat_card("datetime_recommended_action", datetime_health.get("datetime_recommended_action", "monitor")),
        ]
    )
    prediction_calibration_stats = "".join(
        [
            stat_card("calibration_status", prediction_calibration.get("calibration_status", "unavailable")),
            stat_card("ranks_tracked", prediction_calibration.get("ranks_tracked", 0)),
            stat_card("overconfident", prediction_calibration.get("overconfident_count", 0)),
            stat_card("underconfident", prediction_calibration.get("underconfident_count", 0)),
            stat_card("well_calibrated", prediction_calibration.get("well_calibrated_count", 0)),
            stat_card("insufficient_data", prediction_calibration.get("insufficient_data_count", 0)),
            stat_card("overall_brier", fmt_num(prediction_calibration.get("overall_brier", 0.0))),
            stat_card("reference_brier", fmt_num(prediction_calibration.get("reference_brier", 0.0))),
            stat_card("brier_skill_score", fmt_num(prediction_calibration.get("brier_skill_score", 0.0))),
            stat_card("scored_n", prediction_calibration.get("scored_n", 0)),
            stat_card("requires_human_approval", str(prediction_calibration.get("requires_human_approval", True)).lower()),
            stat_card("weights_json_updated", str(prediction_calibration.get("weights_json_updated", False)).lower()),
        ]
    )
    narrative_reliability_stats = "".join(
        [
            stat_card("reliability_status", narrative_reliability.get("narrative_reliability_status", "unavailable")),
            stat_card("narrative_source", narrative_reliability.get("narrative_source", "unavailable")),
            stat_card("total_narratives", narrative_reliability.get("total_narratives", 0)),
            stat_card("strong_positive", narrative_reliability.get("strong_positive_count", 0)),
            stat_card("strong_negative", narrative_reliability.get("strong_negative_count", 0)),
            stat_card("unproven", narrative_reliability.get("unproven_count", 0)),
            stat_card("insufficient_data", narrative_reliability.get("insufficient_data_count", 0)),
            stat_card("decay_divergence", narrative_reliability.get("decay_divergence_count", 0)),
            stat_card("requires_human_approval", str(narrative_reliability.get("requires_human_approval", True)).lower()),
            stat_card("weights_json_updated", str(narrative_reliability.get("weights_json_updated", False)).lower()),
        ]
    )
    transaction_cost_stats = "".join(
        [
            stat_card("cost_model_status", transaction_cost.get("cost_model_status", "unconfigured")),
            stat_card("configured_assets", transaction_cost.get("configured_asset_count", 0)),
            stat_card("unsourced_nonzero", transaction_cost.get("unsourced_nonzero_count", 0)),
            stat_card("missing_provenance", transaction_cost.get("missing_provenance_count", 0)),
            stat_card("invalid_source_type", transaction_cost.get("invalid_source_type_count", 0)),
            stat_card("invalid_source_date", transaction_cost.get("invalid_source_date_count", 0)),
            stat_card("default_source", transaction_cost.get("default_source", "unconfigured")),
            stat_card("configured_sources", ", ".join(transaction_cost.get("configured_sources", []) or []) or "なし"),
            stat_card("net_r_available", str(transaction_cost.get("net_r_available", False)).lower()),
            stat_card("gross_r_available", str(transaction_cost.get("gross_r_available", False)).lower()),
            stat_card("cost_adjusted_rows", transaction_cost.get("cost_adjusted_rows", 0)),
        ]
    )
    transaction_cost_warning = transaction_cost.get("warning", "")
    transaction_cost_warning_html = (
        f'<p class="notice">{html.escape(transaction_cost_warning)}</p>' if transaction_cost_warning else ""
    )
    audit_report_stats = "".join(
        [
            stat_card("latest_audit_status", audit_report.get("latest_audit_status", "unavailable")),
            stat_card("latest_audit_report_date", audit_report.get("latest_audit_report_date") or "未取得"),
            stat_card("audit_report_available", str(audit_report.get("audit_report_available", False)).lower()),
        ]
    )
    narrative_lookahead_stats = "".join(
        [
            stat_card("audit_status", narrative_lookahead.get("audit_status", "unavailable")),
            stat_card("total_checked", narrative_lookahead.get("total_checked", 0)),
            stat_card("warning", narrative_lookahead.get("warning_count", 0)),
            stat_card("high_risk", narrative_lookahead.get("high_risk_count", 0)),
            stat_card("blocked", narrative_lookahead.get("blocked_count", 0)),
            stat_card("unknown_timing", narrative_lookahead.get("unknown_timing_count", 0)),
            stat_card("max_lookahead_score", narrative_lookahead.get("max_lookahead_score", 0)),
            stat_card("recommended_next_action", narrative_lookahead.get("recommended_next_action", "continue_monitoring")),
            stat_card("requires_human_approval", str(narrative_lookahead.get("requires_human_approval", True)).lower()),
        ]
    )
    adversarial_review_stats = "".join(
        [
            stat_card("review_status", adversarial_review.get("review_status", "unavailable")),
            stat_card("total_sources_checked", adversarial_review.get("total_sources_checked", 0)),
            stat_card("total_findings", adversarial_review.get("total_findings", 0)),
            stat_card("warning", adversarial_review.get("warning_count", 0)),
            stat_card("high_risk", adversarial_review.get("high_risk_count", 0)),
            stat_card("blocked", adversarial_review.get("blocked_count", 0)),
            stat_card("auto_apply_violations", adversarial_review.get("auto_apply_violation_count", 0)),
            stat_card("weights_update_violations", adversarial_review.get("weights_update_violation_count", 0)),
            stat_card("contradictions", adversarial_review.get("contradiction_count", 0)),
            stat_card("max_severity", adversarial_review.get("max_severity", "none")),
            stat_card("recommended_next_action", adversarial_review.get("recommended_next_action", "continue_monitoring")),
            stat_card("requires_human_approval", str(adversarial_review.get("requires_human_approval", True)).lower()),
        ]
    )
    data_health_stats = "".join(
        [
            stat_card("health_status", data_health.get("health_status", "unavailable")),
            stat_card("total_layers", data_health.get("total_layers", 0)),
            stat_card("fresh", data_health.get("fresh_count", 0)),
            stat_card("stale", data_health.get("stale_count", 0)),
            stat_card("empty", data_health.get("empty_count", 0)),
            stat_card("missing", data_health.get("missing_count", 0)),
            stat_card("unavailable", data_health.get("unavailable_count", 0)),
            stat_card("unknown_age", data_health.get("unknown_age_count", 0)),
            stat_card("future_timestamp", data_health.get("future_timestamp_count", 0)),
            stat_card("worst_layer", data_health.get("worst_layer", "") or "なし"),
            stat_card("attention_layers", ", ".join(data_health.get("attention_layers", []) or []) or "なし"),
        ]
    )
    data_health_table = pd.DataFrame(data_health.get("layers", []) or [])
    eval_stats = "".join(stat_card(k, fmt_num(v) if isinstance(v, float) else v, value_class(v)) for k, v in eval_summary.items())
    signal_stats = "".join(stat_card(k, v) for k, v in signal_counts.items())
    mode_stats = "".join(stat_card(k, fmt_num(v) if isinstance(v, float) else display_optional(str(v))) for k, v in mode.items())
    prediction_rank_table = prediction_log.get("rank_table", pd.DataFrame())
    prediction_recent_table = prediction_log.get("recent_table", pd.DataFrame())
    prediction_stats = "".join(
        [
            stat_card("prediction_total", prediction_log.get("prediction_total", 0)),
            stat_card("b_rank_win_rate_5d", prediction_log.get("b_rank_win_rate_5d", "—")),
            stat_card("prediction_awaiting", prediction_log.get("prediction_awaiting", 0)),
            stat_card("prediction_suspect", prediction_log.get("prediction_suspect", 0)),
            stat_card("connected_to_signal_score", prediction_log.get("connected_to_signal_score", False)),
        ]
    )
    # 「準備中の分析」行: 蓄積待ち・提案なしのレイヤーを1行ずつに圧縮(壊れていない事の明示)
    _preparing: list[tuple[str, str]] = []
    if not prediction_calibration.get("available"):
        _preparing.append(("確信度と的中率のズレ", "確定した評価の蓄積待ち"))
    if not narrative_reliability.get("available"):
        _preparing.append(("ニュース解釈の信頼性", "確定した評価の蓄積待ち"))
    if not meta_learning.get("available"):
        _preparing.append(("学習パターン分析（メタ学習）", "提案履歴の蓄積待ち"))
    if not auto_calibration.get("available"):
        _preparing.append(("自動較正の候補", "評価データの蓄積待ち"))
    if not human_override.get("available"):
        _preparing.append(("人手オーバーライド分析", "承認判断の履歴待ち"))
    if not weights_patch.get("available"):
        _preparing.append(("重み調整の候補", "候補なし（十分な統計根拠が出るまで提案されません）"))
    if not proposal_adoption.get("available"):
        _preparing.append(("提案の採否記録", "提案がまだありません"))
    preparing_rows = "".join(
        f"<tr><td>{html.escape(name)}</td><td>{html.escape(note)}</td></tr>" for name, note in _preparing
    ) or "<tr><td colspan=2>すべての分析が稼働中です</td></tr>"

    similar_stats = "".join(
        [
            stat_card("similar_narrative_status", similar_narrative.get("similar_narrative_status", "")),
            stat_card("similar_query_date", similar_narrative.get("similar_query_date", "") or "—"),
            stat_card("similar_corpus_days", similar_narrative.get("similar_corpus_days", 0)),
            stat_card("similar_case_rows", similar_narrative.get("similar_case_rows", 0)),
            stat_card("similar_embedding_provider", similar_narrative.get("similar_embedding_provider", "")),
            stat_card("connected_to_signal_score", similar_narrative.get("connected_to_signal_score", False)),
        ]
    )
    ai_counts = ai_summary.get("alignment_counts", {})
    ai_stats = "".join(
        [
            stat_card("latest ai feedback", ai_summary.get("latest_date") or "未取得"),
            stat_card("market_mode_summary", ai_summary.get("market_mode_summary", "AIフィードバック未取得")),
            stat_card("aligned", ai_counts.get("aligned", 0)),
            stat_card("conflicted", ai_counts.get("conflicted", 0)),
            stat_card("neutral", ai_counts.get("neutral", 0)),
            stat_card("insufficient_data", ai_counts.get("insufficient_data", 0)),
        ]
    )
    ai_hypotheses = ai_summary.get("improvement_hypotheses") or ["AIフィードバック未取得"]
    ai_hypothesis_list = "".join(f"<li>{html.escape(str(item))}</li>" for item in ai_hypotheses[:3])
    news_stats = "".join(
        [
            stat_card("latest_news_fetched_at", news_summary.get("latest_news_fetched_at") or "ニュースナラティブ未取得"),
            stat_card("news_fetch_status", news_summary.get("news_fetch_status", "unavailable")),
            stat_card("news_fetch_success_source_count", news_summary.get("news_fetch_success_source_count", 0)),
            stat_card("news_fetch_failed_source_count", news_summary.get("news_fetch_failed_source_count", 0)),
            stat_card("news_fetch_elapsed_seconds", fmt_num(news_summary.get("news_fetch_elapsed_seconds", 0))),
            stat_card("headline_count", news_summary.get("headline_count", 0)),
            stat_card("news_market_bias", news_summary.get("news_market_bias", "insufficient_data")),
            stat_card("news_conflict_score", fmt_num(news_summary.get("news_conflict_score", 0))),
            stat_card("dominant_news_themes", ", ".join(news_summary.get("dominant_news_themes", []) or []) or "なし"),
            stat_card("news_summary_ja", news_summary.get("news_summary_ja", "ニュースナラティブ未取得")),
            stat_card("news_confidence", fmt_num(news_summary.get("news_confidence", 0))),
            stat_card("risk_on_news_score", fmt_num(news_summary.get("risk_on_news_score", 0))),
            stat_card("risk_off_news_score", fmt_num(news_summary.get("risk_off_news_score", 0))),
            stat_card("dollar_strength_news_score", fmt_num(news_summary.get("dollar_strength_news_score", 0))),
            stat_card("rate_pressure_news_score", fmt_num(news_summary.get("rate_pressure_news_score", 0))),
            stat_card("geopolitical_risk_news_score", fmt_num(news_summary.get("geopolitical_risk_news_score", 0))),
            stat_card("oil_supply_risk_news_score", fmt_num(news_summary.get("oil_supply_risk_news_score", 0))),
            stat_card("crypto_liquidity_news_score", fmt_num(news_summary.get("crypto_liquidity_news_score", 0))),
        ]
    )
    news_drivers = news_summary.get("top_news_drivers") or []
    news_driver_list = "".join(
        f"<li>{html.escape(str(item.get('title', item)))}（{html.escape(str(item.get('driver_summary_ja', '分類未確定'))) }）</li>"
        if isinstance(item, dict)
        else f"<li>{html.escape(str(item))}</li>"
        for item in news_drivers[:5]
    )
    if not news_driver_list:
        news_driver_list = "<li>ニュースナラティブ未取得</li>"
    model_state_stats = "".join(
        [
            stat_card("model_state_total_proposals", model_state_summary.get("model_state_total_proposals", 0)),
            stat_card("model_state_increase_count", model_state_summary.get("model_state_increase_count", 0)),
            stat_card("model_state_decrease_count", model_state_summary.get("model_state_decrease_count", 0)),
            stat_card("model_state_hold_count", model_state_summary.get("model_state_hold_count", 0)),
            stat_card("model_state_insufficient_data_count", model_state_summary.get("model_state_insufficient_data_count", 0)),
            stat_card("model_state_audit_status", model_state_summary.get("model_state_audit_status", "unavailable")),
            stat_card("model_state_audit_blocked_count", model_state_summary.get("model_state_audit_blocked_count", 0)),
            stat_card("model_state_audit_warning_count", model_state_summary.get("model_state_audit_warning_count", 0)),
            stat_card("model_state_audit_critical_count", model_state_summary.get("model_state_audit_critical_count", 0)),
            stat_card("model_state_requires_human_review", model_state_summary.get("model_state_requires_human_review", "必須")),
            stat_card("model_state_weights_json_updated", model_state_summary.get("model_state_weights_json_updated", "false")),
            stat_card("model_state_apply_automatically", model_state_summary.get("model_state_apply_automatically", "false")),
        ]
    )
    model_state_strong = pd.DataFrame(model_state_summary.get("strong_candidates", []) or [])
    weights_patch_stats = "".join(
        [
            stat_card("weights_patch_count", weights_patch.get("weights_patch_count", 0)),
            stat_card("weights_patch_excluded_count", weights_patch.get("weights_patch_excluded_count", 0)),
            stat_card("weights_patch_increase_count", weights_patch.get("weights_patch_increase_count", 0)),
            stat_card("weights_patch_decrease_count", weights_patch.get("weights_patch_decrease_count", 0)),
            stat_card("weights_patch_requires_human_approval", weights_patch.get("weights_patch_requires_human_approval", "必須")),
            stat_card("weights_patch_applied", weights_patch.get("weights_patch_applied", "false")),
            stat_card("weights_patch_weights_json_updated", weights_patch.get("weights_patch_weights_json_updated", "false")),
        ]
    )
    weights_patch_candidates = pd.DataFrame(weights_patch.get("patch_candidates", []) or [])
    weights_patch_review_stats = "".join(
        [
            stat_card("weights_patch_review_status", weights_patch_review.get("weights_patch_review_status", "unavailable")),
            stat_card("weights_patch_review_candidate_count", weights_patch_review.get("weights_patch_review_candidate_count", 0)),
            stat_card("weights_patch_review_hold_count", weights_patch_review.get("weights_patch_review_hold_count", 0)),
            stat_card("weights_patch_review_reject_count", weights_patch_review.get("weights_patch_review_reject_count", 0)),
            stat_card("weights_patch_review_blocked_count", weights_patch_review.get("weights_patch_review_blocked_count", 0)),
            stat_card("weights_patch_review_recommended_next_action", weights_patch_review.get("weights_patch_review_recommended_next_action", "no_action")),
            stat_card("weights_patch_review_requires_human_approval", weights_patch_review.get("weights_patch_review_requires_human_approval", "必須")),
            stat_card("weights_patch_review_patch_applied", weights_patch_review.get("weights_patch_review_patch_applied", "false")),
            stat_card("weights_patch_review_weights_json_updated", weights_patch_review.get("weights_patch_review_weights_json_updated", "false")),
        ]
    )
    weights_patch_review_candidates = pd.DataFrame(weights_patch_review.get("candidate_rows", []) or [])
    weights_patch_review_holds = pd.DataFrame(weights_patch_review.get("hold_rows", []) or [])
    proposal_adoption_stats = "".join(
        [
            stat_card("proposal_adoption_tracking_status", proposal_adoption.get("proposal_adoption_tracking_status", "unavailable")),
            stat_card("proposal_adoption_total_count", proposal_adoption.get("proposal_adoption_total_count", 0)),
            stat_card("proposal_adoption_accepted_count", proposal_adoption.get("proposal_adoption_accepted_count", 0)),
            stat_card("proposal_adoption_pending_review_count", proposal_adoption.get("proposal_adoption_pending_review_count", 0)),
            stat_card("proposal_adoption_held_count", proposal_adoption.get("proposal_adoption_held_count", 0)),
            stat_card("proposal_adoption_rejected_count", proposal_adoption.get("proposal_adoption_rejected_count", 0)),
            stat_card("proposal_adoption_blocked_count", proposal_adoption.get("proposal_adoption_blocked_count", 0)),
            stat_card("proposal_adoption_superseded_count", proposal_adoption.get("proposal_adoption_superseded_count", 0)),
            stat_card("proposal_adoption_manual_decision_count", proposal_adoption.get("proposal_adoption_manual_decision_count", 0)),
            stat_card("proposal_adoption_derived_decision_count", proposal_adoption.get("proposal_adoption_derived_decision_count", 0)),
            stat_card("proposal_adoption_recommended_next_action", proposal_adoption.get("proposal_adoption_recommended_next_action", "no_action")),
        ]
    )
    proposal_adoption_pending = pd.DataFrame(proposal_adoption.get("pending_rows", []) or [])
    proposal_adoption_held = pd.DataFrame(proposal_adoption.get("held_rows", []) or [])
    weight_history_stats = "".join(
        [
            stat_card("weight_history_current_version", weight_history.get("weight_history_current_version", "v1")),
            stat_card("weight_history_version_count", weight_history.get("weight_history_version_count", 1)),
            stat_card("weight_history_tracked_count", weight_history.get("weight_history_tracked_count", 0)),
            stat_card("weight_history_held_count", weight_history.get("weight_history_held_count", 0)),
            stat_card("weight_history_candidate_count", weight_history.get("weight_history_candidate_count", 0)),
            stat_card("weight_history_approved_count", weight_history.get("weight_history_approved_count", 0)),
            stat_card("weight_history_rejected_count", weight_history.get("weight_history_rejected_count", 0)),
            stat_card("weight_history_blocked_count", weight_history.get("weight_history_blocked_count", 0)),
            stat_card("weight_history_weights_json_updated", weight_history.get("weight_history_weights_json_updated", "false")),
            stat_card("weight_history_patch_applied", weight_history.get("weight_history_patch_applied", "false")),
            stat_card("weight_history_requires_human_approval", weight_history.get("weight_history_requires_human_approval", "必須")),
        ]
    )
    weight_history_rows = pd.DataFrame(weight_history.get("proposal_rows", []) or [])
    meta_learning_stats = "".join(
        [
            stat_card("meta_learning_status", meta_learning.get("meta_learning_status", "unavailable")),
            stat_card("meta_learning_total_candidates", meta_learning.get("meta_learning_total_candidates", 0)),
            stat_card("meta_learning_success_pattern_count", meta_learning.get("meta_learning_success_pattern_count", 0)),
            stat_card("meta_learning_failure_pattern_count", meta_learning.get("meta_learning_failure_pattern_count", 0)),
            stat_card("meta_learning_neutral_pattern_count", meta_learning.get("meta_learning_neutral_pattern_count", 0)),
            stat_card("meta_learning_insufficient_data_count", meta_learning.get("meta_learning_insufficient_data_count", 0)),
            stat_card("meta_learning_recommended_next_action", meta_learning.get("meta_learning_recommended_next_action", "wait_for_more_data")),
            stat_card("meta_learning_apply_automatically", meta_learning.get("meta_learning_apply_automatically", "false")),
            stat_card("meta_learning_weights_json_updated", meta_learning.get("meta_learning_weights_json_updated", "false")),
            stat_card("meta_learning_patch_applied", meta_learning.get("meta_learning_patch_applied", "false")),
            stat_card("meta_learning_requires_human_approval", meta_learning.get("meta_learning_requires_human_approval", "必須")),
        ]
    )
    meta_learning_success = pd.DataFrame(meta_learning.get("success_rows", []) or [])
    meta_learning_failure = pd.DataFrame(meta_learning.get("failure_rows", []) or [])
    auto_calibration_stats = "".join(
        [
            stat_card("auto_calibration_status", auto_calibration.get("auto_calibration_status", "unavailable")),
            stat_card("auto_calibration_candidate_count", auto_calibration.get("auto_calibration_candidate_count", 0)),
            stat_card("auto_calibration_increase_count", auto_calibration.get("auto_calibration_increase_count", 0)),
            stat_card("auto_calibration_decrease_count", auto_calibration.get("auto_calibration_decrease_count", 0)),
            stat_card("auto_calibration_hold_count", auto_calibration.get("auto_calibration_hold_count", 0)),
            stat_card("auto_calibration_blocked_count", auto_calibration.get("auto_calibration_blocked_count", 0)),
            stat_card("auto_calibration_insufficient_data_count", auto_calibration.get("auto_calibration_insufficient_data_count", 0)),
            stat_card("auto_calibration_recommended_next_action", auto_calibration.get("auto_calibration_recommended_next_action", "wait_for_more_data")),
            stat_card("auto_calibration_requires_human_approval", auto_calibration.get("auto_calibration_requires_human_approval", "必須")),
            stat_card("auto_calibration_patch_applied", auto_calibration.get("auto_calibration_patch_applied", "false")),
            stat_card("auto_calibration_weights_json_updated", auto_calibration.get("auto_calibration_weights_json_updated", "false")),
        ]
    )
    auto_calibration_top = pd.DataFrame(auto_calibration.get("top_candidates", []) or [])
    human_override_stats = "".join(
        [
            stat_card("human_override_status", human_override.get("human_override_status", "unavailable")),
            stat_card("human_override_total_overrides", human_override.get("human_override_total_overrides", 0)),
            stat_card("human_override_accepted_count", human_override.get("human_override_accepted_count", 0)),
            stat_card("human_override_held_count", human_override.get("human_override_held_count", 0)),
            stat_card("human_override_rejected_count", human_override.get("human_override_rejected_count", 0)),
            stat_card("human_override_blocked_count", human_override.get("human_override_blocked_count", 0)),
            stat_card("human_override_positive_count", human_override.get("human_override_positive_count", 0)),
            stat_card("human_override_negative_count", human_override.get("human_override_negative_count", 0)),
            stat_card("human_override_unknown_count", human_override.get("human_override_unknown_count", 0)),
            stat_card("human_override_recommended_next_action", human_override.get("human_override_recommended_next_action", "wait_for_more_data")),
            stat_card("human_override_requires_human_approval", human_override.get("human_override_requires_human_approval", "必須")),
        ]
    )
    human_override_top = pd.DataFrame(human_override.get("top_rows", []) or [])
    portfolio_stats = "".join(
        [
            stat_card("portfolio_status", portfolio_layer.get("portfolio_status", "unavailable")),
            stat_card("portfolio_candidate_assets", portfolio_layer.get("portfolio_candidate_assets", 0)),
            stat_card("portfolio_defensive_assets", portfolio_layer.get("portfolio_defensive_assets", 0)),
            stat_card("portfolio_offensive_assets", portfolio_layer.get("portfolio_offensive_assets", 0)),
            stat_card("portfolio_cash_candidate", fmt_num(portfolio_layer.get("portfolio_cash_candidate", 0))),
            stat_card("portfolio_average_confidence", fmt_num(portfolio_layer.get("portfolio_average_confidence", 0))),
            stat_card("portfolio_concentration", fmt_num(portfolio_layer.get("portfolio_concentration", 0))),
            stat_card("portfolio_risk_concentration", fmt_num(portfolio_layer.get("portfolio_risk_concentration", 0))),
            stat_card("portfolio_recommended_exposure", fmt_num(portfolio_layer.get("portfolio_recommended_exposure", 0))),
            stat_card("portfolio_recommended_next_action", portfolio_layer.get("portfolio_recommended_next_action", "generate_upstream_analysis")),
            stat_card("portfolio_requires_human_approval", portfolio_layer.get("portfolio_requires_human_approval", "必須")),
        ]
    )
    portfolio_top = pd.DataFrame(portfolio_layer.get("top_rows", []) or [])
    pending_stats = "".join(
        [
            stat_card("pending_reevaluation_count", pending_summary.get("pending_reevaluation_count", 0)),
            stat_card("pending_reevaluation_closed_count", pending_summary.get("pending_reevaluation_closed_count", 0)),
            stat_card("pending_reevaluation_open_count", pending_summary.get("pending_reevaluation_open_count", 0)),
            stat_card("pending_reevaluation_no_entry_count", pending_summary.get("pending_reevaluation_no_entry_count", 0)),
            stat_card("pending_reevaluation_missed_count", pending_summary.get("pending_reevaluation_missed_count", 0)),
        ]
    )
    pending_closed = pd.DataFrame(pending_summary.get("recent_closed", []) or [])
    latest_eval_stats = "".join(
        [
            stat_card("latest_evaluation_unique_signal_count", latest_eval_summary.get("latest_evaluation_unique_signal_count", 0)),
            stat_card("latest_evaluation_rows", latest_eval_summary.get("latest_evaluation_rows", 0)),
            stat_card("latest_from_pending_reevaluations", latest_eval_summary.get("latest_from_pending_reevaluations", 0)),
            stat_card("latest_from_evaluations", latest_eval_summary.get("latest_from_evaluations", 0)),
            stat_card("latest_evaluation_closed_count", latest_eval_summary.get("latest_evaluation_closed_count", 0)),
            stat_card("latest_evaluation_pending_count", latest_eval_summary.get("latest_evaluation_pending_count", 0)),
            stat_card("latest_evaluation_open_count", latest_eval_summary.get("latest_evaluation_open_count", 0)),
            stat_card("latest_evaluation_no_entry_count", latest_eval_summary.get("latest_evaluation_no_entry_count", 0)),
            stat_card("latest_evaluation_missed_count", latest_eval_summary.get("latest_evaluation_missed_count", 0)),
        ]
    )
    safe = "".join(f"<li>{html.escape(note)}</li>" for note in SAFETY_NOTES)

    # === ヘッダーピル(信頼と状態の一次情報) ===
    tj = todays_judgements or {}
    perf = performance_series or {}
    gen_date = (generated_at_jst or generated or "")[:10]
    ledger_date = str(tj.get("ledger_date") or "")
    if not tj.get("available"):
        ledger_pill = summary_pill("台帳の記帳", "未取得", "bad")
    elif ledger_date == gen_date:
        ledger_pill = summary_pill("台帳の記帳", f"{ledger_date}(本日分あり)", "good")
    else:
        ledger_pill = summary_pill("台帳の記帳", f"最終 {ledger_date}", "warn")
    _health = str(data_health.get("health_status", "")).strip().lower()
    _health_tone = {"healthy": "good", "watch": "warn", "degraded": "warn", "critical": "bad"}.get(_health, "neutral")
    _health_txt = display_value(_health) if _health else "未取得"
    _mode_raw = str(mode.get("next_week_mode", "")).strip()
    _mode_txt = display_value(_mode_raw) if _mode_raw and _mode_raw.lower() != "not available" else "未取得"
    _mode_tone = {"attack": "good", "aggressive": "good", "defense": "warn", "defensive": "warn", "normal": "neutral"}.get(_mode_raw.lower(), "neutral")
    header_pills = (
        ledger_pill
        + summary_pill("計器の健全性", _health_txt, _health_tone)
        + summary_pill("今週のモード", _mode_txt, _mode_tone)
        + summary_pill("B級 5日勝率(終値)", str(prediction_log.get("b_rank_win_rate_5d", "—")), "good" if prediction_log.get("available") else "neutral")
    )

    # === 01 今日の判断 ===
    if not tj.get("available"):
        today_block = '<div class="empty">台帳(data/signal_log.csv)が読めませんでした。取込フローを確認してください。</div>'
    elif not tj.get("actionable"):
        today_block = f'<div class="empty">{html.escape(ledger_date)} の方向つき判断はありません(全資産 見送り)。</div>'
    else:
        today_block = f'<div class="jgrid">{"".join(judgement_card(r) for r in tj.get("actionable") or [])}</div>'
    stale_note = ""
    if tj.get("available") and ledger_date and ledger_date != gen_date:
        stale_note = (
            f'<p class="notice">⚠ 表示は最終記帳 {html.escape(ledger_date)} 分です。'
            "今朝のレポートを台帳へ取り込むと、ここが本日分に更新されます。</p>"
        )

    # === 02 成績タイル ===
    tiles = perf.get("tiles") or {}
    calib = perf.get("calibration") or {}

    def _tile(k: str, v: str, sub: str = "", cls: str = "") -> str:
        sub_html = f'<div class="t-s">{html.escape(sub)}</div>' if sub else ""
        return f'<div class="tile"><div class="t-k">{html.escape(k)}</div><div class="t-v {cls}">{html.escape(v)}</div>{sub_html}</div>'

    _mean_r = tiles.get("mean_r_5d")
    _mean_cls = "positive" if isinstance(_mean_r, (int, float)) and _mean_r > 0 else "negative" if isinstance(_mean_r, (int, float)) and _mean_r < 0 else ""
    _calib_v = f"{calib['stated_mean']:.2f}→{calib['realized_rate']:.2f}" if calib else "—"
    _calib_s = f"申告→実現(5日勝率)・n={calib['n']}" if calib else "確定データの蓄積待ち"
    tiles_html = "".join([
        _tile("記録した判断", str(tiles.get("total_rows", 0)), "全ランク・全資産"),
        _tile("B級 平均R(5日)", (f"{_mean_r:+.2f}R" if isinstance(_mean_r, (int, float)) else "—"), f"確定 {tiles.get('b_scored', 0)}件", _mean_cls),
        _tile("較正", _calib_v, _calib_s, "accent"),
        _tile("結果待ち", str(tiles.get("awaiting", 0)), "採点地平線が未確定"),
        _tile("採点隔離", str(tiles.get("suspect", 0)), "水準取り違え等を除外"),
    ])
    min_n = prediction_log.get("min_samples", 30)

    # === 03 執行ビュー(到達分のみ) ===
    ev = execution_view or {}
    exec_tiles = ""
    exec_chart = '<p class="notice">到達した判断の確定データがまだありません。</p>'
    exec_windows_html = ""
    exec_reading = ""
    if ev.get("available") and ev.get("fills"):
        _fr = ev.get("fill_rate")
        _fr_txt = f" ({_fr * 100:.0f}%)" if _fr is not None else ""
        _man = ev["capital_pct"]
        exec_tiles = "".join([
            _tile("約定率(到達/発注)", f"{ev['fills']}/{ev['orders']}{_fr_txt}", "risk_pct>0の確定判断のみ"),
            _tile("累積R(到達分)", f"{ev['cum_r']:+.1f}R", f"平均 {ev['avg_r']:+.2f}R/件",
                  "positive" if ev["cum_r"] > 0 else "negative"),
            _tile("資産換算(記帳リスク)", f"{_man:+.2f}%", f"100万円なら約{_man:+.1f}万円",
                  "positive" if _man > 0 else "negative"),
            _tile("最大ドローダウン", f"-{ev['max_dd_r']:.1f}R", "到達分の累積ベース"),
        ])
        exec_chart = cum_r_chart(ev.get("series") or [])
        wrows = ""
        stable_w = None
        for w in ev.get("windows") or []:
            tone = "positive" if w["pos_rate"] >= 0.9 else ""
            if stable_w is None and w["pos_rate"] >= 0.9:
                stable_w = w
            wrows += (
                f"<tr><td>{w['w']}営業日</td><td>{w['n_windows']}</td>"
                f"<td class=\"{tone}\">{w['pos_rate'] * 100:.0f}%</td>"
                f"<td>{w['worst']:+.2f}R</td><td>{w['best']:+.2f}R</td></tr>"
            )
        if wrows:
            exec_windows_html = (
                '<div class="table-wrap"><table class="slim"><thead><tr>'
                '<th>窓幅</th><th>窓の数</th><th>プラス窓率</th><th>最悪の窓</th><th>最良の窓</th>'
                f"</tr></thead><tbody>{wrows}</tbody></table></div>"
            )
        else:
            exec_windows_html = '<p class="notice">窓を作れるだけの記帳日数がまだありません。</p>'
        if stable_w:
            _all_pos = stable_w["pos_rate"] >= 1.0
            _rate_txt = "すべて" if _all_pos else f"{stable_w['pos_rate'] * 100:.0f}%"
            exec_reading = (
                f'<p class="notice"><b>読み方:</b> これまでの実績では、{stable_w["w"]}営業日の窓({stable_w["n_windows"]}本)の'
                f'{_rate_txt}が差し引きプラスでした(最悪の窓 {stable_w["worst"]:+.2f}R)。'
                "この安定性が窓の数を増やしても崩れないかが、リスク許容度を上げる判断材料になります。"
                "窓数が少ないうちは偶然の寄与が大きい点に注意。</p>"
            )
    exec_note = (
        '<p class="notice">終値基準の方向採点で、SL/TP執行は再現していません。到達判定は当日タッチを拾えないため、'
        "同日中に約定して損切りになった判断が「未到達」側に落ち、この枠の成績はその分よく見えます"
        "(判定の修正が別途進行中。反映されると自動で正確になります)。スプレッド等のコストは未控除です。</p>"
    )

    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tactical Swing OS</title>
  <style>{PAGE_CSS}</style>
</head>
<body>
  <div id="tooltip" role="status"></div>
  <div class="topbar"><div class="topbar-in">
    <span class="brand">Tactical Swing OS<small>研究用・実売買なし</small></span>
    <nav class="jump">
      <a href="#today">今日</a><a href="#perf">成績</a><a href="#exec">執行</a><a href="#verify">検証</a><a href="#health">健康</a><a href="#lab">研究ログ</a>
    </nav>
    <span class="gen">{html.escape(generated_at_jst or generated)}</span>
    <button id="theme-toggle" type="button">表示切替</button>
  </div></div>
  <main class="wrap">
    <div class="pills">{header_pills}</div>

    <h2 class="sec" id="today"><span class="n">01</span>今日の判断 <span class="muted" style="font-size:12px; font-weight:600">記帳日 {html.escape(ledger_date or "—")}</span></h2>
    <p class="sec-sub">手動予測台帳の最新記帳。entry帯へ価格が到達した場合のみ検討する監視案であり、成行の指示ではありません。最終判断は人間が行います。</p>
    {stale_note}
    {today_block}
    <section class="card"><h2>見送り(NO_TRADE)</h2>{no_trade_strip(tj.get("no_trade") or [])}</section>
    <section class="card"><h2>前営業日の答え合わせ</h2>{prev_results_html(tj)}</section>

    <h2 class="sec" id="perf"><span class="n">02</span>成績と較正</h2>
    <p class="sec-sub">終値基準の方向採点です(SL/TP執行の再現ではありません)。判断数が{min_n}件未満の集計は「データ不足」として断定しません。</p>
    <div class="tiles">{tiles_html}</div>
    <div class="charts">
      <section class="card"><h2>B級判断の累積R(5日終値基準)</h2>{cum_r_chart(perf.get("cum_r") or [])}</section>
      <section class="card"><h2>地平線別勝率(B級)</h2>{horizon_chart(perf.get("horizon_win") or [])}</section>
    </div>
    <section class="card"><h2>予測ノートの成績</h2><p class="notice">毎朝の相場判断(買い・売り・見送り)をすべて記録し、1・3・5・10営業日後の実際の値動きで採点しています。見送りも採点対象です。</p>{'<div class="empty">予測ノート未取得</div>' if not prediction_log.get('available') else f'<div class="grid">{prediction_stats}</div>'}<h3>ランク別の成績(A=自信あり / B=監視 / NO_TRADE=見送り)</h3>{table_html(prediction_rank_table, ["rank", "judgements", "with_levels", "win_5d", "win_10d", "mean_r_5d", "basis"], "採点データなし")}<h3>直近の判断(新しい順)</h3>{table_html(prediction_recent_table, ["date", "asset", "side", "rank", "r_close_5d", "r_close_10d", "result_5d", "status"], "判断記録なし")}</section>

    <h2 class="sec" id="exec"><span class="n">03</span>執行ビュー(到達分のみ)</h2>
    <p class="sec-sub">「朝に指値を出したもの」(risk_pct&gt;0)のうち、entry帯へ実際に価格が到達した判断だけの損益ビューです。未到達の判断はここには入りません。</p>
    {exec_note}
    <div class="tiles">{exec_tiles}</div>
    <div class="charts">
      <section class="card"><h2>到達分の累積R(5日終値基準)</h2>{exec_chart}</section>
      <section class="card"><h2>安定性 — 移動窓の正味R(記帳日ベース)</h2>{exec_windows_html}{exec_reading}</section>
    </div>

    <details class="group" id="verify"><summary><span class="n" style="color:var(--accent)">04</span> 検証 — 予測は当たっているか<span class="g-sub">評価・理由コード・見送り検証・類似局面・内部エンジン</span></summary><div class="g-body">
    <section class="card"><h2>過去シグナルの結果まとめ(内部エンジン)</h2><div class="grid">{eval_stats}</div></section>
    <section class="card"><h2>直近の評価結果</h2>{'<div class="empty">最新評価ビュー未取得</div>' if not latest_eval_summary.get('available') else f'<div class="grid">{latest_eval_stats}</div>'}</section>
    <section class="card"><h2>結果待ちのシグナル</h2>{'<div class="empty">Pending再評価未取得</div>' if not pending_summary.get('available') else f'<div class="grid">{pending_stats}</div>'}<h3>直近決着シグナル上位5件</h3>{table_html(pending_closed, ["signal_id", "asset", "side", "rank", "previous_outcome", "outcome", "r_multiple", "error_type"], "直近決着シグナルなし")}</section>
    <section class="card"><h2>資産別成績</h2>{table_html(asset_table, ["asset", "signals", "evaluations", "win_rate", "total_r", "average_r", "missed_opportunity_count"])}</section>
    <section class="card"><h2>判断理由ごとの成績(どの根拠が当たるか)</h2><h3>プラス寄与が大きい理由</h3>{table_html(top_positive, ["reason_code", "signals_count", "evaluated_count", "win_rate", "average_r", "total_r", "reliability_label"])}<h3>マイナス寄与が大きい理由</h3>{table_html(top_negative, ["reason_code", "signals_count", "evaluated_count", "win_rate", "average_r", "total_r", "reliability_label"])}<h3>データ不足</h3>{table_html(insufficient, ["reason_code", "signals_count", "evaluated_count", "win_rate", "average_r", "total_r", "reliability_label"])}</section>
    <section class="card"><h2>見送り判断の検証(見送って正解だったか)</h2>{table_html(no_trade_table, ["no_trade_reason", "count", "missed_opportunity_count", "average_mfe_r", "assessment"], "見送り理由データなし")}</section>
    <section class="card"><h2>今日と似た過去の局面</h2><p class="notice">過去ニュース局面との意味的類似検索です。表示・記録のみで signal score には接続していません。</p>{'<div class="empty">類似局面検索 未取得(Narrative Memory 蓄積待ち)</div>' if not similar_narrative.get('available') else f'<div class="grid">{similar_stats}</div>'}<h3>類似局面と 5/10/20営業日後の実リターン</h3>{table_html(similar_table, ["similar_rank", "similar_date", "similarity", "asset", "fwd_return_5d", "fwd_return_10d", "fwd_return_20d", "outcome_status"], "類似局面なし(データ蓄積で自動表示)")}</section>
    <section class="card"><h2>資産配分の目安</h2>{'<div class="empty">ポートフォリオ層未取得</div>' if not portfolio_layer.get('available') else f'<div class="grid">{portfolio_stats}</div>'}<h3>配分候補 上位</h3>{table_html(portfolio_top, ["asset", "allocation_score", "portfolio_weight_candidate", "confidence", "risk_class", "risk_role", "recommended_exposure", "cash_ratio_candidate", "latest_rank", "latest_side", "rationale"], "配分候補なし")}</section>
    <section class="card"><h2>参考: 内部シグナルエンジンの当日候補</h2><p class="notice">ライブ評価ループ(generate_signal)の出力です。台帳の記帳判断とは別系統の研究用シグナルです。</p><div class="grid">{signal_stats}</div>{table_html(signals, ["asset", "side", "rank", "type", "recommended_action", "signal_strength", "setup_quality_score", "entry_quality_score", "direction_confidence", "reason_codes", "no_trade_reason"])}</section>
    <section class="card"><h2>今週・今月のリスク上限モード</h2><div class="grid">{mode_stats}</div></section>
    </div></details>

    <details class="group" id="health"><summary><span class="n" style="color:var(--accent)">05</span> システムの健康<span class="g-sub">このデータを信じてよいか — 鮮度・監査・安全チェック</span></summary><div class="g-body">
    <section class="card"><h2>データの鮮度チェック</h2><p class="notice">古い(stale)・空(empty)・欠損(missing)のデータを正常と誤読しないためのガードです。</p>{'<div class="empty">Data Health未取得</div>' if not data_health.get('available') else f'<div class="grid">{data_health_stats}</div>'}<h3>レイヤー別 鮮度</h3>{table_html(data_health_table, ["layer", "status", "last_generated", "age_hours", "row_count", "threshold_hours", "cadence"], "レイヤー情報なし")}</section>
    <section class="card"><h2>時刻の整合性チェック</h2>{'<div class="empty">Datetime Audit未取得</div>' if not datetime_health.get('available') else f'<div class="grid">{datetime_stats}</div>'}</section>
    <section class="card"><h2>システム状態</h2><div class="grid">{system_stats}</div></section>
    <section class="card"><h2>自動安全チェック(危険な提案の検出)</h2><p class="notice">提案レイヤーを横断レビューし、自動適用違反・サンプル不足・過剰最適化・矛盾を検出する敵対的監査です。警告のみで自動適用しません。</p>{'<div class="empty">Adversarial Review未取得</div>' if not adversarial_review.get('available') else f'<div class="grid">{adversarial_review_stats}</div>'}<h3>停止 / 高リスク / 警告 の詳細</h3>{table_html(adversarial_review_table[adversarial_review_table['severity'].isin(['warning', 'high_risk', 'blocked'])] if (not adversarial_review_table.empty and 'severity' in adversarial_review_table.columns) else adversarial_review_table, ["source_type", "target", "finding_category", "severity", "evidence", "recommended_action"], "危険兆候の検出なし(または未取得)")}</section>
    <section class="card"><h2>未来情報の混入チェック(後出し防止)</h2>{'<div class="empty">Narrative Lookahead Audit未取得</div>' if not narrative_lookahead.get('available') else f'<div class="grid">{narrative_lookahead_stats}</div>'}<h3>警告 / 高リスク / 停止 の詳細</h3>{table_html(narrative_lookahead_table[narrative_lookahead_table['lookahead_risk_level'].isin(['warning', 'high_risk', 'blocked'])] if (not narrative_lookahead_table.empty and 'lookahead_risk_level' in narrative_lookahead_table.columns) else narrative_lookahead_table, ["source_type", "source_timing_class", "lookahead_risk_level", "lookahead_score", "issue_type", "detected_terms", "recommended_action", "text_excerpt"], "混入検出なし(または未取得)")}</section>
    <section class="card"><h2>監査レポート</h2><div class="grid">{audit_report_stats}</div></section>
    <section class="card"><h2>準備中の分析(データが貯まると自動で動き出します)</h2><p class="notice">以下は蓄積待ちであり、壊れているのではありません。</p><div class="table-wrap"><table class="slim"><thead><tr><th>分析</th><th>状態</th></tr></thead><tbody>{preparing_rows}</tbody></table></div></section>
    </div></details>

    <details class="group" id="lab"><summary><span class="n" style="color:var(--accent)">06</span> 研究ログ(開発者向け)<span class="g-sub">較正・ニュース・重み提案・メタ学習・監査の内部データ</span></summary><div class="g-body">
    <section class="card"><h2>確信度と的中率のズレ(キャリブレーション)</h2>{'<div class="empty">Prediction Calibration未取得</div>' if not prediction_calibration.get('available') else f'<div class="grid">{prediction_calibration_stats}</div>'}<h3>Rank別キャリブレーション</h3>{table_html(prediction_calibration_table, ["rank", "implied_probability", "closed_count", "hit_rate", "calibration_gap", "brier_score", "p_value", "calibration_verdict", "recommended_action"], "キャリブレーションデータなし")}</section>
    <section class="card"><h2>ニュース解釈の信頼性</h2>{'<div class="empty">Narrative Reliability未取得</div>' if not narrative_reliability.get('available') else f'<div class="grid">{narrative_reliability_stats}</div>'}<h3>ナラティブ別信頼性</h3>{table_html(narrative_reliability_table, ["narrative", "closed_count", "win_rate", "average_r", "p_value", "reliability_label", "recommended_action"], "ナラティブ信頼性データなし")}</section>
    <section class="card"><h2>ニュース要約(材料の整理)</h2><div class="grid">{news_stats}</div><h3>Top News Drivers</h3><ul>{news_driver_list}</ul></section>
    <section class="card"><h2>AIの自己改善メモ</h2><div class="grid">{ai_stats}</div><h3>上位の改善仮説</h3><ul>{ai_hypothesis_list}</ul></section>
    <section class="card"><h2>取引コストモデル</h2>{transaction_cost_warning_html}<div class="grid">{transaction_cost_stats}</div></section>
    <section class="card"><h2>ルール改善候補</h2><p class="notice">すべての改善候補は自動適用されません: <strong>{str(apply_false).lower()}</strong></p>{table_html(rule_view, ["proposal_type", "target_type", "target_name", "proposal_strength", "priority", "average_r", "win_rate", "proposed_change", "apply_automatically"])}</section>
    <section class="card"><h2>モデル状態 更新提案</h2>{'<div class="empty">Model State更新提案未取得</div>' if not model_state_summary.get('available') else f'<div class="grid">{model_state_stats}</div>'}<h3>strong候補 上位5件</h3>{table_html(model_state_strong, ["category", "target", "sample_count", "win_rate", "avg_r", "proposal_direction", "proposal_strength", "proposed_delta", "proposed_weight", "rationale"], "strong候補なし")}</section>
    <section class="card"><h2>重み調整パッチ候補</h2>{'<div class="empty">Weights Patch候補未取得</div>' if not weights_patch.get('available') else f'<div class="grid">{weights_patch_stats}</div>'}<h3>patch候補 上位5件</h3>{table_html(weights_patch_candidates, ["weight_path", "patch_action", "current_weight", "proposed_delta", "proposed_value", "proposal_direction", "proposal_strength", "rationale"], "patch候補なし")}</section>
    <section class="card"><h2>重み調整パッチ レビュー</h2>{'<div class="empty">Weights Patchレビュー未取得</div>' if not weights_patch_review.get('available') else f'<div class="grid">{weights_patch_review_stats}</div>'}<h3>承認候補 上位5件</h3>{table_html(weights_patch_review_candidates, ["weight_path", "review_decision", "recommended_human_action", "sample_count", "confidence_level", "proposal_strength", "proposed_delta", "patch_risk_level", "review_reason"], "承認候補なし")}<h3>保留候補 上位5件</h3>{table_html(weights_patch_review_holds, ["weight_path", "review_decision", "recommended_human_action", "sample_count", "confidence_level", "proposal_strength", "proposed_delta", "evidence_quality", "missing_conditions", "review_reason"], "保留候補なし")}</section>
    <section class="card"><h2>提案採否トラッキング</h2>{'<div class="empty">Proposal Adoption Tracking未取得</div>' if not proposal_adoption.get('available') else f'<div class="grid">{proposal_adoption_stats}</div>'}<h3>承認判断待ち 上位5件</h3>{table_html(proposal_adoption_pending, ["weight_path", "adoption_status", "adoption_source", "recommended_next_action", "sample_count", "confidence_level", "proposal_strength", "tracking_reason"], "承認判断待ちなし")}<h3>保留中 上位5件</h3>{table_html(proposal_adoption_held, ["weight_path", "adoption_status", "adoption_source", "recommended_next_action", "sample_count", "confidence_level", "proposal_strength", "tracking_reason"], "保留中なし")}</section>
    <section class="card"><h2>重みバージョン履歴</h2>{'<div class="empty">Weight Version History未取得</div>' if not weight_history.get('available') else f'<div class="grid">{weight_history_stats}</div>'}<h3>Proposal一覧 上位5件</h3>{table_html(weight_history_rows, ["version_id", "source", "proposal_id", "review_decision", "adoption_status", "description", "weights_json_updated", "patch_applied", "requires_human_approval", "notes"], "履歴Proposalなし")}</section>
    <section class="card"><h2>メタ学習</h2>{'<div class="empty">Meta Learning未取得</div>' if not meta_learning.get('available') else f'<div class="grid">{meta_learning_stats}</div>'}<h3>成功パターン候補 上位5件</h3>{table_html(meta_learning_success, ["meta_learning_id", "pattern_type", "category", "target", "proposal_id", "impact_score", "sample_count", "confidence_level", "recommended_action", "learning_hypothesis"], "成功パターン候補なし")}<h3>失敗パターン候補 上位5件</h3>{table_html(meta_learning_failure, ["meta_learning_id", "pattern_type", "category", "target", "proposal_id", "impact_score", "sample_count", "confidence_level", "recommended_action", "learning_hypothesis"], "失敗パターン候補なし")}</section>
    <section class="card"><h2>自動較正の候補</h2>{'<div class="empty">Auto Calibration Candidates未取得</div>' if not auto_calibration.get('available') else f'<div class="grid">{auto_calibration_stats}</div>'}<h3>確信度の高い候補 上位</h3>{table_html(auto_calibration_top, ["candidate_id", "asset", "category", "target", "factor", "classification", "current_value", "suggested_delta", "suggested_value", "confidence", "sample_size", "source", "rationale"], "候補なし")}</section>
    <section class="card"><h2>人手オーバーライド分析</h2>{'<div class="empty">Human Override Analytics未取得</div>' if not human_override.get('available') else f'<div class="grid">{human_override_stats}</div>'}<h3>override impact 上位5件</h3>{table_html(human_override_top, ["proposal_id", "review_decision", "adoption_status", "override_type", "override_reason", "impact_status", "impact_score", "source", "recommended_next_action"], "override分析なし")}</section>
    </div></details>

    <footer class="foot"><b>安全上の注意</b> — {html.escape(DASHBOARD_DESCRIPTION)}<ul>{safe}</ul></footer>
  </main>
  <script type="application/json" id="dashboard-summary">{html.escape(json.dumps(summary, ensure_ascii=False))}</script>
  <script>{PAGE_JS}</script>
</body>
</html>
"""
