# -*- coding: utf-8 -*-
"""押し目が来なかったときに成行で入る規則を、過去の台帳の上で試す。

2026-09-09の観測: 約定した110件が -6.53R、約定しなかった32件が +24.53R。
方向は当たっているのに、Entry帯へ戻らないまま走った判断に参加できていない
(人間の言明: 「大相場に乗れないと資産が増えない」)。

ここで測るのは「何本待って、来なければ入るか」の1点だけ。
待ち本数 N を 1..5 で振り、実現Rがどう変わるかを見る。N=5 は現行と同じ。

執行の規約は simulate_execution.py と揃える。ズレると比較にならない:
  - 自然約定はゾーン内の最悪価格
  - 成行で入る場合は、判定できるバーの終値(N-1本目)。そのバーの安値/高値は
    既に過ぎているので、SL/TP判定は翌バーから。ここを同バーから見ると
    「入る前に付いた値」で損切りしたことになり、過去を覗く
  - 決済期限は判断日ラベルを0本目とした EXIT_DEADLINE_BARS 本目(=6本目)。
    遅く入るほど持ち時間が短い。これは規則の費用なので縮めない
  - SLとTP1が同じ足なら SL優先

出力はRの合計・平均・勝率と、成行で入った件数の内訳。
**これは反実仮想であって成績ではない。** 実際にはその値段で入れたとは限らない。
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from simulate_execution import (EXIT_DEADLINE_BARS, FILL_WINDOW_BARS,  # noqa: E402
                                MAX_REFERENCE_ANCHOR_DEVIATION, _num, normalize_side)
from score_prediction_log import decision_time_anchor, load_ohlcv_frame  # noqa: E402

CHASE_ASSETS = {"NASDAQ", "BTC", "USDJPY"}  # 未約定ぶんの方向Rが正で厚い資産


def run_row(row, ohlcv, wait_bars):
    """1行を執行する。wait_bars 本待って未到達なら、その最終バーの終値で成行。

    戻り値: (status, r) / 対象外は (理由, None)
    """
    side = normalize_side(row.get("side"))
    e1, e2 = _num(row.get("entry_low")), _num(row.get("entry_high"))
    sl, tp1 = _num(row.get("sl")), _num(row.get("tp1"))
    if ohlcv.empty or side not in {"LONG", "SHORT"} or not (e1 == e1 and e2 == e2 and sl == sl):
        return "skip_levels", None
    sig_date = pd.to_datetime(row.get("date"), errors="coerce")
    if pd.isna(sig_date) or sig_date.normalize() < pd.to_datetime(ohlcv["date"].iloc[0]):
        return "skip_window", None
    idx0, anchor_idx = decision_time_anchor(ohlcv, sig_date)
    if idx0 >= len(ohlcv):
        return "open", None
    ref = (e1 + e2) / 2
    if anchor_idx >= 0:
        ac = float(ohlcv.iloc[anchor_idx]["close"])
        if ac > 0 and abs(ref / ac - 1.0) > MAX_REFERENCE_ANCHOR_DEVIATION:
            return "excluded_scale", None
    is_long = side == "LONG"

    # 1) 待つあいだの自然約定
    fill_i, fill_price, chased = None, None, False
    for i in range(idx0, min(idx0 + wait_bars, len(ohlcv))):
        bar = ohlcv.iloc[i]
        if float(bar["low"]) <= e2 and float(bar["high"]) >= e1:
            fill_i, fill_price = i, (e2 if is_long else e1)
            break

    # 2) 来なければ、判定できる最終バーの終値で成行
    if fill_i is None:
        k = idx0 + wait_bars - 1
        if k >= len(ohlcv):
            return "open", None
        fill_i, fill_price, chased = k, float(ohlcv.iloc[k]["close"]), True
        beyond_sl = fill_price <= sl if is_long else fill_price >= sl
        if beyond_sl:
            return "chase_beyond_sl", None      # 既に損切り水準の向こう。入らない
        if tp1 == tp1 and (fill_price >= tp1 if is_long else fill_price <= tp1):
            return "chase_beyond_tp1", None     # 目標を過ぎている。追わない

    risk = abs(fill_price - sl)
    if risk <= 0:
        return "skip_levels", None

    def r_of(price):
        return ((price - fill_price) if is_long else (fill_price - price)) / risk

    # 3) 決済。成行で入った足は既に過ぎているので翌足から見る
    start = fill_i + 1 if chased else fill_i
    if not chased:
        bar = ohlcv.iloc[fill_i]
        if (float(bar["low"]) <= sl) if is_long else (float(bar["high"]) >= sl):
            return ("chase_sl" if chased else "filled_sl"), r_of(sl)
        start = fill_i + 1
    deadline = idx0 + EXIT_DEADLINE_BARS
    for i in range(start, min(deadline + 1, len(ohlcv))):
        bar = ohlcv.iloc[i]
        if (float(bar["low"]) <= sl) if is_long else (float(bar["high"]) >= sl):
            return ("chase_sl" if chased else "filled_sl"), r_of(sl)
        if tp1 == tp1 and ((float(bar["high"]) >= tp1) if is_long else (float(bar["low"]) <= tp1)):
            return ("chase_tp1" if chased else "filled_tp1"), r_of(tp1)
    if deadline < len(ohlcv):
        return ("chase_time" if chased else "filled_time_exit"), r_of(float(ohlcv.iloc[deadline]["close"]))
    return "open", None


def sweep(ledger, assets=None):
    cache = {}
    rows = []
    for wait in range(1, FILL_WINDOW_BARS + 1):
        recs = []
        for _, row in ledger.iterrows():
            a = str(row.get("asset") or "")
            if assets is not None and a not in assets:
                continue
            if a not in cache:
                cache[a] = load_ohlcv_frame(a)
            st, r = run_row(row, cache[a], wait)
            recs.append({"asset": a, "status": st, "r": r, "chased": st.startswith("chase")})
        d = pd.DataFrame(recs)
        done = d[d.r.notna()]
        ch = done[done.chased]
        rows.append({
            "待ち本数": wait,
            "約定": len(done),
            "うち成行": len(ch),
            "合計R": round(done.r.sum(), 2),
            "平均R": round(done.r.mean(), 3) if len(done) else None,
            "勝率": round((done.r > 0).mean(), 3) if len(done) else None,
            "成行のR": round(ch.r.sum(), 2) if len(ch) else 0.0,
            "追わず(SL超)": int((d.status == "chase_beyond_sl").sum()),
            "追わず(TP超)": int((d.status == "chase_beyond_tp1").sum()),
        })
    return pd.DataFrame(rows)


def main():
    ledger = pd.read_csv("data/signal_log.csv")
    ledger = ledger[ledger["side"].map(normalize_side).isin({"LONG", "SHORT"})]
    print(f"方向あり {len(ledger)} 件\n")
    print("=== 全資産 ===")
    print(sweep(ledger).to_string(index=False))
    print("\n=== NASDAQ / BTC / USDJPY のみ ===")
    print(sweep(ledger, CHASE_ASSETS).to_string(index=False))
    print("\n=== WTI のみ(未約定ぶんが唯一マイナスだった資産) ===")
    print(sweep(ledger, {"WTI"}).to_string(index=False))


if __name__ == "__main__":
    main()
