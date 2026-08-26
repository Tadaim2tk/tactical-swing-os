from __future__ import annotations

"""日次の市場コンテキストを point-in-time feature store として保存する (SPEC-JMCB-001)。

Phase 27.3-a。TSO 本体が毎朝算出している市場レベルの観測結果を、
「その時点で確定していた値」として恒久記録する。日本株スイング (Phase 27) など
後続の研究が、後知恵なしに当時の市場環境を参照できるようにするのが目的。

設計上の要点:
- **保存は多め、検証投入は少なめ**。10 スコアに加え主要資産の生の変化率・終値も保存する。
  後から「実は US10Y が効いていた」と分かっても、保存していなければ取り返せないため。
  どの変数をモデルに入れるかは 27.3-c の検証で決める(保存 != 採用)。
- **append-only**。既存行は決して書き換えない。1 run 1 行で、同一日に複数 run があれば
  複数行が並ぶ。消費側は `usable_from_utc` が判断時刻より前の最新行を選ぶ。
- **推測で埋めない**。資産が揃わなければ status=insufficient_data を出す(honest red)。
- 本スクリプトは値を保存するだけで、いかなる判断・重み・発注にも関与しない。
"""

from pathlib import Path
import os

import pandas as pd

try:
    import score_market_context
except Exception:  # noqa: BLE001 - snapshot は任意機能。import 失敗で日次サイクルを止めない
    score_market_context = None
from calibration_io import read_csv
from time_utils import format_jst, format_utc, now_utc


RESULTS_DIR = Path("results")
DATA_DIR = Path("data")
MARKET_CSV = RESULTS_DIR / "market_snapshot.csv"
# results/ は .gitignore 対象で永続しないため、後続研究が参照する台帳は data/ に置く
SNAPSHOT_CSV = DATA_DIR / "market_context_daily.csv"

KEY_ASSETS = ["BTC", "GOLD", "WTI", "USDJPY", "SPX", "NASDAQ", "DXY", "VIX", "US10Y"]
SCORE_COLUMNS = [
    "risk_on_score",
    "risk_off_score",
    "dollar_strength_score",
    "rate_pressure_score",
    "gold_safe_haven_score",
    "oil_supply_risk_proxy_score",
    "crypto_liquidity_score",
    "equity_momentum_score",
    "volatility_stress_score",
    "narrative_confidence",
]

# 資産が何件揃えば「揃った」とみなすか。9 資産中 7 件。
MIN_ASSETS_FOR_OK = 7
# 何日古いバーまで許容するか。通常の週末(金→日で 2 日)と 3 連休(3 日)は正常。
# 4 日以上離れていれば取得が止まっている可能性が高いので stale とする。
MAX_STALENESS_DAYS = 4

# 由来。27.3-a が日々生成する行と、27.3-b2 が過去アーティファクトから復元した行を
# 機械的に区別するための列。両者を混ぜて「全部 point-in-time」と扱わないための歯止め。
PROVENANCE_NATIVE = "native_point_in_time"
PROVENANCE_HISTORICAL = "historical_artifact_join"

META_COLUMNS = [
    "snapshot_id",
    "provenance",
    "context_date",
    "generated_at_utc",
    "generated_at_jst",
    "usable_from_utc",
    "source_run_id",
]
QUALITY_COLUMNS = [
    "input_assets_available",
    "input_assets_expected",
    "staleness_days",
    "oldest_asset_date",
    "max_asset_staleness_days",
    "asset_date_spread_days",
    "status",
    "status_reason",
]


def asset_columns() -> list[str]:
    """主要資産ごとの生の観測値。検証で使わなくても保存だけはしておく列。"""
    columns: list[str] = []
    for asset in KEY_ASSETS:
        columns.append(f"chg_pct_{asset}")
        columns.append(f"close_{asset}")
    return columns


SNAPSHOT_COLUMNS = META_COLUMNS + SCORE_COLUMNS + asset_columns() + QUALITY_COLUMNS


def _to_float(value) -> float | None:
    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number):
        return None
    return float(number)


def latest_rows_by_asset(market: pd.DataFrame) -> dict[str, dict]:
    """資産ごとに最新日付の行を1件だけ取り出す。status が ok でない行は採用しない。"""
    if market.empty or "asset" not in market.columns:
        return {}

    frame = market.copy()
    if "status" in frame.columns:
        frame = frame[frame["status"].astype(str).str.strip().str.lower() == "ok"]
    if frame.empty:
        return {}

    frame["_date"] = pd.to_datetime(frame.get("date"), errors="coerce")
    frame = frame.dropna(subset=["_date"])
    if frame.empty:
        return {}

    frame["_asset"] = frame["asset"].astype(str).str.strip().str.upper()
    frame = frame.sort_values("_date").drop_duplicates(subset=["_asset"], keep="last")

    out: dict[str, dict] = {}
    for _, row in frame.iterrows():
        out[str(row["_asset"])] = row.to_dict()
    return out


def asset_date_bounds(rows: dict[str, dict]) -> tuple[pd.Timestamp, pd.Timestamp] | None:
    """主要資産のバー日付の (最新, 最古)。

    資産ごとに配信の進みが違う(FX は米株より 1 日先、指数系は 1 日遅れることがある)ため、
    最新日だけを見ると「一部の資産だけ古い」状態が隠れる。鮮度判定には**最古**を使う。
    """
    dates = [row.get("_date") for asset, row in rows.items() if asset in KEY_ASSETS]
    dates = [d for d in dates if d is not None and not pd.isna(d)]
    if not dates:
        return None
    return max(dates), min(dates)


def classify_status(available: int, max_asset_staleness_days: int | None) -> tuple[str, str]:
    """鮮度判定は**最も古い資産**を基準にする(一部だけ古い状態を隠さないため)。"""
    if available < MIN_ASSETS_FOR_OK:
        return (
            "insufficient_data",
            f"主要資産 {available}/{len(KEY_ASSETS)} 件のみ取得(必要 {MIN_ASSETS_FOR_OK} 件)",
        )
    if max_asset_staleness_days is None:
        return "insufficient_data", "バー日付が判定できない"
    if max_asset_staleness_days >= MAX_STALENESS_DAYS:
        return (
            "stale",
            f"最も古い資産のバーが {max_asset_staleness_days} 日前(許容 {MAX_STALENESS_DAYS - 1} 日)",
        )
    return "ok", ""


def build_snapshot_row(market: pd.DataFrame, generated_dt=None) -> dict:
    """1 run 分のスナップショット行を組み立てる。データ不足でも例外で落ちない。"""
    generated_dt = generated_dt or now_utc()
    generated_utc = format_utc(generated_dt)

    row: dict = {column: "" for column in SNAPSHOT_COLUMNS}
    row["snapshot_id"] = "MCTX-" + generated_dt.strftime("%Y%m%dT%H%M%SZ")
    row["provenance"] = PROVENANCE_NATIVE
    row["generated_at_utc"] = generated_utc
    row["generated_at_jst"] = format_jst(generated_dt)
    # 判断に使ってよい最早時刻。この時刻より前の判断がこの行を参照したら lookahead。
    row["usable_from_utc"] = generated_utc
    row["source_run_id"] = os.environ.get("GITHUB_RUN_ID", "local")
    row["input_assets_expected"] = len(KEY_ASSETS)

    rows_by_asset = latest_rows_by_asset(market)
    available_assets = [asset for asset in KEY_ASSETS if asset in rows_by_asset]
    row["input_assets_available"] = len(available_assets)

    bounds = asset_date_bounds(rows_by_asset)
    max_asset_staleness_days: int | None = None
    if bounds is not None:
        newest, oldest = bounds
        row["context_date"] = newest.date().isoformat()
        row["oldest_asset_date"] = oldest.date().isoformat()
        # staleness_days は最新バー基準(この行が「いつの市場」を描いているか)
        row["staleness_days"] = (generated_dt.date() - newest.date()).days
        # 鮮度判定に使うのは最古バー基準。一部の資産だけ古い状態を隠さない
        max_asset_staleness_days = (generated_dt.date() - oldest.date()).days
        row["max_asset_staleness_days"] = max_asset_staleness_days
        row["asset_date_spread_days"] = (newest.date() - oldest.date()).days

    for asset in KEY_ASSETS:
        source = rows_by_asset.get(asset)
        if not source:
            continue
        close = _to_float(source.get("close"))
        open_ = _to_float(source.get("open"))
        if close is not None:
            row[f"close_{asset}"] = round(close, 6)
        if close is not None and open_ not in (None, 0):
            row[f"chg_pct_{asset}"] = round((close - open_) / open_ * 100.0, 6)

    status, reason = classify_status(len(available_assets), max_asset_staleness_days)
    row["status"] = status
    row["status_reason"] = reason

    # スコアは status に関わらず算出できる分だけ入れる。
    # 不足時は narrative_confidence が自動的に下がるので、消費側は status と併せて判断する。
    if score_market_context is not None and not market.empty:
        scores = score_market_context.score_market_narratives(market)
        if not scores.empty:
            global_row = scores.iloc[0]
            for column in SCORE_COLUMNS:
                value = _to_float(global_row.get(column))
                if value is not None:
                    row[column] = value

    return row


def load_existing() -> pd.DataFrame:
    """台帳を**ヘッダの大文字小文字を保存したまま**読む。

    calibration_io.read_csv は normalize_headers で全ヘッダを小文字化するため、
    契約列 close_BTC が close_btc として読まれ、(1) 旧実装では concat の列和集合で
    大小両ケースが併存する自己増殖(2026-08-25事故の真の発生機構)、(2) #118 の
    schema enforcement では契約列18本が「契約外」と誤認され追記が恒久失敗する
    (Codex事後レビューP1)。ここは生の pandas で大文字小文字を保存して読む。
    """
    if not SNAPSHOT_CSV.exists():
        return pd.DataFrame(columns=SNAPSHOT_COLUMNS)
    try:
        existing = pd.read_csv(SNAPSHOT_CSV, dtype=str, keep_default_na=False)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=SNAPSHOT_COLUMNS)
    if existing.empty and len(existing.columns) == 0:
        return pd.DataFrame(columns=SNAPSHOT_COLUMNS)
    return existing


def append_snapshot(row: dict, existing: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
    """append-only。同一 generated_at_utc が既にあれば何もしない(再実行の冪等性)。

    schema enforcement: 既存ファイルに SNAPSHOT_COLUMNS 外の列があれば例外で落とす。
    黙って温存すると concat の列和集合が自己増殖し、「新行は大文字列だけ・旧行は
    小文字列だけが埋まる」片側欠損が毎日1行ずつ増える(2026-08-25 の close_btc/close_BTC
    事故)。列を変えたいときは明示的な移行コミットで先にヘッダを契約へ一致させること
    (行の append-only と列の schema enforcement は別の不変条件)。
    """
    unknown = [c for c in existing.columns if c not in SNAPSHOT_COLUMNS]
    if unknown:
        raise ValueError(
            "market_context_daily.csv に契約外の列: "
            + ", ".join(sorted(unknown))
            + " — 追記を拒否。明示的な移行コミットで列を SNAPSHOT_COLUMNS に一致させてから再実行"
        )

    if not existing.empty and "generated_at_utc" in existing.columns:
        already = existing["generated_at_utc"].astype(str) == str(row["generated_at_utc"])
        if bool(already.any()):
            return existing, False

    combined = pd.concat([existing, pd.DataFrame([row])], ignore_index=True)
    for column in SNAPSHOT_COLUMNS:
        if column not in combined.columns:
            combined[column] = ""
    return combined[list(SNAPSHOT_COLUMNS)], True


def export_snapshot() -> pd.DataFrame:
    market = read_csv(MARKET_CSV)
    row = build_snapshot_row(market)
    existing = load_existing()
    combined, appended = append_snapshot(row, existing)

    if not appended:
        print(f"snapshot {row['snapshot_id']} already recorded; nothing to append")
        return existing

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    combined.to_csv(SNAPSHOT_CSV, index=False)
    print(
        f"recorded {row['snapshot_id']} status={row['status']} "
        f"assets={row['input_assets_available']}/{len(KEY_ASSETS)} "
        f"context_date={row['context_date'] or 'unknown'}"
    )
    if row["status_reason"]:
        print(f"  reason: {row['status_reason']}")
    return combined


def main() -> None:
    export_snapshot()


if __name__ == "__main__":
    main()
