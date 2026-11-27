# -*- coding: utf-8 -*-
"""進行中の擬似取引（建玉）を、いまの値で測る。日ごとの「確定＋含み」と、週の変化。

なぜ要るか（2026-11-27）
------------------------
ダッシュボードの執行シミュレーションは「決着した擬似取引」の合計だけを出していた。2026-11-23 の週は、
決着ぶんが増えた（13 件・+2.8R）一方で、進行中の 34 件が −11.5R の含み損を抱えていた（11/27 の値）。画面では
週が良く見え、含み損は5営業日後に時間決済で確定するまでどこにも出なかった。負けの週が、終わってから1週間後に見える。

数え方（言葉と計算を一致させるための定義）
------------------------------------------
* 建玉 = data/execution_simulation.csv の status が open で、fill_price がある行（約定済み・未決着）。
  open でも fill_price が無い行は「まだ約定していない」ので建玉ではない（件数だけ別に出す）。
* 含みR = 向き ×（評価の値 − fill_price）÷ risk_unit。fill_price と risk_unit は執行シミュレーションが
  書いた値をそのまま使う（帯の不利な端と、そこから SL まで）。
* 評価の値 = その資産の日足の、その日以前で最も新しい終値。**最新の日は、形成途中の足の終値も使う**
  （いまの値で測るのが目的。執行シミュレーションは形成途中の足では決着させないので、SL や TP1 を越えた足を
  抱えた建玉の含みRは、−1R より悪い値や TP1 より良い値になりうる。次の更新で決着として確定する）。
* 確定＋含み（ある日 t）= t までに決着した行の r_result の合計 ＋ t に建玉だった行の含みR。
  t の建玉 = fill_date ≤ t で、まだ決着していないか exit_date > t の行。決着した日はその行を確定側で数える。
  週5日の資産は、土日には金曜の終値のまま。
* 週 = 月曜〜日曜（throughput_metrics.weekly_table と同じ W-SUN）。週の変化 = その週の最後の日の
  「確定＋含み」− 前の週の最後の日の「確定＋含み」。進行中の週は、最新の日までの変化。
* 測れない建玉 = 価格が無い・risk_unit が 0 以下か欠損・向きが読めない行。含みRに入れず、件数を出す。

含みRは確定した結果ではない。決着したときの r_result とは一致しない。
観測だけ。採点・提案・配分に入る数は変えない。
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from score_prediction_log import RAW_DIR, load_ohlcv_frame

SETTLED = ("filled_sl", "filled_tp1", "filled_time_exit")
_SIDE_SIGN = {"LONG": 1.0, "BUY": 1.0, "SHORT": -1.0, "SELL": -1.0}
_NEEDED = ("asset", "side", "status", "fill_date", "fill_price", "risk_unit", "exit_date", "r_result")


# --------------------------------------------------------------------------- 読み込み
def load_frames(assets, raw_dir: Path = RAW_DIR) -> dict:
    """資産 → 日足。読めない資産は入れない（測れない建玉として数えられる）。"""
    out = {}
    for a in sorted({str(x).strip().upper() for x in assets if isinstance(x, str) and str(x).strip()}):
        f = load_ohlcv_frame(a, raw_dir)
        if f is not None and not f.empty:
            out[a] = f
    return out


def closes_of(frame: pd.DataFrame) -> pd.Series:
    """日付 → 終値（日付順）。"""
    if frame is None or frame.empty or "date" not in frame.columns or "close" not in frame.columns:
        return pd.Series(dtype=float)
    s = pd.Series(pd.to_numeric(frame["close"], errors="coerce").values,
                  index=pd.to_datetime(frame["date"], errors="coerce").dt.normalize())
    s = s[s.index.notna()].dropna()
    return s[~s.index.duplicated(keep="last")].sort_index()


def prepare(sim: pd.DataFrame) -> pd.DataFrame:
    """執行シミュレーションの表から、この計算に要る列だけを型をそろえて取り出す。"""
    cols = ["date", "signal_id", "asset", "side", "sign", "status", "fill_date", "exit_date", "fill_price", "risk_unit", "r"]
    if sim is None or sim.empty or not set(_NEEDED).issubset(sim.columns):
        return pd.DataFrame(columns=cols)
    side = sim["side"].astype(str).str.strip().str.upper()
    out = pd.DataFrame({
        "date": sim["date"].astype(str) if "date" in sim.columns else "",
        "signal_id": sim["signal_id"].astype(str) if "signal_id" in sim.columns else "",
        "asset": sim["asset"].astype(str).str.strip().str.upper(),
        "side": side,
        "sign": side.map(_SIDE_SIGN),
        "status": sim["status"].astype(str).str.strip(),
        "fill_date": pd.to_datetime(sim["fill_date"], errors="coerce").dt.normalize(),
        "exit_date": pd.to_datetime(sim["exit_date"], errors="coerce").dt.normalize(),
        "fill_price": pd.to_numeric(sim["fill_price"], errors="coerce"),
        "risk_unit": pd.to_numeric(sim["risk_unit"], errors="coerce"),
        "r": pd.to_numeric(sim["r_result"], errors="coerce"),
    })
    return out.reset_index(drop=True)[cols]


# --------------------------------------------------------------------------- 測る
def _mark(row, closes: dict, day: pd.Timestamp | None):
    """1行の含みR と、評価に使った足の日付。測れなければ (None, None)。day=None は最新の足。"""
    s = closes.get(row["asset"])
    if s is None or s.empty:
        return None, None
    if day is not None:
        s = s[s.index <= day]
        if s.empty:
            return None, None
    sign, fill, risk = row["sign"], row["fill_price"], row["risk_unit"]
    if not (sign == sign and fill == fill and risk == risk) or risk <= 0:
        return None, None
    return float(sign * (float(s.iloc[-1]) - fill) / risk), s.index[-1]


def positions(sim: pd.DataFrame, frames: dict) -> pd.DataFrame:
    """いまの建玉（約定済み・未決着）を、資産ごとの最新の終値で測る。測れない行は mark_r が欠損。

    row は、渡された表の中で何行目か（0 始まり）。呼ぶ側が元の表の行と突き合わせるのに使う。
    """
    d = prepare(sim)
    cols = ["row", "date", "signal_id", "asset", "side", "fill_date", "fill_price", "risk_unit", "mark_date", "mark_r"]
    held = d[(d["status"] == "open") & d["fill_price"].notna()].copy()
    if held.empty:
        return pd.DataFrame(columns=cols)
    closes = {a: closes_of(f) for a, f in (frames or {}).items()}
    marks = [_mark(r, closes, None) for _, r in held.iterrows()]
    held["mark_r"] = [float("nan") if m is None else m for m, _ in marks]
    held["mark_date"] = [pd.NaT if dt is None else dt for _, dt in marks]
    held["row"] = held.index
    return held.reset_index(drop=True)[cols]


def equity_curve(sim: pd.DataFrame, frames: dict, start, end) -> pd.DataFrame:
    """start〜end の毎日（暦日）について、確定R の累計・建玉の数・含みR・確定＋含み・測れなかった建玉の数。"""
    cols = ["day", "realized_r", "positions", "mark_r", "equity_r", "unmeasured"]
    d = prepare(sim)
    start, end = pd.Timestamp(start).normalize(), pd.Timestamp(end).normalize()
    if d.empty or end < start:
        return pd.DataFrame(columns=cols)
    closes = {a: closes_of(f) for a, f in (frames or {}).items()}
    settled = d[d["status"].isin(SETTLED) & d["r"].notna() & d["exit_date"].notna()]
    filled = d[d["fill_date"].notna() & d["fill_price"].notna() & (d["status"].isin(SETTLED) | (d["status"] == "open"))]
    rows = []
    for t in pd.date_range(start, end, freq="D"):
        realized = float(settled.loc[settled["exit_date"] <= t, "r"].sum())
        held = filled[(filled["fill_date"] <= t) & ((filled["status"] == "open") | (filled["exit_date"] > t))]
        total, n, unmeasured = 0.0, 0, 0
        for _, r in held.iterrows():
            m, _dt = _mark(r, closes, t)
            if m is None:
                unmeasured += 1
            else:
                total += m
                n += 1
        rows.append({"day": t, "realized_r": round(realized, 4), "positions": n, "mark_r": round(total, 4),
                     "equity_r": round(realized + total, 4), "unmeasured": unmeasured})
    return pd.DataFrame(rows, columns=cols)


def weekly_changes(curve: pd.DataFrame) -> pd.DataFrame:
    """日ごとの曲線から、週（月曜〜日曜）ごとの変化。最初の週は前の週の値が無いので出さない。"""
    cols = ["week_start", "last_day", "equity_r", "change_r", "realized_change_r", "mark_r"]
    if curve is None or curve.empty:
        return pd.DataFrame(columns=cols)
    c = curve.sort_values("day").copy()
    c["week"] = pd.to_datetime(c["day"]).dt.to_period("W-SUN")
    last = c.groupby("week").tail(1).reset_index(drop=True)
    rows = []
    for i in range(1, len(last)):
        cur, prev = last.iloc[i], last.iloc[i - 1]
        if cur["week"].ordinal - prev["week"].ordinal != 1:
            continue  # 間の週が抜けている曲線では、前の週との差を名乗らない
        rows.append({"week_start": cur["week"].start_time.normalize(), "last_day": cur["day"],
                     "equity_r": round(float(cur["equity_r"]), 2),
                     "change_r": round(float(cur["equity_r"] - prev["equity_r"]), 2),
                     "realized_change_r": round(float(cur["realized_r"] - prev["realized_r"]), 2),
                     "mark_r": round(float(cur["mark_r"]), 2)})
    return pd.DataFrame(rows, columns=cols)


# --------------------------------------------------------------------------- まとめ
def summary(sim: pd.DataFrame, frames: dict | None = None, raw_dir: Path = RAW_DIR, weeks: int = 2) -> dict:
    """ダッシュボードと CLI が使うまとめ。価格が1つも読めなければ available=False（0 と書かない）。"""
    out = {"available": False, "reason": "", "as_of": "", "positions": 0, "mark_r": None, "unfilled_open": 0,
           "unmeasured": 0, "realized_r": None, "equity_r": None, "by_asset": [], "weeks": []}
    d = prepare(sim)
    if d.empty:
        out["reason"] = "執行シミュレーションの表が空か、列が足りない"
        return out
    open_rows = d[d["status"] == "open"]
    out["unfilled_open"] = int(open_rows["fill_price"].isna().sum())
    if frames is None:
        frames = load_frames(d["asset"].unique(), raw_dir)
    if not frames:
        out["reason"] = "価格（data/raw）を読めなかった"
        return out
    pos = positions(sim, frames)
    measured = pos[pos["mark_r"].notna()] if not pos.empty else pos
    out["positions"] = int(len(measured))
    out["unmeasured"] = int(len(pos) - len(measured))
    realized = float(d.loc[d["status"].isin(SETTLED), "r"].sum())
    mark = float(measured["mark_r"].sum()) if len(measured) else 0.0
    out["realized_r"], out["mark_r"], out["equity_r"] = round(realized, 2), round(mark, 2), round(realized + mark, 2)
    last_bars = [closes_of(f).index[-1] for f in frames.values() if not closes_of(f).empty]
    if not last_bars:
        out["reason"] = "価格（data/raw）に終値が無い"
        return out
    as_of = max(last_bars)
    out["as_of"] = as_of.strftime("%Y-%m-%d")
    if len(measured):
        g = measured.groupby("asset").agg(positions=("mark_r", "size"), mark_r=("mark_r", "sum"), mark_date=("mark_date", "max"))
        out["by_asset"] = [{"asset": a, "positions": int(r["positions"]), "mark_r": round(float(r["mark_r"]), 2),
                            "mark_date": pd.Timestamp(r["mark_date"]).strftime("%Y-%m-%d")}
                           for a, r in g.sort_values("mark_r").iterrows()]
    week_start = as_of.to_period("W-SUN").start_time.normalize()
    curve = equity_curve(sim, frames, week_start - pd.Timedelta(days=7 * max(int(weeks), 1)), as_of)
    wk = weekly_changes(curve)
    out["weeks"] = [{"week_start": r["week_start"].strftime("%Y-%m-%d"), "last_day": pd.Timestamp(r["last_day"]).strftime("%Y-%m-%d"),
                     "equity_r": r["equity_r"], "change_r": r["change_r"], "realized_change_r": r["realized_change_r"],
                     "mark_r": r["mark_r"]} for _, r in wk.tail(max(int(weeks), 1)).iterrows()]
    out["available"] = True
    return out
