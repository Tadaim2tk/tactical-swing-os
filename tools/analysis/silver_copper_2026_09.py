"""銀・銅による「商品ショック vs 安全資産需要」の切り分け検定（v2: #140 Codex P1×3 修正版）。

修正点:
1. 月ブロック入れ替えを「ブロック順の入れ替え」へ（日次ラベル構造を保つ）
2. 予測側の窓を D-1 で終える（旧実装は当日の終値を含む20日和で当日を分類していた＝1日分の先読み）
3. H3 の閾値を全期間の中央値から**拡大窓の中央値**へ（旧実装は2021年の分類に将来の観測が入っていた）

仮説の型: 生存 / ゼロ / 逆が真 / 検出力不足 のいずれかに必ず分類する。
usage: python tools/analysis/silver_copper_2026_09.py  (repo rootで実行・読み取り専用)
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from block_perm import block_permutation  # noqa: E402

WIN = 20

mk = pd.read_csv("data/retro/market_daily.csv", parse_dates=["date"])
ext = pd.read_csv("data/retro/macro_ext.csv", parse_dates=["date"])
w = ext.pivot_table(index="date", columns="asset", values="close")
base = mk.set_index("date")[["close_GOLD", "close_SPX", "close_NASDAQ", "close_VIX"]]
d = base.join(w[["SILVER", "COPPER"]], how="inner").sort_index()
# 共通営業日に揃える（週末行を残したまま窓を取るとローリング和が全てNaNになる）
d = d.dropna(subset=["close_GOLD", "close_SPX", "SILVER", "COPPER"])
for c in ["close_GOLD", "close_SPX", "close_NASDAQ", "close_VIX", "SILVER", "COPPER"]:
    d[f"r_{c}"] = d[c].pct_change(fill_method=None)
d["ym"] = d.index.to_period("M").astype(str)
print(f"母集団: {len(d)}日 ({d.index.min().date()}..{d.index.max().date()}) 月ブロック={d['ym'].nunique()}")


def verdict(p, obs, expect_positive, n_blocks):
    if np.isnan(p):
        return "検出力不足（判定不能）"
    if p < 0.05:
        return "生存（予想どおり）" if (obs > 0) == expect_positive else "**逆が真**（符号が逆で有意）"
    return "検出力不足（判定不能）" if n_blocks < 20 else "ゼロ（効果が見当たらない）"


# 予測側の窓は D-1 で終える（shift(1)）。分類は「前日までの20営業日」で行う。
for col, name in [("r_close_GOLD", "gold"), ("r_SILVER", "silver"), ("r_COPPER", "copper")]:
    d[f"{name}_up"] = d[col].rolling(WIN).sum().shift(1)
sig = d.dropna(subset=["gold_up", "silver_up", "copper_up"]).copy()
sig = sig[sig["gold_up"] > 0]
sig["monetary"] = (sig["silver_up"] > 0) & (sig["copper_up"] < 0)   # 金↑銀↑銅↓ = 通貨型
sig["industrial"] = (sig["silver_up"] > 0) & (sig["copper_up"] > 0)  # 金↑銀↑銅↑ = 産業型
sub = sig[sig["monetary"] | sig["industrial"]].copy()
print(f"金が上げている局面 {len(sig)}日 → 通貨型 {int(sub['monetary'].sum())}日 / 産業型 {int(sub['industrial'].sum())}日\n")

results = []
for tgt, expect in [("SPX", False), ("NASDAQ", False)]:
    fwd = d[f"close_{tgt}"].pct_change(5, fill_method=None).shift(-5).reindex(sub.index)
    obs, p, nb = block_permutation(fwd.values, sub["monetary"].astype(int).values, sub["ym"].values, seed=5)
    v = verdict(p, obs, expect, nb)
    print(f"[H1-{tgt}] 通貨型 − 産業型 の翌5日{tgt}リターン差: {obs*100:+.3f}% (p={p:.3f}, ブロック{nb}) → {v}")
    results.append((f"H1-{tgt}", v))

fwd_g = d["close_GOLD"].pct_change(5, fill_method=None).shift(-5).reindex(sub.index)
obs, p, nb = block_permutation(fwd_g.values, sub["monetary"].astype(int).values, sub["ym"].values, seed=6)
v = verdict(p, obs, True, nb)
print(f"[H2] 通貨型 − 産業型 の翌5日GOLDリターン差: {obs*100:+.3f}% (p={p:.3f}, ブロック{nb}) → {v}")
results.append(("H2", v))

# H3: 閾値は拡大窓の中央値（その日までの情報だけで決める）
d["sc"] = (d["r_SILVER"] - d["r_COPPER"]).rolling(WIN).sum().shift(1)
d["sc_med"] = d["sc"].expanding(min_periods=120).median()
m3 = d["sc"].notna() & d["sc_med"].notna()
lab3 = (d.loc[m3, "sc"] > d.loc[m3, "sc_med"]).astype(int).values
fwd_v = d["close_VIX"].pct_change(5, fill_method=None).shift(-5)[m3]
obs, p, nb = block_permutation(fwd_v.values, lab3, d.loc[m3, "ym"].values, seed=8)
v = verdict(p, obs, True, nb)
print(f"[H3] 銀-銅スプレッド上位(拡大窓中央値) → 翌5日VIX変化率の差: {obs*100:+.3f}% (p={p:.3f}, ブロック{nb}) → {v}")
results.append(("H3", v))

print(f"\n試した仮説={len(results)}件 / "
      f"生存={sum(1 for _, v in results if '生存' in v)} "
      f"逆が真={sum(1 for _, v in results if '逆' in v)} "
      f"ゼロ={sum(1 for _, v in results if 'ゼロ' in v)} "
      f"検出力不足={sum(1 for _, v in results if '検出力' in v)}")
