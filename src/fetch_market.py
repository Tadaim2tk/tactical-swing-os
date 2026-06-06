from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
import yfinance as yf

ASSETS = {
    'BTC-USD': 'BTC',
    'GC=F': 'GOLD',
    'CL=F': 'WTI',
    'JPY=X': 'USDJPY',
    'ES=F': 'SPX',
    'NQ=F': 'NASDAQ',
    'DX-Y.NYB': 'DXY',
    '^VIX': 'VIX',
    '^TNX': 'US10Y'
}

RAW_DIR = Path('data/raw')
RESULTS_DIR = Path('results')


def clean(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [str(c[0]) for c in df.columns]
    df = df.reset_index()
    if 'Date' not in df.columns and 'Datetime' in df.columns:
        df = df.rename(columns={'Datetime': 'Date'})
    keep = [