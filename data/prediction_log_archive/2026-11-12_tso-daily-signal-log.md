<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-11-12 07:00 JST -->
<!-- transport: Complete original ChatGPT read_thread message ed707a73-4910-411b-af2c-1db63ca6932e; raw markdown -->
<!-- archived_at: 2026-11-11T23:16:45Z / chars: 17915 / 値は無修正 -->

# Tactical Swing OS v2 — 2026-11-12 朝次判断

実行モデル: GPT-6
判断日: 2026-11-12（木）日本時間
本日の市場の主役: **NASDAQ**
GOLD基準限月: COMEX 2026年12月限（GCZ26）

## 1\. 本日の結論

**A級0件、B級9件、NO\_TRADE1件。B+観察候補は6件。**

11月11日の米国市場では、AI関連株の反発により株価指数が大幅上昇した。一方、ドル高と金利上昇圧力は継続し、金と暗号資産には弱さが残った。

最大の判断変更はNASDAQ。前日のSELLシナリオはNQ先物が無効化水準28400を突破したため `fired`。本日はBUYへ転換する。

| 方向 | 資産 |
|--------|--------|
| B BUY | USDJPY、SPX、NASDAQ、DXY、US10Y |
| B SELL | GOLD、BTC、ETH、WTI |
| NO\_TRADE | VIX |

B級9件はすべて方向の見立てと監視水準を記帳する。実際の同時参加は日次合計リスク0.50%以内とし、0.25%リスクなら最大2件を基本とする。

crypto\_grounds: etf=有, cme=有
expected\_r\_basis: subjective

expected\_rには5営業日の時間決済、途中撤退、イベント後の反転リスクを織り込んだ。NASDAQ・BTC・USDJPYについてはEntry未到達による不参加確率を差し引いていない。

## 2\. 前回判断の簡易検証

11月11日の方向あり6件と、11月10日から引き継ぐBTC・WTI・SPXの計9件を確認した。VIXには現在追跡対象となる方向あり判断がない。

| signal\_id | 判定 | 確認内容 |
|--------|--------|--------|
| 20261111\_GOLD\_SELL\_PULLBACK | not\_fired | GCZ26高値4074.70、4180未到達 |
| 20261110\_BTC\_SELL\_PULLBACK | not\_fired | BTC高値74750、78000未到達 |
| 20261111\_ETH\_SELL\_MOMENTUM | not\_fired | ETH高値2103.60、2260未到達 |
| 20261110\_WTI\_SELL\_PULLBACK | not\_fired | CLZ26高値88.73、93未到達 |
| 20261111\_USDJPY\_BUY\_PULLBACK | not\_fired | 安値158.659、156.70未到達 |
| 20261110\_SPX\_BUY\_REVERSAL | not\_fired | ESZ26安値7557、7400未到達 |
| 20261111\_NASDAQ\_SELL\_PULLBACK | **fired** | NQZ26高値28696.50、28400突破 |
| 20261111\_DXY\_BUY\_PULLBACK | not\_fired | DXY安値102.21、100.90未到達 |
| 20261111\_US10Y\_BUY\_MOMENTUM | not\_fired | 11/11債券市場休場、最終通常取引値4.983% |

invalidation\_check: 20261111\_GOLD\_SELL\_PULLBACK=not\_fired, 20261110\_BTC\_SELL\_PULLBACK=not\_fired, 20261111\_ETH\_SELL\_MOMENTUM=not\_fired, 20261110\_WTI\_SELL\_PULLBACK=not\_fired, 20261111\_USDJPY\_BUY\_PULLBACK=not\_fired, 20261110\_SPX\_BUY\_REVERSAL=not\_fired, 20261111\_NASDAQ\_SELL\_PULLBACK=fired, 20261111\_DXY\_BUY\_PULLBACK=not\_fired, 20261111\_US10Y\_BUY\_MOMENTUM=not\_fired

NASDAQのfired判定は価格水準突破によるもの。前日の複合的な無効化文言に含まれた金利条件とは分け、今回指定された価格基準で判定した。

## 3\. 市場全体の前提

11月11日の米国株式市場は、CoreWeaveの決算をきっかけにAI関連株が反発。S&amp;P500現物指数は1.31%、NASDAQ総合指数は1.60%上昇した。NQ先物も強い上昇となり、前日の弱気判断を維持する根拠が崩れた。urlReuters 2026-11-11https://www.reuters.com/business/sp-500-nasdaq-futures-rise-after-coreweave-soothes-ai-spending-fears-2026-11-11/

一方、10月CPI上振れにより12月のFRB利上げ観測が強まり、ドル指数は102台後半、金先物12月限は約4000ドルへ下落した。urlReuters 金市場 2026-11-11https://www.reuters.com/world/india/gold-edges-higher-after-sharp-selloff-fed-hike-bets-weigh-2026-11-11/

11月11日は米国Veterans Dayで債券現物市場が休場。US10Yの基準は11月10日の通常取引値4.983%とする。

**市場レジーム: MIXED**

株式はRISK\_ON、暗号資産はRISK\_OFF、金利とドルは引き締め方向という分裂した構造。すべてを単一のリスクオン・オフで扱わない。

### 参照価格とATR10

ATR10は直前までの完成済み日足10本について、各日の `max(高値−安値, |高値−前日終値|, |安値−前日終値|)` を平均した値。暗号資産はUTC日足の11月10日まで、US10Yは休場前の11月10日まで、それ以外は11月11日までを使用した。

| 資産 | 基準価格 | ATR10 | データ時点 |
|--------|--------|--------|--------|
| GOLD GCZ26 | 4000.50 | 103.14 | 11/11 |
| BTC/USD | 約74500 | 2497.35 | 11/11 UTC進行中 |
| ETH/USD | 約2080 | 105.65 | 11/11 UTC進行中 |
| WTI CLZ26 | 86.53 | 5.09 | 11/11 |
| USDJPY | 159.85 | 0.99 | 11/11 |
| SPX ESZ26 | 7644.75 | 173.58 | 11/11 |
| NASDAQ NQZ26 | 28505.00 | 1074.10 | 11/11 |
| DXY | 102.94 | 0.65 | 11/11 |
| US10Y | 4.983 | 0.0853 | 11/10 |
| VIX | 17.43 | 4.44 | 11/11 |

価格・日足の参照先はurlYahoo Finance金先物https://finance.yahoo.com/quote/GC%3DF/history/、urlCoinGlass BTChttps://www.coinglass.com/currencies/BTC/historical-data/、urlCoinGlass ETHhttps://www.coinglass.com/currencies/ETH/historical-data/、urlInvesting.com NQhttps://uk.investing.com/indices/nq-100-futures-historical-data、urlEShttps://uk.investing.com/indices/us-spx-500-futures-historical-data、urlWTIhttps://uk.investing.com/commodities/crude-oil-historical-data、urlDXYhttps://www.investing.com/indices/usdollar-historical-data、urlUSDJPYhttps://www.investing.com/currencies/usd-jpy-historical-data、url米10年債https://finance.yahoo.com/quote/%5ETNX/history/、urlVIXhttps://finance.yahoo.com/quote/%5EVIX/history/。

価格提供元の更新タイミングにより、先物の遅延取引値と公式清算値には差がある。ATR10は参照系列を固定して算出したが、独立した市場データフィードによる全日足照合までは完了していない。

## 4\. 10資産別判断

| 資産 | 判断 | Entry帯 | SL | TP1 | TP2 | RR |
|--------|--------|--------|--------|--------|--------|--------|
| GOLD | B SELL | 4000–4050 | 4140 | 3800 | 3700 | 1.96 |
| BTC | B SELL | 73800–75300 | 77200 | 69500 | 66800 | 1.91 |
| ETH | B SELL | 2070–2130 | 2220 | 1870 | 1760 | 1.92 |
| WTI | B SELL | 86.50–89.00 | 93.25 | 78.50 | 75.50 | 1.68 |
| USDJPY | B BUY | 159.30–159.90 | 158.40 | 161.70 | 162.60 | 1.75 |
| SPX | B BUY | 7600–7660 | 7440 | 7950 | 8070 | 1.68 |
| NASDAQ | B BUY | 28300–28700 | 27350 | 30400 | 31400 | 1.65 |
| DXY | B BUY | 102.60–103.00 | 102.00 | 104.10 | 104.80 | 1.63 |
| US10Y | B BUY | 4.95–5.02 | 4.88 | 5.14 | 5.25 | 1.48 |
| VIX | NO\_TRADE | — | — | — | — | — |

すべての方向あり判断でSL幅は実測ATR10以上。RRはEntry中点から再計算済み。

### 方向判断の要点

**GOLD SELL\:** CPI後のドル高と金利上昇が逆風。GCZ26の4000ドル近辺から戻り売りを想定。MAE想定0.38R。金利急低下と4140突破が無効化条件。

**BTC SELL\:** ETFフローは11月10日に約9500万ドルの純流出。CME先物・オプション情報も確認できたが、下落方向の確信は中程度。MES52とし、B級SELLを記帳。MAE想定0.42R。urlCoinGlasshttps://www.coinglass.com/currencies/BTC/historical-data/、urlCME BTC先物https://finance.yahoo.com/quote/BTC%3DF/

**ETH SELL\:** ETF資金流出とBTCに対する相対的な弱さを重視。反発局面を売る構成。MAE想定0.38R。

**WTI SELL\:** 外交交渉による供給プレミアム縮小を想定。ただし中東での新たな攻撃・供給障害が反転要因。供給ショック直後の成行追随は避け、B級の戻り売りのみ記帳。MAE想定0.50R。urlWSJ 2026-11-11https://www.wsj.com/business/energy-oil/oil-prices-rebound-as-middle-east-supply-risks-persist-4e078d4b

**USDJPY BUY\:** 159円台後半まで上昇。ドル高と米国の引き締め観測が主因。ただし円買い介入と日銀発言が主要リスク。MAE想定0.30R。

**SPX BUY\:** ES先物が反発。AI株の回復が指数全体へ波及する可能性を評価。MAE想定0.34R。

**NASDAQ BUY\:** 前日のSELL無効化後、新たにBUYへ転換。NQ先物の強い反発を確認したが、11月5日の大幅下落後で変動率は依然高い。MAE想定0.31R。

**DXY BUY\:** CPI上振れとFRB利上げ観測に整合。MAE想定0.30R。

**US10Y BUY\:** 5%近辺への再上昇を想定。ただし11月11日の債券休場により、翌営業日の価格発見が重要。MAE想定0.40R。

**VIX NO\_TRADE\:** 11月5日の28台から17台まで急低下。さらに売る方向にも反発を買う方向にも、5営業日スイングの期待値が安定しない。

## 5\. A級候補

**該当なし。**

最大expected\_rはUSDJPYの0.44Rで、A級閾値0.45Rをわずかに下回る。加えて、方向あり9件のMAE想定はいずれも0.25Rを超えている。

A級なしはATR未確認による機械的見送りではない。ATR10を計算し、各SLが下限を満たすことを確認したうえでの評価である。

## 6\. B級監視候補

| 資産 | CBS | EMS | win\_prob | expected\_r | B+ |
|--------|--------|--------|--------|--------|--------|
| GOLD | 74 | 65 | 0.54 | 0.37 | 該当 |
| BTC | 67 | 58 | 0.52 | 0.27 | — |
| ETH | 71 | 62 | 0.55 | 0.36 | 該当 |
| WTI | 62 | 52 | 0.51 | 0.19 | — |
| USDJPY | 78 | 70 | 0.58 | 0.44 | 該当 |
| SPX | 74 | 65 | 0.55 | 0.36 | 該当 |
| NASDAQ | 79 | 68 | 0.56 | 0.40 | 該当 |
| DXY | 77 | 69 | 0.57 | 0.43 | 該当 |
| US10Y | 69 | 60 | 0.55 | 0.28 | — |

**B+観察候補\:** GOLD、ETH、USDJPY、SPX、NASDAQ、DXY。

較正後勝率の上方補正は今回適用せず、生の主観確率で判定した。最優先の観察対象はUSDJPY、NASDAQ、DXY。ただしUSDJPYとDXY、NASDAQとSPXにはそれぞれ強い相関があるため、同時参加によるリスク集中を避ける。

## 7\. 触らない資産

VIXのみNO\_TRADE。

急激なボラティリティ低下後で、売りの継続と反発の両方にリスクがある。17台からさらに低下しても、ATR10が4.44と大きいため、5営業日で安定したRRを確保しにくい。

## 8\. 後日検証ポイント

1. NQの前日SELL無効化後、BUY転換が5営業日でプラスRとなるか。
2. USDJPYの160円突破とDXYの103台定着が同時に起きるか。
3. GOLDが4000ドル割れから下落を加速するか。
4. BTC・ETHのETF流出が継続するか。
5. US10Yが休場明けに5%を突破するか。
6. 11月13日予定の米PPIで、金利・ドル・株式の相関構造が変化するか。
7. 9件のB級について、ATR10以上のSLが通常の日中変動に耐えるか。

## 9\. Obsidian保存用Observation Draft

```markdown
---
date: 2026-11-12
system: TSO_v2
model: GPT-6
regime: MIXED
market_leader: NASDAQ
gold_contract: GCZ26
expected_r_basis: subjective
a_count: 0
b_count: 9
no_trade_count: 1
verification: partially_verified
---

# TSO Observation 2026-11-12

## Market
CoreWeave決算を契機にAI関連株が反発。
NASDAQは前日SELL無効化後、BUYへ転換。
一方、CPI上振れによりドル高・金利上昇圧力は継続。

## Signals
A: 0
B: 9
NO_TRADE: 1

B+:
GOLD, ETH, USDJPY, SPX, NASDAQ, DXY

crypto_grounds: etf=有, cme=有
expected_r_basis: subjective

## ATR10
GOLD 103.14
BTC 2497.35
ETH 105.65
WTI 5.09
USDJPY 0.99
SPX 173.58
NASDAQ 1074.10
DXY 0.65
US10Y 0.0853
VIX 4.44

## Previous invalidation
20261111_NASDAQ_SELL_PULLBACK=fired
Other eight latest directional signals=not_fired

## Next verification
- NASDAQ BUY reversal performance
- USDJPY 160 breakout
- DXY 103 hold
- GOLD 4000 breakdown
- US10Y post-holiday move
- Nov 13 US PPI
```

## 10\. TSO\_LOG

固定28列、10資産10行。CSV全行28列、RR算術一致、NO\_TRADE空欄規則を確認済み。

### CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-11-12,20261112_GOLD_SELL_PULLBACK,GOLD,SELL,B,PULLBACK,4000,4050,4140,3800,3700,1.96,0.54,0.37,69,75,22,0.25,MIXED,65,68,63,58,74,62,GCZ26_high_above_4140,GCZ26_HL_ATR10,partially_verified
2026-11-12,20261112_BTC_SELL_PULLBACK,BTC,SELL,B,PULLBACK,73800,75300,77200,69500,66800,1.91,0.52,0.27,61,67,30,0.25,RISK_OFF,58,61,56,51,67,52,BTCUSD_high_above_77200,BTCUSD_ATR10_ETF_CME,partially_verified
2026-11-12,20261112_ETH_SELL_PULLBACK,ETH,SELL,B,PULLBACK,2070,2130,2220,1870,1760,1.92,0.55,0.36,66,70,27,0.25,RISK_OFF,62,63,58,56,71,50,ETHUSD_high_above_2220,ETHUSD_ATR10_ETF_CME,partially_verified
2026-11-12,20261112_WTI_SELL_PULLBACK,WTI,SELL,B,PULLBACK,86.5,89,93.25,78.5,75.5,1.68,0.51,0.19,57,60,45,0.25,EVENT,52,55,49,44,62,45,CLZ26_high_above_93.25,CLZ26_ATR10_Iran_headlines,partially_verified
2026-11-12,20261112_USDJPY_BUY_PULLBACK,USDJPY,BUY,B,PULLBACK,159.3,159.9,158.4,161.7,162.6,1.75,0.58,0.44,73,80,16,0.25,MIXED,70,70,68,65,78,66,USDJPY_low_below_158.4,USDJPY_ATR10_BOJ_intervention,partially_verified
2026-11-12,20261112_SPX_BUY_MOMENTUM,SPX,BUY,B,MOMENTUM,7600,7660,7440,7950,8070,1.68,0.55,0.36,70,74,21,0.25,RISK_ON,65,64,64,60,74,62,ESZ26_low_below_7440,ESZ26_ATR10_CoreWeave_followthrough,partially_verified
2026-11-12,20261112_NASDAQ_BUY_MOMENTUM,NASDAQ,BUY,B,MOMENTUM,28300,28700,27350,30400,31400,1.65,0.56,0.4,76,82,16,0.25,RISK_ON,68,68,70,66,79,64,NQZ26_low_below_27350,NQZ26_ATR10_AI_rally,partially_verified
2026-11-12,20261112_DXY_BUY_MOMENTUM,DXY,BUY,B,MOMENTUM,102.6,103.0,102.0,104.1,104.8,1.63,0.57,0.43,73,78,19,0.25,MIXED,69,67,65,62,77,67,DXY_low_below_102.0,DXY_ATR10_Fed_expectations,partially_verified
2026-11-12,20261112_US10Y_BUY_PULLBACK,US10Y,BUY,B,PULLBACK,4.95,5.02,4.88,5.14,5.25,1.48,0.55,0.28,65,67,31,0.25,EVENT,60,62,57,51,69,61,US10Y_low_below_4.88,US10Y_ATR10_post_holiday,partially_verified
2026-11-12,20261112_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,39,35,80,,MIXED,42,45,37,30,41,38,VIX_four_day_collapse_reversal_risk,VIX_index_ATR10,partially_verified
```

### JSON

```json
{
  "date": "2026-11-12",
  "model": "GPT-6",
  "market_leader": "NASDAQ",
  "gold_contract": "GCZ26",
  "crypto_grounds": {
    "etf": "有",
    "cme": "有"
  },
  "expected_r_basis": "subjective",
  "records": [
    {
      "date": "2026-11-12",
      "signal_id": "20261112_GOLD_SELL_PULLBACK",
      "asset": "GOLD",
      "side": "SELL",
      "rank": "B",
      "type": "PULLBACK",
      "entry_low": 4000,
      "entry_high": 4050,
      "sl": 4140,
      "tp1": 3800,
      "tp2": 3700,
      "rr": 1.96,
      "win_prob": 0.54,
      "expected_r": 0.37,
      "tq_score": 69,
      "opp_score": 75,
      "no_trade_score": 22,
      "risk_pct": 0.25,
      "regime": "MIXED",
      "ems": 65,
      "ffs": 68,
      "cds": 63,
      "ias": 58,
      "cbs": 74,
      "mes": 62,
      "invalidation": "GCZ26_high_above_4140",
      "verification_target": "GCZ26_HL_ATR10",
      "verified_status": "partially_verified"
    },
    {
      "date": "2026-11-12",
      "signal_id": "20261112_BTC_SELL_PULLBACK",
      "asset": "BTC",
      "side": "SELL",
      "rank": "B",
      "type": "PULLBACK",
      "entry_low": 73800,
      "entry_high": 75300,
      "sl": 77200,
      "tp1": 69500,
      "tp2": 66800,
      "rr": 1.91,
      "win_prob": 0.52,
      "expected_r": 0.27,
      "tq_score": 61,
      "opp_score": 67,
      "no_trade_score": 30,
      "risk_pct": 0.25,
      "regime": "RISK_OFF",
      "ems": 58,
      "ffs": 61,
      "cds": 56,
      "ias": 51,
      "cbs": 67,
      "mes": 52,
      "invalidation": "BTCUSD_high_above_77200",
      "verification_target": "BTCUSD_ATR10_ETF_CME",
      "verified_status": "partially_verified"
    },
    {
      "date": "2026-11-12",
      "signal_id": "20261112_ETH_SELL_PULLBACK",
      "asset": "ETH",
      "side": "SELL",
      "rank": "B",
      "type": "PULLBACK",
      "entry_low": 2070,
      "entry_high": 2130,
      "sl": 2220,
      "tp1": 1870,
      "tp2": 1760,
      "rr": 1.92,
      "win_prob": 0.55,
      "expected_r": 0.36,
      "tq_score": 66,
      "opp_score": 70,
      "no_trade_score": 27,
      "risk_pct": 0.25,
      "regime": "RISK_OFF",
      "ems": 62,
      "ffs": 63,
      "cds": 58,
      "ias": 56,
      "cbs": 71,
      "mes": 50,
      "invalidation": "ETHUSD_high_above_2220",
      "verification_target": "ETHUSD_ATR10_ETF_CME",
      "verified_status": "partially_verified"
    },
    {
      "date": "2026-11-12",
      "signal_id": "20261112_WTI_SELL_PULLBACK",
      "asset": "WTI",
      "side": "SELL",
      "rank": "B",
      "type": "PULLBACK",
      "entry_low": 86.5,
      "entry_high": 89,
      "sl": 93.25,
      "tp1": 78.5,
      "tp2": 75.5,
      "rr": 1.68,
      "win_prob": 0.51,
      "expected_r": 0.19,
      "tq_score": 57,
      "opp_score": 60,
      "no_trade_score": 45,
      "risk_pct": 0.25,
      "regime": "EVENT",
      "ems": 52,
      "ffs": 55,
      "cds": 49,
      "ias": 44,
      "cbs": 62,
      "mes": 45,
      "invalidation": "CLZ26_high_above_93.25",
      "verification_target": "CLZ26_ATR10_Iran_headlines",
      "verified_status": "partially_verified"
    },
    {
      "date": "2026-11-12",
      "signal_id": "20261112_USDJPY_BUY_PULLBACK",
      "asset": "USDJPY",
      "side": "BUY",
      "rank": "B",
      "type": "PULLBACK",
      "entry_low": 159.3,
      "entry_high": 159.9,
      "sl": 158.4,
      "tp1": 161.7,
      "tp2": 162.6,
      "rr": 1.75,
      "win_prob": 0.58,
      "expected_r": 0.44,
      "tq_score": 73,
      "opp_score": 80,
      "no_trade_score": 16,
      "risk_pct": 0.25,
      "regime": "MIXED",
      "ems": 70,
      "ffs": 70,
      "cds": 68,
      "ias": 65,
      "cbs": 78,
      "mes": 66,
      "invalidation": "USDJPY_low_below_158.4",
      "verification_target": "USDJPY_ATR10_BOJ_intervention",
      "verified_status": "partially_verified"
    },
    {
      "date": "2026-11-12",
      "signal_id": "20261112_SPX_BUY_MOMENTUM",
      "asset": "SPX",
      "side": "BUY",
      "rank": "B",
      "type": "MOMENTUM",
      "entry_low": 7600,
      "entry_high": 7660,
      "sl": 7440,
      "tp1": 7950,
      "tp2": 8070,
      "rr": 1.68,
      "win_prob": 0.55,
      "expected_r": 0.36,
      "tq_score": 70,
      "opp_score": 74,
      "no_trade_score": 21,
      "risk_pct": 0.25,
      "regime": "RISK_ON",
      "ems": 65,
      "ffs": 64,
      "cds": 64,
      "ias": 60,
      "cbs": 74,
      "mes": 62,
      "invalidation": "ESZ26_low_below_7440",
      "verification_target": "ESZ26_ATR10_CoreWeave_followthrough",
      "verified_status": "partially_verified"
    },
    {
      "date": "2026-11-12",
      "signal_id": "20261112_NASDAQ_BUY_MOMENTUM",
      "asset": "NASDAQ",
      "side": "BUY",
      "rank": "B",
      "type": "MOMENTUM",
      "entry_low": 28300,
      "entry_high": 28700,
      "sl": 27350,
      "tp1": 30400,
      "tp2": 31400,
      "rr": 1.65,
      "win_prob": 0.56,
      "expected_r": 0.40,
      "tq_score": 76,
      "opp_score": 82,
      "no_trade_score": 16,
      "risk_pct": 0.25,
      "regime": "RISK_ON",
      "ems": 68,
      "ffs": 68,
      "cds": 70,
      "ias": 66,
      "cbs": 79,
      "mes": 64,
      "invalidation": "NQZ26_low_below_27350",
      "verification_target": "NQZ26_ATR10_AI_rally",
      "verified_status": "partially_verified"
    },
    {
      "date": "2026-11-12",
      "signal_id": "20261112_DXY_BUY_MOMENTUM",
      "asset": "DXY",
      "side": "BUY",
      "rank": "B",
      "type": "MOMENTUM",
      "entry_low": 102.6,
      "entry_high": 103.0,
      "sl": 102.0,
      "tp1": 104.1,
      "tp2": 104.8,
      "rr": 1.63,
      "win_prob": 0.57,
      "expected_r": 0.43,
      "tq_score": 73,
      "opp_score": 78,
      "no_trade_score": 19,
      "risk_pct": 0.25,
      "regime": "MIXED",
      "ems": 69,
      "ffs": 67,
      "cds": 65,
      "ias": 62,
      "cbs": 77,
      "mes": 67,
      "invalidation": "DXY_low_below_102.0",
      "verification_target": "DXY_ATR10_Fed_expectations",
      "verified_status": "partially_verified"
    },
    {
      "date": "2026-11-12",
      "signal_id": "20261112_US10Y_BUY_PULLBACK",
      "asset": "US10Y",
      "side": "BUY",
      "rank": "B",
      "type": "PULLBACK",
      "entry_low": 4.95,
      "entry_high": 5.02,
      "sl": 4.88,
      "tp1": 5.14,
      "tp2": 5.25,
      "rr": 1.48,
      "win_prob": 0.55,
      "expected_r": 0.28,
      "tq_score": 65,
      "opp_score": 67,
      "no_trade_score": 31,
      "risk_pct": 0.25,
      "regime": "EVENT",
      "ems": 60,
      "ffs": 62,
      "cds": 57,
      "ias": 51,
      "cbs": 69,
      "mes": 61,
      "invalidation": "US10Y_low_below_4.88",
      "verification_target": "US10Y_ATR10_post_holiday",
      "verified_status": "partially_verified"
    },
    {
      "date": "2026-11-12",
      "signal_id": "20261112_VIX_NONE_NO_TRADE",
      "asset": "VIX",
      "side": "NONE",
      "rank": "NO_TRADE",
      "type": "NO_TRADE",
      "entry_low": null,
      "entry_high": null,
      "sl": null,
      "tp1": null,
      "tp2": null,
      "rr": null,
      "win_prob": null,
      "expected_r": null,
      "tq_score": 39,
      "opp_score": 35,
      "no_trade_score": 80,
      "risk_pct": null,
      "regime": "MIXED",
      "ems": 42,
      "ffs": 45,
      "cds": 37,
      "ias": 30,
      "cbs": 41,
      "mes": 38,
      "invalidation": "VIX_four_day_collapse_reversal_risk",
      "verification_target": "VIX_index_ATR10",
      "verified_status": "partially_verified"
    }
  ]
}
```

**本日の記録結果\:** 10資産すべて記帳。前回のNASDAQ SELLはfired、当日の新規判断はBUYへ転換。9件のB級すべてにEntry・SL・TP・RR・主観勝率・expected\_rを設定し、SL幅がATR10以上であることを確認した。
