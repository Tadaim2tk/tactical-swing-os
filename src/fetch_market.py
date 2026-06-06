from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone

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

RAW