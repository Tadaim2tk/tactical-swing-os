"""Ablation evaluation frame (Phase 29.3) — 3系統を同一cohortで比較する。

系統(arm):
- technical_only:            既存テクニカルロジック（generate_signal.build_row を各日as-ofで再構成）
- text_narrative_only:       Narrative Memory の類似局面検索のみから方向を決める
- technical_plus_text:       テクニカルの向きをテキストが確認/棄却する合成（v0の決定的ルール）

同一cohort: 「narrative memory の局面文書があり(過去{MIN_MEMORY_DAYS}日以上の履歴つき)、
テクニカルを再構成でき、結果窓が確定した (日, 資産, ホライズン)」の交差集合のみ。
どの系統も同じ行で比較する（系統ごとに母集団を変えない）。

指標: hit率 / avg R / net R(cost_model・未設定なら net=gross を正直表示) / Brier /
calibration slope / MFE / MAE / Sharpe / DSR(3系統の多重検定として deflate)。

lookahead 防止:
- テクニカル再構成は各日 d 以前のバーのみ（truncate）
- テキスト系統は d より前の局面のみ検索し、さらに**結果窓が d までに閉じた類似日のみ**
  を方向決定に使う（closes のバー位置で機械judge）
- 出力は分析・比較のみで、実推奨・signal score には未接続

データ不足の間は insufficient_data を正直に出す。データが溜まれば同じコマンドで
自動的に数字が出る（実装はデータを待たない）。
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import cost_model
import generate_signal as gs
from build_narrative_memory import MEMORY_PATH, load_memory
from retrieve_similar_narratives import (
    HORIZONS,
    MIN_MEMORY_DAYS,
    RAW_DIR,
    build_day_documents,
    cosine_similarities,
    load_close_series,
    tfidf_matrix,
)
from stat_guards import deflated_sharpe_ratio, sharpe_ratio
from time_utils import format_jst, format_utc, now_utc

RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/ablation")

ARMS = ["technical_only", "text_narrative_only", "technical_plus_text"]
MIN_SAMPLES = 30          # 判断材料に足る最低 actionable 数(SPEC-SG-001 と整合)。実装はこれを待たない
MIN_BARS_FOR_SIGNAL = 60  # テクニカル再構成に要する最低バー数
TEXT_TOP_K = 5
TEXT_EPS = 0.0005         # 類似日リターンの加重平均がこの絶対値未満なら「テキストに向きなし」
TEXT_VETO_PROB = 0.35     # 合成armで、テキストのテクニカル方向確率がこれ未満なら見送り
RISK_ATR_MULT = 1.2       # Rの分母 = 1.2*ATR14 (generate_signal のSL基準と同一)

METRIC_COLUMNS = [
    "arm",
    "horizon_days",
    "n_cohort",
    "n_actionable",
    "participation_rate",
    "hit_rate",
    "avg_r",
    "net_avg_r",
    "cost_source",
    "brier",
    "calibration_slope",
    "avg_mfe_r",
    "avg_mae_r",
    "sharpe",
    "dsr",
    "status",
]

SAFETY_FIELDS = {
    "requires_human_approval": True,
    "weights_json_updated": False,
    "generate_signal_updated": False,
    "connected_to_signal_score": False,
}


# ── 価格ユーティリティ ──────────────────────────────────────────────────────

def load_ohlcv_frame(asset: str, raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    path = raw_dir / f"{asset}.csv"
    if not path.exists():
        return pd.DataFrame()
    try:
        df = gs.load_ohlcv(path)
    except Exception:  # noqa: BLE001 - 壊れた1資産で全体を止めない
        return pd.DataFrame()
    return df


def bar_index(df: pd.DataFrame, date: str) -> int:
    """date 以前の最後のバー位置。無ければ -1。"""
    if df.empty:
        return -1
    dates = pd.to_datetime(df["date"]).dt.normalize()
    return int(dates.searchsorted(pd.Timestamp(date), side="right")) - 1


def atr14_at(df: pd.DataFrame, idx: int) -> float:
    """idx 時点の ATR14（それ以前のバーのみ使用）。"""
    if idx < 1:
        return float("nan")
    view = df.iloc[: idx + 1]
    close, high, low = view["close"], view["high"], view["low"]
    prev_close = close.shift(1)
    tr = pd.concat([(high - low), (high - prev_close).abs(), (low - prev_close).abs()], axis=1).max(axis=1)
    atr = tr.rolling(14, min_periods=14).mean().iloc[-1]
    return float(atr) if pd.notna(atr) else float("nan")


def realized_outcome(df: pd.DataFrame, idx: int, horizon: int, side: str, risk: float) -> dict | None:
    """d(=idx) から +horizon バーの実結果。窓が閉じていなければ None（捏造しない）。"""
    j = idx + horizon
    if j >= len(df) or risk <= 0 or np.isnan(risk):
        return None
    base_close = float(df.iloc[idx]["close"])
    end_close = float(df.iloc[j]["close"])
    path = df.iloc[idx + 1: j + 1]
    hi = float(path["high"].max())
    lo = float(path["low"].min())
    direction = 1.0 if side == "LONG" else -1.0
    signed_move = direction * (end_close - base_close)
    mfe = (hi - base_close) if side == "LONG" else (base_close - lo)
    mae = (lo - base_close) if side == "LONG" else (base_close - hi)
    return {
        "r": signed_move / risk,
        "hit": 1.0 if signed_move > 0 else 0.0,
        "mfe_r": mfe / risk,
        "mae_r": mae / risk,
        "risk_per_unit": risk,
    }


# ── 各 arm の予測（すべて as-of） ────────────────────────────────────────────

def technical_prediction(df: pd.DataFrame, idx: int, asset: str) -> dict:
    """d 以前のバーだけで generate_signal.build_row を再構成。"""
    if idx + 1 < MIN_BARS_FOR_SIGNAL:
        return {"side": "NONE", "prob": 0.5, "reason": "short_history"}
    truncated = df.iloc[: idx + 1].reset_index(drop=True)
    try:
        row = gs.build_row(asset, truncated)
    except Exception:  # noqa: BLE001 - 1日の再構成失敗で cohort 全体を落とさない
        return {"side": "NONE", "prob": 0.5, "reason": "reconstruction_error"}
    side = str(row.get("side", "NONE")).upper()
    prob = pd.to_numeric(row.get("win_prob"), errors="coerce")
    prob = float(prob) if pd.notna(prob) and prob > 0 else 0.5
    return {"side": side if side in {"LONG", "SHORT"} else "NONE", "prob": prob, "reason": ""}


def text_prediction(
    sims_order: list[tuple[str, float]],
    df: pd.DataFrame,
    d_idx: int,
    horizon: int,
) -> dict:
    """類似日の「d までに閉じた」結果だけから方向と確率を決める。

    sims_order: (similar_date, similarity) 類似度降順の上位。
    """
    rets, weights = [], []
    for sim_date, sim in sims_order:
        s_idx = bar_index(df, sim_date)
        if s_idx < 0:
            continue
        j = s_idx + horizon
        if j >= len(df) or j > d_idx:  # 結果窓が d 時点で未確定なら使わない (as-of)
            continue
        base = float(df.iloc[s_idx]["close"])
        rets.append(float(df.iloc[j]["close"]) / base - 1.0)
        weights.append(max(float(sim), 0.0) + 1e-9)
    if not rets:
        return {"side": "NONE", "prob": 0.5, "n_cases": 0}
    w = np.array(weights)
    r = np.array(rets)
    wmean = float(np.sum(w * r) / np.sum(w))
    if abs(wmean) < TEXT_EPS:
        return {"side": "NONE", "prob": 0.5, "n_cases": len(rets)}
    side = "LONG" if wmean > 0 else "SHORT"
    direction = 1.0 if side == "LONG" else -1.0
    agree = float(np.sum(w[(direction * r) > 0]) / np.sum(w))
    return {"side": side, "prob": float(np.clip(agree, 0.05, 0.95)), "n_cases": len(rets)}


def combined_prediction(tech: dict, text: dict) -> dict:
    """v0 の決定的合成ルール: テキストがテクニカルの向きを確認/棄却する。"""
    if tech["side"] == "NONE":
        return {"side": "NONE", "prob": 0.5}
    if text["side"] == "NONE":
        p_text_dir = 0.5  # テキストに向きなし = 中立
    elif text["side"] == tech["side"]:
        p_text_dir = text["prob"]
    else:
        p_text_dir = 1.0 - text["prob"]
    if p_text_dir < TEXT_VETO_PROB:
        return {"side": "NONE", "prob": 0.5}  # 強い不一致 -> 見送り
    return {"side": tech["side"], "prob": float(np.clip((tech["prob"] + p_text_dir) / 2, 0.05, 0.95))}


# ── cohort 構築 ─────────────────────────────────────────────────────────────

def build_cohort(memory: pd.DataFrame, *, raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """全 (日, 資産, ホライズン, arm) の予測と実結果の long テーブルを作る。"""
    day_docs = build_day_documents(memory)
    if len(day_docs) <= MIN_MEMORY_DAYS:
        return pd.DataFrame()

    dates = day_docs["memory_date"].tolist()
    docs = day_docs["doc"].tolist()
    assets = sorted(p.stem for p in raw_dir.glob("*.csv")) if raw_dir.exists() else []
    if not assets:
        return pd.DataFrame()
    frames = {a: load_ohlcv_frame(a, raw_dir) for a in assets}

    rows: list[dict] = []
    for i in range(MIN_MEMORY_DAYS, len(dates)):
        d = dates[i]
        # 類似検索: d 以前の文書のみで fit (未来語彙の混入なし)
        emb = tfidf_matrix(docs[:i] + [docs[i]])
        sims = cosine_similarities(emb, i)[:i]
        order = np.argsort(-sims)[:TEXT_TOP_K]
        sims_order = [(dates[k], float(sims[k])) for k in order]

        for asset in assets:
            df = frames[asset]
            d_idx = bar_index(df, d)
            if d_idx < 0:
                continue
            risk = RISK_ATR_MULT * atr14_at(df, d_idx)
            if np.isnan(risk) or risk <= 0:
                continue  # risk 不定は arm 非依存 -> (日,資産) ごと除外で cohort 対称性を保つ
            tech = technical_prediction(df, d_idx, asset)
            for h in HORIZONS:
                if d_idx + h >= len(df):
                    continue  # 結果窓未確定も arm 非依存 -> 全arm一律に除外(捏造しない)
                text = text_prediction(sims_order, df, d_idx, h)
                comb = combined_prediction(tech, text)
                preds = {"technical_only": tech, "text_narrative_only": text, "technical_plus_text": comb}
                # 同一cohort: 3系統とも同じ (日,資産,ホライズン) 行で outcome を評価する
                for arm in ARMS:
                    p = preds[arm]
                    outcome = realized_outcome(df, d_idx, h, p["side"], risk) if p["side"] != "NONE" else None
                    rows.append({
                        "date": d, "asset": asset, "horizon_days": h, "arm": arm,
                        "side": p["side"], "prob": round(float(p["prob"]), 4),
                        "actionable": p["side"] != "NONE",
                        "r": round(outcome["r"], 4) if outcome else np.nan,
                        "hit": outcome["hit"] if outcome else np.nan,
                        "mfe_r": round(outcome["mfe_r"], 4) if outcome else np.nan,
                        "mae_r": round(outcome["mae_r"], 4) if outcome else np.nan,
                        "risk_per_unit": outcome["risk_per_unit"] if outcome else np.nan,
                    })
    return pd.DataFrame(rows)


# ── 指標集計 ────────────────────────────────────────────────────────────────

def _calibration_slope(probs: np.ndarray, hits: np.ndarray) -> float:
    if len(probs) < 3 or float(np.var(probs)) <= 1e-12:
        return float("nan")
    return float(np.cov(probs, hits, bias=True)[0, 1] / np.var(probs))


def summarize_metrics(cohort: pd.DataFrame) -> pd.DataFrame:
    if cohort.empty:
        return pd.DataFrame(columns=METRIC_COLUMNS)
    rows: list[dict] = []
    for h in HORIZONS:
        view_h = cohort[cohort["horizon_days"] == h]
        if view_h.empty:
            continue
        # DSR 用: 同一ホライズンの3系統 Sharpe の分散 (3armの多重検定として deflate)
        arm_sharpes = []
        for arm in ARMS:
            act = view_h[(view_h["arm"] == arm) & view_h["actionable"]]
            arm_sharpes.append(sharpe_ratio(act["r"].dropna().tolist()) if not act.empty else 0.0)
        sharpe_var = float(np.var(arm_sharpes))

        for arm in ARMS:
            sub = view_h[view_h["arm"] == arm]
            act = sub[sub["actionable"]].dropna(subset=["r"])
            n_cohort, n_act = int(len(sub)), int(len(act))
            if n_act == 0:
                rows.append({
                    "arm": arm, "horizon_days": h, "n_cohort": n_cohort, "n_actionable": 0,
                    "participation_rate": 0.0, "hit_rate": np.nan, "avg_r": np.nan,
                    "net_avg_r": np.nan, "cost_source": "", "brier": np.nan,
                    "calibration_slope": np.nan, "avg_mfe_r": np.nan, "avg_mae_r": np.nan,
                    "sharpe": np.nan, "dsr": np.nan, "status": "insufficient_data",
                })
                continue
            r = act["r"].to_numpy(dtype=float)
            probs = act["prob"].to_numpy(dtype=float)
            hits = act["hit"].to_numpy(dtype=float)
            # net R: cost_model (未設定なら cost=0 -> net==gross を正直に表示)
            net_vals = [
                cost_model.net_r(float(row.r), str(row.asset), float(row.risk_per_unit), float(h))
                for row in act.itertuples()
            ]
            cost_src = cost_model.asset_cost(str(act.iloc[0]["asset"])).get("source", "unconfigured")
            rows.append({
                "arm": arm,
                "horizon_days": h,
                "n_cohort": n_cohort,
                "n_actionable": n_act,
                "participation_rate": round(n_act / n_cohort, 4) if n_cohort else 0.0,
                "hit_rate": round(float(hits.mean()), 4),
                "avg_r": round(float(r.mean()), 4),
                "net_avg_r": round(float(np.mean(net_vals)), 4),
                "cost_source": cost_src,
                "brier": round(float(np.mean((probs - hits) ** 2)), 4),
                "calibration_slope": round(_calibration_slope(probs, hits), 4),
                "avg_mfe_r": round(float(act["mfe_r"].mean()), 4),
                "avg_mae_r": round(float(act["mae_r"].mean()), 4),
                "sharpe": round(sharpe_ratio(r.tolist()), 4),
                "dsr": round(deflated_sharpe_ratio(r.tolist(), n_trials=len(ARMS), sharpe_variance=sharpe_var), 4),
                "status": "ok" if n_act >= MIN_SAMPLES else "insufficient_data",
            })
    return pd.DataFrame(rows, columns=METRIC_COLUMNS)


def render_report(summary: dict, table: pd.DataFrame) -> str:
    if table.empty:
        body = (
            f"_cohort なし（narrative memory の局面文書 {summary['memory_days_total']} 日 / "
            f"最低 {MIN_MEMORY_DAYS + 1} 日 + 価格履歴が必要）。データが溜まれば自動で数字が出る。_"
        )
    else:
        lines = [
            "| arm | h | cohort | act | 参加率 | hit率 | avg R | net R | Brier | cal.slope | MFE | MAE | Sharpe | DSR | status |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        for _, r in table.iterrows():
            def f(v, p=".3f"):
                return format(v, p) if pd.notna(v) else "—"
            lines.append(
                f"| {r['arm']} | {r['horizon_days']}d | {r['n_cohort']} | {r['n_actionable']} | {f(r['participation_rate'], '.2f')} "
                f"| {f(r['hit_rate'], '.3f')} | {f(r['avg_r'])} | {f(r['net_avg_r'])} | {f(r['brier'])} | {f(r['calibration_slope'])} "
                f"| {f(r['avg_mfe_r'])} | {f(r['avg_mae_r'])} | {f(r['sharpe'])} | {f(r['dsr'])} | {r['status']} |"
            )
        body = "\n".join(lines)
    return f"""# Ablation Comparison（3系統比較 / Phase 29.3）

## 1. 概要

- 生成日時JST: {summary['generated_at_jst']}
- status: **{summary['status']}** / cohort行数: {summary['cohort_rows']} / 局面日数: {summary['memory_days_total']}
- 系統: technical_only / text_narrative_only / technical_plus_text（同一cohort・同一結果窓）
- cost_source が unconfigured の間は net R = gross R（コスト値は捏造しない）

## 2. 指標（arm × horizon）

{body}

## 3. 読み方と注意

- n_actionable >= {MIN_SAMPLES} の行だけが判断材料（status=ok）。未満は insufficient_data の正直表示。
- テキスト系統は「基準日までに結果が確定した類似日」だけで方向を決めている（as-of・lookahead-safe）。
- この比較は分析専用で、実推奨・signal score には未接続。実売買・発注は行わない。
"""


def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    generated_at = now_utc()

    memory = load_memory(MEMORY_PATH)
    day_docs = build_day_documents(memory)
    cohort = build_cohort(memory)
    table = summarize_metrics(cohort)

    status = "ok" if (not table.empty and (table["status"] == "ok").any()) else "insufficient_data"
    summary = {
        "generated_at_jst": format_jst(generated_at),
        "generated_at_utc": format_utc(generated_at),
        "status": status,
        "arms": ARMS,
        "memory_days_total": int(len(day_docs)),
        "cohort_rows": int(len(cohort)),
        "min_samples_for_judgement": MIN_SAMPLES,
    }
    summary.update(SAFETY_FIELDS)

    cohort.to_csv(RESULTS_DIR / "ablation_cohort.csv", index=False)
    table.to_csv(RESULTS_DIR / "ablation_comparison.csv", index=False)
    (RESULTS_DIR / "ablation_comparison_summary.json").write_text(
        json.dumps({"summary": summary,
                    "rows": table.where(pd.notna(table), None).to_dict(orient="records")},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    report_date = format_jst(generated_at)[:10]
    (REPORTS_DIR / f"{report_date}_ablation_comparison.md").write_text(render_report(summary, table), encoding="utf-8")

    print(f"ablation comparison: status={status} cohort_rows={len(cohort)} arms={len(ARMS)} horizons={HORIZONS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
