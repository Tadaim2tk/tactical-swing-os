# -*- coding: utf-8 -*-
"""資産ごとの ATR10 を、朝の判断（ChatGPT の日次タスク）が読める表にする。

なぜ要るか（2026-11-27）
------------------------
日次の本文は 2026-11-04 から「SL幅は 1×ATR10 以上」を求めている。ところが 11月の本文は、27 日のうち 20 日で
「ATR10 を計算できない（10日ぶんの四本値を取れない）ので SL は暫定」と書き、10 日はそれを A級にしない理由に挙げていた
（docs/weekly_readout_2026-11-27.md §7.3）。規則だけがあって、計算の材料が渡っていなかった。
2026-11-27 に所有者が「渡す」と決めた（docs/gpt_prompt_changelog.md (23)）。

出すもの
--------
data/atr10_reference.csv（追跡する。朝の判断が読むのは
https://raw.githubusercontent.com/Tadaim2tk/tactical-swing-os/main/data/atr10_reference.csv ）。
1資産1行で、列は asset, as_of, close, atr10, atr10_pct, updated_at_utc。

    python src/fetch_market.py        # 価格(data/raw は git 管理外)を先に取る
    python tools/atr_reference.py

数え方（言葉と計算を一致させるための定義）
------------------------------------------
* atr10 = 執行シミュレーションと同じ（src/simulate_execution.py の atr_at_decision）。ある足までの10本の、真の値幅の平均。
  値幅の単位はその資産の価格と同じ（US10Y は利回りの％ポイント）。
* as_of = その計算に使った最後の足の日付。**確定した足だけ**を使う（src/score_prediction_log.py の bar_is_final。
  系列の最後の足は、ラベルの日から2日たつまで確定と認めない。形成途中の足で値幅を名乗らない）。
* close = as_of の足の終値。atr10_pct = atr10 ÷ close × 100。
* updated_at_utc = **その行を最後に計算し直した時刻**。中身（as_of・close・atr10）が前回と同じ行は、前回の時刻のまま残す。
* この表は夜間に作るので、朝の判断の時点では古い。判断時に閉まっていた足と比べて、週5日の資産は1〜2本前、
  暗号資産は0〜1本前で止まっている。読む側は as_of を見ること。
* ある資産の価格を取れなかった・確定した足が 11 本に満たなかった日は、**その資産の行を前回のまま残す**
  （as_of と updated_at_utc が古いままなので、古いことは読めば分かる）。前回の行も無ければ、その資産の行は出さない。
  0 や空欄の行は書かない。
* 1資産も計算できなければ、表に触らずに 1 で終わる。1行も変わらなければ、表を書き換えない。

材料を渡すだけ。採点・執行シミュレーション・提案・配分に入る数は変えない。試験は src/test_atr_reference.py。
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from score_prediction_log import _current_utc_date, bar_is_final, load_ohlcv_frame  # noqa: E402
from simulate_execution import ATR_FLOOR_BARS, atr_at_decision  # noqa: E402

# 日次の本文（prompts/tso_daily_signal_log.md）が資産を挙げる順。src/fetch_market.py の ASSETS と同じ集合（試験で確かめる）
ASSET_ORDER = ["GOLD", "BTC", "ETH", "WTI", "USDJPY", "SPX", "NASDAQ", "DXY", "US10Y", "VIX"]
COLUMNS = ["asset", "as_of", "close", "atr10", "atr10_pct", "updated_at_utc"]
OUT_CSV = Path("data/atr10_reference.csv")
RAW_DIR = Path("data/raw")


def _sig(value: float, digits: int) -> float:
    """有効数字で丸める（資産ごとに桁が違う。NASDAQ は 1000 台、US10Y は 0.06 台）。"""
    return float(f"{value:.{digits}g}")


def last_final_index(frame: pd.DataFrame, today: pd.Timestamp) -> int:
    """確定した最後の足の位置。無ければ -1。確定していないのは系列の末尾だけなので、後ろから探す。"""
    for i in range(len(frame) - 1, -1, -1):
        if bar_is_final(frame, i, today):
            return i
    return -1


def compute_row(asset: str, frame: pd.DataFrame, today: pd.Timestamp):
    """1資産の行（as_of・close・atr10・atr10_pct）。計算できなければ None。"""
    if frame is None or frame.empty:
        return None
    i = last_final_index(frame, today)
    if i < ATR_FLOOR_BARS:          # 10本の真の値幅には、その前の足の終値を入れて 11 本要る
        return None
    atr = atr_at_decision(frame, i)
    close = float(frame.iloc[i]["close"])
    if not (atr == atr and atr > 0 and close == close and close > 0):
        return None
    return {"asset": asset, "as_of": pd.Timestamp(frame.iloc[i]["date"]).strftime("%Y-%m-%d"),
            "close": _sig(close, 6), "atr10": _sig(atr, 5), "atr10_pct": round(atr / close * 100, 2)}


def read_previous(path: Path) -> dict:
    """前回の表を、資産 → 行（文字列のまま）で返す。読めなければ空。"""
    if not path.exists():
        return {}
    try:
        df = pd.read_csv(path, dtype=str, keep_default_na=False)
    except (pd.errors.EmptyDataError, OSError):
        return {}
    if not set(COLUMNS).issubset(df.columns):
        return {}
    return {str(r["asset"]).strip().upper(): {c: str(r[c]) for c in COLUMNS} for _, r in df.iterrows()}


def _same(new: dict, old: dict) -> bool:
    try:
        return (new["as_of"] == old["as_of"] and float(new["close"]) == float(old["close"])
                and float(new["atr10"]) == float(old["atr10"]))
    except (KeyError, TypeError, ValueError):
        return False


def build(frames: dict, previous: dict, today: pd.Timestamp, now_utc: str):
    """表の行と、資産ごとの扱い（computed / unchanged / kept_previous / missing）を返す。"""
    rows, state = [], {}
    for asset in ASSET_ORDER:
        new = compute_row(asset, frames.get(asset), today)
        old = previous.get(asset)
        if new is None:
            if old is not None:
                rows.append(dict(old))
                state[asset] = "kept_previous"
            else:
                state[asset] = "missing"
            continue
        if old is not None and _same(new, old):
            rows.append(dict(old))
            state[asset] = "unchanged"
            continue
        rows.append({"asset": asset, "as_of": new["as_of"], "close": repr(new["close"]), "atr10": repr(new["atr10"]),
                     "atr10_pct": f"{new['atr10_pct']:.2f}", "updated_at_utc": now_utc})
        state[asset] = "computed"
    return pd.DataFrame(rows, columns=COLUMNS), state


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raw-dir", default=str(RAW_DIR), help="日足の置き場")
    ap.add_argument("--out", default=str(OUT_CSV), help="表の書き先")
    args = ap.parse_args(argv)
    raw_dir, out = Path(args.raw_dir), Path(args.out)

    frames = {a: load_ohlcv_frame(a, raw_dir) for a in ASSET_ORDER}
    previous = read_previous(out)
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    table, state = build(frames, previous, _current_utc_date(), now_utc)

    fresh = [a for a, s in state.items() if s in ("computed", "unchanged")]
    for asset in ASSET_ORDER:
        row = table[table["asset"] == asset]
        detail = "" if row.empty else f" as_of={row.iloc[0]['as_of']} atr10={row.iloc[0]['atr10']} ({row.iloc[0]['atr10_pct']}%)"
        print(f"{asset}: {state[asset]}{detail}")
    if not fresh:
        print("::error::ATR10 を1資産も計算できなかった（価格が無いか、確定した足が足りない）。表は書き換えていない。")
        return 1
    stale = [a for a, s in state.items() if s == "kept_previous"]
    missing = [a for a, s in state.items() if s == "missing"]
    if stale:
        print(f"::warning::計算できず、前回の行を残した資産: {', '.join(stale)}（as_of が古い）")
    if missing:
        print(f"::warning::計算できず、前回の行も無いので表に無い資産: {', '.join(missing)}")
    if not any(s == "computed" for s in state.values()) and out.exists():
        print("変わった行は無い。表は書き換えていない。")
        return 0
    out.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(out, index=False, lineterminator="\n")
    print(f"wrote {out}（{len(table)} 行。計算し直した {sum(s == 'computed' for s in state.values())} 行）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
