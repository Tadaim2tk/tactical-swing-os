<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-10-15 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-11-02T05:45:08Z / chars: 20738 / 値は無修正 -->

# Tactical Swing OS — Daily Signal Log v2
## 2026年10月15日（木）

**使用モデル：GPT-6**  
**本日の市場の主役：NASDAQ**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**WTI基準限月：NYMEX 2026年11月限（CLX26）**  
**総合regime：EVENT**

**データ基準：2026年10月14日の米国市場終値・清算値、および10月15日07:00 JST前後に参照可能な情報。**

本日も10資産すべてについて新規の市場データ取得を試みました。CMEの限月別清算値、CboeのVIX、米国CPI、暗号資産現物・先物、ETF資金フローを確認しています。

**crypto_grounds: etf=有, cme=有**

10月13日のBTC・ETH ETF確定値と、10月14日のCME先物参考価格を利用しました。10月14日のETFフローは未確定であり、ゼロとして扱いません。

**expected_r_basis: subjective**

本日新規発行するNASDAQの期待値は、二点分布の計算値から、未約定確率、5営業日の時間決済、TSMC決算・米PPIによる早期撤退リスクを織り込んで引き下げています。

**invalidation_check: 20261015_NASDAQ_SELL_PULLBACK=not_fired**

本日新規発行する観察シグナルです。まだEntry帯に到達したことを確認したものではありません。

---

# 1. 本日の結論

| 項目 | 判定 |
|---|---|
| 新規A級 | **0件** |
| 新規B級 | **1件：NASDAQ SELL_PULLBACK** |
| B+観察候補 | 条件付き候補1件、正式認定0件 |
| 過去からの未決着シグナル | 0件 |
| 本日新規の方向判断 | 1件 |
| 新規実取引 | **NO_TRADE** |
| 実際の新規リスク配分 | 0% |
| 通常の日次リスク上限 | 0.50% |

**本日の最大の変化は、米CPIが市場予想を上回り、NASDAQ先物が大幅に下落したことです。**

10月14日に公表された米国9月分CPIは、総合指数が前年同月比**+3.7%**、前月比**+0.6%**でした。

コアCPIも前年同月比**+2.6%**、前月比**+0.3%**となり、インフレ圧力が予想より強い結果でした。citeturn682203search5turn497776view1

これを受けて米国株は下落しました。

TSOが使用する先物系列では、以下の動きが確認されています。

| 指標 | 10月13日清算値 | 10月14日清算値 | 変化 |
|---|---:|---:|---:|
| ESZ26 | 7855.75 | **7770.25** | -85.50 |
| NQZ26 | 30791.50 | **30182.75** | -608.75 |
| GCZ26 | 4177.30 | **4107.90** | -69.40 |
| CLX26 | 94.14 | **95.09** | +0.95 |

ES・NQ・GC・CLはそれぞれ指定された限月の清算値です。現物株価指数を先物価格へ代用していません。citeturn390973view0turn277156view0turn116725view0turn390973view1

今回の特徴は、**NASDAQの下落幅がSPXを大きく上回ったこと**です。

NASDAQの弱さは以前から観察していましたが、CPIを契機に下落が加速しました。

そのため本日は、初めてNASDAQのSELL_PULLBACKを正式なB級観察シグナルとして発行します。

ただし、現在の30,182付近から成行でSELLする判断ではありません。

**30,375～30,475への戻りを待ち、戻り売りが成立するかを観察します。**

---

# 2. 前回判断の簡易検証

## NASDAQ：下方向の観察が継続して成立

10月14日の判断では、NQZ26について次の水準を監視していました。

| 条件 | 判定 |
|---|---|
| 30591割れ | **成立** |
| 30900回復 | 維持できず |
| 31100回復 | 未成立 |
| 新規SELL | 前日は発行せず |

10月14日のNQZ26は、

**始値：30791.50**  
**高値：30891.50**  
**安値：30078.00**  
**清算値：30182.75**

でした。citeturn390973view0

前日に監視していた30591を明確に下回っています。

方向観察は下落と整合しましたが、前日の判断はNO_TRADEだったため、仮想利益は計上しません。

重要なのは、ここでSELL方向を認めても、価格を追わないことです。

今回は大きく下落した後なので、**戻りを待つ設計にする必要があります。**

## GOLD：4170割れから4100付近まで下落

前日のGCZ26は4177.30でした。

10月14日の清算値は4107.90となり、日中は4095.00まで下落しました。citeturn116725view0

以前のSELLシグナルはすでにfiredで閉じています。

今回の下落を使って、過去のSELL判断を成功へ書き換えることはしません。

10月14日のNO_TRADEについても、価格が下落したからといって取引利益を記録しません。

## BTC・ETH：ETF改善と価格下落が併存

10月13日のETFフローは新たに確定しました。

**BTC：+175.7百万ドル**  
**ETH：+24.8百万ドル**

どちらも純流入です。citeturn713465view0turn713465view1

ただし、10月14日の現物価格はBTCが約81,800ドル、ETHが約2,433ドルと弱い状態です。

つまり今回は、

**ETFフロー改善**
と
**価格構造の悪化**

が同時に存在しています。

資金流入が確認されたという理由だけでBUYに変更しません。

---

# 3. 市場全体の前提

## 10資産の最新基準値

| 資産 | 価格 | 参照系列・時点 | 検証状態 |
|---|---:|---|---|
| GOLD | **4107.90** | GCZ26・10/14清算値 | verified |
| BTC | 約81800 | BTC/USD現物・10/14 | partially_verified |
| ETH | 約2433 | ETH/USD現物・10/14 | partially_verified |
| WTI | **95.09** | CLX26・10/14清算値 | verified |
| USDJPY | 約158.27 | ドル円・10/14終値系 | partially_verified |
| SPX | **7770.25** | ESZ26・10/14清算値 | verified |
| NASDAQ | **30182.75** | NQZ26・10/14清算値 | verified |
| DXY | 約102.78 | ドル指数・10/14 | partially_verified |
| US10Y | 約5.19% | 米10年債利回り・10/14終盤 | partially_verified |
| VIX | **16.87** | Cboe・10/14終値 | verified |

CMEの先物清算値は前述の同一限月で統一しています。VIXはCboe公式終値16.87を採用しました。citeturn390973view0turn277156view0turn116725view0turn390973view1turn414172view0

暗号資産は取引所と日次区切りで価格差があるため、近似値です。

10月14日のCME参考価格は、

**BTC先物：約81702ドル**

**ETH先物：約2431.5ドル**

でした。ただし現物との取得時刻が完全に同期していないため、basisは確定計算しません。citeturn212680search1turn212680search3

## 最大のマクロ変化

今回のCPIは予想より強い結果でした。

その直後、米10年債利回りは一時**5.33%前後**まで上昇しています。

ところが、その後は低下し、終盤には**約5.19%**となりました。citeturn911881search2turn753755news111

この点が重要です。

前日の研究課題は、

**「金利が低下しているのにNASDAQが弱いのはなぜか」**

でした。

今回も最終的には、

**US10Y：約5.19%**

**NASDAQ：大幅下落**

という状態です。

CPIによる一時的な金利上昇だけではなく、半導体・大型テクノロジー株に対する売り圧力が独立して存在している可能性が強まりました。

Reutersによると、10月14日は半導体関連株の下落が大きく、フィラデルフィア半導体株指数は約4.3%下落しました。citeturn497776view0

このためNASDAQの方向評価では、金利だけでなく、**半導体セクター固有の需給と業績期待**を重視します。

## VIXの変化

VIXは前日の15.27から**16.87**へ上昇しました。

上昇率は約10.5%です。citeturn414172view0

株式市場の警戒度が明確に上がっています。

ただし、VIXが上昇した直後に株価指数をSELLすると、急反発に巻き込まれる可能性もあります。

したがって、VIX上昇はSELL方向の補強材料ですが、成行追随の理由にはしません。

---

# 4. 10資産別判断

| 資産 | 本日の判断 | CBS | EMS | 主な評価 |
|---|---|---:|---:|---|
| **GOLD** | NO_TRADE | 65 | 58 | GCZ26が4107.90へ急落。追随SELL禁止 |
| **BTC** | NO_TRADE | 60 | 56 | ETF流入改善、価格は弱い。MES47 |
| **ETH** | NO_TRADE | 54 | 50 | 2500割れ。MES44 |
| **WTI** | NO_TRADE | 57 | 40 | 95.09。供給ショックが継続 |
| **USDJPY** | NO_TRADE | 61 | 56 | 159接近後に反落。介入テール警戒 |
| **SPX** | NO_TRADE | 70 | 65 | ESZ26が7800割れ |
| **NASDAQ** | **B SELL_PULLBACK** | **78** | **63** | 半導体主導の下落。戻り売り限定 |
| **DXY** | NO_TRADE | 72 | 71 | 102.78付近。ドル高を追わない |
| **US10Y** | NO_TRADE | 78 | 85 | 5.33%付近から5.19%へ反落 |
| **VIX** | NO_TRADE | 73 | 70 | 16.87。警戒度上昇 |

CBS・EMS・その他のスコアは市場データを基にした主観評価です。

新規方向判断はNASDAQの1件のみです。

---

# 5. A級候補

**本日のA級はありません。**

NASDAQのSELL方向は強まっています。

しかし、今回発行するB級シグナルはA級条件を満たしません。

| A級判定条件 | NASDAQ | 結果 |
|---|---:|---|
| CBS ≥75 | 78 | 適合 |
| EMS ≥65 | 63 | 不適合 |
| expected_r ≥0.45 | 0.30 | 不適合 |
| MAE想定 ≤0.25R | 0.34R | 不適合 |
| RR ≥1.2 | 2.00 | 適合 |
| XM最小ロット損失 ≤3000円 | 未確認 | 未適合扱い |

したがって、方向性が明確でもA級へ昇格させません。

重要なのは、**強い下落を観測したことと、期待値の高い新規売り機会を得たことは別**という点です。

---

# 6. B級監視候補

## 新規 `20261015_NASDAQ_SELL_PULLBACK`

**正式ランク：B**

**実取引：NO_TRADE**

| 項目 | 設定 |
|---|---:|
| 参照系列 | NQZ26 |
| side | SELL |
| Entry Low | **30375** |
| Entry High | **30475** |
| Entry中点 | **30425** |
| SL | **30675** |
| TP1 | **29925** |
| TP2 | **29600** |
| RR | **2.00** |
| win_prob | **0.51** |
| 較正後参考win_prob | 0.51 |
| expected_r | **0.30R** |
| CBS | 78 |
| EMS | 63 |
| MAE想定 | **0.34R** |
| 理論risk_pct | 0.25% |
| 有効期間 | 原則5営業日 |

### Entry設計

NQZ26は10月14日に30182.75で清算しました。

一方、当日の高値は30891.50、安値は30078.00です。citeturn390973view0

すでに大きく下落しているため、30182付近からSELLしません。

**30375～30475への反発を待ち、そこで上昇が失速する場合だけSELLを検討します。**

単にEntry帯へ到達しただけでは、実際の注文成立を意味しません。

### RR再計算

Entry中点は、

\[
(30375+30475)/2=30425
\]

SELLなので、

\[
RR=\frac{30425-29925}{30675-30425}
\]

\[
RR=\frac{500}{250}=\boxed{2.00}
\]

TP1までの距離500ポイントに対し、SLまでの距離は250ポイントです。

SL距離はTP1距離の0.5倍で、指定条件の2倍以下を満たします。

### expected_r

二点分布式による参考値は、

\[
EV=0.51\times2.00-(1-0.51)
\]

\[
EV=1.02-0.49=0.53R
\]

ただし、今回の正式なexpected_rは**0.30R**とします。

理由は、次の3点です。

第一に、Entry帯へ反発せずに下落が継続する可能性があります。

第二に、5営業日の時間決済があるため、TP1まで到達する前に決済する場合があります。

第三に、本日はTSMC決算と米PPIがあり、半導体株の急反発によってSELL仮説が崩れる可能性があります。

この調整は主観推定であり、過去検証で較正された期待値ではありません。

### Invalidation

**GCではなく、NQZ26の同一参照系列**で判定します。

主な失効条件は、

**NQZ26 >30675**

です。

SL到達前でも、TSMC決算を受けて半導体セクターの弱気仮説が崩れ、

**NQZ26 >30500**

かつ

**VIX <15.5**

が確認された場合には、シナリオ崩壊として再評価します。

### XM最小ロット制約

今回のSL距離は250ポイントです。

ドル円を約158.27円として、実損3000円以内に抑えるには、スプレッド・滑りを除いた段階でも、1ポイント当たりの損益額を、

\[
\frac{3000}{250\times158.27}
\approx0.0758
\]

**0.0758米ドル/ポイント以下**にする必要があります。

仮にXMの該当銘柄で最小ロットが0.1米ドル/ポイントなら、

\[
250\times0.1\times158.27
\approx3957円
\]

となり、許容額を超えます。

XMの実際の銘柄名、契約数量、最小ロット、必要証拠金、スプレッドを今回確定できていません。

したがって、**B+の数値条件は満たしていても、ロット条件未確認のため正式B+には認定しません。**

**実取引NO_TRADEです。**

---

# 7. 触らない資産

## WTI

CLX26は95.09ドルまで上昇し、日中高値は96.06ドルでした。citeturn390973view1

中東の供給・輸送リスクが引き続き価格を左右しています。

過去のSELLシグナルが供給ショックで失効した経緯もあります。

現在値からのBUY追随、あるいは供給ショックの終息を先取りするSELLは、どちらも見送ります。

また、**CLX26は10月20日に満期を迎えるため、限月切り替え後の価格をそのまま前日比へ使用しません。**

## GOLD

GCZ26は4107.90まで下落しました。

前日比69.40ドルの下落です。

ドル高・CPI上振れという説明は可能ですが、金利が最終的に低下したにもかかわらずGoldが弱い点は、別の売り圧力を示唆します。

ただし4100付近の支持帯へ近づいた段階で新規SELLを追いません。

## BTC・ETH

BTCは約81,800ドル、ETHは約2,433ドルです。

10月13日のETFフローは両方プラスでしたが、価格の弱さは続いています。

BTCのMESは47、ETHは44です。

BTCは既存ルールのMES50未満に該当します。

**両資産ともNO_TRADEを維持します。**

## USDJPY

10月14日のドル円は一時158.95円付近まで上昇しました。

159円に接近しましたが、その後は158.27円付近となっています。citeturn575277search2

価格だけで為替介入の発生を判断する根拠はありません。

通常のUSDJPY売買と、Intervention Shock Moduleの研究は分離します。

---

# 8. 後日検証ポイント

## 本日15:00 JST：TSMC決算説明会

TSMCの2026年第3四半期決算説明会は、日本時間10月15日15:00に予定されています。citeturn682203search1

今回はNASDAQの新規SELLシグナルに対する最重要イベントです。

TSMCの業績・設備投資見通しが半導体需要への懸念を和らげれば、NASDAQ SELLの根拠が弱まる可能性があります。

逆に需要や収益性に懸念が残れば、半導体株の下落が継続する可能性があります。

## 本日21:30 JST：米PPI

米国9月分PPIが発表予定です。citeturn682203search2

昨日のCPI上振れに続いてPPIも予想を上回るなら、インフレ再加速への警戒が強まります。

ただし、NASDAQの下落が金利上昇によるものなのか、半導体固有の問題なのかを区別する必要があります。

### 主要な確認水準

| 資産 | 監視価格・水準 | 後日検証 |
|---|---|---|
| NASDAQ | **30375–30475** | SELL Entry帯への戻り |
| NASDAQ | **30675** | 新規SELLシナリオ失効 |
| NASDAQ | **29925** | TP1価格到達 |
| GOLD | 4095 / 4140 / 4160 | 安値更新か反発か |
| BTC | 80000 / 83500 | 支持と短期回復 |
| ETH | 2400 / 2500 | 下落継続か回復か |
| WTI | 94 / 96.06 | 供給ショックの持続 |
| USDJPY | 159 / 160 | 円安加速と介入警戒 |
| SPX | 7741 / 7820 | 下落継続と反発 |
| DXY | 102.20 / 102.50 / 102.94 | ドル高の持続 |
| US10Y | 5.15% / 5.33% | CPI後の金利再評価 |
| VIX | 15.5 / 17.5 | 警戒拡大か沈静化 |

### NASDAQの5営業日追跡

本日の新規シグナルは、原則として**10月21日まで**追跡します。

判定の優先順位は、

**シナリオ崩壊 → fired**

**未失効 → not_fired**

**判定根拠不足 → unknown**

です。

実際の注文有無や約定を推測しません。

また、Entryに到達しないままTP1価格へ到達した場合には、Observationに`target_before_entry`として記録します。

---

# 9. Obsidian保存用 Observation Draft

本日の観察内容をMarkdownファイルとして作成しました。

**[TSO Observation — 2026-10-15](sandbox:/mnt/data/TSO_Observation_2026-10-15.md)**

以下はチャット上の保存用要約です。

```markdown
# TSO Observation — 2026-10-15

Model:
GPT-6

Market protagonist:
NASDAQ

Regime:
EVENT

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

New A:
0

New B:
1

New signal:
20261015_NASDAQ_SELL_PULLBACK

Actual execution:
NO_TRADE

Committed risk:
0%

## Main observation

US CPI September:

Headline MoM:
+0.6%

Headline YoY:
+3.7%

Core MoM:
+0.3%

Core YoY:
+2.6%

NQZ26 settlement:
30182.75

Previous:
30791.50

ESZ26 settlement:
7770.25

US10Y:
~5.19%

VIX:
16.87

Observation:

NASDAQ declined sharply
despite late-session
Treasury yield relief.

Semiconductor-specific weakness
remains important.

## New NASDAQ signal

signal_id:
20261015_NASDAQ_SELL_PULLBACK

Rank:
B

Entry:
30375-30475

Mid:
30425

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

two-point EV:
0.53R

subjective expected_r:
0.30R

MAE:
0.34R

CBS:
78

EMS:
63

risk_pct:
0.25

Actual trade:
NO_TRADE

Reason:
XM minimum-lot loss
not verified within 3000 JPY.

Invalidation:
NQZ26 >30675

Alternative invalidation:
confirmed TSMC-led reversal
NQZ26 >30500
and VIX <15.5

## Crypto

BTC spot:
~81800

ETH spot:
~2433

BTC ETF Oct13:
+175.7m USD

ETH ETF Oct13:
+24.8m USD

Oct14 ETF:
not finalized

BTC CME:
~81702

ETH CME:
~2431.5

BTC MES:
47

ETH MES:
44

Both:
NO_TRADE

## Other references

GCZ26:
4107.90

CLX26:
95.09

USDJPY:
~158.27

DXY:
~102.78

US10Y:
~5.19%

VIX:
16.87

## Events

Oct15 15:00 JST:
TSMC Q3 earnings call

Oct15 21:30 JST:
US September PPI

## Invalidation check

20261015_NASDAQ_SELL_PULLBACK=not_fired

## Research priority

1. NQ rebound into Entry zone.
2. TSMC effect on semiconductors.
3. US10Y reaction to PPI.
4. Whether VIX exceeds 17.5.
5. Crypto ETF inflow versus price weakness.
6. WTI contract rollover consistency.

#TSO #NASDAQ #CPI #PPI #TSMC
```

---

# 10. TSO_LOG — CSV / JSON

**固定28列・10資産10行の生成と構造検証が完了しました。**

今回の検証結果は以下です。

| 検証項目 | 結果 |
|---|---|
| CSV列数 | 28 |
| データ行数 | 10 |
| 資産重複 | なし |
| 資産欠落 | なし |
| `asset=NONE` | なし |
| JSONオブジェクト数 | 10 |
| 各JSONキー数 | 28 |
| NASDAQ RR再計算 | **2.00で一致** |
| NO_TRADE行の売買価格・期待値 | 空欄 |
| regime語彙 | 指定6語内 |

### 保存ファイル

**[TSO_LOG CSV — 2026-10-15](sandbox:/mnt/data/TSO_LOG_2026-10-15.csv)**

**[TSO_LOG JSON — 2026-10-15](sandbox:/mnt/data/TSO_LOG_2026-10-15.json)**

## CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-10-15,20261015_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,51,55,91,,EVENT,58,91,92,62,65,87,await_GCZ26_4140_4160_retest_or_failed_break_below_4095_after_PPI,GCZ26_settle_4107.90_prev_4177.30_low_4095_DXY_US10Y_PPI,verified
2026-10-15,20261015_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,52,55,88,,RISK_OFF,56,88,91,58,60,47,BTC_below_83500_despite_Oct13_ETF_inflow_wait_for_83500_reclaim_and_CME_confirmation,BTCspot_approx_81800_CME_Oct14_81702_ETF_Oct13_plus175.7_Oct14_pending_80000_83500,partially_verified
2026-10-15,20261015_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,45,45,92,,RISK_OFF,50,89,92,50,54,44,ETH_spot_below_2500_wait_for_support_and_CME_ETF_reconfirmation,ETHspot_approx_2433_CME_Oct14_2431.5_ETF_Oct13_plus24.8_Oct14_pending_2400_2500,partially_verified
2026-10-15,20261015_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,57,49,96,,EVENT,40,97,96,55,57,98,CLX26_supply_shock_do_not_chase_or_reuse_prior_fired_sell,CLX26_settle_95.09_prev_94.14_high_96.06_Hormuz_Aramco_expiry_20261020,verified
2026-10-15,20261015_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,56,53,91,,EVENT,56,95,96,65,61,90,USDJPY_touched_158.95_near_159_avoid_momentum_intervention_tail,USDJPY_Oct14_approx_158.27_high_158.95_DXY_US10Y_MOF_PPI,partially_verified
2026-10-15,20261015_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,63,58,84,,RISK_OFF,65,91,92,67,70,87,ESZ26_fell_below_7800_wait_7741_hold_or_7820_recovery_after_events,ESZ26_settle_7770.25_prev_7855.75_low_7741_high_7879.75_NQ_VIX,verified
2026-10-15,20261015_NASDAQ_SELL_PULLBACK,NASDAQ,SELL,B,PULLBACK,30375,30475,30675,29925,29600,2.0,0.51,0.3,76,76,54,0.25,EVENT,63,93,91,78,78,90,NQZ26_above_30675_or_confirmed_TSMC_reversal_with_NQ_above_30500_and_VIX_below_15.5,NQZ26_settle_30182.75_last_30139.25_low_30078_entry_30375_30475_sl_30675_PPI_TSMC_5d,verified
2026-10-15,20261015_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,73,67,81,,EVENT,71,93,92,72,72,92,DXY_gap_rally_wait_102.5_retest_or_failure_below_102.2,DXY_Oct14_approx_102.78_high_102.94_CPI_PPI_USDJPY,partially_verified
2026-10-15,20261015_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,63,55,94,,EVENT,85,96,96,80,78,95,US10Y_rejected_5.33_and_closed_near_5.19_await_PPI_response,US10Y_Oct14_close_approx_5.19_intraday_high_5.33_PPI_Treasury,partially_verified
2026-10-15,20261015_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,62,60,83,,RISK_OFF,70,90,93,69,73,90,VIX_recovered_16.87_wait_17.5_or_15.5_break_to_reclassify,Cboe_VIX_Oct14_16.87_prev_15.27_ESZ26_NQZ26,verified
```

## JSON

以下はCSVと同一内容の全10資産分です。

```json
[
{"date":"2026-10-15","signal_id":"20261015_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":51,"opp_score":55,"no_trade_score":91,"risk_pct":null,"regime":"EVENT","ems":58,"ffs":91,"cds":92,"ias":62,"cbs":65,"mes":87,"invalidation":"await_GCZ26_4140_4160_retest_or_failed_break_below_4095_after_PPI","verification_target":"GCZ26_settle_4107.90_prev_4177.30_low_4095_DXY_US10Y_PPI","verified_status":"verified"},
{"date":"2026-10-15","signal_id":"20261015_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":52,"opp_score":55,"no_trade_score":88,"risk_pct":null,"regime":"RISK_OFF","ems":56,"ffs":88,"cds":91,"ias":58,"cbs":60,"mes":47,"invalidation":"BTC_below_83500_despite_Oct13_ETF_inflow_wait_for_83500_reclaim_and_CME_confirmation","verification_target":"BTCspot_approx_81800_CME_Oct14_81702_ETF_Oct13_plus175.7_Oct14_pending_80000_83500","verified_status":"partially_verified"},
{"date":"2026-10-15","signal_id":"20261015_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":45,"opp_score":45,"no_trade_score":92,"risk_pct":null,"regime":"RISK_OFF","ems":50,"ffs":89,"cds":92,"ias":50,"cbs":54,"mes":44,"invalidation":"ETH_spot_below_2500_wait_for_support_and_CME_ETF_reconfirmation","verification_target":"ETHspot_approx_2433_CME_Oct14_2431.5_ETF_Oct13_plus24.8_Oct14_pending_2400_2500","verified_status":"partially_verified"},
{"date":"2026-10-15","signal_id":"20261015_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":57,"opp_score":49,"no_trade_score":96,"risk_pct":null,"regime":"EVENT","ems":40,"ffs":97,"cds":96,"ias":55,"cbs":57,"mes":98,"invalidation":"CLX26_supply_shock_do_not_chase_or_reuse_prior_fired_sell","verification_target":"CLX26_settle_95.09_prev_94.14_high_96.06_Hormuz_Aramco_expiry_20261020","verified_status":"verified"},
{"date":"2026-10-15","signal_id":"20261015_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":56,"opp_score":53,"no_trade_score":91,"risk_pct":null,"regime":"EVENT","ems":56,"ffs":95,"cds":96,"ias":65,"cbs":61,"mes":90,"invalidation":"USDJPY_touched_158.95_near_159_avoid_momentum_intervention_tail","verification_target":"USDJPY_Oct14_approx_158.27_high_158.95_DXY_US10Y_MOF_PPI","verified_status":"partially_verified"},
{"date":"2026-10-15","signal_id":"20261015_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":63,"opp_score":58,"no_trade_score":84,"risk_pct":null,"regime":"RISK_OFF","ems":65,"ffs":91,"cds":92,"ias":67,"cbs":70,"mes":87,"invalidation":"ESZ26_fell_below_7800_wait_7741_hold_or_7820_recovery_after_events","verification_target":"ESZ26_settle_7770.25_prev_7855.75_low_7741_high_7879.75_NQ_VIX","verified_status":"verified"},
{"date":"2026-10-15","signal_id":"20261015_NASDAQ_SELL_PULLBACK","asset":"NASDAQ","side":"SELL","rank":"B","type":"PULLBACK","entry_low":30375,"entry_high":30475,"sl":30675,"tp1":29925,"tp2":29600,"rr":2.0,"win_prob":0.51,"expected_r":0.3,"tq_score":76,"opp_score":76,"no_trade_score":54,"risk_pct":0.25,"regime":"EVENT","ems":63,"ffs":93,"cds":91,"ias":78,"cbs":78,"mes":90,"invalidation":"NQZ26_above_30675_or_confirmed_TSMC_reversal_with_NQ_above_30500_and_VIX_below_15.5","verification_target":"NQZ26_settle_30182.75_last_30139.25_low_30078_entry_30375_30475_sl_30675_PPI_TSMC_5d","verified_status":"verified"},
{"date":"2026-10-15","signal_id":"20261015_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":73,"opp_score":67,"no_trade_score":81,"risk_pct":null,"regime":"EVENT","ems":71,"ffs":93,"cds":92,"ias":72,"cbs":72,"mes":92,"invalidation":"DXY_gap_rally_wait_102.5_retest_or_failure_below_102.2","verification_target":"DXY_Oct14_approx_102.78_high_102.94_CPI_PPI_USDJPY","verified_status":"partially_verified"},
{"date":"2026-10-15","signal_id":"20261015_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":63,"opp_score":55,"no_trade_score":94,"risk_pct":null,"regime":"EVENT","ems":85,"ffs":96,"cds":96,"ias":80,"cbs":78,"mes":95,"invalidation":"US10Y_rejected_5.33_and_closed_near_5.19_await_PPI_response","verification_target":"US10Y_Oct14_close_approx_5.19_intraday_high_5.33_PPI_Treasury","verified_status":"partially_verified"},
{"date":"2026-10-15","signal_id":"20261015_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":62,"opp_score":60,"no_trade_score":83,"risk_pct":null,"regime":"RISK_OFF","ems":70,"ffs":90,"cds":93,"ias":69,"cbs":73,"mes":90,"invalidation":"VIX_recovered_16.87_wait_17.5_or_15.5_break_to_reclassify","verification_target":"Cboe_VIX_Oct14_16.87_prev_15.27_ESZ26_NQZ26","verified_status":"verified"}
]
```

---

## 本日の総括

本日の研究上の最大の変化は、**CPI上振れを契機にNASDAQの下落が加速した一方、米10年債利回りは最終的に低下したこと**です。

これまで観察してきた「金利低下でもNASDAQが弱い」という現象が継続しています。

今回の下落には、半導体・AI関連株固有の売り圧力も関係している可能性があります。

そのため、新規のNASDAQ SELL_PULLBACKをB級観察シグナルとして発行しました。

ただし、実際の取引ではXM最小ロットの損失制約が未確認であり、現在値からの追随SELLも禁止します。

**最終判断：新規実取引NO_TRADE。NASDAQにB級SELL_PULLBACKを1件発行。固定28列・10資産10行のTSO_LOGを保存しました。**

**次指示対象：TSMC決算と米PPI発表後のNQZ26・US10Y・VIXの連動、およびNASDAQ新規SELLシグナルのinvalidation判定。**
