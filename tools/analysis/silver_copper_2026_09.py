# ERSから借りた銀・銅で「商品ショック vs 安全資産需要」を切り分けられるか検定する。
# 仮説の型: 生存 / ゼロ / 逆が真 / 検出力不足 のどれかに必ず分類する。
# 有意性は月ブロック入れ替え(同月内の相関を壊さない)。as-of厳守(判定はD-1まで、結果はD以降)。
import numpy as np
import pandas as pd

mk = pd.read_csv("data/retro/market_daily.csv", parse_dates=["date"])
ext = pd.read_csv("data/retro/macro_ext.csv", parse_dates=["date"])
w = ext.pivot_table(index="date", columns="asset", values="close")
base = mk.set_index("date")[["close_GOLD", "close_SPX", "close_NASDAQ", "close_VIX", "close_US10Y", "close_DXY"]]
d = base.join(w[["SILVER", "COPPER", "SOX", "US5Y", "US30Y"]], how="inner").sort_index()
# 共通営業日に揃える(週末行を残したまま窓を取るとローリング和が全てNaNになる)
d = d.dropna(subset=["close_GOLD", "close_SPX", "SILVER", "COPPER"])
for c in d.columns:
    d[f"r_{c}"] = d[c].pct_change(fill_method=None)
d["ym"] = d.index.to_period("M").astype(str)
print(f"母集団: {len(d)}日 ({d.index.min().date()}..{d.index.max().date()}) 月ブロック={d['ym'].nunique()}\n")

def block_perm(v, lab, blocks, n=5000, seed=1):
    obs = v[lab == 1].mean() - v[lab == 0].mean()
    df = pd.DataFrame({"v": v, "l": lab, "b": blocks})
    bl = df.groupby("b")["l"].mean().round().astype(int)
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        perm = pd.Series(rng.permutation(bl.values), index=bl.index)
        L = df["b"].map(perm).values
        if L.sum() == 0 or (1 - L).sum() == 0:
            continue
        out.append(df["v"].values[L == 1].mean() - df["v"].values[L == 0].mean())
    return obs, float(np.mean(np.abs(out) >= abs(obs)))

def verdict(obs, p, expect_positive=True, n_eff=0):
    """仮説の型分け: 生存/ゼロ/逆が真/検出力不足"""
    if p < 0.05:
        if (obs > 0) == expect_positive:
            return "生存（予想どおり）"
        return "**逆が真**（符号が逆で有意）"
    if n_eff < 20:
        return "検出力不足（判定不能）"
    return "ゼロ（効果が見当たらない）"

# 20日窓で「金が上がった局面」を、銀・銅の同時挙動で3分類（as-of: 全て過去20日の実測）
win = 20
d["gold_up"] = d["r_close_GOLD"].rolling(win).sum()
d["silver_up"] = d["r_SILVER"].rolling(win).sum()
d["copper_up"] = d["r_COPPER"].rolling(win).sum()
sig = d.dropna(subset=["gold_up", "silver_up", "copper_up"]).copy()
sig = sig[sig["gold_up"] > 0]  # 金が上げている局面に限定

# 通貨型: 金↑ 銀↑ 銅↓（産業需要でないのに貴金属が上がる）
# 産業型: 金↑ 銀↑ 銅↑（商品全体が上がっている）
sig["monetary"] = (sig["silver_up"] > 0) & (sig["copper_up"] < 0)
sig["industrial"] = (sig["silver_up"] > 0) & (sig["copper_up"] > 0)
sub = sig[sig["monetary"] | sig["industrial"]].copy()
print(f"金が上げている局面 {len(sig)}日 → 通貨型 {int(sub['monetary'].sum())}日 / 産業型 {int(sub['industrial'].sum())}日")

results = []
# 仮説1: 通貨型(安全資産需要)の局面では、その後5日の株が弱い
for tgt in ["SPX", "NASDAQ"]:
    fwd = d[f"close_{tgt}"].pct_change(5, fill_method=None).shift(-5).reindex(sub.index)
    m = fwd.notna()
    obs, p = block_perm(fwd[m].values, sub.loc[m, "monetary"].astype(int).values, sub.loc[m, "ym"].values, seed=5)
    nb = sub.loc[m, "ym"].nunique()
    v = verdict(obs, p, expect_positive=False, n_eff=nb)
    print(f"[H1-{tgt}] 通貨型 − 産業型 の翌5日株リターン差: {obs*100:+.3f}% (p={p:.3f}, 月ブロック{nb}) → {v}")
    results.append((f"H1-{tgt}", obs, p, v))

# 仮説2: 通貨型の局面では、その後5日の金の伸びが大きい（安全資産買いの継続）
fwd_g = d["close_GOLD"].pct_change(5, fill_method=None).shift(-5).reindex(sub.index)
m = fwd_g.notna()
obs, p = block_perm(fwd_g[m].values, sub.loc[m, "monetary"].astype(int).values, sub.loc[m, "ym"].values, seed=6)
nb = sub.loc[m, "ym"].nunique()
v = verdict(obs, p, True, nb)
print(f"[H2] 通貨型 − 産業型 の翌5日GOLDリターン差: {obs*100:+.3f}% (p={p:.3f}, 月ブロック{nb}) → {v}")
results.append(("H2", obs, p, v))

# 仮説3: 銀/銅の比率は、VIXより先に動くか（先行性）
d["sc_ratio"] = (d["r_SILVER"] - d["r_COPPER"]).rolling(win).sum()
m2 = d["sc_ratio"].notna()
hi = (d.loc[m2, "sc_ratio"] > d.loc[m2, "sc_ratio"].median()).astype(int).values
fwd_vix = d["close_VIX"].pct_change(5, fill_method=None).shift(-5)[m2]
ok = fwd_vix.notna().values
obs, p = block_perm(fwd_vix[ok].values, hi[ok], d.loc[m2, "ym"][ok].values, seed=8)
nb = d.loc[m2, "ym"][ok].nunique()
v = verdict(obs, p, True, nb)
print(f"[H3] 銀-銅スプレッド上位 → 翌5日VIX変化率の差: {obs*100:+.3f}% (p={p:.3f}, 月ブロック{nb}) → {v}")
results.append(("H3", obs, p, v))

print(f"\n試した仮説={len(results)}件 / 生存={sum(1 for r in results if '生存' in r[3])} "
      f"逆が真={sum(1 for r in results if '逆' in r[3])} "
      f"ゼロ={sum(1 for r in results if 'ゼロ' in r[3])} "
      f"検出力不足={sum(1 for r in results if '検出力' in r[3])}")
