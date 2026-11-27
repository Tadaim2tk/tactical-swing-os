<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-11-28 07:00 JST -->
<!-- transport: Complete original read_thread message 1b112b94-a862-4c54-a5fa-b0e8bacf0cd9; raw markdown -->
<!-- archived_at: 2026-11-27T23:02:20Z / chars: 8176 / 値は無修正 -->

# Tactical Swing OS — 2026-11-28（土）

実行モデル：GPT-6.2

## 1\. 本日の結論

**判定：データ取得未完了・10資産の日次記帳を継続**

本日は土曜日。米国市場の11月27日取引分と、週末も取引が継続する暗号資産を区別して評価する必要がある。

今回の実行では外部市場データおよびATR10参照表を取得できていない。実際の価格を確認していない状態で、架空の基準価格や方向性を台帳に混入させることは避ける。

| 項目 | 判定 |
|--------|--------|
| 運用モード | 通常寄り防御 |
| 市場レジーム | UNKNOWN |
| A級 | 0件 |
| B級 | 0件 |
| NO\_TRADE | 10件 |
| 最大日次リスク | 0.50% |
| 新規配分リスク | 0.00% |
| データ取得状態 | DATA\_UNAVAILABLE |
| 日次記帳 | 10資産継続 |

本日の市場の主役：UNKNOWN

`atr_table: unavailable`

今回の見送りは、市場に収益機会が存在しないという判断ではなく、価格情報を取得できていないことによる判断である。

## 2\. 前回判断の簡易検証

前日までの方向あり判断について、最新のsignal\_id、invalidation水準、判断後の高値・安値を確認できていない。

`invalidation_check:`

対象ID未取得のため個別判定未実施。検証対象が存在しないという意味ではない。既存判断の検証期間を終了させず、次回取得時の照合対象として維持する必要がある。

## 3\. 市場全体の前提

| 観察項目 | 状態 |
|--------|--------|
| 米国株式先物 | 11月27日終値未確認 |
| 米10年債利回り | 未確認 |
| ドル指数 | 未確認 |
| 暗号資産現物 | 最新価格未確認 |
| BTC ETFフロー | 未確認 |
| CME建玉・basis | 未確認 |
| 原油需給ニュース | 未確認 |
| ATR10参照表 | 未取得 |

11月26日は米国の感謝祭、27日は短縮取引の影響を考慮すべき日である。通常営業日と比較して、流動性や価格形成の違いが生じる可能性がある。

ただし、実際に流動性が低下したか、どの資産が主導したかについては未確認。

参照予定データ：

- urlATR10参照表https://raw.githubusercontent.com/Tadaim2tk/tactical-swing-os/main/data/atr10_reference.csv
- urlCME Grouphttps://www.cmegroup.com/
- urlCboe VIXhttps://www.cboe.com/tradable_products/vix/
- urlFRED 米10年債利回りhttps://fred.stlouisfed.org/series/DGS10
- urlCoinbasehttps://www.coinbase.com/

上記は参照先であり、今回取得済みのデータを示すものではない。

## 4\. 10資産別判断

| 資産 | 参照系列 | 基準価格 | 判断 | CBS | EMS |
|--------|--------|--------|--------|--------|--------|
| GOLD | GCZ26・12月限 | 未取得 | NO\_TRADE | 0 | 0 |
| BTC | BTC/USD現物 | 未取得 | NO\_TRADE | 0 | 0 |
| ETH | ETH/USD現物 | 未取得 | NO\_TRADE | 0 | 0 |
| WTI | WTI先物 | 未取得 | NO\_TRADE | 0 | 0 |
| USDJPY | ドル円 | 未取得 | NO\_TRADE | 0 | 0 |
| SPX | ES先物 | 未取得 | NO\_TRADE | 0 | 0 |
| NASDAQ | NQ先物 | 未取得 | NO\_TRADE | 0 | 0 |
| DXY | ドル指数 | 未取得 | NO\_TRADE | 0 | 0 |
| US10Y | 米10年債利回り | 未取得 | NO\_TRADE | 0 | 0 |
| VIX | VIX指数 | 未取得 | NO\_TRADE | 0 | 0 |

今回のスコア0は市場の弱さを意味しない。評価根拠を取得できていないことを表す欠損時の代替記帳値であり、通常のスコア較正からは除外すべきである。

### 資産別の確認事項

| 資産 | 次回評価で確認する事項 |
|--------|--------|
| GOLD | 12月限の価格構造、実質金利との整合 |
| BTC | 週末の方向性、ETFフロー、先物basis |
| ETH | BTCに対する相対強度 |
| WTI | 供給要因と需要要因の分離 |
| USDJPY | 日米金利差、介入警戒、価格構造 |
| SPX | ES先物の高値・安値更新 |
| NASDAQ | NQ先物のトレンド継続性 |
| DXY | ドルの方向性と他資産への波及 |
| US10Y | 金利変動と株式市場の反応 |
| VIX | ボラティリティ拡大・縮小の確認 |

## 5\. A級候補

該当なし。

CBS、EMS、expected\_r、MAE、RRおよびATR10条件を評価できていない。条件不合格ではなく、判定材料不足である。

## 6\. B級監視候補

該当なし。

B+観察候補も0件。

価格基準を取得できていないため、検証可能なEntry帯とSLを設定できない。方向あり判断を捏造しない。

## 7\. 触らない資産

全10資産。

なお、今回の見送りにロット制約、許容損失額、過去の連敗、直前判断のSL到達は使用していない。

NASDAQ・BTC・USDJPYの成行参加規則も変更しない。

## 8\. 後日検証ポイント

今回の実行は、戦略の方向性判断とは分離してデータ取得障害として評価する必要がある。

| 検証項目 | 状態 |
|--------|--------|
| 10資産の記帳継続 | 完了 |
| 最新市場データ取得 | 未完了 |
| ATR10参照表取得 | 未完了 |
| 過去判断の個別照合 | 未完了 |
| 方向性判断の較正 | 対象外 |
| RR算術検証 | 対象行なし |
| 28列構造 | 維持 |

11月27日改定のATR10参照表利用規則は維持する。今回取得できなかったことを理由に、次回以降の取得試行を省略しない。

## 9\. Obsidian保存用 Observation Draft

```markdown
---
date: 2026-11-28
system: Tactical Swing OS
model: GPT-6.2
mode: normal_defensive
regime: UNKNOWN
market_leader: UNKNOWN
data_status: DATA_UNAVAILABLE
atr_table: unavailable
a_count: 0
b_count: 0
no_trade_count: 10
daily_risk_pct: 0.00
log_rows: 10
---

# Daily Observation

## Market

米国感謝祭翌日の取引終了後。
週末の暗号資産と休場資産を区別する。

## Signal

基準価格未取得。
方向あり判断なし。
全10資産のNO_TRADE行を維持。

## ATR10

参照表未取得。
11月27日改定規則は維持。

## Invalidation

最新signal_idおよび価格経路未取得。
個別検証未完了。
既存判断を終了扱いにしない。

## Research Notes

今回のNO_TRADEは市場構造による
見送りとは区別する。

欠損時の代替スコアは通常の
スコア較正から除外する。

次回は新規に価格とATR10表を取得する。
運用規則の変更なし。
```

## 10\. TSO\_LOG

### CSV（固定28列・10資産）

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-11-28,20261128_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,0,0,100,,UNKNOWN,0,0,0,0,0,0,price_unavailable,GCZ26,unverified
2026-11-28,20261128_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,0,0,100,,UNKNOWN,0,0,0,0,0,0,price_unavailable,BTCUSD_spot,unverified
2026-11-28,20261128_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,0,0,100,,UNKNOWN,0,0,0,0,0,0,price_unavailable,ETHUSD_spot,unverified
2026-11-28,20261128_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,0,0,100,,UNKNOWN,0,0,0,0,0,0,price_unavailable,CL_futures,unverified
2026-11-28,20261128_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,0,0,100,,UNKNOWN,0,0,0,0,0,0,price_unavailable,USDJPY_spot,unverified
2026-11-28,20261128_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,0,0,100,,UNKNOWN,0,0,0,0,0,0,price_unavailable,ES_futures,unverified
2026-11-28,20261128_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,0,0,100,,UNKNOWN,0,0,0,0,0,0,price_unavailable,NQ_futures,unverified
2026-11-28,20261128_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,0,0,100,,UNKNOWN,0,0,0,0,0,0,price_unavailable,DXY_index,unverified
2026-11-28,20261128_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,0,0,100,,UNKNOWN,0,0,0,0,0,0,price_unavailable,US10Y_yield_pct,unverified
2026-11-28,20261128_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,0,0,100,,UNKNOWN,0,0,0,0,0,0,price_unavailable,VIX_index,unverified
```

### JSON

```json
{
  "date": "2026-11-28",
  "model": "GPT-6.2",
  "data_status": "DATA_UNAVAILABLE",
  "regime": "UNKNOWN",
  "market_leader": "UNKNOWN",
  "atr_table": "unavailable",
  "a_count": 0,
  "b_count": 0,
  "no_trade_count": 10,
  "daily_risk_pct": 0.0,
  "score_calibration_eligible": false,
  "invalidation_check_complete": false,
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
    ["2026-11-28","20261128_GOLD_NONE_NO_TRADE","GOLD","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,0,0,100,null,"UNKNOWN",0,0,0,0,0,0,"price_unavailable","GCZ26","unverified"],
    ["2026-11-28","20261128_BTC_NONE_NO_TRADE","BTC","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,0,0,100,null,"UNKNOWN",0,0,0,0,0,0,"price_unavailable","BTCUSD_spot","unverified"],
    ["2026-11-28","20261128_ETH_NONE_NO_TRADE","ETH","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,0,0,100,null,"UNKNOWN",0,0,0,0,0,0,"price_unavailable","ETHUSD_spot","unverified"],
    ["2026-11-28","20261128_WTI_NONE_NO_TRADE","WTI","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,0,0,100,null,"UNKNOWN",0,0,0,0,0,0,"price_unavailable","CL_futures","unverified"],
    ["2026-11-28","20261128_USDJPY_NONE_NO_TRADE","USDJPY","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,0,0,100,null,"UNKNOWN",0,0,0,0,0,0,"price_unavailable","USDJPY_spot","unverified"],
    ["2026-11-28","20261128_SPX_NONE_NO_TRADE","SPX","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,0,0,100,null,"UNKNOWN",0,0,0,0,0,0,"price_unavailable","ES_futures","unverified"],
    ["2026-11-28","20261128_NASDAQ_NONE_NO_TRADE","NASDAQ","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,0,0,100,null,"UNKNOWN",0,0,0,0,0,0,"price_unavailable","NQ_futures","unverified"],
    ["2026-11-28","20261128_DXY_NONE_NO_TRADE","DXY","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,0,0,100,null,"UNKNOWN",0,0,0,0,0,0,"price_unavailable","DXY_index","unverified"],
    ["2026-11-28","20261128_US10Y_NONE_NO_TRADE","US10Y","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,0,0,100,null,"UNKNOWN",0,0,0,0,0,0,"price_unavailable","US10Y_yield_pct","unverified"],
    ["2026-11-28","20261128_VIX_NONE_NO_TRADE","VIX","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,0,0,100,null,"UNKNOWN",0,0,0,0,0,0,"price_unavailable","VIX_index","unverified"]
  ]
}
```

**実行結果：10資産の記帳完了。市場分析・過去判断の検証は未完了。運用規則の変更なし。**
