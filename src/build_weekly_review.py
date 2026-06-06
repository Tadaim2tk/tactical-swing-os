from __future__ import annotations

import argparse
import math
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/weekly")
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
]
DATE_COLUMNS = ["date", "signal_date", "evaluation_date", "hit_date", "run_ts"]


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
    mask = (out["_review_date"].dt.date >= start.date()) & (out["_review_date"].dt.date <= end.date())
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


def rule_changes(metrics: dict, rank_table: pd.DataFrame, pending_count: int, mode_notes: list[str]) -> list[str]:
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
        changes.append("評価期間またはentry条件の見直し")
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


def build_review(start: pd.Timestamp, end: pd.Timestamp) -> tuple[pd.DataFrame, str]:
    signals = filter_period(read_csv(RESULTS_DIR / "signals.csv"), start, end)
    evaluations = filter_period(read_csv(RESULTS_DIR / "evaluations.csv"), start, end)
    market_snapshot = filter_period(read_csv(RESULTS_DIR / "market_snapshot.csv"), start, end)
    evaluations = enrich_evaluations(evaluations, signals)

    metrics = r_metrics(evaluations)
    closed_count = metrics["closed_count"]
    pending_count = count_status(evaluations, "pending")
    skipped_count = count_status(evaluations, "skipped")

    rank_table = rank_stats(signals, evaluations)
    asset_table = group_stats(signals, evaluations, "asset") if (not signals.empty or not evaluations.empty) else pd.DataFrame()
    side_table = group_stats(signals, evaluations, "side", ["LONG", "SHORT", "NONE"])
    error_table = error_stats(evaluations)
    missed_table, missed_note = missed_audit(signals, evaluations)
    best_asset, worst_asset = best_worst_asset(asset_table)
    mode, max_daily_risk_pct, mode_notes = next_week_decision(metrics, closed_count)
    changes = rule_changes(metrics, rank_table, pending_count, mode_notes)

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

## 9. REVIEW_LOG CSV

```csv
{review.to_csv(index=False).strip()}
```

## 10. REVIEW_LOG JSON

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
