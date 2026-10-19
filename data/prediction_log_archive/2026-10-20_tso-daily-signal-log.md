<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-10-20 07:00 JST -->
<!-- transport: ChatGPT read_thread complete message markdown -->
<!-- archived_at: 2026-10-19T23:01:55Z / chars: 15963 / 値は無修正 -->

# Tactical Swing OS — Daily Signal Log v2
## 2026年10月20日（火）

**使用モデル：GPT-6**  
**本日の市場の主役：WTI**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**WTI基準限月：NYMEX 2026年11月限（CLX26）**  
**総合regime：MIXED**

**データ基準：2026年10月19日米国市場終了後／10月20日07:00 JST頃**

10資産すべてについて新規の市場データ取得を実施しました。

先物は指定限月、BTC・ETHは米ドル建て現物、US10Yは利回り、VIXは指数本体を使用しています。

**crypto_grounds: etf=有, cme=有**

10月19日のBTC・ETH現物とCME先物の価格履歴を確認しました。ETFについては10月16日分まで確定値が利用でき、19日分は未集計です。CME建玉増減と同時刻basisは未確認です。

**expected_r_basis: subjective**

新規方向シグナルはないため、expected_rは全行空欄です。既存NASDAQの0.30Rは発行時の主観期待値として固定しています。この値には未約定確率、5営業日時間決済、シナリオ崩壊による途中撤退を織り込んでいます。

**invalidation_check: 20261015_NASDAQ_SELL_PULLBACK=not_fired**

---

# 1. 本日の結論

| 項目 | 判定 |
|---|---|
| 新規A級 | **0件** |
| 新規B級 | **0件** |
| B+観察候補 | 0件 |
| 継続中の方向判断 | NASDAQ SELL_PULLBACK：1件 |
| 既存シグナルのinvalidation | **not_fired** |
| 本日の新規実取引 | **NO_TRADE** |
| 新規リスク配分 | 0% |
| 最大日次リスク | 0.50% |

**本日の最大の発見は、WTIの11月限と12月限の価格差が急拡大したことです。**

10月19日のWTIは、限月によって正反対の値動きになりました。

| WTI先物 | 10月16日 | 10月19日 | 変化 |
|---|---:|---:|---:|
| 11月限 CLX26 | 101.41 | **103.66** | +2.25 |
| 12月限 CLZ26 | 99.02 | **98.54** | -0.48 |
| 限月間スプレッド | 2.39 | **5.12** | +2.73 |

単位はドル/バレルです。

10月19日の両限月の清算値は、Wall Street JournalとReutersの報道で確認しました。:chatgpt-content-reference{index="0"}

注目すべきは、**11月限が上昇しているのに、12月限は下落している**ことです。

これは単純な原油市場全体の上昇ではありません。

期近の供給逼迫懸念、満期に伴うポジション調整、流動性の低下などが影響している可能性があります。

CLX26は本日10月20日が最終取引日です。:chatgpt-content-reference{index="1"}

したがって、今回の価格差拡大をそのまま持続的な原油需給逼迫の証拠とは扱いません。

**WTIは方向判断より、限月間の価格形成を研究することを優先します。**

一方、NASDAQでは前週の急落から反発が起こりました。

NQZ26は10月19日に**29,722.50ポイント**で清算され、前営業日の29,391.50から上昇しました。

VIXも19.99から18.44へ低下しています。:chatgpt-content-reference{index="2"}

ただし、既存NASDAQ SELLシグナルの失効条件には到達していません。

本日は新規のSELLもBUYも発行しません。

---

# 2. 前回判断の簡易検証

## NASDAQ SELL_PULLBACK

対象：

`20261015_NASDAQ_SELL_PULLBACK`

発行時の条件は固定します。

| 項目 | 発行時設定 |
|---|---:|
| Entry Low | 30375 |
| Entry High | 30475 |
| Entry中点 | 30425 |
| SL | 30675 |
| TP1 | 29925 |
| TP2 | 29600 |
| RR | 2.00 |
| win_prob | 0.51 |
| expected_r | 0.30R |
| MAE想定 | 0.34R |
| CBS | 78 |
| EMS | 63 |
| ランク | B |

### 10月19日の価格経路

新たに確認できたNQZ26の価格は次のとおりです。

| 項目 | 価格 |
|---|---:|
| 始値 | 29227.00 |
| 高値 | **29983.50** |
| 安値 | **29226.00** |
| 清算値 | **29722.50** |

すべて2026年12月限の参照系列です。:chatgpt-content-reference{index="3"}

10月19日は、前週末の安値29268.75を一時下回った後、強く反発しました。

しかし、高値29983.50でも、旧Entry下限30375には届いていません。

### Invalidation判定

旧シグナルの主な失効条件は、

**NQZ26 >30675**

です。

補助条件は、半導体主導の反転を伴う、

**NQZ26 >30500**
かつ
**VIX <15.5**

でした。

10月19日のNQ高値は29983.50、VIX終値は18.44です。

どちらの条件も成立していません。

したがって、

**invalidation：not_fired**

です。

### 現在の研究状態

| 検証項目 | 判定 |
|---|---|
| 当初Entry帯への到達 | なし |
| TP1先行到達 | 確認済み |
| TP2先行到達 | 確認済み |
| 10月19日の反発 | 確認 |
| 価格失効条件 | 未成立 |
| 補助失効条件 | 未成立 |
| 実際の約定 | 未確認 |
| 研究分類 | **TP2_BEFORE_ENTRY** |

ここで重要な区別があります。

**方向仮説はまだ失効していませんが、実行可能な売買注文としては再評価が必要です。**

旧Entry帯に戻ってきたとしても、10月15日と同じ期待値が残っているとは限りません。

したがって、旧指値を再利用しません。

また、TP1・TP2を通過したことによる仮想利益も計上しません。

---

# 3. 市場全体の前提

## 最新10資産の価格基準

| 資産 | 基準値 | 参照系列・日時 | verified_status |
|---|---:|---|---|
| GOLD | **4160.10** | GCZ26・10/19清算値 | verified |
| BTC | **約81963** | BTC/USD現物・10/19 | partially_verified |
| ETH | **約2399** | ETH/USD現物・10/19 | partially_verified |
| WTI | **103.66** | CLX26・10/19清算値 | verified |
| USDJPY | **約158.54** | ドル円・10/19終値系 | partially_verified |
| SPX | **7734.50** | ESZ26・10/19清算値 | verified |
| NASDAQ | **29722.50** | NQZ26・10/19清算値 | verified |
| DXY | **約101.89** | ドル指数・10/19 | partially_verified |
| US10Y | **約5.14%** | 米10年債利回り・10/19 | partially_verified |
| VIX | **18.44** | VIX指数・10/19終値 | verified |

GOLDは指定された12月限の清算値4160.10ドルです。10月19日の高値は4211.20、安値は4155.60でした。:chatgpt-content-reference{index="4"}

ESZ26は7734.50、NQZ26は29722.50で清算されています。両方とも現物指数やETFではなく、指定された先物系列です。:chatgpt-content-reference{index="5"}

BTC現物の日次参考値は約81963ドル、ETHは約2399ドルです。暗号資産は取得時刻による差があるため、厳密な同時刻価格とは扱いません。:chatgpt-content-reference{index="6"}

USDJPYは19日の取得系列で158.54円付近。ただし同じ日付に異なるセッション区切りの記録もあるため、終値の時刻整合は部分検証です。:chatgpt-content-reference{index="7"}

### 米長期金利

10月19日の米10年債利回りは、Investing.comの日次履歴で約5.14%でした。

日中安値は5.051%、高値は5.152%です。:chatgpt-content-reference{index="8"}

一方、Barron'sは取引時間中に5.076%を報じています。:chatgpt-content-reference{index="9"}

この違いは、取得時点の差を含む可能性があります。

**日中の5.076%と日次終盤の約5.14%を、同じ時刻の価格として比較しません。**

今回の重要な観察は、前週の金利低下が一方向には続かなかったことです。

---

## NASDAQ反発の中身

10月19日の米国株式市場では、AI・半導体関連株に買い戻しが入りました。

Reutersによると、Nasdaq Compositeは1.11%、S&P500現物は0.41%上昇しました。

半導体指数も8営業日続いた下落から反発しています。:chatgpt-content-reference{index="10"}

このニュースはNASDAQの市場環境を判断する補助情報として利用します。

TSO_LOGのNASDAQ行に、Nasdaq Compositeの価格を代用することはありません。

今回の反発は、これまでの研究仮説に対する重要な検証材料です。

**仮説A：AI関連株の下落は短期的な過剰反応だった。**

**仮説B：AI設備投資の資金調達問題が残っており、反発は一時的である。**

どちらも現時点では確定できません。

特にCoreWeaveなど、AIインフラ企業の信用市場で要求される利回りには依然として警戒感が残っています。:chatgpt-content-reference{index="11"}

したがって、NASDAQが反発したから直ちにBUYへ転換するのではなく、今週の企業決算と価格の反応を確認します。

---

## Crypto ETF更新

Farsideの表を新規確認しました。

| 日付 | BTC ETF | ETH ETF |
|---|---:|---:|
| 10月13日 | +175.7M | +24.8M |
| 10月14日 | -261.4M | -129.5M |
| 10月15日 | +5.1M | -60.3M |
| 10月16日 | -82.4M | -69.7M |
| **10月19日** | **未集計** | **未集計** |

単位は百万米ドルです。

10月19日のFarside表では構成ETFの数値が未入力で、合計0.0と表示されています。

したがって、純流入ゼロとは扱いません。:chatgpt-content-reference{index="12"}

今回の判断に使用できる最新の確定フローは、引き続き10月16日です。

### CME先物

10月19日のCME先物参考価格は、

**BTC：約81832ドル**

**ETH：約2401.50ドル**

でした。

BTCについては別の配信元で81900ドル前後の記録もあり、ETHにも数ドルの差があります。:chatgpt-content-reference{index="13"}

現物との同時刻比較はできていません。

そのためbasisの確定計算は行いません。

最新建玉の増減も、今回の判断根拠には使用していません。

---

# 4. 10資産別判断

| 資産 | 本日判断 | CBS | EMS | MES | no_trade_score |
|---|---|---:|---:|---:|---:|
| **GOLD** | NO_TRADE | 68 | 64 | 88 | 89 |
| **BTC** | NO_TRADE | 57 | 53 | **45** | 92 |
| **ETH** | NO_TRADE | 53 | 49 | **39** | 94 |
| **WTI** | NO_TRADE | 57 | 41 | 99 | 99 |
| **USDJPY** | NO_TRADE | 65 | 64 | 85 | 86 |
| **SPX** | NO_TRADE | 72 | 68 | 88 | 84 |
| **NASDAQ** | NO_TRADE | 74 | 62 | 90 | 90 |
| **DXY** | NO_TRADE | 68 | 65 | 83 | 87 |
| **US10Y** | NO_TRADE | 74 | 77 | 90 | 90 |
| **VIX** | NO_TRADE | 71 | 69 | 91 | 85 |

これらは取得データに対するモデルの主観評価であり、統計的に較正された数値ではありません。

### GOLD

GCZ26は4160.10ドルです。

前日から下落しました。

米長期金利が再び上昇する可能性と、ドル指数が底堅いことはGoldにとって逆風です。

ただし、4100ドル付近の支持候補も意識されるため、新規SELLを追いません。

### BTC

約81963ドルです。

19日の高値は約83014ドルでしたが、83500ドルの回復には届いていません。

MES45のため、既存ルールに従ってNO_TRADEです。

### ETH

約2399ドルです。

BTCと比べてETF資金需給が弱い状態です。

2500ドル回復まではBUY方向の評価を引き上げません。

### WTI

CLX26は103.66ドルですが、CLZ26は98.54ドルです。

**現在のWTIでは、どの限月を取引対象とするかが方向判断より重要です。**

CLX26の満期を考慮し、新規シグナルを発行しません。

### USDJPY

約158.54円です。

159円に再び接近しています。

ただし、介入警戒は価格だけでなく、短時間の変化率、DXY、他の円クロスとの比較で行います。

### SPX

ESZ26は7734.50です。

10月19日は反発しましたが、10月16日の下落を完全には回復していません。

VIXが18台に残っていることも踏まえ、BUY条件を急いで引き上げません。

### NASDAQ

NQZ26は29722.50です。

反発しましたが、旧SELLシグナルのEntry帯にもinvalidation条件にも到達していません。

新規BUY・SELLは発行しません。

### DXY

約101.89です。

101.80付近を割り込むか、102.20を回復するかが短期的な分岐です。

ただし、新しい方向シグナルを成立させるEntry構造は未確認です。

### US10Y

約5.14%です。

前週の債券買い戻しが継続するかどうかは不透明になっています。

5.00%方向への再低下と、5.20%回復を監視します。

### VIX

10月19日の終値は18.44でした。

前営業日の19.99から低下しています。

株式市場の警戒感はやや和らぎましたが、15.5未満には戻っていません。

---

# 5. A級候補

**新規A級：なし。**

NASDAQは前日までの下落方向から反発しました。

ただし、今回の反発だけでは上昇転換を確認できません。

一方、SELLするには、前週末の大幅下落後であり、再び急反発するリスクがあります。

WTIは限月満期、BTC・ETHはETFフローの更新不足と価格構造の弱さが問題です。

本日、以下を同時に満たす新規取引案はありません。

| A級必須条件 | 本日 |
|---|---|
| CBS ≥75 | 新規候補で未成立 |
| EMS ≥65 | 一部資産のみ |
| expected_r ≥0.45 | 新規取引案なし |
| MAE想定 ≤0.25R | 新規取引案なし |
| RR ≥1.2 | 新規取引案なし |
| SL距離 ≤TP1距離の2倍 | 新規取引案なし |
| XM最小ロット想定実損 ≤3000円 | 未確認 |

**実取引NO_TRADEです。**

---

# 6. B級監視候補

## 継続：NASDAQ SELL_PULLBACK

`20261015_NASDAQ_SELL_PULLBACK`

**ランク：B**

**invalidation：not_fired**

**実取引：NO_TRADE**

発行時のRRを再計算します。

Entry中点：

\[
\frac{30375+30475}{2}=30425
\]

SL距離：

\[
30675-30425=250
\]

TP1距離：

\[
30425-29925=500
\]

したがって、

\[
RR=\frac{500}{250}=\boxed{2.00}
\]

一致しています。

ただし、**これは10月15日の発行条件に対するRRであり、現在値29722.50からSELLする場合のRRではありません。**

### MAEと期待値

発行時のMAE想定は0.34R。

expected_rは0.30Rです。

今回もこの2つの値を変更しません。

現時点で改めてSELLする場合は、全く別のEntry、SL、TPを設定し、別のsignal_idを発行する必要があります。

### XM最小ロット制約

SL距離250ポイント、USDJPY158.54円で計算すると、

\[
3000/(250\times158.54)
\approx0.0757
\]

許容実損3000円以内に収めるには、スプレッドと滑りを除いても、1ポイント当たり約0.0757米ドル以下の損益単位が必要です。

XMの該当CFD銘柄で、その数量が最小ロットとして利用できることは未確認です。

さらに、既存シグナルはTP2_BEFORE_ENTRYを記録しています。

**B+正式認定：0件**

**新規B級：0件**

とします。

---

# 7. 触らない資産

本日は特に**WTI、NASDAQ、ETH**です。

WTIは限月満期と供給リスクが重なっています。

同じ10月19日でも、11月限と12月限で価格の方向が逆になりました。

この状態で通常のmomentumシグナルを作ると、限月固有の値動きを原油全体の値動きと誤認する危険があります。

NASDAQは反発したものの、既存の下落構造が完全に崩れたわけではありません。

急落後の戻りを即座にSELLする判断も、反発を即座にBUYする判断も見送ります。

ETHは価格・ETF需給ともに弱い状態です。

ただし、2400ドル付近での成行SELLは反発リスクがあります。

方向性が弱気でも、現在値で売る優位性は別途確認する必要があります。

---

# 8. 後日検証ポイント

## 最優先：WTIの限月間スプレッド

今回の重要な数値は、

**10月16日：2.39ドル**

**10月19日：5.12ドル**

です。

11月限と12月限の価格差が2.73ドル拡大しました。

研究では、この差が満期後にどう変化するかを追います。

特に、12月限が次の中心限月になった際、

**CLZ26の10月19日価格98.54ドル**

と、

**CLZ26の10月20日価格**

を比較します。

CLX26の103.66ドルとCLZ26の翌日価格を直接比較しません。

これによって、ロールによる架空の損益や価格変化を防止します。

---

## NASDAQ：既存SELLの追跡

10月15日発行のシグナルは、本日で4営業日目の監視対象です。

| 営業日 | 日付 | 状態 |
|---|---|---|
| 1 | 10/15 | シグナル発行 |
| 2 | 10/16 | TP2_BEFORE_ENTRY |
| 3 | 10/19 | not_fired |
| 4 | **10/20** | 継続監視 |
| 5 | **10/21** | 最終判定予定 |

invalidation条件は変更しません。

**NQZ26 >30675**

または、

**NQZ26 >30500**
かつ
**VIX <15.5**

に加えて半導体主導の反転が確認された場合です。

今回、NQは29983.50まで反発しましたが、いずれの条件にも届いていません。

重要なのは、今後の反発が半導体セクターの回復を伴うかどうかです。

---

## Crypto

BTCは80000ドル、83500ドル。

ETHは2350ドル、2500ドルを監視します。

ETFの10月19日分は未集計です。

次回確定値が入った段階で、今回の現物価格と資金フローが整合していたかを評価します。

**ETFフローがないことを理由に評価を停止せず、後日検証対象として残します。**

---

## 米長期金利とNASDAQ

10月19日はNASDAQが反発し、米長期金利も日中に大きく変動しました。

先週の研究では、金利が下落してもNASDAQが弱い状態が続いていました。

今回は、その関係が一時的に変化した可能性があります。

ただし、1営業日の反発だけでは構造変化を認定しません。

今後は、NASDAQの価格上昇とともに、AI関連企業の信用スプレッドや資金調達コストが改善するかを観察します。

---

# 9. Obsidian保存用 Observation Draft

本日のObservationをMarkdownとして作成しました。

**:chatgpt-content-reference{index="15"}[TSO Observation — 2026-10-20](sandbox:/mnt/data/TSO_Observation_2026-10-20.md)**

主要内容をチャットにも保存します。

```markdown
# TSO Observation — 2026-10-20

Model: GPT-6
Market protagonist: WTI
Regime: MIXED

Gold reference:
COMEX December 2026 GCZ26

WTI reference:
NYMEX November 2026 CLX26

crypto_grounds:
etf=有, cme=有

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

## Main finding: WTI calendar spread

October 19:

CLX26 settlement:
103.66

CLZ26 settlement:
98.54

Calendar spread:
5.12

Previous October 16 spread:
2.39

Spread expansion:
2.73

CLX26 expiration:
2026-10-20

Interpretation:

Near-expiry divergence
between November and December
WTI futures.

Do not treat the spread
as a general spot oil rise.

Do not splice different contracts.

## NASDAQ

Active signal:
20261015_NASDAQ_SELL_PULLBACK

Original Entry:
30375-30475

SL:
30675

TP1:
29925

TP2:
29600

Original RR:
2.00

Original win_prob:
0.51

Original expected_r:
0.30

Original MAE:
0.34R

October 19 NQZ26:

High:
29983.50

Low:
29226.00

Settlement:
29722.50

VIX:
18.44

Result:
TP2_BEFORE_ENTRY

invalidation_check:
20261015_NASDAQ_SELL_PULLBACK=not_fired

Actual execution:
UNKNOWN

Old pending order:
NOT AUTHORIZED

## Macro

Gold GCZ26:
4160.10

WTI CLX26:
103.66

USDJPY:
~158.54

ESZ26:
7734.50

NQZ26:
29722.50

DXY:
~101.89

US10Y:
~5.14%

VIX:
18.44

## Crypto

BTC spot:
~81963

ETH spot:
~2399

BTC CME:
~81832

ETH CME:
~2401.50

BTC ETF latest confirmed:
October 16 -82.4m USD

ETH ETF latest confirmed:
October 16 -69.7m USD

October 19 ETF:
NOT FINALIZED

BTC MES:
45

ETH MES:
39

Both:
NO_TRADE

## Research priorities

1. WTI contract expiry and rollover.
2. NQ rebound versus old SELL thesis.
3. TP2_BEFORE_ENTRY order policy.
4. AI financing and credit spreads.
5. BTC/ETH ETF flow updates.
6. XM minimum-lot risk verification.

#TSO #WTI #NASDAQ #BTC #ETH
```

---

# 10. TSO_LOG — CSV / JSON

**固定28列・10資産10行を生成し、プログラムで構造検証しました。**

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
| verified_status許容語彙 | 適合 |
| NO_TRADE行のEntry・SL・TP・RR・確率 | 空欄 |
| CSVとJSONの内容一致 | **確認済み** |

## 保存ファイル

**:chatgpt-content-reference{index="16"}[TSO_LOG CSV — 2026-10-20](sandbox:/mnt/data/TSO_LOG_2026-10-20.csv)**

**:chatgpt-content-reference{index="17"}[TSO_LOG JSON — 2026-10-20](sandbox:/mnt/data/TSO_LOG_2026-10-20.json)**

### CSV全文

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-10-20,20261020_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,61,54,89,,MIXED,64,89,93,67,68,88,GCZ26_reclaim_4185_or_break_4155.6_and_4100_support,GCZ26_20261019_settle_4160.10_high_4211.2_low_4155.6_DXY_US10Y,verified
2026-10-20,20261020_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,49,47,92,,RISK_OFF,53,86,92,55,57,45,BTC_MES_45_ETF_19Oct_pending_83500_unreclaimed,BTCUSD_20261019_approx_81963_high_83014_CME_BTC_81832_80000_83500_ETF_16Oct_m82.4,partially_verified
2026-10-20,20261020_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,43,40,94,,RISK_OFF,49,88,92,50,53,39,ETH_2500_unreclaimed_ETF_19Oct_pending_no_buy,ETHUSD_20261019_approx_2399_high_2443_CME_ETH_2401.5_ETF_16Oct_m69.7,partially_verified
2026-10-20,20261020_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,55,53,99,,EVENT,41,99,97,50,57,99,CLX26_expiry_20261020_calendar_spread_5.12_no_supply_chase,CLX26_20261019_settle_103.66_CLZ26_same_day_settle_98.54_spread_5.12_prior_spread_2.39,verified
2026-10-20,20261020_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,62,56,86,,MIXED,64,91,91,67,65,85,USDJPY_near_158.54_monitor_159_velocity_and_DXY_without_assuming_intervention,USDJPY_20261019_approx_158.54_vendor_duplicate_sessions_157.69_158.55_DXY_101.89,partially_verified
2026-10-20,20261020_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,65,59,84,,MIXED,68,89,90,69,72,88,ESZ26_bounce_watch_7773_reclaim_or_7677_failure,ESZ26_20261019_settle_7734.50_high_7773.25_low_7677.00_VIX_18.44,verified
2026-10-20,20261020_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,68,63,90,,MIXED,62,92,92,70,74,90,active_20261015_NASDAQ_SELL_PULLBACK_not_fired_TP2_before_entry_no_order,NQZ26_20261019_settle_29722.50_high_29983.50_low_29226_entry_30375_30475_SL_30675_VIX_18.44,verified
2026-10-20,20261020_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,58,54,87,,MIXED,65,89,91,65,68,83,DXY_101.80_break_or_102.20_recovery_needs_new_validation,DXY_20261019_approx_101.89_cash_index_not_DX_FUT_101.75_US10Y,partially_verified
2026-10-20,20261020_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,65,61,90,,MIXED,77,94,94,71,74,90,US10Y_vendor_5.076_intraday_vs_5.141_late_do_not_treat_as_same_timestamp,US10Y_20261019_investing_close_5.141pct_low_5.051_high_5.152_vs_20261016_5.098pct,partially_verified
2026-10-20,20261020_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,62,62,85,,MIXED,69,91,93,69,71,91,VIX_18.44_below_19.99_still_above_15.5_NQ_invalidation_aux_not_met,VIX_20261019_close_18.44_high_18.93_low_17.39_NQZ26,verified
```

### JSON

CSVと完全に同じ10資産・28項目のJSONを保存しています。

**:chatgpt-content-reference{index="18"}[TSO_LOG JSON全文](sandbox:/mnt/data/TSO_LOG_2026-10-20.json)**

NO_TRADE行のEntry、SL、TP、RR、win_prob、expected_r、risk_pctは`null`です。

既存NASDAQのB級シグナルについては、新しい日次BUY/SELL行として複製せず、Observationとinvalidation欄で追跡しています。

---

## 本日の総括

10月20日の最大の研究材料は、**WTIの11月限と12月限が逆方向に動き、スプレッドが5.12ドルまで拡大したこと**です。

通常の価格トレンドと、満期による価格形成の変化を分離する必要があります。

NASDAQは10月19日に反発し、VIXも低下しました。

ただし、既存SELLのinvalidation条件には到達していません。

方向仮説はnot_firedとして追跡を続けますが、旧指値の再利用は認めません。

BTC・ETHはETFの10月19日分が未集計です。価格とCME先物は確認できましたが、BUY条件を引き上げるだけの根拠はありません。

**最終判断：新規10資産すべてNO_TRADE。既存NASDAQ B級はnot_firedで継続監視。固定28列・10行のTSO_LOGを保存しました。**

**現在時刻：2026年10月20日07:00頃（日本時間）**  
**次指示対象：WTI11月限満期後の12月限価格形成、NASDAQ既存SELLの4営業日目のinvalidation、BTC・ETHの10月19日ETF確定フロー。**
