<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-21 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-21T12:59:52Z / chars: 16641 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-09-21

**使用モデル：GPT-5.6 Sol**  
**本日の市場の主役：WTI**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**データ基準：9月18日米国終値＋9月20日週末ニュース＋9月21日朝のCrypto/USDJPY。CMEの週初直後の価格は遅延データへまだ十分反映されていないため、一部`partially_verified`。**  
**crypto_grounds: etf=有, cme=有**  
**expected_r_basis: subjective** — 本日の新規方向シグナルは0件。既存WTI `expected_r=0.48`、USDJPY `expected_r=0.43`は発行済み値を変更しません。

**invalidation_check: 20260917_WTI_BUY_PULLBACK=not_fired, 20260919_USDJPY_BUY_PULLBACK=not_fired**

今朝いちばん重要なのは、**WTIの「価格」ではなく参照限月のロール**です。Investing.comでは9月20日に前月から**Nov-26へフロント限月が切り替わり、Oct-26終値100.30に対してNov-26は96.08**です。これは4ドル超の価格急落ではなく限月差です。したがって既存`20260917_WTI_BUY_PULLBACK`の98.90 invalidationを、今日から表示される96.08と比較して**firedにしてはいけません**。既存判断は発行時と同じ**Oct-26系列**、実際の取引はユーザーの**OILCash価格**で管理します。citeturn625906view2

週末にはHouthiによるRiyadh攻撃後、日曜のサウジ株は0.3%安。ただしSaudi Aramcoは序盤安から**+1.3%**で終了しており、地域市場は警戒しているもののパニック反応ではありません。一方、サウジのEast-West Pipeline障害と地域輸送リスクは依然残っています。citeturn408267news25turn408267news31

urlReuters：9月20日のサウジ・湾岸市場turn408267news25  
urlReuters：9月20日のKashkari発言turn408267news27  
urlReuters：9月21日週の米市場見通しturn408267news30  
urlReuters：9月18日のBOJ後ドル円turn847217news24

## 1. 本日の結論

**新規A級：0件**  
**新規B級：0件**  
**既存B：WTI BUY — HOLD**  
**既存B+：USDJPY BUY_PULLBACK — 未約定待機**  
**新規実取引：NO_TRADE**

WTIは週末材料だけなら上方向です。しかし、今日は**①週末地政学ギャップ、②WTIフロント限月ロール、③OILCash週初値がまだ形成されていないタイミング**が重なっています。

XMのOILCashはCash CFDで先物限月そのものではなく、第三者の現行取引仕様では夏時間の月曜取引開始は日本時間**07:05頃**です。このレポート基準時刻では実際のOILCash週初値をまだ確認できません。したがって、**Nov-26の96.08を見てSL割れと判断するのは誤り**です。citeturn785845search0turn785845search5

既存実取引はそのままです。

**OILCash Entry：約101.19  
SL：98.90  
TP：105.20  
実RR：約1.75**

週初のOILCash実価格で98.90に到達すれば撤退。**SLは広げません。**

USDJPYは今朝06:00時点でおよそ**156.75–156.95**。既存B+ Entry `156.00–156.50`よりまだ上なので追いません。BOJ後の円売り構造は残っていますが、rate check後で介入リスクも残っています。citeturn752499search4turn847217news24

---

## 2. 前回判断の簡易検証

### `20260917_WTI_BUY_PULLBACK`

発行時参照は**Oct-26 WTI**。

金曜のOct-26は、

**Open 101.06  
High 103.48  
Low 99.19  
Close 100.30**

でした。したがって金曜時点では98.90には到達していません。citeturn625906view2

その後週末にRiyadhへの攻撃が発生しましたが、日曜のAramco株は最終的には上昇しており、「週末攻撃＝即、巨大な追加供給障害」という確認までは取れていません。citeturn408267news25

したがって現在、

**ENTRY_FILLED / SL_NOT_REACHED / TP_NOT_REACHED / invalidation=not_fired**

です。

ただし今日からデータ取得サイトのfront WTIはNov-26 **96.08**へロールしています。Oct-26との約**4.22ドル差**を相場下落として扱わないことが、今日の最重要データ品質管理です。citeturn625906view2

### `20260919_USDJPY_BUY_PULLBACK`

既存条件：

**Entry 156.00–156.50  
SL 155.20  
TP1 158.20  
TP2 159.60  
RR 1.86**

BOJ後の金曜高値は約158.05。その後rate checkで156円台へ戻りました。今朝06:00時点も156円後半で、155.20 invalidationには到達していません。citeturn752499search4turn847217news24

したがって、

**UNFILLED / invalidation=not_fired**

です。

156.50より上では追いません。

---

## 3. 市場全体の前提

金曜終値では、かなり強いリスク資産耐性が続いています。

**NQZ26：29917.25**  
**ESZ26：7712.50**  
**US10Y：4.996%**  
**VIX：14.81**  
**DXY：99.937**  
**GCZ26：4415.90**

10年債がほぼ5%でもNQが3万直前、VIXが15未満というのが特徴です。citeturn975103view2turn975103view3turn625617view0

ただし日曜にはFedのKashkariが、エネルギー以外を含めインフレは依然高すぎると発言し、先週の利上げを支持しました。Fedの引き締めリスクは消えていません。citeturn408267news27

Goldも金曜は強く、米金先物は4424.90で清算したとのReuters報道があります。GCZ26の取得系列では4415.90です。ドル高・高金利に耐えていること自体は強いものの、週末地政学を受けた月曜ギャップ確認前なので新規BUYにはしません。citeturn423483news24turn975103view4

CryptoはBTC/USD約**80894**、ETH/USD約**2628**。BTC ETFは9月18日に現時点集計で**+324.6Mドル**、ETH ETFは**+29.4Mドル**。ただしBTCは一部欄が未確定で、週全体では資金流入がそれほど強くなかったとの集計もあります。CME BTCは金曜81235付近、ETH futuresは2643.5付近でした。citeturn469068view0turn893449view0turn469068search0turn469068search2turn423483search1turn423483search0

総合regimeは**EVENT / MIXED**です。

---

## 4. 10資産別判断

| 資産 | 判断 | 今朝の評価 |
|---|---|---|
| GOLD | **NO_TRADE** | GCZ26 4415.9。強いが週末リスクのギャップ確認前 |
| BTC | **NO_TRADE** | 約80.9k。ETF改善も82k抵抗前、追わない |
| ETH | **NO_TRADE** | 約2628。週末堅調だが金曜急騰後 |
| WTI | **既存BUY HOLD / 新規NO_TRADE** | **限月ロール注意。Oct100.30≠Nov96.08** |
| USDJPY | **既存B+待機 / 新規NO_TRADE** | 約156.8。Entry156.0–156.5を待つ |
| SPX | **NO_TRADE** | ESZ26 7712.5。週初ギャップ未確認 |
| NASDAQ | **NO_TRADE** | NQZ26 29917.25。30k直前、追わない |
| DXY | **NO_TRADE** | 99.937。明確な独立edgeなし |
| US10Y | **NO_TRADE** | 4.996%。5%攻防＋Fed発言 |
| VIX | **NO_TRADE** | 14.81だが週末地政学未反映 |

---

## 5. A級候補

**なし。**

方向として最も強いのは依然**WTI上**ですが、既存ポジションを持っているため追加しません。

さらに今日からfront monthがOct→Novへ切り替わるため、同一価格軸でEntry/SLを新規設計するには最初の市場形成を確認した方がよいです。

Gold BUYも次点ですが、GCZ26が金曜高値4439.60付近まで既に上昇しています。月曜に地政学ギャップで4450を上回った場合、そこで追えば供給・戦争ショック直後のmomentum追随になり、TSOルールに反します。citeturn975103view4

---

## 6. B級監視候補

新規Bはありません。既存2件のみです。

### WTI — 既存B、約定済み

**OILCash Entry 101.19  
SL 98.90  
TP 105.20  
RR 1.75**

現在の扱いは**HOLD**。

重要なのは参照系列です。

**旧シグナル検証：Oct-26 WTI**  
**本日以降の新規市場観測：Nov-26 WTI**  
**実取引管理：XM OILCash**

この3つを混同しません。

Nov-26の96.08は既存SL98.90の判定材料に使いません。citeturn625906view2

### USDJPY — 既存B+、未約定

**Entry 156.00–156.50  
SL 155.20  
TP1 158.20  
TP2 159.60  
RR 1.86**

今朝約156.8なので待機。

**156.50以下へ押しても155.20を割らない**なら既存シグナルは有効。

ただしWTIの0.25%リスクが既にあるため、USDJPYが実際に約定すれば**合計0.50%**。その日は新しい第三ポジションを取りません。

---

## 7. 触らない資産

今日は**BTC・NASDAQ・GOLD**を特に追いません。

BTCは80kを維持し、ETF資金も金曜に改善しました。一方、金曜CMEは+6%級の上昇で、現在81k近辺。ETF週次の機関需要は完全な強気確認とは言いにくく、82k付近の抵抗も近いので、ここはBUYする場所ではありません。citeturn896444news19turn423483search1

NASDAQも同様です。NQは29917でほぼ30000。金利5%でも強いという方向情報は価値がありますが、それと「29900で買う」は別です。

Goldも4420近辺から週末ニュースを追って買うより、月曜価格形成を見ます。

---

## 8. 後日検証ポイント

### WTI

今日最大の検証項目です。

まず**ロール調整を相場変動と誤認しない**。

既存シグナルはOct-26/OILCash軸で、

**OILCash 98.90 → fired**  
**105.20 → TP**

です。

週明けOILCashが102–103以上へ上昇すれば、週末Saudiリスクが価格へ乗ったことになります。

逆に100近辺またはそれ以下で始まり、その後弱ければ、「攻撃ヘッドラインに対する原油の感応度が低下している」と評価します。

### USDJPY

**156.00–156.50 → Entry帯**  
**155.20 → fired**  
**158.20 → TP1**

BOJ利上げにもかかわらず円安になった構造はBUY側ですが、rate check後なので158円接近時には介入リスクを再評価します。citeturn847217news24

### NASDAQ

**NQ >30000を維持**
＋
**US10Y ≈5%**
＋
**VIX <16**

なら、「高金利耐性」という新regime仮説がさらに強くなります。

逆に29600割れ＋VIX上昇なら、週末地政学がrisk-onを壊した可能性を評価します。

### Crypto

BTCは、

**80k維持＋82k突破＋ETFプラス継続**

まで揃えばBUY候補を作り直します。

78–79kへ戻れば金曜上昇のshort squeeze比率が高かった可能性を再評価します。

### Gold

**GCZ26 4450超を定着**なら強気再評価。

**4370割れ**なら現在の強さを一度否定します。

---

## 9. Obsidian保存用 Observation Draft

```markdown
# 2026-09-21 WTI Contract Roll / Saudi Weekend Risk

Model:
GPT-5.6 Sol

Market protagonist:
WTI

Gold reference:
COMEX Dec-2026 / GCZ26

crypto_grounds:
etf=有
cme=有

expected_r_basis:
subjective

## Regime

EVENT / MIXED

## Critical data-quality event

WTI front contract rolled on Sep20.

Oct-26 Sep18 close:
100.30

Nov-26 Sep18 close:
96.08

spread:
4.22

IMPORTANT:
Do NOT interpret Nov-26 96.08 as a crash through the old 98.90 SL.

Existing signal:
20260917_WTI_BUY_PULLBACK

was generated on Oct-26 / OILCash-like price scale.

For validation:
use Oct-26 until old signal resolves.

For new observations:
use Nov-26 front month.

For real trade:
use actual XM OILCash quote.

## WTI actual trade

Entry:
~101.19

SL:
98.90

TP:
105.20

RR:
1.75

Status:
HOLD

invalidation:
not_fired

Do not widen SL.
Do not add.

## Weekend Saudi event

Houthis attacked Riyadh.
Saudi/Gulf equities fell Sunday.

Saudi index:
-0.3%

Aramco:
+1.3% close after early weakness

Interpretation:
geopolitical risk remains elevated
but regional market did not show panic pricing.

East-West pipeline disruption remains relevant.

## USDJPY active pending

20260919_USDJPY_BUY_PULLBACK

Entry:
156.00-156.50

SL:
155.20

TP1:
158.20

TP2:
159.60

RR:
1.86

Sep21 ~06:00 JST:
~156.75-156.95

Status:
UNFILLED
not_fired

Do not chase above entry band.

## Friday references

GCZ26:
4415.90

NQZ26:
29917.25

ESZ26:
7712.50

US10Y:
4.996%

DXY:
99.937

VIX:
14.81

## Crypto current

BTC:
~80894

ETH:
~2628

BTC ETF Sep18:
+324.6m currently reported
some fields incomplete

ETH ETF Sep18:
+29.4m

CME BTC Sep18:
~81235

CME ETH Sep18:
~2643.5

## Active invalidation

20260917_WTI_BUY_PULLBACK=not_fired
20260919_USDJPY_BUY_PULLBACK=not_fired

## New signals

A:
NONE

B:
NONE

Existing:
WTI BUY active
USDJPY BUY_PULLBACK pending

#TSO #WTI #ContractRoll #USDJPY #BTC #NASDAQ #GOLD
```

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-21,20260921_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,91,84,,EVENT,88,92,97,90,90,88,wait_for_GCZ26_post_weekend_open_break_4450_or_failure_below_4370,GCZ26_4370_4415.90_4439.60_4450_US10Y_DXY_1d_3d,partially_verified
2026-09-21,20260921_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,89,84,,RISK_ON,82,89,95,86,86,83,wait_for_82k_break_hold_or_79k_retest_with_ETF_CME_confirmation,BTC_79000_80000_80894_82000_ETF_CME_1d_3d,partially_verified
2026-09-21,20260921_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,85,86,,RISK_ON,80,88,94,84,83,79,wait_for_2550_2580_retest_or_2670_break_with_ETF_CME_confirmation,ETH_2550_2580_2628_2670_ETF_CME_1d_3d,partially_verified
2026-09-21,20260921_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,96,99,,EVENT,94,99,99,96,95,98,manage_existing_20260917_on_OILCash_and_Oct26_do_not_use_Nov26_roll_price_for_SL,WTI_Oct26_98.90_100.30_101.19_105.20_Nov26_96.08_OILCash_week_open,partially_verified
2026-09-21,20260921_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,91,88,,EVENT,82,95,98,90,85,95,manage_existing_20260919_BUY_PULLBACK_155.20_or_confirmed_intervention_fires,USDJPY_155.20_156.00_156.50_156.8_158.20_MOF_1d_3d,partially_verified
2026-09-21,20260921_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,85,92,,MIXED,76,86,96,84,83,88,wait_for_ESZ26_post_weekend_open_and_VIX_US10Y_confirmation,ESZ26_7675_7712.50_7740_US10Y_VIX_1d_3d,partially_verified
2026-09-21,20260921_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,91,90,,MIXED,82,89,97,91,90,91,wait_for_NQZ26_30000_hold_or_pullback_without_chasing_weekend_gap,NQZ26_29600_29917.25_30000_US10Y_VIX_1d_3d,partially_verified
2026-09-21,20260921_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,82,88,,MIXED,80,91,96,82,82,91,wait_for_DXY_break_100.3_or_failure_below_99.5_with_US10Y_USDJPY_confirmation,DXY_99.5_99.937_100.3_US10Y_USDJPY_1d_3d,partially_verified
2026-09-21,20260921_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,90,90,,EVENT,92,95,98,89,91,97,wait_for_sustained_break_above_5.05_or_rejection_below_4.90_after_hawkish_Fed_comments,US10Y_4.90_4.996_5.05_WTI_GOLD_NQ_1d_3d,partially_verified
2026-09-21,20260921_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,83,95,,EVENT,76,90,97,81,81,91,wait_for_week_open_reclaim_above_16_or_hold_below_15_after_Saudi_weekend_event,VIX_14.81_15_16_ES_NQ_1d_3d,partially_verified
```

### TSO_LOG JSON

```json
[
  {"date":"2026-09-21","signal_id":"20260921_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":91,"no_trade_score":84,"risk_pct":null,"regime":"EVENT","ems":88,"ffs":92,"cds":97,"ias":90,"cbs":90,"mes":88,"invalidation":"wait_for_GCZ26_post_weekend_open_break_4450_or_failure_below_4370","verification_target":"GCZ26_4370_4415.90_4439.60_4450_US10Y_DXY_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-21","signal_id":"20260921_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":89,"no_trade_score":84,"risk_pct":null,"regime":"RISK_ON","ems":82,"ffs":89,"cds":95,"ias":86,"cbs":86,"mes":83,"invalidation":"wait_for_82k_break_hold_or_79k_retest_with_ETF_CME_confirmation","verification_target":"BTC_79000_80000_80894_82000_ETF_CME_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-21","signal_id":"20260921_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":85,"no_trade_score":86,"risk_pct":null,"regime":"RISK_ON","ems":80,"ffs":88,"cds":94,"ias":84,"cbs":83,"mes":79,"invalidation":"wait_for_2550_2580_retest_or_2670_break_with_ETF_CME_confirmation","verification_target":"ETH_2550_2580_2628_2670_ETF_CME_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-21","signal_id":"20260921_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":96,"no_trade_score":99,"risk_pct":null,"regime":"EVENT","ems":94,"ffs":99,"cds":99,"ias":96,"cbs":95,"mes":98,"invalidation":"manage_existing_20260917_on_OILCash_and_Oct26_do_not_use_Nov26_roll_price_for_SL","verification_target":"WTI_Oct26_98.90_100.30_101.19_105.20_Nov26_96.08_OILCash_week_open","verified_status":"partially_verified"},
  {"date":"2026-09-21","signal_id":"20260921_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":91,"no_trade_score":88,"risk_pct":null,"regime":"EVENT","ems":82,"ffs":95,"cds":98,"ias":90,"cbs":85,"mes":95,"invalidation":"manage_existing_20260919_BUY_PULLBACK_155.20_or_confirmed_intervention_fires","verification_target":"USDJPY_155.20_156.00_156.50_156.8_158.20_MOF_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-21","signal_id":"20260921_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":85,"no_trade_score":92,"risk_pct":null,"regime":"MIXED","ems":76,"ffs":86,"cds":96,"ias":84,"cbs":83,"mes":88,"invalidation":"wait_for_ESZ26_post_weekend_open_and_VIX_US10Y_confirmation","verification_target":"ESZ26_7675_7712.50_7740_US10Y_VIX_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-21","signal_id":"20260921_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":91,"no_trade_score":90,"risk_pct":null,"regime":"MIXED","ems":82,"ffs":89,"cds":97,"ias":91,"cbs":90,"mes":91,"invalidation":"wait_for_NQZ26_30000_hold_or_pullback_without_chasing_weekend_gap","verification_target":"NQZ26_29600_29917.25_30000_US10Y_VIX_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-21","signal_id":"20260921_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":82,"no_trade_score":88,"risk_pct":null,"regime":"MIXED","ems":80,"ffs":91,"cds":96,"ias":82,"cbs":82,"mes":91,"invalidation":"wait_for_DXY_break_100.3_or_failure_below_99.5_with_US10Y_USDJPY_confirmation","verification_target":"DXY_99.5_99.937_100.3_US10Y_USDJPY_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-21","signal_id":"20260921_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":90,"no_trade_score":90,"risk_pct":null,"regime":"EVENT","ems":92,"ffs":95,"cds":98,"ias":89,"cbs":91,"mes":97,"invalidation":"wait_for_sustained_break_above_5.05_or_rejection_below_4.90_after_hawkish_Fed_comments","verification_target":"US10Y_4.90_4.996_5.05_WTI_GOLD_NQ_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-21","signal_id":"20260921_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":83,"no_trade_score":95,"risk_pct":null,"regime":"EVENT","ems":76,"ffs":90,"cds":97,"ias":81,"cbs":81,"mes":91,"invalidation":"wait_for_week_open_reclaim_above_16_or_hold_below_15_after_Saudi_weekend_event","verification_target":"VIX_14.81_15_16_ES_NQ_1d_3d","verified_status":"partially_verified"}
]
```

今日の最大のポイントは、**WTIの96ドル表示を損切りシグナルと誤認しないこと**です。Oct-26の100.30からNov-26の96.08への切り替えは契約ロールです。既存OILCashポジションの判断基準は引き続き**実際のOILCash価格98.90**で、現在のシナリオ自体は`not_fired`です。月曜の実価格形成を確認するまでは追加注文を出さない判断とします。
