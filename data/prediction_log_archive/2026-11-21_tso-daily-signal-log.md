<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-11-21 07:00 JST -->
<!-- transport: Complete original read_thread message 174def78-7030-4f04-8dda-c19cf19b9c97; raw markdown -->
<!-- archived_at: 2026-11-20T23:20:00Z / chars: 9974 / 値は無修正 -->

# Tactical Swing OS — 2026年11月21日（土）日次判断

実行モデル：GPT-6
本日の市場の主役：**NASDAQ**
市場レジーム：RISK\_OFF
運用モード：通常寄り防御
データ基準：11月20日（金）の米国市場終値・直近取引データ

## 1\. 本日の結論

**A級0件、B級5件、NO\_TRADE 5件。**

11月20日の米国市場では、AI関連株を中心とする売りが加速し、S&amp;P500とダウ平均が調整局面に入った。NASDAQの下落に加え、金・暗号資産も売られ、VIXは急上昇した。citeturn652109news34turn652109news36turn652109news43

本日の重要な変化は、**通常のドル高・金利高による調整から、広範なリスク資産のポジション解消へ移行している可能性**である。

| 優先度 | 資産 | 判断 | win\_prob | expected\_r |
|--------|--------|--------|--------|--------|
| 1 | NASDAQ | B / SELL | 0.55 | \+0.39R |
| 2 | GOLD | B / SELL | 0.55 | \+0.36R |
| 3 | SPX | B / SELL | 0.54 | \+0.33R |
| 4 | WTI | B / SELL | 0.51 | \+0.21R |
| 5 | USDJPY | B / SELL | 0.51 | \+0.18R |

土曜日のため、通常の先物・為替市場は休場している。本日のB級は新たな方向判断として記帳するが、監視価格は次回取引セッションに向けた暫定水準である。月曜のギャップでEntry・SL・RRが変化する可能性がある。

## 2\. 前回判断の簡易検証

11月20日の最新方向あり判断5件を対象とする。

| 前回signal\_id | invalidation | 検証結果 |
|--------|--------|--------|
| 20261120\_GOLD\_SELL\_PULLBACK | 3830超え | not\_fired |
| 20261120\_WTI\_SELL\_PULLBACK | 87超え | not\_fired |
| 20261120\_USDJPY\_BUY\_PULLBACK | 158.3割れ | unknown |
| 20261120\_SPX\_SELL\_PULLBACK | 7500超え | not\_fired |
| 20261120\_NASDAQ\_SELL\_PULLBACK | 28300超え | not\_fired |

GOLD、WTI、ES、NQは11月20日の確認できた高値がそれぞれのinvalidation水準を下回る。USDJPYは当日の完全な安値系列を照合できないためunknownとした。citeturn652109search0turn551554search0turn551554search2turn510041search6

`invalidation_check: 20261120_GOLD_SELL_PULLBACK=not_fired, 20261120_WTI_SELL_PULLBACK=not_fired, 20261120_USDJPY_BUY_PULLBACK=unknown, 20261120_SPX_SELL_PULLBACK=not_fired, 20261120_NASDAQ_SELL_PULLBACK=not_fired`

この判定はinvalidationの発動有無であり、約定・損益・TP到達の確定判定ではない。

## 3\. 市場全体の前提

| 指標 | 11月20日参照値 | 評価 |
|--------|--------|--------|
| GOLD GCZ26 | 3515.40 | 急落 |
| BTC/USD | 60000割れ | 弱気 |
| ETH/USD | 1735付近（20日05:46 UTC） | 弱気 |
| WTI 2027年1月限 | 81.61 | 弱気 |
| USDJPY | 158.73（20日13:55 GMT） | 円高方向へ反転 |
| ESZ26 | 7098.00 | 弱気 |
| NQZ26 | 約25300〜25400 | 急落 |
| DXY | 103.67（20日13:55 GMT） | 高値圏から反落 |
| US10Y | 4.948%付近 | 安全資産買いで低下 |
| VIX | 約37〜38 | 強い警戒 |

GOLDの3515.40はReutersが報じたCOMEX12月限の清算値。一方、Investing.comの履歴表には3608.50が掲載されており、**同じGCZ26でもデータ間に大きな不一致**がある。GOLDの新規監視帯はReuters値を起点にした暫定評価とし、確定した同一限月の価格照合が必要である。citeturn652109news41turn652109search0

ESは7098、NQは25371付近、WTIは81.61の履歴データを確認。VIXはYahoo Financeの履歴で37台後半、Reutersは米国市場中の急騰を報じている。citeturn551554search2turn510041search8turn551554search0turn510041search2turn510041news25

11月20日のリスクオフでは米国債が買われ、10年債利回りが約4.95%へ低下した。従来の「金利上昇が株式を押し下げる」という説明だけでは不十分になっている。citeturn652109news37

## 4\. 10資産別判断

| 資産 | 判断 | 価格構造・イベントリスク |
|--------|--------|--------|
| GOLD | SELL / B | 急落継続。強制的なポジション解消と短期反発の両方を警戒 |
| BTC | NO\_TRADE | 下落方向だがMES40、ETF/CME裏付け不足 |
| ETH | NO\_TRADE | BTC連動の下落。独立した売買優位性が弱い |
| WTI | SELL / B | 供給超過懸念。ただし中東情勢の急変に注意 |
| USDJPY | SELL / B | 前日のBUYから円高方向への反転を暫定評価 |
| SPX | SELL / B | 調整局面入り、広範な株式売り |
| NASDAQ | SELL / B | AI関連株の下落とボラティリティ拡大 |
| DXY | NO\_TRADE | ドル高一服。反転の持続性は未確認 |
| US10Y | NO\_TRADE | 利回り低下と金融政策見通しが交錯 |
| VIX | NO\_TRADE | 急騰後の反転リスクが大きい |

方向あり5件の監視水準は次のとおり。

| 資産 | Entry帯 | SL | TP1 | TP2 | RR | MAE想定 |
|--------|--------|--------|--------|--------|--------|--------|
| GOLD SELL | 3500–3580 | 3780 | 3100 | 2900 | 1.833 | 0.39R |
| WTI SELL | 81.5–83.5 | 89 | 73 | 69 | 1.462 | 0.43R |
| USDJPY SELL | 158.5–159.3 | 161 | 155 | 153 | 1.857 | 0.38R |
| SPX SELL | 7040–7160 | 7500 | 6500 | 6300 | 1.500 | 0.41R |
| NASDAQ SELL | 25100–25700 | 27500 | 22000 | 21000 | 1.619 | 0.44R |

RRはEntry中点から再計算した。

**ATR10について：** 11月20日までの10営業日OHLCを全資産で同一基準に揃えた厳密な計算は未完了。SL距離は広めに設定した暫定値であり、1×ATR10下限を満たすと確定したものではない。月曜の新規約定判断では、ギャップ後のEntry中点・ATR10・RRを再照合する必要がある。

## 5\. A級候補

**0件。**

最も強いNASDAQでもCBS74、EMS64、expected\_r0.39R、MAE0.44Rであり、A級の複数条件を満たしていない。

急落方向への確信が高まったことと、現在の価格で優れた新規エントリーができることは別である。

## 6\. B級監視候補

NASDAQ、GOLD、SPX、WTI、USDJPYの5件を継続記帳する。

B+観察候補は、NASDAQ、GOLD、SPXの3件。いずれもCBS70以上、EMS60以上、RR1.5以上、主観win\_prob0.50以上を満たす。A級への自動昇格はしない。

USDJPYは前日のBUYからSELLに変更した。これは前日の判断がSLに達したからではなく、ドル高一辺倒の構造が崩れ、リスクオフ局面で円が買われ始めたという価格・市場構造の変化による。

## 7\. 触らない資産

BTC、ETH、DXY、US10Y、VIX。

BTCは方向としては下落優勢だが、MES40とETF/CMEの検証不足によりNO\_TRADE。VIXは急騰しており、価格変動の大きさだけで新規BUYを選択しない。

## 8\. 後日検証ポイント

- NASDAQ：NQZ26の27500回復、または22000方向への下落。
- GOLD：GCZ26の3780回復、または3100方向への下落。
- SPX：ESZ26の7500回復と株式市場の反発力。
- USDJPY：161超えで円高シナリオ否定。
- WTI：89超え、供給ショック・中東情勢の変化。
- VIX：高水準から急反落した場合、株式売りの期待値が低下するか。
- 金曜日に発生した大幅下落後、月曜寄り付きのギャップが新規SELL判断のRRをどう変化させるか。

## 9\. Obsidian保存用Observation Draft

```markdown
# TSO Observation 2026-11-21

model: GPT-6
market_leader: NASDAQ
regime: RISK_OFF
A: 0
B: 5
NO_TRADE: 5

## Market hypothesis
AI関連株の急落を中心にリスクオフが加速。
金・暗号資産にも売りが波及。
米国債は買われ、金利は低下。
従来のドル高・金利高だけでは説明できない
ポジション解消局面へ移行している可能性。

## Directional decisions
NASDAQ SELL B
GOLD SELL B
SPX SELL B
WTI SELL B
USDJPY SELL B

## No trade
BTC ETH DXY US10Y VIX

## Main observations
- VIX急騰
- USDJPYはBUYからSELLへ転換
- GOLD価格提供元の不一致
- 月曜ギャップとATR10の再照合が必要

## Risk
通常0.25%
A級のみ0.50%
日次合計0.50%
5営業日時間決済
```

## 10\. TSO\_LOG

### CSV — 固定28列、10資産

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-11-21,20261121_GOLD_SELL_PULLBACK,GOLD,SELL,B,PULLBACK,3500,3580,3780,3100,2900,1.833,0.55,0.36,73,76,29,0.25,RISK_OFF,64,65,68,55,74,67,GCZ26_above_3780,GCZ26_Dec_futures,partially_verified
2026-11-21,20261121_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,45,43,82,,RISK_OFF,43,46,47,38,50,40,ETF_CME_unconfirmed,BTCUSD_spot,partially_verified
2026-11-21,20261121_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,46,43,78,,RISK_OFF,45,44,47,40,51,44,ETH_structure_unconfirmed,ETHUSD_spot,partially_verified
2026-11-21,20261121_WTI_SELL_PULLBACK,WTI,SELL,B,PULLBACK,81.5,83.5,89,73,69,1.462,0.51,0.21,61,62,52,0.25,EVENT,56,52,51,46,63,55,CLF27_above_89,WTI_Jan27_futures,partially_verified
2026-11-21,20261121_USDJPY_SELL_REVERSAL,USDJPY,SELL,B,REVERSAL,158.5,159.3,161,155,153,1.857,0.51,0.18,60,60,53,0.25,EVENT,57,56,51,47,64,58,USDJPY_above_161,USDJPY_spot,partially_verified
2026-11-21,20261121_SPX_SELL_PULLBACK,SPX,SELL,B,PULLBACK,7040,7160,7500,6500,6300,1.5,0.54,0.33,72,75,34,0.25,RISK_OFF,63,62,67,55,73,65,ESZ26_above_7500,ESZ26_futures,partially_verified
2026-11-21,20261121_NASDAQ_SELL_PULLBACK,NASDAQ,SELL,B,PULLBACK,25100,25700,27500,22000,21000,1.619,0.55,0.39,75,78,32,0.25,RISK_OFF,64,64,69,56,74,66,NQZ26_above_27500,NQZ26_futures,partially_verified
2026-11-21,20261121_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,53,49,70,,MIXED,50,53,49,45,57,54,DXY_reversal_unconfirmed,DXY_index,partially_verified
2026-11-21,20261121_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,52,48,73,,MIXED,49,50,47,43,54,52,US10Y_yield_direction_unconfirmed,US10Y_yield_pct,partially_verified
2026-11-21,20261121_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,55,52,80,,EVENT,47,48,45,42,58,50,VIX_spike_reversal_unconfirmed,VIX_index,partially_verified
```

### JSON

CSVと同一の28列順を維持し、空欄はnullで表す。

```json
{
  "date": "2026-11-21",
  "model": "GPT-6",
  "market_leader": "NASDAQ",
  "columns": [
    "date","signal_id","asset","side","rank","type",
    "entry_low","entry_high","sl","tp1","tp2","rr",
    "win_prob","expected_r","tq_score","opp_score",
    "no_trade_score","risk_pct","regime","ems","ffs",
    "cds","ias","cbs","mes","invalidation",
    "verification_target","verified_status"
  ],
  "rows": [
    ["2026-11-21","20261121_GOLD_SELL_PULLBACK","GOLD","SELL","B","PULLBACK",3500,3580,3780,3100,2900,1.833,0.55,0.36,73,76,29,0.25,"RISK_OFF",64,65,68,55,74,67,"GCZ26_above_3780","GCZ26_Dec_futures","partially_verified"],
    ["2026-11-21","20261121_BTC_NONE_NO_TRADE","BTC","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,45,43,82,null,"RISK_OFF",43,46,47,38,50,40,"ETF_CME_unconfirmed","BTCUSD_spot","partially_verified"],
    ["2026-11-21","20261121_ETH_NONE_NO_TRADE","ETH","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,46,43,78,null,"RISK_OFF",45,44,47,40,51,44,"ETH_structure_unconfirmed","ETHUSD_spot","partially_verified"],
    ["2026-11-21","20261121_WTI_SELL_PULLBACK","WTI","SELL","B","PULLBACK",81.5,83.5,89,73,69,1.462,0.51,0.21,61,62,52,0.25,"EVENT",56,52,51,46,63,55,"CLF27_above_89","WTI_Jan27_futures","partially_verified"],
    ["2026-11-21","20261121_USDJPY_SELL_REVERSAL","USDJPY","SELL","B","REVERSAL",158.5,159.3,161,155,153,1.857,0.51,0.18,60,60,53,0.25,"EVENT",57,56,51,47,64,58,"USDJPY_above_161","USDJPY_spot","partially_verified"],
    ["2026-11-21","20261121_SPX_SELL_PULLBACK","SPX","SELL","B","PULLBACK",7040,7160,7500,6500,6300,1.5,0.54,0.33,72,75,34,0.25,"RISK_OFF",63,62,67,55,73,65,"ESZ26_above_7500","ESZ26_futures","partially_verified"],
    ["2026-11-21","20261121_NASDAQ_SELL_PULLBACK","NASDAQ","SELL","B","PULLBACK",25100,25700,27500,22000,21000,1.619,0.55,0.39,75,78,32,0.25,"RISK_OFF",64,64,69,56,74,66,"NQZ26_above_27500","NQZ26_futures","partially_verified"],
    ["2026-11-21","20261121_DXY_NONE_NO_TRADE","DXY","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,53,49,70,null,"MIXED",50,53,49,45,57,54,"DXY_reversal_unconfirmed","DXY_index","partially_verified"],
    ["2026-11-21","20261121_US10Y_NONE_NO_TRADE","US10Y","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,52,48,73,null,"MIXED",49,50,47,43,54,52,"US10Y_yield_direction_unconfirmed","US10Y_yield_pct","partially_verified"],
    ["2026-11-21","20261121_VIX_NONE_NO_TRADE","VIX","NONE","NO_TRADE","NO_TRADE",null,null,null,null,null,null,null,null,55,52,80,null,"EVENT",47,48,45,42,58,50,"VIX_spike_reversal_unconfirmed","VIX_index","partially_verified"]
  ]
}
```

### 記録検査

- 10資産：10行
- CSV：全行28列、カンマ27個
- JSON：全行28要素
- A級：0件
- B級：5件
- NO\_TRADE：5件
- RR：Entry中点から再計算済み
- GOLD：COMEX 2026年12月限を基準
- 未解決：GOLD提供元価格差、ATR10完全照合、USDJPY前回invalidation

**今回の主要な観察結果は、NASDAQを中心とするリスクオフの加速と、USDJPYの方向判断の転換である。** 10資産の日次記録を継続し、前日の方向あり5件についても個別のinvalidation判定を残した。
