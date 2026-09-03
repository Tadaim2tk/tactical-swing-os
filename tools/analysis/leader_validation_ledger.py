# 主役レンズの遡及検証(as-of。未来参照なし)
# 規約: 判断日Dには D-1 までで確定したコーパス行を merge_asof(backward, allow_exact=False) で当てる。
# 罠対策: (1)連続日は資産×バースト(間隔>7日)でクラスタ化し、検定はクラスタ単位の入れ替えで行う
#         (2)試した切り口の数を数え、同数の切り口を無作為ラベルでも試して最大差の分布と比べる
import numpy as np
import pandas as pd

RISK_ON_LEADERS = {"BTC", "ETH", "NASDAQ", "SPX"}          # 攻めの資産が主役
DEFENSIVE_LEADERS = {"VIX", "US10Y", "DXY", "GOLD", "WTI"}  # 守り/マクロが主役
CLASS = {"BTC": "crypto", "ETH": "crypto", "NASDAQ": "index", "SPX": "index",
         "GOLD": "metal", "WTI": "energy", "USDJPY": "fx", "DXY": "fx",
         "US10Y": "rates", "VIX": "vol"}

led = pd.read_csv("data/signal_log.csv", parse_dates=["date"])
sc = pd.read_csv("data/prediction_log_scores.csv", parse_dates=["date"])
mk = pd.read_csv("data/retro/market_daily.csv", parse_dates=["date"])

ctx = mk[["date", "leader_asset", "leader_margin", "leader_score", "risk_state", "vol_state"]].sort_values("date")
d = sc[(sc["actionable"] == True) & sc["result_5d"].isin(["success", "failure"])].copy()  # noqa: E712
d = pd.merge_asof(d.sort_values("date"), ctx, on="date", direction="backward", allow_exact_matches=False)
d["win"] = (d["result_5d"] == "success").astype(int)
d["r5"] = pd.to_numeric(d["r_close_5d"], errors="coerce")
d = d[d["leader_asset"].notna() & (d["leader_asset"] != "none")].sort_values(["asset", "date"]).reset_index(drop=True)

# クラスタ(資産×連続日バースト)
d["gap"] = d.groupby("asset")["date"].diff().dt.days.fillna(99)
d["cl"] = d.groupby("asset")["gap"].transform(lambda s: (s > 7).cumsum()).astype(str) + "_" + d["asset"]

print(f"母集団: n={len(d)} クラスタ={d['cl'].nunique()} 勝率={d['win'].mean():.3f} 平均R5={d['r5'].mean():+.3f}")
print(f"期間: {d['date'].min().date()}..{d['date'].max().date()} / 主役の分布: {d['leader_asset'].value_counts().to_dict()}\n")

def cluster_test(mask, label, rng):
    """クラスタ単位の入れ替え検定。差はクラスタ平均勝率の差。"""
    sub = d.copy()
    sub["lab"] = mask.astype(int)
    cl = sub.groupby("cl").agg(win=("win", "mean"), r5=("r5", "mean"), lab=("lab", "mean"), n=("win", "size")).reset_index()
    cl["lab"] = (cl["lab"] >= 0.5).astype(int)
    n1, n0 = int(cl["lab"].sum()), int((1 - cl["lab"]).sum())
    if n1 < 3 or n0 < 3:
        print(f"  {label}: クラスタ{n1}vs{n0} — 判定不能(3未満)")
        return None
    obs = cl[cl["lab"] == 1]["win"].mean() - cl[cl["lab"] == 0]["win"].mean()
    obs_r = cl[cl["lab"] == 1]["r5"].mean() - cl[cl["lab"] == 0]["r5"].mean()
    labs, wins = cl["lab"].values, cl["win"].values
    perm = [wins[s == 1].mean() - wins[s == 0].mean() for s in (rng.permutation(labs) for _ in range(10000))]
    p = float(np.mean(np.abs(perm) >= abs(obs)))
    row_n1, row_n0 = int(mask.sum()), int((~mask).sum())
    print(f"  {label}: 行{row_n1}vs{row_n0} / クラスタ{n1}vs{n0} | 勝率差{obs:+.3f} (p={p:.3f}) 平均R差{obs_r:+.3f}")
    return abs(obs), p

rng = np.random.default_rng(20260903)
cuts = []
print("【切り口A】主役の性格で分ける")
cuts.append(cluster_test(d["leader_asset"].isin(RISK_ON_LEADERS), "攻め資産が主役 vs 守り/マクロが主役", rng))

print("\n【切り口B】取引した資産と主役の関係")
cuts.append(cluster_test(d["asset"] == d["leader_asset"], "主役そのものを取引 vs それ以外", rng))
same_class = d.apply(lambda r: CLASS.get(r["asset"]) == CLASS.get(r["leader_asset"]), axis=1)
cuts.append(cluster_test(same_class, "主役と同じ資産クラス vs 別クラス", rng))

print("\n【切り口C】主役の明確さ(2位との差)")
med = d["leader_margin"].median()
cuts.append(cluster_test(d["leader_margin"] > med, f"明確さ上位半分(>{med:.3f}) vs 下位", rng))

print("\n【切り口D】地合いラベル(参考・主役レンズとは別軸)")
cuts.append(cluster_test(d["risk_state"] == "risk_on", "risk_on日 vs それ以外", rng))
cuts.append(cluster_test(d["vol_state"] == "calm", "calm日 vs それ以外", rng))

# 多重比較: 同じ数の切り口を無作為ラベルで試したときの最大差の分布
tried = len([c for c in cuts if c])
print(f"\n【多重比較の補正】試した切り口 = {tried}")
cl_all = d.groupby("cl").agg(win=("win", "mean")).reset_index()
maxdiffs = []
for _ in range(2000):
    best = 0.0
    for _ in range(tried):
        lab = rng.integers(0, 2, len(cl_all))
        if lab.sum() < 3 or (1 - lab).sum() < 3:
            continue
        best = max(best, abs(cl_all["win"].values[lab == 1].mean() - cl_all["win"].values[lab == 0].mean()))
    maxdiffs.append(best)
obs_best = max([c[0] for c in cuts if c], default=0)
print(f"  観測された最大差 = {obs_best:.3f}")
print(f"  無作為ラベルで{tried}切り口試したときの最大差: 中央値{np.median(maxdiffs):.3f} / 95%点{np.percentile(maxdiffs,95):.3f}")
print(f"  補正後p(この大きさが偶然で出る割合) = {np.mean(np.array(maxdiffs) >= obs_best):.3f}")

# 頑健性: 主役判定の窓を変えても結論が動くか(W=20は事前宣言値)
print("\n【頑健性】主役判定の窓を変えた場合(切り口Aのみ)")
prices = pd.read_csv("data/retro/prices_long.csv", parse_dates=["date"])
wide = prices.pivot_table(index="date", columns="asset", values="ret_cc")
for W in (10, 20, 40):
    ar = wide.abs()
    act = ar.rolling(W, min_periods=max(4, W // 2)).mean() / ar.rolling(120, min_periods=40).mean()
    cs = pd.DataFrame(0.0, index=wide.index, columns=wide.columns)
    cn = pd.DataFrame(0, index=wide.index, columns=wide.columns)
    cols = list(wide.columns)
    for i, a in enumerate(cols):
        for b in cols[i + 1:]:
            c = wide[a].rolling(W, min_periods=max(4, W // 2)).corr(wide[b]).abs()
            cs[a] += c.fillna(0); cs[b] += c.fillna(0)
            cn[a] += c.notna().astype(int); cn[b] += c.notna().astype(int)
    dom = (cs / cn.replace(0, np.nan)) * act
    ld = dom.idxmax(axis=1, skipna=True).rename("ldr").reset_index()
    dd = pd.merge_asof(d[["date", "cl", "win"]].sort_values("date"), ld.sort_values("date"),
                       on="date", direction="backward", allow_exact_matches=False)
    dd = dd[dd["ldr"].notna()]
    sub = dd.assign(lab=dd["ldr"].isin(RISK_ON_LEADERS).astype(int))
    cl2 = sub.groupby("cl").agg(win=("win", "mean"), lab=("lab", "mean")).reset_index()
    cl2["lab"] = (cl2["lab"] >= 0.5).astype(int)
    if cl2["lab"].sum() >= 3 and (1 - cl2["lab"]).sum() >= 3:
        diff = cl2[cl2["lab"] == 1]["win"].mean() - cl2[cl2["lab"] == 0]["win"].mean()
        print(f"  W={W}: クラスタ{int(cl2['lab'].sum())}vs{int((1-cl2['lab']).sum())} 勝率差{diff:+.3f}")
    else:
        print(f"  W={W}: 判定不能")
