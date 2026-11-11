<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-30 07:00 JST -->
<!-- transport: Codex read_thread; message e39d8cb0-b1ce-49e6-aee6-6bad149281a9; truncated=false -->
<!-- archived_at: 2026-09-29T23:02:52Z / chars: 18968 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-09-30

**使用モデル：GPT-5.6 Sol**  
**本日の市場の主役：US10Y**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**データ基準：2026年9月29日米国市場終了後〜9月30日06:55 JST前後。先物・Cryptoの一部は遅延値／複数データベンダー照合。**

**crypto_grounds: etf=有, cme=有** — 最新確定ETFフローとして9月28日のBTC **+31.0Mドル**、ETH **+17.1Mドル**を使用。BTCの9月29日ETFフローは今朝時点で全銘柄確定を確認できていないため未使用。CME BTCは9月29日に概ね**83.1k–84.9k**のレンジを確認。:chatgpt-content-reference{index="0"}

**expected_r_basis: subjective** — 新規WTI SELL_PULLBACKは二点分布なら約`+0.58R`だが、未約定確率、中東ヘッドラインによる逆行、PCE当日のクロスアセット変動を織り込み`expected_r=0.39`まで下げる。既存BTCの発行時`expected_r=0.40`は変更しない。

**invalidation_check: 20260924_BTC_BUY_PULLBACK=not_fired, 20260930_WTI_SELL_PULLBACK=not_fired**

今日の最大イベントは**米PCE**です。BEA公式スケジュールでは9月30日08:30 ET、**日本時間21:30**にAugust Personal Income and Outlaysが公表され、同時刻にQ2 GDP第三次推計も出ます。:chatgpt-content-reference{index="1"}

[BEA 9月30日公式リリース予定](https://www.bea.gov/news/schedule/full?utm_source=chatgpt.com)  
[Reuters：9月29日の米株・債券市場](https://www.reuters.com/business/us-stock-futures-flat-tech-bounce-meets-crude-driven-caution-2026-09-29/)  
[Reuters：9月29日のWTIと中東原油輸出](https://www.reuters.com/business/energy/oil-prices-rise-second-session-continued-middle-east-supply-concern-2026-09-29/)

## 1. 本日の結論

**新規A級：0件**

**新規B級：1件 — WTI SELL_PULLBACK**

**B+観察候補：WTI SELL_PULLBACK**

**既存B：BTC BUY_PULLBACK — not_fired、ただし本日が5営業日目**

その他8資産は**NO_TRADE**です。

昨日の米市場で最も重要だったのは、米10年債利回りが一時**5.293%**まで上昇した一方、弱いJOLTSと消費者信頼感、さらにNY連銀Williamsの「追加利上げを急ぐ必要はない」との発言で利上げ確率が約70%から**51.5%**まで低下したことです。つまり金利は極端に高いものの、ここからさらに一方向に上がるという確信度は低下しました。:chatgpt-content-reference{index="5"}

そのため、GOLD・NASDAQ・DXY・US10Yは**PCE前に方向を作らない**判断です。

一方、WTIは事情が違います。9月29日のNovember WTIは**89.38ドル、-3.5%**まで下落。Saudi East-West Pipelineの流量増加、Yanbuからの積み出し再開、中東産油国の9月輸出量が**16.328mbpdと戦争開始後最大**まで回復したことが、これまでの供給不足プレミアムを実際に崩しています。:chatgpt-content-reference{index="6"}

これは単なるチャート下落ではなく、**前回WTI BUYを失敗させた「実効供給回復」仮説がさらに強化された**という点が重要です。

ただし89.38からSELLは追いません。

新規：

**`20260930_WTI_SELL_PULLBACK`**

Entry：**90.30–91.10**  
Mid：**90.70**  
SL：**92.40**  
TP1：**87.50**  
TP2：**85.60**

RR：

\[
(90.70-87.50)/(92.40-90.70)
=3.20/1.70
=1.88
\]

**win_prob：0.55**  
**較正後参考：0.56**  
**expected_r：0.39**  
**MAE想定：0.31R**  
**risk_pct：0.25%**

A級ではありません。`expected_r<0.45`かつMAE想定もA基準0.25Rを超えます。

ただしB+条件のCBS、EMS、RR、win_prob、ロット制約は満たすため、**B+観察候補**とします。

XM OILCashは現行実測仕様で**1lot=100 barrels、最小0.01lot**なので最小ロットは実質1 barrel。90.70→92.40なら価格差損失は約1.70ドル、spreadを加えても概算数百円規模で、3,000円制約には十分収まります。:chatgpt-content-reference{index="7"}

---

## 2. 前回判断の簡易検証

### `20260924_BTC_BUY_PULLBACK`

発行値：

**Entry 83800–84600**  
**Mid 84200**  
**SL 82500**  
**TP1 87400**  
**TP2 90200**  
**RR 1.88**  
**win_prob 0.55**  
**expected_r 0.40**

新しく取得したBTC/USD現物データでは、9月28日にCoinbase系で**安値約82510**まで下げています。

つまりSL82500との差は、わずか約**10ドル**でした。:chatgpt-content-reference{index="8"}

それでも確認できた主要現物系列では82500を明確には割っていません。9月29日の安値も約**82736–82776**。現在BTCは概ね**83.4k**です。:chatgpt-content-reference{index="9"}

CME BTCも9月29日は、

**Open 83855  
High 84935  
Low 83100  
Close系 約83235–83930**

で、83000を明確には失っていません。:chatgpt-content-reference{index="10"}

よって、

**ENTRY_REACHED  
SL_NOT_REACHED  
TP1_NOT_REACHED  
invalidation=not_fired**

です。

ただし実測MAEは、

\[
(84200-82510)/(84200-82500)
\approx0.994R
\]

ほぼ**1R丸ごと逆行**しました。

発行時MAE想定0.29Rに対して大幅な過小評価です。

ETF側も弱くなっています。9月21日の+999Mドルから流入額は徐々に減り、9月28日はわずか**+31Mドル**まで縮小。ETH ETFも同日+17.1Mドルでした。:chatgpt-content-reference{index="11"}

したがって、

> **strong ETF flow / weak price response**

という先週からの警戒は、

> **ETF flow itself is now decelerating**

へ一段悪化しました。

ただしSLは未達なので、推測で`fired`にはしません。

そして今日はシグナル発行後**5営業日目**です。

したがって既存BTCは、

**SL82500維持  
追加BUY禁止  
本日9月30日の時間決済で終了**

とします。

---

## 3. 市場全体の前提

市場全体は**EVENT / MIXED**です。

米10年債は9月29日に一時**5.293%**と2007年以来の高水準。30年債も5.62%まで上昇しました。ところが弱いJOLTS・消費者信頼感とWilliams発言を受け、利回りは高値から低下しました。JOLTS求人件数は**7.079M**で市場予想7.225Mを下回っています。:chatgpt-content-reference{index="12"}

株式は完全崩壊していません。

現物は、

**S&P500 -0.17%**  
**Nasdaq Composite -0.08%**

でした。:chatgpt-content-reference{index="13"}

しかし先物ではESZ26が約**7721**、NQZ26が約**30507**まで低下。9月25日のES7804、NQ30889から見ると、高金利耐性は徐々に削られています。:chatgpt-content-reference{index="14"}

VIXも**16.4前後**。まだ本格的panicではありませんが、先週の14台からは明確にrisk premiumが増えています。:chatgpt-content-reference{index="15"}

DXYは約**101.35**、USDJPYは約**157.5**。DXYは強い一方、USDJPYは159円へ戻らず、円安政策リスクが依然上値を抑えています。:chatgpt-content-reference{index="16"}

GoldのGCZ26は9月28日の大幅下落後、9月29日は約**4179**へ小反発。日中安値は約4145です。複数データ取得地点で清算値に10～20ドル程度の差があるため`partially_verified`とします。:chatgpt-content-reference{index="17"}

WTIだけはかなり明確です。

**89.38ドル**
まで下落し、Saudi輸送回復という物理的根拠も確認されています。さらに米政府はSPRから最大4,000万バレルを貸し出す計画も発表しており、短期の供給制約を緩和する方向です。:chatgpt-content-reference{index="18"}

---

## 4. 10資産別判断

| 資産 | 本日判断 | 評価 |
|---|---|---|
| **GOLD** | **NO_TRADE** | GCZ26約4179。マクロは弱気だがPCE前＋急落直後。 |
| **BTC** | **既存B管理 / 新規NO_TRADE** | 約83.4k。SL82500未達。本日時間決済。 |
| **ETH** | **NO_TRADE** | 約2.69–2.70k。BTCより価格安定だが独立edge不足。:chatgpt-content-reference{index="19"} |
| **WTI** | **B SELL_PULLBACK / B+** | Nov-26 89.38。90.30–91.10への戻りだけSELL。 |
| **USDJPY** | **NO_TRADE** | 約157.5。156.5割れなし、158超定着もなし。 |
| **SPX** | **NO_TRADE** | ESZ26約7721。PCE前、7700支持確認待ち。 |
| **NASDAQ** | **NO_TRADE** | NQZ26約30507。30300は未割れ、しかし金利条件悪化。 |
| **DXY** | **NO_TRADE** | 101.35。上方向だがPCE直前で追わない。 |
| **US10Y** | **NO_TRADE** | 一時5.293%。主役だがPCE直前の極端値。 |
| **VIX** | **NO_TRADE** | 約16.4。risk premium上昇中だが17超未確認。 |

---

## 5. A級候補

**なし。**

WTI SELLが最も方向性のある候補ですが、Aにはしません。

二点分布なら、

\[
0.55\times1.88-(1-0.55)
=+0.584R
\]

ですが、実際には、

- Entry 90.30–91.10へ戻らずそのまま下落する非約定
- Iran/Houthi/Saudi関連ヘッドラインで急騰するテール
- 89ドル台で既にかなり下落している
- MAE想定0.31R

を考慮し、subjective expected_rを**0.39R**としています。

A級基準`0.45R`未満です。

NASDAQ BUYもまだ再開しません。

NQは30507まで下げましたが、US10Yが5.2%台、VIX16台なので、まだ「健全な押し」とは言えません。

---

## 6. B級監視候補

### `20260930_WTI_SELL_PULLBACK` — B / B+

**Entry：90.30–91.10**  
**Mid：90.70**  
**SL：92.40**  
**TP1：87.50**  
**TP2：85.60**  
**RR：1.88**  
**win_prob：0.55**  
**較正後参考：0.56**  
**expected_r：0.39**  
**MAE想定：0.31R**  
**risk_pct：0.25%**

背景は明確です。

Saudi ArabiaのEast-West Pipeline復旧とYanbu輸出再開により、中東原油輸出量は戦争開始後最高へ回復しました。9月29日のWTIは3.5%下落しています。:chatgpt-content-reference{index="20"}

ただし現在89.38なので**成行SELLは禁止**。

90.30～91.10へ戻し、

**91ドル付近で上値失速**
＋
**Saudi輸出回復ニュースが維持**
＋
**新しい大型供給障害なし**

の場合だけシグナル成立です。

`92.40`を超えたら、

**「89ドル割れが単なるovershootだった」**

として失効。

XM OILCash最小ロット想定損失も3,000円を大幅に下回るため、ロット制約上はB+条件を満たします。:chatgpt-content-reference{index="21"}

---

## 7. 触らない資産

今日は特に**GOLD、DXY、US10Y、NASDAQ**です。

すべて21:30 JSTのPCEで直接動く可能性が高いからです。

Goldは高金利・ドル高でSELL方向ですが、9月28日に約3%下落した直後。今からSELLするより、**4200–4230へ戻ったところ**を観察する方がEntry品質が高いです。

DXYも101.35まで上昇していますが、JOLTS悪化とWilliams発言でFed追加利上げ確率が大きく低下しました。強いPCEなら上へ、弱いPCEなら急反落し得ます。:chatgpt-content-reference{index="22"}

US10Yも同様です。5.293%を追う場所ではありません。

NASDAQはESより相対的に耐えていますが、NQ30500近辺では金利方向が決まらない限りedgeが薄いです。

---

## 8. 後日検証ポイント

### BTC

本日が時間決済日です。

**82500 → fired**  
**87400 → TP1**  
**90200 → TP2**  
**2026-09-30 → TIME_EXIT**

9月28日安値は取得系列によって**82510～82560**。

つまりほぼSLまで行きましたが、現在確認できる主要現物系列ではわずかに割っていません。:chatgpt-content-reference{index="23"}

今回の較正結果はかなり明確です。

**予想MAE：0.29R**  
**実測最大MAE：約0.99R**

そして、

**ETF 9/21：+999M  
9/22：+714.7M  
9/23：+347M  
9/24：+190.7M  
9/25：+134.5M  
9/28：+31M**

と、資金流入の**方向は正でも速度が急減**しました。:chatgpt-content-reference{index="24"}

今後のCrypto押し目モデルでは、

**ETF flowの符号**
ではなく、

**ETF flow acceleration / deceleration**

を独立特徴量として入れる価値があります。

### WTI

新規シグナル。

**90.30–91.10 → Entry**  
**92.40 → fired**  
**87.50 → TP1**  
**85.60 → TP2**

89ドルから下へそのまま走った場合は**見送ります**。

「取り逃がしたから89ドルでSELL」は禁止です。

### NASDAQ

NQZ26は約30507。

新しい条件：

**NQ >30650**
＋
**US10Y <5.18**
＋
**VIX <15.5**

ならBUY再評価。

**NQ <30300**
＋
**VIX >17**

ならRISK_OFF側へ一段変更します。

### SPX

ESZ26約7721。

**7700**が重要です。

ここを維持し、PCE後にUS10Yが下がればBUY側再評価。

**7700割れ＋VIX17超**
なら高金利耐性仮説はかなり弱まります。

### GOLD

GCZ26約4179。

次のSELL候補は、

**4200–4230へ戻す**
＋
**US10Y >5.20**

です。

逆にPCE後にUS10Yが5.10を割り、Goldが4230超へ戻るならSELL仮説を破棄します。

### USDJPY

現在約157.5。

**156.50割れ**
→ 円高regime候補。

**158.00～158.50回復**
→ 金利差優勢へ戻る。

PCE前の157円台中央ではNO_TRADEです。

---

## 9. Obsidian保存用 Observation Draft

```markdown
# 2026-09-30 WTI Supply Recovery / BTC Time Exit / PCE Event

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

## Sep29 macro

US10Y:
intraday high ~5.293%

30Y:
~5.62%

JOLTS:
7.079m
below 7.225m expectation

Fed Oct hike probability:
~70%
-> ~51.5% after Williams comments

PCE:
2026-09-30
21:30 JST

## Market references

GCZ26:
~4179

BTC:
~83400

ETH:
~2700

WTI Nov:
89.38

USDJPY:
~157.5

ESZ26:
~7721

NQZ26:
~30507

DXY:
~101.35

VIX:
~16.4

## BTC active

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

Lowest verified spot:
~82510

Observed MAE:
~0.99R

Issue MAE estimate:
0.29R

Status:
ENTRY_REACHED
SL_NOT_REACHED
TP1_NOT_REACHED
not_fired

Time exit:
2026-09-30

No add.
No SL widening.

## BTC flow calibration

BTC ETF:

Sep21 +999m
Sep22 +714.7m
Sep23 +347m
Sep24 +190.7m
Sep25 +134.5m
Sep28 +31m

Observation:

flow stayed positive
but marginal institutional bid collapsed.

New research candidate:
ETF flow acceleration/deceleration
not just positive/negative flow.

## New WTI signal

20260930_WTI_SELL_PULLBACK

Rank:
B

B+:
YES

Reference:
WTI Nov-26

Current:
89.38

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

calibrated:
0.56

two-point EV:
~0.58R

subjective expected_r:
0.39R

MAE estimate:
0.31R

risk:
0.25%

Drivers:
Saudi East-West Pipeline recovery
Yanbu loadings resumed
Middle East exports 16.328mbpd
highest since war began

Execution:
do not chase below entry
wait for rebound

## PCE rule

Do not create:
GOLD chase
DXY chase
US10Y chase
NASDAQ chase

before 21:30 JST PCE.

## Active invalidation

20260924_BTC_BUY_PULLBACK=not_fired
20260930_WTI_SELL_PULLBACK=not_fired

## New signals

A:
NONE

B:
WTI SELL_PULLBACK

B+:
WTI SELL_PULLBACK

#TSO #WTI #BTC #US10Y #PCE #NASDAQ #GOLD
```

---

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-30,20260930_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,93,95,,EVENT,94,97,99,91,91,98,wait_for_PCE_then_GCZ26_rebound_4200_4230_or_reclaim_above_4230_with_US10Y_confirmation,GCZ26_4145_4179_4200_4230_US10Y_DXY_PCE_1d_3d,partially_verified
2026-09-30,20260930_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,97,79,,EVENT,91,97,99,95,91,95,manage_existing_20260924_BUY_SL82500_not_fired_time_exit_20260930_no_add,BTC_82500_82510_83100_83400_87400_ETF_CME_time_exit,partially_verified
2026-09-30,20260930_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,87,89,,MIXED,82,92,97,85,84,89,wait_for_ETH_break_2630_or_reclaim_2750_after_PCE_with_BTC_confirmation,ETH_2630_2687_2700_2750_ETF_CME_PCE_1d_3d,partially_verified
2026-09-30,20260930_WTI_SELL_PULLBACK,WTI,SELL,B,PULLBACK,90.30,91.10,92.40,87.50,85.60,1.88,0.55,0.39,99,96,42,0.25,EVENT,72,94,97,88,83,95,WTI_above_92.40_or_new_confirmed_major_supply_disruption_invalidates_supply_recovery_thesis,WTI_Nov26_89.38_90.30_91.10_92.40_87.50_Saudi_Yanbu_exports_1d_3d_5d,verified
2026-09-30,20260930_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,91,91,,EVENT,89,96,99,90,88,97,wait_for_clean_break_below_156.5_or_reclaim_158_158.5_after_PCE_before_new_signal,USDJPY_156.5_156.98_157.52_158_158.5_DXY_US10Y_PCE_1d_3d,verified
2026-09-30,20260930_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,94,91,,EVENT,90,96,99,91,89,97,wait_for_ES_hold_or_break_7700_after_PCE_with_VIX_US10Y_confirmation,ESZ26_7700_7712.5_7721_7767.5_US10Y_VIX_PCE_1d_3d,verified
2026-09-30,20260930_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,95,91,,EVENT,91,96,99,93,91,97,wait_for_NQ_above_30650_with_US10Y_below_5.18_or_break_below_30300_with_VIX_above_17,NQZ26_30300_30433_30507_30650_US10Y_VIX_PCE_1d_3d,verified
2026-09-30,20260930_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,93,92,,EVENT,92,97,99,91,90,98,do_not_chase_101.35_before_PCE_wait_for_hold_above_101.5_or_failure_below_100.8,DXY_100.8_101.35_101.5_US10Y_PCE_1d_3d,verified
2026-09-30,20260930_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,99,98,,EVENT,99,99,99,98,98,99,do_not_chase_5.29_wait_for_PCE_rejection_below_5.15_or_sustained_break_above_5.30,US10Y_5.15_5.246_5.293_5.30_PCE_NQ_GOLD_DXY_1d_3d,verified
2026-09-30,20260930_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,90,89,,EVENT,86,94,98,86,85,93,wait_for_VIX_break_above_17_or_return_below_15.5_after_PCE_with_ES_NQ_confirmation,VIX_15.5_16.4_17_ES_NQ_US10Y_PCE_1d_3d,verified
```

### TSO_LOG JSON

```json
[
  {"date":"2026-09-30","signal_id":"20260930_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":93,"no_trade_score":95,"risk_pct":null,"regime":"EVENT","ems":94,"ffs":97,"cds":99,"ias":91,"cbs":91,"mes":98,"invalidation":"wait_for_PCE_then_GCZ26_rebound_4200_4230_or_reclaim_above_4230_with_US10Y_confirmation","verification_target":"GCZ26_4145_4179_4200_4230_US10Y_DXY_PCE_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-30","signal_id":"20260930_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":97,"no_trade_score":79,"risk_pct":null,"regime":"EVENT","ems":91,"ffs":97,"cds":99,"ias":95,"cbs":91,"mes":95,"invalidation":"manage_existing_20260924_BUY_SL82500_not_fired_time_exit_20260930_no_add","verification_target":"BTC_82500_82510_83100_83400_87400_ETF_CME_time_exit","verified_status":"partially_verified"},
  {"date":"2026-09-30","signal_id":"20260930_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":87,"no_trade_score":89,"risk_pct":null,"regime":"MIXED","ems":82,"ffs":92,"cds":97,"ias":85,"cbs":84,"mes":89,"invalidation":"wait_for_ETH_break_2630_or_reclaim_2750_after_PCE_with_BTC_confirmation","verification_target":"ETH_2630_2687_2700_2750_ETF_CME_PCE_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-30","signal_id":"20260930_WTI_SELL_PULLBACK","asset":"WTI","side":"SELL","rank":"B","type":"PULLBACK","entry_low":90.30,"entry_high":91.10,"sl":92.40,"tp1":87.50,"tp2":85.60,"rr":1.88,"win_prob":0.55,"expected_r":0.39,"tq_score":99,"opp_score":96,"no_trade_score":42,"risk_pct":0.25,"regime":"EVENT","ems":72,"ffs":94,"cds":97,"ias":88,"cbs":83,"mes":95,"invalidation":"WTI_above_92.40_or_new_confirmed_major_supply_disruption_invalidates_supply_recovery_thesis","verification_target":"WTI_Nov26_89.38_90.30_91.10_92.40_87.50_Saudi_Yanbu_exports_1d_3d_5d","verified_status":"verified"},
  {"date":"2026-09-30","signal_id":"20260930_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":91,"no_trade_score":91,"risk_pct":null,"regime":"EVENT","ems":89,"ffs":96,"cds":99,"ias":90,"cbs":88,"mes":97,"invalidation":"wait_for_clean_break_below_156.5_or_reclaim_158_158.5_after_PCE_before_new_signal","verification_target":"USDJPY_156.5_156.98_157.52_158_158.5_DXY_US10Y_PCE_1d_3d","verified_status":"verified"},
  {"date":"2026-09-30","signal_id":"20260930_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":94,"no_trade_score":91,"risk_pct":null,"regime":"EVENT","ems":90,"ffs":96,"cds":99,"ias":91,"cbs":89,"mes":97,"invalidation":"wait_for_ES_hold_or_break_7700_after_PCE_with_VIX_US10Y_confirmation","verification_target":"ESZ26_7700_7712.5_7721_7767.5_US10Y_VIX_PCE_1d_3d","verified_status":"verified"},
  {"date":"2026-09-30","signal_id":"20260930_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":95,"no_trade_score":91,"risk_pct":null,"regime":"EVENT","ems":91,"ffs":96,"cds":99,"ias":93,"cbs":91,"mes":97,"invalidation":"wait_for_NQ_above_30650_with_US10Y_below_5.18_or_break_below_30300_with_VIX_above_17","verification_target":"NQZ26_30300_30433_30507_30650_US10Y_VIX_PCE_1d_3d","verified_status":"verified"},
  {"date":"2026-09-30","signal_id":"20260930_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":93,"no_trade_score":92,"risk_pct":null,"regime":"EVENT","ems":92,"ffs":97,"cds":99,"ias":91,"cbs":90,"mes":98,"invalidation":"do_not_chase_101.35_before_PCE_wait_for_hold_above_101.5_or_failure_below_100.8","verification_target":"DXY_100.8_101.35_101.5_US10Y_PCE_1d_3d","verified_status":"verified"},
  {"date":"2026-09-30","signal_id":"20260930_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":99,"no_trade_score":98,"risk_pct":null,"regime":"EVENT","ems":99,"ffs":99,"cds":99,"ias":98,"cbs":98,"mes":99,"invalidation":"do_not_chase_5.29_wait_for_PCE_rejection_below_5.15_or_sustained_break_above_5.30","verification_target":"US10Y_5.15_5.246_5.293_5.30_PCE_NQ_GOLD_DXY_1d_3d","verified_status":"verified"},
  {"date":"2026-09-30","signal_id":"20260930_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":90,"no_trade_score":89,"risk_pct":null,"regime":"EVENT","ems":86,"ffs":94,"cds":98,"ias":86,"cbs":85,"mes":93,"invalidation":"wait_for_VIX_break_above_17_or_return_below_15.5_after_PCE_with_ES_NQ_confirmation","verification_target":"VIX_15.5_16.4_17_ES_NQ_US10Y_PCE_1d_3d","verified_status":"verified"}
]
```

本日は**BTCの5営業日目**と**WTIの構造変化**が中心です。

BTCはSLをほぼ1ドル単位の誤差まで試しながら生き残りましたが、ETF流入の減速と実測MAE約1Rから、今回の押し目BUYはエントリー品質の較正材料としてかなり重要です。時間決済ルールは変更せず、本日で閉じます。

WTIは逆に、Saudi輸送の実際の回復が数字として確認され、前回BUY失敗の原因がさらに裏付けられました。ただし89ドル台を追って売らず、**90.30–91.10への戻りだけを売るB+観察候補**としています。
