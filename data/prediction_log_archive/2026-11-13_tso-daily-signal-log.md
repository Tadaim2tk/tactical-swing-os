<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-11-13 07:00 JST -->
<!-- transport: Complete original read_thread message d004bea6-6338-46f1-b660-48e91e4dec3e; raw markdown -->
<!-- archived_at: 2026-11-12T22:56:45Z / chars: 10758 / 値は無修正 -->

# Tactical Swing OS v2 — 2026年11月13日（金）

実行モデル：GPT-6

本日の市場の主役：**US10Y**

## 1\. 本日の結論

**A級：0件 / B級：5件 / NO\_TRADE：5件**

本日は米国の金利上昇とドル高が市場全体を支配している。11月12日の米10年債利回りは約5.113%、DXYは103.17、USDJPYは159.975付近。金利上昇が金・暗号資産・成長株への圧力となる一方、原油は中東の供給リスクによって独立した動きを示している。citeturn444652news21turn960624news37turn960624news36

| 資産 | 判断 | ランク | expected\_r |
|--------|--------|--------|--------|
| GOLD | SELL | B | \+0.24R |
| BTC | NO\_TRADE | — | — |
| ETH | SELL | B | \+0.16R |
| WTI | NO\_TRADE | — | — |
| USDJPY | BUY | B | \+0.21R |
| SPX | NO\_TRADE | — | — |
| NASDAQ | NO\_TRADE | — | — |
| DXY | BUY | B | \+0.25R |
| US10Y | BUY | B | \+0.22R |
| VIX | NO\_TRADE | — | — |

B級5件は方向を持つ独立した観察行として記帳する。いずれも現時点でA級の期待値・品質条件を満たさない。

**データ制約：** 11月12日の報道値と一部の日次価格履歴を取得した。ただし、10資産すべての確定日足OHLCとATR10は揃っていない。今回のEntry・SL・TPは暫定モデル水準であり、**1×ATR10下限の適合は未確認**。正式なATR準拠判定として扱わない。

## 2\. 前回判断の簡易検証

11月12日の判断に対して、米金利・ドル高・金下落・BTC下落という市場方向は確認できた。

BTC/USDはYahoo Financeの日次履歴で11月11日73,964.47ドルから11月12日71,523.30ドルへ下落。ただし価格提供元ごとに日次区切りと終値が異なる。citeturn960624search0turn960624search2

前日までのTSO\_LOG原本から、資産ごとの最新の方向ありsignal\_idとそのinvalidation水準を確定できていない。このため、過去判断の発動判定を捏造しない。

`invalidation_check: 20261112_GOLD=unknown` のような不完全なIDも生成しない。今回の未確定事項は、前日台帳との照合が必要な検証欠損として記録する。

## 3\. 市場全体の前提

- **金利：** 米10年債利回りは約5.113%。強いインフレ指標とFRBのタカ派観測が背景。citeturn444652news21
- **為替：** DXYは103.17、USDJPYは159.975付近。160円接近による日本当局の介入リスクが上昇。citeturn444652news21
- **金：** COMEX金先物の期近報道値は3,878.40ドル。12月限GCZ26の独立した清算値としては未確認。citeturn960624news37
- **原油：** WTIはReutersの終値報道88.74ドルに対し、別の12月限履歴では86.94ドル。系列・時点の不一致があり、執行基準には使用しない。citeturn960624news36turn960624search4
- **株式：** S&amp;P500現物は7,592.40で引けたが、ES・NQ先物の確定値は別途必要。citeturn960624news44

市場レジームは概ねRISK\_OFF。ただし原油と為替介入リスクが独立しており、単純な全面リスクオフではない。

## 4\. 10資産別判断

| 資産 | Entry帯 | SL | TP1 / TP2 | RR |
|--------|--------|--------|--------|--------|
| GOLD SELL | 3890–3930 | 4040 | 3700 / 3600 | 1.62 |
| BTC | — | — | — | — |
| ETH SELL | 2030–2080 | 2240 | 1770 / 1650 | 1.54 |
| WTI | — | — | — | — |
| USDJPY BUY | 159.30–159.80 | 157.90 | 162.40 / 163.50 | 1.73 |
| SPX | — | — | — | — |
| NASDAQ | — | — | — | — |
| DXY BUY | 102.90–103.30 | 102.10 | 104.90 / 105.70 | 1.80 |
| US10Y BUY | 5.06–5.12 | 4.96 | 5.38 / 5.52 | 2.23 |
| VIX | — | — | — | — |

RRはEntry帯の中点から再計算済み。US10Yの数値単位は利回り%。

GOLDは\*\*COMEX 2026年12月限（GCZ26）\*\*を比較基準として固定する。今回の期近報道値との同一限月確認は未完了。

各資産の方向評価：

- **GOLD：** 実質金利上昇に弱い構造。反発売りを観察。想定MAE 0.35R。
- **BTC：** 下落方向だがETF・CME裏付け不足、MES39。NO\_TRADE。
- **ETH：** BTCより弱いリスク資産として戻り売り。想定MAE 0.40R。
- **WTI：** 中東供給ショックにより短期モメンタム追随を回避。
- **USDJPY：** 金利差に沿う買い。ただし160円近辺の介入が最大の反証要因。想定MAE 0.45R。
- **SPX：** ES先物の価格構造を未確定。方向確信が不足。
- **NASDAQ：** NQ先物の値動きと現物指数を混同せず、判断を保留。
- **DXY：** 金利上昇とドル需要による上方向。想定MAE 0.35R。
- **US10Y：** 金利上昇継続。想定MAE 0.45R。
- **VIX：** VIX現物指数の確定値不足。先物価格では代替しない。

## 5\. A級候補

**該当なし。**

B級のうちDXYはCBS70・EMS62・RR1.80・win\_prob0.53で、**B+観察候補**に該当する。ただしATR10確認前の暫定判定。

## 6\. B級監視候補

GOLD、ETH、USDJPY、DXY、US10Yの5件を記帳する。

最大日次リスク0.50%のため、5件を同時に全て0.25%で参加する想定ではない。特にDXY・USDJPY・US10Yはドル金利要因で相関しやすく、同一リスク群として管理する。

## 7\. 触らない資産

BTC、WTI、SPX、NASDAQ、VIX。

BTCはETF/CME裏付け不足、WTIは供給イベント、残り3資産は指定参照系列の価格確認不足または方向確信不足が理由。

## 8\. 後日検証ポイント

1. GCZ26、ES、NQの同一限月OHLCを取得し、ATR10下限を確認。
2. USDJPYの160円突破・為替介入・反転幅を検証。
3. US10Yの5.113%からの方向とDXYの連動を観察。
4. 前日TSO\_LOGから最新signal\_idとinvalidation水準を復元。
5. 5営業日後に時間決済RとTP1到達率を別々に集計。

## 9\. Obsidian保存用Observation Draft

```markdown
---
date: 2026-11-13
system: Tactical Swing OS v2
model: GPT-6
market_leader: US10Y
regime: RISK_OFF
a_count: 0
b_count: 5
no_trade_count: 5
verification: partial
---

# Observation 2026-11-13

米10年債利回り上昇とドル高が中心。
GOLD・ETHは戻り売り、USDJPY・DXY・US10Yは買い方向。
WTIは供給ショックによる追随回避。

B+候補: DXY
GOLD reference: GCZ26

課題:
- ATR10実測未完了
- ES/NQ先物価格未確定
- 前日最新signal_idのinvalidation照合未完了
- WTI報道値と限月別データの不一致

全10資産のTSO_LOGを生成。
```

## 10\. TSO\_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-11-13,20261113_GOLD_SELL_REVERSAL,GOLD,SELL,B,REVERSAL,3890,3930,4040,3700,3600,1.62,0.53,0.24,65,67,25,0.25,RISK_OFF,61,66,60,54,69,56,GCZ26_above_4040,GCZ26,partially_verified
2026-11-13,20261113_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,44,37,77,,RISK_OFF,49,44,42,35,48,39,ETF_CME_confirmation_missing,BTCUSD_spot,partially_verified
2026-11-13,20261113_ETH_SELL_PULLBACK,ETH,SELL,B,PULLBACK,2030,2080,2240,1770,1650,1.54,0.51,0.16,59,60,34,0.25,RISK_OFF,55,57,49,45,61,44,ETHUSD_above_2240,ETHUSD_spot,partially_verified
2026-11-13,20261113_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,40,31,84,,EVENT,40,32,36,28,43,35,supply_shock,CLZ26,partially_verified
2026-11-13,20261113_USDJPY_BUY_PULLBACK,USDJPY,BUY,B,PULLBACK,159.3,159.8,157.9,162.4,163.5,1.73,0.51,0.21,63,65,34,0.25,EVENT,58,61,56,44,67,59,USDJPY_below_157.9_or_intervention,USDJPY_spot,partially_verified
2026-11-13,20261113_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,43,38,75,,RISK_OFF,49,43,47,38,51,47,ES_contract_quote_missing,ES_futures,unverified
2026-11-13,20261113_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,49,47,69,,RISK_OFF,53,48,46,42,57,48,NQ_contract_quote_missing,NQ_futures,unverified
2026-11-13,20261113_DXY_BUY_PULLBACK,DXY,BUY,B,PULLBACK,102.9,103.3,102.1,104.9,105.7,1.8,0.53,0.25,65,67,30,0.25,RISK_OFF,62,64,56,52,70,61,DXY_below_102.1,DXY_index,partially_verified
2026-11-13,20261113_US10Y_BUY_MOMENTUM,US10Y,BUY,B,MOMENTUM,5.06,5.12,4.96,5.38,5.52,2.23,0.52,0.22,62,64,32,0.25,EVENT,60,63,52,46,68,57,US10Y_below_4.96,US10Y_yield,partially_verified
2026-11-13,20261113_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,42,35,79,,MIXED,46,42,41,36,44,40,VIX_index_quote_missing,VIX_index,unverified
```

CSVはヘッダー28列、データ10行、各行28列で構造検証済み。数値のRRも再計算済み。

### JSON

```json
[
  {"date":"2026-11-13","signal_id":"20261113_GOLD_SELL_REVERSAL","asset":"GOLD","side":"SELL","rank":"B","type":"REVERSAL","entry_low":3890,"entry_high":3930,"sl":4040,"tp1":3700,"tp2":3600,"rr":1.62,"win_prob":0.53,"expected_r":0.24,"tq_score":65,"opp_score":67,"no_trade_score":25,"risk_pct":0.25,"regime":"RISK_OFF","ems":61,"ffs":66,"cds":60,"ias":54,"cbs":69,"mes":56,"invalidation":"GCZ26_above_4040","verification_target":"GCZ26","verified_status":"partially_verified"},
  {"date":"2026-11-13","signal_id":"20261113_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":44,"opp_score":37,"no_trade_score":77,"risk_pct":"","regime":"RISK_OFF","ems":49,"ffs":44,"cds":42,"ias":35,"cbs":48,"mes":39,"invalidation":"ETF_CME_confirmation_missing","verification_target":"BTCUSD_spot","verified_status":"partially_verified"},
  {"date":"2026-11-13","signal_id":"20261113_ETH_SELL_PULLBACK","asset":"ETH","side":"SELL","rank":"B","type":"PULLBACK","entry_low":2030,"entry_high":2080,"sl":2240,"tp1":1770,"tp2":1650,"rr":1.54,"win_prob":0.51,"expected_r":0.16,"tq_score":59,"opp_score":60,"no_trade_score":34,"risk_pct":0.25,"regime":"RISK_OFF","ems":55,"ffs":57,"cds":49,"ias":45,"cbs":61,"mes":44,"invalidation":"ETHUSD_above_2240","verification_target":"ETHUSD_spot","verified_status":"partially_verified"},
  {"date":"2026-11-13","signal_id":"20261113_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":40,"opp_score":31,"no_trade_score":84,"risk_pct":"","regime":"EVENT","ems":40,"ffs":32,"cds":36,"ias":28,"cbs":43,"mes":35,"invalidation":"supply_shock","verification_target":"CLZ26","verified_status":"partially_verified"},
  {"date":"2026-11-13","signal_id":"20261113_USDJPY_BUY_PULLBACK","asset":"USDJPY","side":"BUY","rank":"B","type":"PULLBACK","entry_low":159.3,"entry_high":159.8,"sl":157.9,"tp1":162.4,"tp2":163.5,"rr":1.73,"win_prob":0.51,"expected_r":0.21,"tq_score":63,"opp_score":65,"no_trade_score":34,"risk_pct":0.25,"regime":"EVENT","ems":58,"ffs":61,"cds":56,"ias":44,"cbs":67,"mes":59,"invalidation":"USDJPY_below_157.9_or_intervention","verification_target":"USDJPY_spot","verified_status":"partially_verified"},
  {"date":"2026-11-13","signal_id":"20261113_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":43,"opp_score":38,"no_trade_score":75,"risk_pct":"","regime":"RISK_OFF","ems":49,"ffs":43,"cds":47,"ias":38,"cbs":51,"mes":47,"invalidation":"ES_contract_quote_missing","verification_target":"ES_futures","verified_status":"unverified"},
  {"date":"2026-11-13","signal_id":"20261113_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":49,"opp_score":47,"no_trade_score":69,"risk_pct":"","regime":"RISK_OFF","ems":53,"ffs":48,"cds":46,"ias":42,"cbs":57,"mes":48,"invalidation":"NQ_contract_quote_missing","verification_target":"NQ_futures","verified_status":"unverified"},
  {"date":"2026-11-13","signal_id":"20261113_DXY_BUY_PULLBACK","asset":"DXY","side":"BUY","rank":"B","type":"PULLBACK","entry_low":102.9,"entry_high":103.3,"sl":102.1,"tp1":104.9,"tp2":105.7,"rr":1.8,"win_prob":0.53,"expected_r":0.25,"tq_score":65,"opp_score":67,"no_trade_score":30,"risk_pct":0.25,"regime":"RISK_OFF","ems":62,"ffs":64,"cds":56,"ias":52,"cbs":70,"mes":61,"invalidation":"DXY_below_102.1","verification_target":"DXY_index","verified_status":"partially_verified"},
  {"date":"2026-11-13","signal_id":"20261113_US10Y_BUY_MOMENTUM","asset":"US10Y","side":"BUY","rank":"B","type":"MOMENTUM","entry_low":5.06,"entry_high":5.12,"sl":4.96,"tp1":5.38,"tp2":5.52,"rr":2.23,"win_prob":0.52,"expected_r":0.22,"tq_score":62,"opp_score":64,"no_trade_score":32,"risk_pct":0.25,"regime":"EVENT","ems":60,"ffs":63,"cds":52,"ias":46,"cbs":68,"mes":57,"invalidation":"US10Y_below_4.96","verification_target":"US10Y_yield","verified_status":"partially_verified"},
  {"date":"2026-11-13","signal_id":"20261113_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":42,"opp_score":35,"no_trade_score":79,"risk_pct":"","regime":"MIXED","ems":46,"ffs":42,"cds":41,"ias":36,"cbs":44,"mes":40,"invalidation":"VIX_index_quote_missing","verification_target":"VIX_index","verified_status":"unverified"}
]
```

**記録状態：** 10資産の当日TSO\_LOG生成完了。前日までのinvalidation照合とATR10の実測検証は未完了。これらは当日の方向推定と区別し、後日検証時に補完する。
