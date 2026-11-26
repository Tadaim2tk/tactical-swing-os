<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-11-27 07:00 JST -->
<!-- transport: Complete original read_thread message 44012a2b-b56c-43dc-a746-756c437aa56d; raw markdown -->
<!-- archived_at: 2026-11-26T23:05:01Z / chars: 12233 / 値は無修正 -->

# Tactical Swing OS 日次判断｜2026年11月27日（金）

実行モデル：GPT-6.2
判断基準時刻：2026-11-27 06:58 JST
運用モード：通常寄り防御
市場レジーム：EVENT
本日の市場の主役：WTI
GOLD参照限月：COMEX 2026年12月限（GCZ26）

## 1\. 本日の結論

米国の感謝祭からブラックフライデーにかけての特殊な取引環境。原油の供給不安、米国の追加関税、インフレの高止まり、株式市場の自律反発が同時に発生している。

方向性としては、金の反発継続とドル円の短期的な調整を観察したい。株式市場については、反発と下落トレンドからの脱却を区別する必要がある。

| 分類 | 資産 | 方向 |
|--------|--------|--------|
| A級 | 該当なし | — |
| B級 | GOLD | BUY |
| B級 | ETH | BUY |
| B級 | USDJPY | SELL |
| NO\_TRADE | BTC | — |
| NO\_TRADE | WTI | — |
| NO\_TRADE | SPX | — |
| NO\_TRADE | NASDAQ | — |
| NO\_TRADE | DXY | — |
| NO\_TRADE | US10Y | — |
| NO\_TRADE | VIX | — |

- A級：0件
- B級：3件
- B+観察候補：0件
- NO\_TRADE：7件
- 最大日次リスク：0.50%
- B級1件あたりのリスク：0.25%

B級3件をすべて同時に採用すると日次リスク上限を超える。また、今回の3件はいずれもドル安・米金利低下の恩恵を受ける可能性があり、独立した取引として扱わない方がよい。

## 2\. 前回判断の簡易検証

前回までの方向あり判断について、今回参照可能な情報からは最新のsignal\_idおよびinvalidation水準を特定できなかった。

`invalidation_check:`

対象IDの取得未完了。検証件数がゼロという意味ではない。架空のIDや発動結果を記録せず、今回の検証工程の欠損として扱う。

本日分の10資産の記帳は継続する。

## 3\. 市場全体の前提

### マクロ経済・金融政策

米国のインフレ指標と経済成長率が強く、金融引き締めへの警戒が継続している。一方、利上げ期待が相当程度織り込まれているため、強い経済指標に対してもドルや長期金利が必ずしも上昇しない状態にある。

11月26日の市場報道では、以下の水準が確認できる。

- 米10年債利回り：約4.84%
- DXY：103.70
- USDJPY：約159.20
- BTC：60,000ドル台回復
- WTI：84～85ドル付近の参考価格
- VIX：30近辺またはそれ以上との報道

出典：urlReuters・11月26日https://www.reuters.com/world/africa/dollar-steady-sliding-yields-temper-safe-haven-bid-2026-11-26/、urlAmber Markets・11月26日https://lc.ambermarkets.com/daily-report/nov-26th-2026/

### 株式市場

米国株式市場は11月26日が休場、27日が短縮取引となる。

11月25日の米国株式市場では、NASDAQ総合指数が約0.6%下落、S&amp;P500現物指数が約0.3%下落した。一方、26日の米株先物には反発が報じられている。

ただし、月間の下落幅はNASDAQ総合で約9%、S&amp;P500で約6.5%と大きい。現在の反発だけでは中期的な下落構造を否定できない。

出典：urlInvestors Business Dailyhttps://www.investors.com/news/stock-market-hours-thanksgiving-black-friday-sp-500-nasdaq-dow-jones-nvidia/、urlMarketWatchhttps://www.marketwatch.com/story/futures-point-to-black-friday-gains-for-wall-street-as-global-markets-welcome-u-s-resilience-ad6bcef2

### 本日の市場構造

| 要因 | 評価 |
|--------|--------|
| 米金融政策 | 引き締め警戒 |
| ドル | 上昇一服 |
| 米長期金利 | 短期低下 |
| 株式 | 下落基調からの反発 |
| 原油 | 地政学的供給リスク |
| 暗号資産 | 売られ過ぎからの反発 |
| 流動性 | 低い |
| 総合 | EVENT |

本日は、材料そのものよりも、材料に対する市場の反応が変化している点を重視する。

## 4\. 10資産別判断

### 価格取得状況

| 資産 | 参考価格 | データの状態 |
|--------|--------|--------|
| GOLD | 3,578～3,602 | 現物・限月不明価格による近似 |
| BTC | 60,224～60,932 | BTC/USD報道値 |
| ETH | 1,685～1,688 | ETH/USD報道値 |
| WTI | 83.84～85.25 | 限月未確認の参考値 |
| USDJPY | 159.17～159.20 | 為替報道値 |
| SPX | 未確定 | ES先物絶対値未取得 |
| NASDAQ | 未確定 | NQ先物絶対値未取得 |
| DXY | 103.70 | Reuters報道値 |
| US10Y | 4.84% | 市場報道値 |
| VIX | 30近辺 | 報道間に差異あり |

価格は主に11月26日の報道値。同期したリアルタイム価格ではない。

GOLDはGCZ26の直接価格を確認できていないため、後述の監視水準は現物近似に基づく暫定値とする。SPXとNASDAQについては現物指数やCFD価格を先物価格として代用しない。

ATR10については、直近11本の日足OHLCを取得できなかったため、B級のSL幅は推定値幅に基づく暫定設定である。実測ATR10以上であることは未検証。

### GOLD — B級 BUY

金は直近安値の3,426ドル付近から大きく反発。ドル上昇の一服、長期金利の低下、地政学的リスクが反発を支える。

ただし、短期間で150ドル程度反発しており、戻り売りも想定する必要がある。

| 項目 | 評価 |
|--------|--------|
| Entry | 3540–3570 |
| Entry中点 | 3555 |
| SL | 3445 |
| TP1 | 3720 |
| TP2 | 3800 |
| SL距離 | 110 |
| RR | 1.50 |
| 推定ATR10 | 90～110 |
| 主観勝率 | 54% |
| expected\_r | \+0.30R |
| 想定MAE | 0.43R |
| CBS | 72 |
| EMS | 59 |
| リスク | 0.25% |

無効化条件：3445割れ。

GCZ26の実価格およびATR10の照合が必要。A級条件は未達。

### BTC — NO\_TRADE

60,000ドル台を回復しているが、薄商いの中での反発であり、現時点では底打ちと判断するには早い。

ETFフロー、CME建玉、basisを確認できていない。現物価格の反発だけでは持続的な買い需要の裏付けが弱い。

- MES：44
- CBS：55
- EMS：47
- NO\_TRADEスコア：76

出典：urlCointelegraph・11月26日https://www.tradingview.com/news/cointelegraph%3A376c88ef3094b%3A0-bitcoin-price-eyes-61k-as-talos-warns-of-thin-thanksgiving-liquidity/

### ETH — B級 BUY

1,685ドル前後。暗号資産市場全体の反発に伴う短期的な平均回帰を想定する。

独自の資金流入根拠は弱く、BTCの反発が崩れれば連動して下落する可能性が高い。

| 項目 | 評価 |
|--------|--------|
| Entry | 1630–1670 |
| Entry中点 | 1650 |
| SL | 1500 |
| TP1 | 1845 |
| TP2 | 1950 |
| SL距離 | 150 |
| RR | 1.30 |
| 推定ATR10 | 100～150 |
| 主観勝率 | 51% |
| expected\_r | \+0.12R |
| 想定MAE | 0.48R |
| CBS | 62 |
| EMS | 54 |
| リスク | 0.25% |

無効化条件：1500割れ。

価格参照：urlFXNX・11月26日https://fxnx.com/en/analysis/archive/2026-11-26

### WTI — NO\_TRADE

中東の供給不安によって価格が上昇している。現在の市場で最も重要な外生的変動要因と判断する。

方向としては供給不安が上昇圧力となるが、地政学的プレミアムが短期間で剥落する可能性もある。供給ショック直後のmomentum追随を避ける既存規則に従う。

- CBS：68
- EMS：38
- NO\_TRADEスコア：88

供給不安が継続するか、価格が通常の需給評価に戻るかを確認する。

### USDJPY — B級 SELL

159.20円付近。米長期金利の低下とドル上昇の一服から、短期的な円高方向への調整を想定する。

一方、米国の金融引き締め期待がドルを支えており、中期的なドル高構造の反転までは想定しない。

| 項目 | 評価 |
|--------|--------|
| Entry | 159.10–159.50 |
| Entry中点 | 159.30 |
| SL | 160.80 |
| TP1 | 157.05 |
| TP2 | 155.80 |
| SL距離 | 1.50 |
| RR | 1.50 |
| 推定ATR10 | 1.10～1.50 |
| 主観勝率 | 55% |
| expected\_r | \+0.32R |
| 想定MAE | 0.39R |
| CBS | 73 |
| EMS | 63 |
| リスク | 0.25% |

無効化条件：160.80超え。

判断日の終値までにEntry帯へ到達しなかった場合の終値参加規則を維持する。expected\_rに未到達による不参加確率は織り込んでいない。

### SPX — NO\_TRADE

ES先物には反発が報じられているが、絶対価格と日足構造を確認できていない。

株式市場全体の中期下落と短期反発が競合しており、現時点で方向優位性を確定しない。

- CBS：53
- EMS：45
- NO\_TRADEスコア：73

### NASDAQ — NO\_TRADE

AI関連株の調整、関税リスク、金利上昇への警戒が続く一方、急落後の買い戻しも強い。

NQ先物の基準価格を取得できておらず、下落継続と自律反発のどちらが優勢かを判断できない。

成行参加規則や追随回避を理由とした見送りではない。

- CBS：55
- EMS：44
- NO\_TRADEスコア：75

### DXY — NO\_TRADE

103.70付近。ドル高の中期構造と短期的な上昇一服が競合している。

USDJPYの調整仮説はあるが、ドル指数全体については明確な方向優位性を認めない。

- CBS：57
- EMS：51
- NO\_TRADEスコア：67

### US10Y — NO\_TRADE

4.84%付近。インフレと金融引き締め期待は利回り上昇要因だが、株式市場の不安定化は債券需要を支える。

感謝祭休場のため、新しい価格形成が限定的。

- CBS：54
- EMS：46
- NO\_TRADEスコア：74

### VIX — NO\_TRADE

30近辺の高ボラティリティ環境。株式の反発が続けば低下する可能性がある一方、関税や原油供給不安による再上昇も考えられる。

VIX現物指数とVIX先物は区別する。報道間の価格差異も解消できていない。

- CBS：49
- EMS：40
- NO\_TRADEスコア：83

## 5\. A級候補

該当なし。

今回の方向あり3件はいずれもCBS、EMS、expected\_r、MAEの複数条件でA級基準を満たさない。

ATR10の実測値が未確認である点も残る。

## 6\. B級監視候補

| 優先順位 | 資産 | 方向 | 勝率 | 期待R | RR |
|--------|--------|--------|--------|--------|--------|
| 1 | USDJPY | SELL | 55% | \+0.32 | 1.50 |
| 2 | GOLD | BUY | 54% | \+0.30 | 1.50 |
| 3 | ETH | BUY | 51% | \+0.12 | 1.30 |

B+観察候補はなし。

USDJPYは数値上B+条件を満たすが、ATR10未確認および祝日取引環境における評価の不確実性が残るため、**暫定B+観察候補**として区別する。CSV上はrank=Bを維持する。

## 7\. 触らない資産

| 資産 | 主な理由 |
|--------|--------|
| BTC | ETF・CME根拠不足、MES不足 |
| WTI | 供給ショック直後 |
| SPX | 反発と下落構造の競合 |
| NASDAQ | 方向未確定、NQ価格未取得 |
| DXY | 短期・中期方向の不一致 |
| US10Y | 金利上昇・低下要因の競合 |
| VIX | 高ボラティリティと価格不確実性 |

## 8\. 後日検証ポイント

今回の重要な検証テーマは、米国の金融引き締め期待が強い状態でも、ドルと長期金利の調整が継続するかどうかである。

- GOLD：反発が継続するか、下落トレンド中の戻りに終わるか。
- ETH：暗号資産全体の反発が5営業日持続するか。
- USDJPY：159円台からの調整が進むか。
- WTI：供給不安による上昇プレミアムが維持されるか。
- NASDAQ：祝日明けの反発が通常取引再開後も続くか。
- 11月30日の通常取引再開によって方向性が変化するか。
- GCZ26および各方向あり資産の実測ATR10を取得し、SL幅の適合性を検証する。

5営業日の時間決済を基本とし、TP1・TP2は参考目標とする。

## 9\. Obsidian保存用Observation Draft

```yaml
date: 2026-11-27
model: GPT-6.2
system: Tactical Swing OS
mode: normal_defensive
regime: EVENT
market_leader: WTI
gold_contract: GCZ26
gold_contract_price_verified: false
signal_count: 3
rank_a_count: 0
rank_b_count: 3
rank_no_trade_count: 7
daily_risk_limit_pct: 0.50
attack_mode: false
atr10_method: simple_mean_true_range
atr10_verified: false
atr10_floor_compliance: pending
invalidation_check_complete: false
data_status: partially_verified
```

### Observation

米金融引き締め期待が強いにもかかわらず、ドルと長期金利が短期的に低下している。金融政策の織り込み進展による価格反応の変化を観察する。

原油は供給不安による独立した上昇要因を持つ。株式と暗号資産の反発については、感謝祭前後の流動性低下による影響を分離する必要がある。

方向あり判断は3件。SLは推定ATR10に基づく暫定設定。実測値未確認を後日検証時に識別する。

## 10\. TSO\_LOG

### CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-11-27,20261127_GOLD_BUY_PULLBACK,GOLD,BUY,B,PULLBACK,3540,3570,3445,3720,3800,1.50,0.54,0.30,65,69,45,0.25,EVENT,59,64,62,70,72,65,below_3445,GCZ26_ATR10_5D,partially_verified
2026-11-27,20261127_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,48,49,76,,EVENT,47,35,52,48,55,44,ETF_CME_unverified,BTCUSD_5D,partially_verified
2026-11-27,20261127_ETH_BUY_REVERSAL,ETH,BUY,B,REVERSAL,1630,1670,1500,1845,1950,1.30,0.51,0.12,56,59,53,0.25,EVENT,54,43,58,55,62,51,below_1500,ETHUSD_ATR10_5D,partially_verified
2026-11-27,20261127_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,62,48,88,,EVENT,38,69,46,79,68,72,supply_shock_momentum,WTI_front_month_5D,partially_verified
2026-11-27,20261127_USDJPY_SELL_REVERSAL,USDJPY,SELL,B,REVERSAL,159.10,159.50,160.80,157.05,155.80,1.50,0.55,0.32,67,71,43,0.25,EVENT,63,62,65,72,73,67,above_160.80,USDJPY_ATR10_5D,partially_verified
2026-11-27,20261127_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,48,44,73,,EVENT,45,47,43,52,53,49,ES_price_unverified,ESZ26_5D,partially_verified
2026-11-27,20261127_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,47,46,75,,EVENT,44,46,42,55,55,48,NQ_price_unverified,NQZ26_5D,partially_verified
2026-11-27,20261127_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,54,48,67,,EVENT,51,59,49,57,57,61,conflicting_direction,DXY_5D,partially_verified
2026-11-27,20261127_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,49,43,74,,EVENT,46,55,45,59,54,58,holiday_rate_discovery,US10Y_yield_5D,partially_verified
2026-11-27,20261127_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,43,38,83,,EVENT,40,42,39,61,49,53,index_price_discrepancy,VIX_index_5D,partially_verified
```

### JSON

28列の固定スキーマと10資産の配列形式。CSVの空欄はnullとして表現する。

```json
{
  "columns": [
    "date",
    "signal_id",
    "asset",
    "side",
    "rank",
    "type",
    "entry_low",
    "entry_high",
    "sl",
    "tp1",
    "tp2",
    "rr",
    "win_prob",
    "expected_r",
    "tq_score",
    "opp_score",
    "no_trade_score",
    "risk_pct",
    "regime",
    "ems",
    "ffs",
    "cds",
    "ias",
    "cbs",
    "mes",
    "invalidation",
    "verification_target",
    "verified_status"
  ],
  "rows": [
    ["2026-11-27","20261127_GOLD_BUY_PULLBACK","GOLD","BUY","B","PULLBACK",3540,3570,3445,3720,3800,1.50,0.54,0.30,65,69,45,0.25,"EVENT",59,64,62,70,72,65,"below_3445","GCZ26_ATR10_5D","partially_verified"],
    ["2026-11-27","20261127_BTC_NONE_NO_TRADE","BTC","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,48,49,76,null,"EVENT",47,35,52,48,55,44,"ETF_CME_unverified","BTCUSD_5D","partially_verified"],
    ["2026-11-27","20261127_ETH_BUY_REVERSAL","ETH","BUY","B","REVERSAL",1630,1670,1500,1845,1950,1.30,0.51,0.12,56,59,53,0.25,"EVENT",54,43,58,55,62,51,"below_1500","ETHUSD_ATR10_5D","partially_verified"],
    ["2026-11-27","20261127_WTI_NONE_NO_TRADE","WTI","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,62,48,88,null,"EVENT",38,69,46,79,68,72,"supply_shock_momentum","WTI_front_month_5D","partially_verified"],
    ["2026-11-27","20261127_USDJPY_SELL_REVERSAL","USDJPY","SELL","B","REVERSAL",159.10,159.50,160.80,157.05,155.80,1.50,0.55,0.32,67,71,43,0.25,"EVENT",63,62,65,72,73,67,"above_160.80","USDJPY_ATR10_5D","partially_verified"],
    ["2026-11-27","20261127_SPX_NONE_NO_TRADE","SPX","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,48,44,73,null,"EVENT",45,47,43,52,53,49,"ES_price_unverified","ESZ26_5D","partially_verified"],
    ["2026-11-27","20261127_NASDAQ_NONE_NO_TRADE","NASDAQ","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,47,46,75,null,"EVENT",44,46,42,55,55,48,"NQ_price_unverified","NQZ26_5D","partially_verified"],
    ["2026-11-27","20261127_DXY_NONE_NO_TRADE","DXY","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,54,48,67,null,"EVENT",51,59,49,57,57,61,"conflicting_direction","DXY_5D","partially_verified"],
    ["2026-11-27","20261127_US10Y_NONE_NO_TRADE","US10Y","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,49,43,74,null,"EVENT",46,55,45,59,54,58,"holiday_rate_discovery","US10Y_yield_5D","partially_verified"],
    ["2026-11-27","20261127_VIX_NONE_NO_TRADE","VIX","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,43,38,83,null,"EVENT",40,42,39,61,49,53,"index_price_discrepancy","VIX_index_5D","partially_verified"]
  ]
}
```

### 出力監査

| 検査項目 | 結果 |
|--------|--------|
| 固定10資産 | 10/10 |
| CSV列数 | 各28列 |
| CSVカンマ数 | 各27個 |
| JSON行数 | 10 |
| NO\_TRADE空欄処理 | 適合 |
| regime許容値 | 適合 |
| GOLD RR再計算 | 165/110 = 1.50 |
| ETH RR再計算 | 195/150 = 1.30 |
| USDJPY RR再計算 | 2.25/1.50 = 1.50 |
| ATR10実測照合 | 未完了 |
| 過去invalidation検証 | 未完了 |
| 外部保存 | 未実施 |
| チャット上の記帳 | 完了 |

**本日の最終評価：USDJPYの短期SELLを第一監視候補とする。GOLDの反発継続が第二候補。原油は市場の主役だが、供給ショック直後のため見送る。**

TSO\_LOG：10/10出力完了。
