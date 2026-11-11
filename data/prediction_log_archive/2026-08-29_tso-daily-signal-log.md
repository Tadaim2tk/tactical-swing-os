<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-08-29 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 13915 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-08-29

データ基準は**8月28日米国市場終了後〜8月29日07:00 JST前後**です。米国株・先物・債券・商品は週末入りしているため直近金曜終値を基準にし、BTC/ETHのみ週末も価格変動中として扱います。NQ/ESの正確な清算値を十分な品質で直接確認できなかったため、NASDAQ/SPXの価格系列は`partially_verified`とします。NASDAQ行にNASDAQ総合やQQQを代入してはいません。

## 1. 本日の結論

**A級：0件**

**B+観察候補：BTC BUY**

**B級：ETH BUY**

**NO_TRADE：GOLD、WTI、USDJPY、SPX、NASDAQ、DXY、US10Y、VIX**

昨日から最も重要な変化は、entity["organization","Federal Reserve","United States central bank"]議長Kevin WarshのJackson Hole講演です。インフレ抑制のため追加利上げが必要になり得るとの姿勢を示し、9月利上げ確率は約35%から55〜60%程度へ急上昇しました。ドルと米国債利回りが上昇し、金・BTC・NASDAQには逆風となりました。citeturn2news13turn2news14turn0news86

したがって朝の判断からは明確に変更します。

**NASDAQ B+ BUY → NO_TRADE**  
**GOLD B+ BUY → NO_TRADE**

です。

これは仮説の完全否定というより、**「NvidiaによるAI上昇」より「Fedによる金利再評価」の支配力が強くなったため、新規Entryの期待値が不足した**という判断です。

---

## 2. 前回判断の簡易検証

### NASDAQ B+ BUY → **弱化／新規停止**

金曜のNASDAQ総合は**26402.42、-0.52%**、S&P500は**7711.76、-0.25%**でした。citeturn1news51turn0news81

前日のNvidia決算後上昇をすべて吐き出したわけではありません。週間ではNASDAQはなお**+0.8%**です。citeturn1news51

したがって、

**AI earnings thesis = 生存  
短期NASDAQ BUY entry thesis = 一旦停止**

と分離します。

特にWarsh講演後、利上げ観測上昇→債券利回り上昇→高PERテクノロジー売り、という因果がきれいに出ています。citeturn1news52turn2news13

昨日相談していたXM US100Cashについても、週末をまたいで新たに買い増す局面ではありません。

### GOLD B+ BUY → **失敗寄り・停止**

ここが昨日から最大の修正です。

GoldはWarsh発言後に**3%以上急落**し、Reutersではspot **4567.23**、December COMEX **4529.90**まで低下。金曜の下落は明確に金利上昇・ドル高によるものです。citeturn2news12

昨日の監視帯4550–4610には到達しましたが、これは理想的な押し目ではなく、

**「BUY材料を壊すマクロ変化によってEntryまで下落した」**

ケースです。

したがって**価格がEntryに来たから買う、とは扱いません。**

これはTSOにとって重要な教師データです。

### BTC B → **生存**

金曜朝にはBTCが81200付近まで上昇後79560付近へ戻りました。直近検索値では約**80393**。citeturn1search0turn1search3

WarshショックでもBTCが大きく崩れていない点は評価します。

一方、金利上昇は明確な逆風なのでAには上げません。

### ETH B → **生存**

ETHは金曜約**2500前後**。8月安値から約29%上昇しており、ETF流入も背景にありますが、短期的には過熱感があります。citeturn0news4turn1search6

よって押し目限定です。

---

## 3. 市場全体の前提

本日のRegimeは、

**`HAWKISH_FED_REPRICING / AI_TREND_INTACT_BUT_RATE_PRESSURED / STRONGER_DOLLAR / HIGHER_YIELDS / WEEKEND_GAP_RISK`**

へ変更します。

Warsh発言後、9月利上げ確率は約55〜60%へ上昇。短期債利回りが急騰し、ドルは約2カ月半で最大の上昇となりました。citeturn2news13turn2news14

Goldはこの変化に非常に素直に反応して3%以上下落。citeturn2news12

WTIは**83.40**で終了し、週間では4%以上下落。Hormuz再開協議とFed引き締め観測が同時に効いています。citeturn2news16

さらに米株ファンドは8月26日までの週に**223.3億ドル流出**し、3月以来最大の週間流出となりました。citeturn0news82

したがって月曜日に向けては、

**「押したから買う」ではなく、「押した理由が解消したことを確認してから買う」**

へ一段防御的に変更します。

---

## 4. 10資産別判断

| 資産 | 判定 | 判断 |
|---|---|---|
| GOLD | **NO_TRADE** | BUY仮説をFedが破壊 |
| BTC | **B+ BUY** | 77000–79000押し目限定 |
| ETH | **B BUY** | 2380–2460押し目限定 |
| WTI | **NO_TRADE** | Hormuz headline依存 |
| USDJPY | **NO_TRADE** | Fed＋介入リスク |
| SPX | **NO_TRADE** | 金利再評価待ち |
| NASDAQ | **NO_TRADE** | AI強気と金利弱気が衝突 |
| DXY | **NO_TRADE** | Warsh後の急騰追随禁止 |
| US10Y | **NO_TRADE** | 金利上昇追随禁止 |
| VIX | **NO_TRADE** | 確認系列 |

---

## 5. A級候補

**なし。**

NASDAQは昨日まで最も近い候補でしたが、Fed regime changeによって外します。

ここで重要なのは、NASDAQのAI仮説そのものを削除しないことです。

WarshはAIによる生産性向上について肯定的な発言もしており、Mag7の一部は講演後むしろ上昇しました。citeturn0news87

したがって月曜以降、

**US10Y上昇停止  
＋NQが金曜安値を割らない  
＋半導体breadth回復**

ならNASDAQ BUYを再起動できます。

---

## 6. B級監視候補

### BTC — **B+ BUY PULLBACK**

**Entry 77000–79000  
SL 73000  
TP1 85000  
TP2 89000  
RR 1.50  
win_prob 0.61  
較正参考 0.64  
expected_r 0.39  
MAE 0.30R  
risk_pct 0.25%**

現在約80kなので**今から追いません**。citeturn1search3

Warshショックに対する価格耐性はプラスですが、金利上昇という逆風を無視できません。

CBS76 / EMS72 / RR1.50なので、XM最小ロット実損3000円以内なら**B+観察候補**です。

### ETH — **B BUY PULLBACK**

**Entry 2380–2460  
SL 2160  
TP1 2800  
TP2 3000  
RR 1.55  
win_prob 0.58  
較正参考 0.61  
expected_r 0.35  
MAE 0.34R  
risk_pct 0.25%**

約2500なので、こちらも追いません。citeturn0news4turn1search6

BTCより過熱・ボラティリティが高いためB据え置きです。

---

## 7. 触らない資産

特に**GOLDとNASDAQ**です。

GOLDは昨日までのBUY Entry帯へ落ちましたが、今回は「安くなった」のではなく、**金利・ドルという説明変数が悪化して下がった**ためです。citeturn2news12

NASDAQも同じです。

Nvidia決算そのものは依然強い一方、Fedがdiscount rateを引き上げる可能性が増しました。

ここで安易に「昨日より安いから買う」とすると、TSOがファンダメンタル変化を無視した単純逆張りになります。

WTIも83.40ですが、Hormuz再開観測だけで週明けgapが出るため触りません。citeturn2news16

USDJPYについては、日本が7月30日〜8月26日に**15.4兆円規模の円買い介入**を行ったことが確認されました。ドル高Fed材料があっても、159円台を機械的にBUYするのは危険です。citeturn2news15

---

## 8. 後日検証ポイント

今回最も価値がある検証系列は、

**8/26 Nvidia前 → NASDAQ NO_TRADE  
8/27 Nvidia確認 → NASDAQ BUY  
8/27 follow-through → 成功  
8/28 Warsh hawkish → 金利regime変化  
8/29 → NASDAQ新規停止**

です。

特に月曜日は、

**NQ / US10Y / DXY / VIX / Nvidia・半導体breadth**

をセットで検証します。

NQが下がってもUS10Yが低下していればBUY再評価。

逆に、

**US10Y↑ + DXY↑ + NQ↓**

ならNASDAQ BUY仮説をさらに格下げします。

Goldは**4560周辺を維持できるか**よりも、まず米金利・ドルが反転するかを優先します。

BTCは週末中に**79000を維持できるか、81200を再突破できるか**が主要観測点です。

---

## 9. Obsidian保存用Observation Draft

```markdown
# 2026-08-29 Hawkish Fed Repricing

## Regime
HAWKISH_FED_REPRICING
AI_TREND_INTACT_BUT_RATE_PRESSURED
STRONGER_DOLLAR
HIGHER_YIELDS
WEEKEND_GAP_RISK

## Critical change
Warsh Jackson Hole:
inflation still too high
additional tightening possible

Sep hike probability:
~35% -> ~55-60%

Market reaction:
USD up
Treasury yields up
NASDAQ down
Gold >3% down

## Research lesson
Entry touch != valid entry.

Gold entered prior BUY zone because
the macro driver deteriorated.

Therefore:
PRICE_ENTRY_TOUCH
but
THESIS_QUALITY_DETERIORATED

=> NO_TRADE

## NASDAQ
AI thesis:
ALIVE

Immediate BUY thesis:
PAUSED

Friday Nasdaq:
26402.42
-0.52%

Weekly:
+0.8%

Reactivation:
US10Y stabilizes
NQ holds Friday low
semiconductor breadth improves

## Crypto
BTC:
~80k
Warsh shock relatively well absorbed

ETH:
~2.5k
strong rebound but extended

## Signals
A:
NONE

B+:
BTC BUY

B:
ETH BUY

NO_TRADE:
GOLD
WTI
USDJPY
SPX
NASDAQ
DXY
US10Y
VIX

#TSO #Fed #NASDAQ #GOLD #BTC
```

## 10. TSO_LOG CSV / JSON

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-08-29,20260829_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,31,92,,HAWKISH_FED_GOLD_REPRICING,82,88,93,31,62,86,US10Y_and_DXY_must_stabilize_before_buy_reactivation,GOLD_DXY_US10Y_1d_3d_5d,verified
2026-08-29,20260829_BTC_BUY_PULLBACK,BTC,BUY,B,PULLBACK,77000,79000,73000,85000,89000,1.50,0.61,0.39,97,74,43,0.25,BTC_RESILIENT_HAWKISH_FED,72,88,81,75,76,82,73000_break_or_sustained_hawkish_liquidity_selloff,BTC_79k_81200_85k_ETF_3d_5d,partially_verified
2026-08-29,20260829_ETH_BUY_PULLBACK,ETH,BUY,B,PULLBACK,2380,2460,2160,2800,3000,1.55,0.58,0.35,94,66,52,0.25,ETH_REBOUND_HAWKISH_FED,68,84,82,70,72,78,2160_break_or_ETH_relative_strength_failure,ETH_2460_2500_2800_3d_5d,partially_verified
2026-08-29,20260829_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,25,97,,HORMUZ_NEGOTIATION_HEADLINE_REGIME,75,72,99,25,55,70,durable_Hormuz_flow_normalization_or_disruption_confirmation,WTI_80_85_Hormuz_weekend_headlines,verified
2026-08-29,20260829_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,97,29,97,,HAWKISH_FED_INTERVENTION_CONFLICT,84,88,98,27,61,88,post_intervention_and_rate_differential_confirmation,USDJPY_158_160_DXY_US10Y_intervention,partially_verified
2026-08-29,20260829_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,88,52,76,,HAWKISH_FED_EQUITY_REPRICING,73,75,86,55,68,76,ES_hold_with_yield_stabilization_required,ES_US10Y_VIX_Monday_1d_3d,partially_verified
2026-08-29,20260829_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,93,61,72,,AI_TREND_RATE_PRESSURE_CONFLICT,77,82,91,63,73,80,NQ_hold_and_US10Y_stabilization_required,NQ_US10Y_DXY_VIX_semiconductor_breadth_Monday,partially_verified
2026-08-29,20260829_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,92,42,88,,HAWKISH_FED_DOLLAR_SPIKE,82,85,89,43,71,83,post_spike_consolidation_required,DXY_US10Y_FedWatch_1d_3d,partially_verified
2026-08-29,20260829_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,94,43,90,,HAWKISH_FED_YIELD_REPRICING,88,91,92,41,74,89,yield_consolidation_after_Warsh_required,US10Y_DXY_NQ_Monday_1d_3d,partially_verified
2026-08-29,20260829_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,83,37,84,,WEEKEND_EVENT_VOLATILITY_WATCH,69,67,91,46,64,68,VIX_equity_confirmation_required,VIX_NQ_ES_Monday_1d_3d,partially_verified
```

```json
[
{"date":"2026-08-29","signal_id":"20260829_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":31,"no_trade_score":92,"risk_pct":null,"regime":"HAWKISH_FED_GOLD_REPRICING","ems":82,"ffs":88,"cds":93,"ias":31,"cbs":62,"mes":86,"invalidation":"US10Y_and_DXY_must_stabilize_before_buy_reactivation","verification_target":"GOLD_DXY_US10Y_1d_3d_5d","verified_status":"verified"},
{"date":"2026-08-29","signal_id":"20260829_BTC_BUY_PULLBACK","asset":"BTC","side":"BUY","rank":"B","type":"PULLBACK","entry_low":77000,"entry_high":79000,"sl":73000,"tp1":85000,"tp2":89000,"rr":1.50,"win_prob":0.61,"expected_r":0.39,"tq_score":97,"opp_score":74,"no_trade_score":43,"risk_pct":0.25,"regime":"BTC_RESILIENT_HAWKISH_FED","ems":72,"ffs":88,"cds":81,"ias":75,"cbs":76,"mes":82,"invalidation":"73000_break_or_sustained_hawkish_liquidity_selloff","verification_target":"BTC_79k_81200_85k_ETF_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-29","signal_id":"20260829_ETH_BUY_PULLBACK","asset":"ETH","side":"BUY","rank":"B","type":"PULLBACK","entry_low":2380,"entry_high":2460,"sl":2160,"tp1":2800,"tp2":3000,"rr":1.55,"win_prob":0.58,"expected_r":0.35,"tq_score":94,"opp_score":66,"no_trade_score":52,"risk_pct":0.25,"regime":"ETH_REBOUND_HAWKISH_FED","ems":68,"ffs":84,"cds":82,"ias":70,"cbs":72,"mes":78,"invalidation":"2160_break_or_ETH_relative_strength_failure","verification_target":"ETH_2460_2500_2800_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-29","signal_id":"20260829_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":25,"no_trade_score":97,"risk_pct":null,"regime":"HORMUZ_NEGOTIATION_HEADLINE_REGIME","ems":75,"ffs":72,"cds":99,"ias":25,"cbs":55,"mes":70,"invalidation":"durable_Hormuz_flow_normalization_or_disruption_confirmation","verification_target":"WTI_80_85_Hormuz_weekend_headlines","verified_status":"verified"},
{"date":"2026-08-29","signal_id":"20260829_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":97,"opp_score":29,"no_trade_score":97,"risk_pct":null,"regime":"HAWKISH_FED_INTERVENTION_CONFLICT","ems":84,"ffs":88,"cds":98,"ias":27,"cbs":61,"mes":88,"invalidation":"post_intervention_and_rate_differential_confirmation","verification_target":"USDJPY_158_160_DXY_US10Y_intervention","verified_status":"partially_verified"},
{"date":"2026-08-29","signal_id":"20260829_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":88,"opp_score":52,"no_trade_score":76,"risk_pct":null,"regime":"HAWKISH_FED_EQUITY_REPRICING","ems":73,"ffs":75,"cds":86,"ias":55,"cbs":68,"mes":76,"invalidation":"ES_hold_with_yield_stabilization_required","verification_target":"ES_US10Y_VIX_Monday_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-29","signal_id":"20260829_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":93,"opp_score":61,"no_trade_score":72,"risk_pct":null,"regime":"AI_TREND_RATE_PRESSURE_CONFLICT","ems":77,"ffs":82,"cds":91,"ias":63,"cbs":73,"mes":80,"invalidation":"NQ_hold_and_US10Y_stabilization_required","verification_target":"NQ_US10Y_DXY_VIX_semiconductor_breadth_Monday","verified_status":"partially_verified"},
{"date":"2026-08-29","signal_id":"20260829_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":92,"opp_score":42,"no_trade_score":88,"risk_pct":null,"regime":"HAWKISH_FED_DOLLAR_SPIKE","ems":82,"ffs":85,"cds":89,"ias":43,"cbs":71,"mes":83,"invalidation":"post_spike_consolidation_required","verification_target":"DXY_US10Y_FedWatch_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-29","signal_id":"20260829_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":94,"opp_score":43,"no_trade_score":90,"risk_pct":null,"regime":"HAWKISH_FED_YIELD_REPRICING","ems":88,"ffs":91,"cds":92,"ias":41,"cbs":74,"mes":89,"invalidation":"yield_consolidation_after_Warsh_required","verification_target":"US10Y_DXY_NQ_Monday_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-29","signal_id":"20260829_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":83,"opp_score":37,"no_trade_score":84,"risk_pct":null,"regime":"WEEKEND_EVENT_VOLATILITY_WATCH","ems":69,"ffs":67,"cds":91,"ias":46,"cbs":64,"mes":68,"invalidation":"VIX_equity_confirmation_required","verification_target":"VIX_NQ_ES_Monday_1d_3d","verified_status":"partially_verified"}
]
```

**本日の最重要点はGOLDです。** 昨日のEntry帯到達を機械的なBUY成立と扱わず、**「なぜEntryまで下がったか」を再評価してNO_TRADEへ変更**しました。NASDAQについても同様で、AI強気仮説自体は残しますが、月曜に金利上昇を吸収できることを確認するまでは新規BUYを停止します。BTCだけはWarsh後の相対的な耐性が確認できるため、77000–79000への押しに限ってB+を残します。citeturn2news12turn2news13turn1search3 memcite
