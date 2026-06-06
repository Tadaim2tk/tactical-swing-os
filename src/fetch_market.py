import os
from datetime import datetime, timezone
import pandas as pd
import yfinance as yf

ASSETS={'BTC-USD':'BTC','GC=F':'GOLD','CL=F':'WTI','JPY=X':'USDJPY','ES=F':'SPX','NQ=F':'NASDAQ','DX-Y.NYB':'DXY','^VIX':'VIX','^TNX':'US10Y'}

os.makedirs('data/raw', exist_ok=True)
os.makedirs('results', exist_ok=True)
rows=[]
for ticker, asset in ASSETS.items():
    df=yf.download(ticker, period='180d', interval='1d', progress=False, auto_adjust=False)
   