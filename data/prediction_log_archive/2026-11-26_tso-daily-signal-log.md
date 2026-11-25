<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-11-26 07:00 JST -->
<!-- transport: Complete original read_thread message 7b82f5a2-7f3f-438b-8c35-1c58c13f78fc; raw markdown -->
<!-- archived_at: 2026-11-25T23:05:57Z / chars: 11785 / 値は無修正 -->

# Tactical Swing OS｜日次判断 2026-11-26（木）

実行モデル：GPT-6.2
判断基準：2026年11月26日 07:00 JST
運用モード：通常寄り防御
市場レジーム：RISK\_OFF
本日の市場の主役：NASDAQ

## 1\. 本日の結論

米国のAI・半導体関連株の売り圧力が継続しています。一方、11月25日の米国市場では急落後の買い戻しも報じられており、下落方向の確信とエントリーの優位性は区別する必要があります。

本日は米国の感謝祭に当たり、流動性低下と休場・短縮取引に注意が必要です。

| 資産 | 方向 | 判定 | 主観勝率 |
|--------|--------|--------|--------|
| GOLD | 売り | B | 57% |
| BTC | — | NO\_TRADE | — |
| ETH | — | NO\_TRADE | — |
| WTI | — | NO\_TRADE | — |
| USDJPY | 買い | B | 55% |
| SPX | — | NO\_TRADE | — |
| NASDAQ | — | NO\_TRADE | — |
| DXY | — | NO\_TRADE | — |
| US10Y | — | NO\_TRADE | — |
| VIX | — | NO\_TRADE | — |

A級：0件
B級：2件
B+観察候補：0件
NO\_TRADE：8件
最大日次リスク：0.50%

今回はGOLDとUSDJPYについて暫定監視水準を記帳します。NASDAQには弱気の市場認識がありますが、指定されたNQ先物の価格基準を取得できなかったため、価格付きシグナルは作成しません。

---

## 2\. 前回判断の簡易検証

11月25日および24日の判断履歴を参照しました。

| 資産 | 最新判断日 | 前回方向 | 無効化水準 | 検証結果 |
|--------|--------|--------|--------|--------|
| GOLD | 11/25 | SELL | 3750超 | unknown |
| ETH | 11/25 | SELL | 1900超 | unknown |
| WTI | 11/25 | SELL | 91超 | unknown |
| USDJPY | 11/25 | BUY | 155割れ | unknown |
| SPX | 11/25 | SELL | 7600超 | unknown |
| NASDAQ | 11/25 | SELL | 28400超 | unknown |
| DXY | 11/24 | BUY | 102.5割れ | unknown |
| US10Y | 11/24 | BUY | 4.65割れ | unknown |

`invalidation_check: 20261125_GOLD_SELL_PULLBACK=unknown, 20261125_ETH_SELL_PULLBACK=unknown, 20261125_WTI_SELL_PULLBACK=unknown, 20261125_USDJPY_BUY_PULLBACK=unknown, 20261125_SPX_SELL_PULLBACK=unknown, 20261125_NASDAQ_SELL_PULLBACK=unknown, 20261124_DXY_BUY_PULLBACK=unknown, 20261124_US10Y_BUY_PULLBACK=unknown`

判断後の全期間の高値・安値が取得できていないため、途中価格だけでnot\_firedとは認定しません。また、GOLD以外の過去signal\_idについては履歴から方向と日付を確認していますが、type部分は暫定復元です。

BTC・VIXについては検証窓内の最新方向あり判断の有無を確定できていません。今回のinvalidation検証は未完了です。

---

## 3\. 市場全体の前提

### 市場データ取得状況

今回、新規にWeb検索を実施しました。11月25日付の市場報道から価格と市場動向を取得しています。ただし、全資産の確定終値および日足OHLCの取得には至っていません。

| 資産 | 取得参考値 | データ時点・系列 |
|--------|--------|--------|
| GOLD | 3545.03 | 11/25・現物参考値 |
| BTC | 58653 | 11/25・BTC/USD |
| ETH | 未取得 | ETH/USD |
| WTI | 81.652 | 11/25・参考価格 |
| USDJPY | 159.265 | 11/25 |
| SPX | 未取得 | ES先物 |
| NASDAQ | 未取得 | NQ先物 |
| DXY | 104.10 | 11/23・参考値 |
| US10Y | 4.97% | 11/23・参考値 |
| VIX | 30超 | 11/25・取引時間中 |

GOLDの正式参照系列はCOMEX金先物2026年12月限（GCZ26）です。今回は同限月の価格を確認できず、現物価格を参考にした暫定評価です。

ES・NQについては現物株価指数での代用を行っていません。

### マクロ環境

11月25日付の報道では、以下の材料が確認されています。

- AI関連株の売却と半導体株の下落。
- 米国の追加関税を巡る報道。
- 米金融政策の引き締め観測。
- BTCの60000ドル割れ。
- VIXの取引時間中の30超え。
- 米国株の急落後の買い戻し。
- 感謝祭に伴う流動性低下。

参照資料：

- urlAdmirals：11月25日市場概況https://admiralmarkets.com/analytics/traders-blog/tech-sell-off-morning-wrap-25-november-2026
- urlAmber Markets：11月25日市場データhttps://ambermarkets.com/daily-report/nov-25th-2026/
- urlCryptoTicker：株価先物・BTC・VIX動向https://cryptoticker.io/en/crypto-news-nasdaq-futures-tariffs-vix-30/
- urlInvesting.com：米国市場ニュースhttps://www.investing.com/

今回の検索では10資産すべての価格が欠損しているわけではないため、DATA\_UNAVAILABLEは使用しません。

---

## 4\. 10資産別判断

### GOLD — B級 SELL

金は金融引き締め観測に圧迫されています。株式市場が不安定であるにもかかわらず、金が安全資産として十分に買われていないことは弱気材料です。

| 項目 | 評価 |
|--------|--------|
| 参考価格（現物） | 3545.03 |
| Entry | 3570–3610 |
| Entry中点 | 3590 |
| SL | 3750 |
| TP1 | 3350 |
| TP2 | 3200 |
| SL距離 | 160 |
| RR | 1.50 |
| 主観勝率 | 57% |
| expected\_r | \+0.35R |
| MAE想定 | 0.34R |
| CBS | 72 |
| EMS | 63 |
| MES | 69 |
| リスク | 0.25% |

ATR10実測値は未取得です。SL距離160ドルは値幅拡大を考慮した暫定設定であり、1×ATR10以上であることは未検証です。

監視水準はGCZ26の実価格確認を前提とする暫定値です。

無効化条件：GCZ26が3750を上回る。

### BTC — NO\_TRADE

60000ドル割れは弱気材料です。ただし、ETFフロー、CME建玉、basisを確認できていません。株式市場の急落後の買い戻しがBTCにも波及する可能性があります。

MESは46と評価します。BTC固有の運用規則に従い見送ります。

### ETH — NO\_TRADE

BTCと株式市場の不安定さから下方向の圧力を想定しますが、ETH/USDの基準価格が未取得です。価格構造を特定できないため、Entry・SLは作成しません。

### WTI — NO\_TRADE

参考価格は81.65ドル付近です。供給過剰観測と中東の供給リスクが対立しています。

直近安値からの反発が継続するのか、下降トレンド中の一時的な買い戻しなのかを判断する根拠が不足しています。

### USDJPY — B級 BUY

米国の金融引き締め観測はドル円の上昇要因です。一方、160円付近では日本当局の為替介入リスクを無視できません。

| 項目 | 評価 |
|--------|--------|
| 参考価格 | 159.265 |
| Entry | 158.40–159.00 |
| Entry中点 | 158.70 |
| SL | 155.00 |
| TP1 | 162.50 |
| TP2 | 164.00 |
| SL距離 | 3.70 |
| RR | 1.0270 |
| 主観勝率 | 55% |
| expected\_r | \+0.09R |
| MAE想定 | 0.38R |
| CBS | 67 |
| EMS | 61 |
| MES | 64 |
| リスク | 0.25% |

ATR10は未取得です。SL幅は暫定3.70円とし、狭い損切りを避けています。

RRが1.2未満であるためA級には該当しませんが、方向ありのB級として記帳します。

Entry未到達の場合の判断日終値参加規則を維持し、未到達による不参加確率はexpected\_rから差し引いていません。

無効化条件：155円割れ。

### SPX — NO\_TRADE

AI関連株の下落が指数全体に波及していますが、ディフェンシブ銘柄への資金移動も観測されています。

指定系列ESの価格とATR10が取得できていないため、価格付き判断を見送ります。

### NASDAQ — NO\_TRADE

本日の市場の主役です。

AI関連株のバリュエーション調整、半導体株の売却、追加関税懸念という複数の弱気材料があります。ただし急落後の買い戻しも大きく、短期的な反発リスクがあります。

NQ先物の基準価格が未取得です。NASDAQ総合指数やQQQを代用してシグナルを作成することはしません。

### DXY — NO\_TRADE

金融引き締め観測はドル高要因ですが、直近のドル上昇には一服感も報じられています。11月25日の確定価格が未取得で、方向の優位性を十分に評価できません。

### US10Y — NO\_TRADE

金融引き締め観測による利回り上昇圧力と、株安による債券買い・利回り低下圧力が競合しています。

直近の利回り推移を確認してから判断する必要があります。

### VIX — NO\_TRADE

取引時間中に30を超えたとの報道があります。株式市場の警戒度は高いものの、急落後の株価回復に伴ってVIXが急低下する可能性もあります。

終値未取得のため、方向付き判断は行いません。

---

## 5\. A級候補

該当なし。

GOLDはexpected\_rとMAE想定、USDJPYはRRとexpected\_rがA級条件を満たしていません。両資産ともATR10実測値が未取得です。

## 6\. B級監視候補

| 優先 | 資産 | 方向 | Entry | SL | TP1 | TP2 | RR |
|--------|--------|--------|--------|--------|--------|--------|--------|
| 1 | GOLD | SELL | 3570–3610 | 3750 | 3350 | 3200 | 1.50 |
| 2 | USDJPY | BUY | 158.40–159.00 | 155.00 | 162.50 | 164.00 | 1.03 |

B+観察候補：GOLDは数値条件上該当します（CBS72、EMS63、RR1.50、win\_prob0.57）。ただしGCZ26価格とATR10の確認が必要なため、暫定B+観察候補として扱います。

決済は5営業日の時間決済を基本とし、TP1・TP2は参考目標です。

## 7\. 触らない資産

BTC、ETH、WTI、SPX、NASDAQ、DXY、US10Y、VIX。

今回の8件の見送りには、価格構造に基づく見送りと、指定系列の価格取得不足による見送りが混在しています。後日のモデル性能評価では両者を区別する必要があります。

## 8\. 後日検証ポイント

| 検証対象 | 確認事項 |
|--------|--------|
| GOLD | 金融引き締め観測による下落継続 |
| USDJPY | 160円接近時の上値抵抗と介入リスク |
| NASDAQ | 急落後の買い戻しが反転につながるか |
| BTC | 60000ドル回復の有無 |
| VIX | 30超の高ボラティリティ状態の継続 |
| SL設計 | 暫定SL距離と実測ATR10の比較 |
| データ取得 | GCZ26・ES・NQの日足取得 |
| 時間決済 | 感謝祭を考慮した5営業日の計数 |

特に今回は、価格取得不足による見送りを、モデルが方向性を検知できなかった事例として集計しないことが重要です。

---

## 9\. Obsidian保存用Observation Draft

```yaml
date: 2026-11-26
model: GPT-6.2
system: Tactical Swing OS
mode: normal_defensive
regime: RISK_OFF
market_leader: NASDAQ
gold_contract: GCZ26
gold_contract_price_verified: false
assets_total: 10
rank_a: 0
rank_b: 2
rank_b_plus_provisional: 1
rank_no_trade: 8
daily_risk_limit_pct: 0.50
data_status: partially_verified
atr10_verified: false
invalidation_check_complete: false
time_exit: 5_business_days
holiday_risk: US_Thanksgiving
```

Observation\:

米国のAI関連株の調整が継続。急落後の買い戻しも発生しており、単純な下落追随には反転リスクがある。GOLDの弱さとUSDJPYの上昇圧力をB級として記録。指定先物系列の取得不足により株価指数の価格付き判断は未成立。

ロット制約によるSL縮小なし。ATR10未実測のためSLは暫定。BTC・NASDAQ・USDJPYの終値参加規則は変更なし。

---

## 10\. TSO\_LOG

### CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-11-26,20261126_GOLD_SELL_PULLBACK,GOLD,SELL,B,PULLBACK,3570,3610,3750,3350,3200,1.50,0.57,0.35,70,71,39,0.25,RISK_OFF,63,66,71,58,72,69,above_3750_holiday_risk,GCZ26_ATR10_5day,partially_verified
2026-11-26,20261126_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,49,43,79,,RISK_OFF,46,38,58,42,52,46,ETF_CME_basis_unverified,BTCUSD_5day,partially_verified
2026-11-26,20261126_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,40,37,84,,RISK_OFF,43,35,49,40,45,43,reference_price_missing,ETHUSD_5day,unverified
2026-11-26,20261126_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,48,42,77,,MIXED,48,45,50,39,49,46,supply_risk_conflict,WTI_futures_5day,partially_verified
2026-11-26,20261126_USDJPY_BUY_PULLBACK,USDJPY,BUY,B,PULLBACK,158.40,159.00,155.00,162.50,164.00,1.0270,0.55,0.09,66,62,45,0.25,MIXED,61,59,67,49,67,64,below_155_intervention_risk,USDJPY_ATR10_5day,partially_verified
2026-11-26,20261126_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,48,46,80,,RISK_OFF,52,45,57,43,54,53,ES_reference_price_missing,ESZ26_5day,unverified
2026-11-26,20261126_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,57,59,75,,RISK_OFF,59,51,64,46,62,60,NQ_reference_price_missing,NQZ26_5day,partially_verified
2026-11-26,20261126_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,48,42,74,,MIXED,49,48,51,45,51,50,latest_close_missing,DXY_index_5day,partially_verified
2026-11-26,20261126_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,44,40,76,,MIXED,46,45,48,43,47,48,latest_yield_missing,US10Y_yield_5day,partially_verified
2026-11-26,20261126_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,45,43,81,,RISK_OFF,47,43,54,39,49,51,closing_value_missing,VIX_index_5day,partially_verified
```

### JSON

```json
{
  "date": "2026-11-26",
  "model": "GPT-6.2",
  "regime": "RISK_OFF",
  "market_leader": "NASDAQ",
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
  "TSO_LOG": [
    ["2026-11-26","20261126_GOLD_SELL_PULLBACK","GOLD","SELL","B","PULLBACK",3570,3610,3750,3350,3200,1.50,0.57,0.35,70,71,39,0.25,"RISK_OFF",63,66,71,58,72,69,"above_3750_holiday_risk","GCZ26_ATR10_5day","partially_verified"],
    ["2026-11-26","20261126_BTC_NONE_NO_TRADE","BTC","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,49,43,79,null,"RISK_OFF",46,38,58,42,52,46,"ETF_CME_basis_unverified","BTCUSD_5day","partially_verified"],
    ["2026-11-26","20261126_ETH_NONE_NO_TRADE","ETH","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,40,37,84,null,"RISK_OFF",43,35,49,40,45,43,"reference_price_missing","ETHUSD_5day","unverified"],
    ["2026-11-26","20261126_WTI_NONE_NO_TRADE","WTI","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,48,42,77,null,"MIXED",48,45,50,39,49,46,"supply_risk_conflict","WTI_futures_5day","partially_verified"],
    ["2026-11-26","20261126_USDJPY_BUY_PULLBACK","USDJPY","BUY","B","PULLBACK",158.40,159.00,155.00,162.50,164.00,1.0270,0.55,0.09,66,62,45,0.25,"MIXED",61,59,67,49,67,64,"below_155_intervention_risk","USDJPY_ATR10_5day","partially_verified"],
    ["2026-11-26","20261126_SPX_NONE_NO_TRADE","SPX","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,48,46,80,null,"RISK_OFF",52,45,57,43,54,53,"ES_reference_price_missing","ESZ26_5day","unverified"],
    ["2026-11-26","20261126_NASDAQ_NONE_NO_TRADE","NASDAQ","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,57,59,75,null,"RISK_OFF",59,51,64,46,62,60,"NQ_reference_price_missing","NQZ26_5day","partially_verified"],
    ["2026-11-26","20261126_DXY_NONE_NO_TRADE","DXY","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,48,42,74,null,"MIXED",49,48,51,45,51,50,"latest_close_missing","DXY_index_5day","partially_verified"],
    ["2026-11-26","20261126_US10Y_NONE_NO_TRADE","US10Y","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,44,40,76,null,"MIXED",46,45,48,43,47,48,"latest_yield_missing","US10Y_yield_5day","partially_verified"],
    ["2026-11-26","20261126_VIX_NONE_NO_TRADE","VIX","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,45,43,81,null,"RISK_OFF",47,43,54,39,49,51,"closing_value_missing","VIX_index_5day","partially_verified"]
  ]
}
```

### 出力監査

| 監査項目 | 結果 |
|--------|--------|
| 10資産固定出力 | PASS |
| 28列構成 | PASS（構造上の確認） |
| B級候補の記帳 | PASS |
| RR再計算 | PASS |
| regime許容語 | PASS |
| ロット制約による判断変更なし | PASS |
| 参照系列の無断置換なし | PASS |
| ATR10実測確認 | INCOMPLETE |
| 過去invalidation検証 | INCOMPLETE |
| 新規Web検索 | PASS |
| 外部台帳保存 | 未実施 |
| チャット上の記録 | COMPLETE |

本日の10資産分の記録は継続しました。市場データ取得と過去判断の検証には未完了項目が残っていますが、運用停止や判定規則の変更は行いません。
