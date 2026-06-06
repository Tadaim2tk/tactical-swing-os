from pathlib import Path
from datetime import datetime, timezone
import pandas as pd, yfinance as yf

ASSETS={'BTC-USD':'BTC','GC=F':'GOLD','CL=F':'WTI','JPY=X':'USDJPY','ES=F':'SPX','NQ=F':'NASDAQ','DX-Y.NYB':'DXY','^VIX':'VIX','^TNX':'US10Y'}

def main():
    Path('data/raw').mkdir(parents=True,exist_ok=True); Path('results').mkdir(exist_ok=True)
    rows=[]; ts=datetime.now(timezone.utc).isoformat()
    for ticker,asset in ASSETS.items():
