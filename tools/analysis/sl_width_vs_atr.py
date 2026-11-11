# -*- coding: utf-8 -*-
"""SL幅を日中値幅(ATR10)で割り、期間ごとに並べる。

2026-10-23、人間の言明「最近非常にSLしやすくなっている。ほぼ全部」。
9/17以降、約定した6件のうち5件がSL。測ると、SL幅 ÷ ATR10 の中央値が
6-8月 1.66 → 9/16以降 0.57 に落ちていた。初日の値幅がSL幅を上回っている
(1.10倍)ので、方向が合っていても普通の揺れで切られる。
分解: GPTがSLを価格比で約半分に狭めた(3.2%→1.5%)うえ、日中値幅が約4割広がった。

判断時の ATR10 は decision_time_anchor の anchor_idx までのバーだけで計算する
(先読みしない)。建値は simulate_execution と同じゾーン内の最悪価格。
MAE/MFE は判断後5バーの窓。これは観測であって規則の提案ではない。
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from score_prediction_log import decision_time_anchor, load_ohlcv_frame  # noqa: E402
from simulate_execution import _num, normalize_side  # noqa: E402

PERIODS = [("2026-09-01", "06-08月"), ("2026-09-16", "09月前半"), ("9999-12-31", "09/16以降")]


def period_of(d: pd.Timestamp) -> str:
    for edge, name in PERIODS:
        if d < pd.Timestamp(edge):
            return name
    return PERIODS[-1][1]


def build(ledger: pd.DataFrame, sim: pd.DataFrame) -> pd.DataFrame:
    cache: dict[str, pd.DataFrame] = {}
    rows = []
    for _, r in ledger.iterrows():
        side = normalize_side(r.get("side"))
        rp = _num(r.get("risk_pct"))
        # 母集団は simulate_ledger と同じ「朝に指値を出したもの」(#188 Codex P2)。
        # 方向あり A/B でも risk_pct が 0 か欠損の行は注文ではなく、6-8月に31件ある。
        # 混ぜると、比較の土台が最近の注文と別の母集団になる。
        if side not in ("LONG", "SHORT") or str(r.get("rank") or "").upper() not in ("A", "B") or not (rp == rp and rp > 0):
            continue
        a = str(r.get("asset") or "")
        if a not in cache:
            cache[a] = load_ohlcv_frame(a)
        df = cache[a]
        if df.empty:
            continue
        i0, ai = decision_time_anchor(df, r["date"])
        if ai < 1 or i0 >= len(df):
            continue
        e1, e2, sl = _num(r.get("entry_low")), _num(r.get("entry_high")), _num(r.get("sl"))
        if not (e1 == e1 and e2 == e2 and sl == sl):
            continue
        fill = e2 if side == "LONG" else e1
        risk = abs(fill - sl)
        if risk <= 0:
            continue
        h = df.iloc[max(0, ai - 10):ai + 1]   # 判断時に閉まっていたバーだけ
        tr = np.maximum(h["high"] - h["low"],
                        np.maximum((h["high"] - h["close"].shift()).abs(),
                                   (h["low"] - h["close"].shift()).abs())).dropna()
        atr = float(tr.mean()) if len(tr) else np.nan
        w = df.iloc[i0:i0 + 5]
        if w.empty:
            continue
        d = 1 if side == "LONG" else -1
        mae = ((w["low"].min() - fill) if d == 1 else (fill - w["high"].max())) / risk
        mfe = ((w["high"].max() - fill) if d == 1 else (fill - w["low"].min())) / risk
        close5 = ((w["close"].iloc[-1] - fill) * d) / risk if len(w) >= 5 else np.nan
        st = sim.loc[sim["signal_id"] == r["signal_id"], "status"]
        rows.append({
            "date": pd.Timestamp(r["date"]), "asset": a, "side": side,
            "status": st.iloc[0] if len(st) else "",
            "risk_pct": risk / fill * 100, "atr_pct": atr / fill * 100 if atr == atr else np.nan,
            "risk_atr": risk / atr if atr and atr == atr else np.nan,
            "fillday_range_R": float(w["high"].iloc[0] - w["low"].iloc[0]) / risk,
            "mae_R": mae, "mfe_R": mfe, "close5_R": close5,
        })
    out = pd.DataFrame(rows)
    if not out.empty:
        out["期間"] = out["date"].map(period_of)
    return out


def main() -> int:
    ledger = pd.read_csv("data/signal_log.csv")
    sim = pd.read_csv("data/execution_simulation.csv")
    d = build(ledger, sim)
    if d.empty:
        print("対象なし")
        return 1
    print("=== SL幅 ÷ ATR10、SL幅(価格比%)、ATR10(価格比%)、初日値幅 ÷ SL幅、最悪逆行、最大順行 — 中央値 ===")
    g = d.groupby("期間").agg(n=("asset", "size"), risk_atr=("risk_atr", "median"), risk_pct=("risk_pct", "median"),
                            atr_pct=("atr_pct", "median"), fillday_range_R=("fillday_range_R", "median"),
                            mae_R=("mae_R", "median"), mfe_R=("mfe_R", "median")).round(2)
    print(g.to_string())
    f = d[d["status"] == "filled_sl"].copy()
    if not f.empty:
        print("\n=== SLになった注文: 5日目には予測方向に戻っていた件数(揺れで切られた型) と、SL幅を2倍にしたら耐えた件数 ===")
        f["whipsaw"] = f["close5_R"] > 0
        f["survive_2x"] = f["mae_R"] > -2.0
        print(f.groupby("期間").agg(SL件数=("asset", "size"), 戻っていた=("whipsaw", "sum"),
                                  二倍で耐えた=("survive_2x", "sum")).to_string())
    print("\n=== 9/16以降の1件ずつ ===")
    cols = ["date", "asset", "side", "status", "risk_pct", "atr_pct", "risk_atr", "fillday_range_R", "mae_R", "mfe_R", "close5_R"]
    print(d[d["date"] >= "2026-09-16"][cols].round(2).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
