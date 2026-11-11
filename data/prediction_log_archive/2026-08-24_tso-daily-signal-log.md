<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-08-24 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 13678 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026年8月24日

データ基準は**8月21日（金）米国市場終値＋8月24日06:58 JST前後の暗号資産・週末情報**です。ES/NQ・COMEX・WTI・DXY・US10Y・VIXは週明け直前で十分な同時刻価格を揃えられなかったため、金曜確定値を主アンカーとし `partially_verified` を使います。

BTCは複数ソースで現在約**76500～76600ドル**。ETHは最新記事で約**2449ドル**ですが、価格配信に大きな不整合があるためETHだけ特に検証度を落とします。BTC/ETHの米スポットETFは8月17～21日に合計約**26.2億ドル**の純流入で、2026年最大級の週次流入でした。citeturn331463news4turn331463news6turn719707news25turn719707news0

実取引の損失許容は、現在の運用上の**約3000円/回**を優先します。memcite

## 1. 本日の結論

**A級：0件**

**B+観察候補：GOLD BUY**

**B級：BTC BUY、ETH BUY**

**NO_TRADE：WTI、USDJPY、SPX、NASDAQ、DXY、US10Y、VIX**

本日の優先順位は、

**GOLD B+ > BTC B > ETH B**

です。

先週はNASDAQ-100が約-2.45%、S&P500が約-1.4%と株式が崩れた一方、Bitcoinは20%超、金は約5.6%上昇しました。つまり現在の中心テーマは全面Risk-onではなく、引き続き**Gold/Cryptoへの資金ローテーション**です。citeturn331463news67

ただしBTC/ETHはすでに大きく伸びています。本日も成行追随はしません。

---

## 2. 前回判断の簡易検証

**GOLD B BUY：方向成功継続。** 金は先週約5.6%上昇。前回Entry 4580–4630に対して現在は上側にいるため、実取引では `NO_FILL` 寄りです。citeturn331463news67

**BTC B BUY：監視帯上限付近。** 前回Entry 74200–76000に対し、現在約76500～76600。citeturn331463news4turn331463news6 週末に大きな崩れは起きておらず、70k台後半を維持しています。方向仮説は有効ですが、Entry上限を明確に上回れば追いません。

**ETH B BUY：方向成功継続。ただし価格検証品質低下。** 最新記事では約2449ドルまで上昇。ETF需要も継続しています。citeturn719707news0 一方、一部価格配信が明らかに古い値を返しているため、FILL判定は保留します。

**WTI NO_TRADE：維持成功。** WTIは金曜87.06、Brent94.39。Hormuz通航制約と対イラン制裁懸念が主因であり、通常テクニカルよりheadline riskが支配的です。citeturn331463news68

---

## 3. 市場全体の前提

本日のRegime：

**`HARD_ASSET_ROTATION / CRYPTO_ETF_FLOW_CONFIRMED / HIGH_TERM_PREMIUM / OIL_SUPPLY_PREMIUM / EQUITY_REPAIR_UNCONFIRMED`**

先週末時点で米株は小幅反発しましたが、週間ではS&P500 -1.43%、NASDAQ -2.05%。長期金利と原油高が株式、とくにGrowthに重石です。citeturn719707news72turn719707news73

一方でBitcoin・Gold・Crypto関連株は明確に上昇。BTC ETFへの大規模流入は価格上昇と同時発生しており、従来の`FLOW_TO_PRICE_FAILURE`はかなり明確に解消しました。citeturn719707news75turn719707news26

今週は**Nvidia決算、PCE、Jackson HoleでのFed発言**が株式・金利regimeの主要確認材料です。citeturn331463news67turn719707news72

---

## 4. 10資産別判断

| 資産 | 判定 | 要点 |
|---|---|---|
| GOLD | **B+ BUY** | Hard-asset相対強度最良。押し目限定 |
| BTC | **B BUY** | ETF＋価格確認。ただし伸び過ぎ |
| ETH | **B BUY** | ETF＋価格確認。価格データ不整合あり |
| WTI | **NO_TRADE** | Hormuz供給プレミアム |
| USDJPY | **NO_TRADE** | 160近辺リスクと米金利・BOJが競合 |
| SPX | **NO_TRADE** | 金曜反発だけでは週間下落を覆せない |
| NASDAQ | **NO_TRADE** | 高長期金利＋Nvidiaイベント前 |
| DXY | **NO_TRADE** | ドル弱含み後、追随SELLの位置ではない |
| US10Y | **NO_TRADE** | 財政term premiumと政策介入の衝突 |
| VIX | **NO_TRADE** | 方向性より株式regime確認用 |

---

## 5. A級候補

**0件。**

最も近いGOLDでも、

**CBS 88  
EMS 84  
win_prob 0.65  
expected_r 0.44  
MAE 0.27R**

です。

AのCBS/EMS条件は十分ですが、`expected_r>=0.45` と `MAE<=0.25R` を同時には満たしません。

BTCは需給面では非常に強いものの、週間20%超上昇後なのでMAE想定を0.30Rとします。

---

## 6. B級監視候補

### GOLD — **B+ BUY PULLBACK**

**Entry 4580–4640  
SL 4460  
TP1 4940  
TP2 5100  
RR 2.00  
win_prob 0.65  
較正参考 0.68  
expected_r 0.44  
MAE 0.27R  
risk 0.25%**

CBS88、EMS84、RR2.0、win_prob0.65でB+品質です。

XM最小ロット＋SL4460で**想定損失3000円以内なら実取引候補**。4640より上なら追いません。

### BTC — B BUY PULLBACK

**Entry 74200–76000  
SL 70400  
TP1 82500  
TP2 87000  
RR 1.65  
win_prob 0.63  
expected_r 0.43  
MAE 0.30R  
risk 0.25%**

現在約76500～76600。citeturn331463news4turn331463news6

したがって**現状はEntry帯のすぐ上**です。76000以下へ戻れば監視、上へ走ればNO_FILL。

ETF需給は強く、米スポットBTC/ETH ETF合計で先週約26.2億ドル流入。citeturn719707news25

ただしXM最小ロット＋SL70400で3000円を超える場合、**Signal=B / Execution=NO_TRADE**です。

### ETH — B BUY PULLBACK

**Entry 2280–2380  
SL 2080  
TP1 2760  
TP2 2960  
RR 1.72  
win_prob 0.60  
expected_r 0.39  
MAE 0.33R  
risk 0.25%**

最新記事ではETH約2449。米ETH ETFには5日間で約6.93億ドル流入との報告があります。citeturn719707news0

価格自体は強いですが、現在値から追いません。

---

## 7. 触らない資産

**WTIが最優先NO_TRADE。** 金曜WTI87.06、Brent94.39。Hormuzの輸送量は依然通常を大幅に下回り、イラン関連の政治ヘッドライン一つで数ドル動き得ます。citeturn331463news68

**NASDAQもまだ触りません。** 先週NASDAQ-100は約-2.45%。今週はNvidia決算が控え、高い長期金利と合わせてイベント依存度が大きすぎます。citeturn331463news67

---

## 8. 後日検証ポイント

今週最重要なのは3つです。

**① BTC/ETH ETFフローが価格へ定着するか。** BTCは75k以上、ETHは2.3k以上を数日維持できるか確認します。先週のBTC/ETH ETF合計約26.2億ドル流入は非常に強い教師データです。citeturn719707news25

**② GOLDのEntry未到達問題。** 方向判定は良い一方、Deep Pullbackを待ってNO_FILLになる例が増えています。Shallow Pullback仮想Entryを並行記録します。

**③ 株式regime。** Nvidia決算＋PCE＋Jackson Hole後に、NASDAQが再び金利低下へ正反応するかを確認。反応が戻れば再BUY候補、戻らなければGrowthモデルのregime変更を強化します。citeturn331463news67turn719707news72

---

## 9. Obsidian保存用Observation Draft

```markdown
# 2026-08-24 Hard Asset Rotation Continues

## Regime

HARD_ASSET_ROTATION
CRYPTO_ETF_FLOW_CONFIRMED
HIGH_TERM_PREMIUM
OIL_SUPPLY_PREMIUM
EQUITY_REPAIR_UNCONFIRMED

## Weekend / Monday anchors

BTC:
~76500-76600

ETH:
~2449
price verification partially inconsistent

WTI Friday:
87.06

Brent:
94.39

Equity weekly:
S&P500 -1.43%
NASDAQ ~-2.05%
NASDAQ100 ~-2.45%

Bitcoin:
weekly >20%

Gold:
weekly ~+5.6%

## Crypto flows

BTC + ETH spot ETF weekly inflow:
~2.62bn USD

Flow-price confirmation remains strong.

## Signals

A:
NONE

B+:
GOLD BUY
4580-4640
SL 4460
TP1 4940

B:
BTC BUY
74200-76000
SL 70400
TP1 82500

ETH BUY
2280-2380
SL 2080
TP1 2760

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

GOLD >4640:
NO_FILL

BTC >76000:
NO_FILL

ETH >2380:
NO_FILL

XM minimum-lot loss:
operational limit ~3000 JPY

## Week catalysts

Nvidia earnings
PCE
Jackson Hole / Fed communication

## Research

BTC FLOW_TO_PRICE persistence
ETH FLOW_TO_PRICE persistence
GOLD shallow-vs-deep pullback
NASDAQ high-yield regime response

#TSO #GOLD #BTC #ETH #NASDAQ
```

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-08-24,20260824_GOLD_BUY_PULLBACK,GOLD,BUY,B,PULLBACK,4580,4640,4460,4940,5100,2.00,0.65,0.44,98,78,32,0.25,HARD_ASSET_ROTATION_GOLD_STRENGTH,84,86,79,90,88,84,4460_break_or_DXY_US10Y_acceleration,GOLD_entry_24h_3d_5d_MFE_MAE_pullback_model,partially_verified
2026-08-24,20260824_BTC_BUY_PULLBACK,BTC,BUY,B,PULLBACK,74200,76000,70400,82500,87000,1.65,0.63,0.43,99,74,42,0.25,BTC_ETF_FLOW_PRICE_CONFIRMATION_EXTENDED,85,93,80,89,88,89,70400_break_or_ETF_flow_reversal,BTC_70k_75k_82k_ETF_3d_5d_MFE_MAE,verified
2026-08-24,20260824_ETH_BUY_PULLBACK,ETH,BUY,B,PULLBACK,2280,2380,2080,2760,2960,1.72,0.60,0.39,96,69,49,0.25,ETH_ETF_FLOW_PRICE_CONFIRMATION_EXTENDED,77,88,78,80,81,81,2080_break_or_ETH_ETF_flow_reversal,ETH_2.3k_2.7k_ETHBTC_ETF_3d_5d,partially_verified
2026-08-24,20260824_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,14,99,,HORMUZ_SUPPLY_PREMIUM,92,82,99,13,56,81,supply_shock_momentum_chase_prohibited,WTI_85_90_Hormuz_3d_5d,verified
2026-08-24,20260824_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,90,37,91,,USDJPY_POLICY_INTERVENTION_CONFLICT,73,77,90,38,65,70,160_intervention_BOJ_and_US_yield_conflict,USDJPY_157_160_DXY_US10Y_3d,partially_verified
2026-08-24,20260824_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,88,44,81,,EQUITY_WEEKLY_PULLBACK_HIGH_YIELDS,65,73,82,49,68,67,multi_day_ES_stabilization_and_yield_relief_required,ES_US10Y_VIX_Nvidia_PCE_1d_3d,partially_verified
2026-08-24,20260824_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,94,36,89,,TECH_PULLBACK_NVIDIA_HIGH_TERM_PREMIUM,60,72,89,39,63,64,NQ_stabilization_Nvidia_confirmation_and_yield_relief_required,NQ_Nvidia_US10Y_SOX_1d_3d,partially_verified
2026-08-24,20260824_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,93,35,91,,USD_DEBASEMENT_EXTENDED,78,83,90,34,69,79,DXY_reclaim_100_or_confirm_break_below_98_required,DXY_98_100_US10Y_PCE_3d,partially_verified
2026-08-24,20260824_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,22,98,,FISCAL_TERM_PREMIUM_POLICY_CONFLICT,86,91,98,21,75,87,confirmed_break_below_4.60_or_above_4.75_required,US10Y_4.60_4.75_PCE_JacksonHole_3d_5d,verified
2026-08-24,20260824_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,80,42,80,,VOL_RELIEF_EQUITY_WEEKLY_WEAKNESS,65,64,78,57,66,62,VIX_above_17_or_below_14_confirms_next_regime,VIX_14_17_ES_NQ_Nvidia_3d,partially_verified
```

### JSON

```json
[
{"date":"2026-08-24","signal_id":"20260824_GOLD_BUY_PULLBACK","asset":"GOLD","side":"BUY","rank":"B","type":"PULLBACK","entry_low":4580,"entry_high":4640,"sl":4460,"tp1":4940,"tp2":5100,"rr":2.00,"win_prob":0.65,"expected_r":0.44,"tq_score":98,"opp_score":78,"no_trade_score":32,"risk_pct":0.25,"regime":"HARD_ASSET_ROTATION_GOLD_STRENGTH","ems":84,"ffs":86,"cds":79,"ias":90,"cbs":88,"mes":84,"invalidation":"4460_break_or_DXY_US10Y_acceleration","verification_target":"GOLD_entry_24h_3d_5d_MFE_MAE_pullback_model","verified_status":"partially_verified"},
{"date":"2026-08-24","signal_id":"20260824_BTC_BUY_PULLBACK","asset":"BTC","side":"BUY","rank":"B","type":"PULLBACK","entry_low":74200,"entry_high":76000,"sl":70400,"tp1":82500,"tp2":87000,"rr":1.65,"win_prob":0.63,"expected_r":0.43,"tq_score":99,"opp_score":74,"no_trade_score":42,"risk_pct":0.25,"regime":"BTC_ETF_FLOW_PRICE_CONFIRMATION_EXTENDED","ems":85,"ffs":93,"cds":80,"ias":89,"cbs":88,"mes":89,"invalidation":"70400_break_or_ETF_flow_reversal","verification_target":"BTC_70k_75k_82k_ETF_3d_5d_MFE_MAE","verified_status":"verified"},
{"date":"2026-08-24","signal_id":"20260824_ETH_BUY_PULLBACK","asset":"ETH","side":"BUY","rank":"B","type":"PULLBACK","entry_low":2280,"entry_high":2380,"sl":2080,"tp1":2760,"tp2":2960,"rr":1.72,"win_prob":0.60,"expected_r":0.39,"tq_score":96,"opp_score":69,"no_trade_score":49,"risk_pct":0.25,"regime":"ETH_ETF_FLOW_PRICE_CONFIRMATION_EXTENDED","ems":77,"ffs":88,"cds":78,"ias":80,"cbs":81,"mes":81,"invalidation":"2080_break_or_ETH_ETF_flow_reversal","verification_target":"ETH_2.3k_2.7k_ETHBTC_ETF_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-24","signal_id":"20260824_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":14,"no_trade_score":99,"risk_pct":null,"regime":"HORMUZ_SUPPLY_PREMIUM","ems":92,"ffs":82,"cds":99,"ias":13,"cbs":56,"mes":81,"invalidation":"supply_shock_momentum_chase_prohibited","verification_target":"WTI_85_90_Hormuz_3d_5d","verified_status":"verified"},
{"date":"2026-08-24","signal_id":"20260824_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":90,"opp_score":37,"no_trade_score":91,"risk_pct":null,"regime":"USDJPY_POLICY_INTERVENTION_CONFLICT","ems":73,"ffs":77,"cds":90,"ias":38,"cbs":65,"mes":70,"invalidation":"160_intervention_BOJ_and_US_yield_conflict","verification_target":"USDJPY_157_160_DXY_US10Y_3d","verified_status":"partially_verified"},
{"date":"2026-08-24","signal_id":"20260824_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":88,"opp_score":44,"no_trade_score":81,"risk_pct":null,"regime":"EQUITY_WEEKLY_PULLBACK_HIGH_YIELDS","ems":65,"ffs":73,"cds":82,"ias":49,"cbs":68,"mes":67,"invalidation":"multi_day_ES_stabilization_and_yield_relief_required","verification_target":"ES_US10Y_VIX_Nvidia_PCE_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-24","signal_id":"20260824_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":94,"opp_score":36,"no_trade_score":89,"risk_pct":null,"regime":"TECH_PULLBACK_NVIDIA_HIGH_TERM_PREMIUM","ems":60,"ffs":72,"cds":89,"ias":39,"cbs":63,"mes":64,"invalidation":"NQ_stabilization_Nvidia_confirmation_and_yield_relief_required","verification_target":"NQ_Nvidia_US10Y_SOX_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-24","signal_id":"20260824_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":93,"opp_score":35,"no_trade_score":91,"risk_pct":null,"regime":"USD_DEBASEMENT_EXTENDED","ems":78,"ffs":83,"cds":90,"ias":34,"cbs":69,"mes":79,"invalidation":"DXY_reclaim_100_or_confirm_break_below_98_required","verification_target":"DXY_98_100_US10Y_PCE_3d","verified_status":"partially_verified"},
{"date":"2026-08-24","signal_id":"20260824_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":22,"no_trade_score":98,"risk_pct":null,"regime":"FISCAL_TERM_PREMIUM_POLICY_CONFLICT","ems":86,"ffs":91,"cds":98,"ias":21,"cbs":75,"mes":87,"invalidation":"confirmed_break_below_4.60_or_above_4.75_required","verification_target":"US10Y_4.60_4.75_PCE_JacksonHole_3d_5d","verified_status":"verified"},
{"date":"2026-08-24","signal_id":"20260824_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":80,"opp_score":42,"no_trade_score":80,"risk_pct":null,"regime":"VOL_RELIEF_EQUITY_WEEKLY_WEAKNESS","ems":65,"ffs":64,"cds":78,"ias":57,"cbs":66,"mes":62,"invalidation":"VIX_above_17_or_below_14_confirms_next_regime","verification_target":"VIX_14_17_ES_NQ_Nvidia_3d","verified_status":"partially_verified"}
]
```

**8月24日の実務上の第一候補はGOLDです。** BTC/ETHよりも価格の過熱度が低く、RRも2.0を確保できます。ただし4640より上なら追わず、BTCも76000以下、ETHも2380以下への正常な押しが来なければ、すべてNO_FILLで構いません。
