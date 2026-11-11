<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-24 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-26T09:12:02Z / chars: 20779 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-09-24

**使用モデル：GPT-5.6 Sol**  
**本日の市場の主役：US10Y**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**データ基準：2026年9月23日米国市場終了後〜9月24日07:00 JST前後。ES/NQ/VIXの一部は遅延値。**

**crypto_grounds: etf=有, cme=有** — BTC現物ETFは最新の確定性が高い9月22日分で**+714.7Mドル**、4営業日連続流入。9月23日分についても+609Mドル前後の暫定集計がありますが、今回は正式スコアには使っていません。CME BTCは9月23日に**84487.5、安値83575**まで調整しました。citeturn404541search0turn404541search1turn233070search0

**expected_r_basis: subjective** — 本日のBTC BUYは二点分布なら約`+0.58R`ですが、US10Yの5.10%超、Trump–Xi会談、直近急騰後のレバレッジ解消、ETF確定値の1日遅れを織り込み、`expected_r=0.40`まで下げています。

**invalidation_check: 20260924_BTC_BUY_PULLBACK=not_fired**

**resolved_today: 20260922_SPX_BUY_PULLBACK=fired, 20260919_USDJPY_BUY_PULLBACK=target_before_entry**

9月23日は市場の前提が再び変わりました。米Flash Composite PMIは**58.4**と2021年7月以来の高水準となり、米10年債利回りは一時**5.106%**まで上昇。S&P500は-0.75%、Nasdaq現物は-1.13%となり、Fedの10月利上げ確率もReuters集計で71%まで上昇しました。citeturn779792view0turn361956search0turn361956search1

一方、WTIはイラン情勢を受けて**92.16ドル、+1.81%**へ反発。Gold Decemberは**4318.40ドル、-1.3%**。つまり昨日までの「原油安＋金利低下＋Growth上昇」という組み合わせは崩れ、今日は再び**原油・金利・ドルが株式へ圧力をかける構造**です。citeturn369391search3turn652831search0

urlReuters：9月23日の米株・金利市場turn813956news0  
urlReuters：9月24日のTrump–Xi会談の主要論点turn813956news13  
urlReuters：9月23日のGold市場turn652831search0  
urlReuters：9月23日のWTI市場turn369391search3

---

## 1. 本日の結論

**新規A級：0件**

**新規B級：1件 — BTC BUY_PULLBACK**

**B+観察候補：BTC BUY_PULLBACK。ただしXM実損3,000円確認が条件**

**既存方向判断：0件。SPXとUSDJPYは本日までに解決**

残り9資産は**新規NO_TRADE**です。

今日のBTCは、昨日まで待っていた押し目条件が実際に来ました。

BTC/USD現物は9月23日に**83.5k付近まで下落した後、84.2–84.6k付近**。CMEも安値83575、終値84487.5です。これは昨日設定していた「84.0–84.8kまで押してETF/CMEが崩れないなら再評価」という地点そのものです。citeturn249266search1turn249266search2turn233070search0

そこで新規：

**`20260924_BTC_BUY_PULLBACK`**

**Entry：83800–84600**  
**中点：84200**  
**SL：82500**  
**TP1：87400**  
**TP2：90200**

RRは、

\[
(87400-84200)/(84200-82500)
=3200/1700
=1.88
\]

**win_prob：0.55**  
**expected_r：0.40**  
**MAE想定：約0.29R**  
**risk_pct：0.25%**

A級ではありません。最大の理由は**US10Y 5.106%**と本日のTrump–Xi首脳会談です。

ただしBとしては十分に残す価値があります。

XM BTCUSDについて外部の実測仕様では**1lot=1BTC、最小0.01lot、通常スプレッド約40ドル**です。0.01lotなら、Entry中点84200→SL82500の価格損失は17ドル。USDJPY約158.3なら約2,690円、40ドルspreadを0.01lot分加えて概算**約2,750円＋slippage**です。citeturn135313search1turn135313search2turn369391search0

つまり**3,000円制約にかなり近い**。

したがって、

**XM端末上の実際のSL時損失見積もりが3,000円以内ならB+実行候補。3,000円を超えるなら実取引NO_TRADE**

とします。

---

## 2. 前回判断の簡易検証

### `20260922_SPX_BUY_PULLBACK` — FIRED

既存：

**Entry 7760–7780**  
**SL 7730**  
**TP1 7850**  
**TP2 7910**

9月23日のESZ26は、

**Open 7839.00  
High 7843.25  
Low 7758.75  
終盤約7770**

でした。

したがって**Entry帯7760–7780には到達**しています。価格SL7730までは落ちていません。citeturn836567search5

しかし、このシグナルのinvalidationは、

> `ESZ26_below_7730_or_US10Y_above_5.05_with_VIX_risk_repricing`

でした。

実際にUS10Yは**5.106%**まで上昇し、VIXもCboeの15:26 ET時点で14.58へ上昇、より遅い市場スナップショットでは**15.17、+6.76%**まで確認されています。citeturn361956search0turn836567search2turn369391search4

したがって、

**`20260922_SPX_BUY_PULLBACK=fired`**

です。

ここは重要です。

**SL7730を待つ前に、シナリオを支えていた「金利5%未満＋低VIX」という条件が崩れました。**

これは今回ユーザーがinvalidation欄で測ろうとしているもの、そのものです。

なお、Entry到達とUS10Y 5.05突破の正確な秒単位の順序までは今回確認できていないため、研究ログでは**ENTRY_TOUCHED / MACRO_INVALIDATION_FIRED**までを確定し、仮想P/Lは割り当てません。

---

### `20260919_USDJPY_BUY_PULLBACK` — TARGET BEFORE ENTRY

既存：

**Entry 156.00–156.50**  
**SL 155.20**  
**TP1 158.20**  
**TP2 159.60**

発行後の9月21日安値は156.57、22日安値156.82で、Entryには届きませんでした。

そして9月23日は、

**Open 157.46  
High 158.40  
Low 157.44  
Close 約158.32**

となり、Entry未到達のまま**TP1 158.20を先に突破**しました。citeturn369391search0

したがってこのシグナルは、

**方向仮説：成功**  
**実取引：未約定**  
**結果：TARGET_BEFORE_ENTRY**

で閉じます。

157～158円で後追いBUYしなかった運用も維持します。

---

## 3. 市場全体の前提

昨日までのrisk-on前提をそのまま使うのは危険です。

米Flash Composite PMI **58.4**は市場予想以上に強く、米10年債は4.95%付近から一時5.106%へ急騰。Reutersによれば10年債は2007年以来の高水準です。Fed Governor Barrも追加利上げが必要になる可能性を示しています。citeturn779792view0turn361956search1

株式側では、

**S&P500 -0.75%**  
**Nasdaq Composite -1.13%**  
**SOX -1.2%**

でした。citeturn779792view0

ただしNASDAQ参照系列は現物ではなくNQZ26です。

NQZ26は9月23日に、

**Open 約31008.5  
High 31094.75  
Low 30642.75  
終盤約30750**

まで調整しています。citeturn836567search6

つまり**NQも実際に下落しており、現物だけの現象ではありません。**

ドルも強いです。DXY現物系列は約**100.87–100.92**と2カ月近い高値圏。USDJPYも158.3台です。citeturn220613search0turn220613search2turn369391search0

Goldはこの組み合わせに弱く、GCZ26はReuters清算値で**4318.40**。現物金も約4283まで下落しました。citeturn652831search0

WTIは反対に上昇。イラン大統領が米国への降伏を否定し、Hormuz再開にも条件を付けているため地政学プレミアムが戻りました。一方、米原油在庫は約300万バレル増加しており、需給は一方向ではありません。WTI清算値は**92.16**です。citeturn369391search3

そして本日9月24日はTrump–Xi会談。Reutersによれば議題は**貿易休戦、AI、台湾、イラン**などです。citeturn813956news10turn813956news13

したがって総合評価は、

**EVENT / MIXED。昨日より明確に防御寄り**

です。

---

## 4. 10資産別判断

| 資産 | 本日判断 | 評価 |
|---|---|---|
| **GOLD** | **NO_TRADE** | GCZ26 4318.4。金利・ドル上昇で弱いが、急落後のSELLは追わない。 |
| **BTC** | **B BUY_PULLBACK / B+条件付き** | 約84.2–84.6k。ETF買い継続＋CME押し目。唯一の新規方向判断。 |
| **ETH** | **NO_TRADE** | spot約2665–2715。BTCより弱く、同一risk-on群を重複保有しない。 |
| **WTI** | **NO_TRADE** | 92.16。Iran強硬発言で反発したが在庫増・Saudi供給回復と矛盾。 |
| **USDJPY** | **NO_TRADE** | 158.32。旧BUYはtarget-before-entry。介入域に近づくため追わない。 |
| **SPX** | **NO_TRADE** | 旧BUYはmacro invalidation fired。新規BUYへ即再参加しない。 |
| **NASDAQ** | **NO_TRADE** | NQZ26約30750。金利ショック後の構造確認待ち。 |
| **DXY** | **NO_TRADE** | 約100.9。方向は上だが2カ月高値圏＋首脳会談。 |
| **US10Y** | **NO_TRADE** | 5.106%まで急騰。市場の主役だが上昇直後を追わない。 |
| **VIX** | **NO_TRADE** | 14.58～15.17。上昇したがまだパニック域ではない。 |

BTC現物は複数ソースで9月23日終盤**84.0–84.6k**、日中安値83.5k前後。CMEも84487.5で、現物/CMEの整合は十分です。citeturn249266search1turn249266search2turn233070search0

ETHは現物が9月23日に約-3%とBTC以上に弱く、CME/現物の時点差も大きいため`partially_verified`扱いとします。citeturn233070search3turn404541search2

---

## 5. A級候補

**なし。**

BTCは数値的にはAに近づいています。

RR：

\[
1.88
\]

win_prob：

\[
0.55
\]

二点分布EV：

\[
0.55\times1.88-0.45
=+0.584R
\]

しかしAにはしません。

理由は、

- US10Yが5.106%まで急騰
- Fed追加利上げ確率上昇
- Trump–Xi会談当日
- BTCは直前に81k→87kへ急騰した後
- 想定MAE ≈0.29RでA基準0.25R超過
- subjective expected_r=0.40でA基準0.45未満

です。

したがって**B止まり**です。

---

## 6. B級監視候補

### `20260924_BTC_BUY_PULLBACK` — B / 条件付きB+

**Entry：83800–84600**  
**Mid：84200**  
**SL：82500**  
**TP1：87400**  
**TP2：90200**  
**RR：1.88**  
**win_prob：0.55**  
**較正後参考値：0.57**  
**expected_r：0.40**  
**MAE想定：0.29R**  
**risk_pct：0.25%**

根拠は3つ。

第一に、BTC ETFは9月22日まで**4営業日連続プラス、同日+714.7Mドル**。買いは単なるshort squeezeだけではありません。citeturn404541search0turn404541search3

第二に、CMEも87k台から**83.575kまで正常な押し**が入り、84.5k付近まで戻しています。citeturn233070search0

第三に、昨日から指定していた84k近辺の押し目ゾーンへ実際に入っています。後から都合よくEntryを下げているわけではありません。

一方、無視できない弱材料は**US10Y 5.1%超**です。

したがって、

**82500を割る**
または
**CMEが83kを明確に失い、同時にETFフローが反転**

すればinvalidation。

5営業日の時間決済期限は**9月30日**です。

XMについては0.01lot時のSL実損が概算約2,750円＋slippageなので、**実端末表示で3,000円以下を確認できた場合だけB+実行候補**です。少しでも超えるなら研究シグナルはBのまま残し、**実取引NO_TRADE**とします。citeturn135313search2

---

## 7. 触らない資産

今日は特に**US10Y、NASDAQ、USDJPY、WTI**を追いません。

US10Yは方向こそ上ですが、1日で約15bp上昇して5.106%。ここから利回り上昇へ追随すると、PMIショックを一番悪い位置で追う可能性があります。

NASDAQは反対に「押したから買う」と即断しません。NQZ26が30600台まで下げたのは、単なる利益確定ではなく**金利ショック**を伴っています。次の24時間でUS10Yが5.05を下回るかどうかを見ます。

USDJPYも158.3。旧BUY仮説自体は正しかったですが、EntryなしでTPへ到達した以上、今から買えば完全な後追いです。

WTIも92.16まで反発しましたが、Iran強硬発言と米在庫増、Saudi代替供給という相反材料が同時にあります。BUY/SELLどちらにも現在は十分な非対称性がありません。citeturn369391search3

---

## 8. 後日検証ポイント

### BTC

今回の中心です。

**83800–84600：Entry帯**  
**82500：SL / price invalidation**  
**87400：TP1**  
**90200：TP2**

特に、

**BTC 83–84k維持**
＋
**US10Yが5.05以下へ戻る**
＋
**ETFフローがプラス継続**

ならBUY仮説はかなり改善します。

反対にBTCが82500へ落ちる前でも、

**US10Y >5.15**
＋
**NQ <30500**
＋
**BTC ETFフロー反転**

が同時発生すれば早期invalidation候補です。

### SPX

昨日のシグナルはもう閉じています。

次の重要な観察は、

**ESが7700前後を守れるか**

です。

5.1%金利でも7700を維持するなら、株の金利耐性はまだ残っています。

### NASDAQ

**NQ 30500–30600**

を支持できるか。

ここを守り、US10Yが5.05以下へ戻ればBUY再検討。

**NQ <30200**
ならrisk-on仮説をさらに弱めます。

### USDJPY

旧シグナルは終了。

今後は、

**159～160接近時の日本当局対応**

が中心です。

158円台から新規BUYは作りません。

### GOLD

**4300前後**が重要。

金利5.1%にもかかわらず4300を守るなら、Goldは強気候補へ戻せます。

**4290割れ＋DXY>101**
ならSELL優勢ですが、その時も急落追随は避けます。

### WTI

**92.16**。

**94超へ続伸**
ならIran/Hormuzプレミアム再拡大。

**90割れ**
ならSaudi供給回復・在庫増が再び勝っていると判断。

現時点では中央にいるので触りません。

---

## 9. Obsidian保存用 Observation Draft

```markdown
# 2026-09-24 Hot PMI / US10Y Shock / BTC Pullback

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
defensive shift

## Main macro shock

US Flash Composite PMI:
58.4

Highest:
since Jul 2021

US10Y:
high 5.106%

Fed Oct hike probability:
~71%

Market response:

S&P500:
-0.75%

Nasdaq Composite:
-1.13%

NQZ26:
high ~31095
low ~30643
late ~30750

DXY:
~100.9

USDJPY:
158.32

VIX:
14.58 Cboe delayed
~15.17 later snapshot

## Gold

GCZ26 / Dec settlement:
4318.40

Drivers:
higher yields
stronger USD
hawkish Fed

Do not chase SELL.

## WTI

WTI:
92.16
+1.81%

Bullish:
Iran refuses surrender
Hormuz conditions remain

Bearish:
US crude inventories +3.0m barrels
Saudi / Iraq alternative supply improving

Result:
NO_TRADE

## Resolved signals

### SPX

20260922_SPX_BUY_PULLBACK

Entry:
7760-7780

Sep23 ES:
low 7758.75

Entry zone:
TOUCHED

SL:
7730 not reached

Macro invalidation:
US10Y >5.05
+
VIX repricing

Result:
FIRED

Important:
entry-vs-invalidation intraday ordering not fully verified
do not assign synthetic P/L

### USDJPY

20260919_USDJPY_BUY_PULLBACK

Entry:
156.00-156.50

Sep21 low:
156.57

Sep22 low:
156.82

Sep23:
high 158.40

TP1:
158.20

Result:
TARGET_BEFORE_ENTRY

Direction:
correct

Execution:
no trade

Remove from active list.

## New BTC signal

20260924_BTC_BUY_PULLBACK

Rank:
B

Conditional B+:
YES

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

win_prob:
0.55

calibrated reference:
0.57

raw two-point EV:
~0.58R

subjective expected_r:
0.40R

MAE:
~0.29R

Risk:
0.25%

Reasons:
BTC returned into previously-defined 84k pullback zone
CME low 83575 / close 84487.5
BTC ETF Sep22 +714.7m
four consecutive positive ETF sessions

Headwinds:
US10Y 5.106
Fed tightening repricing
Trump-Xi summit today
post-squeeze volatility

XM:
BTCUSD contract size 1 BTC
minimum lot 0.01
approx standard spread ~$40

Estimated loss:
~JPY2750 before slippage

Execution:
only if platform-estimated SL loss <= JPY3000

Invalidation:
BTC <82500
OR CME loses 83000 together with ETF-flow reversal

Time exit:
2026-09-30 close

## Trump-Xi

Date:
2026-09-24

Agenda:
trade truce
AI
Taiwan
Iran

Do not stack correlated risk-on longs.

## Active invalidation

20260924_BTC_BUY_PULLBACK=not_fired

## New signals

A:
NONE

B:
BTC BUY_PULLBACK

B+:
BTC BUY_PULLBACK conditional on real XM loss <= JPY3000

#TSO #BTC #US10Y #NASDAQ #SPX #USDJPY #WTI
```

---

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-24,20260924_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,88,90,,MIXED,86,93,98,85,86,91,wait_for_GCZ26_reclaim_4360_or_break_4290_after_rate_shock_without_chasing,GCZ26_4290_4318.40_4360_DXY_US10Y_1d_3d,verified
2026-09-24,20260924_BTC_BUY_PULLBACK,BTC,BUY,B,PULLBACK,83800,84600,82500,87400,90200,1.88,0.55,0.40,99,90,55,0.25,EVENT,78,90,96,88,84,86,BTC_below_82500_or_CME_loss_of_83000_with_ETF_flow_reversal,BTC_82500_83800_84600_87400_90200_ETF_CME_US10Y_1d_3d_5d,partially_verified
2026-09-24,20260924_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,84,88,,MIXED,74,88,94,82,80,82,prefer_BTC_expression_wait_for_ETH_hold_2600_or_reclaim_2750_with_ETF_CME_confirmation,ETH_2600_2665_2750_2800_ETF_CME_1d_3d,partially_verified
2026-09-24,20260924_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,92,91,,EVENT,90,98,99,90,90,96,wait_for_WTI_break_above_94_or_below_90_after_Iran_inventory_conflict,WTI_90_92.16_94_Hormuz_Iran_EIA_1d_3d,verified
2026-09-24,20260924_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,92,91,,EVENT,88,96,99,92,88,96,previous_20260919_target_before_entry_do_not_chase_158_area_wait_for_new_structure,USDJPY_157_158.32_159_160_MOF_DXY_US10Y_1d_3d,verified
2026-09-24,20260924_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,93,96,,EVENT,90,97,99,91,90,97,previous_20260922_BUY_fired_on_US10Y_above_5.05_with_VIX_repricing_wait_for_new_structure,ESZ26_7700_7758.75_7770_US10Y_VIX_1d_3d,partially_verified
2026-09-24,20260924_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,90,90,,MIXED,86,94,98,89,88,94,wait_for_NQZ26_hold_30500_30600_or_break_below_30200_after_rate_shock,NQZ26_30200_30500_30600_30750_US10Y_VIX_1d_3d,verified
2026-09-24,20260924_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,91,88,,EVENT,90,95,98,89,89,95,wait_for_DXY_hold_above_101_or_failure_below_100.4_after_USChina_event,DXY_100.4_100.9_101_US10Y_USDJPY_TrumpXi_1d_3d,partially_verified
2026-09-24,20260924_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,96,92,,EVENT,99,99,99,96,97,99,do_not_chase_5.106_spike_wait_for_hold_above_5.15_or_rejection_below_5.00,US10Y_5.00_5.106_5.15_NQ_SPX_GOLD_DXY_1d_3d,verified
2026-09-24,20260924_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,86,90,,EVENT,82,92,97,84,84,90,wait_for_VIX_hold_above_16_or_return_below_14.5_after_rate_repricing,VIX_14.5_14.58_15.17_16_ES_NQ_1d_3d,partially_verified
```

### TSO_LOG JSON

```json
[
  {
    "date":"2026-09-24",
    "signal_id":"20260924_GOLD_NONE_NO_TRADE",
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
    "opp_score":88,
    "no_trade_score":90,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":86,
    "ffs":93,
    "cds":98,
    "ias":85,
    "cbs":86,
    "mes":91,
    "invalidation":"wait_for_GCZ26_reclaim_4360_or_break_4290_after_rate_shock_without_chasing",
    "verification_target":"GCZ26_4290_4318.40_4360_DXY_US10Y_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-24",
    "signal_id":"20260924_BTC_BUY_PULLBACK",
    "asset":"BTC",
    "side":"BUY",
    "rank":"B",
    "type":"PULLBACK",
    "entry_low":83800,
    "entry_high":84600,
    "sl":82500,
    "tp1":87400,
    "tp2":90200,
    "rr":1.88,
    "win_prob":0.55,
    "expected_r":0.40,
    "tq_score":99,
    "opp_score":90,
    "no_trade_score":55,
    "risk_pct":0.25,
    "regime":"EVENT",
    "ems":78,
    "ffs":90,
    "cds":96,
    "ias":88,
    "cbs":84,
    "mes":86,
    "invalidation":"BTC_below_82500_or_CME_loss_of_83000_with_ETF_flow_reversal",
    "verification_target":"BTC_82500_83800_84600_87400_90200_ETF_CME_US10Y_1d_3d_5d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-09-24",
    "signal_id":"20260924_ETH_NONE_NO_TRADE",
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
    "opp_score":84,
    "no_trade_score":88,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":74,
    "ffs":88,
    "cds":94,
    "ias":82,
    "cbs":80,
    "mes":82,
    "invalidation":"prefer_BTC_expression_wait_for_ETH_hold_2600_or_reclaim_2750_with_ETF_CME_confirmation",
    "verification_target":"ETH_2600_2665_2750_2800_ETF_CME_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-09-24",
    "signal_id":"20260924_WTI_NONE_NO_TRADE",
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
    "opp_score":92,
    "no_trade_score":91,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":90,
    "ffs":98,
    "cds":99,
    "ias":90,
    "cbs":90,
    "mes":96,
    "invalidation":"wait_for_WTI_break_above_94_or_below_90_after_Iran_inventory_conflict",
    "verification_target":"WTI_90_92.16_94_Hormuz_Iran_EIA_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-24",
    "signal_id":"20260924_USDJPY_NONE_NO_TRADE",
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
    "opp_score":92,
    "no_trade_score":91,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":88,
    "ffs":96,
    "cds":99,
    "ias":92,
    "cbs":88,
    "mes":96,
    "invalidation":"previous_20260919_target_before_entry_do_not_chase_158_area_wait_for_new_structure",
    "verification_target":"USDJPY_157_158.32_159_160_MOF_DXY_US10Y_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-24",
    "signal_id":"20260924_SPX_NONE_NO_TRADE",
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
    "opp_score":93,
    "no_trade_score":96,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":90,
    "ffs":97,
    "cds":99,
    "ias":91,
    "cbs":90,
    "mes":97,
    "invalidation":"previous_20260922_BUY_fired_on_US10Y_above_5.05_with_VIX_repricing_wait_for_new_structure",
    "verification_target":"ESZ26_7700_7758.75_7770_US10Y_VIX_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-09-24",
    "signal_id":"20260924_NASDAQ_NONE_NO_TRADE",
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
    "opp_score":90,
    "no_trade_score":90,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":86,
    "ffs":94,
    "cds":98,
    "ias":89,
    "cbs":88,
    "mes":94,
    "invalidation":"wait_for_NQZ26_hold_30500_30600_or_break_below_30200_after_rate_shock",
    "verification_target":"NQZ26_30200_30500_30600_30750_US10Y_VIX_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-24",
    "signal_id":"20260924_DXY_NONE_NO_TRADE",
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
    "no_trade_score":88,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":90,
    "ffs":95,
    "cds":98,
    "ias":89,
    "cbs":89,
    "mes":95,
    "invalidation":"wait_for_DXY_hold_above_101_or_failure_below_100.4_after_USChina_event",
    "verification_target":"DXY_100.4_100.9_101_US10Y_USDJPY_TrumpXi_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-09-24",
    "signal_id":"20260924_US10Y_NONE_NO_TRADE",
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
    "opp_score":96,
    "no_trade_score":92,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":99,
    "ffs":99,
    "cds":99,
    "ias":96,
    "cbs":97,
    "mes":99,
    "invalidation":"do_not_chase_5.106_spike_wait_for_hold_above_5.15_or_rejection_below_5.00",
    "verification_target":"US10Y_5.00_5.106_5.15_NQ_SPX_GOLD_DXY_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-24",
    "signal_id":"20260924_VIX_NONE_NO_TRADE",
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
    "tq_score":98,
    "opp_score":86,
    "no_trade_score":90,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":82,
    "ffs":92,
    "cds":97,
    "ias":84,
    "cbs":84,
    "mes":90,
    "invalidation":"wait_for_VIX_hold_above_16_or_return_below_14.5_after_rate_repricing",
    "verification_target":"VIX_14.5_14.58_15.17_16_ES_NQ_1d_3d",
    "verified_status":"partially_verified"
  }
]
```

今日の中心的な変化は、**昨日までのSPX押し目BUY仮説が、価格SLではなく「US10Y>5.05＋VIX再上昇」という事前に定義したinvalidationで崩れたこと**です。これはTSOのシナリオ撤退ルールが実際に働いた事例として残します。

一方BTCは、直近の急騰を追わず待っていた**84k付近の押し目が実際に到来**し、ETF買いとCMEも確認できています。ただし今回は金利ショックとTrump–Xi会談が同時にあるため、Aへは上げず、**0.25%のB、XM実損3,000円以内の場合だけB+実行候補**とします。
