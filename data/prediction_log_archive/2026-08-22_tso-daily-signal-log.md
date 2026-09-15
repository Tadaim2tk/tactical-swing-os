<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-08-22 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 15168 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026年8月22日

データ基準は**8月21日（金）の米国市場終値＋8月22日06:57 JST前後の暗号資産**です。土曜日のためGOLD・WTI・ES・NQ・DXY・US10Y・VIXは金曜終値をアンカーにします。部分欠損があっても停止せず、10資産すべて記帳します。

金曜日はS&P500が**7674.37（+0.43%）**、NASDAQ総合が**26180.45（+0.44%）**へ反発しましたが、週間ではそれぞれ-1.4%、-2.1%。米10年債利回りは約**4.70%**と高止まりし、WTIは**87.06ドル**まで6営業日連続で上昇しました。citeturn470040view0turn950097news48turn950097news3turn470040view3

一方、COMEX金先物は契約差がありますが、Reutersの米金先物は**4680.60**、前日比+2.4%。BTCは金曜日に一時**79463**まで上昇し、16:00 ET時点で約77000～77400。ETHも8月21日の日次値で**2326.53**まで急伸しています。citeturn470040view1turn491264news59turn491264news64turn389962news50

なお、ブローカー実執行時の許容損失については、直近の運用更新を優先し**約3000円/回**を使用します。月次較正文中の1500円は旧値として扱います。memcite

## 1. 本日の結論

**A級：0件。**

**B+：0件。**

**B級：GOLD BUY、BTC BUY、ETH BUY。**

**NO_TRADE：WTI、USDJPY、SPX、NASDAQ、DXY、US10Y、VIX。**

本日の分析順位は、

**GOLD B > BTC B > ETH B**

です。

昨日までの「GOLD/BTCだけが株式と異なる相対強度を示す」という構造がさらに強まりました。BTC ETFには8月17～20日の4営業日だけで約**16.1億ドル**が流入し、8月20日単日でも+6.063億ドル。ETH ETFにも同日+2.195億ドルが入りました。citeturn470040news23

ただしBTCは週間+20%超、GOLDも週間+5%超。citeturn491264news59turn470040view1

したがって今日は**強いから買うのではなく、強いので押し目だけを待つ**という判断です。

---

## 2. 前回判断の簡易検証

### GOLD B BUY → **DIRECTION_SUCCESS / NO_FILL濃厚**

昨日：

**Entry 4480–4530  
SL 4350  
TP1 4750**

金曜日の米金先物は4680.60で+2.4%。citeturn470040view1

方向は完全に成功しました。

一方、前日終値水準からさらに上へ走っており、4480～4530へ十分な押しが入ったことは確認できません。

したがって、

**DIRECTION_SUCCESS  
NO_FILL_PROBABLE**

です。

ここでもEntryを追い上げて成行購入していれば、TSOのルール逸脱になります。

---

### BTC B BUY → **DIRECTION_SUCCESS / NO_FILL濃厚**

昨日：

**Entry 69000–70500  
SL 66000  
TP1 76000**

BTCはその後76000を突破し、一時79463まで上昇しました。citeturn491264news59

つまり方向判定ならTP1相当まで成功。

しかし昨日すでに72k台にいたため、69～70.5kへのリテストが確認できないまま上昇しました。

暫定：

**DIRECTION_SUCCESS  
TP1_PRICE_REACHED  
ENTRY_FILL_UNVERIFIED**

です。

実売買成績としてTP1成功とは数えません。

---

### ETH NO_TRADE → **機会損失 / 本日再評価**

ETHは8月19日の1914.81から20日2253.56、21日2326.53へ急上昇しました。citeturn389962news50

さらにETH ETFは8月20日に**+219.5M**、17～20日の4日間で約+508.6M。citeturn470040news23

昨日までのETH NO_TRADEは、当時価格系列の不整合を重視したためですが、現在は、

**ETF flow positive  
＋ price confirmation positive**

が確認できました。

したがって本日からBへ昇格します。

---

### WTI NO_TRADE → **成功継続**

WTIは87.06で6営業日連続上昇。週間+5.66%。citeturn470040view3

それでもNO_TRADEを維持します。

Hormuz通航量低下、対イラン制裁強化、ロシア製油所攻撃などの供給ショックが中心だからです。citeturn470040view3

---

## 3. 市場全体の前提

本日のRegimeは、

**`WEEKEND_HARD_ASSET_RALLY / USD_DEBASEMENT / HIGH_LONG_YIELDS / OIL_SUPPLY_PREMIUM / EQUITY_RELIEF_NOT_CONFIRMATION`**

です。

非常に特徴的なのは、

**US10Y 約4.70%  
WTI 87ドル  
にもかかわらず  
GOLD・BTCが急上昇**

していることです。

通常なら高金利・原油高は金や長duration資産に逆風ですが、今回は米財政・国債買い戻し政策への懸念から「ドル資産以外への分散」が強まっています。Reutersもこの動きをドルの`debasement`懸念と結びつけています。DXYは約98.76、USDJPYは159.01付近でした。citeturn950097news3turn950097news47

一方、株式は金曜日こそ反発しましたが、週間ではS&P500 -1.4%、NASDAQ -2.1%。citeturn950097news48

つまり現状は、

**全面Risk-on**

ではありません。

**Hard assets / crypto > equities**

です。

---

## 4. 10資産別判断

| 資産 | 判定 | 核心 |
|---|---|---|
| GOLD | **B BUY** | 4680までbreakout、押し目限定 |
| BTC | **B BUY** | ETF＋価格確認、ただし極端な過熱 |
| ETH | **B BUY** | ETF＋価格確認へ転換、急騰後 |
| WTI | **NO_TRADE** | 供給ショック6日連騰 |
| USDJPY | **NO_TRADE** | 159付近、BOJ・介入・ドル不信が衝突 |
| SPX | **NO_TRADE** | 金曜反発のみ、週間構造は弱い |
| NASDAQ | **NO_TRADE** | 金曜反発のみ、週間-2.1% |
| DXY | **NO_TRADE** | 98.76、既に大幅軟化後 |
| US10Y | **NO_TRADE** | 4.70、財政・政策介入の綱引き |
| VIX | **NO_TRADE** | 15台推定、株式regime確認用 |

---

## 5. A級候補

**0件です。**

GOLDは基礎条件だけなら、

**CBS 86  
EMS 83**

と非常に強い。

しかし現在の上方extensionを考慮すると、

**expected_r 0.43  
MAE想定 0.28R**

なのでA条件を外します。

BTCも、

**CBS 86  
EMS 82  
MES 84**

まで改善しましたが、週間+20%超・大量ショート清算後なのでMAE想定を0.32Rとします。citeturn491264news59

ETHも同じく急伸直後。

したがってAは作りません。

---

## 6. B級監視候補

### 1位 GOLD — BUY PULLBACK

**Entry 4560–4610  
SL 4440  
TP1 4890  
TP2 5050  
RR 2.10  
win_prob 0.64  
較正参考 0.67  
expected_r 0.43  
MAE 0.28R  
risk_pct 0.25%**

COMEX金先物は4680.60まで上昇。citeturn470040view1

**4680からは買いません。**

4560～4610への押しが入り、ドル安・金価格構造が維持される場合だけ候補です。

---

### 2位 BTC — BUY PULLBACK

**Entry 73500–75500  
SL 70000  
TP1 82000  
TP2 86000  
RR 1.67  
win_prob 0.62  
較正参考 0.65  
expected_r 0.42  
MAE 0.32R  
risk_pct 0.25%**

BTCは一時79463、16時ET時点で約77k。citeturn491264news59turn491264news64

ETFは4日で約16.1億ドル流入。citeturn470040news23

需給確認はかなり強い。

ただし75.5kより上なら追いません。

さらにXM最小ロット＋SL70000で想定実損が約3000円を超えるなら、

**Signal=B / Execution=NO_TRADE**

です。

---

### 3位 ETH — BUY PULLBACK

**Entry 2150–2260  
SL 1980  
TP1 2600  
TP2 2800  
RR 1.76  
win_prob 0.59  
較正参考 0.62  
expected_r 0.37  
MAE 0.34R  
risk_pct 0.25%**

8月21日日次値は2326.53。citeturn389962news50

ETH ETFは4営業日連続流入、合計約508.6M。citeturn470040news23

昨日までとは条件が変わりました。

ただし2000近辺から2300超まで短期間に上昇しているため、BTC以上にMAEを大きく見ます。

**押し目以外はNO_TRADE。**

---

## 7. 触らない資産

最優先は**WTI**です。

WTI 87.06、Brent 94.39。Hormuzを通過した商品船は木曜日わずか7隻で、通常のエネルギー輸送は依然大きく制約されています。citeturn470040view3

これはテクニカル上昇トレンドではなく、

**geopolitical supply premium**

が支配する相場です。

NASDAQも今日は買いません。

金曜日に+0.44%戻しても週間では-2.1%。citeturn950097news48

米10年4.70%・WTI87ドルという組み合わせでは、再びA/B BUYへ戻すにはNQ自身の複数日の安定が必要です。

---

## 8. 後日検証ポイント

最重要は**BTCのFLOW_TO_PRICE_LAG仮説**です。

8月上旬には、

**ETF流入  
→ BTC価格反応なし**

でした。

その後一度フローが悪化し、今週は、

**Aug17 +297.5M  
Aug18 +189.3M  
Aug19 +517.2M  
Aug20 +606.3M  
→ 合計 約1.61B**

と再加速。BTCは65k→70k→79k近辺まで上昇しました。citeturn470040news23turn491264news59

これはTSOの教師データとしてかなり価値があります。

次の5営業日では、

**BTC 75k維持率  
70k再テスト有無  
ETF流入継続  
MFE/MAE**

を保存します。

ETHについても同様に、ETFフローと価格伝播のラグを別系列で記録します。

GOLDでは、前回Bが再び**方向成功だがNO_FILL**になった可能性が高いため、NASDAQで行っているEntry研究をGOLDにも適用します。

---

## 9. Obsidian保存用Observation Draft

```markdown
# 2026-08-22 Hard Asset Rally / GOLD・BTC・ETH flow-price confirmation

## Market anchors

S&P500:
7674.37
+0.43%
weekly -1.4%

NASDAQ Composite:
26180.45
+0.44%
weekly -2.1%

US10Y:
~4.70%

DXY:
~98.76

USDJPY:
~159.0

WTI:
87.06

Brent:
94.39

COMEX Gold futures:
4680.60

BTC:
~77k
intraday high ~79463

ETH:
2326.53 daily reference

## Regime

WEEKEND_HARD_ASSET_RALLY
USD_DEBASEMENT
HIGH_LONG_YIELDS
OIL_SUPPLY_PREMIUM
EQUITY_RELIEF_NOT_CONFIRMATION

## Crypto flows

BTC ETF:

Aug17 +297.5m
Aug18 +189.3m
Aug19 +517.2m
Aug20 +606.3m

4d:
~+1.61bn

ETH ETF Aug20:
+219.5m

ETH 4d:
~+508.6m

## Interpretation

Previous regime:

positive ETF flow
+
weak price transmission

Current regime:

positive ETF flow
+
strong price breakout

FLOW_TO_PRICE_LAG hypothesis supported.

## Signals

A:
NONE

B:

GOLD BUY
4560-4610
SL 4440
TP1 4890

BTC BUY
73500-75500
SL 70000
TP1 82000

ETH BUY
2150-2260
SL 1980
TP1 2600

NO_TRADE:

WTI
USDJPY
SPX
NASDAQ
DXY
US10Y
VIX

## Policy

No momentum chase.

BTC >75500:
NO_FILL

Gold >4610:
NO_FILL

ETH >2260:
NO_FILL

## Research

BTC:
FLOW_TO_PRICE_LAG

ETH:
ETF_FLOW_TO_PRICE_LAG

GOLD:
direction success vs Entry arrival

#TSO #GOLD #BTC #ETH #ETF #US10Y #WTI
```

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-08-22,20260822_GOLD_BUY_PULLBACK,GOLD,BUY,B,PULLBACK,4560,4610,4440,4890,5050,2.10,0.64,0.43,98,75,35,0.25,HARD_ASSET_RALLY_USD_DEBASEMENT,83,84,78,88,86,81,4440_break_or_DXY_US10Y_acceleration,GOLD_entry_24h_3d_5d_MFE_MAE_entry_model,verified
2026-08-22,20260822_BTC_BUY_PULLBACK,BTC,BUY,B,PULLBACK,73500,75500,70000,82000,86000,1.67,0.62,0.42,99,69,47,0.25,BTC_ETF_FLOW_BREAKOUT_OVEREXTENDED,82,88,81,85,86,84,70000_break_or_ETF_flow_reversal,BTC_70k_75k_82k_ETF_3d_5d_MFE_MAE,verified
2026-08-22,20260822_ETH_BUY_PULLBACK,ETH,BUY,B,PULLBACK,2150,2260,1980,2600,2800,1.76,0.59,0.37,95,65,53,0.25,ETH_ETF_FLOW_PRICE_BREAKOUT_OVEREXTENDED,72,81,78,74,76,73,1980_break_or_ETH_ETF_flow_reversal,ETH_2k_2.2k_2.6k_ETF_ETHBTC_3d_5d,partially_verified
2026-08-22,20260822_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,15,99,,HORMUZ_SUPPLY_SHOCK_SIX_DAY_RALLY,91,80,99,15,56,80,supply_shock_momentum_chase_prohibited,WTI_85_90_Hormuz_3d_5d,verified
2026-08-22,20260822_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,90,37,91,,USD_WEAK_BOJ_INTERVENTION_CONFLICT,73,76,90,38,65,70,160_intervention_BOJ_and_DXY_conflict,USDJPY_157_160_DXY_US10Y_3d,partially_verified
2026-08-22,20260822_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,86,47,76,,FRIDAY_EQUITY_RELIEF_WEEKLY_DOWNTREND,66,72,79,52,69,68,ES_multi_day_stabilization_and_US10Y_decline_required,ES_US10Y_VIX_week_open_1d_3d,partially_verified
2026-08-22,20260822_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,91,42,82,,TECH_WEEKLY_PULLBACK_LONG_YIELD_HEADWIND,62,71,84,47,66,65,NQ_multi_day_stabilization_and_yield_relief_required,NQ_US10Y_SOX_week_open_1d_3d,partially_verified
2026-08-22,20260822_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,93,35,91,,USD_DEBASEMENT_EXTENDED,78,82,89,34,69,78,DXY_reclaim_100_or_confirm_break_below_98_required,DXY_98_100_US10Y_3d_5d,partially_verified
2026-08-22,20260822_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,24,97,,FISCAL_TERM_PREMIUM_BUYBACK_CONFLICT,85,90,97,23,75,86,confirmed_break_below_4.60_or_above_4.75_required,US10Y_4.60_4.75_week_open_3d_5d,verified
2026-08-22,20260822_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,78,44,77,,VOL_RELIEF_WITH_WEEKLY_EQUITY_WEAKNESS,65,63,76,59,66,62,VIX_above_17_or_below_14_confirms_next_regime,VIX_14_17_ES_NQ_week_open_3d,partially_verified
```

### JSON

```json
[
{"date":"2026-08-22","signal_id":"20260822_GOLD_BUY_PULLBACK","asset":"GOLD","side":"BUY","rank":"B","type":"PULLBACK","entry_low":4560,"entry_high":4610,"sl":4440,"tp1":4890,"tp2":5050,"rr":2.10,"win_prob":0.64,"expected_r":0.43,"tq_score":98,"opp_score":75,"no_trade_score":35,"risk_pct":0.25,"regime":"HARD_ASSET_RALLY_USD_DEBASEMENT","ems":83,"ffs":84,"cds":78,"ias":88,"cbs":86,"mes":81,"invalidation":"4440_break_or_DXY_US10Y_acceleration","verification_target":"GOLD_entry_24h_3d_5d_MFE_MAE_entry_model","verified_status":"verified"},
{"date":"2026-08-22","signal_id":"20260822_BTC_BUY_PULLBACK","asset":"BTC","side":"BUY","rank":"B","type":"PULLBACK","entry_low":73500,"entry_high":75500,"sl":70000,"tp1":82000,"tp2":86000,"rr":1.67,"win_prob":0.62,"expected_r":0.42,"tq_score":99,"opp_score":69,"no_trade_score":47,"risk_pct":0.25,"regime":"BTC_ETF_FLOW_BREAKOUT_OVEREXTENDED","ems":82,"ffs":88,"cds":81,"ias":85,"cbs":86,"mes":84,"invalidation":"70000_break_or_ETF_flow_reversal","verification_target":"BTC_70k_75k_82k_ETF_3d_5d_MFE_MAE","verified_status":"verified"},
{"date":"2026-08-22","signal_id":"20260822_ETH_BUY_PULLBACK","asset":"ETH","side":"BUY","rank":"B","type":"PULLBACK","entry_low":2150,"entry_high":2260,"sl":1980,"tp1":2600,"tp2":2800,"rr":1.76,"win_prob":0.59,"expected_r":0.37,"tq_score":95,"opp_score":65,"no_trade_score":53,"risk_pct":0.25,"regime":"ETH_ETF_FLOW_PRICE_BREAKOUT_OVEREXTENDED","ems":72,"ffs":81,"cds":78,"ias":74,"cbs":76,"mes":73,"invalidation":"1980_break_or_ETH_ETF_flow_reversal","verification_target":"ETH_2k_2.2k_2.6k_ETF_ETHBTC_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-22","signal_id":"20260822_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":15,"no_trade_score":99,"risk_pct":null,"regime":"HORMUZ_SUPPLY_SHOCK_SIX_DAY_RALLY","ems":91,"ffs":80,"cds":99,"ias":15,"cbs":56,"mes":80,"invalidation":"supply_shock_momentum_chase_prohibited","verification_target":"WTI_85_90_Hormuz_3d_5d","verified_status":"verified"},
{"date":"2026-08-22","signal_id":"20260822_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":90,"opp_score":37,"no_trade_score":91,"risk_pct":null,"regime":"USD_WEAK_BOJ_INTERVENTION_CONFLICT","ems":73,"ffs":76,"cds":90,"ias":38,"cbs":65,"mes":70,"invalidation":"160_intervention_BOJ_and_DXY_conflict","verification_target":"USDJPY_157_160_DXY_US10Y_3d","verified_status":"partially_verified"},
{"date":"2026-08-22","signal_id":"20260822_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":86,"opp_score":47,"no_trade_score":76,"risk_pct":null,"regime":"FRIDAY_EQUITY_RELIEF_WEEKLY_DOWNTREND","ems":66,"ffs":72,"cds":79,"ias":52,"cbs":69,"mes":68,"invalidation":"ES_multi_day_stabilization_and_US10Y_decline_required","verification_target":"ES_US10Y_VIX_week_open_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-22","signal_id":"20260822_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":91,"opp_score":42,"no_trade_score":82,"risk_pct":null,"regime":"TECH_WEEKLY_PULLBACK_LONG_YIELD_HEADWIND","ems":62,"ffs":71,"cds":84,"ias":47,"cbs":66,"mes":65,"invalidation":"NQ_multi_day_stabilization_and_yield_relief_required","verification_target":"NQ_US10Y_SOX_week_open_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-22","signal_id":"20260822_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":93,"opp_score":35,"no_trade_score":91,"risk_pct":null,"regime":"USD_DEBASEMENT_EXTENDED","ems":78,"ffs":82,"cds":89,"ias":34,"cbs":69,"mes":78,"invalidation":"DXY_reclaim_100_or_confirm_break_below_98_required","verification_target":"DXY_98_100_US10Y_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-22","signal_id":"20260822_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":24,"no_trade_score":97,"risk_pct":null,"regime":"FISCAL_TERM_PREMIUM_BUYBACK_CONFLICT","ems":85,"ffs":90,"cds":97,"ias":23,"cbs":75,"mes":86,"invalidation":"confirmed_break_below_4.60_or_above_4.75_required","verification_target":"US10Y_4.60_4.75_week_open_3d_5d","verified_status":"verified"},
{"date":"2026-08-22","signal_id":"20260822_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":78,"opp_score":44,"no_trade_score":77,"risk_pct":null,"regime":"VOL_RELIEF_WITH_WEEKLY_EQUITY_WEAKNESS","ems":65,"ffs":63,"cds":76,"ias":59,"cbs":66,"mes":62,"invalidation":"VIX_above_17_or_below_14_confirms_next_regime","verification_target":"VIX_14_17_ES_NQ_week_open_3d","verified_status":"partially_verified"}
]
```

**8月22日の核心は、GOLD・BTCに加えてETHも「flowとpriceが同方向」へ移ったことです。** BTC ETFでは4日間で約16.1億ドル、ETH ETFでは約5.09億ドルの流入が確認され、価格もそれぞれ明確に上昇しています。citeturn470040news23

ただしこれは同時に**最も追いかけてはいけない局面**でもあります。GOLDは4680、BTCは一時79k、ETHは2300超。月曜日までに提示Entryへ押さなければ、3つとも`NO_FILL`で終了するのが本日のTSO判断です。
