"""Prediction log retro-scorer (Phase 29.6) — 手動予測台帳の「全判断」を遡及採点する。

背景（2026-07-09 人間指示）: プロジェクトの原則は「全ての判断を記録し、後日採点し、
どの条件が有効だったか検証する」。しかし ChatGPT との日次対話で生まれる予測台帳
data/signal_log.csv は記録されるだけで採点されておらず、B級・NO_TRADE の判断が
学習サンプルとして蓄積されない状態だった（=保守側デフォルトによるサンプル廃棄）。

本スクリプトは台帳の**全行**（A/B/NO_TRADE、side NONE 含む）を実価格で採点する:

- 全行共通: 判断日アンカーから +1/3/5/10 営業日の実リターン（「その後何が起きたか」を
  ランクに関わらず記録 → 見送り判断の質も後日検証可能にする）
- actionable 行（BUY/SELL + entry/SL 記録あり）: 当時の記録値による方向つき close-R
  （PROTO-0001 と同じ反後知恵原則: reference/risk は記録値のみ・推定しない）と
  entry ゾーン充足の有無、+5/+10営業日の success/failure
- 結果窓が未確定の行は awaiting の正直表示（再実行で自動更新・重複しない）

これは results/ 側のライブ評価ループ（generate_signal→evaluate_signal）とは独立した
読み取り専用の採点レイヤーであり、台帳をライブループの真実源にはしない。
signal score には未接続。実売買なし。
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from retrieve_similar_narratives import RAW_DIR
from time_utils import format_jst, format_utc, now_utc

LEDGER_PATH = Path("data/signal_log.csv")
SCORES_PATH = Path("data/prediction_log_scores.csv")
RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/prediction_log")

HORIZONS = [1, 3, 5, 10]
MIN_SAMPLES = 30  # 集計判断の敷居(SPEC-SG-001と整合)。件数はそれ未満でも正直に表示する
MAX_REFERENCE_ANCHOR_DEVIATION = 0.10  # reference が anchor からこれ以上離れたら scale_mismatch 隔離

SCORE_COLUMNS = [
    "date",
    "signal_id",
    "asset",
    "side",            # 正規化後 (LONG/SHORT/NONE)
    "rank",
    "actionable",
    "reference_price",
    "risk_unit",
    "anchor_close",
    "fwd_return_1d", "fwd_return_3d", "fwd_return_5d", "fwd_return_10d",
    "r_close_1d", "r_close_3d", "r_close_5d", "r_close_10d",
    "entry_touched_5d",
    "data_quality",     # ok / scale_mismatch(記録水準と価格系列の桁不一致) / extreme_r
    "result_5d",       # success / failure / not_applicable / awaiting
    "result_10d",
    "status",          # scored / awaiting_horizon / invalid_data
    "verified_status",
    "scored_at_utc",
]

SAFETY_FIELDS = {
    "requires_human_approval": True,
    "weights_json_updated": False,
    "generate_signal_updated": False,
    "connected_to_signal_score": False,
}


def normalize_side(value) -> str:
    s = str(value or "").strip().upper()
    return {"BUY": "LONG", "SELL": "SHORT", "LONG": "LONG", "SHORT": "SHORT"}.get(s, "NONE")


def _num(value) -> float:
    v = pd.to_numeric(value, errors="coerce")
    return float(v) if pd.notna(v) else float("nan")


def load_ohlcv_frame(asset: str, raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    path = raw_dir / f"{asset}.csv"
    if not path.exists():
        return pd.DataFrame()
    try:
        df = pd.read_csv(path)
    except (pd.errors.EmptyDataError, OSError):
        return pd.DataFrame()
    df.columns = [str(c).strip().lower() for c in df.columns]
    if "date" not in df.columns or "close" not in df.columns:
        return pd.DataFrame()
    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True).dt.tz_localize(None).dt.normalize()
    for c in ["open", "high", "low", "close"]:
        if c not in df.columns:
            df[c] = np.nan
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.dropna(subset=["date", "close"]).sort_values("date").reset_index(drop=True)


def score_row(row: pd.Series, ohlcv: pd.DataFrame, scored_at: str) -> dict:
    """台帳1行を採点する（純関数）。反後知恵: reference/risk は記録値のみ。"""
    side = normalize_side(row.get("side"))
    entry_low, entry_high, sl = _num(row.get("entry_low")), _num(row.get("entry_high")), _num(row.get("sl"))
    reference = (entry_low + entry_high) / 2 if (entry_low > 0 and entry_high > 0) else float("nan")
    risk = abs(reference - sl) if (not np.isnan(reference) and sl > 0) else float("nan")
    actionable = side in {"LONG", "SHORT"} and not np.isnan(reference) and not np.isnan(risk) and risk > 0

    out = {
        "date": str(row.get("date") or ""),
        "signal_id": str(row.get("signal_id") or ""),
        "asset": str(row.get("asset") or ""),
        "side": side,
        "rank": str(row.get("rank") or ""),
        "actionable": actionable,
        "reference_price": round(reference, 6) if not np.isnan(reference) else np.nan,
        "risk_unit": round(risk, 6) if not np.isnan(risk) else np.nan,
        "anchor_close": np.nan,
        **{f"fwd_return_{h}d": np.nan for h in HORIZONS},
        **{f"r_close_{h}d": np.nan for h in HORIZONS},
        "entry_touched_5d": False,
        "data_quality": "ok",
        "result_5d": "not_applicable",
        "result_10d": "not_applicable",
        "status": "invalid_data",
        "verified_status": str(row.get("verified_status") or ""),
        "scored_at_utc": scored_at,
    }

    signal_date = pd.to_datetime(str(row.get("date") or ""), errors="coerce")
    if ohlcv.empty or pd.isna(signal_date):
        return out
    idx = int(ohlcv["date"].searchsorted(signal_date.normalize(), side="right")) - 1
    if idx < 0:
        return out
    anchor_close = float(ohlcv.iloc[idx]["close"])
    out["anchor_close"] = round(anchor_close, 6)

    # データ品質ガード(反後知恵: 補正はしない・採点から正直に外すだけ):
    # 記録水準が価格系列と不一致 -> 方向Rは計算不能。桁違い(例: QQQ 700台を
    # NASDAQ=NQ先物に記録, x0.02)だけでなく、同族指数の混同(例: NASDAQ総合
    # 26,000台をNQ先物29,000台に記録, x0.88)も (close-reference)/risk が
    # 偽の数R〜数十Rを生むため、anchor から ±10% 超の reference は隔離する。
    # 日次スイングの entry ゾーンが当日終値から10%超離れることは想定しない。
    if actionable and not np.isnan(reference) and anchor_close > 0:
        ratio = reference / anchor_close
        if abs(ratio - 1.0) > MAX_REFERENCE_ANCHOR_DEVIATION:
            out["data_quality"] = "scale_mismatch"
            actionable = False
            out["actionable"] = False
            out["result_5d"] = out["result_10d"] = "suspect_data"

    direction = 1.0 if side == "LONG" else -1.0 if side == "SHORT" else 0.0
    incomplete = False
    for h in HORIZONS:
        j = idx + h
        if j >= len(ohlcv):
            incomplete = True
            continue
        close_h = float(ohlcv.iloc[j]["close"])
        out[f"fwd_return_{h}d"] = round(close_h / anchor_close - 1.0, 6)
        if actionable:
            out[f"r_close_{h}d"] = round(direction * (close_h - reference) / risk, 4)

    if actionable and any(pd.notna(out[f"r_close_{h}d"]) and abs(out[f"r_close_{h}d"]) > 50 for h in HORIZONS):
        out["data_quality"] = "extreme_r"
        out["result_5d"] = out["result_10d"] = "suspect_data"
        for h in HORIZONS:
            out[f"r_close_{h}d"] = np.nan
        actionable = False
        out["actionable"] = False

    if actionable:
        window5 = ohlcv.iloc[idx + 1: idx + 6]
        if not window5.empty:
            touched = ((window5["low"] <= entry_high) & (window5["high"] >= entry_low)).any()
            out["entry_touched_5d"] = bool(touched)
        for h, key in [(5, "result_5d"), (10, "result_10d")]:
            r = out[f"r_close_{h}d"]
            out[key] = "awaiting" if pd.isna(r) else ("success" if r > 0 else "failure")

    out["status"] = "awaiting_horizon" if incomplete else "scored"
    return out


def score_ledger(ledger: pd.DataFrame, *, raw_dir: Path = RAW_DIR, scored_at: str = "") -> pd.DataFrame:
    if ledger.empty:
        return pd.DataFrame(columns=SCORE_COLUMNS)
    cache: dict[str, pd.DataFrame] = {}
    rows = []
    for _, row in ledger.iterrows():
        asset = str(row.get("asset") or "")
        if asset not in cache:
            cache[asset] = load_ohlcv_frame(asset, raw_dir)
        rows.append(score_row(row, cache[asset], scored_at))
    return pd.DataFrame(rows, columns=SCORE_COLUMNS)


def append_scores(new_scores: pd.DataFrame, path: Path = SCORES_PATH) -> pd.DataFrame:
    """signal_id で重複排除(最新優先=awaiting→確定の更新)して保存。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            existing = pd.read_csv(path)
        except (pd.errors.EmptyDataError, OSError):
            existing = pd.DataFrame(columns=SCORE_COLUMNS)
    else:
        existing = pd.DataFrame(columns=SCORE_COLUMNS)
    merged = pd.concat([existing, new_scores], ignore_index=True)
    merged = merged.drop_duplicates(subset=["signal_id"], keep="last")
    merged = merged.reindex(columns=SCORE_COLUMNS).sort_values(["date", "signal_id"]).reset_index(drop=True)
    merged = _preserve_unchanged_score_timestamps(merged, existing)
    merged.to_csv(path, index=False)
    return merged


def _score_value_key(value) -> str:
    if pd.isna(value):
        return ""
    s = str(value).strip()
    return "" if s.lower() in {"nan", "none"} else s


def _preserve_unchanged_score_timestamps(merged: pd.DataFrame, existing: pd.DataFrame) -> pd.DataFrame:
    """採点内容が同じ行は既存の scored_at_utc を保持し、時刻だけのCSV churnを避ける。"""
    if existing.empty or "signal_id" not in existing.columns or "scored_at_utc" not in existing.columns:
        return merged
    existing_latest = existing.drop_duplicates(subset=["signal_id"], keep="last").set_index("signal_id", drop=False)
    compare_cols = [c for c in SCORE_COLUMNS if c != "scored_at_utc"]
    out = merged.copy()
    for idx, row in out.iterrows():
        sid = str(row.get("signal_id") or "")
        if not sid or sid not in existing_latest.index:
            continue
        old = existing_latest.loc[sid]
        unchanged = all(_score_value_key(row.get(c)) == _score_value_key(old.get(c)) for c in compare_cols)
        if unchanged:
            out.at[idx, "scored_at_utc"] = old.get("scored_at_utc", "")
    return out


def summarize(scores: pd.DataFrame) -> dict:
    def rate(sub: pd.DataFrame, col: str):
        closed = sub[sub[col].isin(["success", "failure"])]
        n = int(len(closed))
        wins = int((closed[col] == "success").sum())
        return {
            "n_closed": n,
            "wins": wins,
            "win_rate": round(wins / n, 4) if n else None,
            "statistical_basis": "ok" if n >= MIN_SAMPLES else "insufficient_data",
        }

    by_rank = {}
    for rank, sub in scores.groupby("rank"):
        act = sub[sub["actionable"] == True]  # noqa: E712 - CSV round-trip後も許容
        r5 = pd.to_numeric(act["r_close_5d"], errors="coerce").dropna()
        by_rank[str(rank)] = {
            "rows": int(len(sub)),
            "actionable_rows": int(len(act)),
            "result_5d": rate(act, "result_5d"),
            "result_10d": rate(act, "result_10d"),
            "mean_r_close_5d": round(float(r5.mean()), 4) if len(r5) else None,
        }
    return {
        "total_rows": int(len(scores)),
        "actionable_rows": int((scores["actionable"] == True).sum()),  # noqa: E712
        "awaiting_rows": int((scores["status"] == "awaiting_horizon").sum()),
        "invalid_rows": int((scores["status"] == "invalid_data").sum()),
        "suspect_data_rows": int((scores["data_quality"] != "ok").sum()) if "data_quality" in scores.columns else 0,
        "by_rank": by_rank,
        "min_samples_for_judgement": MIN_SAMPLES,
    }


def render_report(summary_all: dict, scores: pd.DataFrame, generated_at_jst: str) -> str:
    lines = [
        "| date | signal_id | asset | side | rank | +5営業日R | +10営業日R | 5d | 10d | entry充足 | status |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for _, r in scores.sort_values(["date", "signal_id"]).iterrows():
        def f(v):
            return format(v, ".2f") if pd.notna(v) else "—"
        lines.append(
            f"| {r['date']} | {r['signal_id']} | {r['asset']} | {r['side']} | {r['rank']} "
            f"| {f(r['r_close_5d'])} | {f(r['r_close_10d'])} | {r['result_5d']} | {r['result_10d']} "
            f"| {'Y' if r['entry_touched_5d'] else '—'} | {r['status']} |"
        )
    rank_lines = ["| rank | 行数 | actionable | 5d勝率 | 10d勝率 | 平均R(5d) | 統計的根拠 |",
                  "| --- | --- | --- | --- | --- | --- | --- |"]
    for rank, s in sorted(summary_all["by_rank"].items()):
        r5, r10 = s["result_5d"], s["result_10d"]
        def pct(x):
            return f"{x['win_rate']:.0%} ({x['wins']}/{x['n_closed']})" if x["win_rate"] is not None else "—"
        rank_lines.append(
            f"| {rank} | {s['rows']} | {s['actionable_rows']} | {pct(r5)} | {pct(r10)} "
            f"| {s['mean_r_close_5d'] if s['mean_r_close_5d'] is not None else '—'} | {r5['statistical_basis']} |"
        )
    return f"""# Prediction Log 遡及採点（全判断の後日検証 / Phase 29.6）

- 生成日時JST: {generated_at_jst}
- 対象: data/signal_log.csv の**全行**（A/B/NO_TRADE・side NONE 含む）
- 原則: 全ての判断を記録し採点する（見送りも学習サンプル）。reference/risk は判断時の記録値のみ（反後知恵）。

## 1. ランク別集計

{chr(10).join(rank_lines)}

- n<{MIN_SAMPLES} は insufficient_data（件数と勝敗は正直に表示するが、優位性の判断材料にはまだしない）。
- side NONE / NO_TRADE 行は方向Rを持たない（not_applicable）が、+1/3/5/10営業日の実リターンは
  data/prediction_log_scores.csv に記録済み — 「見送った後に何が起きたか」を後日検証できる。

## 2. 全行の採点

{chr(10).join(lines)}

## 3. 注意

- close ベースの R（PROTO-0001 と同じ定義）。SLキャップ後のトレードP&Lとは別物。
- awaiting は結果窓未確定の正直表示。日次再実行で自動確定する。
- 採点のみで signal score・実売買には未接続。
"""


def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    generated_at = now_utc()

    try:
        ledger = pd.read_csv(LEDGER_PATH) if LEDGER_PATH.exists() else pd.DataFrame()
    except (pd.errors.EmptyDataError, OSError):
        ledger = pd.DataFrame()

    scores_new = score_ledger(ledger, scored_at=format_utc(generated_at))
    scores = append_scores(scores_new) if not scores_new.empty else append_scores(pd.DataFrame(columns=SCORE_COLUMNS))

    summary = {
        "generated_at_jst": format_jst(generated_at),
        "generated_at_utc": format_utc(generated_at),
        **summarize(scores),
    }
    summary.update(SAFETY_FIELDS)
    (RESULTS_DIR / "prediction_log_score_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (REPORTS_DIR / f"{format_jst(generated_at)[:10]}_prediction_log_scores.md").write_text(
        render_report(summary, scores, format_jst(generated_at)), encoding="utf-8"
    )
    print(
        f"prediction log scores: total={summary['total_rows']} actionable={summary['actionable_rows']} "
        f"awaiting={summary['awaiting_rows']} invalid={summary['invalid_rows']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
