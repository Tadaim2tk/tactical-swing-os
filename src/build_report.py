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


def csv_block(df: pd.DataFrame) -> str:
    if df.empty:
        return ""
    return df.to_csv(index=False).strip()


def json_block(df: pd.DataFrame) -> str:
    if df.empty:
        return "[]"
    return df.to_json(orient="records", indent=2, force_ascii=False)


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
    signal_cols = ["date", "asset", "side", "rank", "type", "entry_low", "entry_high", "sl", "tp1", "tp2", "tq_score", "expected_r"]
    snapshot_cols = ["asset", "ticker", "status", "date", "close", "rows", "message"]
    evaluation_cols = ["signal_id", "asset", "side", "evaluation_status", "hit_level", "r_result", "mfe", "mae", "bars_checked"]

    report = f"""# Tactical Swing OS Daily Report - {today}

## 本日の結論

{summarize_conclusion(signals)}

## 市場データ取得状況

{markdown_table(snapshot, snapshot_cols)}

## A級候補

{markdown_table(a_candidates, signal_cols)}

## B級監視候補

{markdown_table(b_candidates, signal_cols)}

## No Trade

{markdown_table(no_trade, ["date", "asset", "side", "rank", "regime", "no_trade_score", "verification_target"])}

## 仮想評価

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
