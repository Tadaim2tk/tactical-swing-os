# -*- coding: utf-8 -*-
"""2026-11-27 の週末の読みで使った測定（docs/weekly_readout_2026-11-27.md の数字の再現）。

    python src/fetch_market.py                                  # 価格(data/raw は git 管理外)を先に取る
    python tools/analysis/weekly_2026_11_27.py                  # 全部
    python tools/analysis/weekly_2026_11_27.py flips direction  # 一部だけ: geometry / flips / direction / rows / chase / weekend

一度きりの探索で、採用した規則は1つも無い。読むときの前提:

* 数字は、実行した日の台帳と価格の窓（直近 240 日ぶん）で決まる。あとから同じコマンドを打つと、窓が進んだぶん
  古い期間の値が変わる（測れない行が増える）。文書の値は main の 401819b の台帳と、2026-11-27 13:45 JST に取った価格。
* 切り口を6つ試した。多重比較の補正はしていない。符号が出たものも「観察」で、次の較正で前向きに確かめる対象。
* 取引しない資産（DXY・US10Y）は除いてある。
* 行（注文）で数えた数字は、同じ見立てを毎日出し直した日数ぶん重なる。見立てごと・判断日ごとの数字を並べて出す。

言葉
----
* 注文 = 台帳の rank A/B で向きのある行。見立て = 同じ資産・同じ向きの注文が3日以内に続く並び（src/throughput_metrics.py）。
* 判断時に閉まっていた足 = src/score_prediction_log.py の decision_time_anchor が返す足（週5日の資産は前日ラベル、
  暗号資産はその1本前）。ATR10 は src/simulate_execution.py の atr_at_decision（その足までの10本）。
* 期限 = 執行シミュレーションの時間決済の足（判断の後に始まる最初の足を0本目として5本先。EXIT_DEADLINE_BARS）。
* 成績 = 執行シミュレーションの r_result。未決着で約定済みの行は、最新の終値で測った含みR（src/open_book.py）を使う。
  「決着」とだけ書いた列は r_result だけ。
* 形成途中の足（系列の最後の足で、src/score_prediction_log.py の bar_is_final が確定と認めないもの）を使うのは、
  この含みR だけ。「期限までの動き」と「届いた割合」には、確定した足しか使わない（#242 Codex P2）。
* 期間: a = 2026-06〜09-15（見立てを毎日出し直していた頃）／b = 09-16〜11-03（注文がほぼ出なかった頃。SL幅 0.6 ATR）／
  c = 11-04〜（いまの本文）。
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import open_book as ob  # noqa: E402
import throughput_metrics as tm  # noqa: E402
from score_prediction_log import _current_utc_date, bar_is_final, decision_time_anchor, load_ohlcv_frame  # noqa: E402
from simulate_execution import EXIT_DEADLINE_BARS, atr_at_decision  # noqa: E402

pd.set_option("display.width", 250)
pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 50)

CONTEXT = {"DXY", "US10Y"}
CRYPTO = {"BTC", "ETH"}
RAW = Path("data/raw")


def final_len(f: pd.DataFrame) -> int:
    """確定した足の本数。系列の最後の足が形成途中なら、その1本を除く。"""
    return len(f) if bar_is_final(f, len(f) - 1, _current_utc_date()) else len(f) - 1


def era(day: str) -> str:
    return "a 06〜09/15" if day < "2026-09-16" else ("b 09/16〜11/03" if day < "2026-11-04" else "c 11/04〜")


# --------------------------------------------------------------------------- 読み込み
def load():
    led = tm.load_ledger(Path("data/signal_log.csv"))
    led = led[~led["asset"].isin(CONTEXT)]
    orders = tm.mark_runs(led).sort_values(["asset", "side_n", "date"]).copy()
    orders["run_id"] = orders.groupby(["asset", "side_n"])["run_start"].cumsum().astype(int)
    orders["k"] = orders.groupby(["asset", "side_n", "run_id"]).cumcount() + 1
    orders["day"] = orders["date"].dt.strftime("%Y-%m-%d")
    orders["key"] = orders["day"] + "|" + orders["asset"]
    orders["era"] = orders["day"].map(era)
    frames = {a: f for a in sorted(orders["asset"].unique()) if not (f := load_ohlcv_frame(a, RAW)).empty}
    missing = sorted(set(orders["asset"]) - set(frames))
    if missing:
        print(f"価格の無い資産（どの測定にも入れない）: {missing}")
    orders = orders[orders["asset"].isin(frames)].reset_index(drop=True)

    sim = pd.read_csv("data/execution_simulation.csv")
    pos = ob.positions(sim, frames)
    d = ob.prepare(sim)
    d["mark"] = pd.Series(pos["mark_r"].values, index=pos["row"].values, dtype=float).reindex(d.index)
    d["key"] = d["date"].astype(str) + "|" + d["asset"]
    d["val"] = np.where(d["status"].isin(ob.SETTLED), d["r"], d["mark"])       # 決着R。未決着で約定済みなら含みR
    orders = orders.merge(d[["key", "status", "r", "mark", "val"]], on="key", how="left")

    led_raw = pd.read_csv("data/signal_log.csv", dtype=str)
    led_raw["key"] = led_raw["date"] + "|" + led_raw["asset"]
    for c in ("entry_low", "entry_high", "sl", "tp1", "rr", "win_prob"):
        led_raw[c] = pd.to_numeric(led_raw[c], errors="coerce")
    orders = orders.merge(led_raw[["key", "entry_low", "entry_high", "sl", "tp1", "rr", "win_prob"]].drop_duplicates("key"), on="key", how="left")
    return orders, frames


def anchors(orders: pd.DataFrame, frames: dict) -> pd.DataFrame:
    """注文ごとに、判断時に閉まっていた足（anchor）・判断後の最初の足（k）・ATR10・その足の終値を付ける。測れない行は落とす。"""
    rows = []
    for i, r in orders.iterrows():
        f = frames[r["asset"]]
        k, a = decision_time_anchor(f, r["date"])
        if a < 10 or a >= len(f):
            continue
        atr = atr_at_decision(f, a)
        if not atr == atr or atr <= 0:
            continue
        rows.append({"i": i, "k": k, "a": a, "atr": atr, "c0": float(f.iloc[a]["close"])})
    x = pd.DataFrame(rows).set_index("i")
    out = orders.join(x.rename(columns={"k": "bar_k", "a": "bar_a"}), how="inner")
    out["sgn"] = np.where(out["side_n"] == "BUY", 1.0, -1.0)
    return out


def result_cols(d: pd.DataFrame) -> dict:
    s = d[d["status"].isin(ob.SETTLED)]
    v = d["val"].dropna()
    return {"注文": len(d), "未約定": int((d["status"] == "no_fill").sum()), "決着": len(s),
            "決着の平均R": round(s["r"].mean(), 3) if len(s) else np.nan, "決着の合計R": round(s["r"].sum(), 2),
            "含みを足した件数": len(v), "含みを足した平均R": round(v.mean(), 3) if len(v) else np.nan,
            "含みを足した合計R": round(v.sum(), 2), "判断日の数": d["day"].nunique()}


# --------------------------------------------------------------------------- 1. SL と TP1 の遠さ
def geometry(orders, frames):
    print("\n" + "=" * 100 + "\n1. SL と TP1 を、判断時の値からどれだけ遠くに置いたか（ATR10 単位）と、期限までに届く幅の実績\n" + "=" * 100)
    print("届いた割合 = その資産の過去の足（価格の窓の全部）で、ある足の終値から期限までのあいだに、高値（安値）が\n"
          "            同じ距離（ATR10 単位）まで動いた割合。向きは問わない実績で、予測ではない。")
    x = anchors(orders, frames)
    reach = {}
    for a, f in frames.items():
        span = (2 if a in CRYPTO else 1) + EXIT_DEADLINE_BARS          # anchor の次の足から期限の足まで（週5日の資産は6本、暗号資産は7本）
        up, dn = [], []
        for i in range(10, final_len(f) - span):                         # 期限の足が確定している窓だけ
            atr = atr_at_decision(f, i)
            if not atr == atr or atr <= 0:
                continue
            w = f.iloc[i + 1:i + 1 + span]
            c0 = float(f.iloc[i]["close"])
            up.append((float(w["high"].max()) - c0) / atr)
            dn.append((c0 - float(w["low"].min())) / atr)
        reach[a] = (np.array(up), np.array(dn))
    fill = np.where(x["sgn"] > 0, x["entry_high"], x["entry_low"])           # 執行シミュレーションと同じ、帯の不利な端
    x["sl_w"] = (fill - x["sl"]).abs() / x["atr"]
    x["tp_d"] = x["sgn"] * (x["tp1"] - x["c0"]) / x["atr"]                   # いまの値から TP1 まで（有利な向き）
    x["sl_d"] = x["sgn"] * (x["c0"] - x["sl"]) / x["atr"]                    # いまの値から SL まで（不利な向き）
    x = x.dropna(subset=["sl_w", "tp_d", "sl_d"])
    x["p_tp"] = [float((reach[a][0 if s > 0 else 1] >= t).mean()) if t > 0 else 1.0 for a, s, t in zip(x["asset"], x["sgn"], x["tp_d"])]
    x["p_sl"] = [float((reach[a][1 if s > 0 else 0] >= t).mean()) if t > 0 else 1.0 for a, s, t in zip(x["asset"], x["sgn"], x["sl_d"])]

    def per(d):
        return pd.Series({"注文": len(d), "SL幅(ATR)": d["sl_w"].median(), "今の値→TP1(ATR)": d["tp_d"].median(),
                          "今の値→SL(ATR)": d["sl_d"].median(), "TP1 に届いた割合": d["p_tp"].median(),
                          "SL に届いた割合": d["p_sl"].median(), "SL幅3ATR以上の行": int((d["sl_w"] >= 3).sum()),
                          "申告rr": d["rr"].median(), "申告win_prob": d["win_prob"].median()})

    def slot(day):
        if day < "2026-11-04":
            return era(day)
        return "c1 11/04〜11/14" if day < "2026-11-15" else ("c2 11/15〜11/20" if day < "2026-11-21" else "c3 11/21〜11/27")
    x["slot"] = x["day"].map(slot)
    print("\n期間ごとの中央値"); print(x.groupby("slot").apply(per).round(2).to_string())
    print("\n日ごとの中央値（11/18〜）"); print(x[x["day"] >= "2026-11-18"].groupby("day").apply(per).round(2).to_string())
    print("\n実際の決着（執行シミュレーション。期間ごと）")
    s = orders[orders["status"].isin(ob.SETTLED)].assign(slot=lambda d: d["day"].map(slot))
    print(s.groupby("slot")["status"].value_counts().unstack(fill_value=0).assign(
        TP1の割合=lambda t: (t.get("filled_tp1", 0) / t.sum(axis=1)).round(2)).to_string())


# --------------------------------------------------------------------------- 2. 向きの入れ替わり
def flips(orders, frames):
    print("\n" + "=" * 100 + "\n2. 向きの入れ替わり（同じ資産で、前の注文から7日以内に BUY⇔SELL が変わった注文）\n" + "=" * 100)
    x = anchors(orders, frames).sort_values(["asset", "date"])
    rows = []
    for a, g in x.groupby("asset"):
        g = g.reset_index(drop=True)
        f = frames[a]
        for i in range(1, len(g)):
            if g.loc[i, "side_n"] == g.loc[i - 1, "side_n"] or (g.loc[i, "date"] - g.loc[i - 1, "date"]).days > 7:
                continue
            anc, k, sgn = int(g.loc[i, "bar_a"]), int(g.loc[i, "bar_k"]), g.loc[i, "sgn"]
            exit_i = k + EXIT_DEADLINE_BARS                              # 期限の足（判断後の最初の足を0本目として5本先）
            # 期限の足が確定していなければ「出そろった」に入れない（形成途中の終値は、足が閉じるまでに変わる）
            after = sgn * (float(f.iloc[exit_i]["close"]) - g.loc[i, "c0"]) / g.loc[i, "atr"] if exit_i < final_len(f) else np.nan
            back = i + 1 < len(g) and g.loc[i + 1, "side_n"] != g.loc[i, "side_n"] and (g.loc[i + 1, "date"] - g.loc[i, "date"]).days <= 2
            last_move = sgn * (float(f.iloc[anc]["close"]) - float(f.iloc[anc - 1]["close"]))
            rows.append({"day": g.loc[i, "day"], "asset": a, "new": g.loc[i, "side_n"], "era": g.loc[i, "era"],
                         "直前の足と同じ向き": bool(last_move > 0), "2日以内にまた反転": bool(back), "期限までの動き(ATR)": after})
    fl = pd.DataFrame(rows)
    print("\n11/15 からの一覧"); print(fl[fl["day"] >= "2026-11-15"].drop(columns="era").round(2).to_string(index=False))
    print("\n期間ごと")
    for name, lo, hi in [("a 06/08〜09/15", "2026-06-08", "2026-09-15"), ("c 11/04〜11/27", "2026-11-04", "2026-11-27"),
                         ("  うち 11/04〜11/17", "2026-11-04", "2026-11-17"), ("  うち 11/18〜11/27", "2026-11-18", "2026-11-27")]:
        d = fl[(fl["day"] >= lo) & (fl["day"] <= hi)]
        days = (pd.Timestamp(hi) - pd.Timestamp(lo)).days + 1
        n_assets = orders[(orders["day"] >= lo) & (orders["day"] <= hi)]["asset"].nunique()
        done = d[d["期限までの動き(ATR)"].notna()]
        by_day = done.groupby("day")["期限までの動き(ATR)"].mean()
        print(f"{name}: {len(d)} 回 / {days} 日 / 注文のあった {n_assets} 資産 → 1資産・7日あたり {len(d) / days * 7 / max(n_assets, 1):.2f} 回"
              f" | 直前の足と同じ向きへ {d['直前の足と同じ向き'].mean():.2f} | 2日以内にまた反転 {d['2日以内にまた反転'].mean():.2f}"
              f" | 期限の足が出そろった {len(done)} 回: 新しい向きへ動いていた {int((done['期限までの動き(ATR)'] > 0).sum())} 回・"
              f"平均 {done['期限までの動き(ATR)'].mean():+.2f} ATR（入れ替わった日ごとの平均の平均 {by_day.mean():+.2f} ATR・{len(by_day)} 日）")


# --------------------------------------------------------------------------- 3. 向きの当たり
def direction(orders, frames):
    print("\n" + "=" * 100 + "\n3. 向きの当たり（採点の台帳。判断の1・3・5本後の終値が予測の側にあった割合）\n" + "=" * 100)
    sc = pd.read_csv("data/prediction_log_scores.csv")
    sc["key"] = sc["date"].astype(str) + "|" + sc["asset"].astype(str)
    x = orders.merge(sc[["key", "side", "fwd_return_1d", "fwd_return_3d", "fwd_return_5d"]], on="key", how="left")
    s = x["side"].map({"LONG": 1.0, "SHORT": -1.0})
    for h in (1, 3, 5):
        x[f"hit{h}"] = np.sign(x[f"fwd_return_{h}d"] * s).replace(0, np.nan)
    x["week"] = x["date"].dt.to_period("W-SUN").map(lambda p: p.start_time.strftime("%m/%d") + "の週")

    def per(d):
        out = {"注文": len(d)}
        for h in (1, 3, 5):
            v = d[f"hit{h}"].dropna()
            out[f"{h}本後 n"] = len(v)
            out[f"{h}本後 当たり"] = round((v > 0).mean(), 2) if len(v) else np.nan
        return pd.Series(out)
    print("\n期間ごと（行）"); print(x.groupby("era").apply(per).to_string())
    print("\n期間ごと（見立ての1本目だけ）"); print(x[x["k"] == 1].groupby("era").apply(per).to_string())
    c = x[x["era"].str.startswith("c")]
    print("\n11/04 からの週ごと（月曜〜日曜）"); print(c.groupby("week").apply(per).to_string())
    print("\n11/04 から・資産ごと"); print(c.groupby("asset").apply(per).to_string())
    for name, d in [("a 06〜09/15", x[x["era"].str.startswith("a")]), ("c 11/04〜", c)]:
        daily = d.dropna(subset=["hit5"]).groupby("day")["hit5"].apply(lambda v: (v > 0).mean())
        print(f"{name}・5本後: 判断日ごとの当たり率の平均 {daily.mean():.2f}（{len(daily)} 日。半分より上 {int((daily > 0.5).sum())} 日・下 {int((daily < 0.5).sum())} 日）")


# --------------------------------------------------------------------------- 4. 見立ての何本目か
def rows(orders, frames):
    print("\n" + "=" * 100 + "\n4. 見立ての何本目の注文か（1本目・2本目…）で分けた成績\n" + "=" * 100)
    x = orders.copy()
    x["bucket"] = pd.cut(x["k"], [0, 1, 2, 5, 999], labels=["1本目", "2本目", "3〜5本目", "6本目〜"])
    print("\n期間 × 何本目か"); print(x.groupby(["era", "bucket"], observed=True).apply(lambda d: pd.Series(result_cols(d))).to_string())
    print("\n全期間"); print(x.groupby("bucket", observed=True).apply(lambda d: pd.Series(result_cols(d))).to_string())
    ideas = []
    for (a, s, rid), g in x.groupby(["asset", "side_n", "run_id"]):
        early, late = g[g["k"] <= 2]["val"].dropna(), g[g["k"] >= 3]["val"].dropna()
        ideas.append({"era": g["era"].iloc[0], "asset": a, "side": s, "start": g["day"].min(), "rows": len(g),
                      "early_n": len(early), "early_sum": early.sum(), "late_n": len(late), "late_sum": late.sum()})
    ideas = pd.DataFrame(ideas)
    late = ideas[ideas["late_n"] > 0]
    print("\n3本目以降に値がある見立て（見立てごと。合計は決着R＋含みR）")
    print(late.drop(columns="era").sort_values("late_sum", ascending=False).round(2).to_string(index=False))
    print(f"\n3本目以降: 見立て {len(late)} 本のうち、合計がプラス {int((late['late_sum'] > 0).sum())} 本・マイナス {int((late['late_sum'] < 0).sum())} 本"
          f" / 合計 {late['late_sum'].sum():+.2f}R（上位3本で {late['late_sum'].nlargest(3).sum():+.2f}R）")
    e = ideas[ideas["early_n"] > 0]
    print(f"1〜2本目: 見立て {len(e)} 本のうち、合計がプラス {int((e['early_sum'] > 0).sum())} 本 / 値のある行 {int(e['early_n'].sum())} / 合計 {e['early_sum'].sum():+.2f}R")
    for name in ("a", "b", "c"):
        ee = e[e["era"].str.startswith(name)]
        print(f"   期間 {name}: 見立て {len(ee)} 本・プラス {int((ee['early_sum'] > 0).sum())} 本・値のある行 {int(ee['early_n'].sum())}・合計 {ee['early_sum'].sum():+.2f}R")


# --------------------------------------------------------------------------- 5. 大きく動いた直後
def chase(orders, frames):
    print("\n" + "=" * 100 + "\n5. 判断の直前に閉まった足が、予測の向きへどれだけ動いていたか（ATR10 単位）で分けた成績\n" + "=" * 100)
    x = anchors(orders, frames)
    prev = [float(frames[a].iloc[int(i) - 1]["close"]) for a, i in zip(x["asset"], x["bar_a"])]
    x["m1"] = x["sgn"] * (x["c0"] - np.array(prev)) / x["atr"]
    x["b"] = pd.cut(x["m1"], [-99, 0.0, 1.0, 99], labels=["逆へ動いた", "同じ向きへ1ATR未満", "同じ向きへ1ATR以上"])
    sc = pd.read_csv("data/prediction_log_scores.csv")
    sc["key"] = sc["date"].astype(str) + "|" + sc["asset"].astype(str)
    x = x.merge(sc[["key", "side", "fwd_return_5d"]], on="key", how="left")
    x["hit5"] = np.sign(x["fwd_return_5d"] * x["side"].map({"LONG": 1.0, "SHORT": -1.0})).replace(0, np.nan)

    def per(d):
        out = result_cols(d)
        v = d["hit5"].dropna()
        out["5本後 n"], out["5本後 当たり"] = len(v), round((v > 0).mean(), 2) if len(v) else np.nan
        return pd.Series(out)
    print("\n全期間"); print(x.groupby("b", observed=True).apply(per).to_string())
    for name in ("a", "c"):
        print(f"\n期間 {name}"); print(x[x["era"].str.startswith(name)].groupby("b", observed=True).apply(per).to_string())
    big = x[x["b"] == "同じ向きへ1ATR以上"]
    print("\n「同じ向きへ1ATR以上」の行を、判断日 × 資産の向きでまとめた数（同じ足を見て出した行は1つの出来事）:",
          big.groupby(["bar_a", "asset"]).ngroups, "（行は", len(big), "）")
    print(big[big["day"] >= "2026-11-01"][["day", "asset", "side_n", "m1", "status", "val"]].round(2).to_string(index=False))


# --------------------------------------------------------------------------- 6. 土日の行
def weekend(orders, frames):
    print("\n" + "=" * 100 + "\n6. 土日に出した行（週5日の資産）と、平日の行\n" + "=" * 100)
    x = orders.copy()
    x["kind"] = np.where(x["asset"].isin(CRYPTO), "暗号資産", np.where(x["date"].dt.dayofweek >= 5, "週5日の資産・土日の行", "週5日の資産・平日の行"))
    print("\n期間 × 種類"); print(x.groupby(["era", "kind"]).apply(lambda d: pd.Series(result_cols(d))).to_string())
    print("\n全期間"); print(x.groupby("kind").apply(lambda d: pd.Series(result_cols(d))).to_string())


SECTIONS = {"geometry": geometry, "flips": flips, "direction": direction, "rows": rows, "chase": chase, "weekend": weekend}


def main(argv=None) -> int:
    names = list(argv if argv is not None else sys.argv[1:]) or list(SECTIONS)
    unknown = [n for n in names if n not in SECTIONS]
    if unknown:
        print(f"知らない名前: {unknown}。使えるのは {list(SECTIONS)}")
        return 2
    orders, frames = load()
    if not frames:
        print("価格が無い。先に python src/fetch_market.py")
        return 1
    last = max(f["date"].iloc[-1] for f in frames.values())
    print(f"台帳の注文 {len(orders)} 行（取引する資産・{orders['day'].min()}〜{orders['day'].max()}）/ 価格は {last:%Y-%m-%d} の足まで")
    for n in names:
        SECTIONS[n](orders, frames)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
