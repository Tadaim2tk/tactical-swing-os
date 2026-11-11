<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-29 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-29T20:04:32Z / chars: 19829 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-09-29

**使用モデル：GPT-5.6 Sol**  
**本日の市場の主役：US10Y**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**データ基準：2026年9月28日米国市場終了後〜9月29日06:59 JST。先物は取引所遅延値・日足確定近似を含む。**

**crypto_grounds: etf=有, cme=有** — ETFは9月25日までの確定値を使用。9月28日分はこのレポート時点で十分な確定確認が取れていません。CME Bitcoin Futuresは9月28日データを確認済みです。先週のBTC ETFは5営業日で約+2.39Bドルでした。citeturn446456search2turn397286search3

**expected_r_basis: subjective** — 新規方向シグナルは0件。既存`20260924_BTC_BUY_PULLBACK`の発行時`expected_r=0.40`は固定したままです。現在の管理では「5営業日の時間切れ接近」「US10Y上昇」「ETF流入に対するBTC価格反応の弱さ」「実測MAE拡大」を下方要因として扱います。

**invalidation_check: 20260924_BTC_BUY_PULLBACK=not_fired**

BTC/USDの9月28日安値は取得系列で**82600.3ドル**。SLの82500には約100ドル届かず、CME Bitcoin Futuresの日足安値も**83827ドル**で83000を割っていません。したがって、事前定義した価格失効条件も複合失効条件も現時点では成立していません。citeturn365845search1turn397286search3

---

## 1. 本日の結論

**新規A級：0件**  
**新規B級：0件**  
**既存B：BTC BUY_PULLBACK — 継続、ただしほぼSL圏**  
**新規実取引：NO_TRADE**

昨日まで観察していた「5%超の米金利でも株が耐える」という構造は、**9月28日に明確に弱まりました**。

米10年債利回りは約**5.24%**まで上昇し、2007年以来の高水準。ESZ26は**7739.50（-0.57%）**、NQZ26は**30598.75（-0.81%）**、VIXは**16.09（+8.2%）**へ上昇しました。現物S&P500も約-0.77%、Nasdaq Compositeも約-0.92%です。citeturn169198news0turn954509search4turn954509search3turn588219search5

さらにGCZ26は約**4165～4167ドル**まで急落し、日中安値**4143.3**。同一12月限で前営業日4321.2から約3.6%近い下落です。これは「金利高を無視できる市場」ではなくなったことを示します。データ提供元の取得時点差で終値が数ドルずれるためGoldは`partially_verified`とします。citeturn588219search2turn588219search6

既存BTCはさらに厳しくなりました。9月28日安値82600.3はSL82500の**わずか約100ドル上**です。発行時Entry中点84200からの実測MAEは、

\[
(84200-82600.3)/(84200-82500)
=0.94R
\]

まで拡大しました。

発行時想定MAEは0.29Rでしたから、**今回はMAE予測を約3倍過小評価した**ことになります。

それでも82500そのものは割っていないので`fired`とはしません。

管理は、

**追加BUYなし / SL82500維持 / SLを広げない / 9月30日時間決済維持**

です。

発行時win_prob 0.55は記録上変更しませんが、**現在地点から「SLより先にTP1へ到達する」管理参考確率は約0.30**まで低下したと見ます。

---

## 2. 前回判断の簡易検証

### `20260924_BTC_BUY_PULLBACK`

発行値：

**Entry：83800–84600**  
**Mid：84200**  
**SL：82500**  
**TP1：87400**  
**TP2：90200**  
**RR：1.88**  
**win_prob：0.55**  
**expected_r：0.40**

9月28日のBTC/USDは、

**Open 84466.4  
High 84992.4  
Low 82600.3  
Close系 83045前後**

でした。citeturn365845search1

CME Bitcoin Futuresは、

**Open 84887  
High 85445  
Low 83827  
Close 83925**

の系列を確認しています。citeturn397286search3

したがって経路は、

**ENTRY_REACHED  
→ MAE拡大  
→ 85k再突破失敗  
→ 83k方向へ下落  
→ SL_NOT_REACHED  
→ TP1_NOT_REACHED  
→ not_fired**

です。

特に重要なのは、先週BTC ETFに約**23.9億ドル**が流入したにもかかわらず、BTCが87kから83kへ戻っている点です。ETFフローは9月21日の約999Mドルから、714.7M、346.9M、190.7M、134.5Mへ日ごとに減速しました。citeturn446456search2turn446456search12

したがって前日までの

**strong flow / weak price response**

という警戒は、今日はさらに強まりました。

---

## 3. 市場全体の前提

本日の総合regimeは**EVENT寄りのMIXED**です。

最大の原因はUS10Yです。

Reutersによれば9月28日の米10年債利回りは約**5.24%**、30年債も2004年以来の高水準へ上昇。10月のFed追加利上げ確率も約70%まで上がっています。原油高への懸念がインフレ・金利経路を再び押し上げました。citeturn169198news0turn169198news6

WTIは朝方、米国・イラン関係悪化を受けて4ドル超急騰しました。しかしQatar仲介による協議期待で上昇の大半を吐き出し、最終的には**92.60ドル、+0.19ドル**で清算しました。これは強い**failed breakout**です。citeturn610379search1

DXYは約**101.14**で大きくは動かず。USDJPYは日中**156.52–157.86**、日足終値系では**156.90**でした。先週の159円近辺からの円高が継続し、以前設定した「156.5割れで円高regime再評価」の水準にほぼ到達していますが、明確には割っていません。citeturn588219search1turn169198search16

Goldはかなり弱い。GCZ26は約4166、安値4143。高金利・Fed引き締め観測への感応度が一気に戻りました。citeturn588219search2

Cryptoもrisk-onとは言いにくく、BTCは約83.0k、ETHは約2649。ETH Futuresも9月28日は約2667前後でした。citeturn365845search1turn365845search3turn954509search2

本日以降は**9月29日JOLTS、9月30日PCE、週末の雇用統計**が、US10Y→DXY→NQ/SPX→BTC/Goldの順に波及する可能性があります。Reutersも今週の主要指標としてこれらを挙げています。citeturn169198news0

urlReuters：9月28日の米株・金利市場turn169198news0  
urlReuters：9月28日のWTI清算と米イラン協議turn610379search1  
urlCME：Bitcoin Futuresturn954509search7

---

## 4. 10資産別判断

| 資産 | 判断 | 評価 |
|---|---|---|
| **GOLD** | **NO_TRADE** | GCZ26約4166、安値4143。下方向は明確だが3%超急落後なのでSELL追随禁止。 |
| **BTC** | **既存B継続 / 新規NO_TRADE** | 約83045、安値82600。SL82500目前。`not_fired`だが品質低下。 |
| **ETH** | **NO_TRADE** | 約2649。BTCより相対的に弱く、risk-on重複を避ける。 |
| **WTI** | **NO_TRADE** | 92.60。朝方急騰をほぼ全戻し。ニュース二方向リスクが大きい。 |
| **USDJPY** | **NO_TRADE** | 約156.90、安値156.52。156.5割れ未確認。 |
| **SPX** | **NO_TRADE** | ESZ26 7739.50。高金利耐性が弱まり始めたがSELL追随するほどではない。 |
| **NASDAQ** | **NO_TRADE** | NQZ26 30598.75。昨日までのBUY候補帯を下抜け気味、金利条件も悪化。 |
| **DXY** | **NO_TRADE** | 約101.14。高金利の割に上値加速なし。 |
| **US10Y** | **NO_TRADE** | 約5.24%。市場の主役だが5.25直前を追わない。 |
| **VIX** | **NO_TRADE** | 16.09。risk repricing開始だが17～18の明確なrisk-off域には未到達。 |

ESZ26は9月28日**7739.50、安値7726.25**、NQZ26は**30598.75、安値30537.75**でした。citeturn954509search4turn954509search3

VIXは前営業日14.87から**16.09**へ上昇しました。citeturn588219search5

---

## 5. A級候補

**なし。**

昨日まではNASDAQ BUY_PULLBACKが次候補でしたが、今日は見送ります。

予定していた押し目帯は**30650–30750**でした。しかしNQZ26は安値30537.75まで落ち、終値30598.75。しかも同時に、

**US10Y 5.24%  
VIX 16.09  
Gold急落  
BTC下落**

が起きています。

これは「健全な押し目」ではなく、**マクロ条件悪化を伴う押し**です。

したがって昨日の価格帯だけを機械的に使ってNASDAQ BUYを出すのは誤りです。

新しいBUY条件は少なくとも、

**NQ >30650回復**  
＋
**US10Y <5.18**  
＋
**VIX <15.5**

まで待ちます。

---

## 6. B級監視候補

**新規B級：なし。**

既存1件のみです。

### `20260924_BTC_BUY_PULLBACK`

**Entry：83800–84600**  
**SL：82500**  
**TP1：87400**  
**TP2：90200**  
**RR：1.88**  
**発行時win_prob：0.55**  
**発行時expected_r：0.40**  
**risk_pct：0.25%**

現在：

**価格：約83.0k**  
**最悪値：約82600**  
**実測MAE：約0.94R**  
**残存SL余地：約100ドル（最悪値ベース）**

管理判断は**継続**ですが、これは「強い継続」ではありません。

実口座で約定している場合、

**82500をそのまま維持**します。

現在の位置でSLを82000や81000へ動かして「BTCだから広めに耐える」は禁止です。

また、9月30日が5営業日の時間決済期限です。TP1へ届かなくてもそこで閉じるという元ルールを維持します。

---

## 7. 触らない資産

特に**GOLD、US10Y、WTI、NASDAQ**です。

GoldはSELL方向が正しく見えますが、GCZ26は1日で約150ドル下げています。ここからSELLすれば典型的なmomentum追随です。次は**4200–4230付近への戻り**があり、なおUS10Yが5.20%以上ならSELL_PULLBACKを検討できます。

US10Yも同様です。5.24%まで来たところから「まだ上がる」と追うのはRRが悪い。JOLTS/PCEで弱い数字が出れば数十bp単位の巻き戻し余地があります。

WTIはもっと不向きです。朝方4ドル以上上げて、清算では+0.19ドルしか残りませんでした。citeturn610379search1

NASDAQは昨日まで最有力BUY候補でしたが、**Entry帯へ来た理由が悪い**。これを見分けることが今回の重要な判断です。

---

## 8. 後日検証ポイント

### BTC

現在もっとも重要です。

**82500 → fired**  
**87400 → TP1**  
**90200 → TP2**  
**9月30日終値 → 時間決済**

今日の安値82600.3はSLまで約0.12%です。citeturn365845search1

明日までに、

**83kを回復・維持**
＋
**ETF流入再加速**
＋
**US10Y低下**

が起きなければ、今回のBUYは「機関フローを重視しすぎた」サンプルになる可能性が高まります。

逆に83k台から85kを即回復できれば、82600近辺が最後の売り吸収だった可能性が残ります。

### GOLD

**GCZ26 4143**が直近安値。

**4140割れ**
なら下落継続。

ただしここからSELLはせず、

**4200–4230への戻り失速**
を次のSELL候補として観察します。

**4250超回復**
なら、今回の急落が一時的な金利ショックだった可能性を上げます。

### NASDAQ

NQZ26：

**30598.75**

新しい判定は、

**30650回復＋US10Y<5.18 → BUY再評価**  
**30300割れ＋VIX>17 → RISK_OFF強化**

です。

昨日までの「30650–30750に来れば買い」は撤回します。**価格だけではなく、そこへ来た理由を条件に戻します。**

### SPX

ES：

**7739.5**

**7700割れ**
なら高金利耐性仮説をかなり弱めます。

**7750～7780回復**
＋
**VIX<15.5**
なら、月曜の下落が短期調整だった可能性があります。

### USDJPY

9月28日安値**156.52**。citeturn169198search16

これは以前設定した156.5の境界までほぼ来ています。

**156.50を明確に割り、156前半で定着**
なら円高側の新規仮説を検討します。

**158超へ戻る**
なら高金利差が政策警戒を再度上回ったと判断。

今の156.9前後は中間地点です。

### WTI

9月28日は非常に良いObservationです。

**早朝：約+4ドル  
清算：92.60、+0.19**

でした。citeturn610379search1

つまり市場は地政学供給ショックを一度買ったものの、外交期待ですぐ売り戻しました。

今後、

**95–96を再び突破して維持**
しなければ、供給ショックBUYは弱い。

**91割れ**
なら再び供給正常化・外交期待優勢です。

---

## 9. Obsidian保存用 Observation Draft

```markdown
# 2026-09-29 Rates Finally Bite / BTC Near Invalidation

Model:
GPT-5.6 Sol

Market protagonist:
US10Y

Gold reference:
COMEX Dec-2026 / GCZ26

crypto_grounds:
etf=有
cme=有

expected_r_basis:
subjective

## Regime

EVENT / MIXED

## Main change

Previous observation:
US equities were unusually resilient despite US10Y >5.1%.

Sep28:
that resilience weakened.

US10Y:
~5.24%

ESZ26:
7739.50
-0.57%

NQZ26:
30598.75
-0.81%

VIX:
16.09
+8.2%

GCZ26:
~4166
low 4143.3
~3%+ daily decline

BTC:
~83045
low 82600.3

Interpretation:
higher yields are now transmitting into
Gold
equities
crypto
simultaneously.

## BTC active signal

20260924_BTC_BUY_PULLBACK

Entry:
83800-84600

Mid:
84200

SL:
82500

TP1:
87400

TP2:
90200

RR:
1.88

Issue win_prob:
0.55

Issue expected_r:
0.40

Sep28 spot:
close/reference ~83045
low 82600.3

Observed MAE:
~0.94R

Issue MAE estimate:
0.29R

Status:
ENTRY_REACHED
SL_NOT_REACHED
TP1_NOT_REACHED
not_fired

Current management:
do not add
do not widen SL
time exit Sep30

Current TP1-before-SL/time management probability:
~0.30
not written back to original LOG

## Flow-price divergence

BTC ETF Sep21-25:
~+2.39bn

Daily:
+999m
+714.7m
+346.9m
+190.7m
+134.5m

Despite large inflows:
BTC fell from >87k to ~83k.

Interpretation:
seller absorption is stronger than initially estimated.

ETF flow alone should receive less weight
unless price response confirms it.

## Nasdaq

Previous preferred pullback:
30650-30750

Sep28:
NQ low 30537.75
close 30598.75

But:
US10Y rose
VIX rose
Gold collapsed
BTC fell

Therefore:
this is NOT the benign pullback previously requested.

Do not issue BUY.

Requalification:
NQ >30650
US10Y <5.18
VIX <15.5

## Gold

GCZ26:
~4166
low 4143.3

Direction:
bearish

Execution:
NO_TRADE

Reason:
3%+ shock decline
do not chase

Next candidate:
SELL_PULLBACK only after rebound toward 4200-4230
with US10Y remaining >5.20.

## WTI

Settlement:
92.60

Intraday:
>4 dollar early rally largely reversed

Interpretation:
geopolitical premium failed to hold
because Qatar-mediated US-Iran talks remain possible.

Headline-driven.
NO_TRADE.

## USDJPY

Sep28:
close/reference 156.90
low 156.52

Previous regime-test:
156.50

Not cleanly broken yet.

<156.50 and hold:
yen-strength regime candidate

>158:
yield-differential control returns

## Active invalidation

20260924_BTC_BUY_PULLBACK=not_fired

## New signals

A:
NONE

B:
NONE

Existing:
BTC BUY_PULLBACK active

#TSO #US10Y #BTC #GOLD #NASDAQ #WTI #USDJPY
```

---

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-29,20260929_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,96,96,,EVENT,98,99,99,96,94,99,do_not_chase_sell_after_3pct_drop_wait_for_rebound_4200_4230_or_reclaim_4250_with_US10Y_confirmation,GCZ26_4143_4166_4200_4230_4250_US10Y_DXY_1d_3d,partially_verified
2026-09-29,20260929_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,98,74,,EVENT,90,96,99,95,91,96,manage_existing_20260924_BUY_SL82500_TP87400_not_fired_no_add_time_exit_20260930,BTC_82500_82600_83000_83045_87400_CME_ETF_US10Y_1d_2d,partially_verified
2026-09-29,20260929_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,89,91,,EVENT,85,93,98,87,85,92,wait_for_ETH_hold_2600_or_reclaim_2700_with_BTC_US10Y_confirmation,ETH_2600_2638_2649_2700_CME_BTC_US10Y_1d_3d,partially_verified
2026-09-29,20260929_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,96,98,,EVENT,97,99,99,95,94,99,failed_early_breakout_wait_for_WTI_hold_above_95_or_break_below_91_before_new_signal,WTI_91_92.60_95_96_USIran_Qatar_Hormuz_1d_3d,verified
2026-09-29,20260929_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,95,94,,EVENT,93,98,99,94,91,98,wait_for_clean_break_below_156.5_or_reclaim_above_158_before_new_direction_signal,USDJPY_156.5_156.52_156.90_158_MOF_US10Y_DXY_1d_3d,verified
2026-09-29,20260929_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,95,91,,EVENT,91,97,99,92,90,98,high_rate_resilience_weakened_wait_for_ES_reclaim_7750_7780_or_break_below_7700_with_VIX,ESZ26_7700_7726.25_7739.50_7750_7780_US10Y_VIX_1d_3d,verified
2026-09-29,20260929_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,97,90,,EVENT,92,97,99,94,92,98,previous_pullback_condition_invalidated_by_macro_wait_for_NQ_above_30650_with_US10Y_below_5.18_or_break_30300,NQZ26_30300_30537.75_30598.75_30650_US10Y_VIX_1d_3d,verified
2026-09-29,20260929_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,91,89,,MIXED,88,95,98,88,87,96,wait_for_DXY_hold_above_101.3_or_break_below_100.7_with_US10Y_confirmation,DXY_100.7_100.98_101.14_101.3_US10Y_USDJPY_1d_3d,verified
2026-09-29,20260929_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,99,96,,EVENT,99,99,99,98,98,99,do_not_chase_5.24_wait_for_sustained_break_above_5.25_or_rejection_below_5.15_after_JOLTS_PCE,US10Y_5.15_5.24_5.25_JOLTS_PCE_NQ_GOLD_1d_3d,verified
2026-09-29,20260929_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,92,91,,EVENT,89,95,98,89,88,95,wait_for_VIX_break_above_17_or_return_below_15.5_with_ES_NQ_confirmation,VIX_15.5_16.09_16.43_17_ES_NQ_US10Y_1d_3d,verified
```

### TSO_LOG JSON

```json
[
  {
    "date":"2026-09-29",
    "signal_id":"20260929_GOLD_NONE_NO_TRADE",
    "asset":"GOLD",
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
    "tq_score":99,
    "opp_score":96,
    "no_trade_score":96,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":98,
    "ffs":99,
    "cds":99,
    "ias":96,
    "cbs":94,
    "mes":99,
    "invalidation":"do_not_chase_sell_after_3pct_drop_wait_for_rebound_4200_4230_or_reclaim_4250_with_US10Y_confirmation",
    "verification_target":"GCZ26_4143_4166_4200_4230_4250_US10Y_DXY_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-09-29",
    "signal_id":"20260929_BTC_NONE_NO_TRADE",
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
    "tq_score":99,
    "opp_score":98,
    "no_trade_score":74,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":90,
    "ffs":96,
    "cds":99,
    "ias":95,
    "cbs":91,
    "mes":96,
    "invalidation":"manage_existing_20260924_BUY_SL82500_TP87400_not_fired_no_add_time_exit_20260930",
    "verification_target":"BTC_82500_82600_83000_83045_87400_CME_ETF_US10Y_1d_2d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-09-29",
    "signal_id":"20260929_ETH_NONE_NO_TRADE",
    "asset":"ETH",
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
    "tq_score":98,
    "opp_score":89,
    "no_trade_score":91,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":85,
    "ffs":93,
    "cds":98,
    "ias":87,
    "cbs":85,
    "mes":92,
    "invalidation":"wait_for_ETH_hold_2600_or_reclaim_2700_with_BTC_US10Y_confirmation",
    "verification_target":"ETH_2600_2638_2649_2700_CME_BTC_US10Y_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-09-29",
    "signal_id":"20260929_WTI_NONE_NO_TRADE",
    "asset":"WTI",
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
    "tq_score":99,
    "opp_score":96,
    "no_trade_score":98,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":97,
    "ffs":99,
    "cds":99,
    "ias":95,
    "cbs":94,
    "mes":99,
    "invalidation":"failed_early_breakout_wait_for_WTI_hold_above_95_or_break_below_91_before_new_signal",
    "verification_target":"WTI_91_92.60_95_96_USIran_Qatar_Hormuz_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-29",
    "signal_id":"20260929_USDJPY_NONE_NO_TRADE",
    "asset":"USDJPY",
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
    "tq_score":99,
    "opp_score":95,
    "no_trade_score":94,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":93,
    "ffs":98,
    "cds":99,
    "ias":94,
    "cbs":91,
    "mes":98,
    "invalidation":"wait_for_clean_break_below_156.5_or_reclaim_above_158_before_new_direction_signal",
    "verification_target":"USDJPY_156.5_156.52_156.90_158_MOF_US10Y_DXY_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-29",
    "signal_id":"20260929_SPX_NONE_NO_TRADE",
    "asset":"SPX",
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
    "tq_score":99,
    "opp_score":95,
    "no_trade_score":91,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":91,
    "ffs":97,
    "cds":99,
    "ias":92,
    "cbs":90,
    "mes":98,
    "invalidation":"high_rate_resilience_weakened_wait_for_ES_reclaim_7750_7780_or_break_below_7700_with_VIX",
    "verification_target":"ESZ26_7700_7726.25_7739.50_7750_7780_US10Y_VIX_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-29",
    "signal_id":"20260929_NASDAQ_NONE_NO_TRADE",
    "asset":"NASDAQ",
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
    "tq_score":99,
    "opp_score":97,
    "no_trade_score":90,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":92,
    "ffs":97,
    "cds":99,
    "ias":94,
    "cbs":92,
    "mes":98,
    "invalidation":"previous_pullback_condition_invalidated_by_macro_wait_for_NQ_above_30650_with_US10Y_below_5.18_or_break_30300",
    "verification_target":"NQZ26_30300_30537.75_30598.75_30650_US10Y_VIX_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-29",
    "signal_id":"20260929_DXY_NONE_NO_TRADE",
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
    "tq_score":99,
    "opp_score":91,
    "no_trade_score":89,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":88,
    "ffs":95,
    "cds":98,
    "ias":88,
    "cbs":87,
    "mes":96,
    "invalidation":"wait_for_DXY_hold_above_101.3_or_break_below_100.7_with_US10Y_confirmation",
    "verification_target":"DXY_100.7_100.98_101.14_101.3_US10Y_USDJPY_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-29",
    "signal_id":"20260929_US10Y_NONE_NO_TRADE",
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
    "tq_score":99,
    "opp_score":99,
    "no_trade_score":96,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":99,
    "ffs":99,
    "cds":99,
    "ias":98,
    "cbs":98,
    "mes":99,
    "invalidation":"do_not_chase_5.24_wait_for_sustained_break_above_5.25_or_rejection_below_5.15_after_JOLTS_PCE",
    "verification_target":"US10Y_5.15_5.24_5.25_JOLTS_PCE_NQ_GOLD_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-29",
    "signal_id":"20260929_VIX_NONE_NO_TRADE",
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
    "tq_score":99,
    "opp_score":92,
    "no_trade_score":91,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":89,
    "ffs":95,
    "cds":98,
    "ias":89,
    "cbs":88,
    "mes":95,
    "invalidation":"wait_for_VIX_break_above_17_or_return_below_15.5_with_ES_NQ_confirmation",
    "verification_target":"VIX_15.5_16.09_16.43_17_ES_NQ_US10Y_1d_3d",
    "verified_status":"verified"
  }
]
```

今日の最大の更新は2点です。**BTCが82500のSLまで約100ドルに迫ったこと**、そして**US10Yが5.24%へ上昇したことで、これまで観察していた株式の「高金利耐性」が実際に弱まり始めたこと**です。

昨日まで候補だったNASDAQの押し目BUYを今日は出さないことも重要です。価格は狙っていた水準へ来ましたが、**押しの理由が「健全な利益確定」ではなく金利・VIX・Gold・Cryptoを伴うマクロ悪化に変わった**ためです。
