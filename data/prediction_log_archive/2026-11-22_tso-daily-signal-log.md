<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-11-22 07:00 JST -->
<!-- transport: Complete original read_thread message 818f3c0a-1a3e-42f9-bf73-ea4c228351dd; raw markdown -->
<!-- archived_at: 2026-11-21T22:57:58Z / chars: 11571 / 値は無修正 -->

# Tactical Swing OS v2 — 2026年11月22日（日）

実行モデル：GPT-6
判断基準：11月20日（金）の米国市場終値および11月21日までの報道
本日の市場の主役：**NASDAQ**

## 1\. 本日の結論

**A級：0件 / B級：5件 / NO\_TRADE：5件**

米国株式・暗号資産・金が同時に売られるリスクオフ局面が継続。方向性が最も明確なのはNASDAQの下落だが、急落後の反発幅と価格変動の大きさを考慮し、今回はA級への昇格を見送る。

| 優先 | 資産 | 方向 | 判定 | expected\_r |
|--------|--------|--------|--------|--------|
| 1 | NASDAQ | SELL | B | \+0.39R |
| 2 | SPX | SELL | B | \+0.31R |
| 3 | GOLD | SELL | B | \+0.28R |
| 4 | USDJPY | SELL | B | \+0.22R |
| 5 | WTI | SELL | B | \+0.16R |

NASDAQとSPXは同一の株式リスク要因に強く依存する。両方のシグナルを記録するが、独立した投資機会としてリスクを単純加算しない。

日曜日のため、株式・金・原油・為替の新規判断は次の取引セッションに向けた監視判断である。

**データ上の制約：** 11月20日の市場報道には価格差や参照系列の相違がある。10本の日足OHLCを完全取得できていないため、今回のSLはATR10実測値ではなく、十分な値幅を想定した暫定水準である。したがって、全行を `partially_verified` とし、ATR10下限への適合は未確定とする。

## 2\. 前回判断の簡易検証

前回11月21日の最新方向判断を確認した。

| 資産 | 前回signal\_id | 前回invalidation | 今回判定 |
|--------|--------|--------|--------|
| GOLD | 20261121\_GOLD\_SELL\_PULLBACK | 3780超 | unknown |
| WTI | 20261121\_WTI\_SELL\_PULLBACK | 89超 | unknown |
| USDJPY | 20261121\_USDJPY\_SELL\_REVERSAL | 161超 | unknown |
| SPX | 20261121\_SPX\_SELL\_PULLBACK | 7500超 | unknown |
| NASDAQ | 20261121\_NASDAQ\_SELL\_PULLBACK | 27500超 | unknown |

上記は11月21日の判断以降の同一系列高値を十分に確認できないため、発動・未発動を確定していない。前回までの方向判断を新しいB級判断の停止理由にはしない。

ETHについては11月中旬のSELL判断が存在するが、直近5営業日窓における最新の対象IDと無効化価格を完全に復元できなかったため、誤ったIDを追加しない。

`invalidation_check: 20261121_GOLD_SELL_PULLBACK=unknown, 20261121_WTI_SELL_PULLBACK=unknown, 20261121_USDJPY_SELL_REVERSAL=unknown, 20261121_SPX_SELL_PULLBACK=unknown, 20261121_NASDAQ_SELL_PULLBACK=unknown`

## 3\. 市場全体の前提

11月20日の米国市場では、テクノロジー株の急落と投資家のリスク削減が中心テーマとなった。ReutersはNASDAQの5.3%下落、VIXの37付近への急上昇、米10年債利回りの4.93%付近への低下を報じている。citeturn578235news26turn578235news29

金も大きく下落。原油は地政学的な供給不安から金曜日に反発しており、株式と同じ方向に機械的に売る環境ではない。citeturn578235news24turn578235news28

| 市場指標 | 参考値 | データ上の注意 |
|--------|--------|--------|
| BTC/USD | 約59,075 | 11/20の市場集計 |
| ETH/USD | 約1,632 | 11/20の市場集計 |
| GOLD | 約3,512〜3,532 | COMEX報道値、12月限との同一性未確定 |
| WTI | 83.98 | 11/20決済報道、限月照合要 |
| USDJPY | 約161.00 | 市場集計、別時点の報道は159円台 |
| SPX | 約7,021 | S&amp;P現物指数参考値、ESではない |
| NASDAQ | 約25,554 | NASDAQ100指数参考値、NQではない |
| DXY | 約103.84 | 市場集計 |
| US10Y | 約4.91〜4.94% | データ提供元で差 |
| VIX | 約35.9〜37 | 終値系列・報道時点で差 |

価格参照：citeturn578235search0turn578235search4turn578235search5turn578235news26turn578235news28

GOLDの基準限月は\*\*COMEX 2026年12月限（GCZ26）\*\*を維持する。報道値を異なる限月の価格として連結しない。SPXとNASDAQの現物指数値も、ES・NQ先物価格としてLOGへ代入していない。

全体レジーム：**RISK\_OFF**

## 4\. 10資産別判断

以下のEntry・SL・TPは監視用のモデル推定値であり、確認済み市場注文価格ではない。RRはEntry中点から計算済み。

| 資産 | 判断 | Entry帯 | SL | TP1 | RR |
|--------|--------|--------|--------|--------|--------|
| GOLD | B SELL | 3510–3560 | 3790 | 3100 | 1.706 |
| BTC | NO\_TRADE | — | — | — | — |
| ETH | NO\_TRADE | — | — | — | — |
| WTI | B SELL | 83–85 | 94 | 70 | 1.400 |
| USDJPY | B SELL | 159–161 | 165 | 151 | 1.800 |
| SPX（ES） | B SELL | 7040–7180 | 7600 | 6500 | 1.245 |
| NASDAQ（NQ） | B SELL | 25600–26300 | 28900 | 22200 | 1.271 |
| DXY | NO\_TRADE | — | — | — | — |
| US10Y | NO\_TRADE | — | — | — | — |
| VIX | NO\_TRADE | — | — | — | — |

GOLDは金利・ドル高圧力と資産売却が重なる下落継続を想定。USDJPYは円高への反転を監視するが、介入・政策発言による急変を重視する。WTIは供給ショック時の上昇リスクが大きい。

NASDAQは売り方向の見立てが最も強い。Entry未到達による不参加確率はexpected\_rから控除していない。5営業日の時間決済を前提とする。

## 5\. A級候補

**該当なし。**

NASDAQはCBS76・EMS71を満たすが、expected\_rが0.39Rであり0.45Rに届かない。さらにATR10実測によるSL検証が未完了。

## 6\. B級監視候補

5件をB級として記帳する。B+条件をすべて満たす候補は今回はなし。

MAE想定はNASDAQ 0.35R、SPX 0.33R、GOLD 0.38R、USDJPY 0.42R、WTI 0.45R。いずれも主観推定であり、A級基準の0.25Rを上回る。

リスク配分は各0.25%、日次合計上限0.50%。5件同時採用を意味しない。

## 7\. 触らない資産

BTCは下落方向の圧力があるものの、ETF・CME情報が不足しMES39。ETHは弱いが、反発と下落継続の判別が不十分。DXYは強いドルと金曜日の反落が混在する。US10Yは債券への逃避需要と金融引き締め見通しが交錯。VIXは急騰後の反落リスクが大きい。

## 8\. 後日検証ポイント

- NASDAQとSPXの下落継続、および反発時のMAE。
- GOLDの12月限同一系列OHLCとATR10の再確認。
- WTIの供給関連ニュースと限月ロール。
- USDJPYの161円付近の反転判断と介入リスク。
- 11月21日までの未決着判断について、次の価格更新後にinvalidationを再判定。

## 9\. Obsidian保存用Observation Draft

```markdown
# TSO Observation 2026-11-22

model: GPT-6
regime: RISK_OFF
market_leader: NASDAQ
A_count: 0
B_count: 5
NO_TRADE_count: 5
data_quality: partially_verified

## Hypothesis
米国テクノロジー株の急落が市場全体の
リスク削減を主導する。

## Primary observation
NASDAQ SELL_PULLBACK
CBS=76
EMS=71
expected_r=0.39
rank=B

## Secondary observations
SPX SELL
GOLD SELL
USDJPY SELL
WTI SELL

## Verification debt
- ATR10 actual calculation
- GCZ26 same-contract prices
- ES/NQ futures settlement confirmation
- Previous invalidation price checks
- BTC ETF/CME flow confirmation

## Exit policy
5 business days; TP1/TP2 reference only.

## Status
Observation recorded.
Execution not confirmed.
```

## 10\. TSO\_LOG — CSV / JSON

固定28列、10資産各1行。CSVは各データ行27個のカンマを確認済み。RRはEntry中点・SL・TP1から再計算済み。

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-11-22,20261122_GOLD_SELL_PULLBACK,GOLD,SELL,B,PULLBACK,3510,3560,3790,3100,2950,1.706,0.54,0.28,70,72,25,0.25,RISK_OFF,66,59,63,61,72,62,above_3790,COMEX_GCZ26,partially_verified
2026-11-22,20261122_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,53,47,75,,RISK_OFF,49,44,51,48,54,39,ETF_CME_confirmation_missing,BTCUSD_spot,partially_verified
2026-11-22,20261122_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,59,54,62,,RISK_OFF,55,47,55,52,60,43,trend_break_confirmation,ETHUSD_spot,partially_verified
2026-11-22,20261122_WTI_SELL_PULLBACK,WTI,SELL,B,PULLBACK,83,85,94,70,66,1.4,0.51,0.16,63,60,39,0.25,EVENT,60,55,58,48,65,54,above_94_or_supply_shock,WTI_CLF27,partially_verified
2026-11-22,20261122_USDJPY_SELL_REVERSAL,USDJPY,SELL,B,REVERSAL,159,161,165,151,148,1.8,0.52,0.22,67,67,34,0.25,EVENT,62,60,55,59,70,59,above_165_or_intervention,USDJPY_spot,partially_verified
2026-11-22,20261122_SPX_SELL_PULLBACK,SPX,SELL,B,PULLBACK,7040,7180,7600,6500,6250,1.245,0.55,0.31,74,75,26,0.25,RISK_OFF,69,62,66,67,74,65,above_7600,ES_futures,partially_verified
2026-11-22,20261122_NASDAQ_SELL_PULLBACK,NASDAQ,SELL,B,PULLBACK,25600,26300,28900,22200,21000,1.271,0.57,0.39,76,80,23,0.25,RISK_OFF,71,65,67,69,76,67,above_28900,NQ_futures,partially_verified
2026-11-22,20261122_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,57,51,60,,MIXED,54,50,49,48,58,52,dollar_index_structure,DXY_index,partially_verified
2026-11-22,20261122_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,58,50,64,,MIXED,52,49,53,50,56,49,yield_structure,US10Y_yield_pct,partially_verified
2026-11-22,20261122_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,65,40,81,,RISK_OFF,58,50,46,43,60,55,volatility_spike,VIX_index,partially_verified
```

JSONは同じ28列のキーを保持した10件の配列。

```json
[
  {"date":"2026-11-22","signal_id":"20261122_GOLD_SELL_PULLBACK","asset":"GOLD","side":"SELL","rank":"B","type":"PULLBACK","entry_low":3510,"entry_high":3560,"sl":3790,"tp1":3100,"tp2":2950,"rr":1.706,"win_prob":0.54,"expected_r":0.28,"tq_score":70,"opp_score":72,"no_trade_score":25,"risk_pct":0.25,"regime":"RISK_OFF","ems":66,"ffs":59,"cds":63,"ias":61,"cbs":72,"mes":62,"invalidation":"above_3790","verification_target":"COMEX_GCZ26","verified_status":"partially_verified"},
  {"date":"2026-11-22","signal_id":"20261122_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":53,"opp_score":47,"no_trade_score":75,"risk_pct":"","regime":"RISK_OFF","ems":49,"ffs":44,"cds":51,"ias":48,"cbs":54,"mes":39,"invalidation":"ETF_CME_confirmation_missing","verification_target":"BTCUSD_spot","verified_status":"partially_verified"},
  {"date":"2026-11-22","signal_id":"20261122_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":59,"opp_score":54,"no_trade_score":62,"risk_pct":"","regime":"RISK_OFF","ems":55,"ffs":47,"cds":55,"ias":52,"cbs":60,"mes":43,"invalidation":"trend_break_confirmation","verification_target":"ETHUSD_spot","verified_status":"partially_verified"},
  {"date":"2026-11-22","signal_id":"20261122_WTI_SELL_PULLBACK","asset":"WTI","side":"SELL","rank":"B","type":"PULLBACK","entry_low":83,"entry_high":85,"sl":94,"tp1":70,"tp2":66,"rr":1.4,"win_prob":0.51,"expected_r":0.16,"tq_score":63,"opp_score":60,"no_trade_score":39,"risk_pct":0.25,"regime":"EVENT","ems":60,"ffs":55,"cds":58,"ias":48,"cbs":65,"mes":54,"invalidation":"above_94_or_supply_shock","verification_target":"WTI_CLF27","verified_status":"partially_verified"},
  {"date":"2026-11-22","signal_id":"20261122_USDJPY_SELL_REVERSAL","asset":"USDJPY","side":"SELL","rank":"B","type":"REVERSAL","entry_low":159,"entry_high":161,"sl":165,"tp1":151,"tp2":148,"rr":1.8,"win_prob":0.52,"expected_r":0.22,"tq_score":67,"opp_score":67,"no_trade_score":34,"risk_pct":0.25,"regime":"EVENT","ems":62,"ffs":60,"cds":55,"ias":59,"cbs":70,"mes":59,"invalidation":"above_165_or_intervention","verification_target":"USDJPY_spot","verified_status":"partially_verified"},
  {"date":"2026-11-22","signal_id":"20261122_SPX_SELL_PULLBACK","asset":"SPX","side":"SELL","rank":"B","type":"PULLBACK","entry_low":7040,"entry_high":7180,"sl":7600,"tp1":6500,"tp2":6250,"rr":1.245,"win_prob":0.55,"expected_r":0.31,"tq_score":74,"opp_score":75,"no_trade_score":26,"risk_pct":0.25,"regime":"RISK_OFF","ems":69,"ffs":62,"cds":66,"ias":67,"cbs":74,"mes":65,"invalidation":"above_7600","verification_target":"ES_futures","verified_status":"partially_verified"},
  {"date":"2026-11-22","signal_id":"20261122_NASDAQ_SELL_PULLBACK","asset":"NASDAQ","side":"SELL","rank":"B","type":"PULLBACK","entry_low":25600,"entry_high":26300,"sl":28900,"tp1":22200,"tp2":21000,"rr":1.271,"win_prob":0.57,"expected_r":0.39,"tq_score":76,"opp_score":80,"no_trade_score":23,"risk_pct":0.25,"regime":"RISK_OFF","ems":71,"ffs":65,"cds":67,"ias":69,"cbs":76,"mes":67,"invalidation":"above_28900","verification_target":"NQ_futures","verified_status":"partially_verified"},
  {"date":"2026-11-22","signal_id":"20261122_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":57,"opp_score":51,"no_trade_score":60,"risk_pct":"","regime":"MIXED","ems":54,"ffs":50,"cds":49,"ias":48,"cbs":58,"mes":52,"invalidation":"dollar_index_structure","verification_target":"DXY_index","verified_status":"partially_verified"},
  {"date":"2026-11-22","signal_id":"20261122_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":58,"opp_score":50,"no_trade_score":64,"risk_pct":"","regime":"MIXED","ems":52,"ffs":49,"cds":53,"ias":50,"cbs":56,"mes":49,"invalidation":"yield_structure","verification_target":"US10Y_yield_pct","verified_status":"partially_verified"},
  {"date":"2026-11-22","signal_id":"20261122_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":65,"opp_score":40,"no_trade_score":81,"risk_pct":"","regime":"RISK_OFF","ems":58,"ffs":50,"cds":46,"ias":43,"cbs":60,"mes":55,"invalidation":"volatility_spike","verification_target":"VIX_index","verified_status":"partially_verified"}
]
```

**本日の記録結果：10資産すべて記帳。** 方向あり5件、見送り5件。最大の未解決事項はATR10実測と先物参照系列の整合確認であり、今回の数値はその検証を残した暫定判断として扱う。
