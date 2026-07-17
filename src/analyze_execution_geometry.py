"""執行ジオメトリの格子探索 (分析専用CLI・表示のみ)。

SL幅倍率 × entry位置 × 決済ポリシーの格子で、保守的執行ルール
(simulate_execution と同じ: 同足SL負け・TP翌足以降・SL優先) の成績を比較する。
8/1 月次較正などで新規データに対して再実行し、2026-07-17 のジオメトリ介入
(docs/gpt_prompt_changelog.md (4)) をアウトオブサンプルで検証するための道具。

注意: 過去データへの当てはめ(in-sample)なので、最良セルの数字をそのまま
将来の期待にしない。ロバストな領域(隣接セルも同符号)だけを読む。
"""
from __future__ import annotations

import pandas as pd

from score_prediction_log import load_ohlcv_frame, normalize_side
from simulate_execution import MAX_REFERENCE_ANCHOR_DEVIATION

SL_MULTS = (1.0, 1.5, 2.0, 2.5, 3.0)
ENTRY_MODES = ("worst", "mid", "deep")
TP_POLICIES = ("tp1", "none")


def _num(v):
    n = pd.to_numeric(v, errors="coerce")
    return float(n) if pd.notna(n) else None


def load_orders(ledger: pd.DataFrame) -> list[dict]:
    orders = []
    cache: dict[str, pd.DataFrame] = {}
    for _, r in ledger.iterrows():
        side = normalize_side(r.get("side"))
        rank = str(r.get("rank") or "").strip().upper()
        rp = _num(r.get("risk_pct"))
        e1, e2, sl, tp1 = (_num(r.get(k)) for k in ("entry_low", "entry_high", "sl", "tp1"))
        if side not in {"LONG", "SHORT"} or rank not in {"A", "B"} or not rp or rp <= 0:
            continue
        if e1 is None or e2 is None or sl is None:
            continue
        asset = str(r.get("asset") or "")
        if asset not in cache:
            cache[asset] = load_ohlcv_frame(asset)
        o = cache[asset]
        if o.empty:
            continue
        d = pd.to_datetime(r.get("date"), errors="coerce")
        if pd.isna(d):
            continue
        i0 = int(o["date"].searchsorted(d.normalize(), side="left"))
        if i0 >= len(o):
            continue
        anchor = float(o.iloc[i0]["close"])
        if anchor <= 0 or abs(((e1 + e2) / 2) / anchor - 1) > MAX_REFERENCE_ANCHOR_DEVIATION:
            continue
        orders.append({"side": side, "rp": rp, "e1": e1, "e2": e2, "sl": sl,
                       "tp1": tp1, "i0": i0, "ohlc": o})
    return orders


def simulate(o: dict, entry_mode: str, sl_mult: float, tp_policy: str):
    """保守ルールで1注文を執行。R_k(拡張後リスク単位)、未決着はNone/'open'。"""
    long = o["side"] == "LONG"
    e1, e2 = o["e1"], o["e2"]
    price = {"worst": e2 if long else e1, "mid": (e1 + e2) / 2, "deep": e1 if long else e2}[entry_mode]
    dist0 = abs(price - o["sl"])
    if dist0 <= 0:
        return None
    risk = sl_mult * dist0
    slp = price - risk if long else price + risk
    tp = o["tp1"] if tp_policy == "tp1" else None
    ohlc, i0 = o["ohlc"], o["i0"]
    deadline = i0 + 5
    fill_i = None
    for i in range(i0, min(i0 + 5, len(ohlc))):
        b = ohlc.iloc[i]
        if (float(b["low"]) <= price) if long else (float(b["high"]) >= price):
            fill_i = i
            break
    if fill_i is None:
        return None if (i0 + 5) <= len(ohlc) else "open"
    b = ohlc.iloc[fill_i]
    if (float(b["low"]) <= slp) if long else (float(b["high"]) >= slp):
        return -1.0
    for i in range(fill_i + 1, min(deadline + 1, len(ohlc))):
        b = ohlc.iloc[i]
        if (float(b["low"]) <= slp) if long else (float(b["high"]) >= slp):
            return -1.0
        if tp is not None and ((float(b["high"]) >= tp) if long else (float(b["low"]) <= tp)):
            return abs(tp - price) / risk
    if deadline < len(ohlc):
        c = float(ohlc.iloc[deadline]["close"])
        return ((c - price) if long else (price - c)) / risk
    return "open"


def main() -> int:
    ledger = pd.read_csv("data/signal_log.csv", dtype=str, keep_default_na=False)
    orders = load_orders(ledger)
    print(f"対象注文(水準ガード通過): {len(orders)}")
    header = f"{'entry':6s} {'tp':5s} " + " ".join(f"k={k:<5}" for k in SL_MULTS)
    print(header)
    print("=" * len(header))
    for entry_mode in ENTRY_MODES:
        for tp_policy in TP_POLICIES:
            cells = []
            n = 0
            for k in SL_MULTS:
                rs = [simulate(o, entry_mode, k, tp_policy) for o in orders]
                vals = [r * o["rp"] for r, o in zip(rs, orders) if isinstance(r, float)]
                n = len(vals)
                cells.append(f"{sum(vals):+6.1f}%")
            print(f"{entry_mode:6s} {tp_policy:5s} " + " ".join(cells) + f"  (n={n})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
