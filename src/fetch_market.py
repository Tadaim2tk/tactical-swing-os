from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yfinance as yf


ASSETS = {
    "BTC-USD": "BTC",
    "ETH-USD": "ETH",
    "GC=F": "GOLD",
    "CL=F": "WTI",
    "JPY=X": "USDJPY",
    "ES=F": "SPX",
    "NQ=F": "NASDAQ",
    "DX-Y.NYB": "DXY",
    "^VIX": "VIX",
    "^TNX": "US10Y",
}

RAW_DIR = Path("data/raw")
RESULTS_DIR = Path("results")


def normalize_download(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [str(col[0]) for col in df.columns]

    df = df.reset_index()
    df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]
    rename_map = {
        "datetime": "date",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "adj_close": "adj_close",
        "volume": "volume",
    }
    df = df.rename(columns=rename_map)
    if "date" not in df.columns:
        raise ValueError("downloaded data has no date column")

    keep = ["date", "open", "high", "low", "close", "adj_close", "volume"]
    for col in keep:
        if col not in df.columns:
            df[col] = pd.NA

    df = df[keep].copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")
    for col in ["open", "high", "low", "close", "adj_close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["date", "open", "high", "low", "close"])
    df = df.sort_values("date").drop_duplicates(subset=["date"], keep="last")
    return df


def latest_snapshot(run_ts: str, ticker: str, asset: str, status: str, message: str, df: pd.DataFrame | None) -> dict:
    row = {
        "run_ts": run_ts,
        "asset": asset,
        "ticker": ticker,
        "status": status,
        "message": message,
        "date": None,
        "open": None,
        "high": None,
        "low": None,
        "close": None,
        "volume": None,
        "rows": 0,
    }
    if df is not None and not df.empty:
        last = df.iloc[-1]
        row.update(
            {
                "date": last["date"],
                "open": last["open"],
                "high": last["high"],
                "low": last["low"],
                "close": last["close"],
                "volume": last.get("volume"),
                "rows": len(df),
            }
        )
    return row


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    success_count = 0
    run_ts = datetime.now(timezone.utc).isoformat()

    for ticker, asset in ASSETS.items():
        try:
            downloaded = yf.download(
                ticker,
                period="240d",
                interval="1d",
                progress=False,
                auto_adjust=False,
                threads=False,
            )
            df = normalize_download(downloaded)
            if df.empty:
                rows.append(latest_snapshot(run_ts, ticker, asset, "empty", "no usable OHLC rows", None))
                continue

            output_path = RAW_DIR / f"{asset}.csv"
            df.to_csv(output_path, index=False)
            success_count += 1
            rows.append(latest_snapshot(run_ts, ticker, asset, "ok", "", df))
            print(f"ok: {asset} ({ticker}) rows={len(df)}")
        except Exception as exc:  # noqa: BLE001 - keep the daily cycle alive per asset.
            rows.append(latest_snapshot(run_ts, ticker, asset, "error", str(exc), None))
            print(f"error: {asset} ({ticker}) {exc}")

    snapshot = pd.DataFrame(rows)
    snapshot.to_csv(RESULTS_DIR / "market_snapshot.csv", index=False)
    snapshot.to_json(RESULTS_DIR / "market_snapshot.json", orient="records", indent=2, force_ascii=False)

    if success_count == 0:
        print("market fetch failed: all assets failed")
        return 1

    print(f"market fetch completed: {success_count}/{len(ASSETS)} assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
