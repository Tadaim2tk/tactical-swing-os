<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-08-14 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 17172 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026年8月14日

データ基準は**8月13日米国市場終了後～8月14日07:00 JST前後**。10資産すべて新規取得を試み、ES/NQは先物系列を直接確認しました。NASDAQ総合やQQQをNASDAQ行の価格へ代用していません。

7月PPIは**前月比0.0%**で市場予想+0.2%を下回り、前年比も+4.7%へ鈍化。これを受け、米10年債利回りは4.645%付近へ低下しました。WTIも81.25まで-2.4%。S&P500は7798.99で史上最高値、NASDAQ総合も+0.81%。ES9月限は7835付近、NQ9月限は30214付近まで上昇しました。citeturn537619news70turn511537news18turn846628search0turn846628search13

**本日はNASDAQをA級へ昇格します。** ただし本日も米小売売上高・ミシガン消費者信頼感などが控えるため、A級でもリスクは0.25%に抑えます。今週金曜に小売売上高と消費者信頼感が予定されていることが確認されています。citeturn646580news17

---

## 1. 本日の結論

**A級：NASDAQ BUY PULLBACK 1件。**

**B級：SPX BUY、GOLD BUY。**

**NO_TRADE：BTC、ETH、WTI、USDJPY、DXY、US10Y、VIX。**

本日の優先順位は、

**NASDAQ A > SPX B > GOLD B**

です。

PPI通過によって昨日までNASDAQのA昇格を妨げていた主要イベントリスクが一つ消えました。PPIは予想を下回り、10年金利低下、原油下落、VIX低位、NQ上昇が同時成立しています。citeturn537619news70turn511537news18turn846628news37turn511537search4

これは8月4日のNASDAQ A級とかなり近い、

**AI/Growth strength  
＋ inflation pressure easing  
＋ yields down  
＋ oil down  
＋ volatility low**

という構造です。

ただしNQはすでに30200台。

**A判定＝30200台を成行で買う、ではありません。**

押し目のみです。

---

# 2. 前回判断の簡易検証

### NASDAQ B BUY → **方向成功 / NO_FILL**

昨日Entry：

**29450–29700**

8月13日のNQ9月限は、

**Open 29825  
Low 29780.50  
High 30272.75  
Close付近 30214.25**

でした。citeturn846628search13

安値29780.50なので、昨日のEntry上限29700へ**約80ポイント届いていません**。

したがって、

**DIRECTION_SUCCESS  
NO_FILL**

です。

これは重要です。

今回もまた、

> 方向は合っているが、押し目が浅くEntry未到達

になりました。

それでも成行追随ルールへはまだ変更しません。

---

### SPX B BUY → **FILL可能性高 / 方向成功**

昨日ES Entry：

**7730–7770**

ES9月限は、

**Open 7770  
Low 7764.25  
High 7838.50  
Close付近 7835**

でした。citeturn846628search0turn846628search12

これは参照系列上、**Entry帯に実際に入っています**。

したがって暫定的に、

**ENTRY_REACHED  
DIRECTION_SUCCESS**

と判定します。

Entry帯上限7760～7770近辺からなら、その後7830台まで順行したため、昨日のSPX Bは良いシグナルでした。

---

### GOLD B BUY → **Entry到達 / 短期方向失敗**

昨日Entry：

**4410–4450**

Reutersでは米金先物が**4420.40**で決済、-1.1%。現物金も4350.72付近まで下落しました。citeturn511537news18

したがってEntry帯には入った一方、その後の値動きはBUY方向に反しました。

**ENTRY_REACHED  
1D_DIRECTION_FAIL  
SL_NOT_REACHED**

とします。

ただしCOMEXの限月によって決済値に差があり、別データでは8月限4363.60との値も確認できます。citeturn846628news40

そのためGOLDの価格レベルについては本日は `partially_verified` とします。

---

### WTI NO_TRADE → **成功**

WTIは83ドル台から**81.25、-2.4%**へ反落しました。米原油在庫が1740万バレル増と2023年1月以来最大の増加になり、OPEC・IEAの需要見通し引き下げも売り材料になりました。citeturn846628news37

80ドル台で供給ショックBUYを追わなかった判断は適切でした。

**SUCCESSFUL_AVOIDANCE**

です。

---

### BTC / ETH NO_TRADE → **継続妥当**

BTCは約63411、ETHは約1625です。citeturn537619finance0turn537619finance1

NASDAQが史上最高値圏まで上昇した環境でもBTCが64k近辺を脱していないため、相対強度の問題は解消していません。

---

# 3. 市場全体の前提

本日のRegimeは、

**`POST_PPI_RISK_ON / LOWER_YIELDS / OIL_PULLBACK / AI_STRENGTH / RETAIL_SALES_AHEAD`**

です。

PPI前月比0.0%は予想+0.2%を下回り、前年比も5.5%から4.7%へ低下しました。市場では9月Fed据え置き確率が前日の約50%から65%程度まで上昇しました。citeturn537619news70turn511537news18

10年金利は**4.645%**へ約4.7bp低下。DXYはほぼ横ばいの99.98、USDJPYは159.55でした。citeturn511537news18

WTIも81.25へ反落。citeturn846628news37

つまり前日の、

**Oil↑ → inflation↑ → yields↑**

というNASDAQ逆風がかなり薄れ、

**PPI↓  
＋ Oil↓  
→ yields↓  
→ Growth valuation支援**

へ再び戻っています。

株式はこれを素直に評価し、S&P500は7798.99で最高値、NASDAQ総合は26803.03まで上昇しました。citeturn846628news42turn511537news18

ただし本日は小売売上高とミシガン消費者信頼感があります。citeturn646580news17

したがって、

**Risk-on confirmed  
but not event-free**

です。

---

# 4. 10資産別判断

| 資産 | 判定 | 本日の要点 |
|---|---|---|
| GOLD | **B BUY** | 金利低下は追い風だがprice confirmation悪化 |
| BTC | **NO_TRADE** | 株高に対する相対弱さ継続 |
| ETH | **NO_TRADE** | 1625近辺、独自強度なし |
| WTI | **NO_TRADE** | 供給リスクと需要弱化が衝突 |
| USDJPY | **NO_TRADE** | 159.55、介入リスク |
| SPX | **B BUY** | 最高値更新、押し目継続 |
| NASDAQ | **A BUY** | PPI・金利・Oil・AI・Priceが整合 |
| DXY | **NO_TRADE** | 99.98、方向性不足 |
| US10Y | **NO_TRADE** | 4.645まで低下、追わない |
| VIX | **NO_TRADE** | 14.5前後、株BUY確認用 |

### GOLD — B / BUY PULLBACK

金はPPI後に一時上昇しましたが、その後利益確定で下落し、米金先物は約4420.40で決済しました。citeturn511537news18

マクロはBUYですがprice confirmationが弱い。

**Entry 4320–4380  
SL 4150  
TP1 4540  
TP2 4680  
win_prob 0.60  
expected_r 0.38  
MAE想定 0.30R  
risk_pct 0.25%**

B維持です。

---

### BTC — NO_TRADE

約63411。citeturn537619finance0

NASDAQが強く上昇する中でも65kを突破できていません。

MES=48。

規定通りNO_TRADE。

---

### ETH — NO_TRADE

約1625。citeturn537619finance1

ここは変化なし。

BTC以上に相対強度が悪いので底値狙いはしません。

---

### WTI — NO_TRADE

81.25。前日比-2.4%。citeturn846628news37

需要見通し悪化と在庫急増はSELL材料ですが、中東供給リスクは残っています。

今度は下落を追ってSELLするのも避けます。

---

### USDJPY — NO_TRADE

159.55。citeturn511537news18

PPI下振れ・米金利低下にもかかわらず円高にならなかった点はUSDJPYの強さです。

しかし160円近辺には介入リスクがある。

BUYエッジはあってもRRが不足します。

---

### SPX — B / BUY PULLBACK

ESは7835付近まで上昇。citeturn846628search0

新Entry：

**7780–7810**

SL：

**7600**

TP1：

**8010**

TP2：

**8130**

win_prob **0.62**

expected_r **0.42**

MAE **0.27R**

risk_pct **0.25%**

最高値を成行追随するほどのOpportunityではないのでBです。

---

### NASDAQ — **A / BUY PULLBACK**

NQ9月限は**30214.25付近**まで上昇し、日中高値30272.75でした。citeturn846628search13

新Entry：

**29850–30100**

SL：

**28900**

TP1：

**31250**

TP2：

**32050**

win_prob：

**0.65**

expected_r：

**0.47R**

MAE想定：

**0.24R**

CBS：

**85**

EMS：

**81**

A条件を満たします。

ただし本日の小売売上高があるため、

**risk_pct = 0.25%**

に制限します。citeturn646580news17

さらに実売買ではXMの最小ロット＋SL幅で許容損失を超えるなら、分析上Aでも `BROKER_MIN_LOT_RISK / NO_TRADE` とします。memcite

---

### DXY — NO_TRADE

99.98付近。citeturn511537news18

PPI下振れでもドル指数はほぼ横ばい。

SELLするほど弱くありません。

---

### US10Y — NO_TRADE

4.645%。citeturn511537news18

方向は金利低下ですが、PPI後の動きを今から追いません。

また長期的には財政赤字・債券供給・Oil term premiumが上方向リスクとして残っています。citeturn511537news18

---

### VIX — NO_TRADE

8月13日のVIXは**14.54付近**。citeturn511537search4

株BUYのconfirmationとしては非常に良い。

しかし14台でさらにVIX SELLを行うRRは悪い。

NASDAQ/SPXのinvalidation指標として使います。

---

# 5. A級候補

## NASDAQ — A BUY PULLBACK

**Entry：29850–30100  
SL：28900  
TP1：31250  
TP2：32050  
RR：1.25  
win_prob：0.65  
expected_r：0.47R  
MAE：0.24R  
risk_pct：0.25%**

A判定の根拠は5つです。

**PPI予想下振れ、US10Y低下、WTI下落、VIX14台、NQ自身の高値更新。** citeturn537619news70turn511537news18turn846628news37turn511537search4turn846628search13

さらにAI関連企業の決算・設備投資期待が引き続きNASDAQを支援しています。citeturn511537news18

今回は**8月4日以来のNASDAQ A級**として扱います。

ただし今回も「Aだから高値を買う」のではありません。

**30100以下への軽い押しを待つ。**

30200台からそのまま上昇すればNO_FILLです。

---

# 6. B級監視候補

| 優先 | 資産 | Entry | SL | TP1 | win_prob | expected_r | MAE |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | SPX BUY | 7780–7810 | 7600 | 8010 | 0.62 | 0.42 | 0.27R |
| 2 | GOLD BUY | 4320–4380 | 4150 | 4540 | 0.60 | 0.38 | 0.30R |

SPXは昨日Entry到達後に上昇したため、B判定の実績として良いサンプルになりました。ESは7764.25まで押した後7830台まで上昇しています。citeturn846628search0

GOLDは逆です。

Entryへ到達したが短期逆行しました。

したがって本日は**NASDAQ/SPXの方をGOLDより優先**します。

---

# 7. 触らない資産

最優先は**WTI**。

今回の81.25への下落は、米在庫+1740万バレル、OPEC/IEA需要見通し引き下げという明確なSELL材料によるものですが、Hormuz・サウジ施設への攻撃など供給面のテールリスクも残っています。citeturn846628news37

BUYもSELLも追いません。

次にBTC/ETH。

特にBTCは、現在の株式Risk-onに対する**非参加そのものが情報**です。

---

# 8. 後日検証ポイント

最重要は当然、**本日のNASDAQ A**です。

記録対象：

**Entry到達有無  
24h MFE/MAE  
3営業日MFE/MAE  
5営業日MFE/MAE  
TP1/TP2  
SL  
5営業日時間決済**

さらに重要なのが**Entry方式の比較**です。

NASDAQでは8月4日以降、

**方向成功  
→ Deep Pullback Entry未到達  
→ NO_FILL  
→ その後上昇**

という例が複数発生しています。

今回Aについても、

**現行Entry 29850–30100**

とは別に仮想記録として、

**Shallow Pullback  
Breakout Retest  
Market Chase**

の3方式を同時追跡します。

ただし実運用はまだ現行Entryのみ。

少なくとも10～20件程度の教師データが蓄積するまでは、NO_FILLを理由にEntryを緩めません。

また今夜の米小売売上高・消費者信頼感前後で、

**NQ / ES / US10Y / DXY / VIX**

を記録します。金曜にこれらの主要マクロ指標が予定されています。citeturn646580news17

---

# 9. Obsidian保存用Observation Draft

```markdown
# 2026-08-14 PPI下振れ / NASDAQ A級再昇格

## Macro

July PPI:
MoM 0.0%
Consensus +0.2%

YoY:
4.7%
Previous 5.5%

US10Y:
~4.645%

DXY:
~99.98

USDJPY:
~159.55

WTI:
81.25
-2.4%

VIX:
~14.54

## Equity futures

ES Sep:
Open 7770
Low 7764.25
High ~7838
Close ~7835

NQ Sep:
Open 29825
Low 29780.50
High 30272.75
Close ~30214

## Regime

POST_PPI_RISK_ON
LOWER_YIELDS
OIL_PULLBACK
AI_STRENGTH
RETAIL_SALES_AHEAD

## Previous signal review

NASDAQ B:
DIRECTION_SUCCESS
NO_FILL

Previous Entry:
29450-29700

NQ Low:
29780.50

SPX B:
ENTRY_REACHED
DIRECTION_SUCCESS

GOLD B:
ENTRY_REACHED
1D_DIRECTION_FAIL

WTI NO_TRADE:
SUCCESSFUL_AVOIDANCE

## Signals

A:

NASDAQ BUY PULLBACK
Entry 29850-30100
SL 28900
TP1 31250
TP2 32050

win_prob 0.65
expected_r 0.47
MAE 0.24R
risk 0.25%

B:

SPX BUY
7780-7810
SL 7600
TP1 8010

GOLD BUY
4320-4380
SL 4150
TP1 4540

NO_TRADE:

BTC
ETH
WTI
USDJPY
DXY
US10Y
VIX

## Research

NASDAQ repeated pattern:

direction success
+
deep pullback not reached
+
NO_FILL
+
continued upside

Continue logging hypothetical:

Deep Pullback
Shallow Pullback
Breakout Retest
Market Chase

Do not modify live entry rule yet.

## Next event

US retail sales
Michigan consumer sentiment

Track:
NQ
ES
US10Y
DXY
VIX

#TSO #NASDAQ #SPX #GOLD #PPI #NO_FILL
```

# 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-08-14,20260814_GOLD_BUY_PULLBACK,GOLD,BUY,B,PULLBACK,4320,4380,4150,4540,4680,1.10,0.60,0.38,87,65,47,0.25,POST_PPI_GOLD_PULLBACK_PRICE_CONFIRMATION_WEAK,68,75,76,64,72,69,4150_break_or_DXY_US10Y_reacceleration,GOLD_entry_24h_3d_5d_MFE_MAE,partially_verified
2026-08-14,20260814_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,74,39,88,,CRYPTO_EQUITY_RELATIVE_WEAKNESS,57,68,72,39,55,48,65000_failure_despite_equity_risk_on,BTC_60k_65k_ETF_CME_NQ_relative_3d_5d,verified
2026-08-14,20260814_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,86,25,96,,ETH_SEVERE_RELATIVE_WEAKNESS,45,50,82,27,43,37,ETH_price_weakness_without_independent_confirmation,ETH_1600_1800_ETHBTC_ETF_3d_5d,partially_verified
2026-08-14,20260814_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,94,34,94,,SUPPLY_RISK_DEMAND_WEAKNESS_CONFLICT,77,67,95,33,58,66,inventory_demand_bearishness_conflicts_with_geopolitical_supply_risk,WTI_EIA_Hormuz_80_85_3d_5d,verified
2026-08-14,20260814_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,86,35,91,,USDJPY_160_INTERVENTION_RATE_CONFLICT,70,71,88,34,64,67,160_intervention_risk_limits_long_RR,USDJPY_160_US10Y_DXY_3d_5d,verified
2026-08-14,20260814_SPX_BUY_PULLBACK,SPX,BUY,B,PULLBACK,7780,7810,7600,8010,8130,1.05,0.62,0.42,94,74,35,0.25,POST_PPI_RECORD_HIGH_RISK_ON,77,78,77,82,80,74,7600_break_or_yield_VIX_oil_reversal,ES_entry_24h_3d_5d_MFE_MAE,verified
2026-08-14,20260814_NASDAQ_BUY_PULLBACK,NASDAQ,BUY,A,PULLBACK,29850,30100,28900,31250,32050,1.25,0.65,0.47,97,82,25,0.25,POST_PPI_AI_GROWTH_RISK_ON,81,81,78,88,85,78,28900_break_or_yield_VIX_growth_breadth_reversal,NQ_entry_24h_3d_5d_MFE_MAE_entry_model_comparison,verified
2026-08-14,20260814_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,78,42,79,,POST_PPI_DOLLAR_NEUTRAL,69,72,75,45,64,68,dollar_fails_to_confirm_PPI_yield_decline,DXY_retail_sales_US10Y_1d_3d,verified
2026-08-14,20260814_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,86,45,79,,POST_PPI_YIELD_DECLINE_FISCAL_TERM_PREMIUM,75,80,84,48,69,76,retail_sales_or_fiscal_supply_can_reverse_yield_decline,US10Y_retail_sales_1h_1d_3d,verified
2026-08-14,20260814_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,80,32,88,,RECORD_HIGH_LOW_VOL_RISK_ON,68,64,78,58,66,64,VIX_expansion_with_equity_break_or_macro_surprise,VIX_ES_NQ_retail_sales_1h_1d_3d,verified
```

## JSON

```json
[
{"date":"2026-08-14","signal_id":"20260814_GOLD_BUY_PULLBACK","asset":"GOLD","side":"BUY","rank":"B","type":"PULLBACK","entry_low":4320,"entry_high":4380,"sl":4150,"tp1":4540,"tp2":4680,"rr":1.10,"win_prob":0.60,"expected_r":0.38,"tq_score":87,"opp_score":65,"no_trade_score":47,"risk_pct":0.25,"regime":"POST_PPI_GOLD_PULLBACK_PRICE_CONFIRMATION_WEAK","ems":68,"ffs":75,"cds":76,"ias":64,"cbs":72,"mes":69,"invalidation":"4150_break_or_DXY_US10Y_reacceleration","verification_target":"GOLD_entry_24h_3d_5d_MFE_MAE","verified_status":"partially_verified"},
{"date":"2026-08-14","signal_id":"20260814_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":74,"opp_score":39,"no_trade_score":88,"risk_pct":null,"regime":"CRYPTO_EQUITY_RELATIVE_WEAKNESS","ems":57,"ffs":68,"cds":72,"ias":39,"cbs":55,"mes":48,"invalidation":"65000_failure_despite_equity_risk_on","verification_target":"BTC_60k_65k_ETF_CME_NQ_relative_3d_5d","verified_status":"verified"},
{"date":"2026-08-14","signal_id":"20260814_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":86,"opp_score":25,"no_trade_score":96,"risk_pct":null,"regime":"ETH_SEVERE_RELATIVE_WEAKNESS","ems":45,"ffs":50,"cds":82,"ias":27,"cbs":43,"mes":37,"invalidation":"ETH_price_weakness_without_independent_confirmation","verification_target":"ETH_1600_1800_ETHBTC_ETF_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-14","signal_id":"20260814_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":94,"opp_score":34,"no_trade_score":94,"risk_pct":null,"regime":"SUPPLY_RISK_DEMAND_WEAKNESS_CONFLICT","ems":77,"ffs":67,"cds":95,"ias":33,"cbs":58,"mes":66,"invalidation":"inventory_demand_bearishness_conflicts_with_geopolitical_supply_risk","verification_target":"WTI_EIA_Hormuz_80_85_3d_5d","verified_status":"verified"},
{"date":"2026-08-14","signal_id":"20260814_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":86,"opp_score":35,"no_trade_score":91,"risk_pct":null,"regime":"USDJPY_160_INTERVENTION_RATE_CONFLICT","ems":70,"ffs":71,"cds":88,"ias":34,"cbs":64,"mes":67,"invalidation":"160_intervention_risk_limits_long_RR","verification_target":"USDJPY_160_US10Y_DXY_3d_5d","verified_status":"verified"},
{"date":"2026-08-14","signal_id":"20260814_SPX_BUY_PULLBACK","asset":"SPX","side":"BUY","rank":"B","type":"PULLBACK","entry_low":7780,"entry_high":7810,"sl":7600,"tp1":8010,"tp2":8130,"rr":1.05,"win_prob":0.62,"expected_r":0.42,"tq_score":94,"opp_score":74,"no_trade_score":35,"risk_pct":0.25,"regime":"POST_PPI_RECORD_HIGH_RISK_ON","ems":77,"ffs":78,"cds":77,"ias":82,"cbs":80,"mes":74,"invalidation":"7600_break_or_yield_VIX_oil_reversal","verification_target":"ES_entry_24h_3d_5d_MFE_MAE","verified_status":"verified"},
{"date":"2026-08-14","signal_id":"20260814_NASDAQ_BUY_PULLBACK","asset":"NASDAQ","side":"BUY","rank":"A","type":"PULLBACK","entry_low":29850,"entry_high":30100,"sl":28900,"tp1":31250,"tp2":32050,"rr":1.25,"win_prob":0.65,"expected_r":0.47,"tq_score":97,"opp_score":82,"no_trade_score":25,"risk_pct":0.25,"regime":"POST_PPI_AI_GROWTH_RISK_ON","ems":81,"ffs":81,"cds":78,"ias":88,"cbs":85,"mes":78,"invalidation":"28900_break_or_yield_VIX_growth_breadth_reversal","verification_target":"NQ_entry_24h_3d_5d_MFE_MAE_entry_model_comparison","verified_status":"verified"},
{"date":"2026-08-14","signal_id":"20260814_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":78,"opp_score":42,"no_trade_score":79,"risk_pct":null,"regime":"POST_PPI_DOLLAR_NEUTRAL","ems":69,"ffs":72,"cds":75,"ias":45,"cbs":64,"mes":68,"invalidation":"dollar_fails_to_confirm_PPI_yield_decline","verification_target":"DXY_retail_sales_US10Y_1d_3d","verified_status":"verified"},
{"date":"2026-08-14","signal_id":"20260814_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":86,"opp_score":45,"no_trade_score":79,"risk_pct":null,"regime":"POST_PPI_YIELD_DECLINE_FISCAL_TERM_PREMIUM","ems":75,"ffs":80,"cds":84,"ias":48,"cbs":69,"mes":76,"invalidation":"retail_sales_or_fiscal_supply_can_reverse_yield_decline","verification_target":"US10Y_retail_sales_1h_1d_3d","verified_status":"verified"},
{"date":"2026-08-14","signal_id":"20260814_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":80,"opp_score":32,"no_trade_score":88,"risk_pct":null,"regime":"RECORD_HIGH_LOW_VOL_RISK_ON","ems":68,"ffs":64,"cds":78,"ias":58,"cbs":66,"mes":64,"invalidation":"VIX_expansion_with_equity_break_or_macro_surprise","verification_target":"VIX_ES_NQ_retail_sales_1h_1d_3d","verified_status":"verified"}
]
```

本日の核心は、**NASDAQがA級へ戻ったこと**です。前回Aだった8月4日と同様、方向・金利・原油・ボラティリティの整合性がかなり高くなりました。PPI下振れ後にNQ自身が30200台へ上昇しており、分析条件はかなり明瞭です。citeturn537619news70turn511537news18turn846628search13

ただし、過去の成功を見て価格を追う運用にはしません。**29850–30100へ押せば候補、来なければNO_FILL。** 月数回程度のA級が大きな方向を捉えられている限り、約定率を上げるために無理にリスクを増やす必要はありません。memcite

navlist8月13日の主要市場材料turn537619news70,turn511537news18,turn846628news37
