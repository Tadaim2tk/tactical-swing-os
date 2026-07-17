from __future__ import annotations

"""Dashboard オーケストレーション (分割後の薄い本体)。

データ読込→サマリー作成→dashboard_summary.json書き込み→HTML描画→index.html書き込み。
出力(reports/dashboard/index.html, dashboard_summary.json)は分割前と完全互換。
"""

import json
from pathlib import Path

import pandas as pd

from time_utils import format_jst, format_utc, now_utc

from dashboard_io import *  # noqa: F401,F403
from dashboard_summaries import *  # noqa: F401,F403
from dashboard_render import *  # noqa: F401,F403


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
    prediction_calibration = prediction_calibration_summary(
        extras["prediction_calibration_json"],
        extras["prediction_calibration"],
    )
    narrative_reliability = narrative_reliability_summary(
        extras["narrative_reliability_json"],
        extras["narrative_reliability"],
    )
    similar_narrative = similar_narrative_summary(
        extras["similar_narrative_cases"],
        extras["similar_narrative_summary_json"],
    )
    prediction_log = prediction_log_summary(
        extras["prediction_log_scores"],
        extras["prediction_log_summary_json"],
    )
    todays_judgements = todays_judgements_summary(
        extras["signal_ledger"],
        extras["prediction_log_scores"],
    )
    performance_series = performance_series_summary(
        extras["prediction_log_scores"],
        extras["signal_ledger"],
    )
    execution_view = execution_view_summary(
        extras["prediction_log_scores"],
        extras["signal_ledger"],
    )
    execution_sim = execution_sim_summary(extras["execution_simulation"])
    generated_dt_utc = now_utc()
    dashboard_as_of = generated_dt_utc.date().isoformat()
    transaction_cost = transaction_cost_summary(evaluations, extras["cost_model_json"], as_of=dashboard_as_of)
    audit_report = audit_report_summary(extras["latest_audit_status"])
    narrative_lookahead = narrative_lookahead_summary(
        extras["narrative_lookahead_audit_summary_json"],
        extras["narrative_lookahead_audit"],
    )
    adversarial_review = adversarial_review_summary(
        extras["adversarial_review_summary_json"],
        extras["adversarial_review"],
    )
    latest_sig = latest_signals(signals)
    sig_summary = signal_summary(latest_sig)
    eval_summary = evaluation_summary(evaluations, as_of=dashboard_as_of)
    asset_table = asset_performance(signals, evaluations, as_of=dashboard_as_of)
    mode = weekly_monthly_mode(weekly, monthly)
    reason_tops = top_reason_codes(reason_table)
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
        "prediction_calibration": len(extras["prediction_calibration"]),
        "narrative_reliability": len(extras["narrative_reliability"]),
        "similar_narrative_cases": len(extras["similar_narrative_cases"]),
        "prediction_log_scores": len(extras["prediction_log_scores"]),
        "narrative_lookahead_audit": len(extras["narrative_lookahead_audit"]),
        "adversarial_review": len(extras["adversarial_review"]),
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
    # Phase 24: Data Health / Freshness (古い・空のデータを正常と誤読しないガード)
    data_health = data_health_summary(extras, row_counts, latest_dates, generated_dt_utc)
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
        "prediction_calibration_summary": prediction_calibration,
        "narrative_reliability_summary": narrative_reliability,
        "similar_narrative_summary": similar_narrative,
        "prediction_log_summary": {k: v for k, v in prediction_log.items() if k not in ("rank_table", "recent_table")},
        "transaction_cost_summary": transaction_cost,
        "audit_report_summary": audit_report,
        "narrative_lookahead_summary": narrative_lookahead,
        "adversarial_review_summary": adversarial_review,
        "data_health_summary": data_health,
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
        prediction_calibration=prediction_calibration,
        prediction_calibration_table=extras["prediction_calibration"],
        narrative_reliability=narrative_reliability,
        narrative_reliability_table=extras["narrative_reliability"],
        transaction_cost=transaction_cost,
        audit_report=audit_report,
        narrative_lookahead=narrative_lookahead,
        narrative_lookahead_table=extras["narrative_lookahead_audit"],
        adversarial_review=adversarial_review,
        adversarial_review_table=extras["adversarial_review"],
        data_health=data_health,
        mode=mode,
        ai_summary=ai_summary,
        news_summary=news_summary,
        pending_summary=pending_summary,
        latest_eval_summary=latest_eval_summary,
        evaluation_view_source=evaluation_view_source,
        evaluation_fallback_used=evaluation_fallback_used,
        similar_narrative=similar_narrative,
        similar_table=extras["similar_narrative_cases"],
        prediction_log=prediction_log,
        apply_false=apply_false,
        todays_judgements=todays_judgements,
        performance_series=performance_series,
        execution_view=execution_view,
        execution_sim=execution_sim,
        summary=summary,
    )
    html_path = REPORTS_DIR / "index.html"
    html_path.write_text(html_text, encoding="utf-8")
    print(f"dashboard generated: {html_path}")
    print(f"dashboard summary generated: {REPORTS_DIR / 'dashboard_summary.json'}")
    return summary, str(html_path)


def main() -> int:
    build_dashboard()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
