"""取引コストモデル (SPEC-TC-001 + Phase 26 証拠フレーム)。

仮想評価のグロスR(コストゼロ)を、実戦のネットR(スプレッド・手数料・スワップ控除後)
へ変換する。XMTradingで実資金を運用する段階では、紙の上の勝ち筋と実際に資金が
増える筋を分離する必要がある。

設計原則(憲章「証拠主義」):
- コストは出典(source)なしには採用しない。config/cost_model.json の初期値は全て0で、
  ネットR=グロスRに一致する(後方互換)。実測値/公開仕様を source 付きで記入して初めて効く。
- **機械的強制**: source が未設定(""/"unconfigured")のコストは、値が非ゼロでも
  net R 計算に採用しない(無効化)。捏造・無出典の数値が黙って評価へ混入するのを防ぐ。
- 出典メタ: source(出典) / source_date(取得日) / source_type(measured|published_spec) /
  responsibility(更新責任者) を各アセットに持たせる。
- price単位は各アセットの建値と同一(USDJPY=円、BTC=米ドル、指数=ポイント)。
- scipy等の追加依存なし(標準ライブラリのみ)。
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CONFIG_PATH = Path("config/cost_model.json")

# 出典付き(sourced)アセットが宣言すべき source_type。
# unconfigured は未宣言の状態であり、sourced なら不正(Phase 26.1)。
VALID_SOURCE_TYPES = {"measured", "published_spec"}

_ZERO_COST = {
    "spread": 0.0,
    "commission_round_turn": 0.0,
    "swap_per_bar": 0.0,
    "source": "unconfigured",
    "source_date": "",
    "source_type": "unconfigured",
    "responsibility": "",
}

# source がこれらのときは「未出典」とみなし、コストを採用しない。
UNSOURCED_VALUES = {"", "unconfigured", "placeholder", "none", "tbd"}

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


def is_sourced(source: Any) -> bool:
    """source が実出典(非空・未設定値でない)か。証拠主義の判定の単一情報源。"""
    return str(source).strip().lower() not in UNSOURCED_VALUES


def parse_iso_date(value):
    """厳格な YYYY-MM-DD 文字列を date へ。形式不正/実在しない日付なら None。

    前後空白は許容(strip)するが、ゼロ埋め必須("2026-6-6"は不正)。"""
    s = str(value).strip()
    try:
        parsed = datetime.strptime(s, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None
    # strptime は "2026-6-6" 等の非ゼロ埋めを許容するため、再シリアライズ一致で厳格化
    if parsed.strftime("%Y-%m-%d") != s:
        return None
    return parsed


def _today_utc():
    """境界が明確な「今日」。host のローカル日付(date.today())ではなく UTC を用いる。"""
    return datetime.now(timezone.utc).date()


def _resolve_entry(asset: str, model: dict[str, Any]) -> dict[str, Any]:
    """アセットの実効コスト定義を解決する(asset_cost と validate の単一情報源)。

    重要(証拠主義): **source はエントリ単位で解決する**。アセットが自前のエントリを
    持つ場合は、その source のみを採用し、default の source へはフォールバックしない。
    こうしないと「自前のコスト数値はあるが source を省いたアセット」が default の
    source を黙って継承し、無出典コストが net R に採用される証拠整合性バグになる。
    数値フィールドのみ default へフォールバックする(初期 default=0 なら無害)。
    アセットが config に存在しない場合のみ entry=default(=house-wide default を適用)。
    """
    default = {**_ZERO_COST, **(model.get("default") or {})}
    raw = (model.get("assets") or {}).get(str(asset), None)
    entry = raw if isinstance(raw, dict) else default
    source = str(entry.get("source", "unconfigured"))  # entry単位(default.sourceへフォールバックしない)
    return {
        "spread": _coerce(entry.get("spread"), _coerce(default.get("spread"))),
        "commission_round_turn": _coerce(entry.get("commission_round_turn"), _coerce(default.get("commission_round_turn"))),
        "swap_per_bar": _coerce(entry.get("swap_per_bar"), _coerce(default.get("swap_per_bar"))),
        "source": source,
        "source_date": str(entry.get("source_date", "")),
        "source_type": str(entry.get("source_type", "unconfigured")),
        "responsibility": str(entry.get("responsibility", "")),
        "sourced": is_sourced(source),
    }


def asset_cost(asset: str, model: dict[str, Any] | None = None) -> dict[str, Any]:
    """アセット別コスト定義(出典メタ込み)を返す。

    返す `sourced` は、出典が記入され採用可能かどうか(証拠主義ゲート)。
    source 解決は `_resolve_entry` に従い、自前 source を持たないアセットは未出典扱い。
    """
    return _resolve_entry(str(asset), model or load_cost_model())


def cost_in_price(asset: str, bars_held: float, model: dict[str, Any] | None = None) -> float:
    """1取引あたりの往復コストを price 単位で返す。

    出典が無い(sourced=False)場合は、値が非ゼロでも 0.0 を返す(証拠主義の機械的強制)。
    """
    cost = asset_cost(asset, model)
    if not cost["sourced"]:
        return 0.0
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


def validate_cost_model(model: dict[str, Any] | None = None, today: Any = None) -> list[dict[str, str]]:
    """証拠主義の機械的検証。問題のあるアセットを列挙する。

    - unsourced_nonzero_cost: 非ゼロコストだが出典が無い → net R に採用されず無視される
    - missing_source_date: 出典はあるが取得日が無い
    - invalid_source_date: 取得日が YYYY-MM-DD でない/実在しない (Phase 26.1)
    - future_source_date: 取得日が未来 (Phase 26.1)
    - invalid_source_type: sourced だが source_type が measured/published_spec でない (Phase 26.1)
    - missing_responsibility: 出典はあるが更新責任者が無い

    today: 未来日付判定の基準日(YYYY-MM-DD)。None または不正なら UTC基準の今日(_today_utc)。
    """
    model = model or load_cost_model()
    # today 未指定/不正なら UTC の今日へフォールバック(future チェックを黙って無効化しない)
    today_date = parse_iso_date(today) if today is not None else None
    if today_date is None:
        today_date = _today_utc()
    issues: list[dict[str, str]] = []
    assets = model.get("assets") or {}
    for asset, entry in assets.items():
        if not isinstance(entry, dict):
            continue
        # 実行時(asset_cost/cost_in_price)と同一の解決を使い、検証と実挙動を一致させる
        r = _resolve_entry(str(asset), model)
        a = str(asset)
        raw_nonzero = any(r[k] != 0.0 for k in ("spread", "commission_round_turn", "swap_per_bar"))
        if raw_nonzero and not r["sourced"]:
            issues.append({"asset": a, "issue": "unsourced_nonzero_cost",
                           "detail": "非ゼロコストだが出典なし。証拠主義によりnet Rへ採用されず無視されます。"})
        if not r["sourced"]:
            continue
        # --- 以下は sourced アセットのみ ---
        date_str = r["source_date"].strip()
        if not date_str:
            issues.append({"asset": a, "issue": "missing_source_date", "detail": "出典の取得日が未記入。"})
        else:
            parsed = parse_iso_date(date_str)
            if parsed is None:
                issues.append({"asset": a, "issue": "invalid_source_date", "detail": "取得日が YYYY-MM-DD 形式でない/実在しません。"})
            elif parsed > today_date:
                issues.append({"asset": a, "issue": "future_source_date", "detail": "取得日が未来です。"})
        if r["source_type"].strip().lower() not in VALID_SOURCE_TYPES:
            issues.append({"asset": a, "issue": "invalid_source_type",
                           "detail": "source_type は measured / published_spec のいずれかにしてください。"})
        if not r["responsibility"].strip():
            issues.append({"asset": a, "issue": "missing_responsibility", "detail": "更新責任者が未記入。"})
    return issues
