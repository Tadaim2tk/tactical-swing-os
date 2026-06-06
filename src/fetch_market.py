import yfinance as yf
import pandas as pd
from pathlib import Path

ASSETS={
 'BTC-USD':'BTC',
 'GC=F':'GOLD',
 'CL=F':'WTI',
 'JPY=X':'USDJPY'
}

Path('data/raw').mkdir(parents=True,exist_ok=True)
for ticker,name in ASSETS.items():
    df=yf.download(ticker,period='180d',interval='1d',auto_adjust=True,progress=False)
    df.to_csv(f'data/raw/{name}.csv')
print('download complete')
