<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-08-25 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 15724 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026年8月25日

データ基準は**8月24日米国市場終了後～8月25日06:58 JST前後**。10資産すべて新規取得を試みました。ES/NQは9月限先物、GOLDはCOMEX、WTIはWTI先物、BTC/ETHは現物を基準にしています。

8月24日はCOMEX金先物が**4692.49付近**まで続伸。WTIは**85.01ドル、-2.4%**。米10年債利回りは**4.709%**へ約2.8bp低下しました。一方、S&P500は-0.28～0.3%、NASDAQは約-0.76～0.8%。NQ9月限は**29168、-0.75%**、ES9月限は**7669.25、-0.43%**でした。citeturn575648search10turn345213news36turn575648news40turn293304news65turn575648search4turn345213search2

BTCは24日に約**78993ドル**まで上昇し、ETHも約**2500ドル**。先週の米スポットETFはBTC約19.2億ドル、ETH約6.97億ドルの純流入でした。citeturn575648news37turn963082search0turn293304news11

実取引の許容損失は、現在の運用上の**約3000円/回**を優先します。memcite

## 1. 本日の結論

**A級：0件**

**B+：0件**

**B級：GOLD BUY、BTC BUY、ETH BUY**

**NO_TRADE：WTI、USDJPY、SPX、NASDAQ、DXY、US10Y、VIX**

優先順位は、

**GOLD B > BTC B > ETH B**

です。

昨日までのHard Asset Rotationはまだ生きています。重要なのは、**米10年債利回りが4.709%へ低下したのにNASDAQが下落した**ことです。普通ならGrowth株には追い風となる金利低下をNQが利用できていません。citeturn575648news40turn575648search4

したがってNASDAQの再BUYはまだ見送ります。

一方GOLDは高値更新、BTC/ETHもETFフローと価格が同方向。3資産はBUY方向を維持しますが、すべて**押し目限定**です。

---

## 2. 前回判断の簡易検証

### GOLD B BUY → **方向成功 / NO_FILL**

前回：

**Entry 4580–4640  
SL 4460  
TP1 4940**

8月24日のCOMEX系データは、

**Open 4681.44  
High 4712.89  
Low 4652.40  
Close 4692.49**

でした。citeturn575648search10

安値4652.40なのでEntry上限4640へ**約12ドル届いていません**。

したがって、

**DIRECTION_SUCCESS  
NO_FILL**

です。

GOLDではこれで再び「方向成功だが押し目不足」のサンプルが増えました。

---

### BTC B BUY → **方向成功 / NO_FILL**

前回：

**Entry 74200–76000**

24日のBTCは朝77k台から上昇し、Reutersでは**78993.42ドル**、Yahoo系取得では朝の時点で79106ドルでした。citeturn575648news37turn963082search6

少なくとも確認できた24日の価格帯では76000以下への押しは確認できません。

**DIRECTION_SUCCESS / NO_FILL**

です。

ETF流入後の上昇継続という仮説自体は機能しています。

---

### ETH B BUY → **方向成功 / NO_FILL**

前回：

**Entry 2280–2380**

8月24日のETHは、

**Open 2463.25  
Low 2424.86  
High 2518.35  
Close付近 2498.71**

でした。citeturn963082search0

Entryには未到達。

**DIRECTION_SUCCESS / NO_FILL**

です。

---

### WTI NO_TRADE → **成功**

WTIは6連騰後、24日に**85.01ドルへ-2.4%**。Brentも92.17へ下落しました。米国の新たな対イラン制裁発表後も原油がさらに上へ走らず、利益確定が入りました。citeturn345213news36turn345213news39

高値87ドル台で供給ショックを追わなかった判断は引き続き妥当です。

---

## 3. 市場全体の前提

本日のRegimeは、

**`HARD_ASSET_STRENGTH / LOWER_YIELDS_TECH_NONCONFIRMATION / OIL_PULLBACK / NVIDIA_EVENT_RISK / CRYPTO_FLOW_CONFIRMATION`**

とします。

24日のクロスアセット構造は重要です。

**US10Y 4.709%へ低下  
WTI 85.01へ低下**

なら、本来NASDAQにはかなり好都合です。

しかし実際には、

**S&P500 -0.3%  
NASDAQ -0.8%  
NQ -0.75%**

でした。citeturn575648news40turn345213news36turn293304news65turn575648search4

つまり現在のNASDAQは、

**金利問題だけではなくAI株そのものの期待値・バリュエーション問題**

へ移っています。

Nvidiaは8月26日に決算を控えており、24日には株価が約2.9%下落しました。citeturn575648news39

対照的に金は4営業日続伸しCOMEXで4640.80～4692付近。米財政・ドル価値への懸念が継続的な買い材料になっています。citeturn575648news36turn575648search10

---

## 4. 10資産別判断

| 資産 | 判定 | 核心 |
|---|---|---|
| GOLD | **B BUY** | 相対強度最良。ただし連騰後 |
| BTC | **B BUY** | 79k近辺＋ETFフロー強い。過熱 |
| ETH | **B BUY** | 2500近辺＋ETFフロー強い。過熱 |
| WTI | **NO_TRADE** | 供給ショック後の初反落 |
| USDJPY | **NO_TRADE** | 金利低下・DXY反発・BOJ/介入が競合 |
| SPX | **NO_TRADE** | 金利低下でも株価反応弱い |
| NASDAQ | **NO_TRADE** | NQ -0.75%、Nvidia決算前 |
| DXY | **NO_TRADE** | 98.99へ小反発。方向性不足 |
| US10Y | **NO_TRADE** | 4.709へ低下したが追わない |
| VIX | **NO_TRADE** | 約16近辺、イベント前の確認指標 |

DXYは24日に**98.99、+0.17%**。長期金利低下にもかかわらずドルが反発しており、単純なDXY SELLにはなりません。citeturn575648news37

VIXは24日寄り前に15.91まで上昇。Nvidia・Iran・Jackson Holeなどイベントリスクを価格に入れ始めています。citeturn345213news37

---

## 5. A級候補

**0件です。**

GOLDが最も近く、

**CBS 88  
EMS 85  
win_prob 0.65  
expected_r 0.44  
MAE 0.27R**

と評価します。

CBS/EMS/RRは十分。

しかし、

**expected_r 0.44 < 0.45  
MAE 0.27R > 0.25R**

なのでAにはしません。

BTCもCBS/EMS/MESは非常に高いですが、過去1週間で約24%上昇しており、直近の下方ボラティリティを過小評価できません。citeturn963082search2

---

## 6. B級監視候補

### 1位 GOLD — BUY PULLBACK

**Entry 4620–4660  
SL 4490  
TP1 4930  
TP2 5100  
RR 1.80  
win_prob 0.65  
較正参考 0.68  
expected_r 0.44  
MAE 0.27R  
risk 0.25%**

現在のCOMEX水準は4690前後。citeturn575648search10

前日の安値4652.40だったことから、昨日よりEntryをわずかに浅くします。

これは成行追随ではなく、**GOLDで繰り返されているShallow Pullback仮説を教師データ化するための較正**です。

4660より上なら追いません。

---

### 2位 BTC — BUY PULLBACK

**Entry 76500–78000  
SL 72500  
TP1 83500  
TP2 88000  
RR 1.48  
win_prob 0.63  
較正参考 0.66  
expected_r 0.42  
MAE 0.30R  
risk 0.25%**

24日は約79k。citeturn575648news37turn963082search10

先週ETFは約**19.2億ドル流入**、5営業日連続流入でした。citeturn572261search0turn572261news24

需給は強い。

ただしRRが1.5をわずかに下回るためB+にはしません。

またXM最小ロット＋SL72500で想定損失が**約3000円超ならExecution NO_TRADE**です。

---

### 3位 ETH — BUY PULLBACK

**Entry 2400–2470  
SL 2180  
TP1 2820  
TP2 3000  
RR 1.55  
win_prob 0.60  
較正参考 0.63  
expected_r 0.39  
MAE 0.33R  
risk 0.25%**

24日安値2424.86なので、このEntry帯は実際に市場が使った支持帯に近い水準です。citeturn963082search0

ETH ETFは先週**+697.2M**。BlackRock ETHAだけでも21日に+145.2Mでした。citeturn293304news11turn572261search1

ただしETHは週間約30%上昇。

3候補中もっともMAEを大きく見ます。

---

## 7. 触らない資産

最優先は**NASDAQ**です。

米10年金利とWTIが両方下がったのにNQは29168まで-0.75%。citeturn575648search4turn575648news40turn345213news36

これは重要なnegative confirmationです。

しかもNvidia決算直前。

ここでBUYすると、

**金利改善を買う取引**

ではなく、

**Nvidia決算に賭ける取引**

になってしまいます。

SELLも、決算前のテック下落を追うことになるので行いません。

WTIも引き続き触りません。24日の2.4%下落だけで供給ショックregime終了とは判断できず、Iranの反応次第で再び大幅ギャップが可能です。citeturn345213news36

---

## 8. 後日検証ポイント

今日の研究対象は3つです。

第一は**GOLD Entryモデル**。

8月24日は、

**Entry上限4640  
実際の安値4652.40  
→ 約12ドル差でNO_FILL  
→ その後4692**

でした。citeturn575648search10

この種の「方向成功・僅差NO_FILL」が増えているため、

**Deep Pullback  
Shallow Pullback  
Breakout Retest**

の仮想成績を明確に分けます。

第二は**NASDAQの金利感応度低下**。

US10Y低下＋Oil低下でもNQが下落したため、今後Nvidia決算後に、

**NQ反発  
SOX反発  
US10Y<4.70**

が揃うまでBUY再開を遅らせます。

第三は**Crypto FLOW_TO_PRICEの持続性**。

先週ETF流入はBTC1.9B、ETH697M。24日もBTC約79k、ETH約2.5kを維持しました。citeturn293304news11turn963082search0

5営業日後に、

**BTC 75k維持  
ETH 2.3k維持  
ETFフロー継続**

なら一時的ショートスクイーズではなく、より持続的な需給regime changeとして格上げします。

---

## 9. Obsidian保存用Observation Draft

```markdown
# 2026-08-25 Lower Yields but Tech Fails to Confirm

## Market anchors

ES Sep:
7669.25
-0.43%

NQ Sep:
29168
-0.75%

COMEX Gold:
~4692

WTI:
85.01
-2.4%

US10Y:
4.709%

DXY:
98.99

BTC:
~79k

ETH:
~2500

VIX:
~16 area

## Regime

HARD_ASSET_STRENGTH
LOWER_YIELDS_TECH_NONCONFIRMATION
OIL_PULLBACK
NVIDIA_EVENT_RISK
CRYPTO_FLOW_CONFIRMATION

## Key observation

Normally:

US10Y down
+
oil down

should help growth equities.

But:

NQ -0.75%

Therefore Nasdaq weakness
is no longer explained only by rates.

AI expectations / valuation / Nvidia event risk
are now dominant.

## Previous signals

GOLD B:
DIRECTION_SUCCESS
NO_FILL

Entry upper:
4640

Monday low:
4652.4

Difference:
~12.4

BTC B:
DIRECTION_SUCCESS
NO_FILL

ETH B:
DIRECTION_SUCCESS
NO_FILL

WTI NO_TRADE:
SUCCESSFUL_AVOIDANCE

## Signals

A:
NONE

B:

GOLD BUY
4620-4660
SL 4490
TP1 4930

BTC BUY
76500-78000
SL 72500
TP1 83500

ETH BUY
2400-2470
SL 2180
TP1 2820

NO_TRADE:

WTI
USDJPY
SPX
NASDAQ
DXY
US10Y
VIX

## Research

GOLD:
deep vs shallow pullback

NASDAQ:
rate sensitivity breakdown

Crypto:
ETF FLOW_TO_PRICE persistence

## Execution

No chase.

GOLD >4660:
NO_FILL

BTC >78000:
NO_FILL

ETH >2470:
NO_FILL

XM minimum-lot expected loss:
operational limit ~3000 JPY

#TSO #GOLD #BTC #ETH #NASDAQ #US10Y
```

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-08-25,20260825_GOLD_BUY_PULLBACK,GOLD,BUY,B,PULLBACK,4620,4660,4490,4930,5100,1.80,0.65,0.44,98,80,30,0.25,HARD_ASSET_STRENGTH_SHALLOW_PULLBACK,85,87,79,91,88,85,4490_break_or_DXY_US10Y_reacceleration,GOLD_entry_24h_3d_5d_MFE_MAE_shallow_vs_deep,verified
2026-08-25,20260825_BTC_BUY_PULLBACK,BTC,BUY,B,PULLBACK,76500,78000,72500,83500,88000,1.48,0.63,0.42,99,73,44,0.25,BTC_ETF_FLOW_CONFIRMATION_OVEREXTENDED,84,93,80,88,87,89,72500_break_or_ETF_flow_reversal,BTC_75k_80k_83.5k_ETF_3d_5d_MFE_MAE,partially_verified
2026-08-25,20260825_ETH_BUY_PULLBACK,ETH,BUY,B,PULLBACK,2400,2470,2180,2820,3000,1.55,0.60,0.39,97,69,50,0.25,ETH_ETF_FLOW_CONFIRMATION_OVEREXTENDED,77,88,79,80,81,82,2180_break_or_ETH_ETF_flow_reversal,ETH_2.3k_2.5k_2.8k_ETF_ETHBTC_3d_5d,verified
2026-08-25,20260825_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,25,96,,SUPPLY_SHOCK_FIRST_PULLBACK,84,76,97,25,58,76,one_day_oil_pullback_does_not_end_geopolitical_regime,WTI_82_87_Hormuz_Iran_response_3d_5d,verified
2026-08-25,20260825_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,89,39,88,,USDJPY_RATE_DOLLAR_BOJ_CONFLICT,72,76,88,40,65,70,clear_157_or_160_break_with_policy_confirmation_required,USDJPY_157_160_DXY_US10Y_3d,partially_verified
2026-08-25,20260825_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,86,46,77,,LOWER_YIELD_EQUITY_NONCONFIRMATION,66,72,80,52,68,67,ES_requires_multi_day_stabilization_and_breadth_confirmation,ES_7600_7700_US10Y_VIX_Nvidia_1d_3d,verified
2026-08-25,20260825_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,97,29,95,,LOWER_YIELD_TECH_NONCONFIRMATION_NVIDIA_RISK,58,68,94,32,60,62,NQ_requires_Nvidia_SOX_and_yield_confirmation,NQ_28900_29500_Nvidia_SOX_US10Y_1d_3d,verified
2026-08-25,20260825_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,84,43,82,,DOLLAR_REBOUND_FISCAL_CONFLICT,71,76,84,45,66,71,clear_break_below_98_or_reclaim_100_required,DXY_98_100_US10Y_JacksonHole_3d,verified
2026-08-25,20260825_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,94,31,92,,YIELD_PULLBACK_FISCAL_TERM_PREMIUM,80,86,93,31,72,82,confirmed_break_below_4.60_or_rebound_above_4.75_required,US10Y_4.60_4.75_Nvidia_JacksonHole_3d,verified
2026-08-25,20260825_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,83,38,84,,EVENT_VOL_NVIDIA_JACKSON_HOLE,70,66,84,47,66,65,VIX_above_18_with_NQ_break_or_below_14_with_equity_recovery,VIX_14_18_ES_NQ_Nvidia_3d,partially_verified
```

### JSON

```json
[
{"date":"2026-08-25","signal_id":"20260825_GOLD_BUY_PULLBACK","asset":"GOLD","side":"BUY","rank":"B","type":"PULLBACK","entry_low":4620,"entry_high":4660,"sl":4490,"tp1":4930,"tp2":5100,"rr":1.80,"win_prob":0.65,"expected_r":0.44,"tq_score":98,"opp_score":80,"no_trade_score":30,"risk_pct":0.25,"regime":"HARD_ASSET_STRENGTH_SHALLOW_PULLBACK","ems":85,"ffs":87,"cds":79,"ias":91,"cbs":88,"mes":85,"invalidation":"4490_break_or_DXY_US10Y_reacceleration","verification_target":"GOLD_entry_24h_3d_5d_MFE_MAE_shallow_vs_deep","verified_status":"verified"},
{"date":"2026-08-25","signal_id":"20260825_BTC_BUY_PULLBACK","asset":"BTC","side":"BUY","rank":"B","type":"PULLBACK","entry_low":76500,"entry_high":78000,"sl":72500,"tp1":83500,"tp2":88000,"rr":1.48,"win_prob":0.63,"expected_r":0.42,"tq_score":99,"opp_score":73,"no_trade_score":44,"risk_pct":0.25,"regime":"BTC_ETF_FLOW_CONFIRMATION_OVEREXTENDED","ems":84,"ffs":93,"cds":80,"ias":88,"cbs":87,"mes":89,"invalidation":"72500_break_or_ETF_flow_reversal","verification_target":"BTC_75k_80k_83.5k_ETF_3d_5d_MFE_MAE","verified_status":"partially_verified"},
{"date":"2026-08-25","signal_id":"20260825_ETH_BUY_PULLBACK","asset":"ETH","side":"BUY","rank":"B","type":"PULLBACK","entry_low":2400,"entry_high":2470,"sl":2180,"tp1":2820,"tp2":3000,"rr":1.55,"win_prob":0.60,"expected_r":0.39,"tq_score":97,"opp_score":69,"no_trade_score":50,"risk_pct":0.25,"regime":"ETH_ETF_FLOW_CONFIRMATION_OVEREXTENDED","ems":77,"ffs":88,"cds":79,"ias":80,"cbs":81,"mes":82,"invalidation":"2180_break_or_ETH_ETF_flow_reversal","verification_target":"ETH_2.3k_2.5k_2.8k_ETF_ETHBTC_3d_5d","verified_status":"verified"},
{"date":"2026-08-25","signal_id":"20260825_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":25,"no_trade_score":96,"risk_pct":null,"regime":"SUPPLY_SHOCK_FIRST_PULLBACK","ems":84,"ffs":76,"cds":97,"ias":25,"cbs":58,"mes":76,"invalidation":"one_day_oil_pullback_does_not_end_geopolitical_regime","verification_target":"WTI_82_87_Hormuz_Iran_response_3d_5d","verified_status":"verified"},
{"date":"2026-08-25","signal_id":"20260825_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":89,"opp_score":39,"no_trade_score":88,"risk_pct":null,"regime":"USDJPY_RATE_DOLLAR_BOJ_CONFLICT","ems":72,"ffs":76,"cds":88,"ias":40,"cbs":65,"mes":70,"invalidation":"clear_157_or_160_break_with_policy_confirmation_required","verification_target":"USDJPY_157_160_DXY_US10Y_3d","verified_status":"partially_verified"},
{"date":"2026-08-25","signal_id":"20260825_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":86,"opp_score":46,"no_trade_score":77,"risk_pct":null,"regime":"LOWER_YIELD_EQUITY_NONCONFIRMATION","ems":66,"ffs":72,"cds":80,"ias":52,"cbs":68,"mes":67,"invalidation":"ES_requires_multi_day_stabilization_and_breadth_confirmation","verification_target":"ES_7600_7700_US10Y_VIX_Nvidia_1d_3d","verified_status":"verified"},
{"date":"2026-08-25","signal_id":"20260825_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":97,"opp_score":29,"no_trade_score":95,"risk_pct":null,"regime":"LOWER_YIELD_TECH_NONCONFIRMATION_NVIDIA_RISK","ems":58,"ffs":68,"cds":94,"ias":32,"cbs":60,"mes":62,"invalidation":"NQ_requires_Nvidia_SOX_and_yield_confirmation","verification_target":"NQ_28900_29500_Nvidia_SOX_US10Y_1d_3d","verified_status":"verified"},
{"date":"2026-08-25","signal_id":"20260825_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":84,"opp_score":43,"no_trade_score":82,"risk_pct":null,"regime":"DOLLAR_REBOUND_FISCAL_CONFLICT","ems":71,"ffs":76,"cds":84,"ias":45,"cbs":66,"mes":71,"invalidation":"clear_break_below_98_or_reclaim_100_required","verification_target":"DXY_98_100_US10Y_JacksonHole_3d","verified_status":"verified"},
{"date":"2026-08-25","signal_id":"20260825_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":94,"opp_score":31,"no_trade_score":92,"risk_pct":null,"regime":"YIELD_PULLBACK_FISCAL_TERM_PREMIUM","ems":80,"ffs":86,"cds":93,"ias":31,"cbs":72,"mes":82,"invalidation":"confirmed_break_below_4.60_or_rebound_above_4.75_required","verification_target":"US10Y_4.60_4.75_Nvidia_JacksonHole_3d","verified_status":"verified"},
{"date":"2026-08-25","signal_id":"20260825_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":83,"opp_score":38,"no_trade_score":84,"risk_pct":null,"regime":"EVENT_VOL_NVIDIA_JACKSON_HOLE","ems":70,"ffs":66,"cds":84,"ias":47,"cbs":66,"mes":65,"invalidation":"VIX_above_18_with_NQ_break_or_below_14_with_equity_recovery","verification_target":"VIX_14_18_ES_NQ_Nvidia_3d","verified_status":"partially_verified"}
]
```

**8月25日の実務上の第一候補は引き続きGOLDです。** 昨日はEntryにわずか12ドル届かず上昇したため、本日は4620–4660へ浅く較正します。ただし現在値4690台からは追いません。citeturn575648search10

BTC/ETHも需給は良好ですが、上昇率が大きいためA級にはしません。対照的にNASDAQは、**金利低下と原油下落という本来の追い風を受けても下落した**ことを重視し、Nvidia決算を通過するまで新規BUYを停止します。citeturn575648news40turn345213news36turn575648search4
