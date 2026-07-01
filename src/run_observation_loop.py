"""Minimal observation loop (Phase 29.4) — 観測→事前ナラティブ→評価→類似検索→教訓 を1周回す。

PROTO-0001 (Obsidian vault: TSO A Rank Expected R) の定義に従う:
- 適格イベント: A-rank かつ CBS >= 80 かつ EMS >= 70
- ホライズン: 5営業日（+10営業日は補足情報）
- R は「当時記録された reference price / risk unit」で計算（反後知恵: 後から修復しない）
- 元記録に必要データが無ければ invalid_data（推定で埋めない）

適格イベントが無い間も、直近の A-rank 候補で **non_qualifying_dry_run** として
ループの機械を実際に回す（プロトコル台帳は汚さない）。ループを回すこと自体が
運用上の穴を見つける手段であり、実装はデータを待たない。

出力（git追跡・恒久記録）:
- data/observation_log.csv          … 1イベント1行の台帳（event_id で重複排除）
- data/observations/OBS-*.md        … 観測レコード全文（教訓セクション付き）
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from build_narrative_memory import MEMORY_PATH, load_memory
from retrieve_similar_narratives import RAW_DIR, build_day_documents, load_close_series, retrieve
from time_utils import format_jst, format_utc, now_utc

LEDGER_PATH = Path("data/signal_log.csv")
OBS_LOG_PATH = Path("data/observation_log.csv")
OBS_DIR = Path("data/observations")
RESULTS_DIR = Path("results")

PROTOCOL_ID = "PROTO-0001"
QUALIFY_CBS = 80.0
QUALIFY_EMS = 70.0
HORIZON_PRIMARY = 5
HORIZON_SECONDARY = 10

OBS_COLUMNS = [
    "event_id",
    "protocol_id",
    "run_type",            # qualifying / non_qualifying_dry_run
    "signal_id",
    "a_rank_date",
    "asset",
    "side",
    "cbs",
    "ems",
    "reference_price",
    "risk_unit",
    "review_due",
    "outcome_price_5d",
    "realized_r_5d",
    "outcome_price_10d",
    "realized_r_10d",
    "result",              # success / failure / invalid_data / pending
    "similar_cases_status",
    "narrative_memory_asof_days",
    "lesson_file",
    "recorded_at_utc",
    "notes",
]

SAFETY_FIELDS = {
    "requires_human_approval": True,
    "weights_json_updated": False,
    "generate_signal_updated": False,
    "connected_to_signal_score": False,
}


def _num(value) -> float:
    v = pd.to_numeric(value, errors="coerce")
    return float(v) if pd.notna(v) else float("nan")


def select_candidate(ledger: pd.DataFrame, signal_id: str | None = None) -> tuple[pd.Series | None, str]:
    """観測対象を選ぶ。適格イベント優先、無ければ直近A-rankで dry-run。"""
    if ledger.empty or "rank" not in ledger.columns:
        return None, "no_candidate"
    a_ranks = ledger[ledger["rank"].astype(str).str.upper() == "A"].copy()
    if signal_id:
        a_ranks = a_ranks[a_ranks["signal_id"].astype(str) == signal_id]
    if a_ranks.empty:
        return None, "no_candidate"
    a_ranks["_cbs"] = pd.to_numeric(a_ranks.get("cbs"), errors="coerce")
    a_ranks["_ems"] = pd.to_numeric(a_ranks.get("ems"), errors="coerce")
    a_ranks = a_ranks.sort_values("date")
    qualifying = a_ranks[(a_ranks["_cbs"] >= QUALIFY_CBS) & (a_ranks["_ems"] >= QUALIFY_EMS)]
    if not qualifying.empty:
        return qualifying.iloc[-1], "qualifying"
    return a_ranks.iloc[-1], "non_qualifying_dry_run"


def pre_narrative_record(row: pd.Series, memory: pd.DataFrame) -> dict:
    """事前ナラティブ = 判断時に記録済みのフィールドのみ（反後知恵: 後から足さない）。

    + 当時 as-of で参照できた narrative memory の局面日数（無ければ正直に0）。
    """
    a_date = str(row.get("date", ""))
    day_docs = build_day_documents(memory)
    asof_days = int((day_docs["memory_date"] <= a_date).sum()) if not day_docs.empty else 0
    return {
        "regime": row.get("regime"),
        "signal_type": row.get("type"),
        "invalidation": row.get("invalidation"),
        "verification_target": row.get("verification_target"),
        "win_prob": row.get("win_prob"),
        "expected_r": row.get("expected_r"),
        "tq_score": row.get("tq_score"),
        "scores": {k: row.get(k) for k in ["ems", "ffs", "cds", "ias", "cbs", "mes"]},
        "narrative_memory_asof_days": asof_days,
        "narrative_memory_status": "available" if asof_days > 0 else "no_memory_asof",
    }


def evaluate_outcome(row: pd.Series, closes: pd.Series) -> dict:
    """PROTO-0001 の評価: 当時の reference price / risk unit で +5/+10営業日 R を計算。"""
    entry_low, entry_high, sl = _num(row.get("entry_low")), _num(row.get("entry_high")), _num(row.get("sl"))
    side = str(row.get("side", "")).upper()
    out = {
        "reference_price": np.nan, "risk_unit": np.nan, "review_due": "",
        "outcome_price_5d": np.nan, "realized_r_5d": np.nan,
        "outcome_price_10d": np.nan, "realized_r_10d": np.nan,
        "result": "invalid_data",
    }
    # 反後知恵: 元記録に entry/sl が無ければ invalid_data（推定で埋めない）
    if any(np.isnan(v) for v in [entry_low, entry_high, sl]) or side not in {"LONG", "SHORT"}:
        return out
    reference = (entry_low + entry_high) / 2
    risk = abs(reference - sl)
    out["reference_price"] = round(reference, 6)
    out["risk_unit"] = round(risk, 6)
    if risk <= 0:
        return out
    if closes.empty:
        out["result"] = "invalid_data"
        return out
    a_date = pd.Timestamp(str(row.get("date")))
    idx = int(closes.index.searchsorted(a_date, side="right")) - 1
    if idx < 0:
        return out
    direction = 1.0 if side == "LONG" else -1.0

    def r_at(h: int) -> tuple[float, float]:
        j = idx + h
        if j >= len(closes):
            return float("nan"), float("nan")
        price = float(closes.iloc[j])
        return price, direction * (price - reference) / risk

    p5, r5 = r_at(HORIZON_PRIMARY)
    p10, r10 = r_at(HORIZON_SECONDARY)
    out["outcome_price_5d"], out["realized_r_5d"] = (round(p5, 6), round(r5, 4)) if not np.isnan(r5) else (np.nan, np.nan)
    out["outcome_price_10d"], out["realized_r_10d"] = (round(p10, 6), round(r10, 4)) if not np.isnan(r10) else (np.nan, np.nan)
    j5 = idx + HORIZON_PRIMARY
    out["review_due"] = closes.index[j5].strftime("%Y-%m-%d") if j5 < len(closes) else ""
    if np.isnan(r5):
        out["result"] = "pending"  # +5営業日の窓が未確定（正直に待つ）
    else:
        out["result"] = "success" if r5 > 0 else "failure"
    return out


def render_observation(event: dict, pre: dict, similar_meta: dict, holes: list[str]) -> str:
    scores = pre.get("scores", {})
    return f"""# {event['event_id']} — 最小観測ループ記録（Phase 29.4）

- protocol: {PROTOCOL_ID}（run_type: **{event['run_type']}**）
- recorded_at: {event['recorded_at_utc']}
- 実売買なし・研究記録のみ。judged fields は判断時の記録値を使用（反後知恵）。

## 1. 観測（判断時の記録）

- signal_id: `{event['signal_id']}` / {event['a_rank_date']} / {event['asset']} {event['side']} A-rank
- CBS: {event['cbs']} / EMS: {event['ems']}（PROTO-0001 適格条件: CBS>={QUALIFY_CBS:.0f} & EMS>={QUALIFY_EMS:.0f}）
- reference_price: {event['reference_price']} / risk_unit: {event['risk_unit']}
- regime: {pre.get('regime')} / type: {pre.get('signal_type')}
- スコア: {json.dumps(scores, ensure_ascii=False, default=str)}

## 2. 事前ナラティブ（判断時に存在した情報のみ）

- invalidation: {pre.get('invalidation')}
- verification_target: {pre.get('verification_target')}
- win_prob: {pre.get('win_prob')} / expected_r: {pre.get('expected_r')}
- as-of narrative memory: **{pre.get('narrative_memory_status')}**（局面文書 {pre.get('narrative_memory_asof_days')} 日分）

## 3. 評価（+5/+10営業日・当時のリスクユニット）

- review_due(+5営業日): {event['review_due'] or '—'}
- +5営業日: price={event['outcome_price_5d']} → **realized R = {event['realized_r_5d']}**
- +10営業日: price={event['outcome_price_10d']} → realized R = {event['realized_r_10d']}
- 判定: **{event['result']}**（success = R>0 / failure = R<=0 / invalid_data = 元記録不足）

## 4. 類似局面検索（as-of {event['a_rank_date']}）

- status: **{similar_meta.get('status')}**（過去局面 {similar_meta.get('corpus_days', 0)} 日 / provider: {similar_meta.get('embedding_provider') or '—'}）

## 5. 教訓・運用上の穴（このループで見つかったもの）

{chr(10).join(f'- {h}' for h in holes) if holes else '- （なし）'}

## 6. 次のアクション

- 適格イベント（CBS>=80 & EMS>=70 の A-rank）が出た日に同コマンドを実行し、
  PROTO-0001 Observation Log（vault）へ正式記録する。
- narrative memory が5日分を超えたら、類似局面検索が本レコードにも自動で付くようになる。
"""


def run(*, ledger_path: Path = LEDGER_PATH, signal_id: str | None = None,
        obs_log_path: Path = OBS_LOG_PATH, obs_dir: Path = OBS_DIR,
        raw_dir: Path = RAW_DIR, memory_path: Path = MEMORY_PATH) -> dict:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    obs_dir.mkdir(parents=True, exist_ok=True)
    generated_at = now_utc()

    try:
        ledger = pd.read_csv(ledger_path) if ledger_path.exists() else pd.DataFrame()
    except (pd.errors.EmptyDataError, OSError):
        ledger = pd.DataFrame()

    row, run_type = select_candidate(ledger, signal_id)
    summary = {
        "generated_at_jst": format_jst(generated_at),
        "generated_at_utc": format_utc(generated_at),
        "protocol_id": PROTOCOL_ID,
        "run_type": run_type,
        **SAFETY_FIELDS,
    }
    if row is None:
        summary["status"] = "no_candidate"
        (RESULTS_DIR / "observation_loop_summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        return summary

    memory = load_memory(memory_path)
    pre = pre_narrative_record(row, memory)
    asset = str(row.get("asset", ""))
    closes = load_close_series(asset, raw_dir)
    outcome = evaluate_outcome(row, closes)
    cases, similar_meta = retrieve(memory, str(row.get("date")), raw_dir=raw_dir)

    a_date = str(row.get("date", ""))
    event_id = f"OBS-{a_date.replace('-', '')}-{asset}"
    lesson_file = f"data/observations/{event_id}.md"

    holes: list[str] = []
    if run_type == "non_qualifying_dry_run":
        holes.append(
            f"PROTO-0001 適格イベント未発生（この A-rank は CBS={row.get('cbs')} < {QUALIFY_CBS:.0f}）。"
            "dry-run としてループ機構のみ検証。プロトコル台帳には記録しない。"
        )
    if pre["narrative_memory_asof_days"] == 0:
        holes.append("判断日時点の narrative memory が存在しない（memory 稼働開始前のシグナル）。事前ナラティブは判断時の記録フィールドのみ。")
    if similar_meta.get("status") != "ok":
        holes.append(f"類似局面検索は {similar_meta.get('status')}（過去局面 {similar_meta.get('corpus_days', 0)} 日）。日次蓄積で自動解消。")
    if outcome["result"] == "invalid_data":
        holes.append("元記録に entry/SL が欠けており R を計算できない（反後知恵ルールにより推定しない）。")
    if outcome["result"] == "pending":
        holes.append("+5営業日の結果窓が未確定。窓が閉じた後に同コマンドで再実行すると確定する。")

    event = {
        "event_id": event_id,
        "protocol_id": PROTOCOL_ID,
        "run_type": run_type,
        "signal_id": row.get("signal_id"),
        "a_rank_date": a_date,
        "asset": asset,
        "side": str(row.get("side", "")).upper(),
        "cbs": _num(row.get("cbs")),
        "ems": _num(row.get("ems")),
        **outcome,
        "similar_cases_status": similar_meta.get("status", ""),
        "narrative_memory_asof_days": pre["narrative_memory_asof_days"],
        "lesson_file": lesson_file,
        "recorded_at_utc": format_utc(generated_at),
        "notes": "",
    }

    # 台帳へ追記（event_id 重複は最新で上書き = 再実行で pending -> 確定へ更新可能）
    if obs_log_path.exists():
        try:
            log = pd.read_csv(obs_log_path)
        except (pd.errors.EmptyDataError, OSError):
            log = pd.DataFrame(columns=OBS_COLUMNS)
    else:
        log = pd.DataFrame(columns=OBS_COLUMNS)
    log = pd.concat([log, pd.DataFrame([event])], ignore_index=True)
    log = log.drop_duplicates(subset=["event_id"], keep="last").reindex(columns=OBS_COLUMNS)
    obs_log_path.parent.mkdir(parents=True, exist_ok=True)
    log.to_csv(obs_log_path, index=False)

    (obs_dir / f"{event_id}.md").write_text(render_observation(event, pre, similar_meta, holes), encoding="utf-8")

    summary.update({
        "status": "recorded",
        "event_id": event_id,
        "result": event["result"],
        "realized_r_5d": event["realized_r_5d"],
        "holes_found": len(holes),
    })
    (RESULTS_DIR / "observation_loop_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one minimal observation loop (PROTO-0001 compatible).")
    parser.add_argument("--signal-id", default=None, help="対象 signal_id（省略時は適格>直近A-rank）")
    args = parser.parse_args()
    summary = run(signal_id=args.signal_id)
    if summary.get("status") == "no_candidate":
        print("observation loop: no A-rank candidate in ledger (honest no-op)")
    else:
        print(
            f"observation loop: {summary['event_id']} run_type={summary['run_type']} "
            f"result={summary['result']} r5d={summary['realized_r_5d']} holes={summary['holes_found']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
