"""ワン株（単元未満株）コストモデル (JP-COST-001)。

ワン株の手数料体系はCFDと異なり、取引金額 × 料率 と 最低手数料 の大きい方が片道ごとに発生する。
また注文→約定に1営業日のラグがある。

証拠主義（既存 cost_model.py と同じ思想）:
  source が未設定(unconfigured) のコストは、値が非ゼロでも net R に採用しない。

足切り判定:
  min_fee_dominates(): 最低手数料が料率より高い（数千円台の低価格株で発生しやすい）。
  fee_viable(): 想定利益に対してコストが過大かどうかの目安。
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

CONFIG_PATH = Path("config/jp_cost_model.json")
BROKER_KEY = "monex_wankabu"

UNSOURCED_VALUES = {"", "unconfigured", "placeholder", "none", "tbd"}

_cache: dict[str, Any] | None = None


def load_jp_cost_model(path: Path = CONFIG_PATH) -> dict[str, Any]:
    global _cache
    if _cache is not None:
        return _cache
    if not path.exists():
        _cache = {}
        return _cache
    try:
        with path.open(encoding="utf-8") as fh:
            data = json.load(fh)
    except (json.JSONDecodeError, OSError):
        _cache = {}
        return _cache
    _cache = data
    return data


def reset_cache() -> None:
    global _cache
    _cache = None


def _coerce(value: Any, fallback: float = 0.0) -> float:
    try:
        n = float(value)
    except (TypeError, ValueError):
        return fallback
    if math.isnan(n) or math.isinf(n):
        return fallback
    return n


def is_sourced(source: Any) -> bool:
    return str(source).strip().lower() not in UNSOURCED_VALUES


def broker_config(model: dict[str, Any] | None = None) -> dict[str, Any]:
    """BROKER_KEY のコンフィグを返す。source 判定込み。"""
    m = model if model is not None else load_jp_cost_model()
    raw = m.get(BROKER_KEY, {})
    source = str(raw.get("source", "unconfigured"))
    return {
        "buy_rate": _coerce(raw.get("buy_rate")),
        "buy_min_fee": _coerce(raw.get("buy_min_fee")),
        "sell_rate": _coerce(raw.get("sell_rate")),
        "sell_min_fee": _coerce(raw.get("sell_min_fee")),
        "tax_rate": _coerce(raw.get("tax_rate")),
        "execution_lag_days": int(_coerce(raw.get("execution_lag_days", 1))),
        "source": source,
        "source_date": str(raw.get("source_date", "")),
        "source_type": str(raw.get("source_type", "unconfigured")),
        "responsibility": str(raw.get("responsibility", "")),
        "sourced": is_sourced(source),
    }


def buy_commission(price: float, shares: int, cfg: dict[str, Any]) -> float:
    """買い片道手数料（円）。sourced でなければ 0.0。"""
    if not cfg.get("sourced", False):
        return 0.0
    p = _coerce(price)
    s = max(0, int(shares))
    rate_fee = p * s * cfg["buy_rate"] * (1.0 + cfg["tax_rate"])
    min_fee = cfg["buy_min_fee"]
    return max(rate_fee, min_fee)


def sell_commission(price: float, shares: int, cfg: dict[str, Any]) -> float:
    """売り片道手数料（円）。sourced でなければ 0.0。"""
    if not cfg.get("sourced", False):
        return 0.0
    p = _coerce(price)
    s = max(0, int(shares))
    rate_fee = p * s * cfg["sell_rate"] * (1.0 + cfg["tax_rate"])
    min_fee = cfg["sell_min_fee"]
    return max(rate_fee, min_fee)


def total_commission(entry_price: float, exit_price: float, shares: int,
                     cfg: dict[str, Any]) -> float:
    """往復手数料合計（円）。"""
    return buy_commission(entry_price, shares, cfg) + sell_commission(exit_price, shares, cfg)


def net_r(entry_price: float, exit_price: float, sl_price: float, shares: int,
          cfg: dict[str, Any]) -> float:
    """ロングポジションのネットR。
    risk = (entry - sl) * shares。 sl >= entry または shares<=0 なら 0.0。
    """
    ep = _coerce(entry_price)
    xp = _coerce(exit_price)
    sp = _coerce(sl_price)
    sh = max(0, int(shares))
    risk = (ep - sp) * sh
    if risk <= 0.0 or sh == 0:
        return 0.0
    gross_pnl = (xp - ep) * sh
    fees = total_commission(ep, xp, sh, cfg)
    return (gross_pnl - fees) / risk


def gross_r(entry_price: float, exit_price: float, sl_price: float, shares: int) -> float:
    """ロングポジションのグロスR（手数料なし）。"""
    ep = _coerce(entry_price)
    xp = _coerce(exit_price)
    sp = _coerce(sl_price)
    sh = max(0, int(shares))
    risk = (ep - sp) * sh
    if risk <= 0.0 or sh == 0:
        return 0.0
    return ((xp - ep) * sh) / risk


def min_fee_dominates(price_per_share: float, cfg: dict[str, Any]) -> bool:
    """最低手数料が料率より高い（= 実効コスト率が表面料率より悪化）。

    数千円台の低価格株で起きやすい。1株分のコストを基準に判定する。
    sourced でない場合は判定不能として False を返す。
    """
    if not cfg.get("sourced", False):
        return False
    p = _coerce(price_per_share)
    if p <= 0.0:
        return False
    rate_fee = p * cfg["sell_rate"] * (1.0 + cfg["tax_rate"])
    return rate_fee < cfg["sell_min_fee"]


def effective_fee_rate(price_per_share: float, shares: int, cfg: dict[str, Any]) -> float:
    """往復実効コスト率（手数料/ポジション価値）。sourced でなければ 0.0。"""
    p = _coerce(price_per_share)
    sh = max(1, int(shares))
    position_value = p * sh
    if not cfg.get("sourced", False) or position_value <= 0.0:
        return 0.0
    total = buy_commission(p, sh, cfg) + sell_commission(p, sh, cfg)
    return total / position_value


def fee_viable(entry_price: float, shares: int, expected_gain_pct: float,
               cfg: dict[str, Any]) -> bool:
    """期待利益率がコスト率の2倍以上あるかの目安チェック。

    sourced でない場合は True を返す（コスト不明なら足切りしない）。
    """
    if not cfg.get("sourced", False):
        return True
    rate = effective_fee_rate(entry_price, shares, cfg)
    return _coerce(expected_gain_pct) / 100.0 >= rate * 2.0


def lag_adjusted_edge(
    current_price: float,
    expected_entry_price: float,
    tp1_price: float,
    sl_price: float,
) -> dict[str, float]:
    """1日ラグ後の期待値残存チェック。

    ラグによって想定エントリーが current_price より不利になった場合、
    R倍率とリスクリワードがどう変化するかを返す。
    current_price: ラグ前（仮説形成時）の価格
    expected_entry_price: ラグ後の想定約定価格（翌営業日寄付値の推定）
    """
    cp = _coerce(current_price)
    ep = _coerce(expected_entry_price)
    tp = _coerce(tp1_price)
    sp = _coerce(sl_price)

    risk_now = cp - sp if cp > sp else 0.0
    risk_lag = ep - sp if ep > sp else 0.0
    reward_now = tp - cp if tp > cp else 0.0
    reward_lag = tp - ep if tp > ep else 0.0

    rr_now = reward_now / risk_now if risk_now > 0.0 else 0.0
    rr_lag = reward_lag / risk_lag if risk_lag > 0.0 else 0.0

    lag_slippage_pct = (ep - cp) / cp * 100.0 if cp > 0.0 else 0.0

    return {
        "rr_now": round(rr_now, 3),
        "rr_lag": round(rr_lag, 3),
        "rr_degradation": round(rr_now - rr_lag, 3),
        "lag_slippage_pct": round(lag_slippage_pct, 3),
        "edge_survives": rr_lag >= 1.5,
    }


def execution_lag_cost_jpy(expected_price: float, actual_price: float, shares: int) -> float:
    """1日ラグによる価格劣化コスト（円）。

    ロングポジションでは、実際の約定価格が想定より高いほどコストが増える。
    execution_lag_cost = (actual_price - expected_price) * shares
    正なら不利（ラグでコスト増）、負なら有利（ラグで得）。

    手数料とは別に、台帳の execution_lag_cost_jpy フィールドへ記録する。
    """
    ep = _coerce(expected_price)
    ap = _coerce(actual_price)
    sh = max(0, int(shares))
    return (ap - ep) * sh


def validate_jp_cost_model(model: dict[str, Any] | None = None) -> list[dict[str, str]]:
    """証拠主義の機械的検証。問題のあるフィールドを列挙する。"""
    m = model if model is not None else load_jp_cost_model()
    cfg = broker_config(m)
    issues: list[dict[str, str]] = []

    nonzero = any(cfg[k] != 0.0 for k in ("buy_rate", "buy_min_fee", "sell_rate", "sell_min_fee"))
    if nonzero and not cfg["sourced"]:
        issues.append({
            "field": "source",
            "issue": "unsourced_nonzero_cost",
            "detail": "非ゼロコストだが source が未設定。証拠主義により net R へ採用されません。",
        })
    if cfg["sourced"]:
        if not cfg["source_date"].strip():
            issues.append({"field": "source_date", "issue": "missing_source_date",
                           "detail": "source_date が未記入です。"})
        if cfg["source_type"].strip().lower() not in {"published_spec", "measured"}:
            issues.append({"field": "source_type", "issue": "invalid_source_type",
                           "detail": "source_type は published_spec / measured のいずれかにしてください。"})
        if not cfg["responsibility"].strip():
            issues.append({"field": "responsibility", "issue": "missing_responsibility",
                           "detail": "responsibility が未記入です。"})
    return issues
