import pandas as pd
from pathlib import Path

Path('results').mkdir(exist_ok=True)
rows=[]
for f in Path('data/raw').glob('*.csv'):
    df=pd.read_csv(f)
    close=df['Close']
    ma20=close.rolling(20).mean().iloc[-1]
    last=close.iloc[-1]
    signal='LONG' if last>ma20 else 'SHORT'
    rows.append([f.stem,last,ma20,signal])

pd.DataFrame(rows,columns=['asset','price','ma20','signal']).to_csv('results/signals.csv',index=False)
print('signals generated')
