from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
import yfinance as yf

ASSETS = {
    'BTC-USD': 'BTC', 'GC=F': 'GOLD', 'CL=F': 'WTI', 'JPY=X': 'USDJPY',
    'ES=F': 'SPX', 'NQ=F': 'NASDAQ', 'DX-Y.NYB': 'DXY', '^VIX': 'VIX', '^TNX': 'US10Y'
}
RAW_DIR = Path('data/raw')
RESULTS_DIR = Path('results')

def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    run_ts = datetime.now(timezone.utc).isoformat()
    for ticker, asset in ASSETS.items():
        try:
            df = yf.download(ticker, period='180d', interval='1d', auto_adjust=False, progress=False)
            if df.empty:
