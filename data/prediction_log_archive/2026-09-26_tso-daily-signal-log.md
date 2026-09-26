<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-26 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-26T09:12:02Z / chars: 18199 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-09-26

**使用モデル：GPT-5.6 Sol**  
**本日の市場の主役：US10Y**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**データ基準：2026年9月25日米国市場終了後＋9月26日朝のCrypto現物。土曜日のため、FX・先物・株式は金曜終値／最終確認値を使用。**

**crypto_grounds: etf=有, cme=有** — 9月24日のBTC現物ETFフローは最終的に約**+191Mドル**となり、6営業日連続流入。したがって昨日`unknown`だったBTC invalidationのETF側条件を本日は判定できます。9月25日分ETFはまだ確定していません。CME BTCは9月25日に安値**83885**、高値**85742**まで反発しています。citeturn865879search2turn865879search5turn865879search6

**expected_r_basis: subjective** — 本日の新規方向シグナルは0件。既存`20260924_BTC_BUY_PULLBACK`の発行時`expected_r=0.40`は変更しません。現在の管理評価では、ETF実需・CME反発をプラス、US10Y 5.18%台・週末spotの伸び悩み・既発行時MAE過小評価をマイナスとして扱います。

**invalidation_check: 20260924_BTC_BUY_PULLBACK=not_fired**

昨日`unknown`だった理由は、9月24日にCMEが一時83000を割った一方で「ETFフロー反転」が未確定だったためです。その後9月24日のETFは**+191Mドルの純流入**と確認されました。したがって、事前定義した複合条件

**CME <83000 ＋ ETFフロー反転**

は成立しておらず、価格SL **82500**にも到達していません。よって本日は明確に`not_fired`へ更新します。citeturn865879search2turn865879search6

---

## 1. 本日の結論

**新規A級：0件**  
**新規B級：0件**  
**既存B：BTC BUY_PULLBACK — 継続 / not_fired**  
**新規実取引：NO_TRADE**

今日は土曜日なので、新しい株・FX・先物シグナルを作りません。

ただし、昨日から重要な改善が1つあります。

BTCは9月24日に、

**Entry帯83800–84600到達  
→ CME 82850付近まで逆行  
→ それでもETFは+191Mドル流入  
→ 9月25日CMEは高値85742、終値系では約85.4k**

まで戻しました。citeturn865879search0turn865879search6

したがって昨日の、

**「価格構造が壊れ始めている可能性」**

から、

**「MAEは想定以上だったが、機関需要を伴って支持帯を回復した」**

へ評価を少し戻します。

ただし週末BTC/USD現物は約**84.0k**まで戻っており、87400のTP1へ向けて明確に走り始めたわけではありません。9月25日のBTC/USDは約84042、レンジ約84042–84879でした。citeturn935130search8

したがって管理は、

**HOLD相当 / 追加BUYなし / SL82500維持**

です。

金曜の市場全体では、S&P500が約**+0.43%**、Nasdaq Compositeが約**+0.46%**。AI関連株が再び市場を支えました。高金利下でも株が崩れていないという昨日のObservationは継続しています。citeturn435213search0

---

## 2. 前回判断の簡易検証

### `20260924_BTC_BUY_PULLBACK`

発行条件：

**Entry：83800–84600**  
**Mid：84200**  
**SL：82500**  
**TP1：87400**  
**TP2：90200**  
**RR：1.88**  
**win_prob：0.55**  
**expected_r：0.40**

RR再確認：

\[
(87400-84200)/(84200-82500)
=3200/1700
=1.882
\]

**記帳1.88で一致。**

9月24日のCME低値は約**82850**。ただし9月25日は、

**Open 84372  
High 85742  
Low 83885  
Close 85390**

という高出来高系列を確認しました。citeturn865879search6

つまり、

**ENTRY_TOUCHED  
→ 深いMAE  
→ SL_NOT_REACHED  
→ 支持帯回復  
→ TP1_NOT_REACHED**

です。

昨日問題だったETF側についても、9月24日は最終的に約**+191Mドル**。6営業日連続流入、累計約28億ドルとなりました。citeturn865879search2turn865879search5

したがって、

**`20260924_BTC_BUY_PULLBACK=not_fired`**

へ更新します。

発行時想定MAE 0.29Rに対し実測は約0.79Rだったので、**Entry品質評価が甘かったという較正結果はそのまま残します。**

現在の管理上の主観勝率は**0.54前後**。

発行時0.55を大きく変える理由はありません。

ETF需要とCME反発はプラスですが、US10Y 5.18%台と週末spotの伸び悩みが相殺しています。

---

## 3. 市場全体の前提

昨日までの、

**原油↑  
US10Y↑  
DXY↑**

という一方向のインフレ再加速は、金曜に少し緩みました。

WTIは**92.41ドル、-2.3%**で清算。米国とイランの段階的停戦・Hormuz再開協議への期待が、HouthiによるSaudi攻撃リスクを上回りました。citeturn407793search1

US10Yは木曜高値5.227%から、金曜は約**5.185%**へ若干低下。ただし依然として19年ぶり級の高水準です。citeturn543485search0turn543485search4

DXYも上昇が一服し、9月25日は約**101.23**。citeturn935130search5

GoldはGCZ26で約**4308.20**まで反発。高値4331.05、安値4290.87でした。Reutersの広義米金先物清算値4321.20とは若干差があるため、TSOでは指定通り**GCZ26=4308.20**を採用し、Goldだけ`partially_verified`とします。citeturn550058search1turn883968view2

VIXも**15.38**へ低下。木曜15.67からややrisk-offが後退しています。citeturn407793search0

USDJPYは重要です。

9月25日は日銀集計で東京時間レンジ**157.95–158.84**、17:00時点**158.09–158.11**。別の24時間系列でも終値約158.16です。さらにTrump大統領が円安への懸念を日本側へ伝えていたことが明らかになり、日本当局は再びrate checkを実施しました。citeturn864529search46turn864529search10turn407793search2turn407793search5

これはUSDJPYの160方向を追わない判断をさらに支持します。

米消費者センチメント確報は**48.1**。8月51.7から低下し、1年先インフレ期待は**4.6%**、5年先は**3.4%**でした。成長不安とインフレ懸念が同時に残っています。citeturn590018search3

したがって現在は、

**全面RISK_ONでもRISK_OFFでもなく、AI株の強さと非常に高い金利が共存するMIXED regime**

です。

---

## 4. 10資産別判断

| 資産 | 本日判断 | 評価 |
|---|---|---|
| **GOLD** | **NO_TRADE** | GCZ26 約4308.2。4290を守り反発したがUS10Y 5.18%が重い。citeturn550058search1 |
| **BTC** | **既存B継続 / 新規NO_TRADE** | spot約84.0k。9/24 ETF +191M、CME金曜反発。`not_fired`。 |
| **ETH** | **NO_TRADE** | spot約2675、CME約2715。BTCよりやや弱い。citeturn935130search7turn865879search8 |
| **WTI** | **NO_TRADE** | 92.41。停戦期待で-2.3%。地政学ヘッドライン依存が強過ぎる。citeturn407793search1 |
| **USDJPY** | **NO_TRADE** | 約158.2。日米双方から円安懸念、rate check再発。 |
| **SPX** | **NO_TRADE** | ESZ26は金曜概ね7770台。高金利下でも底堅いが週末前上昇後。 |
| **NASDAQ** | **NO_TRADE** | NQZ26は金曜約30900台。AIが強いが短期指標は過熱。citeturn543116search1turn435213search0 |
| **DXY** | **NO_TRADE** | 101.23。上昇基調だが金曜は伸び止まり。citeturn935130search5 |
| **US10Y** | **NO_TRADE** | 約5.185%。主役だが5.227から一服、追随SELL/BUYとも不利。citeturn543485search0 |
| **VIX** | **NO_TRADE** | 15.38。木曜15.67から低下しパニック化していない。citeturn407793search0 |

---

## 5. A級候補

**なし。**

最も興味深いのはNASDAQですが、Aにはしません。

金曜のNQZ26はテクニカル系列で**30,900台**へ回復し、RSIも強気、主要移動平均を上回っています。一方でStochasticなどは過熱域です。citeturn543116search1turn550352search3

より重要なのは、

**US10Y ≈5.18%  
＋ DXY ≈101.2  
なのにNASDAQが上がっている**

ことです。

これは強い。

ただし強さを確認した直後に追いかけるのではなく、**次の押しで強さが残るか**を見ます。

BTCもAではありません。

ETF需要は強いものの、実測MAEがA基準を大幅超過した既存シグナルを持っているため、新規Aとして積み増す理由はありません。

---

## 6. B級監視候補

**新規B：なし。**

継続は1件だけです。

### `20260924_BTC_BUY_PULLBACK`

**Entry 83800–84600**  
**Mid 84200**  
**SL 82500**  
**TP1 87400**  
**TP2 90200**  
**RR 1.88**  
**win_prob 0.55**  
**expected_r 0.40**  
**risk_pct 0.25%**

現在：

**Entry reached**  
**SL not reached**  
**TP1 not reached**  
**invalidation not fired**

9月24日のETFは約+191Mドルで、前日の複合invalidation条件を否定しました。citeturn865879search2

CMEも9月25日に83.9kを下値として85.7kまで上昇しています。citeturn865879search6

一方、週末現物は約84kへ戻っているので、まだ勝負はついていません。

したがって、

**追加BUY：禁止**  
**SL82500：変更なし**  
**TP1 87400：変更なし**

です。

なお実口座で約定した事実は確認できていないため、これはあくまで**研究シグナル管理**として扱います。

---

## 7. 触らない資産

今日は特に**USDJPY、WTI、US10Y**です。

USDJPYは金利差だけなら上方向ですが、158～160円では通常のトレンド評価より政策介入テールの方が重要です。

9月25日にはTrump大統領自身が円安を問題視していたことが公表され、日本側もrate checkを実施しています。これは158円台後半からBUYするRRを大きく悪化させます。citeturn407793search2turn407793search5

WTIは94.61→92.41と、1日で材料評価が反転しました。

**Houthi攻撃**
と
**US–Iran/Hormuz和平期待**

のヘッドラインだけで数ドル動いています。ここで92ドルSELLを追えば、ニュース一発で96ドルへ戻される可能性があります。

US10Yも同じです。5.227まで急騰した後5.18台。ここから利回り上昇を追うより、次週の雇用統計・インフレ指標を待つ方がEntry品質が高いです。Reutersも来週の主要テーマを米雇用・インフレ指標として挙げています。citeturn812650news0

---

## 8. 後日検証ポイント

### BTC

最優先。

**82500 → fired**  
**87400 → TP1**  
**90200 → TP2**

追加のシナリオ失効条件は、

**CME <83000**
＋
**ETF純流出**

です。

9月24日はCME<83000があってもETFが+191Mだったため、成立しませんでした。

次回もし再び83k割れとなり、その日にETFフローも純流出へ転じれば、82500到達前の早期撤退ルールを発動させます。

時間決済は**9月30日**。

### NASDAQ

来週の最重要株式観察。

NQZ26は金曜およそ30,900台。

**30,650–30,750へ押して維持**
＋
**US10Y <=5.20**
なら、新しいBUY_PULLBACK候補を作れます。

**30,300割れ**
なら高金利耐性仮説を撤回。

現在値からの追随BUYはしません。

### SPX

ESでは、

**7750–7770**

が短期均衡帯になっています。

5.18%金利でもここを維持しているので、来週も7700を守れば株式全体の耐性は強い。

**ES <7680**
＋
**VIX >17**

ならrisk-off再判定です。

### USDJPY

金曜のrate checkとTrump発言で条件が変わりました。

**159–160でBUYは作らない。**

今後は、

**158.8超へ再上昇しても介入がない**
のか、

それとも

**157台へ円高が継続**
するのかを観察します。

157.0～157.5へ低下すれば、旧来の単純なドル金利差BUY regimeからの変化を疑います。

### GOLD

GCZ26は、

**4290付近を支持**
→ 金曜4308へ反発。

次は、

**4350回復**
ならSELL圧力一巡。

**4275割れ**
なら再び弱気。

ただしUS10Yが5.1%を割るならGold SELLは避けます。

### WTI

Friday settle **92.41**。

**90割れ**
ならHormuz正常化期待優勢。

**95超**
ならSaudi/Houthi供給リスク再優勢。

92～94は現在のニュース均衡帯なので触りません。

---

## 9. Obsidian保存用 Observation Draft

```markdown
# 2026-09-26 BTC Invalidation Resolved / Equity Resilience / Rates Still Extreme

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

MIXED

AI / Nasdaq:
RISK_ON bias

Rates:
EVENT / restrictive

Oil:
EVENT / headline-driven

FX:
intervention-sensitive

## Main change

BTC invalidation yesterday:
unknown

Reason:
CME temporarily <83000
ETF Sep24 not finalized

New evidence:
Sep24 BTC ETF final ~+191m
six consecutive inflow sessions
~2.8bn cumulative

Therefore:

CME <83000
+
ETF reversal

was NOT satisfied.

20260924_BTC_BUY_PULLBACK:
not_fired

## BTC active

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

win_prob at issue:
0.55

expected_r at issue:
0.40

Sep24:
CME low ~82850

Sep25 CME:
open ~84372
high ~85742
low ~83885
close ~85390

Weekend spot:
~84000

Status:
ENTRY_REACHED
SL_NOT_REACHED
TP1_NOT_REACHED
NOT_FIRED

Observed MAE:
~0.79R

Learning remains:
initial MAE estimate 0.29R was too optimistic.

Do not add.
Do not widen SL.

Time exit:
2026-09-30

## Sep25 macro

US10Y:
~5.185%
after high 5.227

DXY:
101.23

USDJPY:
~158.1-158.2
Tokyo range 157.95-158.84

VIX:
15.38

WTI:
92.41
-2.3%

GCZ26:
4308.20

US equities:
S&P ~+0.43%
Nasdaq Composite ~+0.46%

Interpretation:

Oil and yields eased marginally
while AI equities remained resilient.

No broad risk-off confirmation.

## USDJPY policy risk

Trump disclosed concern over weak yen.

Japan:
rate check again

Interpretation:
159-160 area has asymmetric intervention risk.

Do not chase USDJPY BUY.

## Oil

US-Iran:
phased truce / Hormuz reopening discussions

Houthi:
Saudi attack risk remains

WTI:
94.61 Thu
-> 92.41 Fri

Two-way event market.

NO_TRADE.

## Gold

GCZ26:
4308.20

Fri low:
4290.87

Fri high:
4331.05

Still pressured by:
high yields
hawkish Fed

But:
4290 support held.

NO_TRADE.

## Next-week tests

BTC:
82500 / 87400 / ETF flows

NQ:
30650-30750 support
30300 failure level

ES:
7700 resilience

US10Y:
5.10 / 5.25

WTI:
90 / 95

USDJPY:
157 / 159-160

## Active invalidation

20260924_BTC_BUY_PULLBACK=not_fired

## New signals

A:
NONE

B:
NONE

Existing:
BTC BUY_PULLBACK active

#TSO #BTC #US10Y #NASDAQ #USDJPY #WTI #GOLD
```

---

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-26,20260926_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,87,90,,MIXED,86,94,98,84,85,94,wait_for_GCZ26_reclaim_4350_or_break_4275_with_US10Y_DXY_confirmation,GCZ26_4275_4290.87_4308.20_4331.05_4350_US10Y_DXY_1d_3d,partially_verified
2026-09-26,20260926_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,94,62,,MIXED,84,93,98,91,87,92,manage_existing_20260924_BUY_SL82500_TP87400_not_fired_Sep24_ETF_positive,BTC_82500_83800_84000_84600_87400_ETF_CME_1d_3d_5d,partially_verified
2026-09-26,20260926_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,84,88,,MIXED,76,89,95,82,81,85,prefer_existing_BTC_expression_wait_for_ETH_hold_2630_or_reclaim_2750,ETH_2630_2675_2715_2750_ETF_CME_1d_3d,partially_verified
2026-09-26,20260926_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,93,95,,EVENT,95,99,99,92,92,98,wait_for_WTI_break_below_90_or_reclaim_above_95_after_USIran_Hormuz_negotiations,WTI_90_92.41_95_96_Hormuz_USIran_Houthi_1d_3d,verified
2026-09-26,20260926_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,95,97,,EVENT,95,98,99,95,92,99,do_not_chase_158_area_after_rate_check_and_US_concern_wait_for_157_or_clear_policy_response,USDJPY_157_157.95_158.16_158.84_159_160_MOF_US_1d_3d,verified
2026-09-26,20260926_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,91,86,,MIXED,83,93,97,88,87,95,wait_for_ES_pullback_7720_7750_or_break_below_7680_with_VIX_confirmation,ESZ26_7680_7720_7750_7775_7820_US10Y_VIX_1d_3d,partially_verified
2026-09-26,20260926_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,96,84,,RISK_ON,88,95,98,95,94,95,do_not_chase_AI_rally_wait_for_NQ_pullback_30650_30750_or_failure_below_30300,NQZ26_30300_30650_30750_30900_31000_US10Y_VIX_1d_3d,partially_verified
2026-09-26,20260926_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,90,88,,MIXED,88,95,98,88,88,96,wait_for_DXY_break_above_101.5_or_pullback_below_100.7_with_US10Y_confirmation,DXY_100.7_101.0_101.23_101.5_US10Y_USDJPY_1d_3d,verified
2026-09-26,20260926_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,98,94,,EVENT,99,99,99,97,97,99,do_not_chase_5.18_wait_for_rejection_below_5.10_or_sustained_break_above_5.25,US10Y_5.10_5.185_5.227_5.25_NQ_GOLD_DXY_1d_3d,verified
2026-09-26,20260926_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,82,89,,MIXED,74,89,96,78,78,88,wait_for_VIX_break_above_17_or_return_below_14.5_with_ES_NQ_confirmation,VIX_14.5_15.38_17_ES_NQ_US10Y_1d_3d,verified
```

### TSO_LOG JSON

```json
[
  {"date":"2026-09-26","signal_id":"20260926_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":87,"no_trade_score":90,"risk_pct":null,"regime":"MIXED","ems":86,"ffs":94,"cds":98,"ias":84,"cbs":85,"mes":94,"invalidation":"wait_for_GCZ26_reclaim_4350_or_break_4275_with_US10Y_DXY_confirmation","verification_target":"GCZ26_4275_4290.87_4308.20_4331.05_4350_US10Y_DXY_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-26","signal_id":"20260926_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":94,"no_trade_score":62,"risk_pct":null,"regime":"MIXED","ems":84,"ffs":93,"cds":98,"ias":91,"cbs":87,"mes":92,"invalidation":"manage_existing_20260924_BUY_SL82500_TP87400_not_fired_Sep24_ETF_positive","verification_target":"BTC_82500_83800_84000_84600_87400_ETF_CME_1d_3d_5d","verified_status":"partially_verified"},
  {"date":"2026-09-26","signal_id":"20260926_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":84,"no_trade_score":88,"risk_pct":null,"regime":"MIXED","ems":76,"ffs":89,"cds":95,"ias":82,"cbs":81,"mes":85,"invalidation":"prefer_existing_BTC_expression_wait_for_ETH_hold_2630_or_reclaim_2750","verification_target":"ETH_2630_2675_2715_2750_ETF_CME_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-26","signal_id":"20260926_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":93,"no_trade_score":95,"risk_pct":null,"regime":"EVENT","ems":95,"ffs":99,"cds":99,"ias":92,"cbs":92,"mes":98,"invalidation":"wait_for_WTI_break_below_90_or_reclaim_above_95_after_USIran_Hormuz_negotiations","verification_target":"WTI_90_92.41_95_96_Hormuz_USIran_Houthi_1d_3d","verified_status":"verified"},
  {"date":"2026-09-26","signal_id":"20260926_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":95,"no_trade_score":97,"risk_pct":null,"regime":"EVENT","ems":95,"ffs":98,"cds":99,"ias":95,"cbs":92,"mes":99,"invalidation":"do_not_chase_158_area_after_rate_check_and_US_concern_wait_for_157_or_clear_policy_response","verification_target":"USDJPY_157_157.95_158.16_158.84_159_160_MOF_US_1d_3d","verified_status":"verified"},
  {"date":"2026-09-26","signal_id":"20260926_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":91,"no_trade_score":86,"risk_pct":null,"regime":"MIXED","ems":83,"ffs":93,"cds":97,"ias":88,"cbs":87,"mes":95,"invalidation":"wait_for_ES_pullback_7720_7750_or_break_below_7680_with_VIX_confirmation","verification_target":"ESZ26_7680_7720_7750_7775_7820_US10Y_VIX_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-26","signal_id":"20260926_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":96,"no_trade_score":84,"risk_pct":null,"regime":"RISK_ON","ems":88,"ffs":95,"cds":98,"ias":95,"cbs":94,"mes":95,"invalidation":"do_not_chase_AI_rally_wait_for_NQ_pullback_30650_30750_or_failure_below_30300","verification_target":"NQZ26_30300_30650_30750_30900_31000_US10Y_VIX_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-26","signal_id":"20260926_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":90,"no_trade_score":88,"risk_pct":null,"regime":"MIXED","ems":88,"ffs":95,"cds":98,"ias":88,"cbs":88,"mes":96,"invalidation":"wait_for_DXY_break_above_101.5_or_pullback_below_100.7_with_US10Y_confirmation","verification_target":"DXY_100.7_101.0_101.23_101.5_US10Y_USDJPY_1d_3d","verified_status":"verified"},
  {"date":"2026-09-26","signal_id":"20260926_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":98,"no_trade_score":94,"risk_pct":null,"regime":"EVENT","ems":99,"ffs":99,"cds":99,"ias":97,"cbs":97,"mes":99,"invalidation":"do_not_chase_5.18_wait_for_rejection_below_5.10_or_sustained_break_above_5.25","verification_target":"US10Y_5.10_5.185_5.227_5.25_NQ_GOLD_DXY_1d_3d","verified_status":"verified"},
  {"date":"2026-09-26","signal_id":"20260926_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":82,"no_trade_score":89,"risk_pct":null,"regime":"MIXED","ems":74,"ffs":89,"cds":96,"ias":78,"cbs":78,"mes":88,"invalidation":"wait_for_VIX_break_above_17_or_return_below_14.5_with_ES_NQ_confirmation","verification_target":"VIX_14.5_15.38_17_ES_NQ_US10Y_1d_3d","verified_status":"verified"}
]
```

本日の最大の更新は、**BTCの`unknown`が`not_fired`へ解消したこと**です。9月24日にCMEが83kを一時割ったものの、ETFは反転せず約+191Mドルの純流入でした。その後CMEも金曜に85k台へ回復しています。したがって既存BUY仮説はまだ有効ですが、発行時MAE推定が甘かった事実は残ります。

同時に、**US10Yが5.18%台という異常に高い水準でもNASDAQが再び上昇している**ことも継続観察価値があります。来週NQが押しても30,650–30,750を維持できれば、次の高品質なBUY候補になり得ます。
