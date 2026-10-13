<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-10-08 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-10-13T20:23:35Z / chars: 20266 / 値は無修正 -->

# Tactical Swing OS — Daily Signal Log v2
## 2026年10月8日（木）

**使用モデル：GPT-6**  
**本日の市場の主役：US10Y**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**データ基準：2026年10月7日米国市場終了後〜10月8日07:00 JST**

**総合regime：EVENT**

**crypto_grounds: etf=有, cme=有**

BTC・ETHともETFフローとCME先物価格を取得できました。ETFは10月6日分まで確認でき、10月7日分は未集計です。未集計を流入額ゼロとして扱いません。

**expected_r_basis: subjective**

本日発行するGOLDのexpected_rは、二点分布による期待値から、指値未約定、5営業日時間決済、イベントによる早期撤退を織り込んで引き下げています。

**invalidation_check: 20261006_WTI_SELL_PULLBACK=not_fired, 20261008_GOLD_SELL_PULLBACK=not_fired**

前者は継続監視中、後者は本日新規発行する観察シグナルです。

---

# 1. 本日の結論

| 項目 | 結果 |
|---|---|
| 新規A級 | **0件** |
| 新規B級 | **1件：GOLD SELL_PULLBACK** |
| B+観察候補 | 0件（実損・参照系列の条件未確認） |
| 既存方向シグナル | WTI SELL_PULLBACK |
| 実取引推奨 | **NO_TRADE** |
| 最大日次リスク | 0.50%維持 |

本日の中心は、**米10年債利回りが2002年以来の高水準を更新したものの、国債入札後に大きく反落したこと**です。

10月7日、米10年債利回りは一時**5.366%**まで上昇しました。

しかし39億ドルではなく、**390億ドル規模の10年債入札**が好調だったことで買い戻しが入り、最終的には約5.27%まで低下しました。

入札の応札倍率は2.77倍。直近6回平均の2.54倍を上回り、プライマリーディーラーへの配分も2.5%にとどまりました。

つまり、

**長期債への需要が消えたわけではない**

ことが確認されています。citeturn438644view0turn335562search3

一方、FOMC議事要旨はややタカ派的でした。

9月会合では、参加者の大半が年内にもう一度の利上げを適切と判断していたことが分かりました。

ただし追加利上げの理由については、エネルギー供給ショックによる物価上昇を警戒する立場と、需要主導のインフレを警戒する立場に分かれています。citeturn906301search0

この結果、現在の市場には次の矛盾があります。

**長期金利は極端に高い。**  
**しかし高利回りの国債には買い需要が戻る。**  
**株式の下落は限定的。**  
**一方でGoldとCryptoは明確に弱い。**

この不均衡を踏まえ、本日はGOLDにB級の戻り売り観察シグナルを設定します。

ただし、**現在値を成行SELLする判断ではありません。**

---

# 2. 前回判断の簡易検証

## WTI：既存B級シグナル

`20261006_WTI_SELL_PULLBACK`

前回の設定は以下です。

| 項目 | 設定 |
|---|---:|
| Entry | 90.20–90.80 |
| Mid | 90.50 |
| SL | 92.00 |
| TP1 | 87.20 |
| TP2 | 84.80 |
| RR | 2.20 |
| win_prob | 0.52 |
| expected_r | 0.34 |

10月7日のWTI先物は、

**Open：89.99**  
**High：90.98**  
**Low：88.02**  
**Settlement：88.28**

でした。citeturn335562search5turn228104news21

これは重要な変化です。

10月6日はEntry下限90.20に届かず、先にTP1の87.20を下回りました。

しかし10月7日は**90.98まで上昇したため、旧Entry帯90.20–90.80を通過**しています。

したがって研究上の状態は次のようになります。

| 判定 | 結果 |
|---|---|
| 10月6日 | TARGET_BEFORE_ENTRY |
| 10月7日 | ENTRY_ZONE_REACHED |
| SL 92.00 | 未到達 |
| 新たな供給障害による仮説崩壊 | 未確認 |
| invalidation | **not_fired** |

事前指値を有効にしていた場合、価格経路上は約定可能な水準へ到達しています。

ただし、前日のTP先行到達を受けて注文を取り消していた場合は当然未約定です。また、日足OHLCだけでは約定後の正確なMFE・MAEを再構築できません。

**実際に約定したとは記録しません。**

この区別はTSOの検証上重要です。

### WTIの材料更新

10月7日にはIEAが石油備蓄放出の加速を決定しました。

同時に米EIAは、原油在庫が予想の170万バレル増に反して**320万バレル減少**したと発表しています。

供給面では、フーシ派による攻撃などのリスクも残ります。citeturn438644view2

したがって、

**供給改善による下落仮説は維持**

しますが、旧Entry帯への再接近時には新しい供給情報で再評価が必要です。

SL92.00は変更しません。

---

# 3. 市場全体の前提

## マクロ環境

本日最も重要なのは、米国の長期金利とインフレ期待です。

| 指標 | 10月7日の基準値 | 解釈 |
|---|---:|---|
| US10Y | **5.272%** | 一時5.366%から反落 |
| DXY | **102.29** | ドル高再開 |
| USDJPY | **約158.09** | 円安継続だが159円未達 |
| VIX | **約15.07** | 株式の警戒感は限定的 |
| GOLD GCZ26 | **4140.70** | 金利・ドル高を嫌気 |
| WTI CLX26 | **88.28** | 備蓄放出加速で下落 |
| BTC/USD | **約83350** | 84500を下抜け |
| ETH/USD | **約2560** | 約5%の下落 |
| ESZ26 | **約7850** | 最高値圏から小幅反落 |
| NQZ26 | **約31394** | 上昇一服 |

数値は10月7日の終値・清算値または米国市場終了後の遅延値です。ES/NQは12月限の同一参照系列を使用していますが、取引所清算値との照合が完了していないため`partially_verified`とします。citeturn335562search3turn100131search5turn100131search8turn100131search0turn228104news7turn228104news21turn906301search2turn674044search2turn674044view0turn674044view1

## 最大の特徴：株式とCryptoの分裂

10月7日はBTCが約2.6%、ETHが約5%下落しました。

対してES/NQ先物の下落は、おおむね0.3%程度です。

さらにVIXも15前後にとどまっています。citeturn906301search2turn674044search2turn674044view0turn674044view1turn100131search0

これは、

**Cryptoだけが先行してリスクを織り込んでいる**

可能性と、

**Crypto固有の売り圧力が強まっている**

可能性の両方を示します。

現時点では、どちらが正しいか断定できません。

そこでTSOでは、

**BTC・ETHの下落を理由にNASDAQを自動的にSELLしない**

という判断を維持します。

## ETFフロー更新

10月6日のFarside確定値は次のとおりです。

| 日付 | BTC ETF | ETH ETF |
|---|---:|---:|
| 10月2日 | +189.9Mドル | -37.4Mドル |
| 10月5日 | -89.8Mドル | -50.8Mドル |
| 10月6日 | **+118.8Mドル** | **-201.9Mドル** |
| 10月7日 | 未集計 | 未集計 |

BTCは流入と流出が交互に発生しています。

ETHは6営業日連続の流出で、10月6日には特に大きく悪化しました。

これは単なるCrypto全体のrisk-offではなく、**ETH固有の資金需給悪化**が存在する可能性を示しています。citeturn451781view0turn906301view0

---

# 4. 10資産別判断

| 資産 | 価格基準 | 今日の判断 | 方向・理由 |
|---|---:|---|---|
| **GOLD** | 4140.70 | **B SELL_PULLBACK** | 金利・ドル高で弱い。戻り売り限定 |
| **BTC** | 約83350 | NO_TRADE | 84500割れ。流入再開だけでは買えない |
| **ETH** | 約2560 | NO_TRADE | 価格下落とETF大量流出が一致 |
| **WTI** | 88.28 | 新規NO_TRADE | 既存SELL監視継続。Entry到達を検証 |
| **USDJPY** | 約158.09 | NO_TRADE | ドル高だが介入リスクが非対称 |
| **SPX** | 約7850 | NO_TRADE | 高値圏で金利上昇への耐性確認 |
| **NASDAQ** | 約31394 | NO_TRADE | 長期トレンド強いが押し待ち |
| **DXY** | 102.29 | NO_TRADE | 上昇中だが直近高値付近 |
| **US10Y** | 5.272% | NO_TRADE | 5.366%から反落。入札反応を重視 |
| **VIX** | 15.07 | NO_TRADE | 株式市場の警戒感は依然低い |

なお、暗号資産の現物とCME先物は別系列です。

10月7日の参考値は、

**BTC CME：約83517.5**  
**ETH CME：約2581.5**

です。

現物との価格差を同一価格として扱いません。citeturn100131search4turn437858search0

---

# 5. A級候補

**本日A級はありません。**

もっともA級に近いのはGOLDのSELL方向ですが、以下の問題があります。

金利とドルはGoldにとって弱気材料です。

実際、12月限Goldは10月6日の4187.10から10月7日の4140.70へ下落しました。

**46.40ドルの下落**です。citeturn228104news8turn228104news7

ただし、すでに2か月ぶりの安値を付けており、成行SELLは追随になり過ぎます。

また本日は米国時間10月8日に**220億ドル規模の30年債入札**があります。

日本時間では10月9日02:00です。citeturn465033search0

10年債入札に続いて30年債も好調なら、金利が低下し、Goldに買い戻しが入る可能性があります。

そのためA級は見送ります。

---

# 6. B級監視候補

## 新規 `20261008_GOLD_SELL_PULLBACK`

**判定：B**

| 項目 | 設定 |
|---|---:|
| 参照系列 | GCZ26 |
| Entry Low | 4170.00 |
| Entry High | 4185.00 |
| Entry Mid | 4177.50 |
| SL | 4215.00 |
| TP1 | 4090.00 |
| TP2 | 4045.00 |
| RR | **2.33** |
| win_prob | **0.53** |
| expected_r | **0.33R** |
| CBS | 78 |
| EMS | 65 |
| MAE想定 | **0.31R** |
| リスク配分 | 0.25% |

### RR再計算

\[
RR=\frac{4177.50-4090.00}{4215.00-4177.50}
\]

\[
RR=\frac{87.50}{37.50}=2.3333
\]

したがってTSO_LOGには**2.33**を記帳します。

### 期待値

二点分布なら、

\[
EV=0.53\times2.33-0.47
\]

\[
EV\approx0.765R
\]

ただし今回は、未約定確率、5営業日時間決済、4090より手前での部分撤退、30年債入札による金利反転リスクを織り込みます。

**subjective expected_r：+0.33R**

これは主観推定であり、過去検証から得られた実測期待値ではありません。

### Invalidation

以下のいずれかを確認したらSELL仮説を再評価します。

- GCZ26が**4215超**
- US10Yが5.20%未満へ低下し、同時にDXYが101.80を下回る

後者はSL到達前でもシナリオ崩壊を疑う条件です。

### ロット制約

XMのスタンダード系口座で、GOLDの最小取引量を**1オンス**とした場合、

\[
37.50\times158.09\approx5928円
\]

となり、スプレッドを除いても実損上限3000円を超えます。

したがって、**XMスタンダード系の最小ロットでは実取引NO_TRADE**です。

マイクロ口座等でより小さい契約数量を扱える場合でも、GCZ26先物とXM現物Gold CFDの価格差を補正し、MT5の契約仕様を確認するまでは実行対象にしません。citeturn471380search4

**B+観察候補への昇格は保留**します。

---

# 7. 触らない資産

## ETH

本日もっとも積極的に避ける資産です。

10月7日のETHは約2698ドルから2560ドル近辺まで下落。

10月6日のETF純流出も**-201.9Mドル**でした。citeturn674044search2turn906301view0

下落方向の整合性はありますが、ここからSELLを追うと直近急落後の反発に巻き込まれる可能性があります。

**売り方向の観察は継続、成行SELLは禁止**とします。

## USDJPY

約158.09円です。

DXYは上昇しているのに、ドル円は159円へ加速していません。

これは円固有の動きがある可能性もありますが、現時点では介入の証拠ではありません。

現在検討しているIntervention Shock Moduleについては、

**159円接近＝警戒度上昇**

とします。

ただし、159円という価格だけで日本当局の介入を予測しません。

## NASDAQ

NQZ26は約31394。

10月7日の高値は31521、安値は31143でした。citeturn674044view0

短期的には下方向への圧力が増えましたが、直ちにSELLへ転換するほどではありません。

米10年債利回りが5.36%台に達してもNASDAQの下落が限定的だったことは、引き続き重要な相対強度です。

---

# 8. 後日検証ポイント

### US10Y

本日の重要水準は、

**5.366%：上方向の基準**  
**5.20%：金利上昇一服の確認候補**

です。

30年債入札後に5.20%を割るなら、Gold・NASDAQのシナリオを再評価します。

逆に5.366%を再突破すれば、長期金利上昇が再加速する可能性があります。

### GOLD

**4170–4185への戻り**を待ちます。

そこへ戻らず4090へ下落した場合は未約定のまま見送ります。

4170へ戻っても、US10Yが急低下しているならSELL注文を無条件に維持しません。

### WTI

既存シグナルは、

`20261006_WTI_SELL_PULLBACK`

です。

10月7日にEntry帯を通過したため、今回の検証では、

**TARGET_BEFORE_ENTRY → ENTRY_ZONE_REACHED**

という価格経路を記録します。

ただし約定後MFE/MAEを確定するには分足データが必要です。

### BTC

**84500回復**が最初の確認水準。

その後87500を再突破し、ETF流入も持続するならBUYを再評価します。

**82800割れ**なら下方向の圧力が強まったとみます。

### ETH

**2650回復**までBUY判断を保留。

2500割れなら次の支持帯を再調査します。

### NASDAQ・SPX

NQは**31100–31250**の支持確認を優先。

ESは**7800–7820**の支持確認を優先します。

どちらも価格だけでなく、US10YとVIXの反応を合わせて評価します。

---

# 9. Obsidian保存用 Observation Draft

```markdown
# 2026-10-08 TSO Daily Observation

Model:
GPT-6

Market protagonist:
US10Y

Gold reference:
COMEX December 2026
GCZ26

Regime:
EVENT

crypto_grounds:
etf=有
cme=有

expected_r_basis:
subjective

## Main observation

US10Y reached 5.366%
then declined toward 5.272%.

Strong 10Y Treasury auction:
39bn USD
Bid-to-cover 2.77
Dealer allocation 2.5%

FOMC minutes:
Most participants expected
another hike by year-end.

Interpretation:
Long-end Treasury demand
remains present despite
extreme interest rates.

## Market references

GCZ26:
4140.70

WTI CLX26:
88.28

BTC spot:
~83350

ETH spot:
~2560

USDJPY:
~158.09

ESZ26:
~7850

NQZ26:
~31394

DXY:
102.29

US10Y:
5.272%

VIX:
15.07

## Crypto flows

BTC ETF Oct6:
+118.8m USD

ETH ETF Oct6:
-201.9m USD

Oct7:
not finalized

BTC CME:
~83517.5

ETH CME:
~2581.5

Interpretation:
ETH demand deterioration
is significantly stronger
than BTC ETF deterioration.

No crypto BUY signal.

## Existing WTI signal

signal_id:
20261006_WTI_SELL_PULLBACK

Entry:
90.20-90.80

SL:
92.00

TP1:
87.20

Oct6:
target_before_entry

Oct7:
high 90.98
low 88.02
settlement 88.28

Research status:
ENTRY_ZONE_REACHED

Actual execution:
UNKNOWN

Invalidation:
not_fired

Do not retroactively alter Entry.

## New GOLD signal

signal_id:
20261008_GOLD_SELL_PULLBACK

Side:
SELL

Rank:
B

Entry:
4170-4185

Mid:
4177.50

SL:
4215

TP1:
4090

TP2:
4045

RR:
2.33

win_prob:
0.53

expected_r:
0.33

expected_r_basis:
subjective

MAE:
0.31R

CBS:
78

EMS:
65

Risk:
0.25%

Actual trade:
NO_TRADE until XM lot
and GCZ26/spot basis confirmed.

Invalidation:
GCZ26 >4215
OR
US10Y <5.20 AND DXY <101.80

## Next event

Oct8 US:
30Y Treasury auction

13:00 ET
02:00 JST Oct9

## Invalidation check

20261006_WTI_SELL_PULLBACK=not_fired
20261008_GOLD_SELL_PULLBACK=not_fired

## Signals

A:
NONE

B:
GOLD SELL_PULLBACK

Existing B:
WTI SELL_PULLBACK

#TSO #US10Y #GOLD #WTI #BTC #ETH
```

---

# 10. TSO_LOG — CSV / JSON

本日の10資産すべてについて、固定28列のログを生成しました。

データ取得のない部分と、主観評価の部分は区別しています。`verified_status`は参照データの検証状態を示し、主観的なスコアや予測確率の正しさを保証するものではありません。

保存用ファイルも用意しています。

[TSO_LOG CSV — 2026-10-08](sandbox:/mnt/data/TSO_LOG_2026-10-08.csv)

[TSO_LOG JSON — 2026-10-08](sandbox:/mnt/data/TSO_LOG_2026-10-08.json)

## CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-10-08,20261008_GOLD_SELL_PULLBACK,GOLD,SELL,B,PULLBACK,4170,4185,4215,4090,4045,2.33,0.53,0.33,76,79,53,0.25,EVENT,65,87,91,82,78,88,GCZ26_above_4215_or_US10Y_below_5.20_and_DXY_below_101.80,GCZ26_4090_4140.70_4170_4185_4215_US10Y_DXY_1d_3d_5d,verified
2026-10-08,20261008_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,53,47,90,,RISK_OFF,62,88,94,69,66,58,wait_for_BTC_reclaim_84500_then_87500_and_ETF_sustained_inflow,BTCspot_82800_83350_84500_87500_CME_83517_ETF_1d_3d,partially_verified
2026-10-08,20261008_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,45,43,95,,RISK_OFF,57,87,95,63,60,54,wait_for_ETH_reclaim_2650_with_ETF_flow_reversal_or_break_below_2500,ETHspot_2500_2560_2650_CME_2581.5_ETF_outflow_1d_3d,partially_verified
2026-10-08,20261008_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,72,68,86,,EVENT,59,94,95,77,75,88,existing_20261006_WTI_SELL_PULLBACK_not_fired_revalidate_after_target_before_entry,CLX26_87.20_88.28_90.20_90.80_90.98_92_IEA_EIA_1d_3d_5d,verified
2026-10-08,20261008_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,56,49,84,,EVENT,78,91,93,78,69,85,avoid_chasing_USDJPY_into_159_160_intervention_tail_wait_for_cross_asset_confirmation,USDJPY_157.85_158.09_158.51_159_160_DXY_US10Y_MOF_1d_3d,partially_verified
2026-10-08,20261008_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,68,59,76,,MIXED,73,87,93,84,78,87,wait_for_ESZ26_pullback_7800_7820_and_US10Y_stabilization_or_reclaim_7885,ESZ26_7815.75_7850.25_7884.50_US10Y_VIX_1d_3d,partially_verified
2026-10-08,20261008_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,70,60,77,,MIXED,76,89,93,85,81,88,avoid_chasing_NQ_retest_31480_31520_or_wait_for_31100_31250_pullback_with_yields_lower,NQZ26_31143_31393.75_31521_US10Y_VIX_1d_3d,partially_verified
2026-10-08,20261008_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,63,58,78,,EVENT,76,90,93,82,78,90,wait_for_DXY_sustain_above_102.50_or_fail_below_101.80,DXY_101.80_102.29_102.50_US10Y_GOLD_EURUSD_1d_3d,partially_verified
2026-10-08,20261008_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,72,67,94,,EVENT,92,96,98,92,85,95,wait_for_US10Y_break_above_5.366_or_retreat_below_5.20_after_auction_and_FOMC,US10Y_5.20_5.272_5.366_FOMC_auction_NQ_GOLD_1d_3d,verified
2026-10-08,20261008_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,51,44,86,,MIXED,69,87,92,72,73,81,low_VIX_diverges_from_rates_and_crypto_wait_for_sustained_reclaim_above_16.5,VIX_14.97_15.07_16.01_16.5_ES_NQ_US10Y_1d_3d,verified
```

## JSON

```json
[
  {
    "date":"2026-10-08",
    "signal_id":"20261008_GOLD_SELL_PULLBACK",
    "asset":"GOLD",
    "side":"SELL",
    "rank":"B",
    "type":"PULLBACK",
    "entry_low":4170,
    "entry_high":4185,
    "sl":4215,
    "tp1":4090,
    "tp2":4045,
    "rr":2.33,
    "win_prob":0.53,
    "expected_r":0.33,
    "tq_score":76,
    "opp_score":79,
    "no_trade_score":53,
    "risk_pct":0.25,
    "regime":"EVENT",
    "ems":65,
    "ffs":87,
    "cds":91,
    "ias":82,
    "cbs":78,
    "mes":88,
    "invalidation":"GCZ26_above_4215_or_US10Y_below_5.20_and_DXY_below_101.80",
    "verification_target":"GCZ26_4090_4140.70_4170_4185_4215_US10Y_DXY_1d_3d_5d",
    "verified_status":"verified"
  },
  {
    "date":"2026-10-08",
    "signal_id":"20261008_BTC_NONE_NO_TRADE",
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
    "tq_score":53,
    "opp_score":47,
    "no_trade_score":90,
    "risk_pct":null,
    "regime":"RISK_OFF",
    "ems":62,
    "ffs":88,
    "cds":94,
    "ias":69,
    "cbs":66,
    "mes":58,
    "invalidation":"wait_for_BTC_reclaim_84500_then_87500_and_ETF_sustained_inflow",
    "verification_target":"BTCspot_82800_83350_84500_87500_CME_83517_ETF_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-10-08",
    "signal_id":"20261008_ETH_NONE_NO_TRADE",
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
    "tq_score":45,
    "opp_score":43,
    "no_trade_score":95,
    "risk_pct":null,
    "regime":"RISK_OFF",
    "ems":57,
    "ffs":87,
    "cds":95,
    "ias":63,
    "cbs":60,
    "mes":54,
    "invalidation":"wait_for_ETH_reclaim_2650_with_ETF_flow_reversal_or_break_below_2500",
    "verification_target":"ETHspot_2500_2560_2650_CME_2581.5_ETF_outflow_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-10-08",
    "signal_id":"20261008_WTI_NONE_NO_TRADE",
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
    "tq_score":72,
    "opp_score":68,
    "no_trade_score":86,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":59,
    "ffs":94,
    "cds":95,
    "ias":77,
    "cbs":75,
    "mes":88,
    "invalidation":"existing_20261006_WTI_SELL_PULLBACK_not_fired_revalidate_after_target_before_entry",
    "verification_target":"CLX26_87.20_88.28_90.20_90.80_90.98_92_IEA_EIA_1d_3d_5d",
    "verified_status":"verified"
  },
  {
    "date":"2026-10-08",
    "signal_id":"20261008_USDJPY_NONE_NO_TRADE",
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
    "tq_score":56,
    "opp_score":49,
    "no_trade_score":84,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":78,
    "ffs":91,
    "cds":93,
    "ias":78,
    "cbs":69,
    "mes":85,
    "invalidation":"avoid_chasing_USDJPY_into_159_160_intervention_tail_wait_for_cross_asset_confirmation",
    "verification_target":"USDJPY_157.85_158.09_158.51_159_160_DXY_US10Y_MOF_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-10-08",
    "signal_id":"20261008_SPX_NONE_NO_TRADE",
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
    "tq_score":68,
    "opp_score":59,
    "no_trade_score":76,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":73,
    "ffs":87,
    "cds":93,
    "ias":84,
    "cbs":78,
    "mes":87,
    "invalidation":"wait_for_ESZ26_pullback_7800_7820_and_US10Y_stabilization_or_reclaim_7885",
    "verification_target":"ESZ26_7815.75_7850.25_7884.50_US10Y_VIX_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-10-08",
    "signal_id":"20261008_NASDAQ_NONE_NO_TRADE",
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
    "tq_score":70,
    "opp_score":60,
    "no_trade_score":77,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":76,
    "ffs":89,
    "cds":93,
    "ias":85,
    "cbs":81,
    "mes":88,
    "invalidation":"avoid_chasing_NQ_retest_31480_31520_or_wait_for_31100_31250_pullback_with_yields_lower",
    "verification_target":"NQZ26_31143_31393.75_31521_US10Y_VIX_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-10-08",
    "signal_id":"20261008_DXY_NONE_NO_TRADE",
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
    "tq_score":63,
    "opp_score":58,
    "no_trade_score":78,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":76,
    "ffs":90,
    "cds":93,
    "ias":82,
    "cbs":78,
    "mes":90,
    "invalidation":"wait_for_DXY_sustain_above_102.50_or_fail_below_101.80",
    "verification_target":"DXY_101.80_102.29_102.50_US10Y_GOLD_EURUSD_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-10-08",
    "signal_id":"20261008_US10Y_NONE_NO_TRADE",
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
    "tq_score":72,
    "opp_score":67,
    "no_trade_score":94,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":92,
    "ffs":96,
    "cds":98,
    "ias":92,
    "cbs":85,
    "mes":95,
    "invalidation":"wait_for_US10Y_break_above_5.366_or_retreat_below_5.20_after_auction_and_FOMC",
    "verification_target":"US10Y_5.20_5.272_5.366_FOMC_auction_NQ_GOLD_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-10-08",
    "signal_id":"20261008_VIX_NONE_NO_TRADE",
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
    "tq_score":51,
    "opp_score":44,
    "no_trade_score":86,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":69,
    "ffs":87,
    "cds":92,
    "ias":72,
    "cbs":73,
    "mes":81,
    "invalidation":"low_VIX_diverges_from_rates_and_crypto_wait_for_sustained_reclaim_above_16.5",
    "verification_target":"VIX_14.97_15.07_16.01_16.5_ES_NQ_US10Y_1d_3d",
    "verified_status":"verified"
  }
]
```

---

## 本日の研究上の重要な発見

本日は2点あります。

第一に、**WTIは前日に目標価格へ先行到達したあと、翌日に元のEntry帯へ戻った**ことです。

これは通常の勝敗分類だけでは追跡できません。

特に、TPを先に通過した時点で注文を取り消すべきなのか、それとも当初のEntry条件を維持するべきなのかという問題があります。

このケースは、今後のEntry設計の較正対象として残します。

第二に、**US10Yが5.366%まで上昇したにもかかわらず、10年債入札では強い需要が確認された**ことです。

これは、現在の長期金利上昇が無制限に続くと単純に考えるべきではないという材料になります。

本日発行する唯一の新規方向シグナルはGOLDの戻り売りですが、現状では実取引条件を満たしていません。

**最終判断：新規実取引NO_TRADE。GOLDのB級観察と、既存WTIのinvalidation監視を継続します。**
