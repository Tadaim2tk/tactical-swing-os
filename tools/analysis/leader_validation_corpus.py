# 主役レンズの遡及検証その2: 5年コーパス(1,830日)で市場構造の仮説として検定する。
# 台帳(3か月・独立16クラスタ)では検出力が足りないため、判断の当否ではなく
# 「主役という区分が、その後の値動きについて何か言えるか」を直接測る。
# 全て as-of(D-1までの情報で主役を決め、Dから先のリターンを見る)。
# 有意性は月ブロック入れ替え(同月内の相関を壊さない)で判定する。
import numpy as np
import pandas as pd

RISK_ON = {"BTC", "ETH", "NASDAQ", "SPX"}
mk = pd.read_csv("data/retro/market_daily.csv", parse_dates=["date"]).sort_values("date").reset_index(drop=True)
mk["ym"] = mk["date"].dt.to_period("M").astype(str)
assets = [c[4:] for c in mk.columns if c.startswith("ret_")]

# 主役は前日までで確定 → 当日以降のリターンを見る(未来参照なし)
mk["ldr"] = mk["leader_asset"].shift(1)
mk["ldr_margin"] = mk["leader_margin"].shift(1)
mk = mk[mk["ldr"].notna() & (mk["ldr"] != "none")].reset_index(drop=True)
print(f"母集団: {len(mk)}日 ({mk['date'].min().date()}..{mk['date'].max().date()}) / 月ブロック={mk['ym'].nunique()}")
print(f"主役の分布(上位): {mk['ldr'].value_counts().head(6).to_dict()}\n")

def block_perm(values, labels, blocks, n=5000, seed=1):
    """月ブロック単位でラベルを入れ替える。ブロック内の相関を壊さない。"""
    obs = values[labels == 1].mean() - values[labels == 0].mean()
    df = pd.DataFrame({"v": values, "l": labels, "b": blocks})
    bl = df.groupby("b")["l"].mean().round().astype(int)
    rng = np.random.default_rng(seed)
    keys = bl.index.values
    out = []
    for _ in range(n):
        perm = pd.Series(rng.permutation(bl.values), index=keys)
        lab = df["b"].map(perm).values
        if lab.sum() == 0 or (1 - lab).sum() == 0:
            continue
        out.append(df["v"].values[lab == 1].mean() - df["v"].values[lab == 0].mean())
    return obs, float(np.mean(np.abs(out) >= abs(obs)))

results = []

# 仮説1: 主役が攻め資産の期間は、株の翌5日リターンが高い(レジーム判定として使えるか)
for tgt in ["SPX", "NASDAQ"]:
    fwd = mk[f"close_{tgt}"].pct_change(5, fill_method=None).shift(-5)
    m = fwd.notna()
    lab = mk.loc[m, "ldr"].isin(RISK_ON).astype(int).values
    obs, p = block_perm(fwd[m].values, lab, mk.loc[m, "ym"].values, seed=11)
    print(f"[仮説1] 主役=攻め資産 → {tgt}の翌5日リターン差: {obs*100:+.3f}% (p={p:.3f}) n={m.sum()}")
    results.append(("H1-" + tgt, abs(obs), p))

# 仮説2: 主役アセット自身の翌5日モメンタムは、非主役より継続しやすいか
rows = []
for _, r in mk.iterrows():
    a = r["ldr"]
    if f"close_{a}" not in mk.columns:
        continue
    rows.append(r["date"])
idx = mk.set_index("date")
lead_fwd, other_fwd, ym_l = [], [], []
for i in range(len(mk) - 5):
    r = mk.iloc[i]
    a = r["ldr"]
    col = f"close_{a}"
    if col not in mk.columns:
        continue
    c0, c1 = mk.iloc[i][col], mk.iloc[i + 5][col]
    if pd.notna(c0) and pd.notna(c1) and c0 > 0:
        lead_fwd.append(abs(c1 / c0 - 1.0))
        ym_l.append(r["ym"])
        others = [x for x in assets if x != a and f"close_{x}" in mk.columns]
        vals = []
        for x in others:
            d0, d1 = mk.iloc[i][f"close_{x}"], mk.iloc[i + 5][f"close_{x}"]
            if pd.notna(d0) and pd.notna(d1) and d0 > 0:
                vals.append(abs(d1 / d0 - 1.0))
        other_fwd.append(np.mean(vals) if vals else np.nan)
lf, of_ = np.array(lead_fwd), np.array(other_fwd)
ok = ~np.isnan(of_)
diff = (lf[ok] - of_[ok])
dfb = pd.DataFrame({"d": diff, "b": np.array(ym_l)[ok]})
bm = dfb.groupby("b")["d"].mean()
rng = np.random.default_rng(3)
boot = [bm.sample(len(bm), replace=True, random_state=int(s)).mean() for s in rng.integers(0, 1e6, 5000)]
lo, hi = np.percentile(boot, [2.5, 97.5])
print(f"[仮説2] 主役アセットの翌5日変動幅 − 他資産平均: {diff.mean()*100:+.3f}%pt "
      f"(月ブロックbootstrap 95%CI [{lo*100:+.3f}, {hi*100:+.3f}]) n={ok.sum()}日")
results.append(("H2", abs(diff.mean()), 0.0 if (lo > 0 or hi < 0) else 1.0))

# 仮説3: 主役の明確さが高い日ほど、その後の値動きは主役に連動しやすいか
hi_m = mk["ldr_margin"] > mk["ldr_margin"].median()
fwd_spx = mk["close_SPX"].pct_change(5, fill_method=None).shift(-5)
m = fwd_spx.notna() & mk["ldr_margin"].notna()
obs, p = block_perm(fwd_spx[m].abs().values, hi_m[m].astype(int).values, mk.loc[m, "ym"].values, seed=7)
print(f"[仮説3] 明確さ上位 → SPXの翌5日変動幅の差: {obs*100:+.3f}%pt (p={p:.3f}) n={m.sum()}")
results.append(("H3", abs(obs), p))

print(f"\n試した仮説 = {len(results)}件。うち有意(p<0.05)は {sum(1 for _,_,p in results if p < 0.05)}件")
