"""Shadow outcome linkage (Phase 29.5) — weighted vs base のポリシー価値差 d_i を蓄積する。

docs/phase29_design_reasoning.md §1 の実装。昇格ゲートの `no_outcome_linkage` を解除する
唯一の経路であり、統計判断（ゼロ込みペア・divergent 併記・uncomputable の除外+可視化）は
設計書で凍結済み。**この方針を変更しない**こと（§1.6 やってはいけないこと参照）。

ペア = 同一 signal_id の (base の意思決定, weighted の意思決定)。side は weights で変わらないため
差が出るのは actionable ⇔ NO_TRADE の入れ替わりのみ:

| base | weighted | diff |
|---|---|---|
| actionable | actionable | 0（同一トレード） |
| actionable | NO_TRADE   | − R_base |
| NO_TRADE   | actionable | + R_hypothetical（同じ評価ロジックで仮想評価） |
| NO_TRADE   | NO_TRADE   | 0 |

- diff=0 のペアも系列に含める（ポリシー全体の価値差の不偏推定。除外は選択バイアス）。
- 評価が閉じていないペアは awaiting として除外し、件数を必ず表示（捏造しない）。
- 反実仮想が計算不能なら uncomputable_counterfactual として除外+可視化。0 と置かない。
- weights_version はその日の shadow 実行時の版。版をまたいで合算しない。

出力: data/shadow_outcome_diffs.csv（(signal_id, weights_version) で重複排除・最新優先）
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from evaluate_signal import evaluate_trade, load_ohlcv
from time_utils import format_jst, format_utc, now_utc

RESULTS_DIR = Path("results")
DIFFS_PATH = Path("data/shadow_outcome_diffs.csv")
DEFAULT_HORIZON = 10  # daily_cycle の評価ホライズンと同一

ACTIONABLE_RANKS = {"A", "B"}

DIFF_COLUMNS = [
    "date",
    "asset",
    "signal_id",
    "weights_version",
    "pair_type",        # same_action / weighted_skipped / weighted_added / both_no_trade
    "base_r",
    "weighted_r",
    "diff",
    "linked_at_utc",
]

SAFETY_FIELDS = {
    "requires_human_approval": True,
    "weights_json_updated": False,
    "generate_signal_updated": False,
    "affects_live_recommendation": False,
    "shadow_mode": True,
}


def _num(value) -> float:
    v = pd.to_numeric(value, errors="coerce")
    return float(v) if pd.notna(v) else float("nan")


def _is_actionable(rank, side) -> bool:
    return str(rank).upper() in ACTIONABLE_RANKS and str(side).upper() in {"LONG", "SHORT"}


def base_r_from_evaluation(ev: pd.Series, horizon: int) -> tuple[float | None, str]:
    """確定した評価から base の R を取る。未確定は (None, 'awaiting')。

    - r_result があればそれ（SLキャップ込みトレードR）
    - entry が一度も充足せず結果窓が閉じた → R=0.0（トレード不成立は正当なゼロ）
    - それ以外（窓が開いている等） → awaiting
    """
    r = pd.to_numeric(ev.get("r_result"), errors="coerce")
    if pd.notna(r):
        return float(r), "ok"
    entry_hit = str(ev.get("entry_hit")).strip().lower() == "true" or ev.get("entry_hit") is True
    bars = pd.to_numeric(ev.get("bars_checked"), errors="coerce")
    if not entry_hit and pd.notna(bars) and int(bars) >= horizon:
        return 0.0, "no_fill"
    return None, "awaiting"


def hypothetical_r(signal_like: pd.Series, ohlcv: pd.DataFrame, horizon: int) -> tuple[float | None, str]:
    """base=NO_TRADE を weighted が採った場合の仮想R。同じ評価ロジック(evaluate_trade)を適用。

    判定不能は (None, 'uncomputable') — 0 と置かない（設計書 §1.4）。
    """
    if ohlcv is None or ohlcv.empty:
        return None, "uncomputable"
    try:
        res = evaluate_trade(signal_like, ohlcv, horizon)
    except Exception:  # noqa: BLE001 - 反実仮想の失敗で連結全体を止めない(正直に除外)
        return None, "uncomputable"
    r = pd.to_numeric(res.get("r_result"), errors="coerce")
    if pd.notna(r):
        return float(r), "ok"
    if not res.get("entry_hit") and int(res.get("bars_checked") or 0) >= horizon:
        return 0.0, "no_fill"
    if res.get("error_type"):
        return None, "uncomputable"
    return None, "awaiting"


def build_pairs(
    shadow: pd.DataFrame,
    evaluations: pd.DataFrame,
    *,
    horizon: int = DEFAULT_HORIZON,
    ohlcv_loader=load_ohlcv,
    linked_at: str = "",
) -> tuple[pd.DataFrame, dict]:
    """shadow 行 × 評価行 を signal_id で突き合わせ、確定ペアの diff 行を返す。

    返り値: (diff行 DataFrame, 集計 dict[awaiting/uncomputable/missing_evaluation 件数])
    """
    counts = {"pairs_linked": 0, "awaiting": 0, "uncomputable_counterfactual": 0, "missing_evaluation": 0}
    if shadow.empty or "signal_id" not in shadow.columns:
        return pd.DataFrame(columns=DIFF_COLUMNS), counts

    ev_by_id: dict[str, pd.Series] = {}
    if not evaluations.empty and "signal_id" in evaluations.columns:
        for _, row in evaluations.iterrows():
            ev_by_id[str(row.get("signal_id"))] = row

    ohlcv_cache: dict[str, pd.DataFrame] = {}
    rows: list[dict] = []
    for _, s in shadow.iterrows():
        sid = str(s.get("signal_id"))
        side = str(s.get("side", "NONE")).upper()
        version = str(s.get("weights_version") or "")
        base_act = _is_actionable(s.get("base_rank"), side)
        weighted_act = _is_actionable(s.get("weighted_rank"), side)
        ev = ev_by_id.get(sid)

        if ev is None:
            counts["missing_evaluation"] += 1
            continue

        base_r: float | None
        weighted_r: float | None
        if base_act and weighted_act:
            pair_type = "same_action"
            base_r, st = base_r_from_evaluation(ev, horizon)
            if base_r is None:
                counts["awaiting"] += 1
                continue
            weighted_r = base_r  # 同一トレード
        elif base_act and not weighted_act:
            pair_type = "weighted_skipped"
            base_r, st = base_r_from_evaluation(ev, horizon)
            if base_r is None:
                counts["awaiting"] += 1
                continue
            weighted_r = 0.0
        elif not base_act and weighted_act:
            pair_type = "weighted_added"
            base_r = 0.0
            asset = str(s.get("asset") or ev.get("asset") or "")
            if asset not in ohlcv_cache:
                try:
                    ohlcv_cache[asset] = ohlcv_loader(asset)
                except Exception:  # noqa: BLE001
                    ohlcv_cache[asset] = pd.DataFrame()
            signal_like = pd.Series({
                "signal_id": sid, "asset": asset, "side": side,
                "rank": s.get("weighted_rank"), "type": ev.get("type"),
                "date": ev.get("signal_date"),
                "entry_low": ev.get("entry_low"), "entry_high": ev.get("entry_high"),
                "sl": ev.get("sl"), "tp1": ev.get("tp1"), "tp2": ev.get("tp2"),
            })
            weighted_r, st = hypothetical_r(signal_like, ohlcv_cache[asset], horizon)
            if weighted_r is None:
                counts["uncomputable_counterfactual" if st == "uncomputable" else "awaiting"] += 1
                continue
        else:
            pair_type = "both_no_trade"
            base_r, weighted_r = 0.0, 0.0

        rows.append({
            "date": str(ev.get("signal_date") or s.get("date") or ""),
            "asset": str(s.get("asset") or ""),
            "signal_id": sid,
            "weights_version": version,
            "pair_type": pair_type,
            "base_r": round(float(base_r), 4),
            "weighted_r": round(float(weighted_r), 4),
            "diff": round(float(weighted_r) - float(base_r), 4),
            "linked_at_utc": linked_at,
        })
        counts["pairs_linked"] += 1
    return pd.DataFrame(rows, columns=DIFF_COLUMNS), counts


def append_diffs(new_rows: pd.DataFrame, path: Path = DIFFS_PATH) -> pd.DataFrame:
    """(signal_id, weights_version) で重複排除して追記。再実行は最新で上書き(awaiting→確定を更新)。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            existing = pd.read_csv(path)
        except (pd.errors.EmptyDataError, OSError):
            existing = pd.DataFrame(columns=DIFF_COLUMNS)
    else:
        existing = pd.DataFrame(columns=DIFF_COLUMNS)
    merged = pd.concat([existing, new_rows], ignore_index=True)
    merged = merged.drop_duplicates(subset=["signal_id", "weights_version"], keep="last")
    merged = merged.reindex(columns=DIFF_COLUMNS).sort_values(["date", "signal_id"]).reset_index(drop=True)
    merged.to_csv(path, index=False)
    return merged


def diffs_for_version(weights_version: str, path: Path = DIFFS_PATH) -> tuple[list[float], int]:
    """指定版の diff 系列と divergent（diff≠0）件数を返す。ゲートに渡す用。"""
    if not path.exists():
        return [], 0
    try:
        df = pd.read_csv(path)
    except (pd.errors.EmptyDataError, OSError):
        return [], 0
    view = df[df["weights_version"].astype(str) == str(weights_version)]
    diffs = pd.to_numeric(view.get("diff"), errors="coerce").dropna().tolist()
    divergent = int(sum(1 for d in diffs if abs(d) > 1e-12))
    return diffs, divergent


def run(*, horizon: int = DEFAULT_HORIZON) -> dict:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    generated_at = now_utc()

    def read(path: Path) -> pd.DataFrame:
        if not path.exists():
            return pd.DataFrame()
        try:
            return pd.read_csv(path)
        except (pd.errors.EmptyDataError, OSError):
            return pd.DataFrame()

    shadow = read(RESULTS_DIR / "shadow_weighted_signals.csv")
    evaluations = read(RESULTS_DIR / "evaluations.csv")
    latest = read(RESULTS_DIR / "latest_evaluations.csv")
    if not latest.empty:
        evaluations = latest  # 最新評価ビューを優先(評価ループの正)

    new_rows, counts = build_pairs(shadow, evaluations, horizon=horizon, linked_at=format_utc(generated_at))
    ledger = append_diffs(new_rows) if not new_rows.empty else append_diffs(pd.DataFrame(columns=DIFF_COLUMNS))

    version = str(shadow["weights_version"].iloc[0]) if (not shadow.empty and "weights_version" in shadow.columns) else ""
    diffs, divergent = diffs_for_version(version) if version else ([], 0)

    summary = {
        "generated_at_jst": format_jst(generated_at),
        "generated_at_utc": format_utc(generated_at),
        "weights_version": version,
        **counts,
        "ledger_rows_total": int(len(ledger)),
        "diffs_for_current_version": len(diffs),
        "divergent_pairs": divergent,  # 実際に決定が変わったペア数(必ず併記・設計書 §1.2)
        "status": "linked" if counts["pairs_linked"] > 0 else "no_pairs",
    }
    summary.update(SAFETY_FIELDS)
    (RESULTS_DIR / "shadow_outcome_link_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


def main() -> int:
    s = run()
    print(
        f"shadow outcome link: status={s['status']} linked={s['pairs_linked']} "
        f"awaiting={s['awaiting']} uncomputable={s['uncomputable_counterfactual']} "
        f"total={s['ledger_rows_total']} divergent={s['divergent_pairs']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
