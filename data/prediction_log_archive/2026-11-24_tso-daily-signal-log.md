<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-11-24 07:00 JST -->
<!-- transport: Complete original read_thread message 3e58b88a-bd49-490f-9d28-80febdd6ea12; raw markdown -->
<!-- archived_at: 2026-11-23T23:07:51Z / chars: 9462 / 値は無修正 -->

# Tactical Swing OS — 2026年11月24日（火）

実行モデル：GPT-6
本日の市場の主役：NASDAQ
運用モード：通常寄り防御
GOLD基準限月：COMEX 2026年12月限（GCZ26）

## 1\. 本日の結論

**A級0件、B級8件、NO\_TRADE 2件。**

昨日の米国株式市場は、NVIDIAの経営体制を巡る材料から急反発しました。S&amp;P500現物は約4.75%上昇し、NASDAQ市場ではさらに大きな上昇が確認されています。ただし、前週の急落を完全に修復したわけではありません。citeturn502126news38

今回の判断は、NASDAQ・SPX・GOLDの反発継続を中心に、WTIの戻り売り、DXYの上昇継続を観察する構成です。

| 判定 | 資産 |
|--------|--------|
| A級 | 該当なし |
| B級 | GOLD、ETH、WTI、USDJPY、SPX、NASDAQ、DXY、US10Y |
| NO\_TRADE | BTC、VIX |
| B+観察候補 | NASDAQ、DXY |

**重要な検証制約：** 新規市場検索は実施しましたが、10資産のATR10を算出するための同一参照系列・連続10営業日分のOHLCを確保できていません。以下のSLは広めの暫定値であり、1×ATR10以上であることを検証済みとは扱いません。そのため、A級への昇格は保留し、B級判断を継続します。

## 2\. 前回判断の簡易検証

11月23日の最新方向あり判断について、取得できた価格と比較しました。

| 資産 | 前回方向 | invalidation | 暫定判定 |
|--------|--------|--------|--------|
| GOLD | SELL | 3780超 | not\_fired |
| ETH | SELL | 2000超 | not\_fired |
| WTI | SELL | 91超 | not\_fired |
| USDJPY | SELL | 164.5超 | unknown |
| SPX | SELL | 7350超 | unknown |
| NASDAQ | SELL | 26800超 | unknown |
| DXY | BUY | 102.1割れ | not\_fired |
| US10Y | SELL | 5.18超 | unknown |

GOLDの12月限は11月23日に高値3691.00を記録しており、3780には到達していません。DXYも確認できた当日安値103.59で、102.1を下回っていません。citeturn460088search0turn195205search1

一方、NASDAQ・SPXは前日の売り方向に逆行する大幅反発でした。特にNASDAQは売り仮説の信頼度が低下しています。ただし、**逆行したこととinvalidation水準に到達したことは別**であり、先物の該当時間帯の高値が未確認のため、推測でfiredとはしません。

invalidation\_check: 20261123\_GOLD\_SELL\_PULLBACK=not\_fired, 20261123\_ETH\_SELL\_PULLBACK=not\_fired, 20261123\_WTI\_SELL\_PULLBACK=not\_fired, 20261123\_USDJPY\_SELL\_REVERSAL=unknown, 20261123\_SPX\_SELL\_PULLBACK=unknown, 20261123\_NASDAQ\_SELL\_PULLBACK=unknown, 20261123\_DXY\_BUY\_PULLBACK=not\_fired, 20261123\_US10Y\_SELL\_REVERSAL=unknown

BTC・VIXについては11月23日がNO\_TRADEであり、それ以前の最新方向ありシグナルIDを今回確定できていません。したがって、該当する未決着シグナルの有無は別途台帳照合が必要です。

## 3\. 市場全体の前提

| 市場 | 確認できた基準値 | 時点・状態 |
|--------|--------|--------|
| GOLD GCZ26 | 3639.80 | 11/23 20:24 UTC、遅延値 |
| BTC/USD | 約61376 | 11/23、現物参考値 |
| ETH/USD | 約1735 | 11/23、現物参考値 |
| WTI CLF27 | 約80 | 11/23、概算 |
| USDJPY | 約158.5〜158.95 | 11/23、日中参考値 |
| SPX ESZ26 | 7098.50 | 11/23 米国寄り前、古い参考値 |
| NASDAQ NQZ26 | 25929.50 | 11/23 米国寄り前、古い参考値 |
| DXY | 104.29 | 11/23 日次価格 |
| US10Y | 約4.95% | 11/23、報道参考値 |
| VIX | 20台後半 | 11/23 日中、概算 |

GOLDの価格はGCZ26の個別限月を使用。ES/NQは現物指数の終値を代入せず、先物の寄り前価格を基準にしています。米国株の大幅反発後の先物終値とは異なるため、Entry帯には特に注意が必要です。citeturn460088search0turn502126search6turn195205view0turn460088search3turn195205search1turn502126news40

市場レジームはMIXED。株式の急反発とドル高・金利上昇圧力が同居しています。11月25日の米PCE、26日の感謝祭休場、27日の短縮取引が、通常の5営業日保有に影響します。citeturn195205view0

## 4\. 10資産別判断

以下のEntry・SL・TPは市場価格の確定値ではなく、取得情報に基づく暫定的なモデル判断です。RRはEntry中点から再計算しています。MAEも予測値です。

| 資産 | 判断 | Entry | SL | TP1 | RR | MAE想定 |
|--------|--------|--------|--------|--------|--------|--------|
| GOLD | B BUY | 3600–3650 | 3430 | 3950 | 1.667 | 0.35R |
| BTC | NO\_TRADE | — | — | — | — | — |
| ETH | B BUY | 1700–1760 | 1480 | 2130 | 1.600 | 0.42R |
| WTI | B SELL | 80–83 | 90 | 68 | 1.588 | 0.38R |
| USDJPY | B SELL | 158–159.5 | 162 | 153 | 1.769 | 0.36R |
| SPX | B BUY | 7150–7250 | 6700 | 7900 | 1.400 | 0.33R |
| NASDAQ | B BUY | 26000–26700 | 24000 | 31000 | 1.979 | 0.30R |
| DXY | B BUY | 103.8–104.3 | 102.5 | 107 | 1.903 | 0.32R |
| US10Y | B BUY | 4.88–4.98 | 4.65 | 5.35 | 1.500 | 0.39R |
| VIX | NO\_TRADE | — | — | — | — | — |

NASDAQは11月23日の大幅反発によって前回SELLからBUYへ方向転換。もっとも、急騰直後の押し戻しやPCE前の利食いが想定されるため、CBS73・EMS64・expected\_r0.33でA級条件には未達です。

GOLDは前週の急落後に反発しましたが、まだ下降構造の修復過程です。WTIは供給回復報道による下落を評価し、供給ショック直後の上昇追随ではなくSELLの戻り売り監視とします。citeturn195205view0

BTCは現物が反発しているものの、ETF資金流出とMES39を重視してNO\_TRADE。ETHは反発方向の監視水準を残します。

## 5\. A級候補

本日は該当なし。

NASDAQが最も近いものの、CBS75・EMS65・expected\_r0.45の各条件を満たしていません。ATR10の未検証も残っています。A級を無理に作らず、B級で観測を継続します。

## 6\. B級監視候補

優先順位はNASDAQ、GOLD、DXY、SPX、USDJPY、WTI、US10Y、ETHです。

NASDAQとDXYはB+観察条件を満たします。NASDAQはCBS73、EMS64、RR1.979、win\_prob0.53。DXYはCBS67のため、厳密にはB+条件未達です。したがって、**正式なB+観察候補はNASDAQのみ**と訂正します。

日次リスクは通常0.25%、合計上限0.50%。複数のB級候補を同時に全件参加する前提ではありません。

## 7\. 触らない資産

BTCはETF/CME根拠の不足とMES39により見送り。VIXは反発局面でのボラティリティ急低下後に方向の優位性を確定できず、NO\_TRADEとします。

## 8\. 後日検証ポイント

1. NASDAQの反発が一日限りか、翌営業日も継続するか。
2. GCZ26が3600を維持し、反発構造を形成するか。
3. BTCの60000維持とETFフロー改善が同時に起きるか。
4. WTIが80を割り込むか、供給関連ニュースで反転するか。
5. PCE前後でドル・米金利・株式の相関が変化するか。
6. 全B級のATR10実測、SL下限適合、5営業日後のR損益。

## 9\. Obsidian保存用Observation Draft

```markdown
# TSO Observation 2026-11-24

Model: GPT-6
Market Leader: NASDAQ
Regime: MIXED
Gold Contract: GCZ26

## Summary
A: 0
B: 8
NO_TRADE: 2
B+: NASDAQ

## Thesis
- NVIDIA関連材料で米国株が急反発
- NASDAQは前回SELLからBUYへ転換
- GOLDは急落後の反発
- WTIは供給回復を背景にSELL監視
- BTCはETFフローとMES不足で見送り

## Data Quality
- ATR10 exact calculation: pending
- ES/NQ post-rally futures settlement: pending
- Prior invalidation checks: partially complete
- All entries and targets: model estimates

## Next Verification
- ATR10 compliance
- PCE event response
- Five-business-day time exit
- Entry and SL path verification
```

## 10\. TSO\_LOG

CSVは固定28列、10資産10行です。NO\_TRADE行の8項目とrisk\_pctは空欄。RRはEntry中点・SL・TP1から算出しています。

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-11-24,20261124_GOLD_BUY_REVERSAL,GOLD,BUY,B,REVERSAL,3600,3650,3430,3950,4100,1.667,0.51,0.27,68,67,36,0.25,MIXED,63,55,59,60,69,60,below_3430,GCZ26,partially_verified
2026-11-24,20261124_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,48,43,77,,MIXED,45,38,42,40,48,39,below_55000,BTCUSD_spot,partially_verified
2026-11-24,20261124_ETH_BUY_REVERSAL,ETH,BUY,B,REVERSAL,1700,1760,1480,2130,2300,1.6,0.48,0.12,56,57,49,0.25,MIXED,54,44,48,46,57,45,below_1480,ETHUSD_spot,partially_verified
2026-11-24,20261124_WTI_SELL_PULLBACK,WTI,SELL,B,PULLBACK,80,83,90,68,63,1.588,0.53,0.21,64,62,44,0.25,EVENT,58,53,55,51,65,58,above_90,CLF27,partially_verified
2026-11-24,20261124_USDJPY_SELL_PULLBACK,USDJPY,SELL,B,PULLBACK,158,159.5,162,153,150,1.769,0.52,0.24,65,63,42,0.25,MIXED,61,55,56,57,68,58,above_162,USDJPY,partially_verified
2026-11-24,20261124_SPX_BUY_REVERSAL,SPX,BUY,B,REVERSAL,7150,7250,6700,7900,8200,1.4,0.52,0.28,66,66,43,0.25,MIXED,62,58,54,60,70,60,below_6700,ESZ26,partially_verified
2026-11-24,20261124_NASDAQ_BUY_REVERSAL,NASDAQ,BUY,B,REVERSAL,26000,26700,24000,31000,33000,1.979,0.53,0.33,70,70,39,0.25,MIXED,64,60,58,61,73,62,below_24000,NQZ26,partially_verified
2026-11-24,20261124_DXY_BUY_PULLBACK,DXY,BUY,B,PULLBACK,103.8,104.3,102.5,107,108,1.903,0.52,0.2,64,61,43,0.25,MIXED,61,56,58,57,67,60,below_102.5,DXY,partially_verified
2026-11-24,20261124_US10Y_BUY_REVERSAL,US10Y,BUY,B,REVERSAL,4.88,4.98,4.65,5.35,5.5,1.5,0.51,0.16,59,55,50,0.25,MIXED,55,51,49,53,60,54,below_4.65,US10Y_yield,partially_verified
2026-11-24,20261124_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,45,37,79,,MIXED,40,43,38,37,43,40,VIX_index_reversal,VIX_index,partially_verified
```

JSONは同じ10件を固定列順の配列として保持します。先頭の`columns`がCSVヘッダーと対応し、`rows`の各配列は28要素です。空欄は`null`で表現します。

```json
{
  "date": "2026-11-24",
  "columns": ["date","signal_id","asset","side","rank","type","entry_low","entry_high","sl","tp1","tp2","rr","win_prob","expected_r","tq_score","opp_score","no_trade_score","risk_pct","regime","ems","ffs","cds","ias","cbs","mes","invalidation","verification_target","verified_status"],
  "rows": [
    ["2026-11-24","20261124_GOLD_BUY_REVERSAL","GOLD","BUY","B","REVERSAL",3600,3650,3430,3950,4100,1.667,0.51,0.27,68,67,36,0.25,"MIXED",63,55,59,60,69,60,"below_3430","GCZ26","partially_verified"],
    ["2026-11-24","20261124_BTC_NONE_NO_TRADE","BTC","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,48,43,77,null,"MIXED",45,38,42,40,48,39,"below_55000","BTCUSD_spot","partially_verified"],
    ["2026-11-24","20261124_ETH_BUY_REVERSAL","ETH","BUY","B","REVERSAL",1700,1760,1480,2130,2300,1.6,0.48,0.12,56,57,49,0.25,"MIXED",54,44,48,46,57,45,"below_1480","ETHUSD_spot","partially_verified"],
    ["2026-11-24","20261124_WTI_SELL_PULLBACK","WTI","SELL","B","PULLBACK",80,83,90,68,63,1.588,0.53,0.21,64,62,44,0.25,"EVENT",58,53,55,51,65,58,"above_90","CLF27","partially_verified"],
    ["2026-11-24","20261124_USDJPY_SELL_PULLBACK","USDJPY","SELL","B","PULLBACK",158,159.5,162,153,150,1.769,0.52,0.24,65,63,42,0.25,"MIXED",61,55,56,57,68,58,"above_162","USDJPY","partially_verified"],
    ["2026-11-24","20261124_SPX_BUY_REVERSAL","SPX","BUY","B","REVERSAL",7150,7250,6700,7900,8200,1.4,0.52,0.28,66,66,43,0.25,"MIXED",62,58,54,60,70,60,"below_6700","ESZ26","partially_verified"],
    ["2026-11-24","20261124_NASDAQ_BUY_REVERSAL","NASDAQ","BUY","B","REVERSAL",26000,26700,24000,31000,33000,1.979,0.53,0.33,70,70,39,0.25,"MIXED",64,60,58,61,73,62,"below_24000","NQZ26","partially_verified"],
    ["2026-11-24","20261124_DXY_BUY_PULLBACK","DXY","BUY","B","PULLBACK",103.8,104.3,102.5,107,108,1.903,0.52,0.2,64,61,43,0.25,"MIXED",61,56,58,57,67,60,"below_102.5","DXY","partially_verified"],
    ["2026-11-24","20261124_US10Y_BUY_REVERSAL","US10Y","BUY","B","REVERSAL",4.88,4.98,4.65,5.35,5.5,1.5,0.51,0.16,59,55,50,0.25,"MIXED",55,51,49,53,60,54,"below_4.65","US10Y_yield","partially_verified"],
    ["2026-11-24","20261124_VIX_NONE_NO_TRADE","VIX","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,45,37,79,null,"MIXED",40,43,38,37,43,40,"VIX_index_reversal","VIX_index","partially_verified"]
  ]
}
```

**本日の最終判断：NASDAQのBUY反転を最優先で観察。ただしA級は0件。** 前日までの売り仮説から大きく環境が変化した日として、方向転換の妥当性と5営業日後の結果を重点的に検証します。
