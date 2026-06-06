"""build_report.py – Daily Markdown report generator.

Phase 6 additions:
  - setup_quality_score, direction_confidence, reason_codes,
    no_trade_reason, recommended_action per asset
  - A / B / NO_TRADE count summary
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def markdown_table(df: pd.DataFrame, columns: list[str] | None = None, empty: str = "_該当なし_") -> str:
    if df.empty:
        return empty
    view = df.copy()
    if columns:
        view = view[[col for col in columns if col in view.columns]]
    if view.empty:
        return empty

    formatted = view.fillna("").astype(str)
    headers = list(formatted.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in formatted.iterrows():
        values = [str(row[col]).replace("|", "\\|") for col in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def summarize_conclusion(signals: pd.DataFrame) -> str:
    if signals.empty:
        return "シグナルは生成されていません。データ取得状況を確認してください。"
    a_count = int((signals.get("rank") == "A").sum()) if "rank" in signals else 0
    b_count = int((signals.get("rank") == "B").sum()) if "rank" in signals else 0
    no_count = int((signals.get("rank") == "NO_TRADE").sum()) if "rank" in signals else 0
    if a_count:
        return f"A級候補が {a_count} 件あります。実売買は行わず、仮想評価対象として保存します。"
    if b_count:
        return f"A級候補はありません。B級監視候補 {b_count} 件を監視対象として保存します。"
    return f"本日は見送り優勢です。No Trade は {no_count} 件です。"


def rank_summary_table(signals: pd.DataFrame) -> str:
    """Return a small markdown table with A/B/NO_TRADE counts and totals."""
    if signals.empty or "rank" not in signals.columns:
        return "_シグナルなし_"
    a_cnt = int((signals["rank"] == "A").sum())
    b_cnt = int((signals["rank"] == "B").sum())
    nt_cnt = int((signals["rank"] == "NO_TRADE").sum())
    total = len(signals)
    rows = [
        ("A", a_cnt, "TRADE"),
        ("B", b_cnt, "WATCH"),
        ("NO_TRADE", nt_cnt, "NO_TRADE"),
    ]
    lines = [
        "| rank | count | recommended_action |",
        "| --- | --- | --- |",
    ]
    for rank, cnt, action in rows:
        lines.append(f"| {rank} | {cnt} | {action} |")
    lines.append(f"| **合計** | **{total}** | |")
    return "\n".join(lines)


def phase6_signal_table(df: pd.DataFrame) -> str:
    """Per-asset Phase-6 scoring table."""
    cols = [
        "asset", "side", "rank",
        "setup_quality_score", "direction_confidence",
        "reason_codes", "no_trade_reason", "recommended_action",
    ]
    return markdown_table(df, cols)


def csv_block(df: pd.DataFrame) -> str:
    if df.empty:
        return ""
    return df.to_csv(index=False).strip()


def json_block(df: pd.DataFrame) -> str:
    if df.empty:
        return "[]"
    return df.to_json(orient="records", indent=2, force_ascii=False)


def evaluation_summary(evaluations: pd.DataFrame) -> pd.DataFrame:
    labels = [
        "win_tp2",
        "win_tp1",
        "loss_sl",
        "no_entry",
        "missed_opportunity",
        "no_trade_correct",
        "no_trade_missed",
    ]
    if evaluations.empty:
        return pd.DataFrame({"metric": labels, "count": [0] * len(labels)})

    outcome = evaluations["outcome"].astype(str) if "outcome" in evaluations else pd.Series([], dtype=str)
    rows = []
    for label in labels:
        if label == "missed_opportunity":
            if "missed_opportunity" in evaluations:
                count = int(evaluations["missed_opportunity"].astype(str).str.lower().isin(["true", "1", "yes"]).sum())
            else:
                count = 0
        else:
            count = int((outcome == label).sum()) if not outcome.empty else 0
        rows.append({"metric": label, "count": count})
    return pd.DataFrame(rows)


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    snapshot = read_csv(RESULTS_DIR / "market_snapshot.csv")
    signals = read_csv(RESULTS_DIR / "signals.csv")
    evaluations = read_csv(RESULTS_DIR / "evaluations.csv")

    today = datetime.now().strftime("%Y-%m-%d")
    report_path = REPORTS_DIR / f"{today}.md"

    a_candidates = signals[signals["rank"] == "A"] if "rank" in signals else pd.DataFrame()
    b_candidates = signals[signals["rank"] == "B"] if "rank" in signals else pd.DataFrame()
    no_trade = signals[signals["rank"] == "NO_TRADE"] if "rank" in signals else pd.DataFrame()

    signal_cols = [
        "date", "asset", "side", "rank", "type",
        "entry_low", "entry_high", "sl", "tp1", "tp2",
        "tq_score", "expected_r",
    ]
    snapshot_cols = ["asset", "ticker", "status", "date", "close", "rows", "message"]
    evaluation_cols = ["signal_id", "asset", "side", "status", "outcome", "error_type", "r_multiple", "mfe_r", "mae_r", "missed_opportunity", "bars_checked"]
    summary = evaluation_summary(evaluations)

    report = f"""# Tactical Swing OS Daily Report - {today}

## 本日の結論

{summarize_conclusion(signals)}

## Rank別サマリー（Phase 6）

{rank_summary_table(signals)}

## Phase 6 スコア・理由コード一覧

{phase6_signal_table(signals)}

## 市場データ取得状況

{markdown_table(snapshot, snapshot_cols)}

## A級候補

{markdown_table(a_candidates, signal_cols)}

## B級監視候補

{markdown_table(b_candidates, signal_cols)}

## No Trade

{markdown_table(no_trade, ["date", "asset", "side", "rank", "regime", "no_trade_score", "no_trade_reason", "verification_target"])}

## 仮想評価

### 評価要約

{markdown_table(summary)}

### 評価明細

{markdown_table(evaluations, evaluation_cols)}

## TSO_LOG CSVブロック

```csv
{csv_block(signals)}
```

## TSO_LOG JSONブロック

```json
{json_block(signals)}
```
"""

    report_path.write_text(report, encoding="utf-8")
    print(f"report generated: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
