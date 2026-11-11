<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-08-21 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 15423 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026年8月21日

データ基準は**8月20日米国市場終値～8月21日07:00 JST前後**。今回は10資産すべて新規取得を試みました。ES/NQは先物系列、VIXはCboe、BTC/ETHは現物を使用しています。

最大の変化は、**8月19日のTreasury buybackによる金利低下が持続しなかったこと**です。米10年債利回りは再び約4.69%へ上昇し、S&P500は7641.16（-0.9%）、NASDAQ総合は26067.17（-1.0%）。WTIも87.83ドルまで上昇しました。citeturn881503news71turn376196news37turn436355view1

一方、COMEX金先物は**4571.40**へ上昇し、BTCは現在**72719ドル**。米スポットBTC ETFも8月17～19日に資金流入が再加速しており、BTCについてはこれまで不足していたprice/flow confirmationがかなり揃いました。citeturn436355view2turn881503finance0turn980659search1turn980659search10

## 1. 本日の結論

**A級：0件。**

**B+：0件。**

**B級：GOLD BUY、BTC BUY。**

**NO_TRADE：ETH、WTI、USDJPY、SPX、NASDAQ、DXY、US10Y、VIX。**

本日の分析順位は、

**GOLD B > BTC B > その他NO_TRADE**

です。

昨日のSPX B+は**新規では解除**します。Treasury買い戻しで一度低下した長期金利が早くも反発し、WTIも87.83へ上昇。ES9月限は7667.75まで下落しました。citeturn376196search14turn436355view1turn376196news39

一方、GOLDはこの逆風下でもCOMEX先物4571.40。BTCも株式市場が下落する中で72k台へ上昇しています。両者に**株式とは異なる相対強度**が出ています。citeturn436355view2turn980659news20

ただし両方とも急上昇後なので**現在値成行BUYは禁止**です。

---

# 2. 前回判断の簡易検証

### SPX B+ BUY → **ENTRY_REACHED / 逆行拡大 / SL未到達**

前回：

**Entry 7640–7690  
SL 7520  
TP1 7910**

8月20日のES9月限は、

**Open 7733  
High 7746.50  
Low 7657.75  
Close 7667.75**

でした。citeturn376196search11turn376196search14

したがってEntry成立。

しかしその後はEntry下側へ進み、

**ENTRY_REACHED  
MAE_EXPANDED  
SL_NOT_REACHED  
THESIS_WEAKENED**

です。

昨日の「Treasury buybackでterm premiumが持続的に低下する」という前提は、少なくとも現時点では確認できません。

---

### GOLD B BUY → **方向成功 / Entry接近**

前回：

**Entry 4440–4490  
SL 4310  
TP1 4720**

8月20日の現物金安値は**4450.08**、COMEX先物決済は4571.40でした。citeturn436355view2

参照系列はCOMEXなので現物4450.08だけでFILL確定にはしませんが、監視帯までかなり近づいた後に上昇しています。

**DIRECTION_SUCCESS  
FILL_PARTIALLY_VERIFIED**

です。

---

### BTC NO_TRADE → **方向上昇 / 追随回避は維持**

昨日約69k時点で、

> breakout確認だが一日急騰後なので追わない

としました。

その後BTCはさらに上昇し、現在**72719**、日中高値72917。citeturn881503finance0

したがって方向だけ見ればBUYでした。

しかしBTCは4日間で約14%上昇しており、20日の上昇にはショートカバーも大きく寄与しました。citeturn980659news17turn980659news20

昨日のNO_TRADEを後知恵で失敗にはしません。

ただし今日はETFフロー確認が増えたため、**NO_TRADE → B BUY PULLBACKへ昇格**させます。

---

### WTI NO_TRADE → **成功継続**

WTIはさらに**87.83ドル、+2.3%**。Brentは93.78ドルです。citeturn436355view1

方向は完全に上。

しかしHormuz封鎖と対イラン圧力という供給ショックが主因です。

ここまで追わなかったことは、

**SUCCESSFUL_AVOIDANCE**

として記録します。

---

# 3. 市場全体の前提

本日のRegimeは、

**`TREASURY_RELIEF_FAILURE / LONG_YIELDS_REBOUND / OIL_INFLATION / EQUITY_RISK_OFF_LITE / GOLD_BTC_ALTERNATIVE_ASSET_STRENGTH`**

です。

8月19日は、

**Treasury buyback↑  
→ US10Y↓  
→ DXY↓  
→ GOLD/BTC↑**

という非常に明瞭な反応でした。

しかし8月20日は10年債利回りが約4.69～4.70%へ戻り、VIXはCboe公式で**16.01、+7.52%**。citeturn376196news39turn436355view3

S&P500 -0.9%、NASDAQ -1.0%。citeturn376196news37

つまり今回のTreasury措置は今のところ、

**regime change**

ではなく、

**one-day relief shock**

だった可能性が高まっています。

さらにWTI 87.83、Brent 93.78という原油高がインフレ・長期金利へ逆風を戻しています。citeturn436355view1

---

# 4. 10資産別判断

| 資産 | 判定 | 核心 |
|---|---|---|
| **GOLD** | **B BUY** | 株安・高金利でも4571、相対強度強い |
| **BTC** | **B BUY** | 72.7k＋ETF流入確認、ただし過熱 |
| ETH | **NO_TRADE** | 価格データ間の不整合・急伸後 |
| WTI | **NO_TRADE** | 87.83、供給ショック追随禁止 |
| USDJPY | **NO_TRADE** | 159.12、金利・介入・BOJが衝突 |
| SPX | **NO_TRADE** | 前回BUY逆行、金利再上昇 |
| NASDAQ | **NO_TRADE** | NQ29300台、長期金利が再び逆風 |
| DXY | **NO_TRADE** | 98.89、財政懸念vs金利上昇 |
| US10Y | **NO_TRADE** | 4.69付近、政策介入と財政懸念が衝突 |
| VIX | **NO_TRADE** | 16.01、risk-off確認だが追随BUY不足 |

USDJPYは**159.12**。ドルは対円で0.6%上昇しました。citeturn436355view0 160円近辺の介入警戒が残るためBUYしません。

NASDAQ参照系列のNQ9月限は8月20日に**29300台**へ低下しています。citeturn376196search12 QQQやNASDAQ総合をEntry価格へ代用していません。

---

# 5. A級候補

**0件です。**

最も近いGOLDでも、

**CBS 82  
EMS 78  
win_prob 0.63  
expected_r 0.43  
MAE 0.27R**

です。

CBS/EMS/RRは十分ですが、

**expected_r < 0.45  
MAE > 0.25R**

なのでA不合格。

BTCもprice/flow confirmationは急改善しましたが、4日で約14%上昇しており、MAE想定を0.31Rまで上げます。citeturn980659news20

---

# 6. B級監視候補

### 1位 GOLD — BUY PULLBACK

**Entry 4480–4530  
SL 4350  
TP1 4750  
TP2 4900  
RR 1.58  
win_prob 0.63  
較正参考 0.65  
expected_r 0.43  
MAE 0.27R  
risk_pct 0.25%**

COMEX決済4571.40なので、**現在値4570台から追いません**。citeturn436355view2

4480～4530へ押した場合のみ。

金は、

**財政不安  
＋ドルへの信認低下  
＋地政学リスク  
＋高Oil**

から「代替的な価値保存先」として買われている面が強くなっています。Reutersも20日のドル・金・BTCの動きを`debasement trade`として説明しています。citeturn436355view0

---

### 2位 BTC — BUY PULLBACK

**Entry 69000–70500  
SL 66000  
TP1 76000  
TP2 80000  
RR 1.67  
win_prob 0.61  
較正参考 0.64  
expected_r 0.40  
MAE 0.31R  
risk_pct 0.25%**

MESを、

**66 → 76**

へ引き上げます。

理由は、今回は価格だけではありません。

8月17日BTC ETF **+297.6M**、18日 **+189.3M**、19日は約**+517M**と流入が続いたとのデータがあります。citeturn980659search10turn980659search1

つまり、

**ETF flow ↑  
＋ BTC price breakout ↑**

が初めて明瞭に一致しました。

以前の、

**positive flow / negative price**

regimeは終了候補です。

ただし現在72719なので、**72k台で追いません**。69～70.5kへの正常なリテストを待ちます。

またXMではBTC最小ロットが資金規模に対して大きくなりやすいため、必要SL66000で実損が約3000円を超えるなら、**Signal=B / Execution=NO_TRADE**です。memcite

---

# 7. 触らない資産

最優先は引き続き**WTI**。

WTIは5営業日連続上昇し87.83ドル。Hormuzの船舶量は戦前を大きく下回ったままで、米国の対イラン圧力も強まっています。citeturn436355view1

ここでBUYすると完全な供給ショック追随です。

NASDAQも本日は触りません。

Treasury買い戻しで19日に長期金利が急低下したにもかかわらず、20日にはその効果が巻き戻されNQは再下落しました。これはGrowth株にとってかなり悪いconfirmationです。citeturn291777news30turn376196search12

---

# 8. 後日検証ポイント

最重要は**Treasury buyback shockの持続期間**です。

8月19日：

**US10Y↓ / DXY↓ / GOLD↑ / BTC↑**

8月20日：

**US10Y再上昇 / 株↓ / Oil↑**

となりました。citeturn291777news30turn291777news31

現時点では、

**「Treasury intervention = persistent regime change」仮説は弱化**

です。

もう一つ非常に重要なのがBTC。

過去数週間は、

**ETF flow positive  
→ price transmission failure**

を記録してきました。

今回は、

**ETF流入継続  
→ 65k突破  
→ 70k突破  
→ 72k**

まで価格へ伝播しました。citeturn980659search1turn881503finance0

今後5日、

**68k維持  
70kリテスト  
ETFフロー  
MFE/MAE**

を記録し、`FLOW_TO_PRICE_LAG` の典型例として検証します。

---

# 9. Obsidian保存用Observation Draft

```markdown
# 2026-08-21 Treasury relief fades / GOLD・BTC relative strength

## Market

S&P500:
7641.16
-0.9%

ES Sep:
7667.75
Low 7657.75

NASDAQ Composite:
26067.17
-1.0%

NQ Sep:
~29300s

US10Y:
~4.69-4.70%

DXY:
98.89

USDJPY:
159.12

VIX:
16.01

COMEX Gold:
4571.40

WTI:
87.83

BTC:
72719

## Regime

TREASURY_RELIEF_FAILURE
LONG_YIELDS_REBOUND
OIL_INFLATION
EQUITY_RISK_OFF_LITE
GOLD_BTC_ALTERNATIVE_ASSET_STRENGTH

## Treasury shock

Aug19:
Treasury buyback
-> yields down
-> dollar down
-> gold/BTC up

Aug20:
yields rebound
equities down
oil up

Interpretation:

Treasury intervention currently looks
more like temporary relief
than persistent regime change.

## Signals

A:
NONE

B:

GOLD BUY
4480-4530
SL 4350
TP1 4750

BTC BUY
69000-70500
SL 66000
TP1 76000

NO_TRADE:

ETH
WTI
USDJPY
SPX
NASDAQ
DXY
US10Y
VIX

## BTC regime change candidate

ETF flows:

Aug17 +297.6m
Aug18 +189.3m
Aug19 ~+517m

Price:

65k breakout
70k breakout
~72.7k

Previous:
positive flow / weak price

Current:
positive flow / positive price confirmation

MES:
66 -> 76

Do not chase.
Wait for 69k-70.5k retest.

## Research

Treasury buyback:
temporary vs persistent term-premium effect

BTC:
FLOW_TO_PRICE_LAG

GOLD:
alternative-asset relative strength

#TSO #GOLD #BTC #US10Y #WTI #NASDAQ
```

# 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-08-21,20260821_GOLD_BUY_PULLBACK,GOLD,BUY,B,PULLBACK,4480,4530,4350,4750,4900,1.58,0.63,0.43,96,78,31,0.25,GOLD_ALTERNATIVE_ASSET_STRENGTH_YIELD_REBOUND,78,81,80,83,82,78,4350_break_or_DXY_US10Y_acceleration,GOLD_entry_24h_3d_5d_MFE_MAE,verified
2026-08-21,20260821_BTC_BUY_PULLBACK,BTC,BUY,B,PULLBACK,69000,70500,66000,76000,80000,1.67,0.61,0.40,98,72,43,0.25,BTC_BREAKOUT_ETF_FLOW_CONFIRMED_OVEREXTENDED,76,82,77,80,81,76,66000_break_or_ETF_flow_reversal,BTC_68k_70k_76k_ETF_flow_3d_5d_MFE_MAE,verified
2026-08-21,20260821_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,82,40,85,,ETH_BREAKOUT_DATA_CONFLICT_OVEREXTENDED,59,65,75,43,57,55,stable_ETH_price_and_ETF_confirmation_required,ETH_ETHBTC_ETF_1d_3d_5d,partially_verified
2026-08-21,20260821_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,17,99,,HORMUZ_SUPPLY_SHOCK_5DAY_MOMENTUM,90,79,99,16,57,78,supply_shock_momentum_chase_prohibited,WTI_85_90_Hormuz_3d_5d,verified
2026-08-21,20260821_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,91,34,93,,USDJPY_YIELD_INTERVENTION_BOJ_CONFLICT,74,77,92,33,64,71,160_intervention_and_BOJ_yield_conflict,USDJPY_157_160_US10Y_DXY_3d,verified
2026-08-21,20260821_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,94,35,91,,TREASURY_RELIEF_FAILURE_EQUITY_PULLBACK,61,69,90,39,63,64,new_long_requires_ES_stabilization_US10Y_below_4.65,ES_7520_7650_US10Y_VIX_1d_3d,verified
2026-08-21,20260821_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,97,28,96,,GROWTH_LONG_YIELD_PRESSURE_RELIEF_FAILURE,56,65,94,31,59,61,NQ_stabilization_and_US10Y_decline_required,NQ_29000_US10Y_SOX_1d_3d,verified
2026-08-21,20260821_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,89,42,84,,DOLLAR_DEBASEMENT_YIELD_REBOUND_CONFLICT,72,77,86,44,66,72,clear_DXY_98_or_100_break_required,DXY_98_100_US10Y_3d,verified
2026-08-21,20260821_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,21,98,,TREASURY_BUYBACK_RELIEF_FAILURE_TERM_PREMIUM,85,89,98,20,74,85,confirmed_break_below_4.60_or_above_4.75_required,US10Y_4.60_4.75_3d_5d,verified
2026-08-21,20260821_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,90,39,87,,VOL_EXPANSION_EQUITY_PULLBACK,74,69,89,47,68,67,VIX_above_17_with_ES_NQ_break_confirms_risk_off,VIX_16_17_ES_NQ_1d_3d,verified
```

## JSON

```json
[
{"date":"2026-08-21","signal_id":"20260821_GOLD_BUY_PULLBACK","asset":"GOLD","side":"BUY","rank":"B","type":"PULLBACK","entry_low":4480,"entry_high":4530,"sl":4350,"tp1":4750,"tp2":4900,"rr":1.58,"win_prob":0.63,"expected_r":0.43,"tq_score":96,"opp_score":78,"no_trade_score":31,"risk_pct":0.25,"regime":"GOLD_ALTERNATIVE_ASSET_STRENGTH_YIELD_REBOUND","ems":78,"ffs":81,"cds":80,"ias":83,"cbs":82,"mes":78,"invalidation":"4350_break_or_DXY_US10Y_acceleration","verification_target":"GOLD_entry_24h_3d_5d_MFE_MAE","verified_status":"verified"},
{"date":"2026-08-21","signal_id":"20260821_BTC_BUY_PULLBACK","asset":"BTC","side":"BUY","rank":"B","type":"PULLBACK","entry_low":69000,"entry_high":70500,"sl":66000,"tp1":76000,"tp2":80000,"rr":1.67,"win_prob":0.61,"expected_r":0.40,"tq_score":98,"opp_score":72,"no_trade_score":43,"risk_pct":0.25,"regime":"BTC_BREAKOUT_ETF_FLOW_CONFIRMED_OVEREXTENDED","ems":76,"ffs":82,"cds":77,"ias":80,"cbs":81,"mes":76,"invalidation":"66000_break_or_ETF_flow_reversal","verification_target":"BTC_68k_70k_76k_ETF_flow_3d_5d_MFE_MAE","verified_status":"verified"},
{"date":"2026-08-21","signal_id":"20260821_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":82,"opp_score":40,"no_trade_score":85,"risk_pct":null,"regime":"ETH_BREAKOUT_DATA_CONFLICT_OVEREXTENDED","ems":59,"ffs":65,"cds":75,"ias":43,"cbs":57,"mes":55,"invalidation":"stable_ETH_price_and_ETF_confirmation_required","verification_target":"ETH_ETHBTC_ETF_1d_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-21","signal_id":"20260821_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":17,"no_trade_score":99,"risk_pct":null,"regime":"HORMUZ_SUPPLY_SHOCK_5DAY_MOMENTUM","ems":90,"ffs":79,"cds":99,"ias":16,"cbs":57,"mes":78,"invalidation":"supply_shock_momentum_chase_prohibited","verification_target":"WTI_85_90_Hormuz_3d_5d","verified_status":"verified"},
{"date":"2026-08-21","signal_id":"20260821_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":91,"opp_score":34,"no_trade_score":93,"risk_pct":null,"regime":"USDJPY_YIELD_INTERVENTION_BOJ_CONFLICT","ems":74,"ffs":77,"cds":92,"ias":33,"cbs":64,"mes":71,"invalidation":"160_intervention_and_BOJ_yield_conflict","verification_target":"USDJPY_157_160_US10Y_DXY_3d","verified_status":"verified"},
{"date":"2026-08-21","signal_id":"20260821_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":94,"opp_score":35,"no_trade_score":91,"risk_pct":null,"regime":"TREASURY_RELIEF_FAILURE_EQUITY_PULLBACK","ems":61,"ffs":69,"cds":90,"ias":39,"cbs":63,"mes":64,"invalidation":"new_long_requires_ES_stabilization_US10Y_below_4.65","verification_target":"ES_7520_7650_US10Y_VIX_1d_3d","verified_status":"verified"},
{"date":"2026-08-21","signal_id":"20260821_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":97,"opp_score":28,"no_trade_score":96,"risk_pct":null,"regime":"GROWTH_LONG_YIELD_PRESSURE_RELIEF_FAILURE","ems":56,"ffs":65,"cds":94,"ias":31,"cbs":59,"mes":61,"invalidation":"NQ_stabilization_and_US10Y_decline_required","verification_target":"NQ_29000_US10Y_SOX_1d_3d","verified_status":"verified"},
{"date":"2026-08-21","signal_id":"20260821_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":89,"opp_score":42,"no_trade_score":84,"risk_pct":null,"regime":"DOLLAR_DEBASEMENT_YIELD_REBOUND_CONFLICT","ems":72,"ffs":77,"cds":86,"ias":44,"cbs":66,"mes":72,"invalidation":"clear_DXY_98_or_100_break_required","verification_target":"DXY_98_100_US10Y_3d","verified_status":"verified"},
{"date":"2026-08-21","signal_id":"20260821_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":21,"no_trade_score":98,"risk_pct":null,"regime":"TREASURY_BUYBACK_RELIEF_FAILURE_TERM_PREMIUM","ems":85,"ffs":89,"cds":98,"ias":20,"cbs":74,"mes":85,"invalidation":"confirmed_break_below_4.60_or_above_4.75_required","verification_target":"US10Y_4.60_4.75_3d_5d","verified_status":"verified"},
{"date":"2026-08-21","signal_id":"20260821_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":90,"opp_score":39,"no_trade_score":87,"risk_pct":null,"regime":"VOL_EXPANSION_EQUITY_PULLBACK","ems":74,"ffs":69,"cds":89,"ias":47,"cbs":68,"mes":67,"invalidation":"VIX_above_17_with_ES_NQ_break_confirms_risk_off","verification_target":"VIX_16_17_ES_NQ_1d_3d","verified_status":"verified"}
]
```

**本日の核心は「Treasury買い戻しだけでは長期金利問題を解決できなかった」ことです。** 8月20日に10年債利回りは約4.69%へ戻り、株式も明確に下落しました。citeturn291777news30turn376196news37

一方でBTCは判定を変えます。**ETF資金流入と価格上昇がようやく同方向へ揃ったため、MES<50による機械的NO_TRADE局面は終了**。ただし72k台を追うのではなく、**69k～70.5kへのリテスト限定のB級**です。GOLDも同様に4480～4530への押し目限定です。

navlist8月20日の主要市場材料turn291777news31,turn436355view2,turn436355view1,turn980659news17
