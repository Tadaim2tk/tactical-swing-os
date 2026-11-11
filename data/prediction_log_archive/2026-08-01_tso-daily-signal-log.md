<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-08-01 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 13720 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026年8月1日

**価格基準:** 2026年7月31日の米国市場終値・先物清算値、および8月1日朝の暗号資産価格。土曜日のため、株価指数・商品・為替の新規執行は次の取引開始後を想定します。

## 1. 本日の結論

**A級候補：なし**

**B級監視候補**

- GOLD：深めの押し目買い
- NASDAQ：上昇継続時の押し目買い。ただし米長期金利が4.75%を超えている間は執行優先度を下げる

**NO_TRADE**

BTC、ETH、WTI、USDJPY、SPX、DXY、US10Y、VIX。

7月31日の米国株は、Amazonなどの好決算を背景にS&P500が0.7%、NASDAQが1.0%上昇しました。一方、米10年債利回りは4.747%、30年債利回りは約5.25%へ上昇しています。株価と金利が同時に上昇しており、リスクオンではあるものの、NASDAQにとっては持続性を疑うべき組み合わせです。citeturn251206news93turn251206news94turn251206news96

WTIは9月限が84.60ドルへ急騰しました。中東の輸送障害を背景とする供給ショック要因が大きいため、既定ルールどおり買い追随を禁止します。citeturn143371search1turn143371news38

---

## 2. 前回判断の簡易検証

### GOLD：`20260731_GOLD_LONG_B-PULLBACK`

前回条件：

- Entry：4060～4090
- SL：3970
- TP1：4190
- TP2：4275

7月31日の米金先物は一時下落し、Reuters確認値では4,107ドル付近でした。現物金は4,049ドル台まで下落した時間帯があり、先物も前回Entry帯へ接近または到達した可能性があります。ただし、COMEX先物の日中安値を同一系列で完全確認できていないため、**約定はpartially verified** とします。citeturn251206search1turn143371search0

暫定評価：

- Entry：到達の可能性が高い
- 仮想約定：4075
- SL：未到達と推定
- TP1：未到達
- 推定MFE：約+0.3R
- MAE：精密値未確認
- 判断：既存B級は継続可能。ただし追加買いは深い押し目だけ

### NASDAQ：前回NO_TRADE

7月31日のNQ9月限は、取得元により28,287～28,512付近で終了しました。現物NASDAQも1.0%上昇しました。前回はMicrosoft依存と高金利を理由に見送りましたが、Amazon決算後も株高が継続したため、**見送りは安全だった一方、上昇機会は逃した**と評価します。citeturn328151search6turn328151search19turn251206news94

ただし、米10年債利回りが4.747%まで上昇したため、成行で買わなかった判断自体は妥当です。citeturn251206news93turn251206news96

---

## 3. 市場全体の前提

### 判定：リスクオン寄り。ただし「高金利下の大型株集中相場」

確認できる主要要素は次のとおりです。

- S&P500現物：7489.72、前日比+0.7%
- NASDAQ総合：25373.85、前日比+1.0%
- ES先物：7月31日の日中高値7541付近、終盤7519付近
- NQ先物：おおむね28287～28512付近
- 米10年債利回り：4.747%
- VIX：16.82
- WTI9月限：84.60
- USDJPY：介入観測後、158～160円台
- BTC：62885ドル citeturn251206news94turn328151search11turn328151search6turn143371search3turn143371search1turn143371search2turn251206finance0

株価上昇とVIX低下だけを見ればリスクオンです。しかし、長期金利が高値を更新し、原油も再上昇しています。これは将来のインフレと追加利上げを警戒する債券市場と、好決算を買う株式市場が分裂している状態です。

したがって、指数買いの方向性は否定しませんが、**押し目を待ち、SLを広くしてロットを落とす局面**です。

---

## 4. 10資産別判断

### GOLD

米金先物は7月31日に約4107ドルまで下落しました。ドルの反発と金利上昇が逆風です。一方、中東リスクと将来のインフレ懸念は下値を支えます。citeturn251206search1turn251206news93

**判断：B級押し目買い**

現在値付近ではRRが不足します。4015～4050までの深い押しを待ちます。

### BTC

BTCは62885ドル、日中高値65266ドル、安値62426ドルです。米株が上昇した日にBTCは下落しており、短期的な相対弱さがあります。citeturn251206finance0

7月31日のETFフローは実行時点で確定確認できず、CME basisも未確認です。MESは44と評価します。

**判断：NO_TRADE**

62400ドル付近の下値維持と、ETF・CMEの裏付けが揃うまで待ちます。

### ETH

ETHは1624.95ドルです。高値・安値の取得が不完全で、BTCに対する独立した相対強度も確認できません。citeturn251206finance1

**判断：NO_TRADE**

### WTI

WTI9月限は84.60ドル、前日比+5.20ドルでした。日中高値は85.57ドルです。急騰の中心は中東の輸送障害と供給不安です。citeturn143371search1turn143371news38

**判断：NO_TRADE**

方向は上ですが、供給ショック直後のmomentum追随に該当します。新規買いは禁止します。

### USDJPY

ドル円は介入観測を受け、163円台から一時158円前後まで急落しました。7月31日は158.225円付近とのReuters確認値があり、別時点では160円台への反発も確認されています。citeturn143371search2turn143371news42

**判断：NO_TRADE**

介入後の乱高下局面です。売り追随も、反発狙いの買いも不利です。

### SPX

ES先物は7月31日の日中高値7541、終盤7519付近でした。S&P500現物は7489.72で終了しています。citeturn328151search11turn251206news94

大型株決算は強いものの、金利4.75%近辺では上値追随のRRが悪化します。

**判断：NO_TRADE**

7440～7470への調整なら再評価します。

### NASDAQ

NQ先物は取得元により28287～28512付近です。Amazon決算が買いを支えましたが、Appleは弱く、大型テクノロジー株の中でも差があります。citeturn328151search6turn328151search19turn251206news93

**判断：B級押し目買い監視**

28100～28300の押し目で、VIX18未満かつ米10年債利回り4.80%未満なら検討します。

### DXY

DXYは一時99.857まで下落後、100.126付近へ反発しました。米金利上昇はドル高要因ですが、円介入や中央銀行政策の影響で通貨間の値動きが不安定です。citeturn143371news42

**判断：NO_TRADE**

### US10Y

米10年債利回りは4.747%まで上昇しました。複数のFRB当局者が直近会合で利上げを支持したと説明し、追加引き締め観測が強まりました。citeturn251206news93turn251206news96

**判断：NO_TRADE**

上方向は強いものの、4.75%付近での追随は債券買い戻しリスクがあります。4.80%超の定着か4.68%割れを待ちます。

### VIX

VIXは16.82で終了しました。株式上昇に伴い警戒感は後退しています。citeturn143371search3turn143371news41

**判断：NO_TRADE**

低下方向を追うにはすでに水準が低く、買うには株式トレンドが強すぎます。

---

## 5. A級候補

**なし**

GOLDはexpected_rとMAE条件が不足します。NASDAQは方向性が改善していますが、米10年債利回り4.747%と大型株集中がA級昇格を妨げます。

---

## 6. B級監視候補

### GOLD押し目買い

- signal_id：`20260801_GOLD_LONG_B-PULLBACK`
- Entry：4015～4050
- SL：3920
- TP1：4180
- TP2：4270
- RR：1.34
- win_prob：0.60
- expected_r：0.43
- risk_pct：0.25
- MAE想定：0.30R
- 時間決済：5営業日
- 無効化：3920割れ、DXY101超、US10Y4.85%超
- A級昇格：4050以上への反発、CBS75以上、expected_r0.45以上、MAE0.25R以下

### NASDAQ押し目買い

- signal_id：`20260801_NASDAQ_LONG_B-PULLBACK`
- Entry：28100～28300
- SL：27400
- TP1：29100
- TP2：29750
- RR：1.14
- win_prob：0.59
- expected_r：0.38
- risk_pct：0.25
- MAE想定：0.35R
- 時間決済：5営業日
- 無効化：27400割れ、US10Y4.85%超、VIX20超
- A級昇格：28300以上への反発定着、半導体株の上昇拡大、CBS75以上、MAE0.25R以下

両方が同日に発動する場合、合計リスクを0.50%以内に制限します。

---

## 7. 触らない資産

- BTC：株高日に下落、MES44
- ETH：価格情報と独立材料が不足
- WTI：供給ショック直後
- USDJPY：介入後の価格形成が不安定
- SPX：高金利下での高値追随
- DXY：円介入と米金利上昇が交錯
- US10Y：高値圏で追随RR不足
- VIX：16台で方向優位が小さい

---

## 8. 後日検証ポイント

1. GOLDが4015～4050へ下落して反発するか
2. 前回GOLD買いが4190へ到達するか
3. NQが28100～28300で支持されるか
4. 米10年債利回りが4.80%を超えるか
5. WTIが85.57を超えて定着するか
6. BTCが62426を割るか、65000を回復するか
7. USDJPYが158を維持するか、160円台へ戻るか
8. VIXが16台を維持するか
9. Amazon・Microsoft以外へ株高が拡大するか

---

## 9. Obsidian保存用Observation Draft

```markdown
# 2026-08-01 株高・原油高・長期金利高の同時進行

Type: 一般市場Observation

## Summary

7月31日の米国株はAmazonなどの好決算を受けて続伸した。
一方、米10年債利回りは4.747%、WTIは84.60ドルへ上昇した。
株式市場はリスクオンだが、債券と原油はインフレおよび追加利上げリスクを示している。
A級候補はなく、GOLDとNASDAQの押し目買いをB級監視とする。

## Observation

- S&P500現物は7489.72。
- ES先物は終盤約7519。
- NASDAQ総合は25373.85。
- NQ先物は約28287～28512。
- US10Yは4.747%。
- WTI9月限は84.60。
- VIXは16.82。
- BTCは62885。
- ETHは1624.95。
- USDJPYは介入観測後158～160円台。
- DXYは約100.126。
- 金先物は約4107。

## Evaluation

A級候補なし。
GOLD4015～4050、NASDAQ28100～28300をB級押し目買い監視とする。
WTIは供給ショック追随禁止。
BTCはMES44でNO_TRADE。
USDJPYは介入後のためNO_TRADE。

## Interpretation

株式市場は大型企業の好決算を買っているが、長期金利と原油価格はインフレ再加速を示している。
高金利が続けばNASDAQの上昇持続性は低下する。
週明けは高値追随ではなく押し目の支持確認が重要になる。

## Later Review

- GOLD4015～4050
- GOLD4190
- NQ28100～28300
- US10Y4.80
- WTI85.57
- BTC62426・65000
- USDJPY158・160
- VIX16・18

## Tags

#TSO #MarketObservation #GOLD #NASDAQ #WTI #US10Y #BTC #USDJPY
```

---

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-08-01,20260801_GOLD_LONG_B-PULLBACK,GOLD,BUY,B,PULLBACK,4015,4050,3920,4180,4270,1.34,0.60,0.43,69,68,35,0.25,BULLISH_PULLBACK,66,63,67,68,73,64,3920_break_or_DXY_above_101_or_US10Y_above_4.85,5d_close_MFE_MAE_4180_and_yields,partially_verified
2026-08-01,20260801_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,48,42,84,,EQUITY_DIVERGENCE_WEAK,52,41,48,47,53,44,mes_below_50_and_equity_divergence,BTC_62426_65000_ETF_flow_CME_basis_and_5d_close,verified
2026-08-01,20260801_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,42,38,85,,WEAK,46,39,43,44,48,39,no_independent_relative_strength,ETH_BTC_ratio_price_range_and_5d_close,partially_verified
2026-08-01,20260801_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,85,48,91,,SUPPLY_SHOCK_UP,74,72,87,61,70,75,post_supply_shock_momentum_chase,WTI_85.57_hold_shipping_status_and_5d_close,verified
2026-08-01,20260801_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,79,44,93,,INTERVENTION_SHOCK,68,61,88,38,55,63,intervention_price_discovery_unstable,USDJPY_158_160_official_confirmation_and_5d_close,partially_verified
2026-08-01,20260801_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,78,57,70,,EARNINGS_RALLY_HIGH_YIELD,70,63,68,69,72,64,high_yield_and_high_level_chase_risk,ES_7440_7540_breadth_US10Y_and_5d_close,verified
2026-08-01,20260801_NASDAQ_LONG_B-PULLBACK,NASDAQ,BUY,B,PULLBACK,28100,28300,27400,29100,29750,1.14,0.59,0.38,80,66,39,0.25,MEGACAP_RALLY_HIGH_YIELD,70,58,69,71,72,62,27400_break_or_US10Y_above_4.85_or_VIX_above_20,5d_close_MFE_MAE_chip_breadth_and_yields,partially_verified
2026-08-01,20260801_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,61,46,78,,POLICY_VOLATILE,64,61,62,48,58,59,yen_intervention_and_US_yield_conflict,DXY_99.85_101_USDJPY_and_5d_close,partially_verified
2026-08-01,20260801_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,78,49,82,,HAWKISH_BREAKOUT,72,70,69,59,67,70,extended_yield_breakout_and_reversal_risk,US10Y_4.68_4.80_oil_and_5d_close,verified
2026-08-01,20260801_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,66,42,76,,LOW_VOL_RISK_ON,61,56,64,67,65,56,VIX_already_below_17,VIX_16_hold_or_18_recovery_and_5d_close,verified
```

## TSO_LOG JSON

```json
[
  {"date":"2026-08-01","signal_id":"20260801_GOLD_LONG_B-PULLBACK","asset":"GOLD","side":"BUY","rank":"B","type":"PULLBACK","entry_low":4015,"entry_high":4050,"sl":3920,"tp1":4180,"tp2":4270,"rr":1.34,"win_prob":0.60,"expected_r":0.43,"tq_score":69,"opp_score":68,"no_trade_score":35,"risk_pct":0.25,"regime":"BULLISH_PULLBACK","ems":66,"ffs":63,"cds":67,"ias":68,"cbs":73,"mes":64,"invalidation":"3920_break_or_DXY_above_101_or_US10Y_above_4.85","verification_target":"5d_close_MFE_MAE_4180_and_yields","verified_status":"partially_verified"},
  {"date":"2026-08-01","signal_id":"20260801_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":48,"opp_score":42,"no_trade_score":84,"risk_pct":null,"regime":"EQUITY_DIVERGENCE_WEAK","ems":52,"ffs":41,"cds":48,"ias":47,"cbs":53,"mes":44,"invalidation":"mes_below_50_and_equity_divergence","verification_target":"BTC_62426_65000_ETF_flow_CME_basis_and_5d_close","verified_status":"verified"},
  {"date":"2026-08-01","signal_id":"20260801_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":42,"opp_score":38,"no_trade_score":85,"risk_pct":null,"regime":"WEAK","ems":46,"ffs":39,"cds":43,"ias":44,"cbs":48,"mes":39,"invalidation":"no_independent_relative_strength","verification_target":"ETH_BTC_ratio_price_range_and_5d_close","verified_status":"partially_verified"},
  {"date":"2026-08-01","signal_id":"20260801_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":85,"opp_score":48,"no_trade_score":91,"risk_pct":null,"regime":"SUPPLY_SHOCK_UP","ems":74,"ffs":72,"cds":87,"ias":61,"cbs":70,"mes":75,"invalidation":"post_supply_shock_momentum_chase","verification_target":"WTI_85.57_hold_shipping_status_and_5d_close","verified_status":"verified"},
  {"date":"2026-08-01","signal_id":"20260801_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":79,"opp_score":44,"no_trade_score":93,"risk_pct":null,"regime":"INTERVENTION_SHOCK","ems":68,"ffs":61,"cds":88,"ias":38,"cbs":55,"mes":63,"invalidation":"intervention_price_discovery_unstable","verification_target":"USDJPY_158_160_official_confirmation_and_5d_close","verified_status":"partially_verified"},
  {"date":"2026-08-01","signal_id":"20260801_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":78,"opp_score":57,"no_trade_score":70,"risk_pct":null,"regime":"EARNINGS_RALLY_HIGH_YIELD","ems":70,"ffs":63,"cds":68,"ias":69,"cbs":72,"mes":64,"invalidation":"high_yield_and_high_level_chase_risk","verification_target":"ES_7440_7540_breadth_US10Y_and_5d_close","verified_status":"verified"},
  {"date":"2026-08-01","signal_id":"20260801_NASDAQ_LONG_B-PULLBACK","asset":"NASDAQ","side":"BUY","rank":"B","type":"PULLBACK","entry_low":28100,"entry_high":28300,"sl":27400,"tp1":29100,"tp2":29750,"rr":1.14,"win_prob":0.59,"expected_r":0.38,"tq_score":80,"opp_score":66,"no_trade_score":39,"risk_pct":0.25,"regime":"MEGACAP_RALLY_HIGH_YIELD","ems":70,"ffs":58,"cds":69,"ias":71,"cbs":72,"mes":62,"invalidation":"27400_break_or_US10Y_above_4.85_or_VIX_above_20","verification_target":"5d_close_MFE_MAE_chip_breadth_and_yields","verified_status":"partially_verified"},
  {"date":"2026-08-01","signal_id":"20260801_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":61,"opp_score":46,"no_trade_score":78,"risk_pct":null,"regime":"POLICY_VOLATILE","ems":64,"ffs":61,"cds":62,"ias":48,"cbs":58,"mes":59,"invalidation":"yen_intervention_and_US_yield_conflict","verification_target":"DXY_99.85_101_USDJPY_and_5d_close","verified_status":"partially_verified"},
  {"date":"2026-08-01","signal_id":"20260801_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":78,"opp_score":49,"no_trade_score":82,"risk_pct":null,"regime":"HAWKISH_BREAKOUT","ems":72,"ffs":70,"cds":69,"ias":59,"cbs":67,"mes":70,"invalidation":"extended_yield_breakout_and_reversal_risk","verification_target":"US10Y_4.68_4.80_oil_and_5d_close","verified_status":"verified"},
  {"date":"2026-08-01","signal_id":"20260801_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":66,"opp_score":42,"no_trade_score":76,"risk_pct":null,"regime":"LOW_VOL_RISK_ON","ems":61,"ffs":56,"cds":64,"ias":67,"cbs":65,"mes":56,"invalidation":"VIX_already_below_17","verification_target":"VIX_16_hold_or_18_recovery_and_5d_close","verified_status":"verified"}
]
```
