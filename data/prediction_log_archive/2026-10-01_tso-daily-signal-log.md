<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-10-01 07:00 JST -->
<!-- transport: Codex read_thread; message 5597c10b-4443-4a38-b944-b9488f5bcd67; truncated=false -->
<!-- archived_at: 2026-09-30T23:03:05Z / chars: 17594 / 値は無修正 -->

> **取込監査注記（原文とは別、PR #179）**: 以下はChatGPT原文の保存であり、本文の決着・成績を検証済みとするものではありません。BTC `20260924_BTC_BUY_PULLBACK` の `time_exit` / `-0.19R` は採用しません。リポジトリの翌営業日から5本という規約では5本目は10/1、最終確認は10/2朝です。また本文の06:55 JST時点では9/30 UTCのBTC日足は未確定です。サイドカー本体は `unknown`、`time_exit` は原語隔離のみ。10/2の監視対象を維持し、原文の終値を採点用価格へ転記していません。以下の原文は無改変です。

# TSO Daily Signal Log v2 — 2026-10-01

**使用モデル：GPT-5.6 Sol**  
**本日の市場の主役：US10Y**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**データ基準：2026年9月30日米国市場終了後〜10月1日06:55 JST前後。ES/NQ/GCZ26の一部は遅延値・同一原資産のMicro契約照合を含む。**

**crypto_grounds: etf=有, cme=有** — 9月29日の米現物ETFはBTC約**+66.2Mドル**、ETH約**-2.8Mドル**。CME系のBTC先物根拠も取得できています。:chatgpt-content-reference{index="0"}

**expected_r_basis: subjective** — 本日の新規方向シグナルは0件。既存`20260930_WTI_SELL_PULLBACK`の`expected_r=0.39`は発行時固定。非約定確率、地政学ヘッドライン、5営業日時間決済を織り込んだ値です。

**invalidation_check: 20260930_WTI_SELL_PULLBACK=not_fired**

**resolved_today: 20260924_BTC_BUY_PULLBACK=time_exit**

9月30日のPCEは、総合指数が前月比**+0.3%**と市場予想+0.4%を下回り、前年比も**+3.4%**と予想+3.7%を下回りました。これを受け10月Fed利上げ確率は一時**37%**まで低下しました。ところが10年債利回りは最終的に**約5.29%**へ戻りました。つまり「政策金利期待は低下したが、長期金利は下がらない」という、短期スイングには扱いにくいイールドカーブの変化です。:chatgpt-content-reference{index="1"}

---

## 1. 本日の結論

**新規A級：0件**  
**新規B級：0件**  
**既存B：WTI SELL_PULLBACK — Entry到達済み / not_fired**  
**BTC BUY_PULLBACK：5営業日時間決済で終了**  
**本日の新規実取引：NO_TRADE**

昨日のPCEは一見risk-on材料でしたが、長期金利の反応が悪いです。

2年債利回りは低下した一方、10年債は朝の約5.20%から最終的に**約5.29%**、30年債も約**5.64%**へ上昇しました。背景はインフレだけではなく、強いGDP、財政・国債供給への懸念です。:chatgpt-content-reference{index="2"}

株式もこれをそのまま好感できませんでした。最終的に、

**S&P500 -0.25%  
Nasdaq Composite +0.24%  
VIX 約16.34**

です。:chatgpt-content-reference{index="3"}

したがって、昨日まで考えていたNASDAQ BUY再開は**まだ見送ります**。

一方WTIは、昨日発行したSELL_PULLBACKのEntry帯`90.30–91.10`へ実際に戻りました。

WTIは最終的に**90.42ドル**で清算。日中には91ドル台まで戻しており、Entry条件は成立しています。SL92.40には達していません。:chatgpt-content-reference{index="4"}

したがって、

**`20260930_WTI_SELL_PULLBACK = ENTRY_FILLED / not_fired`**

として継続管理します。

---

## 2. 前回判断の簡易検証

### `20260924_BTC_BUY_PULLBACK` — TIME EXIT

発行条件：

**Entry：83800–84600**  
**Mid：84200**  
**SL：82500**  
**TP1：87400**  
**TP2：90200**  
**RR：1.88**  
**win_prob：0.55**  
**expected_r：0.40**

このシグナルは9月30日で5営業日の時間決済期限を迎えました。

Bitfinexの9月30日BTC/USD日足は、

**Open 83719  
High 85567  
Low 83048  
Close 83879**

でした。:chatgpt-content-reference{index="5"}

したがって、

**ENTRY_REACHED  
SL_NOT_REACHED  
TP1_NOT_REACHED  
TIME_EXIT**

です。

中点84200を仮想Entry、83879を時間決済基準にすると、

\[
(83879-84200)/(84200-82500)
=-321/1700
\approx -0.19R
\]

よって研究上の代表値は**約-0.19R**。

実際の約定位置がEntry帯のどこだったかで実損益は変わるため、これは仮想検証値です。

今回の最大MAEは別系列で82550前後まで確認されているため、ほぼ**-1R直前まで逆行してから-0.19R程度まで戻して終了**した形です。

ETFフローについても、9月29日はBTCが+66.2Mドルまで再び増えましたが、先週の+999M、+714Mに比べれば小さい。価格も87kへ戻れませんでした。:chatgpt-content-reference{index="6"}

今回の学習はかなり明確です。

**ETF純流入の有無だけでは不十分。**

次回以降は、

**flow direction  
＋ flow acceleration  
＋ price response**

を分離した方がよいです。

---

### `20260930_WTI_SELL_PULLBACK` — ENTRY FILLED / 継続

発行：

**Entry 90.30–91.10**  
**Mid 90.70**  
**SL 92.40**  
**TP1 87.50**  
**TP2 85.60**  
**RR 1.88**

9月30日のWTIは最終的に**90.42**、前日比+1.04ドル。日中は91ドル台まで上昇したためEntry帯へ到達しています。:chatgpt-content-reference{index="7"}

上昇要因は、米イラン協議の停滞、燃料在庫減少です。一方でSaudi East-West Pipeline復旧とGulf exports回復自体は継続しており、Goldman推計では湾岸輸出は直近**23.3mbpd**まで戻っています。:chatgpt-content-reference{index="8"}

したがってSELL仮説は、

**弱くなったが壊れてはいない**

と判定します。

現状は、

**ENTRY_FILLED  
SL_NOT_REACHED  
TP1_NOT_REACHED  
not_fired**

です。

---

## 3. 市場全体の前提

本日のregimeは**MIXED**です。

PCEの結果だけならrisk-onです。

米PCEは前月比+0.3%、前年比+3.4%で予想以下。Fed利上げ確率は約37%まで低下しました。:chatgpt-content-reference{index="9"}

しかし重要なのはその後です。

**2Y ↓  
10Y ↑  
30Y ↑**

となりました。

10年債は約5.29%、30年債は約5.64%。市場は「Fedが追加利上げしなくても、長期金利は高いままかもしれない」と価格形成しています。:chatgpt-content-reference{index="10"}

これが本日の市場の主役をUS10Yとした理由です。

DXYは約**101.47**、USDJPYは約**157.34**。ドルはPCE後も大崩れしていません。:chatgpt-content-reference{index="11"}

GoldはGCZ26近辺で概ね**4190～4200ドル**。Yahooの12月限では直近約4201ドル、Reuters系市場表示ではGold futures約4189ドルと差があるため`partially_verified`です。:chatgpt-content-reference{index="12"}

ES/NQはCME系12月限遅延値で、

**ES ≈7770  
NQ ≈30850–30860**

まで回復しています。Micro契約とE-miniは同一指数・同一満期の価格軸なので方向確認には使えますが、本日のLOGでは`partially_verified`扱いにします。:chatgpt-content-reference{index="13"}

BTCは日足終値系列で約**83879**、ETHは約**2690前後**。PCE直後BTCは一時85.5k近辺まで上昇しましたが、その上昇を維持できませんでした。:chatgpt-content-reference{index="14"}

---

## 4. 10資産別判断

| 資産 | 本日判断 | 評価 |
|---|---|---|
| **GOLD** | **NO_TRADE** | GCZ26約4190–4200。Soft PCEはプラスだが10Y/30Y上昇が相殺。 |
| **BTC** | **NO_TRADE** | 旧BUYはTIME_EXIT。83.9k付近。新規は作らない。 |
| **ETH** | **NO_TRADE** | 約2690。独立edge不足、ETFは最新確認で小幅流出。 |
| **WTI** | **既存B SELL管理 / 新規NO_TRADE** | 90.42。Entry成立。SL92.40維持。 |
| **USDJPY** | **NO_TRADE** | 約157.34。Soft PCEでも円高加速せず、政策リスクと金利差が拮抗。 |
| **SPX** | **NO_TRADE** | ES約7770。回復したが長期金利5.29%＋VIX16台。 |
| **NASDAQ** | **NO_TRADE** | NQ約30850台。強いが短期過熱＋長期金利逆風。 |
| **DXY** | **NO_TRADE** | 約101.47。PCE後も崩れず。 |
| **US10Y** | **NO_TRADE** | 約5.29%。方向は強いが極端値を追わない。 |
| **VIX** | **NO_TRADE** | 約16.34。panicではないがrisk premiumは残る。 |

---

## 5. A級候補

**なし。**

NASDAQは価格だけならかなり強いです。

Micro NQ Dec-26の遅延テクニカルでは、

**RSI ≈65  
MACD Buy  
主要MAすべてBuy**

ですが、

**Stochastic ≈100  
StochRSI ≈94**

と過熱しています。:chatgpt-content-reference{index="15"}

さらにUS10Yが5.29%です。

したがって「NASDAQが強い」と「今買う」を分離します。

A級を作れるのは、少なくとも

**NQが30700前後まで押す**  
＋
**US10Yが5.20以下へ低下**  
＋
**VIXが15.5以下**

が揃ってからです。

---

## 6. B級監視候補

**新規B級：なし。**

既存のみ。

### `20260930_WTI_SELL_PULLBACK`

**Entry 90.30–91.10**  
**Mid 90.70**  
**SL 92.40**  
**TP1 87.50**  
**TP2 85.60**  
**RR 1.88**  
**win_prob 0.55**  
**expected_r 0.39**  
**risk_pct 0.25%**

現在の90.42は、ほぼEntry中点付近です。

供給面では湾岸輸出回復が続いていますが、米イラン協議の停滞と燃料在庫減少が上方向へ反発させました。:chatgpt-content-reference{index="16"}

したがって現在は、

**「供給回復SELL」対「地政学・製品在庫BUY」**

の競合状態です。

SL92.40を変更しません。

また、

**91.5超**
＋
**新しいSaudi/Iran/Hormuz供給障害**

が確認された場合は、92.40到達前でも早期invalidation候補とします。

---

## 7. 触らない資産

特に**US10Y、NASDAQ、GOLD、BTC**です。

US10Yは5.29%まで来ていますが、ここから利回り上昇を追うとFridayの雇用統計で急反転するリスクがあります。

NASDAQはPCEを好感しましたが、S&P全体は下落しました。AI/大型techだけが強い選別相場です。:chatgpt-content-reference{index="17"}

GoldはSoft PCEに対して思ったほど上がっていません。これは長期金利上昇がまだ重いという意味で、BUYにもSELLにも非対称性が足りません。

BTCも同じです。

PCE直後に85k台へ上がっても、日足で83k台へ戻りました。:chatgpt-content-reference{index="18"}

旧BUYを時間決済した直後に再BUYする根拠はありません。

---

## 8. 後日検証ポイント

### WTI

唯一の未決着方向判断です。

**92.40 → fired**  
**87.50 → TP1**  
**85.60 → TP2**

特に、

**WTI >91.5**
＋
**Gulf export回復が鈍化**

ならSELL仮説を弱めます。

逆に、

**WTI <89**
＋
**Saudi/Gulf exports高水準維持**

ならTP1方向の確率を上げます。

### BTC

今回のシグナルは終了。

代表値：

**TIME_EXIT：約83879**  
**Mid基準：約-0.19R**  
**最大MAE：約1R**

次回以降、Crypto BUYでETF flowを使う場合は、

**flow > 0**

だけではなく、

**flow acceleration > 0**
と
**price response > 0**

の両方を確認したいところです。

### NASDAQ

新しい観察帯：

**30700–30780 → 次のBUY_PULLBACK候補**

ただし、

**US10Y <=5.20  
VIX <=15.5**

が必要。

**NQ <30500**
＋
**US10Y >5.30**
ならBUY仮説は撤回。

### SPX

ESでは、

**7740–7760**
が次の支持帯。

ここを維持しながら10年債が低下すればBUY候補。

逆に、

**ES <7700  
VIX >17**

ならRISK_OFF判定を強めます。

### USDJPY

現在約157.3。

**156.5割れ・定着**
なら円高SELL仮説。

**158.5回復**
なら金利差BUY仮説再評価。

中間では触りません。

### GOLD

GCZ26：

**4150–4170**
が直近支持。

**4200–4230回復**
＋
**US10Y <5.20**
ならBUY候補。

**4140割れ**
＋
**US10Y >5.30**
なら再びSELL優勢ですが、ブレイク直後は追いません。

---

## 9. Obsidian保存用 Observation Draft

```markdown
# 2026-10-01 Soft PCE / Long-End Yield Refuses to Fall / BTC Time Exit

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

## PCE

Aug headline PCE:
+0.3% MoM
vs +0.4% expected

YoY:
+3.4%
vs +3.7% expected

Fed Oct hike probability:
~37%

## Critical divergence

Short-end:
yields down

Long-end:
10Y ~5.29%
30Y ~5.64%

Interpretation:

Fed hike risk fell,
but term premium / fiscal / growth pressure remained.

This is not a clean risk-on macro setup.

## US equities

S&P500:
-0.25%

Nasdaq Composite:
+0.24%

VIX:
~16.34

Tech:
relative strength

Broad market:
weak

## Futures

ES Dec:
~7770 delayed

NQ Dec:
~30850-30860 delayed

NQ technical:
strong
but overbought

Do not chase.

Requalification:
NQ pullback ~30700
US10Y <=5.20
VIX <=15.5

## BTC resolved

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

Sep30 Bitfinex:
close 83879
high 85567
low 83048

Result:
TIME_EXIT

Midpoint synthetic result:
~ -0.19R

Maximum observed MAE:
~1R

Learning:
ETF flow sign alone was insufficient.

Candidate new features:
ETF flow acceleration
price response per flow
flow-price divergence duration

Remove from active invalidation list.

## WTI active

20260930_WTI_SELL_PULLBACK

Entry:
90.30-91.10

Mid:
90.70

SL:
92.40

TP1:
87.50

TP2:
85.60

RR:
1.88

win_prob:
0.55

expected_r:
0.39

Sep30 settle:
90.42

Status:
ENTRY_FILLED
SL_NOT_REACHED
TP1_NOT_REACHED
not_fired

Bullish counterforces:
stalled US-Iran talks
gasoline/distillate draw
tight product markets

Bearish thesis:
Saudi East-West Pipeline restored
Yanbu exports resumed
Gulf exports ~23.3mbpd

Do not widen SL.

## Active invalidation

20260930_WTI_SELL_PULLBACK=not_fired

## New signals

A:
NONE

B:
NONE

Existing B:
WTI SELL_PULLBACK

#TSO #US10Y #WTI #BTC #NASDAQ #GOLD
```

---

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-10-01,20261001_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,91,92,,EVENT,90,96,99,87,87,97,wait_for_GCZ26_hold_4150_4170_or_reclaim_4200_4230_with_US10Y_confirmation,GCZ26_4140_4150_4170_4190_4200_4230_US10Y_DXY_1d_3d,partially_verified
2026-10-01,20261001_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,90,85,,MIXED,80,93,98,86,82,88,previous_20260924_BUY_resolved_by_time_exit_wait_for_new_structure,BTC_83000_83879_85000_CME_ETF_flow_acceleration_1d_3d,partially_verified
2026-10-01,20261001_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,84,89,,MIXED,76,90,96,81,80,84,wait_for_ETH_hold_2630_or_reclaim_2750_with_BTC_and_ETF_confirmation,ETH_2630_2690_2750_ETF_CME_1d_3d,partially_verified
2026-10-01,20261001_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,96,63,,EVENT,78,96,99,91,86,97,manage_existing_20260930_SELL_PULLBACK_SL92.40_TP87.50_not_fired_no_new_position,WTI_Nov26_89_90.42_91.5_92.40_87.50_Gulf_exports_USIran_1d_3d_5d,verified
2026-10-01,20261001_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,90,92,,EVENT,88,96,99,89,87,97,wait_for_clean_break_below_156.5_or_reclaim_above_158.5_before_new_signal,USDJPY_156.5_157.34_158.5_DXY_US10Y_MOF_1d_3d,verified
2026-10-01,20261001_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,92,90,,MIXED,86,95,98,89,88,96,wait_for_ES_hold_7740_7760_with_US10Y_below_5.20_or_break_below_7700_with_VIX_above_17,ESZ26_7700_7740_7760_7770_US10Y_VIX_1d_3d,partially_verified
2026-10-01,20261001_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,96,87,,MIXED,89,96,98,94,92,96,do_not_chase_overbought_NQ_wait_for_30700_30780_pullback_with_US10Y_below_5.20_and_VIX_below_15.5,NQZ26_30500_30700_30780_30858_US10Y_VIX_1d_3d,partially_verified
2026-10-01,20261001_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,89,89,,MIXED,85,94,98,85,85,95,wait_for_DXY_break_above_101.7_or_failure_below_100.8_with_yield_confirmation,DXY_100.8_101.47_101.7_US10Y_USDJPY_1d_3d,verified
2026-10-01,20261001_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,99,97,,EVENT,99,99,99,98,98,99,do_not_chase_long_end_yield_wait_for_rejection_below_5.20_or_sustained_break_above_5.30_after_jobs_data,US10Y_5.20_5.29_5.30_jobs_NQ_GOLD_DXY_1d_3d,verified
2026-10-01,20261001_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,87,88,,MIXED,81,92,97,82,82,91,wait_for_VIX_break_above_17_or_return_below_15.5_with_ES_NQ_confirmation,VIX_15.5_16.34_17_ES_NQ_US10Y_1d_3d,verified
```

### TSO_LOG JSON

```json
[
  {"date":"2026-10-01","signal_id":"20261001_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":91,"no_trade_score":92,"risk_pct":null,"regime":"EVENT","ems":90,"ffs":96,"cds":99,"ias":87,"cbs":87,"mes":97,"invalidation":"wait_for_GCZ26_hold_4150_4170_or_reclaim_4200_4230_with_US10Y_confirmation","verification_target":"GCZ26_4140_4150_4170_4190_4200_4230_US10Y_DXY_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-10-01","signal_id":"20261001_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":90,"no_trade_score":85,"risk_pct":null,"regime":"MIXED","ems":80,"ffs":93,"cds":98,"ias":86,"cbs":82,"mes":88,"invalidation":"previous_20260924_BUY_resolved_by_time_exit_wait_for_new_structure","verification_target":"BTC_83000_83879_85000_CME_ETF_flow_acceleration_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-10-01","signal_id":"20261001_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":84,"no_trade_score":89,"risk_pct":null,"regime":"MIXED","ems":76,"ffs":90,"cds":96,"ias":81,"cbs":80,"mes":84,"invalidation":"wait_for_ETH_hold_2630_or_reclaim_2750_with_BTC_and_ETF_confirmation","verification_target":"ETH_2630_2690_2750_ETF_CME_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-10-01","signal_id":"20261001_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":96,"no_trade_score":63,"risk_pct":null,"regime":"EVENT","ems":78,"ffs":96,"cds":99,"ias":91,"cbs":86,"mes":97,"invalidation":"manage_existing_20260930_SELL_PULLBACK_SL92.40_TP87.50_not_fired_no_new_position","verification_target":"WTI_Nov26_89_90.42_91.5_92.40_87.50_Gulf_exports_USIran_1d_3d_5d","verified_status":"verified"},
  {"date":"2026-10-01","signal_id":"20261001_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":90,"no_trade_score":92,"risk_pct":null,"regime":"EVENT","ems":88,"ffs":96,"cds":99,"ias":89,"cbs":87,"mes":97,"invalidation":"wait_for_clean_break_below_156.5_or_reclaim_above_158.5_before_new_signal","verification_target":"USDJPY_156.5_157.34_158.5_DXY_US10Y_MOF_1d_3d","verified_status":"verified"},
  {"date":"2026-10-01","signal_id":"20261001_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":92,"no_trade_score":90,"risk_pct":null,"regime":"MIXED","ems":86,"ffs":95,"cds":98,"ias":89,"cbs":88,"mes":96,"invalidation":"wait_for_ES_hold_7740_7760_with_US10Y_below_5.20_or_break_below_7700_with_VIX_above_17","verification_target":"ESZ26_7700_7740_7760_7770_US10Y_VIX_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-10-01","signal_id":"20261001_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":96,"no_trade_score":87,"risk_pct":null,"regime":"MIXED","ems":89,"ffs":96,"cds":98,"ias":94,"cbs":92,"mes":96,"invalidation":"do_not_chase_overbought_NQ_wait_for_30700_30780_pullback_with_US10Y_below_5.20_and_VIX_below_15.5","verification_target":"NQZ26_30500_30700_30780_30858_US10Y_VIX_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-10-01","signal_id":"20261001_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":89,"no_trade_score":89,"risk_pct":null,"regime":"MIXED","ems":85,"ffs":94,"cds":98,"ias":85,"cbs":85,"mes":95,"invalidation":"wait_for_DXY_break_above_101.7_or_failure_below_100.8_with_yield_confirmation","verification_target":"DXY_100.8_101.47_101.7_US10Y_USDJPY_1d_3d","verified_status":"verified"},
  {"date":"2026-10-01","signal_id":"20261001_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":99,"no_trade_score":97,"risk_pct":null,"regime":"EVENT","ems":99,"ffs":99,"cds":99,"ias":98,"cbs":98,"mes":99,"invalidation":"do_not_chase_long_end_yield_wait_for_rejection_below_5.20_or_sustained_break_above_5.30_after_jobs_data","verification_target":"US10Y_5.20_5.29_5.30_jobs_NQ_GOLD_DXY_1d_3d","verified_status":"verified"},
  {"date":"2026-10-01","signal_id":"20261001_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":87,"no_trade_score":88,"risk_pct":null,"regime":"MIXED","ems":81,"ffs":92,"cds":97,"ias":82,"cbs":82,"mes":91,"invalidation":"wait_for_VIX_break_above_17_or_return_below_15.5_with_ES_NQ_confirmation","verification_target":"VIX_15.5_16.34_17_ES_NQ_US10Y_1d_3d","verified_status":"verified"}
]
```

本日の中心は、**「Soft PCEなのに長期金利が下がらなかった」こと**です。Fed利上げ確率は大幅に落ちた一方、10年・30年債利回りは高止まりしました。短期金利と長期金利が別方向へ動いているため、NASDAQ・Gold・DXYを単純な「Fedハト派化」で追うのは避けます。

BTCは5営業日ルールに従って終了。代表値では約**-0.19R**で、SL直前からかなり戻しての時間決済でした。WTI SELLだけが現在の未決着方向判断です。
