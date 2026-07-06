"""Shadow weights layer (Phase 29.1) — 学習ループ閉鎖の第一接続。

models/approved_weights.json（人間承認済み weights）を読み、base シグナルに対する
weighted シグナルを **shadow** で計算・記録する。

- 実推奨（results/signals.csv の既存列）には一切影響しない。
- ここでの「承認」は shadow 比較の開始許可であり、実推奨への反映（active 昇格）は
  別途人間承認（PRマージ）が必要（governance_reform_2026-07 §2 #4）。
- 比較は data/shadow_weight_comparisons.csv に日次追記され、累積 30 件以上で
  昇格判断の材料が揃う（判断は人間）。

設計メモ:
- weighted 側は signals.csv に保存済みのコンポーネントスコア
  (trend/momentum/volatility/risk_penalty/entry_quality/direction_confidence/rr)
  から post-hoc に再構成する。丸め誤差による偽差分を避けるため、差分は
  「weights=1 で再構成した base」と「approved weights で再構成した weighted」を
  同じ式で比較する（identity weights なら厳密にゼロ差分）。
- base side=NONE の行は重み以前のハードゲート（risk>=80 / trend不明瞭 / 低ATR /
  データ不足）で落ちており entry水準も無いため、weighted でも NO_TRADE のまま
  （復活させない）。重みが影響するのは actionable 行の A/B/NO_TRADE 裁定と強度。
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from time_utils import format_jst, format_utc, now_utc

MODELS_PATH = Path("models/approved_weights.json")
RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/model_state")
LEDGER_PATH = Path("data/shadow_weight_comparisons.csv")
MIN_COMPARISONS_FOR_PROMOTION = 30

# shadow 成果物が必ず携行する安全フィールド。
# adversarial review はこの組合せ（shadow_mode=true / affects_live_recommendation=false）を
# 「正当な shadow 記録」と判定し、逆の主張を blocked として検出する。
SAFETY_FIELDS = {
    "shadow_mode": True,
    "affects_live_recommendation": False,
    "weights_json_updated": False,
    "patch_applied": False,
    "apply_automatically": False,
    "requires_human_approval": True,  # active昇格(実推奨反映)に対する人間承認
}

SHADOW_COLUMNS = [
    "date",
    "signal_id",
    "asset",
    "side",
    "base_rank",
    "base_recommended_action",
    "base_signal_strength",
    "recon_base_setup_quality",
    "recon_base_rank",
    "recon_base_signal_strength",
    "weighted_setup_quality",
    "weighted_rank",
    "weighted_recommended_action",
    "weighted_signal_strength",
    "rank_changed",
    "action_changed",
    "strength_delta",
    "reconstruction_mismatch",
    "weights_version",
    "shadow_mode",
    "affects_live_recommendation",
]

LEDGER_COLUMNS = [
    "date",
    "weights_version",
    "n_signals",
    "n_actionable",
    "rank_changes",
    "action_changes",
    "mean_abs_strength_delta",
    "max_abs_strength_delta",
    "reconstruction_mismatches",
]

_GLOBAL_KEYS = ["rank_weight", "trend_weight", "momentum_weight", "volatility_weight", "risk_penalty_weight"]


def _finite_number(value) -> bool:
    try:
        return np.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def load_approved_weights(path: Path = MODELS_PATH) -> dict:
    """approved weights を読み、正直なステータス付きで返す。

    status: approved / missing / invalid / not_approved
    weights は status == approved のときのみ非None。
    """
    result = {"status": "missing", "weights": None, "weights_version": "", "meta": {}}
    if not path.exists():
        return result
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        result["status"] = "invalid"
        return result
    if not isinstance(payload, dict):
        result["status"] = "invalid"
        return result

    result["weights_version"] = str(payload.get("weights_version", ""))
    result["meta"] = {
        "approved_by": payload.get("approved_by"),
        "approved_at": payload.get("approved_at"),
        "source_pr": payload.get("source_pr"),
        "sample_count": payload.get("sample_count"),
        "guard_report_id": payload.get("guard_report_id"),
    }

    if str(payload.get("status", "")).strip().lower() != "approved":
        result["status"] = "not_approved"
        return result

    glob = payload.get("global")
    assets = payload.get("asset_weights")
    ranks = payload.get("rank_weights")
    sides = payload.get("side_weights")
    if not (isinstance(glob, dict) and isinstance(assets, dict) and isinstance(ranks, dict) and isinstance(sides, dict)):
        result["status"] = "invalid"
        return result
    for key in _GLOBAL_KEYS:
        if not _finite_number(glob.get(key)):
            result["status"] = "invalid"
            return result
    for mapping in (assets, ranks, sides):
        for v in mapping.values():
            if not _finite_number(v):
                result["status"] = "invalid"
                return result

    result["status"] = "approved"
    result["weights"] = {
        "global": {k: float(glob[k]) for k in _GLOBAL_KEYS},
        "asset_weights": {str(k): float(v) for k, v in assets.items()},
        "rank_weights": {str(k): float(v) for k, v in ranks.items()},
        "side_weights": {str(k): float(v) for k, v in sides.items()},
    }
    return result


def is_identity_weights(weights: dict) -> bool:
    if not weights:
        return False
    values = list(weights["global"].values())
    for mapping in (weights["asset_weights"], weights["rank_weights"], weights["side_weights"]):
        values.extend(mapping.values())
    return all(abs(float(v) - 1.0) < 1e-12 for v in values)


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    if pd.isna(value):
        return 0.0
    return float(max(low, min(high, value)))


def _num(row, col, default=np.nan) -> float:
    v = pd.to_numeric(row.get(col), errors="coerce")
    return float(v) if pd.notna(v) else default


def _setup_quality(trend_d: float, momentum_d: float, volatility: float, risk_penalty: float, g: dict) -> float:
    # generate_signal.calc_setup_quality と同一の式に global weights を乗せたもの。
    raw = (
        0.35 * g["trend_weight"] * trend_d
        + 0.35 * g["momentum_weight"] * momentum_d
        + 0.20 * g["volatility_weight"] * volatility
        - 0.20 * g["risk_penalty_weight"] * risk_penalty
        + 10
    )
    return _clamp(raw)


def _rank(setup: float, entry_q: float, conf: float, risk_penalty: float, rr: float) -> str:
    # generate_signal.build_row の rank 裁定と同一の閾値。
    if setup >= 75 and entry_q >= 65 and conf >= 65 and risk_penalty < 60 and rr >= 1.5:
        return "A"
    if setup >= 60 and entry_q >= 50 and conf >= 50 and rr >= 1.5:
        return "B"
    return "NO_TRADE"


def _action(rank: str) -> str:
    return {"A": "TRADE", "B": "WATCH"}.get(rank, "NO_TRADE")


def _strength(setup: float, conf: float, entry_q: float, rank: str, side: str, asset: str, weights: dict | None) -> float:
    if rank == "NO_TRADE":
        return 0.0
    raw = setup * 0.5 + conf * 0.3 + entry_q * 0.2
    if weights is not None:
        raw *= weights["asset_weights"].get(asset, 1.0)
        raw *= weights["rank_weights"].get(rank, 1.0) * weights["global"]["rank_weight"]
        raw *= weights["side_weights"].get(side, 1.0)
    return round(_clamp(raw), 2)


_IDENTITY_GLOBAL = {k: 1.0 for k in _GLOBAL_KEYS}


def compute_shadow(signals: pd.DataFrame, weights: dict, weights_version: str) -> pd.DataFrame:
    """base シグナルに対する weighted シグナルを shadow で計算する（純関数・入力非破壊）。"""
    rows: list[dict] = []
    for _, r in signals.iterrows():
        side = str(r.get("side", "NONE")).upper()
        asset = str(r.get("asset", ""))
        base_rank = str(r.get("rank", "NO_TRADE")).upper()
        trend = _num(r, "trend_score", 0.0)
        momentum = _num(r, "momentum_score", 0.0)
        volatility = _num(r, "volatility_score", 0.0)
        risk_penalty = _num(r, "risk_penalty_score", 100.0)
        entry_q = _num(r, "entry_quality_score", 0.0)
        conf = _num(r, "direction_confidence", 0.0)
        rr = _num(r, "rr", 0.0)

        # SHORT はディレクショナル反転（generate_signal と同じ規約）
        trend_d = trend if side != "SHORT" else 100.0 - trend
        momentum_d = momentum if side != "SHORT" else 100.0 - momentum

        actionable = side in {"LONG", "SHORT"}
        if actionable:
            recon_setup = _setup_quality(trend_d, momentum_d, volatility, risk_penalty, _IDENTITY_GLOBAL)
            recon_rank = _rank(recon_setup, entry_q, conf, risk_penalty, rr)
            recon_strength = _strength(recon_setup, conf, entry_q, recon_rank, side, asset, None)
            w_setup = _setup_quality(trend_d, momentum_d, volatility, risk_penalty, weights["global"])
            w_rank = _rank(w_setup, entry_q, conf, risk_penalty, rr)
            w_strength = _strength(w_setup, conf, entry_q, w_rank, side, asset, weights)
        else:
            # ハードゲートで落ちた行は weighted でも復活させない（重み以前の除外）。
            recon_setup = _setup_quality(trend_d, momentum_d, volatility, risk_penalty, _IDENTITY_GLOBAL)
            recon_rank = "NO_TRADE"
            recon_strength = 0.0
            w_setup = _setup_quality(trend_d, momentum_d, volatility, risk_penalty, weights["global"])
            w_rank = "NO_TRADE"
            w_strength = 0.0

        rows.append({
            "date": r.get("date"),
            "signal_id": r.get("signal_id"),
            "asset": asset,
            "side": side,
            "base_rank": base_rank,
            "base_recommended_action": r.get("recommended_action"),
            "base_signal_strength": _num(r, "signal_strength", 0.0),
            "recon_base_setup_quality": round(recon_setup, 2),
            "recon_base_rank": recon_rank,
            "recon_base_signal_strength": recon_strength,
            "weighted_setup_quality": round(w_setup, 2),
            "weighted_rank": w_rank,
            "weighted_recommended_action": _action(w_rank),
            "weighted_signal_strength": w_strength,
            "rank_changed": w_rank != recon_rank,
            "action_changed": _action(w_rank) != _action(recon_rank),
            "strength_delta": round(w_strength - recon_strength, 2),
            # 再構成が保存値と食い違った行数の可視化（actionable のみ意味を持つ）
            "reconstruction_mismatch": actionable and (recon_rank != base_rank),
            "weights_version": weights_version,
            "shadow_mode": True,
            "affects_live_recommendation": False,
        })
    return pd.DataFrame(rows, columns=SHADOW_COLUMNS)


def _append_ledger(entry: dict, path: Path = LEDGER_PATH) -> pd.DataFrame:
    """比較台帳へ日次1行を追記（同 date+weights_version は最新で上書き）。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            ledger = pd.read_csv(path)
        except (pd.errors.EmptyDataError, OSError):
            ledger = pd.DataFrame(columns=LEDGER_COLUMNS)
    else:
        ledger = pd.DataFrame(columns=LEDGER_COLUMNS)
    ledger = pd.concat([ledger, pd.DataFrame([entry])], ignore_index=True)
    ledger = ledger.drop_duplicates(subset=["date", "weights_version"], keep="last").reset_index(drop=True)
    ledger = ledger.reindex(columns=LEDGER_COLUMNS)
    ledger.to_csv(path, index=False)
    return ledger


def _comparisons_accumulated(ledger: pd.DataFrame, weights_version: str) -> int:
    if ledger.empty or "weights_version" not in ledger.columns:
        return 0
    view = ledger[ledger["weights_version"].astype(str) == str(weights_version)]
    return int(pd.to_numeric(view.get("n_actionable"), errors="coerce").fillna(0).sum())


def evaluate_promotion_gate(
    outcome_r_diffs: list[float] | None,
    comparisons_accumulated: int,
    *,
    n_trials: int = 1,
    sharpe_variance: float = 0.0,
) -> dict:
    """非identity weights を「昇格判断の材料あり」と言えるかの機械ゲート。

    通過しても行われるのは人間への材料提示のみ（承認は人間PR / 不可侵 #4）。
    小標本1件の後知恵（例: 単発の failure 観測）で weight を動かせない構造を、
    identity のうちにテストで固定するのが目的（司令 B-1 指示）。

    outcome_r_diffs: 「weighted選択 − base選択」の R 差分系列（結果が閉じたもの）。
    v0 では outcome 連結が未実装のため None → no_outcome_linkage で必ず blocked。
    n_trials: 同時に検討している weights 候補数（多重検定として DSR を deflate）。
    sharpe_variance: 候補間 Sharpe の分散（n_trials>1 のとき呼び手が供給。単独候補では0でPSR相当）。

    判定は SPEC-SG-001 / SPEC-DSR-001 と同一の統計ゲートに通す:
    n >= MIN_COMPARISONS_FOR_PROMOTION / t検定 p<=0.05 かつ平均差>0 /
    DSR >= DEFLATED_SHARPE_CONFIDENCE。blocked 理由はすべて列挙する（false green を作らない）。
    """
    from stat_guards import DEFLATED_SHARPE_CONFIDENCE, deflated_sharpe_ratio, t_test_one_sample

    reasons: list[str] = []
    metrics: dict = {
        "n_outcome_diffs": 0,
        "mean_r_diff": None,
        "t_p_value": None,
        "dsr": None,
        "dsr_threshold": DEFLATED_SHARPE_CONFIDENCE,
        "n_trials": int(n_trials),
    }

    if comparisons_accumulated < MIN_COMPARISONS_FOR_PROMOTION:
        reasons.append(
            f"insufficient_comparisons: {comparisons_accumulated} < {MIN_COMPARISONS_FOR_PROMOTION}"
        )

    diffs = [float(v) for v in (outcome_r_diffs or []) if pd.notna(v)]
    metrics["n_outcome_diffs"] = len(diffs)
    if not diffs:
        reasons.append("no_outcome_linkage: weighted vs base の R 差分系列が未接続（結果で裏づけられない変更は提案しない）")
    else:
        mean_diff = float(np.mean(diffs))
        metrics["mean_r_diff"] = round(mean_diff, 4)
        if len(diffs) < MIN_COMPARISONS_FOR_PROMOTION:
            reasons.append(f"insufficient_outcome_samples: {len(diffs)} < {MIN_COMPARISONS_FOR_PROMOTION}")
        if all(abs(d) < 1e-12 for d in diffs):
            reasons.append("zero_difference: base と weighted の結果に差が無く、weights 変更を正当化できない")
        elif float(np.std(diffs)) < 1e-9:
            # レビュー指摘#5: 定数系列は分散情報が無く、丸め残差でDSRが最大確信に化ける。fail-closed。
            reasons.append("degenerate_variance: 差分系列が定数で分散情報が無く、統計判定できない")
        else:
            _t, p = t_test_one_sample(diffs, mu=0.0)
            metrics["t_p_value"] = round(float(p), 4)
            if mean_diff <= 0:
                reasons.append(f"mean_diff_not_positive: {mean_diff:.4f} <= 0")
            if p > 0.05:
                reasons.append(f"not_significant: p={p:.4f} > 0.05")
            dsr = deflated_sharpe_ratio(diffs, n_trials=n_trials, sharpe_variance=float(sharpe_variance))
            metrics["dsr"] = round(float(dsr), 4)
            if dsr < DEFLATED_SHARPE_CONFIDENCE:
                reasons.append(f"dsr_below_threshold: {dsr:.4f} < {DEFLATED_SHARPE_CONFIDENCE}（多重検定後は偶然と区別できない）")

    return {
        "decision": "materials_ready" if not reasons else "blocked",
        "blocked_reasons": reasons,
        **metrics,
        # 材料が揃っても自動適用はしない（不可侵 #4）
        "requires_human_approval": True,
        "apply_automatically": False,
    }


def build_summary(shadow: pd.DataFrame, loaded: dict, comparisons_accumulated: int, generated_at, outcome_r_diffs: list[float] | None = None) -> dict:
    actionable = shadow[shadow["side"].isin(["LONG", "SHORT"])] if not shadow.empty else pd.DataFrame()
    abs_delta = pd.to_numeric(actionable.get("strength_delta"), errors="coerce").abs() if not actionable.empty else pd.Series(dtype=float)
    summary = {
        "generated_at_jst": format_jst(generated_at),
        "generated_at_utc": format_utc(generated_at),
        "weights_status": loaded["status"],
        "weights_version": loaded["weights_version"],
        "is_identity_weights": is_identity_weights(loaded.get("weights")),  # weights が読めていれば status に関わらず判定
        "n_signals": int(len(shadow)),
        "n_actionable": int(len(actionable)),
        "rank_changes": int(actionable["rank_changed"].sum()) if not actionable.empty else 0,
        "action_changes": int(actionable["action_changed"].sum()) if not actionable.empty else 0,
        "mean_abs_strength_delta": round(float(abs_delta.mean()), 4) if len(abs_delta) else 0.0,
        "max_abs_strength_delta": round(float(abs_delta.max()), 4) if len(abs_delta) else 0.0,
        "reconstruction_mismatches": int(shadow["reconstruction_mismatch"].sum()) if not shadow.empty else 0,
        "comparisons_accumulated": int(comparisons_accumulated),
        "min_comparisons_for_promotion": MIN_COMPARISONS_FOR_PROMOTION,
        "promotion_sample_ready": bool(comparisons_accumulated >= MIN_COMPARISONS_FOR_PROMOTION),
        # 昇格ゲート: outcome 連結(link_shadow_outcomes)の diff 系列が無い間は必ず blocked。
        # identity weights では全ゼロ -> zero_difference で blocked が正しい。
        # sample_ready は「蓄積の進捗」、gate は「昇格材料の統計的成立」— 別物として両方出す。
        "promotion_gate": evaluate_promotion_gate(outcome_r_diffs, comparisons_accumulated),
    }
    summary.update(SAFETY_FIELDS)
    return summary


def render_report(summary: dict, shadow: pd.DataFrame) -> str:
    changed = pd.DataFrame()
    if not shadow.empty:
        mask = shadow["rank_changed"] | (pd.to_numeric(shadow["strength_delta"], errors="coerce").abs() > 0)
        changed = shadow[mask & shadow["side"].isin(["LONG", "SHORT"])]

    def table(df: pd.DataFrame) -> str:
        if df.empty:
            return "_差分なし_"
        lines = [
            "| signal_id | asset | side | recon_rank | weighted_rank | Δstrength | weighted_action |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
        for _, r in df.head(20).iterrows():
            lines.append(
                f"| {r['signal_id']} | {r['asset']} | {r['side']} | {r['recon_base_rank']} | "
                f"{r['weighted_rank']} | {r['strength_delta']} | {r['weighted_recommended_action']} |"
            )
        return "\n".join(lines)

    if summary["weights_status"] != "approved":
        status_note = {
            "missing": "models/approved_weights.json が存在しない。",
            "invalid": "approved_weights.json が壊れているか、数値でない重みを含む。",
            "not_approved": "status が approved ではないため読み込まない（承認済みのみ読込）。",
            "no_signals": "本日のシグナルが無いため比較対象なし。",
        }.get(summary["weights_status"], "")
        body_note = f"**weights未適用（{summary['weights_status']}）**: {status_note} shadow比較は実行していない。"
    elif summary["is_identity_weights"]:
        body_note = (
            "現在の approved weights は **identity（全1.0）ベースライン**。weighted == base が"
            "構成上成立し、差分ゼロが正常。実差分の比較を始めるには、非identityの候補weightsを"
            "人間承認PRで models/approved_weights.json に昇格させる。"
        )
    else:
        body_note = "approved weights による shadow 比較を実行中。"

    ready = summary["promotion_sample_ready"]
    return f"""# Shadow Weight Impact（週次昇格判断の材料）

## 1. 概要

- 生成日時JST: {summary['generated_at_jst']}
- weights_status: **{summary['weights_status']}** / version: {summary['weights_version'] or '—'}
- identity weights: {str(summary['is_identity_weights']).lower()}
- 本日のシグナル数: {summary['n_signals']}（actionable: {summary['n_actionable']}）
- rank変化: {summary['rank_changes']} / action変化: {summary['action_changes']}
- |Δstrength| 平均: {summary['mean_abs_strength_delta']} / 最大: {summary['max_abs_strength_delta']}
- 再構成不一致（recon_base_rank != base_rank）: {summary['reconstruction_mismatches']}

{body_note}

## 2. 昇格判断の材料

- 累積比較数（actionable, version={summary['weights_version'] or '—'}）: **{summary['comparisons_accumulated']} / {summary['min_comparisons_for_promotion']}**
- 昇格判断に足るサンプル: **{'到達' if ready else '未到達'}**
- 統計ゲート判定: **{summary['promotion_gate']['decision']}**
  {chr(10).join('  - ' + r for r in summary['promotion_gate']['blocked_reasons']) or '  - （全条件クリア: 材料を人間へ提示可能）'}
- ゲート仕様: n>={summary['min_comparisons_for_promotion']} / t検定 p<=0.05 かつ平均R差>0 /
  DSR>={summary['promotion_gate']['dsr_threshold']}（SPEC-SG-001 / SPEC-DSR-001 と同一の統計基準）。
  **単発観測・小標本の後知恵では weights を動かせない。**
- 昇格の手続き: ゲート通過後も自動適用はない。候補weightsを `models/approved_weights.json` に反映し
  `models/weight_versions/` にスナップショットを置く**人間承認PR**を出す。
  実推奨（active）への反映はさらに別の人間承認PRが必要。

## 3. 本日の差分（rank変化 or |Δstrength|>0、上位20件）

{table(changed)}

## 4. 安全条件

- これは shadow 記録であり、実推奨（results/signals.csv の既存列）には影響しない。
- affects_live_recommendation=false / weights_json_updated=false / patch_applied=false。
- 実売買・発注・XM/証券会社操作は行わない。昇格判断は人間が行う。
"""


def run(signals: pd.DataFrame | None = None, *, models_path: Path = MODELS_PATH) -> dict:
    """shadow 計算の実行本体。generate_signal.main() から毎日呼ばれる。"""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    generated_at = now_utc()

    if signals is None:
        path = RESULTS_DIR / "signals.csv"
        if path.exists():
            try:
                signals = pd.read_csv(path)
            except (pd.errors.EmptyDataError, OSError):
                signals = pd.DataFrame()
        else:
            signals = pd.DataFrame()

    loaded = load_approved_weights(models_path)

    if loaded["status"] == "approved" and not signals.empty:
        shadow = compute_shadow(signals, loaded["weights"], loaded["weights_version"])
        signal_date = str(shadow["date"].iloc[0]) if len(shadow) else format_jst(generated_at)[:10]
        actionable = shadow[shadow["side"].isin(["LONG", "SHORT"])]
        abs_delta = pd.to_numeric(actionable["strength_delta"], errors="coerce").abs()
        ledger = _append_ledger({
            "date": signal_date,

            "weights_version": loaded["weights_version"],
            "n_signals": int(len(shadow)),
            "n_actionable": int(len(actionable)),
            "rank_changes": int(actionable["rank_changed"].sum()) if not actionable.empty else 0,
            "action_changes": int(actionable["action_changed"].sum()) if not actionable.empty else 0,
            "mean_abs_strength_delta": round(float(abs_delta.mean()), 4) if len(abs_delta) else 0.0,
            "max_abs_strength_delta": round(float(abs_delta.max()), 4) if len(abs_delta) else 0.0,
            "reconstruction_mismatches": int(shadow["reconstruction_mismatch"].sum()),
        }, LEDGER_PATH)
        accumulated = _comparisons_accumulated(ledger, loaded["weights_version"])
    else:
        shadow = pd.DataFrame(columns=SHADOW_COLUMNS)
        if loaded["status"] == "approved" and signals.empty:
            loaded = dict(loaded, status="no_signals")
        accumulated = 0
        if LEDGER_PATH.exists():
            try:
                accumulated = _comparisons_accumulated(pd.read_csv(LEDGER_PATH), loaded["weights_version"])
            except (pd.errors.EmptyDataError, OSError):
                accumulated = 0

    try:
        from link_shadow_outcomes import diffs_for_version
        outcome_diffs, _divergent = diffs_for_version(str(loaded.get("weights_version") or ""))
        outcome_diffs = outcome_diffs or None
    except Exception:  # noqa: BLE001 - 連結未整備でも shadow 本体は止めない(ゲートは no_outcome_linkage)
        outcome_diffs = None
    summary = build_summary(shadow, loaded, accumulated, generated_at, outcome_r_diffs=outcome_diffs)

    shadow.to_csv(RESULTS_DIR / "shadow_weighted_signals.csv", index=False)
    shadow.to_json(RESULTS_DIR / "shadow_weighted_signals.json", orient="records", indent=2, force_ascii=False)
    (RESULTS_DIR / "shadow_weight_impact_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (REPORTS_DIR / "shadow_weight_impact.md").write_text(render_report(summary, shadow), encoding="utf-8")
    return summary


def main() -> int:
    summary = run()
    print(
        f"shadow weights: status={summary['weights_status']} version={summary['weights_version'] or '-'} "
        f"signals={summary['n_signals']} rank_changes={summary['rank_changes']} "
        f"comparisons={summary['comparisons_accumulated']}/{summary['min_comparisons_for_promotion']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
