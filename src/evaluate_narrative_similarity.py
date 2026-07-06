"""Narrative similarity evaluation v0 (Phase 29.2) — 類似検索に予測力はあるかの検証。

過去の各局面日 d について、それ**以前**の局面のみから top-1 類似日 s を検索し
（as-of・lookahead-safe）、「s の直後リターンの符号」が「d の直後リターンの符号」と
一致した割合（方向一致率）を資産×ホライズン別に集計する。

- サンプルが MIN_PAIRS 未満の間は insufficient_data を正直に表示する
  （実装はデータを待たない: データが溜まれば同じコマンドで自動的に数字が出る）。
- 出力は評価・表示のみで、signal score には未接続。
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from build_narrative_memory import MEMORY_PATH, load_memory
from retrieve_similar_narratives import (
    HORIZONS,
    MIN_MEMORY_DAYS,
    RAW_DIR,
    SAFETY_FIELDS,
    build_day_documents,
    cosine_similarities,
    forward_returns,
    load_close_series,
    tfidf_matrix,
)
from time_utils import format_jst, format_utc, now_utc

RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/narrative")
MIN_PAIRS = 30  # 採用判断に足る最低ペア数(SPEC-SG-001 の n>=30 と整合)。実装はこれを待たない。

EVAL_COLUMNS = [
    "asset",
    "horizon_days",
    "pairs_evaluated",
    "direction_agreement_rate",
    "mean_similar_fwd_return",
    "mean_query_fwd_return",
    "status",
]


def _pairs(day_docs: pd.DataFrame) -> list[tuple[str, str, float]]:
    """各日 d について、d より前の局面のみから top-1 類似日 s を返す (d, s, similarity)。

    TF-IDF は毎回「d 以前の文書だけ」で fit する（未来語彙の混入を防ぐ as-of 徹底）。
    """
    dates = day_docs["memory_date"].tolist()
    docs = day_docs["doc"].tolist()
    out: list[tuple[str, str, float]] = []
    for i in range(len(dates)):
        if i < MIN_MEMORY_DAYS:
            continue  # 過去局面が最低日数に満たない日は評価しない
        corpus_docs = docs[:i] + [docs[i]]
        emb = tfidf_matrix(corpus_docs)
        sims = cosine_similarities(emb, len(corpus_docs) - 1)[:-1]
        j = int(np.argmax(sims))
        out.append((dates[i], dates[j], float(sims[j])))
    return out


def evaluate(memory: pd.DataFrame, *, raw_dir: Path = RAW_DIR) -> tuple[pd.DataFrame, dict]:
    day_docs = build_day_documents(memory)
    meta = {"memory_days_total": int(len(day_docs)), "pairs_total": 0, "status": ""}
    if len(day_docs) <= MIN_MEMORY_DAYS:
        meta["status"] = "insufficient_data"
        return pd.DataFrame(columns=EVAL_COLUMNS), meta

    pairs = _pairs(day_docs)
    meta["pairs_total"] = len(pairs)
    if not pairs:
        meta["status"] = "insufficient_data"
        return pd.DataFrame(columns=EVAL_COLUMNS), meta

    assets = sorted(p.stem for p in raw_dir.glob("*.csv")) if raw_dir.exists() else []
    if not assets:
        meta["status"] = "no_price_data"
        return pd.DataFrame(columns=EVAL_COLUMNS), meta

    rows: list[dict] = []
    for asset in assets:
        closes = load_close_series(asset, raw_dir)
        for h in HORIZONS:
            col = f"fwd_return_{h}d"
            q_rets, s_rets = [], []
            seen_bars: set[int] = set()
            for d, s, _sim in pairs:
                if closes.empty:
                    continue
                idx_d = int(closes.index.searchsorted(pd.Timestamp(d), side="right")) - 1
                idx_s = int(closes.index.searchsorted(pd.Timestamp(s), side="right")) - 1
                if idx_d < 0 or idx_s < 0:
                    continue
                # レビュー指摘#1: 類似日 s の結果窓が d 時点で閉じていること(重なり=lookahead防止)。
                # d の未来を含む窓を「予測子」に使うと iid でも一致率が構造的に膨らむ。
                if idx_s + h > idx_d:
                    continue
                # レビュー指摘#2: 週末の暦日が同一バーに解決される重複を1件に(独立性・nの水増し防止)
                if idx_d in seen_bars:
                    continue
                q = forward_returns(closes, d, [h])[col]
                sv = forward_returns(closes, s, [h])[col]
                if pd.notna(q) and pd.notna(sv):
                    seen_bars.add(idx_d)
                    q_rets.append(float(q))
                    s_rets.append(float(sv))
            n = len(q_rets)
            if n == 0:
                rows.append({"asset": asset, "horizon_days": h, "pairs_evaluated": 0,
                             "direction_agreement_rate": np.nan, "mean_similar_fwd_return": np.nan,
                             "mean_query_fwd_return": np.nan, "status": "insufficient_data"})
                continue
            agree = sum(1 for q, sv in zip(q_rets, s_rets) if np.sign(q) == np.sign(sv) and q != 0)
            rows.append({
                "asset": asset,
                "horizon_days": h,
                "pairs_evaluated": n,
                "direction_agreement_rate": round(agree / n, 4),
                "mean_similar_fwd_return": round(float(np.mean(s_rets)), 6),
                "mean_query_fwd_return": round(float(np.mean(q_rets)), 6),
                # n>=30 で初めて「判断材料」。未満は正直に insufficient_data
                "status": "ok" if n >= MIN_PAIRS else "insufficient_data",
            })
    table = pd.DataFrame(rows, columns=EVAL_COLUMNS)
    meta["status"] = "ok" if (table["status"] == "ok").any() else "insufficient_data"
    return table, meta


def render_report(meta: dict, table: pd.DataFrame, generated_at_jst: str) -> str:
    if table.empty:
        body = "_評価対象なし（局面文書の蓄積待ち。データが溜まれば自動で数字が出る）_"
    else:
        lines = [
            "| asset | horizon | pairs | 方向一致率 | mean fwd(similar) | mean fwd(query) | status |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
        for _, r in table.iterrows():
            rate = f"{r['direction_agreement_rate']:.2%}" if pd.notna(r["direction_agreement_rate"]) else "—"
            lines.append(
                f"| {r['asset']} | {r['horizon_days']}d | {r['pairs_evaluated']} | {rate} "
                f"| {r['mean_similar_fwd_return']} | {r['mean_query_fwd_return']} | {r['status']} |"
            )
        body = "\n".join(lines)
    return f"""# Narrative Similarity Evaluation（類似検索の予測力検証 v0）

## 1. 概要

- 生成日時JST: {generated_at_jst}
- status: **{meta['status']}** / 局面日数: {meta['memory_days_total']} / 評価ペア: {meta['pairs_total']}
- 方式: 各日 d の top-1 類似日 s（d 以前のみから as-of 検索）について、
  d と s の +5/10/20営業日リターンの**方向一致率**を集計。n>={MIN_PAIRS} で判断材料になる。

## 2. 資産×ホライズン別

{body}

## 3. 注意

- insufficient_data はデータ不足の正直表示であり失敗ではない。実装はデータを待たない。
- 表示・検証のみ。signal score には未接続。実売買・発注は行わない。
"""


def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    generated_at = now_utc()

    memory = load_memory(MEMORY_PATH)
    table, meta = evaluate(memory)

    summary = {
        "generated_at_jst": format_jst(generated_at),
        "generated_at_utc": format_utc(generated_at),
        **meta,
        "min_pairs_for_judgement": MIN_PAIRS,
    }
    summary.update(SAFETY_FIELDS)

    table.to_csv(RESULTS_DIR / "narrative_similarity_evaluation.csv", index=False)
    (RESULTS_DIR / "narrative_similarity_evaluation.json").write_text(
        json.dumps({"summary": summary, "rows": table.where(pd.notna(table), None).to_dict(orient="records")},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    report_date = format_jst(generated_at)[:10]
    (REPORTS_DIR / f"{report_date}_narrative_similarity_evaluation.md").write_text(
        render_report(meta, table, format_jst(generated_at)), encoding="utf-8"
    )
    print(f"narrative similarity evaluation: status={meta['status']} days={meta['memory_days_total']} pairs={meta['pairs_total']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
