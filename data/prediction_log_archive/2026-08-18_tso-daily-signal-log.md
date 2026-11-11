<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-08-18 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 15631 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026年8月18日

データ基準は**8月17日米国市場終値＋8月18日朝のGlobex/暗号資産**です。今回はES/NQを先物系列で直接確認できています。ES9月限は8月17日に**7763.50～7824.50**、NQ9月限は**30054.50～30343.00、settlement 30096.00**。8月18日朝の遅延GlobexではES約7813、NQ約30210まで戻しています。citeturn279955search1turn879038view0turn111448search4turn111448search9

COMEX金12月限は**4473.70**で+0.8%。WTIは17日に約84.5～84.7ドルまで上昇しましたが、今朝CMEでは次限月を含む表示が82ドル台となっており、**ロールによる参照水準差**が発生しています。WTIはこの理由も含め `partially_verified` とします。citeturn111448news35turn189146news25turn189146search9

なお実執行ゲートは、直近の運用指示を優先して**1回の許容損失約3000円**として判定します。memcite

## 1. 本日の結論

**A級：0件。**

**B+観察：SPX BUY 1件。**

**B級：NASDAQ BUY、GOLD BUY。**

**NO_TRADE：BTC、ETH、WTI、USDJPY、DXY、US10Y、VIX。**

分析順位は、

**NASDAQ B > SPX B+ > GOLD B**

ですが、実執行順位は

**SPX > GOLD > NASDAQ**

です。

17日はS&P500が**-0.52%**、NASDAQ総合が-0.31%。原油上昇と長期金利上昇が株価の重石になりました。10年債利回りは**4.724%**、30年債は5.31%まで上昇しています。citeturn826381news73turn189146news25

一方、ドル指数は99.6付近へ軟化し、COMEX金は上昇。つまり現在は、

**Growth slowdown → USD↓ / GOLD↑**

と

**Oil↑＋fiscal term premium↑ → long yields↑ / stocks↓**

が同時進行しています。citeturn189146news25turn111448news35

これはNASDAQをAに戻せる環境ではありません。

---

## 2. 前回判断の簡易検証

### SPX B+ BUY → **ENTRY_REACHED / 初動ほぼ横ばい**

前回Entry：

**7740–7780**

17日のES9月限は**安値7763.50**。明確にEntry帯へ入りました。終盤値は7765.50前後で、日中としてはほぼEntry近傍で終了。その後8月18日朝のGlobexでは7810台へ反発しています。citeturn279955search1turn111448search4

したがって暫定評価は、

**ENTRY_REACHED  
SL_NOT_REACHED  
MFE_POSITIVE_AFTER_SESSION**

です。

これは本日もSPXを実務上の最優先候補とする根拠になります。

### NASDAQ B BUY → **ENTRY_REACHED / 仮説維持**

前回Entry：

**29850–30100**

17日のNQは**安値30054.50**。Entry帯へ到達しました。settlementは30096.00、今朝は30200台へ戻しています。citeturn879038view0

したがって、

**ENTRY_REACHED  
SL_NOT_REACHED  
THESIS_VALID**

です。

ただし原油・長期金利の上昇によりクロスアセット条件は悪化しています。

### GOLD B BUY → **方向成功 / NO_FILL可能性**

17日のCOMEX12月限は4473.70へ+0.8%。citeturn111448news35

前回Entry4320–4380はかなり深いため、今回も方向成功でも未約定だった可能性が高い。

**DIRECTION_SUCCESS / FILL_UNVERIFIED**

です。

### BTC NO_TRADE → **維持妥当**

BTCは現在約**64331ドル**まで反発しています。citeturn826381finance0

ただし17日の上昇でも約0.9%程度、株式・金利・ドルの大きな再価格付けに比べればまだ強いブレイクアウトではありません。またETFフローについては、直近の短期流出と8月上旬からの累積流入という相反するデータがあり、一方向に確定できません。citeturn826381news77turn826381search13

したがってMESは50未満を維持します。

---

## 3. 市場全体の前提

本日のRegimeは、

**`STAGFLATION_TWIST / OIL_UP / LONG_YIELDS_UP / USD_SOFT / EQUITY_PULLBACK`**

です。

17日にWTIは約**84.66ドル、+2.7%**。背景は米・イラン交渉停滞とHormuz供給懸念です。citeturn189146news25turn189146news29

通常なら弱い米指標とFed利上げ観測後退で長期金利も低下しそうですが、実際には10年4.724%、30年5.31%へ上昇しました。Reutersは財政懸念、弱い国債需要、AI関連企業の大型債券発行などを背景として挙げています。citeturn189146news25

つまり、

**Fed policy expectations ↓  
but long-term term premium ↑**

です。

これがNASDAQにとって最大の問題。

一方、DXYは99.6、金は4473.70まで上昇。citeturn189146news25turn111448news35

したがって現在は単純なRisk-On/Risk-Offではなく、**株式には慎重、金にはやや有利**という構造です。

USDJPYは17日に約**159.49**。BOJの9月利上げ観測は高く、同時に160円近辺では再介入リスクがあります。citeturn892165news26turn826381news80

VIXは17日終値**15.19**。14.25から上昇しましたが、依然として低い水準です。citeturn111448search11

---

## 4. 10資産別判断

| 資産 | 判定 | 核心 |
|---|---|---|
| GOLD | **B BUY** | USD軟化・景気不安＋価格上昇、ただし長期金利上昇 |
| BTC | **NO_TRADE** | 64k回復もMES<50、フロー判断混在 |
| ETH | **NO_TRADE** | 約1625、独自強度なし |
| WTI | **NO_TRADE** | Hormuz＋ロール水準差 |
| USDJPY | **NO_TRADE** | 159.5、BOJ＋介入リスク |
| SPX | **B+ BUY** | Entry到達後反発、実執行可能性あり |
| NASDAQ | **B BUY** | Entry到達後反発、長期金利が逆風 |
| DXY | **NO_TRADE** | 弱いがOil/term premiumと衝突 |
| US10Y | **NO_TRADE** | 4.724、高値追随禁止 |
| VIX | **NO_TRADE** | 15.19、株式確認指標 |

ETHは約**1624.95ドル**で、BTCのような64k回復に相当する独自のprice confirmationが確認できません。citeturn826381finance1

---

## 5. A級候補

**0件です。**

最も近いNASDAQでも、

**CBS 77  
EMS 70  
win_prob 0.60  
expected_r 0.40  
MAE 0.29R**

と評価。

CBS/EMSは良好ですが、

**expected_r < 0.45  
MAE > 0.25R**

なのでA不合格。

17日の長期金利上昇が特に大きな減点です。

SPXもCBS74、EMS68なのでAではありません。

---

## 6. B級監視候補

### 1位 SPX — **B+ BUY PULLBACK**

**Entry 7740–7785  
SL 7630  
TP1 8010  
TP2 8130  
RR 1.87  
win_prob 0.58  
expected_r 0.38  
MAE 0.31R  
risk_pct 0.25%**

CBS **75**  
EMS **68**

B+定量条件、

**CBS>=70  
EMS>=60  
RR>=1.5  
win_prob>=0.50**

を満たします。

また昨日のES安値7763.50でEntryが実際に機能しました。citeturn279955search1

**XM最小ロット＋SL7630で損失がおおむね3000円以内なら実取引可能。3000円を明確に超えるならNO_TRADE。**

今朝7810台へ戻っているため、**ここから成行では追いません。**

### 2位 NASDAQ — B BUY PULLBACK

**Entry 29880–30120  
SL 29200  
TP1 31400  
TP2 32250  
RR 1.75  
win_prob 0.60  
expected_r 0.40  
MAE 0.29R  
risk_pct 0.25%**

17日安値30054.50でEntry成立、今朝30200台へ反発。citeturn879038view0turn111448search9

シグナル品質はSPXより若干高く見ています。

ただしXM最小ロットで必要SLを置いた際の損失が以前同様1万円規模なら、**Signal=B / Execution=NO_TRADE**です。memcite

### 3位 GOLD — B BUY PULLBACK

**Entry 4380–4430  
SL 4260  
TP1 4660  
TP2 4800  
RR 1.76  
win_prob 0.60  
expected_r 0.41  
MAE 0.28R  
risk_pct 0.25%**

COMEX12月限は4473.70。citeturn111448news35

金は現在、

**USD↓  
Fed hike probability↓  
geopolitical risk↑**

という3つの追い風があります。

しかしUS10Y 4.724%は明確な逆風。

そのためAではなくBです。

---

## 7. 触らない資産

最優先は**WTI**。

17日には約84.5～84.7ドルまで上昇しましたが、今朝CMEの表示は82.7ドル前後となっており、**限月ロールによる価格水準差**が発生しています。citeturn189146news25turn189146search9

これを価格急落と誤認してはいけません。

さらにHormuzヘッドラインで数ドル単位のギャップが繰り返されています。

**参照系列ロール＋headline regime**

なので強いNO_TRADEです。

USDJPYも触りません。159.49近辺で、9月BOJ利上げ観測と160円介入警戒が共存しています。citeturn892165news26turn826381news80

---

## 8. 後日検証ポイント

本日の最重要教師データは**SPXとNASDAQのEntry成立後反発**です。

前日シグナルについて、

**SPX：7763.5でEntry到達  
NASDAQ：30054.5でEntry到達**

が確認されました。citeturn279955search1turn879038view0

今後、

**Entry → 24h MFE/MAE → 3d → 5d**

を残します。

また8月14日のNASDAQ A級も5営業日評価を継続。

もう一つ重要なのが**長期金利のregime変化**です。

弱い経済指標にもかかわらず10年4.724%、30年5.31%へ上昇したことは、

**Fed expectationsよりfiscal/term-premiumが優勢になり始めた**

可能性を示します。citeturn189146news25

これが続けば、NASDAQの「弱い景気＝金利低下＝買い」という従来ロジックを弱める必要があります。

---

## 9. Obsidian保存用Observation Draft

```markdown
# 2026-08-18 Long-yield divergence / SPX・NASDAQ Entry成立

## Market anchors

ES Sep:
Aug17 low 7763.50
close area 7765.50
Aug18 morning ~7810-7813

NQ Sep:
Aug17 low 30054.50
settlement 30096.00
Aug18 morning ~30210

COMEX Gold Dec:
4473.70

WTI:
Aug17 ~84.5-84.7
new contract display ~82.7

DXY:
~99.6

US10Y:
4.724%

USDJPY:
~159.49

VIX:
15.19

BTC:
~64331

ETH:
~1625

## Regime

STAGFLATION_TWIST
OIL_UP
LONG_YIELDS_UP
USD_SOFT
EQUITY_PULLBACK

## Key observation

Weak economic data did NOT push long yields lower.

Instead:

soft growth
+
oil inflation
+
fiscal term premium
+
AI corporate bond supply

-> US long yields higher.

Potential regime change for NASDAQ model.

## Previous signals

SPX B+:
ENTRY_REACHED
Low 7763.5
subsequent rebound

NASDAQ B:
ENTRY_REACHED
Low 30054.5
subsequent rebound

GOLD B:
DIRECTION_SUCCESS
FILL_UNVERIFIED

## Signals

A:
NONE

B+:
SPX BUY
7740-7785
SL 7630
TP1 8010

B:
NASDAQ BUY
29880-30120
SL 29200
TP1 31400

GOLD BUY
4380-4430
SL 4260
TP1 4660

NO_TRADE:
BTC
ETH
WTI
USDJPY
DXY
US10Y
VIX

## Research

Track whether:

weak macro data
still causes
lower yields + growth-stock strength

or whether:

fiscal/oil term premium
dominates monetary expectations.

This is a possible
bad-news-is-good-news
regime transition.

#TSO #SPX #NASDAQ #GOLD #US10Y #WTI
```

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-08-18,20260818_GOLD_BUY_PULLBACK,GOLD,BUY,B,PULLBACK,4380,4430,4260,4660,4800,1.76,0.60,0.41,91,72,39,0.25,USD_SOFT_GOLD_STRONG_LONG_YIELD_HEADWIND,74,77,82,74,78,72,4260_break_or_DXY_US10Y_acceleration,GOLD_entry_24h_3d_5d_MFE_MAE_XM_loss,verified
2026-08-18,20260818_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,72,47,79,,BTC_64K_RECOVERY_FLOW_MIXED,58,55,70,47,57,48,65000_break_plus_sustained_ETF_CME_confirmation_required,BTC_64k_65k_ETF_CME_flow_3d_5d,partially_verified
2026-08-18,20260818_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,86,24,96,,ETH_RELATIVE_WEAKNESS,44,47,83,26,42,36,independent_price_and_flow_confirmation_required,ETH_1600_1800_ETHBTC_ETF_3d_5d,partially_verified
2026-08-18,20260818_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,19,99,,HORMUZ_HEADLINE_FRONT_MONTH_ROLL,85,74,99,18,55,73,headline_gap_and_contract_roll_make_reference_unstable,WTI_front_month_roll_Hormuz_80_85_3d_5d,partially_verified
2026-08-18,20260818_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,91,28,96,,USDJPY_160_BOJ_INTERVENTION_CONFLICT,73,76,94,27,62,69,160_intervention_and_September_BOJ_hike_risk,USDJPY_160_BOJ_DXY_US10Y_3d_5d,verified
2026-08-18,20260818_SPX_BUY_PULLBACK,SPX,BUY,B,PULLBACK,7740,7785,7630,8010,8130,1.87,0.58,0.38,91,73,42,0.25,EQUITY_UPTREND_OIL_YIELD_HEADWIND,68,74,82,74,75,69,7630_break_or_VIX_oil_long_yield_acceleration,ES_entry_24h_3d_5d_MFE_MAE_XM_loss_3000JPY,verified
2026-08-18,20260818_NASDAQ_BUY_PULLBACK,NASDAQ,BUY,B,PULLBACK,29880,30120,29200,31400,32250,1.75,0.60,0.40,94,75,40,0.25,AI_UPTREND_LONG_YIELD_HEADWIND,70,77,84,82,77,71,29200_break_or_long_yield_AI_breadth_repricing,NQ_entry_24h_3d_5d_MFE_MAE_XM_loss,verified
2026-08-18,20260818_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,82,39,84,,FED_DOVISH_USD_SOFT_TERM_PREMIUM_OFFSET,71,74,82,41,65,68,long_yield_or_geopolitical_safe_haven_reversal,DXY_99_100_US10Y_FOMC_minutes_3d,verified
2026-08-18,20260818_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,95,27,96,,FISCAL_TERM_PREMIUM_YIELD_UP,81,86,94,29,71,81,weak_growth_finally_forces_long_yields_below_4.60,US10Y_4.60_4.75_FOMC_minutes_oil_3d,verified
2026-08-18,20260818_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,84,34,87,,LOW_VOL_EQUITY_PULLBACK,67,63,84,52,65,62,VIX_breaks_17_with_ES_NQ_structure_failure,VIX_15_17_ES_NQ_3d_5d,verified
```

### JSON

```json
[
{"date":"2026-08-18","signal_id":"20260818_GOLD_BUY_PULLBACK","asset":"GOLD","side":"BUY","rank":"B","type":"PULLBACK","entry_low":4380,"entry_high":4430,"sl":4260,"tp1":4660,"tp2":4800,"rr":1.76,"win_prob":0.60,"expected_r":0.41,"tq_score":91,"opp_score":72,"no_trade_score":39,"risk_pct":0.25,"regime":"USD_SOFT_GOLD_STRONG_LONG_YIELD_HEADWIND","ems":74,"ffs":77,"cds":82,"ias":74,"cbs":78,"mes":72,"invalidation":"4260_break_or_DXY_US10Y_acceleration","verification_target":"GOLD_entry_24h_3d_5d_MFE_MAE_XM_loss","verified_status":"verified"},
{"date":"2026-08-18","signal_id":"20260818_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":72,"opp_score":47,"no_trade_score":79,"risk_pct":null,"regime":"BTC_64K_RECOVERY_FLOW_MIXED","ems":58,"ffs":55,"cds":70,"ias":47,"cbs":57,"mes":48,"invalidation":"65000_break_plus_sustained_ETF_CME_confirmation_required","verification_target":"BTC_64k_65k_ETF_CME_flow_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-18","signal_id":"20260818_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":86,"opp_score":24,"no_trade_score":96,"risk_pct":null,"regime":"ETH_RELATIVE_WEAKNESS","ems":44,"ffs":47,"cds":83,"ias":26,"cbs":42,"mes":36,"invalidation":"independent_price_and_flow_confirmation_required","verification_target":"ETH_1600_1800_ETHBTC_ETF_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-18","signal_id":"20260818_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":19,"no_trade_score":99,"risk_pct":null,"regime":"HORMUZ_HEADLINE_FRONT_MONTH_ROLL","ems":85,"ffs":74,"cds":99,"ias":18,"cbs":55,"mes":73,"invalidation":"headline_gap_and_contract_roll_make_reference_unstable","verification_target":"WTI_front_month_roll_Hormuz_80_85_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-18","signal_id":"20260818_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":91,"opp_score":28,"no_trade_score":96,"risk_pct":null,"regime":"USDJPY_160_BOJ_INTERVENTION_CONFLICT","ems":73,"ffs":76,"cds":94,"ias":27,"cbs":62,"mes":69,"invalidation":"160_intervention_and_September_BOJ_hike_risk","verification_target":"USDJPY_160_BOJ_DXY_US10Y_3d_5d","verified_status":"verified"},
{"date":"2026-08-18","signal_id":"20260818_SPX_BUY_PULLBACK","asset":"SPX","side":"BUY","rank":"B","type":"PULLBACK","entry_low":7740,"entry_high":7785,"sl":7630,"tp1":8010,"tp2":8130,"rr":1.87,"win_prob":0.58,"expected_r":0.38,"tq_score":91,"opp_score":73,"no_trade_score":42,"risk_pct":0.25,"regime":"EQUITY_UPTREND_OIL_YIELD_HEADWIND","ems":68,"ffs":74,"cds":82,"ias":74,"cbs":75,"mes":69,"invalidation":"7630_break_or_VIX_oil_long_yield_acceleration","verification_target":"ES_entry_24h_3d_5d_MFE_MAE_XM_loss_3000JPY","verified_status":"verified"},
{"date":"2026-08-18","signal_id":"20260818_NASDAQ_BUY_PULLBACK","asset":"NASDAQ","side":"BUY","rank":"B","type":"PULLBACK","entry_low":29880,"entry_high":30120,"sl":29200,"tp1":31400,"tp2":32250,"rr":1.75,"win_prob":0.60,"expected_r":0.40,"tq_score":94,"opp_score":75,"no_trade_score":40,"risk_pct":0.25,"regime":"AI_UPTREND_LONG_YIELD_HEADWIND","ems":70,"ffs":77,"cds":84,"ias":82,"cbs":77,"mes":71,"invalidation":"29200_break_or_long_yield_AI_breadth_repricing","verification_target":"NQ_entry_24h_3d_5d_MFE_MAE_XM_loss","verified_status":"verified"},
{"date":"2026-08-18","signal_id":"20260818_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":82,"opp_score":39,"no_trade_score":84,"risk_pct":null,"regime":"FED_DOVISH_USD_SOFT_TERM_PREMIUM_OFFSET","ems":71,"ffs":74,"cds":82,"ias":41,"cbs":65,"mes":68,"invalidation":"long_yield_or_geopolitical_safe_haven_reversal","verification_target":"DXY_99_100_US10Y_FOMC_minutes_3d","verified_status":"verified"},
{"date":"2026-08-18","signal_id":"20260818_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":95,"opp_score":27,"no_trade_score":96,"risk_pct":null,"regime":"FISCAL_TERM_PREMIUM_YIELD_UP","ems":81,"ffs":86,"cds":94,"ias":29,"cbs":71,"mes":81,"invalidation":"weak_growth_finally_forces_long_yields_below_4.60","verification_target":"US10Y_4.60_4.75_FOMC_minutes_oil_3d","verified_status":"verified"},
{"date":"2026-08-18","signal_id":"20260818_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":84,"opp_score":34,"no_trade_score":87,"risk_pct":null,"regime":"LOW_VOL_EQUITY_PULLBACK","ems":67,"ffs":63,"cds":84,"ias":52,"cbs":65,"mes":62,"invalidation":"VIX_breaks_17_with_ES_NQ_structure_failure","verification_target":"VIX_15_17_ES_NQ_3d_5d","verified_status":"verified"}
]
```

**本日の実務判断はSPXです。** 17日に前回Entryへ実際に到達し、その後今朝のGlobexで7810台へ戻しています。したがってシグナル自体は機能中ですが、**現在値から追うのではなく7740–7785へ再度押した場合だけ検討**します。citeturn279955search1turn111448search4

NASDAQも30054.5まで押してEntry成立後に30200台へ戻しており方向は悪くありません。ただし今は**原油高＋長期金利高**というGrowth株に不利な組み合わせが強くなったため、A級には戻しません。citeturn879038view0turn189146news25

navlist8月17日の主要市場材料turn826381news73,turn189146news25,turn111448news35
