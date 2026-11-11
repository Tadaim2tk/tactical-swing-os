<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-08-27 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 14519 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026年8月27日

データ基準は**8月26日米国市場終了後～8月27日06:58 JST前後**。10資産すべて新規取得を試みています。ES/NQは先物系列を優先し、取得できない箇所では現物指数を方向確認だけに使用しました。GOLDはCOMEX限月差が残るため `partially_verified` とします。

26日の最大イベントはNvidia決算です。売上高**962.2億ドル**、調整EPS **2.22ドル**はいずれも市場予想を上回り、次四半期売上見通しも**1080億ドル vs 市場予想1041.9億ドル**。時間外では最終的に4%以上上昇しました。citeturn847714view1

ただしマクロ側は逆風です。7月PCEは前年比**3.7%**で予想3.6%を上回り、9月利上げ確率は約40%へ上昇。S&P500は7675.70（-0.02%）、NASDAQ総合は26130.20（-0.08%）でした。citeturn847714view0turn847714view3

---

## 1. 本日の結論

**A級：0件**

**B+：0件**

**B級：NASDAQ BUY、GOLD BUY、BTC BUY、ETH BUY**

**NO_TRADE：WTI、USDJPY、SPX、DXY、US10Y、VIX**

分析順位は、

**NASDAQ B > GOLD B > BTC B > ETH B**

です。

昨日までのNASDAQの最大障害だった**Nvidia決算イベントはポジティブに通過**しました。売上・利益・ガイダンスが揃って予想超過なので、NASDAQは今日からBUY監視へ戻します。citeturn847714view1

ただし**成行追随は禁止**。Nvidia時間外+4%を見た後なので、NQの押し目だけを対象にします。

また、今日の月次較正ルールは明記された**XM最小ロット損失1500円以内**をそのまま適用します。NASDAQ・GOLD・BTC・ETHはいずれも、実際のXM最小ロットでSL損失が1500円を超えるなら**Signal成立でも実取引NO_TRADE**です。

---

## 2. 前回判断の簡易検証

**NASDAQ NO_TRADEは成功**です。決算発表前にポジションを取らず、二値イベントを回避しました。その後Nvidiaは好決算で時間外+4%以上。結果を見てから新しいシグナルとして評価できます。citeturn847714view1

**GOLD B BUY**は方向が一旦逆行。26日の米金先物は日中**4673.90**まで低下し、現物金は4618ドル近辺、その後4590ドル台まで軟化しました。前回Entry 4610–4660への接近または到達は限月によって判定が変わるため、`ENTRY_TOUCH_PARTIALLY_VERIFIED` とします。citeturn844033view0

**BTC B BUY**は78～79k周辺で保ち合い。Bitcoinは26日に約79000ドルまで下げましたが、8月ETF流入は30億ドル超へ拡大しています。価格急騰は止まった一方、フローは崩れていません。citeturn844033news0

**ETH B BUY**も2460ドル近辺へ調整。ETFには25日も約1.80億ドルの流入が報告されており、価格調整と機関投資家フローの乖離が続いています。citeturn844033news2

WTI NO_TRADEも妥当でした。WTIは82.23ドルで終了し、Hormuz再開協議を受けて地政学プレミアムがさらに縮小しています。citeturn847714view2

---

## 3. 市場全体の前提

本日のRegimeは、

**`NVIDIA_BEAT / HOT_PCE / OIL_PREMIUM_UNWIND / CRYPTO_FLOW_SUPPORT / JACKSON_HOLE_AHEAD`**

です。

株式には相反する2要素があります。

**Nvidia好決算 → AI/Growthにプラス**

対して、

**PCE 3.7% → Fed利上げ確率上昇 → long-duration株にマイナス**

です。citeturn847714view1turn847714view3

したがってNASDAQをA級へ一気に戻すほどではありません。

原油ではIran/OmanがHormuz管理について協議を進め、WTIは82.23ドル。市場は「長期封鎖」より「部分再開」を価格へ織り込み始めています。ただし実際の通航船は火曜日にわずか5隻で、平常化したわけではありません。citeturn847714view2

ドル指数は**99.145**、USDJPYは**159.37**。BOJについては9月利上げ予想が強まっているため、USDJPY BUYは依然取りにくい状況です。citeturn847714view3turn589168news38

---

## 4. 10資産別判断

| 資産 | 判定 | 要点 |
|---|---|---|
| GOLD | **B BUY** | 押し目形成。ただしPCE高止まりが逆風 |
| BTC | **B BUY** | ETF流入継続、80–82k抵抗 |
| ETH | **B BUY** | ETF流入＋押し目形成 |
| WTI | **NO_TRADE** | Hormuzプレミアム縮小中で方向転換局面 |
| USDJPY | **NO_TRADE** | Fed/BOJ/介入要因が衝突 |
| SPX | **NO_TRADE** | Nvidia恩恵よりNASDAQの方が純度高い |
| NASDAQ | **B BUY** | Nvidia決算成功、押し目限定で再開 |
| DXY | **NO_TRADE** | Hot PCEで上昇も追随余地不足 |
| US10Y | **NO_TRADE** | PCEとTreasury介入の綱引き |
| VIX | **NO_TRADE** | 低ボラ、方向シグナルより確認系列 |

---

## 5. A級候補

**0件です。**

NASDAQはモデル上、

**CBS 79  
EMS 74  
expected_r 0.46  
MAE想定 0.24R**

まで回復しました。

つまり**市場モデルだけならA水準**です。

しかし追加条件の**XM最小ロット損失1500円以内**を満たす確認がなく、NQの必要SL幅を考えると実際には超過する可能性が高い。

したがって**A認定はしません**。

これは重要で、

**Forecast quality = A近似  
Trade executability = NO**

という状態です。

---

## 6. B級監視候補

### 1位 NASDAQ — BUY PULLBACK

**Entry 29100–29400  
SL 28450  
TP1 30600  
TP2 31400  
RR 1.69  
win_prob 0.64  
expected_r 0.46  
MAE 0.24R  
risk_pct 0.25%**

Nvidia決算は明確なプラス確認です。売上96.22B、次四半期見通し108B、時間外+4%以上。citeturn847714view1

ただしNQが決算後に上へギャップした場合は追いません。

**29100–29400へ戻って維持した場合だけBUY候補。**

XM最小ロット＋SL28450の損失が1500円を超えるなら、**実取引NO_TRADE**です。

### 2位 GOLD — BUY PULLBACK

**Entry 4560–4620  
SL 4440  
TP1 4860  
TP2 5000  
RR 1.67  
win_prob 0.62  
expected_r 0.40  
MAE 0.29R  
risk_pct 0.25%**

26日は金が調整し、伸び切った状態はかなり解消されました。ただしHot PCEとドル反発が逆風です。米金先物は日中4673.90、現物は4618付近まで低下しました。citeturn844033view0turn847714view3

昨日よりスコアを少し落とします。

### 3位 BTC — BUY PULLBACK

**Entry 76500–79000  
SL 72500  
TP1 85000  
TP2 89000  
RR 1.50  
win_prob 0.62  
expected_r 0.40  
MAE 0.31R  
risk_pct 0.25%**

Bitcoinは約79kまで調整した一方、8月ETF流入は30億ドル超。25日にも約3.14億ドル流入しています。citeturn844033news0turn844033news2

80～82k突破失敗は減点ですが、フローがまだ支えています。

### 4位 ETH — BUY PULLBACK

**Entry 2380–2470  
SL 2160  
TP1 2800  
TP2 3000  
RR 1.55  
win_prob 0.59  
expected_r 0.37  
MAE 0.33R  
risk_pct 0.25%**

ETHは約2460まで調整。一方25日のスポットETFは約**+179.8M**。citeturn844033news2

価格の過熱解消は進んでいますが、BTCより変動幅が大きいため4位です。

---

## 7. 触らない資産

今日は**WTIを新たにSELLしない**ことが重要です。

87ドル台から82ドル台まで地政学プレミアムが急速に剥落しましたが、Hormuzの実通航量はまだ平常時を大きく下回ります。citeturn847714view2

したがって、

**BUY＝旧供給ショック追随  
SELL＝和平期待追随**

の両方になりやすい。

USDJPYも159.37でNO_TRADE。米インフレはドル高材料ですが、BOJ9月利上げ予想と過去の協調介入リスクが反対方向です。citeturn847714view3turn589168news38

---

## 8. 後日検証ポイント

最重要は**NASDAQのNvidia後反応**です。

今回、

**決算前NO_TRADE  
→ Nvidia EPS/売上/Guidance beat  
→ 時間外+4%**

となりました。citeturn847714view1

これから、

**NQ寄り付き  
→ 1h  
→ 米国終値  
→ +1d  
→ +3d  
→ +5d**

を追跡します。

特に、

**好決算なのにNQが29400以上を維持できない**

場合、AI期待値が既に高過ぎるというnegative evidenceになります。

BTCではもう一つ重要な検証が始まっています。

**ETF流入継続  
＋価格80–82k突破失敗**

です。ETFフローが強くても価格が上がらなければ、再び `FLOW_TO_PRICE_FAILURE` が発生したことになります。citeturn844033news0turn844033news2

---

## 9. Obsidian保存用Observation Draft

```markdown
# 2026-08-27 Nvidia Beat / Nasdaq Re-entry Watch

## Regime

NVIDIA_BEAT
HOT_PCE
OIL_PREMIUM_UNWIND
CRYPTO_FLOW_SUPPORT
JACKSON_HOLE_AHEAD

## Nvidia

Revenue:
96.22bn
vs 92.17bn expected

Adjusted EPS:
2.22
vs 2.10 expected

Next-quarter revenue:
108bn
vs 104.19bn expected

After-hours:
> +4%

Interpretation:
AI demand thesis remains intact.

## Macro

July PCE:
3.7% YoY
vs 3.6% expected

Fed September hike probability:
~40%

DXY:
99.145

USDJPY:
159.37

WTI:
82.23

## Signals

A:
NONE

B:

NASDAQ BUY
29100-29400
SL 28450
TP1 30600

GOLD BUY
4560-4620
SL 4440
TP1 4860

BTC BUY
76500-79000
SL 72500
TP1 85000

ETH BUY
2380-2470
SL 2160
TP1 2800

NO_TRADE:

WTI
USDJPY
SPX
DXY
US10Y
VIX

## Execution

NASDAQ is model-A-like,
but broker executability prevents A classification
unless XM minimum-lot SL loss <=1500 JPY.

Do not chase Nvidia post-earnings gap.

## Research

Nvidia:
earnings beat -> NQ follow-through?

BTC:
ETF inflows -> 80-82k breakout or renewed flow-price failure?

WTI:
Hormuz reopening premium unwind

#TSO #NASDAQ #NVIDIA #GOLD #BTC #ETH
```

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-08-27,20260827_GOLD_BUY_PULLBACK,GOLD,BUY,B,PULLBACK,4560,4620,4440,4860,5000,1.67,0.62,0.40,94,73,42,0.25,GOLD_PULLBACK_HOT_PCE,76,82,80,76,79,78,4440_break_or_DXY_US10Y_acceleration,GOLD_entry_24h_3d_5d_MFE_MAE_contract_consistency,partially_verified
2026-08-27,20260827_BTC_BUY_PULLBACK,BTC,BUY,B,PULLBACK,76500,79000,72500,85000,89000,1.50,0.62,0.40,97,72,45,0.25,BTC_ETF_FLOW_80K_RESISTANCE,80,93,82,79,83,89,72500_break_or_ETF_flow_reversal,BTC_76k_80k_82k_85k_ETF_3d_5d_MFE_MAE,partially_verified
2026-08-27,20260827_ETH_BUY_PULLBACK,ETH,BUY,B,PULLBACK,2380,2470,2160,2800,3000,1.55,0.59,0.37,94,68,51,0.25,ETH_ETF_FLOW_PULLBACK,75,89,80,76,79,83,2160_break_or_ETH_ETF_flow_reversal,ETH_2.4k_2.8k_ETF_ETHBTC_3d_5d,partially_verified
2026-08-27,20260827_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,30,94,,HORMUZ_PREMIUM_UNWIND_TRANSITION,72,76,97,31,59,72,confirmed_Hormuz_reopening_or_supply_reescalation_required,WTI_80_85_Hormuz_transits_3d_5d,verified
2026-08-27,20260827_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,92,38,92,,HOT_PCE_BOJ_INTERVENTION_CONFLICT,76,79,91,37,67,74,clear_157_or_160_break_with_policy_confirmation_required,USDJPY_157_160_BOJ_DXY_US10Y_3d,verified
2026-08-27,20260827_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,84,57,68,,NVIDIA_POSITIVE_HOT_PCE_OFFSET,72,74,74,63,72,70,ES_followthrough_and_breadth_confirmation_required,ES_Nvidia_US10Y_VIX_1d_3d,verified
2026-08-27,20260827_NASDAQ_BUY_PULLBACK,NASDAQ,BUY,B,PULLBACK,29100,29400,28450,30600,31400,1.69,0.64,0.46,98,82,31,0.25,NVIDIA_BEAT_HOT_PCE_OFFSET,74,82,78,85,79,74,28450_break_or_post_Nvidia_followthrough_failure,NQ_29400_30600_Nvidia_SOX_US10Y_1d_3d_5d,partially_verified
2026-08-27,20260827_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,88,41,84,,HOT_PCE_DOLLAR_REBOUND_FISCAL_CONFLICT,75,79,85,43,68,75,clear_break_below_98_or_reclaim_100_required,DXY_98_100_JacksonHole_3d,verified
2026-08-27,20260827_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,94,36,90,,HOT_PCE_TREASURY_SUPPORT_CONFLICT,82,87,92,36,73,83,confirmed_break_below_4.60_or_above_4.75_required,US10Y_4.60_4.75_JacksonHole_3d_5d,partially_verified
2026-08-27,20260827_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,86,40,84,,POST_NVIDIA_LOW_VOL_EVENT_RISK,68,66,86,51,67,65,VIX_above_18_or_below_14_with_equity_confirmation,VIX_14_18_NQ_ES_JacksonHole_3d,partially_verified
```

### JSON

```json
[
{"date":"2026-08-27","signal_id":"20260827_GOLD_BUY_PULLBACK","asset":"GOLD","side":"BUY","rank":"B","type":"PULLBACK","entry_low":4560,"entry_high":4620,"sl":4440,"tp1":4860,"tp2":5000,"rr":1.67,"win_prob":0.62,"expected_r":0.40,"tq_score":94,"opp_score":73,"no_trade_score":42,"risk_pct":0.25,"regime":"GOLD_PULLBACK_HOT_PCE","ems":76,"ffs":82,"cds":80,"ias":76,"cbs":79,"mes":78,"invalidation":"4440_break_or_DXY_US10Y_acceleration","verification_target":"GOLD_entry_24h_3d_5d_MFE_MAE_contract_consistency","verified_status":"partially_verified"},
{"date":"2026-08-27","signal_id":"20260827_BTC_BUY_PULLBACK","asset":"BTC","side":"BUY","rank":"B","type":"PULLBACK","entry_low":76500,"entry_high":79000,"sl":72500,"tp1":85000,"tp2":89000,"rr":1.50,"win_prob":0.62,"expected_r":0.40,"tq_score":97,"opp_score":72,"no_trade_score":45,"risk_pct":0.25,"regime":"BTC_ETF_FLOW_80K_RESISTANCE","ems":80,"ffs":93,"cds":82,"ias":79,"cbs":83,"mes":89,"invalidation":"72500_break_or_ETF_flow_reversal","verification_target":"BTC_76k_80k_82k_85k_ETF_3d_5d_MFE_MAE","verified_status":"partially_verified"},
{"date":"2026-08-27","signal_id":"20260827_ETH_BUY_PULLBACK","asset":"ETH","side":"BUY","rank":"B","type":"PULLBACK","entry_low":2380,"entry_high":2470,"sl":2160,"tp1":2800,"tp2":3000,"rr":1.55,"win_prob":0.59,"expected_r":0.37,"tq_score":94,"opp_score":68,"no_trade_score":51,"risk_pct":0.25,"regime":"ETH_ETF_FLOW_PULLBACK","ems":75,"ffs":89,"cds":80,"ias":76,"cbs":79,"mes":83,"invalidation":"2160_break_or_ETH_ETF_flow_reversal","verification_target":"ETH_2.4k_2.8k_ETF_ETHBTC_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-27","signal_id":"20260827_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":30,"no_trade_score":94,"risk_pct":null,"regime":"HORMUZ_PREMIUM_UNWIND_TRANSITION","ems":72,"ffs":76,"cds":97,"ias":31,"cbs":59,"mes":72,"invalidation":"confirmed_Hormuz_reopening_or_supply_reescalation_required","verification_target":"WTI_80_85_Hormuz_transits_3d_5d","verified_status":"verified"},
{"date":"2026-08-27","signal_id":"20260827_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":92,"opp_score":38,"no_trade_score":92,"risk_pct":null,"regime":"HOT_PCE_BOJ_INTERVENTION_CONFLICT","ems":76,"ffs":79,"cds":91,"ias":37,"cbs":67,"mes":74,"invalidation":"clear_157_or_160_break_with_policy_confirmation_required","verification_target":"USDJPY_157_160_BOJ_DXY_US10Y_3d","verified_status":"verified"},
{"date":"2026-08-27","signal_id":"20260827_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":84,"opp_score":57,"no_trade_score":68,"risk_pct":null,"regime":"NVIDIA_POSITIVE_HOT_PCE_OFFSET","ems":72,"ffs":74,"cds":74,"ias":63,"cbs":72,"mes":70,"invalidation":"ES_followthrough_and_breadth_confirmation_required","verification_target":"ES_Nvidia_US10Y_VIX_1d_3d","verified_status":"verified"},
{"date":"2026-08-27","signal_id":"20260827_NASDAQ_BUY_PULLBACK","asset":"NASDAQ","side":"BUY","rank":"B","type":"PULLBACK","entry_low":29100,"entry_high":29400,"sl":28450,"tp1":30600,"tp2":31400,"rr":1.69,"win_prob":0.64,"expected_r":0.46,"tq_score":98,"opp_score":82,"no_trade_score":31,"risk_pct":0.25,"regime":"NVIDIA_BEAT_HOT_PCE_OFFSET","ems":74,"ffs":82,"cds":78,"ias":85,"cbs":79,"mes":74,"invalidation":"28450_break_or_post_Nvidia_followthrough_failure","verification_target":"NQ_29400_30600_Nvidia_SOX_US10Y_1d_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-27","signal_id":"20260827_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":88,"opp_score":41,"no_trade_score":84,"risk_pct":null,"regime":"HOT_PCE_DOLLAR_REBOUND_FISCAL_CONFLICT","ems":75,"ffs":79,"cds":85,"ias":43,"cbs":68,"mes":75,"invalidation":"clear_break_below_98_or_reclaim_100_required","verification_target":"DXY_98_100_JacksonHole_3d","verified_status":"verified"},
{"date":"2026-08-27","signal_id":"20260827_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":94,"opp_score":36,"no_trade_score":90,"risk_pct":null,"regime":"HOT_PCE_TREASURY_SUPPORT_CONFLICT","ems":82,"ffs":87,"cds":92,"ias":36,"cbs":73,"mes":83,"invalidation":"confirmed_break_below_4.60_or_above_4.75_required","verification_target":"US10Y_4.60_4.75_JacksonHole_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-27","signal_id":"20260827_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":86,"opp_score":40,"no_trade_score":84,"risk_pct":null,"regime":"POST_NVIDIA_LOW_VOL_EVENT_RISK","ems":68,"ffs":66,"cds":86,"ias":51,"cbs":67,"mes":65,"invalidation":"VIX_above_18_or_below_14_with_equity_confirmation","verification_target":"VIX_14_18_NQ_ES_JacksonHole_3d","verified_status":"partially_verified"}
]
```

**8月27日の核心はNASDAQです。** Nvidia決算という最大の未知数がポジティブに解消されたため、昨日までのNO_TRADEから**B BUYへ復帰**させます。ただしHot PCEという逆風があるのでAまでは上げません。citeturn847714view1turn847714view0

実際に注文するなら、Nvidia時間外高を見てNQを追うのではなく、**29100–29400への押し＋そこでの下げ止まり**を待つのが本日のTSO判断です。
