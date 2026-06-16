"""JP One-Share Swing 評価エンジン (JP-EVAL-001)。

約定済み仮説の評価を行う。

設計上の制約:
- horizon は 10/20/30 営業日（固定）
- 1日ラグを考慮した「約定日 = 注文日 + 1営業日」を前提とする
- outcome_type A〜F の自動推定は補助的なもの。thesis_correct / timing_correct / execution_degraded
  は人間が記入する（機械的に決定できない）
- yfinance で JP 株 OHLCV を取得する（ticker は '7203.T' 形式）

False-confidence ルール（TSO 安全思想から継承）:
  「データ不足 → 不明」。outcome が判定できない場合は open_unresolved。
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd

import jp_one_share_cost as cost_lib
import jp_swing_ledger as ledger

try:
    import yfinance as yf
    _YF_AVAILABLE = True
except ImportError:
    _YF_AVAILABLE = False


# ── OHLCV 取得 ────────────────────────────────────────────────────

def fetch_ohlcv(ticker: str, start: str, end: str) -> pd.DataFrame:
    """yfinance で日次 OHLCV を取得する。失敗時は空 DataFrame。

    ticker: '7203.T' 形式。start/end: 'YYYY-MM-DD'。
    """
    if not _YF_AVAILABLE:
        return pd.DataFrame()
    try:
        raw = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
    except Exception:
        return pd.DataFrame()
    if raw.empty:
        return pd.DataFrame()
    df = raw.copy()
    df.columns = [str(c).lower() for c in df.columns]
    df.index = pd.to_datetime(df.index)
    df = df.reset_index().rename(columns={"index": "date", "Date": "date"})
    df["date"] = pd.to_datetime(df["date"], utc=False).dt.normalize()
    for col in ["open", "high", "low", "close"]:
        if col not in df.columns:
            df[col] = np.nan
    return df.dropna(subset=["date", "open", "high", "low", "close"]).sort_values("date")


# ── 評価ロジック ──────────────────────────────────────────────────

def _coerce(value: Any, fallback: float = float("nan")) -> float:
    try:
        v = float(value)
    except (TypeError, ValueError):
        return fallback
    if math.isnan(v) or math.isinf(v):
        return fallback
    return v


def evaluate_signal(
    row: dict[str, Any],
    ohlcv: pd.DataFrame | None = None,
    cost_cfg: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """仮説台帳の1行を評価する。

    ohlcv が None のときは yfinance で自動取得を試みる。
    評価できない場合は status=open のまま返す。
    """
    ticker = str(row.get("ticker", ""))
    entry_date_str = str(row.get("actual_entry_date", "") or row.get("order_date", ""))
    entry_price = _coerce(row.get("actual_entry_price"))
    sl_price = _coerce(row.get("sl_price"))
    tp1_price = _coerce(row.get("tp1_price"))
    tp2_price = _coerce(row.get("tp2_price"))
    shares = int(_coerce(row.get("shares", 0), 0))
    horizon = int(_coerce(row.get("horizon_days", 20), 20))
    cfg = cost_cfg if cost_cfg is not None else cost_lib.broker_config()

    result: dict[str, Any] = {k: row.get(k) for k in ledger.JP_SIGNAL_COLUMNS}
    result["status"] = str(row.get("status", "pending"))

    if result["status"] == "closed":
        return result

    if math.isnan(entry_price) or entry_price <= 0.0 or shares <= 0:
        return result  # 未約定

    result["status"] = "open"

    if ohlcv is None:
        try:
            entry_dt = pd.Timestamp(entry_date_str)
        except Exception:
            return result
        end_dt = entry_dt + pd.offsets.BDay(horizon + 5)
        ohlcv = fetch_ohlcv(ticker, start=str(entry_dt.date()), end=str(end_dt.date()))

    if ohlcv is None or ohlcv.empty:
        return result

    # エントリー日以降の足
    try:
        entry_dt = pd.Timestamp(entry_date_str)
    except Exception:
        return result

    future = ohlcv[ohlcv["date"] > entry_dt].head(horizon)
    if future.empty:
        return result

    risk_per_share = entry_price - sl_price
    risk_jpy = risk_per_share * shares if risk_per_share > 0.0 else 0.0

    sl_hit = False
    tp1_hit = False
    tp2_hit = False
    sl_hit_date = None
    tp1_hit_date = None
    tp2_hit_date = None
    exit_price_eval = entry_price
    exit_date_eval = None

    for _, bar in future.iterrows():
        bar_date = bar["date"]
        bar_low = float(bar["low"])
        bar_high = float(bar["high"])

        if not math.isnan(sl_price) and bar_low <= sl_price:
            sl_hit = True
            sl_hit_date = bar_date
            exit_price_eval = sl_price
            exit_date_eval = bar_date
            break

        if not math.isnan(tp1_price) and bar_high >= tp1_price:
            tp1_hit = True
            tp1_hit_date = bar_date
            if not exit_date_eval:
                exit_price_eval = tp1_price
                exit_date_eval = bar_date

        if not math.isnan(tp2_price) and bar_high >= tp2_price:
            tp2_hit = True
            tp2_hit_date = bar_date
            exit_price_eval = tp2_price
            exit_date_eval = bar_date
            break

    # 時間切れの場合は最終足の終値で仮評価
    time_exit = not sl_hit and not tp2_hit
    if time_exit and not exit_date_eval:
        last_bar = future.iloc[-1]
        exit_price_eval = float(last_bar["close"])
        exit_date_eval = last_bar["date"]

    # PnL 計算
    gross_pnl = (exit_price_eval - entry_price) * shares
    buy_fee = cost_lib.buy_commission(entry_price, shares, cfg)
    sell_fee = cost_lib.sell_commission(exit_price_eval, shares, cfg)
    net_pnl = gross_pnl - buy_fee - sell_fee

    g_r = gross_pnl / risk_jpy if risk_jpy > 0.0 else 0.0
    n_r = net_pnl / risk_jpy if risk_jpy > 0.0 else 0.0

    holding_days = len(future[future["date"] <= exit_date_eval]) if exit_date_eval else len(future)

    result["sl_price"] = sl_price
    result["tp1_price"] = tp1_price
    result["tp2_price"] = tp2_price if not math.isnan(tp2_price) else result["tp2_price"]
    result["exit_date"] = str(exit_date_eval.date()) if exit_date_eval else result["exit_date"]
    result["exit_price"] = round(exit_price_eval, 2)
    result["exit_reason"] = (
        "sl_hit" if sl_hit else
        "tp2_hit" if tp2_hit else
        "tp1_hit" if tp1_hit else
        "time_exit"
    )
    result["holding_days"] = holding_days
    result["buy_fee_jpy"] = round(buy_fee, 0)
    result["sell_fee_jpy"] = round(sell_fee, 0)
    result["gross_pnl_jpy"] = round(gross_pnl, 0)
    result["net_pnl_jpy"] = round(net_pnl, 0)
    result["risk_jpy"] = round(risk_jpy, 0)
    result["gross_r"] = round(g_r, 3)
    result["net_r"] = round(n_r, 3)
    result["status"] = "closed" if (sl_hit or tp2_hit or time_exit) else "open"

    # outcome_type の補助推定（thesis_correct等の人間入力が優先）
    result["outcome_type"] = _suggest_outcome(result, row)

    # execution_degraded の自動チェック
    if not result.get("execution_degraded"):
        effective_rate = cost_lib.effective_fee_rate(entry_price, shares, cfg)
        result["execution_degraded"] = bool(effective_rate > 0.02)  # コスト率 2%超で自動フラグ

    return result


def _suggest_outcome(result: dict[str, Any], original_row: dict[str, Any]) -> str:
    """outcome_type を補助推定する。確定は人間の判断が優先。

    thesis_correct / timing_correct が記入済みの場合はそれを優先する。
    """
    # 人間が既に記入していれば維持
    existing = str(original_row.get("outcome_type", "")).strip()
    if existing and existing in ledger.OUTCOME_TYPES:
        return existing

    thesis_correct = str(original_row.get("thesis_correct", "")).strip().lower()
    timing_correct = str(original_row.get("timing_correct", "")).strip().lower()
    execution_degraded = str(result.get("execution_degraded", "")).strip().lower()
    exit_reason = str(result.get("exit_reason", ""))
    net_r = _coerce(result.get("net_r", float("nan")))

    win = exit_reason in {"tp1_hit", "tp2_hit"} or (not math.isnan(net_r) and net_r > 0.0)
    loss = exit_reason == "sl_hit" or (not math.isnan(net_r) and net_r < 0.0)

    if execution_degraded in {"true", "1", "yes"} and loss:
        return "C"
    if thesis_correct == "true" and timing_correct == "true" and win:
        return "A"
    if thesis_correct == "true" and timing_correct == "false":
        return "B"
    if thesis_correct == "false" and win:
        return "F"
    if thesis_correct == "false" and loss:
        return "D"
    # 判定不能 → open_unresolved（false-confidence ルール）
    return ""


# ── 集計 ─────────────────────────────────────────────────────────

def summarize(df: pd.DataFrame) -> dict[str, Any]:
    """台帳全体のサマリーを返す（ダッシュボード用）。"""
    closed = df[df["status"] == "closed"].copy()
    total = len(df)
    n_closed = len(closed)
    n_open = len(df[df["status"] == "open"])

    summary: dict[str, Any] = {
        "total_hypotheses": total,
        "closed": n_closed,
        "open": n_open,
        "pending": len(df[df["status"] == "pending"]),
    }

    if n_closed == 0:
        summary["insufficient_data"] = True
        return summary

    def safe_float_col(col: str) -> pd.Series:
        return pd.to_numeric(closed[col], errors="coerce")

    net_rs = safe_float_col("net_r")
    gross_rs = safe_float_col("gross_r")
    wins = (net_rs > 0).sum()
    losses = (net_rs < 0).sum()

    summary["win_rate"] = round(wins / n_closed, 3) if n_closed > 0 else None
    summary["avg_net_r"] = round(float(net_rs.mean()), 3) if not net_rs.isna().all() else None
    summary["avg_gross_r"] = round(float(gross_rs.mean()), 3) if not gross_rs.isna().all() else None
    summary["total_net_pnl_jpy"] = int(safe_float_col("net_pnl_jpy").sum())

    # outcome 分布
    outcome_counts: dict[str, int] = {k: 0 for k in ledger.OUTCOME_TYPES}
    for ot in closed["outcome_type"].dropna():
        ot_str = str(ot).strip()
        if ot_str in outcome_counts:
            outcome_counts[ot_str] += 1
    summary["outcome_distribution"] = outcome_counts

    # calibration: confidence_pct が記入済みの closed 行のみ
    conf_col = safe_float_col("confidence_pct")
    valid = closed[conf_col.notna() & net_rs.notna()].copy()
    if len(valid) >= 5:
        conf_mean = float(conf_col[conf_col.index.isin(valid.index)].mean())
        actual_wr = float((net_rs[net_rs.index.isin(valid.index)] > 0).mean())
        summary["calibration"] = {
            "avg_confidence_pct": round(conf_mean, 1),
            "actual_win_rate": round(actual_wr, 3),
            "gap": round(conf_mean / 100.0 - actual_wr, 3),
            "n": len(valid),
        }
    else:
        summary["calibration"] = {"insufficient_data": True, "n": len(valid)}

    return summary
