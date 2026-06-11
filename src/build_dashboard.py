from __future__ import annotations

import html
import json
import os
from datetime import datetime
from pathlib import Path

import pandas as pd

import analyze_reason_codes as arc
from time_utils import format_jst, format_utc, now_utc


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/dashboard")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_MAPPINGS = {
    "market_snapshot": ("MARKET_SNAPSHOT", RESULTS_DIR / "market_snapshot.csv"),
    "signals": ("SIGNALS", RESULTS_DIR / "signals.csv"),
    "evaluations": ("EVALUATIONS", RESULTS_DIR / "evaluations.csv"),
}
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
    "no_entry": "未約定",
    "no_trade": "見送り",
    "win_rate": "勝率",
    "total_r": "総R",
    "average_r": "平均R",
    "best_r": "最大R",
    "worst_r": "最小R",
    "missed_opportunity_count": "取り逃し候補数",
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
}


def normalize_column_name(column: str) -> str:
    normalized = str(column).strip().lower().replace("-", "_")
    normalized = "_".join(normalized.split())
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    return normalized


def normalize_headers(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    out.columns = [normalize_column_name(col) for col in out.columns]
    return out


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return normalize_headers(pd.read_csv(path))
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def read_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def get_sheets_client():
    service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not service_account_json or not sheet_id:
        return None

    import gspread
    from google.oauth2.service_account import Credentials

    account_info = json.loads(service_account_json)
    credentials = Credentials.from_service_account_info(account_info, scopes=SCOPES)
    return gspread.authorize(credentials)


def worksheet_to_dataframe(worksheet) -> pd.DataFrame:
    values = worksheet.get_all_values()
    if not values:
        return pd.DataFrame()
    header = [normalize_column_name(col) for col in values[0]]
    rows = []
    for row in values[1:]:
        padded = list(row) + [""] * max(0, len(header) - len(row))
        trimmed = padded[: len(header)]
        if any(str(cell).strip() for cell in trimmed):
            rows.append(trimmed)
    return pd.DataFrame(rows, columns=header)


def load_sheet_data() -> tuple[dict[str, pd.DataFrame] | None, str]:
    try:
        client = get_sheets_client()
        if client is None:
            return None, "local fallback"
        spreadsheet = client.open_by_key(os.environ["GOOGLE_SHEET_ID"])
        data: dict[str, pd.DataFrame] = {}
        for key, (sheet_name, _) in SHEET_MAPPINGS.items():
            try:
                data[key] = worksheet_to_dataframe(spreadsheet.worksheet(sheet_name))
                print(f"ok: loaded {len(data[key])} rows from Google Sheets {sheet_name}")
            except Exception as exc:  # noqa: BLE001 - missing worksheets should not break dashboard.
                print(f"warning: Google Sheets worksheet {sheet_name} unavailable: {exc}")
                data[key] = pd.DataFrame()
        return data, "Google Sheets"
    except Exception as exc:  # noqa: BLE001 - fallback is intentional for artifact generation.
        print(f"warning: Google Sheets read failed; using local fallback: {exc}")
        return None, "local fallback"


def load_data() -> tuple[dict[str, pd.DataFrame], dict[str, object], str]:
    sheet_data, source = load_sheet_data()
    data = sheet_data if sheet_data is not None else {
        key: read_csv(path) for key, (_, path) in SHEET_MAPPINGS.items()
    }
    extras = {
        "weekly_review": read_csv(RESULTS_DIR / "weekly_review.csv"),
        "monthly_calibration": read_csv(RESULTS_DIR / "monthly_calibration.csv"),
        "reason_code_analysis": read_csv(RESULTS_DIR / "reason_code_analysis.csv"),
        "rule_update_proposals": read_csv(RESULTS_DIR / "rule_update_proposals.csv"),
        "model_state_update_proposals": read_csv(RESULTS_DIR / "model_state_update_proposals.csv"),
        "ai_feedback": read_csv(RESULTS_DIR / "ai_feedback.csv"),
        "news_narrative_scores": read_csv(RESULTS_DIR / "news_narrative_scores.csv"),
        "pending_reevaluations": read_csv(RESULTS_DIR / "pending_reevaluations.csv"),
        "latest_evaluations": read_csv(RESULTS_DIR / "latest_evaluations.csv"),
        "weekly_review_json": read_json(RESULTS_DIR / "weekly_review.json"),
        "monthly_calibration_json": read_json(RESULTS_DIR / "monthly_calibration.json"),
        "reason_code_analysis_json": read_json(RESULTS_DIR / "reason_code_analysis.json"),
        "rule_update_proposals_json": read_json(RESULTS_DIR / "rule_update_proposals.json"),
        "model_state_update_proposals_json": read_json(RESULTS_DIR / "model_state_update_proposals.json"),
        "model_state_update_summary_json": read_json(RESULTS_DIR / "model_state_update_summary.json"),
        "model_state_proposal_audit": read_csv(RESULTS_DIR / "model_state_proposal_audit.csv"),
        "model_state_proposal_audit_json": read_json(RESULTS_DIR / "model_state_proposal_audit.json"),
        "weights_patch_proposal": read_csv(RESULTS_DIR / "weights_patch_proposal.csv"),
        "weights_patch_proposal_json": read_json(RESULTS_DIR / "weights_patch_proposal.json"),
        "weights_patch_summary_json": read_json(RESULTS_DIR / "weights_patch_summary.json"),
        "weights_patch_review": read_csv(RESULTS_DIR / "weights_patch_review.csv"),
        "weights_patch_review_json": read_json(RESULTS_DIR / "weights_patch_review.json"),
        "weights_patch_review_summary_json": read_json(RESULTS_DIR / "weights_patch_review_summary.json"),
        "proposal_adoption_tracking": read_csv(RESULTS_DIR / "proposal_adoption_tracking.csv"),
        "proposal_adoption_tracking_json": read_json(RESULTS_DIR / "proposal_adoption_tracking.json"),
        "proposal_adoption_tracking_summary_json": read_json(RESULTS_DIR / "proposal_adoption_tracking_summary.json"),
        "weight_version_history": read_csv(RESULTS_DIR / "weight_version_history.csv"),
        "weight_version_history_json": read_json(RESULTS_DIR / "weight_version_history.json"),
        "weight_version_history_summary_json": read_json(RESULTS_DIR / "weight_version_history_summary.json"),
        "meta_learning": read_csv(RESULTS_DIR / "meta_learning.csv"),
        "meta_learning_json": read_json(RESULTS_DIR / "meta_learning.json"),
        "meta_learning_summary_json": read_json(RESULTS_DIR / "meta_learning_summary.json"),
        "auto_calibration_candidates": read_csv(RESULTS_DIR / "auto_calibration_candidates.csv"),
        "auto_calibration_candidates_json": read_json(RESULTS_DIR / "auto_calibration_candidates.json"),
        "auto_calibration_candidates_summary_json": read_json(RESULTS_DIR / "auto_calibration_candidates_summary.json"),
        "human_override_analytics": read_csv(RESULTS_DIR / "human_override_analytics.csv"),
        "human_override_analytics_json": read_json(RESULTS_DIR / "human_override_analytics.json"),
        "human_override_analytics_summary_json": read_json(RESULTS_DIR / "human_override_analytics_summary.json"),
        "portfolio_layer": read_csv(RESULTS_DIR / "portfolio_layer.csv"),
        "portfolio_layer_json": read_json(RESULTS_DIR / "portfolio_layer.json"),
        "portfolio_layer_summary_json": read_json(RESULTS_DIR / "portfolio_layer_summary.json"),
        "datetime_audit": read_csv(RESULTS_DIR / "datetime_audit.csv"),
        "datetime_audit_json": read_json(RESULTS_DIR / "datetime_audit.json"),
        "datetime_audit_summary_json": read_json(RESULTS_DIR / "datetime_audit_summary.json"),
        "ai_feedback_json": read_json(RESULTS_DIR / "ai_feedback.json"),
        "news_narrative_scores_json": read_json(RESULTS_DIR / "news_narrative_scores.json"),
        "latest_evaluations_summary_json": read_json(RESULTS_DIR / "latest_evaluations_summary.json"),
    }
    return data, extras, source


def latest_date(df: pd.DataFrame, columns: list[str]) -> str:
    dates = []
    for col in columns:
        if not df.empty and col in df.columns:
            parsed = pd.to_datetime(df[col], errors="coerce", utc=True).dt.tz_localize(None)
            dates.extend(parsed.dropna().tolist())
    if not dates:
        return ""
    return max(dates).strftime("%Y-%m-%d")


def latest_file_date(pattern: str) -> str:
    files = sorted(Path().glob(pattern))
    if not files:
        return ""
    latest = max(files, key=lambda p: p.stat().st_mtime)
    stem = latest.stem
    text = stem[:10]
    return text if len(text) == 10 else latest.name


def fmt_num(value) -> str:
    value = pd.to_numeric(value, errors="coerce")
    if pd.isna(value):
        return ""
    return f"{float(value):.2f}"


def numeric_or(value, default: float = 0.0) -> float:
    number = pd.to_numeric(value, errors="coerce")
    return float(number) if not pd.isna(number) else default


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


def latest_signals(signals: pd.DataFrame) -> pd.DataFrame:
    date_col = "date" if "date" in signals.columns else "signal_date" if "signal_date" in signals.columns else ""
    if signals.empty or not date_col:
        return pd.DataFrame()
    out = signals.copy()
    out["_date"] = pd.to_datetime(out[date_col], errors="coerce", utc=True).dt.tz_localize(None)
    if out["_date"].dropna().empty:
        return signals
    latest = out["_date"].max()
    return out[out["_date"] == latest].drop(columns=["_date"])


def signal_summary(signals: pd.DataFrame) -> dict:
    if signals.empty or "rank" not in signals.columns:
        return {"A": 0, "B": 0, "NO_TRADE": 0}
    rank = signals["rank"].fillna("").astype(str).str.upper()
    return {
        "A": int((rank == "A").sum()),
        "B": int((rank == "B").sum()),
        "NO_TRADE": int((rank == "NO_TRADE").sum()),
    }


def evaluation_summary(evaluations: pd.DataFrame) -> dict:
    if evaluations.empty:
        return {
            "total_evaluated": 0,
            "closed": 0,
            "pending": 0,
            "skipped": 0,
            "no_entry": 0,
            "no_trade": 0,
            "win_rate": 0.0,
            "total_r": 0.0,
            "average_r": 0.0,
            "best_r": 0.0,
            "worst_r": 0.0,
            "missed_opportunity_count": 0,
        }
    out = evaluations.copy()
    if "evaluation_date" in out.columns:
        out["_date"] = pd.to_datetime(out["evaluation_date"], errors="coerce", utc=True).dt.tz_localize(None)
        cutoff = pd.Timestamp(datetime.now().date()) - pd.Timedelta(days=29)
        if not out["_date"].dropna().empty:
            out = out[(out["_date"].isna()) | (out["_date"] >= cutoff)]
    status = out.get("evaluation_status", out.get("status", pd.Series(index=out.index, dtype=str))).fillna("").astype(str).str.lower()
    outcome = out.get("outcome", pd.Series(index=out.index, dtype=str)).fillna("").astype(str)
    r = pd.to_numeric(out.get("r_multiple", out.get("r_result", pd.Series(index=out.index, dtype=float))), errors="coerce")
    wins = outcome.isin(["win_tp1", "win_tp2"]) | (r > 0)
    evaluated_count = int(r.notna().sum())
    return {
        "total_evaluated": evaluated_count,
        "closed": int((status == "closed").sum()),
        "pending": int((status == "pending").sum()),
        "skipped": int((status == "skipped").sum()),
        "no_entry": int((outcome == "no_entry").sum()),
        "no_trade": int((outcome.astype(str).str.startswith("no_trade")).sum()),
        "win_rate": float(wins.sum() / evaluated_count) if evaluated_count else 0.0,
        "total_r": float(r.dropna().sum()) if evaluated_count else 0.0,
        "average_r": float(r.dropna().mean()) if evaluated_count else 0.0,
        "best_r": float(r.dropna().max()) if evaluated_count else 0.0,
        "worst_r": float(r.dropna().min()) if evaluated_count else 0.0,
        "missed_opportunity_count": int(out.get("missed_opportunity", pd.Series(index=out.index, dtype=str)).fillna("").astype(str).str.lower().isin(["true", "1", "yes"]).sum()),
    }


def asset_performance(signals: pd.DataFrame, evaluations: pd.DataFrame) -> pd.DataFrame:
    assets = set()
    if not signals.empty and "asset" in signals.columns:
        assets |= set(signals["asset"].dropna().astype(str))
    if not evaluations.empty and "asset" in evaluations.columns:
        assets |= set(evaluations["asset"].dropna().astype(str))
    rows = []
    for asset in sorted(assets):
        sig = signals[signals["asset"].astype(str) == asset] if "asset" in signals.columns and not signals.empty else pd.DataFrame()
        ev = evaluations[evaluations["asset"].astype(str) == asset] if "asset" in evaluations.columns and not evaluations.empty else pd.DataFrame()
        metrics = evaluation_summary(ev)
        rows.append(
            {
                "asset": asset,
                "signals": len(sig),
                "evaluations": len(ev),
                "win_rate": metrics["win_rate"],
                "total_r": metrics["total_r"],
                "average_r": metrics["average_r"],
                "missed_opportunity_count": metrics["missed_opportunity_count"],
            }
        )
    return pd.DataFrame(rows)


def reason_code_data(signals: pd.DataFrame, evaluations: pd.DataFrame, reason_csv: pd.DataFrame, reason_json) -> tuple[pd.DataFrame, pd.DataFrame]:
    reason_table = reason_csv.copy()
    no_trade_table = pd.DataFrame()
    if reason_json:
        no_trade_table = pd.DataFrame(reason_json.get("no_trade_reason_summary", []))
        no_trade_table = normalize_headers(no_trade_table)
    if reason_table.empty:
        merged = arc.combine_signals_evaluations(signals, evaluations)
        reason_table = arc.reason_summary(arc.explode_reason_codes(merged))
        if no_trade_table.empty:
            no_trade_table = arc.no_trade_summary(merged)
    return normalize_headers(reason_table), normalize_headers(no_trade_table)


def weekly_monthly_mode(weekly: pd.DataFrame, monthly: pd.DataFrame) -> dict:
    row_w = weekly.iloc[-1].to_dict() if not weekly.empty else {}
    row_m = monthly.iloc[-1].to_dict() if not monthly.empty else {}
    return {
        "next_week_mode": row_w.get("next_week_mode", "not available"),
        "next_month_mode": row_m.get("next_month_mode", "not available"),
        "max_daily_risk_pct": row_m.get("max_daily_risk_pct", row_w.get("max_daily_risk_pct", "not available")),
        "best_asset": row_m.get("best_asset", row_w.get("best_asset", "not available")),
        "worst_asset": row_m.get("worst_asset", row_w.get("worst_asset", "not available")),
        "best_rank": row_m.get("best_rank", "not available"),
        "worst_rank": row_m.get("worst_rank", "not available"),
    }


def ai_feedback_summary(ai_feedback: pd.DataFrame, ai_feedback_json) -> dict:
    if not ai_feedback_json and ai_feedback.empty:
        return {
            "available": False,
            "latest_date": "",
            "market_mode_summary": "AIフィードバック未取得",
            "alignment_counts": {"aligned": 0, "conflicted": 0, "neutral": 0, "insufficient_data": 0},
            "improvement_hypotheses": [],
        }
    counts = {"aligned": 0, "conflicted": 0, "neutral": 0, "insufficient_data": 0}
    if not ai_feedback.empty and "narrative_alignment" in ai_feedback.columns:
        raw_counts = ai_feedback["narrative_alignment"].fillna("neutral").astype(str).value_counts().to_dict()
        counts = {key: int(raw_counts.get(key, 0)) for key in counts}
    latest = ""
    market_mode = "データなし"
    hypotheses = []
    if ai_feedback_json:
        latest = str(ai_feedback_json.get("date", "") or "")
        market_mode = str(ai_feedback_json.get("market_mode_summary", "データなし"))
        hypotheses = list(ai_feedback_json.get("improvement_hypotheses", []) or [])
        if not any(counts.values()):
            for row in ai_feedback_json.get("signal_alignment", []) or []:
                key = str(row.get("narrative_alignment", "neutral"))
                if key in counts:
                    counts[key] += 1
    elif not ai_feedback.empty:
        latest = latest_date(ai_feedback, ["date"])
    return {
        "available": True,
        "latest_date": latest,
        "market_mode_summary": market_mode,
        "alignment_counts": counts,
        "improvement_hypotheses": hypotheses[:3],
    }


def news_narrative_summary(news_csv: pd.DataFrame, news_json) -> dict:
    if isinstance(news_json, dict) and news_json:
        return {
            "available": True,
            "latest_news_fetched_at": news_json.get("generated_at_jst", ""),
            "news_fetch_status": news_json.get("news_fetch_status", "unavailable"),
            "news_fetch_success_source_count": int(numeric_or(news_json.get("news_fetch_success_source_count", 0), 0)),
            "news_fetch_failed_source_count": int(numeric_or(news_json.get("news_fetch_failed_source_count", 0), 0)),
            "news_fetch_elapsed_seconds": numeric_or(news_json.get("news_fetch_elapsed_seconds", 0), 0.0),
            "headline_count": int(numeric_or(news_json.get("headline_count", 0), 0)),
            "news_market_bias": news_json.get("news_market_bias", "insufficient_data"),
            "news_conflict_score": numeric_or(news_json.get("news_conflict_score", 0), 0.0),
            "dominant_news_themes": list(news_json.get("dominant_news_themes", []) or []),
            "news_summary_ja": news_json.get("news_summary_ja", "ニュースナラティブ未取得"),
            "news_confidence": numeric_or(news_json.get("news_confidence", 0), 0.0),
            "risk_on_news_score": numeric_or(news_json.get("risk_on_news_score", 0), 0.0),
            "risk_off_news_score": numeric_or(news_json.get("risk_off_news_score", 0), 0.0),
            "dollar_strength_news_score": numeric_or(news_json.get("dollar_strength_news_score", 0), 0.0),
            "rate_pressure_news_score": numeric_or(news_json.get("rate_pressure_news_score", 0), 0.0),
            "geopolitical_risk_news_score": numeric_or(news_json.get("geopolitical_risk_news_score", 0), 0.0),
            "oil_supply_risk_news_score": numeric_or(news_json.get("oil_supply_risk_news_score", 0), 0.0),
            "crypto_liquidity_news_score": numeric_or(news_json.get("crypto_liquidity_news_score", 0), 0.0),
            "top_news_drivers": list(news_json.get("top_news_drivers", []) or [])[:5],
        }
    if not news_csv.empty:
        row = news_csv.iloc[-1].to_dict()
        drivers = row.get("top_news_drivers", [])
        if isinstance(drivers, str):
            try:
                drivers = json.loads(drivers)
            except json.JSONDecodeError:
                drivers = []
        return {
            "available": True,
            "latest_news_fetched_at": row.get("generated_at_jst", ""),
            "news_fetch_status": row.get("news_fetch_status", "unavailable"),
            "news_fetch_success_source_count": int(numeric_or(row.get("news_fetch_success_source_count", 0), 0)),
            "news_fetch_failed_source_count": int(numeric_or(row.get("news_fetch_failed_source_count", 0), 0)),
            "news_fetch_elapsed_seconds": numeric_or(row.get("news_fetch_elapsed_seconds", 0), 0.0),
            "headline_count": int(numeric_or(row.get("headline_count", 0), 0)),
            "news_market_bias": row.get("news_market_bias", "insufficient_data"),
            "news_conflict_score": numeric_or(row.get("news_conflict_score", 0), 0.0),
            "dominant_news_themes": str(row.get("dominant_news_themes", "") or "").split("|") if row.get("dominant_news_themes", "") else [],
            "news_summary_ja": row.get("news_summary_ja", "ニュースナラティブ未取得"),
            "news_confidence": numeric_or(row.get("news_confidence", 0), 0.0),
            "risk_on_news_score": numeric_or(row.get("risk_on_news_score", 0), 0.0),
            "risk_off_news_score": numeric_or(row.get("risk_off_news_score", 0), 0.0),
            "dollar_strength_news_score": numeric_or(row.get("dollar_strength_news_score", 0), 0.0),
            "rate_pressure_news_score": numeric_or(row.get("rate_pressure_news_score", 0), 0.0),
            "geopolitical_risk_news_score": numeric_or(row.get("geopolitical_risk_news_score", 0), 0.0),
            "oil_supply_risk_news_score": numeric_or(row.get("oil_supply_risk_news_score", 0), 0.0),
            "crypto_liquidity_news_score": numeric_or(row.get("crypto_liquidity_news_score", 0), 0.0),
            "top_news_drivers": drivers[:5] if isinstance(drivers, list) else [],
        }
    return {
        "available": False,
        "latest_news_fetched_at": "",
        "news_fetch_status": "unavailable",
        "news_fetch_success_source_count": 0,
        "news_fetch_failed_source_count": 0,
        "news_fetch_elapsed_seconds": 0.0,
        "headline_count": 0,
        "news_market_bias": "insufficient_data",
        "news_conflict_score": 0.0,
        "dominant_news_themes": [],
        "news_summary_ja": "ニュースナラティブ未取得",
        "news_confidence": 0.0,
        "risk_on_news_score": 0.0,
        "risk_off_news_score": 0.0,
        "dollar_strength_news_score": 0.0,
        "rate_pressure_news_score": 0.0,
        "geopolitical_risk_news_score": 0.0,
        "oil_supply_risk_news_score": 0.0,
        "crypto_liquidity_news_score": 0.0,
        "top_news_drivers": [],
    }


def model_state_update_summary(proposals: pd.DataFrame, proposals_json, summary_json) -> dict:
    if isinstance(summary_json, dict) and summary_json:
        strong = proposals[proposals["proposal_strength"].astype(str) == "strong"] if not proposals.empty and "proposal_strength" in proposals.columns else pd.DataFrame()
        return {
            "available": True,
            "model_state_total_proposals": int(numeric_or(summary_json.get("total_proposals", len(proposals)), 0)),
            "model_state_increase_count": int(numeric_or(summary_json.get("increase_count", 0), 0)),
            "model_state_decrease_count": int(numeric_or(summary_json.get("decrease_count", 0), 0)),
            "model_state_hold_count": int(numeric_or(summary_json.get("hold_count", 0), 0)),
            "model_state_insufficient_data_count": int(numeric_or(summary_json.get("insufficient_data_count", 0), 0)),
            "model_state_apply_automatically": str((summary_json.get("safety", {}) or {}).get("apply_automatically", False)).lower(),
            "strong_candidates": strong.head(5).to_dict(orient="records"),
        }
    if isinstance(proposals_json, dict) and proposals_json:
        summary = proposals_json.get("summary", {}) or {}
        rows = proposals_json.get("proposals", []) or []
        table = normalize_headers(pd.DataFrame(rows))
        strong = table[table["proposal_strength"].astype(str) == "strong"] if not table.empty and "proposal_strength" in table.columns else pd.DataFrame()
        return {
            "available": True,
            "model_state_total_proposals": int(numeric_or(summary.get("total_proposals", len(rows)), 0)),
            "model_state_increase_count": int(numeric_or(summary.get("increase_count", 0), 0)),
            "model_state_decrease_count": int(numeric_or(summary.get("decrease_count", 0), 0)),
            "model_state_hold_count": int(numeric_or(summary.get("hold_count", 0), 0)),
            "model_state_insufficient_data_count": int(numeric_or(summary.get("insufficient_data_count", 0), 0)),
            "model_state_apply_automatically": str((proposals_json.get("safety", {}) or {}).get("apply_automatically", False)).lower(),
            "strong_candidates": strong.head(5).to_dict(orient="records"),
        }
    if not proposals.empty:
        strong = proposals[proposals["proposal_strength"].astype(str) == "strong"] if "proposal_strength" in proposals.columns else pd.DataFrame()
        direction = proposals.get("proposal_direction", pd.Series("", index=proposals.index)).fillna("").astype(str)
        confidence = proposals.get("confidence_level", pd.Series("", index=proposals.index)).fillna("").astype(str)
        return {
            "available": True,
            "model_state_total_proposals": int(len(proposals)),
            "model_state_increase_count": int((direction == "increase").sum()),
            "model_state_decrease_count": int((direction == "decrease").sum()),
            "model_state_hold_count": int((direction == "hold").sum()),
            "model_state_insufficient_data_count": int((confidence == "insufficient_data").sum()),
            "model_state_apply_automatically": "false",
            "strong_candidates": strong.head(5).to_dict(orient="records"),
        }
    return {
        "available": False,
        "model_state_total_proposals": 0,
        "model_state_increase_count": 0,
        "model_state_decrease_count": 0,
        "model_state_hold_count": 0,
        "model_state_insufficient_data_count": 0,
        "model_state_apply_automatically": "false",
        "strong_candidates": [],
    }


def model_state_audit_summary(audit_json, audit_csv: pd.DataFrame) -> dict:
    if isinstance(audit_json, dict) and audit_json:
        return {
            "model_state_audit_status": audit_json.get("audit_status", "unavailable"),
            "model_state_audit_warning_count": int(numeric_or(audit_json.get("warning_count", 0), 0)),
            "model_state_audit_blocked_count": int(numeric_or(audit_json.get("blocked_count", 0), 0)),
            "model_state_audit_critical_count": int(numeric_or(audit_json.get("critical_count", 0), 0)),
            "model_state_requires_human_review": "必須" if audit_json.get("requires_human_review", True) else "不要",
            "model_state_weights_json_updated": str(audit_json.get("weights_json_updated", False)).lower(),
        }
    if not audit_csv.empty:
        result = audit_csv.get("audit_result", pd.Series("", index=audit_csv.index)).fillna("").astype(str)
        severity = audit_csv.get("severity", pd.Series("", index=audit_csv.index)).fillna("").astype(str)
        status = "blocked" if (result == "blocked").any() else "warning" if (result == "warning").any() else "passed"
        return {
            "model_state_audit_status": status,
            "model_state_audit_warning_count": int((result == "warning").sum()),
            "model_state_audit_blocked_count": int((result == "blocked").sum()),
            "model_state_audit_critical_count": int((severity == "critical").sum()),
            "model_state_requires_human_review": "必須",
            "model_state_weights_json_updated": "false",
        }
    return {
        "model_state_audit_status": "unavailable",
        "model_state_audit_warning_count": 0,
        "model_state_audit_blocked_count": 0,
        "model_state_audit_critical_count": 0,
        "model_state_requires_human_review": "必須",
        "model_state_weights_json_updated": "false",
    }


def weights_patch_summary(patch_csv: pd.DataFrame, patch_json, summary_json) -> dict:
    if isinstance(patch_json, dict) and patch_json:
        summary = patch_json.get("summary", {}) or {}
        safety = patch_json.get("safety", {}) or {}
        rows = patch_json.get("patches", []) or []
        return {
            "available": True,
            "weights_patch_count": int(numeric_or(summary.get("eligible_patch_count", len(rows)), 0)),
            "weights_patch_excluded_count": int(numeric_or(summary.get("excluded_count", 0), 0)),
            "weights_patch_increase_count": int(numeric_or(summary.get("increase_count", 0), 0)),
            "weights_patch_decrease_count": int(numeric_or(summary.get("decrease_count", 0), 0)),
            "weights_patch_requires_human_approval": "必須" if safety.get("requires_human_approval", True) else "不要",
            "weights_patch_applied": str(safety.get("patch_applied", False)).lower(),
            "weights_patch_weights_json_updated": str(safety.get("weights_json_updated", False)).lower(),
            "patch_candidates": rows[:5],
        }
    if isinstance(summary_json, dict) and summary_json:
        safety = summary_json.get("safety", {}) or {}
        return {
            "available": True,
            "weights_patch_count": int(numeric_or(summary_json.get("eligible_patch_count", len(patch_csv)), 0)),
            "weights_patch_excluded_count": int(numeric_or(summary_json.get("excluded_count", 0), 0)),
            "weights_patch_increase_count": int(numeric_or(summary_json.get("increase_count", 0), 0)),
            "weights_patch_decrease_count": int(numeric_or(summary_json.get("decrease_count", 0), 0)),
            "weights_patch_requires_human_approval": "必須" if safety.get("requires_human_approval", True) else "不要",
            "weights_patch_applied": str(safety.get("patch_applied", False)).lower(),
            "weights_patch_weights_json_updated": str(safety.get("weights_json_updated", False)).lower(),
            "patch_candidates": patch_csv.head(5).to_dict(orient="records"),
        }
    if not patch_csv.empty:
        direction = patch_csv.get("proposal_direction", pd.Series("", index=patch_csv.index)).fillna("").astype(str)
        return {
            "available": True,
            "weights_patch_count": int(len(patch_csv)),
            "weights_patch_excluded_count": 0,
            "weights_patch_increase_count": int((direction == "increase").sum()),
            "weights_patch_decrease_count": int((direction == "decrease").sum()),
            "weights_patch_requires_human_approval": "必須",
            "weights_patch_applied": "false",
            "weights_patch_weights_json_updated": "false",
            "patch_candidates": patch_csv.head(5).to_dict(orient="records"),
        }
    return {
        "available": False,
        "weights_patch_count": 0,
        "weights_patch_excluded_count": 0,
        "weights_patch_increase_count": 0,
        "weights_patch_decrease_count": 0,
        "weights_patch_requires_human_approval": "必須",
        "weights_patch_applied": "false",
        "weights_patch_weights_json_updated": "false",
        "patch_candidates": [],
    }


def weights_patch_review_summary(review_csv: pd.DataFrame, review_json, summary_json) -> dict:
    if isinstance(review_json, dict) and review_json:
        rows = review_json.get("patch_review", []) or []
        return {
            "available": True,
            "weights_patch_review_status": review_json.get("review_status", "unavailable"),
            "weights_patch_review_candidate_count": int(numeric_or(review_json.get("candidate_count", 0), 0)),
            "weights_patch_review_hold_count": int(numeric_or(review_json.get("hold_count", 0), 0)),
            "weights_patch_review_reject_count": int(numeric_or(review_json.get("reject_count", 0), 0)),
            "weights_patch_review_blocked_count": int(numeric_or(review_json.get("blocked_count", 0), 0)),
            "weights_patch_review_recommended_next_action": review_json.get("recommended_next_action", "no_action"),
            "weights_patch_review_requires_human_approval": "必須" if review_json.get("requires_human_approval", True) else "不要",
            "weights_patch_review_patch_applied": str(review_json.get("patch_applied", False)).lower(),
            "weights_patch_review_weights_json_updated": str(review_json.get("weights_json_updated", False)).lower(),
            "candidate_rows": [row for row in rows if str(row.get("review_decision", "")) == "candidate"][:5],
            "hold_rows": [row for row in rows if str(row.get("review_decision", "")) == "hold"][:5],
        }
    if isinstance(summary_json, dict) and summary_json:
        candidates = review_csv[review_csv["review_decision"].astype(str) == "candidate"].head(5) if not review_csv.empty and "review_decision" in review_csv.columns else pd.DataFrame()
        holds = review_csv[review_csv["review_decision"].astype(str) == "hold"].head(5) if not review_csv.empty and "review_decision" in review_csv.columns else pd.DataFrame()
        return {
            "available": True,
            "weights_patch_review_status": summary_json.get("review_status", "unavailable"),
            "weights_patch_review_candidate_count": int(numeric_or(summary_json.get("candidate_count", 0), 0)),
            "weights_patch_review_hold_count": int(numeric_or(summary_json.get("hold_count", 0), 0)),
            "weights_patch_review_reject_count": int(numeric_or(summary_json.get("reject_count", 0), 0)),
            "weights_patch_review_blocked_count": int(numeric_or(summary_json.get("blocked_count", 0), 0)),
            "weights_patch_review_recommended_next_action": summary_json.get("recommended_next_action", "no_action"),
            "weights_patch_review_requires_human_approval": "必須" if summary_json.get("requires_human_approval", True) else "不要",
            "weights_patch_review_patch_applied": str(summary_json.get("patch_applied", False)).lower(),
            "weights_patch_review_weights_json_updated": str(summary_json.get("weights_json_updated", False)).lower(),
            "candidate_rows": candidates.to_dict(orient="records"),
            "hold_rows": holds.to_dict(orient="records"),
        }
    if not review_csv.empty and "review_decision" in review_csv.columns:
        decision = review_csv["review_decision"].fillna("").astype(str)
        risk = review_csv.get("patch_risk_level", pd.Series("", index=review_csv.index)).fillna("").astype(str)
        return {
            "available": True,
            "weights_patch_review_status": "blocked" if (decision == "blocked").any() else "warning" if decision.isin(["hold", "reject"]).any() else "passed",
            "weights_patch_review_candidate_count": int((decision == "candidate").sum()),
            "weights_patch_review_hold_count": int((decision == "hold").sum()),
            "weights_patch_review_reject_count": int((decision == "reject").sum()),
            "weights_patch_review_blocked_count": int((decision == "blocked").sum()),
            "weights_patch_review_recommended_next_action": "manual_review" if (decision == "candidate").any() else "wait_for_more_data" if (decision == "hold").any() else "no_action",
            "weights_patch_review_requires_human_approval": "必須",
            "weights_patch_review_patch_applied": "false",
            "weights_patch_review_weights_json_updated": "false",
            "weights_patch_review_low_risk_count": int((risk == "low").sum()),
            "weights_patch_review_medium_risk_count": int((risk == "medium").sum()),
            "weights_patch_review_high_risk_count": int((risk == "high").sum()),
            "candidate_rows": review_csv[decision == "candidate"].head(5).to_dict(orient="records"),
            "hold_rows": review_csv[decision == "hold"].head(5).to_dict(orient="records"),
        }
    return {
        "available": False,
        "weights_patch_review_status": "unavailable",
        "weights_patch_review_candidate_count": 0,
        "weights_patch_review_hold_count": 0,
        "weights_patch_review_reject_count": 0,
        "weights_patch_review_blocked_count": 0,
        "weights_patch_review_recommended_next_action": "no_action",
        "weights_patch_review_requires_human_approval": "必須",
        "weights_patch_review_patch_applied": "false",
        "weights_patch_review_weights_json_updated": "false",
        "candidate_rows": [],
        "hold_rows": [],
    }


def proposal_adoption_summary(adoption_csv: pd.DataFrame, adoption_json, summary_json) -> dict:
    payload = adoption_json if isinstance(adoption_json, dict) and adoption_json else summary_json if isinstance(summary_json, dict) else {}
    if payload:
        rows = adoption_json.get("adoptions", []) if isinstance(adoption_json, dict) else []
        if not rows and not adoption_csv.empty:
            rows = adoption_csv.to_dict(orient="records")
        return {
            "available": True,
            "proposal_adoption_tracking_status": payload.get("tracking_status", "unavailable"),
            "proposal_adoption_total_count": int(numeric_or(payload.get("total_tracked_proposals", len(rows)), 0)),
            "proposal_adoption_accepted_count": int(numeric_or(payload.get("accepted_count", 0), 0)),
            "proposal_adoption_pending_review_count": int(numeric_or(payload.get("pending_review_count", 0), 0)),
            "proposal_adoption_held_count": int(numeric_or(payload.get("held_count", 0), 0)),
            "proposal_adoption_rejected_count": int(numeric_or(payload.get("rejected_count", 0), 0)),
            "proposal_adoption_blocked_count": int(numeric_or(payload.get("blocked_count", 0), 0)),
            "proposal_adoption_superseded_count": int(numeric_or(payload.get("superseded_count", 0), 0)),
            "proposal_adoption_manual_decision_count": int(numeric_or(payload.get("manual_decision_count", 0), 0)),
            "proposal_adoption_derived_decision_count": int(numeric_or(payload.get("derived_decision_count", 0), 0)),
            "proposal_adoption_recommended_next_action": payload.get("recommended_next_action", "no_action"),
            "pending_rows": [row for row in rows if str(row.get("adoption_status", "")) == "pending_review"][:5],
            "held_rows": [row for row in rows if str(row.get("adoption_status", "")) == "held"][:5],
        }
    if not adoption_csv.empty and "adoption_status" in adoption_csv.columns:
        status = adoption_csv["adoption_status"].fillna("").astype(str)
        source = adoption_csv.get("adoption_source", pd.Series("", index=adoption_csv.index)).fillna("").astype(str)
        return {
            "available": True,
            "proposal_adoption_tracking_status": "active",
            "proposal_adoption_total_count": int(len(adoption_csv)),
            "proposal_adoption_accepted_count": int((status == "accepted").sum()),
            "proposal_adoption_pending_review_count": int((status == "pending_review").sum()),
            "proposal_adoption_held_count": int((status == "held").sum()),
            "proposal_adoption_rejected_count": int((status == "rejected").sum()),
            "proposal_adoption_blocked_count": int((status == "blocked").sum()),
            "proposal_adoption_superseded_count": int((status == "superseded").sum()),
            "proposal_adoption_manual_decision_count": int((source == "manual").sum()),
            "proposal_adoption_derived_decision_count": int((source == "derived_from_review").sum()),
            "proposal_adoption_recommended_next_action": "manual_review" if (status == "pending_review").any() else "wait_for_more_data" if (status == "held").any() else "no_action",
            "pending_rows": adoption_csv[status == "pending_review"].head(5).to_dict(orient="records"),
            "held_rows": adoption_csv[status == "held"].head(5).to_dict(orient="records"),
        }
    return {
        "available": False,
        "proposal_adoption_tracking_status": "unavailable",
        "proposal_adoption_total_count": 0,
        "proposal_adoption_accepted_count": 0,
        "proposal_adoption_pending_review_count": 0,
        "proposal_adoption_held_count": 0,
        "proposal_adoption_rejected_count": 0,
        "proposal_adoption_blocked_count": 0,
        "proposal_adoption_superseded_count": 0,
        "proposal_adoption_manual_decision_count": 0,
        "proposal_adoption_derived_decision_count": 0,
        "proposal_adoption_recommended_next_action": "no_action",
        "pending_rows": [],
        "held_rows": [],
    }


def weight_version_history_summary(history_csv: pd.DataFrame, history_json, summary_json) -> dict:
    payload = history_json if isinstance(history_json, dict) and history_json else summary_json if isinstance(summary_json, dict) else {}
    if payload:
        rows = history_json.get("proposals", []) if isinstance(history_json, dict) else []
        if not rows and not history_csv.empty:
            rows = history_csv.to_dict(orient="records")
        return {
            "available": True,
            "weight_history_current_version": payload.get("current_version", "v1"),
            "weight_history_version_count": int(numeric_or(payload.get("version_count", 1), 1)),
            "weight_history_tracked_count": int(numeric_or(payload.get("tracked_count", 0), 0)),
            "weight_history_held_count": int(numeric_or(payload.get("held_count", 0), 0)),
            "weight_history_candidate_count": int(numeric_or(payload.get("candidate_count", 0), 0)),
            "weight_history_approved_count": int(numeric_or(payload.get("approved_count", 0), 0)),
            "weight_history_rejected_count": int(numeric_or(payload.get("rejected_count", 0), 0)),
            "weight_history_blocked_count": int(numeric_or(payload.get("blocked_count", 0), 0)),
            "weight_history_weights_json_updated": str(payload.get("weights_json_updated", False)).lower(),
            "weight_history_patch_applied": str(payload.get("patch_applied", False)).lower(),
            "weight_history_requires_human_approval": "必須" if payload.get("requires_human_approval", True) else "不要",
            "proposal_rows": rows[:5],
        }
    if not history_csv.empty and "adoption_status" in history_csv.columns:
        status = history_csv["adoption_status"].fillna("").astype(str)
        return {
            "available": True,
            "weight_history_current_version": "v1",
            "weight_history_version_count": 1,
            "weight_history_tracked_count": int((status == "tracked").sum()),
            "weight_history_held_count": int((status == "held").sum()),
            "weight_history_candidate_count": int((status == "candidate").sum()),
            "weight_history_approved_count": int((status == "approved").sum()),
            "weight_history_rejected_count": int((status == "rejected").sum()),
            "weight_history_blocked_count": int((status == "blocked").sum()),
            "weight_history_weights_json_updated": "false",
            "weight_history_patch_applied": "false",
            "weight_history_requires_human_approval": "必須",
            "proposal_rows": history_csv.head(5).to_dict(orient="records"),
        }
    return {
        "available": False,
        "weight_history_current_version": "v1",
        "weight_history_version_count": 1,
        "weight_history_tracked_count": 0,
        "weight_history_held_count": 0,
        "weight_history_candidate_count": 0,
        "weight_history_approved_count": 0,
        "weight_history_rejected_count": 0,
        "weight_history_blocked_count": 0,
        "weight_history_weights_json_updated": "false",
        "weight_history_patch_applied": "false",
        "weight_history_requires_human_approval": "必須",
        "proposal_rows": [],
    }


def meta_learning_summary(meta_csv: pd.DataFrame, meta_json, summary_json) -> dict:
    payload = meta_json if isinstance(meta_json, dict) and meta_json else summary_json if isinstance(summary_json, dict) else {}
    if payload:
        rows = meta_json.get("meta_learning_candidates", []) if isinstance(meta_json, dict) else []
        if not rows and not meta_csv.empty:
            rows = meta_csv.to_dict(orient="records")
        return {
            "available": True,
            "meta_learning_status": payload.get("meta_learning_status", "unavailable"),
            "meta_learning_total_candidates": int(numeric_or(payload.get("total_candidates", len(rows)), 0)),
            "meta_learning_success_pattern_count": int(numeric_or(payload.get("success_pattern_count", 0), 0)),
            "meta_learning_failure_pattern_count": int(numeric_or(payload.get("failure_pattern_count", 0), 0)),
            "meta_learning_neutral_pattern_count": int(numeric_or(payload.get("neutral_pattern_count", 0), 0)),
            "meta_learning_insufficient_data_count": int(numeric_or(payload.get("insufficient_data_count", 0), 0)),
            "meta_learning_recommended_next_action": payload.get("recommended_next_action", "wait_for_more_data"),
            "meta_learning_apply_automatically": str(payload.get("apply_automatically", False)).lower(),
            "meta_learning_weights_json_updated": str(payload.get("weights_json_updated", False)).lower(),
            "meta_learning_patch_applied": str(payload.get("patch_applied", False)).lower(),
            "meta_learning_requires_human_approval": "必須" if payload.get("requires_human_approval", True) else "不要",
            "success_rows": [row for row in rows if str(row.get("pattern_type", "")) == "success_pattern"][:5],
            "failure_rows": [row for row in rows if str(row.get("pattern_type", "")) == "failure_pattern"][:5],
        }
    if not meta_csv.empty and "pattern_type" in meta_csv.columns:
        pattern = meta_csv["pattern_type"].fillna("").astype(str)
        return {
            "available": True,
            "meta_learning_status": "active",
            "meta_learning_total_candidates": int(len(meta_csv)),
            "meta_learning_success_pattern_count": int((pattern == "success_pattern").sum()),
            "meta_learning_failure_pattern_count": int((pattern == "failure_pattern").sum()),
            "meta_learning_neutral_pattern_count": int((pattern == "neutral_pattern").sum()),
            "meta_learning_insufficient_data_count": int((pattern == "insufficient_data").sum()),
            "meta_learning_recommended_next_action": "human_review" if pattern.isin(["success_pattern", "failure_pattern"]).any() else "wait_for_more_data",
            "meta_learning_apply_automatically": "false",
            "meta_learning_weights_json_updated": "false",
            "meta_learning_patch_applied": "false",
            "meta_learning_requires_human_approval": "必須",
            "success_rows": meta_csv[pattern == "success_pattern"].head(5).to_dict(orient="records"),
            "failure_rows": meta_csv[pattern == "failure_pattern"].head(5).to_dict(orient="records"),
        }
    return {
        "available": False,
        "meta_learning_status": "unavailable",
        "meta_learning_total_candidates": 0,
        "meta_learning_success_pattern_count": 0,
        "meta_learning_failure_pattern_count": 0,
        "meta_learning_neutral_pattern_count": 0,
        "meta_learning_insufficient_data_count": 0,
        "meta_learning_recommended_next_action": "wait_for_more_data",
        "meta_learning_apply_automatically": "false",
        "meta_learning_weights_json_updated": "false",
        "meta_learning_patch_applied": "false",
        "meta_learning_requires_human_approval": "必須",
        "success_rows": [],
        "failure_rows": [],
    }


def auto_calibration_summary(candidate_csv: pd.DataFrame, candidate_json, summary_json) -> dict:
    payload = candidate_json if isinstance(candidate_json, dict) and candidate_json else summary_json if isinstance(summary_json, dict) else {}
    if payload:
        rows = candidate_json.get("candidates", []) if isinstance(candidate_json, dict) else []
        if not rows and not candidate_csv.empty:
            rows = candidate_csv.to_dict(orient="records")
        sorted_rows = sorted(rows, key=lambda row: numeric_or(row.get("confidence", 0), 0), reverse=True)
        return {
            "available": True,
            "auto_calibration_status": payload.get("candidate_status", "unavailable"),
            "auto_calibration_candidate_count": int(numeric_or(payload.get("candidate_count", len(rows)), 0)),
            "auto_calibration_increase_count": int(numeric_or(payload.get("increase_count", 0), 0)),
            "auto_calibration_decrease_count": int(numeric_or(payload.get("decrease_count", 0), 0)),
            "auto_calibration_hold_count": int(numeric_or(payload.get("hold_count", 0), 0)),
            "auto_calibration_blocked_count": int(numeric_or(payload.get("blocked_count", 0), 0)),
            "auto_calibration_insufficient_data_count": int(numeric_or(payload.get("insufficient_data_count", 0), 0)),
            "auto_calibration_recommended_next_action": payload.get("recommended_next_action", "wait_for_more_data"),
            "auto_calibration_requires_human_approval": "必須" if payload.get("requires_human_approval", True) else "不要",
            "auto_calibration_patch_applied": str(payload.get("patch_applied", False)).lower(),
            "auto_calibration_weights_json_updated": str(payload.get("weights_json_updated", False)).lower(),
            "top_candidates": sorted_rows[:5],
        }
    if not candidate_csv.empty and "classification" in candidate_csv.columns:
        classification = candidate_csv["classification"].fillna("").astype(str)
        top = candidate_csv.sort_values("confidence", ascending=False).head(5) if "confidence" in candidate_csv.columns else candidate_csv.head(5)
        return {
            "available": True,
            "auto_calibration_status": "active",
            "auto_calibration_candidate_count": int(len(candidate_csv)),
            "auto_calibration_increase_count": int((classification == "increase").sum()),
            "auto_calibration_decrease_count": int((classification == "decrease").sum()),
            "auto_calibration_hold_count": int((classification == "hold").sum()),
            "auto_calibration_blocked_count": int((classification == "blocked").sum()),
            "auto_calibration_insufficient_data_count": int((classification == "insufficient_data").sum()),
            "auto_calibration_recommended_next_action": "human_review" if classification.isin(["increase", "decrease"]).any() else "wait_for_more_data",
            "auto_calibration_requires_human_approval": "必須",
            "auto_calibration_patch_applied": "false",
            "auto_calibration_weights_json_updated": "false",
            "top_candidates": top.to_dict(orient="records"),
        }
    return {
        "available": False,
        "auto_calibration_status": "unavailable",
        "auto_calibration_candidate_count": 0,
        "auto_calibration_increase_count": 0,
        "auto_calibration_decrease_count": 0,
        "auto_calibration_hold_count": 0,
        "auto_calibration_blocked_count": 0,
        "auto_calibration_insufficient_data_count": 0,
        "auto_calibration_recommended_next_action": "wait_for_more_data",
        "auto_calibration_requires_human_approval": "必須",
        "auto_calibration_patch_applied": "false",
        "auto_calibration_weights_json_updated": "false",
        "top_candidates": [],
    }


def human_override_summary(override_csv: pd.DataFrame, override_json, summary_json) -> dict:
    payload = override_json if isinstance(override_json, dict) and override_json else summary_json if isinstance(summary_json, dict) else {}
    if payload:
        rows = override_json.get("overrides", []) if isinstance(override_json, dict) else []
        if not rows and not override_csv.empty:
            rows = override_csv.to_dict(orient="records")
        top_rows = sorted(rows, key=lambda row: abs(numeric_or(row.get("impact_score", 0), 0)), reverse=True)
        return {
            "available": True,
            "human_override_status": payload.get("analytics_status", "unavailable"),
            "human_override_total_overrides": int(numeric_or(payload.get("total_overrides", len(rows)), 0)),
            "human_override_accepted_count": int(numeric_or(payload.get("accepted_count", 0), 0)),
            "human_override_held_count": int(numeric_or(payload.get("held_count", 0), 0)),
            "human_override_rejected_count": int(numeric_or(payload.get("rejected_count", 0), 0)),
            "human_override_blocked_count": int(numeric_or(payload.get("blocked_count", 0), 0)),
            "human_override_positive_count": int(numeric_or(payload.get("positive_override_count", 0), 0)),
            "human_override_negative_count": int(numeric_or(payload.get("negative_override_count", 0), 0)),
            "human_override_unknown_count": int(numeric_or(payload.get("unknown_outcome_count", 0), 0)),
            "human_override_recommended_next_action": payload.get("recommended_next_action", "wait_for_more_data"),
            "human_override_requires_human_approval": "必須" if payload.get("requires_human_approval", True) else "不要",
            "top_rows": top_rows[:5],
        }
    if not override_csv.empty and "override_type" in override_csv.columns:
        override_type = override_csv["override_type"].fillna("").astype(str)
        impact_status = override_csv.get("impact_status", pd.Series("", index=override_csv.index)).fillna("").astype(str)
        impact_score = pd.to_numeric(override_csv.get("impact_score", pd.Series(0, index=override_csv.index)), errors="coerce").fillna(0)
        top = override_csv.reindex(impact_score.abs().sort_values(ascending=False).index).head(5) if "impact_score" in override_csv.columns else override_csv.head(5)
        return {
            "available": True,
            "human_override_status": "active",
            "human_override_total_overrides": int(len(override_csv)),
            "human_override_accepted_count": int((override_type == "accepted").sum()),
            "human_override_held_count": int((override_type == "held").sum()),
            "human_override_rejected_count": int((override_type == "rejected").sum()),
            "human_override_blocked_count": int((override_type == "blocked").sum()),
            "human_override_positive_count": int((impact_status == "positive").sum()),
            "human_override_negative_count": int((impact_status == "negative").sum()),
            "human_override_unknown_count": int((impact_status == "unknown").sum()),
            "human_override_recommended_next_action": "wait_for_proposal_impact" if (impact_status == "unknown").any() else "review_successful_overrides",
            "human_override_requires_human_approval": "必須",
            "top_rows": top.to_dict(orient="records"),
        }
    return {
        "available": False,
        "human_override_status": "unavailable",
        "human_override_total_overrides": 0,
        "human_override_accepted_count": 0,
        "human_override_held_count": 0,
        "human_override_rejected_count": 0,
        "human_override_blocked_count": 0,
        "human_override_positive_count": 0,
        "human_override_negative_count": 0,
        "human_override_unknown_count": 0,
        "human_override_recommended_next_action": "wait_for_more_data",
        "human_override_requires_human_approval": "必須",
        "top_rows": [],
    }


def portfolio_layer_summary(portfolio_csv: pd.DataFrame, portfolio_json, summary_json) -> dict:
    payload = summary_json if isinstance(summary_json, dict) and summary_json else portfolio_json if isinstance(portfolio_json, dict) else {}
    rows = portfolio_json.get("portfolio_candidates", []) if isinstance(portfolio_json, dict) else []
    if payload:
        if not rows and not portfolio_csv.empty:
            rows = portfolio_csv.to_dict(orient="records")
        top_rows = sorted(rows, key=lambda row: numeric_or(row.get("portfolio_weight_candidate", 0), 0), reverse=True)[:5]
        return {
            "available": True,
            "portfolio_status": payload.get("portfolio_status", "active"),
            "portfolio_candidate_assets": int(numeric_or(payload.get("candidate_assets", len(top_rows)), 0)),
            "portfolio_defensive_assets": int(numeric_or(payload.get("defensive_assets", 0), 0)),
            "portfolio_offensive_assets": int(numeric_or(payload.get("offensive_assets", 0), 0)),
            "portfolio_cash_candidate": numeric_or(payload.get("cash_candidate", payload.get("cash_ratio_candidate", 0)), 0),
            "portfolio_average_confidence": numeric_or(payload.get("average_confidence", 0), 0),
            "portfolio_concentration": numeric_or(payload.get("portfolio_concentration", 0), 0),
            "portfolio_risk_concentration": numeric_or(payload.get("risk_concentration", 0), 0),
            "portfolio_recommended_exposure": numeric_or(payload.get("recommended_exposure", 0), 0),
            "portfolio_recommended_next_action": payload.get("recommended_next_action", "human_review_allocations"),
            "portfolio_requires_human_approval": "必須" if payload.get("requires_human_approval", True) else "不要",
            "top_rows": top_rows,
        }
    if not portfolio_csv.empty:
        weights = pd.to_numeric(portfolio_csv.get("portfolio_weight_candidate", pd.Series(dtype=float)), errors="coerce").fillna(0)
        confidence = pd.to_numeric(portfolio_csv.get("confidence", pd.Series(dtype=float)), errors="coerce").fillna(0)
        risk_class = portfolio_csv.get("risk_class", pd.Series(dtype=str)).fillna("").astype(str)
        risk_role = portfolio_csv.get("risk_role", pd.Series(dtype=str)).fillna("").astype(str)
        candidate_mask = weights > 0
        top = portfolio_csv.sort_values("portfolio_weight_candidate", ascending=False).head(5) if "portfolio_weight_candidate" in portfolio_csv.columns else portfolio_csv.head(5)
        return {
            "available": True,
            "portfolio_status": "active",
            "portfolio_candidate_assets": int(candidate_mask.sum()),
            "portfolio_defensive_assets": int(((risk_role == "defensive") & candidate_mask).sum()),
            "portfolio_offensive_assets": int(((risk_role == "offensive") & candidate_mask).sum()),
            "portfolio_cash_candidate": max(0.0, 1.0 - float(weights.sum())),
            "portfolio_average_confidence": float(confidence.mean()) if not confidence.empty else 0,
            "portfolio_concentration": float(weights.max()) if not weights.empty else 0,
            "portfolio_risk_concentration": float(weights[risk_class == "high"].sum()) if not weights.empty else 0,
            "portfolio_recommended_exposure": float(weights.sum()),
            "portfolio_recommended_next_action": "human_review_allocations",
            "portfolio_requires_human_approval": "必須",
            "top_rows": top.to_dict(orient="records"),
        }
    return {
        "available": False,
        "portfolio_status": "unavailable",
        "portfolio_candidate_assets": 0,
        "portfolio_defensive_assets": 0,
        "portfolio_offensive_assets": 0,
        "portfolio_cash_candidate": 0,
        "portfolio_average_confidence": 0,
        "portfolio_concentration": 0,
        "portfolio_risk_concentration": 0,
        "portfolio_recommended_exposure": 0,
        "portfolio_recommended_next_action": "generate_upstream_analysis",
        "portfolio_requires_human_approval": "必須",
        "top_rows": [],
    }


def datetime_audit_summary(audit_json, summary_json, audit_csv: pd.DataFrame) -> dict:
    payload = audit_json if isinstance(audit_json, dict) and audit_json else summary_json if isinstance(summary_json, dict) else {}
    if payload:
        return {
            "available": True,
            "datetime_audit_status": payload.get("audit_status", "unavailable"),
            "datetime_issues_found": int(numeric_or(payload.get("issues_found", len(audit_csv)), 0)),
            "datetime_timezone_mismatch": int(numeric_or(payload.get("timezone_mismatch", 0), 0)),
            "datetime_naive_datetime": int(numeric_or(payload.get("naive_datetime", 0), 0)),
            "datetime_timestamp_mismatch": int(numeric_or(payload.get("timestamp_mismatch", 0), 0)),
            "datetime_recommended_action": payload.get("recommended_action", "monitor"),
        }
    if not audit_csv.empty:
        issue_type = audit_csv.get("issue_type", pd.Series("", index=audit_csv.index)).fillna("").astype(str)
        severity = audit_csv.get("severity", pd.Series("", index=audit_csv.index)).fillna("").astype(str)
        return {
            "available": True,
            "datetime_audit_status": "warning" if (severity == "warning").any() else "passed",
            "datetime_issues_found": int(len(audit_csv)),
            "datetime_timezone_mismatch": int((issue_type == "timezone_mismatch").sum()),
            "datetime_naive_datetime": int((issue_type == "naive_datetime").sum()),
            "datetime_timestamp_mismatch": int((issue_type == "timestamp_mismatch").sum()),
            "datetime_recommended_action": "normalize_to_timestamp" if (issue_type == "timestamp_mismatch").any() else "monitor",
        }
    return {
        "available": False,
        "datetime_audit_status": "unavailable",
        "datetime_issues_found": 0,
        "datetime_timezone_mismatch": 0,
        "datetime_naive_datetime": 0,
        "datetime_timestamp_mismatch": 0,
        "datetime_recommended_action": "monitor",
    }


def pending_reevaluation_summary(pending: pd.DataFrame) -> dict:
    if pending.empty:
        return {
            "available": False,
            "pending_reevaluation_count": 0,
            "pending_reevaluation_closed_count": 0,
            "pending_reevaluation_open_count": 0,
            "pending_reevaluation_no_entry_count": 0,
            "pending_reevaluation_missed_count": 0,
            "recent_closed": [],
        }
    out = pending.copy()
    status = out.get("evaluation_status", out.get("status", pd.Series("", index=out.index))).fillna("").astype(str).str.lower()
    outcome = out.get("outcome", pd.Series("", index=out.index)).fillna("").astype(str).str.lower()
    missed = out.get("missed_opportunity", pd.Series("", index=out.index)).fillna("").astype(str).str.lower().isin(["true", "1", "yes"])
    closed_mask = (status == "closed") | outcome.isin(["win_tp1", "win_tp2", "loss_sl"])
    recent_closed = out[closed_mask].tail(5)
    return {
        "available": True,
        "pending_reevaluation_count": int(len(out)),
        "pending_reevaluation_closed_count": int(closed_mask.sum()),
        "pending_reevaluation_open_count": int((outcome == "open_unresolved").sum()),
        "pending_reevaluation_no_entry_count": int((outcome == "no_entry").sum()),
        "pending_reevaluation_missed_count": int(missed.sum()),
        "recent_closed": recent_closed.to_dict(orient="records"),
    }


def choose_evaluations_for_dashboard(data_evaluations: pd.DataFrame, extras: dict[str, object]) -> tuple[pd.DataFrame, str]:
    latest = extras.get("latest_evaluations", pd.DataFrame())
    pending = extras.get("pending_reevaluations", pd.DataFrame())
    if isinstance(latest, pd.DataFrame) and not latest.empty:
        return latest, "latest_evaluations"
    if isinstance(pending, pd.DataFrame) and not pending.empty:
        return pending, "pending_reevaluations"
    return data_evaluations, "evaluations"


def latest_evaluation_view_summary(latest: pd.DataFrame, summary_json) -> dict:
    if isinstance(summary_json, dict) and summary_json:
        return {
            "available": True,
            "latest_evaluation_unique_signal_count": int(numeric_or(summary_json.get("unique_signal_count", 0), 0)),
            "latest_evaluation_rows": int(numeric_or(summary_json.get("latest_rows", 0), 0)),
            "latest_from_pending_reevaluations": int(numeric_or(summary_json.get("latest_from_pending_reevaluations", 0), 0)),
            "latest_from_evaluations": int(numeric_or(summary_json.get("latest_from_evaluations", 0), 0)),
            "latest_evaluation_closed_count": int(numeric_or(summary_json.get("closed_count", 0), 0)),
            "latest_evaluation_pending_count": int(numeric_or(summary_json.get("pending_count", 0), 0)),
            "latest_evaluation_open_count": int(numeric_or(summary_json.get("open_count", 0), 0)),
            "latest_evaluation_no_entry_count": int(numeric_or(summary_json.get("no_entry_count", 0), 0)),
            "latest_evaluation_missed_count": int(numeric_or(summary_json.get("missed_opportunity_count", 0), 0)),
        }
    if latest.empty:
        return {
            "available": False,
            "latest_evaluation_unique_signal_count": 0,
            "latest_evaluation_rows": 0,
            "latest_from_pending_reevaluations": 0,
            "latest_from_evaluations": 0,
            "latest_evaluation_closed_count": 0,
            "latest_evaluation_pending_count": 0,
            "latest_evaluation_open_count": 0,
            "latest_evaluation_no_entry_count": 0,
            "latest_evaluation_missed_count": 0,
        }
    status = latest.get("evaluation_status", latest.get("status", pd.Series("", index=latest.index))).fillna("").astype(str).str.lower()
    outcome = latest.get("outcome", pd.Series("", index=latest.index)).fillna("").astype(str).str.lower()
    latest_source = latest.get("latest_source", pd.Series("", index=latest.index)).fillna("").astype(str)
    missed = latest.get("missed_opportunity", pd.Series("", index=latest.index)).fillna("").astype(str).str.lower().isin(["true", "1", "yes"])
    return {
        "available": True,
        "latest_evaluation_unique_signal_count": int(latest["signal_id"].nunique()) if "signal_id" in latest.columns else len(latest),
        "latest_evaluation_rows": int(len(latest)),
        "latest_from_pending_reevaluations": int((latest_source == "pending_reevaluations").sum()),
        "latest_from_evaluations": int((latest_source == "evaluations").sum()),
        "latest_evaluation_closed_count": int((status == "closed").sum()),
        "latest_evaluation_pending_count": int((status == "pending").sum()),
        "latest_evaluation_open_count": int(((status == "open") | (outcome == "open_unresolved")).sum()),
        "latest_evaluation_no_entry_count": int((outcome == "no_entry").sum()),
        "latest_evaluation_missed_count": int(missed.sum()),
    }


def top_reason_codes(reason_table: pd.DataFrame) -> dict:
    if reason_table.empty:
        return {"positive": [], "negative": [], "insufficient": []}
    positive = reason_table[reason_table["reliability_label"].isin(["strong_positive", "positive"])].head(5) if "reliability_label" in reason_table.columns else pd.DataFrame()
    negative = (
        reason_table[reason_table["reliability_label"].isin(["strong_negative", "negative"])].sort_values("average_r").head(5)
        if {"reliability_label", "average_r"}.issubset(reason_table.columns)
        else pd.DataFrame()
    )
    insufficient = reason_table[reason_table["reliability_label"].astype(str) == "insufficient_data"].head(5) if "reliability_label" in reason_table.columns else pd.DataFrame()
    return {
        "positive": positive.to_dict(orient="records"),
        "negative": negative.to_dict(orient="records"),
        "insufficient": insufficient.to_dict(orient="records"),
    }


def json_safe(value):
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [json_safe(v) for v in value]
    if isinstance(value, tuple):
        return [json_safe(v) for v in value]
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if not isinstance(value, (dict, list, tuple)):
        try:
            if pd.isna(value):
                return None
        except (TypeError, ValueError):
            pass
    if hasattr(value, "item"):
        try:
            return value.item()
        except (ValueError, TypeError):
            pass
    return value


def build_dashboard() -> tuple[dict, str]:
    data, extras, source = load_data()
    snapshot = data["market_snapshot"]
    signals = data["signals"]
    raw_evaluations = data["evaluations"]
    weekly = extras["weekly_review"]
    monthly = extras["monthly_calibration"]
    ai_feedback = extras["ai_feedback"]
    news_summary = news_narrative_summary(extras["news_narrative_scores"], extras["news_narrative_scores_json"])
    pending_summary = pending_reevaluation_summary(extras["pending_reevaluations"])
    evaluations, evaluation_view_source = choose_evaluations_for_dashboard(raw_evaluations, extras)
    evaluation_fallback_used = evaluation_view_source != "latest_evaluations"
    latest_eval_summary = latest_evaluation_view_summary(extras["latest_evaluations"], extras["latest_evaluations_summary_json"])
    reason_table, no_trade_table = reason_code_data(signals, evaluations, extras["reason_code_analysis"], extras["reason_code_analysis_json"])
    rule_updates = extras["rule_update_proposals"]
    model_state_updates = extras["model_state_update_proposals"]
    ai_summary = ai_feedback_summary(ai_feedback, extras["ai_feedback_json"])
    model_state_summary = model_state_update_summary(
        model_state_updates,
        extras["model_state_update_proposals_json"],
        extras["model_state_update_summary_json"],
    )
    model_state_audit = model_state_audit_summary(
        extras["model_state_proposal_audit_json"],
        extras["model_state_proposal_audit"],
    )
    model_state_summary.update(model_state_audit)
    weights_patch = weights_patch_summary(
        extras["weights_patch_proposal"],
        extras["weights_patch_proposal_json"],
        extras["weights_patch_summary_json"],
    )
    weights_patch_review = weights_patch_review_summary(
        extras["weights_patch_review"],
        extras["weights_patch_review_json"],
        extras["weights_patch_review_summary_json"],
    )
    proposal_adoption = proposal_adoption_summary(
        extras["proposal_adoption_tracking"],
        extras["proposal_adoption_tracking_json"],
        extras["proposal_adoption_tracking_summary_json"],
    )
    weight_history = weight_version_history_summary(
        extras["weight_version_history"],
        extras["weight_version_history_json"],
        extras["weight_version_history_summary_json"],
    )
    meta_learning = meta_learning_summary(
        extras["meta_learning"],
        extras["meta_learning_json"],
        extras["meta_learning_summary_json"],
    )
    auto_calibration = auto_calibration_summary(
        extras["auto_calibration_candidates"],
        extras["auto_calibration_candidates_json"],
        extras["auto_calibration_candidates_summary_json"],
    )
    human_override = human_override_summary(
        extras["human_override_analytics"],
        extras["human_override_analytics_json"],
        extras["human_override_analytics_summary_json"],
    )
    portfolio_layer = portfolio_layer_summary(
        extras["portfolio_layer"],
        extras["portfolio_layer_json"],
        extras["portfolio_layer_summary_json"],
    )
    datetime_health = datetime_audit_summary(
        extras["datetime_audit_json"],
        extras["datetime_audit_summary_json"],
        extras["datetime_audit"],
    )
    latest_sig = latest_signals(signals)
    sig_summary = signal_summary(latest_sig)
    eval_summary = evaluation_summary(evaluations)
    asset_table = asset_performance(signals, evaluations)
    mode = weekly_monthly_mode(weekly, monthly)
    reason_tops = top_reason_codes(reason_table)
    generated_dt_utc = now_utc()
    generated_at_jst = format_jst(generated_dt_utc)
    generated_at_utc = format_utc(generated_dt_utc)
    generated = generated_at_jst
    row_counts = {
        "market_snapshot": len(snapshot),
        "signals": len(signals),
        "evaluations": len(evaluations),
        "raw_evaluations": len(raw_evaluations),
        "latest_evaluations": len(extras["latest_evaluations"]),
        "weekly_review": len(weekly),
        "monthly_calibration": len(monthly),
        "reason_code_analysis": len(reason_table),
        "rule_update_proposals": len(rule_updates),
        "model_state_update_proposals": len(model_state_updates),
        "weights_patch_proposal": len(extras["weights_patch_proposal"]),
        "weights_patch_review": len(extras["weights_patch_review"]),
        "proposal_adoption_tracking": len(extras["proposal_adoption_tracking"]),
        "weight_version_history": len(extras["weight_version_history"]),
        "meta_learning": len(extras["meta_learning"]),
        "auto_calibration_candidates": len(extras["auto_calibration_candidates"]),
        "human_override_analytics": len(extras["human_override_analytics"]),
        "portfolio_layer": len(extras["portfolio_layer"]),
        "datetime_audit": len(extras["datetime_audit"]),
        "ai_feedback": len(ai_feedback),
        "news_narrative_scores": 1 if news_summary.get("available") else 0,
        "pending_reevaluations": len(extras["pending_reevaluations"]),
    }
    latest_signal_date = latest_date(signals, ["signal_date", "date"])
    latest_evaluation_date = latest_date(evaluations, ["evaluation_date", "hit_date", "signal_date"])
    data_reference_date = latest_signal_date or latest_evaluation_date or latest_date(snapshot, ["date", "timestamp", "run_ts"])
    latest_dates = {
        "latest_signal_date": latest_signal_date,
        "latest_evaluation_date": latest_evaluation_date,
        "latest_daily_report_date": latest_file_date("reports/*.md"),
        "latest_weekly_review_date": latest_file_date("reports/weekly/*_weekly_review.md"),
        "latest_monthly_calibration_date": latest_file_date("reports/monthly/*_monthly_calibration.md"),
        "latest_reason_code_analysis_date": latest_file_date("reports/reason_codes/*_reason_code_analysis.md"),
        "latest_rule_update_proposals_date": latest_file_date("reports/rule_updates/*_rule_update_proposals.md"),
        "latest_model_state_update_proposals_date": latest_file_date("reports/model_state/*_model_state_update_proposals.md"),
        "latest_ai_feedback_date": latest_file_date("reports/ai_feedback/*_ai_feedback.md") or ai_summary["latest_date"],
    }
    apply_false = True
    if not rule_updates.empty and "apply_automatically" in rule_updates.columns:
        apply_false = rule_updates["apply_automatically"].fillna(False).astype(str).str.lower().isin(["false", "0", "no"]).all()
    rule_update_summary = {
        "count": int(len(rule_updates)),
        "high_priority": int((rule_updates.get("proposal_strength", pd.Series(dtype=str)).astype(str) == "HIGH").sum()) if not rule_updates.empty else 0,
        "apply_automatically_all_false": bool(apply_false),
    }
    summary = json_safe({
        "generated_at": generated,
        "generated_at_jst": generated_at_jst,
        "generated_at_utc": generated_at_utc,
        "timezone": "Asia/Tokyo",
        "data_reference_date": data_reference_date,
        "display_language": "ja",
        "data_source": source,
        "evaluation_view_source": evaluation_view_source,
        "evaluation_fallback_used": evaluation_fallback_used,
        "row_counts": row_counts,
        "latest_dates": latest_dates,
        "daily_signal_summary": sig_summary,
        "evaluation_summary": eval_summary,
        "asset_performance": asset_table.to_dict(orient="records"),
        "top_reason_codes": reason_tops,
        "rule_update_summary": rule_update_summary,
        "model_state_update_summary": model_state_summary,
        "weights_patch_summary": weights_patch,
        "weights_patch_review_summary": weights_patch_review,
        "proposal_adoption_summary": proposal_adoption,
        "weight_version_history_summary": weight_history,
        "meta_learning_summary": meta_learning,
        "auto_calibration_summary": auto_calibration,
        "human_override_summary": human_override,
        "portfolio_layer_summary": portfolio_layer,
        "datetime_audit_summary": datetime_health,
        "ai_feedback_summary": ai_summary,
        "news_narrative_summary": news_summary,
        "pending_reevaluation_summary": pending_summary,
        "latest_evaluation_view_summary": latest_eval_summary,
        "safety_notes": SAFETY_NOTES,
    })

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "dashboard_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    html_text = render_html(
        generated=generated,
        generated_at_jst=generated_at_jst,
        generated_at_utc=generated_at_utc,
        data_reference_date=data_reference_date,
        source=source,
        latest_dates=latest_dates,
        row_counts=row_counts,
        signals=latest_sig,
        signal_counts=sig_summary,
        eval_summary=eval_summary,
        asset_table=asset_table,
        reason_table=reason_table,
        no_trade_table=no_trade_table,
        rule_updates=rule_updates,
        model_state_updates=model_state_updates,
        model_state_summary=model_state_summary,
        weights_patch=weights_patch,
        weights_patch_review=weights_patch_review,
        proposal_adoption=proposal_adoption,
        weight_history=weight_history,
        meta_learning=meta_learning,
        auto_calibration=auto_calibration,
        human_override=human_override,
        portfolio_layer=portfolio_layer,
        datetime_health=datetime_health,
        mode=mode,
        ai_summary=ai_summary,
        news_summary=news_summary,
        pending_summary=pending_summary,
        latest_eval_summary=latest_eval_summary,
        evaluation_view_source=evaluation_view_source,
        evaluation_fallback_used=evaluation_fallback_used,
        apply_false=apply_false,
        summary=summary,
    )
    html_path = REPORTS_DIR / "index.html"
    html_path.write_text(html_text, encoding="utf-8")
    print(f"dashboard generated: {html_path}")
    print(f"dashboard summary generated: {REPORTS_DIR / 'dashboard_summary.json'}")
    return summary, str(html_path)


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
    <section class="card"><h2>システム状態</h2><div class="grid">{system_stats}</div></section>
    <section class="card"><h2>System Health</h2>{'<div class="empty">Datetime Audit未取得</div>' if not datetime_health.get('available') else f'<div class="grid">{datetime_stats}</div>'}</section>
    <section class="card"><h2>本日のシグナル概要</h2><div class="grid">{signal_stats}</div>{table_html(signals, ["asset","side","rank","type","recommended_action","signal_strength","setup_quality_score","entry_quality_score","direction_confidence","reason_codes","no_trade_reason"])}</section>
    <section class="card"><h2>評価概要</h2><div class="grid">{eval_stats}</div></section>
    <section class="card"><h2>資産別成績</h2>{table_html(asset_table, ["asset","signals","evaluations","win_rate","total_r","average_r","missed_opportunity_count"])}</section>
    <section class="card"><h2>判断理由コード別成績</h2><h3>プラス寄与が大きい理由</h3>{table_html(top_positive, ["reason_code","signals_count","evaluated_count","win_rate","average_r","total_r","reliability_label"])}<h3>マイナス寄与が大きい理由</h3>{table_html(top_negative, ["reason_code","signals_count","evaluated_count","win_rate","average_r","total_r","reliability_label"])}<h3>データ不足</h3>{table_html(insufficient, ["reason_code","signals_count","evaluated_count","win_rate","average_r","total_r","reliability_label"])}</section>
    <section class="card"><h2>見送り理由分析</h2>{table_html(no_trade_table, ["no_trade_reason","count","missed_opportunity_count","average_mfe_r","assessment"], "見送り理由データなし")}</section>
    <section class="card"><h2>ルール改善候補</h2><p class="notice">すべての改善候補は自動適用されません: <strong>{str(apply_false).lower()}</strong></p>{table_html(rule_view, ["proposal_type","target_type","target_name","proposal_strength","priority","average_r","win_rate","proposed_change","apply_automatically"])}</section>
    <section class="card"><h2>Model State 更新提案</h2>{'<div class="empty">Model State更新提案未取得</div>' if not model_state_summary.get('available') else f'<div class="grid">{model_state_stats}</div>'}<h3>strong候補 上位5件</h3>{table_html(model_state_strong, ["category","target","sample_count","win_rate","avg_r","proposal_direction","proposal_strength","proposed_delta","proposed_weight","rationale"], "strong候補なし")}</section>
    <section class="card"><h2>Weights Patch候補</h2>{'<div class="empty">Weights Patch候補未取得</div>' if not weights_patch.get('available') else f'<div class="grid">{weights_patch_stats}</div>'}<h3>patch候補 上位5件</h3>{table_html(weights_patch_candidates, ["weight_path","patch_action","current_weight","proposed_delta","proposed_value","proposal_direction","proposal_strength","rationale"], "patch候補なし")}</section>
    <section class="card"><h2>Weights Patchレビュー</h2>{'<div class="empty">Weights Patchレビュー未取得</div>' if not weights_patch_review.get('available') else f'<div class="grid">{weights_patch_review_stats}</div>'}<h3>承認候補 上位5件</h3>{table_html(weights_patch_review_candidates, ["weight_path","review_decision","recommended_human_action","sample_count","confidence_level","proposal_strength","proposed_delta","patch_risk_level","review_reason"], "承認候補なし")}<h3>保留候補 上位5件</h3>{table_html(weights_patch_review_holds, ["weight_path","review_decision","recommended_human_action","sample_count","confidence_level","proposal_strength","proposed_delta","evidence_quality","missing_conditions","review_reason"], "保留候補なし")}</section>
    <section class="card"><h2>Proposal Adoption Tracking</h2>{'<div class="empty">Proposal Adoption Tracking未取得</div>' if not proposal_adoption.get('available') else f'<div class="grid">{proposal_adoption_stats}</div>'}<h3>承認判断待ち 上位5件</h3>{table_html(proposal_adoption_pending, ["weight_path","adoption_status","adoption_source","recommended_next_action","sample_count","confidence_level","proposal_strength","tracking_reason"], "承認判断待ちなし")}<h3>保留中 上位5件</h3>{table_html(proposal_adoption_held, ["weight_path","adoption_status","adoption_source","recommended_next_action","sample_count","confidence_level","proposal_strength","tracking_reason"], "保留中なし")}</section>
    <section class="card"><h2>Weight Version History</h2>{'<div class="empty">Weight Version History未取得</div>' if not weight_history.get('available') else f'<div class="grid">{weight_history_stats}</div>'}<h3>Proposal一覧 上位5件</h3>{table_html(weight_history_rows, ["version_id","source","proposal_id","review_decision","adoption_status","description","weights_json_updated","patch_applied","requires_human_approval","notes"], "履歴Proposalなし")}</section>
    <section class="card"><h2>Meta Learning</h2>{'<div class="empty">Meta Learning未取得</div>' if not meta_learning.get('available') else f'<div class="grid">{meta_learning_stats}</div>'}<h3>成功パターン候補 上位5件</h3>{table_html(meta_learning_success, ["meta_learning_id","pattern_type","category","target","proposal_id","impact_score","sample_count","confidence_level","recommended_action","learning_hypothesis"], "成功パターン候補なし")}<h3>失敗パターン候補 上位5件</h3>{table_html(meta_learning_failure, ["meta_learning_id","pattern_type","category","target","proposal_id","impact_score","sample_count","confidence_level","recommended_action","learning_hypothesis"], "失敗パターン候補なし")}</section>
    <section class="card"><h2>Auto Calibration Candidates</h2>{'<div class="empty">Auto Calibration Candidates未取得</div>' if not auto_calibration.get('available') else f'<div class="grid">{auto_calibration_stats}</div>'}<h3>top confidence candidates</h3>{table_html(auto_calibration_top, ["candidate_id","asset","category","target","factor","classification","current_value","suggested_delta","suggested_value","confidence","sample_size","source","rationale"], "候補なし")}</section>
    <section class="card"><h2>Human Override Analytics</h2>{'<div class="empty">Human Override Analytics未取得</div>' if not human_override.get('available') else f'<div class="grid">{human_override_stats}</div>'}<h3>override impact 上位5件</h3>{table_html(human_override_top, ["proposal_id","review_decision","adoption_status","override_type","override_reason","impact_status","impact_score","source","recommended_next_action"], "override分析なし")}</section>
    <section class="card"><h2>Portfolio Layer</h2>{'<div class="empty">Portfolio Layer未取得</div>' if not portfolio_layer.get('available') else f'<div class="grid">{portfolio_stats}</div>'}<h3>top allocation candidates</h3>{table_html(portfolio_top, ["asset","allocation_score","portfolio_weight_candidate","confidence","risk_class","risk_role","recommended_exposure","cash_ratio_candidate","latest_rank","latest_side","rationale"], "配分候補なし")}</section>
    <section class="card"><h2>ニュースナラティブ要約</h2><div class="grid">{news_stats}</div><h3>Top News Drivers</h3><ul>{news_driver_list}</ul></section>
    <section class="card"><h2>AIフィードバック要約</h2><div class="grid">{ai_stats}</div><h3>上位の改善仮説</h3><ul>{ai_hypothesis_list}</ul></section>
    <section class="card"><h2>Pending再評価 要約</h2>{'<div class="empty">Pending再評価未取得</div>' if not pending_summary.get('available') else f'<div class="grid">{pending_stats}</div>'}<h3>直近決着シグナル上位5件</h3>{table_html(pending_closed, ["signal_id","asset","side","rank","previous_outcome","outcome","r_multiple","error_type"], "直近決着シグナルなし")}</section>
    <section class="card"><h2>最新評価ビュー 要約</h2>{'<div class="empty">最新評価ビュー未取得</div>' if not latest_eval_summary.get('available') else f'<div class="grid">{latest_eval_stats}</div>'}</section>
    <section class="card"><h2>週次・月次モード</h2><div class="grid">{mode_stats}</div></section>
    <section class="card"><h2>安全上の注意</h2><p class="notice">{html.escape(DASHBOARD_DESCRIPTION)}</p><ul>{safe}</ul></section>
  </main>
  <script type="application/json" id="dashboard-summary">{html.escape(json.dumps(summary, ensure_ascii=False))}</script>
</body>
</html>
"""


def main() -> int:
    build_dashboard()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
