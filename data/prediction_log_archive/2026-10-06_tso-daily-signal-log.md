<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-10-06 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-10-13T20:23:35Z / chars: 19123 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-10-06

**使用モデル：GPT-5.6 Sol**  
**本日の市場の主役：US10Y**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**データ基準：2026年10月5日米国市場終了後〜10月6日06:55 JST前後。ES/NQはCME同限月の遅延データ提供元を併用。**

**crypto_grounds: etf=有, cme=有** — Farsideの最新完全確定日は10月2日で、BTC現物ETFは**+189.9Mドル**、ETH現物ETFは**-37.4Mドル**。10月5日欄は全銘柄未入力のため「0」とは扱いません。CME Bitcoinは10月5日に概ね**85.2k–87.4k**、Ether先物は概ね**2,687–2,748**を確認しました。citeturn846435view0turn846435view1turn354819search1turn672715search1

**expected_r_basis: subjective** — 新規WTI SELL_PULLBACKの二点分布EVは約`+0.66R`ですが、Entry未到達、5営業日時間決済、地政学ヘッドラインによる早期invalidationを織り込み、TSO_LOGでは`expected_r=0.34`とします。

**invalidation_check: 20261006_WTI_SELL_PULLBACK=not_fired**

---

## 1. 本日の結論

**新規A級：0件**

**新規B級：1件 — WTI SELL_PULLBACK**

**条件付きB+観察候補：WTI SELL_PULLBACK**  
XMで**OILCash 0.01 lot**を使う場合は最小ロット損失条件を満たします。XMのOILCashは1 lot=100 barrels、最小0.01 lotなので実質1 barrelです。今回のSL距離約1.50ドルなら価格差損失は約1.5ドル＋spreadで、3,000円制約を大きく下回ります。一方、XMの通常のWTI先物CFD `OIL` は最小1 lot=100 barrelsなので、同じSLでは許容額を超える可能性が高く、その場合は**実取引NO_TRADE**です。citeturn758158search1turn758158search8

**その他9資産：NO_TRADE**

10月5日の最大の情報は、ISM Servicesが**54.9**と拡大を維持しながら、Prices Paidが**74.0**まで上昇したことです。これは2022年7月以来の高水準で、弱い雇用統計とは反対にインフレ圧力を示しました。米10年債利回りは最終的に約**5.31%**、途中では約5.35%まで上昇しています。citeturn748118view0turn361717view0

それでもS&P500は**+0.66%**、Nasdaqは**+1.05%**で史上最高値を更新しました。つまり、

**US10Y↑ + DXY↑ + NASDAQ↑**

という異例の組み合わせです。citeturn156737view1turn701739view0

一方WTIは**89.43ドル、-1.84%**まで下落。中東原油輸出回復とG7備蓄放出が価格を押し下げています。citeturn970986news0

ただし89.43からSELLは追いません。

新規シグナル：

**`20261006_WTI_SELL_PULLBACK`**

Entry：**90.20–90.80**  
Mid：**90.50**  
SL：**92.00**  
TP1：**87.20**  
TP2：**84.80**

RR：

\[
(90.50-87.20)/(92.00-90.50)
=3.30/1.50
=2.20
\]

**win_prob：0.52**  
**較正後参考：0.53**  
**expected_r：0.34**  
**MAE想定：0.30R**  
**risk_pct：0.25%**

A級ではありません。`MAE>0.25R`かつsubjective `expected_r<0.45`です。

---

## 2. 前回判断の簡易検証

10月5日は10資産すべてNO_TRADEでした。

### NASDAQ

昨日の条件は、

**NQ 31300超 → trend continuation確認**
ただし
**US10Y <=5.20がない限り追わない**

でした。

実際、NQZ26はデータベンダー間で最終値に多少差がありますが、概ね**31,300前後**まで上昇しました。一方US10Yは5.31%へ上昇しています。現物Nasdaqも+1.05%で最高値更新です。citeturn941950search6turn941950search8turn156737view1

したがって、

**trend判定＝正しい**  
**Entry判定＝NO_TRADE継続**

です。

高値を追わなかったことで上昇分は取り逃しましたが、これはTSOの「方向予測」と「Entry品質」を分離するルールに沿っています。

### BTC

昨日のBUY再評価条件は、

**BTC >87400**
＋
**CME >87000**
＋
**ETF再加速**

でした。

CME Bitcoinの10月5日高値は**87397.5**。

ほぼ設定した87400に一致しましたが、その後は86k前後へ戻りました。citeturn354819search0

つまり、

**一瞬の閾値接触≠breakout維持**

でした。

さらにFarsideの最新確定値では10月2日のBTC ETFは**+189.9Mドル**へ改善していますが、10月5日は未確定です。citeturn846435view0

したがって新規BUYを見送った判断を維持します。

### WTI

昨日設定した観察条件、

**90割れ → 下方向再評価**

が成立しました。

WTIは**89.43**で清算。中東からの原油輸出回復とG7の備蓄供給が売り材料になりました。citeturn970986news0turn361717view0

そのため今日は「成行SELL」ではなく、**戻り売りだけをB級化**します。

---

## 3. 市場全体の前提

総合regimeは**MIXED**です。

米国サービス業はまだ強いです。9月ISM Servicesは54.9、新規受注59.8、雇用指数50.1。一方、Prices Paidは74.0まで上がり、燃料、銅、鉄鋼、石油製品などのコスト上昇が広がっています。citeturn748118view0

これは現在の長期金利上昇を説明する材料になります。

**弱い雇用**
と
**強いサービス需要＋インフレ圧力**

が同時に存在しています。

米10年債は約**5.31%**。DXYは**102.19**、日中高値102.53。USDJPYは約**158.04**です。citeturn361717view0turn701739view0

株式はそれを無視するように上昇しています。

S&P500現物：**7773.95、+0.66%**  
Nasdaq Composite：**27477.31、+1.05%**

Nvidia、Microsoft、Metaなど大型AI/Growthが主導しました。citeturn156737view1

ESZ26は遅延系列で概ね**7,830前後**、NQZ26は**31,300前後**まで上昇しています。データ提供元間でセッション切替時刻による差があるため両方`partially_verified`扱いです。citeturn941950search7turn941950search8

VIXはCboe公式で**15.52**。まだrisk-on圏ですが、前日の15.31からはわずかに上昇しました。citeturn558554view0

GoldはGCZ26が**4156.8ドル**で清算。Fedの10月利上げ確率低下は支援材料ですが、DXYと長期金利上昇に押されています。citeturn156737view2

WTIは89.43。

ただし「供給正常化＝原油価格が簡単に下がる」という状況でもありません。Hormuz通過量は戦争前の約80%まで戻っていますが、タンカー運賃、保険、精製能力不足、diesel不足が価格を支えています。Reuters分析では中東→アジアのVLCC運賃が1月約3万ドル/日から最近**120万ドル/日超**まで上昇しています。citeturn156737view3

これがWTI SELLをA級にできない最大の理由です。

---

## 4. 10資産別判断

| 資産 | 本日判断 | 評価 |
|---|---|---|
| **GOLD** | **NO_TRADE** | GCZ26 4156.8。金利・ドルは弱気だが4150付近を成行SELLするRRは悪い。 |
| **BTC** | **NO_TRADE** | 現物約85.7–85.8k、CME約86k。87.4k突破維持失敗。 |
| **ETH** | **NO_TRADE** | 現物約2712、CME約2720。ETFは最新確定日-37.4M。 |
| **WTI** | **B SELL_PULLBACK** | 89.43。90.20–90.80への戻りのみSELL。 |
| **USDJPY** | **NO_TRADE** | 約158.04。金利差BUY方向だが159–160へ近づくほど介入テール増大。 |
| **SPX** | **NO_TRADE** | ESZ26約7830。高値追随禁止。 |
| **NASDAQ** | **NO_TRADE** | NQZ26約31300。最強資産だがUS10Y 5.31%で新規BUYの非対称性不足。 |
| **DXY** | **NO_TRADE** | 102.19。日中102.53まで上昇。高値追い禁止。 |
| **US10Y** | **NO_TRADE** | 約5.31%。5.35近辺の極端値を追わない。 |
| **VIX** | **NO_TRADE** | 15.52。株高継続だが低ボラ追随にedgeなし。 |

BTC現物は約**85.8k**、ETHは約**2712**。CME Bitcoinは10月5日に高値87397.5、Ether先物は高値2748.25でした。citeturn764226search1turn764226search2turn354819search0turn672715search1

---

## 5. A級候補

**なし。**

NASDAQは方向性だけなら非常に強いです。

しかし、

**NQ >31300**
＋
**US10Y ≈5.31**
＋
**DXY >102**
＋
**2営業日連続の強い上昇**

なのでEntryを作りません。

以前の「US10Y <=5.20」を外して無理にA級へ昇格させる理由はありません。

逆に、ここからUS10Yが5.2以下へ下がってもNQが31,000前後を維持するなら、かなり強いBUY候補になります。

---

## 6. B級監視候補

### `20261006_WTI_SELL_PULLBACK` — B

**Entry：90.20–90.80**  
**Mid：90.50**  
**SL：92.00**  
**TP1：87.20**  
**TP2：84.80**  
**RR：2.20**  
**win_prob：0.52**  
**較正後参考：0.53**  
**two-point EV：約+0.66R**  
**subjective expected_r：+0.34R**  
**MAE想定：0.30R**  
**risk_pct：0.25%**

背景：

中東原油輸出は回復し、G7も供給増に動いています。WTIは89.43まで下落しました。citeturn970986news0turn156737view4

一方で、

- Hormuz物流は完全正常化していない
- タンカー運賃が極端に高い
- diesel/精製能力不足
- Iran関連の突発headline

が残ります。citeturn156737view3

したがって89ドル台の成行SELLはしません。

**90.20–90.80へ戻して失速した場合だけ参加**です。

`92.00`超、または新たな大規模供給障害が確認された場合はシナリオ失効。

なおOILCash使用ならB+のロット条件まで満たしますが、XMの通常OIL先物CFDなら最小ロット制約を超える可能性があるため、**銘柄がOILCashである場合のみB+実取引候補**とします。citeturn758158search1turn758158search8

---

## 7. 触らない資産

特に**US10Y、NASDAQ、USDJPY**です。

US10Yは5.35%付近まで来ており、ここから利回り上昇を追うと国債入札やFOMC議事要旨で逆方向へ巻き戻されるリスクがあります。

NASDAQは逆に非常に強いですが、**金利が上がっても上がるから買う**という判断は危険です。現在はAI大型株が金利逆風を吸収している局面で、指数内部の集中度が高い可能性があります。

USDJPYは158.04。

通常の金利差モデルではBUY方向ですが、159–160へ近づくと通常の連続分布とは別の**介入ジャンプリスク**を考える必要があります。

現在研究中のIntervention Shock Moduleの考え方では、

**158→159方向を追う通常BUY**
と
**介入級急落だけを狙うtail-limit**

は完全に別戦略として管理します。

---

## 8. 後日検証ポイント

### WTI

新規未決着：

**`20261006_WTI_SELL_PULLBACK`**

観察：

**90.20–90.80 → ENTRY**  
**92.00 → fired**  
**87.20 → TP1**  
**84.80 → TP2**

89.43からそのまま87方向へ下落した場合は**未約定のまま見送り**です。

取り逃がしても追いません。

### BTC

10月5日のCME高値**87397.5**は、事前設定していた87400にほぼ完全一致しました。citeturn354819search0

しかし維持できませんでした。

したがって次は、

**87500超で日中維持**
＋
**CMEも87500超**
＋
**ETF純流入継続**

まで要求します。

Farsideの最新完全値は10月2日**+189.9Mドル**なので、10月5日の確定値を次回比較します。citeturn846435view0

### ETH

CMEは約2720。

**2750–2800回復**
＋
**ETF流入転換**

まではBTCより低評価を維持します。

最新完全ETFは10月2日**-37.4Mドル**です。citeturn846435view1

### NASDAQ

NQ：

**約31300**

次のBUY候補は、

**31000–31100への押し**
＋
**US10Y <5.20**
＋
**VIX <=15.5**

です。

以前の30750–30900より指数水準自体が切り上がったため、支持帯を上方更新します。

**NQ<30900**
なら今回のbreakoutを再検討します。

### SPX

ES：

**約7830**

**7800–7810**を押し目支持にできるか確認。

NQだけ強くESが7800を割る場合は、依然としてAI集中相場と評価します。

### GOLD

GCZ26：

**4156.8**

次のSELL候補：

**4190–4210**
＋
**US10Y >5.25**
＋
**DXY >102**

です。

逆に、

**4230超**
＋
**US10Y <5.15**

ならBUY側へ反転評価します。

### USDJPY

現在約158.04。citeturn701739view0

**159接近**
＋
**1時間足で円安加速**
＋
**財務省警告強化**

なら通常BUY評価を落とします。

**160近辺では通常momentum BUYを原則停止**し、介入shock研究側へ切り替える方針を維持します。

### US10Y

**5.35**が直近最大分岐。

ISM Prices 74.0という材料が加わったため、

**5.35超定着**
なら「term premiumだけ」ではなく**実際のインフレ再加速懸念**も含むregimeへ変更。

**5.20割れ**
ならNASDAQ/GOLDのEntry条件が大きく改善します。

---

## 9. Obsidian保存用 Observation Draft

```markdown
# 2026-10-06 ISM Price Shock / Nasdaq Resilience / WTI Breakdown

Model:
GPT-5.6 Sol

Market protagonist:
US10Y

Gold reference:
COMEX Dec-2026 / GCZ26

crypto_grounds:
etf=有
cme=有

expected_r_basis:
subjective

## Regime

MIXED

## US macro

ISM Services:
54.9

Prior:
55.4

Prices Paid:
74.0

Prior:
72.6

Highest since:
Jul 2022

Employment:
50.1

Interpretation:

Weak payroll data
did not translate into broad disinflation.

Services demand remains strong
and input-price pressure is increasing.

## Rates / FX

US10Y:
~5.31%

Intraday:
~5.35%

DXY:
102.19

Intraday high:
102.53

USDJPY:
~158.04

Interpretation:

Dollar and long-end yields remain strong
despite reduced October Fed hike probability.

## Equities

S&P500:
7773.95
+0.66%

Nasdaq Composite:
27477.31
+1.05%
record close

ESZ26:
~7830

NQZ26:
~31300 area

VIX:
15.52

Observation:

NASDAQ continues to absorb
extreme long-end yield pressure.

Do not chase.

New preferred NQ pullback:
31000-31100

Required:
US10Y <5.20
VIX <=15.5

## Crypto

BTC spot:
~85700-85800

BTC CME:
Oct5 high 87397.5
close area ~86k

BTC ETF latest complete:
Oct2 +189.9m

Oct5:
not finalized

ETH spot:
~2712

ETH CME:
~2720

ETH ETF latest complete:
Oct2 -37.4m

Observation:

BTC almost exactly touched
previous 87400 breakout threshold
but failed to maintain it.

No new signal.

## Gold

GCZ26:
4156.8

Drivers:
DXY strong
US10Y high
October hike probability lower

No trade at support.

Sell observation:
4190-4210
US10Y >5.25
DXY >102

## WTI

Current:
89.43

New:
20261006_WTI_SELL_PULLBACK

Entry:
90.20-90.80

Mid:
90.50

SL:
92.00

TP1:
87.20

TP2:
84.80

RR:
2.20

win_prob:
0.52

two-point EV:
+0.66R

subjective expected_r:
+0.34R

MAE:
0.30R

risk:
0.25%

Rank:
B

Conditional B+:
YES if XM OILCash 0.01 lot
NO if standard OIL futures minimum lot exceeds loss cap

Drivers:
Middle East crude exports recovering
G7 reserve release
WTI below 90

Counterforces:
shipping cost
insurance
refining shortage
diesel shortage
Iran headline risk

Execution:
DO NOT chase at 89.43
sell rebound only

## USDJPY intervention observation

Current:
158.04

No Intervention Shock trigger yet.

159-160:
normal momentum BUY quality deteriorates

Separate:
normal TSO signal
from
Intervention Shock Module.

## Active invalidation

20261006_WTI_SELL_PULLBACK=not_fired

## New signals

A:
NONE

B:
WTI SELL_PULLBACK

#TSO #US10Y #WTI #NASDAQ #BTC #USDJPY
```

---

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-10-06,20261006_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,94,84,,MIXED,89,95,98,89,89,97,wait_for_GCZ26_rebound_4190_4210_with_US10Y_above_5.25_or_reclaim_4230_with_US10Y_below_5.15,GCZ26_4100_4140_4156.8_4190_4210_4230_US10Y_DXY_1d_3d,verified
2026-10-06,20261006_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,95,79,,MIXED,84,94,98,90,88,90,previous_87400_breakout_not_maintained_wait_for_87500_hold_with_CME_and_ETF_confirmation,BTC_84000_85750_87400_87500_CME_ETF_1d_3d,partially_verified
2026-10-06,20261006_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,85,88,,MIXED,78,90,96,82,80,84,wait_for_ETH_reclaim_2750_2800_with_ETF_inflow_and_BTC_confirmation_or_break_below_2630,ETH_2630_2712_2750_2800_ETF_CME_1d_3d,partially_verified
2026-10-06,20261006_WTI_SELL_PULLBACK,WTI,SELL,B,PULLBACK,90.20,90.80,92.00,87.20,84.80,2.20,0.52,0.34,99,96,42,0.25,EVENT,63,93,96,87,79,94,WTI_above_92.00_or_confirmed_new_major_supply_disruption_invalidates_bearish_supply_relief_thesis,WTI_87.20_89.43_90.20_90.80_92.00_G7_Hormuz_exports_logistics_1d_3d_5d,verified
2026-10-06,20261006_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,94,90,,EVENT,94,98,99,95,92,98,avoid_normal_momentum_buy_toward_159_160_intervention_sensitive_zone_wait_for_pullback_or_policy_response,USDJPY_157_158.04_159_160_US10Y_DXY_MOF_intervention_1d_3d,verified
2026-10-06,20261006_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,97,66,,RISK_ON,89,95,97,94,93,95,do_not_chase_highs_wait_for_ES_pullback_7800_7810_with_US10Y_below_5.20_or_clean_hold_above_7850,ESZ26_7780_7800_7810_7830_7850_US10Y_VIX_1d_3d,partially_verified
2026-10-06,20261006_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,99,59,,RISK_ON,91,96,98,97,96,97,trend_strong_but_yield_condition_failed_wait_for_NQ_pullback_31000_31100_with_US10Y_below_5.20,NQZ26_30900_31000_31100_31300_31400_US10Y_VIX_1d_3d,partially_verified
2026-10-06,20261006_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,94,83,,MIXED,90,95,98,90,89,97,do_not_chase_17_month_high_wait_for_DXY_hold_above_102.5_or_failure_below_101.7_with_yield_confirmation,DXY_101.7_102.19_102.53_US10Y_USDJPY_EURUSD_1d_3d,verified
2026-10-06,20261006_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,99,95,,EVENT,99,99,99,99,99,99,do_not_chase_5.35_wait_for_sustained_break_above_5.35_or_rejection_below_5.20,US10Y_5.20_5.31_5.35_ISM_FOMC_minutes_Treasury_auctions_1d_3d,verified
2026-10-06,20261006_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,89,80,,RISK_ON,80,92,97,83,82,90,wait_for_VIX_hold_below_15_or_reclaim_above_17_with_ES_NQ_confirmation,VIX_15_15.52_17_ES_NQ_US10Y_1d_3d,verified
```

### TSO_LOG JSON

```json
[
  {"date":"2026-10-06","signal_id":"20261006_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":94,"no_trade_score":84,"risk_pct":null,"regime":"MIXED","ems":89,"ffs":95,"cds":98,"ias":89,"cbs":89,"mes":97,"invalidation":"wait_for_GCZ26_rebound_4190_4210_with_US10Y_above_5.25_or_reclaim_4230_with_US10Y_below_5.15","verification_target":"GCZ26_4100_4140_4156.8_4190_4210_4230_US10Y_DXY_1d_3d","verified_status":"verified"},
  {"date":"2026-10-06","signal_id":"20261006_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":95,"no_trade_score":79,"risk_pct":null,"regime":"MIXED","ems":84,"ffs":94,"cds":98,"ias":90,"cbs":88,"mes":90,"invalidation":"previous_87400_breakout_not_maintained_wait_for_87500_hold_with_CME_and_ETF_confirmation","verification_target":"BTC_84000_85750_87400_87500_CME_ETF_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-10-06","signal_id":"20261006_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":85,"no_trade_score":88,"risk_pct":null,"regime":"MIXED","ems":78,"ffs":90,"cds":96,"ias":82,"cbs":80,"mes":84,"invalidation":"wait_for_ETH_reclaim_2750_2800_with_ETF_inflow_and_BTC_confirmation_or_break_below_2630","verification_target":"ETH_2630_2712_2750_2800_ETF_CME_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-10-06","signal_id":"20261006_WTI_SELL_PULLBACK","asset":"WTI","side":"SELL","rank":"B","type":"PULLBACK","entry_low":90.20,"entry_high":90.80,"sl":92.00,"tp1":87.20,"tp2":84.80,"rr":2.20,"win_prob":0.52,"expected_r":0.34,"tq_score":99,"opp_score":96,"no_trade_score":42,"risk_pct":0.25,"regime":"EVENT","ems":63,"ffs":93,"cds":96,"ias":87,"cbs":79,"mes":94,"invalidation":"WTI_above_92.00_or_confirmed_new_major_supply_disruption_invalidates_bearish_supply_relief_thesis","verification_target":"WTI_87.20_89.43_90.20_90.80_92.00_G7_Hormuz_exports_logistics_1d_3d_5d","verified_status":"verified"},
  {"date":"2026-10-06","signal_id":"20261006_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":94,"no_trade_score":90,"risk_pct":null,"regime":"EVENT","ems":94,"ffs":98,"cds":99,"ias":95,"cbs":92,"mes":98,"invalidation":"avoid_normal_momentum_buy_toward_159_160_intervention_sensitive_zone_wait_for_pullback_or_policy_response","verification_target":"USDJPY_157_158.04_159_160_US10Y_DXY_MOF_intervention_1d_3d","verified_status":"verified"},
  {"date":"2026-10-06","signal_id":"20261006_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":97,"no_trade_score":66,"risk_pct":null,"regime":"RISK_ON","ems":89,"ffs":95,"cds":97,"ias":94,"cbs":93,"mes":95,"invalidation":"do_not_chase_highs_wait_for_ES_pullback_7800_7810_with_US10Y_below_5.20_or_clean_hold_above_7850","verification_target":"ESZ26_7780_7800_7810_7830_7850_US10Y_VIX_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-10-06","signal_id":"20261006_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":99,"no_trade_score":59,"risk_pct":null,"regime":"RISK_ON","ems":91,"ffs":96,"cds":98,"ias":97,"cbs":96,"mes":97,"invalidation":"trend_strong_but_yield_condition_failed_wait_for_NQ_pullback_31000_31100_with_US10Y_below_5.20","verification_target":"NQZ26_30900_31000_31100_31300_31400_US10Y_VIX_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-10-06","signal_id":"20261006_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":94,"no_trade_score":83,"risk_pct":null,"regime":"MIXED","ems":90,"ffs":95,"cds":98,"ias":90,"cbs":89,"mes":97,"invalidation":"do_not_chase_17_month_high_wait_for_DXY_hold_above_102.5_or_failure_below_101.7_with_yield_confirmation","verification_target":"DXY_101.7_102.19_102.53_US10Y_USDJPY_EURUSD_1d_3d","verified_status":"verified"},
  {"date":"2026-10-06","signal_id":"20261006_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":99,"no_trade_score":95,"risk_pct":null,"regime":"EVENT","ems":99,"ffs":99,"cds":99,"ias":99,"cbs":99,"mes":99,"invalidation":"do_not_chase_5.35_wait_for_sustained_break_above_5.35_or_rejection_below_5.20","verification_target":"US10Y_5.20_5.31_5.35_ISM_FOMC_minutes_Treasury_auctions_1d_3d","verified_status":"verified"},
  {"date":"2026-10-06","signal_id":"20261006_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":89,"no_trade_score":80,"risk_pct":null,"regime":"RISK_ON","ems":80,"ffs":92,"cds":97,"ias":83,"cbs":82,"mes":90,"invalidation":"wait_for_VIX_hold_below_15_or_reclaim_above_17_with_ES_NQ_confirmation","verification_target":"VIX_15_15.52_17_ES_NQ_US10Y_1d_3d","verified_status":"verified"}
]
```

本日の最大の観察は、**ISM Prices 74.0とUS10Y 5.31%にもかかわらずNASDAQが最高値を更新したこと**です。これはかなり強い相対強度ですが、今からNQを追うより、金利が5.20%以下へ下がったときに株価が崩れず残るかを見る方がEntryとして有利です。citeturn748118view0turn156737view1

一方、WTIは昨日まで待っていた90ドル割れが実現しました。今日の唯一の方向判断は**90.20–90.80への戻りだけを売るB級SELL_PULLBACK**です。89ドル台からの追随SELLは禁止します。 memcite
