<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-10-21 07:00 JST -->
<!-- transport: ChatGPT read_thread complete message markdown -->
<!-- archived_at: 2026-10-20T23:02:40Z / chars: 16897 / 値は無修正 -->

# Tactical Swing OS — Daily Signal Log v2
## 2026年10月21日（水）

**使用モデル：GPT-6**  
**本日の市場の主役：BTC**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**WTI基準限月：NYMEX 2026年12月限（CLZ26）へ移行**  
**総合regime：MIXED**  
**データ基準：10月20日米国市場／10月21日07:03 JST**

10資産すべてについて、新規の市場データ検索・照合を実施しました。

金、米国株価指数先物、WTIは指定限月の価格を使用しています。BTC・ETHは米ドル建て現物です。確定清算値と遅延値が混在するため、個別に検証状態を記録しました。

**crypto_grounds: etf=有, cme=有**

10月19日のBTC・ETH ETFフローが新たに確定しました。CME先物価格も確認していますが、現物との同時刻basisおよび最新建玉の増減は十分に検証できていません。

**expected_r_basis: subjective**

本日の新規方向シグナルはありません。既存NASDAQシグナルの`expected_r=0.30`は発行時の主観値として固定します。これは未約定確率、5営業日の時間決済、シナリオ崩壊時の途中撤退を考慮した値であり、後日変更しません。

**invalidation_check: 20261015_NASDAQ_SELL_PULLBACK=not_fired**

10月20日のNQZ26の価格経路を確認しました。10月21日は5営業日目にあたり、米国市場終了後に時間経過による最終判定を行う対象です。

---

# 1. 本日の結論

| 項目 | 判定 |
|---|---|
| 新規A級 | **0件** |
| 新規B級 | **0件** |
| B+観察候補 | 0件 |
| 継続監視中の方向シグナル | NASDAQ SELL_PULLBACK：1件 |
| 既存シグナルのinvalidation | **not_fired** |
| 新規実取引 | **NO_TRADE** |
| 新規リスク配分 | 0% |
| 最大日次リスク | 0.50% |

**本日の最大の変化は、BTCのETFに5億ドルを超える資金が流入した一方、ETHでは資金流出が続いたことです。**

10月19日の米国現物ETFフローは次のとおりです。

| 資産 | 10月19日ETFフロー |
|---|---:|
| **BTC** | **+526.7百万ドル** |
| **ETH** | **-103.3百万ドル** |

BTCの純流入526.7百万ドルは、10月に入ってからの大幅な資金流出傾向に対する重要な変化です。

一方、ETHは4営業日連続の資金流出となりました。:chatgpt-content-reference{index="0"}

ただし、BTCの現物価格は約82,489ドルです。

これまで監視していた83,500ドルには届いていません。

したがって、本日の判断は、

**BTCの資金需給は改善したが、価格構造の反転は未確認**

です。

BTCのMESを前日の45から**54**へ引き上げました。

MES50未満による見送り条件は解消しましたが、それだけでBUYシグナルにはなりません。

現在は、ETF流入が価格上昇を伴って持続するかを確認する段階です。

もう一つの重要な変化は、WTIの限月切り替えです。

11月限CLX26は10月20日に最終取引を迎えました。

今後は12月限CLZ26を基準とします。

**限月切り替えによって発生する見かけの値下がりを、通常の価格下落として記録しないことが重要です。**

---

# 2. 前回判断の簡易検証

## NASDAQ SELL_PULLBACK

継続監視対象：

`20261015_NASDAQ_SELL_PULLBACK`

発行時の数値は変更しません。

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
| expected_r | 0.30R |
| MAE想定 | 0.34R |
| CBS | 78 |
| EMS | 63 |
| rank | B |

### 10月20日の価格経路

新たに確認したNQZ26の履歴は次のとおりです。

| 項目 | 10月20日 |
|---|---:|
| 高値 | **29897.75** |
| 安値 | **29399.25** |
| 日次基準値 | **29836.75** |
| 前営業日基準値 | 29722.50 |

同じ2026年12月限の先物価格を使用しています。:chatgpt-content-reference{index="1"}

10月20日は前営業日から約0.38%上昇しました。

しかし高値29897.75でも、旧Entry下限30375には到達していません。

### Invalidation判定

旧シグナルの主な失効条件は、

**NQZ26 >30675**

でした。

補助条件は、半導体主導の反転を伴う、

**NQZ26 >30500**
かつ
**VIX <15.5**

です。

10月20日のVIXは17.31でした。

したがって、いずれの条件も成立していません。:chatgpt-content-reference{index="2"}

**invalidation：not_fired**

を維持します。

### 現在の研究状態

| 検証項目 | 判定 |
|---|---|
| Entry帯到達 | 未確認・価格経路上は未到達 |
| TP1先行到達 | 過去に確認済み |
| TP2先行到達 | 過去に確認済み |
| 10月20日の反発 | 確認 |
| 価格失効条件 | 未成立 |
| 補助失効条件 | 未成立 |
| 実際のXM約定 | 未確認 |
| 研究分類 | **TP2_BEFORE_ENTRY** |

重要なのは、**方向仮説がまだ失効していないことと、旧指値が実行可能であることは別**という点です。

旧Entry帯に戻ってきた場合の期待値は、10月15日の発行時点とは異なっている可能性があります。

そのため、旧指値の再利用は認めません。

今回も仮想利益は計上しません。

---

# 3. 市場全体の前提

## 最新10資産の基準価格

| 資産 | 基準値 | 参照系列・時点 | verified_status |
|---|---:|---|---|
| GOLD | **4142.60** | GCZ26・10/20遅延値 | partially_verified |
| BTC | **約82489** | BTC/USD現物・10/20 | partially_verified |
| ETH | **約2441** | ETH/USD現物・10/20 | partially_verified |
| WTI | **97.82** | CLZ26・10/20清算値 | verified |
| USDJPY | **約158.14** | ドル円・10/20 | partially_verified |
| SPX | **7753.50** | ESZ26・10/20日次値 | partially_verified |
| NASDAQ | **29836.75** | NQZ26・10/20日次値 | partially_verified |
| DXY | **約101.71** | ドル指数・10/20 | partially_verified |
| US10Y | **約5.116%** | 米10年債利回り・10/20 | partially_verified |
| VIX | **17.31** | Cboe VIX・10/20 | verified |

GOLDの4142.60ドルは12月限の遅延取引値です。ReutersおよびMarketWatchで確認しましたが、今回の参照値を正式な取引所清算値とは断定しません。:chatgpt-content-reference{index="3"}

BTC・ETHはYahoo Financeの現物日次系列です。

10月20日のBTCは約82,489ドル、ETHは約2,441ドルでした。日次確定時刻や配信更新の違いを考慮し、近似値として扱います。:chatgpt-content-reference{index="4"}

ESZ26は7753.50、NQZ26は29836.75です。

株価指数の現物価格やETFでは代用していません。:chatgpt-content-reference{index="5"}

DXYはReutersが報じた101.71付近を採用しました。

**WSJ Dollar Indexの96.96とは異なる指数です。** この2系列を混同しません。:chatgpt-content-reference{index="6"}

米10年債利回りは約5.116%です。米財務省の10月20日分日次値を独立に確定できなかったため、主要金融メディアの終盤値を採用しています。:chatgpt-content-reference{index="7"}

VIXの17.31はCboeの10月20日参照値です。:chatgpt-content-reference{index="8"}

---

## 重要変化①：WTI限月間スプレッドの縮小

前日からの研究対象です。

| 項目 | 10月19日 | 10月20日 |
|---|---:|---:|
| CLX26・11月限 | 103.66 | **101.79** |
| CLZ26・12月限 | 98.54 | **97.82** |
| 限月間スプレッド | **5.12** | **3.97** |

単位はドル/バレルです。

10月20日の11月限最終価格は101.79ドル、12月限は97.82ドルでした。:chatgpt-content-reference{index="9"}

ここで重要なのは、**スプレッドが5.12ドルから3.97ドルへ縮小したこと**です。

縮小幅は1.15ドルです。

10月19日には期近11月限の価格だけが上昇し、限月間スプレッドが急拡大していました。

10月20日には両限月が下落し、価格差も縮小しました。

この結果は、満期に伴う需給の偏りが一部解消された可能性と整合します。

ただし、限月間スプレッドの縮小だけで、現物市場の供給逼迫が解消されたと断定することはできません。

### 本日からのWTI参照系列

今後の基準は、

**CLZ26：2026年12月限**

です。

10月19日：98.54ドル

10月20日：97.82ドル

同一限月で比較すると、下落幅は**0.72ドル、約0.73%**です。

11月限の103.66ドルから12月限の97.82ドルへ直接つないで、5.84ドルの価格下落として記録することは禁止します。

---

## 重要変化②：BTC ETFへの大幅な資金流入

Farsideの最新集計を確認しました。

| 日付 | BTC ETF | ETH ETF |
|---|---:|---:|
| 10/14 | -261.4M | -129.5M |
| 10/15 | +5.1M | -60.3M |
| 10/16 | -82.4M | -69.7M |
| **10/19** | **+526.7M** | **-103.3M** |
| 10/20 | 未集計 | 未集計 |

単位は百万米ドルです。

10月20日のFarside欄は構成ETFの大部分が未入力です。

表示上の0.0は純流入ゼロを意味しないため、未集計として扱います。:chatgpt-content-reference{index="10"}

### BTC

10月19日のBTC ETFには526.7百万ドルの純流入がありました。

そのうちBlackRockのIBITへの流入は665.2百万ドルです。

ただし、他のETFでは資金流出も発生しています。

これはETF全体への均等な資金流入ではなく、**一部の大型ETFへ資金が集中した状態**です。:chatgpt-content-reference{index="11"}

10月20日のBTC現物は約82489ドルです。

前日の約81854ドルから約0.78%上昇しています。

ただし、日中高値は83199.88ドルで、83500ドルには届きませんでした。:chatgpt-content-reference{index="12"}

ETF資金需給の改善は確認できます。

しかし、短期下落構造が解消したとはまだ判断できません。

### ETH

10月19日のETH ETFは103.3百万ドルの流出でした。

10月14日から4営業日連続の流出です。:chatgpt-content-reference{index="13"}

ETH現物は10月20日に約2441ドルまで反発しました。

しかし2500ドルを回復していません。

BTCと比較すると、資金需給の弱さが継続しています。

---

## 重要変化③：VIX低下と米株の反発

10月20日のVIXは、

**18.44 → 17.31**

へ低下しました。

約6.1%の低下です。

同時に、ESZ26は7734.50から7753.50へ、NQZ26は29722.50から29836.75へ上昇しました。

したがって、

**株価指数：反発**

**VIX：低下**

という組み合わせです。

ただし、NASDAQはまだ30000ポイントを回復していません。

また、10月21日はMetaとTeslaの決算発表予定日です。:chatgpt-content-reference{index="14"}

短期的な警戒感の後退は確認できますが、全面的なRISK_ONへ転換したとは判断しません。

---

# 4. 10資産別判断

| 資産 | 判断 | CBS | EMS | MES | no_trade_score |
|---|---|---:|---:|---:|---:|
| **GOLD** | NO_TRADE | 69 | 63 | 84 | 88 |
| **BTC** | NO_TRADE | 70 | 62 | **54** | 80 |
| **ETH** | NO_TRADE | 53 | 49 | **41** | 91 |
| **WTI** | NO_TRADE | 59 | 42 | 99 | 98 |
| **USDJPY** | NO_TRADE | 65 | 60 | 86 | 87 |
| **SPX** | NO_TRADE | 73 | 68 | 83 | 80 |
| **NASDAQ** | NO_TRADE | 75 | 64 | 88 | 88 |
| **DXY** | NO_TRADE | 68 | 65 | 82 | 85 |
| **US10Y** | NO_TRADE | 72 | 73 | 87 | 90 |
| **VIX** | NO_TRADE | 71 | 72 | 82 | 85 |

各スコアは取得できた市場データに対する主観評価です。

### GOLD

GCZ26は4142.60ドル付近です。

10月20日の安値は4130.10ドル、高値は4174.90ドルでした。

4175ドル付近の回復がなければ、短期下落構造の解消とは評価しません。

一方、4130ドル付近から成行SELLする場合、直近安値への追随となります。

NO_TRADEです。

### BTC

約82489ドルです。

ETF資金流入によりMESは54へ改善しました。

83500ドルを回復し、CME先物でも同方向の価格形成を確認できれば、BUY_PULLBACKを再評価します。

現段階では新規BUYを発行しません。

### ETH

約2441ドルです。

ETF資金流出が継続しています。

BTCと比べて相対的に弱く、2500ドル回復も未成立です。

NO_TRADEです。

### WTI

12月限は97.82ドルです。

11月限満期に伴う価格差の変化を整理する必要があります。

また、中東の供給・輸送リスクは解消したとは確認できません。

NO_TRADEです。

### USDJPY

約158.14円です。

米長期金利とDXYが低下したことと整合する円高方向の反応がありました。

ただし、介入を示す確定材料はありません。

159円接近時の短時間の価格変化率を引き続き監視します。

### SPX

ESZ26は7753.50です。

前営業日から反発しました。

しかし7800ポイントを回復しておらず、新規BUYへ十分な優位性を認めません。

### NASDAQ

NQZ26は29836.75です。

30000ポイント未回復であり、上昇転換の判断には不十分です。

旧SELLシグナルはnot_firedですが、旧Entryの再利用は認めません。

### DXY

101.71付近です。

101.50割れと102.20回復を観察します。

現状では新しい方向シグナルのEntry構造が不足しています。

### US10Y

約5.116%です。

米住宅関連指標の弱さと、原油価格の下落が金利低下の材料になりました。

ただし、金利低下が継続するかは未確定です。:chatgpt-content-reference{index="15"}

### VIX

17.31です。

前営業日から低下しています。

ただし、VIXが低下したことだけでNASDAQのSELL仮説を失効させません。

NQと半導体セクターの価格構造を合わせて判断します。

---

# 5. A級候補

**新規A級：なし。**

最も評価が改善したのはBTCです。

しかし、BTCは83500ドルを回復しておらず、ETF流入が1営業日だけの改善なのか、継続的な資金流入の始まりなのかをまだ区別できません。

NASDAQは反発していますが、今夜予定されている主要企業決算の影響が大きくなっています。

WTIは限月切り替えによる価格系列の整理が必要です。

本日、CBS75以上、EMS65以上、expected_r0.45以上、MAE想定0.25R以下を同時に満たす新規取引案はありません。

したがって、**実取引NO_TRADE**です。

---

# 6. B級監視候補

**新規B級：なし。**

**B+観察候補：なし。**

ただし、BTCはB級への再評価に最も近い監視対象です。

## BTC：BUY_PULLBACKの再評価

現在のBTCは約82489ドルです。

83500ドル回復を確認した場合、次の条件を評価します。

| 条件 | 現在 |
|---|---|
| ETF資金フロー改善 | **成立** |
| BTC現物83500回復 | 未成立 |
| CME価格の方向確認 | 部分的に確認 |
| CME建玉増減 | 未確認 |
| MES50以上 | **54で成立** |
| 正式Entry・SL・TP | 未設定 |

今回のMES改善により、BTCは以前よりBUY方向を検討しやすい状態になりました。

しかし、Entry品質が十分ではありません。

正式なB級シグナルは発行しません。

## 既存NASDAQ B級

`20261015_NASDAQ_SELL_PULLBACK`

引き続き追跡します。

発行時のRRは、

\[
RR=\frac{30425-29925}{30675-30425}
=\frac{500}{250}
=\boxed{2.00}
\]

で一致しています。

ただし、これは発行時のEntryに対するRRです。

本日現在の価格でSELLした場合のRRではありません。

### XM最小ロット制約

旧シグナルのSL距離は250ポイントです。

ドル円158.14円を使用すると、損失3000円以内に抑えるためには、スプレッド・滑りを除いて、

\[
3000/(250\times158.14)
\approx0.0759
\]

1ポイント当たり約0.0759米ドル以下の損益単位が必要です。

XMの対象銘柄で、この数量以下の最小ロットを利用できることは今回も確認できていません。

したがって、旧シグナルは引き続き**実取引NO_TRADE**です。

---

# 7. 触らない資産

本日は特に**WTI、NASDAQ、ETH**です。

WTIは限月切り替え直後です。

11月限と12月限の価格差が縮小しましたが、中東情勢による供給リスクが消えたわけではありません。

12月限へ移行した直後に新しいmomentum BUY・SELLを発行することは避けます。

NASDAQは今夜のMeta・Tesla決算が重要です。

特にMetaのAI設備投資額、収益化の見通し、Teslaの自動運転・ロボティクス投資の進展は、現在の大型テクノロジー株評価に影響する可能性があります。

ただし、決算が良好だから株価が上昇するとは限りません。

**決算内容と株価反応を別々に検証します。**

ETHはETF流出が継続しています。

ただし、現在値からSELLしても、直近支持帯からの急反発リスクがあります。

方向性が弱気であることだけでは、現在価格でSELLする根拠になりません。

---

# 8. 後日検証ポイント

## ① BTC：ETF大幅流入の持続性

本日の最重要研究対象です。

10月19日のBTC ETFは+526.7百万ドルでした。

次に確認するのは10月20日分の確定フローです。

もし2営業日連続で大幅流入となり、BTC現物も83500ドルを回復するなら、BUY方向の評価をさらに引き上げます。

一方、20日のETFが再び流出し、現物が80000ドル方向へ下落する場合は、19日の資金流入を一時的なものとして再評価します。

ただし、この段階でETF流入を将来の上昇率へ機械的に換算することはしません。

## ② NASDAQ：5営業日目の最終判定

10月15日に発行したSELLシグナルは、本日10月21日が5営業日目です。

| 営業日 | 日付 | 状態 |
|---|---|---|
| 1 | 10/15 | シグナル発行 |
| 2 | 10/16 | TP2_BEFORE_ENTRY |
| 3 | 10/19 | not_fired |
| 4 | 10/20 | **not_fired** |
| 5 | **10/21** | 最終判定対象 |

10月21日の米国市場終了後に、

**fired**

**not_firedのまま時間経過で終了**

**unknown**

のいずれかを判定します。

10月20日までの価格経路では、失効条件は成立していません。

ただし、まだ10月21日の取引を確認していないため、シグナルを今朝の時点で終了扱いにはしません。

## ③ WTI：限月切り替え後の初日

新しい基準価格は、

**CLZ26：97.82ドル**

です。

10月21日の12月限価格と直接比較します。

今後の研究では、CLX26満期直前のスプレッド拡大と、その後の縮小が一時的な現象だったかを検証します。

## ④ 米国企業決算

本日10月21日はMetaとTeslaの決算発表が予定されています。:chatgpt-content-reference{index="16"}

検証する中心テーマは、

**AI設備投資の拡大が、株価に対してプラスに働くか、それとも資金調達負担への懸念を強めるか**

です。

また、10月20日に発表されたNetflixの決算では、利益が増加した一方、今後の見通しへの懸念から時間外で株価が下落しました。:chatgpt-content-reference{index="17"}

これは、現在の市場が足元の好業績だけでなく、将来の収益成長と投資効率を重視している可能性を示す参考事例です。

## ⑤ 次の主要マクロイベント

米国9月分PCEを含む個人所得・支出統計は、BEAの公式日程では**10月29日08:30米東部時間**です。

日本時間では10月29日21:30です。:chatgpt-content-reference{index="18"}

今後のGold、NASDAQ、US10Y、DXYの判断では、10月27～28日のFOMCと併せてイベントリスクを評価します。

---

# 9. Obsidian保存用Observation Draft

本日のObservationをMarkdownファイルとして作成しました。

**:chatgpt-content-reference{index="20"}[TSO Observation — 2026-10-21](sandbox:/mnt/data/TSO_Observation_2026-10-21.md)**

主要部分をチャットにも保存します。

```markdown
# TSO Observation — 2026-10-21

Model: GPT-6
Market protagonist: BTC
Regime: MIXED

Gold reference:
COMEX December 2026 GCZ26

WTI reference:
NYMEX December 2026 CLZ26

crypto_grounds:
etf=有, cme=有

expected_r_basis:
subjective

## Conclusion

New A: 0
New B: 0
B+: 0

Actual new trades:
NO_TRADE

Risk allocation:
0%

## Main finding

BTC ETF Oct19:
+526.7m USD

ETH ETF Oct19:
-103.3m USD

BTC spot Oct20:
~82489

ETH spot Oct20:
~2441

BTC MES:
54

ETH MES:
41

Observation:

BTC institutional fund flow
improved sharply.

ETH fund flow remained negative.

BTC has not reclaimed 83500.

Result:
NO_TRADE for both.

## WTI rollover

CLX26 final Oct20:
101.79

CLZ26 Oct20:
97.82

Calendar spread:
3.97

Previous spread:
5.12

Spread contraction:
1.15

New reference:
CLZ26

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

Oct20 NQZ26 high:
29897.75

Oct20 NQZ26 low:
29399.25

Daily reference:
29836.75

Research classification:
TP2_BEFORE_ENTRY

invalidation_check:
20261015_NASDAQ_SELL_PULLBACK=not_fired

Actual execution:
UNKNOWN

Old pending order:
NOT AUTHORIZED

Tracking:
Final fifth business day Oct21.

## Macro

GCZ26:
~4142.60

USDJPY:
~158.14

ESZ26:
7753.50

NQZ26:
29836.75

DXY:
~101.71

US10Y:
~5.116%

VIX:
17.31

## Next research

1. BTC ETF flow persistence.
2. BTC 83500 reclaim.
3. ETH ETF weakness.
4. WTI December contract price formation.
5. NQ fifth-day invalidation.
6. Meta and Tesla earnings.
7. XM minimum-lot risk verification.

#TSO #BTC #ETH #WTI #NASDAQ
```

---

# 10. TSO_LOG — CSV / JSON

**固定28列・10資産10行のCSVとJSONを生成し、プログラムで構造検証しました。**

| 検証項目 | 結果 |
|---|---|
| CSV列数 | **28** |
| データ行数 | **10** |
| 資産重複 | なし |
| 資産欠落 | なし |
| `asset=NONE` | なし |
| JSONオブジェクト数 | **10** |
| 各JSONキー数 | **28** |
| regime許容語彙 | 適合 |
| verified_status許容語彙 | 適合 |
| NO_TRADE行の価格・RR・確率 | 空欄 |
| CSV・JSON内容一致 | **確認済み** |

## 保存ファイル

**:chatgpt-content-reference{index="21"}[TSO_LOG CSV — 2026-10-21](sandbox:/mnt/data/TSO_LOG_2026-10-21.csv)**

**:chatgpt-content-reference{index="22"}[TSO_LOG JSON — 2026-10-21](sandbox:/mnt/data/TSO_LOG_2026-10-21.json)**

### CSV全文

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-10-21,20261021_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,60,55,88,,MIXED,63,87,92,66,69,84,GCZ26_no_fresh_reversal_await_4175_reclaim_or_4130_break,GCZ26_20261020_delayed_4142.60_prev_4160.10_range_4130.10_4174.90_FOMC_1027,partially_verified
2026-10-21,20261021_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,68,70,80,,MIXED,62,80,88,71,70,54,ETF_Oct19_plus526.7_but_spot_83500_not_reclaimed_wait_confirm,BTCUSD_Oct20_82489_high_83199.88_CME_Oct20_around_82675_ETF_Oct19_plus526.7_Oct20_pending,partially_verified
2026-10-21,20261021_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,51,47,91,,RISK_OFF,49,89,93,55,53,41,ETH_ETF_Oct19_minus103.3_and_spot_below_2500,ETHUSD_Oct20_2440.62_high_2470.11_CME_ETH_Oct_contract_delayed_only_ETF_Oct19_minus103.3,partially_verified
2026-10-21,20261021_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,52,58,98,,EVENT,42,99,97,51,59,99,CLX26_expired_20261020_use_CLZ26_20261020_then_20261021_no_splicing,CLZ26_Oct19_98.54_Oct20_97.82_CLX26_expiry_101.79_spread_3.97_Hormuz_EIA,verified
2026-10-21,20261021_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,57,53,87,,MIXED,60,90,92,65,65,86,JPY_strength_without_confirmed_MOF_intervention_wait_159_velocity,USDJPY_Oct20_approx_158.14_BoJ_1700_158.07to158.09_DXY_101.71_US10Y_5.116,partially_verified
2026-10-21,20261021_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,70,65,80,,MIXED,68,89,91,74,73,83,ESZ26_rebound_but_7800_reclaim_unconfirmed_and_earnings_event,ESZ26_Oct20_7753.50_prev_7734.50_high_7791.25_low_7705.00_VIX_17.31,partially_verified
2026-10-21,20261021_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,67,64,88,,MIXED,64,91,92,72,75,88,20261015_NASDAQ_SELL_PULLBACK_not_fired_asof_20261020_target_before_entry_no_order_5th_day,NQZ26_Oct20_29836.75_high_29897.75_low_29399.25_original_SL_30675_VIX_17.31,partially_verified
2026-10-21,20261021_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,62,58,85,,MIXED,65,90,92,68,68,82,DXY_under_101.8_wait_101.5_break_or_102.2_reclaim,DXY_Oct20_approx_101.71_vs_Oct19_101.98_US10Y_USDJPY,partially_verified
2026-10-21,20261021_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,61,56,90,,MIXED,73,90,92,75,72,87,UST10Y_lower_on_weak_housing_not_enough_to_confirm_risk_on,UST10Y_Oct20_approx_5.116pct_from_WSJ_Oct19_Treasury_5.15pct_official_20_pending,partially_verified
2026-10-21,20261021_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,63,59,85,,MIXED,72,86,89,74,71,82,VIX_17.31_below_17.5_but_NQ30500_condition_not_met,Cboe_VIX_Oct20_close_17.31_prev_18.44_intraday_high_19.13_low_17.25,verified
```

### JSON

CSVと同一の10資産・28項目を保持するJSONファイルです。

**:chatgpt-content-reference{index="23"}[TSO_LOG JSON全文](sandbox:/mnt/data/TSO_LOG_2026-10-21.json)**

NO_TRADE行のEntry、SL、TP、RR、win_prob、expected_r、risk_pctは`null`で記録しています。

既存NASDAQ B級については、新しい日次シグナルとして複製せず、invalidation欄とObservationで追跡を継続しています。

---

## 本日の総括

**10月21日の最大の発見は、BTCのETF資金流入が大幅に改善した一方、ETHのETF流出が継続したことです。**

これまでCrypto全体を弱気に評価していましたが、BTCとETHの資金需給に明確な差が生じています。

BTCのMESは54へ改善しました。

ただし、現物価格が83500ドルを回復していないため、正式BUYは発行しません。

WTIでは11月限が満期を迎え、12月限が新しい参照系列になりました。

限月間スプレッドは5.12ドルから3.97ドルへ縮小しています。

NASDAQの既存SELLシグナルは、10月20日時点でnot_firedです。10月21日の米国市場終了後に最終判定を行う対象として維持します。

**最終判断：新規10資産すべてNO_TRADE。既存NASDAQ B級はnot_firedで追跡継続。TSO_LOG固定28列・10行を保存しました。**

**判断基準時刻：2026年10月21日07:03（日本時間）**  
**次指示対象：BTC ETFの10月20日確定値、NASDAQ既存SELLの5営業日目最終判定、WTI12月限の価格形成、Meta・Tesla決算後のNASDAQ反応。**
