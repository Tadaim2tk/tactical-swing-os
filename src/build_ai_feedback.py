from __future__ import annotations

import html
import json
import os
from datetime import date, datetime
from pathlib import Path

import pandas as pd

import score_narratives as narratives


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/ai_feedback")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_MAPPINGS = {
    "market_snapshot": ("MARKET_SNAPSHOT", RESULTS_DIR / "market_snapshot.csv"),
    "signals": ("SIGNALS", RESULTS_DIR / "signals.csv"),
    "evaluations": ("EVALUATIONS", RESULTS_DIR / "evaluations.csv"),
}
LOCAL_EXTRA_FILES = {
    "reason_code_analysis": RESULTS_DIR / "reason_code_analysis.csv",
    "rule_update_proposals": RESULTS_DIR / "rule_update_proposals.csv",
    "weekly_review": RESULTS_DIR / "weekly_review.csv",
    "monthly_calibration": RESULTS_DIR / "monthly_calibration.csv",
    "dashboard_summary": RESULTS_DIR / "dashboard_summary.json",
    "rule_update_proposals_json": RESULTS_DIR / "rule_update_proposals.json",
}
AI_FEEDBACK_COLUMNS = [
    "generated_at",
    "date",
    "asset",
    "signal_id",
    "side",
    "rank",
    "recommended_action",
    "reason_codes",
    "narrative_alignment",
    "narrative_alignment_score",
    "risk_on_score",
    "risk_off_score",
    "dollar_strength_score",
    "rate_pressure_score",
    "gold_safe_haven_score",
    "crypto_liquidity_score",
    "volatility_stress_score",
    "narrative_confidence",
    "latest_outcome",
    "latest_r_multiple",
    "feedback_type",
    "feedback_summary",
    "proposed_next_action",
    "apply_automatically",
]
SAFETY_NOTES = [
    "実売買には使わない",
    "自動発注しない",
    "weights.jsonを自動更新しない",
    "generate_signal.pyを自動変更しない",
    "ナラティブ評価は仮説であり、人間レビューが必要",
    "ニュース本文/LLM評価は今後の拡張",
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


def read_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def sanitize_for_json(value):
    if isinstance(value, dict):
        return {str(k): sanitize_for_json(v) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize_for_json(v) for v in value]
    if isinstance(value, tuple):
        return [sanitize_for_json(v) for v in value]
    if isinstance(value, pd.DataFrame):
        return sanitize_for_json(value.to_dict(orient="records"))
    if isinstance(value, pd.Series):
        return sanitize_for_json(value.to_dict())
    if isinstance(value, (pd.Timestamp, datetime, date)):
        if pd.isna(value):
            return None
        return value.isoformat()
    if not isinstance(value, (str, bytes)):
        try:
            if pd.isna(value):
                return None
        except (TypeError, ValueError):
            pass
    if hasattr(value, "item"):
        try:
            return sanitize_for_json(value.item())
        except (TypeError, ValueError):
            pass
    return value


def safe_json_dumps(obj) -> str:
    return json.dumps(sanitize_for_json(obj), ensure_ascii=False, indent=2, default=str)


def get_sheets_client():
    service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not service_account_json or not sheet_id:
        print("Google Sheets env not set; using local fallback")
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


def load_from_sheets() -> tuple[dict[str, pd.DataFrame] | None, str]:
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
            except Exception as exc:  # noqa: BLE001 - missing sheet should not stop fallback output.
                print(f"warning: Google Sheets worksheet {sheet_name} unavailable: {exc}")
                data[key] = pd.DataFrame()
        return data, "Google Sheets"
    except Exception as exc:  # noqa: BLE001 - local fallback is intentional.
        print(f"warning: Google Sheets read failed; using local fallback: {exc}")
        return None, "local fallback"


def load_input_data() -> tuple[dict[str, pd.DataFrame], dict[str, object], str]:
    sheets, source = load_from_sheets()
    data = sheets if sheets is not None else {
        key: read_csv(path) for key, (_, path) in SHEET_MAPPINGS.items()
    }
    extras: dict[str, object] = {}
    for key, path in LOCAL_EXTRA_FILES.items():
        extras[key] = read_json(path) if path.suffix == ".json" else read_csv(path)
    return data, extras, source


def latest_date(signals: pd.DataFrame, evaluations: pd.DataFrame) -> str:
    candidates = []
    for df, columns in [(signals, ["date", "signal_date"]), (evaluations, ["evaluation_date", "signal_date"])]:
        for col in columns:
            if not df.empty and col in df.columns:
                parsed = pd.to_datetime(df[col], errors="coerce", utc=True).dt.tz_localize(None)
                candidates.extend(parsed.dropna().tolist())
    if not candidates:
        return datetime.now().strftime("%Y-%m-%d")
    return max(candidates).strftime("%Y-%m-%d")


def latest_signals(signals: pd.DataFrame) -> pd.DataFrame:
    if signals.empty:
        return signals.copy()
    date_col = "date" if "date" in signals.columns else "signal_date" if "signal_date" in signals.columns else ""
    if not date_col:
        return signals.copy()
    out = signals.copy()
    out["_signal_date"] = pd.to_datetime(out[date_col], errors="coerce", utc=True).dt.tz_localize(None)
    if out["_signal_date"].dropna().empty:
        return out.drop(columns=["_signal_date"])
    latest = out["_signal_date"].max()
    return out[out["_signal_date"] == latest].drop(columns=["_signal_date"])


def latest_evaluation_lookup(evaluations: pd.DataFrame) -> pd.DataFrame:
    if evaluations.empty or "signal_id" not in evaluations.columns:
        return pd.DataFrame(columns=["signal_id", "latest_outcome", "latest_r_multiple"])
    out = evaluations.copy()
    sort_col = "evaluation_date" if "evaluation_date" in out.columns else "signal_date" if "signal_date" in out.columns else ""
    if sort_col:
        out["_eval_date"] = pd.to_datetime(out[sort_col], errors="coerce", utc=True).dt.tz_localize(None)
        out = out.sort_values("_eval_date")
    out = out.drop_duplicates(subset=["signal_id"], keep="last")
    r_col = "r_multiple" if "r_multiple" in out.columns else "r_result" if "r_result" in out.columns else ""
    result = pd.DataFrame(
        {
            "signal_id": out["signal_id"],
            "latest_outcome": out.get("outcome", pd.Series(index=out.index, dtype=str)),
            "latest_r_multiple": pd.to_numeric(out[r_col], errors="coerce") if r_col else pd.Series(index=out.index, dtype=float),
        }
    )
    return result


def build_feedback_rows(
    generated_at: str,
    report_date: str,
    signals: pd.DataFrame,
    evaluations: pd.DataFrame,
    narrative_scores: pd.DataFrame,
    alignment: pd.DataFrame,
) -> pd.DataFrame:
    latest_eval = latest_evaluation_lookup(evaluations)
    score = narrative_scores.iloc[0].to_dict() if not narrative_scores.empty else {}
    rows = alignment.copy()
    if rows.empty:
        rows = pd.DataFrame(
            [
                {
                    "asset": "GLOBAL",
                    "signal_id": "",
                    "side": "",
                    "rank": "",
                    "recommended_action": "",
                    "reason_codes": "",
                    "narrative_alignment": "insufficient_data",
                    "narrative_alignment_score": 0,
                    "narrative_comment": "シグナルデータがありません。",
                }
            ]
        )
    if not latest_eval.empty and "signal_id" in rows.columns:
        rows = rows.merge(latest_eval, on="signal_id", how="left")
    else:
        rows["latest_outcome"] = ""
        rows["latest_r_multiple"] = ""

    rows["generated_at"] = generated_at
    rows["date"] = report_date
    for col in [
        "risk_on_score",
        "risk_off_score",
        "dollar_strength_score",
        "rate_pressure_score",
        "gold_safe_haven_score",
        "crypto_liquidity_score",
        "volatility_stress_score",
        "narrative_confidence",
    ]:
        rows[col] = score.get(col, 0)
    rows["feedback_type"] = rows["narrative_alignment"].map(
        {
            "aligned": "context_support",
            "conflicted": "context_warning",
            "neutral": "context_neutral",
            "insufficient_data": "data_insufficient",
        }
    ).fillna("context_neutral")
    rows["feedback_summary"] = rows.get("narrative_comment", "")
    rows["proposed_next_action"] = rows.apply(proposed_action_for_row, axis=1)
    rows["apply_automatically"] = False
    for col in AI_FEEDBACK_COLUMNS:
        if col not in rows.columns:
            rows[col] = ""
    return rows[AI_FEEDBACK_COLUMNS]


def proposed_action_for_row(row) -> str:
    alignment = str(row.get("narrative_alignment", ""))
    asset = str(row.get("asset", ""))
    side = str(row.get("side", ""))
    if alignment == "aligned":
        return f"{asset} {side} は市場文脈と整合。既存ルールを維持し、過剰強化はしない。"
    if alignment == "conflicted":
        return f"{asset} {side} は市場文脈と衝突。明日はrank/entry条件を慎重化する仮説。"
    if alignment == "insufficient_data":
        return "データ不足。判定を急がず、追加データ取得後に再評価。"
    return f"{asset} {side} は中立。テクニカル優先だが、文脈変化を監視。"


def recent_evaluation_reflection(evaluations: pd.DataFrame, alignment: pd.DataFrame) -> list[dict]:
    if evaluations.empty:
        return [{"type": "data_missing", "summary": "評価データがないため、前回判断の反省は保留です。"}]
    df = evaluations.copy()
    date_col = "evaluation_date" if "evaluation_date" in df.columns else "signal_date" if "signal_date" in df.columns else ""
    if date_col:
        df["_date"] = pd.to_datetime(df[date_col], errors="coerce", utc=True).dt.tz_localize(None)
        df = df.sort_values("_date", ascending=False)
    interesting = {"win_tp1", "win_tp2", "loss_sl", "no_entry", "no_trade_missed"}
    if "outcome" in df.columns:
        df = df[df["outcome"].astype(str).isin(interesting) | df.get("missed_opportunity", pd.Series(False, index=df.index)).astype(str).str.lower().isin(["true", "1", "yes"])]
    rows = []
    align_lookup = alignment.set_index("signal_id").to_dict(orient="index") if not alignment.empty and "signal_id" in alignment.columns else {}
    for _, row in df.head(8).iterrows():
        signal_id = row.get("signal_id", "")
        outcome = row.get("outcome", "")
        aligned = align_lookup.get(signal_id, {}).get("narrative_alignment", "unknown")
        r_value = row.get("r_multiple", row.get("r_result", ""))
        rows.append(
            {
                "signal_id": signal_id,
                "asset": row.get("asset", ""),
                "outcome": outcome,
                "r_multiple": r_value,
                "technical_view": technical_reflection(outcome),
                "narrative_alignment": aligned,
                "improvement": improvement_reflection(outcome, aligned),
            }
        )
    return rows or [{"type": "no_recent_closed", "summary": "直近で反省対象となる決着データはありません。"}]


def technical_reflection(outcome: str) -> str:
    outcome = str(outcome)
    if outcome in {"win_tp1", "win_tp2"}:
        return "エントリー/方向判断は一定程度機能しました。"
    if outcome == "loss_sl":
        return "損切り到達。Entry/SL幅またはrank判定の再確認が必要です。"
    if outcome == "no_entry":
        return "未約定。entry帯が保守的すぎた可能性があります。"
    if outcome == "no_trade_missed":
        return "見送り後に動意が出たため、見送り条件の過剰さを点検します。"
    return "評価継続中または分類外です。"


def improvement_reflection(outcome: str, alignment: str) -> str:
    if outcome in {"win_tp1", "win_tp2"} and alignment == "aligned":
        return "文脈整合時の成功例として、類似条件を監視します。"
    if outcome == "loss_sl" and alignment == "conflicted":
        return "文脈逆風をrank低下に反映する仮説を検討します。"
    if outcome == "no_entry":
        return "MFEが大きい場合はentry帯の柔軟化候補です。"
    if outcome == "no_trade_missed":
        return "低ボラ見送りでもbreakout兆候があれば監視強化します。"
    return "追加サンプルで検証します。"


def improvement_hypotheses(scores: pd.DataFrame, alignment: pd.DataFrame, evaluations: pd.DataFrame) -> list[str]:
    score = scores.iloc[0].to_dict() if not scores.empty else {}
    hypotheses = []
    if score.get("rate_pressure_score", 50) >= 58 and score.get("dollar_strength_score", 50) >= 58:
        hypotheses.append("GOLDのLONGは、US10Y上昇とドル高が同時に強い局面ではsetup_quality_scoreを弱める候補。")
    if score.get("crypto_liquidity_score", 50) >= 58 and score.get("risk_on_score", 50) >= 55:
        hypotheses.append("BTCのLONGは、NASDAQ上昇とDXY低下が重なる局面で監視優先度を強める候補。")
    if score.get("volatility_stress_score", 50) >= 58:
        hypotheses.append("VIX上昇中の株価指数LONGは慎重化し、entry条件を厳格化する候補。")
    if not alignment.empty and (alignment["narrative_alignment"] == "conflicted").any():
        hypotheses.append("ナラティブ衝突シグナルは、翌日のrankまたはrisk_pctを下げる仮説として監視。")
    if not evaluations.empty and "outcome" in evaluations.columns and (evaluations["outcome"].astype(str) == "no_trade_missed").any():
        hypotheses.append("no_trade_reasonがlow_volatilityでも、breakout直前なら見送り過剰に注意。")
    return hypotheses[:6] or ["データ不足のため、明日の補正仮説は現行ルール維持を基本とします。"]


def rule_proposal_crosscheck(rule_updates: pd.DataFrame, alignment: pd.DataFrame) -> list[dict]:
    if rule_updates.empty:
        return [{"summary": "rule_update_proposals がないため照合は未実施です。"}]
    proposals = rule_updates.copy()
    if "priority" in proposals.columns:
        proposals["_priority"] = pd.to_numeric(proposals["priority"], errors="coerce").fillna(999)
        proposals = proposals.sort_values("_priority")
    conflicts = set(alignment.loc[alignment.get("narrative_alignment", pd.Series(dtype=str)) == "conflicted", "asset"].astype(str)) if not alignment.empty and "asset" in alignment.columns else set()
    rows = []
    for _, row in proposals.head(5).iterrows():
        target = str(row.get("target_name", ""))
        rows.append(
            {
                "proposal_id": row.get("proposal_id", ""),
                "target_name": target,
                "proposal_strength": row.get("proposal_strength", ""),
                "proposed_change": row.get("proposed_change", ""),
                "narrative_crosscheck": "ナラティブ衝突資産と一致" if target in conflicts else "直接衝突なし",
                "apply_automatically": False,
            }
        )
    return rows


def markdown_table(rows, columns: list[str]) -> str:
    df = pd.DataFrame(rows)
    if df.empty:
        return "データなし"
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    df = df[columns]
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for _, row in df.iterrows():
        body.append("| " + " | ".join(html.escape("" if pd.isna(row[col]) else str(row[col])) for col in columns) + " |")
    return "\n".join([header, sep, *body])


def build_report(
    generated_at: str,
    report_date: str,
    data_source: str,
    scores: pd.DataFrame,
    alignment: pd.DataFrame,
    feedback_rows: pd.DataFrame,
    reflections: list[dict],
    hypotheses: list[str],
    crosscheck: list[dict],
) -> str:
    score_row = scores.iloc[0].to_dict() if not scores.empty else {}
    counts = narratives.alignment_counts(alignment)
    score_cols = [
        "asset",
        "risk_on_score",
        "risk_off_score",
        "dollar_strength_score",
        "rate_pressure_score",
        "gold_safe_haven_score",
        "crypto_liquidity_score",
        "volatility_stress_score",
        "narrative_confidence",
    ]
    align_cols = [
        "signal_id",
        "asset",
        "side",
        "rank",
        "recommended_action",
        "reason_codes",
        "narrative_alignment",
        "narrative_alignment_score",
        "narrative_comment",
    ]
    csv_block = feedback_rows.to_csv(index=False)
    payload = {
        "generated_at": generated_at,
        "date": report_date,
        "data_source": data_source,
        "market_mode_summary": narratives.market_mode_summary(scores),
        "narrative_scores": scores.to_dict(orient="records"),
        "signal_alignment": alignment.to_dict(orient="records"),
        "recent_evaluation_reflection": reflections,
        "improvement_hypotheses": hypotheses,
        "rule_proposal_crosscheck": crosscheck,
        "safety_notes": SAFETY_NOTES,
    }
    try:
        json_block = safe_json_dumps(payload)
    except Exception as exc:  # noqa: BLE001 - markdown should not fail the workflow.
        print(f"warning: ai feedback markdown json serialization fallback used: {exc}")
        json_block = safe_json_dumps(
            {
                "generated_at": generated_at,
                "date": report_date,
                "data_source": data_source,
                "market_mode_summary": narratives.market_mode_summary(scores),
                "serialization_warning": "full payload omitted from markdown because it contained non-JSON values",
                "safety_notes": SAFETY_NOTES,
            }
        )

    return f"""# Tactical Swing OS AI Feedback Report

生成日時: {generated_at}
対象日: {report_date}
データソース: {data_source}

## 1. 今日の総合判断

- 今日の市場モード: {narratives.market_mode_summary(scores)}
- risk_on: {score_row.get("risk_on_score", "データなし")}
- risk_off: {score_row.get("risk_off_score", "データなし")}
- dollar: {score_row.get("dollar_strength_score", "データなし")}
- rate: {score_row.get("rate_pressure_score", "データなし")}
- volatility: {score_row.get("volatility_stress_score", "データなし")}
- シグナル整合性: aligned={counts["aligned"]}, conflicted={counts["conflicted"]}, neutral={counts["neutral"]}, insufficient_data={counts["insufficient_data"]}

## 2. 資産別ナラティブスコア

{markdown_table(scores.to_dict(orient="records"), score_cols)}

## 3. シグナル別ナラティブ整合性

{markdown_table(alignment.to_dict(orient="records"), align_cols)}

## 4. 前回評価からの反省

{markdown_table(reflections, ["signal_id", "asset", "outcome", "r_multiple", "technical_view", "narrative_alignment", "improvement"])}

## 5. 明日に向けた補正仮説

{chr(10).join(f"- {item}" for item in hypotheses)}

## 6. rule_update_proposalsとの照合

{markdown_table(crosscheck, ["proposal_id", "target_name", "proposal_strength", "proposed_change", "narrative_crosscheck", "apply_automatically"])}

## 7. 今日の注意点

- データ不足の可能性があります。
- 評価件数不足の場合、結論は仮説扱いです。
- LLM未使用のためニュース本文は未評価です。
- 実売買には使いません。
- 自動発注、weights.json自動更新、generate_signal.py自動変更は行いません。

## 8. AI_FEEDBACK_LOG CSV

```csv
{csv_block}
```

## 9. AI_FEEDBACK_LOG JSON

```json
{json_block}
```
"""


def write_outputs(
    generated_at: str,
    report_date: str,
    data_source: str,
    scores: pd.DataFrame,
    alignment: pd.DataFrame,
    feedback_rows: pd.DataFrame,
    reflections: list[dict],
    hypotheses: list[str],
    crosscheck: list[dict],
) -> dict:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = sanitize_for_json({
        "generated_at": generated_at,
        "date": report_date,
        "data_source": data_source,
        "market_mode_summary": narratives.market_mode_summary(scores),
        "narrative_scores": scores.to_dict(orient="records"),
        "signal_alignment": alignment.to_dict(orient="records"),
        "recent_evaluation_reflection": reflections,
        "improvement_hypotheses": hypotheses,
        "rule_proposal_crosscheck": crosscheck,
        "safety_notes": SAFETY_NOTES,
    })
    (RESULTS_DIR / "ai_feedback.csv").write_text(feedback_rows.to_csv(index=False), encoding="utf-8")
    (RESULTS_DIR / "ai_feedback.json").write_text(safe_json_dumps(payload), encoding="utf-8")
    try:
        report = build_report(generated_at, report_date, data_source, scores, alignment, feedback_rows, reflections, hypotheses, crosscheck)
    except Exception as exc:  # noqa: BLE001 - preserve artifacts even if markdown rendering regresses.
        print(f"warning: ai feedback markdown fallback used: {exc}")
        report = fallback_report(generated_at, report_date, data_source, payload, exc)
    report_path = REPORTS_DIR / f"{report_date}_ai_feedback.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"ai feedback report generated: {report_path}")
    print("ai feedback csv generated: results/ai_feedback.csv")
    print("ai feedback json generated: results/ai_feedback.json")
    return payload


def fallback_report(generated_at: str, report_date: str, data_source: str, payload: dict, exc: Exception) -> str:
    return f"""# Tactical Swing OS AI Feedback Report

生成日時: {generated_at}
対象日: {report_date}
データソース: {data_source}

warning: ai feedback markdown fallback used: {html.escape(str(exc))}

## 今日の総合判断

{html.escape(str(payload.get("market_mode_summary", "データなし")))}

## AI_FEEDBACK_LOG JSON

```json
{safe_json_dumps(payload)}
```
"""


def build_ai_feedback() -> dict:
    generated_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    data, extras, source = load_input_data()
    market_snapshot = data.get("market_snapshot", pd.DataFrame())
    signals = latest_signals(data.get("signals", pd.DataFrame()))
    evaluations = data.get("evaluations", pd.DataFrame())
    report_date = latest_date(signals, evaluations)
    scores = narratives.score_market_narratives(market_snapshot)
    alignment = narratives.evaluate_signal_alignment(signals, scores)
    feedback_rows = build_feedback_rows(generated_at, report_date, signals, evaluations, scores, alignment)
    reflections = recent_evaluation_reflection(evaluations, alignment)
    hypotheses = improvement_hypotheses(scores, alignment, evaluations)
    rule_updates = extras.get("rule_update_proposals", pd.DataFrame())
    crosscheck = rule_proposal_crosscheck(rule_updates if isinstance(rule_updates, pd.DataFrame) else pd.DataFrame(), alignment)
    return write_outputs(generated_at, report_date, source, scores, alignment, feedback_rows, reflections, hypotheses, crosscheck)


def main() -> int:
    build_ai_feedback()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
