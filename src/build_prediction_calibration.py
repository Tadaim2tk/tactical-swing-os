from __future__ import annotations

"""予測キャリブレーション層 (SPEC-BC-001)。

Rank A/B が暗黙に主張する勝率(implied probability)と実際の的中率を比較し、
AIの「自信」そのものをBrierスコアで採点する。ハルシネーション傾向の確率レベル監査。

設計原則:
- 提案・分析のみ。weights.jsonは更新しない。人間承認必須。
- implied probability は config/rank_implied_probability.json で人間が管理(無ければ凍結デフォルト)。
- n >= 30 (SPEC-SG-001) までキャリブレーション判定は保留。
"""

import json
import math
from pathlib import Path
from typing import Any

import pandas as pd

import stat_guards
from calibration_io import read_csv
from time_utils import format_jst, format_utc, now_utc


RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/calibration")
CONFIG_PATH = Path("config/rank_implied_probability.json")
SIGNALS_CSV = RESULTS_DIR / "signals.csv"
EVALUATIONS_CANDIDATES = [
    RESULTS_DIR / "latest_evaluations.csv",
    RESULTS_DIR / "evaluations.csv",
]
# 凍結デフォルト (SPEC-BC-001): Rank別の暗黙的勝率主張。configで人間が更新可能。
DEFAULT_IMPLIED_PROBABILITY = {"A": 0.55, "B": 0.45}
CALIBRATION_COLUMNS = [
    "generated_at_jst",
    "rank",
    "implied_probability",
    "closed_count",
    "hit_count",
    "hit_rate",
    "calibration_gap",
    "brier_score",
    "t_stat",
    "p_value",
    "significant",
    "calibration_verdict",
    "recommended_action",
    "evidence_note",
    "requires_human_approval",
    "weights_json_updated",
]


def load_implied_probabilities() -> tuple[dict[str, float], str]:
    if CONFIG_PATH.exists():
        try:
            payload = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            if isinstance(payload, dict) and payload:
                cleaned = {}
                for key, value in payload.items():
                    try:
                        p = float(value)
                    except (TypeError, ValueError):
                        continue
                    if 0.0 < p < 1.0:
                        cleaned[str(key).strip().upper()] = p
                if cleaned:
                    return cleaned, str(CONFIG_PATH)
        except (OSError, json.JSONDecodeError):
            pass
    return dict(DEFAULT_IMPLIED_PROBABILITY), "default (SPEC-BC-001 frozen)"


def load_evaluations() -> pd.DataFrame:
    for path in EVALUATIONS_CANDIDATES:
        df = read_csv(path)
        if not df.empty:
            return df
    return pd.DataFrame()


def closed_hits_by_rank(signals: pd.DataFrame, evaluations: pd.DataFrame) -> pd.DataFrame:
    """rank別の (signal_id, hit) テーブル。hit = r_result > 0。"""
    if signals.empty or evaluations.empty:
        return pd.DataFrame()
    if "signal_id" not in signals.columns or "rank" not in signals.columns or "signal_id" not in evaluations.columns:
        return pd.DataFrame()
    if "evaluation_status" in evaluations.columns:
        closed = evaluations[evaluations["evaluation_status"].astype(str).str.lower() == "closed"].copy()
    else:
        closed = evaluations.copy()
    if closed.empty or "r_result" not in closed.columns:
        return pd.DataFrame()
    closed["r_result"] = pd.to_numeric(closed["r_result"], errors="coerce")
    closed = closed.dropna(subset=["r_result"]).drop_duplicates(subset=["signal_id"], keep="last")
    ranks = signals[["signal_id", "rank"]].drop_duplicates(subset=["signal_id"], keep="last")
    joined = closed.merge(ranks, on="signal_id", how="inner")
    if joined.empty:
        return pd.DataFrame()
    joined["rank"] = joined["rank"].astype(str).str.strip().str.upper()
    joined["hit"] = (joined["r_result"] > 0).astype(int)
    return joined[["signal_id", "rank", "hit"]]


def calibration_verdict(gap: float, significant: bool, n: int) -> tuple[str, str]:
    if n < stat_guards.MIN_SAMPLES_WEIGHT_CHANGE:
        return "insufficient_data", "wait_for_more_data"
    if not significant:
        return "well_calibrated", "no_action"
    if gap < 0:
        return "overconfident", "human_review_lower_implied_probability_or_tighten_rank_criteria"
    return "underconfident", "human_review_raise_implied_probability_or_relax_rank_criteria"


def build_calibration_rows(hits: pd.DataFrame, implied: dict[str, float], generated_at_jst: str) -> pd.DataFrame:
    if hits.empty:
        return pd.DataFrame(columns=CALIBRATION_COLUMNS)
    rows = []
    for rank, p in sorted(implied.items()):
        group = hits[hits["rank"] == rank]
        n = len(group)
        if n == 0:
            continue
        hit_values = group["hit"].astype(float).tolist()
        hit_count = int(sum(hit_values))
        hit_rate = hit_count / n
        gap = hit_rate - p
        brier = sum((p - h) ** 2 for h in hit_values) / n
        # (hit_i - p) の一標本t検定: 的中率がimpliedと有意に異なるか
        t_stat, p_value = stat_guards.t_test_one_sample([h - p for h in hit_values])
        significant = p_value < stat_guards.SIGNIFICANCE_ALPHA and n >= stat_guards.MIN_SAMPLES_WEIGHT_CHANGE
        verdict, action = calibration_verdict(gap, p_value < stat_guards.SIGNIFICANCE_ALPHA, n)
        rows.append(
            {
                "generated_at_jst": generated_at_jst,
                "rank": rank,
                "implied_probability": round(p, 4),
                "closed_count": n,
                "hit_count": hit_count,
                "hit_rate": round(hit_rate, 4),
                "calibration_gap": round(gap, 4),
                "brier_score": round(brier, 4),
                "t_stat": round(t_stat, 4) if math.isfinite(t_stat) else t_stat,
                "p_value": round(p_value, 6),
                "significant": bool(significant),
                "calibration_verdict": verdict,
                "recommended_action": action,
                "evidence_note": f"n={n}, hit={hit_rate:.3f}, implied={p:.2f}, gap={gap:+.3f}, brier={brier:.4f}, p={p_value:.4f}",
                "requires_human_approval": True,
                "weights_json_updated": False,
            }
        )
    return pd.DataFrame(rows, columns=CALIBRATION_COLUMNS)


def brier_skill_score(hits: pd.DataFrame, implied: dict[str, float]) -> dict[str, float]:
    """全体Brier vs 基準Brier(全体的中率を常に予測した場合)。BSS = 1 - BS/BS_ref。"""
    scored = hits[hits["rank"].isin(implied.keys())]
    if scored.empty:
        return {"overall_brier": 0.0, "reference_brier": 0.0, "brier_skill_score": 0.0, "scored_n": 0}
    base_rate = float(scored["hit"].mean())
    bs = float(sum((implied[r] - h) ** 2 for r, h in zip(scored["rank"], scored["hit"])) / len(scored))
    bs_ref = float(sum((base_rate - h) ** 2 for h in scored["hit"]) / len(scored))
    bss = 1.0 - (bs / bs_ref) if bs_ref > 0 else 0.0
    return {
        "overall_brier": round(bs, 4),
        "reference_brier": round(bs_ref, 4),
        "brier_skill_score": round(bss, 4),
        "scored_n": int(len(scored)),
    }


def summary_from(table: pd.DataFrame, skill: dict[str, float], source: str, generated_at_jst: str, generated_at_utc: str) -> dict[str, Any]:
    verdict = table.get("calibration_verdict", pd.Series(dtype=str)) if not table.empty else pd.Series(dtype=str)
    return {
        "generated_at_jst": generated_at_jst,
        "generated_at_utc": generated_at_utc,
        "calibration_status": "unavailable" if table.empty else "active",
        "implied_probability_source": source,
        "ranks_tracked": int(len(table)),
        "overconfident_count": int((verdict == "overconfident").sum()) if not table.empty else 0,
        "underconfident_count": int((verdict == "underconfident").sum()) if not table.empty else 0,
        "well_calibrated_count": int((verdict == "well_calibrated").sum()) if not table.empty else 0,
        "insufficient_data_count": int((verdict == "insufficient_data").sum()) if not table.empty else 0,
        **skill,
        "gate_spec": "SPEC-SG-001 (n>=30, alpha=0.05)",
        "requires_human_approval": True,
        "weights_json_updated": False,
        "apply_automatically": False,
    }


def markdown_table(df: pd.DataFrame, empty: str = "該当なし") -> str:
    if df.empty:
        return empty
    cols = [str(col) for col in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("\n", " ").replace("|", "/") for col in df.columns) + " |")
    return "\n".join(lines)


def render_markdown(summary: dict[str, Any], table: pd.DataFrame) -> str:
    cols = ["rank", "implied_probability", "closed_count", "hit_rate", "calibration_gap", "brier_score", "p_value", "calibration_verdict", "recommended_action"]
    return f"""# Prediction Calibration (SPEC-BC-001)

## 1. 概要

- 生成日時JST: {summary["generated_at_jst"]}
- calibration_status: {summary["calibration_status"]}
- implied_probability_source: {summary["implied_probability_source"]}
- overall_brier: {summary["overall_brier"]} / reference_brier: {summary["reference_brier"]}
- **Brier Skill Score: {summary["brier_skill_score"]}** (scored_n={summary["scored_n"]})
- overconfident: {summary["overconfident_count"]} / underconfident: {summary["underconfident_count"]} / well_calibrated: {summary["well_calibrated_count"]} / insufficient: {summary["insufficient_data_count"]}
- 適用ゲート: {summary["gate_spec"]}
- weights_json_updated: false / requires_human_approval: true

## 2. Rank別キャリブレーション

{markdown_table(table[cols] if not table.empty else table)}

## 3. 読み方

- calibration_gap = 実際の的中率 - 暗黙的勝率。負で有意なら **overconfident** (AIは自信過剰)
- Brier Skill Score > 0 なら、Rank分けは「常に平均勝率を予測する」より情報量がある
- n >= 30 未満のRankは判定保留

## 4. 注意

- このレポートはAIの確信度を採点するだけです。weights.jsonは更新しません
- implied probabilityの変更は config/rank_implied_probability.json で人間が行います
- 実売買・発注は行いません
"""


def build_prediction_calibration() -> tuple[pd.DataFrame, dict[str, Any], str]:
    generated_dt_utc = now_utc()
    generated_at_jst = format_jst(generated_dt_utc)
    generated_at_utc = format_utc(generated_dt_utc)
    implied, source = load_implied_probabilities()
    signals = read_csv(SIGNALS_CSV)
    evaluations = load_evaluations()
    hits = closed_hits_by_rank(signals, evaluations)
    table = build_calibration_rows(hits, implied, generated_at_jst)
    skill = brier_skill_score(hits, implied) if not hits.empty else {"overall_brier": 0.0, "reference_brier": 0.0, "brier_skill_score": 0.0, "scored_n": 0}
    summary = summary_from(table, skill, source, generated_at_jst, generated_at_utc)
    payload = {
        **summary,
        "safety": {
            "weights_json_updated": False,
            "patch_applied": False,
            "requires_human_approval": True,
            "apply_automatically": False,
        },
        "rank_calibration": table.to_dict(orient="records"),
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_date = generated_at_jst[:10]
    csv_path = RESULTS_DIR / "prediction_calibration.csv"
    json_path = RESULTS_DIR / "prediction_calibration.json"
    report_path = REPORTS_DIR / f"{report_date}_prediction_calibration.md"
    table.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    report_path.write_text(render_markdown(summary, table), encoding="utf-8")
    print(f"prediction calibration generated: {report_path}")
    print(f"prediction calibration rows: {len(table)}")
    return table, summary, str(report_path)


def main() -> int:
    build_prediction_calibration()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
