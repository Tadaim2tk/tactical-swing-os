"""取引コストモデル (SPEC-TC-001)。

仮想評価のグロスR(コストゼロ)を、実戦のネットR(スプレッド・手数料・スワップ控除後)
へ変換する。XMTradingで実資金を運用する段階では、紙の上の勝ち筋と実際に資金が
増える筋を分離する必要がある。

設計原則(憲章「証拠主義」):
- コストは出典(source)なしには採用しない。config/cost_model.json の初期値は全て0で、
  ネットR=グロスRに一致する(後方互換)。実測値を source 付きで記入して初めて効く。
- price単位は各アセットの建値と同一(USDJPY=円、BTC=米ドル、指数=ポイント)。
- scipy等の追加依存なし(標準ライブラリのみ)。
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

CONFIG_PATH = Path("config/cost_model.json")

_ZERO_COST = {"spread": 0.0, "commission_round_turn": 0.0, "swap_per_bar": 0.0, "source": "unconfigured"}

# モジュール内キャッシュ(同一プロセスで何度も読まない)
_cache: dict[str, Any] | None = None


def load_cost_model(path: Path = CONFIG_PATH) -> dict[str, Any]:
    global _cache
    if _cache is not None:
        return _cache
    if not path.exists():
        _cache = {"default": dict(_ZERO_COST), "assets": {}}
        return _cache
    try:
        with path.open(encoding="utf-8") as fh:
            data = json.load(fh)
    except (json.JSONDecodeError, OSError):
        _cache = {"default": dict(_ZERO_COST), "assets": {}}
        return _cache
    _cache = data
    return data


def reset_cache() -> None:
    """テスト用: 設定キャッシュを破棄する。"""
    global _cache
    _cache = None


def _coerce(value: Any, fallback: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return fallback
    if math.isnan(number) or math.isinf(number):
        return fallback
    return number


def asset_cost(asset: str, model: dict[str, Any] | None = None) -> dict[str, float]:
    """アセット別コスト定義を返す。未定義アセットは default にフォールバック。"""
    model = model or load_cost_model()
    default = {**_ZERO_COST, **(model.get("default") or {})}
    entry = (model.get("assets") or {}).get(str(asset), None)
    if not isinstance(entry, dict):
        entry = default
    return {
        "spread": _coerce(entry.get("spread"), _coerce(default.get("spread"))),
        "commission_round_turn": _coerce(entry.get("commission_round_turn"), _coerce(default.get("commission_round_turn"))),
        "swap_per_bar": _coerce(entry.get("swap_per_bar"), _coerce(default.get("swap_per_bar"))),
        "source": str(entry.get("source", default.get("source", "unconfigured"))),
    }


def cost_in_price(asset: str, bars_held: float, model: dict[str, Any] | None = None) -> float:
    """1取引あたりの往復コストを price 単位で返す。"""
    cost = asset_cost(asset, model)
    bars = max(0.0, _coerce(bars_held))
    return cost["spread"] + cost["commission_round_turn"] + cost["swap_per_bar"] * bars


def cost_r(asset: str, risk_per_unit: float, bars_held: float, model: dict[str, Any] | None = None) -> float:
    """往復コストを R 単位で返す。1R = risk_per_unit(建値→SLの価格距離)。

    risk が 0 以下/不正なら 0.0(評価不能時はコストを課さない)。
    """
    risk = _coerce(risk_per_unit)
    if risk <= 0.0:
        return 0.0
    return cost_in_price(asset, bars_held, model) / risk


def net_r(gross_r: float, asset: str, risk_per_unit: float, bars_held: float, model: dict[str, Any] | None = None) -> float:
    """グロスRからコストを控除したネットRを返す。コストは常に不利方向(減算)。"""
    return _coerce(gross_r) - cost_r(asset, risk_per_unit, bars_held, model)
