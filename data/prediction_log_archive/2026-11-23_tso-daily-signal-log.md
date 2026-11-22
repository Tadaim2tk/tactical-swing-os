<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-11-23 07:00 JST -->
<!-- transport: Complete original read_thread message 5aebae70-366d-4b2a-b45d-b17bfabeb758; raw markdown -->
<!-- archived_at: 2026-11-22T23:02:49Z / chars: 7478 / 値は無修正 -->

# Tactical Swing OS v2 — 2026年11月23日（月）

実行モデル：GPT-6
判断基準時刻：2026年11月23日 07:03 JST
本日の市場の主役：**NASDAQ**

## 1\. 本日の結論

**A級候補0件、B級監視候補8件、NO\_TRADE 2件。**

11月20日の米国市場では、S&amp;P500が3.70%下落し、NASDAQ総合指数は5.28%下落。VIXは35.89まで上昇しました。AI関連株を中心とした売却が他資産にも波及しています。citeturn989455news32turn989455search2

ただし、下落方向が強いことと、新規売りの期待値が高いことは別です。急落後の反発を考慮し、A級への昇格は見送ります。

| 優先 | 資産 | 判断 | 主観勝率 | expected\_r |
|--------|--------|--------|--------|--------|
| 1 | NASDAQ | B・SELL | 0.52 | \+0.38R |
| 2 | SPX | B・SELL | 0.51 | \+0.35R |
| 3 | GOLD | B・SELL | 0.49 | \+0.30R |
| 4 | USDJPY | B・SELL | 0.49 | \+0.31R |
| 5 | DXY | B・BUY | 0.51 | \+0.29R |

このほかETH、WTI、US10YもB級として記帳します。BTCとVIXはNO\_TRADEです。

**重要な検証制約：** 価格の基準値は複数資産で取得できましたが、10本分の確定OHLCによるATR10計算はGOLD以外で完了していません。以下のB級水準は暫定モデル値であり、全銘柄について1×ATR10以上のSL条件を確認済みという意味ではありません。

## 2\. 前回判断の簡易検証

11月20日までの個別TSO\_LOGについて、前回の方向あり判断のsignal\_idとinvalidation水準を完全には照合できていません。

したがって、前回判断の勝敗、SL到達、invalidation発動を推測で確定させません。

`invalidation_check: 対象となる過去signal_idの個別照合未完了`

これは全資産の価格が取得不能という意味ではありません。前回のsignal\_idと当該判断日以降の高値・安値の照合が未完了という意味です。前回判断の検証結果は未確定として扱います。

## 3\. 市場全体の前提

### 直近の市場基準値

| 資産 | 参照価格 | データ時点・系列 |
|--------|--------|--------|
| GOLD | 3,515.40 | 11/20、COMEX 2026年12月限 GCZ6 |
| BTC | 60,744.83 | 11/22 18:00 UTC、Coinbase現物 |
| ETH | 1,712.01 | 同上 |
| WTI | 83.98 | 11/20、2027年1月限 |
| USDJPY | 約161.00 | 11/20、参考値 |
| SPX | 6,910.39 | 11/20、S&amp;P500現物参考値 |
| NASDAQ | 25,028.98 | 11/20、NASDAQ100現物参考値 |
| DXY | 約103.9 | 11/20 |
| US10Y | 約4.92% | 11/20 |
| VIX | 35.89 | 11/20 |

GOLDはGCZ6の終値系列を採用します。SPXとNASDAQの表中価格は現物指数であり、TSO\_LOGのESZ6・NQZ6とは異なります。したがって先物のEntry帯は暫定値で、現物終値を先物終値として代入していません。citeturn989455search4turn874152search6turn874152news37turn989455search7turn874152search1

### 今週のイベント

11月23日に米国PMI、25日に米国GDP・個人消費関連指標、26日に感謝祭、27日に短縮取引が予定されています。今週は通常より流動性が低下しやすく、5営業日保有の評価にも祝日を反映する必要があります。citeturn989455search3turn874152search6

市場レジームは **RISK\_OFF** を中心に評価します。ただしドル円とWTIには独自のイベント要因があり、全資産を一律に同方向とは判断しません。

## 4\. 10資産別判断

| 資産 | 方向・級 | Entry帯 | SL | TP1 | RR |
|--------|--------|--------|--------|--------|--------|
| GOLD | SELL B | 3590–3630 | 3780 | 3340 | 1.588 |
| BTC | NO\_TRADE | — | — | — | — |
| ETH | SELL B | 1730–1780 | 2000 | 1390 | 1.490 |
| WTI | SELL B | 84–86 | 91 | 75 | 1.667 |
| USDJPY | SELL B | 160–161.5 | 164.5 | 154.5 | 1.667 |
| SPX | SELL B | 6890–7010 | 7350 | 6400 | 1.375 |
| NASDAQ | SELL B | 24900–25400 | 26800 | 22400 | 1.667 |
| DXY | BUY B | 103.4–104 | 102.1 | 106 | 1.437 |
| US10Y | SELL B | 4.90–4.99 | 5.18 | 4.55 | 1.681 |
| VIX | NO\_TRADE | — | — | — | — |

上記は全て主観的な監視水準です。RRはEntry帯の中点とSL・TP1から再計算済みです。

GOLDは金利・ドル高と資産売却圧力が下落要因。NASDAQとSPXは株式市場の下落継続を基本シナリオとしますが、売られ過ぎによる急反発が最大のリスクです。

USDJPYはドル高と円買い介入警戒が競合します。WTIは供給環境と中東情勢の急変に注意します。BTCは週末に55,106ドルまで下落した後、60,000ドル台へ回復しましたが、ETF・CME根拠の不足とMES42によりNO\_TRADEを優先します。citeturn874152search6turn874152news35turn874152news37

各B級のMAE想定は現時点で定量確定できず、A級条件のMAE≤0.25Rは未充足扱いです。ATR10確認前にSLを縮小することはしません。

## 5\. A級候補

**該当なし。**

NASDAQが最も近い候補ですが、CBS74、EMS63、expected\_r+0.38Rで、A級の基準を下回ります。今後の価格検証で条件を満たせば再評価します。

## 6\. B級監視候補

GOLD、ETH、WTI、USDJPY、SPX、NASDAQ、DXY、US10Yの8件を記帳します。

B+条件を全て満たす候補はありません。NASDAQはCBS74、EMS63、RR1.667、主観勝率0.52で、B+観察条件の数値上は満たします。ただしATR10未検証のため、**暫定B+観察候補**とします。

## 7\. 触らない資産

BTCは週末の大幅な上下動とETF・CME根拠不足、VIXは急騰後の反落リスクと直接売買する商品との価格差が理由です。

## 8\. 後日検証ポイント

1. NASDAQが25,400付近を回復できるか、下落が再開するか。
2. GOLDのGCZ6が3,500付近を維持できるか。
3. BTCが週末安値55,106と高値61,568のどちらを突破するか。
4. 米国PMIと25日の経済指標が金利・ドル・株式の相関を変えるか。
5. ESZ6・NQZ6および他資産のATR10を確定し、B級SLの下限条件を再検証する。

## 9\. Obsidian保存用Observation Draft

```text
date: 2026-11-23
model: GPT-6
system: Tactical Swing OS v2
market_leader: NASDAQ
dominant_regime: RISK_OFF
A_count: 0
B_count: 8
NO_TRADE_count: 2
B_plus_provisional: NASDAQ
main_hypothesis: AI関連株主導の下落が他資産へ波及
counter_hypothesis: 急落後の買い戻しによる反発
data_quality: partially_verified
atr10_validation: incomplete_except_GOLD_data_available
previous_signal_validation: incomplete
risk_mode: normal_defensive
daily_risk_cap_pct: 0.50
time_exit: 5_business_days
observation: 下落方向の優位性と新規参加の期待値を区別する
```

## 10\. TSO\_LOG — CSV

28列固定、10資産10行、各行27個のカンマを確認済みです。

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-11-23,20261123_GOLD_SELL_PULLBACK,GOLD,SELL,B,PULLBACK,3590,3630,3780,3340,3220,1.588,0.49,0.3,72,68,30,0.25,RISK_OFF,63,68,58,60,72,55,GCZ6_above_3780,GCZ6_OHLC,partially_verified
2026-11-23,20261123_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,56,54,75,,EVENT,50,50,45,48,55,42,BTC_ETF_CME_unconfirmed,BTCUSD_spot_OHLC,partially_verified
2026-11-23,20261123_ETH_SELL_PULLBACK,ETH,SELL,B,PULLBACK,1730,1780,2000,1390,1250,1.49,0.48,0.25,68,65,40,0.25,RISK_OFF,59,61,52,58,68,48,ETHUSD_above_2000,ETHUSD_spot_OHLC,partially_verified
2026-11-23,20261123_WTI_SELL_PULLBACK,WTI,SELL,B,PULLBACK,84,86,91,75,71,1.667,0.51,0.28,65,62,45,0.25,EVENT,55,62,55,54,66,50,WTI_Jan27_above_91,CLF27_OHLC,partially_verified
2026-11-23,20261123_USDJPY_SELL_REVERSAL,USDJPY,SELL,B,REVERSAL,160,161.5,164.5,154.5,152,1.667,0.49,0.31,68,66,43,0.25,EVENT,57,60,55,58,69,58,USDJPY_above_164.5,USDJPY_OHLC,partially_verified
2026-11-23,20261123_SPX_SELL_PULLBACK,SPX,SELL,B,PULLBACK,6890,7010,7350,6400,6200,1.375,0.51,0.35,73,70,30,0.25,RISK_OFF,61,66,62,63,73,60,ES_above_7350,ESZ6_OHLC,partially_verified
2026-11-23,20261123_NASDAQ_SELL_PULLBACK,NASDAQ,SELL,B,PULLBACK,24900,25400,26800,22400,21400,1.667,0.52,0.38,74,72,29,0.25,RISK_OFF,63,65,61,64,74,62,NQ_above_26800,NQZ6_OHLC,partially_verified
2026-11-23,20261123_DXY_BUY_PULLBACK,DXY,BUY,B,PULLBACK,103.4,104,102.1,106,107,1.437,0.51,0.29,67,65,39,0.25,MIXED,60,63,57,58,69,57,DXY_below_102.1,DXY_OHLC,partially_verified
2026-11-23,20261123_US10Y_SELL_REVERSAL,US10Y,SELL,B,REVERSAL,4.9,4.99,5.18,4.55,4.4,1.681,0.51,0.26,64,60,45,0.25,RISK_OFF,58,62,55,56,65,54,US10Y_above_5.18,US10Y_yield_OHLC,partially_verified
2026-11-23,20261123_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,45,40,80,,RISK_OFF,43,44,40,42,45,40,VIX_spike_reversal,VIX_index_OHLC,partially_verified
```

### TSO\_LOG — JSON

CSVと同じ10資産の判断を、主要評価項目を保持した簡易JSONとして併記します。完全な28列の記録は上記CSVを正本とします。

```json
{
  "date": "2026-11-23",
  "model": "GPT-6",
  "market_leader": "NASDAQ",
  "regime": "RISK_OFF",
  "atr10_validation": "incomplete",
  "previous_invalidation_validation": "incomplete",
  "signals": [
    {"asset":"GOLD","side":"SELL","rank":"B","rr":1.588,"win_prob":0.49,"expected_r":0.30},
    {"asset":"BTC","side":"NONE","rank":"NO_TRADE"},
    {"asset":"ETH","side":"SELL","rank":"B","rr":1.490,"win_prob":0.48,"expected_r":0.25},
    {"asset":"WTI","side":"SELL","rank":"B","rr":1.667,"win_prob":0.51,"expected_r":0.28},
    {"asset":"USDJPY","side":"SELL","rank":"B","rr":1.667,"win_prob":0.49,"expected_r":0.31},
    {"asset":"SPX","side":"SELL","rank":"B","rr":1.375,"win_prob":0.51,"expected_r":0.35},
    {"asset":"NASDAQ","side":"SELL","rank":"B","rr":1.667,"win_prob":0.52,"expected_r":0.38},
    {"asset":"DXY","side":"BUY","rank":"B","rr":1.437,"win_prob":0.51,"expected_r":0.29},
    {"asset":"US10Y","side":"SELL","rank":"B","rr":1.681,"win_prob":0.51,"expected_r":0.26},
    {"asset":"VIX","side":"NONE","rank":"NO_TRADE"}
  ],
  "verified_status": "partially_verified"
}
```

**最終判断：** NASDAQの下落継続を中心仮説とし、SPX・GOLDを次点とします。ただし、A級は0件です。10資産の日次記録は維持し、ATR10と前回invalidationの未確定項目を次回検証対象として残します。
