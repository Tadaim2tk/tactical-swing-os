from __future__ import annotations

"""過去の GitHub Actions アーティファクトから point-in-time 市場コンテキストを復元する
(Phase 27.3-b2 / SPEC-JMCB-001)。

旧 earnings-research-os の日本株決算研究 254 件に、**当時保存されていた** TSO の
market_snapshot を結合するための土台。

固定された4条件:
1. どのアーティファクト / run / snapshot を使ったか provenance を全件に残す
2. 「寄り前の最新」という結合規則を機械的に保証する(usable_from < 判断時刻)
3. 週末などで最大3日空いたケースも除外しない。**当時利用可能だった最新記録**として扱う
4. ここで生成する行(historical_artifact_join)と、27.3-a が日々生成する行
   (native_point_in_time)を provenance 列で区別する

**再構成はしない。** 当時の記録が無い日は unavailable とし、現在の価格から
後付けで市場コンテキストを作らない(それは lookahead 汚染になる)。
"""

import argparse
import csv
import datetime as dt
import re
from pathlib import Path

import pandas as pd

import export_market_context_snapshot as mcs
from calibration_io import read_csv


DATA_DIR = Path("data")
HISTORICAL_CSV = DATA_DIR / "market_context_historical.csv"
LINK_CSV = DATA_DIR / "ers_legacy_context_link.csv"

JST = dt.timezone(dt.timedelta(hours=9))
# 東証の寄り付き。日本株の判断はこの時点までに確定している必要がある。
MARKET_OPEN_JST = dt.time(9, 0)

PROVENANCE_COLUMNS = [
    "source_artifact_id",
    "source_artifact_name",
    "artifact_created_at_utc",
    "source_market_run_ts_utc",
]
HISTORICAL_COLUMNS = mcs.SNAPSHOT_COLUMNS + PROVENANCE_COLUMNS

LINK_COLUMNS = [
    "ers_code",
    "ers_name",
    "ers_date",
    "ers_quarter",
    "decision_cutoff_utc",
    "join_status",
    "snapshot_id",
    "provenance",
    "snapshot_usable_from_utc",
    "snapshot_generated_at_utc",
    "lag_hours",
    "snapshot_status",
    "snapshot_max_asset_staleness_days",
    "source_artifact_id",
    "source_run_id",
]


def parse_utc(value) -> dt.datetime | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip()
    if not text:
        return None
    text = text.replace("Z", "+00:00").replace(" UTC", "+00:00")
    try:
        parsed = dt.datetime.fromisoformat(text)
    except ValueError:
        parsed = pd.to_datetime(text, errors="coerce", utc=True)
        if pd.isna(parsed):
            return None
        return parsed.to_pydatetime()
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def run_id_from_artifact_name(name: str) -> str:
    match = re.search(r"(\d+)$", str(name))
    return match.group(1) if match else ""


def market_run_ts(market: pd.DataFrame) -> dt.datetime | None:
    """market_snapshot.csv の run_ts = 実際にその値が算出された時刻。"""
    if market.empty or "run_ts" not in market.columns:
        return None
    values = [parse_utc(v) for v in market["run_ts"].tolist()]
    values = [v for v in values if v is not None]
    return min(values) if values else None


def snapshot_row_from_artifact(
    market: pd.DataFrame,
    artifact_id: str,
    artifact_name: str,
    artifact_created_at: dt.datetime,
) -> dict | None:
    """1アーティファクト分の市場コンテキスト行を復元する。

    - `generated_at` は market_snapshot.csv の run_ts(実際に算出された時刻)
    - `usable_from_utc` は**アーティファクトの作成時刻**。run_ts より後で、
      「その値が確実に手元にあった時刻」として保守側に倒す
    """
    run_ts = market_run_ts(market)
    if run_ts is None:
        return None

    row = mcs.build_snapshot_row(market, generated_dt=run_ts)
    row["provenance"] = mcs.PROVENANCE_HISTORICAL
    row["source_run_id"] = run_id_from_artifact_name(artifact_name)
    # 保守側: 算出時刻ではなくアーティファクト確定時刻を「使ってよい最早時刻」とする
    usable_from = max(run_ts, artifact_created_at)
    row["usable_from_utc"] = mcs.format_utc(usable_from)
    row["source_artifact_id"] = str(artifact_id)
    row["source_artifact_name"] = str(artifact_name)
    row["artifact_created_at_utc"] = mcs.format_utc(artifact_created_at)
    row["source_market_run_ts_utc"] = mcs.format_utc(run_ts)
    return row


def build_historical_ledger(entries: list[dict]) -> pd.DataFrame:
    """entries: [{artifact_id, artifact_name, created_at, market_csv(DataFrame)}]"""
    rows = []
    for entry in entries:
        row = snapshot_row_from_artifact(
            entry["market"], entry["artifact_id"], entry["artifact_name"], entry["created_at"]
        )
        if row is not None:
            rows.append(row)
    if not rows:
        return pd.DataFrame(columns=HISTORICAL_COLUMNS)
    frame = pd.DataFrame(rows)
    for column in HISTORICAL_COLUMNS:
        if column not in frame.columns:
            frame[column] = ""
    frame = frame[HISTORICAL_COLUMNS]
    frame["_usable"] = frame["usable_from_utc"].map(parse_utc)
    frame = frame.sort_values("_usable").drop(columns=["_usable"]).reset_index(drop=True)
    return frame


def decision_cutoff_utc(decision_date: dt.date) -> dt.datetime:
    """判断の締切 = その日の東証寄り付き(09:00 JST)。"""
    return dt.datetime.combine(decision_date, MARKET_OPEN_JST, JST).astimezone(dt.timezone.utc)


def latest_usable_snapshot(ledger: pd.DataFrame, cutoff: dt.datetime) -> dict | None:
    """結合規則: usable_from_utc が判断時刻より**厳密に前**の最新1行のみ。

    週末などで数日空いても除外しない。当時利用可能だった最新の記録がそれだから。
    lag は記録するので、消費側が必要なら自分で絞り込める。
    """
    if ledger.empty:
        return None
    best = None
    best_usable = None
    for _, row in ledger.iterrows():
        usable = parse_utc(row.get("usable_from_utc"))
        if usable is None or not (usable < cutoff):
            continue
        if best_usable is None or usable > best_usable:
            best, best_usable = row.to_dict(), usable
    return best


def link_records(records: list[dict], ledger: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for record in records:
        raw_date = str(record.get("date", "")).strip()
        base = {column: "" for column in LINK_COLUMNS}
        base["ers_code"] = record.get("code", "")
        base["ers_name"] = record.get("name", "")
        base["ers_date"] = raw_date
        base["ers_quarter"] = record.get("quarter", "")

        try:
            decision_date = dt.date.fromisoformat(raw_date)
        except ValueError:
            base["join_status"] = "unavailable"
            base["provenance"] = ""
            rows.append(base)
            continue

        cutoff = decision_cutoff_utc(decision_date)
        base["decision_cutoff_utc"] = mcs.format_utc(cutoff)
        match = latest_usable_snapshot(ledger, cutoff)
        if match is None:
            # 当時の記録が無い日は再構成しない
            base["join_status"] = "unavailable"
            rows.append(base)
            continue

        usable = parse_utc(match.get("usable_from_utc"))
        base["join_status"] = "ok"
        base["snapshot_id"] = match.get("snapshot_id", "")
        base["provenance"] = match.get("provenance", "")
        base["snapshot_usable_from_utc"] = match.get("usable_from_utc", "")
        base["snapshot_generated_at_utc"] = match.get("generated_at_utc", "")
        base["lag_hours"] = round((cutoff - usable).total_seconds() / 3600.0, 2)
        base["snapshot_status"] = match.get("status", "")
        base["snapshot_max_asset_staleness_days"] = match.get("max_asset_staleness_days", "")
        base["source_artifact_id"] = match.get("source_artifact_id", "")
        base["source_run_id"] = match.get("source_run_id", "")
        rows.append(base)
    return pd.DataFrame(rows, columns=LINK_COLUMNS)


def load_artifact_entries(artifacts_dir: Path, index_tsv: Path) -> list[dict]:
    """index_tsv: artifact_id \t name \t created_at \t size"""
    entries = []
    for line in index_tsv.read_text().splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        artifact_id, name, created = parts[0], parts[1], parts[2]
        market_csv = artifacts_dir / artifact_id / "results" / "market_snapshot.csv"
        if not market_csv.exists():
            continue
        created_at = parse_utc(created)
        if created_at is None:
            continue
        entries.append(
            {
                "artifact_id": artifact_id,
                "artifact_name": name,
                "created_at": created_at,
                "market": read_csv(market_csv),
            }
        )
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts-dir", required=True, type=Path)
    parser.add_argument("--artifact-index", required=True, type=Path)
    parser.add_argument("--records", required=True, type=Path, help="旧ERS data/records.csv")
    args = parser.parse_args()

    entries = load_artifact_entries(args.artifacts_dir, args.artifact_index)
    ledger = build_historical_ledger(entries)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ledger.to_csv(HISTORICAL_CSV, index=False)
    print(f"historical ledger: {len(ledger)} rows -> {HISTORICAL_CSV}")

    with args.records.open(newline="") as handle:
        records = list(csv.DictReader(handle))
    link = link_records(records, ledger)
    link.to_csv(LINK_CSV, index=False)

    ok = int((link["join_status"] == "ok").sum())
    print(f"link: {ok}/{len(link)} joined -> {LINK_CSV}")
    if ok:
        lags = pd.to_numeric(link.loc[link["join_status"] == "ok", "lag_hours"], errors="coerce")
        print(f"  lag_hours median={lags.median():.1f} max={lags.max():.1f}")
        print(f"  snapshot_status: {link.loc[link['join_status']=='ok','snapshot_status'].value_counts().to_dict()}")


if __name__ == "__main__":
    main()
