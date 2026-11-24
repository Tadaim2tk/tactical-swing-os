<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-11-20 07:00 JST -->
<!-- transport: Complete original read_thread message 426dd656-a12a-4f81-808b-2773a296199a; raw markdown -->
<!-- archived_at: 2026-11-19T23:02:06Z / chars: 8494 / 値は無修正 -->

# Tactical Swing OS 日次判断 — 2026年11月20日（金）

実行モデル：GPT-6
本日の市場の主役：**GOLD**

## 1\. 本日の結論

**A級：0件、B級：5件、NO\_TRADE：5件。**

米国の金融引き締め観測、ドル高、金価格の下落、株式市場の不安定化を踏まえ、方向性のある5資産をB級として記帳する。

金曜日であることから週末のギャップリスクを考慮する。ただし、週末リスクだけを理由に方向判断を取り消さない。

| 優先 | 資産 | 判断 | 主観勝率 | expected\_r |
|--------|--------|--------|--------|--------|
| 1 | GOLD | B / SELL | 0.54 | \+0.28R |
| 2 | USDJPY | B / BUY | 0.55 | \+0.32R |
| 3 | SPX | B / SELL | 0.53 | \+0.27R |
| 4 | NASDAQ | B / SELL | 0.52 | \+0.25R |
| 5 | WTI | B / SELL | 0.51 | \+0.19R |

いずれもA級条件を満たさない。B級の記録は継続する。

本日の市場データは主として11月19日の終値・日中価格に基づく。11月20日午前7時時点の完全なリアルタイム値ではない。

## 2\. 前回判断の簡易検証

前回の方向あり判断について、最新のsignal\_idとinvalidation水準を含む完全な台帳を今回取得できていない。そのため、個別のfired判定を推測で補完しない。

**invalidation\_check\:** 前回の個別signal\_id未照合。対象の確定と価格照合が未完了。

本日の新規5件は、前回判断の結果とは独立して評価した。

## 3\. 市場全体の前提

11月19日の市場情報では、FRBのタカ派的な政策見通しを背景にドルと米国債利回りが上昇し、金やリスク資産に圧力がかかっている。citeturn501425search6turn501425search7turn501425news34

| 指標 | 参照水準 | 状況 |
|--------|--------|--------|
| COMEX GOLD 12月限 | 3680.17 | 下落基調 |
| BTC/USD | 約63550 | 弱含み |
| ETH/USD | 約1802 | 弱含み |
| WTI | 約82.75〜83.32 | 下落基調 |
| USDJPY | 約159.6 | ドル高 |
| ES 12月限 | 7293.50 | 下落基調 |
| NQ 12月限 | 27258.00 | 戻りと不安定さが併存 |
| DXY | 約103.95 | ドル高 |
| US10Y | 約5.08% | 高金利 |
| VIX | 約24.56 | 警戒水準 |

出典：Investing.comの先物履歴、11月19日付市場レポート。citeturn208745search2turn208745search0turn208745search4turn501425search1turn501425search6turn501425search4

注意点として、GOLDはGCZ6、SPXはESZ6、NASDAQはNQZ6を使用した。WTIの取得系列には限月の確認が残るため、監視価格は暫定値とする。

## 4\. 10資産別判断

| 資産 | 判断 | 根拠・留意点 |
|--------|--------|--------|
| GOLD | B SELL | 金利上昇とドル高が逆風。戻り売りを優先 |
| BTC | NO\_TRADE | ETF/CME裏付け不足、MES38 |
| ETH | NO\_TRADE | BTCと連動した弱さ。独立した優位性が弱い |
| WTI | B SELL | 下落継続を想定。ただし供給ショックに注意 |
| USDJPY | B BUY | ドル高継続。ただし160円付近の介入リスク |
| SPX | B SELL | 株式全体の弱さを評価 |
| NASDAQ | B SELL | 戻り局面を売り方向で監視 |
| DXY | NO\_TRADE | ドル高だが具体的な参加条件が弱い |
| US10Y | NO\_TRADE | 金利高止まり、方向の優位性不足 |
| VIX | NO\_TRADE | 高水準だが方向性が不安定 |

### B級の価格設定

| 資産 | Entry帯 | SL | TP1 | TP2 | RR |
|--------|--------|--------|--------|--------|--------|
| GOLD SELL | 3690–3740 | 3830 | 3510 | 3400 | 1.783 |
| WTI SELL | 82–84 | 87 | 76 | 73 | 1.750 |
| USDJPY BUY | 159.3–159.7 | 158.3 | 161.5 | 162.2 | 1.667 |
| SPX SELL | 7270–7330 | 7500 | 6990 | 6850 | 1.550 |
| NASDAQ SELL | 27100–27400 | 28300 | 25600 | 24900 | 1.571 |

RRはEntry中点から再計算済み。

ATR10については、GOLD・SPX・NASDAQ・WTIの直近の日足レンジを参照した。USDJPYは取得した履歴から概算した。いずれも厳密な統一セッションによるATR10の再計算が完了していないため、**SLの1×ATR10適合は暫定判定**とする。実際の発注前には再照合が必要。

想定MAEはGOLD 0.30R、WTI 0.40R、USDJPY 0.35R、SPX 0.33R、NASDAQ 0.38R。いずれもA級上限の0.25Rを超える。

NASDAQとUSDJPYには、Entry帯未到達時の判断日終値成行参加規則を適用する。expected\_rには未参加確率を二重計上していない。

## 5\. A級候補

**該当なし。**

CBS75以上、EMS65以上、expected\_r0.45以上、MAE0.25R以下の条件を同時に満たす候補はない。

## 6\. B級監視候補

GOLD、USDJPY、SPX、NASDAQ、WTIの5件。

GOLDとUSDJPYが相対的に強い方向判断。ただしUSDJPYは160円付近での政策対応、GOLDは急落後の反発が主なリスク。

B+観察候補の追加条件を全て満たす銘柄はない。

通常リスク0.25%、日次合計0.50%を維持する。5件を同時に建てることは想定しない。

## 7\. 触らない資産

BTC、ETH、DXY、US10Y、VIX。

BTCはMES38であり、ETFフローとCME建玉の十分な確認もできていないため、運用ルール上NO\_TRADEを優先する。

## 8\. 後日検証ポイント

- GOLD：GCZ6が3830を超えるか。ドル高・金利高が続くか。
- USDJPY：158.3割れ、または介入による急変が発生するか。
- SPX：ESZ6が7500を超えて弱気構造を否定するか。
- NASDAQ：NQZ6が28300を超えるか。
- WTI：87超えと供給関連ニュースの発生。
- 各判断の5営業日後の時間決済R、最大MAE、TP1到達状況。
- 金曜エントリーと翌週月曜のギャップによる損益差。

## 9\. Obsidian保存用Observation Draft

```markdown
# TSO Observation 2026-11-20

Model: GPT-6
Market protagonist: GOLD
Regime: RISK_OFF / MIXED

## Hypothesis
FRBのタカ派姿勢と米金利上昇により、
GOLD・株価指数には下落圧力が残る。
USDJPYはドル高方向だが介入リスクがある。

## Decisions
A: 0
B: GOLD SELL, WTI SELL, USDJPY BUY,
   SPX SELL, NASDAQ SELL
NO_TRADE: BTC, ETH, DXY, US10Y, VIX

## Execution
通常リスク0.25%
日次最大0.50%
基本5営業日決済
金曜日の週末リスクを別途観察

## Verification gaps
前回signal_idの個別照合
厳密なATR10再計算
WTI限月確認
BTC ETF/CMEデータ
```

## 10\. TSO\_LOG

### CSV（固定28列・10資産）

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-11-20,20261120_GOLD_SELL_PULLBACK,GOLD,SELL,B,PULLBACK,3690,3740,3830,3510,3400,1.783,0.54,0.28,70,72,38,0.25,RISK_OFF,62,65,61,55,72,68,GCZ6_above_3830,GCZ6,partially_verified
2026-11-20,20261120_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,44,39,77,,RISK_OFF,43,48,42,40,48,38,BTC_below_62600,BTCUSD_spot_ETF_CME,partially_verified
2026-11-20,20261120_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,43,37,76,,RISK_OFF,44,45,42,39,47,40,ETH_below_1750,ETHUSD_spot,partially_verified
2026-11-20,20261120_WTI_SELL_PULLBACK,WTI,SELL,B,PULLBACK,82,84,87,76,73,1.75,0.51,0.19,62,60,55,0.25,EVENT,53,51,47,46,60,54,WTI_above_87,WTI_futures_contract,partially_verified
2026-11-20,20261120_USDJPY_BUY_PULLBACK,USDJPY,BUY,B,PULLBACK,159.3,159.7,158.3,161.5,162.2,1.667,0.55,0.32,70,68,49,0.25,EVENT,61,63,55,49,71,65,USDJPY_below_158.3_or_intervention,USDJPY,partially_verified
2026-11-20,20261120_SPX_SELL_PULLBACK,SPX,SELL,B,PULLBACK,7270,7330,7500,6990,6850,1.55,0.53,0.27,69,65,44,0.25,RISK_OFF,60,60,54,49,69,65,ES_above_7500,ESZ6,partially_verified
2026-11-20,20261120_NASDAQ_SELL_PULLBACK,NASDAQ,SELL,B,PULLBACK,27100,27400,28300,25600,24900,1.571,0.52,0.25,67,64,47,0.25,MIXED,59,60,52,48,68,61,NQ_above_28300,NQZ6,partially_verified
2026-11-20,20261120_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,51,48,65,,RISK_OFF,52,49,47,43,55,58,DXY_above_104.5,DXY_index,partially_verified
2026-11-20,20261120_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,50,43,72,,EVENT,48,45,42,41,52,55,US10Y_above_5.2,US10Y_yield,partially_verified
2026-11-20,20261120_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,47,40,78,,RISK_OFF,46,44,40,38,49,48,VIX_above_28,VIX_index,partially_verified
```

### JSON

列順は上記CSVと同じ。各配列が1資産の28フィールドに対応する。

```json
{
  "date": "2026-11-20",
  "model": "GPT-6",
  "market_protagonist": "GOLD",
  "columns": [
    "date","signal_id","asset","side","rank","type",
    "entry_low","entry_high","sl","tp1","tp2","rr",
    "win_prob","expected_r","tq_score","opp_score",
    "no_trade_score","risk_pct","regime","ems","ffs",
    "cds","ias","cbs","mes","invalidation",
    "verification_target","verified_status"
  ],
  "rows": [
    ["2026-11-20","20261120_GOLD_SELL_PULLBACK","GOLD","SELL","B","PULLBACK",3690,3740,3830,3510,3400,1.783,0.54,0.28,70,72,38,0.25,"RISK_OFF",62,65,61,55,72,68,"GCZ6_above_3830","GCZ6","partially_verified"],
    ["2026-11-20","20261120_BTC_NONE_NO_TRADE","BTC","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,44,39,77,null,"RISK_OFF",43,48,42,40,48,38,"BTC_below_62600","BTCUSD_spot_ETF_CME","partially_verified"],
    ["2026-11-20","20261120_ETH_NONE_NO_TRADE","ETH","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,43,37,76,null,"RISK_OFF",44,45,42,39,47,40,"ETH_below_1750","ETHUSD_spot","partially_verified"],
    ["2026-11-20","20261120_WTI_SELL_PULLBACK","WTI","SELL","B","PULLBACK",82,84,87,76,73,1.75,0.51,0.19,62,60,55,0.25,"EVENT",53,51,47,46,60,54,"WTI_above_87","WTI_futures_contract","partially_verified"],
    ["2026-11-20","20261120_USDJPY_BUY_PULLBACK","USDJPY","BUY","B","PULLBACK",159.3,159.7,158.3,161.5,162.2,1.667,0.55,0.32,70,68,49,0.25,"EVENT",61,63,55,49,71,65,"USDJPY_below_158.3_or_intervention","USDJPY","partially_verified"],
    ["2026-11-20","20261120_SPX_SELL_PULLBACK","SPX","SELL","B","PULLBACK",7270,7330,7500,6990,6850,1.55,0.53,0.27,69,65,44,0.25,"RISK_OFF",60,60,54,49,69,65,"ES_above_7500","ESZ6","partially_verified"],
    ["2026-11-20","20261120_NASDAQ_SELL_PULLBACK","NASDAQ","SELL","B","PULLBACK",27100,27400,28300,25600,24900,1.571,0.52,0.25,67,64,47,0.25,"MIXED",59,60,52,48,68,61,"NQ_above_28300","NQZ6","partially_verified"],
    ["2026-11-20","20261120_DXY_NONE_NO_TRADE","DXY","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,51,48,65,null,"RISK_OFF",52,49,47,43,55,58,"DXY_above_104.5","DXY_index","partially_verified"],
    ["2026-11-20","20261120_US10Y_NONE_NO_TRADE","US10Y","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,50,43,72,null,"EVENT",48,45,42,41,52,55,"US10Y_above_5.2","US10Y_yield","partially_verified"],
    ["2026-11-20","20261120_VIX_NONE_NO_TRADE","VIX","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,47,40,78,null,"RISK_OFF",46,44,40,38,49,48,"VIX_above_28","VIX_index","partially_verified"]
  ]
}
```

**記録結果：10資産10行、各28列、RR算術照合済み。** 全行partially\_verified。未完了項目は過去signal\_id照合、厳密なATR10検証、WTI限月確認であり、今回の判断と日次ログは継続して残した。
