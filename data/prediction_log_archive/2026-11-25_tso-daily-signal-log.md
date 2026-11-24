<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-11-25 07:00 JST -->
<!-- transport: Complete original read_thread message 1bb60a09-69aa-4a38-96bf-4384fd6f5a3f; raw markdown -->
<!-- archived_at: 2026-11-24T23:06:56Z / chars: 17427 / 値は無修正 -->

# Tactical Swing OS — 2026年11月25日（水）

実行モデル：GPT-6.2
判断基準時刻：2026-11-25 07:00 JST
運用モード：通常寄り防御
市場レジーム：RISK\_OFF
本日の市場の主役：USDJPY

## 1\. 本日の結論

**前日のリスクオン方向への反転判断を修正する。米国株、金、暗号資産の反落に加え、ドル円が独立した大幅上昇を示している。**

前日の株式市場の急反発は、持続的なトレンド転換ではなく、一時的な買い戻しだった可能性が高まった。

| 資産 | 方向 | 判定 | 主観勝率 | 期待R |
|--------|--------|--------|--------|--------|
| GOLD | SELL | B | 61% | \+0.39 |
| BTC | — | NO\_TRADE | — | — |
| ETH | SELL | B | 57% | \+0.24 |
| WTI | SELL | B | 58% | \+0.32 |
| USDJPY | BUY | B | 59% | \+0.35 |
| SPX | SELL | B | 55% | \+0.19 |
| NASDAQ | SELL | B | 60% | \+0.36 |
| DXY | — | NO\_TRADE | — | — |
| US10Y | — | NO\_TRADE | — | — |
| VIX | — | NO\_TRADE | — | — |

- A級：0件
- B級：6件
- B+観察候補：3件
- NO\_TRADE：4件
- 優先観察順位：GOLD、NASDAQ、USDJPY
- 日次最大リスク：0.50%

本日は方向性そのものよりも、急激な価格変動によってエントリー後の逆行幅が大きくなりやすい点が問題となる。

## 2\. 前回判断の簡易検証

11月24日の判断はA級0件、B級8件、NO\_TRADE2件だった。

| 資産 | 前回方向 | その後の市場方向 | 暫定評価 |
|--------|--------|--------|--------|
| GOLD | BUY | 下落 | 逆方向 |
| ETH | BUY | 下落 | 逆方向 |
| WTI | SELL | 反発 | 逆方向 |
| USDJPY | SELL | 大幅上昇 | 逆方向 |
| SPX | BUY | 下落 | 逆方向 |
| NASDAQ | BUY | 下落 | 逆方向 |
| DXY | BUY | 下落 | 逆方向 |
| US10Y | BUY | 小幅低下 | 逆方向 |

前回判断は、方向の初期評価としては不良だった。ただし、約定の有無、SL到達、5営業日後の決済結果とは区別する。

invalidation\_check: 20261124\_NASDAQ\_BUY\_REVERSAL=not\_fired, 20261124\_GOLD\_BUY\_REVERSAL=unknown

NASDAQの前回無効化水準24000に対し、取得したNQの観測安値は26142.25。ただし、判断日以降の全時間帯の安値を取得できていないため、not\_firedは取得範囲内の暫定判定である。

残り6資産については前回方向を復元できたが、正確なsignal\_idと無効化水準を完全には復元できなかった。架空のIDを生成せず、検証欠損として記録する。

## 3\. 市場全体の前提

### 3.1 市場価格

11月24日米国時間の市場データを新規取得した。終盤値、清算値、米国市場開始前の値が混在している。

| 資産 | 参照価格 | 変化率 | データ状態 |
|--------|--------|--------|--------|
| GOLD | 3559.90 | \-2.45% | 限月未照合 |
| BTC | 59876.97 | \-2.28% | 終盤値 |
| ETH | 1679.51 | \-1.82% | 終盤値 |
| WTI | 81.55 | \+1.72% | 終盤値 |
| USDJPY | 161.30 | \+3.14% | 終盤値 |
| SPX（ES） | 7159.50 | \-1.35% | 米国市場開始前 |
| NASDAQ（NQ） | 26222.25 | \-2.22% | 米国市場開始前 |
| DXY | 103.821 | \-0.48% | 終盤値 |
| US10Y | 4.906% | 約-1.2bp | 終盤値 |
| VIX | 30.10 | \+11.28% | 米国市場開始前 |

参照資料：

- urlWSJ：金先物の反落と金融政策見通しhttps://www.wsj.com/finance/commodities-futures/gold-rises-amid-risk-on-sentiment-across-markets-ae66946a
- url11月24日市場終盤データhttps://www.telegramsignalslive.com/news/market-wrap-24-november-2026-gold-usdjpy-nasdaq.html
- urlES・NQ先物およびVIX観測値https://thetradesignal.com/brief/2026-11-24/premarket
- urlBarron's：米国市場開始前の動向https://www.barrons.com/articles/s-p-500-futures-drop-in-premarket-trading-intercorp-finl-svcs-dick-s-sporting-goods-lead-b7229f67

GOLDの指定基準限月はCOMEX 2026年12月限（GCZ26）。取得した清算値の限月を独立確認できていないため、暫定参照価格として使用する。

### 3.2 市場構造

| 市場要因 | 評価 |
|--------|--------|
| 株式リスク選好 | 悪化 |
| 暗号資産リスク選好 | 悪化 |
| 金の安全資産機能 | 弱い |
| ドル全面高 | 不成立 |
| 円固有の売り圧力 | 強い |
| 原油の中期方向 | 下向き |
| ボラティリティ | 高い |
| 金融政策リスク | 高い |

特に重要なのは、DXYが下落する一方でUSDJPYが大幅上昇したことである。通常のドル高トレードとは分離して円固有の弱さを評価する必要がある。

### 3.3 イベントリスク

| 日付 | イベント | 影響 |
|--------|--------|--------|
| 11/25 米国時間 | 米PCE物価指標（報道ベース） | 高 |
| 11/25 米国時間 | 原油在庫関連 | 中〜高 |
| 11/26 | 米国感謝祭 | 流動性低下 |
| 11/27 | 米国市場短縮取引 | 流動性低下 |

今週は通常の5営業日保有と実際の取引可能時間が異なる。時間決済の営業日計算に注意する。

## 4\. 10資産別判断

### 4.1 GOLD — B / SELL

基準：COMEX 2026年12月限

参照価格：3559.90

金先物は直近5営業日のうち4営業日で下落したと報じられている。株式市場の不安定化にもかかわらず買われず、金融引き締め観測と資金流出の影響が強いと判断する。

| 項目 | 評価 |
|--------|--------|
| Entry | 3580–3620 |
| Entry中点 | 3600 |
| SL | 3750 |
| TP1 | 3360 |
| TP2 | 3240 |
| RR | 1.60 |
| 主観勝率 | 0.61 |
| expected\_r | \+0.39 |
| MAE想定 | 0.38R |
| CBS | 74 |
| EMS | 64 |

ATR10暫定推定：110–140。SL距離150。実測ATR10は未確認。

無効化：3750超え。

B+観察候補。PCE上振れは売り仮説を補強するが、3500近辺からの反発には注意する。

### 4.2 BTC — NO\_TRADE

参照価格：59876.97

直近20日安値として55130が報告されており、価格構造は弱い。しかし、ETF資金流出入、CME建玉、basisの最新情報を確認できていない。

MES：44。

下落方向のバイアスはあるが、BTC固有の運用条件を適用して見送る。

### 4.3 ETH — B / SELL

参照価格：1679.51

直近5日間の下落率は約4.4%。BTCの弱さに加え、暗号資産全体の資金流出リスクを考慮する。

| 項目 | 評価 |
|--------|--------|
| Entry | 1690–1730 |
| SL | 1900 |
| TP1 | 1440 |
| TP2 | 1300 |
| RR | 1.42 |
| 主観勝率 | 0.57 |
| expected\_r | \+0.24 |
| MAE想定 | 0.44R |
| CBS | 66 |
| EMS | 57 |

ATR10暫定推定：130–180。SL距離190。

無効化：1900超え。

### 4.4 WTI — B / SELL

参照価格：81.55

日中は反発したが、直近5日間の下落率は約5.2%。中期下落構造の中での反発と評価する。

| 項目 | 評価 |
|--------|--------|
| Entry | 83–85 |
| SL | 91 |
| TP1 | 73 |
| TP2 | 68 |
| RR | 1.57 |
| 主観勝率 | 0.58 |
| expected\_r | \+0.32 |
| MAE想定 | 0.41R |
| CBS | 69 |
| EMS | 59 |

ATR10暫定推定：4.5–6.5。SL距離7。

無効化：91超え。

供給ショックによる上昇リスクが残るため、反発を待つ戻り売り型とする。

### 4.5 USDJPY — B / BUY

参照価格：161.30

本日の最重要観察対象。DXY下落と同時に大幅上昇していることから、ドル全面高では説明できない円売りが発生した可能性がある。

| 項目 | 評価 |
|--------|--------|
| Entry | 159.50–160.50 |
| SL | 155.00 |
| TP1 | 167.50 |
| TP2 | 170.00 |
| RR | 1.50 |
| 主観勝率 | 0.59 |
| expected\_r | \+0.35 |
| MAE想定 | 0.46R |
| CBS | 73 |
| EMS | 62 |

ATR10暫定推定：2.8–4.5。SL距離5.00。

無効化：155.00割れ。

B+観察候補。167.50は5営業日以内の上振れ参考目標であり、直近高値163.965の突破が前提となる。

為替介入リスクが大きく、急変時にはSL価格での決済が保証されない。

### 4.6 SPX — B / SELL

参照系列：ES先物

参照価格：7159.50

前日の大幅反発から再び下落。株式市場の反転成立を支持する価格構造が弱まった。

| 項目 | 評価 |
|--------|--------|
| Entry | 7200–7300 |
| SL | 7600 |
| TP1 | 6800 |
| TP2 | 6550 |
| RR | 1.29 |
| 主観勝率 | 0.55 |
| expected\_r | \+0.19 |
| MAE想定 | 0.43R |
| CBS | 65 |
| EMS | 58 |

ATR10暫定推定：230–330。SL距離350。

無効化：7600超え。

### 4.7 NASDAQ — B / SELL

参照系列：NQ先物

参照価格：26222.25

ESに比べて下落率が大きく、ハイテク株への売り圧力が相対的に強い。前日の反転買い仮説を修正する。

| 項目 | 評価 |
|--------|--------|
| Entry | 26500–26900 |
| SL | 28400 |
| TP1 | 24000 |
| TP2 | 22500 |
| RR | 1.59 |
| 主観勝率 | 0.60 |
| expected\_r | \+0.36 |
| MAE想定 | 0.42R |
| CBS | 74 |
| EMS | 64 |

ATR10暫定推定：1100–1600。SL距離1700。

無効化：28400超え。

B+観察候補。判断日終値での参加規則を期待値評価に反映済み。Entry未到達による期待値の減額は行っていない。

### 4.8 DXY — NO\_TRADE

参照価格：103.821

日次では下落した一方、直近5日間では小幅上昇。USDJPYの上昇とも整合しないため、ドル全体の方向性は不明瞭と判断する。

### 4.9 US10Y — NO\_TRADE

参照利回り：4.906%

金融引き締め観測と株式市場のリスク回避による債券需要が競合している。PCE前に明確な方向を設定できるほどの優位性は認めない。

### 4.10 VIX — NO\_TRADE

参照価格：30.10

高ボラティリティ状態。株式市場の急反発と急落が交互に発生しており、VIX自体の持続的な方向判断は困難。

株式シグナルの補助変数として活用する。

## 5\. A級候補

該当なし。

| 資産 | CBS | EMS | 期待R | MAE想定 | RR |
|--------|--------|--------|--------|--------|--------|
| A級基準 | 75 | 65 | 0.45 | 0.25R以下 | 1.20以上 |
| GOLD | 74 | 64 | 0.39 | 0.38R | 1.60 |
| NASDAQ | 74 | 64 | 0.36 | 0.42R | 1.59 |
| USDJPY | 73 | 62 | 0.35 | 0.46R | 1.50 |

上位3資産とも方向性は認められるが、想定逆行幅とイベントリスクがA級昇格を妨げている。

また、ATR10の実測値を取得できていないため、SL幅の下限条件は暫定評価にとどまる。

## 6\. B級監視候補

| 優先 | 資産 | 方向 | Entry | SL | TP1 | RR |
|--------|--------|--------|--------|--------|--------|--------|
| 1 | GOLD | SELL | 3580–3620 | 3750 | 3360 | 1.60 |
| 2 | NASDAQ | SELL | 26500–26900 | 28400 | 24000 | 1.59 |
| 3 | USDJPY | BUY | 159.50–160.50 | 155.00 | 167.50 | 1.50 |
| 4 | WTI | SELL | 83–85 | 91 | 73 | 1.57 |
| 5 | ETH | SELL | 1690–1730 | 1900 | 1440 | 1.42 |
| 6 | SPX | SELL | 7200–7300 | 7600 | 6800 | 1.29 |

B+観察候補：GOLD、NASDAQ、USDJPY。

較正後勝率については最新の較正係数を取得できていないため、今回は上方補正なしで評価した。

各行のrisk\_pctは0.25%。6件すべてへの同時配分を意味しない。日次合計0.50%の制約を維持する。

## 7\. 触らない資産

| 資産 | 見送り理由 |
|--------|--------|
| BTC | MES不足、ETF/CME根拠不足 |
| DXY | 日次と中期方向の不一致 |
| US10Y | 金融政策と債券需要の競合 |
| VIX | 高変動下での方向持続性不足 |

## 8\. 後日検証ポイント

今回の研究上の重要テーマは、急反発をトレンド転換と判断する条件の妥当性である。

前回は8資産に方向あり判断を出したが、取得できた価格変化では全8資産が逆方向に動いた。個別シグナルの失敗だけではなく、市場レジームの認識が複数資産の判断に共通して影響した可能性がある。

| 検証項目 | 確認内容 |
|--------|--------|
| 反転判定 | 急反発翌日の反落頻度 |
| GOLD | 3500近辺の支持帯の持続性 |
| NASDAQ | ESに対する相対的弱さ |
| USDJPY | DXYとの逆相関状態の持続性 |
| ATR10 | 暫定推定と実測値の差 |
| 時間決済 | 感謝祭を含む営業日処理 |
| MAE | 1ATR以上のSLによる改善 |
| 前回判断 | 正確なsignal\_idと無効化水準の復元 |

現時点でモデルの判定閾値や運用規則は変更しない。

## 9\. Obsidian保存用Observation Draft

```markdown
---
date: 2026-11-25
model: GPT-6.2
system: Tactical Swing OS
regime: RISK_OFF
market_leader: USDJPY
a_count: 0
b_count: 6
b_plus_count: 3
no_trade_count: 4
verified_status: partially_verified
---

# Market Observation

前日の急反発後に株式・金・暗号資産が反落。
USDJPYはDXY下落と同時に大幅上昇。

## Primary Hypothesis

前日の株式反発は持続的なトレンド転換ではなく、
一時的な買い戻しだった可能性が高い。

## Secondary Hypothesis

USDJPYの上昇はドル全面高ではなく、
円固有の弱さに起因する可能性がある。

## Directional Signals

GOLD SELL B+
NASDAQ SELL B+
USDJPY BUY B+
WTI SELL B
ETH SELL B
SPX SELL B

## Research Flags

- REVERSAL_CLASSIFICATION_REVIEW
- CROSS_ASSET_REGIME_DEPENDENCY
- JPY_IDIOSYNCRATIC_WEAKNESS
- ATR10_ESTIMATED_NOT_MEASURED
- THANKSGIVING_LIQUIDITY
- HISTORICAL_INVALIDATION_INCOMPLETE
- GOLD_CONTRACT_UNCONFIRMED
- MIXED_QUOTE_TIMESTAMPS

## Execution Rules

SL distance: minimum 1 ATR10
ATR10 status: provisional estimate
Time exit: 5 trading days
Daily risk limit: 0.50%
Model parameters changed: false
```

## 10\. TSO\_LOG

### CSV — 固定28列・10資産

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-11-25,20261125_GOLD_SELL_PULLBACK,GOLD,SELL,B,PULLBACK,3580,3620,3750,3360,3240,1.60,0.61,0.39,72,74,35,0.25,RISK_OFF,64,71,73,61,74,65,above_3750_PCE_risk,GCZ26_5tradingdays,partially_verified
2026-11-25,20261125_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,49,43,78,,RISK_OFF,48,42,62,40,51,44,ETF_CME_evidence_missing,BTCUSD_5tradingdays,partially_verified
2026-11-25,20261125_ETH_SELL_PULLBACK,ETH,SELL,B,PULLBACK,1690,1730,1900,1440,1300,1.42,0.57,0.24,64,65,46,0.25,RISK_OFF,57,55,68,53,66,58,above_1900,ETHUSD_5tradingdays,partially_verified
2026-11-25,20261125_WTI_SELL_PULLBACK,WTI,SELL,B,PULLBACK,83,85,91,73,68,1.57,0.58,0.32,67,68,43,0.25,RISK_OFF,59,62,69,55,69,61,above_91_supply_risk,CLF27_5tradingdays,partially_verified
2026-11-25,20261125_USDJPY_BUY_PULLBACK,USDJPY,BUY,B,PULLBACK,159.50,160.50,155.00,167.50,170.00,1.50,0.59,0.35,71,73,39,0.25,RISK_OFF,62,68,74,54,73,67,below_155_intervention_risk,USDJPY_5tradingdays,partially_verified
2026-11-25,20261125_SPX_SELL_PULLBACK,SPX,SELL,B,PULLBACK,7200,7300,7600,6800,6550,1.29,0.55,0.19,63,62,48,0.25,RISK_OFF,58,59,65,52,65,60,above_7600_PCE_risk,ESZ26_5tradingdays,partially_verified
2026-11-25,20261125_NASDAQ_SELL_PULLBACK,NASDAQ,SELL,B,PULLBACK,26500,26900,28400,24000,22500,1.59,0.60,0.36,73,74,37,0.25,RISK_OFF,64,67,75,60,74,66,above_28400_PCE_risk,NQZ26_5tradingdays,partially_verified
2026-11-25,20261125_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,48,44,72,,MIXED,49,51,46,45,49,50,direction_conflict,DXY_5tradingdays,partially_verified
2026-11-25,20261125_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,47,42,76,,EVENT,46,50,44,43,47,49,PCE_direction_uncertain,US10Y_yield_5tradingdays,partially_verified
2026-11-25,20261125_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,45,40,79,,RISK_OFF,47,44,51,42,46,48,volatility_direction_uncertain,VIX_index_5tradingdays,partially_verified
```

### JSON — 固定28項目・10資産

```json
[
  {
    "date":"2026-11-25",
    "signal_id":"20261125_GOLD_SELL_PULLBACK",
    "asset":"GOLD",
    "side":"SELL",
    "rank":"B",
    "type":"PULLBACK",
    "entry_low":3580,
    "entry_high":3620,
    "sl":3750,
    "tp1":3360,
    "tp2":3240,
    "rr":1.60,
    "win_prob":0.61,
    "expected_r":0.39,
    "tq_score":72,
    "opp_score":74,
    "no_trade_score":35,
    "risk_pct":0.25,
    "regime":"RISK_OFF",
    "ems":64,
    "ffs":71,
    "cds":73,
    "ias":61,
    "cbs":74,
    "mes":65,
    "invalidation":"above_3750_PCE_risk",
    "verification_target":"GCZ26_5tradingdays",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-11-25",
    "signal_id":"20261125_BTC_NONE_NO_TRADE",
    "asset":"BTC",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":49,
    "opp_score":43,
    "no_trade_score":78,
    "risk_pct":null,
    "regime":"RISK_OFF",
    "ems":48,
    "ffs":42,
    "cds":62,
    "ias":40,
    "cbs":51,
    "mes":44,
    "invalidation":"ETF_CME_evidence_missing",
    "verification_target":"BTCUSD_5tradingdays",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-11-25",
    "signal_id":"20261125_ETH_SELL_PULLBACK",
    "asset":"ETH",
    "side":"SELL",
    "rank":"B",
    "type":"PULLBACK",
    "entry_low":1690,
    "entry_high":1730,
    "sl":1900,
    "tp1":1440,
    "tp2":1300,
    "rr":1.42,
    "win_prob":0.57,
    "expected_r":0.24,
    "tq_score":64,
    "opp_score":65,
    "no_trade_score":46,
    "risk_pct":0.25,
    "regime":"RISK_OFF",
    "ems":57,
    "ffs":55,
    "cds":68,
    "ias":53,
    "cbs":66,
    "mes":58,
    "invalidation":"above_1900",
    "verification_target":"ETHUSD_5tradingdays",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-11-25",
    "signal_id":"20261125_WTI_SELL_PULLBACK",
    "asset":"WTI",
    "side":"SELL",
    "rank":"B",
    "type":"PULLBACK",
    "entry_low":83,
    "entry_high":85,
    "sl":91,
    "tp1":73,
    "tp2":68,
    "rr":1.57,
    "win_prob":0.58,
    "expected_r":0.32,
    "tq_score":67,
    "opp_score":68,
    "no_trade_score":43,
    "risk_pct":0.25,
    "regime":"RISK_OFF",
    "ems":59,
    "ffs":62,
    "cds":69,
    "ias":55,
    "cbs":69,
    "mes":61,
    "invalidation":"above_91_supply_risk",
    "verification_target":"CLF27_5tradingdays",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-11-25",
    "signal_id":"20261125_USDJPY_BUY_PULLBACK",
    "asset":"USDJPY",
    "side":"BUY",
    "rank":"B",
    "type":"PULLBACK",
    "entry_low":159.50,
    "entry_high":160.50,
    "sl":155.00,
    "tp1":167.50,
    "tp2":170.00,
    "rr":1.50,
    "win_prob":0.59,
    "expected_r":0.35,
    "tq_score":71,
    "opp_score":73,
    "no_trade_score":39,
    "risk_pct":0.25,
    "regime":"RISK_OFF",
    "ems":62,
    "ffs":68,
    "cds":74,
    "ias":54,
    "cbs":73,
    "mes":67,
    "invalidation":"below_155_intervention_risk",
    "verification_target":"USDJPY_5tradingdays",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-11-25",
    "signal_id":"20261125_SPX_SELL_PULLBACK",
    "asset":"SPX",
    "side":"SELL",
    "rank":"B",
    "type":"PULLBACK",
    "entry_low":7200,
    "entry_high":7300,
    "sl":7600,
    "tp1":6800,
    "tp2":6550,
    "rr":1.29,
    "win_prob":0.55,
    "expected_r":0.19,
    "tq_score":63,
    "opp_score":62,
    "no_trade_score":48,
    "risk_pct":0.25,
    "regime":"RISK_OFF",
    "ems":58,
    "ffs":59,
    "cds":65,
    "ias":52,
    "cbs":65,
    "mes":60,
    "invalidation":"above_7600_PCE_risk",
    "verification_target":"ESZ26_5tradingdays",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-11-25",
    "signal_id":"20261125_NASDAQ_SELL_PULLBACK",
    "asset":"NASDAQ",
    "side":"SELL",
    "rank":"B",
    "type":"PULLBACK",
    "entry_low":26500,
    "entry_high":26900,
    "sl":28400,
    "tp1":24000,
    "tp2":22500,
    "rr":1.59,
    "win_prob":0.60,
    "expected_r":0.36,
    "tq_score":73,
    "opp_score":74,
    "no_trade_score":37,
    "risk_pct":0.25,
    "regime":"RISK_OFF",
    "ems":64,
    "ffs":67,
    "cds":75,
    "ias":60,
    "cbs":74,
    "mes":66,
    "invalidation":"above_28400_PCE_risk",
    "verification_target":"NQZ26_5tradingdays",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-11-25",
    "signal_id":"20261125_DXY_NONE_NO_TRADE",
    "asset":"DXY",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":48,
    "opp_score":44,
    "no_trade_score":72,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":49,
    "ffs":51,
    "cds":46,
    "ias":45,
    "cbs":49,
    "mes":50,
    "invalidation":"direction_conflict",
    "verification_target":"DXY_5tradingdays",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-11-25",
    "signal_id":"20261125_US10Y_NONE_NO_TRADE",
    "asset":"US10Y",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":47,
    "opp_score":42,
    "no_trade_score":76,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":46,
    "ffs":50,
    "cds":44,
    "ias":43,
    "cbs":47,
    "mes":49,
    "invalidation":"PCE_direction_uncertain",
    "verification_target":"US10Y_yield_5tradingdays",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-11-25",
    "signal_id":"20261125_VIX_NONE_NO_TRADE",
    "asset":"VIX",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":45,
    "opp_score":40,
    "no_trade_score":79,
    "risk_pct":null,
    "regime":"RISK_OFF",
    "ems":47,
    "ffs":44,
    "cds":51,
    "ias":42,
    "cbs":46,
    "mes":48,
    "invalidation":"volatility_direction_uncertain",
    "verification_target":"VIX_index_5tradingdays",
    "verified_status":"partially_verified"
  }
]
```

### 出力監査

| 検査項目 | 結果 |
|--------|--------|
| 対象資産 | 10/10 |
| CSVデータ行 | 10 |
| 固定列数 | 28 |
| JSONレコード | 10 |
| 方向あり判断 | 6 |
| NO\_TRADE | 4 |
| RR再計算 | 6/6一致（小数第2位丸め） |
| B級のEntry・SL・TP1 | 全件記帳 |
| ATR10実測確認 | 未完了 |
| 過去invalidation確認 | 不完全 |
| 新規市場データ取得 | 実施 |
| 運用ルール変更 | なし |
| 外部台帳への保存 | 未実施 |
| チャット上の日次記録 | 完了 |

**本日の研究上の結論：前日の反転買い判断は初期段階で広範囲に逆行した。今日は下落方向を中心に6件を記帳し、USDJPYのみ独立した上昇仮説を採用する。反転判定と市場レジームの共通依存性を今後の検証対象とする。**
