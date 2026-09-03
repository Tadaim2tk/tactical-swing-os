"""ERSコーパスのマクロ系列をTSO遡及コーパスへ橋渡しする (SPEC-RNC-001の拡張)。

ERS側 (~/.ers-corpus/regime_history/regime_2021_2026.parquet) は2021-2026の
マクロ20系列を既に取得済み。**再取得せず参照する**（一度きり取得の原則）。

TSOに無くて価値が高いもの:
- SI=F 銀   : 銅と揃えば産業需要、銅を置いて上がれば通貨側。ERS知見が名指しで推奨
- HG=F 銅   : 上の対照
- ^SOX 半導体: NASDAQの内訳。AI相場の主役判定に効く
- ^N225 日経 : 日本株。ERS(決算)との橋渡し軸
- ^FVX/^TYX  : 5年/30年金利。10年だけでは曲線の形が見えない
- SOL/XRP    : 暗号資産の広がり（BTC/ETHだけでは資産クラス内の分散が見えない）

出力: data/retro/macro_ext.csv（資産別 close-to-close、TSO本体の系列とは別ファイル）
provenance: ers_corpus_reference（TSOが自分で取得した系列とは区別する）
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ERS_REGIME = Path.home() / ".ers-corpus/regime_history/regime_2021_2026.parquet"
OUT = Path("data/retro/macro_ext.csv")

# TSO本体(10資産)に無い系列だけを借りる。重複は借りない（出所を混ぜない）。
BORROW = {
    "SI=F": "SILVER", "HG=F": "COPPER", "^SOX": "SOX", "^N225": "N225",
    "^FVX": "US5Y", "^TYX": "US30Y", "SOL-USD": "SOL", "XRP-USD": "XRP",
    "1306.T": "TOPIX_ETF", "1343.T": "JREIT_ETF",
}


def main() -> int:
    if not ERS_REGIME.exists():
        print(f"error: ERSコーパスが見つからない: {ERS_REGIME}", file=sys.stderr)
        return 1
    r = pd.read_parquet(ERS_REGIME)
    r["date"] = pd.to_datetime(r["date"]).dt.normalize()
    r = r[r["symbol"].isin(BORROW)].copy()
    r["asset"] = r["symbol"].map(BORROW)

    frames = []
    for asset, g in r.groupby("asset"):
        g = g.sort_values("date").drop_duplicates("date").reset_index(drop=True)
        out = pd.DataFrame({
            "asset": asset,
            "symbol": g["symbol"].iloc[0],
            "role": g["role"].iloc[0],
            "date": g["date"],
            "close": pd.to_numeric(g["close"], errors="coerce"),
        }).dropna(subset=["close"])
        # 資産固有カレンダー上の close-to-close（埋めない）
        out["ret_cc"] = out["close"].pct_change(fill_method=None)
        frames.append(out)
    ext = pd.concat(frames, ignore_index=True)
    ext["provenance"] = "ers_corpus_reference"
    ext["source_file"] = str(ERS_REGIME)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ext.to_csv(OUT, index=False)

    print(f"borrowed {ext['asset'].nunique()} series, {len(ext)} rows -> {OUT}")
    for asset, g in ext.groupby("asset"):
        print(f"  {asset:10s} {g['symbol'].iloc[0]:9s} {len(g):5d}本 "
              f"{g['date'].min().date()}..{g['date'].max().date()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
