from __future__ import annotations

"""ナラティブ信頼性ゲート (SPEC-NQ-001)。

AIの文章分析(ニュースナラティブ分類)の出力を、クオンツ側と同一の
証拠基準(SPEC-SG-001: n>=30 + t検定 + Sharpe)で監査する。
ナラティブカテゴリ単位でR成績を集計し、統計的に信頼できるものだけを
strong_positive / strong_negative としてラベル付けする。

設計原則:
- 提案・分析のみ。weights.jsonは更新しない。人間承認必須。
- 入力スキーマに寛容(列名・ファイル名は候補リストで解決)。
- 入力が無い場合は unavailable summary を生成して正常終了する。
"""

import json
from pathlib import Path
from typing import Any

import pandas as pd

import stat_guards
from time_utils import format_jst, format_utc, now_utc


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/narrative")
# ナラティブ成果物の候補(存在する最初のものを使用)
NARRATIVE_FILE_CANDIDATES = [
    RESULTS_DIR / "narrative_scores.csv",
    RESULTS_DIR / "news_narratives.csv",
    RESULTS_DIR / "classified_narratives.csv",
    RESULTS_DIR / "narratives.csv",
]
SIGNALS_CSV = RESULTS_DIR / "signals.csv"
EVALUATIONS_CANDIDATES = [
    RESULTS_DIR / "latest_evaluations.csv",
    RESULTS_DIR / "evaluations.csv",
]
NARRATIVE_LABEL_CANDIDATES = ["narrative", "narrative_label", "narrative_category", "narrative_type", "category"]
ASSET_CANDIDATES = ["asset", "symbol", "ticker"]
DATE_CANDIDATES = ["date", "news_date", "classified_date", "run_date"]
SIGNAL_ID_CANDIDATES = ["signal_id"]
RELIABILITY_COLUMNS = [
    "generated_at_jst",
    "narrative",
    "linked_signals",
    "closed_count",
    "win_rate",
    "average_r",
    "total_r",
    "sharpe",
    "p_value",
    "significant",
    "decayed_avg_r",
    "effective_n",
    "decay_divergence",
    "reliability_label",
    "recommended_action",
    "evidence_note",
    "requires_human_approval",
    "weights_json_updated",
]


def normalize_column_name(column: str) -> str:
    normalized = str(column).strip().lower().replace("-", "_")
    normalized = "_".join(normalized.split())
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    return normalized


def normalize_headers(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()
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


def first_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for col in candidates:
        if col in df.columns:
            return col
    return None


def load_narratives() -> tuple[pd.DataFrame, str]:
    for path in NARRATIVE_FILE_CANDIDATES:
        df = read_csv(path)
        if not df.empty:
            return df, str(path)
    return pd.DataFrame(), "missing"


def load_evaluations() -> pd.DataFrame:
    for path in EVALUATIONS_CANDIDATES:
        df = read_csv(path)
        if not df.empty:
            return df
    return pd.DataFrame()


def closed_r_by_signal(evaluations: pd.DataFrame) -> pd.DataFrame:
    """signal_id -> (r_result, evaluation_date) のclosed評価テーブル。"""
    if evaluations.empty or "signal_id" not in evaluations.columns:
        return pd.DataFrame()
    if "evaluation_status" in evaluations.columns:
        closed = evaluations[evaluations["evaluation_status"].astype(str).str.lower() == "closed"].copy()
    else:
        closed = evaluations.copy()
    if closed.empty or "r_result" not in closed.columns:
        return pd.DataFrame()
    closed["r_result"] = pd.to_numeric(closed["r_result"], errors="coerce")
    closed = closed.dropna(subset=["r_result"])
    date_col = first_column(closed, ["evaluation_date", "hit_date", "date"])
    closed["_eval_date"] = pd.to_datetime(closed[date_col], errors="coerce", utc=True).dt.tz_localize(None) if date_col else pd.NaT
    return closed[["signal_id", "r_result", "_eval_date"]].drop_duplicates(subset=["signal_id"], keep="last")


def link_narratives_to_signals(narratives: pd.DataFrame, signals: pd.DataFrame) -> pd.DataFrame:
    """ナラティブ行をシグナルへ紐付ける。signal_id直結を優先し、無ければ(asset, date)で結合。"""
    narratives = normalize_headers(narratives)
    label_col = first_column(narratives, NARRATIVE_LABEL_CANDIDATES)
    if label_col is None:
        return pd.DataFrame()
    out = narratives.rename(columns={label_col: "narrative"}).copy()
    out["narrative"] = out["narrative"].fillna("").astype(str).str.strip()
    out = out[out["narrative"] != ""]
    sig_col = first_column(out, SIGNAL_ID_CANDIDATES)
    if sig_col:
        return out[["narrative", sig_col]].rename(columns={sig_col: "signal_id"}).drop_duplicates()
    # (asset, date) 結合
    if signals.empty or "signal_id" not in signals.columns:
        return pd.DataFrame()
    n_asset = first_column(out, ASSET_CANDIDATES)
    n_date = first_column(out, DATE_CANDIDATES)
    s_asset = first_column(signals, ASSET_CANDIDATES)
    s_date = first_column(signals, DATE_CANDIDATES)
    if not all([n_asset, n_date, s_asset, s_date]):
        return pd.DataFrame()
    left = out[["narrative", n_asset, n_date]].copy()
    left["_asset"] = left[n_asset].astype(str).str.upper().str.strip()
    left["_date"] = pd.to_datetime(left[n_date], errors="coerce", utc=True).dt.tz_localize(None).dt.normalize()
    right = signals[["signal_id", s_asset, s_date]].copy()
    right["_asset"] = right[s_asset].astype(str).str.upper().str.strip()
    right["_date"] = pd.to_datetime(right[s_date], errors="coerce", utc=True).dt.tz_localize(None).dt.normalize()
    merged = left.merge(right[["signal_id", "_asset", "_date"]], on=["_asset", "_date"], how="inner")
    return merged[["narrative", "signal_id"]].drop_duplicates()


def reliability_label(report: dict[str, Any], closed_count: int) -> tuple[str, str]:
    if closed_count < stat_guards.MIN_SAMPLES_WEIGHT_CHANGE:
        return "insufficient_data", "wait_for_more_data"
    if not report["significant"]:
        return "unproven", "continue_tracking"
    if report["mean"] > 0 and report["sharpe"] > stat_guards.MIN_SHARPE_FOR_INCREASE:
        return "strong_positive", "human_review_for_weight_candidate"
    if report["mean"] < 0:
        return "strong_negative", "human_review_for_suppression"
    return "unproven", "continue_tracking"


def build_reliability_rows(
    links: pd.DataFrame,
    closed: pd.DataFrame,
    generated_at_jst: str,
    as_of: pd.Timestamp | None = None,
) -> pd.DataFrame:
    if links.empty or closed.empty:
        return pd.DataFrame(columns=RELIABILITY_COLUMNS)
    joined = links.merge(closed, on="signal_id", how="inner")
    if joined.empty:
        return pd.DataFrame(columns=RELIABILITY_COLUMNS)
    as_of = as_of or pd.Timestamp.now().normalize()
    rows = []
    for narrative, group in joined.groupby("narrative"):
        r_values = group["r_result"].astype(float).tolist()
        report = stat_guards.significance_report(r_values)
        n = report["n"]
        wins = sum(1 for v in r_values if v > 0)
        ages = [
            max(0.0, float((as_of - d).days)) if pd.notna(d) else 0.0
            for d in group["_eval_date"]
        ]
        decayed = stat_guards.decayed_mean(r_values, ages)
        decay_divergence = bool(
            report["mean"] * decayed["decayed_mean"] < 0
            and abs(report["mean"]) > 0.05
            and abs(decayed["decayed_mean"]) > 0.05
        )
        label, action = reliability_label(report, n)
        rows.append(
            {
                "generated_at_jst": generated_at_jst,
                "narrative": str(narrative),
                "linked_signals": int(group["signal_id"].nunique()),
                "closed_count": n,
                "win_rate": round(wins / n, 4) if n else 0.0,
                "average_r": round(report["mean"], 4),
                "total_r": round(sum(r_values), 4),
                "sharpe": round(report["sharpe"], 4),
                "p_value": round(report["p_value"], 6),
                "significant": bool(report["significant"]),
                "decayed_avg_r": round(decayed["decayed_mean"], 4),
                "effective_n": round(decayed["effective_n"], 2),
                "decay_divergence": decay_divergence,
                "reliability_label": label,
                "recommended_action": action,
                "evidence_note": (
                    f"n={n}, win={wins / n:.2f}, avg_r={report['mean']:.3f}, "
                    f"sharpe={report['sharpe']:.3f}, p={report['p_value']:.4f}"
                    if n
                    else "no closed evaluations"
                ),
                "requires_human_approval": True,
                "weights_json_updated": False,
            }
        )
    out = pd.DataFrame(rows, columns=RELIABILITY_COLUMNS)
    return out.sort_values(["reliability_label", "total_r"], ascending=[True, False]).reset_index(drop=True)


def summary_from(table: pd.DataFrame, source: str, generated_at_jst: str, generated_at_utc: str) -> dict[str, Any]:
    label = table.get("reliability_label", pd.Series(dtype=str)) if not table.empty else pd.Series(dtype=str)
    return {
        "generated_at_jst": generated_at_jst,
        "generated_at_utc": generated_at_utc,
        "narrative_reliability_status": "unavailable" if table.empty else "active",
        "narrative_source": source,
        "total_narratives": int(len(table)),
        "strong_positive_count": int((label == "strong_positive").sum()) if not table.empty else 0,
        "strong_negative_count": int((label == "strong_negative").sum()) if not table.empty else 0,
        "unproven_count": int((label == "unproven").sum()) if not table.empty else 0,
        "insufficient_data_count": int((label == "insufficient_data").sum()) if not table.empty else 0,
        "decay_divergence_count": int(table["decay_divergence"].sum()) if not table.empty else 0,
        "gate_spec": "SPEC-SG-001 (n>=30, p<0.05, Sharpe>0.5 for positive)",
        "requires_human_approval": True,
        "weights_json_updated": False,
        "apply_automatically": False,
    }


def markdown_table(df: pd.DataFrame, empty: str = "該当なし") -> str:
    if df.empty:
        return empty
    cols = [str(col) for col in df.columns]
    lines = [
        "| " + " | ".join(cols) + " |",
        "| " + " | ".join(["---"] * len(cols)) + " |",
    ]
    for _, row in df.iterrows():
        values = [str(row.get(col, "")).replace("\n", " ").replace("|", "/") for col in df.columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def render_markdown(summary: dict[str, Any], table: pd.DataFrame) -> str:
    cols = ["narrative", "closed_count", "win_rate", "average_r", "sharpe", "p_value", "decayed_avg_r", "decay_divergence", "reliability_label", "recommended_action"]
    strong_pos = table[table["reliability_label"] == "strong_positive"] if not table.empty else pd.DataFrame()
    strong_neg = table[table["reliability_label"] == "strong_negative"] if not table.empty else pd.DataFrame()
    rest = table[~table["reliability_label"].isin(["strong_positive", "strong_negative"])] if not table.empty else pd.DataFrame()
    return f"""# Narrative Reliability (SPEC-NQ-001)

## 1. 概要

- 生成日時JST: {summary["generated_at_jst"]}
- narrative_reliability_status: {summary["narrative_reliability_status"]}
- narrative_source: {summary["narrative_source"]}
- total_narratives: {summary["total_narratives"]}
- strong_positive: {summary["strong_positive_count"]} / strong_negative: {summary["strong_negative_count"]}
- unproven: {summary["unproven_count"]} / insufficient_data: {summary["insufficient_data_count"]}
- decay_divergence: {summary["decay_divergence_count"]}
- 適用ゲート: {summary["gate_spec"]}
- weights_json_updated: false / requires_human_approval: true

## 2. strong_positive (統計的に信頼できる追い風ナラティブ)

{markdown_table(strong_pos[cols] if not strong_pos.empty else strong_pos)}

## 3. strong_negative (統計的に信頼できる逆風ナラティブ)

{markdown_table(strong_neg[cols] if not strong_neg.empty else strong_neg)}

## 4. 未証明・データ不足

{markdown_table(rest[cols] if not rest.empty else rest)}

## 5. 注意

- AIの文章分析(ナラティブ分類)はここで初めて統計的監査を受けます
- strong_positive/negativeは「人間レビュー用の候補」であり、weights.jsonは更新しません
- n>=30未満のナラティブは判断保留(insufficient_data)です
- 実売買・発注は行いません
"""


def build_narrative_reliability() -> tuple[pd.DataFrame, dict[str, Any], str]:
    generated_dt_utc = now_utc()
    generated_at_jst = format_jst(generated_dt_utc)
    generated_at_utc = format_utc(generated_dt_utc)
    narratives, source = load_narratives()
    signals = read_csv(SIGNALS_CSV)
    evaluations = load_evaluations()
    links = link_narratives_to_signals(narratives, signals) if not narratives.empty else pd.DataFrame()
    closed = closed_r_by_signal(evaluations)
    table = build_reliability_rows(links, closed, generated_at_jst)
    summary = summary_from(table, source, generated_at_jst, generated_at_utc)
    payload = {
        **summary,
        "safety": {
            "weights_json_updated": False,
            "patch_applied": False,
            "requires_human_approval": True,
            "apply_automatically": False,
        },
        "narrative_reliability": table.to_dict(orient="records"),
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_date = generated_at_jst[:10]
    csv_path = RESULTS_DIR / "narrative_reliability.csv"
    json_path = RESULTS_DIR / "narrative_reliability.json"
    report_path = REPORTS_DIR / f"{report_date}_narrative_reliability.md"
    table.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    report_path.write_text(render_markdown(summary, table), encoding="utf-8")
    print(f"narrative reliability generated: {report_path}")
    print(f"narrative reliability rows: {len(table)}")
    return table, summary, str(report_path)


def main() -> int:
    build_narrative_reliability()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
