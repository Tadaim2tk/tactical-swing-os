from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path

import pandas as pd

import analyze_reason_codes as arc


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/rule_updates")
PROPOSAL_COLUMNS = [
    "generated_at",
    "period_start",
    "period_end",
    "proposal_id",
    "proposal_type",
    "target_type",
    "target_name",
    "proposal_strength",
    "evidence_count",
    "win_rate",
    "average_r",
    "total_r",
    "missed_opportunity_count",
    "current_behavior",
    "proposed_change",
    "expected_effect",
    "risk_note",
    "apply_automatically",
    "priority",
    "notes",
]
SAFETY_NOTES = [
    "実売買には使わない",
    "自動反映しない",
    "closed評価が30〜50件以上溜まるまでは提案のみ",
    "人間レビュー後に必要なら実装",
]


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return arc.normalize_headers(pd.read_csv(path))
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def generated_at() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")


def default_period() -> tuple[pd.Timestamp, pd.Timestamp]:
    end = pd.Timestamp(datetime.now().date())
    return end - pd.Timedelta(days=29), end


def numeric(df: pd.DataFrame, column: str) -> pd.Series:
    if df.empty or column not in df.columns:
        return pd.Series(dtype=float)
    return pd.to_numeric(df[column], errors="coerce").dropna()


def bool_series(df: pd.DataFrame, column: str) -> pd.Series:
    if df.empty or column not in df.columns:
        return pd.Series([False] * len(df), index=df.index)
    return df[column].fillna("").astype(str).str.lower().isin(["true", "1", "yes"])


def scalar_float(value, default: float = 0.0) -> float:
    value = pd.to_numeric(value, errors="coerce")
    if pd.isna(value):
        return default
    return float(value)


def scalar_int(value, default: int = 0) -> int:
    value = pd.to_numeric(value, errors="coerce")
    if pd.isna(value):
        return default
    return int(value)


def status_evaluated(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    r = pd.to_numeric(df.get("r_multiple", pd.Series(index=df.index, dtype=float)), errors="coerce")
    outcome = df.get("outcome", pd.Series(index=df.index, dtype=str)).fillna("").astype(str)
    return df[r.notna() | outcome.ne("")]


def r_metrics(df: pd.DataFrame) -> dict:
    evaluated = status_evaluated(df)
    r = numeric(evaluated, "r_multiple")
    outcome = evaluated.get("outcome", pd.Series(index=evaluated.index, dtype=str)).fillna("").astype(str)
    wins = int(outcome.isin(["win_tp1", "win_tp2"]).sum())
    count = len(evaluated)
    return {
        "evaluated_count": count,
        "win_rate": wins / count if count else 0.0,
        "average_r": float(r.mean()) if not r.empty else 0.0,
        "total_r": float(r.sum()) if not r.empty else 0.0,
        "missed_opportunity_count": int(bool_series(evaluated, "missed_opportunity").sum()),
    }


def proposal_strength(evaluated_count: int, average_r: float) -> str:
    if evaluated_count < 5:
        return "DATA_INSUFFICIENT"
    if abs(average_r) >= 0.5 and evaluated_count >= 10:
        return "HIGH"
    if abs(average_r) >= 0.2 and evaluated_count >= 5:
        return "MEDIUM"
    return "LOW"


def priority_from_strength(strength: str) -> int:
    return {"HIGH": 1, "MEDIUM": 2, "LOW": 3, "DATA_INSUFFICIENT": 4}.get(strength, 4)


def make_proposal(
    rows: list[dict],
    *,
    generated: str,
    start: pd.Timestamp,
    end: pd.Timestamp,
    proposal_type: str,
    target_type: str,
    target_name: str,
    evidence_count: int,
    win_rate: float,
    average_r: float,
    total_r: float,
    missed_opportunity_count: int,
    current_behavior: str,
    proposed_change: str,
    expected_effect: str,
    risk_note: str,
    notes: str,
    strength: str | None = None,
) -> None:
    strength = strength or proposal_strength(evidence_count, average_r)
    proposal_id = f"{end.strftime('%Y%m%d')}_{target_type}_{target_name}_{proposal_type}".replace(" ", "_").replace("|", "_")
    rows.append(
        {
            "generated_at": generated,
            "period_start": start.strftime("%Y-%m-%d"),
            "period_end": end.strftime("%Y-%m-%d"),
            "proposal_id": proposal_id,
            "proposal_type": proposal_type,
            "target_type": target_type,
            "target_name": target_name,
            "proposal_strength": strength,
            "evidence_count": int(evidence_count),
            "win_rate": round(float(win_rate), 4),
            "average_r": round(float(average_r), 4),
            "total_r": round(float(total_r), 4),
            "missed_opportunity_count": int(missed_opportunity_count),
            "current_behavior": current_behavior,
            "proposed_change": proposed_change,
            "expected_effect": expected_effect,
            "risk_note": risk_note,
            "apply_automatically": False,
            "priority": priority_from_strength(strength),
            "notes": notes,
        }
    )


def load_reason_table(signals: pd.DataFrame, evaluations: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    local = read_csv(RESULTS_DIR / "reason_code_analysis.csv")
    if not local.empty:
        return local
    merged = arc.combine_signals_evaluations(arc.filter_period(signals, start, end), arc.filter_period(evaluations, start, end))
    return arc.reason_summary(arc.explode_reason_codes(merged))


def load_no_trade_table(signals: pd.DataFrame, evaluations: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    json_path = RESULTS_DIR / "reason_code_analysis.json"
    if json_path.exists():
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            table = pd.DataFrame(payload.get("no_trade_reason_summary", []))
            if not table.empty:
                return arc.normalize_headers(table)
        except (OSError, json.JSONDecodeError):
            pass
    merged = arc.combine_signals_evaluations(arc.filter_period(signals, start, end), arc.filter_period(evaluations, start, end))
    return arc.no_trade_summary(merged)


def load_inputs(start: pd.Timestamp, end: pd.Timestamp) -> dict[str, pd.DataFrame]:
    data = arc.load_input_data()
    signals = data.get("signals", pd.DataFrame())
    evaluations = data.get("evaluations", pd.DataFrame())
    reason_table = load_reason_table(signals, evaluations, start, end)
    no_trade_table = load_no_trade_table(signals, evaluations, start, end)
    weekly = read_csv(RESULTS_DIR / "weekly_review.csv")
    monthly = read_csv(RESULTS_DIR / "monthly_calibration.csv")
    return {
        "signals": arc.filter_period(signals, start, end),
        "evaluations": arc.filter_period(evaluations, start, end),
        "reason_table": reason_table,
        "no_trade_table": no_trade_table,
        "weekly": weekly,
        "monthly": monthly,
    }


def reason_code_proposals(rows: list[dict], reason_table: pd.DataFrame, generated: str, start: pd.Timestamp, end: pd.Timestamp) -> None:
    if reason_table.empty:
        make_proposal(
            rows,
            generated=generated,
            start=start,
            end=end,
            proposal_type="data_insufficient",
            target_type="reason_code",
            target_name="reason_codes",
            evidence_count=0,
            win_rate=0,
            average_r=0,
            total_r=0,
            missed_opportunity_count=0,
            current_behavior="reason_code_analysisが未生成または空",
            proposed_change="Phase 6以降のSIGNALS/EVALUATIONSを蓄積して再分析",
            expected_effect="十分な根拠が集まるまで判断を保留",
            risk_note="少数サンプルでは誤判定しやすい",
            notes="reason_code単位の提案なし",
            strength="DATA_INSUFFICIENT",
        )
        return

    for _, row in reason_table.iterrows():
        code = str(row.get("reason_code", ""))
        evaluated = scalar_int(row.get("evaluated_count", 0))
        win_rate = scalar_float(row.get("win_rate", 0))
        average_r = scalar_float(row.get("average_r", 0))
        total_r = scalar_float(row.get("total_r", 0))
        missed = scalar_int(row.get("missed_opportunity_count", 0))
        label = str(row.get("reliability_label", ""))
        if evaluated < 5:
            make_proposal(
                rows,
                generated=generated,
                start=start,
                end=end,
                proposal_type="data_insufficient",
                target_type="reason_code",
                target_name=code,
                evidence_count=evaluated,
                win_rate=win_rate,
                average_r=average_r,
                total_r=total_r,
                missed_opportunity_count=missed,
                current_behavior=f"{code} は評価件数不足",
                proposed_change="自動変更せず監視継続",
                expected_effect="誤ったルール変更を避ける",
                risk_note="評価件数5件未満",
                notes=label,
                strength="DATA_INSUFFICIENT",
            )
        elif average_r > 0.2 and win_rate >= 0.45:
            make_proposal(
                rows,
                generated=generated,
                start=start,
                end=end,
                proposal_type="strengthen_reason_code",
                target_type="reason_code",
                target_name=code,
                evidence_count=evaluated,
                win_rate=win_rate,
                average_r=average_r,
                total_r=total_r,
                missed_opportunity_count=missed,
                current_behavior=f"{code} は良好な期待値",
                proposed_change="setup_quality_scoreに +2〜+5 の補正を検討",
                expected_effect="有効なセットアップのrank向上",
                risk_note="過学習を避けるため人間レビュー必須",
                notes=label,
            )
        elif average_r < -0.2:
            make_proposal(
                rows,
                generated=generated,
                start=start,
                end=end,
                proposal_type="weaken_reason_code",
                target_type="reason_code",
                target_name=code,
                evidence_count=evaluated,
                win_rate=win_rate,
                average_r=average_r,
                total_r=total_r,
                missed_opportunity_count=missed,
                current_behavior=f"{code} は負の期待値",
                proposed_change="risk_penalty_scoreを +3〜+8、またはrankを一段階下げる条件を検討",
                expected_effect="低期待値シグナルの抑制",
                risk_note="相場環境依存の可能性あり",
                notes=label,
            )
        else:
            make_proposal(
                rows,
                generated=generated,
                start=start,
                end=end,
                proposal_type="monitor_reason_code",
                target_type="reason_code",
                target_name=code,
                evidence_count=evaluated,
                win_rate=win_rate,
                average_r=average_r,
                total_r=total_r,
                missed_opportunity_count=missed,
                current_behavior=f"{code} は中立",
                proposed_change="変更せず監視継続",
                expected_effect="安定性を確認",
                risk_note="明確な改善根拠なし",
                notes=label,
            )


def no_trade_proposals(rows: list[dict], table: pd.DataFrame, generated: str, start: pd.Timestamp, end: pd.Timestamp) -> None:
    if table.empty:
        return
    for _, row in table.iterrows():
        reason = str(row.get("no_trade_reason", ""))
        count = scalar_int(row.get("count", 0))
        correct = scalar_int(row.get("no_trade_correct_count", 0))
        missed_count = scalar_int(row.get("no_trade_missed_count", 0))
        missed = scalar_int(row.get("missed_opportunity_count", 0))
        average_mfe = scalar_float(row.get("average_mfe_r", 0))
        average_r = scalar_float(row.get("average_r", 0))
        if count < 3:
            ptype = "data_insufficient"
            change = "見送り理由の件数が少ないため監視継続"
            effect = "誤ったフィルター調整を避ける"
            strength = "DATA_INSUFFICIENT"
        elif missed >= 2 and average_mfe > 1.0:
            ptype = "relax_no_trade_filter"
            change = "この見送り理由は取り逃しが多く、NO_TRADE条件を緩和する候補"
            effect = "機会損失の低減"
            strength = None
        elif correct > missed_count:
            ptype = "strengthen_no_trade_filter"
            change = "有効な見送り条件として維持または軽く強化を検討"
            effect = "低品質シグナルの抑制"
            strength = None
        else:
            ptype = "data_insufficient"
            change = "追加データを待つ"
            effect = "判断保留"
            strength = "DATA_INSUFFICIENT"
        make_proposal(
            rows,
            generated=generated,
            start=start,
            end=end,
            proposal_type=ptype,
            target_type="no_trade_reason",
            target_name=reason,
            evidence_count=count,
            win_rate=correct / count if count else 0,
            average_r=average_r,
            total_r=average_r * count,
            missed_opportunity_count=missed,
            current_behavior=f"{reason}: correct={correct}, missed={missed_count}, avg_mfe_r={average_mfe:.2f}",
            proposed_change=change,
            expected_effect=effect,
            risk_note="NO_TRADE緩和はノイズ取引増加に注意",
            notes=str(row.get("assessment", "")),
            strength=strength,
        )


def group_proposals(rows: list[dict], merged: pd.DataFrame, group_col: str, generated: str, start: pd.Timestamp, end: pd.Timestamp) -> None:
    if merged.empty or group_col not in merged.columns:
        return
    target_map = {"asset": "asset", "side": "side", "rank": "rank"}
    for value, part in merged.groupby(group_col, dropna=False):
        value = str(value)
        metrics = r_metrics(part)
        evaluated = metrics["evaluated_count"]
        avg_r = metrics["average_r"]
        if group_col == "asset":
            positive_type, negative_type = "increase_asset_weight", "reduce_asset_weight"
        elif group_col == "side":
            positive_type, negative_type = "increase_side_bias", "reduce_side_bias"
        else:
            positive_type, negative_type = "review_rank_threshold", "review_rank_threshold"

        if evaluated < 5:
            ptype = "data_insufficient"
            change = "評価件数不足のため監視継続"
            effect = "過剰調整を避ける"
            strength = "DATA_INSUFFICIENT"
        elif avg_r > 0.2:
            ptype = positive_type
            change = f"{group_col}={value} の条件をやや優遇する候補"
            effect = "高期待値カテゴリの活用"
            strength = None
        elif avg_r < -0.2:
            ptype = negative_type
            change = f"{group_col}={value} の条件を抑制または閾値見直し"
            effect = "低期待値カテゴリの抑制"
            strength = None
        else:
            continue

        make_proposal(
            rows,
            generated=generated,
            start=start,
            end=end,
            proposal_type=ptype,
            target_type=target_map[group_col],
            target_name=value,
            evidence_count=evaluated,
            win_rate=metrics["win_rate"],
            average_r=avg_r,
            total_r=metrics["total_r"],
            missed_opportunity_count=metrics["missed_opportunity_count"],
            current_behavior=f"{group_col}={value} avg_r={avg_r:.4f}",
            proposed_change=change,
            expected_effect=effect,
            risk_note="カテゴリ単位の調整は相場環境依存に注意",
            notes="group performance review",
            strength=strength,
        )


def rank_threshold_proposals(rows: list[dict], merged: pd.DataFrame, generated: str, start: pd.Timestamp, end: pd.Timestamp) -> None:
    if merged.empty or "rank" not in merged.columns:
        return
    rank_metrics = {}
    for rank, part in merged.groupby("rank"):
        rank_metrics[str(rank)] = r_metrics(part)
    if "A" in rank_metrics and "B" in rank_metrics and rank_metrics["A"]["average_r"] < rank_metrics["B"]["average_r"]:
        make_proposal(
            rows,
            generated=generated,
            start=start,
            end=end,
            proposal_type="review_rank_threshold",
            target_type="rank",
            target_name="A_vs_B",
            evidence_count=rank_metrics["A"]["evaluated_count"] + rank_metrics["B"]["evaluated_count"],
            win_rate=rank_metrics["A"]["win_rate"],
            average_r=rank_metrics["A"]["average_r"] - rank_metrics["B"]["average_r"],
            total_r=rank_metrics["A"]["total_r"] + rank_metrics["B"]["total_r"],
            missed_opportunity_count=rank_metrics["A"]["missed_opportunity_count"] + rank_metrics["B"]["missed_opportunity_count"],
            current_behavior="Aランクのaverage_rがBランクより低い",
            proposed_change="A級判定条件を再検証",
            expected_effect="rank品質の改善",
            risk_note="件数不足時は結論を保留",
            notes="rank threshold review",
        )
    no_trade = merged[merged["rank"].astype(str) == "NO_TRADE"] if "rank" in merged.columns else pd.DataFrame()
    if not no_trade.empty and bool_series(no_trade, "missed_opportunity").sum() >= 2:
        metrics = r_metrics(no_trade)
        make_proposal(
            rows,
            generated=generated,
            start=start,
            end=end,
            proposal_type="review_rank_threshold",
            target_type="rank",
            target_name="NO_TRADE",
            evidence_count=len(no_trade),
            win_rate=metrics["win_rate"],
            average_r=metrics["average_r"],
            total_r=metrics["total_r"],
            missed_opportunity_count=metrics["missed_opportunity_count"],
            current_behavior="NO_TRADEのmissed_opportunityが多い",
            proposed_change="NO_TRADE閾値とwatch条件を再検証",
            expected_effect="取り逃しの低減",
            risk_note="緩和しすぎると低品質シグナルが増える",
            notes="no_trade threshold review",
        )


def build_proposals(start: pd.Timestamp, end: pd.Timestamp) -> tuple[pd.DataFrame, str]:
    generated = generated_at()
    inputs = load_inputs(start, end)
    signals = inputs["signals"]
    evaluations = inputs["evaluations"]
    merged = arc.combine_signals_evaluations(signals, evaluations)
    rows: list[dict] = []
    reason_code_proposals(rows, inputs["reason_table"], generated, start, end)
    no_trade_proposals(rows, inputs["no_trade_table"], generated, start, end)
    for group_col in ["asset", "side", "rank"]:
        group_proposals(rows, merged, group_col, generated, start, end)
    rank_threshold_proposals(rows, merged, generated, start, end)

    proposals = pd.DataFrame(rows, columns=PROPOSAL_COLUMNS)
    if not proposals.empty:
        proposals = proposals.sort_values(["priority", "proposal_type", "target_type", "target_name"])
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = RESULTS_DIR / "rule_update_proposals.csv"
    json_path = RESULTS_DIR / "rule_update_proposals.json"
    report_path = REPORTS_DIR / f"{end.strftime('%Y-%m-%d')}_rule_update_proposals.md"
    proposals.to_csv(csv_path, index=False)

    high_priority = proposals[proposals["proposal_strength"] == "HIGH"] if not proposals.empty else pd.DataFrame()
    insufficient = proposals[proposals["proposal_strength"] == "DATA_INSUFFICIENT"] if not proposals.empty else pd.DataFrame()
    summary = {
        "proposal_count": int(len(proposals)),
        "high_priority_count": int(len(high_priority)),
        "data_insufficient_count": int(len(insufficient)),
        "apply_automatically": False,
    }
    payload = {
        "generated_at": generated,
        "period_start": start.strftime("%Y-%m-%d"),
        "period_end": end.strftime("%Y-%m-%d"),
        "summary": summary,
        "proposals": proposals.to_dict(orient="records"),
        "high_priority_proposals": high_priority.to_dict(orient="records"),
        "data_insufficient_items": insufficient.to_dict(orient="records"),
        "safety_notes": SAFETY_NOTES,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    strengthen = proposals[proposals["proposal_type"] == "strengthen_reason_code"] if not proposals.empty else pd.DataFrame()
    weaken = proposals[proposals["proposal_type"] == "weaken_reason_code"] if not proposals.empty else pd.DataFrame()
    no_trade = proposals[proposals["target_type"] == "no_trade_reason"] if not proposals.empty else pd.DataFrame()
    group = proposals[proposals["target_type"].isin(["asset", "side", "rank"])] if not proposals.empty else pd.DataFrame()
    conclusion = "ルール改善候補を生成しました。自動反映は行いません。"
    if proposals.empty:
        conclusion = "改善候補は生成されませんでした。データ蓄積後に再確認してください。"
    report = f"""# Tactical Swing OS Rule Update Proposals

## 1. 結論

{conclusion}

対象期間: {start.strftime('%Y-%m-%d')} - {end.strftime('%Y-%m-%d')}

## 2. 高優先度の改善候補

{arc.markdown_table(high_priority)}

## 3. reason_codeを強める候補

{arc.markdown_table(strengthen)}

## 4. reason_codeを弱める候補

{arc.markdown_table(weaken)}

## 5. no_trade_reasonの見直し候補

{arc.markdown_table(no_trade)}

## 6. asset / side / rank の見直し候補

{arc.markdown_table(group)}

## 7. データ不足の項目

{arc.markdown_table(insufficient)}

## 8. 自動反映しない理由

- 実売買には使わない
- weights.jsonは自動更新しない
- generate_signal.pyは自動変更しない
- closed評価が30〜50件以上溜まるまでは提案のみ

## 9. 次に人間が確認すべき点

- HIGH / MEDIUM の提案が特定assetやsideに偏っていないか
- no_trade_reason緩和で低品質シグナルが増えないか
- reason_codeの成績が一時的な相場環境に依存していないか

## 10. RULE_UPDATE_PROPOSALS CSV

```csv
{proposals.to_csv(index=False).strip()}
```

## 11. RULE_UPDATE_PROPOSALS JSON

```json
{json.dumps(payload, ensure_ascii=False, indent=2)}
```
"""
    report_path.write_text(report, encoding="utf-8")
    print(f"rule update proposals generated: {report_path}")
    print(f"proposal rows: {len(proposals)}")
    return proposals, str(report_path)


def main() -> int:
    start, end = default_period()
    build_proposals(start, end)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
