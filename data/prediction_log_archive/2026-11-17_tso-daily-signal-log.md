<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-11-17 07:00 JST -->
<!-- transport: Complete original read_thread message f896518c-04db-4fb0-b21a-b5337c37ab09; raw markdown -->
<!-- archived_at: 2026-11-16T23:03:47Z / chars: 13411 / 値は無修正 -->

# Tactical Swing OS v2 — 2026年11月17日（火）

実行モデル：GPT-6
評価基準：日本時間 2026年11月17日 07:02頃
本日の市場の主役：**NASDAQ**
市場レジーム：RISK\_OFF
運用モード：通常寄り防御

## 1\. 本日の結論

**A級0件、B級7件、NO\_TRADE 3件。**

11月16日の米国市場では、ハイテク株を中心に売りが拡大しました。S&amp;P500現物は1.9%安、NASDAQ総合は2.5%安となり、NVIDIAも4.1%下落しています。これらは市場環境の判断材料であり、TSOのSPX・NASDAQ行にはES・NQ先物を使用します。

金は12月限が約3853ドルまで下落し、WTIも85.72ドルで清算されました。ドル指数は103.50付近まで上昇しました。

今回の優先順位は次のとおりです。

| 優先 | 資産 | 判断 | RR | expected\_r |
|--------|--------|--------|--------|--------|
| 1 | NASDAQ | B SELL | 1.571 | \+0.42R |
| 2 | WTI | B SELL | 1.625 | \+0.33R |
| 3 | USDJPY | B BUY | 1.600 | \+0.31R |
| 4 | SPX | B SELL | 1.609 | \+0.29R |
| 5 | GOLD | B SELL | 1.625 | \+0.28R |
| 6 | DXY | B BUY | 1.727 | \+0.27R |
| 7 | ETH | B SELL | 1.453 | \+0.25R |

**B+観察候補：NASDAQ、WTI。**

NASDAQはCBS74、EMS66、RR1.571、較正後参考勝率0.55。WTIはCBS72、EMS64、RR1.625、較正後参考勝率0.54でB+条件を満たします。

ただし、前日までの10営業日分の完全な日足OHLCを照合できていないため、ATR10によるSL下限の実測確認は未完了です。方向判断は継続しますが、A級への認定は行いません。

## 2\. 前回判断の簡易検証

11月16日の方向あり判断4件と、直近のBTC方向判断を確認しました。

| signal\_id | 無効化水準 | 判定 |
|--------|--------|--------|
| 20261116\_GOLD\_SELL\_PULLBACK | 4050超 | not\_fired |
| 20261114\_BTC\_SELL\_PULLBACK | 74500超 | unknown |
| 20261116\_ETH\_SELL\_PULLBACK | 2070超 | unknown |
| 20261116\_WTI\_SELL\_PULLBACK | 96超 | not\_fired |
| 20261116\_USDJPY\_BUY\_PULLBACK | 158.20割れ | not\_fired |

GOLDの12月限は11月16日に下落し、WTIも85.72ドルで清算されました。USDJPYについては日銀公表の11月16日レンジが159.37～159.88円であり、158.20円には達していません。ただし、米国時間を含む全時間帯の高安値を確認できていないため、これらのnot\_firedは取得済みデータ範囲での暫定判定です。

BTCとETHは判断日以降の連続した高値・安値を十分に照合できず、unknownを維持します。

`invalidation_check: 20261116_GOLD_SELL_PULLBACK=not_fired, 20261114_BTC_SELL_PULLBACK=unknown, 20261116_ETH_SELL_PULLBACK=unknown, 20261116_WTI_SELL_PULLBACK=not_fired, 20261116_USDJPY_BUY_PULLBACK=not_fired`

## 3\. 市場全体の前提

今回、新規に市場データとニュースを検索しました。

| 資産 | 取得基準値 | 時点・系列 |
|--------|--------|--------|
| GOLD | 約3853 | COMEX 2026年12月限、11/16清算値 |
| BTC | 約64856 | BTC/USD現物、11/16報道時点 |
| ETH | 約1817 | ETH/USD現物、11/16参考値 |
| WTI | 85.72 | WTI先物、11/16清算値 |
| USDJPY | 159.38～159.55 | 11/16米国時間参考値 |
| SPX | 7561 | ES先物、11/16米国早朝参考値 |
| NASDAQ | 27801 | NQ先物、11/16米国早朝参考値 |
| DXY | 103.50 | 11/16取引時間中 |
| US10Y | 約5.12～5.13% | 11/16米国市場 |
| VIX | 19.30 | 11/16終値の参考報告 |

ES・NQの値は米国市場の最終清算値ではありません。11月16日の現物市場の急落を方向判断に反映していますが、先物価格との厳密な同時点照合は未完了です。

GOLDは今回も\*\*COMEX 2026年12月限（GCZ26）\*\*を基準とします。スポット価格との混用は行いません。

主な市場材料は、FRBの追加利上げ観測、米国ハイテク株の売り、ドル高、原油の供給余剰見通しです。Reutersによれば、12月の25bp利上げ確率は約95%まで上昇しています。

参考資料：

- urlReuters — 11月16日のドル高とFRB利上げ観測https://www.reuters.com/world/middle-east/yen-steady-against-euro-dollar-after-soft-japanese-gdp-data-2026-11-16/
- urlReuters — 金価格下落と12月限清算値https://www.reuters.com/world/india/gold-edges-higher-investors-await-warsh-remarks-rate-signals-2026-11-16/
- urlReuters — 原油供給余剰とWTI下落https://www.reuters.com/business/energy/oil-prices-fall-expectations-coming-supply-surplus-2026-11-16/
- urlAP — 11月16日の米国株下落https://apnews.com/article/35786b8f539ec95f16ae0500f71cfcc7
- url日本銀行 — 11月16日外国為替市況https://www.boj.or.jp/statistics/market/forex/fxdaily/fxlist/fx261116.pdf

## 4\. 10資産別判断

| 資産 | 判断 | 主な根拠 |
|--------|--------|--------|
| GOLD | B SELL | ドル高・金利上昇による下落継続 |
| BTC | NO\_TRADE | ETF・CME根拠不足、MES38 |
| ETH | B SELL | 暗号資産全体の弱さ、戻り売り |
| WTI | B SELL | 供給余剰見通し、11/16に3.2%下落 |
| USDJPY | B BUY | ドル高基調。ただし160円近辺の介入警戒 |
| SPX | B SELL | 米国株の下落、リスクオフ |
| NASDAQ | B SELL | ハイテク株売り、AI関連リスク |
| DXY | B BUY | 米金利とドル高の継続 |
| US10Y | NO\_TRADE | 金利方向の短期構造が不明瞭 |
| VIX | NO\_TRADE | 変動率上昇後の反落リスク |

NASDAQとSPXは前日のNO\_TRADEからB級売りへ変更しました。理由は、11月16日の米国株下落によって弱気方向の根拠が増えたためです。

## 5\. A級候補

**該当なし。**

NASDAQが最も近く、CBS74、EMS66、expected\_r0.42です。A級基準のCBS75、expected\_r0.45をわずかに下回っています。

加えて、ATR10実測が未完了であり、MAE想定も0.25R以下ではありません。したがって、B+にとどめます。

## 6\. B級監視候補

| 資産 | Entry帯 | SL | TP1 | TP2 | RR |
|--------|--------|--------|--------|--------|--------|
| GOLD SELL | 3840～3880 | 4020 | 3600 | 3450 | 1.625 |
| ETH SELL | 1800～1850 | 2090 | 1440 | 1320 | 1.453 |
| WTI SELL | 85～87 | 94 | 73 | 69 | 1.625 |
| USDJPY BUY | 159.20～159.60 | 157.90 | 161.80 | 162.70 | 1.600 |
| SPX SELL | 7440～7520 | 7710 | 7110 | 6900 | 1.609 |
| NASDAQ SELL | 27200～27600 | 28800 | 25200 | 24400 | 1.571 |
| DXY BUY | 103.20～103.60 | 102.30 | 105.30 | 106.00 | 1.727 |

上記はモデルが推定した監視用価格計画です。SL距離は実測ATR10との照合前であり、1×ATR10以上という運用規則への適合を保証するものではありません。

| 資産 | win\_prob | expected\_r | MAE想定 |
|--------|--------|--------|--------|
| GOLD | 0.53 | \+0.28R | 0.43R |
| ETH | 0.52 | \+0.25R | 0.48R |
| WTI | 0.54 | \+0.33R | 0.42R |
| USDJPY | 0.53 | \+0.31R | 0.38R |
| SPX | 0.53 | \+0.29R | 0.45R |
| NASDAQ | 0.55 | \+0.42R | 0.35R |
| DXY | 0.53 | \+0.27R | 0.42R |

NASDAQはNVIDIA決算とAI関連ニュース、WTIは中東の輸送・供給リスク、USDJPYは日本当局による為替介入が主要イベントリスクです。

NASDAQ・USDJPYについては、判断日の終値までにEntry帯へ来なければ終値で成行参加する規則を維持します。Entry未到達による不参加確率はexpected\_rから控除していません。

B級は1件0.25%、日次合計0.50%以内とし、7件すべてへの同時参加は想定しません。相関の高いNASDAQとSPXを重複して選ぶ場合も合計リスクを管理します。

## 7\. 触らない資産

BTC、US10Y、VIXの3資産をNO\_TRADEとします。

BTCは下落方向の可能性を否定しませんが、ETFフロー・CME建玉・basisの確認不足に加え、MES38です。現行ルールに従って見送ります。

US10YはFRB利上げ観測が金利上昇材料である一方、11月16日の株安と原油安が金利低下方向にも作用しています。VIXは上昇していますが、19台という水準だけでは継続的な方向優位を判断できません。

## 8\. 後日検証ポイント

1. NASDAQの弱気判断が5営業日後まで有効か。NVIDIA決算前後の反転に注意。
2. WTIが85ドルを割って下落を継続するか、供給ショックで94ドルを超えるか。
3. USDJPYが160円を回復するか、介入警戒によって157.90円を割るか。
4. GOLD12月限が3800ドルを割るか、4020ドルを回復するか。
5. 全B級についてATR10実測値とSL距離を照合する。
6. 11月16日以前の最新方向判断について、invalidationの未確定分を再照合する。

## 9\. Obsidian保存用Observation Draft

```markdown
# TSO Observation — 2026-11-17

model: GPT-6
market_leader: NASDAQ
regime: RISK_OFF
mode: normal_defensive

## Summary
A: 0
B: 7
NO_TRADE: 3

## Directional hypotheses
- NASDAQ SELL B+: technology-led risk-off
- WTI SELL B+: supply surplus
- USDJPY BUY B: strong dollar, intervention risk
- SPX SELL B: equity weakness
- GOLD SELL B: stronger dollar and yields
- DXY BUY B: Fed repricing
- ETH SELL B: crypto weakness

## Risk
- B risk: 0.25% each
- Daily maximum: 0.50%
- Time exit: 5 business days
- TP1/TP2: reference targets

## Data limitations
- ATR10 OHLC incomplete
- ES/NQ final settlement not confirmed
- ETF/CME/basis incomplete
- Some historical invalidation paths incomplete

## Next review
- Reconcile ATR10 and SL
- Confirm latest invalidation states
- Monitor Nvidia earnings and Fed minutes
- Evaluate 5-day realized R
```

## 10\. TSO\_LOG CSVとJSON

以下は固定28列、10資産10行です。RRはEntry中点から再計算し、小数第3位に丸めました。スコア・確率・expected\_rはモデルの主観評価です。

### CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-11-17,20261117_GOLD_SELL_PULLBACK,GOLD,SELL,B,PULLBACK,3840,3880,4020,3600,3450,1.625,0.53,0.28,67,70,34,0.25,RISK_OFF,64,59,57,55,72,60,above_4020,GCZ26_ATR10,partially_verified
2026-11-17,20261117_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,48,49,80,,RISK_OFF,47,42,43,41,56,38,ETF_CME_missing,BTCUSD_spot,partially_verified
2026-11-17,20261117_ETH_SELL_PULLBACK,ETH,SELL,B,PULLBACK,1800,1850,2090,1440,1320,1.453,0.52,0.25,61,65,41,0.25,RISK_OFF,60,52,53,47,66,45,above_2090,ETHUSD_ATR10,partially_verified
2026-11-17,20261117_WTI_SELL_PULLBACK,WTI,SELL,B,PULLBACK,85,87,94,73,69,1.625,0.54,0.33,68,70,35,0.25,EVENT,64,59,57,51,72,55,above_94,CL_futures_ATR10,partially_verified
2026-11-17,20261117_USDJPY_BUY_PULLBACK,USDJPY,BUY,B,PULLBACK,159.2,159.6,157.9,161.8,162.7,1.6,0.53,0.31,65,66,42,0.25,EVENT,61,55,53,50,69,58,below_157.9,USDJPY_ATR10,partially_verified
2026-11-17,20261117_SPX_SELL_PULLBACK,SPX,SELL,B,PULLBACK,7440,7520,7710,7110,6900,1.609,0.53,0.29,65,67,38,0.25,RISK_OFF,62,55,54,50,69,55,above_7710,ESZ26_ATR10,partially_verified
2026-11-17,20261117_NASDAQ_SELL_PULLBACK,NASDAQ,SELL,B,PULLBACK,27200,27600,28800,25200,24400,1.571,0.55,0.42,71,73,31,0.25,RISK_OFF,66,59,58,53,74,58,above_28800,NQZ26_ATR10,partially_verified
2026-11-17,20261117_DXY_BUY_PULLBACK,DXY,BUY,B,PULLBACK,103.2,103.6,102.3,105.3,106,1.727,0.53,0.27,64,65,40,0.25,RISK_OFF,61,57,54,49,68,58,below_102.3,DXY_ATR10,partially_verified
2026-11-17,20261117_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,51,47,67,,MIXED,55,50,47,44,58,52,yield_path_unclear,US10Y_yield,partially_verified
2026-11-17,20261117_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,46,42,75,,RISK_OFF,49,44,42,39,51,45,index_term_structure,VIX_index,partially_verified
```

### JSON

```json
[
  {"date":"2026-11-17","signal_id":"20261117_GOLD_SELL_PULLBACK","asset":"GOLD","side":"SELL","rank":"B","type":"PULLBACK","entry_low":3840,"entry_high":3880,"sl":4020,"tp1":3600,"tp2":3450,"rr":1.625,"win_prob":0.53,"expected_r":0.28,"tq_score":67,"opp_score":70,"no_trade_score":34,"risk_pct":0.25,"regime":"RISK_OFF","ems":64,"ffs":59,"cds":57,"ias":55,"cbs":72,"mes":60,"invalidation":"above_4020","verification_target":"GCZ26_ATR10","verified_status":"partially_verified"},
  {"date":"2026-11-17","signal_id":"20261117_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":48,"opp_score":49,"no_trade_score":80,"risk_pct":null,"regime":"RISK_OFF","ems":47,"ffs":42,"cds":43,"ias":41,"cbs":56,"mes":38,"invalidation":"ETF_CME_missing","verification_target":"BTCUSD_spot","verified_status":"partially_verified"},
  {"date":"2026-11-17","signal_id":"20261117_ETH_SELL_PULLBACK","asset":"ETH","side":"SELL","rank":"B","type":"PULLBACK","entry_low":1800,"entry_high":1850,"sl":2090,"tp1":1440,"tp2":1320,"rr":1.453,"win_prob":0.52,"expected_r":0.25,"tq_score":61,"opp_score":65,"no_trade_score":41,"risk_pct":0.25,"regime":"RISK_OFF","ems":60,"ffs":52,"cds":53,"ias":47,"cbs":66,"mes":45,"invalidation":"above_2090","verification_target":"ETHUSD_ATR10","verified_status":"partially_verified"},
  {"date":"2026-11-17","signal_id":"20261117_WTI_SELL_PULLBACK","asset":"WTI","side":"SELL","rank":"B","type":"PULLBACK","entry_low":85,"entry_high":87,"sl":94,"tp1":73,"tp2":69,"rr":1.625,"win_prob":0.54,"expected_r":0.33,"tq_score":68,"opp_score":70,"no_trade_score":35,"risk_pct":0.25,"regime":"EVENT","ems":64,"ffs":59,"cds":57,"ias":51,"cbs":72,"mes":55,"invalidation":"above_94","verification_target":"CL_futures_ATR10","verified_status":"partially_verified"},
  {"date":"2026-11-17","signal_id":"20261117_USDJPY_BUY_PULLBACK","asset":"USDJPY","side":"BUY","rank":"B","type":"PULLBACK","entry_low":159.2,"entry_high":159.6,"sl":157.9,"tp1":161.8,"tp2":162.7,"rr":1.6,"win_prob":0.53,"expected_r":0.31,"tq_score":65,"opp_score":66,"no_trade_score":42,"risk_pct":0.25,"regime":"EVENT","ems":61,"ffs":55,"cds":53,"ias":50,"cbs":69,"mes":58,"invalidation":"below_157.9","verification_target":"USDJPY_ATR10","verified_status":"partially_verified"},
  {"date":"2026-11-17","signal_id":"20261117_SPX_SELL_PULLBACK","asset":"SPX","side":"SELL","rank":"B","type":"PULLBACK","entry_low":7440,"entry_high":7520,"sl":7710,"tp1":7110,"tp2":6900,"rr":1.609,"win_prob":0.53,"expected_r":0.29,"tq_score":65,"opp_score":67,"no_trade_score":38,"risk_pct":0.25,"regime":"RISK_OFF","ems":62,"ffs":55,"cds":54,"ias":50,"cbs":69,"mes":55,"invalidation":"above_7710","verification_target":"ESZ26_ATR10","verified_status":"partially_verified"},
  {"date":"2026-11-17","signal_id":"20261117_NASDAQ_SELL_PULLBACK","asset":"NASDAQ","side":"SELL","rank":"B","type":"PULLBACK","entry_low":27200,"entry_high":27600,"sl":28800,"tp1":25200,"tp2":24400,"rr":1.571,"win_prob":0.55,"expected_r":0.42,"tq_score":71,"opp_score":73,"no_trade_score":31,"risk_pct":0.25,"regime":"RISK_OFF","ems":66,"ffs":59,"cds":58,"ias":53,"cbs":74,"mes":58,"invalidation":"above_28800","verification_target":"NQZ26_ATR10","verified_status":"partially_verified"},
  {"date":"2026-11-17","signal_id":"20261117_DXY_BUY_PULLBACK","asset":"DXY","side":"BUY","rank":"B","type":"PULLBACK","entry_low":103.2,"entry_high":103.6,"sl":102.3,"tp1":105.3,"tp2":106,"rr":1.727,"win_prob":0.53,"expected_r":0.27,"tq_score":64,"opp_score":65,"no_trade_score":40,"risk_pct":0.25,"regime":"RISK_OFF","ems":61,"ffs":57,"cds":54,"ias":49,"cbs":68,"mes":58,"invalidation":"below_102.3","verification_target":"DXY_ATR10","verified_status":"partially_verified"},
  {"date":"2026-11-17","signal_id":"20261117_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":51,"opp_score":47,"no_trade_score":67,"risk_pct":null,"regime":"MIXED","ems":55,"ffs":50,"cds":47,"ias":44,"cbs":58,"mes":52,"invalidation":"yield_path_unclear","verification_target":"US10Y_yield","verified_status":"partially_verified"},
  {"date":"2026-11-17","signal_id":"20261117_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":46,"opp_score":42,"no_trade_score":75,"risk_pct":null,"regime":"RISK_OFF","ems":49,"ffs":44,"cds":42,"ias":39,"cbs":51,"mes":45,"invalidation":"index_term_structure","verification_target":"VIX_index","verified_status":"partially_verified"}
]
```

**記録結果：10資産10行、CSV各行28列、RR算術照合済み。**

今回の重要な変化は、NASDAQとSPXを新たにB級売りとして記帳したことです。最優先観察対象はNASDAQですが、ATR10下限の実測確認とNQ先物の最新清算値照合が残っています。これらを未確認事項として明示したうえで、日次判断と検証用台帳を継続します。
