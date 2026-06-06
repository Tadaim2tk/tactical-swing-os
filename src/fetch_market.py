from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yfinance as yf


ASSETS = {
    "BTC-USD": "BTC",
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


def _normalise_download