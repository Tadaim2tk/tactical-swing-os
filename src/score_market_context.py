"""score_market_context.py — 価格由来の市場コンテキストスコア(旧 score_narratives.py)。

2026-07 改名: このモジュールは価格データから risk_on/risk_off 等を推定する
**価格プロキシ**であり、文章(テキスト)ベースのナラティブ判断ではない。
文章系の意味ベクトル層 (build_narrative_memory / retrieve_similar_narratives) と
名前空間を分離するため score_market_context へ改名した (Phase 29.2 follow-up)。
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


SCORE_COLUMNS = [
    "risk_on_score",
    "risk_off_score",
    "dollar_strength_score",
    "rate_pressure_score",
    "gold_safe_haven_score",
    "oil_supply_risk_proxy_score",
    "crypto_liquidity_score",
    "equity_momentum_score",
    "volatility_stress_score",
    "narrative_confidence",
]
KEY_ASSETS = ["BTC", "GOLD", "WTI", "USDJPY", "SPX", "NASDAQ", "DXY", "VIX", "US10Y"]


@dataclass(frozen=True)
class MarketContext:
    changes: dict[str, float]
    available_assets: set[str]


def normalize_column_name(column: str) -> str:
    normalized = str(column).strip().lower().replace("-", "_")
    normalized = "_".join(normalized.split())
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    return normalized


def normalize_headers(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    out = df.copy()
    out.columns = [normalize_column_name(col) for col in out.columns]
    return out


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return round(max(low, min(high, value)), 2)


def directional_score(change_pct: float | None, positive_is_good: bool = True, sensitivity: float = 0.8) -> float:
    if change_pct is None or pd.isna(change_pct):
        return 50.0
    signed = change_pct if positive_is_good else -change_pct
    return clamp(50.0 + signed * sensitivity)


def asset_change_map(market_snapshot: pd.DataFrame) -> MarketContext:
    df = normalize_headers(market_snapshot)
    if df.empty or "asset" not in df.columns:
        return MarketContext(changes={}, available_assets=set())

    if "date" in df.columns:
        parsed = pd.to_datetime(df["date"], errors="coerce", utc=True).dt.tz_localize(None)
        if not parsed.dropna().empty:
            df = df.assign(_date=parsed)
            df = df.sort_values("_date").drop_duplicates(subset=["asset"], keep="last")

    changes: dict[str, float] = {}
    for _, row in df.iterrows():
        asset = str(row.get("asset", "")).strip().upper()
        if not asset:
            continue
        close = pd.to_numeric(row.get("close"), errors="coerce")
        open_ = pd.to_numeric(row.get("open"), errors="coerce")
        if pd.isna(close) or pd.isna(open_) or float(open_) == 0:
            continue
        changes[asset] = float((float(close) - float(open_)) / float(open_) * 100.0)
    return MarketContext(changes=changes, available_assets=set(changes))


def ch(context: MarketContext, asset: str) -> float | None:
    return context.changes.get(asset.upper())


def avg(values: list[float]) -> float:
    values = [v for v in values if not pd.isna(v)]
    return sum(values) / len(values) if values else 50.0


def score_market_narratives(market_snapshot: pd.DataFrame) -> pd.DataFrame:
    context = asset_change_map(market_snapshot)
    available_ratio = len(context.available_assets.intersection(KEY_ASSETS)) / len(KEY_ASSETS)
    confidence = clamp(35.0 + available_ratio * 65.0)

    risk_on = avg(
        [
            directional_score(ch(context, "SPX"), True, 1.1),
            directional_score(ch(context, "NASDAQ"), True, 1.1),
            directional_score(ch(context, "BTC"), True, 0.9),
            directional_score(ch(context, "VIX"), False, 1.0),
            directional_score(ch(context, "DXY"), False, 0.8),
        ]
    )
    risk_off = avg(
        [
            directional_score(ch(context, "VIX"), True, 1.2),
            directional_score(ch(context, "GOLD"), True, 0.8),
            directional_score(ch(context, "SPX"), False, 1.0),
            directional_score(ch(context, "NASDAQ"), False, 1.0),
            directional_score(ch(context, "DXY"), True, 0.7),
        ]
    )
    dollar = avg(
        [
            directional_score(ch(context, "DXY"), True, 1.2),
            directional_score(ch(context, "USDJPY"), True, 1.0),
            directional_score(ch(context, "GOLD"), False, 0.7),
        ]
    )
    rate = avg(
        [
            directional_score(ch(context, "US10Y"), True, 2.0),
            directional_score(ch(context, "NASDAQ"), False, 0.9),
            directional_score(ch(context, "GOLD"), False, 0.7),
        ]
    )
    gold_safe = avg(
        [
            directional_score(ch(context, "GOLD"), True, 1.0),
            directional_score(ch(context, "VIX"), True, 0.9),
            directional_score(ch(context, "DXY"), False, 0.4),
        ]
    )
    oil_supply = avg(
        [
            directional_score(ch(context, "WTI"), True, 1.2),
            directional_score(ch(context, "DXY"), False, 0.3),
            directional_score(ch(context, "SPX"), False, 0.2),
        ]
    )
    crypto_liquidity = avg(
        [
            directional_score(ch(context, "BTC"), True, 1.1),
            directional_score(ch(context, "NASDAQ"), True, 0.9),
            directional_score(ch(context, "DXY"), False, 0.9),
            directional_score(ch(context, "VIX"), False, 0.8),
        ]
    )
    equity_momentum = avg(
        [
            directional_score(ch(context, "SPX"), True, 1.1),
            directional_score(ch(context, "NASDAQ"), True, 1.1),
            directional_score(ch(context, "VIX"), False, 0.8),
        ]
    )
    vol_stress = avg(
        [
            directional_score(ch(context, "VIX"), True, 1.3),
            directional_score(ch(context, "SPX"), False, 0.9),
            directional_score(ch(context, "NASDAQ"), False, 0.9),
            directional_score(ch(context, "BTC"), False, 0.7),
        ]
    )

    row = {
        "asset": "GLOBAL",
        "risk_on_score": clamp(risk_on),
        "risk_off_score": clamp(risk_off),
        "dollar_strength_score": clamp(dollar),
        "rate_pressure_score": clamp(rate),
        "gold_safe_haven_score": clamp(gold_safe),
        "oil_supply_risk_proxy_score": clamp(oil_supply),
        "crypto_liquidity_score": clamp(crypto_liquidity),
        "equity_momentum_score": clamp(equity_momentum),
        "volatility_stress_score": clamp(vol_stress),
        "narrative_confidence": confidence,
    }

    rows = [row]
    for asset in sorted(context.available_assets):
        asset_row = row.copy()
        asset_row["asset"] = asset
        asset_row["asset_change_pct"] = round(context.changes[asset], 4)
        rows.append(asset_row)
    return pd.DataFrame(rows)


def market_mode_summary(scores: pd.DataFrame) -> str:
    if scores.empty:
        return "データ不足のため市場モード判定は未確定"
    row = scores.iloc[0]
    risk_on = float(row.get("risk_on_score", 50))
    risk_off = float(row.get("risk_off_score", 50))
    dollar = float(row.get("dollar_strength_score", 50))
    rate = float(row.get("rate_pressure_score", 50))
    vol = float(row.get("volatility_stress_score", 50))
    parts = []
    if risk_on >= risk_off + 8:
        parts.append("リスクオン優勢")
    elif risk_off >= risk_on + 8:
        parts.append("リスクオフ優勢")
    else:
        parts.append("リスクオン/オフは中立")
    parts.append("ドル高圧力あり" if dollar >= 58 else "ドル高圧力は限定的" if dollar <= 45 else "ドルは中立")
    parts.append("金利上昇圧力あり" if rate >= 58 else "金利圧力は限定的")
    parts.append("ボラティリティ警戒" if vol >= 58 else "ボラティリティは落ち着き")
    return " / ".join(parts)


def _global_scores(scores: pd.DataFrame) -> dict:
    if scores.empty:
        return {col: 50.0 for col in SCORE_COLUMNS}
    row = scores.iloc[0]
    return {col: float(row.get(col, 50.0)) for col in SCORE_COLUMNS}


def _side(signals_row) -> str:
    return str(signals_row.get("side", "")).upper()


def _asset(signals_row) -> str:
    return str(signals_row.get("asset", "")).upper()


def evaluate_signal_alignment(signals: pd.DataFrame, scores: pd.DataFrame) -> pd.DataFrame:
    sig = normalize_headers(signals)
    if sig.empty:
        return pd.DataFrame(
            columns=[
                "signal_id",
                "asset",
                "side",
                "rank",
                "recommended_action",
                "reason_codes",
                "narrative_alignment",
                "narrative_alignment_score",
                "narrative_comment",
            ]
        )
    score = _global_scores(scores)
    rows = []
    for _, row in sig.iterrows():
        asset = _asset(row)
        side = _side(row)
        signal_id = row.get("signal_id", "")
        rank = row.get("rank", "")
        recommended_action = row.get("recommended_action", row.get("type", ""))
        reason_codes = row.get("reason_codes", "")

        if score.get("narrative_confidence", 0) < 45:
            alignment_score = 0
            alignment = "insufficient_data"
            comment = "市場データが不足しているため、ナラティブ整合性は未判定です。"
        elif side in {"NONE", "NO_TRADE", ""} or str(rank).upper() == "NO_TRADE":
            alignment_score = 0
            alignment = "neutral"
            comment = "見送りシグナルのため、ナラティブは参考情報として扱います。"
        else:
            alignment_score, comment = alignment_for_asset(asset, side, score)
            if alignment_score >= 10:
                alignment = "aligned"
            elif alignment_score <= -10:
                alignment = "conflicted"
            else:
                alignment = "neutral"

        rows.append(
            {
                "signal_id": signal_id,
                "asset": asset,
                "side": side,
                "rank": rank,
                "recommended_action": recommended_action,
                "reason_codes": reason_codes,
                "narrative_alignment": alignment,
                "narrative_alignment_score": int(round(alignment_score)),
                "narrative_comment": comment,
            }
        )
    return pd.DataFrame(rows)


def alignment_for_asset(asset: str, side: str, score: dict) -> tuple[float, str]:
    direction = 1 if side == "LONG" else -1 if side == "SHORT" else 0
    if direction == 0:
        return 0.0, "売買方向が明確でないため中立評価です。"

    if asset == "BTC":
        base = (score["risk_on_score"] + score["crypto_liquidity_score"] - score["dollar_strength_score"] - score["volatility_stress_score"]) / 2
        comment = "BTCはリスクオン、流動性、ドル圧力、ボラティリティの組み合わせで評価しました。"
    elif asset == "GOLD":
        base = score["gold_safe_haven_score"] + score["risk_off_score"] - score["dollar_strength_score"] - score["rate_pressure_score"]
        comment = "GOLDは安全資産需要とドル高/金利上昇圧力の綱引きで評価しました。"
    elif asset == "WTI":
        base = score["oil_supply_risk_proxy_score"] + score["risk_on_score"] * 0.4 - score["dollar_strength_score"] * 0.4 - 35
        comment = "WTIは供給リスクproxyとリスク選好、ドル圧力で評価しました。"
    elif asset == "USDJPY":
        base = score["dollar_strength_score"] + score["rate_pressure_score"] - 100
        comment = "USDJPYはドル高と米金利圧力を中心に評価しました。"
    elif asset in {"SPX", "NASDAQ"}:
        base = score["risk_on_score"] + score["equity_momentum_score"] - score["rate_pressure_score"] * 0.6 - score["volatility_stress_score"] * 0.8 - 20
        comment = f"{asset}は株式モメンタム、金利圧力、ボラティリティで評価しました。"
    elif asset == "DXY":
        base = score["dollar_strength_score"] - 50
        comment = "DXYはドル高圧力を中心に評価しました。"
    elif asset == "VIX":
        base = score["volatility_stress_score"] + score["risk_off_score"] - 100
        comment = "VIXはボラティリティストレスとリスクオフで評価しました。"
    elif asset == "US10Y":
        base = score["rate_pressure_score"] - 50
        comment = "US10Yは金利上昇圧力で評価しました。"
    else:
        base = score["risk_on_score"] - score["risk_off_score"]
        comment = "資産固有ルールがないため、全体リスク選好で評価しました。"

    aligned_score = base * direction
    return max(-100.0, min(100.0, aligned_score)), comment


def alignment_counts(alignment: pd.DataFrame) -> dict[str, int]:
    if alignment.empty or "narrative_alignment" not in alignment.columns:
        return {"aligned": 0, "conflicted": 0, "neutral": 0, "insufficient_data": 0}
    counts = alignment["narrative_alignment"].fillna("neutral").astype(str).value_counts().to_dict()
    return {key: int(counts.get(key, 0)) for key in ["aligned", "conflicted", "neutral", "insufficient_data"]}
