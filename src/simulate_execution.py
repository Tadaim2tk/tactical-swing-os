"""SL/TP執行シミュレーション (保守的・反後知恵) — 台帳判断を日足OHLCで擬似執行する。

close基準の方向採点(score_prediction_log)の一段上の忠実度として、
「朝に指値を出していたら何が起きたか」を日足の範囲で再現する。

反後知恵の原則 — 日中の順序が分からない曖昧さは、必ず戦略に不利な側へ倒す:
- 約定価格はゾーン内の最悪価格 (BUY=entry_high / SELL=entry_low)
- 約定した足でSLにも触れていれば、順序不明 → SL成立(-1R)とみなす
- TP1は約定した足では成立させない(翌足以降のみ)。SLとTP1が同じ足なら SL優先
- 判断当日の足は約定検出に含める(7:00 JSTの記帳は各系列の当日セッション開始前。
  境界の曖昧さは上記ルールにより不利側へしか作用しない)
- 記帳水準が当日終値から10%超乖離した行は excluded_scale として隔離(採点系と同じ閾値)

執行ポリシー v0 (docs/gpt_prompt_changelog.md の運用と整合):
- 対象: side BUY/SELL・rank A/B・entry/SL記帳あり・risk_pct>0 の判断
- 約定待ち: 判断日を含む5営業日バー。未到達は no_fill
- 決済: SL / TP1 / 判断日+5バー目の終値で時間切れ決済 (TP2・分割決済は扱わない)
- コスト: 未控除(絶対値の出典が未設定のため)。サマリーに R建ての感応度のみ提示

出力:
- data/execution_simulation.csv   (全注文の擬似執行結果・追跡対象)
- results/execution_simulation_summary.json (人間向けサマリー)

表示・研究のみ。実売買・発注は行わない。weights.json も更新しない。
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from score_prediction_log import (
    MAX_REFERENCE_ANCHOR_DEVIATION,
    _current_utc_date,
    load_ohlcv_frame,
    normalize_side,
)
from time_utils import format_utc, now_utc

LEDGER_PATH = Path("data/signal_log.csv")
OUT_CSV = Path("data/execution_simulation.csv")
RESULTS_DIR = Path("results")

FILL_WINDOW_BARS = 5   # 判断日を含む約定待ちバー数
EXIT_DEADLINE_BARS = 5  # 判断日からの決済期限(バー) — このバーの終値で時間切れ決済
COST_SENSITIVITY_R = (0.02, 0.05, 0.10)

COLUMNS = [
    "date", "signal_id", "asset", "side", "rank", "risk_pct",
    "entry_low", "entry_high", "sl", "tp1",
    "status",        # filled_sl / filled_tp1 / filled_time_exit / no_fill / open / excluded_scale / excluded_bad_levels / invalid_data / data_window_expired
    "fill_date", "fill_price", "risk_unit", "exit_date", "exit_price",
    "r_result", "capital_pct", "simulated_at_utc",
]


def _num(v) -> float:
    n = pd.to_numeric(v, errors="coerce")
    return float(n) if pd.notna(n) else float("nan")


def simulate_row(row: pd.Series, ohlcv: pd.DataFrame, simulated_at: str) -> dict:
    """台帳1行を擬似執行する(純関数)。曖昧さは不利側へ。"""
    side = normalize_side(row.get("side"))
    out = {
        "date": str(row.get("date") or ""),
        "signal_id": str(row.get("signal_id") or ""),
        "asset": str(row.get("asset") or ""),
        "side": side,
        "rank": str(row.get("rank") or "").strip().upper(),
        "risk_pct": _num(row.get("risk_pct")),
        "entry_low": _num(row.get("entry_low")),
        "entry_high": _num(row.get("entry_high")),
        "sl": _num(row.get("sl")),
        "tp1": _num(row.get("tp1")),
        "status": "invalid_data",
        "fill_date": "", "fill_price": np.nan, "risk_unit": np.nan,
        "exit_date": "", "exit_price": np.nan,
        "r_result": np.nan, "capital_pct": np.nan,
        "simulated_at_utc": simulated_at,
    }
    e1, e2, sl, tp1 = out["entry_low"], out["entry_high"], out["sl"], out["tp1"]
    if ohlcv.empty or side not in {"LONG", "SHORT"} or not (e1 == e1 and e2 == e2 and sl == sl):
        return out
    sig_date = pd.to_datetime(out["date"], errors="coerce")
    if pd.isna(sig_date):
        return out
    # 価格窓が信号日より後に始まる場合は約定探索をしない(監査P1-4a: rawは直近240日で
    # 上書きされるため、放置すると2027-02頃から古い判断が窓先頭のバーで「約定」する)。
    if sig_date.normalize() < pd.to_datetime(ohlcv["date"].iloc[0]):
        out["status"] = "data_window_expired"
        return out
    idx0 = int(ohlcv["date"].searchsorted(sig_date.normalize(), side="left"))
    if idx0 >= len(ohlcv):
        out["status"] = "open"  # 当日バー未取得(週末記帳など) — 次回実行で解決
        return out

    anchor_close = float(ohlcv.iloc[idx0]["close"])
    reference = (e1 + e2) / 2
    if anchor_close > 0 and abs(reference / anchor_close - 1.0) > MAX_REFERENCE_ANCHOR_DEVIATION:
        out["status"] = "excluded_scale"
        return out

    is_long = side == "LONG"
    fill_price = e2 if is_long else e1  # ゾーン内の最悪価格
    risk = abs(fill_price - sl)
    if risk <= 0:
        out["status"] = "excluded_bad_levels"
        return out
    out["risk_unit"] = round(risk, 6)

    deadline = idx0 + EXIT_DEADLINE_BARS
    fill_i = None
    for i in range(idx0, min(idx0 + FILL_WINDOW_BARS, len(ohlcv))):
        bar = ohlcv.iloc[i]
        if float(bar["low"]) <= e2 and float(bar["high"]) >= e1:
            fill_i = i
            break
    if fill_i is None:
        window_complete = (idx0 + FILL_WINDOW_BARS) <= len(ohlcv)
        out["status"] = "no_fill" if window_complete else "open"
        return out

    out["fill_date"] = str(ohlcv.iloc[fill_i]["date"].date())
    out["fill_price"] = round(fill_price, 6)

    def finish(status: str, i: int, price: float) -> dict:
        r = (price - fill_price) / risk if is_long else (fill_price - price) / risk
        out["status"] = status
        out["exit_date"] = str(ohlcv.iloc[i]["date"].date())
        out["exit_price"] = round(float(price), 6)
        out["r_result"] = round(float(r), 4)
        rp = out["risk_pct"]
        if rp == rp:
            out["capital_pct"] = round(float(r) * rp, 4)
        return out

    # 約定足: SLのみ判定(順序不明 → 不利側)。TP1は翌足以降
    bar = ohlcv.iloc[fill_i]
    sl_hit = float(bar["low"]) <= sl if is_long else float(bar["high"]) >= sl
    if sl_hit:
        return finish("filled_sl", fill_i, sl)

    for i in range(fill_i + 1, min(deadline + 1, len(ohlcv))):
        bar = ohlcv.iloc[i]
        sl_hit = float(bar["low"]) <= sl if is_long else float(bar["high"]) >= sl
        if sl_hit:  # SLとTP1が同じ足なら SL優先(不利側)
            return finish("filled_sl", i, sl)
        if tp1 == tp1:
            tp_hit = float(bar["high"]) >= tp1 if is_long else float(bar["low"]) <= tp1
            if tp_hit:
                return finish("filled_tp1", i, tp1)
    if deadline < len(ohlcv):
        # 期限バーが形成途中(ラベル日がUTCでまだ過ぎていない)なら時間決済を確定しない
        # (#137 Codex P2と同型: 日中値を終値決済として記録しない)。
        if pd.Timestamp(ohlcv.iloc[deadline]["date"]).normalize() < _current_utc_date():
            return finish("filled_time_exit", deadline, float(ohlcv.iloc[deadline]["close"]))
    out["status"] = "open"  # 期限バー未到来/未確定 — 正直に進行中
    return out


def simulate_ledger(ledger: pd.DataFrame, raw_dir: Path | None = None) -> pd.DataFrame:
    if ledger is None or ledger.empty:
        return pd.DataFrame(columns=COLUMNS)
    simulated_at = format_utc(now_utc())
    kwargs = {"raw_dir": raw_dir} if raw_dir is not None else {}
    cache: dict[str, pd.DataFrame] = {}
    rows = []
    for _, row in ledger.iterrows():
        side = normalize_side(row.get("side"))
        rank = str(row.get("rank") or "").strip().upper()
        rp = _num(row.get("risk_pct"))
        if side not in {"LONG", "SHORT"} or rank not in {"A", "B"} or not (rp == rp and rp > 0):
            continue  # 「朝に指値を出したもの」のみが対象
        asset = str(row.get("asset") or "")
        if asset not in cache:
            cache[asset] = load_ohlcv_frame(asset, **kwargs) if kwargs else load_ohlcv_frame(asset)
        rows.append(simulate_row(row, cache[asset], simulated_at))
    return pd.DataFrame(rows, columns=COLUMNS)


def summarize(sim: pd.DataFrame) -> dict:
    resolved_status = {"filled_sl", "filled_tp1", "filled_time_exit"}
    out = {
        "orders": int(len(sim)),
        "excluded_scale": 0, "excluded_bad_levels": 0, "invalid_data": 0,
        "no_fill": 0, "open": 0, "data_window_expired": 0, "fills_resolved": 0,
        "exit_breakdown": {}, "win_rate": None,
        "gross_total_r": None, "avg_r": None, "gross_capital_pct": None,
        "cost_sensitivity_r": {},
        "policy": {
            "fill_window_bars": FILL_WINDOW_BARS,
            "exit_deadline_bars": EXIT_DEADLINE_BARS,
            "conservative_rules": "worst-in-zone fill; same-bar SL loses; TP1 next-bar-only; SL priority",
            "costs": "not deducted (unsourced); sensitivity in R below",
        },
        "requires_human_approval": True,
        "connected_to_signal_score": False,
    }
    if sim.empty:
        return out
    counts = sim["status"].value_counts()
    # data_window_expired もサマリーで数える(#128 Codex P2: 表示カテゴリから消えると
    # ガード発動時に注文内訳が照合不能になる)
    for k in ("excluded_scale", "excluded_bad_levels", "invalid_data", "no_fill", "open", "data_window_expired"):
        out[k] = int(counts.get(k, 0))
    resolved = sim[sim["status"].isin(resolved_status)].copy()
    out["fills_resolved"] = int(len(resolved))
    if resolved.empty:
        return out
    out["exit_breakdown"] = {k: int(v) for k, v in resolved["status"].value_counts().items()}
    r = pd.to_numeric(resolved["r_result"], errors="coerce").dropna()
    out["gross_total_r"] = round(float(r.sum()), 2)
    out["avg_r"] = round(float(r.mean()), 3)
    out["win_rate"] = round(float((r > 0).mean()), 3)
    cap = pd.to_numeric(resolved["capital_pct"], errors="coerce").dropna()
    out["gross_capital_pct"] = round(float(cap.sum()), 2)
    for c in COST_SENSITIVITY_R:
        out["cost_sensitivity_r"][f"{c:.2f}R"] = round(float(r.sum() - c * len(r)), 2)
    return out


def main() -> int:
    ledger = pd.read_csv(LEDGER_PATH, dtype=str, keep_default_na=False) if LEDGER_PATH.exists() else pd.DataFrame()
    sim = simulate_ledger(ledger)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    sim.to_csv(OUT_CSV, index=False)
    summary = summarize(sim)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "execution_simulation_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"execution simulation: {len(sim)} orders -> {OUT_CSV}")
    print(json.dumps({k: summary[k] for k in ("orders", "fills_resolved", "no_fill", "open", "gross_total_r", "win_rate", "gross_capital_pct")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
