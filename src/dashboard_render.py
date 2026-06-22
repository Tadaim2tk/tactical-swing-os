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
    apply_false: bool,
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
    # === ひとめ要約バナー（投資判断の最優先サマリを最上部に） ===
    def _pill(label: str, value: str, tone: str) -> str:
        return (
            f'<span class="summary-pill pill-{tone}">'
            f'<span class="pill-k">{html.escape(label)}</span>'
            f'<span class="pill-v">{html.escape(value)}</span></span>'
        )

    _health = str(data_health.get("health_status", "")).strip().lower()
    _health_tone = {"healthy": "good", "watch": "warn", "degraded": "warn", "critical": "bad"}.get(_health, "neutral")
    _health_txt = display_value(_health) if _health else "未取得"
    _a = int(numeric_or(signal_counts.get("A", 0), 0))
    _b = int(numeric_or(signal_counts.get("B", 0), 0))
    _nt = int(numeric_or(signal_counts.get("NO_TRADE", 0), 0))
    _sig_txt = f"シグナル候補 {_a + _b} / 見送り {_nt}"
    _sig_tone = "warn" if (_a + _b) > 0 else "neutral"
    _mat = str(eval_summary.get("evaluation_maturity", "")).strip().lower()
    _closed = int(numeric_or(eval_summary.get("closed", 0), 0))
    _mat_txt = {"no_signals": "データなし", "accumulating": "蓄積中", "active": "活動中"}.get(_mat, _mat or "未取得")
    _mat_tone = {"active": "good", "accumulating": "warn", "no_signals": "neutral"}.get(_mat, "neutral")
    _eval_txt = f"{_mat_txt}（決着 {_closed}）"
    _mode_raw = str(mode.get("next_week_mode", "")).strip()
    _mode_txt = display_value(_mode_raw) if _mode_raw and _mode_raw.lower() != "not available" else "未取得"
    _mode_tone = {"attack": "good", "aggressive": "good", "defense": "warn", "defensive": "warn", "normal": "neutral"}.get(_mode_raw.lower(), "neutral")
    summary_banner = (
        '<section class="summary-banner">'
        + _pill("計器の健全性", _health_txt, _health_tone)
        + _pill("当日シグナル", _sig_txt, _sig_tone)
        + _pill("評価の蓄積", _eval_txt, _mat_tone)
        + _pill("今週のモード", _mode_txt, _mode_tone)
        + "</section>"
    )

    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tactical Swing OS ダッシュボード</title>
  <style>
    :root {{ color-scheme: dark; --bg:#0b1020; --panel:#121a2e; --panel2:#17213a; --text:#edf2ff; --muted:#98a6c7; --line:#263553; --pos:#65d98c; --neg:#ff7b86; --warn:#ffd166; --accent:#7aa2ff; }}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background:var(--bg); color:var(--text); }}
    header {{ padding:28px; background:linear-gradient(135deg, #111b35, #0c1224); border-bottom:1px solid var(--line); }}
    h1 {{ margin:0 0 10px; font-size:28px; }}
    h2 {{ margin:0 0 14px; font-size:18px; }}
    h3 {{ margin:18px 0 10px; font-size:14px; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; }}
    main {{ padding:20px; display:grid; gap:18px; }}
    .meta {{ display:flex; flex-wrap:wrap; gap:10px; color:var(--muted); font-size:13px; }}
    .lead {{ margin:14px 0 0; max-width:960px; color:var(--muted); line-height:1.7; }}
    .card {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:16px; box-shadow:0 8px 24px rgba(0,0,0,.18); }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(160px,1fr)); gap:10px; }}
    .stat {{ background:var(--panel2); border:1px solid var(--line); border-radius:8px; padding:12px; }}
    .stat-label {{ color:var(--muted); font-size:12px; }}
    .stat-value {{ margin-top:6px; font-size:20px; font-weight:700; }}
    .table-wrap {{ overflow-x:auto; border:1px solid var(--line); border-radius:8px; }}
    table {{ width:100%; border-collapse:collapse; min-width:720px; }}
    th, td {{ padding:9px 10px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; font-size:13px; }}
    th {{ color:var(--muted); background:#10182b; position:sticky; top:0; }}
    tr:hover td {{ background:rgba(122,162,255,.05); }}
    .badge {{ display:inline-flex; align-items:center; border-radius:999px; padding:2px 8px; font-size:12px; font-weight:700; background:#273554; color:#dbe6ff; }}
    .badge-a, .badge-trade, .badge-strong_positive, .badge-positive {{ background:rgba(101,217,140,.16); color:var(--pos); }}
    .badge-b, .badge-watch, .badge-medium {{ background:rgba(255,209,102,.16); color:var(--warn); }}
    .badge-no_trade, .badge-none, .badge-data_insufficient, .badge-insufficient_data {{ background:rgba(152,166,199,.16); color:var(--muted); }}
    .badge-strong_negative, .badge-negative, .badge-high {{ background:rgba(255,123,134,.16); color:var(--neg); }}
    .positive {{ color:var(--pos); font-weight:700; }}
    .negative {{ color:var(--neg); font-weight:700; }}
    .neutral {{ color:var(--muted); }}
    .empty {{ color:var(--muted); padding:14px; border:1px dashed var(--line); border-radius:8px; }}
    .notice {{ color:var(--muted); margin:8px 0 12px; }}
    ul {{ margin:8px 0 0; padding-left:20px; color:var(--muted); }}
    .summary-banner {{ display:flex; flex-wrap:wrap; gap:12px; padding:16px; background:var(--panel); border:1px solid var(--line); border-radius:8px; }}
    .summary-pill {{ display:flex; flex-direction:column; gap:3px; padding:10px 16px; border-radius:10px; border:1px solid var(--line); background:var(--panel2); min-width:140px; }}
    .summary-pill .pill-k {{ font-size:11px; color:var(--muted); letter-spacing:.04em; }}
    .summary-pill .pill-v {{ font-size:17px; font-weight:800; }}
    .pill-good {{ border-color:rgba(101,217,140,.55); }} .pill-good .pill-v {{ color:var(--pos); }}
    .pill-warn {{ border-color:rgba(255,209,102,.55); }} .pill-warn .pill-v {{ color:var(--warn); }}
    .pill-bad {{ border-color:rgba(255,123,134,.65); }} .pill-bad .pill-v {{ color:var(--neg); }}
    .pill-neutral .pill-v {{ color:var(--text); }}
    h2.tier {{ margin:14px 0 0; padding:10px 14px; font-size:16px; border-left:4px solid var(--accent); background:rgba(122,162,255,.10); border-radius:4px; color:var(--text); }}
    details.tier4 > summary {{ cursor:pointer; padding:10px 14px; font-size:15px; font-weight:700; border-left:4px solid var(--muted); background:rgba(152,166,199,.10); border-radius:4px; color:var(--muted); }}
    details.tier4[open] > summary {{ margin-bottom:14px; }}
    details.tier4 > section.card {{ margin-top:14px; }}
  </style>
</head>
<body>
  <header>
    <h1>Tactical Swing OS ダッシュボード</h1>
    <div class="meta">
      <span>生成日時（JST）: {html.escape(generated_at_jst or generated)}</span>
      <span>Actions実行時刻（UTC）: {html.escape(generated_at_utc)}</span>
      <span>データ基準日: {html.escape(display_optional(data_reference_date))}</span>
      <span>データソース: {html.escape(display_source(source))}</span>
      <span>最新シグナル日: {html.escape(display_optional(latest_dates["latest_signal_date"]))}</span>
      <span>最新評価日: {html.escape(display_optional(latest_dates["latest_evaluation_date"]))}</span>
    </div>
    <p class="lead">{html.escape(DASHBOARD_DESCRIPTION)}</p>
  </header>
    <main>
    {summary_banner}

    <h2 class="tier">① 当日の判断材料</h2>
    <section class="card"><h2>本日のシグナル概要</h2><div class="grid">{signal_stats}</div>{table_html(signals, ["asset","side","rank","type","recommended_action","signal_strength","setup_quality_score","entry_quality_score","direction_confidence","reason_codes","no_trade_reason"])}</section>
    <section class="card"><h2>今週・今月のモード（リスク上限）</h2><div class="grid">{mode_stats}</div></section>
    <section class="card"><h2>評価概要</h2><div class="grid">{eval_stats}</div></section>
    <section class="card"><h2>最新評価ビュー 要約</h2>{'<div class="empty">最新評価ビュー未取得</div>' if not latest_eval_summary.get('available') else f'<div class="grid">{latest_eval_stats}</div>'}</section>
    <section class="card"><h2>Pending再評価 要約</h2>{'<div class="empty">Pending再評価未取得</div>' if not pending_summary.get('available') else f'<div class="grid">{pending_stats}</div>'}<h3>直近決着シグナル上位5件</h3>{table_html(pending_closed, ["signal_id","asset","side","rank","previous_outcome","outcome","r_multiple","error_type"], "直近決着シグナルなし")}</section>
    <section class="card"><h2>資産別成績</h2>{table_html(asset_table, ["asset","signals","evaluations","win_rate","total_r","average_r","missed_opportunity_count"])}</section>
    <section class="card"><h2>ポートフォリオ層</h2>{'<div class="empty">ポートフォリオ層未取得</div>' if not portfolio_layer.get('available') else f'<div class="grid">{portfolio_stats}</div>'}<h3>配分候補 上位</h3>{table_html(portfolio_top, ["asset","allocation_score","portfolio_weight_candidate","confidence","risk_class","risk_role","recommended_exposure","cash_ratio_candidate","latest_rank","latest_side","rationale"], "配分候補なし")}</section>

    <h2 class="tier">② 信頼性チェック（この出力を信じてよいか）</h2>
    <section class="card"><h2>データ健全性（鮮度）</h2><p class="notice">各分析レイヤーの最終生成時刻・行数・鮮度を一覧化します。古い(stale)・空(empty)・欠損(missing)・unavailableなデータを正常と誤読しないためのガードです。表示専用でweights.jsonは更新しません。</p>{'<div class="empty">Data Health未取得</div>' if not data_health.get('available') else f'<div class="grid">{data_health_stats}</div>'}<h3>レイヤー別 鮮度</h3>{table_html(data_health_table, ["layer","status","last_generated","age_hours","row_count","threshold_hours","cadence"], "レイヤー情報なし")}</section>
    <section class="card"><h2>システム整合性（日時監査）</h2>{'<div class="empty">Datetime Audit未取得</div>' if not datetime_health.get('available') else f'<div class="grid">{datetime_stats}</div>'}</section>
    <section class="card"><h2>システム状態</h2><div class="grid">{system_stats}</div></section>
    <section class="card"><h2>敵対的レビュー（提案の危険兆候）</h2><p class="notice">提案レイヤー(Rule/Model State/Weights Patch/Auto Calibration/AI Feedback)を横断レビューし、自動適用違反・サンプル不足・過剰最適化・矛盾・過信表現を検出する敵対的監査です。自動適用せず警告のみ。weights.jsonも更新しません。</p>{'<div class="empty">Adversarial Review未取得</div>' if not adversarial_review.get('available') else f'<div class="grid">{adversarial_review_stats}</div>'}<h3>停止 / 高リスク / 警告 の詳細</h3>{table_html(adversarial_review_table[adversarial_review_table['severity'].isin(['warning','high_risk','blocked'])] if (not adversarial_review_table.empty and 'severity' in adversarial_review_table.columns) else adversarial_review_table, ["source_type","target","finding_category","severity","evidence","recommended_action"], "危険兆候の検出なし(または未取得)")}</section>
    <section class="card"><h2>未来情報の混入監査</h2><p class="notice">ニュース/AI要約への未来情報・評価結果の混入を検出する研究プロセス監査です。自動売買判断ではなく、weights.jsonも更新しません。</p>{'<div class="empty">Narrative Lookahead Audit未取得</div>' if not narrative_lookahead.get('available') else f'<div class="grid">{narrative_lookahead_stats}</div>'}<h3>警告 / 高リスク / 停止 の詳細</h3>{table_html(narrative_lookahead_table[narrative_lookahead_table['lookahead_risk_level'].isin(['warning','high_risk','blocked'])] if (not narrative_lookahead_table.empty and 'lookahead_risk_level' in narrative_lookahead_table.columns) else narrative_lookahead_table, ["source_type","source_timing_class","lookahead_risk_level","lookahead_score","issue_type","detected_terms","recommended_action","text_excerpt"], "混入検出なし(または未取得)")}</section>
    <section class="card"><h2>監査レポート</h2><p class="notice">統合状態確認用のシステム監査です。</p><div class="grid">{audit_report_stats}</div></section>

    <h2 class="tier">③ AI判断の質</h2>
    <section class="card"><h2>予測キャリブレーション（確信度の正確さ）</h2><p class="notice">AIの確信度を採点する分析専用層です。weights.jsonは更新しません。</p>{'<div class="empty">Prediction Calibration未取得</div>' if not prediction_calibration.get('available') else f'<div class="grid">{prediction_calibration_stats}</div>'}<h3>Rank別キャリブレーション</h3>{table_html(prediction_calibration_table, ["rank","implied_probability","closed_count","hit_rate","calibration_gap","brier_score","p_value","calibration_verdict","recommended_action"], "キャリブレーションデータなし")}</section>
    <section class="card"><h2>ナラティブ信頼性</h2><p class="notice">ナラティブの統計的信頼性を検定する分析専用層です。weights.jsonは更新しません。</p>{'<div class="empty">Narrative Reliability未取得</div>' if not narrative_reliability.get('available') else f'<div class="grid">{narrative_reliability_stats}</div>'}<h3>ナラティブ別信頼性</h3>{table_html(narrative_reliability_table, ["narrative","closed_count","win_rate","average_r","p_value","reliability_label","recommended_action"], "ナラティブ信頼性データなし")}</section>
    <section class="card"><h2>判断理由コード別成績</h2><h3>プラス寄与が大きい理由</h3>{table_html(top_positive, ["reason_code","signals_count","evaluated_count","win_rate","average_r","total_r","reliability_label"])}<h3>マイナス寄与が大きい理由</h3>{table_html(top_negative, ["reason_code","signals_count","evaluated_count","win_rate","average_r","total_r","reliability_label"])}<h3>データ不足</h3>{table_html(insufficient, ["reason_code","signals_count","evaluated_count","win_rate","average_r","total_r","reliability_label"])}</section>
    <section class="card"><h2>見送り理由分析</h2>{table_html(no_trade_table, ["no_trade_reason","count","missed_opportunity_count","average_mfe_r","assessment"], "見送り理由データなし")}</section>
    <section class="card"><h2>ニュースナラティブ要約</h2><div class="grid">{news_stats}</div><h3>Top News Drivers</h3><ul>{news_driver_list}</ul></section>
    <section class="card"><h2>AIフィードバック要約</h2><div class="grid">{ai_stats}</div><h3>上位の改善仮説</h3><ul>{ai_hypothesis_list}</ul></section>
    <section class="card"><h2>取引コストモデル</h2><p class="notice">ネットR評価のための分析専用モデルです。実売買・発注は行いません。</p>{transaction_cost_warning_html}<div class="grid">{transaction_cost_stats}</div></section>

    <details class="tier4"><summary>④ 研究の内部機構（提案・パッチ・履歴・学習。クリックで展開）</summary>
    <section class="card"><h2>ルール改善候補</h2><p class="notice">すべての改善候補は自動適用されません: <strong>{str(apply_false).lower()}</strong></p>{table_html(rule_view, ["proposal_type","target_type","target_name","proposal_strength","priority","average_r","win_rate","proposed_change","apply_automatically"])}</section>
    <section class="card"><h2>モデル状態 更新提案</h2>{'<div class="empty">Model State更新提案未取得</div>' if not model_state_summary.get('available') else f'<div class="grid">{model_state_stats}</div>'}<h3>strong候補 上位5件</h3>{table_html(model_state_strong, ["category","target","sample_count","win_rate","avg_r","proposal_direction","proposal_strength","proposed_delta","proposed_weight","rationale"], "strong候補なし")}</section>
    <section class="card"><h2>重み調整パッチ候補</h2>{'<div class="empty">Weights Patch候補未取得</div>' if not weights_patch.get('available') else f'<div class="grid">{weights_patch_stats}</div>'}<h3>patch候補 上位5件</h3>{table_html(weights_patch_candidates, ["weight_path","patch_action","current_weight","proposed_delta","proposed_value","proposal_direction","proposal_strength","rationale"], "patch候補なし")}</section>
    <section class="card"><h2>重み調整パッチ レビュー</h2>{'<div class="empty">Weights Patchレビュー未取得</div>' if not weights_patch_review.get('available') else f'<div class="grid">{weights_patch_review_stats}</div>'}<h3>承認候補 上位5件</h3>{table_html(weights_patch_review_candidates, ["weight_path","review_decision","recommended_human_action","sample_count","confidence_level","proposal_strength","proposed_delta","patch_risk_level","review_reason"], "承認候補なし")}<h3>保留候補 上位5件</h3>{table_html(weights_patch_review_holds, ["weight_path","review_decision","recommended_human_action","sample_count","confidence_level","proposal_strength","proposed_delta","evidence_quality","missing_conditions","review_reason"], "保留候補なし")}</section>
    <section class="card"><h2>提案採否トラッキング</h2>{'<div class="empty">Proposal Adoption Tracking未取得</div>' if not proposal_adoption.get('available') else f'<div class="grid">{proposal_adoption_stats}</div>'}<h3>承認判断待ち 上位5件</h3>{table_html(proposal_adoption_pending, ["weight_path","adoption_status","adoption_source","recommended_next_action","sample_count","confidence_level","proposal_strength","tracking_reason"], "承認判断待ちなし")}<h3>保留中 上位5件</h3>{table_html(proposal_adoption_held, ["weight_path","adoption_status","adoption_source","recommended_next_action","sample_count","confidence_level","proposal_strength","tracking_reason"], "保留中なし")}</section>
    <section class="card"><h2>重みバージョン履歴</h2>{'<div class="empty">Weight Version History未取得</div>' if not weight_history.get('available') else f'<div class="grid">{weight_history_stats}</div>'}<h3>Proposal一覧 上位5件</h3>{table_html(weight_history_rows, ["version_id","source","proposal_id","review_decision","adoption_status","description","weights_json_updated","patch_applied","requires_human_approval","notes"], "履歴Proposalなし")}</section>
    <section class="card"><h2>メタ学習</h2>{'<div class="empty">Meta Learning未取得</div>' if not meta_learning.get('available') else f'<div class="grid">{meta_learning_stats}</div>'}<h3>成功パターン候補 上位5件</h3>{table_html(meta_learning_success, ["meta_learning_id","pattern_type","category","target","proposal_id","impact_score","sample_count","confidence_level","recommended_action","learning_hypothesis"], "成功パターン候補なし")}<h3>失敗パターン候補 上位5件</h3>{table_html(meta_learning_failure, ["meta_learning_id","pattern_type","category","target","proposal_id","impact_score","sample_count","confidence_level","recommended_action","learning_hypothesis"], "失敗パターン候補なし")}</section>
    <section class="card"><h2>自動較正の候補</h2>{'<div class="empty">Auto Calibration Candidates未取得</div>' if not auto_calibration.get('available') else f'<div class="grid">{auto_calibration_stats}</div>'}<h3>確信度の高い候補 上位</h3>{table_html(auto_calibration_top, ["candidate_id","asset","category","target","factor","classification","current_value","suggested_delta","suggested_value","confidence","sample_size","source","rationale"], "候補なし")}</section>
    <section class="card"><h2>人手オーバーライド分析</h2>{'<div class="empty">Human Override Analytics未取得</div>' if not human_override.get('available') else f'<div class="grid">{human_override_stats}</div>'}<h3>override impact 上位5件</h3>{table_html(human_override_top, ["proposal_id","review_decision","adoption_status","override_type","override_reason","impact_status","impact_score","source","recommended_next_action"], "override分析なし")}</section>
    </details>

    <section class="card"><h2>安全上の注意</h2><p class="notice">{html.escape(DASHBOARD_DESCRIPTION)}</p><ul>{safe}</ul></section>
  </main>
  <script type="application/json" id="dashboard-summary">{html.escape(json.dumps(summary, ensure_ascii=False))}</script>
</body>
</html>
"""
