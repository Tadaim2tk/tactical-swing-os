"""SL/TP執行シミュレーション (保守的・反後知恵) — 台帳判断を日足OHLCで擬似執行する。

close基準の方向採点(score_prediction_log)の一段上の忠実度として、
「朝に指値を出していたら何が起きたか」を日足の範囲で再現する。

反後知恵の原則 — 日中の順序が分からない曖昧さは、必ず戦略に不利な側へ倒す:
- 約定価格はゾーン内の最悪価格 (BUY=entry_high / SELL=entry_low)
- 約定した足でSLにも触れていれば、順序不明 → SL成立(-1R)とみなす
- TP1は約定した足では成立させない(翌足以降のみ)。SLとTP1が同じ足なら SL優先
- 判断当日の足は約定検出に含める(7:00 JSTの記帳は各系列の当日セッション開始前。
  境界の曖昧さは上記ルールにより不利側へしか作用しない)
- 記帳水準が**判断時に既知の終値**から10%超乖離した行は excluded_scale として隔離
  (採点系と同じ閾値・同じアンカー規約。監査F3で当日終値からの乖離判定を修正)

執行ポリシー v0 (docs/gpt_prompt_changelog.md の運用と整合):
- 対象: side BUY/SELL・rank A/B・entry/SL記帳あり・risk_pct>0 の判断
- 約定待ち: 判断日を含む5営業日バー。未到達は no_fill
- 決済: SL / TP1 / 判断日+5バー目の終値で時間切れ決済 (TP2・分割決済は扱わない)
- コスト: 未控除(絶対値の出典が未設定のため)。サマリーに R建ての感応度のみ提示

出力:
- data/execution_simulation.csv   (全注文の擬似執行結果・追跡対象)
- results/execution_simulation_summary.json (人間向けサマリー)

表示・研究のみ。実売買・発注は行わない。weights.json も更新しない。
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from score_prediction_log import (
    MAX_REFERENCE_ANCHOR_DEVIATION,
    decision_time_anchor,
    _current_utc_date,
    load_ohlcv_frame,
    normalize_side,
)
from time_utils import format_utc, now_utc

LEDGER_PATH = Path("data/signal_log.csv")
OUT_CSV = Path("data/execution_simulation.csv")
RESULTS_DIR = Path("results")

FILL_WINDOW_BARS = 5   # 判断日を含む約定待ちバー数
# 判断日ラベルのバーを起点(0本目)として EXIT_DEADLINE_BARS 本先、つまり**6本目**の
# 終値で時間切れ決済する。採点側の r_close_5d は判断後**5本目**の終値であり、
# **1バー違う別の量**である(監査F5, 2026-09-06)。
#
# 2026-09-07 の人間の言明で、どちらも「実際の手仕舞い」ではないことが確定した:
#   「何日目とかそういうものを具体的に決めるわけではなく、SLやTPまで引っ張らなくても
#     シナリオ崩壊が確認できれば手仕舞いにしています」
# したがってこれは現実に合わせるべき数ではなく、**測定規約**である。合わせるべきは
# 現実ではなく名前の方で、同じ「5日」で呼ぶのをやめる。
#   - r_close_5d           = 5営業日後の終値で測った方向リターン(決済を含意しない)
#   - filled_time_exit     = 6本目の終値で強制決済したときの執行R(ベンチマーク)
# 実際の手仕舞い(シナリオ崩壊)は invalidation_check として別に記録し始めた(changelog(15))。
EXIT_DEADLINE_BARS = 5  # 判断日ラベルのバーを0本目とした決済期限。実質6本目の終値
COST_SENSITIVITY_R = (0.02, 0.05, 0.10)

# 押し目待ちの逆選択への対処(人間の承認 2026-09-09)。
# 観測: 約定した110件が -6.53R、約定しなかった32件が +24.53R。方向は当たっているのに
# Entry帯へ戻らないまま走った判断に参加できていない(「大相場に乗れないと資産が増えない」)。
# 規則: 判断日ラベルのバーの終値までに約定しなければ、その終値で成行。
# 対象は未約定ぶんの方向Rが正で厚い3資産のみ。WTIは唯一マイナス(-3.04R)なので入れない。
#
# **これは併走させる観測であって、既定の執行規約ではない。** r_result は従来どおり
# 押し目待ちのまま計算し、追った場合を chase_r に別置きする。過去データでの改善は
# 総当たりで選んだ最良値が50件で平均+0.040R であり、補正すれば残らない大きさ。
# 前向きに測って10月の較正で判断する(measurement-discipline: min-P補正)。
CHASE_ASSETS = frozenset({"NASDAQ", "BTC", "USDJPY"})
CHASE_WAIT_BARS = 1

# TP1で全部降りると、伸びた分を取り逃す(人間の承認 2026-09-09)。
# 観測: 約定した118件のうち46件が TP1 を中央値 1.14R ぶん超えて伸びていた(合計55R)。
# 未約定ぶんの17.1Rより大きく、「大相場に乗れない」の主因はこちらの可能性がある。
# 規則: TP1で半分だけ降り、残りを時間決済(6本目の終値)まで持つ。
#
# 残りに置く損切りを2通り測る。どちらにするかを数字で決めるため、両方残す:
#   half_exit_r     残りも元のSLのまま。伸びなければ利益を返上しうる
#   half_exit_be_r  残りは建値(fill_price)で降りる。返上はしないが早く出される
# **これも併走観測であって既定の執行規約ではない。** r_result はTP1全決済のまま。
HALF_EXIT_FRACTION = 0.5

COLUMNS = [
    "date", "signal_id", "asset", "side", "rank", "risk_pct",
    "entry_low", "entry_high", "sl", "tp1",
    "status",        # filled_sl / filled_tp1 / filled_time_exit / no_fill / open / excluded_scale / excluded_bad_levels / invalid_data / data_window_expired
    "reference_deviation",  # reference/anchor-1。隔離の可否を後から検算できるよう常に残す
    "exit_bar_offset",  # 時間決済したバーの位置(判断日ラベル=0本目)。「5日」の曖昧さを列で解消する
    "scale_check",   # passed / excluded / not_checked(判断前のバーが無く検査できない)
    "fill_date", "fill_price", "risk_unit", "exit_date", "exit_price",
    "r_result", "capital_pct",
    # 到達しなかった判断が、方向としては何Rぶん動いたか。status=no_fill の行にだけ入る。
    # Entry帯へ戻らなかった判断ほど方向が当たっている、という逆選択が実際に起きているかを、
    # 執行側の表だけで検算できるようにするための観察列。建値は約定した場合と同じ
    # 「ゾーン内の最悪価格」なので、r_result と同じ物差しで並ぶ。参加はしていない。
    "forgone_r",
    # 押し目を待たずに追った場合の併走観測(CHASE_ASSETS のみ)。r_result とは別枠。
    "chase_status", "chase_r",
    # TP1で半分降りて残りを時間決済まで持った場合の併走観測。r_result とは別枠。
    # _be_ は残りの損切りを建値に上げた版。どちらにするかは10月の較正で決める。
    "half_exit_status", "half_exit_r", "half_exit_be_r",
    "simulated_at_utc",
]


def _num(v) -> float:
    n = pd.to_numeric(v, errors="coerce")
    return float(n) if pd.notna(n) else float("nan")


def simulate_row(row: pd.Series, ohlcv: pd.DataFrame, simulated_at: str) -> dict:
    """台帳1行を擬似執行する(純関数)。曖昧さは不利側へ。"""
    side = normalize_side(row.get("side"))
    out = {
        "date": str(row.get("date") or ""),
        "signal_id": str(row.get("signal_id") or ""),
        "asset": str(row.get("asset") or ""),
        "side": side,
        "rank": str(row.get("rank") or "").strip().upper(),
        "risk_pct": _num(row.get("risk_pct")),
        "entry_low": _num(row.get("entry_low")),
        "entry_high": _num(row.get("entry_high")),
        "sl": _num(row.get("sl")),
        "tp1": _num(row.get("tp1")),
        "status": "invalid_data",
        "fill_date": "", "fill_price": np.nan, "risk_unit": np.nan,
        "exit_date": "", "exit_price": np.nan,
        "r_result": np.nan, "capital_pct": np.nan, "forgone_r": np.nan, "chase_status": "", "chase_r": np.nan,
        "half_exit_status": "", "half_exit_r": np.nan, "half_exit_be_r": np.nan,
        "simulated_at_utc": simulated_at,
    }
    e1, e2, sl, tp1 = out["entry_low"], out["entry_high"], out["sl"], out["tp1"]
    if ohlcv.empty or side not in {"LONG", "SHORT"} or not (e1 == e1 and e2 == e2 and sl == sl):
        return out
    sig_date = pd.to_datetime(out["date"], errors="coerce")
    if pd.isna(sig_date):
        return out
    # 価格窓が信号日より後に始まる場合は約定探索をしない(監査P1-4a: rawは直近240日で
    # 上書きされるため、放置すると2027-02頃から古い判断が窓先頭のバーで「約定」する)。
    if sig_date.normalize() < pd.to_datetime(ohlcv["date"].iloc[0]):
        out["status"] = "data_window_expired"
        return out
    idx0, anchor_idx = decision_time_anchor(ohlcv, sig_date)
    if idx0 >= len(ohlcv):
        out["status"] = "open"  # 当日バー未取得(週末記帳など) — 次回実行で解決
        return out

    # 監査F3 (2026-09-06): 旧実装は ohlcv.iloc[idx0]["close"] = **判断日ラベルのバーの終値**を
    # 基準にしていた。これは判断の22〜26時間後に確定する値であり、判断時には未知。
    # 同じ事前情報・同じ損切り到達でも、後から判明した終値だけで母集団に含むかが変わっていた
    # (監査の合成再現: 当日終値80なら excluded_scale、100なら filled_sl -1R)。
    # 採点側は #128 で decision_time_anchor へ修正済みだったが、執行側に写しが残っていた。
    # 判断前のバーが系列に無い(窓の先頭)場合、この検査は**実施できない**。
    # 実施できないことを理由に標本を落とさない: 系列取り違えの検査は健全性チェックであって
    # シミュレーションの目的ではなく、検査不能を除外に変えると母集団が静かに縮む。
    # 検査できたか否かを scale_check に残し、後から母集団を再構成できるようにする。
    reference = (e1 + e2) / 2
    anchor_close = float(ohlcv.iloc[anchor_idx]["close"]) if anchor_idx >= 0 else float("nan")
    if anchor_idx < 0 or not (anchor_close > 0):
        out["scale_check"] = "not_checked"
    else:
        out["reference_deviation"] = round(reference / anchor_close - 1.0, 6)
        if abs(reference / anchor_close - 1.0) > MAX_REFERENCE_ANCHOR_DEVIATION:
            out["scale_check"] = "excluded"
            out["status"] = "excluded_scale"
            return out
        out["scale_check"] = "passed"

    is_long = side == "LONG"
    fill_price = e2 if is_long else e1  # ゾーン内の最悪価格
    risk = abs(fill_price - sl)
    if risk <= 0:
        out["status"] = "excluded_bad_levels"
        return out
    out["risk_unit"] = round(risk, 6)

    deadline = idx0 + EXIT_DEADLINE_BARS
    fill_i = None
    for i in range(idx0, min(idx0 + FILL_WINDOW_BARS, len(ohlcv))):
        bar = ohlcv.iloc[i]
        if float(bar["low"]) <= e2 and float(bar["high"]) >= e1:
            fill_i = i
            break
    if fill_i is None:
        window_complete = (idx0 + FILL_WINDOW_BARS) <= len(ohlcv)
        out["status"] = "no_fill" if window_complete else "open"
        # 最終バーが形成途中なら逃した分を名乗らない(#165 Codex P2 / #137と同型)。
        # window_complete は行数だけで決まるので、24時間動く資産では
        # 当日ラベルのバーがまだ閉じていないまま5本目に数えられ、
        # 日中値を「終値で測った方向R」として記録してしまう。
        last_i = idx0 + FILL_WINDOW_BARS - 1
        if window_complete and pd.Timestamp(ohlcv.iloc[last_i]["date"]).normalize() < _current_utc_date():
            last = float(ohlcv.iloc[last_i]["close"])
            gain = (last - fill_price) if is_long else (fill_price - last)
            out["forgone_r"] = round(gain / risk, 4)
        return out

    out["fill_date"] = str(ohlcv.iloc[fill_i]["date"].date())
    out["fill_price"] = round(fill_price, 6)

    def finish(status: str, i: int, price: float) -> dict:
        r = (price - fill_price) / risk if is_long else (fill_price - price) / risk
        out["status"] = status
        out["exit_date"] = str(ohlcv.iloc[i]["date"].date())
        out["exit_price"] = round(float(price), 6)
        out["r_result"] = round(float(r), 4)
        rp = out["risk_pct"]
        if rp == rp:
            out["capital_pct"] = round(float(r) * rp, 4)
        return out

    # 約定足: SLのみ判定(順序不明 → 不利側)。TP1は翌足以降
    bar = ohlcv.iloc[fill_i]
    sl_hit = float(bar["low"]) <= sl if is_long else float(bar["high"]) >= sl
    if sl_hit:
        return finish("filled_sl", fill_i, sl)

    for i in range(fill_i + 1, min(deadline + 1, len(ohlcv))):
        bar = ohlcv.iloc[i]
        sl_hit = float(bar["low"]) <= sl if is_long else float(bar["high"]) >= sl
        if sl_hit:  # SLとTP1が同じ足なら SL優先(不利側)
            return finish("filled_sl", i, sl)
        if tp1 == tp1:
            tp_hit = float(bar["high"]) >= tp1 if is_long else float(bar["low"]) <= tp1
            if tp_hit:
                return finish("filled_tp1", i, tp1)
    if deadline < len(ohlcv):
        # 期限バーが形成途中(ラベル日がUTCでまだ過ぎていない)なら時間決済を確定しない
        # (#137 Codex P2と同型: 日中値を終値決済として記録しない)。
        if pd.Timestamp(ohlcv.iloc[deadline]["date"]).normalize() < _current_utc_date():
            out["exit_bar_offset"] = EXIT_DEADLINE_BARS
            return finish("filled_time_exit", deadline, float(ohlcv.iloc[deadline]["close"]))
    out["status"] = "open"  # 期限バー未到来/未確定 — 正直に進行中
    return out


def chase_row(row, ohlcv: pd.DataFrame, wait_bars: int = CHASE_WAIT_BARS) -> tuple[str, float]:
    """押し目を待たずに追った場合を併走で測る。(status, r) を返す。

    wait_bars 本のあいだに Entry帯へ来なければ、その最終バーの**終値**で成行。
    終値で入るので、そのバーの安値/高値は既に過ぎている。SL/TP の判定を同じバーから
    始めると「入る前に付いた値」で決済したことになるため、追った場合だけ翌バーから見る。
    自然約定した場合の規約(ゾーン内の最悪価格・約定足はSLのみ・TP1は翌足以降・SL優先)は
    simulate_row と揃える。ズレると r_result と並べて読めない。

    決済期限は判断日ラベルを0本目とした EXIT_DEADLINE_BARS 本目のまま動かさない。
    遅く入るほど持ち時間が短いのは規則の費用であって、消してよい不都合ではない。
    """
    side = normalize_side(row.get("side"))
    e1, e2 = _num(row.get("entry_low")), _num(row.get("entry_high"))
    sl, tp1 = _num(row.get("sl")), _num(row.get("tp1"))
    if ohlcv.empty or side not in {"LONG", "SHORT"} or not (e1 == e1 and e2 == e2 and sl == sl):
        return "", np.nan
    sig_date = pd.to_datetime(row.get("date"), errors="coerce")
    if pd.isna(sig_date) or sig_date.normalize() < pd.to_datetime(ohlcv["date"].iloc[0]):
        return "", np.nan
    idx0, _ = decision_time_anchor(ohlcv, sig_date)
    if idx0 >= len(ohlcv):
        return "open", np.nan
    is_long = side == "LONG"

    fill_i = fill_price = None
    for i in range(idx0, min(idx0 + wait_bars, len(ohlcv))):
        bar = ohlcv.iloc[i]
        if float(bar["low"]) <= e2 and float(bar["high"]) >= e1:
            fill_i, fill_price = i, (e2 if is_long else e1)
            break
    chased = fill_i is None
    if chased:
        k = idx0 + wait_bars - 1
        # 形成途中のバーの終値で建値を作らない(#137/#165 と同型)
        if k >= len(ohlcv) or pd.Timestamp(ohlcv.iloc[k]["date"]).normalize() >= _current_utc_date():
            return "open", np.nan
        fill_i, fill_price = k, float(ohlcv.iloc[k]["close"])
        if (fill_price <= sl) if is_long else (fill_price >= sl):
            return "beyond_sl", np.nan      # 既に損切り水準の向こう。追わない
        if tp1 == tp1 and ((fill_price >= tp1) if is_long else (fill_price <= tp1)):
            return "beyond_tp1", np.nan     # 目標を過ぎている。追わない

    risk = abs(fill_price - sl)
    if risk <= 0:
        return "", np.nan

    def r_of(price: float) -> float:
        return round(((price - fill_price) if is_long else (fill_price - price)) / risk, 4)

    pre = "chase_" if chased else "band_"
    if not chased:
        bar = ohlcv.iloc[fill_i]
        if (float(bar["low"]) <= sl) if is_long else (float(bar["high"]) >= sl):
            return pre + "sl", r_of(sl)
    deadline = idx0 + EXIT_DEADLINE_BARS
    for i in range(fill_i + 1, min(deadline + 1, len(ohlcv))):
        bar = ohlcv.iloc[i]
        if (float(bar["low"]) <= sl) if is_long else (float(bar["high"]) >= sl):
            return pre + "sl", r_of(sl)
        if tp1 == tp1 and ((float(bar["high"]) >= tp1) if is_long else (float(bar["low"]) <= tp1)):
            return pre + "tp1", r_of(tp1)
    if deadline < len(ohlcv) and pd.Timestamp(ohlcv.iloc[deadline]["date"]).normalize() < _current_utc_date():
        return pre + "time_exit", r_of(float(ohlcv.iloc[deadline]["close"]))
    return "open", np.nan


def half_exit_row(row, ohlcv: pd.DataFrame) -> tuple[str, float, float]:
    """TP1で半分降り、残りを時間決済まで持った場合を測る。

    戻り値 (status, r, r_breakeven)。r は残りの損切りを元のSLに置いたまま、
    r_breakeven は TP1 到達後に残りの損切りを建値へ上げた場合。

    建値・SL優先・TP1は翌足以降・決済期限といった規約は simulate_row と同じ。
    ズレると r_result と並べて読めない。**TP2は使わない**(人間の指定は
    「残りを時間決済まで持つ」であって、二段目の利確ではない)。

    TP1に届かなかった場合・SLが先に付いた場合は、半分に分ける意味が無いので
    r_result と同じ値になる。差が出るのは TP1 を踏んだ行だけ。
    """
    nan = float("nan")
    side = normalize_side(row.get("side"))
    e1, e2 = _num(row.get("entry_low")), _num(row.get("entry_high"))
    sl, tp1 = _num(row.get("sl")), _num(row.get("tp1"))
    if ohlcv.empty or side not in {"LONG", "SHORT"} or not (e1 == e1 and e2 == e2 and sl == sl):
        return "", nan, nan
    if tp1 != tp1:
        return "", nan, nan          # TP1が無ければ分ける対象ではない
    sig_date = pd.to_datetime(row.get("date"), errors="coerce")
    if pd.isna(sig_date) or sig_date.normalize() < pd.to_datetime(ohlcv["date"].iloc[0]):
        return "", nan, nan
    idx0, anchor_idx = decision_time_anchor(ohlcv, sig_date)
    if idx0 >= len(ohlcv):
        return "open", nan, nan
    is_long = side == "LONG"
    ref = (e1 + e2) / 2
    if anchor_idx >= 0:
        ac = float(ohlcv.iloc[anchor_idx]["close"])
        if ac > 0 and abs(ref / ac - 1.0) > MAX_REFERENCE_ANCHOR_DEVIATION:
            return "", nan, nan
    fill_price = e2 if is_long else e1
    risk = abs(fill_price - sl)
    if risk <= 0:
        return "", nan, nan

    def r_of(price):
        return ((price - fill_price) if is_long else (fill_price - price)) / risk

    fill_i = None
    for i in range(idx0, min(idx0 + FILL_WINDOW_BARS, len(ohlcv))):
        bar = ohlcv.iloc[i]
        if float(bar["low"]) <= e2 and float(bar["high"]) >= e1:
            fill_i = i
            break
    if fill_i is None:
        return "", nan, nan          # 建っていない。分ける対象ではない

    deadline = idx0 + EXIT_DEADLINE_BARS

    def hit_sl(bar, level):
        return (float(bar["low"]) <= level) if is_long else (float(bar["high"]) >= level)

    # 約定足はSLのみ判定(順序不明 → 不利側)。TP1は翌足以降
    if hit_sl(ohlcv.iloc[fill_i], sl):
        r = round(r_of(sl), 4)
        return "half_sl_before_tp1", r, r

    tp_i = None
    for i in range(fill_i + 1, min(deadline + 1, len(ohlcv))):
        bar = ohlcv.iloc[i]
        if hit_sl(bar, sl):          # SLとTP1が同じ足なら SL優先(不利側)
            r = round(r_of(sl), 4)
            return "half_sl_before_tp1", r, r
        if (float(bar["high"]) >= tp1) if is_long else (float(bar["low"]) <= tp1):
            tp_i = i
            break

    if tp_i is None:
        # TP1に届かないまま期限。分けても全部でも同じ
        if deadline < len(ohlcv) and pd.Timestamp(ohlcv.iloc[deadline]["date"]).normalize() < _current_utc_date():
            r = round(r_of(float(ohlcv.iloc[deadline]["close"])), 4)
            return "half_no_tp1_time_exit", r, r
        return "open", nan, nan

    # TP1で半分。残りは期限まで。残りの損切りを2通りで測る
    booked = r_of(tp1) * HALF_EXIT_FRACTION
    rest = 1.0 - HALF_EXIT_FRACTION

    def runner(stop):
        for j in range(tp_i + 1, min(deadline + 1, len(ohlcv))):
            if hit_sl(ohlcv.iloc[j], stop):
                return r_of(stop), "stopped"
        if deadline < len(ohlcv) and pd.Timestamp(ohlcv.iloc[deadline]["date"]).normalize() < _current_utc_date():
            return r_of(float(ohlcv.iloc[deadline]["close"])), "time"
        return None, "open"

    r_sl, how_sl = runner(sl)
    r_be, how_be = runner(fill_price)
    if r_sl is None or r_be is None:
        return "open", nan, nan
    return (f"half_tp1_then_{how_sl}",
            round(booked + rest * r_sl, 4),
            round(booked + rest * r_be, 4))


def simulate_ledger(ledger: pd.DataFrame, raw_dir: Path | None = None) -> pd.DataFrame:
    if ledger is None or ledger.empty:
        return pd.DataFrame(columns=COLUMNS)
    simulated_at = format_utc(now_utc())
    kwargs = {"raw_dir": raw_dir} if raw_dir is not None else {}
    cache: dict[str, pd.DataFrame] = {}
    rows = []
    for _, row in ledger.iterrows():
        side = normalize_side(row.get("side"))
        rank = str(row.get("rank") or "").strip().upper()
        rp = _num(row.get("risk_pct"))
        if side not in {"LONG", "SHORT"} or rank not in {"A", "B"} or not (rp == rp and rp > 0):
            continue  # 「朝に指値を出したもの」のみが対象
        asset = str(row.get("asset") or "")
        if asset not in cache:
            cache[asset] = load_ohlcv_frame(asset, **kwargs) if kwargs else load_ohlcv_frame(asset)
        out = simulate_row(row, cache[asset], simulated_at)
        if asset in CHASE_ASSETS and out["status"] not in {"excluded_scale", "excluded_bad_levels",
                                                           "invalid_data", "data_window_expired"}:
            out["chase_status"], out["chase_r"] = chase_row(row, cache[asset])
        if out["status"] not in {"excluded_scale", "excluded_bad_levels",
                                 "invalid_data", "data_window_expired"}:
            (out["half_exit_status"], out["half_exit_r"],
             out["half_exit_be_r"]) = half_exit_row(row, cache[asset])
        rows.append(out)
    return pd.DataFrame(rows, columns=COLUMNS)


def summarize(sim: pd.DataFrame) -> dict:
    resolved_status = {"filled_sl", "filled_tp1", "filled_time_exit"}
    out = {
        "orders": int(len(sim)),
        "excluded_scale": 0, "excluded_bad_levels": 0, "invalid_data": 0,
        "no_fill": 0, "open": 0, "data_window_expired": 0, "fills_resolved": 0,
        "exit_breakdown": {}, "win_rate": None,
        "gross_total_r": None, "avg_r": None, "gross_capital_pct": None,
        "cost_sensitivity_r": {},
        # 未参加の逆選択: no_fill の方向Rが filled の執行Rを上回るなら、
        # Entry規則は「当たった判断ほど落とす」側に働いている。実現Rとは別枠に置く。
        "no_fill_forgone_r": None, "no_fill_forgone_avg_r": None,
        # 追った場合の併走観測(CHASE_ASSETS のみ)。実現Rとは別枠に置く。
        # TP1で半分降りた場合の併走観測。分岐が起きるのはTP1を踏んだ行だけなので、
        # 同じ行の r_result と並べないと差が読めない。baseline は同じ母集団の実現R。
        "half_exit": {"fraction": HALF_EXIT_FRACTION, "orders": 0, "tp1_split": 0,
                      "total_r": None, "total_r_breakeven": None,
                      "baseline_total_r": None, "win_rate": None},
        "chase": {"assets": sorted(CHASE_ASSETS), "wait_bars": CHASE_WAIT_BARS,
                  "orders": 0, "chased": 0, "total_r": None, "avg_r": None, "win_rate": None,
                  "baseline_total_r": None},
        "policy": {
            "fill_window_bars": FILL_WINDOW_BARS,
            "exit_deadline_bars": EXIT_DEADLINE_BARS,
            "conservative_rules": "worst-in-zone fill; same-bar SL loses; TP1 next-bar-only; SL priority",
            "costs": "not deducted (unsourced); sensitivity in R below",
        },
        "requires_human_approval": True,
        "connected_to_signal_score": False,
    }
    if sim.empty:
        return out
    counts = sim["status"].value_counts()
    # data_window_expired もサマリーで数える(#128 Codex P2: 表示カテゴリから消えると
    # ガード発動時に注文内訳が照合不能になる)
    for k in ("excluded_scale", "excluded_bad_levels", "invalid_data", "no_fill", "open", "data_window_expired"):
        out[k] = int(counts.get(k, 0))
    nf = pd.to_numeric(sim.loc[sim["status"] == "no_fill", "forgone_r"], errors="coerce").dropna() \
        if "forgone_r" in sim.columns else pd.Series(dtype=float)
    if not nf.empty:
        out["no_fill_forgone_r"] = round(float(nf.sum()), 2)
        out["no_fill_forgone_avg_r"] = round(float(nf.mean()), 3)
    if "half_exit_r" in sim.columns:
        hv = pd.to_numeric(sim["half_exit_r"], errors="coerce")
        done = sim[hv.notna()]
        if not done.empty:
            a = pd.to_numeric(done["half_exit_r"], errors="coerce")
            b = pd.to_numeric(done["half_exit_be_r"], errors="coerce")
            base = pd.to_numeric(done["r_result"], errors="coerce").dropna()
            out["half_exit"].update({
                "orders": int(len(done)),
                "tp1_split": int(done["half_exit_status"].astype(str)
                                 .str.startswith("half_tp1_then_").sum()),
                "total_r": round(float(a.sum()), 2),
                "total_r_breakeven": round(float(b.sum()), 2),
                "baseline_total_r": round(float(base.sum()), 2) if not base.empty else None,
                "win_rate": round(float((a > 0).mean()), 3),
            })
    if "chase_r" in sim.columns:
        cr = pd.to_numeric(sim["chase_r"], errors="coerce")
        done = sim[cr.notna()]
        if not done.empty:
            v = pd.to_numeric(done["chase_r"], errors="coerce")
            out["chase"].update({
                "orders": int(len(done)),
                "chased": int(done["chase_status"].astype(str).str.startswith("chase_").sum()),
                "total_r": round(float(v.sum()), 2), "avg_r": round(float(v.mean()), 3),
                "win_rate": round(float((v > 0).mean()), 3),
            })
            # 同じ資産の、押し目待ちのままの実現R。並べないと改善かどうか言えない
            base = sim[(sim["asset"].isin(CHASE_ASSETS)) & (sim["status"].isin(resolved_status))]
            bv = pd.to_numeric(base["r_result"], errors="coerce").dropna()
            out["chase"]["baseline_total_r"] = round(float(bv.sum()), 2) if not bv.empty else None
    resolved = sim[sim["status"].isin(resolved_status)].copy()
    out["fills_resolved"] = int(len(resolved))
    if resolved.empty:
        return out
    out["exit_breakdown"] = {k: int(v) for k, v in resolved["status"].value_counts().items()}
    r = pd.to_numeric(resolved["r_result"], errors="coerce").dropna()
    out["gross_total_r"] = round(float(r.sum()), 2)
    out["avg_r"] = round(float(r.mean()), 3)
    out["win_rate"] = round(float((r > 0).mean()), 3)
    cap = pd.to_numeric(resolved["capital_pct"], errors="coerce").dropna()
    out["gross_capital_pct"] = round(float(cap.sum()), 2)
    for c in COST_SENSITIVITY_R:
        out["cost_sensitivity_r"][f"{c:.2f}R"] = round(float(r.sum() - c * len(r)), 2)
    return out


def main() -> int:
    ledger = pd.read_csv(LEDGER_PATH, dtype=str, keep_default_na=False) if LEDGER_PATH.exists() else pd.DataFrame()
    sim = simulate_ledger(ledger)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    sim.to_csv(OUT_CSV, index=False)
    summary = summarize(sim)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "execution_simulation_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"execution simulation: {len(sim)} orders -> {OUT_CSV}")
    print(json.dumps({k: summary[k] for k in ("orders", "fills_resolved", "no_fill", "open", "gross_total_r", "win_rate", "gross_capital_pct", "no_fill_forgone_r", "no_fill_forgone_avg_r")}, ensure_ascii=False))
    c = summary["chase"]
    print(json.dumps({"chase": {k: c[k] for k in ("orders", "chased", "total_r", "avg_r",
                                                  "win_rate", "baseline_total_r")}}, ensure_ascii=False))
    h = summary["half_exit"]
    print(json.dumps({"half_exit": {k: h[k] for k in ("orders", "tp1_split", "total_r",
                                                      "total_r_breakeven", "baseline_total_r",
                                                      "win_rate")}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
