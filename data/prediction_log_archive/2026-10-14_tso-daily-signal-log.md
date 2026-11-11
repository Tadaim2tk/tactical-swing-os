<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-10-14 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-11-02T05:45:08Z / chars: 21193 / 値は無修正 -->

# Tactical Swing OS — Daily Signal Log v2
## 2026年10月14日（水）

**使用モデル：GPT-6**  
**本日の市場の主役：NASDAQ**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**WTI基準限月：NYMEX 2026年11月限（CLX26）**  
**総合regime：EVENT**  
**データ基準：2026年10月13日米国市場／10月14日07:04 JST**

今回は10資産すべてについて、新しい市場データの取得を試みました。

GOLD・WTIは清算値を採用。ES/NQは12月限の遅延値、BTC/ETHは現物とCME先物を別々に確認しています。

**crypto_grounds: etf=有, cme=有**

Farsideの10月12日分が更新され、BTC ETFは**-65.4百万ドル**、ETH ETFは**-85.4百万ドル**となりました。10月13日分の確定値は今回確認できていません。CME先物は10月13日の取引履歴を利用しています。citeturn386449search4turn386449search0turn498696search0turn503057search5

**expected_r_basis: subjective**

本日の新規方向シグナルはありません。方向判断を評価する際は、5営業日の時間決済、未約定確率、CPIによる価格飛躍、シナリオ崩壊時の早期撤退を考慮します。ただし正式な売買条件が成立していないため、expected_rは全行空欄です。

**invalidation_check: none**

10月6日のWTI SELL、10月8日のGOLD SELLはともに過去にfiredとなり、追跡終了済みです。現在の会話内台帳では、未決着方向シグナルはありません。

---

# 1. 本日の結論

| 項目 | 判定 |
|---|---|
| 新規A級 | **0件** |
| 新規B級 | **0件** |
| B+観察候補 | 0件 |
| 未決着方向シグナル | 0件 |
| 本日の新規実取引 | **NO_TRADE** |
| 新規リスク配分 | 0% |
| 通常の最大日次リスク | 0.50% |

**本日の最大の変化は、米長期金利が低下したにもかかわらず、NASDAQの下落が続いたことです。**

10月13日の市場では、次の組み合わせが確認されました。

| 資産 | 10月13日の基準値 | 方向 |
|---|---:|---|
| NASDAQ・NQZ26 | 約30765 | 下落 |
| SPX・ESZ26 | 約7853 | ほぼ横ばい |
| US10Y | 約5.21% | 低下 |
| DXY | 約102.18 | 低下 |
| GOLD・GCZ26 | 4177.30 | 下落 |
| WTI・CLX26 | 94.14 | 小幅上昇 |

NQZ26は取引時間中に**30591.25**まで下落しました。

一方、米10年債利回りは5.21%前後まで低下。ドル指数も下落しています。citeturn503057search3turn970589search2turn386449news20turn386449news16turn675536news70

従来の単純な関係は、

**米金利低下 → NASDAQ上昇**

でした。

ところが、現在は金利が低下してもNASDAQが弱い。

Reutersによると、半導体株はAI設備投資の持続性や中国企業との競争を背景に売られ、フィラデルフィア半導体指数は5営業日連続で下落しました。citeturn386449news18

これはNASDAQの下落要因が、割引率の上昇だけでは説明できなくなっている可能性を示します。

**今日の最重要仮説は「NASDAQの弱さがマクロ要因から半導体・AI関連の個別要因へ移りつつあるか」です。**

ただし、本日は米CPI発表日です。

日本時間21:30に9月分CPIが発表されるため、現時点で新規SELLを追うより、発表後の市場反応を確認する判断を優先します。citeturn675536search0

---

# 2. 前回判断の簡易検証

## NASDAQ：下落継続

10月13日の監視条件は、

**30845割れ → SELL方向継続を警戒**

**30953回復 → 下落圧力の一服**

**31100回復 → 短期下落の失敗を再評価**

でした。

今回のNQZ26は、

| 項目 | 価格 |
|---|---:|
| 始値 | 30876.00 |
| 高値 | 30906.00 |
| 安値 | **30591.25** |
| 取得した遅延値 | 約30765 |

でした。citeturn503057search3

**30845割れが成立しています。**

一方、30953への回復は確認できませんでした。

したがって、前日のSELL方向警戒は価格の動きと整合しています。

ただし、昨日は正式SELLシグナルを発行していません。

研究上の分類は、

**方向観察：弱気方向と整合**

**実取引：NO_TRADE**

です。

方向が合っていたからといって、仮想利益を記録しません。

## BTC：反発したが構造改善は不十分

BTCは10月12日に81,762ドル付近まで下落した後、10月13日には83,000ドル台へ反発しました。

Yahoo Financeの取得値では、10月13日は一時84,059ドル付近まで上昇しています。citeturn587763search0

しかし、以前からの監視条件である**84500ドル突破**には届いていません。

さらにETFフローは10月12日に再び純流出でした。

したがって、短期反発は確認できても、BUYへの転換条件は未成立です。

## ETH：反発したが2550未回復

ETHも10月13日に反発しました。

Binanceの現物履歴では、約2449ドルから2502ドル付近へ上昇し、高値は2538ドル前後でした。citeturn587763search3

ただし2550ドルを維持できていません。

ETF流出も継続しているため、BUY条件は不成立です。

---

# 3. 市場全体の前提

## 最新10資産の基準価格

| 資産 | 基準値 | 使用系列 | verified_status |
|---|---:|---|---|
| GOLD | **4177.30** | GCZ26・10/13清算値 | verified |
| BTC | 約83180 | BTC/USD現物・10/13遅延値 | partially_verified |
| ETH | 約2508 | ETH/USD現物・10/13遅延値 | partially_verified |
| WTI | **94.14** | CLX26・10/13清算値 | verified |
| USDJPY | **158.35** | ドル円・10/13日次値 | partially_verified |
| SPX | 約7853 | ESZ26・10/13遅延値 | partially_verified |
| NASDAQ | 約30765 | NQZ26・10/13遅延値 | partially_verified |
| DXY | 約102.18 | ドル指数・10/13遅延値 | partially_verified |
| US10Y | 約5.21% | 米10年債利回り・10/13 | partially_verified |
| VIX | 約15.5 | VIX指数・10/13遅延値 | partially_verified |

GOLDの12月限は4177.30ドル、WTIの11月限は94.14ドルです。ES/NQについては現物株価指数で代用せず、12月限の価格履歴を利用しました。citeturn386449news16turn675536news70turn503057search2turn503057search3

US10Yは市場データ提供元で5.213～5.217%程度の差があります。VIXも取得時刻により15.2～15.5台の値が表示されたため、約15.5を参考値とし、確定終値とは断定しません。citeturn970589search0turn970589search2turn327522search0

また、DXYはドル指数の値を採用しています。ドル指数先物の価格とは混同しません。

## Crypto資金フロー：10月12日分が判明

| 日付 | BTC ETF | ETH ETF |
|---|---:|---:|
| 10月7日 | -484.9M | -160.9M |
| 10月8日 | -244.1M | -72.5M |
| 10月9日 | +21.1M | -56.1M |
| **10月12日** | **-65.4M** | **-85.4M** |

単位は百万米ドルです。

10月12日のETFフローがマイナスだったことは、両資産にとって弱気材料です。citeturn386449search4turn386449search0

一方、10月13日のCME先物履歴では、

**BTC先物：約83195ドル**

**ETH先物：約2506.50ドル**

を確認しました。

ただし現物との同時刻比較ができていないため、basisの確定計算は行いません。citeturn498696search0turn503057search5

## 米国マクロ：原油と金利の関係

昨日は原油が小幅上昇した一方、米長期金利は低下しました。

WTIは93.74ドルから94.14ドルへ上昇。

米10年債利回りは約5.24%から約5.21%へ低下しています。citeturn675536news70turn970589search2

したがって、昨日検討した、

**原油高 → インフレ懸念 → 金利上昇 → NASDAQ下落**

という一連の経路は、10月13日の値動きでは確認できません。

むしろ今回確認できたのは、

**原油：小幅上昇**

**金利：低下**

**ドル：低下**

**NASDAQ：下落**

です。

これは非常に重要な観察結果です。

NASDAQの弱さには、金利以外の要因をより強く織り込む必要があります。

---

# 4. 10資産別判断

| 資産 | 判断 | no_trade_score | 主な評価 |
|---|---|---:|---|
| **GOLD** | NO_TRADE | 91 | 金利低下でも上昇できず。CPI前 |
| **BTC** | NO_TRADE | 90 | 反発したが84500未回復、MES45 |
| **ETH** | NO_TRADE | 94 | ETF流出継続、MES43 |
| **WTI** | NO_TRADE | 98 | 94.14。供給・政策材料が競合 |
| **USDJPY** | NO_TRADE | 91 | 158.35。CPIと介入テール |
| **SPX** | NO_TRADE | 83 | ESは比較的底堅い |
| **NASDAQ** | NO_TRADE | 87 | 金利低下でも下落。半導体が弱い |
| **DXY** | NO_TRADE | 86 | 102.18へ反落 |
| **US10Y** | NO_TRADE | 93 | 5.21%へ低下。CPI待ち |
| **VIX** | NO_TRADE | 88 | 15台。株価下落の割に警戒感は限定的 |

本日の10資産はすべて新規NO_TRADEです。

各スコアは取得情報を基にしたモデルの主観評価であり、統計的な較正済みスコアではありません。

---

# 5. A級候補

**新規A級：なし。**

最も注目しているのはNASDAQのSELL方向です。

しかし、現在のNQZ26は30,765付近です。

10月13日の安値30,591に接近しているため、ここから成行SELLすると、すでに下落した後の追随になります。

また、今夜のCPIで金利が急低下した場合、NASDAQに買い戻しが発生する可能性があります。

逆にCPIが強ければ、一段の金利上昇とNASDAQ下落が発生する可能性もあります。

**どちらのシナリオでも、今朝の価格から新規ポジションを保有する優位性は十分ではありません。**

A級の必要条件であるCBS75以上、EMS65以上、expected_r0.45以上、MAE想定0.25R以下、RR最低1.2、XM最小ロット損失約3000円以内を同時に満たす取引案はありません。

---

# 6. B級監視候補

**正式B級：なし。**

**B+観察候補：なし。**

ただし、次の3資産を監視します。

## NASDAQ：SELL方向

NQZ26の現在の重要水準は、

**30591：10月13日安値**

**30900：直近の上値確認帯**

**31100：短期構造回復の確認帯**

です。

30591を明確に下回れば、下落継続の可能性を評価します。

一方30900を回復し、CPI後の金利が落ち着いていれば、下落加速が一服した可能性を検討します。

ただし、どちらも正式なEntry帯ではありません。

## DXY：方向再評価

現在は約102.18です。

10月12日の強いドルから一転して下落しました。

**102.60超**

ならドル高再開。

**101.80割れ**

ならドル高の一服を疑います。

今夜のCPIを受けた値動きが重要です。

## BTC：BUY方向

BTCは83,000ドル台へ反発しています。

しかしMESは45です。

現在のTSOルールではMES50未満のため、NO_TRADEを優先します。

また、CME先物の参考値と現物価格は近いものの、ETFフローは再び流出しています。

84,500ドルを回復するまでは新規BUYを作りません。

---

# 7. 触らない資産

## WTI

本日もっとも注意したい資産です。

WTIは94.14ドルへ上昇しました。

10月13日は、米国とロシアのディーゼル供給をめぐる協議、中東の輸送リスク、OPEC+の供給動向などが競合しています。citeturn675536news70

現在のWTIは、供給ショックに対するヘッドラインで価格が大きく変わる状態です。

前回のWTI SELLは供給障害で失効しました。

そのため、以前の売り仮説を再利用しません。

同時に、価格が上昇したからといって新規BUYへ反転することもしません。

## GOLD

GOLDは、米金利とDXYが低下したにもかかわらず、12月限が4177.30ドルへ下落しました。

これは従来の「金利低下ならGold上昇」という単純な関係では説明できません。

Gold市場自体の売り圧力や、CPI前のポジション調整を調べる必要があります。

以前のSELL失効を取り消すことはしません。

## USDJPY

ドル円は158.35円です。

10月13日のレンジは157.84～158.53円でした。citeturn970589search3

159円にはまだ到達していません。

介入リスクは監視しますが、価格だけで実際の介入を予測しません。

本日のCPIで短時間の円安加速が発生した場合は、通常のUSDJPY momentum BUYとIntervention Shock Moduleを分離して評価します。

---

# 8. 後日検証ポイント

## 本日21:30 — 米CPI

**2026年10月14日21:30 JST**

米労働統計局の公式予定では、9月分CPIが発表されます。

翌15日にはPPIも予定されています。citeturn675536search0

現在の市場では、インフレ率そのものに加え、金利と株価がどう反応するかが重要です。

検証するシナリオを3つに分けます。

| CPI後の反応 | 観察する関係 | TSO上の意味 |
|---|---|---|
| 金利上昇・NASDAQ下落 | 通常の金利逆風 | SELL側を再評価 |
| 金利低下・NASDAQ上昇 | 従来の逆相関が復活 | BUY_PULLBACK再評価 |
| **金利低下・NASDAQ下落** | 半導体・AI固有の弱さが継続 | マクロ以外の要因を重視 |

特に3番目が重要です。

10月13日には、金利低下にもかかわらずNASDAQが弱いという関係が観察されました。

CPI後にも同じ関係が続くなら、短期的には金利よりもAI関連株の業績期待や設備投資への懸念が優勢になっている可能性があります。

## その他の検証水準

| 資産 | 重要水準 | 検証内容 |
|---|---|---|
| GOLD | 4170 / 4215 | 下落継続か反発か |
| BTC | 81200 / 83500 / 84500 | 反発の持続性 |
| ETH | 2410 / 2550 | 相対弱さの継続 |
| WTI | 92 / 94.14 / 96 | 供給ショックの持続 |
| USDJPY | 159 / 160 | 円安加速・介入警戒 |
| SPX | 7800 / 7880 | 支持・上値回復 |
| NASDAQ | 30591 / 30900 / 31100 | 下落継続・回復 |
| DXY | 101.80 / 102.60 | CPI後のドル方向 |
| US10Y | 5.15% / 5.35% | CPIによる金利再評価 |
| VIX | 15 / 16.5 | リスク回避の拡大 |

XMの最小ロット制約は、正式な方向シグナルを作った段階で再確認します。

本日は新規実取引候補がないため、想定実損・RR・MAEは未設定とします。

---

# 9. Obsidian保存用 Observation Draft

本日のObservationをMarkdownで保存しました。

**[TSO Observation — 2026-10-14](sandbox:/mnt/data/TSO_Observation_2026-10-14.md)**

主要部分をチャットにも残します。

```markdown
# TSO Observation — 2026-10-14

Model:
GPT-6

Market protagonist:
NASDAQ

Gold reference:
COMEX December 2026
GCZ26

WTI reference:
NYMEX November 2026
CLX26

Regime:
EVENT

crypto_grounds:
etf=有
cme=有

expected_r_basis:
subjective

## Conclusion

New A:
0

New B:
0

B+:
0

Actual execution:
NO_TRADE

Risk allocation:
0%

invalidation_check:
none

## Main research observation

NQZ26:
~30765

Previous:
~30898

US10Y:
~5.21%

Previous:
~5.24%

DXY:
~102.18

WTI:
94.14

Interpretation:

NASDAQ declined despite
lower Treasury yields
and a weaker dollar.

The simple relationship:

US10Y down
-> NASDAQ up

did not hold.

Possible alternative explanation:

Semiconductor weakness
AI capital expenditure concerns
China semiconductor competition

Research priority:
Separate macro discount-rate
effects from AI-sector-specific risk.

## Crypto

BTC spot:
~83180

BTC CME:
~83195

BTC ETF Oct12:
-65.4m USD

BTC MES:
45

ETH spot:
~2508

ETH CME:
~2506.5

ETH ETF Oct12:
-85.4m USD

ETH MES:
43

ETF Oct13:
not verified

Both:
NO_TRADE

## Gold

GCZ26:
4177.30

Previous:
4190.60

US10Y:
lower

DXY:
lower

Gold:
lower

Observation:

Gold did not benefit
from lower yields and dollar.

Do not reactivate prior SELL.

## WTI

CLX26:
94.14

Previous:
93.74

Supply / policy risk:
high

No momentum chase.

## Event

2026-10-14

US September CPI
21:30 JST

2026-10-15

US PPI
21:30 JST

## Previous directional signals

20261006_WTI_SELL_PULLBACK:
FIRED / CLOSED

20261008_GOLD_SELL_PULLBACK:
FIRED / CLOSED

Active directional signals:
NONE

## Next research

1. NQ and US10Y after CPI.
2. Semiconductor relative weakness.
3. Gold response to falling yields.
4. BTC/ETH ETF flow deterioration.
5. WTI supply risk persistence.
6. USDJPY intervention-tail monitoring.

#TSO #NASDAQ #CPI #US10Y #BTC #ETH
```

---

# 10. TSO_LOG — CSV / JSON

**固定28列・10資産10行の生成と構造検証が完了しました。**

今回も以下のルールを維持しています。

- 10資産を各1行で記録
- `asset=NONE`なし
- `regime`は指定6語のみ
- NO_TRADE行のEntry・SL・TP・RR・win_prob・expected_r・risk_pctは空欄
- スコア・invalidation・verification_target・verified_statusは記録
- JSONはCSVと同じ28項目を保持

### 保存ファイル

**[TSO_LOG CSV — 2026-10-14](sandbox:/mnt/data/TSO_LOG_2026-10-14.csv)**

**[TSO_LOG JSON — 2026-10-14](sandbox:/mnt/data/TSO_LOG_2026-10-14.json)**

## CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-10-14,20261014_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,54,53,91,,EVENT,60,94,93,64,65,84,await_CPI_no_reverse_trade_after_prior_gold_sell_fired,GCZ26_4177.30_settlement_20261013_4170_4190_4215_4234_US10Y_DXY_CPI,verified
2026-10-14,20261014_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,58,51,90,,MIXED,55,90,93,60,61,45,MES_below_50_and_BTCspot_below_84500_wait_sustained_reclaim_and_ETF_flow_turn,BTCspot_approx_83180_20261013_CME_BTC_83195_ETF_BTC_20261012_minus65.4_81200_83500_84500,partially_verified
2026-10-14,20261014_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,50,45,94,,RISK_OFF,50,92,93,52,52,43,MES_below_50_ETHspot_below_2550_and_ETF_outflow_wait_stabilization,ETHspot_approx_2508_20261013_CME_ETH_2506.5_ETF_ETH_20261012_minus85.4_2410_2550,partially_verified
2026-10-14,20261014_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,47,54,98,,EVENT,38,97,95,48,53,95,no_supply_shock_momentum_trade_monitor_94.14_96_and_policy_headlines,CLX26_93.74_prior_94.14_settle_20261013_92_94.14_96_Hormuz_Russian_diesel_CPI,verified
2026-10-14,20261014_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,61,53,91,,EVENT,58,92,95,65,68,90,do_not_chase_toward_159_intervention_risk_watch_speed_and_CPI,USDJPY_158.35_20261013_157.84_low_158.53_high_159_160_DXY_US10Y_CPI,partially_verified
2026-10-14,20261014_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,64,59,83,,MIXED,67,94,94,72,73,88,ESZ26_range_and_CPI_wait_for_7800_support_or_7880_reclaim,ESZ26_approx_7853_20261013_delayed_7834.5_low_7864_high_7800_7880_VIX,partially_verified
2026-10-14,20261014_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,60,62,87,,RISK_OFF,62,94,94,69,75,91,NQZ26_30591_support_break_or_30900_reclaim_only_after_CPI_confirm,NQZ26_approx_30765_20261013_delayed_30591.25_low_30906_high_31100_US10Y_VIX,partially_verified
2026-10-14,20261014_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,61,58,86,,MIXED,67,93,93,69,70,88,DXY_spot_retreat_wait_CPI_break_above_102.6_or_below_101.8,DXY_spot_approx_102.18_20261013_not_DX_futures_101.8_102.6_CPI_US10Y,partially_verified
2026-10-14,20261014_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,66,63,93,,EVENT,80,95,95,76,76,96,yield_reopened_and_fell_wait_CPI_5.15_or_5.35_break,US10Y_approx_5.21pct_20261013_5.17_low_5.35_ceiling_CPI_20261014,partially_verified
2026-10-14,20261014_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,51,48,88,,MIXED,66,93,95,63,67,86,VIX_low15s_wait_16.5_break_or_below_15_with_equity_confirm,VIX_approx_15.5_20261013_intraday_15.17_low_15.61_high_ESZ26_NQZ26_CPI,partially_verified
```

## JSON

全28項目を保持した10資産分のJSONです。

```json
[
  {
    "date": "2026-10-14",
    "signal_id": "20261014_GOLD_NONE_NO_TRADE",
    "asset": "GOLD",
    "side": "NONE",
    "rank": "NO_TRADE",
    "type": "NO_TRADE",
    "entry_low": null,
    "entry_high": null,
    "sl": null,
    "tp1": null,
    "tp2": null,
    "rr": null,
    "win_prob": null,
    "expected_r": null,
    "tq_score": 54,
    "opp_score": 53,
    "no_trade_score": 91,
    "risk_pct": null,
    "regime": "EVENT",
    "ems": 60,
    "ffs": 94,
    "cds": 93,
    "ias": 64,
    "cbs": 65,
    "mes": 84,
    "invalidation": "await_CPI_no_reverse_trade_after_prior_gold_sell_fired",
    "verification_target": "GCZ26_4177.30_settlement_20261013_4170_4190_4215_4234_US10Y_DXY_CPI",
    "verified_status": "verified"
  },
  {
    "date": "2026-10-14",
    "signal_id": "20261014_BTC_NONE_NO_TRADE",
    "asset": "BTC",
    "side": "NONE",
    "rank": "NO_TRADE",
    "type": "NO_TRADE",
    "entry_low": null,
    "entry_high": null,
    "sl": null,
    "tp1": null,
    "tp2": null,
    "rr": null,
    "win_prob": null,
    "expected_r": null,
    "tq_score": 58,
    "opp_score": 51,
    "no_trade_score": 90,
    "risk_pct": null,
    "regime": "MIXED",
    "ems": 55,
    "ffs": 90,
    "cds": 93,
    "ias": 60,
    "cbs": 61,
    "mes": 45,
    "invalidation": "MES_below_50_and_BTCspot_below_84500_wait_sustained_reclaim_and_ETF_flow_turn",
    "verification_target": "BTCspot_approx_83180_20261013_CME_BTC_83195_ETF_BTC_20261012_minus65.4_81200_83500_84500",
    "verified_status": "partially_verified"
  },
  {
    "date": "2026-10-14",
    "signal_id": "20261014_ETH_NONE_NO_TRADE",
    "asset": "ETH",
    "side": "NONE",
    "rank": "NO_TRADE",
    "type": "NO_TRADE",
    "entry_low": null,
    "entry_high": null,
    "sl": null,
    "tp1": null,
    "tp2": null,
    "rr": null,
    "win_prob": null,
    "expected_r": null,
    "tq_score": 50,
    "opp_score": 45,
    "no_trade_score": 94,
    "risk_pct": null,
    "regime": "RISK_OFF",
    "ems": 50,
    "ffs": 92,
    "cds": 93,
    "ias": 52,
    "cbs": 52,
    "mes": 43,
    "invalidation": "MES_below_50_ETHspot_below_2550_and_ETF_outflow_wait_stabilization",
    "verification_target": "ETHspot_approx_2508_20261013_CME_ETH_2506.5_ETF_ETH_20261012_minus85.4_2410_2550",
    "verified_status": "partially_verified"
  },
  {
    "date": "2026-10-14",
    "signal_id": "20261014_WTI_NONE_NO_TRADE",
    "asset": "WTI",
    "side": "NONE",
    "rank": "NO_TRADE",
    "type": "NO_TRADE",
    "entry_low": null,
    "entry_high": null,
    "sl": null,
    "tp1": null,
    "tp2": null,
    "rr": null,
    "win_prob": null,
    "expected_r": null,
    "tq_score": 47,
    "opp_score": 54,
    "no_trade_score": 98,
    "risk_pct": null,
    "regime": "EVENT",
    "ems": 38,
    "ffs": 97,
    "cds": 95,
    "ias": 48,
    "cbs": 53,
    "mes": 95,
    "invalidation": "no_supply_shock_momentum_trade_monitor_94.14_96_and_policy_headlines",
    "verification_target": "CLX26_93.74_prior_94.14_settle_20261013_92_94.14_96_Hormuz_Russian_diesel_CPI",
    "verified_status": "verified"
  },
  {
    "date": "2026-10-14",
    "signal_id": "20261014_USDJPY_NONE_NO_TRADE",
    "asset": "USDJPY",
    "side": "NONE",
    "rank": "NO_TRADE",
    "type": "NO_TRADE",
    "entry_low": null,
    "entry_high": null,
    "sl": null,
    "tp1": null,
    "tp2": null,
    "rr": null,
    "win_prob": null,
    "expected_r": null,
    "tq_score": 61,
    "opp_score": 53,
    "no_trade_score": 91,
    "risk_pct": null,
    "regime": "EVENT",
    "ems": 58,
    "ffs": 92,
    "cds": 95,
    "ias": 65,
    "cbs": 68,
    "mes": 90,
    "invalidation": "do_not_chase_toward_159_intervention_risk_watch_speed_and_CPI",
    "verification_target": "USDJPY_158.35_20261013_157.84_low_158.53_high_159_160_DXY_US10Y_CPI",
    "verified_status": "partially_verified"
  },
  {
    "date": "2026-10-14",
    "signal_id": "20261014_SPX_NONE_NO_TRADE",
    "asset": "SPX",
    "side": "NONE",
    "rank": "NO_TRADE",
    "type": "NO_TRADE",
    "entry_low": null,
    "entry_high": null,
    "sl": null,
    "tp1": null,
    "tp2": null,
    "rr": null,
    "win_prob": null,
    "expected_r": null,
    "tq_score": 64,
    "opp_score": 59,
    "no_trade_score": 83,
    "risk_pct": null,
    "regime": "MIXED",
    "ems": 67,
    "ffs": 94,
    "cds": 94,
    "ias": 72,
    "cbs": 73,
    "mes": 88,
    "invalidation": "ESZ26_range_and_CPI_wait_for_7800_support_or_7880_reclaim",
    "verification_target": "ESZ26_approx_7853_20261013_delayed_7834.5_low_7864_high_7800_7880_VIX",
    "verified_status": "partially_verified"
  },
  {
    "date": "2026-10-14",
    "signal_id": "20261014_NASDAQ_NONE_NO_TRADE",
    "asset": "NASDAQ",
    "side": "NONE",
    "rank": "NO_TRADE",
    "type": "NO_TRADE",
    "entry_low": null,
    "entry_high": null,
    "sl": null,
    "tp1": null,
    "tp2": null,
    "rr": null,
    "win_prob": null,
    "expected_r": null,
    "tq_score": 60,
    "opp_score": 62,
    "no_trade_score": 87,
    "risk_pct": null,
    "regime": "RISK_OFF",
    "ems": 62,
    "ffs": 94,
    "cds": 94,
    "ias": 69,
    "cbs": 75,
    "mes": 91,
    "invalidation": "NQZ26_30591_support_break_or_30900_reclaim_only_after_CPI_confirm",
    "verification_target": "NQZ26_approx_30765_20261013_delayed_30591.25_low_30906_high_31100_US10Y_VIX",
    "verified_status": "partially_verified"
  },
  {
    "date": "2026-10-14",
    "signal_id": "20261014_DXY_NONE_NO_TRADE",
    "asset": "DXY",
    "side": "NONE",
    "rank": "NO_TRADE",
    "type": "NO_TRADE",
    "entry_low": null,
    "entry_high": null,
    "sl": null,
    "tp1": null,
    "tp2": null,
    "rr": null,
    "win_prob": null,
    "expected_r": null,
    "tq_score": 61,
    "opp_score": 58,
    "no_trade_score": 86,
    "risk_pct": null,
    "regime": "MIXED",
    "ems": 67,
    "ffs": 93,
    "cds": 93,
    "ias": 69,
    "cbs": 70,
    "mes": 88,
    "invalidation": "DXY_spot_retreat_wait_CPI_break_above_102.6_or_below_101.8",
    "verification_target": "DXY_spot_approx_102.18_20261013_not_DX_futures_101.8_102.6_CPI_US10Y",
    "verified_status": "partially_verified"
  },
  {
    "date": "2026-10-14",
    "signal_id": "20261014_US10Y_NONE_NO_TRADE",
    "asset": "US10Y",
    "side": "NONE",
    "rank": "NO_TRADE",
    "type": "NO_TRADE",
    "entry_low": null,
    "entry_high": null,
    "sl": null,
    "tp1": null,
    "tp2": null,
    "rr": null,
    "win_prob": null,
    "expected_r": null,
    "tq_score": 66,
    "opp_score": 63,
    "no_trade_score": 93,
    "risk_pct": null,
    "regime": "EVENT",
    "ems": 80,
    "ffs": 95,
    "cds": 95,
    "ias": 76,
    "cbs": 76,
    "mes": 96,
    "invalidation": "yield_reopened_and_fell_wait_CPI_5.15_or_5.35_break",
    "verification_target": "US10Y_approx_5.21pct_20261013_5.17_low_5.35_ceiling_CPI_20261014",
    "verified_status": "partially_verified"
  },
  {
    "date": "2026-10-14",
    "signal_id": "20261014_VIX_NONE_NO_TRADE",
    "asset": "VIX",
    "side": "NONE",
    "rank": "NO_TRADE",
    "type": "NO_TRADE",
    "entry_low": null,
    "entry_high": null,
    "sl": null,
    "tp1": null,
    "tp2": null,
    "rr": null,
    "win_prob": null,
    "expected_r": null,
    "tq_score": 51,
    "opp_score": 48,
    "no_trade_score": 88,
    "risk_pct": null,
    "regime": "MIXED",
    "ems": 66,
    "ffs": 93,
    "cds": 95,
    "ias": 63,
    "cbs": 67,
    "mes": 86,
    "invalidation": "VIX_low15s_wait_16.5_break_or_below_15_with_equity_confirm",
    "verification_target": "VIX_approx_15.5_20261013_intraday_15.17_low_15.61_high_ESZ26_NQZ26_CPI",
    "verified_status": "partially_verified"
  }
]
```

---

## 本日の総括

本日の研究上の重要な発見は、**NASDAQが米長期金利とドルの低下にもかかわらず下落したこと**です。

これは、現在のNASDAQを単純な金利感応度だけで評価することの限界を示しています。

特に半導体・AI関連株の相対的な弱さが続く場合、今後のTSOでは金利、指数全体の方向性、半導体セクター固有の要因を分離して評価する必要があります。

一方、BTCとETHは10月13日に反発しましたが、ETF資金フローは10月12日に両方ともマイナスでした。

そのため新規BUYへは転換しません。

**最終判断：10資産すべてNO_TRADE。未決着方向シグナル0件。固定28列・10行のTSO_LOGを保存しました。**

**現在時刻：2026年10月14日07時台（日本時間）**  
**次指示対象：米CPI発表後のNASDAQ・US10Y・DXY・GOLDの反応と、金利低下時のNASDAQ相対弱さの検証。**
