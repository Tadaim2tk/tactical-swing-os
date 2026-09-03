"""主役レンズの5年検証（v2: #139 Codex P1×2+P2 修正版）。

修正点:
1. 月ブロック入れ替えを「ブロック順の入れ替え」へ（日次ラベル構造を保つ。旧実装は
   各月を多数決1ラベルに潰しており、観測統計量と帰無分布が別推定量だった）
2. 5日先リターンを**各資産の営業日カレンダー**で数える（旧実装は暦の和集合の行を5つ
   進めており、週5日資産では5営業日にならなかった）
3. ブートストラップを報告値と同じ推定量（観測数重み）で行う

as-of厳守: 主役は前日までで確定した値を使い、リターンは当日以降を見る。
usage: python tools/analysis/leader_validation_corpus.py  (repo rootで実行・読み取り専用)
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from block_perm import block_permutation, forward_return_on_own_calendar  # noqa: E402

RISK_ON = {"BTC", "ETH", "NASDAQ", "SPX"}

mk = pd.read_csv("data/retro/market_daily.csv", parse_dates=["date"]).sort_values("date").reset_index(drop=True)
prices = pd.read_csv("data/retro/prices_long.csv", parse_dates=["date"]).sort_values(["asset", "date"])
mk["ym"] = mk["date"].dt.to_period("M").astype(str)
assets = sorted(prices["asset"].unique())

mk["ldr"] = mk["leader_asset"].shift(1)            # 前日までで確定した主役
mk["ldr_margin"] = mk["leader_margin"].shift(1)
mk = mk[mk["ldr"].notna() & (mk["ldr"] != "none")].reset_index(drop=True)
print(f"母集団: {len(mk)}日 ({mk['date'].min().date()}..{mk['date'].max().date()}) 月ブロック={mk['ym'].nunique()}")

results = []

# 仮説1: 主役が攻め資産の期間は株の翌5営業日リターンが高い
for tgt in ["SPX", "NASDAQ"]:
    fwd = mk["date"].map(lambda d: forward_return_on_own_calendar(prices, tgt, d, 5))
    lab = mk["ldr"].isin(RISK_ON).astype(int).values
    obs, p, nb = block_permutation(fwd.values, lab, mk["ym"].values, seed=11)
    print(f"[H1-{tgt}] 主役=攻め資産 → {tgt}翌5営業日の差: {obs*100:+.3f}% (p={p:.3f}, ブロック{nb})")
    results.append((f"H1-{tgt}", obs, p))

# 仮説2: 主役アセット自身の翌5営業日の変動幅は他資産平均より大きい（各資産の暦で計算）
lead_abs, other_abs, ym_keep = [], [], []
for _, r in mk.iterrows():
    a, d = r["ldr"], r["date"]
    lf = forward_return_on_own_calendar(prices, a, d, 5)
    if np.isnan(lf):
        continue
    vals = [forward_return_on_own_calendar(prices, x, d, 5) for x in assets if x != a]
    vals = [abs(v) for v in vals if not np.isnan(v)]
    if not vals:
        continue
    lead_abs.append(abs(lf))
    other_abs.append(float(np.mean(vals)))
    ym_keep.append(r["ym"])
diff = np.array(lead_abs) - np.array(other_abs)
ym_keep = np.array(ym_keep)
point = diff.mean()
# 報告値と同じ観測数重みでブートストラップ（月ブロックを再抽出し、月内の観測をそのまま使う）
dfb = pd.DataFrame({"d": diff, "b": ym_keep})
groups = [g["d"].values for _, g in dfb.groupby("b", sort=True)]
rng = np.random.default_rng(3)
boot = [np.concatenate([groups[i] for i in rng.integers(0, len(groups), len(groups))]).mean()
        for _ in range(5000)]
lo, hi = np.percentile(boot, [2.5, 97.5])
print(f"[H2] 主役アセットの翌5営業日変動幅 − 他資産平均: {point*100:+.3f}%pt "
      f"(観測数重みブートストラップ95%CI [{lo*100:+.3f}, {hi*100:+.3f}]) n={len(diff)}日/{len(groups)}ブロック")
results.append(("H2", point, 0.0 if (lo > 0 or hi < 0) else 1.0))

# 仮説3: 主役が明確な日ほどその後の変動が大きい
fwd_spx = mk["date"].map(lambda d: forward_return_on_own_calendar(prices, "SPX", d, 5)).abs()
m = mk["ldr_margin"].notna()
lab = (mk.loc[m, "ldr_margin"] > mk.loc[m, "ldr_margin"].median()).astype(int).values
obs, p, nb = block_permutation(fwd_spx[m].values, lab, mk.loc[m, "ym"].values, seed=7)
print(f"[H3] 明確さ上位 → SPX翌5営業日の変動幅の差: {obs*100:+.3f}%pt (p={p:.3f}, ブロック{nb})")
results.append(("H3", obs, p))

print(f"\n試した仮説={len(results)}件 / 有意(p<0.05)={sum(1 for _, _, p in results if p < 0.05)}件")
