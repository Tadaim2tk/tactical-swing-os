<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-18 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-21T12:59:52Z / chars: 17199 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-09-18

**使用モデル：GPT-5.6 Sol**  
**本日の市場の主役：USDJPY**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**データ基準：2026年9月17日米国市場終了後〜9月18日06:59 JST。遅延値・終値を含む。**  
**crypto_grounds: etf=有, cme=有**  
**expected_r_basis: subjective** — 本日の新規方向シグナルは0件。既存WTIシグナルの発行時`expected_r=0.48`は未約定確率、5営業日時間決済、供給正常化リスクを織り込んだ値であり、発行済みLOGは変更しません。

**invalidation_check: 20260912_BTC_SELL_PULLBACK=not_fired, 20260917_WTI_BUY_PULLBACK=not_fired**

BTCは本日が5営業日確認の最終日。WTIは実取引で約定済みのため継続管理です。

9月17日の米市場では、WTIが**101.91ドル**まで戻して終了し、一時100ドルを割った下落のかなりの部分を回復しました。Saudi/Oman経由の追加供給とEast-West pipelineの復旧期待は弱材料ですが、実際の修理時期はなお不明で、Hormuzのタンカー交通も低調なままです。したがって昨日のWTI BUYのinvalidationはまだ発動していません。citeturn371053view1

一方、米10年債利回りは5.00%台から**4.94～4.95%**へ低下し、株は大幅反発。S&P500現物+1.14%、Nasdaq Composite+1.69%、VIXも15台へ低下しました。FOMC後に見ていた「高金利→NASDAQ下落」の単純な連鎖は、かなり弱くなっています。citeturn371053view2turn213762view1turn395295search2

そして今日はBOJです。Reutersの事前予想では**1.00%→1.25%への25bp利上げ**が中心で、市場は利上げそのものより植田総裁が今後の利上げペースをどこまで示唆するかを見ています。citeturn371053view3

url9月17日のWTI市場（Reuters）https://www.reuters.com/business/energy/oil-prices-extend-losses-fears-middle-east-supply-disruptions-ease-2026-09-17/  
url9月17日の世界市場（Reuters）https://www.reuters.com/world/china/global-markets-global-markets-2026-09-17/  
url9月18日のBOJ見通し（Reuters）https://www.reuters.com/world/asia-pacific/boj-set-raise-interest-rates-31-year-high-inflation-risks-loom-2026-09-16/

## 1. 本日の結論

**新規A級：0件**  
**新規B級：0件**  
**新規B+：0件**  
**既存Bポジション：WTI BUYを継続管理**  
**残り9資産：新規NO_TRADE**

今日は「方向が分からない」日ではありません。

むしろ昨夜は、

**WTI↓ → US10Y↓ → VIX↓ → NQ/SPX↑**

というかなり明瞭なrisk-on反応でした。

NQZ26は9月17日を**29725.5**、ESZ26は**7699.5**付近で終了しています。NQは+1.60%、ESは+1.00%程度でした。citeturn893419search2turn179160search4

ただし今日はBOJです。

したがってNASDAQ BUY、USDJPY SELL/BUY、US10Y SELLなどを**BOJ直前に新規発行することはしません**。

昨日の「イベント前だから入らない」と同じ理由です。

### 既存WTI実取引

ユーザー実取引：

**OILCash Entry：約101.19**  
**SL：98.90**  
**TP：105.20へ変更済み**

TSO参照系列はWTI先物なので、XMのOILCash価格と完全一致させません。

WTI先物の9月17日清算値は**101.91**。したがって参照系列上ではEntry水準を上回って米国市場を終了しました。citeturn371053view1

実取引RRは、

\[
(105.20-101.19)/(101.19-98.90)=1.75
\]

です。

**現時点：HOLD。SL98.90は広げない。TP105.20も維持。**

---

## 2. 前回判断の簡易検証

### 20260917_WTI_BUY_PULLBACK

発行条件：

**Entry 100.80–101.60**  
**SL 98.90**  
**TP1 105.20**  
**TP2 108.00**  
**RR 1.74**  
**win_prob 0.61**  
**expected_r 0.48**

実際にユーザー口座で約101.19で約定。

9月17日はSaudi/Oman追加供給のニュースでWTIが一時100ドルを割りましたが、終値は**101.91ドル**まで回復しました。Reutersによれば、追加供給は一部不足を補う一方、East-West pipelineでは3つのポンプ施設が損傷し修理時期は不明、Hormuzのタンカー交通も低水準です。citeturn371053view1

したがって、

**ENTRY_FILLED / SL_NOT_REACHED / TP_NOT_REACHED / invalidation=not_fired**

です。

特に重要なのは、

**「供給正常化ニュースが出たのに100ドル割れを維持できなかった」**

という価格反応です。

昨日16時時点よりBUY仮説にはややプラスです。

ただし105.20までの確率を大幅に上げるほどではありません。**現時点主観55～60%程度**を維持します。

### 20260912_BTC_SELL_PULLBACK

既存：

**Entry 79200–79800**  
**SL 80850**  
**TP1 76450**  
**TP2 74800**

9月15日のCME BTC安値は**74925**。

つまり、

**TP1 76450 → 到達**  
**TP2 74800 → わずか125ドル届かず**

でした。citeturn974534search2

9月17日のCME BTCは、

**Open 76230  
High 77182.5  
Low 75935  
Close 76587**

で、80850のinvalidationには遠いままです。citeturn974534search2

最新確定ETFフローは9月16日でBitcoin ETF **-295.9Mドル**、Ether ETF **-224.1Mドル**。9月17日分については今朝の検索時点で確定値を十分に検証できませんでした。citeturn565652search6

したがって、

**20260912_BTC_SELL_PULLBACK=not_fired**

です。

本日で5営業日窓を終了します。

評価は、

**方向成功 / TP1到達 / TP2未達 / invalidation発動なし**

です。

---

## 3. 市場全体の前提

昨日までの中心仮説、

**原油高 → インフレ → US10Y 5% → NASDAQ下**

に明確な変化が入りました。

WTIが105ドル台から101.91まで低下し、10年債利回りも9月16日の5.004%から9月17日は**4.952%**へ低下しました。citeturn371053view1turn770182search4

その結果、

**S&P500 +1.14%**  
**Nasdaq +1.69%**  
**SOX +3%以上**  
**VIX 約15.9**

となりました。citeturn213762view1turn395295search2

これはかなり強いrisk-on反応です。

Goldも反転しました。

COMEX 2026年12月限は**4399.70ドル**で清算。現物金も一時4360ドル付近まで上昇しました。ドルと米金利の低下が主因です。citeturn371053view5

Cryptoも少し反発しています。

BTC現物は約**76.3k**、CME BTCは**76587**。ETH現物は約**2440台**、CME ETHは**2453.5**です。citeturn213762news10turn974534search2turn213762news23turn735941search6

ただしETF需要は直近では弱いので、Cryptoをrisk-onだけでBUYするほどではありません。

USDJPYは約**155.97**。DXYはデータ提供元に若干差がありますが約**100.3**です。citeturn371053view2turn212658search4

今日はここへBOJが入ります。

総合regimeは、**MIXED → BOJ前のEVENT**です。

---

## 4. 10資産別判断

| 資産 | 判断 | 基準値と見方 |
|---|---|---|
| GOLD | **NO_TRADE** | GCZ26 **4399.7**。金利低下で強く反発したが一日で追わない。citeturn371053view5 |
| BTC | **NO_TRADE / 既存SELL最終確認** | spot約76.3k、CME **76587**。ETF流出は弱材料だが新規SELLは遅い。citeturn974534search2turn565652search6 |
| ETH | **NO_TRADE** | spot約2440台、CME **2453.5**。反発したがETF需給は弱い。citeturn735941search6 |
| WTI | **既存BUY HOLD / 新規NO_TRADE** | **101.91**。100割れから戻す。既存101.19 BUYを管理。citeturn371053view1 |
| USDJPY | **NO_TRADE** | 約**155.97**。本日BOJ。方向よりイベント結果を待つ。citeturn371053view2turn371053view3 |
| SPX | **NO_TRADE** | ESZ26 **7699.5**、+1%。risk-onだが反発後を追わない。citeturn179160search4 |
| NASDAQ | **NO_TRADE** | NQZ26 **29725.5**、+1.6%。昨日のSELL仮説は弱体化。citeturn893419search2 |
| DXY | **NO_TRADE** | 約**100.3**。BOJ前でUSDJPYと同様にevent-dependent。citeturn212658search4 |
| US10Y | **NO_TRADE** | **4.952%**。5%拒否は明瞭だがBOJが世界金利を動かし得る。citeturn770182search4 |
| VIX | **NO_TRADE** | 約**15.9**。17.71から大幅低下。risk-offは一旦解除。citeturn395295search2 |

---

## 5. A級候補

**なし。**

数値だけならNASDAQ BUY方向が最も改善しました。

NQZ26は前日安値圏から**29725.5**へ反発し、US10Yは4.95%へ低下、VIXは15台です。citeturn893419search2turn770182search4turn395295search2

しかし今ここでBUYすると、

**「Fed後の反発を1.6%上昇した後から追う」**

ことになります。

TSOのEntry品質基準では不合格です。

さらに数時間後にBOJ。

したがってAにはしません。

---

## 6. B級監視候補

**新規B級なし。**

ただし、既存BとしてWTIを継続します。

### 既存 `20260917_WTI_BUY_PULLBACK`

実約定：

**101.19**

現在の実取引設定：

**SL 98.90**  
**TP 105.20**  
**RR 1.75**

現時点では**HOLD**。

今回の重要な観察は、

**Saudi/Oman供給緩和ニュース**
↓
**WTI一時100割れ**
↓
**終値101.91**

です。citeturn371053view1

弱材料に対して下値が続かなかったのはBUY側に有利です。

ただし、

**East-West pipelineの実際の復旧確認**
＋
**Hormuz交通の正常化**

が同時に出れば、98.90到達前でもシナリオを再評価します。

**SLを広げる変更はしません。**

---

## 7. 触らない資産

今日は特に**USDJPY、DXY、US10Y**です。

理由は全てBOJ。

市場は1.25%への利上げをほぼ前提にしているため、重要なのは利上げそのものではありません。Reutersによれば、焦点は植田総裁が今後の利上げ時期・ペースについてどこまで示すかです。citeturn371053view3

したがって、

**1.25%利上げ＋曖昧なガイダンス**
→ 円売りの可能性

**1.25%利上げ＋追加利上げを強く示唆**
→ 円買いの可能性

の両方があります。

155.9付近から事前に賭ける必要はありません。

NASDAQも今朝は触りません。

方向は昨日より明確に**上寄り**へ変化しましたが、NQが既に1.6%上昇した後です。

「上がりそうだから買う」ではなく、**上方向の仮説を持ったまま良いEntryを待つ**のがTSOです。

---

## 8. 後日検証ポイント

最重要はBOJ後の**USDJPY × JGB × US10Y**です。

### BOJシナリオ

**USDJPY <154.50**
＋
日本10年債利回り上昇

なら、

**BOJ tightening → JPY BUY**

が素直に機能していると判断。

逆に、

**利上げしたのにUSDJPY >156.50**

なら、

**「1.25%は完全織込み＋ガイダンス不足」**

と判断します。

この場合、新しいUSDJPY BUY仮説の候補になります。

### NASDAQ

現在NQZ26 29725付近。

BOJ後も、

**NQ >29600**
＋
**US10Y <4.97**
＋
**VIX <16.5**

なら、昨日のrisk-on反転は本物である可能性が高まります。

その場合、次の押し目でBUYを再検討します。

逆に、

**NQ <29350**
＋
**US10Y >5.02**

なら昨日の反発はshort-covering主体だったと判断します。

### WTI

実取引で最重要。

**105.20 → 利確**

**98.90 → SL / シナリオ失効**

その間では、

**100～101を再度試しても割れない**
＋
供給制約継続

ならBUY仮説支持。

**East-West pipeline半分復旧確認**
＋
Hormuz船舶数正常化
＋
WTI <100

なら、98.90以前のinvalidation候補です。

### BTC

本日で5営業日窓終了。

`20260912_BTC_SELL_PULLBACK`は、

**Entry到達**
**TP1到達**
**TP2ほぼ到達**
**invalidationなし**

なので、研究上はかなり質の良い方向判断でした。

明日からinvalidation_check対象から外します。

---

## 9. Obsidian保存用 Observation Draft

```markdown
# 2026-09-18 BOJ Day / Post-Fed Risk-On / WTI Position Active

Model:
GPT-5.6 Sol

Market protagonist:
USDJPY

Gold reference:
COMEX Dec-2026 / GCZ26

crypto_grounds:
etf=有
cme=有

expected_r_basis:
subjective

## Regime

EVENT
underlying tone:
RISK_ON recovery

## US close Sep17

WTI:
101.91

US10Y:
4.952%

GCZ26:
4399.70

ESZ26:
7699.50

NQZ26:
29725.50

DXY:
~100.3

USDJPY:
~155.97

VIX:
~15.9

BTC spot:
~76.3k

CME BTC:
76587

ETH spot:
~2440

CME ETH:
2453.5

## Main change

Previous macro chain:

WTI up
-> inflation
-> US10Y up
-> Nasdaq down

weakened materially.

Sep17:

WTI down
US10Y down
VIX down
NQ +1.6%
ES +1.0%

Price action contradicts continuing Nasdaq SELL thesis.

## BOJ

Expected:
1.00% -> 1.25%

Main variable:
Ueda guidance on future hikes

Do not pre-position.

USDJPY <154.50:
yen tightening thesis strengthens

USDJPY >156.50 despite hike:
BOJ disappointment / USDJPY BUY thesis candidate

## WTI actual trade

TSO:
20260917_WTI_BUY_PULLBACK

User execution:
OILCash

Entry:
~101.19

SL:
98.90

TP:
105.20

RR:
1.75

WTI futures Sep17 settle:
101.91

News:
Saudi crude via Oman
East-West pipeline repair effort

Counterpoint:
repair timeline unclear
Hormuz traffic remains constrained
physical market still tight

Status:
HOLD

invalidation:
not_fired

Do not widen SL.

## BTC final review

20260912_BTC_SELL_PULLBACK

Entry:
79200-79800

TP1:
76450 reached

TP2:
74800

CME Sep15 low:
74925

missed TP2 by:
125

CME Sep17 close:
76587

SL:
80850 not reached

Final:
direction success
not_fired
5-business-day window complete

Remove from invalidation_check tomorrow.

## Active invalidation

20260912_BTC_SELL_PULLBACK=not_fired
20260917_WTI_BUY_PULLBACK=not_fired

## New signals

A:
NONE

B:
NONE

Existing B:
WTI BUY active

#TSO #BOJ #WTI #USDJPY #NASDAQ #BTC
```

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-18,20260918_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,82,76,,MIXED,78,84,91,80,81,74,wait_for_post_BOJ_yield_DXY_confirmation_before_new_gold_signal,GCZ26_4350_4399.7_4450_US10Y_DXY_1d_3d,verified
2026-09-18,20260918_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,78,80,,MIXED,72,83,90,79,78,68,existing_20260912_sell_final_day_not_fired,BTC_74800_76450_76587_79200_80850_ETF_CME_1d,partially_verified
2026-09-18,20260918_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,76,82,,MIXED,70,82,88,76,75,66,wait_for_2500_reclaim_or_2350_failure_with_ETF_confirmation,ETH_2350_2453_2500_ETF_CME_1d_3d,partially_verified
2026-09-18,20260918_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,90,94,,EVENT,88,92,96,87,86,90,manage_existing_20260917_BUY_SL98.90_TP105.20_no_new_entry,WTI_98.90_101.19_101.91_105.20_pipeline_Hormuz_1d_3d,verified
2026-09-18,20260918_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,94,99,,EVENT,99,98,99,94,92,99,BOJ_decision_and_Ueda_guidance_required_before_new_signal,USDJPY_154.50_155.97_156.50_BOJ_JGB_US10Y_1d,verified
2026-09-18,20260918_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,84,74,,RISK_ON,74,80,92,83,82,78,wait_for_post_BOJ_ES_pullback_or_break_confirmation,ESZ26_7620_7699.5_7750_US10Y_VIX_1d_3d,verified
2026-09-18,20260918_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,89,72,,RISK_ON,76,84,94,88,87,82,wait_for_post_BOJ_pullback_NQ_hold_29600_with_yields_below_4.97,NQZ26_29350_29600_29725.5_30000_US10Y_VIX_1d_3d,verified
2026-09-18,20260918_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,86,96,,EVENT,96,94,98,88,86,97,BOJ_USDJPY_reaction_required_before_new_DXY_signal,DXY_99.8_100.3_100.7_USDJPY_BOJ_1d,partially_verified
2026-09-18,20260918_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,88,91,,EVENT,94,93,98,87,89,96,BOJ_global_yield_reaction_required_after_5pct_rejection,US10Y_4.85_4.952_5.02_BOJ_NQ_GOLD_1d_3d,verified
2026-09-18,20260918_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,72,81,,RISK_ON,70,78,91,72,74,76,wait_for_VIX_reclaim_17_or_hold_below_16_after_BOJ,VIX_15_15.9_17_ES_NQ_1d_3d,partially_verified
```

### TSO_LOG JSON

```json
[
  {"date":"2026-09-18","signal_id":"20260918_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":99,"opp_score":82,"no_trade_score":76,"risk_pct":"","regime":"MIXED","ems":78,"ffs":84,"cds":91,"ias":80,"cbs":81,"mes":74,"invalidation":"wait_for_post_BOJ_yield_DXY_confirmation_before_new_gold_signal","verification_target":"GCZ26_4350_4399.7_4450_US10Y_DXY_1d_3d","verified_status":"verified"},
  {"date":"2026-09-18","signal_id":"20260918_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":99,"opp_score":78,"no_trade_score":80,"risk_pct":"","regime":"MIXED","ems":72,"ffs":83,"cds":90,"ias":79,"cbs":78,"mes":68,"invalidation":"existing_20260912_sell_final_day_not_fired","verification_target":"BTC_74800_76450_76587_79200_80850_ETF_CME_1d","verified_status":"partially_verified"},
  {"date":"2026-09-18","signal_id":"20260918_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":98,"opp_score":76,"no_trade_score":82,"risk_pct":"","regime":"MIXED","ems":70,"ffs":82,"cds":88,"ias":76,"cbs":75,"mes":66,"invalidation":"wait_for_2500_reclaim_or_2350_failure_with_ETF_confirmation","verification_target":"ETH_2350_2453_2500_ETF_CME_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-18","signal_id":"20260918_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":99,"opp_score":90,"no_trade_score":94,"risk_pct":"","regime":"EVENT","ems":88,"ffs":92,"cds":96,"ias":87,"cbs":86,"mes":90,"invalidation":"manage_existing_20260917_BUY_SL98.90_TP105.20_no_new_entry","verification_target":"WTI_98.90_101.19_101.91_105.20_pipeline_Hormuz_1d_3d","verified_status":"verified"},
  {"date":"2026-09-18","signal_id":"20260918_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":99,"opp_score":94,"no_trade_score":99,"risk_pct":"","regime":"EVENT","ems":99,"ffs":98,"cds":99,"ias":94,"cbs":92,"mes":99,"invalidation":"BOJ_decision_and_Ueda_guidance_required_before_new_signal","verification_target":"USDJPY_154.50_155.97_156.50_BOJ_JGB_US10Y_1d","verified_status":"verified"},
  {"date":"2026-09-18","signal_id":"20260918_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":99,"opp_score":84,"no_trade_score":74,"risk_pct":"","regime":"RISK_ON","ems":74,"ffs":80,"cds":92,"ias":83,"cbs":82,"mes":78,"invalidation":"wait_for_post_BOJ_ES_pullback_or_break_confirmation","verification_target":"ESZ26_7620_7699.5_7750_US10Y_VIX_1d_3d","verified_status":"verified"},
  {"date":"2026-09-18","signal_id":"20260918_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":99,"opp_score":89,"no_trade_score":72,"risk_pct":"","regime":"RISK_ON","ems":76,"ffs":84,"cds":94,"ias":88,"cbs":87,"mes":82,"invalidation":"wait_for_post_BOJ_pullback_NQ_hold_29600_with_yields_below_4.97","verification_target":"NQZ26_29350_29600_29725.5_30000_US10Y_VIX_1d_3d","verified_status":"verified"},
  {"date":"2026-09-18","signal_id":"20260918_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":98,"opp_score":86,"no_trade_score":96,"risk_pct":"","regime":"EVENT","ems":96,"ffs":94,"cds":98,"ias":88,"cbs":86,"mes":97,"invalidation":"BOJ_USDJPY_reaction_required_before_new_DXY_signal","verification_target":"DXY_99.8_100.3_100.7_USDJPY_BOJ_1d","verified_status":"partially_verified"},
  {"date":"2026-09-18","signal_id":"20260918_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":99,"opp_score":88,"no_trade_score":91,"risk_pct":"","regime":"EVENT","ems":94,"ffs":93,"cds":98,"ias":87,"cbs":89,"mes":96,"invalidation":"BOJ_global_yield_reaction_required_after_5pct_rejection","verification_target":"US10Y_4.85_4.952_5.02_BOJ_NQ_GOLD_1d_3d","verified_status":"verified"},
  {"date":"2026-09-18","signal_id":"20260918_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":98,"opp_score":72,"no_trade_score":81,"risk_pct":"","regime":"RISK_ON","ems":70,"ffs":78,"cds":91,"ias":72,"cbs":74,"mes":76,"invalidation":"wait_for_VIX_reclaim_17_or_hold_below_16_after_BOJ","verification_target":"VIX_15_15.9_17_ES_NQ_1d_3d","verified_status":"partially_verified"}
]
```

今日の核心は、**新規ポジションを増やさずWTIを管理すること**です。

WTIは昨日の弱材料で一時100ドルを割ったにもかかわらず101.91まで戻しており、現時点では`20260917_WTI_BUY_PULLBACK=not_fired`。実取引の**101.19 / SL98.90 / TP105.20**はそのままでよいと判断します。

一方、NASDAQについては明確に評価を変更します。**Fedが利上げした後でも、原油・金利低下を受けてNQが+1.6%反発したため、従来のNASDAQ SELL仮説は終了に近い**です。ただし今日はBOJなので、BUYへ反転して飛び乗ることもしません。

BTC SELLは本日で5営業日検証を完了し、**Entry→TP1到達、TP2まで125ドル、invalidationなし**という結果で閉じます。memcite
