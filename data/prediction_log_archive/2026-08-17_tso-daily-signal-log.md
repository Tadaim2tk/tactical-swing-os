<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-08-17 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 14385 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026年8月17日

データ基準は**8月17日06:57 JST前後**。月曜朝でCMEの新週セッション開始前に近いため、ES/NQ・GOLD・WTI・DXY・US10Y・VIXは原則として**8月14日（金）の確定値をアンカー**にし、週末ニュースを上乗せしています。BTCは週末も取引され、8月16日は約**62990ドル**で、ETFフローも前週の流入から流出へ反転したとの複数報道があります。citeturn1news2turn0news11turn0news39

なお、前回会話で実運用の許容損失が更新されたため、**本日からXM最小ロットの実損ゲートは約3000円**として運用します。月次較正文面の1500円は旧値として扱います。memcite

## 1. 本日の結論

**A級：0件。**

**B級：NASDAQ BUY、SPX BUY、GOLD BUY。**

**B+観察候補：SPX BUY（実損条件付き）。**

**NO_TRADE：BTC、ETH、WTI、USDJPY、DXY、US10Y、VIX。**

分析順位は、

**NASDAQ B > SPX B+ > GOLD B**

です。

ただし**実取引順位はSPX > GOLD > NASDAQ**。

NASDAQは分析品質では最上位ですが、以前確認したXM最小ロット＋必要SLでは損失が1万円超になり得るため、3000円基準でも現状は**実取引NO_TRADE**です。SPXは以前の実測約3000円が現在も同程度なら、新基準では執行可能域へ入りました。memcite

したがって本日の実務上の注目は、**SPXの押し目が来るか**です。

---

## 2. 前回判断の簡易検証

日曜日だったため、ES/NQ/GOLD等に新しい通常セッションはありません。

8月14日のNASDAQ A級、

**Entry 29850–30100  
NQ安値 30028.5  
→ ENTRY_REACHED  
→ 正のMFE**

は引き続き5営業日検証対象です。

BTCは週末も63kを明確に回復できず、8月16日時点で約62990ドル。週間では約-2.7%と報じられています。citeturn1news2

さらに米現物BTC ETFは、8月第1週の大きな流入から第2週に流出へ転じました。citeturn0news11turn0news39

したがって前日の、

**BTC NO_TRADE / MES<50**

は維持が妥当です。

WTIについても、週末を通してHormuz問題は解消していません。イランは海峡への強硬姿勢を維持し、Kharg Islandでは原油積み出しが再開された一方、海峡輸送能力への不確実性は依然大きい状態です。citeturn0news31turn0news33

**WTI NO_TRADEも維持成功**とします。

---

## 3. 市場全体の前提

本日のRegime：

**`WEEK_OPEN / EQUITY_UPTREND / GROWTH_SCARE / HORMUZ_PREMIUM / CRYPTO_RELATIVE_WEAKNESS`**

米国株は週間ではS&P500・NASDAQとも**3週連続上昇**。AI関連への需要が株式を支えています。citeturn1news20

一方、7月小売売上高は前月比**-0.6%**と9カ月ぶりに減少。8月ミシガン消費者信頼感も**55.2→51.0**、1年先インフレ期待は**4.3%**へ上昇しました。citeturn0news49turn0news50

ここが現在の核心です。

**景気↓  
→ Fed利上げ確率↓  
→ Growth株にはプラス**

と、

**景気↓＋Oil高  
→ Stagflation/recession懸念  
→ 株式にはマイナス**

が競合しています。

金曜日にはS&P500 -0.17%、NASDAQ -0.28%。WTIは82ドル台へ反発し、米10年債利回りも上昇しました。citeturn1news30

今週最大のマクロイベントは**水曜日のFOMC議事要旨**。月曜はEmpire State Manufacturing、火曜は住宅着工・鉱工業生産、木曜は失業保険・Philadelphia Fed、金曜はPMIが予定されています。citeturn0news21

したがって今日は**イベント前の通常寄り防御**を維持します。

---

## 4. 10資産別判断

| 資産 | 判定 | 核心 |
|---|---|---|
| GOLD | **B BUY** | 景気不安・ドル軟化 vs Oil・長期金利 |
| BTC | **NO_TRADE** | 約63k、ETFフロー悪化 |
| ETH | **NO_TRADE** | 独自強度不足 |
| WTI | **NO_TRADE** | Hormuz headline dominant |
| USDJPY | **NO_TRADE** | 160介入圏＋BOJ利上げ観測 |
| SPX | **B+ BUY** | トレンド＋実損3000円条件に接近 |
| NASDAQ | **B BUY** | 分析品質最高、XM最小ロットが問題 |
| DXY | **NO_TRADE** | 弱い米指標とOilの綱引き |
| US10Y | **NO_TRADE** | Growth↓ vs Oil/fiscal premium |
| VIX | **NO_TRADE** | 14台、SELL余地不足 |

USDJPYについては金曜日にドルが弱い小売売上高を受け下落。円は159円台で、BOJの追加利上げ観測も強まっています。citeturn0news59turn0news60

---

## 5. A級候補

**本日0件。**

最も近いNASDAQは、

**CBS 78  
EMS 71  
win_prob 0.61  
expected_r 0.42  
MAE 0.28R**

と評価。

CBS/EMS/RRは良好ですが、

**expected_r < 0.45  
MAE > 0.25R**

なのでA条件を満たしません。

さらにXM最小ロットで必要SLを置くと3000円を大幅に超える可能性が高い。

よって、

**Signal=B  
Execution=NO_TRADE**

です。

これは重要な区別です。

---

## 6. B級監視候補

### 1. NASDAQ — B BUY PULLBACK

**Entry 29850–30100  
SL 29150  
TP1 31250  
TP2 32100  
RR 1.55  
win_prob 0.61  
expected_r 0.42  
MAE 0.28R  
risk 0.25%**

トレンドそのものは最も強い。

ただし**XM実損>3000円なら注文禁止**。

したがって分析1位でも実売買候補ではありません。

### 2. SPX — **B+ BUY PULLBACK**

**Entry 7740–7780  
SL 7620  
TP1 7980  
TP2 8110  
RR 1.57  
win_prob 0.59  
expected_r 0.39  
MAE 0.30R  
risk 0.25%**

CBS **76**  
EMS **69**

B+条件の、

**CBS>=70  
EMS>=60  
RR>=1.5  
win_prob>=0.50**

を満たします。

そして実損上限が1500円→**3000円へ更新されたため、以前確認したXM最小ロット損失約3000円が現在も同程度なら執行可能**です。memcite

ただし上限ぎりぎりなので、**3000円を明確に超える場合はNO_TRADE**。

月曜寄りで7780より上へギャップした場合も追いません。

### 3. GOLD — B BUY PULLBACK

**Entry 4320–4380  
SL 4220  
TP1 4560  
TP2 4690  
RR 1.62  
win_prob 0.58  
expected_r 0.36  
MAE 0.32R  
risk 0.25%**

金曜日はドル安と弱い米経済指標を背景に金が上昇しました。citeturn1news30

ただしOil高・長期金利高が相殺要因。

現在値を追わずEntry待ちです。

---

## 7. 触らない資産

**WTIが最優先NO_TRADE。**

WTIは約82.40ドル。週末もHormuzを巡る政治・軍事的不確実性が続いています。citeturn0news30turn0news31

現在のWTIは通常の、

**technical → entry → SL → TP**

より、

**headline → gap → reversal**

の影響が大きい。

ここでは予測精度よりギャップリスクが問題です。

次がBTC。

BTCは約63kで、S&P500/NASDAQが3週連続上昇しているのに相対的に弱い。citeturn1news2turn1news20

ETFフローも悪化。

**MES=42。**

規定通りNO_TRADEです。

---

## 8. 後日検証ポイント

今週は二つを重点研究します。

第一は**8月14日NASDAQ A**。

既に、

**A判定  
→ Entry到達  
→ MFE正**

まで確認済み。

3営業日・5営業日のMFE/MAEと時間決済成績を記録します。

第二は今日の**SPX B+**。

許容実損を3000円へ更新したことで、初めて、

**「シグナルはBだが、実際に取引可能な高品質候補」**

としてSPXが戻ってきます。

今後は、

**Forecast Quality  
Signal Rank  
Broker Executability  
Actual Trade Result**

を別々に記録します。

また今週は水曜FOMC議事要旨を境に、**bad news = lower rates = stocks up** がまだ機能するかを確認します。citeturn0news21

---

## 9. Obsidian保存用Observation Draft

```markdown
# 2026-08-17 SPX B+ returns after risk-limit update

## Regime

WEEK_OPEN
EQUITY_UPTREND
GROWTH_SCARE
HORMUZ_PREMIUM
CRYPTO_RELATIVE_WEAKNESS

## Weekend update

BTC:
~62990

BTC ETF:
weekly flow reversal to outflows

WTI:
~82.40

Hormuz:
geopolitical uncertainty persists

US equity:
S&P500 and Nasdaq
3 consecutive weekly gains

## Macro

July retail sales:
-0.6%

Michigan sentiment:
51.0

1y inflation expectations:
4.3%

## Execution rule update

Previous XM loss gate:
1500 JPY

Current operational loss tolerance:
~3000 JPY

This changes broker executability,
not signal quality.

## Signals

A:
NONE

B+:
SPX BUY
Entry 7740-7780
SL 7620
TP1 7980
TP2 8110

Execution:
allowed only if XM minimum-lot loss <= ~3000 JPY

B:

NASDAQ BUY
29850-30100
SL 29150
TP1 31250

Signal quality highest
but broker loss likely >3000 JPY
=> execution NO_TRADE

GOLD BUY
4320-4380
SL 4220
TP1 4560

NO_TRADE:

BTC
ETH
WTI
USDJPY
DXY
US10Y
VIX

## Research

Continue Aug14 NASDAQ A:
3d MFE/MAE
5d MFE/MAE

Start SPX B+ executable-signal sample.

Separate:

forecast quality
signal quality
broker executability
actual trade outcome

## Week catalyst

Monday:
Empire State

Wednesday:
FOMC minutes

Friday:
PMI

#TSO #SPX #NASDAQ #GOLD #BTC
```

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-08-17,20260817_GOLD_BUY_PULLBACK,GOLD,BUY,B,PULLBACK,4320,4380,4220,4560,4690,1.62,0.58,0.36,86,64,49,0.25,WEEK_OPEN_GROWTH_SCARE_GOLD_HEDGE,67,73,79,64,72,67,4220_break_or_DXY_US10Y_oil_reacceleration,GOLD_entry_24h_3d_5d_MFE_MAE_XM_loss,partially_verified
2026-08-17,20260817_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,84,26,96,,CRYPTO_ETF_OUTFLOW_RELATIVE_WEAKNESS,49,42,81,28,47,42,64000_recovery_plus_ETF_flow_improvement_required,BTC_60k_64k_65k_ETF_CME_flow_3d_5d,partially_verified
2026-08-17,20260817_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,87,22,97,,ETH_RELATIVE_WEAKNESS,43,46,84,24,41,35,ETH_independent_price_and_flow_confirmation_required,ETH_1600_1800_ETHBTC_ETF_3d_5d,unverified
2026-08-17,20260817_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,22,99,,HORMUZ_HEADLINE_SUPPLY_RISK,84,73,99,21,57,72,headline_gap_risk_dominates_technical_edge,WTI_80_85_Hormuz_week_open_3d_5d,partially_verified
2026-08-17,20260817_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,90,29,95,,USDJPY_160_INTERVENTION_BOJ_RISK,73,75,93,28,63,69,160_intervention_and_BOJ_hike_risk_limit_RR,USDJPY_160_BOJ_DXY_US10Y_3d_5d,partially_verified
2026-08-17,20260817_SPX_BUY_PULLBACK,SPX,BUY,B,PULLBACK,7740,7780,7620,7980,8110,1.57,0.59,0.39,92,72,40,0.25,WEEK_OPEN_RECORD_HIGH_GROWTH_SCARE,69,74,81,75,76,70,7620_break_or_VIX_recession_oil_yield_repricing,ES_entry_24h_3d_5d_MFE_MAE_XM_loss_3000JPY,partially_verified
2026-08-17,20260817_NASDAQ_BUY_PULLBACK,NASDAQ,BUY,B,PULLBACK,29850,30100,29150,31250,32100,1.55,0.61,0.42,95,75,38,0.25,WEEK_OPEN_AI_UPTREND_GROWTH_SCARE,71,77,83,83,78,72,29150_break_or_growth_recession_VIX_yield_repricing,NQ_entry_Aug14_A_3d_5d_MFE_MAE_XM_loss,partially_verified
2026-08-17,20260817_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,81,38,85,,WEAK_DATA_SOFT_DOLLAR_OIL_OFFSET,71,73,81,40,65,68,oil_inflation_or_long_yield_rebound_restores_dollar,DXY_100_US10Y_WTI_FOMC_minutes,partially_verified
2026-08-17,20260817_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,92,35,92,,GROWTH_SCARE_FISCAL_OIL_CONFLICT,76,83,92,36,68,78,growth_slowdown_conflicts_with_fiscal_and_oil_term_premium,US10Y_4.60_4.70_FOMC_minutes_WTI,partially_verified
2026-08-17,20260817_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,86,28,93,,LOW_VOL_MACRO_GEOPOLITICAL_RISK,66,61,89,46,63,60,VIX_expansion_with_equity_break_or_growth_shock,VIX_14_15_ES_NQ_FOMC_minutes_3d_5d,partially_verified
```

### JSON

```json
[
{"date":"2026-08-17","signal_id":"20260817_GOLD_BUY_PULLBACK","asset":"GOLD","side":"BUY","rank":"B","type":"PULLBACK","entry_low":4320,"entry_high":4380,"sl":4220,"tp1":4560,"tp2":4690,"rr":1.62,"win_prob":0.58,"expected_r":0.36,"tq_score":86,"opp_score":64,"no_trade_score":49,"risk_pct":0.25,"regime":"WEEK_OPEN_GROWTH_SCARE_GOLD_HEDGE","ems":67,"ffs":73,"cds":79,"ias":64,"cbs":72,"mes":67,"invalidation":"4220_break_or_DXY_US10Y_oil_reacceleration","verification_target":"GOLD_entry_24h_3d_5d_MFE_MAE_XM_loss","verified_status":"partially_verified"},
{"date":"2026-08-17","signal_id":"20260817_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":84,"opp_score":26,"no_trade_score":96,"risk_pct":null,"regime":"CRYPTO_ETF_OUTFLOW_RELATIVE_WEAKNESS","ems":49,"ffs":42,"cds":81,"ias":28,"cbs":47,"mes":42,"invalidation":"64000_recovery_plus_ETF_flow_improvement_required","verification_target":"BTC_60k_64k_65k_ETF_CME_flow_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-17","signal_id":"20260817_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":87,"opp_score":22,"no_trade_score":97,"risk_pct":null,"regime":"ETH_RELATIVE_WEAKNESS","ems":43,"ffs":46,"cds":84,"ias":24,"cbs":41,"mes":35,"invalidation":"ETH_independent_price_and_flow_confirmation_required","verification_target":"ETH_1600_1800_ETHBTC_ETF_3d_5d","verified_status":"unverified"},
{"date":"2026-08-17","signal_id":"20260817_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":22,"no_trade_score":99,"risk_pct":null,"regime":"HORMUZ_HEADLINE_SUPPLY_RISK","ems":84,"ffs":73,"cds":99,"ias":21,"cbs":57,"mes":72,"invalidation":"headline_gap_risk_dominates_technical_edge","verification_target":"WTI_80_85_Hormuz_week_open_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-17","signal_id":"20260817_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":90,"opp_score":29,"no_trade_score":95,"risk_pct":null,"regime":"USDJPY_160_INTERVENTION_BOJ_RISK","ems":73,"ffs":75,"cds":93,"ias":28,"cbs":63,"mes":69,"invalidation":"160_intervention_and_BOJ_hike_risk_limit_RR","verification_target":"USDJPY_160_BOJ_DXY_US10Y_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-17","signal_id":"20260817_SPX_BUY_PULLBACK","asset":"SPX","side":"BUY","rank":"B","type":"PULLBACK","entry_low":7740,"entry_high":7780,"sl":7620,"tp1":7980,"tp2":8110,"rr":1.57,"win_prob":0.59,"expected_r":0.39,"tq_score":92,"opp_score":72,"no_trade_score":40,"risk_pct":0.25,"regime":"WEEK_OPEN_RECORD_HIGH_GROWTH_SCARE","ems":69,"ffs":74,"cds":81,"ias":75,"cbs":76,"mes":70,"invalidation":"7620_break_or_VIX_recession_oil_yield_repricing","verification_target":"ES_entry_24h_3d_5d_MFE_MAE_XM_loss_3000JPY","verified_status":"partially_verified"},
{"date":"2026-08-17","signal_id":"20260817_NASDAQ_BUY_PULLBACK","asset":"NASDAQ","side":"BUY","rank":"B","type":"PULLBACK","entry_low":29850,"entry_high":30100,"sl":29150,"tp1":31250,"tp2":32100,"rr":1.55,"win_prob":0.61,"expected_r":0.42,"tq_score":95,"opp_score":75,"no_trade_score":38,"risk_pct":0.25,"regime":"WEEK_OPEN_AI_UPTREND_GROWTH_SCARE","ems":71,"ffs":77,"cds":83,"ias":83,"cbs":78,"mes":72,"invalidation":"29150_break_or_growth_recession_VIX_yield_repricing","verification_target":"NQ_entry_Aug14_A_3d_5d_MFE_MAE_XM_loss","verified_status":"partially_verified"},
{"date":"2026-08-17","signal_id":"20260817_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":81,"opp_score":38,"no_trade_score":85,"risk_pct":null,"regime":"WEAK_DATA_SOFT_DOLLAR_OIL_OFFSET","ems":71,"ffs":73,"cds":81,"ias":40,"cbs":65,"mes":68,"invalidation":"oil_inflation_or_long_yield_rebound_restores_dollar","verification_target":"DXY_100_US10Y_WTI_FOMC_minutes","verified_status":"partially_verified"},
{"date":"2026-08-17","signal_id":"20260817_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":92,"opp_score":35,"no_trade_score":92,"risk_pct":null,"regime":"GROWTH_SCARE_FISCAL_OIL_CONFLICT","ems":76,"ffs":83,"cds":92,"ias":36,"cbs":68,"mes":78,"invalidation":"growth_slowdown_conflicts_with_fiscal_and_oil_term_premium","verification_target":"US10Y_4.60_4.70_FOMC_minutes_WTI","verified_status":"partially_verified"},
{"date":"2026-08-17","signal_id":"20260817_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":86,"opp_score":28,"no_trade_score":93,"risk_pct":null,"regime":"LOW_VOL_MACRO_GEOPOLITICAL_RISK","ems":66,"ffs":61,"cds":89,"ias":46,"cbs":63,"mes":60,"invalidation":"VIX_expansion_with_equity_break_or_growth_shock","verification_target":"VIX_14_15_ES_NQ_FOMC_minutes_3d_5d","verified_status":"partially_verified"}
]
```

**本日の実務上の変更点はSPXです。** 3000円まで許容する現在の実運用なら、以前ならブローカー制約だけで落としていたSPXが再び候補になります。一方NASDAQは分析上の方向性が依然もっとも良いものの、必要SLを保ったまま最小ロットで3000円以内に収まらないなら見送ります。

今日は月曜寄りで無理に入らず、**ESが7740–7780へ押して、かつXM画面上でSL時損失がおおむね3000円以内ならSPXを最優先で検討**、という判断です。memcite
