"""Similar narrative retrieval v0 (Phase 29.2) — 「今日の局面は過去のどの局面に似ているか」。

data/narrative_memory.csv の allowed_for_signal=true な record を日毎の「局面文書」に
まとめ、基準日(as-of)の文書と過去の文書の意味的類似度を計算して上位を返す。
各類似日について、その後 5/10/20 営業日の資産別リターンを data/raw の実価格から付す。

lookahead 防止（機械的・不可侵）:
- allowed_for_signal=false の record は使わない
- 基準日の cutoff より後に材料になる record は使わない（signal_cutoff_utc で比較）
- 類似候補は基準日より**前**の日のみ

embedding provider:
- 環境変数 TSO_EMBEDDING_PROVIDER=openai + OPENAI_API_KEY 設定時のみ OpenAI embeddings を使用
  （モデルは TSO_EMBEDDING_MODEL、既定 text-embedding-3-small）
- キー未設定・API失敗時は **TF-IDF ローカルフォールバック**（純numpy・依存追加なし）で必ず動く

出力は表示・記録のみで、signal score には未接続（summary の connected_to_signal_score=false）。
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

import numpy as np
import pandas as pd

from build_narrative_memory import MEMORY_PATH, load_memory
from time_utils import JST, format_jst, format_utc, now_utc

RAW_DIR = Path("data/raw")
RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/narrative")

TOP_K = 5
MIN_MEMORY_DAYS = 5          # これ未満の過去日しか無ければ insufficient_data
HORIZONS = [5, 10, 20]       # 営業日(=バー数)
MAX_DOC_CHARS = 8000

CASE_COLUMNS = [
    "query_date",
    "similar_rank",
    "similar_date",
    "similarity",
    "embedding_provider",
    "asset",
    "fwd_return_5d",
    "fwd_return_10d",
    "fwd_return_20d",
    "outcome_status",
]

SAFETY_FIELDS = {
    "requires_human_approval": True,
    "weights_json_updated": False,
    "generate_signal_updated": False,
    "connected_to_signal_score": False,
}


# ── トークナイズ / TF-IDF (純numpy・sklearn不使用) ─────────────────────────────

_WORD_RE = re.compile(r"[a-z0-9]{2,}")
# ひらがな・カタカナ・CJK統合漢字
_CJK_RE = re.compile("[\u3040-\u30ff\u4e00-\u9fff]+")


def tokenize(text: str) -> list[str]:
    """英数字は単語、日本語(CJK)は文字bigramでトークン化する。"""
    s = str(text).lower()
    tokens = _WORD_RE.findall(s)
    for run in _CJK_RE.findall(s):
        if len(run) == 1:
            tokens.append(run)
        else:
            tokens.extend(run[i:i + 2] for i in range(len(run) - 1))
    return tokens


def tfidf_matrix(docs: list[str]) -> np.ndarray:
    """docs を L2 正規化済み TF-IDF 行列へ（行=doc）。"""
    token_lists = [tokenize(d) for d in docs]
    vocab: dict[str, int] = {}
    for toks in token_lists:
        for t in toks:
            if t not in vocab:
                vocab[t] = len(vocab)
    n_docs, n_terms = len(docs), max(len(vocab), 1)
    mat = np.zeros((n_docs, n_terms), dtype=float)
    for i, toks in enumerate(token_lists):
        for t in toks:
            mat[i, vocab[t]] += 1.0
    df = (mat > 0).sum(axis=0)
    idf = np.log((n_docs + 1) / (df + 1)) + 1.0
    mat *= idf
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return mat / norms


def cosine_similarities(matrix: np.ndarray, query_index: int) -> np.ndarray:
    return matrix @ matrix[query_index]


# ── Embedding provider (任意・フォールバック必須) ──────────────────────────────

def embed_documents(docs: list[str]) -> tuple[np.ndarray | None, str]:
    """provider embedding を試み、(行列 or None, provider名) を返す。失敗は None (TF-IDFへ)。"""
    provider = os.getenv("TSO_EMBEDDING_PROVIDER", "").strip().lower()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if provider != "openai" or not api_key:
        return None, "tfidf_local"
    try:
        import requests

        model = os.getenv("TSO_EMBEDDING_MODEL", "text-embedding-3-small")
        resp = requests.post(
            "https://api.openai.com/v1/embeddings",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": model, "input": [d[:MAX_DOC_CHARS] for d in docs]},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()["data"]
        mat = np.array([row["embedding"] for row in data], dtype=float)
        norms = np.linalg.norm(mat, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return mat / norms, f"openai:{model}"
    except Exception as exc:  # noqa: BLE001 - フォールバックで必ず動く(キーはログに出さない)
        print(f"warning: embedding provider failed; falling back to TF-IDF: {type(exc).__name__}")
        return None, "tfidf_local"


# ── 日毎の局面文書 ───────────────────────────────────────────────────────────

def build_day_documents(memory: pd.DataFrame) -> pd.DataFrame:
    """allowed record を memory_date 毎に連結し「局面文書」を作る。"""
    if memory.empty:
        return pd.DataFrame(columns=["memory_date", "doc", "record_count"])
    allowed = memory[memory["allowed_for_signal"].astype(bool)].copy()
    if allowed.empty:
        return pd.DataFrame(columns=["memory_date", "doc", "record_count"])
    grouped = (
        allowed.groupby("memory_date")["text"]
        .apply(lambda s: " ".join(str(t) for t in s)[:MAX_DOC_CHARS])
        .reset_index()
        .rename(columns={"text": "doc"})
    )
    counts = allowed.groupby("memory_date").size().reset_index(name="record_count")
    return grouped.merge(counts, on="memory_date").sort_values("memory_date").reset_index(drop=True)


# ── 先行きリターン (実価格・営業日=バー数) ──────────────────────────────────────

def load_close_series(asset: str, raw_dir: Path = RAW_DIR) -> pd.Series:
    path = raw_dir / f"{asset}.csv"
    if not path.exists():
        return pd.Series(dtype=float)
    try:
        df = pd.read_csv(path)
    except (pd.errors.EmptyDataError, OSError):
        return pd.Series(dtype=float)
    df.columns = [str(c).strip().lower() for c in df.columns]
    if "date" not in df.columns or "close" not in df.columns:
        return pd.Series(dtype=float)
    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True).dt.tz_localize(None)
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna(subset=["date", "close"]).sort_values("date")
    return pd.Series(df["close"].values, index=df["date"].dt.normalize())


def forward_returns(closes: pd.Series, base_date: str, horizons: list[int] = HORIZONS) -> dict:
    """base_date 以前の最後のバーを起点に、+h バー先の単純リターンを返す。

    未来バーが足りないホライズンは NaN（データ捏造しない）。
    """
    out = {f"fwd_return_{h}d": np.nan for h in horizons}
    status = "ok"
    if closes.empty:
        return {**out, "outcome_status": "no_price_data"}
    base = pd.Timestamp(base_date)
    idx = closes.index.searchsorted(base, side="right") - 1
    if idx < 0:
        return {**out, "outcome_status": "before_price_history"}
    base_close = float(closes.iloc[idx])
    incomplete = False
    for h in horizons:
        j = idx + h
        if j < len(closes):
            out[f"fwd_return_{h}d"] = round(float(closes.iloc[j]) / base_close - 1.0, 6)
        else:
            incomplete = True
    if incomplete:
        status = "awaiting_horizon"
    return {**out, "outcome_status": status}


# ── retrieval 本体 ───────────────────────────────────────────────────────────

def retrieve(memory: pd.DataFrame, as_of_date: str, *, top_k: int = TOP_K, raw_dir: Path = RAW_DIR) -> tuple[pd.DataFrame, dict]:
    """as_of_date の局面文書に類似する過去日を返す（as-of / lookahead-safe）。"""
    days = build_day_documents(memory)
    meta = {
        "query_date": as_of_date,
        "memory_days_total": int(len(days)),
        "corpus_days": 0,
        "status": "",
        "embedding_provider": "",
    }
    if days.empty or as_of_date not in set(days["memory_date"]):
        meta["status"] = "no_query_document"
        return pd.DataFrame(columns=CASE_COLUMNS), meta

    corpus = days[days["memory_date"] < as_of_date].reset_index(drop=True)  # 基準日より前のみ
    meta["corpus_days"] = int(len(corpus))
    if len(corpus) < MIN_MEMORY_DAYS:
        meta["status"] = "insufficient_data"
        return pd.DataFrame(columns=CASE_COLUMNS), meta

    docs = corpus["doc"].tolist() + [days.loc[days["memory_date"] == as_of_date, "doc"].iloc[0]]
    emb, provider = embed_documents(docs)
    if emb is None:
        emb = tfidf_matrix(docs)
        provider = "tfidf_local"
    meta["embedding_provider"] = provider

    sims = cosine_similarities(emb, len(docs) - 1)[:-1]  # 自分自身を除く
    order = np.argsort(-sims)[:top_k]

    assets = sorted(p.stem for p in raw_dir.glob("*.csv")) if raw_dir.exists() else []
    closes = {a: load_close_series(a, raw_dir) for a in assets}

    rows: list[dict] = []
    for rank, ci in enumerate(order, start=1):
        sim_date = str(corpus.iloc[ci]["memory_date"])
        similarity = round(float(sims[ci]), 4)
        if not assets:
            rows.append({
                "query_date": as_of_date, "similar_rank": rank, "similar_date": sim_date,
                "similarity": similarity, "embedding_provider": provider, "asset": "",
                "fwd_return_5d": np.nan, "fwd_return_10d": np.nan, "fwd_return_20d": np.nan,
                "outcome_status": "no_price_data",
            })
            continue
        for asset in assets:
            outcome = forward_returns(closes[asset], sim_date)
            rows.append({
                "query_date": as_of_date, "similar_rank": rank, "similar_date": sim_date,
                "similarity": similarity, "embedding_provider": provider, "asset": asset,
                **outcome,
            })
    meta["status"] = "ok"
    return pd.DataFrame(rows, columns=CASE_COLUMNS), meta


def render_report(meta: dict, cases: pd.DataFrame) -> str:
    if meta["status"] != "ok":
        note = {
            "no_query_document": "基準日の局面文書が無い（本日の allowed ニュースが未取込）。",
            "insufficient_data": f"過去の局面文書が {meta['corpus_days']} 日分しか無く、最低 {MIN_MEMORY_DAYS} 日に満たない。",
        }.get(meta["status"], meta["status"])
        body = f"**{meta['status']}**: {note} データが溜まれば自動で結果が出る（実装はデータを待たない）。"
        table = "_類似局面なし_"
    else:
        body = f"embedding provider: `{meta['embedding_provider']}` / 過去局面 {meta['corpus_days']} 日から上位 {TOP_K} 日を検索。"
        lines = [
            "| rank | similar_date | similarity | asset | +5d | +10d | +20d | status |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        for _, r in cases.head(45).iterrows():
            def pct(v):
                return f"{v * 100:.2f}%" if pd.notna(v) else "—"
            lines.append(
                f"| {r['similar_rank']} | {r['similar_date']} | {r['similarity']} | {r['asset']} "
                f"| {pct(r['fwd_return_5d'])} | {pct(r['fwd_return_10d'])} | {pct(r['fwd_return_20d'])} | {r['outcome_status']} |"
            )
        table = "\n".join(lines)
    return f"""# Similar Narrative Cases（類似局面検索 v0）

## 1. 概要

- 基準日: {meta['query_date']}
- status: **{meta['status']}**
- {body}

## 2. 類似局面と、その後の実リターン（5/10/20営業日）

{table}

## 3. 注意

- allowed_for_signal=true の record のみ・基準日より前の局面のみを検索（lookahead-safe）。
- この出力は表示・記録のみで、signal score には接続していない（connected_to_signal_score=false）。
- 実売買・発注は行わない。
"""


def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    generated_at = now_utc()

    memory = load_memory(MEMORY_PATH)
    day_docs = build_day_documents(memory)
    as_of = str(day_docs["memory_date"].max()) if not day_docs.empty else format_jst(generated_at)[:10]

    cases, meta = retrieve(memory, as_of)
    summary = {
        "generated_at_jst": format_jst(generated_at),
        "generated_at_utc": format_utc(generated_at),
        **meta,
        "case_rows": int(len(cases)),
        "top_k": TOP_K,
        "min_memory_days": MIN_MEMORY_DAYS,
    }
    summary.update(SAFETY_FIELDS)

    cases.to_csv(RESULTS_DIR / "similar_narrative_cases.csv", index=False)
    cases.to_json(RESULTS_DIR / "similar_narrative_cases.json", orient="records", indent=2, force_ascii=False)
    (RESULTS_DIR / "similar_narrative_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    report_date = pd.Timestamp(generated_at).tz_convert(JST).strftime("%Y-%m-%d") if pd.Timestamp(generated_at).tzinfo else str(generated_at)[:10]
    (REPORTS_DIR / f"{report_date}_similar_narratives.md").write_text(render_report(meta, cases), encoding="utf-8")

    print(f"similar narratives: status={meta['status']} corpus_days={meta['corpus_days']} rows={len(cases)} provider={meta.get('embedding_provider') or '-'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
