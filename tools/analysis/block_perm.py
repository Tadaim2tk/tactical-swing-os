"""月ブロック入れ替えの共通実装（#139/#140 Codex P1 対応）。

誤り: 各月を多数決ラベル1個に潰してから入れ替えると、観測統計量（日次ラベル）と
帰無分布（月次ラベル）が別の推定量になる。実測では53か月中30か月が両ラベルを含み、
潰した瞬間に比較対象がすり替わっていた。

正: **ブロックの並び順だけを入れ替える**。ブロック内の日次ラベル構造はそのまま保つので、
観測統計量と同じ推定量のまま帰無分布が作れる。
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def block_permutation(values, labels, blocks, n_perm: int = 5000, seed: int = 1):
    """ブロック順の入れ替えによる両側p値。

    values/labels/blocks は同じ長さの1次元配列。labels は 0/1。
    戻り値: (観測差, p値, 有効ブロック数)
    """
    v = np.asarray(values, dtype=float)
    lab = np.asarray(labels, dtype=int)
    blk = np.asarray(blocks)
    ok = ~np.isnan(v)
    v, lab, blk = v[ok], lab[ok], blk[ok]
    if lab.sum() == 0 or (1 - lab).sum() == 0:
        return float("nan"), float("nan"), 0
    obs = v[lab == 1].mean() - v[lab == 0].mean()

    df = pd.DataFrame({"v": v, "l": lab, "b": blk})
    groups = [g["l"].values for _, g in df.groupby("b", sort=True)]
    rng = np.random.default_rng(seed)
    null = []
    for _ in range(n_perm):
        order = rng.permutation(len(groups))
        lp = np.concatenate([groups[i] for i in order])
        if lp.sum() == 0 or (1 - lp).sum() == 0:
            continue
        null.append(v[lp == 1].mean() - v[lp == 0].mean())
    if not null:
        return obs, float("nan"), len(groups)
    return obs, float(np.mean(np.abs(null) >= abs(obs))), len(groups)


def forward_return_on_own_calendar(prices_long: pd.DataFrame, asset: str, date, bars: int = 5):
    """資産固有の営業日カレンダー上で bars 本先までのリターン（#139 Codex P1）。

    market_daily は暦の和集合（暗号資産のせいで週末行がある）なので、行を5つ進めても
    週5日資産にとっては5営業日にならない。必ず各資産の系列上で数える。
    """
    g = prices_long[prices_long["asset"] == asset]
    if g.empty:
        return np.nan
    d = pd.to_datetime(date).normalize()
    idx = int(g["date"].searchsorted(d, side="left"))
    if idx >= len(g) or idx + bars >= len(g):
        return np.nan
    c0 = float(g.iloc[idx]["close"])
    c1 = float(g.iloc[idx + bars]["close"])
    if not (c0 > 0):
        return np.nan
    return c1 / c0 - 1.0
