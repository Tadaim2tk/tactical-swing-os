"""Narrative Memory v0 (Phase 29.2) の単体テスト。

検証の柱:
1. 時刻フィールドと cutoff の機械的判定（lookahead 防止の根幹）
2. published 欠損 / cutoff 違反は allowed_for_signal=false で機械除外
3. TF-IDF ローカルフォールバックが日本語・英語で動く
4. retrieval は as-of（基準日より前のみ・allowedのみ）
5. データ不足時は insufficient_data の正直表示（捏造しない）
6. 先行きリターンは実価格から・未来バー不足は awaiting_horizon
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import build_narrative_memory as bnm
import evaluate_narrative_similarity as ens
import retrieve_similar_narratives as rsn


# === 1. cutoff 計算 ===

def test_cutoff_same_day_when_observed_before_2155utc():
    obs = pd.Timestamp("2026-07-01 21:50:00")
    assert bnm.compute_signal_cutoff_utc(obs) == pd.Timestamp("2026-07-01 21:55:00")


def test_cutoff_next_day_when_observed_after_2155utc():
    obs = pd.Timestamp("2026-07-01 22:57:00")
    assert bnm.compute_signal_cutoff_utc(obs) == pd.Timestamp("2026-07-02 21:55:00")


# === 2. record 構築と機械除外 ===

def _headline(**over) -> dict:
    base = dict(
        fetched_at_utc="2026-07-01 21:50:00 UTC",
        published_utc="2026-07-01 20:00:00 UTC",
        title="Fed keeps rates unchanged",
        summary="Federal Reserve holds policy rate steady.",
        link="https://example.com/a",
        source="TestWire", source_category="macro", matched_assets="SPX|GOLD",
    )
    base.update(over)
    return base


def test_build_records_allowed_when_published_before_cutoff():
    df = pd.DataFrame([_headline()])
    out = bnm.build_records(df, pd.Timestamp("2026-07-01 21:52:00"))
    r = out.iloc[0]
    assert bool(r["allowed_for_signal"]) is True
    assert bool(r["cutoff_violation"]) is False
    assert r["signal_cutoff_utc"] == "2026-07-01 21:55:00 UTC"
    assert r["memory_date"] == "2026-07-01"
    assert r["source_published_at_utc"] == "2026-07-01 20:00:00 UTC"


def test_missing_published_is_excluded_not_allowed():
    df = pd.DataFrame([_headline(published_utc="")])
    r = bnm.build_records(df, pd.Timestamp("2026-07-01 21:52:00")).iloc[0]
    assert bool(r["allowed_for_signal"]) is False
    assert r["exclusion_reason"] == "missing_published_at"
    assert bool(r["cutoff_violation"]) is False


def test_published_after_cutoff_is_violation_and_excluded():
    # 公表が cutoff より後 = この cutoff のシグナルには使えない情報
    df = pd.DataFrame([_headline(published_utc="2026-07-01 23:00:00 UTC")])
    r = bnm.build_records(df, pd.Timestamp("2026-07-01 21:52:00")).iloc[0]
    assert bool(r["allowed_for_signal"]) is False
    assert bool(r["cutoff_violation"]) is True
    assert r["exclusion_reason"] == "published_after_cutoff"


def test_merge_memory_dedupes_and_keeps_first():
    df = pd.DataFrame([_headline()])
    a = bnm.build_records(df, pd.Timestamp("2026-07-01 21:52:00"))
    b = bnm.build_records(df, pd.Timestamp("2026-07-02 21:52:00"))  # 同一record再取込
    merged = bnm.merge_memory(a, b)
    assert len(merged) == 1
    assert merged.iloc[0]["ingested_at_utc"] == a.iloc[0]["ingested_at_utc"]  # 先着保持


def test_summary_flags_allowed_violation_as_zero_normally():
    df = pd.DataFrame([_headline(), _headline(link="https://example.com/b", published_utc="")])
    mem = bnm.build_records(df, pd.Timestamp("2026-07-01 21:52:00"))
    from time_utils import now_utc
    s = bnm.build_summary(mem, added=2, generated_at=now_utc())
    assert s["total_records"] == 2
    assert s["allowed_for_signal_count"] == 1
    assert s["allowed_with_violation_count"] == 0  # 機械除外が破れていない
    assert s["connected_to_signal_score"] is False


# === 3. TF-IDF フォールバック ===

def test_tfidf_similar_texts_rank_higher():
    docs = [
        "inflation pressure rises as oil surges",       # 類似
        "champions league final tonight",               # 無関係
        "inflation and oil prices keep rising fast",    # クエリ
    ]
    m = rsn.tfidf_matrix(docs)
    sims = rsn.cosine_similarities(m, 2)
    assert sims[0] > sims[1]


def test_tokenize_japanese_bigrams():
    toks = rsn.tokenize("日銀が利上げ decision")
    assert "日銀" in toks and "利上" in toks and "decision" in toks


# === 4/5. retrieval: as-of とデータ不足の正直表示 ===

def _memory_days(n: int, start="2026-06-01") -> pd.DataFrame:
    """n日分の allowed 局面record（1日1件）を持つ memory を作る。"""
    dates = pd.bdate_range(start, periods=n)
    rows = []
    for i, d in enumerate(dates):
        rows.append({
            "record_id": f"r{i}", "memory_date": d.strftime("%Y-%m-%d"),
            "asset_tags": "", "source": "t", "source_category": "macro",
            "text": f"macro topic {i} inflation oil rates day{i}",
            "link": f"https://x/{i}",
            "observed_at_utc": f"{d.strftime('%Y-%m-%d')} 21:50:00 UTC",
            "source_published_at_utc": f"{d.strftime('%Y-%m-%d')} 20:00:00 UTC",
            "ingested_at_utc": f"{d.strftime('%Y-%m-%d')} 21:52:00 UTC",
            "signal_cutoff_utc": f"{d.strftime('%Y-%m-%d')} 21:55:00 UTC",
            "allowed_for_signal": True, "cutoff_violation": False, "exclusion_reason": "",
        })
    return pd.DataFrame(rows, columns=bnm.MEMORY_COLUMNS)


def test_retrieve_insufficient_data_is_honest(tmp_path):
    mem = _memory_days(3)
    as_of = mem["memory_date"].max()
    cases, meta = rsn.retrieve(mem, as_of, raw_dir=tmp_path)
    assert meta["status"] == "insufficient_data"
    assert cases.empty  # 捏造しない


def test_retrieve_only_uses_past_days(tmp_path):
    mem = _memory_days(10)
    as_of = mem["memory_date"].max()
    cases, meta = rsn.retrieve(mem, as_of, raw_dir=tmp_path)
    assert meta["status"] == "ok"
    assert (cases["similar_date"] < as_of).all()  # 基準日より前のみ
    assert meta["corpus_days"] == 9


def test_retrieve_excludes_disallowed_records(tmp_path):
    mem = _memory_days(10)
    # 全record を not-allowed にすると局面文書が消える
    mem["allowed_for_signal"] = False
    cases, meta = rsn.retrieve(mem, mem["memory_date"].max(), raw_dir=tmp_path)
    assert meta["status"] == "no_query_document"
    assert cases.empty


# === 6. 先行きリターン ===

def _price_csv(tmp_path: Path, asset="SPX", n=40, start="2026-06-01"):
    dates = pd.bdate_range(start, periods=n)
    close = pd.Series(100.0 * (1.01 ** np.arange(n)))  # 毎バー+1%
    df = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "open": close, "high": close, "low": close, "close": close})
    (tmp_path / f"{asset}.csv").write_text(df.to_csv(index=False), encoding="utf-8")
    return dates


def test_forward_returns_from_real_prices(tmp_path):
    dates = _price_csv(tmp_path, n=40)
    closes = rsn.load_close_series("SPX", tmp_path)
    out = rsn.forward_returns(closes, dates[5].strftime("%Y-%m-%d"))
    assert abs(out["fwd_return_5d"] - (1.01 ** 5 - 1)) < 1e-6   # 出力は6桁丸め
    assert abs(out["fwd_return_20d"] - (1.01 ** 20 - 1)) < 1e-6
    assert out["outcome_status"] == "ok"


def test_forward_returns_awaiting_horizon_when_future_missing(tmp_path):
    dates = _price_csv(tmp_path, n=10)
    closes = rsn.load_close_series("SPX", tmp_path)
    out = rsn.forward_returns(closes, dates[-2].strftime("%Y-%m-%d"))
    assert pd.isna(out["fwd_return_20d"])  # 未来バー不足を捏造しない
    assert out["outcome_status"] == "awaiting_horizon"


def test_retrieve_joins_forward_returns(tmp_path):
    _price_csv(tmp_path, n=60)
    mem = _memory_days(10, start="2026-06-01")
    cases, meta = rsn.retrieve(mem, mem["memory_date"].max(), raw_dir=tmp_path)
    assert meta["status"] == "ok"
    spx = cases[cases["asset"] == "SPX"]
    assert not spx.empty
    assert spx["fwd_return_5d"].notna().any()


# === 評価モジュール ===

def test_evaluation_insufficient_when_few_days(tmp_path):
    table, meta = ens.evaluate(_memory_days(4), raw_dir=tmp_path)
    assert meta["status"] == "insufficient_data"
    assert table.empty


def test_evaluation_runs_with_enough_days_and_prices(tmp_path):
    _price_csv(tmp_path, n=80)
    table, meta = ens.evaluate(_memory_days(20), raw_dir=tmp_path)
    assert meta["pairs_total"] > 0
    spx5 = table[(table["asset"] == "SPX") & (table["horizon_days"] == 5)]
    assert len(spx5) == 1
    n = int(spx5.iloc[0]["pairs_evaluated"])
    assert n > 0
    # n<30 のうちは判断材料にしない正直表示
    expected = "ok" if n >= ens.MIN_PAIRS else "insufficient_data"
    assert spx5.iloc[0]["status"] == expected


def test_safety_fields_present_in_modules():
    for fields in (bnm.SAFETY_FIELDS, rsn.SAFETY_FIELDS):
        assert fields["connected_to_signal_score"] is False
        assert fields["weights_json_updated"] is False
        assert fields["generate_signal_updated"] is False
        assert fields["requires_human_approval"] is True
