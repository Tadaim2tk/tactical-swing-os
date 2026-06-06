import os
from datetime import datetime, timezone
import pandas as pd
import yfinance as yf

ASSETS = {'BTC-USD':'BTC','GC=F':'GOLD','CL=F':'WTI','JPY=X':'USDJPY','ES=F':'SPX','NQ=F':'NASDAQ','DX-Y.NYB':'DXY','^VIX':'VIX','^TNX':'US10Y'}

os.makedirs('data/raw', exist_ok=True)
os.makedirs('results', exist_ok=True)
rows = []
run_ts = datetime.now(timezone.utc).isoformat()

for ticker, asset in ASSETS.items():
    try:
        df = yf.download(ticker, period='180d', interval='1d', progress=False, auto_adjust=False)
        if df.empty:
            rows.append({'run_ts': run_ts, 'asset': asset, 'ticker': ticker, 'status': 'empty'})
            continue
        if