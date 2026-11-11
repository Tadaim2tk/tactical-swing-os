<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-08-30 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 12787 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-08-30

基準時点は**8月30日07:00 JST前後**。日曜のためGOLD・WTI・USDJPY・ES・NQ・DXY・US10Y・VIXは**8月28日金曜終値**、BTC/ETHのみ週末現物を新規確認しています。

## 1. 本日の結論

**A級：0件 / B級：0件 / 10資産すべてNO_TRADE**とします。

昨日まで残していた**BTC B+、ETH Bを本日は停止**します。最大の理由は価格下落そのものではなく、日曜でETFフローとCME価格形成が停止しており、金曜のWarsh発言による**米金利上方再評価を週末cryptoだけで吸収できたと判定できない**ためです。

特にBTCは約**78259ドル**まで低下し、昨日の77000–79000 Entry帯には入りました。しかし、これは「待っていた良い押し目が来た」と即断しません。ETHは約**2450–2458ドル**で、こちらも監視Entry帯2380–2460に入っています。citeturn251055news75turn874262search1

**今日の方針は「Entry帯到達 ≠ 自動約定」。月曜のNQ・US10Y・DXY・BTC CME再開を見てから判断**です。

---

## 2. 前回判断の簡易検証

### BTC B+ BUY → **Entry到達。ただし新規停止**

前回：

**Entry 77000–79000 / SL 73000 / TP1 85000**

現在BTCは約78259。価格だけ見ればEntry条件を満たしました。citeturn251055news75

しかし前回から追加された情報は、

- 金曜の米10年債利回り **4.73%**
- 2年債 **4.34%**
- Warsh発言前35%だった9月利上げ確率が一時**60%**
- DXYが約**99.5～99.7**
- BTCが80k台を維持できず78k台へ後退

です。Warsh発言を受け、米2年・10年金利とドルが上昇しました。citeturn217324view3turn251055news52turn251055news42

よって、

**PRICE_ENTRY_TOUCH = YES**  
**THESIS_CONFIRMATION = NO**

とします。

### ETH B → **Entry到達。ただし停止**

ETHは約2450～2458で、2380–2460のEntry帯上端に入りました。24時間では小幅反発ですが、8月28日の下落を十分取り戻していません。citeturn874262search1turn874262search9

BTCと同様、月曜のクロスアセット確認待ちです。

### NASDAQ NO_TRADE → **妥当**

金曜のNQ先物は約**29509.50、-0.6%**、Nasdaq-100現物は**29433.43、-0.70%**。一方でVIXは**14.43**までむしろ低下しました。citeturn874262search8turn874262search7turn874262search4

つまり今のところ、

**金利ショックはあるが、全面的risk-offではない**

という状態です。

NASDAQ BUY仮説を完全棄却する材料でもありませんが、再開確認もありません。

---

## 3. 市場全体の前提

本日のRegimeを

**`WEEKEND_CONFIRMATION_GAP / HAWKISH_FED_REPRICING / LOW_VIX_HIGH_YIELD_DIVERGENCE / CRYPTO_ENTRY_TOUCH_UNCONFIRMED`**

とします。

金曜時点で米10年債は**4.73%**。Warsh発言によって市場は明確にFedをタカ派方向へ再評価しました。citeturn251055news52turn217324view3

ところがVIXは**14.43**で低位のままです。citeturn874262search4

これは、

**債券市場＝警戒  
株式volatility＝まだ平静**

という不一致です。

月曜日にこのどちらへ収束するかが次のトレードを決めます。

WTIは**83.40**で終了し、週間では**-4.2%**。Hormuz経由の供給回復期待とFed引き締め懸念が下押ししました。ただし輸送量は依然不安定で、headline反転リスクが高いためSELLも追いません。citeturn217324view1

USDJPYは金曜NY終盤で約**160.1～160.2**。金利差ならBUYですが、介入警戒水準なので追随禁止です。citeturn990876search0turn990876search2

---

## 4. 10資産別判断

| 資産 | 本日 | 仮説状態 |
|---|---|---|
| GOLD | **NO_TRADE** | 長期BUY生存、短期BUY停止 |
| BTC | **NO_TRADE** | Entry到達、月曜確認待ち |
| ETH | **NO_TRADE** | Entry到達、BTC連動確認待ち |
| WTI | **NO_TRADE** | headline regime継続 |
| USDJPY | **NO_TRADE** | Fed BUY要因 vs 介入リスク |
| SPX | **NO_TRADE** | 金利吸収確認待ち |
| NASDAQ | **NO_TRADE** | AI仮説生存、短期再開待ち |
| DXY | **NO_TRADE** | タカ派上昇を追わない |
| US10Y | **NO_TRADE** | 4.73%まで上昇後 |
| VIX | **NO_TRADE** | 14.43、確認系列 |

---

## 5. A級候補

**なし。**

NASDAQの中期AI仮説はまだ生きています。しかし現在、

**NQ↓ + US10Y↑ + DXY↑**

なのでA条件には戻せません。

月曜に、

**US10Y ≤ 4.73%で安定  
NQが金曜安値を維持  
VIXが18未満  
半導体が相対的に回復**

まで揃えばBUY再評価です。

---

## 6. B級監視候補

**今日は正式なB級を出しません。**

ただし月曜再評価の優先順位は、

**BTC → NASDAQ → ETH → GOLD**

です。

BTC 77–79kとETH 2380–2460は価格だけなら魅力的です。しかしBTCについてはユーザールール通り、**ETF/CME根拠が週末で更新不能なためNO_TRADE優先**を適用します。

特に今回は「指値を入れて放置」より、**月曜確認後の多少高いEntryを許容する方が期待損失を抑えられる**と判断します。

---

## 7. 触らない資産

最も触らないのは**USDJPYとWTI**。

USDJPYは160円台まで戻っています。Fedだけなら上方向ですが、直近の大規模円買い介入後であり、週明けgapを含めリターン分布が非対称です。citeturn990876search3turn990876search0

WTIも83.40まで下がっていますが、Hormuzの物理フローは完全正常化しておらず、金曜時点でも通航数が過去平均を下回っています。週末headline一本で数ドル戻せるため、SELLも不適切です。citeturn217324view1

---

## 8. 後日検証ポイント

月曜の最重要観測セットは、

**NQ / ES / US10Y / DXY / VIX / BTC CME / BTC spot**

です。

判定条件は単純化します。

**ケースA：**
US10Y低下・DXY低下・NQ上昇  
→ NASDAQ BUY再開、BTC/ETHもBUY再評価。

**ケースB：**
US10Y高止まりでもNQ横ばい以上  
→ AI相対強度を評価。NASDAQ B候補。

**ケースC：**
US10Y↑・DXY↑・NQ↓・BTC<77000  
→ リスク資産BUY仮説をさらに格下げ。

BTCでは**77000を守るか**が最重要です。73000までは従来SL候補ですが、77000を明確に割るなら月曜時点で新規BUYの質はかなり低下します。

---

## 9. Obsidian保存用Observation Draft

```markdown
# 2026-08-30 Weekend Confirmation Gap

## Regime
WEEKEND_CONFIRMATION_GAP
HAWKISH_FED_REPRICING
LOW_VIX_HIGH_YIELD_DIVERGENCE
CRYPTO_ENTRY_TOUCH_UNCONFIRMED

## Friday references
NQ futures:
~29509.50
-0.6%

ES futures:
~7724.75
-0.2%

US10Y:
4.73%

DXY:
~99.5-99.7

VIX:
14.43

WTI:
83.40
weekly -4.2%

USDJPY:
~160.1-160.2

## Weekend crypto
BTC:
~78259

ETH:
~2450-2458

Both prior BUY entry zones touched.

Important:
ENTRY_TOUCH != TRADE_TRIGGER

Reason:
ETF and CME confirmation unavailable on weekend
Fed repricing not yet tested in Monday cross-asset trade

## Decision
A:
NONE

B:
NONE

NO_TRADE:
GOLD
BTC
ETH
WTI
USDJPY
SPX
NASDAQ
DXY
US10Y
VIX

## Monday priority
1 BTC
2 NASDAQ
3 ETH
4 GOLD

## Reactivation
US10Y stabilizes
DXY stops rising
NQ holds Friday low
BTC holds 77000 with CME confirmation

#TSO #Weekend #NASDAQ #BTC #Fed
```

## 10. TSO_LOG CSV / JSON

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-08-30,20260830_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,91,41,84,,HAWKISH_FED_WEEKEND_CONFIRMATION,78,82,90,40,65,80,US10Y_and_DXY_stabilization_required,GOLD_US10Y_DXY_Monday_1d_3d,partially_verified
2026-08-30,20260830_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,66,71,,BTC_ENTRY_TOUCH_CME_ETF_STALE,67,79,84,61,71,55,Monday_CME_confirmation_and_77000_hold_required,BTC_77000_79000_CME_ETF_US10Y_Monday,partially_verified
2026-08-30,20260830_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,96,61,72,,ETH_ENTRY_TOUCH_MACRO_UNCONFIRMED,64,76,83,59,69,54,BTC_confirmation_and_2380_hold_required,ETH_2380_2460_BTC_CME_US10Y_Monday,partially_verified
2026-08-30,20260830_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,27,97,,HORMUZ_HEADLINE_WEEKEND_GAP,73,71,99,24,54,68,sustained_Hormuz_flow_confirmation_required,WTI_Hormuz_80_85_Monday,verified
2026-08-30,20260830_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,28,98,,USDJPY_160_INTERVENTION_RATE_CONFLICT,85,89,99,24,60,88,post_weekend_intervention_and_yield_confirmation,USDJPY_160_DXY_US10Y_intervention_Monday,partially_verified
2026-08-30,20260830_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,89,48,79,,ES_HIGH_YIELD_LOW_VIX_CONFLICT,72,74,88,50,67,72,ES_hold_with_US10Y_stabilization_required,ES_US10Y_VIX_Monday_1d_3d,partially_verified
2026-08-30,20260830_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,94,59,75,,AI_THESIS_ALIVE_RATE_PRESSURE,76,83,91,61,72,76,NQ_hold_and_US10Y_DXY_stabilization_required,NQ_US10Y_DXY_VIX_semis_Monday,partially_verified
2026-08-30,20260830_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,93,38,91,,DXY_HAWKISH_FED_EXTENDED,82,86,91,36,69,82,post_spike_consolidation_required,DXY_99_100_US10Y_Monday,partially_verified
2026-08-30,20260830_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,35,96,,US10Y_HAWKISH_REPRICING_473,89,92,94,31,72,90,yield_stabilization_below_or_near_473_required,US10Y_473_DXY_NQ_Monday,verified
2026-08-30,20260830_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,96,34,87,,LOW_VIX_HIGH_YIELD_DIVERGENCE,66,64,88,48,63,64,VIX_equity_rate_confirmation_required,VIX_14_18_NQ_ES_US10Y_Monday,verified
```

```json
[
{"date":"2026-08-30","signal_id":"20260830_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":91,"opp_score":41,"no_trade_score":84,"risk_pct":null,"regime":"HAWKISH_FED_WEEKEND_CONFIRMATION","ems":78,"ffs":82,"cds":90,"ias":40,"cbs":65,"mes":80,"invalidation":"US10Y_and_DXY_stabilization_required","verification_target":"GOLD_US10Y_DXY_Monday_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-30","signal_id":"20260830_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":66,"no_trade_score":71,"risk_pct":null,"regime":"BTC_ENTRY_TOUCH_CME_ETF_STALE","ems":67,"ffs":79,"cds":84,"ias":61,"cbs":71,"mes":55,"invalidation":"Monday_CME_confirmation_and_77000_hold_required","verification_target":"BTC_77000_79000_CME_ETF_US10Y_Monday","verified_status":"partially_verified"},
{"date":"2026-08-30","signal_id":"20260830_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":96,"opp_score":61,"no_trade_score":72,"risk_pct":null,"regime":"ETH_ENTRY_TOUCH_MACRO_UNCONFIRMED","ems":64,"ffs":76,"cds":83,"ias":59,"cbs":69,"mes":54,"invalidation":"BTC_confirmation_and_2380_hold_required","verification_target":"ETH_2380_2460_BTC_CME_US10Y_Monday","verified_status":"partially_verified"},
{"date":"2026-08-30","signal_id":"20260830_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":27,"no_trade_score":97,"risk_pct":null,"regime":"HORMUZ_HEADLINE_WEEKEND_GAP","ems":73,"ffs":71,"cds":99,"ias":24,"cbs":54,"mes":68,"invalidation":"sustained_Hormuz_flow_confirmation_required","verification_target":"WTI_Hormuz_80_85_Monday","verified_status":"verified"},
{"date":"2026-08-30","signal_id":"20260830_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":28,"no_trade_score":98,"risk_pct":null,"regime":"USDJPY_160_INTERVENTION_RATE_CONFLICT","ems":85,"ffs":89,"cds":99,"ias":24,"cbs":60,"mes":88,"invalidation":"post_weekend_intervention_and_yield_confirmation","verification_target":"USDJPY_160_DXY_US10Y_intervention_Monday","verified_status":"partially_verified"},
{"date":"2026-08-30","signal_id":"20260830_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":89,"opp_score":48,"no_trade_score":79,"risk_pct":null,"regime":"ES_HIGH_YIELD_LOW_VIX_CONFLICT","ems":72,"ffs":74,"cds":88,"ias":50,"cbs":67,"mes":72,"invalidation":"ES_hold_with_US10Y_stabilization_required","verification_target":"ES_US10Y_VIX_Monday_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-30","signal_id":"20260830_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":94,"opp_score":59,"no_trade_score":75,"risk_pct":null,"regime":"AI_THESIS_ALIVE_RATE_PRESSURE","ems":76,"ffs":83,"cds":91,"ias":61,"cbs":72,"mes":76,"invalidation":"NQ_hold_and_US10Y_DXY_stabilization_required","verification_target":"NQ_US10Y_DXY_VIX_semis_Monday","verified_status":"partially_verified"},
{"date":"2026-08-30","signal_id":"20260830_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":93,"opp_score":38,"no_trade_score":91,"risk_pct":null,"regime":"DXY_HAWKISH_FED_EXTENDED","ems":82,"ffs":86,"cds":91,"ias":36,"cbs":69,"mes":82,"invalidation":"post_spike_consolidation_required","verification_target":"DXY_99_100_US10Y_Monday","verified_status":"partially_verified"},
{"date":"2026-08-30","signal_id":"20260830_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":35,"no_trade_score":96,"risk_pct":null,"regime":"US10Y_HAWKISH_REPRICING_473","ems":89,"ffs":92,"cds":94,"ias":31,"cbs":72,"mes":90,"invalidation":"yield_stabilization_below_or_near_473_required","verification_target":"US10Y_473_DXY_NQ_Monday","verified_status":"verified"},
{"date":"2026-08-30","signal_id":"20260830_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":96,"opp_score":34,"no_trade_score":87,"risk_pct":null,"regime":"LOW_VIX_HIGH_YIELD_DIVERGENCE","ems":66,"ffs":64,"cds":88,"ias":48,"cbs":63,"mes":64,"invalidation":"VIX_equity_rate_confirmation_required","verification_target":"VIX_14_18_NQ_ES_US10Y_Monday","verified_status":"verified"}
]
```

今日の重要な更新は、**BTCとETHが実際に監視Entry帯まで下がったのに買わない**ことです。価格条件だけなら昨日より魅力的ですが、金利regimeの確認ができない日曜なので、ここでは指値を機械的に発動させません。月曜のクロスアセット確認後に仮説を再起動する方がTSOとして一貫しています。citeturn217324view3turn251055news75turn874262search1 memcite
