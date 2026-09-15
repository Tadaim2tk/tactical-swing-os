<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-08-23 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 14337 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026年8月23日

本日は日曜日です。**BTC/ETHは8月23日朝まで新規Web取得を試み、GOLD・WTI・ES・NQ・DXY・US10Y・VIXは8月21日（金）の終値を基準値**とします。BTC/ETHについて完全同時刻の複数ソース照合ができないため `partially_verified`、金曜確定系列もソース品質に応じて `verified / partially_verified` を使います。

週末の新情報で最重要なのはETFフローです。米スポットBTC ETFは8月21日までの1週間で**約19億ドル純流入**、ETH ETFも**約6.97億ドル純流入**となり、両方とも2026年最大の週間流入。合計約26億ドルで前週の約3.92億ドル流出から大幅反転しました。土曜午後時点でBTC約77,200ドル、ETH約2,423ドルでした。citeturn693056news0turn693056news1

---

## 1. 本日の結論

**A級：0件**

**B+観察候補：0件**

**B級：GOLD BUY、BTC BUY、ETH BUY**

**NO_TRADE：WTI、USDJPY、SPX、NASDAQ、DXY、US10Y、VIX**

順位は、

**GOLD B > BTC B > ETH B**

です。

昨日から方向性はほぼ変えません。ただしBTC/ETHについては、ETFフローの追加確認によって**「単なるショートスクイーズ」よりも実需を伴う上昇だった確度が上昇**しました。BTC ETF週間+1.9B、ETH ETF+697M、ETF出来高も大幅増です。citeturn693056news0

それでもAにしない理由は**価格の伸び過ぎ**です。BTCは週間20%超、ETHも24～28%程度上昇。押し目なしで追えばMAEとRRが急速に悪化します。citeturn693056news0turn693056news62

実執行では、現在の運用上の許容損失を**1回約3000円**として扱います。必要SLをXM最小ロットで置いて3000円を明確に超える商品は、シグナル成立でもExecution NO_TRADEです。memcite

---

## 2. 前回判断の簡易検証

### GOLD B BUY
前回Entryは**4560–4610**。金曜の金先物は約4670ドルまで上昇し、週間+5%以上となりました。citeturn254752news60

**DIRECTION_SUCCESS / FILL未確認**。

方向シグナルは良好ですが、週末のため新しいCOMEXセッションはありません。

### BTC B BUY
前回Entryは**73500–75500**。土曜日のBTCは約77,200ドルで推移し、前回Entryより上を維持しています。citeturn693056news0

金曜日に一時79,463ドルへ上昇後、77k近辺へ落ち着いているため、

**DIRECTION_SUCCESS / ENTRY_RETEST未確認 / TP1未到達**

とします。

### ETH B BUY
前回Entryは**2150–2260**。土曜午後のETHは約2,423ドル。citeturn693056news0

**DIRECTION_SUCCESS / NO_FILL濃厚**。

昨日B昇格後も上方向を維持しました。

### WTI NO_TRADE
WTIは金曜日まで6営業日続伸。地政学的供給懸念が主因です。Reutersも週末にかけた米株市場の主要リスクとしてIranと原油を挙げています。citeturn693056news10turn693056news60

引き続き**SUCCESSFUL_AVOIDANCE**です。

---

## 3. 市場全体の前提

本日のRegimeは、

**`WEEKEND_HARD_ASSET_STRENGTH / CRYPTO_FLOW_CONFIRMATION / HIGH_TERM_PREMIUM / OIL_INFLATION / EQUITY_NOT_CONFIRMED`**

です。

現在はかなり明確な分断があります。

**GOLD / BTC / ETH：強い**

一方、

**S&P500 / NASDAQ：週間下落**

です。

S&P500は週間-1.43%、NASDAQは-2.05%。長期金利もTreasury買い戻し拡大にもかかわらず10年債4.737%、30年債5.276%付近で週を終えました。citeturn693056news60turn254752news58

つまり、

**Liquidity/debasement trade → GOLD・Crypto**

と、

**high yields / oil inflation → Equities圧迫**

が同時進行しています。

このため「BTCが上がったからNASDAQも買う」というクロスアセット転用はしません。

---

## 4. 10資産別判断

| 資産 | 判定 | 要点 |
|---|---|---|
| GOLD | **B BUY** | ドル不安・財政懸念・価格強度。過熱のみ減点 |
| BTC | **B BUY** | ETF+1.9B、価格確認済み。押し目限定 |
| ETH | **B BUY** | ETF+697M、価格確認済み。BTCより低評価 |
| WTI | **NO_TRADE** | 地政学供給ショック継続 |
| USDJPY | **NO_TRADE** | 160近辺介入・BOJ・米金利が競合 |
| SPX | **NO_TRADE** | 週間-1.43%、高金利構造未解消 |
| NASDAQ | **NO_TRADE** | 週間-2.05%、長期金利逆風 |
| DXY | **NO_TRADE** | ドル弱含みだが既に伸びたSELL |
| US10Y | **NO_TRADE** | Treasury政策と財政term premiumが競合 |
| VIX | **NO_TRADE** | 株式regime確認用。直接売買優位性不足 |

BTC/ETHについては前日より需給評価を上げます。ETF取引量はBTCが前週69億ドル→**221億ドル**、ETHも19億ドル→**69億ドル**へ急増しており、フローの信頼度が高まりました。citeturn693056news0

---

## 5. A級候補

**0件です。**

GOLD：

**CBS 87  
EMS 84  
expected_r 0.44  
MAE 0.27R**

BTC：

**CBS 88  
EMS 84  
MES 88  
expected_r 0.43  
MAE 0.30R**

ETH：

**CBS 80  
EMS 76  
expected_r 0.39  
MAE 0.33R**

いずれもCBS/EMSは強いものの、**expected_r>=0.45・MAE<=0.25Rを同時に満たしません。**

市場方向ではなく、**Entry時点の価格位置がAを阻害しています。**

---

## 6. B級監視候補

### GOLD — B BUY PULLBACK

**Entry 4580–4630  
SL 4450  
TP1 4920  
TP2 5080  
RR 2.00  
win_prob 0.64  
較正参考 0.67  
expected_r 0.44  
MAE 0.27R  
risk 0.25%**

金先物は金曜約4670ドルまで上昇。ドル安・米財政不安による`debasement trade`が主要テーマです。citeturn254752news60turn254752news56

**4630より上では買いません。**

### BTC — B BUY PULLBACK

**Entry 74200–76000  
SL 70400  
TP1 82500  
TP2 87000  
RR 1.65  
win_prob 0.63  
較正参考 0.66  
expected_r 0.43  
MAE 0.30R  
risk 0.25%**

ETF週間+1.9B、出来高22.1B。citeturn693056news0

これは前週までより明確な強気材料です。

ただし77k台を追わず、**76k以下へのリテスト限定**。

XM最小ロット＋SL70400で約3000円を超えるなら実取引NO_TRADEです。

### ETH — B BUY PULLBACK

**Entry 2240–2340  
SL 2050  
TP1 2700  
TP2 2920  
RR 1.74  
win_prob 0.60  
較正参考 0.63  
expected_r 0.39  
MAE 0.33R  
risk 0.25%**

ETH ETF週間+697.2M、出来高6.9B。citeturn693056news0

以前の「ETF/価格確認不足」はほぼ解消しました。

ただしBTCより変動が大きく、MAEを高く見積もります。

---

## 7. 触らない資産

**WTIが最優先NO_TRADE**です。

原油はIran/Hormuz懸念から6日続伸し、米株市場でもインフレ・長期金利の主要リスクになっています。citeturn693056news10turn693056news60

ここからBUYは供給ショックmomentum chase。

逆にSELLも地政学イベントへの逆張りです。

NASDAQもまだ触りません。金曜日は反発しましたが週間-2.05%。長期債利回りも高止まりしています。citeturn693056news60turn254752news58

---

## 8. 後日検証ポイント

最大の研究テーマは引き続き**Crypto FLOW_TO_PRICE_LAG**です。

今週の確定値は、

**BTC ETF +1.9B  
ETH ETF +697.2M  
Combined +2.6B**

で2026年最大。前週はCombined -392Mでした。citeturn693056news0

つまり、

**前週：flow悪化 / price弱い**

から、

**今週：flow急改善 / price急騰**

への明確なregime shiftです。

今後5営業日は、

**BTC：74k / 70k維持、82k到達、ETF継続流入**

**ETH：2.2k維持、2.6k到達、ETH/BTC相対強度**

を追跡します。

またGOLDでは、「方向成功だがEntry未到達」が繰り返されているため、NASDAQと同様に**Deep Pullback vs Shallow Pullback**の仮想比較を蓄積します。

---

## 9. Obsidian保存用Observation Draft

```markdown
# 2026-08-23 Crypto ETF Confirmation / Weekend

## Regime

WEEKEND_HARD_ASSET_STRENGTH
CRYPTO_FLOW_CONFIRMATION
HIGH_TERM_PREMIUM
OIL_INFLATION
EQUITY_NOT_CONFIRMED

## Crypto ETF weekly flows

BTC:
+1.9bn USD

ETH:
+697.2m USD

Combined:
+2.6bn USD

Previous week:
-392m USD

BTC ETF volume:
6.9bn -> 22.1bn

ETH ETF volume:
1.9bn -> 6.9bn

## Weekend prices

BTC:
~77.2k

ETH:
~2.42k

## Interpretation

Flow-price confirmation strengthened materially.

Previous:
ETF flow without price confirmation

Current:
ETF inflow
+
higher ETF volume
+
price breakout

Regime shift increasingly confirmed.

## Signals

A:
NONE

B:

GOLD BUY
4580-4630
SL 4450
TP1 4920

BTC BUY
74200-76000
SL 70400
TP1 82500

ETH BUY
2240-2340
SL 2050
TP1 2700

NO_TRADE:
WTI
USDJPY
SPX
NASDAQ
DXY
US10Y
VIX

## Execution

No momentum chase.

GOLD >4630:
NO_FILL

BTC >76000:
NO_FILL

ETH >2340:
NO_FILL

XM minimum-lot loss must remain near or below
operational ~3000 JPY limit.

## Research

BTC FLOW_TO_PRICE_LAG
ETH FLOW_TO_PRICE_LAG
GOLD shallow-vs-deep pullback

#TSO #BTC #ETH #GOLD #ETF
```

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-08-23,20260823_GOLD_BUY_PULLBACK,GOLD,BUY,B,PULLBACK,4580,4630,4450,4920,5080,2.00,0.64,0.44,98,76,34,0.25,HARD_ASSET_DEBASEMENT_RALLY,84,85,79,89,87,82,4450_break_or_DXY_US10Y_acceleration,GOLD_entry_24h_3d_5d_MFE_MAE_pullback_model,verified
2026-08-23,20260823_BTC_BUY_PULLBACK,BTC,BUY,B,PULLBACK,74200,76000,70400,82500,87000,1.65,0.63,0.43,99,73,43,0.25,BTC_ETF_FLOW_PRICE_CONFIRMATION_OVEREXTENDED,84,92,80,88,88,88,70400_break_or_ETF_flow_reversal,BTC_70k_74k_82k_ETF_3d_5d_MFE_MAE,partially_verified
2026-08-23,20260823_ETH_BUY_PULLBACK,ETH,BUY,B,PULLBACK,2240,2340,2050,2700,2920,1.74,0.60,0.39,97,68,49,0.25,ETH_ETF_FLOW_PRICE_CONFIRMATION_OVEREXTENDED,76,87,79,79,80,80,2050_break_or_ETH_ETF_flow_reversal,ETH_2.2k_2.6k_ETHBTC_ETF_3d_5d,partially_verified
2026-08-23,20260823_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,15,99,,HORMUZ_SUPPLY_SHOCK_SIX_DAY_RALLY,91,81,99,14,56,80,supply_shock_momentum_chase_prohibited,WTI_85_90_Hormuz_week_open_3d_5d,verified
2026-08-23,20260823_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,90,37,91,,USD_WEAK_BOJ_INTERVENTION_CONFLICT,73,77,90,38,65,70,160_intervention_BOJ_and_DXY_conflict,USDJPY_157_160_DXY_US10Y_3d,partially_verified
2026-08-23,20260823_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,87,45,79,,WEEKLY_EQUITY_PULLBACK_HIGH_YIELDS,65,72,81,50,68,67,ES_multi_day_stabilization_and_US10Y_decline_required,ES_US10Y_VIX_week_open_1d_3d,partially_verified
2026-08-23,20260823_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,92,39,86,,TECH_WEEKLY_PULLBACK_HIGH_TERM_PREMIUM,61,71,86,43,64,64,NQ_stabilization_and_long_yield_relief_required,NQ_US10Y_SOX_week_open_1d_3d,partially_verified
2026-08-23,20260823_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,93,34,92,,USD_DEBASEMENT_EXTENDED,78,83,90,33,69,79,DXY_reclaim_100_or_confirm_break_below_98_required,DXY_98_100_US10Y_3d_5d,partially_verified
2026-08-23,20260823_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,22,98,,FISCAL_TERM_PREMIUM_BUYBACK_CONFLICT,86,91,98,21,75,87,confirmed_break_below_4.60_or_above_4.75_required,US10Y_4.60_4.75_week_open_3d_5d,verified
2026-08-23,20260823_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,79,43,79,,VOL_RELIEF_WEEKLY_EQUITY_WEAKNESS,65,64,77,58,66,62,VIX_above_17_or_below_14_confirms_next_regime,VIX_14_17_ES_NQ_week_open_3d,partially_verified
```

### JSON

```json
[
{"date":"2026-08-23","signal_id":"20260823_GOLD_BUY_PULLBACK","asset":"GOLD","side":"BUY","rank":"B","type":"PULLBACK","entry_low":4580,"entry_high":4630,"sl":4450,"tp1":4920,"tp2":5080,"rr":2.00,"win_prob":0.64,"expected_r":0.44,"tq_score":98,"opp_score":76,"no_trade_score":34,"risk_pct":0.25,"regime":"HARD_ASSET_DEBASEMENT_RALLY","ems":84,"ffs":85,"cds":79,"ias":89,"cbs":87,"mes":82,"invalidation":"4450_break_or_DXY_US10Y_acceleration","verification_target":"GOLD_entry_24h_3d_5d_MFE_MAE_pullback_model","verified_status":"verified"},
{"date":"2026-08-23","signal_id":"20260823_BTC_BUY_PULLBACK","asset":"BTC","side":"BUY","rank":"B","type":"PULLBACK","entry_low":74200,"entry_high":76000,"sl":70400,"tp1":82500,"tp2":87000,"rr":1.65,"win_prob":0.63,"expected_r":0.43,"tq_score":99,"opp_score":73,"no_trade_score":43,"risk_pct":0.25,"regime":"BTC_ETF_FLOW_PRICE_CONFIRMATION_OVEREXTENDED","ems":84,"ffs":92,"cds":80,"ias":88,"cbs":88,"mes":88,"invalidation":"70400_break_or_ETF_flow_reversal","verification_target":"BTC_70k_74k_82k_ETF_3d_5d_MFE_MAE","verified_status":"partially_verified"},
{"date":"2026-08-23","signal_id":"20260823_ETH_BUY_PULLBACK","asset":"ETH","side":"BUY","rank":"B","type":"PULLBACK","entry_low":2240,"entry_high":2340,"sl":2050,"tp1":2700,"tp2":2920,"rr":1.74,"win_prob":0.60,"expected_r":0.39,"tq_score":97,"opp_score":68,"no_trade_score":49,"risk_pct":0.25,"regime":"ETH_ETF_FLOW_PRICE_CONFIRMATION_OVEREXTENDED","ems":76,"ffs":87,"cds":79,"ias":79,"cbs":80,"mes":80,"invalidation":"2050_break_or_ETH_ETF_flow_reversal","verification_target":"ETH_2.2k_2.6k_ETHBTC_ETF_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-23","signal_id":"20260823_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":15,"no_trade_score":99,"risk_pct":null,"regime":"HORMUZ_SUPPLY_SHOCK_SIX_DAY_RALLY","ems":91,"ffs":81,"cds":99,"ias":14,"cbs":56,"mes":80,"invalidation":"supply_shock_momentum_chase_prohibited","verification_target":"WTI_85_90_Hormuz_week_open_3d_5d","verified_status":"verified"},
{"date":"2026-08-23","signal_id":"20260823_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":90,"opp_score":37,"no_trade_score":91,"risk_pct":null,"regime":"USD_WEAK_BOJ_INTERVENTION_CONFLICT","ems":73,"ffs":77,"cds":90,"ias":38,"cbs":65,"mes":70,"invalidation":"160_intervention_BOJ_and_DXY_conflict","verification_target":"USDJPY_157_160_DXY_US10Y_3d","verified_status":"partially_verified"},
{"date":"2026-08-23","signal_id":"20260823_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":87,"opp_score":45,"no_trade_score":79,"risk_pct":null,"regime":"WEEKLY_EQUITY_PULLBACK_HIGH_YIELDS","ems":65,"ffs":72,"cds":81,"ias":50,"cbs":68,"mes":67,"invalidation":"ES_multi_day_stabilization_and_US10Y_decline_required","verification_target":"ES_US10Y_VIX_week_open_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-23","signal_id":"20260823_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":92,"opp_score":39,"no_trade_score":86,"risk_pct":null,"regime":"TECH_WEEKLY_PULLBACK_HIGH_TERM_PREMIUM","ems":61,"ffs":71,"cds":86,"ias":43,"cbs":64,"mes":64,"invalidation":"NQ_stabilization_and_long_yield_relief_required","verification_target":"NQ_US10Y_SOX_week_open_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-23","signal_id":"20260823_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":93,"opp_score":34,"no_trade_score":92,"risk_pct":null,"regime":"USD_DEBASEMENT_EXTENDED","ems":78,"ffs":83,"cds":90,"ias":33,"cbs":69,"mes":79,"invalidation":"DXY_reclaim_100_or_confirm_break_below_98_required","verification_target":"DXY_98_100_US10Y_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-23","signal_id":"20260823_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":22,"no_trade_score":98,"risk_pct":null,"regime":"FISCAL_TERM_PREMIUM_BUYBACK_CONFLICT","ems":86,"ffs":91,"cds":98,"ias":21,"cbs":75,"mes":87,"invalidation":"confirmed_break_below_4.60_or_above_4.75_required","verification_target":"US10Y_4.60_4.75_week_open_3d_5d","verified_status":"verified"},
{"date":"2026-08-23","signal_id":"20260823_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":79,"opp_score":43,"no_trade_score":79,"risk_pct":null,"regime":"VOL_RELIEF_WEEKLY_EQUITY_WEAKNESS","ems":65,"ffs":64,"cds":77,"ias":58,"cbs":66,"mes":62,"invalidation":"VIX_above_17_or_below_14_confirms_next_regime","verification_target":"VIX_14_17_ES_NQ_week_open_3d","verified_status":"partially_verified"}
]
```

**8月23日の更新点は、BTC/ETHのB判定を裏付ける需給証拠がかなり強くなったことです。** ETF週間流入がBTC約19億ドル、ETH約6.97億ドルまで確定し、出来高も3倍超へ増加しました。これは直近の上昇がショートカバーだけでは説明しにくいことを示します。citeturn693056news0turn693056news62

それでも本日の実行方針は変わらず、**GOLD 4630超、BTC 76000超、ETH 2340超なら追わずNO_FILL**です。
