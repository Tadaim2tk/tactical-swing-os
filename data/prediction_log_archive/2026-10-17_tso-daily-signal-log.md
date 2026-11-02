<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-10-17 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-11-02T05:45:08Z / chars: 22104 / 値は無修正 -->

# Tactical Swing OS — Daily Signal Log v2
## 2026年10月17日（土）

**使用モデル：GPT-6**  
**本日の市場の主役：NASDAQ**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**WTI基準限月：NYMEX 2026年11月限（CLX26）**  
**総合regime：RISK_OFF**

**データ基準：2026年10月16日米国市場終了後／10月17日日本時間早朝**

10資産すべてについて新たに市場データを検索しました。金・原油・株価指数は指定限月、BTC・ETHは米ドル建て現物、US10Yは米国債利回りを参照しています。

金曜日の清算値と時間外取引値が混在する場合は区別し、照合が不完全な資産には`partially_verified`を設定しました。

**crypto_grounds: etf=有, cme=有**

Farsideの10月15日確定ETFフローと、10月16日のCME BTC・ETH先物履歴を利用しました。10月16日のETFフローは未集計です。最新建玉と同時刻basisは確認できていません。citeturn221343view0turn221343view1turn928774search2turn928774search0

**expected_r_basis: subjective**

本日の新規方向シグナルはありません。既存NASDAQシグナルの`expected_r=0.30`は発行時の主観評価として維持します。この値は未約定確率、5営業日の時間決済、途中撤退を織り込んでおり、今回の値動きによって後付け修正しません。

**invalidation_check: 20261015_NASDAQ_SELL_PULLBACK=not_fired**

---

# 1. 本日の結論

| 項目 | 判定 |
|---|---|
| 新規A級 | **0件** |
| 新規B級 | **0件** |
| B+観察候補 | 0件 |
| 継続監視中の方向判断 | NASDAQ SELL_PULLBACK：1件 |
| 既存方向判断のinvalidation | **not_fired** |
| 本日の新規実取引 | **NO_TRADE** |
| 新規リスク配分 | 0% |
| 通常の日次リスク上限 | 0.50% |

**本日の最大の変化は、NASDAQの下落がさらに加速し、10月15日に発行したSELLシグナルがEntry未到達のままTP2まで先行通過したことです。**

10月16日の米国市場では、NASDAQ先物が大幅に下落しました。

| 指標 | 10月15日 | 10月16日 | 変化 |
|---|---:|---:|---:|
| NQZ26 | 30143.75 | **29391.50** | 約-2.50% |
| ESZ26 | 7791.00 | **7704.25** | 約-1.11% |
| VIX | 16.46 | **約20.2** | 約+23% |
| WTI CLX26 | 97.97 | **101.41** | 約+3.51% |
| US10Y | 5.10% | **5.09%** | 小幅低下 |

ES/NQは12月限が中心となっている先物系列から取得した清算値です。NQは29,391.50、ESは7,704.25を基準にしました。VIXは提供元によって20.15～20.57程度の差があるため近似値です。citeturn351674search9turn417905view0turn246538search1turn246538news91

WTIの101.41ドルは11月限の10月16日清算値です。citeturn417905news52

今回の市場では、次の組み合わせが成立しています。

**NASDAQ：大幅下落**

**VIX：急上昇**

**WTI：100ドル突破**

**米長期金利：上昇せず**

これは単なる金利上昇による成長株安ではありません。

AI関連企業の設備投資・資金調達に対する懸念が続く一方、原油市場には供給ショックが発生しています。

10月16日の米国株では、半導体・テクノロジー関連株の下落が目立ちました。S&P500現物は1.09%、Nasdaq Compositeは2.14%下落しています。citeturn246538news90

**今回のTSO判断では、NASDAQの方向評価と、実際に参加できる価格の設計を明確に分離します。**

方向観察が正しくても、Entryが遠すぎて約定できなければ利益は発生しません。

---

# 2. 前回判断の簡易検証

## NASDAQ SELL_PULLBACK

対象シグナル：

`20261015_NASDAQ_SELL_PULLBACK`

発行時の条件は変更しません。

| 項目 | 固定値 |
|---|---:|
| Entry Low | 30375 |
| Entry High | 30475 |
| Entry中点 | 30425 |
| SL | 30675 |
| TP1 | 29925 |
| TP2 | 29600 |
| RR | 2.00 |
| win_prob | 0.51 |
| expected_r | 0.30 |
| MAE想定 | 0.34R |
| CBS | 78 |
| EMS | 63 |
| rank | B |

### 10月16日の価格経路

NQZ26の10月16日の主なデータは次のとおりです。

**始値：約30089**

**高値：約30225**

**安値：約29268.75**

**清算値：29391.50**

同じ2026年12月限の履歴を使用しています。citeturn345394view0turn351674search9

これをシグナルの価格条件と比較します。

| 条件 | 判定 |
|---|---|
| Entry下限30375 | **未到達** |
| TP1 29925 | **到達** |
| TP2 29600 | **到達** |
| SL30675 | 未到達 |
| NQ30500超＋VIX15.5未満 | 未成立 |
| invalidation | **not_fired** |
| 実際の約定 | 未確認 |
| 研究上の分類 | **TP2_BEFORE_ENTRY** |

今回の特徴は、TP1だけではなくTP2まで到達したことです。

10月15日は、

**TARGET_BEFORE_ENTRY**

でした。

10月16日は、

**TP1_AND_TP2_BEFORE_ENTRY**

へ進みました。

方向観察は下落と整合しています。しかし、発行後の価格がEntry帯へ戻っていないため、指定した指値条件では約定機会がありませんでした。

**仮想利益は0Rとして扱うのではなく、「未約定・損益未発生」として記録します。**

0Rで時間決済した約定済み取引と、未約定の取引では意味が異なるからです。

### Invalidationはなぜnot_firedなのか

旧シグナルの主な失効条件は、

**NQZ26 >30675**

または、半導体主導の反転を伴う、

**NQZ26 >30500**
かつ
**VIX <15.5**

でした。

10月16日のNQ高値は30225付近にとどまりました。

したがって、価格によるinvalidationは確認されていません。

一方、VIXは上昇しています。

このため方向仮説自体は失効していないと判断します。

ただし、**方向仮説がnot_firedであることと、古い指値注文を維持することは別問題**です。

今回もTP1・TP2価格が先行通過したため、旧指値を無条件に残すことは推奨しません。

研究上の追跡は継続します。

---

# 3. 市場全体の前提

## 10資産の最新参照価格

| 資産 | 基準値 | 参照時点 | verified_status |
|---|---:|---|---|
| GOLD | **4181.10** | GCZ26・10/16清算値 | partially_verified |
| BTC | 約81500 | BTC/USD現物・10/16～17 | partially_verified |
| ETH | 約2412 | ETH/USD現物・10/16～17 | partially_verified |
| WTI | **101.41** | CLX26・10/16清算値 | verified |
| USDJPY | **158.139** | 10/16終値系 | partially_verified |
| SPX | **7704.25** | ESZ26・10/16清算値系 | partially_verified |
| NASDAQ | **29391.50** | NQZ26・10/16清算値系 | partially_verified |
| DXY | 約101.94 | 10/16ドル指数 | partially_verified |
| US10Y | **5.09%** | 10/16米財務省日次利回り | verified |
| VIX | 約20.2 | 10/16終値付近 | partially_verified |

GOLDのGCZ26については、MarketWatchに清算値4181.10ドル、時間外の遅延値4186.70ドルが表示されています。また別の提供元では4184ドル台の値が確認できます。今回は4181.10を固定基準とし、価格の完全照合ができていないため`partially_verified`としました。citeturn431780view1turn224867search5

BTC現物は約81,500ドル、ETH現物は約2,412ドルです。取得時点の差があるため、厳密な同時刻価格ではありません。citeturn161022search7turn345394search0

USDJPYは10月16日の日次履歴で158.139円、DXYは101.94付近です。citeturn246538search3turn246538news86

### マクロで重要な変化

本日は、前日まで観察してきた仮説がさらに強まりました。

**米長期金利が下がってもNASDAQが下落する。**

10月16日の米10年債利回りは、米財務省由来の日次系列で約5.09%です。

前日の5.10%から小幅に低下しています。citeturn246538search1

一方、NASDAQ先物は約2.5%下落しました。

これは割引率の低下だけでは株価を支えられない状況を示しています。

考えられる仮説は、AI関連投資に対する市場の期待修正です。

特に、

**設備投資の増加**

**借入・社債による資金調達**

**収益化までの期間**

**将来キャッシュフローへの不確実性**

が投資家から再評価されている可能性があります。

10月16日に公表されたReutersのファンドフロー分析でも、米国株式ファンド全体には資金が流入した一方、テクノロジーセクターからは約52.1億ドルが流出しました。citeturn224867news62

市場全体から資金が逃げているというより、**テクノロジーへの資金配分が選別され始めている**可能性があります。

## Crypto ETF更新

最新の確定フローは以下です。

| 日付 | BTC ETF | ETH ETF |
|---|---:|---:|
| 10月13日 | +175.7M | +24.8M |
| 10月14日 | -261.4M | -129.5M |
| **10月15日** | **+5.1M** | **-60.3M** |
| 10月16日 | 未集計 | 未集計 |

単位は百万米ドルです。

Farsideの10月16日欄は未入力であり、表示される0.0を純流入ゼロとは扱いません。citeturn221343view0turn221343view1

BTCは10月15日に小幅流入へ転換しましたが、10月12～15日の合計では約1.46億ドルの流出です。

ETHも約2.50億ドルの流出となっています。

### CME先物

10月16日の履歴では、

**BTC先物：約81030ドル**

**ETH先物：約2411.50ドル**

を確認しました。citeturn928774search2turn928774search0

これは現物価格ではなくCME先物です。

両方とも現物との取得時刻が同期しておらず、CME建玉の増減も確定できていません。

したがって、今回の判断では同時点basisを計算せず、先物価格の方向確認に限定します。

---

# 4. 10資産別判断

| 資産 | 本日判断 | CBS | EMS | no_trade_score | 評価 |
|---|---|---:|---:|---:|---|
| **GOLD** | NO_TRADE | 68 | 65 | 83 | 金利・ドル安で小幅反発。方向確認不足 |
| **BTC** | NO_TRADE | 54 | 52 | 92 | MES43。ETFの持続的改善なし |
| **ETH** | NO_TRADE | 48 | 47 | 95 | MES38。ETF流出継続 |
| **WTI** | NO_TRADE | 61 | 43 | 98 | 101.41。供給ショックと限月満期 |
| **USDJPY** | NO_TRADE | 63 | 58 | 87 | 158.14。円固有の反応確認待ち |
| **SPX** | NO_TRADE | 68 | 58 | 89 | ESが7700付近へ下落 |
| **NASDAQ** | NO_TRADE | 76 | 59 | 92 | NQ29391。旧B級はTP2先行到達 |
| **DXY** | NO_TRADE | 61 | 64 | 84 | 101.94。ドル高が一服 |
| **US10Y** | NO_TRADE | 77 | 71 | 88 | 5.09%。原油高でも金利上昇せず |
| **VIX** | NO_TRADE | 71 | 65 | 95 | 約20.2。リスク回避が拡大 |

各スコアは今回取得したデータに基づく主観評価です。

**本日、新規方向シグナルを出す資産はありません。**

ただし、10月15日のNASDAQ B級判断については、引き続きinvalidationの追跡を行います。

---

# 5. A級候補

**なし。**

現在、方向の優位性が最も明確なのはNASDAQのSELL側です。

しかし、NQZ26は10月15日の清算値30143.75から、10月16日には29391.50まで下落しました。

約752ポイントの下落です。

ここで新規SELLする場合、さらに下落する可能性はあります。

しかし、**下落方向の確信度が高いことと、現在値からのRR・MAEが良いことは別**です。

加えて、VIXは20台へ上昇しています。

この状況では、下落方向を正しく予測しても、短時間の反発で通常のSL幅に到達する可能性が高まります。

既存ルールの、

**SL幅を広げない**

**MAE想定0.25R以下**

**expected_r0.45以上**

を同時に満たせるEntry設計ができていません。

そのため、A級を発行しません。

---

# 6. B級監視候補

## 継続：`20261015_NASDAQ_SELL_PULLBACK`

**rank：B**

**invalidation：not_fired**

**実取引：NO_TRADE**

前回の設定は維持します。

| 項目 | 設定 |
|---|---:|
| Entry | 30375–30475 |
| SL | 30675 |
| TP1 | 29925 |
| TP2 | 29600 |
| RR | 2.00 |
| win_prob | 0.51 |
| expected_r | 0.30 |
| MAE想定 | 0.34R |

### RR再確認

\[
Entry_{mid}=\frac{30375+30475}{2}=30425
\]

\[
RR=\frac{30425-29925}{30675-30425}
\]

\[
RR=\frac{500}{250}=2.00
\]

計算は一致しています。

ただし、これは**10月15日時点の条件に対するRR**です。

現在値29391.50から売った場合のRRではありません。

### B+判定

既存シグナルは、

CBS：78  
EMS：63  
RR：2.00  
win_prob：0.51

という点ではB+の数値条件を満たしています。

しかし、XM最小ロットの損失制約を確認できていません。

SL距離は250ポイントです。

ドル円158.139円を使用すると、想定実損を3000円以内に抑えるためには、

\[
3000/(250\times158.139)
\approx0.07588
\]

1ポイント当たりの損益額を、スプレッド・滑りを除いても**0.07588米ドル以下**にする必要があります。

XMの対象CFDの最小ロットがこの条件を満たすと確認できていないため、**B+正式認定は行いません。**

また、TP1・TP2が先に到達しているため、旧Entryで実行する優位性も未検証です。

**正式B+：0件**

**新規B級：0件**

---

# 7. 触らない資産

## WTI

**本日、最も積極的に避けるのはWTIです。**

10月16日のWTI11月限は101.41ドルで清算しました。

前営業日の97.97ドルから約3.5%上昇しています。

中東の輸送障害に加え、ウクライナによるロシア製油所への攻撃が供給懸念を強めました。citeturn417905news49

この局面では、供給ショック直後のmomentum追随を禁止する既存ルールを適用します。

現在値からのBUYは行いません。

一方、急騰の反動だけを狙ったSELLも作りません。

### WTI限月の注意

11月限CLX26は**10月20日が満期**です。

今回確認した12月限CLZ26の清算値は約99.02ドルです。citeturn417905news48

11月限101.41ドルに対し、12月限は約2.39ドル低い状態です。

この期近プレミアムは、短期的な供給逼迫懸念と整合します。

ただし、限月間の価格差だけで実際の在庫不足や将来価格を断定することはできません。

**ロール後のCLZ26を、CLX26の前日価格と直接比較しない**ことを徹底します。

## BTC・ETH

BTCは約81500ドル、ETHは約2412ドルです。

ETFフローはBTCが小幅流入、ETHが流出継続です。

しかし、価格構造は両方とも弱く、CME建玉増減の確証もありません。

今回のMESは、

**BTC：43**

**ETH：38**

です。

BTCは既存のMES50未満ルールに該当します。

両方ともNO_TRADEを維持します。

## USDJPY

ドル円は約158.14円です。

前日の158.0円付近から大きな方向変化は確認できていません。

米長期金利とDXYが低下している一方、円高方向への反応は限定的です。

ただし、これだけで円固有の売り圧力や為替介入の可能性を定量化できません。

Intervention Shock Moduleでは、

**159円接近**

**短時間の円安加速**

**DXYと他の円クロスとの乖離**

を引き続き監視します。

---

# 8. 後日検証ポイント

## ① NASDAQ：TP2_BEFORE_ENTRY

本日の最大の研究課題です。

10月15日に発行したSELL判断は、

**Entry：30375–30475**

でした。

しかし発行後の価格はEntry帯へ戻らず、10月16日にはTP2の29600まで下落しました。

このため、シグナルの方向判断と注文成立を別々に評価する必要があります。

今後の比較対象は以下です。

| 注文管理ルール | 今回のケースへの影響 |
|---|---|
| TP1先行到達で指値取消 | 未約定のまま終了 |
| TP2先行到達で指値取消 | 未約定のまま終了 |
| 指値を5営業日保持 | 今後の戻りで約定する可能性 |
| シナリオ崩壊時のみ取消 | not_firedなら注文が残る可能性 |

この4方式の期待値を、今後の複数シグナルで比較する価値があります。

ただし、今回の値動きを見てから過去の注文を取り消したことにはしません。

**TSO_LOGの過去28列は変更せず、Observation側に注文管理の仮説を追記します。**

## ② NASDAQとVIX

NQZ26は29391.50まで下落しました。

VIXは20台です。

次の観察では、

**NQが30000を回復するか**

**VIXが17.5未満へ戻るか**

を確認します。

ここで価格が回復し、半導体株の下落も一服するなら、SELL優先の評価を引き下げる可能性があります。

## ③ 米長期金利

US10Yは約5.09%です。

WTIが100ドルを突破したにもかかわらず、米長期金利は上昇していません。

これは、

**原油高 → 金利高 → NASDAQ安**

という単純な説明を支持しません。

今後も、

**原油**

**米10年債利回り**

**NASDAQ**

の3系列を分離して観察します。

特に、US10Yが5.00%を下回ってもNASDAQが弱ければ、AI関連企業の収益化・資金調達に対する懸念が、金利低下による株価支援を上回っている可能性を調べます。

## ④ Crypto

BTCは80000ドルの維持を優先します。

83500ドルを回復し、ETFフローが継続的に改善するならBUY側を再評価します。

ETHは2400ドル付近の支持と2500ドル回復を確認します。

次のETF確定値が入った際には、10月15日のBTC小幅流入が持続したかを検証します。

## ⑤ GOLD

GCZ26は4181.10ドルです。

16日のレンジは4167.50～4220.40ドルでした。citeturn431780view1

4167.50を維持できるか、4220.40を上抜けるかを確認します。

以前のSELLシグナルは失効済みです。

新しい方向判断を作る場合は別のsignal_idを発行します。

---

# 9. Obsidian保存用 Observation Draft

**[TSO Observation — 2026-10-17](sandbox:/mnt/data/TSO_Observation_2026-10-17.md)**

Markdownファイルには、参照価格、シグナル検証、未確認データ、研究課題を保存しました。

チャット上にも主要記録を残します。

```markdown
# TSO Observation — 2026-10-17

Model:
GPT-6

Market protagonist:
NASDAQ

Regime:
RISK_OFF

Gold reference:
COMEX December 2026
GCZ26

WTI reference:
NYMEX November 2026
CLX26

crypto_grounds:
etf=有
cme=有

expected_r_basis:
subjective

## Conclusion

New A: 0
New B: 0
B+: 0

New actual trades:
NO_TRADE

Risk allocation:
0%

## Active directional signal

20261015_NASDAQ_SELL_PULLBACK

Original Entry:
30375-30475

SL:
30675

TP1:
29925

TP2:
29600

RR:
2.00

win_prob:
0.51

expected_r:
0.30

Oct16 NQZ26:

High:
~30225

Low:
~29268.75

Settlement:
29391.50

Result:
ENTRY_NOT_REACHED
TP1_BEFORE_ENTRY
TP2_BEFORE_ENTRY

Invalidation:
NOT_FIRED

Actual execution:
UNKNOWN

Research note:

Directional movement was consistent
with the original SELL scenario.

However no valid Entry occurred.

Do not book hypothetical profit.

Do not automatically retain
the stale pending order.

## Market references

GOLD GCZ26:
4181.10

WTI CLX26:
101.41

WTI CLZ26:
~99.02

USDJPY:
158.139

ESZ26:
7704.25

NQZ26:
29391.50

DXY:
~101.944

US10Y:
5.09%

VIX:
~20.2

BTC spot:
~81500

ETH spot:
~2412

## Crypto

BTC CME:
~81030

ETH CME:
~2411.50

BTC ETF Oct15:
+5.1m USD

ETH ETF Oct15:
-60.3m USD

Oct16 ETF:
NOT FINALIZED

BTC MES:
43

ETH MES:
38

Both:
NO_TRADE

## Main macro observation

WTI increased strongly.

NQ and ES declined.

VIX increased.

US10Y did not increase.

Interpretation:

Oil supply shocks
and AI investment risks
are coexisting.

Do not reduce the market
to a single oil-yield-equity
causal relationship.

## WTI rollover

CLX26 expiry:
2026-10-20

CLX26:
101.41

CLZ26:
~99.02

Calendar spread:
~2.39 USD

Do not directly splice prices
from different expiries.

## Invalidation check

20261015_NASDAQ_SELL_PULLBACK=not_fired

## Research tasks

1. TP2_before_entry classification.
2. Compare pending-order expiry rules.
3. Separate directional accuracy
   from execution probability.
4. NQ and VIX stabilization.
5. WTI calendar spread and rollover.
6. ETF flow versus spot momentum.
7. XM minimum lot risk validation.

#TSO #NASDAQ #WTI #VIX #BTC #US10Y
```

---

# 10. TSO_LOG — CSV / JSON

**固定28列・10資産10行を生成し、構造検証を完了しました。**

| 検証項目 | 結果 |
|---|---|
| CSV列数 | **28** |
| データ行数 | **10** |
| 資産の重複 | なし |
| 資産の欠落 | なし |
| `asset=NONE` | なし |
| JSONオブジェクト数 | 10 |
| JSON各オブジェクトのキー数 | 28 |
| regime許容語彙 | 適合 |
| NO_TRADE行の価格・RR・確率 | 空欄 |
| 既存NASDAQのRR再計算 | 2.00で一致 |

本日は新規方向シグナルがないため、10資産すべてNO_TRADE行です。

既存NASDAQの方向判断は、新しい日次シグナルへコピーせず、invalidationとObservationに記録しています。

## 保存ファイル

**[TSO_LOG CSV — 2026-10-17](sandbox:/mnt/data/TSO_LOG_2026-10-17.csv)**

**[TSO_LOG JSON — 2026-10-17](sandbox:/mnt/data/TSO_LOG_2026-10-17.json)**

## CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-10-17,20261017_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,62,57,83,,MIXED,65,85,91,71,68,83,prior_GOLD_SELL_fired_closed_await_GCZ26_4167.5_support_or_4220.4_break,GCZ26_20261016_settle_4181.10_high_4220.40_low_4167.50_US10Y_DXY,partially_verified
2026-10-17,20261017_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,44,45,92,,RISK_OFF,52,86,93,52,54,43,BTC_MES_43_weekly_ETF_net_outflow_wait_83500_reclaim_and_CME_confirmation,BTCspot_approx_81500_20261016_CME_BTC_81030_ETF_20261015_plus5.1_80000_83500,partially_verified
2026-10-17,20261017_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,38,39,95,,RISK_OFF,47,85,94,46,48,38,ETH_MES_38_ETF_outflow_wait_2500_reclaim_without_market_chase,ETHspot_approx_2412_20261016_CME_ETH_2411.50_ETF_20261015_minus60.3_2350_2500,partially_verified
2026-10-17,20261017_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,56,62,98,,EVENT,43,98,96,57,61,99,CLX26_supply_shock_and_Oct20_expiry_no_momentum_buy_or_automatic_sell,CLX26_20261016_settle_101.41_CLZ26_99.02_Hormuz_Russian_refineries_expiry,verified
2026-10-17,20261017_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,57,48,87,,MIXED,58,90,92,62,63,85,no_confirmed_intervention_watch_159_160_and_one_hour_JPY_cross_speed,USDJPY_20261016_close_158.139_high_158.182_DXY_US10Y_MOF,partially_verified
2026-10-17,20261017_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,55,53,89,,RISK_OFF,58,92,95,57,68,90,ESZ26_break_below_7676_or_reclaim_7770_with_VIX_normalization,ESZ26_20261016_settle_approx_7704.25_range_7676_7809.5_VIX_20.2,partially_verified
2026-10-17,20261017_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,67,61,92,,RISK_OFF,59,96,95,69,76,96,active_20261015_NASDAQ_SELL_PULLBACK_not_fired_TP1_TP2_before_entry_order_revalidation_required,NQZ26_20261016_settle_29391.50_high_30225_low_29268.75_entry_30375_30475_sl_30675,partially_verified
2026-10-17,20261017_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,51,47,84,,MIXED,64,91,92,62,61,85,DXY_below_102.2_wait_101.80_break_or_102.60_reclaim,DXY_20261016_approx_101.944_intra_low_101.816_US10Y_USDJPY,partially_verified
2026-10-17,20261017_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,61,60,88,,MIXED,71,93,94,69,77,91,yield_near_5.09_not_rising_with_oil_watch_5.00_or_5.20,US10Y_20261016_Treasury_par_5.09_20261015_5.10_WTI_NQ,verified
2026-10-17,20261017_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,58,55,95,,RISK_OFF,65,94,95,61,71,95,VIX_near_20.2_high_22.31_wait_volatility_normalization_below_17.5,VIX_20261016_approx_20.2_intraday_high_22.31_prior_16.46_ES_NQ,partially_verified
```

## JSON

CSVと同一の固定28項目を保持した10資産分です。

```json
[
{"date":"2026-10-17","signal_id":"20261017_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":62,"opp_score":57,"no_trade_score":83,"risk_pct":null,"regime":"MIXED","ems":65,"ffs":85,"cds":91,"ias":71,"cbs":68,"mes":83,"invalidation":"prior_GOLD_SELL_fired_closed_await_GCZ26_4167.5_support_or_4220.4_break","verification_target":"GCZ26_20261016_settle_4181.10_high_4220.40_low_4167.50_US10Y_DXY","verified_status":"partially_verified"},
{"date":"2026-10-17","signal_id":"20261017_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":44,"opp_score":45,"no_trade_score":92,"risk_pct":null,"regime":"RISK_OFF","ems":52,"ffs":86,"cds":93,"ias":52,"cbs":54,"mes":43,"invalidation":"BTC_MES_43_weekly_ETF_net_outflow_wait_83500_reclaim_and_CME_confirmation","verification_target":"BTCspot_approx_81500_20261016_CME_BTC_81030_ETF_20261015_plus5.1_80000_83500","verified_status":"partially_verified"},
{"date":"2026-10-17","signal_id":"20261017_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":38,"opp_score":39,"no_trade_score":95,"risk_pct":null,"regime":"RISK_OFF","ems":47,"ffs":85,"cds":94,"ias":46,"cbs":48,"mes":38,"invalidation":"ETH_MES_38_ETF_outflow_wait_2500_reclaim_without_market_chase","verification_target":"ETHspot_approx_2412_20261016_CME_ETH_2411.50_ETF_20261015_minus60.3_2350_2500","verified_status":"partially_verified"},
{"date":"2026-10-17","signal_id":"20261017_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":56,"opp_score":62,"no_trade_score":98,"risk_pct":null,"regime":"EVENT","ems":43,"ffs":98,"cds":96,"ias":57,"cbs":61,"mes":99,"invalidation":"CLX26_supply_shock_and_Oct20_expiry_no_momentum_buy_or_automatic_sell","verification_target":"CLX26_20261016_settle_101.41_CLZ26_99.02_Hormuz_Russian_refineries_expiry","verified_status":"verified"},
{"date":"2026-10-17","signal_id":"20261017_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":57,"opp_score":48,"no_trade_score":87,"risk_pct":null,"regime":"MIXED","ems":58,"ffs":90,"cds":92,"ias":62,"cbs":63,"mes":85,"invalidation":"no_confirmed_intervention_watch_159_160_and_one_hour_JPY_cross_speed","verification_target":"USDJPY_20261016_close_158.139_high_158.182_DXY_US10Y_MOF","verified_status":"partially_verified"},
{"date":"2026-10-17","signal_id":"20261017_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":55,"opp_score":53,"no_trade_score":89,"risk_pct":null,"regime":"RISK_OFF","ems":58,"ffs":92,"cds":95,"ias":57,"cbs":68,"mes":90,"invalidation":"ESZ26_break_below_7676_or_reclaim_7770_with_VIX_normalization","verification_target":"ESZ26_20261016_settle_approx_7704.25_range_7676_7809.5_VIX_20.2","verified_status":"partially_verified"},
{"date":"2026-10-17","signal_id":"20261017_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":67,"opp_score":61,"no_trade_score":92,"risk_pct":null,"regime":"RISK_OFF","ems":59,"ffs":96,"cds":95,"ias":69,"cbs":76,"mes":96,"invalidation":"active_20261015_NASDAQ_SELL_PULLBACK_not_fired_TP1_TP2_before_entry_order_revalidation_required","verification_target":"NQZ26_20261016_settle_29391.50_high_30225_low_29268.75_entry_30375_30475_sl_30675","verified_status":"partially_verified"},
{"date":"2026-10-17","signal_id":"20261017_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":51,"opp_score":47,"no_trade_score":84,"risk_pct":null,"regime":"MIXED","ems":64,"ffs":91,"cds":92,"ias":62,"cbs":61,"mes":85,"invalidation":"DXY_below_102.2_wait_101.80_break_or_102.60_reclaim","verification_target":"DXY_20261016_approx_101.944_intra_low_101.816_US10Y_USDJPY","verified_status":"partially_verified"},
{"date":"2026-10-17","signal_id":"20261017_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":61,"opp_score":60,"no_trade_score":88,"risk_pct":null,"regime":"MIXED","ems":71,"ffs":93,"cds":94,"ias":69,"cbs":77,"mes":91,"invalidation":"yield_near_5.09_not_rising_with_oil_watch_5.00_or_5.20","verification_target":"US10Y_20261016_Treasury_par_5.09_20261015_5.10_WTI_NQ","verified_status":"verified"},
{"date":"2026-10-17","signal_id":"20261017_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":58,"opp_score":55,"no_trade_score":95,"risk_pct":null,"regime":"RISK_OFF","ems":65,"ffs":94,"cds":95,"ias":61,"cbs":71,"mes":95,"invalidation":"VIX_near_20.2_high_22.31_wait_volatility_normalization_below_17.5","verification_target":"VIX_20261016_approx_20.2_intraday_high_22.31_prior_16.46_ES_NQ","verified_status":"partially_verified"}
]
```

---

## 本日の総括

**10月17日の最重要研究材料は、NASDAQの方向判断が下落と整合した一方、Entry設計によって取引機会を得られなかったことです。**

10月15日に発行したNASDAQ SELL_PULLBACKは、10月16日までにTP1・TP2の両方を先に通過しました。

方向の予測精度だけを検証すれば、強い下落を事前に警戒できていた事例です。

しかし取引システムとして見ると、指定Entryへの戻りがなく、実行可能な利益には結びついていません。

この違いを今後の較正で重視します。

もう一つの重要事項は、WTIが100ドルを突破したにもかかわらず、米長期金利が上昇せず、NASDAQの下落が加速したことです。

**現在の市場では、エネルギー供給リスクとAI関連投資リスクを独立した要因として扱う必要があります。**

本日は新規A級・B級を発行しません。

**最終判断：10資産すべて新規NO_TRADE。既存NASDAQ B級はnot_firedで継続監視。固定28列・10行のTSO_LOGを保存しました。**

**次指示対象：NASDAQのTP2_BEFORE_ENTRY後の価格経路、VIXの正常化、WTI限月切り替え、BTC・ETHの最新ETFフローの追跡。**
