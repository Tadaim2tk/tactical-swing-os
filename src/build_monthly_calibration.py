from __future__ import annotations

import argparse
import json
import math
from datetime import datetime
from pathlib import Path

import pandas as pd

import evaluation_loader
import stat_guards
from calibration_io import (  # noqa: F401 - 後方互換のため再エクスポート
    RESULTS_DIR,
    SCOPES,
    SHEET_MAPPINGS,
    get_sheets_client,
    load_from_local_csv,
    load_from_sheets,
    load_input_data,
    normalize_column_name,
    normalize_headers,
    read_csv,
    worksheet_to_dataframe,
)
from calibration_report import markdown_table, render_monthly_report  # noqa: F401


REPORTS_DIR = Path("reports/monthly")
WEIGHTS_PATH = Path("models/weights.json")
DATE_COLUMNS = ["date", "signal_date", "evaluation_date", "hit_date", "run_ts"]
LOG_COLUMNS = [
    "month_start",
    "month_end",
    "total_signals",
    "closed_signals",
    "pending_signals",
    "skipped_signals",
    "win_rate",
    "profit_factor",
    "total_r",
    "average_r",
    "max_win_r",
    "max_loss_r",
    "best_asset",
    "worst_asset",
    "best_rank",
    "worst_rank",
    "best_side",
    "worst_side",
    "next_month_mode",
    "max_daily_risk_pct",
    "weight_change_summary",
    "rule_change_1",
    "rule_change_2",
    "rule_change_3",
    "evaluation_source",
    "latest_evaluations_available",
    "fallback_used",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Tactical Swing OS monthly calibration.")
    parser.add_argument("--start", help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end", help="End date in YYYY-MM-DD format")
    return parser.parse_args()


def default_period() -> tuple[pd.Timestamp, pd.Timestamp]:
    end = pd.Timestamp(datetime.now().date())
    start = end - pd.Timedelta(days=29)
    return start, end


def find_date_column(df: pd.DataFrame) -> str | None:
    for col in DATE_COLUMNS:
        if col in df.columns:
            return col
    return None


def filter_period(df: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    date_col = find_date_column(df)
    if not date_col:
        return df.copy()
    out = df.copy()
    out["_calibration_date"] = pd.to_datetime(out[date_col], errors="coerce", utc=True).dt.tz_localize(None)
    mask = (out["_calibration_date"].dt.date >= start.date()) & (out["_calibration_date"].dt.date <= end.date())
    return out[mask].drop(columns=["_calibration_date"])


def enrich_evaluations(evaluations: pd.DataFrame, signals: pd.DataFrame) -> pd.DataFrame:
    if evaluations.empty or signals.empty or "signal_id" not in evaluations.columns or "signal_id" not in signals.columns:
        return evaluations.copy()
    cols = [col for col in ["signal_id", "asset", "side", "rank", "regime", "date"] if col in signals.columns]
    lookup = signals[cols].drop_duplicates(subset=["signal_id"], keep="last")
    out = evaluations.merge(lookup, on="signal_id", how="left", suffixes=("", "_signal"))
    for col in ["asset", "side", "rank", "regime"]:
        signal_col = f"{col}_signal"
        if signal_col in out.columns:
            if col in out.columns:
                out[col] = out[col].fillna(out[signal_col])
            else:
                out[col] = out[signal_col]
            out = out.drop(columns=[signal_col])
    return out.drop(columns=[col for col in ["date_signal"] if col in out.columns])


def closed_df(evaluations: pd.DataFrame) -> pd.DataFrame:
    if evaluations.empty or "evaluation_status" not in evaluations.columns:
        return pd.DataFrame()
    return evaluations[evaluations["evaluation_status"].astype(str).str.lower() == "closed"].copy()


def numeric_r(df: pd.DataFrame) -> pd.Series:
    if df.empty or "r_result" not in df.columns:
        return pd.Series(dtype=float)
    return pd.to_numeric(df["r_result"], errors="coerce").dropna()


def r_metrics(evaluations: pd.DataFrame) -> dict:
    closed = closed_df(evaluations)
    r = numeric_r(closed)
    wins = r[r > 0]
    losses = r[r < 0]
    closed_count = len(closed)
    gross_profit = float(wins.sum()) if not wins.empty else 0.0
    gross_loss = abs(float(losses.sum())) if not losses.empty else 0.0
    if gross_loss > 0:
        profit_factor = gross_profit / gross_loss
    elif gross_profit > 0:
        profit_factor = math.inf
    else:
        profit_factor = 0.0
    return {
        "closed_count": closed_count,
        "win_rate": float(len(wins) / closed_count) if closed_count else 0.0,
        "profit_factor": profit_factor,
        "total_r": float(r.sum()) if not r.empty else 0.0,
        "average_r": float(r.mean()) if not r.empty else 0.0,
        "max_win_r": float(r.max()) if not r.empty else 0.0,
        "max_loss_r": float(r.min()) if not r.empty else 0.0,
    }


def count_status(evaluations: pd.DataFrame, status: str) -> int:
    if evaluations.empty or "evaluation_status" not in evaluations.columns:
        return 0
    return int((evaluations["evaluation_status"].astype(str).str.lower() == status).sum())


def proposed_change(
    closed_count: int,
    win_rate: float,
    average_r: float,
    r_values: list[float] | None = None,
) -> tuple[float, str]:
    """重み変更提案 (SPEC-SG-001)。

    憲章ルールの実装:
    - n >= 30 (MIN_SAMPLES_WEIGHT_CHANGE) 未満は提案禁止
    - 一標本t検定 p < 0.05 (SIGNIFICANCE_ALPHA) を満たさない場合は提案禁止
    - 増加提案: 有意性に加えて Sharpe > 0.5 を要求(過学習ブレーキ)
    - 減少提案: 有意性のみ要求(Ruin回避を優先し、Sharpe閾値は課さない)
    reason文字列には n / win / avg_r / sharpe / p を必ず記録する(後日監査用)。
    """
    if closed_count < stat_guards.MIN_SAMPLES_WEIGHT_CHANGE:
        return 0.0, f"データ不足 (n={closed_count} < {stat_guards.MIN_SAMPLES_WEIGHT_CHANGE})"
    report = stat_guards.significance_report(r_values or [])
    stats_note = (
        f"n={closed_count}, win={win_rate:.2f}, avg_r={average_r:.3f}, "
        f"sharpe={report['sharpe']:.3f}, p={report['p_value']:.4f}"
    )
    if not report["significant"]:
        return 0.0, f"統計的有意性なし (p >= {stat_guards.SIGNIFICANCE_ALPHA}) | {stats_note}"
    if average_r < -0.3:
        return -0.05, f"average_r < -0.3 (有意・リスク優先) | {stats_note}"
    if average_r < -0.1:
        return -0.03, f"average_r < -0.1 (有意・リスク優先) | {stats_note}"
    if report["sharpe"] <= stat_guards.MIN_SHARPE_FOR_INCREASE:
        return 0.0, f"Sharpe <= {stat_guards.MIN_SHARPE_FOR_INCREASE} のため増加提案を保留 | {stats_note}"
    if average_r > 0.3 and win_rate >= 0.5:
        return 0.05, f"average_r > 0.3 and win_rate >= 0.5 | {stats_note}"
    if average_r > 0.1 and win_rate >= 0.45:
        return 0.03, f"average_r > 0.1 and win_rate >= 0.45 | {stats_note}"
    return 0.0, f"変更なし | {stats_note}"


# SPEC-RD-001: 減衰の年齢は「結果が確定した日」で測る(シグナル日ではなく評価日を優先)
DECAY_DATE_COLUMNS = ["evaluation_date", "hit_date", "date", "signal_date", "run_ts"]


def decayed_metrics(eval_part: pd.DataFrame, as_of: pd.Timestamp | None) -> dict[str, float] | None:
    """closed評価の減衰加重統計(SPEC-RD-001)。日付が取れない場合はNone。"""
    if as_of is None:
        return None
    closed = closed_df(eval_part)
    if closed.empty or "r_result" not in closed.columns:
        return None
    date_col = next((col for col in DECAY_DATE_COLUMNS if col in closed.columns), None)
    if date_col is None:
        return None
    r = pd.to_numeric(closed["r_result"], errors="coerce")
    dates = pd.to_datetime(closed[date_col], errors="coerce", utc=True).dt.tz_localize(None)
    values: list[float] = []
    ages: list[float] = []
    for value, date in zip(r, dates):
        if pd.isna(value) or pd.isna(date):
            continue
        values.append(float(value))
        ages.append(float((as_of - date).days))
    if not values:
        return None
    return stat_guards.decayed_mean(values, ages)


def calibration_table(
    signals: pd.DataFrame,
    evaluations: pd.DataFrame,
    column: str,
    values: list[str] | None = None,
    as_of: pd.Timestamp | None = None,
) -> pd.DataFrame:
    if values is None:
        observed = set(signals[column].dropna().astype(str)) if column in signals.columns and not signals.empty else set()
        observed |= set(evaluations[column].dropna().astype(str)) if column in evaluations.columns and not evaluations.empty else set()
        values = sorted(observed)
    rows = []
    for value in values:
        sig_part = signals[signals[column].astype(str) == value] if column in signals.columns and not signals.empty else pd.DataFrame()
        eval_part = evaluations[evaluations[column].astype(str) == value] if column in evaluations.columns and not evaluations.empty else pd.DataFrame()
        metrics = r_metrics(eval_part)
        r_values = numeric_r(closed_df(eval_part)).tolist()
        change, reason = proposed_change(metrics["closed_count"], metrics["win_rate"], metrics["average_r"], r_values)
        decayed = decayed_metrics(eval_part, as_of)
        decayed_avg_r = decayed["decayed_mean"] if decayed else 0.0
        effective_n = decayed["effective_n"] if decayed else 0.0
        # レジームシフト検知: 全期間平均と減衰平均の符号が逆 = 最近成績が反転している兆候
        decay_divergence = bool(
            decayed is not None
            and metrics["average_r"] * decayed_avg_r < 0
            and abs(metrics["average_r"]) > 0.05
            and abs(decayed_avg_r) > 0.05
        )
        rows.append(
            {
                column: value,
                "signals": len(sig_part),
                "closed": metrics["closed_count"],
                "win_rate": round(metrics["win_rate"], 4),
                "total_r": round(metrics["total_r"], 4),
                "average_r": round(metrics["average_r"], 4),
                "decayed_avg_r": round(decayed_avg_r, 4),
                "effective_n": round(effective_n, 2),
                "decay_divergence": decay_divergence,
                "best_r": round(metrics["max_win_r"], 4),
                "worst_r": round(metrics["max_loss_r"], 4),
                "proposed_weight_change": change,
                "reason": reason,
            }
        )
    return pd.DataFrame(rows)


def best_worst(table: pd.DataFrame, label_col: str) -> tuple[str, str]:
    if table.empty or "total_r" not in table.columns:
        return "", ""
    scored = table.copy()
    scored["total_r"] = pd.to_numeric(scored["total_r"], errors="coerce")
    scored = scored.dropna(subset=["total_r"])
    if scored.empty:
        return "", ""
    best = str(scored.sort_values("total_r", ascending=False).iloc[0][label_col])
    worst = str(scored.sort_values("total_r", ascending=True).iloc[0][label_col])
    return best, worst


def next_month_decision(metrics: dict) -> tuple[str, float, list[str]]:
    total_r = metrics["total_r"]
    win_rate = metrics["win_rate"]
    closed_count = metrics["closed_count"]
    notes = []
    if total_r > 3.0 and win_rate >= 0.5:
        mode = "攻撃"
    elif total_r >= 0 and win_rate >= 0.4:
        mode = "通常"
    else:
        mode = "防御"
    if closed_count < 10:
        mode = "通常"
        notes.append("データ不足")
    risk = {"攻撃": 1.0, "通常": 0.5, "防御": 0.25}[mode]
    return mode, risk, notes


def weight_change_summary(*tables: pd.DataFrame) -> str:
    changes = []
    for table in tables:
        if table.empty or "proposed_weight_change" not in table.columns:
            continue
        label_col = table.columns[0]
        for _, row in table.iterrows():
            change = float(row["proposed_weight_change"])
            if change:
                changes.append(f"{label_col}:{row[label_col]} {change:+.2f}")
    return "; ".join(changes) if changes else "変更提案なし"


def rule_changes(metrics: dict, mode_notes: list[str], summary: str) -> list[str]:
    changes = []
    if metrics["closed_count"] < 10:
        changes.append("closed評価10件未満のため自動適用しない")
    if summary != "変更提案なし":
        changes.append("提案のみ。weights.jsonは更新しない")
    if metrics["total_r"] < 0:
        changes.append("Entry/SL/Rank判定の見直し")
    elif metrics["total_r"] > 0 and metrics["win_rate"] >= 0.45:
        changes.append("現行ルール維持")
    changes.extend(mode_notes)
    while len(changes) < 3:
        changes.append("")
    return changes[:3]


def load_reason_code_analysis() -> pd.DataFrame:
    path = RESULTS_DIR / "reason_code_analysis.csv"
    if not path.exists():
        return pd.DataFrame()
    return read_csv(path)


def monthly_reason_code_memo(reasons: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, str]:
    if reasons.empty or "reliability_label" not in reasons.columns:
        return pd.DataFrame(), pd.DataFrame(), "reason_code分析は未生成です。別artifact生成後に月次較正メモへ反映されます。"
    strong_positive = reasons[reasons["reliability_label"].astype(str) == "strong_positive"].head(10)
    strong_negative = (
        reasons[reasons["reliability_label"].astype(str) == "strong_negative"].sort_values("average_r").head(10)
        if "average_r" in reasons.columns
        else pd.DataFrame()
    )
    if strong_positive.empty and strong_negative.empty:
        memo = "現時点ではstrong_positive / strong_negativeのreason_codeはありません。weights.jsonは据え置きます。"
    else:
        memo = "reason_code単位の将来weights調整候補です。今回もweights.jsonは自動更新しません。"
    return strong_positive, strong_negative, memo


def build_monthly_calibration(start: pd.Timestamp, end: pd.Timestamp) -> tuple[pd.DataFrame, str]:
    input_data = load_input_data()
    preferred_evaluations, evaluation_meta = evaluation_loader.load_evaluations_prefer_latest()
    if not preferred_evaluations.empty or evaluation_meta.get("evaluation_source") != "none":
        input_data["evaluations"] = preferred_evaluations
    signals = filter_period(input_data["signals"], start, end)
    evaluations = filter_period(input_data["evaluations"], start, end)
    market_snapshot = filter_period(input_data["market_snapshot"], start, end)
    evaluations = enrich_evaluations(evaluations, signals)

    metrics = r_metrics(evaluations)
    pending_count = count_status(evaluations, "pending")
    skipped_count = count_status(evaluations, "skipped")
    asset_table = calibration_table(signals, evaluations, "asset", as_of=end)
    rank_table = calibration_table(signals, evaluations, "rank", ["A", "B", "NO_TRADE"], as_of=end)
    side_table = calibration_table(signals, evaluations, "side", ["LONG", "SHORT", "NONE"], as_of=end)
    regime_table = calibration_table(signals, evaluations, "regime", ["UPTREND", "DOWNTREND", "RANGE", "UNKNOWN"], as_of=end)
    best_asset, worst_asset = best_worst(asset_table, "asset")
    best_rank, worst_rank = best_worst(rank_table, "rank")
    best_side, worst_side = best_worst(side_table, "side")
    mode, risk, mode_notes = next_month_decision(metrics)
    summary = weight_change_summary(asset_table, rank_table, side_table)
    changes = rule_changes(metrics, mode_notes, summary)
    reason_analysis = load_reason_code_analysis()
    strong_positive_reasons, strong_negative_reasons, reason_memo = monthly_reason_code_memo(reason_analysis)

    row = {
        "month_start": start.strftime("%Y-%m-%d"),
        "month_end": end.strftime("%Y-%m-%d"),
        "total_signals": len(signals),
        "closed_signals": metrics["closed_count"],
        "pending_signals": pending_count,
        "skipped_signals": skipped_count,
        "win_rate": round(metrics["win_rate"], 4),
        "profit_factor": "inf" if math.isinf(metrics["profit_factor"]) else round(metrics["profit_factor"], 4),
        "total_r": round(metrics["total_r"], 4),
        "average_r": round(metrics["average_r"], 4),
        "max_win_r": round(metrics["max_win_r"], 4),
        "max_loss_r": round(metrics["max_loss_r"], 4),
        "best_asset": best_asset,
        "worst_asset": worst_asset,
        "best_rank": best_rank,
        "worst_rank": worst_rank,
        "best_side": best_side,
        "worst_side": worst_side,
        "next_month_mode": mode,
        "max_daily_risk_pct": risk,
        "weight_change_summary": summary,
        "rule_change_1": changes[0],
        "rule_change_2": changes[1],
        "rule_change_3": changes[2],
        "evaluation_source": evaluation_meta["evaluation_source"],
        "latest_evaluations_available": evaluation_meta["latest_evaluations_available"],
        "fallback_used": evaluation_meta["fallback_used"],
    }
    log = pd.DataFrame([row], columns=LOG_COLUMNS)

    proposed_weight_changes = {
        "asset": asset_table[["asset", "proposed_weight_change", "reason"]].to_dict(orient="records") if not asset_table.empty else [],
        "rank": rank_table[["rank", "proposed_weight_change", "reason"]].to_dict(orient="records") if not rank_table.empty else [],
        "side": side_table[["side", "proposed_weight_change", "reason"]].to_dict(orient="records") if not side_table.empty else [],
    }
    payload = {
        **row,
        "asset_calibration": asset_table.to_dict(orient="records"),
        "rank_calibration": rank_table.to_dict(orient="records"),
        "side_calibration": side_table.to_dict(orient="records"),
        "regime_calibration": regime_table.to_dict(orient="records"),
        "decay_half_life_days": stat_guards.DECAY_HALF_LIFE_DAYS,
        "proposed_weight_changes": proposed_weight_changes,
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"{end.strftime('%Y-%m-%d')}_monthly_calibration.md"
    data_warning = (
        f"closed評価が{stat_guards.MIN_SAMPLES_WEIGHT_CHANGE}件未満、"
        f"または統計的有意性(p < {stat_guards.SIGNIFICANCE_ALPHA})が確認できない区分には、重み変更を提案しません。"
        "weights.jsonの自動適用は引き続き行いません。(SPEC-SG-001)"
    )
    divergent = regime_table[regime_table["decay_divergence"] == True] if not regime_table.empty else pd.DataFrame()  # noqa: E712
    all_tables = pd.concat([t for t in [asset_table, rank_table, side_table] if not t.empty], ignore_index=True) if any(not t.empty for t in [asset_table, rank_table, side_table]) else pd.DataFrame()
    other_divergent_count = int((all_tables["decay_divergence"] == True).sum()) if not all_tables.empty and "decay_divergence" in all_tables.columns else 0  # noqa: E712
    if not divergent.empty or other_divergent_count > 0:
        divergence_note = (
            f"**警告: decay_divergence検出** (regime: {len(divergent)}件 / その他区分: {other_divergent_count}件)。"
            "全期間と直近で成績の符号が反転しています。レジームシフトの可能性があるため、該当区分の重み変更提案は一層慎重に扱ってください。"
        )
    else:
        divergence_note = "decay_divergenceは検出されていません。"
    conclusion = f"翌月モードは「{mode}」、最大日次リスクは {risk}% です。{(' / '.join(mode_notes) + '。') if mode_notes else ''}"
    report = render_monthly_report(
        conclusion=conclusion,
        log=log,
        evaluation_meta=evaluation_meta,
        asset_table=asset_table,
        rank_table=rank_table,
        side_table=side_table,
        regime_table=regime_table,
        divergence_note=divergence_note,
        mode=mode,
        risk=risk,
        summary=summary,
        data_warning=data_warning,
        reason_memo=reason_memo,
        strong_positive_reasons=strong_positive_reasons,
        strong_negative_reasons=strong_negative_reasons,
        payload=payload,
    )
    report_path.write_text(report, encoding="utf-8")
    log.to_csv(RESULTS_DIR / "monthly_calibration.csv", index=False)
    (RESULTS_DIR / "monthly_calibration.json").write_text(json.dumps([payload], ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"monthly calibration generated: {report_path}")
    print(f"market snapshot rows in period: {len(market_snapshot)}")
    print(f"weights reference: {WEIGHTS_PATH}")
    return log, str(report_path)


def main() -> int:
    args = parse_args()
    if args.start and args.end:
        start = pd.Timestamp(args.start)
        end = pd.Timestamp(args.end)
    else:
        start, end = default_period()
    if start > end:
        raise ValueError("--start must be before or equal to --end")
    build_monthly_calibration(start, end)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
