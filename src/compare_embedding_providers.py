"""C-1: TF-IDF vs OpenAI embedding の retrieval 比較 (設計書 §3.4 の実行)。

目的: embedding が「類似局面検索の結論」を変えるかを数字で見る。
- 各 query 日(過去局面>=5日)について両プロバイダで top-K 類似日を取得
- (a) top-K 集合の Jaccard 重なり (b) 類似度順位の Spearman 相関 を算出
- 判定(設計書で固定済み・事前信念で決めない):
    mean Jaccard >= 0.6 -> 「結論はほぼ同じ」= TF-IDF のまま運用可(コスト0)
    mean Jaccard <  0.6 -> 「retrieval が実質的に変わる」= 予測力比較へ進む
      (方向一致率の比較は evaluate_narrative_similarity のデータが溜まってから。
       溜まるまでは verdict=materially_different_await_predictive を正直表示)

実行場所: OPENAI_API_KEY は Actions secret にのみ存在するため CI で dispatch する。
キーはログ・レポートに出さない。
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

RESULTS_DIR = Path("results")
TOP_K = 5
JACCARD_THRESHOLD = 0.6


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def spearman(x: list[float], y: list[float]) -> float:
    """Spearman 順位相関 (純numpy・タイは平均順位)。n<2 は nan。"""
    if len(x) != len(y) or len(x) < 2:
        return float("nan")
    def ranks(v):
        arr = np.asarray(v, dtype=float)
        order = arr.argsort()
        r = np.empty_like(arr)
        r[order] = np.arange(1, len(arr) + 1, dtype=float)
        # タイの平均順位化
        for val in np.unique(arr):
            mask = arr == val
            if mask.sum() > 1:
                r[mask] = r[mask].mean()
        return r
    rx, ry = ranks(x), ranks(y)
    if np.std(rx) == 0 or np.std(ry) == 0:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def retrieve_both(memory, query_date: str):
    """同一 query 日について (tfidf_cases, openai_cases) を返す。"""
    import retrieve_similar_narratives as rsn

    saved_provider = os.environ.pop("TSO_EMBEDDING_PROVIDER", None)
    try:
        cases_tfidf, meta_tfidf = rsn.retrieve(memory, query_date)
    finally:
        if saved_provider is not None:
            os.environ["TSO_EMBEDDING_PROVIDER"] = saved_provider
    cases_ai, meta_ai = rsn.retrieve(memory, query_date)
    return (cases_tfidf, meta_tfidf), (cases_ai, meta_ai)


def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    if not os.getenv("OPENAI_API_KEY", "").strip():
        print("error: OPENAI_API_KEY が無い環境では比較できない (CIで実行すること)")
        return 1
    os.environ["TSO_EMBEDDING_PROVIDER"] = "openai"

    from build_narrative_memory import load_memory
    import retrieve_similar_narratives as rsn

    memory = load_memory()
    days = rsn.build_day_documents(memory)
    dates = days["memory_date"].tolist()
    query_days = [d for i, d in enumerate(dates) if i >= rsn.MIN_MEMORY_DAYS]
    if not query_days:
        print(f"insufficient_data: 局面文書 {len(dates)} 日 (query可能日なし)")
        return 1

    rows = []
    for d in query_days:
        (ct, mt), (ca, ma) = retrieve_both(memory, d)
        if mt.get("status") != "ok" or ma.get("status") != "ok":
            rows.append({"query_date": d, "status": f"skip ({mt.get('status')}/{ma.get('status')})"})
            continue
        if not str(ma.get("embedding_provider", "")).startswith("openai"):
            print(f"error: openai 側の provider が {ma.get('embedding_provider')} (フォールバックした=API失敗)")
            return 1
        top_t = ct.drop_duplicates("similar_date").sort_values("similar_rank")
        top_a = ca.drop_duplicates("similar_date").sort_values("similar_rank")
        set_t = set(top_t["similar_date"].head(TOP_K))
        set_a = set(top_a["similar_date"].head(TOP_K))
        # Spearman: 両者に共通する類似日の順位相関(共通2件未満は nan)
        common = list(set_t & set_a)
        rank_t = {r.similar_date: r.similar_rank for r in top_t.itertuples()}
        rank_a = {r.similar_date: r.similar_rank for r in top_a.itertuples()}
        rho = spearman([rank_t[c] for c in common], [rank_a[c] for c in common]) if len(common) >= 2 else float("nan")
        rows.append({"query_date": d, "status": "ok",
                     "jaccard_top5": round(jaccard(set_t, set_a), 4),
                     "spearman_common": round(rho, 4) if not np.isnan(rho) else None,
                     "tfidf_top": sorted(set_t), "openai_top": sorted(set_a)})

    ok = [r for r in rows if r["status"] == "ok"]
    mean_j = float(np.mean([r["jaccard_top5"] for r in ok])) if ok else float("nan")
    if not ok:
        verdict = "insufficient_data"
    elif mean_j >= JACCARD_THRESHOLD:
        verdict = "equivalent_keep_tfidf_ok"  # どちらでも結論同じ(コスト0のTF-IDFで十分)
    else:
        verdict = "materially_different_await_predictive"  # 予測力比較(方向一致率)の蓄積待ち

    report = {"query_days_compared": len(ok), "mean_jaccard_top5": round(mean_j, 4) if ok else None,
              "threshold": JACCARD_THRESHOLD, "verdict": verdict, "per_day": rows}
    (RESULTS_DIR / "embedding_comparison_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"C-1: days={len(ok)} mean_jaccard={report['mean_jaccard_top5']} verdict={verdict}")
    for r in rows:
        if r["status"] == "ok":
            print(f"  {r['query_date']}: J={r['jaccard_top5']} rho={r['spearman_common']}")
        else:
            print(f"  {r['query_date']}: {r['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
