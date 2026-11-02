<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-10-16 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-11-02T05:45:08Z / chars: 20192 / 値は無修正 -->

# Tactical Swing OS — Daily Signal Log v2
## 2026年10月16日（金）

**使用モデル：GPT-6**  
**本日の市場の主役：NASDAQ**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**WTI基準限月：NYMEX 2026年11月限（CLX26）**  
**総合regime：MIXED**

**データ基準：2026年10月15日米国市場終了後／10月16日07:00 JST前後**

10資産について市場データを新規取得しました。価格は清算値・終値を優先し、取得時刻の異なる遅延値は区別しています。

**crypto_grounds: etf=有, cme=有**

BTC・ETHともETFフローとCME先物の価格情報を確認しました。ETFの最新完全確定日は10月14日です。10月15日分は未集計であり、ゼロ流入とは扱いません。CME先物は確認できましたが、現物との同時刻basisおよび最新建玉の確定検証はできていません。citeturn884146view0turn884146view1turn567347search2turn567347search3

**expected_r_basis: subjective**

本日の新規方向シグナルはありません。既存NASDAQシグナルの`expected_r=0.30`は発行時の主観値として固定し、未約定確率・5営業日時間決済・途中撤退リスクを織り込んだ数値を後付けで変更しません。

**invalidation_check: 20261015_NASDAQ_SELL_PULLBACK=not_fired**

---

# 1. 本日の結論

| 項目 | 判定 |
|---|---|
| 新規A級 | **0件** |
| 新規B級 | **0件** |
| B+観察候補 | 0件 |
| 継続監視中の方向シグナル | **NASDAQ SELL_PULLBACK：1件** |
| 既存シグナルのinvalidation | **not_fired** |
| 本日の新規実取引 | **NO_TRADE** |
| 新規リスク配分 | 0% |
| 通常の日次リスク上限 | 0.50% |

**本日の最大の発見は、NASDAQが昨日のSELLシグナルのEntry帯へ戻らないまま、TP1を先に通過したことです。**

10月15日のNQZ26は、

- 日中高値：**30196.75**
- 日中安値：**29622.50**
- 清算値：**30143.75**

でした。citeturn210165view0

昨日のSELLシグナルは、

**Entry：30375–30475**

**TP1：29925**

でした。

つまり、Entry下限30375に届かず、先に29925を下回っています。

研究上の分類は、

**TARGET_BEFORE_ENTRY**

です。

これは10月6日のWTIでも発生した現象です。

方向判断は下落と整合しましたが、想定した価格で参加する機会はありませんでした。

**今回も仮想利益は計上しません。**

もう一つ重要なのは、米長期金利です。

9月PPIが大幅に上振れたにもかかわらず、米10年債利回りは約**5.19%から5.08%へ低下**しました。

市場がインフレだけでなく、AI関連企業の資金調達・信用リスクを強く意識し始めている可能性があります。citeturn143854news79turn517575search0turn143854news72

---

# 2. 前回判断の簡易検証

## NASDAQ SELL_PULLBACK

対象：

`20261015_NASDAQ_SELL_PULLBACK`

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
| expected_r | 0.30 |
| MAE想定 | 0.34R |
| CBS | 78 |
| EMS | 63 |
| rank | B |

### 10月15日の実際の価格経路

NQZ26の高値は30196.75です。

Entry下限30375との差は、

**178.25ポイント**

でした。

その後、安値は29622.50まで下落しています。

TP1の29925を**302.50ポイント下回りました**。

一方、TP2の29600には22.50ポイント届いていません。

| 検証項目 | 結果 |
|---|---|
| Entry帯30375–30475 | **未到達** |
| TP1価格29925 | **先行到達** |
| TP2価格29600 | 未到達 |
| SL30675 | 未到達 |
| 補助invalidation | 成立を確認できず |
| シグナル状態 | **not_fired** |
| 実際の約定 | 未確認 |
| 研究ラベル | **TARGET_BEFORE_ENTRY** |

価格履歴はNQZ26の同一限月です。citeturn210165view0

ここで区別すべき状態が2つあります。

**方向仮説としては、まだfiredではありません。**

しかし、**注文としての魅力は一度大きく低下しています。**

TP1を先に通過した後、再びEntry帯へ戻ってきた場合、昨日と同じ期待値が存在するとは限りません。

したがって、旧シグナルの追跡は継続しますが、実際の指値注文を無条件で維持することは推奨しません。

### TSMC決算による再評価

TSMCの2026年第3四半期純利益は**7631億台湾ドル**で、前年同期比69%増加しました。

市場予想も上回っています。

それでも米国市場では半導体株の弱さが続きました。citeturn143854news74turn143854news77turn517575news95

これは重要です。

NASDAQの弱さを単純に、

「AI半導体の需要が悪化した」

とは説明できなくなりました。

むしろ、

**半導体需要自体は強いが、AIインフラへの投資規模・資金調達・収益化に市場が不安を持っている**

という仮説の優先度が上がります。

---

# 3. 市場全体の前提

## 10月15日の主要市場

| 資産 | 最新基準値 | 比較・特徴 | verified_status |
|---|---:|---|---|
| GOLD | **4170.10** | GCZ26清算値。遅延値4193.60も確認 | partially_verified |
| BTC | 約81500–82100 | 現物。日中80000割れ | partially_verified |
| ETH | 約2418–2445 | 現物。日中2324付近まで下落 | partially_verified |
| WTI | **97.97** | CLX26清算値、約3%上昇 | verified |
| USDJPY | 約158.20 | 157.55–158.25付近のレンジ | partially_verified |
| SPX | **7791.00** | ESZ26清算値 | verified |
| NASDAQ | **30143.75** | NQZ26清算値 | verified |
| DXY | 約102.10 | 前日102.55付近から低下 | partially_verified |
| US10Y | **5.079%** | 前日5.190%から低下 | verified |
| VIX | **16.46** | Cboe公式。前日16.87 | verified |

GCZ26については、Reutersが12月限の清算値4170.10ドルを報じています。一方、MarketWatchにはその後の遅延取引値4193.60ドルが表示されています。両者を同じ時点の価格として比較せず、清算値4170.10を本日の基準にします。citeturn134110news33turn465843view1

WTIの97.97ドルは11月限清算値です。ESZ26・NQZ26は現物指数ではなく指定されたCME先物系列を使用しています。citeturn465843view2turn465843view0turn210165view0

US10Yは日次履歴で5.079%。VIXはCboe公式で16.46を確認しました。citeturn517575search0turn641933view0

## 重要なマクロ変化：PPI上振れでも金利が低下

10月15日に発表された米国9月PPIは、

**前月比：+1.3%**

**前年同月比：+6.3%**

でした。

前月比の伸びは2022年3月以来の大きさです。citeturn143854news79

通常、これだけ強いインフレ指標は米金利上昇を促す材料です。

しかし米10年債利回りは、

**10月14日：5.190%**

**10月15日：5.079%**

へ低下しました。

日中には**5.038%**まで下がっています。citeturn517575search0

この逆方向の動きを、TSOでは重要なregime変化として扱います。

現段階で考えられる説明は、インフレ警戒が消えたことではなく、AI関連株の下落や企業信用リスクへの懸念に伴って米国債が買われたというものです。

Financial Timesも、AI企業の財務・資金調達への不安が安全資産需要を強めたと報じています。citeturn143854news72

### 株式市場内部の分裂

10月15日の米国市場では、

- S&P500現物：+0.33%
- Nasdaq Composite：+0.08%
- Dow Jones：+1.08%
- フィラデルフィア半導体指数：下落継続

となりました。citeturn517575news95

ただし、TSO_LOGのSPXとNASDAQには現物指数の数値を代用しません。

この現物市場の結果は、あくまで**市場内部の強弱を確認する補助情報**です。

重要なのは、ヘルスケアなどへ資金が移る一方、AI関連株が売られている点です。

全面的なRISK_OFFというより、**セクター間の資金移動が大きいMIXED市場**と評価します。

## Crypto ETF更新

Farsideの10月14日確定値は次のとおりです。

| 日付 | BTC ETF | ETH ETF |
|---|---:|---:|
| 10/12 | -65.4M | -85.4M |
| 10/13 | +175.7M | +24.8M |
| **10/14** | **-261.4M** | **-129.5M** |
| 10/15 | 未集計 | 未集計 |

単位は百万米ドルです。citeturn884146view0turn884146view1

10月13日の流入改善は持続しませんでした。

BTC・ETHとも価格が弱く、ETF資金フローも再び悪化しています。

現物とCME先物の同期したbasis、および最新建玉の増減は確認できていないため、先物主導の売りかどうかまでは断定しません。

---

# 4. 10資産別判断

| 資産 | 今日の判断 | CBS | EMS | no_trade_score | 評価 |
|---|---|---:|---:|---:|---|
| GOLD | NO_TRADE | 73 | 71 | 82 | 金利・ドル安で反発。新規BUY条件は不十分 |
| BTC | NO_TRADE | 58 | 53 | 91 | ETF流出。MES44 |
| ETH | NO_TRADE | 54 | 50 | 94 | 2500未回復。MES42 |
| WTI | NO_TRADE | 55 | 40 | 98 | 97.97。供給ショックと在庫減少 |
| USDJPY | NO_TRADE | 65 | 61 | 86 | 158.20付近。金利低下との整合性を監視 |
| SPX | NO_TRADE | 73 | 75 | 78 | ES反発。NASDAQとの乖離 |
| NASDAQ | NO_TRADE | 76 | 67 | 87 | 旧B級監視。TP1先行到達 |
| DXY | NO_TRADE | 73 | 70 | 80 | ドル反落。101.80が次の分岐 |
| US10Y | NO_TRADE | 76 | 86 | 91 | インフレ上振れでも金利低下 |
| VIX | NO_TRADE | 70 | 75 | 83 | 一時18.01、終盤16.46 |

スコアは取得した価格・市場環境に基づく主観評価です。

本日は正式な新規方向シグナルがないため、Entry、SL、TP、RR、win_prob、expected_r、risk_pctを新規設定しません。

---

# 5. A級候補

**なし。**

現在、NASDAQの下落方向には一定の優位性があると考えています。

しかし昨日のB級シグナルでは、Entryより先にTP1価格へ到達しました。

ここで新しいSELLを発行すると、急落後の追随になりやすい状態です。

また、NASDAQは日中に29622.50まで下落した後、清算値30143.75まで戻しています。

**約521ポイントの安値からの回復**です。

下方向への勢いだけでなく、買い戻しの強さも無視できません。

現状では、A級に必要なMAE想定0.25R以下、expected_r0.45以上を満たす新規Entry案を認定しません。

---

# 6. B級監視候補

## 継続：`20261015_NASDAQ_SELL_PULLBACK`

既存シグナルは**not_fired**です。

ただし、注文の実行適格性は再評価が必要です。

昨日設定した水準は変更しません。

| 項目 | 固定値 |
|---|---:|
| Entry | 30375–30475 |
| SL | 30675 |
| TP1 | 29925 |
| TP2 | 29600 |
| RR | 2.00 |
| win_prob | 0.51 |
| expected_r | 0.30 |

RRの再計算は、

\[
\frac{30425-29925}{30675-30425}
=\frac{500}{250}
=2.00
\]

で一致します。

### 次の判断条件

重要なのは、価格が30375へ戻ってきたときです。

そこへ到達したからといって、自動的にSELLを実行するべきではありません。

**TP1先行到達後の戻り**は、最初の戻り売りとは異なる価格構造だからです。

次回は、半導体株の反発、US10Y、VIXを再評価してから参加の可否を判定します。

### Invalidation

元の条件は維持します。

**NQZ26 >30675**

または、

**NQZ26 >30500**
かつ
**VIX <15.5**

に加えて半導体主導の反転が確認された場合です。

10月15日の価格経路では、これらの成立を確認できませんでした。

したがって`not_fired`です。

### XM制約

既存シグナルのSL距離は250ポイント。

ドル円158.20円を使用すると、実損3000円以内に抑えるための損益単位は、

\[
3000/(250\times158.20)
\approx0.0759
\]

**0.0759米ドル/ポイント以下**です。

XMの対象CFD銘柄について、この条件を満たす最小ロットを今回確認できていません。

よって**実取引NO_TRADE**を維持します。

**B+観察候補も正式認定しません。**

---

# 7. 触らない資産

## WTI

本日最も慎重に扱うのはWTIです。

CLX26は**97.97ドル**で清算されました。

米EIAが原油在庫の**860万バレル減少**を報告したことが上昇材料となっています。citeturn143583news95

中東の供給・海上輸送リスクも継続しています。

現段階でSELLするには供給改善の確証が不足しています。

一方、97ドル台からのBUYは供給ショック後の追随となります。

また、CLX26は10月20日に満期を迎えるため、次週以降は限月切り替えへの注意が必要です。

**新しい12月限の価格を、11月限の前日価格と直接比較しません。**

## BTC・ETH

BTCは10月15日の現物データで一時80000ドルを下回りました。

ETHも一時2324ドル付近まで下落しています。citeturn143583search0turn517575search3

両方ともETF流出が確認されています。

BTCのMESは44、ETHは42と評価しました。

現在のTSOルールでは、BTCのMES50未満はNO_TRADE優先です。

ETHも明確な反転根拠が不足しています。

ここからの成行SELLも、急落後の反発リスクを考慮して見送ります。

## USDJPY

ドル円は約158.20円です。

10月15日の取引レンジは157.55～158.25円付近でした。citeturn998269search3

米長期金利とDXYが低下している一方、ドル円は158円台を維持しています。

ただし、これだけで介入の有無や円独自の売り圧力を断定しません。

通常のUSDJPY売買とIntervention Shock Moduleは分離します。

---

# 8. 後日検証ポイント

### ① NASDAQ：TARGET_BEFORE_ENTRY

本日最も重要な検証対象です。

**10月15日発行**

Entry：30375–30475

**同日安値：29622.50**

TP1：29925

つまり、発行したシグナルがEntryへ到達しないままTP1へ到達しました。

これは「当たったシグナル」ではなく、**方向性は整合したが、注文が成立しなかったシグナル**として記録します。

次回は、TP1先行到達後に旧指値を失効させる方針と、指値を維持する方針を比較するための研究材料にします。

### ② US10Y：5.00%接近

米10年債利回りは5.079%です。

次の重要な水準は**5.00%**です。

ここを下回ってもNASDAQが弱いなら、金利以外の要因がさらに優勢になっている可能性があります。

逆に、5.00%への接近でNASDAQが反発するなら、通常の金利感応度が回復した可能性を調べます。

### ③ GOLD：金利低下への反応

GCZ26は清算値4170.10ドル。

日中・その後の遅延値では4190ドル台も確認できました。

今後は4200ドルを回復して定着できるかを観察します。

ただし、価格の違いが取得時刻によるものである点に注意します。

### ④ SPXとNASDAQの乖離

ESZ26は日中安値7717.25から回復し、7791.00で清算されました。

NQZ26も安値から反発しましたが、半導体株の弱さが続いています。

**ESの回復にNQが追随できるか**を確認します。

### ⑤ Crypto

BTCは80000ドル、83500ドルを重要水準とします。

ETHは2400ドル、2500ドルを重要水準とします。

ETFの10月15日確定フローが出た際には、価格と資金フローの関係を再評価します。

### ⑥ WTI

98.32ドルが10月15日の高値です。

100ドル到達の有無よりも、供給障害が改善するかを優先します。

また、限月切り替え前後の価格差を記録して、ロールによる見かけの価格変化を誤認しないようにします。

---

# 9. Obsidian保存用 Observation Draft

本日のObservationをMarkdownファイルとして保存しました。

**[TSO Observation — 2026-10-16](sandbox:/mnt/data/TSO_Observation_2026-10-16.md)**

主要な記録は以下です。

```markdown
# TSO Observation — 2026-10-16

Model: GPT-6
Market protagonist: NASDAQ
Regime: MIXED

Gold reference:
COMEX December 2026 GCZ26

WTI reference:
NYMEX November 2026 CLX26

crypto_grounds:
etf=有
cme=有

expected_r_basis:
subjective

## Conclusion

New A: 0
New B: 0
New execution: NO_TRADE

Unresolved directional signal:
20261015_NASDAQ_SELL_PULLBACK

invalidation_check:
20261015_NASDAQ_SELL_PULLBACK=not_fired

## Main research finding

NQZ26:

Oct15 high:
30196.75

Oct15 low:
29622.50

Settlement:
30143.75

Existing SELL Entry:
30375-30475

SL:
30675

TP1:
29925

TP2:
29600

Result:
TARGET_BEFORE_ENTRY
ENTRY_NOT_REACHED
NOT_FIRED

Actual execution:
UNKNOWN

Research priority:
Pending-order expiry after
target_before_entry.

Do not retroactively revise
win_prob or expected_r.

## Macro

US September PPI:
+1.3% MoM
+6.3% YoY

US10Y:
5.079%

Previous:
5.190%

Intraday low:
5.038%

DXY:
~102.10

VIX:
16.46

Interpretation:
Hot inflation data
coexisted with falling Treasury yields.

Possible driver:
AI funding and credit concerns.

## TSMC

Q3 net profit:
TWD 763.1bn

YoY:
+69%

Result:
Above expectations

Observation:
Strong chipmaker results
did not eliminate technology-stock weakness.

## Crypto

BTC spot:
~81500-82100

ETH spot:
~2418-2445

BTC ETF Oct14:
-261.4m USD

ETH ETF Oct14:
-129.5m USD

Oct15 ETF:
NOT FINALIZED

BTC MES:
44

ETH MES:
42

Both:
NO_TRADE

## Other assets

GCZ26 settlement:
4170.10

WTI CLX26 settlement:
97.97

USDJPY:
~158.20

ESZ26 settlement:
7791.00

NQZ26 settlement:
30143.75

DXY:
~102.10

US10Y:
5.079%

VIX:
16.46

## Research priorities

1. NQ target_before_entry policy.
2. AI credit risk vs Treasury yields.
3. TSMC earnings vs semiconductor weakness.
4. WTI contract rollover.
5. BTC/ETH ETF flow persistence.
6. XM minimum-lot loss validation.

#TSO #NASDAQ #US10Y #WTI #BTC #ETH
```

---

# 10. TSO_LOG — CSV / JSON

**固定28列・10資産10行を生成し、構造検証しました。**

今回も新規方向シグナルはありません。

既存NASDAQのB級監視はObservationとinvalidation欄に残しています。

CSVとJSONは同じ28項目・10資産を保持しています。

### 保存ファイル

**[TSO_LOG CSV — 2026-10-16](sandbox:/mnt/data/TSO_LOG_2026-10-16.csv)**

**[TSO_LOG JSON — 2026-10-16](sandbox:/mnt/data/TSO_LOG_2026-10-16.json)**

## CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-10-16,20261016_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,64,61,82,,MIXED,71,89,92,75,73,85,prior_GOLD_SELL_fired_no_reuse_wait_GCZ26_4200_confirm_or_4120_failure,GCZ26_20261015_settle_4170.10_late_4193.60_US10Y_5.079_DXY_102.10,partially_verified
2026-10-16,20261016_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,47,46,91,,RISK_OFF,53,87,92,56,58,44,ETF_Oct14_outflow_and_MES_below_50_wait_83500_reclaim_and_CME_synchronization,BTCspot_Oct15_79789low_81573_82100_ETF_Oct14_m261.4_CME_quotes_unsynchronized,partially_verified
2026-10-16,20261016_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,45,44,94,,RISK_OFF,50,86,92,52,54,42,ETF_Oct14_outflow_and_MES_below_50_wait_2500_confirm,ETHspot_Oct15_2324low_2418_2445_ETF_Oct14_m129.5_CME_quotes_unsynchronized,partially_verified
2026-10-16,20261016_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,54,49,98,,EVENT,40,97,97,55,55,97,CLX26_supply_shock_and_expiry_20261020_no_momentum_chase,CLX26_Oct15_settle_97.97_high_98.32_low_93.58_EIA_draw_8.6m_roll,verified
2026-10-16,20261016_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,56,49,86,,MIXED,61,89,92,62,65,83,no_intervention_price_only_trigger_watch_159_with_speed_and_crossJPY,USDJPY_Oct15_157.55low_158.20late_US10Y_5.079_DXY_102.10,partially_verified
2026-10-16,20261016_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,63,60,78,,MIXED,75,87,90,78,73,86,ESZ26_rebound_after_7717_low_watch_7800_acceptance_vs_7700_break,ESZ26_Oct15_settle_7791_low_7717.25_high_7801.75_NQZ26_VIX,verified
2026-10-16,20261016_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,69,66,87,,RISK_OFF,67,94,93,74,76,92,active_20261015_NASDAQ_SELL_PULLBACK_not_fired_target_before_entry_pending_revalidation,NQZ26_Oct15_high_30196.75_low_29622.50_settle_30143.75_entry_30375_30475_tp1_29925_sl_30675_VIX,verified
2026-10-16,20261016_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,65,62,80,,MIXED,70,91,92,72,73,86,DXY_fell_from_102.55_watch_101.80_break_or_102.60_recovery,DXY_Oct15_102.10_Oct14_102.55_Oct15_range_101.88_102.29,partially_verified
2026-10-16,20261016_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,59,57,91,,EVENT,86,94,96,78,76,93,US10Y_safe_haven_rally_despite_hot_PPI_watch_5.00_and_5.20,US10Y_Oct15_5.079_Oct14_5.190_intraday_low_5.038_PPI_1.3pct_mom,verified
2026-10-16,20261016_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,58,55,83,,MIXED,75,91,90,70,70,86,VIX_intraday_18.01_but_close_16.46_watch_17.5_reclaim,VIX_Cboe_Oct15_16.46_open_17.55_Oct14_16.87_NQZ26_ESZ26,verified
```

## JSON

以下はCSVと同一内容の10資産分です。

```json
[
{"date":"2026-10-16","signal_id":"20261016_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":64,"opp_score":61,"no_trade_score":82,"risk_pct":null,"regime":"MIXED","ems":71,"ffs":89,"cds":92,"ias":75,"cbs":73,"mes":85,"invalidation":"prior_GOLD_SELL_fired_no_reuse_wait_GCZ26_4200_confirm_or_4120_failure","verification_target":"GCZ26_20261015_settle_4170.10_late_4193.60_US10Y_5.079_DXY_102.10","verified_status":"partially_verified"},
{"date":"2026-10-16","signal_id":"20261016_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":47,"opp_score":46,"no_trade_score":91,"risk_pct":null,"regime":"RISK_OFF","ems":53,"ffs":87,"cds":92,"ias":56,"cbs":58,"mes":44,"invalidation":"ETF_Oct14_outflow_and_MES_below_50_wait_83500_reclaim_and_CME_synchronization","verification_target":"BTCspot_Oct15_79789low_81573_82100_ETF_Oct14_m261.4_CME_quotes_unsynchronized","verified_status":"partially_verified"},
{"date":"2026-10-16","signal_id":"20261016_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":45,"opp_score":44,"no_trade_score":94,"risk_pct":null,"regime":"RISK_OFF","ems":50,"ffs":86,"cds":92,"ias":52,"cbs":54,"mes":42,"invalidation":"ETF_Oct14_outflow_and_MES_below_50_wait_2500_confirm","verification_target":"ETHspot_Oct15_2324low_2418_2445_ETF_Oct14_m129.5_CME_quotes_unsynchronized","verified_status":"partially_verified"},
{"date":"2026-10-16","signal_id":"20261016_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":54,"opp_score":49,"no_trade_score":98,"risk_pct":null,"regime":"EVENT","ems":40,"ffs":97,"cds":97,"ias":55,"cbs":55,"mes":97,"invalidation":"CLX26_supply_shock_and_expiry_20261020_no_momentum_chase","verification_target":"CLX26_Oct15_settle_97.97_high_98.32_low_93.58_EIA_draw_8.6m_roll","verified_status":"verified"},
{"date":"2026-10-16","signal_id":"20261016_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":56,"opp_score":49,"no_trade_score":86,"risk_pct":null,"regime":"MIXED","ems":61,"ffs":89,"cds":92,"ias":62,"cbs":65,"mes":83,"invalidation":"no_intervention_price_only_trigger_watch_159_with_speed_and_crossJPY","verification_target":"USDJPY_Oct15_157.55low_158.20late_US10Y_5.079_DXY_102.10","verified_status":"partially_verified"},
{"date":"2026-10-16","signal_id":"20261016_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":63,"opp_score":60,"no_trade_score":78,"risk_pct":null,"regime":"MIXED","ems":75,"ffs":87,"cds":90,"ias":78,"cbs":73,"mes":86,"invalidation":"ESZ26_rebound_after_7717_low_watch_7800_acceptance_vs_7700_break","verification_target":"ESZ26_Oct15_settle_7791_low_7717.25_high_7801.75_NQZ26_VIX","verified_status":"verified"},
{"date":"2026-10-16","signal_id":"20261016_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":69,"opp_score":66,"no_trade_score":87,"risk_pct":null,"regime":"RISK_OFF","ems":67,"ffs":94,"cds":93,"ias":74,"cbs":76,"mes":92,"invalidation":"active_20261015_NASDAQ_SELL_PULLBACK_not_fired_target_before_entry_pending_revalidation","verification_target":"NQZ26_Oct15_high_30196.75_low_29622.50_settle_30143.75_entry_30375_30475_tp1_29925_sl_30675_VIX","verified_status":"verified"},
{"date":"2026-10-16","signal_id":"20261016_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":65,"opp_score":62,"no_trade_score":80,"risk_pct":null,"regime":"MIXED","ems":70,"ffs":91,"cds":92,"ias":72,"cbs":73,"mes":86,"invalidation":"DXY_fell_from_102.55_watch_101.80_break_or_102.60_recovery","verification_target":"DXY_Oct15_102.10_Oct14_102.55_Oct15_range_101.88_102.29","verified_status":"partially_verified"},
{"date":"2026-10-16","signal_id":"20261016_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":59,"opp_score":57,"no_trade_score":91,"risk_pct":null,"regime":"EVENT","ems":86,"ffs":94,"cds":96,"ias":78,"cbs":76,"mes":93,"invalidation":"US10Y_safe_haven_rally_despite_hot_PPI_watch_5.00_and_5.20","verification_target":"US10Y_Oct15_5.079_Oct14_5.190_intraday_low_5.038_PPI_1.3pct_mom","verified_status":"verified"},
{"date":"2026-10-16","signal_id":"20261016_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":58,"opp_score":55,"no_trade_score":83,"risk_pct":null,"regime":"MIXED","ems":75,"ffs":91,"cds":90,"ias":70,"cbs":70,"mes":86,"invalidation":"VIX_intraday_18.01_but_close_16.46_watch_17.5_reclaim","verification_target":"VIX_Cboe_Oct15_16.46_open_17.55_Oct14_16.87_NQZ26_ESZ26","verified_status":"verified"}
]
```

---

## 本日の総括

今回の研究上の最大の成果は、**NASDAQのB級SELLシグナルが、Entryに到達しないままTP1へ先行到達したこと**です。

同様の問題はWTIでも発生しており、TSOでは「方向判断の精度」と「実際に約定できるEntry設計」を別々に較正する必要性が高まっています。

もう一つ重要なのは、米PPIが大幅に上振れたにもかかわらず、米10年債利回りが5.08%付近へ低下したことです。

AI関連企業の信用・資金調達リスクと、安全資産としての米国債需要を分離して評価する必要があります。

**最終判断：新規10資産すべてNO_TRADE。既存NASDAQ B級はnot_firedで継続監視。固定28列・10行のTSO_LOGを保存しました。**

**次指示対象：NASDAQのTARGET_BEFORE_ENTRY後の価格経路、US10Yの5.00%接近、WTIの限月切り替え、BTC・ETHのETFフロー更新。**
