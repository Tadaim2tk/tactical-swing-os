<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-10-07 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-10-13T20:23:35Z / chars: 18246 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-10-07

**使用モデル：GPT-5.6 Sol**  
**本日の市場の主役：US10Y**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**データ基準：2026年10月6日米国市場終了後。ES/NQはCME 2026年12月限、BTC/ETHは現物＋CME先物を使用。**

**crypto_grounds: etf=有, cme=有** — BTC ETFは10月5日に**-89.8Mドル**へ流出転換。ETHも流出継続で、10月6日分は今朝時点でFarside未確定です。CMEはBTC約85.8k、ETH約2.70kまで確認できています。citeturn624862view6turn973518search2turn436912search1turn522215search0

**expected_r_basis: subjective** — 本日の新規方向シグナルは0件。既存`20261006_WTI_SELL_PULLBACK`の`expected_r=0.34`は発行時固定で、5営業日時間決済・未約定確率・地政学invalidationを織り込んだsubjective値です。

**invalidation_check: 20261006_WTI_SELL_PULLBACK=not_fired**

---

## 1. 本日の結論

**新規A級：0件**  
**新規B級：0件**  
**未決着方向判断：1件 — WTI SELL_PULLBACK**  
**本日の新規実取引：NO_TRADE**

昨日の市場は、米10年債利回りが約**5.31%→5.27%**へ低下したことで株式がさらに上昇し、S&P500とNASDAQがともに最高値を更新しました。S&P500は**7818.93、+0.58%**、Nasdaq Compositeは**27599.79、+0.45%**。一方でRussell 2000は下落しており、依然として大型AI・メガキャップへの集中度が高い上昇です。citeturn624862view2turn723276news52turn453633news38

ESZ26は**7878.50**、NQZ26は**31540.75**まで上昇しました。どちらも高値圏で、ここからの成行追随はTSOルール上行いません。citeturn159609search5turn361879search8

GoldはGCZ26が**4187.10ドル**まで反発。米長期金利とドルの一服を素直に好感しました。citeturn624862view3

最大の検証対象だったWTIは**89.44ドル**でほぼ横ばい。ただし日中は**90.04→86.88**という大きなレンジでした。昨日のSELL Entry下限90.20には届かず、そのままTP1の87.20を一時下回っています。citeturn624862view1turn159609search7

つまり昨日のWTIは、

**方向仮説：かなり良かった**  
**注文設計：約定せず**

という結果です。

また本日は米国時間10月7日に**FOMC議事要旨**が公表されます。Fed公式カレンダーでは14:00 ET、つまり日本時間では**10月8日03:00**です。長期金利・DXY・NASDAQ・Goldへのイベントリスクが大きいため、新規シグナルを作る日ではありません。citeturn955132search0turn955132search1

---

## 2. 前回判断の簡易検証

### `20261006_WTI_SELL_PULLBACK`

発行条件：

**Entry：90.20–90.80**  
**Mid：90.50**  
**SL：92.00**  
**TP1：87.20**  
**TP2：84.80**  
**RR：2.20**  
**win_prob：0.52**  
**expected_r：0.34**

10月6日のWTIはデータ系列で、

**Open：89.18**  
**High：90.04**  
**Low：86.88**  
**Settle：約89.44**

でした。citeturn624862view1turn159609search7

したがって、

**ENTRY_NOT_REACHED**  
**TP1_PRICE_REACHED_BEFORE_ENTRY**  
**SL_NOT_REACHED**  
**invalidation=not_fired**

です。

これは研究上かなり重要です。

売り方向は正しく、実際にTP1より安い86.88まで下落しました。しかしEntryを90.20以上に限定したため、**0.16ドル差で約定せず**でした。

ここでEntryを後付けで89台へ下げることはしません。

一方、価格がすでにTP1まで一度走ったあとに、昨日の指値を無条件で置き続けるのも好ましくありません。

したがって実運用では、

**旧シグナルのinvalidation追跡は継続**
しつつ、

**90.20–90.80へ再度戻った場合は、その時点の供給材料を再評価してから参加**

とします。

古い指値の盲目的な放置はしません。

---

### NASDAQ

昨日は、

**NQ約31300**
で

**「強いが追わない」**

でした。

10月6日のNQZ26は、

**Open 31339.00  
High 31614.50  
Low 31310.50  
Close 31540.75**

となりました。citeturn361879search8

方向判断としては完全に上でした。

一方、押し目を待つ方針だったため約定機会なし。

これは「方向を当てたが取引しなかった」ケースとして記録します。

---

### BTC

BTCは再び**87,000ドルで拒否**されました。

CoinDeskでも、9月23日以降3回目となる87k付近の上値拒否が確認されています。BTCは約85.6kへ戻りました。citeturn624862view5

さらに10月5日の米BTC ETFは**-89.8Mドル**へ純流出転換。10月1日+102.7M、10月2日+189.9Mから再び悪化しました。citeturn624862view6

したがって、

**87k resistance**
＋
**ETF flow deterioration**

が一致しています。

昨日のNO_TRADEを維持します。

---

## 3. 市場全体の前提

本日の総合regimeは**MIXED**です。

株式だけ見ると明確なRISK_ONです。

ESZ26：

**7878.50**
**+0.67%**

NQZ26：

**31540.75**
**+0.71%**。citeturn159609search5turn361879search8

VIXも約**15.3**まで低下しています。ただし取得元によって15.0台前半に若干の差があるため`partially_verified`とします。citeturn972156search0turn972156search1

しかし小型株やBTCが参加しておらず、広範なrisk-onとは言いにくい状態です。citeturn453633news38

債券は一旦落ち着きました。

米10年債利回りは約**5.269%**。前日の5.31%から低下していますが、依然として極端に高い水準です。citeturn723276news49

DXYも、

**102.17 → 101.85**

へ低下。citeturn159609search0

この

**US10Y↓**
＋
**DXY↓**

がGold・NASDAQを支えました。

Gold Decemberは**4187.10ドル、+0.7%**。citeturn624862view3

USDJPYは逆にあまり下がらず、

**158.14**

で終了。日中レンジは157.77–158.25でした。citeturn159609search1

つまり円は、

**ドル安・米金利低下に対して反応が鈍い**

状態です。

介入警戒モジュールの観点ではまだ159–160の警戒帯には入っていませんが、通常のUSDJPY BUYを積極的に追う水準でもありません。

---

## 4. 10資産別判断

| 資産 | 本日判断 | 評価 |
|---|---|---|
| **GOLD** | **NO_TRADE** | GCZ26 4187.1。反発したがFOMC議事要旨前。 |
| **BTC** | **NO_TRADE** | 約85.6k。87kで3度目の拒否＋ETF流出。 |
| **ETH** | **NO_TRADE** | 約2690、CME約2700。ETF流出継続。 |
| **WTI** | **既存B監視 / 新規NO_TRADE** | 89.44。昨日Entry未到達のまま86.88まで下落。 |
| **USDJPY** | **NO_TRADE** | 158.14。金利低下でも円高反応鈍いが政策テールあり。 |
| **SPX** | **NO_TRADE** | ESZ26 7878.5。史上最高値圏、追随禁止。 |
| **NASDAQ** | **NO_TRADE** | NQZ26 31540.75。最強資産だが高値追い不可。 |
| **DXY** | **NO_TRADE** | 101.85。前日から低下、FOMC待ち。 |
| **US10Y** | **NO_TRADE** | 5.269%。高値から反落したがイベント直前。 |
| **VIX** | **NO_TRADE** | 約15.3。低ボラだが大型株集中との乖離あり。 |

BTC CMEの10月6日は**85827**、高値87030、安値85345。ETH CMEは概ね**2700前後**でした。citeturn436912search1turn522215search0

---

## 5. A級候補

**なし。**

最も強いのはNASDAQです。

ただしNQは2営業日で、

**31061 → 31318 → 31541**

まで上昇しています。citeturn361879search8

ここでA級BUYを作ると、

**方向性は良いがEntry品質が悪い**

という典型になります。

次のBUY候補帯を、

**31200–31300**

へ上方更新します。

ただし条件は、

**US10Y <=5.20**
＋
**VIX <=15.5**

です。

この条件なら、

**価格構造は上昇維持**
＋
**discount rate shock低下**

の両方が揃います。

---

## 6. B級監視候補

### 既存 `20261006_WTI_SELL_PULLBACK`

正式にはまだ**not_fired**です。

ただし本日は新規発注を推奨しません。

昨日、

**Entry下限90.20**
に対して
**High 90.04**

だったため未約定。

その後、

**Low 86.88**

でTP1 87.20を下回りました。citeturn159609search7

つまりedgeの大半を一度消化しています。

今後90.20–90.80へ戻った場合、

**「昨日の注文だから売る」**

ではなく、

- 中東輸出量
- G7備蓄放出
- Gulf cyclone
- Houthi攻撃
- EIA在庫

を再確認して、新しいSELL_PULLBACKとして評価し直します。

WTIは現在、約1200万bpdの中東原油と約200万bpdの製品輸出が再開している一方、Houthi攻撃とメキシコ湾サイクロンリスクが残っています。citeturn624862view1

---

## 7. 触らない資産

特に**NASDAQ、US10Y、USDJPY**です。

NASDAQは最も強いですが、

**「強い＝今買う」**

ではありません。

株価指数が最高値を更新する一方、Russell 2000やBTCが付いてきていないため、現在の上昇は完全な市場全体risk-onというより、**大型AI・メガキャップ集中型**です。citeturn453633news38

US10Yは本日、

**10年債入札**
＋
**FOMC議事要旨**

というイベントが重なります。Fed公式では議事要旨は米国時間10月7日14:00です。citeturn955132search0turn723276search2

USDJPYは158円台。

金利差からはBUY方向ですが、158後半から159台になると介入risk/rewardが悪化します。

通常のmomentum BUYと、現在研究中のIntervention Shock Moduleは引き続き分離します。

---

## 8. 後日検証ポイント

### WTI

`20261006_WTI_SELL_PULLBACK`

**invalidation：not_fired**

ただし、

**Entry未到達**
＋
**TP1先行到達**

という特殊ケース。

これは今後TSOで、

**target_before_entry**

という検証ラベルを追加する価値があります。

今回のケースでは、

> シグナル方向は正しい  
> Entry帯が深すぎて約定しない

という問題を分離できます。

### NASDAQ

NQZ26：

**31540.75**

次の重要帯：

**31200–31300**
→ BUY_PULLBACK候補。

**31000割れ**
→ breakout momentum減速。

**31600–31700をそのまま突破**
→ 強いが追わない。

特にFOMC議事要旨後、

**US10Y<5.20**
なのに
**NQ>31300**

ならA級BUY候補にかなり近づきます。

### SPX

ESZ26：

**7878.50**

観察：

**7850**
→ 最初の支持。

**7800–7820**
→ より良いBUY_PULLBACK候補。

**7900突破**
でも成行追随なし。

### GOLD

GCZ26：

**4187.10**

昨日までのSELL候補帯4190–4210へほぼ到達しました。

しかし条件だった

**US10Y >5.25**

は満たしている一方、

**DXY >102**

は失敗しています。

さらにFOMC議事要旨直前。

したがってSELLは作りません。

次は、

**4210–4230**
＋
**US10Y再上昇**

ならSELL再評価。

逆に、

**4230超**
＋
**US10Y<5.15**

ならBUY側へ切り替えます。

### BTC

現物：

**約85600**

87kは明確な壁になっています。citeturn624862view5

今後のBUY条件をさらに厳格化します。

**BTC >87500**
＋
**CME >87500**
＋
**ETF flow >0**

です。

10月5日のETFが-89.8Mなので、現在は条件不成立です。citeturn624862view6

**84500割れ**
ならtriangle下側を警戒。

### ETH

現物約2690、CME約2700。

最新ETFは流出継続。

**2750–2800回復**
＋
**ETF純流入転換**

まではNO_TRADEです。

### USDJPY

**158.14**

次の介入警戒閾値：

**159**
＋
**1時間上昇速度加速**

で通常BUY評価を下げます。

**160前後**
では通常momentum BUYを原則停止。

### US10Y

**5.269%**

本日の最重要分岐：

**5.35超**
→ bond selloff再開。

**5.20割れ**
→ NASDAQ/GOLDのEntry品質改善。

**5.15割れ**
→ 先週からの長期金利shockがピークアウトした可能性。

---

## 9. Obsidian保存用 Observation Draft

```markdown
# 2026-10-07 WTI Target-Before-Entry / Equity Records / FOMC Minutes Ahead

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

## US equities

ESZ26:
7878.50
+0.67%

NQZ26:
31540.75
+0.71%

S&P500 cash:
7818.93
record

Nasdaq Composite:
27599.79
record

Russell 2000:
down

Interpretation:

large-cap / AI-led risk-on
not broad risk-on.

## Rates

US10Y:
~5.269%

Previous:
~5.31%

Bond yield relief
supported Gold and equities.

But yield remains historically extreme.

## Event risk

Oct7 US time:
FOMC minutes

Release:
14:00 ET
03:00 JST Oct8

Also:
10Y Treasury auction

No new directional trade
before rates event.

## Gold

GCZ26:
4187.10

+0.7%

Previous SELL observation:
4190-4210

Conditions:
US10Y >5.25 = YES
DXY >102 = NO

Therefore:
NO_TRADE

Watch:
4210-4230 with yields rising
or
4230 breakout with US10Y <5.15

## Crypto

BTC spot:
~85600

BTC CME:
85827
high 87030
low 85345

BTC:
third rejection near 87000

BTC ETF Oct5:
-89.8m

Oct6 ETF:
not finalized

ETH spot:
~2690

ETH CME:
~2700

ETH ETF:
outflow trend persists

Interpretation:

equity risk-on is not transmitting
to crypto.

No new signal.

## WTI existing signal

20261006_WTI_SELL_PULLBACK

Entry:
90.20-90.80

SL:
92.00

TP1:
87.20

TP2:
84.80

Oct6:
high 90.04
low 86.88
settle ~89.44

Result:
ENTRY_NOT_REACHED
TP1_PRICE_REACHED_BEFORE_ENTRY
not_fired

Research note:

direction thesis was correct
but entry placement missed trade by 0.16.

Candidate future label:
target_before_entry

Do not lower entry retroactively.

If price returns to prior Entry zone:
re-evaluate fundamentals before execution.

## USDJPY

158.14

No Intervention Shock trigger.

159:
raise intervention awareness

160:
normal momentum BUY disabled

## Active invalidation

20261006_WTI_SELL_PULLBACK=not_fired

## New signals

A:
NONE

B:
NONE

#TSO #US10Y #NASDAQ #WTI #BTC #GOLD #USDJPY
```

---

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-10-07,20261007_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,94,78,,MIXED,88,95,98,91,90,96,wait_for_GCZ26_4210_4230_response_to_US10Y_and_FOMC_or_reclaim_4230_with_US10Y_below_5.15,GCZ26_4150_4187.10_4210_4230_US10Y_DXY_FOMC_1d_3d,verified
2026-10-07,20261007_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,94,86,,MIXED,82,94,98,89,86,88,third_87000_rejection_and_ETF_outflow_wait_for_87500_hold_with_CME_and_positive_ETF_flow,BTC_84500_85600_87000_87500_CME_ETF_1d_3d,partially_verified
2026-10-07,20261007_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,82,91,,MIXED,74,90,96,80,78,82,wait_for_ETH_reclaim_2750_2800_with_ETF_inflow_and_BTC_confirmation_or_break_below_2630,ETH_2630_2690_2750_2800_CME_ETF_1d_3d,partially_verified
2026-10-07,20261007_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,96,58,,EVENT,61,94,97,86,78,95,existing_20261006_SELL_not_fired_but_target_before_entry_requires_revalidation_before_any_future_execution,WTI_86.88_87.20_89.44_90.04_90.20_92.00_EIA_G7_Hormuz_1d_3d_5d,verified
2026-10-07,20261007_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,93,92,,EVENT,92,98,99,94,91,98,avoid_normal_momentum_buy_as_price_approaches_159_160_intervention_sensitive_zone,USDJPY_157.77_158.14_159_160_US10Y_DXY_MOF_intervention_1d_3d,verified
2026-10-07,20261007_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,98,66,,RISK_ON,90,95,97,95,94,95,do_not_chase_record_high_wait_for_ES_pullback_7800_7820_or_7850_support_after_rates_event,ESZ26_7800_7820_7850_7878.50_7900_US10Y_VIX_FOMC_1d_3d,verified
2026-10-07,20261007_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,99,64,,RISK_ON,92,96,98,97,96,97,do_not_chase_record_high_wait_for_NQ_pullback_31200_31300_with_US10Y_below_5.20,NQZ26_31000_31200_31300_31540.75_31600_US10Y_VIX_FOMC_1d_3d,verified
2026-10-07,20261007_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,91,85,,MIXED,85,94,97,87,85,94,wait_for_post_FOMC_DXY_break_above_102.3_or_failure_below_101.5_with_US10Y_confirmation,DXY_101.5_101.85_102.3_US10Y_USDJPY_FOMC_1d_3d,verified
2026-10-07,20261007_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,99,96,,EVENT,99,99,99,99,99,99,major_event_risk_wait_for_10Y_auction_and_FOMC_minutes_break_above_5.35_or_below_5.20,US10Y_5.15_5.20_5.269_5.35_FOMC_10Y_auction_NQ_GOLD_1d_3d,verified
2026-10-07,20261007_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,88,82,,RISK_ON,80,92,96,83,82,90,wait_for_VIX_hold_below_15_or_reclaim_above_17_with_ES_NQ_and_rates_confirmation,VIX_15_15.3_17_ES_NQ_US10Y_FOMC_1d_3d,partially_verified
```

### TSO_LOG JSON

```json
[
  {"date":"2026-10-07","signal_id":"20261007_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":94,"no_trade_score":78,"risk_pct":null,"regime":"MIXED","ems":88,"ffs":95,"cds":98,"ias":91,"cbs":90,"mes":96,"invalidation":"wait_for_GCZ26_4210_4230_response_to_US10Y_and_FOMC_or_reclaim_4230_with_US10Y_below_5.15","verification_target":"GCZ26_4150_4187.10_4210_4230_US10Y_DXY_FOMC_1d_3d","verified_status":"verified"},
  {"date":"2026-10-07","signal_id":"20261007_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":94,"no_trade_score":86,"risk_pct":null,"regime":"MIXED","ems":82,"ffs":94,"cds":98,"ias":89,"cbs":86,"mes":88,"invalidation":"third_87000_rejection_and_ETF_outflow_wait_for_87500_hold_with_CME_and_positive_ETF_flow","verification_target":"BTC_84500_85600_87000_87500_CME_ETF_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-10-07","signal_id":"20261007_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":82,"no_trade_score":91,"risk_pct":null,"regime":"MIXED","ems":74,"ffs":90,"cds":96,"ias":80,"cbs":78,"mes":82,"invalidation":"wait_for_ETH_reclaim_2750_2800_with_ETF_inflow_and_BTC_confirmation_or_break_below_2630","verification_target":"ETH_2630_2690_2750_2800_CME_ETF_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-10-07","signal_id":"20261007_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":96,"no_trade_score":58,"risk_pct":null,"regime":"EVENT","ems":61,"ffs":94,"cds":97,"ias":86,"cbs":78,"mes":95,"invalidation":"existing_20261006_SELL_not_fired_but_target_before_entry_requires_revalidation_before_any_future_execution","verification_target":"WTI_86.88_87.20_89.44_90.04_90.20_92.00_EIA_G7_Hormuz_1d_3d_5d","verified_status":"verified"},
  {"date":"2026-10-07","signal_id":"20261007_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":93,"no_trade_score":92,"risk_pct":null,"regime":"EVENT","ems":92,"ffs":98,"cds":99,"ias":94,"cbs":91,"mes":98,"invalidation":"avoid_normal_momentum_buy_as_price_approaches_159_160_intervention_sensitive_zone","verification_target":"USDJPY_157.77_158.14_159_160_US10Y_DXY_MOF_intervention_1d_3d","verified_status":"verified"},
  {"date":"2026-10-07","signal_id":"20261007_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":98,"no_trade_score":66,"risk_pct":null,"regime":"RISK_ON","ems":90,"ffs":95,"cds":97,"ias":95,"cbs":94,"mes":95,"invalidation":"do_not_chase_record_high_wait_for_ES_pullback_7800_7820_or_7850_support_after_rates_event","verification_target":"ESZ26_7800_7820_7850_7878.50_7900_US10Y_VIX_FOMC_1d_3d","verified_status":"verified"},
  {"date":"2026-10-07","signal_id":"20261007_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":99,"no_trade_score":64,"risk_pct":null,"regime":"RISK_ON","ems":92,"ffs":96,"cds":98,"ias":97,"cbs":96,"mes":97,"invalidation":"do_not_chase_record_high_wait_for_NQ_pullback_31200_31300_with_US10Y_below_5.20","verification_target":"NQZ26_31000_31200_31300_31540.75_31600_US10Y_VIX_FOMC_1d_3d","verified_status":"verified"},
  {"date":"2026-10-07","signal_id":"20261007_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":91,"no_trade_score":85,"risk_pct":null,"regime":"MIXED","ems":85,"ffs":94,"cds":97,"ias":87,"cbs":85,"mes":94,"invalidation":"wait_for_post_FOMC_DXY_break_above_102.3_or_failure_below_101.5_with_US10Y_confirmation","verification_target":"DXY_101.5_101.85_102.3_US10Y_USDJPY_FOMC_1d_3d","verified_status":"verified"},
  {"date":"2026-10-07","signal_id":"20261007_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":99,"no_trade_score":96,"risk_pct":null,"regime":"EVENT","ems":99,"ffs":99,"cds":99,"ias":99,"cbs":99,"mes":99,"invalidation":"major_event_risk_wait_for_10Y_auction_and_FOMC_minutes_break_above_5.35_or_below_5.20","verification_target":"US10Y_5.15_5.20_5.269_5.35_FOMC_10Y_auction_NQ_GOLD_1d_3d","verified_status":"verified"},
  {"date":"2026-10-07","signal_id":"20261007_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":88,"no_trade_score":82,"risk_pct":null,"regime":"RISK_ON","ems":80,"ffs":92,"cds":96,"ias":83,"cbs":82,"mes":90,"invalidation":"wait_for_VIX_hold_below_15_or_reclaim_above_17_with_ES_NQ_and_rates_confirmation","verification_target":"VIX_15_15.3_17_ES_NQ_US10Y_FOMC_1d_3d","verified_status":"partially_verified"}
]
```

本日の研究上の最大の収穫はWTIです。**方向判断は合っていたのに、Entryが0.16ドル届かず、その後TP1を先に通過した**というケースになりました。これは勝敗ではなく、Entry設計の較正に使えるデータです。今後TSO_LOG28列は変えず、Observation側で`target_before_entry`を記録しておく価値があります。

一方、NASDAQは最高値更新を続けていますが、BTC・小型株が追随していません。今夜の10年債入札とFOMC議事要旨後に**US10Yが5.20%を割ってもNQが31300以上を維持するか**が、次のA級BUY候補を作るうえで最も重要な確認になります。
