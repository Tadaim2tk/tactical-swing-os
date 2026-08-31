from __future__ import annotations

import argparse
import json
import math
import os
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

import evaluation_loader
from score_prediction_log import normalize_side


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/weekly")
PREDICTION_LEDGER_PATH = Path("data/signal_log.csv")
PREDICTION_SCORES_PATH = Path("data/prediction_log_scores.csv")
REVIEW_COLUMNS = [
    "week_start",
    "week_end",
    "total_signals",
    "a_signals",
    "b_signals",
    "no_trade_signals",
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
    "next_week_mode",
    "max_daily_risk_pct",
    "rule_change_1",
    "rule_change_2",
    "rule_change_3",
    "evaluation_source",
    "latest_evaluations_available",
    "fallback_used",
    "signal_source",
    "prediction_log_rows",
    "prediction_score_rows",
    "prediction_awaiting_rows",
]
DATE_COLUMNS = ["date", "signal_date", "evaluation_date", "hit_date", "run_ts"]
SHEET_MAPPINGS = {
    "market_snapshot": ("MARKET_SNAPSHOT", RESULTS_DIR / "market_snapshot.csv"),
    "signals": ("SIGNALS", RESULTS_DIR / "signals.csv"),
    "evaluations": ("EVALUATIONS", RESULTS_DIR / "evaluations.csv"),
}
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Tactical Swing OS weekly review.")
    parser.add_argument("--start", help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end", help="End date in YYYY-MM-DD format")
    return parser.parse_args()


def default_period() -> tuple[pd.Timestamp, pd.Timestamp]:
    end = pd.Timestamp(datetime.now().date())
    start = end - pd.Timedelta(days=6)
    return start, end


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def normalize_column_name(column: str) -> str:
    normalized = str(column).strip().lower()
    normalized = normalized.replace("-", "_")
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


def get_sheets_client():
    service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not service_account_json or not sheet_id:
        print("Google Sheets env not set; using local CSV fallback")
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


def load_from_sheets() -> dict[str, pd.DataFrame] | None:
    try:
        client = get_sheets_client()
        if client is None:
            return None
        spreadsheet = client.open_by_key(os.environ["GOOGLE_SHEET_ID"])
        data: dict[str, pd.DataFrame] = {}
        for key, (sheet_name, _) in SHEET_MAPPINGS.items():
            try:
                worksheet = spreadsheet.worksheet(sheet_name)
            except Exception as exc:  # noqa: BLE001 - missing sheets should not stop fallback.
                print(f"warning: Google Sheets worksheet {sheet_name} not found or unreadable: {exc}")
                data[key] = pd.DataFrame()
                continue
            df = worksheet_to_dataframe(worksheet)
            data[key] = df
            print(f"ok: loaded {len(df)} rows from Google Sheets {sheet_name}")
        return data
    except Exception as exc:  # noqa: BLE001 - fallback to local CSV is intentional.
        print(f"warning: Google Sheets read failed; falling back to local CSV: {exc}")
        return None


def load_from_local_csv() -> dict[str, pd.DataFrame]:
    data = {}
    for key, (_, path) in SHEET_MAPPINGS.items():
        df = normalize_headers(read_csv(path))
        data[key] = df
        print(f"ok: loaded {len(df)} rows from local CSV {path}")
    return data


def load_prediction_log_data() -> dict[str, pd.DataFrame]:
    return {
        "signal_log": normalize_headers(read_csv(PREDICTION_LEDGER_PATH)),
        "prediction_scores": normalize_headers(read_csv(PREDICTION_SCORES_PATH)),
    }


def load_input_data() -> dict[str, pd.DataFrame]:
    sheets_data = load_from_sheets()
    if sheets_data is not None:
        return sheets_data
    return load_from_local_csv()


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
    out["_review_date"] = pd.to_datetime(out[date_col], errors="coerce", utc=True).dt.tz_localize(None)
    start_ts = pd.Timestamp(start).tz_localize(None).normalize()
    end_ts = pd.Timestamp(end).tz_localize(None).normalize()
    review_date = out["_review_date"].dt.normalize()
    mask = (review_date >= start_ts) & (review_date <= end_ts)
    return out[mask].drop(columns=["_review_date"])


def enrich_evaluations(evaluations: pd.DataFrame, signals: pd.DataFrame) -> pd.DataFrame:
    if evaluations.empty or signals.empty or "signal_id" not in evaluations.columns or "signal_id" not in signals.columns:
        return evaluations.copy()
    cols = [col for col in ["signal_id", "asset", "side", "rank", "date"] if col in signals.columns]
    lookup = signals[cols].drop_duplicates(subset=["signal_id"], keep="last")
    out = evaluations.merge(lookup, on="signal_id", how="left", suffixes=("", "_signal"))
    for col in ["asset", "side", "rank"]:
        signal_col = f"{col}_signal"
        if signal_col in out.columns:
            if col in out.columns:
                out[col] = out[col].fillna(out[signal_col])
            else:
                out[col] = out[signal_col]
            out = out.drop(columns=[signal_col])
    if "date_signal" in out.columns and "date" not in out.columns:
        out["date"] = out["date_signal"]
    return out.drop(columns=[col for col in ["date_signal"] if col in out.columns])


def prediction_scores_to_evaluations(scores: pd.DataFrame) -> pd.DataFrame:
    """Map manual prediction-log scores into the weekly review evaluation shape."""
    if scores.empty:
        return pd.DataFrame()
    out = scores.copy()
    status = out.get("status", pd.Series([""] * len(out), index=out.index)).astype(str).str.lower()
    if "r_result" not in out.columns:
        if "r_close_5d" in out.columns:
            out["r_result"] = out["r_close_5d"]
        elif "r_close_10d" in out.columns:
            out["r_result"] = out["r_close_10d"]
        else:
            out["r_result"] = ""
    # closed = scored かつ 方向Rが数値で在る行のみ(#125 Codex P2: NO_TRADE等の非actionable行も
    # status=scored になるため、そのままclosedに写すと勝率の分母が空白Rの行で薄まり
    # next_week_mode の判定まで歪む)。非actionableのscored行は not_applicable として区別する。
    r_numeric = pd.to_numeric(out["r_result"], errors="coerce")
    out["evaluation_status"] = "pending"
    out.loc[(status == "scored") & r_numeric.notna(), "evaluation_status"] = "closed"
    out.loc[(status == "scored") & r_numeric.isna(), "evaluation_status"] = "not_applicable"
    out.loc[status.isin(["invalid_data", "invalid"]), "evaluation_status"] = "skipped"
    if "error_type" not in out.columns:
        out["error_type"] = status.mask(status == "", "未分類")
    return out


def select_weekly_inputs(
    signals: pd.DataFrame,
    evaluations: pd.DataFrame,
    prediction_signals: pd.DataFrame,
    prediction_scores: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Prefer the GPT prediction ledger for the weekly human-facing review.

    The live SIGNALS/EVALUATIONS path is still kept as a fallback. This avoids
    showing a false zero-signal week when the primary Phase-29 learning ledger
    has accumulated rows but the legacy results/SHEETS signal snapshot is stale.
    """
    if not prediction_signals.empty:
        # 台帳の side は BUY/SELL 表記。集計表は LONG/SHORT/NONE を要求するため、
        # 採点系と同じ正規化を通してから渡す(#125 Codex P2: 生のまま渡すと
        # actionable な判断が side 別集計で全て0件に化ける)。
        ledger_signals = prediction_signals.copy()
        if "side" in ledger_signals.columns:
            ledger_signals["side"] = ledger_signals["side"].map(normalize_side)
        return (
            ledger_signals,
            prediction_scores_to_evaluations(prediction_scores),
            {
                "signal_source": "prediction_log",
                "evaluation_source_override": "prediction_log_scores",
                "fallback_used_override": True,
            },
        )
    return (
        signals,
        evaluations,
        {
            "signal_source": "signals",
            "evaluation_source_override": "",
            "fallback_used_override": None,
        },
    )


def numeric_r(df: pd.DataFrame) -> pd.Series:
    if df.empty or "r_result" not in df.columns:
        return pd.Series(dtype=float)
    return pd.to_numeric(df["r_result"], errors="coerce").dropna()


def closed_df(evaluations: pd.DataFrame) -> pd.DataFrame:
    if evaluations.empty or "evaluation_status" not in evaluations.columns:
        return pd.DataFrame()
    return evaluations[evaluations["evaluation_status"].astype(str).str.lower() == "closed"].copy()


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


def group_stats(signals: pd.DataFrame, evaluations: pd.DataFrame, column: str, values: list[str] | None = None) -> pd.DataFrame:
    if values is None:
        observed = set(signals[column].dropna().astype(str)) if column in signals.columns and not signals.empty else set()
        observed |= set(evaluations[column].dropna().astype(str)) if column in evaluations.columns and not evaluations.empty else set()
        values = sorted(observed)

    rows = []
    for value in values:
        sig_part = signals[signals[column].astype(str) == value] if column in signals.columns and not signals.empty else pd.DataFrame()
        eval_part = evaluations[evaluations[column].astype(str) == value] if column in evaluations.columns and not evaluations.empty else pd.DataFrame()
        metrics = r_metrics(eval_part)
        rows.append(
            {
                column: value,
                "signals": len(sig_part),
                "closed": metrics["closed_count"],
                "win_rate": round(metrics["win_rate"], 4),
                "total_r": round(metrics["total_r"], 4),
                "average_r": round(metrics["average_r"], 4),
                "best_r": round(metrics["max_win_r"], 4),
                "worst_r": round(metrics["max_loss_r"], 4),
            }
        )
    return pd.DataFrame(rows)


def rank_stats(signals: pd.DataFrame, evaluations: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for rank in ["A", "B", "NO_TRADE"]:
        sig_part = signals[signals["rank"].astype(str) == rank] if "rank" in signals.columns and not signals.empty else pd.DataFrame()
        eval_part = evaluations[evaluations["rank"].astype(str) == rank] if "rank" in evaluations.columns and not evaluations.empty else pd.DataFrame()
        metrics = r_metrics(eval_part)
        rows.append(
            {
                "rank": rank,
                "signals": len(sig_part),
                "closed": metrics["closed_count"],
                "win_rate": round(metrics["win_rate"], 4),
                "total_r": round(metrics["total_r"], 4),
                "average_r": round(metrics["average_r"], 4),
            }
        )

    known = {"A", "B", "NO_TRADE"}
    sig_other = signals[~signals["rank"].astype(str).isin(known)] if "rank" in signals.columns and not signals.empty else pd.DataFrame()
    eval_other = evaluations[~evaluations["rank"].astype(str).isin(known)] if "rank" in evaluations.columns and not evaluations.empty else pd.DataFrame()
    metrics = r_metrics(eval_other)
    rows.append(
        {
            "rank": "その他",
            "signals": len(sig_other),
            "closed": metrics["closed_count"],
            "win_rate": round(metrics["win_rate"], 4),
            "total_r": round(metrics["total_r"], 4),
            "average_r": round(metrics["average_r"], 4),
        }
    )
    return pd.DataFrame(rows)


def error_stats(evaluations: pd.DataFrame) -> pd.DataFrame:
    if evaluations.empty or "error_type" not in evaluations.columns:
        return pd.DataFrame([{"error_type": "未分類", "count": len(evaluations)}])
    errors = evaluations["error_type"].fillna("").astype(str).str.strip()
    errors = errors.mask(errors == "", "未分類")
    return errors.value_counts().rename_axis("error_type").reset_index(name="count")


def missed_audit(signals: pd.DataFrame, evaluations: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    rows = []
    if not evaluations.empty and {"rank", "evaluation_status", "asset"}.issubset(evaluations.columns):
        watch = evaluations[
            evaluations["rank"].astype(str).isin(["A", "B"])
            & evaluations["evaluation_status"].astype(str).str.lower().isin(["pending", "skipped"])
        ]
        for asset, part in watch.groupby("asset"):
            rows.append({"missed_candidate": "pending_or_skipped_ab", "asset": asset, "count": len(part), "note": "A/B候補の未完了評価が多い可能性"})

    if "mfe" not in evaluations.columns:
        note = "MFE未実装のため暫定監査不可"
    else:
        mfe = pd.to_numeric(evaluations["mfe"], errors="coerce")
        large_mfe = evaluations[mfe >= 1.0] if not evaluations.empty else pd.DataFrame()
        for _, row in large_mfe.iterrows():
            rows.append(
                {
                    "missed_candidate": "large_mfe_review",
                    "asset": row.get("asset", ""),
                    "count": 1,
                    "note": f"MFE={row.get('mfe')} のためentry/約定条件を確認",
                }
            )
        note = "" if not large_mfe.empty else "MFE候補はありません"

    return pd.DataFrame(rows), note


def best_worst_asset(asset_table: pd.DataFrame) -> tuple[str, str]:
    if asset_table.empty or "total_r" not in asset_table.columns:
        return "", ""
    scored = asset_table.copy()
    if "closed" in scored.columns:
        closed = pd.to_numeric(scored["closed"], errors="coerce").fillna(0)
        scored = scored[closed > 0]
        if scored.empty:
            return "", ""
    scored["total_r"] = pd.to_numeric(scored["total_r"], errors="coerce")
    scored = scored.dropna(subset=["total_r"])
    if scored.empty:
        return "", ""
    best = str(scored.sort_values("total_r", ascending=False).iloc[0]["asset"])
    worst = str(scored.sort_values("total_r", ascending=True).iloc[0]["asset"])
    return best, worst


def next_week_decision(metrics: dict, closed_count: int) -> tuple[str, float, list[str]]:
    total_r = metrics["total_r"]
    win_rate = metrics["win_rate"]
    notes = []
    if total_r > 1.5 and win_rate >= 0.5:
        mode = "攻撃"
    elif total_r >= 0 and win_rate >= 0.4:
        mode = "通常"
    else:
        mode = "防御"

    if closed_count < 3:
        mode = "通常"
        notes.append("データ不足")

    risk = {"攻撃": 1.0, "通常": 0.5, "防御": 0.25}[mode]
    return mode, risk, notes


def rule_changes(
    metrics: dict,
    rank_table: pd.DataFrame,
    pending_count: int,
    mode_notes: list[str],
    pending_note: str = "",
) -> list[str]:
    changes = []
    if metrics["total_r"] > 0 and metrics["win_rate"] >= 0.45:
        changes.append("現行ルール維持")
    if metrics["total_r"] < 0:
        changes.append("Entry/SL/Rank判定の見直し")

    if not rank_table.empty:
        rank_map = {row["rank"]: row for _, row in rank_table.iterrows()}
        if "A" in rank_map and "B" in rank_map and float(rank_map["A"]["average_r"]) < float(rank_map["B"]["average_r"]):
            changes.append("A級判定条件を再検証")

    if pending_count >= 3:
        changes.append(pending_note or "評価期間またはentry条件の見直し")
    changes.extend(mode_notes)
    while len(changes) < 3:
        changes.append("")
    return changes[:3]


def markdown_table(df: pd.DataFrame, empty: str = "_該当なし_") -> str:
    if df.empty:
        return empty
    view = df.fillna("").astype(str)
    headers = list(view.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in view.iterrows():
        lines.append("| " + " | ".join(str(row[col]).replace("|", "\\|") for col in headers) + " |")
    return "\n".join(lines)


def json_records(df: pd.DataFrame) -> str:
    if df.empty:
        return "[]"
    return df.to_json(orient="records", indent=2, force_ascii=False)


def load_reason_code_analysis() -> tuple[pd.DataFrame, pd.DataFrame]:
    reason_path = RESULTS_DIR / "reason_code_analysis.csv"
    json_path = RESULTS_DIR / "reason_code_analysis.json"
    reasons = normalize_headers(read_csv(reason_path))
    no_trade = pd.DataFrame()
    if json_path.exists():
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            no_trade = pd.DataFrame(payload.get("no_trade_reason_summary", []))
        except (json.JSONDecodeError, OSError):
            no_trade = pd.DataFrame()
    return reasons, normalize_headers(no_trade)


def reason_code_weekly_summary(reasons: pd.DataFrame, no_trade: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, str]:
    if reasons.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), "reason code analysisは別artifact参照。現時点では分析結果が未生成です。"
    positive = reasons[reasons["reliability_label"].isin(["strong_positive", "positive"])].head(3) if "reliability_label" in reasons.columns else pd.DataFrame()
    negative = (
        reasons[reasons["reliability_label"].isin(["strong_negative", "negative"])].sort_values("average_r").head(3)
        if {"reliability_label", "average_r"}.issubset(reasons.columns)
        else pd.DataFrame()
    )
    missed = (
        no_trade[no_trade["missed_opportunity_count"].astype(str) != "0"].head(3)
        if not no_trade.empty and "missed_opportunity_count" in no_trade.columns
        else pd.DataFrame()
    )
    note = "reason code analysisは別artifact参照。詳細は reports/reason_codes/*.md を確認してください。"
    return positive, negative, missed, note


def build_review(start: pd.Timestamp, end: pd.Timestamp) -> tuple[pd.DataFrame, str]:
    input_data = load_input_data()
    preferred_evaluations, evaluation_meta = evaluation_loader.load_evaluations_prefer_latest()
    if not preferred_evaluations.empty or evaluation_meta.get("evaluation_source") != "none":
        input_data["evaluations"] = preferred_evaluations
    signals = filter_period(input_data["signals"], start, end)
    evaluations = filter_period(input_data["evaluations"], start, end)
    market_snapshot = filter_period(input_data["market_snapshot"], start, end)

    prediction_data = load_prediction_log_data()
    prediction_signals = filter_period(prediction_data["signal_log"], start, end)
    prediction_scores = filter_period(prediction_data["prediction_scores"], start, end)
    signals, evaluations, weekly_source_meta = select_weekly_inputs(
        signals,
        evaluations,
        prediction_signals,
        prediction_scores,
    )
    if weekly_source_meta["evaluation_source_override"]:
        evaluation_meta = {
            **evaluation_meta,
            "evaluation_source": weekly_source_meta["evaluation_source_override"],
            "latest_evaluations_available": False,
            "fallback_used": bool(weekly_source_meta["fallback_used_override"]),
        }

    evaluations = enrich_evaluations(evaluations, signals)

    metrics = r_metrics(evaluations)
    closed_count = metrics["closed_count"]
    pending_count = count_status(evaluations, "pending")
    skipped_count = count_status(evaluations, "skipped")
    prediction_awaiting_rows = (
        int((prediction_scores["status"].astype(str) == "awaiting_horizon").sum())
        if "status" in prediction_scores.columns and not prediction_scores.empty
        else 0
    )

    rank_table = rank_stats(signals, evaluations)
    asset_table = group_stats(signals, evaluations, "asset") if (not signals.empty or not evaluations.empty) else pd.DataFrame()
    side_table = group_stats(signals, evaluations, "side", ["LONG", "SHORT", "NONE"])
    error_table = error_stats(evaluations)
    missed_table, missed_note = missed_audit(signals, evaluations)
    best_asset, worst_asset = best_worst_asset(asset_table)
    mode, max_daily_risk_pct, mode_notes = next_week_decision(metrics, closed_count)
    pending_note = ""
    if weekly_source_meta["signal_source"] == "prediction_log" and pending_count and pending_count == prediction_awaiting_rows:
        pending_note = "予測ログは評価期間中（awaiting_horizon）"
    changes = rule_changes(metrics, rank_table, pending_count, mode_notes, pending_note)
    reason_analysis, no_trade_analysis = load_reason_code_analysis()
    reason_positive, reason_negative, reason_missed, reason_note = reason_code_weekly_summary(reason_analysis, no_trade_analysis)

    review_row = {
        "week_start": start.strftime("%Y-%m-%d"),
        "week_end": end.strftime("%Y-%m-%d"),
        "total_signals": len(signals),
        "a_signals": int((signals["rank"].astype(str) == "A").sum()) if "rank" in signals.columns and not signals.empty else 0,
        "b_signals": int((signals["rank"].astype(str) == "B").sum()) if "rank" in signals.columns and not signals.empty else 0,
        "no_trade_signals": int((signals["rank"].astype(str) == "NO_TRADE").sum()) if "rank" in signals.columns and not signals.empty else 0,
        "closed_signals": closed_count,
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
        "next_week_mode": mode,
        "max_daily_risk_pct": max_daily_risk_pct,
        "rule_change_1": changes[0],
        "rule_change_2": changes[1],
        "rule_change_3": changes[2],
        "evaluation_source": evaluation_meta["evaluation_source"],
        "latest_evaluations_available": evaluation_meta["latest_evaluations_available"],
        "fallback_used": evaluation_meta["fallback_used"],
        "signal_source": weekly_source_meta["signal_source"],
        "prediction_log_rows": len(prediction_signals),
        "prediction_score_rows": len(prediction_scores),
        "prediction_awaiting_rows": prediction_awaiting_rows,
    }
    review = pd.DataFrame([review_row], columns=REVIEW_COLUMNS)

    conclusion = []
    conclusion.append(f"次週モードは「{mode}」、最大日次リスクは {max_daily_risk_pct}% です。")
    if mode_notes:
        conclusion.append(" / ".join(mode_notes))
    if metrics["total_r"] > 0:
        conclusion.append("週次R損益はプラスです。")
    elif metrics["total_r"] < 0:
        conclusion.append("週次R損益はマイナスです。")
    else:
        conclusion.append("週次R損益は横ばいです。")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"{end.strftime('%Y-%m-%d')}_weekly_review.md"

    report = f"""# Tactical Swing OS Weekly Review

## 1. 週次結論

{' '.join(conclusion)}

## 2. 週次サマリー

{markdown_table(review)}

評価データソース: {evaluation_meta["evaluation_source"]} / latest_evaluations_available: {evaluation_meta["latest_evaluations_available"]} / fallback_used: {evaluation_meta["fallback_used"]}

シグナル集計ソース: {weekly_source_meta["signal_source"]} / prediction_log_rows: {len(prediction_signals)} / prediction_score_rows: {len(prediction_scores)}

## 3. Rank別成績

{markdown_table(rank_table)}

## 4. 資産別成績

{markdown_table(asset_table)}

## 5. Side別成績

{markdown_table(side_table)}

## 6. エラー分類

{markdown_table(error_table)}

## 7. 取り逃し監査

{(missed_note + chr(10) + chr(10)) if missed_note else ""}{markdown_table(missed_table)}

## 8. モデル更新メモ

- {changes[0] or '特記事項なし'}
- {changes[1] or '特記事項なし'}
- {changes[2] or '特記事項なし'}

## 9. Reason Code分析メモ

{reason_note}

### reason_code 上位プラス3件

{markdown_table(reason_positive)}

### reason_code 上位マイナス3件

{markdown_table(reason_negative)}

### no_trade_reason 取り逃し候補

{markdown_table(reason_missed)}

## 10. REVIEW_LOG CSV

```csv
{review.to_csv(index=False).strip()}
```

## 11. REVIEW_LOG JSON

```json
{json_records(review)}
```
"""
    report_path.write_text(report, encoding="utf-8")
    review.to_csv(RESULTS_DIR / "weekly_review.csv", index=False)
    review.to_json(RESULTS_DIR / "weekly_review.json", orient="records", indent=2, force_ascii=False)
    print(f"weekly review generated: {report_path}")
    print(f"market snapshot rows in period: {len(market_snapshot)}")
    return review, str(report_path)


def main() -> int:
    args = parse_args()
    if args.start and args.end:
        start = pd.Timestamp(args.start)
        end = pd.Timestamp(args.end)
    else:
        start, end = default_period()
    if start > end:
        raise ValueError("--start must be before or equal to --end")
    build_review(start, end)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
