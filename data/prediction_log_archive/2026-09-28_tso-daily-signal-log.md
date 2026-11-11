<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-28 07:00 JST -->
<!-- transport: Codex read_thread; message 289b8765-d20a-45af-8356-640197193cc9; truncated=false -->
<!-- archived_at: 2026-09-28T20:48:54Z / chars: 16644 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-09-28

**使用モデル：GPT-5.6 Sol**  
**本日の市場の主役：BTC**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**データ基準：9月25日米国終値＋9月27日までの週末Crypto。米先物の週初価格形成前なので、GOLD・WTI・SPX・NASDAQ・DXY・US10Y・VIXは金曜値を基準に判定。**

**crypto_grounds: etf=有, cme=有** — 9月21〜25日の米BTC現物ETFは週間約**+2.39Bドル**、7営業日連続流入。ETH ETFも同週約**+689.9Mドル**。BTC現物は週末も約84.3k、ETHは約2695ドルです。:chatgpt-content-reference{index="0"}

**expected_r_basis: subjective** — 新規方向シグナルはありません。既存`20260924_BTC_BUY_PULLBACK`の`expected_r=0.40`は発行時固定。現在は「ETF需要継続」をプラス、「84–85kで価格が伸びないこと」「US10Y 5.17%」「実測MAE過大」をマイナスとして管理します。

**invalidation_check: 20260924_BTC_BUY_PULLBACK=not_fired**

週末BTCの確認安値は概ね**83.16k付近**で、価格invalidationの82500には達していません。またCMEは週末休場で、新しい`CME<83000 + ETF純流出`の複合失効も発生していません。:chatgpt-content-reference{index="1"}

---

## 1. 本日の結論

**新規A級：0件**  
**新規B級：0件**  
**既存B：BTC BUY_PULLBACK — 継続 / not_fired**  
**新規実取引：NO_TRADE**

今日の新しい観察は、BTCの**「フローと価格の乖離」**です。

9月21〜25日のBTC ETF流入は約**23.9億ドル**で、2026年でも突出して強い週でした。それでもBTCは84–85kに滞留し、87k方向へ再加速していません。週末の分析でも、長期保有者の売り供給が84–85k周辺に集中している可能性が指摘されています。:chatgpt-content-reference{index="2"}

これは既存BUYを即否定する材料ではありません。ただし、

**「ETF流入が強いから上がる」**
から、
**「強いETF買いを既存売りが吸収している」**

へ評価を少し変更します。

したがって既存BTCは、

**SL 82500維持**  
**TP1 87400維持**  
**追加BUY禁止**

です。

管理参考win_probは、発行時0.55から**約0.50〜0.51**まで低下させます。

一方、米株は依然かなり強いです。金曜のESZ26は**7803.75、+0.47%**、NQZ26は**30889.25、+0.40%**。特にNQは日足テクニカルがStrong Buyで、RSIは58.5程度ですが短期Stochasticは過熱圏です。方向は上でも、31,000直前を追う位置ではありません。:chatgpt-content-reference{index="3"}

---

## 2. 前回判断の簡易検証

### `20260924_BTC_BUY_PULLBACK`

発行値：

**Entry 83800–84600**  
**Mid 84200**  
**SL 82500**  
**TP1 87400**  
**TP2 90200**  
**RR 1.88**  
**win_prob 0.55**  
**expected_r 0.40**

現状は、

**ENTRY_REACHED  
→ MAE約0.79R  
→ 一時85k台へ回復  
→ 週末84k台へ再停滞  
→ SL_NOT_REACHED  
→ TP1_NOT_REACHED**

です。

BTC現物は現在およそ**84.3k**。週末のETHは約2695ドルです。:chatgpt-content-reference{index="4"}

ETF側はむしろ強化されています。週間BTC ETFフローは約+2.39Bドルで、2026年通年フローも再びプラス圏へ転じたと報じられています。:chatgpt-content-reference{index="5"}

したがって、

**`20260924_BTC_BUY_PULLBACK=not_fired`**

です。

ただし今回の教師データとして重要なのは、

**大量の実需流入 ≠ 即時の価格上昇**

という点です。

今後はETF flowそのものだけでなく、

**ETF流入1ドル当たりの価格反応**
を観察対象にする価値があります。

---

## 3. 市場全体の前提

金曜終値のクロスアセットは、

**株式：強い**  
**VIX：低い**  
**米金利：極端に高い**  
**ドル：一服**  
**原油：低下**  
**Gold：小反発**

という組み合わせです。

ESZ26は**7803.75**、NQZ26は**30889.25**。VIXは**14.87**まで低下しています。つまりUS10Yが約5.17%という非常に高い水準でも、株式市場はまだ本格的なrisk-offになっていません。:chatgpt-content-reference{index="6"}

US10Yは9月25日を**5.17%**で終了。これは引き続きTSO全体の最大マクロ変数です。:chatgpt-content-reference{index="7"}

DXYは**100.97**で、木曜101.29から下落。USDJPYも金曜最終付近は**157.28–157.29**で、前日158.8台からかなり円高へ戻っています。:chatgpt-content-reference{index="8"}

WTIは11月限で**92.41ドル**。米国とイランがHormuz再開を含む段階的な出口を模索しているとの報道で、金曜は約2%下落しました。:chatgpt-content-reference{index="9"}

GOLDはGCZ26で**4321.20ドル**。高金利が重石ですが、4290近辺からは反発しています。:chatgpt-content-reference{index="10"}

今週は**Core PCEと米雇用統計**が重要です。追加利上げ観測が強まった状態なので、雇用・インフレが強ければUS10Y再上昇、弱ければ金利急低下という非対称性があります。:chatgpt-content-reference{index="11"}

総合regimeは**MIXED**です。

---

## 4. 10資産別判断

| 資産 | 判断 | 本日評価 |
|---|---|---|
| **GOLD** | **NO_TRADE** | GCZ26 4321.2。4290支持は確認したが5.17%金利が重い。 |
| **BTC** | **既存B継続 / 新規NO_TRADE** | 約84.3k。ETF流入は極めて強いが価格反応が鈍い。 |
| **ETH** | **NO_TRADE** | 約2695。ETF流入は改善したがBTCよりedgeが弱い。 |
| **WTI** | **NO_TRADE** | 92.41。Hormuz交渉で弱いが地政学反転リスクあり。 |
| **USDJPY** | **NO_TRADE** | 157.28付近。政策上限が効く一方、米金利差は依然大きい。 |
| **SPX** | **NO_TRADE** | ESZ26 7803.75。高金利耐性は強いが金曜反発後。 |
| **NASDAQ** | **NO_TRADE** | NQZ26 30889.25。方向は強いが31k直前＋短期過熱。 |
| **DXY** | **NO_TRADE** | 100.97。上昇モメンタム一服。 |
| **US10Y** | **NO_TRADE** | 5.17%。主役級だが高値追い禁止。 |
| **VIX** | **NO_TRADE** | 14.87。株式risk-offを否定する水準。 |

NQZ26は9月25日のレンジが**30679–30999.5**、終値30889.25。ESZ26は**7748.5–7814.75**、終値7803.75でした。:chatgpt-content-reference{index="12"}

---

## 5. A級候補

**なし。**

最も方向品質が高いのはNASDAQですが、Entry品質が不足しています。

NQZ26のテクニカルはStrong Buyで、

**RSI ≈58.5**  
**MACD Buy**  
**主要MAはすべてBuy**

ですが、StochasticとWilliams %RはOverboughtです。:chatgpt-content-reference{index="13"}

ここで30,900台を成行BUYすると、TSOが避けるべき**高値追随**になります。

現時点では、

**30650–30750までの押し**

を待つ方がよいです。

BTCもAには戻しません。

ETF需要はA級相当でも、**価格反応がA級ではない**ためです。

---

## 6. B級監視候補

**新規Bなし。**

既存のみ。

### `20260924_BTC_BUY_PULLBACK`

**Entry：83800–84600**  
**SL：82500**  
**TP1：87400**  
**TP2：90200**  
**RR：1.88**  
**発行時win_prob：0.55**  
**管理参考win_prob：約0.50–0.51**  
**expected_r：0.40**  
**risk_pct：0.25%**

プラス材料：

- BTC ETF週間+2.39Bドル
- 7営業日連続流入
- 83k台で売り崩れなかった
- CME金曜高値85.7k

マイナス材料：

- これだけETF流入があっても85k突破失敗
- 発行時想定MAE 0.29Rに対し実測約0.79R
- US10Y 5.17%
- 87k付近からの売り供給

したがって、

**既存は維持できるが、新規で同じEntryを追加するほど強くない**

という判断です。

---

## 7. 触らない資産

特に**USDJPY、WTI、US10Y、BTC追加BUY**です。

USDJPYは売り方向が少し魅力的になっていますが、まだ新規SELLを作りません。

金曜に159近辺から157.28まで落ちたので政策上限は機能しています。ただし米10年債が5.17%と極端に高く、金利差自体は依然ドル高要因です。

したがって昨日設定した観察条件を維持します。

**158.5再奪回 → ドル金利差優位**  
**156.5割れ → 円高regime変化候補**

どちらも確認してから次のシグナルを作ります。

WTIも92.41からSELLしません。テクニカルはStrong Sellですが、StochRSIはoversoldに近く、地政学ヘッドライン1本で反転しやすい市場です。:chatgpt-content-reference{index="14"}

---

## 8. 後日検証ポイント

### BTC

最優先です。

**82500 → fired**  
**87400 → TP1**  
**90200 → TP2**

加えて、

**CME <83000**
＋
**ETF純流出**

なら早期invalidation。

ただし今週から、もう1つ観察項目を追加します。

**ETF流入継続なのにBTCが85kを突破できない日数**

です。

これが長引けば、

> strong flow / weak price response

という明確な弱気情報になります。

逆に85kを明確に突破して87.4kへ向かえば、吸収局面が終わったと判断します。

### NASDAQ

金曜値：

**NQZ26 30889.25**

重要水準：

**30650–30750 → BUY_PULLBACK候補**  
**31000超定着 → breakout確認、ただし追わず押し待ち**  
**30300割れ → 高金利耐性仮説を弱める**

特にUS10Yが5.15%以上のままNQが31kを突破するなら、かなり強い市場です。

### SPX

ESZ26：

**7803.75**

**7750–7780を維持**
ならrisk-on継続。

**7700割れ＋VIX>17**
ならrisk-offへ変更。

### USDJPY

**156.5割れ**
ならSELL側の新規仮説を検討できます。

**158.5回復**
なら金利差優位を再確認。

157円台中央ではNO_TRADEです。

### GOLD

GCZ26：

**4321.2**

**4350超**
なら4290–4300支持形成。

**4280割れ**
ならSELL優位。

ただしUS10Yが5.10を割ればGoldの下方向edgeは大きく低下します。

### WTI

**90割れ**
→ Hormuz正常化・供給回復優勢。

**95超**
→ 中東供給プレミアム復活。

92ドル台はまだ中間帯。

---

## 9. Obsidian保存用 Observation Draft

```markdown
# 2026-09-28 BTC Flow/Price Divergence

Model:
GPT-5.6 Sol

Market protagonist:
BTC

Gold reference:
COMEX Dec-2026 / GCZ26

crypto_grounds:
etf=有
cme=有

expected_r_basis:
subjective

## Regime

MIXED

## Weekend state

BTC:
~84300

ETH:
~2695

BTC ETF Sep21-25:
~+2.39bn

ETF streak:
7 positive sessions

ETH ETF weekly:
~+689.9m

Observation:
institutional flow is very strong,
but BTC remains trapped near 84-85k.

Interpretation:
buyer demand is being absorbed by substantial seller supply.

This is not yet invalidation,
but price response quality is deteriorating.

## Active BTC

20260924_BTC_BUY_PULLBACK

Entry:
83800-84600

Mid:
84200

SL:
82500

TP1:
87400

TP2:
90200

RR:
1.88

Issue win_prob:
0.55

Current management estimate:
~0.50-0.51

Issue MAE estimate:
0.29R

Observed MAE:
~0.79R

Status:
ENTRY_REACHED
SL_NOT_REACHED
TP1_NOT_REACHED
not_fired

Do not add.
Do not widen SL.

Time exit:
Sep30

## Friday macro references

GCZ26:
4321.20

WTI:
92.41

USDJPY:
157.28

ESZ26:
7803.75

NQZ26:
30889.25

DXY:
100.97

US10Y:
5.17%

VIX:
14.87

## Equity observation

Despite US10Y >5.1%:

ES:
strong

NQ:
strong

VIX:
below 15

High-rate resilience remains intact.

NQ technical:
daily Strong Buy

But:
short-term stochastic overbought

Preferred next entry:
30650-30750 pullback

Do not chase 31000.

## USDJPY

Friday:
~159 -> 157.28

Policy ceiling remains relevant.

No new signal inside middle zone.

Tests:
<156.5 = yen-strength regime candidate
>158.5 = yield differential regains control

## WTI

92.41

US-Iran talks:
bearish oil

Houthi / Saudi risk:
bullish tail

Technical:
Strong Sell
but short-term oversold characteristics

NO_TRADE

## Week ahead

Core PCE
US payrolls
multiple Fed speakers

Main causal chain:

jobs / inflation
-> Fed hike probability
-> US10Y
-> DXY
-> NQ / SPX
-> BTC / Gold

## Active invalidation

20260924_BTC_BUY_PULLBACK=not_fired

## New signals

A:
NONE

B:
NONE

Existing:
BTC BUY_PULLBACK active

#TSO #BTC #US10Y #NASDAQ #USDJPY #WTI #GOLD
```

---

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-28,20260928_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,86,89,,MIXED,84,93,97,83,84,94,wait_for_GCZ26_reclaim_4350_or_break_4280_with_US10Y_confirmation,GCZ26_4280_4321.2_4350_US10Y_DXY_1d_3d,verified
2026-09-28,20260928_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,96,64,,MIXED,86,95,98,93,89,95,manage_existing_20260924_BUY_SL82500_TP87400_not_fired_no_add_monitor_flow_price_divergence,BTC_82500_83160_84300_85000_87400_ETF_CME_1d_3d_5d,partially_verified
2026-09-28,20260928_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,86,86,,MIXED,79,91,96,84,83,90,prefer_existing_BTC_expression_wait_for_ETH_reclaim_2750_or_failure_below_2630,ETH_2630_2695_2750_ETF_CME_1d_3d,partially_verified
2026-09-28,20260928_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,94,95,,EVENT,95,99,99,92,92,98,wait_for_WTI_break_below_90_or_reclaim_above_95_after_Hormuz_negotiations,WTI_Nov26_90_92.41_95_USIran_Hormuz_Houthi_1d_3d,verified
2026-09-28,20260928_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,95,93,,EVENT,94,98,99,94,91,98,wait_for_USDJPY_break_below_156.5_or_reclaim_above_158.5_before_new_direction_signal,USDJPY_156.5_157.28_158.5_159_MOF_US10Y_1d_3d,verified
2026-09-28,20260928_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,93,83,,RISK_ON,85,94,98,90,89,96,wait_for_ES_pullback_7750_7780_or_failure_below_7700_with_VIX_confirmation,ESZ26_7700_7748.5_7750_7780_7803.75_7814.75_US10Y_VIX_1d_3d,verified
2026-09-28,20260928_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,97,82,,RISK_ON,89,96,98,95,94,97,do_not_chase_31000_wait_for_NQ_pullback_30650_30750_or_failure_below_30300,NQZ26_30300_30650_30679_30750_30889.25_31000_US10Y_VIX_1d_3d,verified
2026-09-28,20260928_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,88,89,,MIXED,85,94,97,85,85,95,wait_for_DXY_reclaim_101.3_or_break_below_100.7_with_US10Y_confirmation,DXY_100.7_100.97_101.3_US10Y_USDJPY_1d_3d,verified
2026-09-28,20260928_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,98,95,,EVENT,99,99,99,97,97,99,wait_for_US10Y_break_above_5.25_or_rejection_below_5.10_after_US_data,US10Y_5.10_5.17_5.25_PCE_payrolls_NQ_GOLD_DXY_1d_3d,verified
2026-09-28,20260928_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,81,89,,RISK_ON,71,88,95,76,77,85,wait_for_VIX_reclaim_above_16.5_or_hold_below_14.5_with_ES_NQ_confirmation,VIX_14.5_14.87_16.5_ES_NQ_US10Y_1d_3d,verified
```

### TSO_LOG JSON

```json
[
  {"date":"2026-09-28","signal_id":"20260928_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":86,"no_trade_score":89,"risk_pct":null,"regime":"MIXED","ems":84,"ffs":93,"cds":97,"ias":83,"cbs":84,"mes":94,"invalidation":"wait_for_GCZ26_reclaim_4350_or_break_4280_with_US10Y_confirmation","verification_target":"GCZ26_4280_4321.2_4350_US10Y_DXY_1d_3d","verified_status":"verified"},
  {"date":"2026-09-28","signal_id":"20260928_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":96,"no_trade_score":64,"risk_pct":null,"regime":"MIXED","ems":86,"ffs":95,"cds":98,"ias":93,"cbs":89,"mes":95,"invalidation":"manage_existing_20260924_BUY_SL82500_TP87400_not_fired_no_add_monitor_flow_price_divergence","verification_target":"BTC_82500_83160_84300_85000_87400_ETF_CME_1d_3d_5d","verified_status":"partially_verified"},
  {"date":"2026-09-28","signal_id":"20260928_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":86,"no_trade_score":86,"risk_pct":null,"regime":"MIXED","ems":79,"ffs":91,"cds":96,"ias":84,"cbs":83,"mes":90,"invalidation":"prefer_existing_BTC_expression_wait_for_ETH_reclaim_2750_or_failure_below_2630","verification_target":"ETH_2630_2695_2750_ETF_CME_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-28","signal_id":"20260928_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":94,"no_trade_score":95,"risk_pct":null,"regime":"EVENT","ems":95,"ffs":99,"cds":99,"ias":92,"cbs":92,"mes":98,"invalidation":"wait_for_WTI_break_below_90_or_reclaim_above_95_after_Hormuz_negotiations","verification_target":"WTI_Nov26_90_92.41_95_USIran_Hormuz_Houthi_1d_3d","verified_status":"verified"},
  {"date":"2026-09-28","signal_id":"20260928_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":95,"no_trade_score":93,"risk_pct":null,"regime":"EVENT","ems":94,"ffs":98,"cds":99,"ias":94,"cbs":91,"mes":98,"invalidation":"wait_for_USDJPY_break_below_156.5_or_reclaim_above_158.5_before_new_direction_signal","verification_target":"USDJPY_156.5_157.28_158.5_159_MOF_US10Y_1d_3d","verified_status":"verified"},
  {"date":"2026-09-28","signal_id":"20260928_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":93,"no_trade_score":83,"risk_pct":null,"regime":"RISK_ON","ems":85,"ffs":94,"cds":98,"ias":90,"cbs":89,"mes":96,"invalidation":"wait_for_ES_pullback_7750_7780_or_failure_below_7700_with_VIX_confirmation","verification_target":"ESZ26_7700_7748.5_7750_7780_7803.75_7814.75_US10Y_VIX_1d_3d","verified_status":"verified"},
  {"date":"2026-09-28","signal_id":"20260928_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":97,"no_trade_score":82,"risk_pct":null,"regime":"RISK_ON","ems":89,"ffs":96,"cds":98,"ias":95,"cbs":94,"mes":97,"invalidation":"do_not_chase_31000_wait_for_NQ_pullback_30650_30750_or_failure_below_30300","verification_target":"NQZ26_30300_30650_30679_30750_30889.25_31000_US10Y_VIX_1d_3d","verified_status":"verified"},
  {"date":"2026-09-28","signal_id":"20260928_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":88,"no_trade_score":89,"risk_pct":null,"regime":"MIXED","ems":85,"ffs":94,"cds":97,"ias":85,"cbs":85,"mes":95,"invalidation":"wait_for_DXY_reclaim_101.3_or_break_below_100.7_with_US10Y_confirmation","verification_target":"DXY_100.7_100.97_101.3_US10Y_USDJPY_1d_3d","verified_status":"verified"},
  {"date":"2026-09-28","signal_id":"20260928_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":98,"no_trade_score":95,"risk_pct":null,"regime":"EVENT","ems":99,"ffs":99,"cds":99,"ias":97,"cbs":97,"mes":99,"invalidation":"wait_for_US10Y_break_above_5.25_or_rejection_below_5.10_after_US_data","verification_target":"US10Y_5.10_5.17_5.25_PCE_payrolls_NQ_GOLD_DXY_1d_3d","verified_status":"verified"},
  {"date":"2026-09-28","signal_id":"20260928_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":81,"no_trade_score":89,"risk_pct":null,"regime":"RISK_ON","ems":71,"ffs":88,"cds":95,"ias":76,"cbs":77,"mes":85,"invalidation":"wait_for_VIX_reclaim_above_16.5_or_hold_below_14.5_with_ES_NQ_confirmation","verification_target":"VIX_14.5_14.87_16.5_ES_NQ_US10Y_1d_3d","verified_status":"verified"}
]
```

本日の更新で最も重要なのは、**BTCのETF需要がさらに強いことが確認されたのに、価格が84–85kで停滞していること**です。これは既存BUYを切る理由にはまだなりませんが、追加BUYを止めるには十分な情報です。

もう一つは、**US10Yが5.17%でもES/NQが高値圏を維持していること**です。週初にNQが30650–30750へ押して耐えるなら、次に新しい方向シグナルを作る候補はNASDAQが最有力です。
