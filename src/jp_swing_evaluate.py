"""JP One-Share Swing 評価エンジン (JP-EVAL-001 rev2)。

約定済み仮説の評価を行う。

─── 設計上の前提 ────────────────────────────────────────────────────
・horizon は 10/20/30 営業日（fixed）
・評価開始は actual_execution_date の翌日（>）。
  理由: ワン株は寄付約定。約定日のバーは入場価格を含むため同日 SL/TP を
  チェックすると「約定直後に即 SL 判定」という論理矛盾が起きる。
  同日チェックを外すことで「約定後の値動き」のみを評価対象にする。
  これは意図的な除外であり、ドキュメントとテストで明示する。
・SL/TP 未達かつ len(future) < horizon の場合は status=open のまま返す。
  False-confidence rule: horizon 到達前のデータ不足を早仕舞いと混同しない。

─── コスト計算の分離方針 ────────────────────────────────────────────
net_pnl_jpy = gross_pnl - buy_fee - sell_fee
  gross_pnl = (exit_price - actual_entry_price) × shares
  actual_entry_price にはラグコストが既に埋め込まれている。

execution_lag_cost_jpy = (actual_entry_price - expected_entry_price) × shares
  【帰因(attribution)専用・signed value】
  net_pnl には含めない（二重計上防止）。
  正 → 想定より高く買わされた（ラグが不利に働いた）
  負 → 想定より安く買えた（ラグが有利に働いた）

─── 補助フラグと outcome 推定の順序 ─────────────────────────────────
evaluation_hurt は機械的に推定できる唯一のフラグ（fee率 or ラグ率が閾値超）。
_suggest_outcome() がこの値を使って outcome C を判定できるよう、
execution_hurt の自動補完は必ず _suggest_outcome() より先に行う。

thesis_hit / timing_hit は機械判定できない。人間が記入する。
最終確定は人間が記入する（false-confidence ルール）。
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

    フィールド名は JP_SIGNAL_COLUMNS（rev2）に準拠:
      actual_execution_date  — 約定日（旧: actual_entry_date / order_date）
      thesis_hit             — 仮説が正しかったか（旧: thesis_correct）
      timing_hit             — タイミングが正しかったか（旧: timing_correct）
      execution_hurt         — ラグ/費用で実質不利だったか（旧: execution_degraded）

    ohlcv が None のときは yfinance で自動取得を試みる。
    評価できない場合は status=open のまま返す。
    """
    ticker = str(row.get("ticker", ""))
    # actual_execution_date が主キー（旧 actual_entry_date / order_date は参照しない）
    exec_date_str = str(row.get("actual_execution_date", "") or "").strip()
    entry_price = _coerce(row.get("actual_entry_price"))
    expected_price = _coerce(row.get("expected_entry_price"))
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

    if not exec_date_str or math.isnan(entry_price) or entry_price <= 0.0 or shares <= 0:
        return result  # 未約定 or 必須項目欠落 → pending のまま

    result["status"] = "open"

    if ohlcv is None:
        try:
            exec_dt = pd.Timestamp(exec_date_str)
        except Exception:
            return result
        end_dt = exec_dt + pd.offsets.BDay(horizon + 5)
        ohlcv = fetch_ohlcv(ticker, start=str(exec_dt.date()), end=str(end_dt.date()))

    if ohlcv is None or ohlcv.empty:
        return result

    try:
        exec_dt = pd.Timestamp(exec_date_str)
    except Exception:
        return result

    # 約定日の翌日から評価（設計上の除外: モジュール冒頭のコメント参照）
    future = ohlcv[ohlcv["date"] > exec_dt].head(horizon)
    if future.empty:
        return result

    # execution_lag_cost_jpy はデータ不足でも記録する（帰因専用）
    lag_cost = (
        cost_lib.execution_lag_cost_jpy(expected_price, entry_price, shares)
        if not math.isnan(expected_price) and not math.isnan(entry_price)
        else 0.0
    )
    result["execution_lag_cost_jpy"] = round(lag_cost, 0)

    risk_per_share = entry_price - sl_price
    risk_jpy = risk_per_share * shares if risk_per_share > 0.0 else 0.0

    sl_hit = False
    tp1_hit = False
    tp2_hit = False
    exit_price_eval = entry_price
    exit_date_eval = None

    for _, bar in future.iterrows():
        bar_date = bar["date"]
        bar_low = float(bar["low"])
        bar_high = float(bar["high"])

        if not math.isnan(sl_price) and bar_low <= sl_price:
            sl_hit = True
            exit_price_eval = sl_price
            exit_date_eval = bar_date
            break

        if not math.isnan(tp1_price) and bar_high >= tp1_price:
            tp1_hit = True
            if not exit_date_eval:
                exit_price_eval = tp1_price
                exit_date_eval = bar_date

        if not math.isnan(tp2_price) and bar_high >= tp2_price:
            tp2_hit = True
            exit_price_eval = tp2_price
            exit_date_eval = bar_date
            break

    # tp1 が唯一の利確目標（tp2 未定義）の場合はそこで閉じる
    tp1_is_final = tp1_hit and math.isnan(tp2_price)

    # time_exit は horizon 本数に到達したときだけ（データ不足は open のまま）
    time_exit = not sl_hit and not tp2_hit and not tp1_is_final and len(future) >= horizon

    if not (sl_hit or tp2_hit or tp1_is_final or time_exit):
        # SL/TP 未達かつ horizon 未満 → データ不足、閉じない
        return result

    if time_exit and not exit_date_eval:
        last_bar = future.iloc[-1]
        exit_price_eval = float(last_bar["close"])
        exit_date_eval = last_bar["date"]

    # PnL 計算 ─ net_pnl = gross_pnl - fees のみ（ラグコストは含まない）
    gross_pnl = (exit_price_eval - entry_price) * shares
    buy_fee = cost_lib.buy_commission(entry_price, shares, cfg)
    sell_fee = cost_lib.sell_commission(exit_price_eval, shares, cfg)
    net_pnl = gross_pnl - buy_fee - sell_fee

    g_r = gross_pnl / risk_jpy if risk_jpy > 0.0 else 0.0
    n_r = net_pnl / risk_jpy if risk_jpy > 0.0 else 0.0

    holding_days = len(future[future["date"] <= exit_date_eval]) if exit_date_eval else len(future)

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
    result["status"] = "closed"

    # execution_hurt 自動フラグ（人間未記入の場合のみ）
    # ★ _suggest_outcome() より前に設定すること（outcome C 判定に使われるため）
    raw_hurt = str(row.get("execution_hurt", "")).strip().lower()
    if raw_hurt not in {"true", "false", "1", "0", "yes", "no"}:
        effective_rate = cost_lib.effective_fee_rate(entry_price, shares, cfg)
        result["execution_hurt"] = bool(
            effective_rate > 0.02 or abs(lag_cost) / (entry_price * shares) > 0.01
        )

    # outcome_type 補助推定（execution_hurt 自動フラグ設定後に呼ぶ）
    result["outcome_type"] = _suggest_outcome(result, row)

    return result


def _suggest_outcome(result: dict[str, Any], original_row: dict[str, Any]) -> str:
    """outcome_type を補助推定する（確定は人間の記入が優先）。

    フラグ名（rev2）:
      thesis_hit / timing_hit → 人間入力のみ（original_row から読む）
      execution_hurt → 人間入力 or 自動補完（result からフォールバック）
    """
    existing = str(original_row.get("outcome_type", "")).strip()
    if existing and existing in ledger.OUTCOME_TYPES:
        return existing

    def _bool(key: str) -> str:
        return str(original_row.get(key, "")).strip().lower()

    def _bool_with_auto(key: str) -> str:
        """人間未記入のとき result（自動補完値）を使う。"""
        v = str(original_row.get(key, "")).strip().lower()
        if v not in {"true", "false", "1", "0", "yes", "no"}:
            v = str(result.get(key, "")).strip().lower()
        return v

    thesis_hit = _bool("thesis_hit")
    timing_hit = _bool("timing_hit")
    execution_hurt = _bool_with_auto("execution_hurt")  # 自動補完フォールバック
    exit_reason = str(result.get("exit_reason", ""))
    net_r_val = _coerce(result.get("net_r", float("nan")))

    win = exit_reason in {"tp1_hit", "tp2_hit"} or (not math.isnan(net_r_val) and net_r_val > 0.0)
    loss = exit_reason == "sl_hit" or (not math.isnan(net_r_val) and net_r_val < 0.0)

    # 人間が thesis/timing を明示した場合は優先（A/B/F/D を先に決める）
    if thesis_hit == "true" and timing_hit == "true" and win:
        return "A"
    if thesis_hit == "true" and timing_hit == "false":
        return "B"
    if thesis_hit == "false" and win:
        return "F"
    if thesis_hit == "false" and loss:
        return "D"
    # C は thesis/timing 未設定かつ execution_hurt かつ loss のとき（実行コスト主因）
    if execution_hurt in {"true", "1", "yes"} and loss:
        return "C"
    return ""  # false-confidence: 判定不能は強制しない


# ── 集計 ─────────────────────────────────────────────────────────

def summarize(df: pd.DataFrame) -> dict[str, Any]:
    """台帳全体のサマリーを返す（ダッシュボード用）。"""
    closed = df[df["status"] == "closed"].copy()
    total = len(df)
    n_closed = len(closed)

    summary: dict[str, Any] = {
        "total_hypotheses": total,
        "closed": n_closed,
        "open": len(df[df["status"] == "open"]),
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

    summary["win_rate"] = round(wins / n_closed, 3) if n_closed > 0 else None
    summary["avg_net_r"] = round(float(net_rs.mean()), 3) if not net_rs.isna().all() else None
    summary["avg_gross_r"] = round(float(gross_rs.mean()), 3) if not gross_rs.isna().all() else None
    summary["total_net_pnl_jpy"] = int(safe_float_col("net_pnl_jpy").sum())
    summary["total_lag_cost_jpy"] = int(safe_float_col("execution_lag_cost_jpy").sum())

    outcome_counts: dict[str, int] = {k: 0 for k in ledger.OUTCOME_TYPES}
    for ot in closed["outcome_type"].dropna():
        ot_str = str(ot).strip()
        if ot_str in outcome_counts:
            outcome_counts[ot_str] += 1
    summary["outcome_distribution"] = outcome_counts

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
