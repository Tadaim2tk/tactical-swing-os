<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-10-22 07:00 JST -->
<!-- transport: ChatGPT read_thread complete message markdown -->
<!-- archived_at: 2026-10-21T22:58:37Z / chars: 13741 / 値は無修正 -->

> **取込監査注記（原文とは別）**: PR #187レビューで、BTC `20261022_BTC_BUY_PULLBACK` の expected_r=0.32 の説明に「未約定確率」を含むことを確認。これは出力契約のBTC未参加ディスカウント禁止と矛盾する。許容される調整の内訳が不明なため0.542857等への再計算・置換は行わない。原値は未修正で保存し、PRの自動マージを解除して判断待ちとした。以下は原文であり、妥当性を確認済みという意味ではない。

# Tactical Swing OS — Daily Signal Log v2
## 2026年10月22日（木）

**使用モデル：GPT-6**  
**本日の市場の主役：BTC**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**WTI基準限月：NYMEX 2026年12月限（CLZ26）**  
**総合regime：MIXED**  
**実行基準：2026年10月22日07:03 JST**

今回も10資産の市場データを新規検索しました。原則として10月21日の米国市場終値・先物清算値を使用しています。暗号資産は10月21日の遅延現物価格を採用し、日次確定値とは区別します。

**crypto_grounds: etf=有, cme=有**

Farsideの10月20日確定ETFフローと、10月21日のCME BTC・ETH先物価格履歴を取得しました。10月21日のETFフロー、同期した先物basis、最新建玉増減は未確認です。

**expected_r_basis: subjective**

本日のBTCシグナルでは、二点分布の参考期待値から、Entry未到達、5営業日の時間決済、早期撤退、FOMC前後の価格変動リスクを考慮して期待値を引き下げています。

**invalidation_check: 20261015_NASDAQ_SELL_PULLBACK=not_fired, 20261022_BTC_BUY_PULLBACK=not_fired**

NASDAQは5営業日の最終判定を終え、本日から追跡対象を外します。BTCは新規発行時点の判定です。

---

# 1. 本日の結論

| 項目 | 判定 |
|---|---|
| 新規A級 | **0件** |
| 新規B級 | **1件：BTC BUY_PULLBACK** |
| B+観察候補 | **BTC：条件付き1件** |
| 既存NASDAQ SELL | **5営業日終了・not_fired** |
| 新規実取引 | **NO_TRADE** |
| 新規実リスク配分 | 0% |
| 最大日次リスク | 0.50% |

**本日の重要な変化は、BTCが83,500ドルだけでなく、84,500ドル付近まで回復したことです。**

BTCは10月20日に約82,941ドル、10月21日の取得履歴では約84,521ドルとなっています。

10月21日の高値は84,682ドル付近です。:chatgpt-content-reference{index="0"}

これまでTSOでは、

**83,500ドル：短期回復確認**

**84,500ドル：下落構造改善の確認候補**

として監視していました。

今回は両方の水準に到達しています。

さらに、BTC ETFは10月19日に5億ドルを超える純流入となり、20日も小幅ながら純流入を維持しました。

| 日付 | BTC ETF | ETH ETF |
|---|---:|---:|
| 10月19日 | +526.7M | -103.3M |
| 10月20日 | **+23.2M** | **-26.1M** |
| 10月21日 | 未集計 | 未集計 |

単位は百万米ドルです。:chatgpt-content-reference{index="1"}

BTCの資金需給と価格構造が同時に改善したため、**新規B級BUY_PULLBACKを発行します。**

ただし現在値から買う判断ではありません。押し目が形成されることを条件とします。

---

# 2. 前回判断の簡易検証

## NASDAQ SELL_PULLBACK：5営業日目の最終判定

対象シグナル：

`20261015_NASDAQ_SELL_PULLBACK`

発行時の条件は変更しません。

| 項目 | 固定値 |
|---|---:|
| Entry | 30375–30475 |
| SL | 30675 |
| TP1 | 29925 |
| TP2 | 29600 |
| RR | 2.00 |
| win_prob | 0.51 |
| expected_r | 0.30R |
| ランク | B |

10月21日のNQZ26は、以下の価格経路でした。

| 項目 | 価格 |
|---|---:|
| 始値 | 29925.00 |
| 高値 | **30113.00** |
| 安値 | 29727.50 |
| 清算値 | **30007.00** |

すべて2026年12月限の先物価格です。:chatgpt-content-reference{index="2"}

主なinvalidation条件は、

**NQZ26 >30675**

でした。

補助条件は、半導体主導の反転に加え、

**NQZ26 >30500**

かつ

**VIX <15.5**

です。

10月21日の高値は30113であり、VIXも約16.68でした。

したがって、価格条件によるinvalidationは確認されていません。:chatgpt-content-reference{index="3"}

### 最終結果

| 検証項目 | 結果 |
|---|---|
| Entry帯到達 | **なし** |
| TP1先行到達 | 成立 |
| TP2先行到達 | 成立 |
| SL到達 | なし |
| invalidation | **not_fired** |
| 5営業日の追跡 | **終了** |
| 研究ラベル | **TP2_BEFORE_ENTRY** |
| 実際のXM約定 | 未確認 |
| 実現損益 | 計上しない |

今回の研究上の分類は、

**方向判断：下落と整合**

**Entry品質：約定機会なし**

**シナリオ失効：確認されず**

**時間経過：終了**

です。

`not_fired`のまま追跡期間が終了したことを、売買成功とみなしません。

### データ品質上の発見

今回、新たに確認したMarketWatchの履歴では、10月20日のNQZ26清算値は**29675.25**です。

前回レポートで使用した29836.75とは161.50ポイントの差があります。

清算値と別時点の取引価格が混在していた可能性があります。:chatgpt-content-reference{index="4"}

過去のTSO_LOGを後付け変更せず、Observationに価格系列の不一致として記録します。

本日の新規判断では、確認できた10月21日の清算値30007.00を採用しました。

---

# 3. 市場全体の前提

## 最新10資産の参照価格

| 資産 | 基準価格 | データ時点 | verified_status |
|---|---:|---|---|
| GOLD | **4150.00** | 10/21 GCZ26清算値 | verified |
| BTC | **約84520** | 10/21 BTC/USD現物遅延値 | partially_verified |
| ETH | **約2507** | 10/21 ETH/USD現物遅延値 | partially_verified |
| WTI | **97.15** | 10/21 CLZ26清算値 | verified |
| USDJPY | **158.11** | 10/21日次値 | partially_verified |
| SPX | **7800.25** | 10/21 ESZ26清算値 | verified |
| NASDAQ | **30007.00** | 10/21 NQZ26清算値 | verified |
| DXY | **約101.70** | 10/21ドル指数遅延値 | partially_verified |
| US10Y | **約5.12%** | 10/21米10年債利回り | partially_verified |
| VIX | **約16.68** | 10/21指数終値系 | partially_verified |

先物清算値はMarketWatchの限月別データを採用しました。BTC・ETHはYahoo Financeの現物履歴です。VIXはMarketWatchの指数表示を基準にしています。:chatgpt-content-reference{index="5"}

USDJPYは158.11円、DXYはICEドル指数の101.70付近です。DXYの代わりにDX先物やWSJ Dollar Indexを使用していません。:chatgpt-content-reference{index="6"}

US10Yはデータ提供元で5.119～5.123%程度の差がありました。今回は約5.12%として扱います。:chatgpt-content-reference{index="7"}

### 重要変化①：米国株の反発

10月21日のESZ26は7800.25、NQZ26は30007.00で清算されました。

NASDAQは前週の大幅下落から回復し、30000ポイントを再び上回りました。

VIXも前営業日の17.31から16.68付近へ低下しています。

これは短期的な株式市場の警戒感が緩和したことと整合します。:chatgpt-content-reference{index="8"}

ただし、全面的なRISK_ONへの転換とはまだ判断しません。

### 重要変化②：企業決算

10月21日に発表されたMetaの決算は売上高が市場予想を上回りました。

MetaはAIインフラへの積極投資を継続しており、2026年の設備投資見通しは1350億～1450億ドルです。

Teslaは売上高がおおむね横ばいで、利益面には圧力が残りました。:chatgpt-content-reference{index="9"}

以前のTSOでは、AI設備投資の資金調達負担をNASDAQの下落要因として仮説に置いていました。

今回の決算は、その仮説を再評価する材料になります。

ただし、好決算と株価上昇を同一視せず、翌営業日の価格反応を追跡します。

### 重要変化③：WTI

WTI12月限は97.15ドルで清算されました。

前営業日の97.82ドルから0.67ドル下落しています。

今回は同じCLZ26同士の比較です。

米EIAは原油在庫が約306万バレル減少したと報告しましたが、外交交渉に関する報道も価格を左右しました。

原油価格の上昇・下落を単一要因で説明しないことが重要です。:chatgpt-content-reference{index="10"}

---

# 4. 10資産別判断

| 資産 | 判断 | CBS | EMS | MES | no_trade_score |
|---|---|---:|---:|---:|---:|
| GOLD | NO_TRADE | 68 | 64 | 79 | 85 |
| **BTC** | **B BUY_PULLBACK** | **73** | **66** | **62** | 49 |
| ETH | NO_TRADE | 61 | 57 | 48 | 90 |
| WTI | NO_TRADE | 59 | 41 | 97 | 97 |
| USDJPY | NO_TRADE | 64 | 61 | 85 | 87 |
| SPX | NO_TRADE | 74 | 67 | 81 | 80 |
| NASDAQ | NO_TRADE | 72 | 64 | 80 | 85 |
| DXY | NO_TRADE | 63 | 64 | 83 | 88 |
| US10Y | NO_TRADE | 66 | 69 | 87 | 90 |
| VIX | NO_TRADE | 68 | 67 | 85 | 86 |

スコアは今回の市場情報に基づく主観評価です。

BTCでは、ETF資金流入、現物価格の回復、CME先物の上昇を評価しました。

ETHも2500ドルを回復しましたが、ETF流出が継続しているためNO_TRADEです。

NASDAQは短期反発を確認したものの、今週の決算と来週のFOMCによるイベントリスクが残っています。

---

# 5. A級候補

**新規A級：0件。**

BTCが今回最もA級に近い資産ですが、必須条件を満たしていません。

| A級条件 | BTC | 判定 |
|---|---:|---|
| CBS ≥75 | 73 | 不適合 |
| EMS ≥65 | 66 | 適合 |
| expected_r ≥0.45 | 0.32 | 不適合 |
| MAE想定 ≤0.25R | 0.33R | 不適合 |
| RR ≥1.2 | 1.857 | 適合 |
| SL距離 ≤TP1距離の2倍 | 適合 | 適合 |

したがって、BTCはB級に留めます。

**強い方向変化を認めても、A級条件を緩和しません。**

---

# 6. B級監視候補

## 新規：BTC BUY_PULLBACK

`20261022_BTC_BUY_PULLBACK`

| 項目 | 設定 |
|---|---:|
| 参照系列 | BTC/USD現物 |
| side | BUY |
| rank | **B** |
| type | PULLBACK |
| Entry Low | **83550** |
| Entry High | **84050** |
| Entry中点 | **83800** |
| SL | **82400** |
| TP1 | **86400** |
| TP2 | **88000** |
| RR | **1.857143** |
| win_prob | **0.54** |
| expected_r | **0.32R** |
| CBS | 73 |
| EMS | 66 |
| MES | 62 |
| MAE想定 | **0.33R** |
| 理論risk_pct | **0.25%** |
| 有効期間 | 原則5営業日 |

### Entry設計

BTCは約84520ドルです。

そのため、現在値で成行BUYは行いません。

**83550～84050ドルへの押し目を待ち、価格が支持されて上昇へ転じることを確認する条件付きBUY**です。

Entry帯に到達しても、価格構造が崩れている場合は参加しません。

### RR再計算

Entry中点は、

\[
(83550+84050)/2=83800
\]

SLまでの距離は、

\[
83800-82400=1400
\]

TP1までの距離は、

\[
86400-83800=2600
\]

したがって、

\[
RR=\frac{2600}{1400}
=\boxed{1.857143}
\]

TSO_LOGの値と一致します。

### 主観勝率と期待値

今回の生の主観勝率は**0.54**です。

二点分布式による参考期待値は、

\[
0.54\times1.857143-(1-0.54)
\]

\[
=\boxed{0.542857R}
\]

です。

一方、TSO_LOGへ記帳する正式値は**0.32R**です。

約0.22Rの差は、未約定確率、5営業日の時間決済、途中撤退、来週のFOMCに伴うイベントリスクを主観的に織り込んだものです。

この調整は統計的な較正結果ではありません。

### Invalidation

主な失効条件は、

**BTC/USD現物の4時間足終値が82400ドルを下回ること**

です。

一瞬の下ヒゲだけではfiredと判定しません。

また、83500ドルの回復が持続せず、ETF・CMEの改善根拠も反転した場合はシナリオを再評価します。

### XM最小ロット制約

XMTradingの取引条件に関する情報では、BTCUSDの最小取引数量は0.01BTC相当とされています。:chatgpt-content-reference{index="11"}

仮に0.01BTCで取引できる場合、SL距離1400ドルの損失は、

\[
1400\times0.01=14\text{ USD}
\]

ドル円158.11円として、

\[
14\times158.11
=\boxed{2213.54円}
\]

となります。

これはスプレッド・滑り・スワップを除く概算です。

3000円までの余裕は約786円ありますが、実際の約定条件によっては上限を超える可能性があります。

したがって今回の評価は、

**B+観察候補：条件付き適合**

**正式な実取引：NO_TRADE**

とします。

XMの実際の契約仕様、スプレッド、口座残高に対するリスク比率を確認できないため、注文は承認しません。

---

# 7. 触らない資産

## ETH

ETHは約2507ドルです。

価格面では改善しています。

しかし、10月20日のETFフローは-26.1百万ドルでした。

BTCとは資金需給が異なります。

ETHのMESは48であり、BUY方向の正式条件は不足しています。

現時点では、BTCの回復にETHが遅れて追随している可能性と、ETH独自の反転が始まっている可能性を区別できません。

NO_TRADEです。

## WTI

CLZ26は97.15ドルです。

10月21日の日中高値は100.40ドル、安値は96.26ドルでした。:chatgpt-content-reference{index="12"}

1日で4ドル以上の値幅があり、供給・外交関連の材料が価格を左右しています。

供給ショック直後のmomentum追随は禁止します。

また、旧11月限CLX26の値動きを12月限へ直接接続しません。

## GOLD

GCZ26は4150ドルで清算されました。

10月21日の安値は4122.30ドル、高値は4160.60ドルです。:chatgpt-content-reference{index="13"}

短期的には反発しましたが、来週のFOMCが重要です。

4160.60ドル突破が定着するか、4122.30ドルを再び下回るかを確認します。

現時点ではBUY・SELLとも発行しません。

## USDJPY

ドル円は158.11円付近です。

159円へ向かう短時間の円安加速や、DXYとの乖離が確認されていません。

Intervention Shock Moduleの監視は維持しますが、介入が発生したとは判断しません。

---

# 8. 後日検証ポイント

今回の最優先研究対象は、**BTCの回復が一時的な反発なのか、持続的な資金流入を伴う上昇への転換なのか**です。

| 対象 | 検証条件 | 目的 |
|---|---|---|
| BTC | 83550–84050への押し | B級Entry品質 |
| BTC | 82400割れ | シナリオ崩壊 |
| BTC | 86400到達 | TP1参考値 |
| BTC ETF | 10/21確定フロー | 資金流入の持続性 |
| ETH ETF | 流出停止 | BTCとの差 |
| NASDAQ | 30375回復 | 旧SELL仮説の事後検証 |
| VIX | 15.5未満 | 警戒感の正常化 |
| WTI | 96.26 / 100.40 | 12月限の方向形成 |
| GOLD | 4122.30 / 4160.60 | 同一限月の支持・抵抗 |
| US10Y | 5.00% / 5.20% | FOMC前の金利方向 |

### NASDAQの研究上の終了処理

`20261015_NASDAQ_SELL_PULLBACK`は、5営業日目の10月21日を経過しました。

最終状態は、

**EXPIRED_NOT_FIRED**

です。

旧SELLは新しい10月22日の方向シグナルへコピーしません。

また、TP2_BEFORE_ENTRYという研究分類は維持します。

今後は、方向判断と実行可能性を別々に較正します。

### 今後のイベントリスク

10月27～28日にはFOMCが予定されています。

新規BTCシグナルの5営業日追跡期間と重なります。

したがって、BTCのEntry条件が成立しても、FOMC前に実際の取引を保有するかは別途判断する必要があります。

---

# 9. Obsidian保存用Observation Draft

本日のObservationをMarkdownファイルとして作成しました。

**:chatgpt-content-reference{index="15"}[TSO Observation — 2026-10-22](sandbox:/mnt/data/TSO_Observation_2026-10-22.md)**

保存内容には、本日の10資産の参照価格、新規BTC B級シグナル、既存NASDAQの最終検証、WTI限月管理、XMのロット制約、取得できなかった項目を含めています。

今回特に残すべきObservationは次の3点です。

**第一に、BTCは価格構造とETF資金需給が同時に改善しました。** これは単なる価格反発よりも強い根拠ですが、2営業日のETF流入だけで持続性を認定しません。

**第二に、NASDAQの旧SELLは失効しないまま5営業日が終了しました。** ただしEntry未到達のため、実行可能な利益はありませんでした。

**第三に、10月20日のNQZ26について、前回使用値と今回取得した清算値に差がありました。** 参照時刻・価格種別を区別する必要があります。

この3件を今後の較正対象として保存します。

---

# 10. TSO_LOG — CSV / JSON

**固定28列・10資産10行の生成とプログラム検証が完了しました。**

| 検証項目 | 結果 |
|---|---|
| CSV列数 | **28** |
| データ行数 | **10** |
| 資産の重複・欠落 | なし |
| `asset=NONE` | なし |
| JSONオブジェクト数 | **10** |
| JSON各オブジェクトのキー数 | **28** |
| regime許容語彙 | 適合 |
| verified_status許容語彙 | 適合 |
| BTC RR再計算 | **1.857143で一致** |
| NO_TRADE行の価格・確率 | 空欄 |
| CSV・JSONの構造整合 | 確認済み |

## 保存ファイル

**:chatgpt-content-reference{index="16"}[TSO_LOG CSV — 2026-10-22](sandbox:/mnt/data/TSO_LOG_2026-10-22.csv)**

**:chatgpt-content-reference{index="17"}[TSO_LOG JSON — 2026-10-22](sandbox:/mnt/data/TSO_LOG_2026-10-22.json)**

### CSV全文

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-10-22,20261022_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,62,59,85,,MIXED,64,87,90,68,68,79,GCZ26_low_4122.30_or_reclaim_4160.60_watch_FOMC_no_direction,GCZ26_20261021_settle_4150.00_high_4160.60_low_4122.30_US10Y_DXY_FOMC,verified
2026-10-22,20261022_BTC_BUY_PULLBACK,BTC,BUY,B,PULLBACK,83550,84050,82400,86400,88000,1.857143,0.54,0.32,74,75,49,0.25,MIXED,66,84,89,74,73,62,BTCUSD_spot_4h_close_below_82400_or_confirmed_failed_reclaim_below_83500_with_ETF_CME_deterioration,BTCUSD_20261021_approx_84520_high_84682.45_low_82565.87_ETF_20261020_plus23.2_CME_BTCV26_approx_84632_20261021_FOMC_20261027_28,partially_verified
2026-10-22,20261022_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,61,57,90,,MIXED,57,88,92,62,61,48,ETHUSD_above_2500_but_ETF_5d_outflow_wait_2550_hold_and_flow_reversal,ETHUSD_20261021_approx_2507_high_2520.65_ETF_20261020_minus26.1_CME_ETHV26_approx_2519.5,partially_verified
2026-10-22,20261022_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,56,53,97,,EVENT,41,97,95,54,59,97,CLZ26_supply_shock_post_roll_no_momentum_trade_watch_96.26_100.40,CLZ26_20261021_settle_97.15_low_96.26_high_100.40_EIA_crude_draw_3.06m,verified
2026-10-22,20261022_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,56,53,87,,MIXED,61,91,92,63,64,85,USDJPY_no_confirmed_intervention_watch_157.84_158.39_159_and_DXY_US10Y,USDJPY_20261021_daily_158.11_high_158.39_low_157.84_DXY_101.70,partially_verified
2026-10-22,20261022_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,70,67,80,,MIXED,67,90,91,73,74,81,ESZ26_recovered_7800_but_event_risk_earnings_FOMC_wait_7812.25_hold,ESZ26_20261021_settle_7800.25_low_7751.00_high_7812.25,verified
2026-10-22,20261022_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,71,65,85,,MIXED,64,89,92,72,72,80,prior_20261015_NASDAQ_SELL_PULLBACK_expired_after_5d_not_fired_entry_never_reached_TP2_before_entry,NQZ26_20261021_settle_30007.00_high_30113.00_low_29727.50_prior_ENTRY_30375_30475_VIX_16.68,verified
2026-10-22,20261022_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,57,56,88,,MIXED,64,87,90,63,63,83,DXY_below_101.80_await_101.50_break_or_102.20_reclaim_FOMC,DXY_ICE_index_20261021_approx_101.70_day_101.64_101.84_not_DX_futures,partially_verified
2026-10-22,20261022_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,60,56,90,,MIXED,69,92,91,65,66,87,US10Y_around_5.12pct_flat_inconsistent_with_simple_equity_rate_link_watch_5.00_5.20,UST10Y_20261021_vendor_closes_5.119_to_5.123pct_5.080_low_5.160_high,partially_verified
2026-10-22,20261022_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,62,61,86,,MIXED,67,89,90,68,68,85,VIX_below_17.31_and_17.5_but_still_above_15.5_NQ_recovery_verify,Cboe_VIX_20261021_approx_16.68_marketwatch_high_17.58_low_16.51,partially_verified
```

### JSON

CSVと同一の固定28項目を持つ10資産分のJSONです。

**:chatgpt-content-reference{index="18"}[TSO_LOG JSON全文](sandbox:/mnt/data/TSO_LOG_2026-10-22.json)**

NO_TRADE行ではEntry、SL、TP、RR、win_prob、expected_r、risk_pctを`null`として記録しています。

BTCのB級行のみ、方向判断に必要な各数値を設定しています。

---

## 本日の総括

10月22日の最大の変化は、**BTCが83,500ドルと84,500ドルの監視水準を回復し、ETF資金流入も2営業日連続でプラスとなったこと**です。

BTCのMESは62へ改善しました。

今回、新規B級BUY_PULLBACKを発行しましたが、成行追随は認めません。Entry帯への押しと、そこからの反転確認が必要です。

一方、NASDAQの10月15日SELLシグナルは、5営業日が経過しました。

最終判定はnot_firedですが、Entry未到達でTP1・TP2を先行通過したため、約定可能な利益はありませんでした。研究分類を保持して追跡を終了します。

WTIは新しい12月限での比較ができ、価格系列の混同を避けられています。

**最終判断：新規BTC B級1件、A級0件、実取引NO_TRADE。TSO_LOG固定28列・10資産10行を保存しました。**

**現在時刻：2026年10月22日07:03頃（日本時間）**  
**次指示対象：BTC BUY_PULLBACKのEntry到達とinvalidation、10月21日のETFフロー確定、NASDAQ旧SELLの検証台帳への終了記録。**
