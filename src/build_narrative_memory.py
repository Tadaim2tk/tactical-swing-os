"""Narrative Memory v0 (Phase 29.2) — 意味ベクトル層の記憶ストア構築。

results/news_headlines.csv の見出しを、時刻フィールド付きの narrative record として
data/narrative_memory.csv（git追跡・Actionsのdata追記コミットで永続化）に蓄積する。

必須時刻フィールド（lookahead 防止の根幹。governance_reform_2026-07 不可侵 #3）:

- observed_at_utc:          我々がその情報を観測した時刻（= news の fetched_at_utc）
- source_published_at_utc:  情報源の公表時刻（= published_utc。欠損なら検証不能）
- ingested_at_utc:          本スクリプトが memory へ取り込んだ時刻
- signal_cutoff_utc:        この record が材料になり得る最初のシグナル生成時刻
                            （observed_at 以降の最初の 21:55 UTC = daily_cycle cron）
- allowed_for_signal:       source_published_at_utc が存在し、かつ
                            source_published_at_utc <= signal_cutoff_utc のときのみ true

allowed_for_signal=false の record は store に残る（監査可能）が、類似検索の
as-of retrieval からは機械的に除外される。公表時刻が cutoff より後の record は
cutoff_violation=true として narrative lookahead audit から見えるようにする。
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd

from time_utils import format_jst, format_utc, now_utc

RESULTS_DIR = Path("results")
MEMORY_PATH = Path("data/narrative_memory.csv")

# daily_cycle の cron (21:55 UTC)。シグナル生成 = この時刻に走る。
SIGNAL_CUTOFF_HOUR_UTC = 21
SIGNAL_CUTOFF_MINUTE_UTC = 55

MEMORY_COLUMNS = [
    "record_id",
    "memory_date",
    "asset_tags",
    "source",
    "source_category",
    "text",
    "link",
    "observed_at_utc",
    "source_published_at_utc",
    "ingested_at_utc",
    "signal_cutoff_utc",
    "allowed_for_signal",
    "cutoff_violation",
    "exclusion_reason",
]

SAFETY_FIELDS = {
    "requires_human_approval": True,
    "weights_json_updated": False,
    "generate_signal_updated": False,
    "connected_to_signal_score": False,  # v0: 表示・記録のみ。signal score には未接続
}


def _clean(value) -> str:
    """NaN/None を '' に、それ以外を strip 済み文字列に（'nan' 文字列化を防ぐ）。"""
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()


def parse_utc(value) -> pd.Timestamp | None:
    """'YYYY-MM-DD HH:MM:SS UTC' 形式(等)を naive UTC Timestamp へ。"""
    if value is None:
        return None
    s = str(value).strip()
    if not s or s.lower() in {"nan", "none", "nat"}:
        return None
    s = s.replace(" UTC", "").strip()
    ts = pd.to_datetime(s, errors="coerce", utc=True)
    if pd.isna(ts):
        return None
    return pd.Timestamp(ts).tz_convert("UTC").tz_localize(None)


def compute_signal_cutoff_utc(observed: pd.Timestamp) -> pd.Timestamp:
    """observed 以降で最初に来る 21:55 UTC（= daily_cycle 実行時刻）を返す。"""
    cutoff = observed.normalize() + pd.Timedelta(hours=SIGNAL_CUTOFF_HOUR_UTC, minutes=SIGNAL_CUTOFF_MINUTE_UTC)
    if observed > cutoff:
        cutoff += pd.Timedelta(days=1)
    return cutoff


def _record_id(link: str, title: str) -> str:
    # published は含めない(配信側の published 更新・再配信で同一記事が別IDになる二重登録を防ぐ。レビュー指摘#3)
    raw = f"{link}|{title}".encode("utf-8", errors="ignore")
    return hashlib.sha1(raw).hexdigest()[:16]


def as_bool_series(series: pd.Series) -> pd.Series:
    """fail-closed の bool 化。NaN/欠損/不明値は False(=シグナル用途から除外)。

    `.astype(bool)` は NaN を True にする(fail-open)ため使用禁止。レビュー指摘#4。
    """
    return series.map(
        lambda v: v is True or (isinstance(v, (bool, int, float)) and v == 1 and not pd.isna(v))
        or str(v).strip().lower() == "true"
    ).fillna(False).astype(bool)


def _fmt(ts: pd.Timestamp | None) -> str:
    return ts.strftime("%Y-%m-%d %H:%M:%S UTC") if ts is not None else ""


def build_records(headlines: pd.DataFrame, ingested_at_utc: pd.Timestamp) -> pd.DataFrame:
    """news_headlines の行を narrative record 群へ変換する（純関数）。"""
    if headlines.empty:
        return pd.DataFrame(columns=MEMORY_COLUMNS)

    rows: list[dict] = []
    for _, h in headlines.iterrows():
        title = _clean(h.get("title"))
        summary = _clean(h.get("summary"))
        if not title and not summary:
            continue
        observed = parse_utc(h.get("fetched_at_utc"))
        published = parse_utc(h.get("published_utc"))
        if observed is None:
            # 観測時刻が無い行は時系列位置を決められない -> 取り込まない(正直に捨てる)
            continue
        cutoff = compute_signal_cutoff_utc(observed)

        if published is None:
            allowed = False
            violation = False
            reason = "missing_published_at"
        elif published > cutoff:
            allowed = False
            violation = True
            reason = "published_after_cutoff"
        else:
            allowed = True
            violation = False
            reason = ""

        text = title if not summary else f"{title}。{summary}"
        rows.append({
            "record_id": _record_id(_clean(h.get("link")), title),
            # memory_date = この record が材料になり得るシグナル実行日(UTC)。日毎の「局面」文書のキー。
            "memory_date": cutoff.strftime("%Y-%m-%d"),
            "asset_tags": _clean(h.get("matched_assets")),
            "source": _clean(h.get("source")),
            "source_category": _clean(h.get("source_category")),
            "text": text,
            "link": _clean(h.get("link")),
            "observed_at_utc": _fmt(observed),
            "source_published_at_utc": _fmt(published),
            "ingested_at_utc": _fmt(ingested_at_utc),
            "signal_cutoff_utc": _fmt(cutoff),
            "allowed_for_signal": allowed,
            "cutoff_violation": violation,
            "exclusion_reason": reason,
        })
    return pd.DataFrame(rows, columns=MEMORY_COLUMNS)


def load_memory(path: Path = MEMORY_PATH) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=MEMORY_COLUMNS)
    try:
        df = pd.read_csv(path)
    except (pd.errors.EmptyDataError, OSError):
        return pd.DataFrame(columns=MEMORY_COLUMNS)
    return df.reindex(columns=MEMORY_COLUMNS)


def merge_memory(existing: pd.DataFrame, new: pd.DataFrame) -> pd.DataFrame:
    """既存storeへ新recordを追記。record_id 重複は既存(先着)を保持=過去の記録を書き換えない。

    さらに (link, text) 同一の記事も先着保持で重複除去する(published 更新・再配信対策。
    旧ID方式で登録済みの過去recordとの二重登録もこれで吸収する。レビュー指摘#3)。
    """
    merged = pd.concat([existing, new], ignore_index=True)
    merged = merged.drop_duplicates(subset=["record_id"], keep="first")
    merged = merged.drop_duplicates(subset=["link", "text"], keep="first").reset_index(drop=True)
    return merged.sort_values(["memory_date", "record_id"]).reset_index(drop=True)


def build_summary(memory: pd.DataFrame, added: int, generated_at) -> dict:
    allowed = as_bool_series(memory["allowed_for_signal"]) if not memory.empty else pd.Series(dtype=bool)
    violations = as_bool_series(memory["cutoff_violation"]) if not memory.empty else pd.Series(dtype=bool)
    allowed_violations = int((allowed & violations).sum()) if not memory.empty else 0
    summary = {
        "generated_at_jst": format_jst(generated_at),
        "generated_at_utc": format_utc(generated_at),
        "total_records": int(len(memory)),
        "records_added_this_run": int(added),
        "allowed_for_signal_count": int(allowed.sum()) if not memory.empty else 0,
        "excluded_count": int((~allowed).sum()) if not memory.empty else 0,
        "cutoff_violation_count": int(violations.sum()) if not memory.empty else 0,
        # allowed なのに cutoff違反 = あってはならない状態(機械的除外の破れ)。lookahead audit が監視。
        "allowed_with_violation_count": allowed_violations,
        "distinct_memory_days": int(memory["memory_date"].nunique()) if not memory.empty else 0,
    }
    summary.update(SAFETY_FIELDS)
    return summary


def run(headlines: pd.DataFrame | None = None, *, memory_path: Path = MEMORY_PATH) -> dict:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    memory_path.parent.mkdir(parents=True, exist_ok=True)
    generated_at = now_utc()

    if headlines is None:
        path = RESULTS_DIR / "news_headlines.csv"
        try:
            headlines = pd.read_csv(path) if path.exists() else pd.DataFrame()
        except (pd.errors.EmptyDataError, OSError):
            headlines = pd.DataFrame()

    new_records = build_records(headlines, pd.Timestamp(generated_at).tz_convert("UTC").tz_localize(None) if pd.Timestamp(generated_at).tzinfo else pd.Timestamp(generated_at))
    existing = load_memory(memory_path)
    before = len(existing)
    memory = merge_memory(existing, new_records)
    memory.to_csv(memory_path, index=False)

    summary = build_summary(memory, added=len(memory) - before, generated_at=generated_at)
    (RESULTS_DIR / "narrative_memory_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


def main() -> int:
    summary = run()
    print(
        f"narrative memory: total={summary['total_records']} (+{summary['records_added_this_run']}) "
        f"allowed={summary['allowed_for_signal_count']} violations={summary['cutoff_violation_count']} "
        f"days={summary['distinct_memory_days']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
