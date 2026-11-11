<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-10-12 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-10-13T20:23:35Z / chars: 17919 / 値は無修正 -->

# Tactical Swing OS — Daily Signal Log v2
## 2026年10月12日（月）

**使用モデル：GPT-6**  
**本日の市場の主役：BTC**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**総合regime：MIXED**

**データ基準：2026年10月12日06:55 JST前後。**

BTC・ETHは10月11日の現物市場データ、その他8資産は原則10月9日の終値・清算値を使用しました。米国先物の週明け取引再開直前のため、金曜日の値を新しい月曜日の価格として扱っていません。

**crypto_grounds: etf=有, cme=有**

Farsideの10月9日確定ETFフローと、CME BTC・ETH先物の10月9日履歴を取得しました。週末の現物価格と金曜日のCME価格から、同時点のbasisは計算しません。

**expected_r_basis: subjective**

本日は新規方向シグナルがないため、expected_rは全行空欄です。未約定確率、5営業日の時間決済、イベント時の早期撤退を考慮する運用方針は維持します。

**invalidation_check: none**

既存の方向シグナルはすべて決着済みです。

---

# 1. 本日の結論

| 項目 | 判断 |
|---|---|
| 新規A級 | **0件** |
| 新規B級 | **0件** |
| B+観察候補 | 0件 |
| 未決着方向シグナル | 0件 |
| 本日の実取引 | **NO_TRADE** |
| 新規リスク配分 | 0% |
| 最大日次リスク上限 | 0.50% |

本日の最大の変化は、**BTCが83,500ドルを回復した一方、ETHが相対的に弱いこと**です。

10月11日のBTC現物は約83,577ドル。10月10日の82,912ドルから約0.8%上昇しました。

一方、ETHは約2,500ドルで、前日からほぼ横ばいです。citeturn439987search0turn520827search0

ここで重要なのは、BTCの回復がCrypto全体へ波及していないことです。

さらに米国ETFの10月5～9日週間フローは、

**BTC：-678.9百万ドル**

**ETH：-542.2百万ドル**

でした。

BTCは金曜日に小幅な純流入へ転換しましたが、週全体の流出額は依然大きい状態です。citeturn545235view1turn637928view2

したがって、BTCを短期BUY候補へ再評価する余地はありますが、現時点で正式シグナルは発行しません。

また、本日は日米の祝日が重なります。

日本の現物株式市場は休場ですが、大阪取引所・東京商品取引所のデリバティブでは祝日取引が実施されます。米国では株式市場が通常取引予定である一方、SIFMAは米ドル建て債券市場の全面休場を推奨しています。citeturn713089search5turn713089search1turn520827news110

**本日は「株式は動くが、米国債現物の通常の価格発見がない」という特殊な市場環境**です。

このため、金利確認を必要とするNASDAQやGoldのA級判定には注意が必要です。

---

# 2. 前回判断の簡易検証

## BTC

10月11日の判断はNO_TRADEでした。

当時の監視水準は、

**83,500ドル：短期回復確認**

**84,500ドル：下落構造の改善確認**

です。

今回確認したBTC現物は約83,577ドルです。

したがって、最初の83,500ドルには到達しました。

しかし84,500ドルには届いていません。citeturn439987search0

判定は次のとおりです。

| 検証項目 | 結果 |
|---|---|
| 83,500回復 | 成立 |
| 84,500突破 | 未成立 |
| ETF純流入転換 | 10月9日に成立 |
| 週間ETF需給改善 | 未成立 |
| 週末CME追認 | 未確認 |
| 新規BUY条件 | **未成立** |

BTCは前日より改善しました。

しかし、改善したことと、買うべき価格に到達したことは別です。

### ETH

10月11日のETHは約2,500ドル。

前日の2,504ドル付近から大きく変わっていません。

監視していた2,550ドルも未回復です。citeturn520827search0

ETHはBTCより相対的に弱く、ETFも流出が継続しています。

NO_TRADEを維持します。

## 過去の方向シグナル

| signal_id | 最終状態 |
|---|---|
| `20261006_WTI_SELL_PULLBACK` | fired・追跡終了 |
| `20261008_GOLD_SELL_PULLBACK` | fired・追跡終了 |

両方とも新しいシグナルへ再利用しません。

また、実際のXM注文履歴は確認していないため、仮想シグナルの失効を実取引損益へ変換しません。

---

# 3. 市場全体の前提

## 主要10資産の参照価格

| 資産 | 基準値 | 参照日時 | 検証状態 |
|---|---:|---|---|
| GOLD | **4216.30** | 10/9 GCZ26清算値 | verified |
| BTC | **約83577** | 10/11 BTC/USD現物 | partially_verified |
| ETH | **約2499** | 10/11 ETH/USD現物 | partially_verified |
| WTI | **91.85** | 10/9 CLX26清算値 | verified |
| USDJPY | **約158.3** | 10/9 FX終値系 | partially_verified |
| SPX | **7859.75** | 10/9 ESZ26清算値 | verified |
| NASDAQ | **31108.75** | 10/9 NQZ26清算値 | verified |
| DXY | **102.21** | 10/9ドル指数終値 | verified |
| US10Y | **約5.24%** | 10/9米10年債利回り | verified |
| VIX | **14.84** | 10/9終値 | verified |

GCZ26、CLX26、ESZ26、NQZ26は、それぞれ契約月を特定した清算値です。NASDAQ総合やQQQをNQ先物の代用にはしていません。citeturn637928view0turn637928view1turn624296view0turn624296view3

USDJPYは提供元のセッション区切りにより158.25～158.34円程度の差があります。DXYはYahoo Financeの日次終値102.21、VIXは10月9日終値14.84です。citeturn437147search0turn437147search3turn439987search8turn545235search0

US10Yは金曜日の約5.24%を使用します。月曜日の新しい米国債現物利回りが確定したという意味ではありません。citeturn868018search0

## BTC・ETHのCME先物

新たに取得した10月9日のCME先物履歴は、

**BTC先物：82,470ドル**

**ETH先物：2,485.50ドル**

です。

いずれも遅延・履歴データであり、取引所の公式清算値とは独立に照合できていません。citeturn204643search0turn204643search2

現在のBTC現物価格はそれより高いですが、比較日時が異なります。

したがって、これを先物basis拡大や機関投資家の買い需要と解釈しません。

## ETFフロー

| 日付 | BTC ETF | ETH ETF |
|---|---:|---:|
| 10月5日 | -89.8M | -50.8M |
| 10月6日 | +118.8M | -201.9M |
| 10月7日 | -484.9M | -160.9M |
| 10月8日 | -244.1M | -72.5M |
| 10月9日 | **+21.1M** | **-56.1M** |
| **週間合計** | **-678.9M** | **-542.2M** |

単位は百万米ドルです。Farsideの各日合計から週間値を算出しています。citeturn545235view1turn637928view2

BTCでは、

**ETFフローの符号：改善**

**週間フロー：大幅マイナス**

**現物価格：小幅反発**

という状態です。

一方ETHでは、

**ETFフロー：マイナス継続**

**価格：ほぼ横ばい**

となっています。

BTCとETHの需給状態には明確な差があります。

---

# 4. 10資産別判断

| 資産 | 判断 | no_trade_score | 理由 |
|---|---|---:|---|
| **GOLD** | NO_TRADE | 92 | GCZ26の急反発後。CPI前で方向未確定 |
| **BTC** | NO_TRADE | 83 | 83,500回復。ただしMES49、週間ETF流出 |
| **ETH** | NO_TRADE | 93 | 2,550未回復。ETF流出継続 |
| **WTI** | NO_TRADE | 96 | 供給ショック・外交材料が競合 |
| **USDJPY** | NO_TRADE | 92 | 日米祝日、薄商い、介入テール |
| **SPX** | NO_TRADE | 77 | ES先物の週明け価格確認待ち |
| **NASDAQ** | NO_TRADE | 81 | NQ31,200回復未確認 |
| **DXY** | NO_TRADE | 86 | 101.80～102.50内で方向不明確 |
| **US10Y** | NO_TRADE | 98 | 米国債現物市場の休場日 |
| **VIX** | NO_TRADE | 90 | 金曜14.84。新しい株式市場の反応待ち |

各スコアは今回の市場情報に対する主観評価です。

正式な方向シグナルがないため、Entry、SL、TP、RR、win_prob、expected_r、risk_pctは設定しません。

したがって、XM最小ロットでの想定実損やMAEも、本日の実取引候補としては計算対象外です。

---

# 5. A級候補

**なし。**

本日時点で、A級の必須条件を同時に満たす取引案はありません。

特にNASDAQについては、通常なら押し目BUYを検討する余地があります。

しかし、金曜日のNQZ26清算値は31,108.75です。

10月9日の値幅は、

**安値：30,953.00**

**高値：31,266.50**

でした。citeturn624296view3

現在の最初の確認水準は31,200です。

31,200を維持してから、31,000～31,100方向への押しを作るならBUY_PULLBACKを再評価できます。

ただし今日の米国債現物市場休場により、US10Yが安定しているかを通常どおり判定できません。

**金曜日の5.24%を、そのまま月曜日の金利安定根拠として使用しない**ことが重要です。

---

# 6. B級監視候補

正式B級シグナルはありません。

B+観察候補もありません。

ただし、次の方向監視は継続します。

## BTC：BUY方向の再評価

現在のBTCは約83,577ドルです。

最初の83,500ドルを回復しました。

次に必要なのは、

**84,500ドル突破**

と、

**CME先物の追認**

です。

ETFについては、10月9日の小幅純流入が次の営業日にも続くかを確認します。

本日のMES主観評価は**49**です。

既存ルールのMES50未満に該当するため、現時点ではNO_TRADEを維持します。

## NASDAQ：BUY_PULLBACK候補

31,200回復後も、価格がそのまま上昇する場合は成行追随しません。

押し目で価格構造が維持されるかを確認します。

米国債市場が通常取引へ戻り、US10Yの反応を確認できる段階でCBS、EMS、expected_rを再評価します。

---

# 7. 触らない資産

## WTI

金曜日のWTIは91.85ドルで清算しました。

中東情勢に関する外交発言と、メキシコ湾のハリケーンに伴う生産停止が競合しています。

Reutersは10月9日、米国沖合原油生産の70%以上が停止したと報じています。citeturn520827news107

供給ショック後のmomentum追随は、現在のTSOルールで禁止しています。

旧SELLがfiredになったからといって、新規BUYへ自動反転しません。

## USDJPY

金曜終値系は約158.3円です。

159円へ接近した場合は、Intervention Shock Moduleの警戒度を上げます。

ただし、現段階では**介入を示す価格異常を確認していません**。

今日のような薄商いでは、DXYと米金利だけでなく、他の円クロスや短時間の上昇速度を比較する必要があります。

介入可能性と通常のUSDJPY BUY判断は引き続き分離します。

## ETH

ETHは約2,500ドルです。

直近のETF流出はBTCより持続的です。

2,550ドルを回復しない段階では、新規BUYを作りません。

一方、急落後の水準から成行SELLすることも避けます。

---

# 8. 後日検証ポイント

## ① 本日の祝日市場

10月12日は日本のスポーツの日、米国のコロンブス・デーです。

ただし、日本のデリバティブ市場には祝日取引があります。

**日本の現物市場休場と、先物市場の全面休場を混同しません。**

また、米国債現物市場が休場推奨日であるため、US10Yの前日値を新しい観測値として扱いません。citeturn713089search0turn713089search1

## ② BTC

監視水準：

**82,500：週末の支持候補**

**83,500：回復維持の確認**

**84,500：上方向への構造改善候補**

84,500を上回り、CMEとETFの改善が確認できれば、BUY_PULLBACK候補を再計算します。

## ③ ETH

**2,470：短期支持候補**

**2,550：回復確認**

ETH/BTC比率が低下し続ける場合、Crypto全体の回復ではなくBTC単独の反発と評価します。

## ④ GOLD

GCZ26は金曜日に4,233.70ドルまで上昇しました。

今後は、

**4,233.70：直近高値**

**4,170：反発失敗時の確認帯**

を観察します。

10月8日のSELLシグナルはfiredで確定しています。

新しいシグナルには別のsignal_idを発行します。

## ⑤ NASDAQ・SPX

NASDAQは31,200回復、SPXはES先物7,850前後の維持を確認します。

特に、US10Yが再び上昇したときにNASDAQが上昇を維持できるかを重視します。

## ⑥ 10月14日：米CPI

米労働統計局の公式日程では、9月分CPIは**2026年10月14日08:30米東部時間**に発表予定です。

日本時間では**10月14日21:30**です。citeturn520827search1

これはGold、USDJPY、NASDAQ、US10Yにとって重要なイベントです。

CPI直前の新規参加では、通常よりイベントリスクを高く評価します。

---

# 9. Obsidian保存用 Observation Draft

本日のObservationはMarkdownファイルとして保存しました。

[TSO Observation — 2026-10-12](sandbox:/mnt/data/TSO_Observation_2026-10-12.md)

主要内容を以下に記録します。

```markdown
# TSO Observation — 2026-10-12

Model:
GPT-6

Market protagonist:
BTC

Gold reference:
COMEX December 2026
GCZ26

Regime:
MIXED

crypto_grounds:
etf=有
cme=有

expected_r_basis:
subjective

## Main conclusion

New A:
0

New B:
0

B+:
0

New executions:
NO_TRADE

Active directional signals:
0

## BTC

Spot:
~83577

Previous daily reference:
~82912

Change:
~+0.8%

Oct9 CME historical:
82470

ETF Oct9:
+21.1m USD

ETF Oct5-9:
-678.9m USD

MES:
49

Observation:

BTC reclaimed 83500.

However:
84500 not recovered.

Weekly ETF flow remains negative.

CME Friday value cannot establish
synchronized weekend basis.

Result:
NO_TRADE

## ETH

Spot:
~2499

Oct9 CME historical:
2485.50

ETF Oct9:
-56.1m USD

ETF Oct5-9:
-542.2m USD

MES:
42

Observation:

ETH is weaker than BTC.

2550 resistance not recovered.

Result:
NO_TRADE

## Macro references

GCZ26:
4216.30

WTI CLX26:
91.85

USDJPY:
~158.3

ESZ26:
7859.75

NQZ26:
31108.75

DXY:
102.21

US10Y:
~5.24%

VIX:
14.84

## Holiday market

Oct12:
Japan Sports Day

Japanese cash equities:
CLOSED

JPX/OSE/TOCOM derivatives:
HOLIDAY TRADING

US fixed income:
FULL CLOSE RECOMMENDED

US equities:
SCHEDULED OPEN

Important:

Do not interpret unchanged
US10Y as new evidence
of interest-rate stability.

## Previous signals

20261006_WTI_SELL_PULLBACK:
FIRED / CLOSED

20261008_GOLD_SELL_PULLBACK:
FIRED / CLOSED

invalidation_check:
none

## Next event

2026-10-14
US September CPI
21:30 JST

## Research priorities

1. BTC 83500 hold and 84500 break.
2. ETH/BTC relative weakness.
3. US10Y and Nasdaq after holiday.
4. GCZ26 4233.70 resistance.
5. WTI supply shock normalization.
6. USDJPY intervention-tail monitoring.

#TSO #BTC #ETH #NASDAQ #US10Y
```

---

# 10. TSO_LOG — CSV / JSON

**固定28列・10資産10行の生成と検証が完了しました。**

検証内容は、28列の一致、10資産の重複・欠落なし、許容regime語彙、NO_TRADE行の数値空欄、JSONのキー順序と件数です。

### 保存用ファイル

[TSO_LOG CSV — 2026-10-12](sandbox:/mnt/data/TSO_LOG_2026-10-12.csv)

[TSO_LOG JSON — 2026-10-12](sandbox:/mnt/data/TSO_LOG_2026-10-12.json)

## CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-10-12,20261012_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,68,58,92,,EVENT,58,88,94,67,63,79,former_20261008_GOLD_SELL_fired_closed_wait_for_GCZ26_hold_4233.7_or_failure_below_4170,GCZ26_4156.1_4216.3_4233.7_US10Y_DXY_CPI_20261014,verified
2026-10-12,20261012_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,62,60,83,,MIXED,57,86,91,62,61,49,weekend_BTC_reclaim_83500_unconfirmed_MES_below_50_ETF_weekly_net_outflow,BTCspot_82912_83577_84500_CME_82470_20261009_BTCETF_plus21.1_1d_3d,partially_verified
2026-10-12,20261012_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,45,47,93,,RISK_OFF,43,84,92,49,48,42,ETH_2550_not_reclaimed_ETF_outflows_continue_watch_2470_support,ETHspot_2499_2504_2550_CME_2485.5_20261009_ETHETF_minus56.1_1d_3d,partially_verified
2026-10-12,20261012_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,48,52,96,,EVENT,37,97,97,50,46,93,former_20261006_WTI_SELL_fired_closed_supply_and_policy_event_no_chase,CLX26_90.01_91.85_92.17_Hormuz_Isaias_Russia_diesel_1d_3d,verified
2026-10-12,20261012_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,54,53,92,,EVENT,52,91,95,55,59,85,20261012_Japan_US_holiday_thin_liquidity_no_159_160_intervention_assumption,USDJPY_157.76_158.34_158.44_159_160_DXY_US10Y_MOF_1d_3d,partially_verified
2026-10-12,20261012_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,72,69,77,,MIXED,68,87,91,76,73,85,ESZ26_7859.75_no_fresh_Globex_hold_confirmation_before_US_open,ESZ26_7817_7859.75_7870.5_VIX_14.84_CPI_20261014,verified
2026-10-12,20261012_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,67,65,81,,MIXED,65,88,91,73,72,84,NQZ26_31200_reclaim_not_confirmed_yields_unavailable_today,NQZ26_30953_31108.75_31200_31266.5_ESZ26_VIX_CPI_20261014,verified
2026-10-12,20261012_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,58,56,86,,MIXED,59,88,92,62,65,85,DXY_101.80_102.50_break_not_confirmed_us_bond_holiday,DXY_101.92_102.21_102.34_USDJPY_US10Y_CPI_20261014,verified
2026-10-12,20261012_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,76,74,98,,EVENT,94,97,98,86,80,97,20261012_US_Treasury_cash_holiday_last_20261009_yield_not_new_quote,US10Y_20261009_5.24_5.20_5.35_SIFMA_holiday_CPI_20261014,verified
2026-10-12,20261012_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,64,59,90,,MIXED,70,88,92,68,69,86,VIX_14.84_last_close_watch_15_16.5_after_equities_reopen,VIX_20261009_14.77_14.84_15.34_ESZ26_NQZ26_1d_3d,verified
```

## JSON

完全な28項目を含むJSONです。

```json
[
{"date":"2026-10-12","signal_id":"20261012_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":68,"opp_score":58,"no_trade_score":92,"risk_pct":null,"regime":"EVENT","ems":58,"ffs":88,"cds":94,"ias":67,"cbs":63,"mes":79,"invalidation":"former_20261008_GOLD_SELL_fired_closed_wait_for_GCZ26_hold_4233.7_or_failure_below_4170","verification_target":"GCZ26_4156.1_4216.3_4233.7_US10Y_DXY_CPI_20261014","verified_status":"verified"},
{"date":"2026-10-12","signal_id":"20261012_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":62,"opp_score":60,"no_trade_score":83,"risk_pct":null,"regime":"MIXED","ems":57,"ffs":86,"cds":91,"ias":62,"cbs":61,"mes":49,"invalidation":"weekend_BTC_reclaim_83500_unconfirmed_MES_below_50_ETF_weekly_net_outflow","verification_target":"BTCspot_82912_83577_84500_CME_82470_20261009_BTCETF_plus21.1_1d_3d","verified_status":"partially_verified"},
{"date":"2026-10-12","signal_id":"20261012_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":45,"opp_score":47,"no_trade_score":93,"risk_pct":null,"regime":"RISK_OFF","ems":43,"ffs":84,"cds":92,"ias":49,"cbs":48,"mes":42,"invalidation":"ETH_2550_not_reclaimed_ETF_outflows_continue_watch_2470_support","verification_target":"ETHspot_2499_2504_2550_CME_2485.5_20261009_ETHETF_minus56.1_1d_3d","verified_status":"partially_verified"},
{"date":"2026-10-12","signal_id":"20261012_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":48,"opp_score":52,"no_trade_score":96,"risk_pct":null,"regime":"EVENT","ems":37,"ffs":97,"cds":97,"ias":50,"cbs":46,"mes":93,"invalidation":"former_20261006_WTI_SELL_fired_closed_supply_and_policy_event_no_chase","verification_target":"CLX26_90.01_91.85_92.17_Hormuz_Isaias_Russia_diesel_1d_3d","verified_status":"verified"},
{"date":"2026-10-12","signal_id":"20261012_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":54,"opp_score":53,"no_trade_score":92,"risk_pct":null,"regime":"EVENT","ems":52,"ffs":91,"cds":95,"ias":55,"cbs":59,"mes":85,"invalidation":"20261012_Japan_US_holiday_thin_liquidity_no_159_160_intervention_assumption","verification_target":"USDJPY_157.76_158.34_158.44_159_160_DXY_US10Y_MOF_1d_3d","verified_status":"partially_verified"},
{"date":"2026-10-12","signal_id":"20261012_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":72,"opp_score":69,"no_trade_score":77,"risk_pct":null,"regime":"MIXED","ems":68,"ffs":87,"cds":91,"ias":76,"cbs":73,"mes":85,"invalidation":"ESZ26_7859.75_no_fresh_Globex_hold_confirmation_before_US_open","verification_target":"ESZ26_7817_7859.75_7870.5_VIX_14.84_CPI_20261014","verified_status":"verified"},
{"date":"2026-10-12","signal_id":"20261012_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":67,"opp_score":65,"no_trade_score":81,"risk_pct":null,"regime":"MIXED","ems":65,"ffs":88,"cds":91,"ias":73,"cbs":72,"mes":84,"invalidation":"NQZ26_31200_reclaim_not_confirmed_yields_unavailable_today","verification_target":"NQZ26_30953_31108.75_31200_31266.5_ESZ26_VIX_CPI_20261014","verified_status":"verified"},
{"date":"2026-10-12","signal_id":"20261012_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":58,"opp_score":56,"no_trade_score":86,"risk_pct":null,"regime":"MIXED","ems":59,"ffs":88,"cds":92,"ias":62,"cbs":65,"mes":85,"invalidation":"DXY_101.80_102.50_break_not_confirmed_us_bond_holiday","verification_target":"DXY_101.92_102.21_102.34_USDJPY_US10Y_CPI_20261014","verified_status":"verified"},
{"date":"2026-10-12","signal_id":"20261012_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":76,"opp_score":74,"no_trade_score":98,"risk_pct":null,"regime":"EVENT","ems":94,"ffs":97,"cds":98,"ias":86,"cbs":80,"mes":97,"invalidation":"20261012_US_Treasury_cash_holiday_last_20261009_yield_not_new_quote","verification_target":"US10Y_20261009_5.24_5.20_5.35_SIFMA_holiday_CPI_20261014","verified_status":"verified"},
{"date":"2026-10-12","signal_id":"20261012_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":64,"opp_score":59,"no_trade_score":90,"risk_pct":null,"regime":"MIXED","ems":70,"ffs":88,"cds":92,"ias":68,"cbs":69,"mes":86,"invalidation":"VIX_14.84_last_close_watch_15_16.5_after_equities_reopen","verification_target":"VIX_20261009_14.77_14.84_15.34_ESZ26_NQZ26_1d_3d","verified_status":"verified"}
]
```

---

## 本日の総括

本日の新しい観察は、**BTCが83,500ドルを回復した一方、ETHがほとんど追随しなかったこと**です。

これはCrypto全体のrisk-onではなく、BTC優位の局所的な反発である可能性があります。

BTCのETFは10月9日にプラスへ転換しましたが、週間では大幅流出です。

そのため、BTCのMESは49、ETHは42と評価し、どちらもNO_TRADEを維持しました。

また、本日は米国債現物市場が通常の取引を行わない祝日です。

NASDAQ・Goldの判断では、US10Yの金曜日の値を新しい金利安定の証拠として扱わないことが重要です。

**最終判断：10資産すべてNO_TRADE。未決着方向シグナル0件。TSO_LOG固定28列・10行を保存しました。**
