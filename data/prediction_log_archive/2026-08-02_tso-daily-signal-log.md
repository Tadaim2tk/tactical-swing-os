<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-08-02 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 13499 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026年8月2日

本日は日曜日です。**BTC・ETHのみ週末価格形成が進行中**で、GOLD・WTI・USDJPY・ES・NQ・DXY・US10Y・VIXは原則として7月31日の最終取引データを基準にします。市場休場を理由に記録は止めず、10資産すべてを本日分として記帳します。

## 1. 本日の結論

**A級候補：なし**

**B級新規シグナル：なし**

**10資産すべて新規NO_TRADE**です。

昨日までGOLDとNASDAQをB級押し目買い監視としていましたが、週末のためEntry判定を更新できません。BTCは約6.3万ドルまで下落しており、米株が強かった7月31日にも暗号資産側の相対的な弱さが残っています。7月31日のBTCは約63,940ドル、その後8月1日に62,972ドルまで下落したことが確認できます。citeturn772201news37turn772201news34

したがって本日は、**新しいポジションを作る日ではなく、週明けのギャップと週末BTCの弱さが他市場へ伝播するかを見る日**とします。

---

## 2. 前回判断の簡易検証

### GOLD：`20260801_GOLD_LONG_B-PULLBACK`

前回条件：

- Entry：4015～4050
- SL：3920
- TP1：4180
- TP2：4270

7月31日の取引終了後であり、本日まで通常COMEX金先物の新しい日足はありません。

取得できる8月限金先物データでは4046.70ドルという水準が確認され、前回Entry帯と整合する価格帯ですが、これは最新の同一時点データとは断定できません。citeturn940682search0

したがって、

- Entry：**判定保留**
- SL：新規判定なし
- TP：新規判定なし
- MFE/MAE：更新なし
- 前回シグナル：取消さず監視継続
- 本日新規発行：NO_TRADE

とします。

### NASDAQ：`20260801_NASDAQ_LONG_B-PULLBACK`

前回条件：

- Entry：28100～28300
- SL：27400
- TP1：29100
- TP2：29750

米国株は7月31日にS&P500 +0.70%、NASDAQ +1.00%と続伸しましたが、その後は週末入りしています。上昇はAmazon・Microsoftなど大型テック決算が主因で、Appleは約7%下落しており、全面高ではありませんでした。citeturn787264news1

したがって、

- Entry：週末のため新規判定なし
- シグナル：監視継続
- 成行追随：禁止
- 週明けに28100～28300への押しが発生した場合のみ再評価

とします。

### BTC：前回NO_TRADE

ここは見送り判断が機能しています。

7月31日約63,940ドルから、8月1日には62,972ドルまで低下しました。Coinbase決算の弱さと暗号資産市場のセンチメント悪化が指摘されています。citeturn772201news34turn772201news37

前回の「株高に対してBTCが弱い」「MES50未満」という判断は維持します。

---

## 3. 市場全体の前提

### 判定：株式リスクオン × 金利・原油警戒 × 暗号資産弱含み

7月31日の主要構造はかなり特徴的です。

米国株はAmazonやMicrosoftの決算を好感して上昇しました。一方で、長期米国債利回りは複数年ぶりの高水準へ上昇しています。FRB当局者のタカ派姿勢とインフレ懸念が債券市場に残っています。citeturn787264news1

さらにWTIは7月31日に**84.67ドル**で終了し、7月だけで約21%上昇しました。ホルムズ海峡などを巡る輸送障害と供給不安が原油価格を支えています。citeturn940682news60

一方、BTCは株価上昇についていけず6.3万ドルを割り込みました。citeturn772201news34

したがって現在は、

**「米大型株は強いが、マクロ環境全体がリスクオンになったわけではない」**

という状態です。

週明けに重要なのは、金利高・原油高・BTC安のどれが株式市場に伝染するかです。

---

## 4. 10資産別判断

### GOLD — NO_TRADE

金はドル・長期金利上昇が逆風ですが、中東リスクとインフレ懸念が下値を支えています。

前回の4015～4050押し目買い監視は維持しますが、日曜日に新しいCOMEX日足がないため**本日新シグナルは発行しません**。

週明けに4050以下→反発なら再びB級候補。

---

### BTC — NO_TRADE

7月31日には約63,940ドル、8月1日には62,972ドルまで下落しました。citeturn772201news34turn772201news37

また、7月30日時点ではBTC先物建玉が2カ月ぶり高水準まで増加していました。建玉増加そのものは方向を保証せず、弱い価格と高いレバレッジの組み合わせは下方向の清算リスクも増やします。citeturn772201news43

**MES：43**

65000回復以前に、まず63000～64000を再び支持帯として確立する必要があります。

---

### ETH — NO_TRADE

ETHについては週末の高品質な価格系列を十分取得できませんでした。

BTCより強いという証拠もありません。

したがって価格を推測してB級を作らず、

**NO_TRADE / partially_verified**

とします。

---

### WTI — NO_TRADE

WTIは7月31日に**84.67ドル**で終了。7月月間では約21%上昇しました。citeturn940682news60

ホルムズ海峡だけでなく、紅海・黒海周辺でも輸送・供給リスクが残っています。

ただしこれはTSOで既知の危険領域です。

**供給ショック後の買い追随は禁止。**

方向の強さと、取引期待値は別です。

---

### USDJPY — NO_TRADE

7月31日は日本当局による介入後の円高が継続し、市場は追加介入を警戒していました。citeturn787264news22

介入直後は通常の金利差モデルが機能しにくく、

- ドル買い → 再介入リスク
- ドル売り → 米長期金利高リスク

となります。

週明けの価格発見を待ちます。

---

### SPX — NO_TRADE

7月31日のS&P500は+0.70%。

Amazon・Microsoftなどの好決算が牽引しました。citeturn787264news1

トレンド自体は強いですが、

- 長期金利上昇
- 原油84ドル台
- 大型株への集中
- 週明けギャップ

を考慮すると高値での新規追随は不要です。

---

### NASDAQ — NO_TRADE

NASDAQは7月31日+1.00%。

AI投資に対する信頼回復が支援しましたが、Appleは約7%下落しており、メガテック全体が一様に強いわけではありません。citeturn787264news1

前回の28100～28300押し目買い候補は維持。

**現在値を追わない。**

---

### DXY — NO_TRADE

7月31日はドル指数が小幅低下しました。一方、米長期金利は上昇しました。通常なら金利高はドルを支えるため、この乖離は注意が必要です。citeturn787264news1

円介入の影響も混ざっています。

週明けにドルと金利の相関が戻るまで見送ります。

---

### US10Y — NO_TRADE

7月31日は米長期債利回りが複数年ぶりの高水準へ上昇しました。FRB当局者の利上げ支持・インフレ懸念が背景です。citeturn787264news1

ただし、高値圏からさらに利回り上昇を追うのはRRが悪い。

週明けは、

- 4.80%方向へ突破
- 4.65～4.68%へ反落

のどちらになるか確認します。

---

### VIX — NO_TRADE

株式上昇局面ではボラティリティは低下方向ですが、金利・原油・地政学リスクが残っています。

CboeのVIXは株式市場再開まで新しい通常セッション価格がありません。citeturn787264news21

低VIXをさらに売る優位性も、週末にVIXを買う根拠も不足しています。

---

## 5. A級候補

**なし**

A級条件を満たす対象はありません。

特に今日は日曜日であり、BTC/ETH以外では新しい市場価格形成がありません。ここで金曜日価格から人工的にA級シグナルを作ることは、Entry追随禁止ルールと矛盾します。

---

## 6. B級監視候補

**新規発行なし。**

ただし既存監視条件を引き継ぎます。

**GOLD**

- 4015～4050への押し
- 反発確認
- US10Y < 4.85%
- DXY < 101

**NASDAQ**

- NQ 28100～28300
- VIX < 18
- US10Y < 4.80%
- 半導体株の上昇幅維持

条件成立時に新signal_idを発行します。

---

## 7. 触らない資産

BTCは株高との逆行、ETHは情報密度不足、WTIは供給ショック後、USDJPYは介入後、SPX/NASDAQは週明けギャップ待ち、DXYは金利との乖離、US10Yは利回り高値圏、VIXは休場中です。

**本日は「方向がない」のではなく、「条件が整っていない」NO_TRADEです。**

---

## 8. 後日検証ポイント

1. BTCが63000を回復できるか
2. BTCが62400近辺を割るか
3. 週末BTC安がNQへ波及するか
4. NQが28100～28300まで調整するか
5. GOLDが4015～4050へ入るか
6. WTI84.67からさらに上昇するか
7. US10Yが4.80%方向へ進むか
8. USDJPYが介入後の円高を維持するか
9. VIXが週明け18を超えるか
10. Amazon/Microsoft以外へ株高が拡大するか

---

## 9. Obsidian保存用Observation Draft

```markdown
# 2026-08-02 週末BTC安と米大型株高の乖離

Type: 一般市場Observation

## Summary

7月31日の米国株はAmazon・Microsoftなどの決算を背景に上昇した。
一方、米長期金利と原油価格は高く、BTCは週末に63000ドルを割り込んだ。

株式だけを見るとリスクオンだが、債券・商品・暗号資産を含めたクロスアセットでは確認が取れていない。

本日は日曜日のため新規A級・B級シグナルを発行せず、10資産すべてNO_TRADEとする。

## Observation

- S&P500は7月31日に+0.70%
- NASDAQは+1.00%
- Amazon・Microsoftが株高を牽引
- Appleは約7%下落
- WTIは84.67ドル
- WTIは7月月間約21%上昇
- BTCは8月1日に62972ドルまで低下
- 米長期金利は複数年ぶり高水準
- 円は介入後の不安定な価格形成

## Evaluation

A級候補なし。
新規B級候補なし。

GOLD4015～4050とNASDAQ28100～28300の既存監視条件を維持する。

BTCはMES43としてNO_TRADE。
WTIは供給ショック追随禁止。
USDJPYは介入後のためNO_TRADE。

## Interpretation

米大型株高とBTC安の乖離は、全面的な流動性リスクオンではなく、好決算銘柄への集中買いである可能性を示す。

週明けにNASDAQも下落するならBTCが先行指標だった可能性がある。
逆にBTCが63000～64000を回復すれば週末固有の弱さだった可能性が高まる。

## Later Review

- BTC 62400 / 63000 / 65000
- NQ 28100～28300
- GOLD 4015～4050
- WTI 84.67
- US10Y 4.80%
- USDJPY介入後レンジ
- VIX 18

## Tags

#TSO #MarketObservation #BTC #NASDAQ #GOLD #WTI #US10Y #Weekend
```

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-08-02,20260802_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,65,51,75,,WEEKEND_BULLISH_CONFLICTED,64,61,63,62,67,61,market_closed_existing_pullback_not_confirmed,GOLD_4015_4050_US10Y_DXY_and_next_session,partially_verified
2026-08-02,20260802_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,45,39,87,,WEEKEND_WEAK,50,40,52,43,49,43,mes_below_50_and_price_below_63000,BTC_62400_63000_65000_ETF_CME_and_5d_close,verified
2026-08-02,20260802_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,42,36,84,,WEEKEND_WEAK_UNKNOWN,46,39,45,42,47,39,no_confirmed_relative_strength,ETH_BTC_ratio_current_price_and_5d_close,unverified
2026-08-02,20260802_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,84,45,90,,SUPPLY_SHOCK_UP,73,72,86,60,69,74,post_supply_shock_momentum_chase,WTI_84.67_shipping_flows_and_next_session,verified
2026-08-02,20260802_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,76,41,91,,POST_INTERVENTION_VOLATILE,67,59,84,40,55,61,post_intervention_price_discovery,USDJPY_next_open_intervention_and_5d_close,verified
2026-08-02,20260802_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,75,52,76,,MEGACAP_RISK_ON_HIGH_YIELD,68,62,67,66,69,62,market_closed_and_high_yield_chase_risk,ES_next_open_breadth_US10Y_and_5d_close,verified
2026-08-02,20260802_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,79,58,72,,MEGACAP_RALLY_WEEKEND,69,57,66,68,71,61,market_closed_and_pullback_entry_not_reached,NQ_28100_28300_chip_breadth_US10Y_and_5d_close,verified
2026-08-02,20260802_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,58,43,79,,YIELD_DIVERGENCE_POLICY_VOLATILE,62,60,59,47,56,57,yield_dollar_divergence_and_yen_intervention,DXY_next_open_US10Y_USDJPY_and_5d_close,partially_verified
2026-08-02,20260802_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,77,46,83,,HAWKISH_HIGH_YIELD,71,70,69,57,65,69,extended_yield_level_and_market_closed,US10Y_4.65_4.80_oil_and_next_session,partially_verified
2026-08-02,20260802_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,61,38,80,,WEEKEND_LOW_VOL,59,53,61,62,61,53,market_closed_and_no_directional_edge,VIX_18_next_open_and_5d_close,verified
```

## TSO_LOG JSON

```json
[
{"date":"2026-08-02","signal_id":"20260802_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":65,"opp_score":51,"no_trade_score":75,"risk_pct":null,"regime":"WEEKEND_BULLISH_CONFLICTED","ems":64,"ffs":61,"cds":63,"ias":62,"cbs":67,"mes":61,"invalidation":"market_closed_existing_pullback_not_confirmed","verification_target":"GOLD_4015_4050_US10Y_DXY_and_next_session","verified_status":"partially_verified"},
{"date":"2026-08-02","signal_id":"20260802_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":45,"opp_score":39,"no_trade_score":87,"risk_pct":null,"regime":"WEEKEND_WEAK","ems":50,"ffs":40,"cds":52,"ias":43,"cbs":49,"mes":43,"invalidation":"mes_below_50_and_price_below_63000","verification_target":"BTC_62400_63000_65000_ETF_CME_and_5d_close","verified_status":"verified"},
{"date":"2026-08-02","signal_id":"20260802_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":42,"opp_score":36,"no_trade_score":84,"risk_pct":null,"regime":"WEEKEND_WEAK_UNKNOWN","ems":46,"ffs":39,"cds":45,"ias":42,"cbs":47,"mes":39,"invalidation":"no_confirmed_relative_strength","verification_target":"ETH_BTC_ratio_current_price_and_5d_close","verified_status":"unverified"},
{"date":"2026-08-02","signal_id":"20260802_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":84,"opp_score":45,"no_trade_score":90,"risk_pct":null,"regime":"SUPPLY_SHOCK_UP","ems":73,"ffs":72,"cds":86,"ias":60,"cbs":69,"mes":74,"invalidation":"post_supply_shock_momentum_chase","verification_target":"WTI_84.67_shipping_flows_and_next_session","verified_status":"verified"},
{"date":"2026-08-02","signal_id":"20260802_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":76,"opp_score":41,"no_trade_score":91,"risk_pct":null,"regime":"POST_INTERVENTION_VOLATILE","ems":67,"ffs":59,"cds":84,"ias":40,"cbs":55,"mes":61,"invalidation":"post_intervention_price_discovery","verification_target":"USDJPY_next_open_intervention_and_5d_close","verified_status":"verified"},
{"date":"2026-08-02","signal_id":"20260802_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":75,"opp_score":52,"no_trade_score":76,"risk_pct":null,"regime":"MEGACAP_RISK_ON_HIGH_YIELD","ems":68,"ffs":62,"cds":67,"ias":66,"cbs":69,"mes":62,"invalidation":"market_closed_and_high_yield_chase_risk","verification_target":"ES_next_open_breadth_US10Y_and_5d_close","verified_status":"verified"},
{"date":"2026-08-02","signal_id":"20260802_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":79,"opp_score":58,"no_trade_score":72,"risk_pct":null,"regime":"MEGACAP_RALLY_WEEKEND","ems":69,"ffs":57,"cds":66,"ias":68,"cbs":71,"mes":61,"invalidation":"market_closed_and_pullback_entry_not_reached","verification_target":"NQ_28100_28300_chip_breadth_US10Y_and_5d_close","verified_status":"verified"},
{"date":"2026-08-02","signal_id":"20260802_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":58,"opp_score":43,"no_trade_score":79,"risk_pct":null,"regime":"YIELD_DIVERGENCE_POLICY_VOLATILE","ems":62,"ffs":60,"cds":59,"ias":47,"cbs":56,"mes":57,"invalidation":"yield_dollar_divergence_and_yen_intervention","verification_target":"DXY_next_open_US10Y_USDJPY_and_5d_close","verified_status":"partially_verified"},
{"date":"2026-08-02","signal_id":"20260802_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":77,"opp_score":46,"no_trade_score":83,"risk_pct":null,"regime":"HAWKISH_HIGH_YIELD","ems":71,"ffs":70,"cds":69,"ias":57,"cbs":65,"mes":69,"invalidation":"extended_yield_level_and_market_closed","verification_target":"US10Y_4.65_4.80_oil_and_next_session","verified_status":"partially_verified"},
{"date":"2026-08-02","signal_id":"20260802_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":61,"opp_score":38,"no_trade_score":80,"risk_pct":null,"regime":"WEEKEND_LOW_VOL","ems":59,"ffs":53,"cds":61,"ias":62,"cbs":61,"mes":53,"invalidation":"market_closed_and_no_directional_edge","verification_target":"VIX_18_next_open_and_5d_close","verified_status":"verified"}
]
```

**本日の主要判定は「全10資産NO_TRADE」ですが、これはデータ欠落ではなく正式な市場判断として記帳します。** 週明けはBTCの週末弱含みがNASDAQへ波及するか、逆にBTCが63000～64000を奪回して米株のリスクオンへ収斂するかが最初の確認点です。
