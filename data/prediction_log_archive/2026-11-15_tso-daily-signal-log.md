<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-11-15 07:00 JST -->
<!-- transport: Complete original read_thread message 8086283b-6a16-4394-9328-fea6a66f256d; raw markdown -->
<!-- archived_at: 2026-11-14T22:56:29Z / chars: 10581 / 値は無修正 -->

# Tactical Swing OS — 2026年11月15日（日）

実行モデル：GPT-6
本日の市場の主役：BTC
運用モード：通常寄り防御
市場レジーム：RISK\_OFF

## 1\. 本日の結論

**A級候補0件、B級監視候補2件、NO\_TRADE 8件。**

本日は日曜日であり、米国株価指数先物・金・原油などの通常取引は週末休場中です。暗号資産は取引されていますが、BTCの急落が続いており、週末流動性と価格変動の不確実性が大きくなっています。

11月13日のBTCは約69,135ドルでしたが、14日の報道では64,000ドル割れが伝えられています。ETHも2,000ドルを割り込みました。citeturn325991news2turn325991news10turn325991news8

方向性としてはGOLDとETHの戻り売りを監視します。ただし、今回のB級価格帯は暫定設計であり、**ATR10の実測照合が完了していません。** A級への昇格は行いません。

## 2\. 前回判断の簡易検証

11月14日までの各資産の最新signal\_idと、そのinvalidation水準を今回の取得資料から確定できませんでした。そのため、発動・非発動を推測しません。

`invalidation_check:` 対象signal\_id未復元のため個別判定保留

これは指定された最大10件の検証を完了したという意味ではありません。過去の最新方向あり判断と、その判断日以降の高値・安値を照合する作業が未完了です。

## 3\. 市場全体の前提

| 指標 | 確認した参考値 | データ時点 |
|--------|--------|--------|
| GOLD（COMEX 2026年12月限） | 3886.30 | 11/13清算値 |
| BTC/USD | 64000割れとの報道 | 11/14 |
| ETH/USD | 約1905 | 11/14掲載値 |
| WTI先物 | 88.46 | 11/13取引時間中 |
| ES先物 | 7624.00 | 11/13米国市場前 |
| NQ先物 | 28379.75 | 11/13米国市場前 |
| DXY | 103.22 | 11/13取引時間中 |
| US10Y | 5.103% | 11/12終値 |
| VIX | 18.37 | 11/13米国市場前 |

金12月限の清算値はReuters、その他の複数指標は市場データ記事、ETHはYahoo Financeの履歴を参照しました。これらは同時刻の価格ではなく、ES・NQについては金曜日の最終清算値でもありません。citeturn325991news36turn325991news0turn325991search11

市場の主要なリスクは、米金利上昇への警戒、暗号資産からの資金流出、株式市場のリスク許容度低下です。BTCのETF資金流出とレバレッジポジションの清算も確認されています。citeturn325991news35turn325991news37

## 4\. 10資産別判断

| 資産 | 判断 | 理由 |
|--------|--------|--------|
| GOLD | B SELL | 金利上昇環境で戻り売り優勢 |
| BTC | NO\_TRADE | 下落方向だがETF・CMEと週末流動性の確認不足 |
| ETH | B SELL | 2000ドル割れと資金流出 |
| WTI | NO\_TRADE | 供給要因と先物限月の精査不足 |
| USDJPY | NO\_TRADE | 同一時点のドル円水準未確認 |
| SPX | NO\_TRADE | ES最終清算値・ATR未確認 |
| NASDAQ | NO\_TRADE | NQ最終清算値・ATR未確認 |
| DXY | NO\_TRADE | 方向性はドル高寄りだが値幅不足 |
| US10Y | NO\_TRADE | 高金利方向だが直近水準の確認不足 |
| VIX | NO\_TRADE | 株式市場休場中で判断材料不足 |

## 5\. A級候補

該当なし。

CBS、EMS、expected\_rの条件を満たす可能性がある資産についても、1×ATR10の実測確認ができていないためA級認定は保留します。

## 6\. B級監視候補

| 項目 | GOLD SELL | ETH SELL |
|--------|--------|--------|
| Entry | 3860–3900 | 1880–1920 |
| Entry中点 | 3880 | 1900 |
| SL | 4050 | 2100 |
| TP1 | 3600 | 1600 |
| TP2 | 3450 | 1500 |
| RR | 1.65 | 1.50 |
| win\_prob | 0.53 | 0.54 |
| expected\_r | \+0.26 | \+0.29 |
| 想定MAE | 0.45R | 0.48R |
| risk\_pct | 0.25% | 0.25% |

RRは中点から再計算済みです。GOLDは280÷170＝1.647、ETHは300÷200＝1.500です。

**B+観察候補はありません。** 両資産ともCBS・EMSの条件を満たさないためです。

SL距離が実測ATR10以上であることは未検証です。今回の価格帯を確定した執行水準と扱わず、月曜日の取引再開時に再照合する必要があります。

## 7\. 触らない資産

BTCは下落が強いものの、週末の急変動後であり、ETF・CMEの根拠不足を考慮してNO\_TRADEとします。NASDAQとSPXは週末の間に新たな先物清算値が形成されていません。

WTIについても、供給ショック直後のmomentum追随を避ける規則を維持します。

## 8\. 後日検証ポイント

1. BTCが64,000ドルを回復するか、下回った状態を維持するか。
2. ETHが1,900ドル近辺で反発するか、下落を継続するか。
3. GOLD12月限が3,900ドルを回復できるか。
4. 月曜日のES・NQ先物で週末のリスクオフが継続するか。
5. 各資産の直近10営業日OHLCからATR10を再計算し、B級SLの適合性を検証する。

## 9\. Obsidian保存用Observation Draft

```markdown
# TSO Observation 2026-11-15

model: GPT-6
market_leader: BTC
regime: RISK_OFF
mode: normal_defensive

## Summary
- A: 0
- B: 2
- NO_TRADE: 8
- Market: weekend, crypto selloff
- GOLD reference: COMEX 2026-12
- Primary concern: BTC downside and US rate expectations

## Hypotheses
- GOLD: SELL pullback
- ETH: SELL pullback
- BTC: bearish, but no entry authorization
- Other seven assets: NO_TRADE

## Verification limitations
- ATR10 actual values not confirmed
- Previous signal IDs not restored
- ES/NQ final settlements not confirmed
- ETF/CME evidence incomplete
- B entry/SL/TP values provisional

## Next review
- Recalculate ATR10
- Check latest historical invalidations
- Re-evaluate after Monday futures reopening
```

## 10\. TSO\_LOG CSVとJSON

以下のスコアは、取得した市場情報に基づくモデルの暫定主観評価です。価格未確認の資産も10行を維持し、`verified_status`で区別しています。

### CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-11-15,20261115_GOLD_SELL_PULLBACK,GOLD,SELL,B,PULLBACK,3860,3900,4050,3600,3450,1.65,0.53,0.26,63,66,38,0.25,RISK_OFF,61,57,58,53,68,57,above_4050,GOLD_DEC26_ATR10,partially_verified
2026-11-15,20261115_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,42,48,82,,RISK_OFF,46,39,43,40,52,38,ETF_CME_unconfirmed,BTC_USD_spot,partially_verified
2026-11-15,20261115_ETH_SELL_PULLBACK,ETH,SELL,B,PULLBACK,1880,1920,2100,1600,1500,1.50,0.54,0.29,62,65,40,0.25,RISK_OFF,60,54,57,51,67,46,above_2100,ETH_USD_ATR10,partially_verified
2026-11-15,20261115_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,40,39,79,,EVENT,43,38,40,36,42,44,supply_shock_unconfirmed,WTI_futures,partially_verified
2026-11-15,20261115_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,45,44,75,,MIXED,48,45,43,40,49,48,USDJPY_reference_missing,USDJPY_spot,unverified
2026-11-15,20261115_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,47,45,73,,RISK_OFF,49,45,44,42,50,46,ES_final_close_missing,ES_futures,partially_verified
2026-11-15,20261115_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,48,49,72,,RISK_OFF,51,47,45,43,53,47,NQ_final_close_missing,NQ_futures,partially_verified
2026-11-15,20261115_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,51,47,65,,RISK_OFF,54,48,49,46,55,51,DXY_ATR_missing,DXY_index,partially_verified
2026-11-15,20261115_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,48,43,71,,EVENT,50,46,43,42,51,47,US10Y_latest_missing,US10Y_yield,partially_verified
2026-11-15,20261115_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,39,36,81,,RISK_OFF,43,41,38,35,42,40,VIX_final_close_missing,VIX_index,partially_verified
```

### JSON

```json
[
  {"date":"2026-11-15","signal_id":"20261115_GOLD_SELL_PULLBACK","asset":"GOLD","side":"SELL","rank":"B","type":"PULLBACK","entry_low":3860,"entry_high":3900,"sl":4050,"tp1":3600,"tp2":3450,"rr":1.65,"win_prob":0.53,"expected_r":0.26,"tq_score":63,"opp_score":66,"no_trade_score":38,"risk_pct":0.25,"regime":"RISK_OFF","ems":61,"ffs":57,"cds":58,"ias":53,"cbs":68,"mes":57,"invalidation":"above_4050","verification_target":"GOLD_DEC26_ATR10","verified_status":"partially_verified"},
  {"date":"2026-11-15","signal_id":"20261115_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":42,"opp_score":48,"no_trade_score":82,"risk_pct":null,"regime":"RISK_OFF","ems":46,"ffs":39,"cds":43,"ias":40,"cbs":52,"mes":38,"invalidation":"ETF_CME_unconfirmed","verification_target":"BTC_USD_spot","verified_status":"partially_verified"},
  {"date":"2026-11-15","signal_id":"20261115_ETH_SELL_PULLBACK","asset":"ETH","side":"SELL","rank":"B","type":"PULLBACK","entry_low":1880,"entry_high":1920,"sl":2100,"tp1":1600,"tp2":1500,"rr":1.50,"win_prob":0.54,"expected_r":0.29,"tq_score":62,"opp_score":65,"no_trade_score":40,"risk_pct":0.25,"regime":"RISK_OFF","ems":60,"ffs":54,"cds":57,"ias":51,"cbs":67,"mes":46,"invalidation":"above_2100","verification_target":"ETH_USD_ATR10","verified_status":"partially_verified"},
  {"date":"2026-11-15","signal_id":"20261115_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":40,"opp_score":39,"no_trade_score":79,"risk_pct":null,"regime":"EVENT","ems":43,"ffs":38,"cds":40,"ias":36,"cbs":42,"mes":44,"invalidation":"supply_shock_unconfirmed","verification_target":"WTI_futures","verified_status":"partially_verified"},
  {"date":"2026-11-15","signal_id":"20261115_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":45,"opp_score":44,"no_trade_score":75,"risk_pct":null,"regime":"MIXED","ems":48,"ffs":45,"cds":43,"ias":40,"cbs":49,"mes":48,"invalidation":"USDJPY_reference_missing","verification_target":"USDJPY_spot","verified_status":"unverified"},
  {"date":"2026-11-15","signal_id":"20261115_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":47,"opp_score":45,"no_trade_score":73,"risk_pct":null,"regime":"RISK_OFF","ems":49,"ffs":45,"cds":44,"ias":42,"cbs":50,"mes":46,"invalidation":"ES_final_close_missing","verification_target":"ES_futures","verified_status":"partially_verified"},
  {"date":"2026-11-15","signal_id":"20261115_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":48,"opp_score":49,"no_trade_score":72,"risk_pct":null,"regime":"RISK_OFF","ems":51,"ffs":47,"cds":45,"ias":43,"cbs":53,"mes":47,"invalidation":"NQ_final_close_missing","verification_target":"NQ_futures","verified_status":"partially_verified"},
  {"date":"2026-11-15","signal_id":"20261115_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":51,"opp_score":47,"no_trade_score":65,"risk_pct":null,"regime":"RISK_OFF","ems":54,"ffs":48,"cds":49,"ias":46,"cbs":55,"mes":51,"invalidation":"DXY_ATR_missing","verification_target":"DXY_index","verified_status":"partially_verified"},
  {"date":"2026-11-15","signal_id":"20261115_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":48,"opp_score":43,"no_trade_score":71,"risk_pct":null,"regime":"EVENT","ems":50,"ffs":46,"cds":43,"ias":42,"cbs":51,"mes":47,"invalidation":"US10Y_latest_missing","verification_target":"US10Y_yield","verified_status":"partially_verified"},
  {"date":"2026-11-15","signal_id":"20261115_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":39,"opp_score":36,"no_trade_score":81,"risk_pct":null,"regime":"RISK_OFF","ems":43,"ffs":41,"cds":38,"ias":35,"cbs":42,"mes":40,"invalidation":"VIX_final_close_missing","verification_target":"VIX_index","verified_status":"partially_verified"}
]
```

**記録結果：10資産、28列形式で出力。** 本日の最大の未完了事項は、過去signal\_idの個別invalidation照合とATR10の実測確認です。これらを未確認のままA級認定したり、過去シグナルの発動を推測したりすることは避けています。
