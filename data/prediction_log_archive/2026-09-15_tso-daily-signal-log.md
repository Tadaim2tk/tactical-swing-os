<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-15 07:00 JST -->
<!-- transport: DOM innerText -> Blob download -> tools/archive_gpt_prose.py -->
<!-- archived_at: 2026-09-15T03:04:24Z / chars: 18024 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-09-15

**使用モデル：GPT-5.6 Sol**  
**本日の市場の主役：US10Y**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**株価指数先物：新規観察は12月限 ESZ26 / NQZ26。既存9/11 NASDAQシグナルだけは発行時のNQU26で最後まで判定。**  
**crypto_grounds: etf=有, cme=有**  
**expected_r_basis: subjective** — 本日は新規方向ありシグナルを発行しないため、当日LOGの`expected_r`は空欄。既存シグナルでは未約定、5営業日時間決済、マクロinvalidation、イベント前の早期撤退を含む従来基準を維持します。

**invalidation_check: 20260908_WTI_BUY_PULLBACK=not_fired, 20260908_USDJPY_SELL_PULLBACK=not_fired, 20260909_WTI_BUY_PULLBACK=not_fired, 20260909_USDJPY_SELL_PULLBACK=not_fired, 20260911_NASDAQ_SELL_PULLBACK=not_fired, 20260912_BTC_SELL_PULLBACK=unknown**

9/4～9/7起点の方向あり判断は、9/14終了時点で5営業日窓を満了したため本日から除外しました。9/8起点は本日が5営業日目の最終確認日です。BTCだけ`unknown`なのは、価格側80850超は確認されていない一方、9/12に定義したもう一つの失効条件「fresh ETF reinflow with CME reclaim」について、9/14のETF確定値が実行時点で未完成かつ「CME reclaim」の閾値を元ログから数値として確定できないためです。推測で`not_fired`にはしません。Farsideでは9/14欄がまだ未入力で、最新完成値はBTCが9/11の-13.2Mドル、ETHが+216.4Mドルです。citeturn803118view0turn325965view0

データ基準は**2026-09-14米国市場終了～9/15 07:00 JST直前**です。新規Web取得を実施しています。

## 1. 本日の結論

**新規A級：0件**  
**新規B級：0件**  
**新規B+：0件**

**10資産すべて新規NO_TRADE。**

ただし、昨日までと違って「方向が分からないから見送り」ではありません。現在かなり明確なのは、

**WTI：上方向の供給ショック継続**  
**US10Y：5%到達、金利上方向圧力**  
**GOLD：金利・ドル高に押される**  
**NASDAQ：マクロ逆風だが、安値からかなり戻す**  
**USDJPY：ドル高で反発したがBOJ引き締め仮説は生存**  
**BTC：80kを回復できず**

です。

9月14日、米10年債利回りは**5.01%**まで上昇し、2023年以来初めて5%を突破しました。終盤は約**4.96%**へ戻しています。原油高、インフレ再加速懸念、AI関連投資に伴う債券供給増などが背景です。citeturn309720view1turn910542news72

WTIは一時ほぼ5%上昇したものの、最終的には**101.39ドル、+1.3%**で清算。Brentは105.68ドルでした。つまりサウジ東西パイプライン停止・ホルムズ通航減少という極めて強い材料に対して、**高値から大きく押し戻されています**。citeturn309720view2

ここが今日の重要点です。

**材料はWTI強気だが、価格反応は以前より鈍い。**

したがってWTIを今からBUYするより、「供給ショックが価格に織り込まれ始めたか」を観察する局面に移っています。

Fedは9月15～16日の会合で25bp利上げが中心予想で、Reuters調査では85%のエコノミストが利上げを予想。市場価格でも約90%が織り込まれています。BOJも9月18日に1.25%への25bp利上げが中心予想です。citeturn280478news15turn280478news19

urlReuters：米10年債利回り5%突破（9月14日）turn309720view1  
urlReuters：WTI 101.39ドル清算（9月14日）turn309720view2

## 2. 前回判断の簡易検証

9/14は新規方向あり判断を発行していないため、既存判断を検証します。

### 20260908 / 20260909 WTI BUY

9/8シグナルのEntryは91ドル台、9/9は91.80–92.50。9/14のWTIは**101.39ドル清算**で、両シグナルの価格失効水準を大幅に上回っています。

また、供給面でも正常化していません。サウジ東西パイプラインは攻撃で停止し、ホルムズの船舶通過も週末には1日一桁まで減少。Reutersによれば東西パイプライン停止は最大で世界供給の約4%を脅かします。citeturn309720view2

したがって、

**20260908_WTI_BUY_PULLBACK=not_fired**  
**20260909_WTI_BUY_PULLBACK=not_fired**

です。

9/8は今日で5営業日の確認を終了します。

### 20260908 / 20260909 USDJPY SELL

9/14のUSDJPYはデータ提供元で**高値155.00、終値付近154.36**。Reuters終盤値も154.355円です。citeturn494345search6turn309720view0

9/9シグナル：

**Entry 154.80–155.40  
SL 156.20**

なので、**Entryには到達しました**。

9/8シグナルもEntry下端が155.00付近だったため、価格としては下端タッチですが、データの丸め・bid/askを考慮し「明確約定」とは断定しません。

重要なのは、どちらも失効水準156.20/156.40には届いていないことです。

さらにBOJは今週25bp利上げがほぼ中心シナリオなので、円高側の政策仮説も消えていません。citeturn280478news19

したがって、

**20260908_USDJPY_SELL_PULLBACK=not_fired**  
**20260909_USDJPY_SELL_PULLBACK=not_fired**

です。

9/8は本日で最終確認。

### 20260911 NASDAQ SELL

既存：

**NQU26 Entry 29300–29400  
SL 29620  
TP1 28750**

ロール前のNQU26は9/14に**高値約29303**までで、29620には到達していません。マクロ失効条件だった

**US10Y <4.80 かつ WTI <100**

も、10年債約4.96%、WTI101.39なので成立していません。citeturn489732search9turn309720view2turn910542news72

したがって、

**20260911_NASDAQ_SELL_PULLBACK=not_fired**

です。

ただし、新主力のNQZ26は9/14に**29107付近まで急落後、29560台まで大きく戻した**ことが確認できます。これはSELL仮説にとって注意すべき価格反応です。citeturn489732search9

### 20260912 BTC SELL

既存：

**Entry 79200–79800  
SL 80850  
TP1 76450**

最新のBTC/USD取得値には時点差があります。遅い時間の市場データでは約**77.6k**、Reuters記事では一時**79,152**が確認されました。いずれも80850には達しておらず、79,200のEntry下端も明確に上抜けたとは確認できません。citeturn250699search6turn309720view0

ただし9/14 ETFフローがまだ確定していないため、前述の通りinvalidation全体は**unknown**とします。

取引状態は現時点で、

**ORDER_NOT_CONFIRMED_FILLED / PRICE_THESIS_ALIVE**

です。

## 3. 市場全体の前提

本日の総合regimeは**EVENT**。

市場を支配しているのは「原油そのもの」より、現在は**原油高を金利市場がどう処理しているか**です。

米10年債5%は重要な閾値です。5%近辺まで上がると、株式の益回りとの比較で債券が相対的に魅力を増し、住宅・企業金融・消費者信用まで広く引き締めます。Reutersも5%を株式市場への重要な脅威となり得る水準として扱っています。citeturn309720view1

一方で、株式は完全には崩れていません。S&P500現物は9/14に-0.5%、Nasdaq Compositeは-0.6%でしたが、先物ではNQZ26が一時29100台まで下げた後、29500台へ大きく戻しました。citeturn910542news73turn489732search9

このため、

**US10Y 5%突破＝即NASDAQ SELL**

とはしません。

むしろ「5%でもNQが安値から戻せる」こと自体を新しい観察データとします。

DXYは**99.41**まで上昇。USDJPYは154.36。ドルは広く買われましたが、円はBOJ利上げ期待があるため他通貨ほど一方向には弱くなっていません。citeturn309720view0

GoldはReutersで米金先物**4351.90ドル**、一方GCZ26の別データ提供元では約4320ドルと差があります。どちらも方向は大幅安で一致していますが、基準値の差が無視できないためGOLDは`partially_verified`にします。citeturn241223news32turn472805search5

VIXは約**17.18**まで上昇しましたが、20には届いていません。株式の警戒は増えたもののパニックではありません。citeturn309720view4

CryptoではBTCが80kを維持できない一方、ETHは9/14に約**2543ドル**まで上昇。前週ETFフローもBTCが-462.7Mドル、ETHが+196.9Mドルと大きく分岐しています。citeturn202676search3turn472805search2

## 4. 10資産別判断

| 資産 | 本日判断 | コメント |
|---|---|---|
| GOLD | **NO_TRADE** | 金利・DXYはSELL材料だが既に下落済み、価格ソース差も大 |
| BTC | **NO_TRADE / 既存SELL管理** | 約77.6k基準、79.2kへ戻らない限り追わない |
| ETH | **NO_TRADE** | 約2543、BTCより強いがFed直前 |
| WTI | **NO_TRADE / 既存BUY管理** | 101.39、高値から失速。供給ショック追随禁止 |
| USDJPY | **NO_TRADE / 既存SELL管理** | 154.36、既存Entry到達。新規を重ねない |
| SPX | **NO_TRADE** | ESZ26約7700台、5%金利と押し目需要が衝突 |
| NASDAQ | **NO_TRADE / 既存SELL管理** | NQZ26安値から強く戻す。追加SELL禁止 |
| DXY | **NO_TRADE** | 99.41、Fed織り込み済み |
| US10Y | **NO_TRADE** | 5%突破済み、Fed前に追わない |
| VIX | **NO_TRADE** | 約17.18、上昇したが20未満 |

ESZ26は遅延値で約**7708**、日中レンジ約7661–7720。NQZ26は約**29560台**、日中レンジ約29107–29605です。12月限へロール済みなので、本日の新規市場観察はこちらを使います。citeturn910542search5turn489732search9

## 5. A級候補

**なし。**

数値だけならWTI・US10Y・NASDAQはCBS/EMSが高いですが、現在は3資産とも**Entry品質が悪い**です。

WTIは供給障害を知った後の100ドル超追随。

US10Yは5%突破後。

NASDAQは一度急落した後に大きく戻しており、しかもFed直前。

A級に必要なのは「方向確信」ではなく、**良い価格で非対称なリスクを取れること**なので、今日は該当しません。

## 6. B級監視候補

**新規B級なし。**

既存で監視価値があるのは3つです。

**20260909_USDJPY_SELL_PULLBACK**  
Entry 154.80–155.40は9/14に到達。SL156.20、TP1 152.50。現在は既存シグナルの管理対象で、新しくSELLを重ねません。

**20260911_NASDAQ_SELL_PULLBACK**  
NQU26の29620超でfired。今後はロール差を混ぜないため、NQZ26の値を29620へ直接比較しません。

**20260912_BTC_SELL_PULLBACK**  
Entry 79200–79800。現在77k台なら追わない。76450がTP1参考です。

これら3本で十分です。新しいsignal_idを追加して同一仮説を重複計上しません。

## 7. 触らない資産

最優先は**WTI**です。

9/14はサウジ供給リスクで一時約5%上がったにもかかわらず、最終上昇率は1.3%まで縮小しました。これは「悪材料が強い＝価格も永遠に上がる」局面ではなくなりつつある可能性があります。citeturn309720view2

ここからBUYすると高値掴み、SELLすると供給ショック逆張り。どちらも悪い取引です。

次が**US10Y**。5%は重要ですが、Fed決定を約1日後に控えた状態で5%突破を追うのはイベントギャンブル化します。

**GOLD**も追いSELLしません。金利・ドルの逆風は明確ですが、すでに大きく下落し、中東情勢によるsafe-haven需要がいつ戻るか分かりません。

**NASDAQ**は特に重要です。5%金利＋AI関連悪材料＋原油高という強いSELL材料に対し、NQZ26が29100台から29500台まで戻しました。**弱材料に対する下落持続力が不足した可能性**があります。追加SELLはしません。

## 8. 後日検証ポイント

第一は**US10Yの5%定着**です。

Fedが25bp利上げして、

**US10Y >5.00を維持  
＋ NQZ26が再び29100方向**

なら、金利主導RISK_OFFを強く支持します。

逆に利上げしても、

**US10Y <4.90  
＋ NQZ26 >29600**

なら、「利上げは既に価格に織り込み済み」だった可能性が高まります。

第二はWTI。

9/14に供給ショックで高値を大きく削りました。

**WTI >105定着**なら供給不足が価格形成を再支配。

**WTI <100 despite continued disruption**ならbad-news exhaustionです。

これは既存BUY群の終了判断に重要です。

第三はUSDJPY。

9/14に米10年債が5%へ上がったことでUSDJPYも155.00まで戻しました。

それでも、

**Fed利上げ後に156を超えられない**

なら、BOJ利上げ・円ロング転換の力が依然強いと判断します。

第四はBTC/ETH。

Farsideの9/14 ETF欄は実行時点で未完成です。確定後、

**BTC ETF再流入 + BTC >80k + CME >80k**

なら9/12 SELLの需給失効を強く疑います。

一方、

**BTC ETF流出継続 + BTC <76450**

ならSELL仮説を支持。

ETHについては、**ETF流入継続 + ETH >2600**なら単独BUY候補へ昇格させます。

第五は今週の中央銀行。

Fedは**9月16日**、BOJは**9月18日**。両方利上げが中心シナリオなので、USDJPYは通常以上に「米金利だけ」では説明できない週です。citeturn280478news15turn280478news19

## 9. Obsidian保存用 Observation Draft

```markdown
# 2026-09-15 US10Y Breaks 5 Percent

Model:
GPT-5.6 Sol

Market protagonist:
US10Y

Gold reference:
COMEX Dec-2026 / GCZ26

Equity futures:
new observations = ESZ26 / NQZ26
existing Sep11 NASDAQ signal = NQU26 until expiry of signal window

crypto_grounds:
etf=有
cme=有

ETF freshness:
Sep14 incomplete at execution
latest completed:
BTC Sep11 -13.2m
ETH Sep11 +216.4m

CME BTC:
Sep14 data available
feed timestamps differ
roughly high-77k to high-78k range

expected_r_basis:
subjective

Today:
no new directional signal

## Regime

EVENT

## Market

WTI:
101.39 settle
intraday nearly +5%
large fade from highs

Brent:
105.68

US10Y:
crossed 5.00
intraday ~5.01
late ~4.96

DXY:
99.41

USDJPY:
~154.36
Sep14 high ~155.00

Gold Dec:
Reuters US futures ~4351.9
alternative GCZ26 feed ~4320
partially_verified

VIX:
~17.18

ESZ26:
~7708 delayed
range ~7661-7720

NQZ26:
~29560s delayed
range ~29107-29605

BTC:
~77.6k late-feed reference
Reuters intraday print ~79.15k
partially_verified

ETH:
~2543

## Existing invalidation

20260908_WTI_BUY_PULLBACK=not_fired
20260908_USDJPY_SELL_PULLBACK=not_fired
20260909_WTI_BUY_PULLBACK=not_fired
20260909_USDJPY_SELL_PULLBACK=not_fired
20260911_NASDAQ_SELL_PULLBACK=not_fired
20260912_BTC_SELL_PULLBACK=unknown

Sep4-Sep7 signals:
5-business-day window completed Sep14
removed from active invalidation list

## Existing USDJPY sell

Sep9:
Entry 154.80-155.40
Sep14 high ~155.00
Entry reached

SL 156.20:
not reached

## Existing NASDAQ sell

NQU26:
Entry 29300-29400
SL 29620
TP1 28750

Sep14:
SL not reached

Macro invalidation:
US10Y <4.80 AND WTI <100
not triggered

## Existing BTC sell

Entry:
79200-79800

SL:
80850

TP1:
76450

Price SL:
not triggered

ETF/CME invalidation:
unknown
Sep14 ETF flow incomplete

## Today

A:
NONE

B new:
NONE

NO_TRADE:
GOLD
BTC
ETH
WTI
USDJPY
SPX
NASDAQ
DXY
US10Y
VIX

## Primary research test

US10Y 5 percent threshold

If Fed hike:
US10Y >5.00
NQZ26 -> 29100
supports yield-driven risk-off

If:
US10Y <4.90
NQZ26 >29600
suggests hike largely priced

## Oil exhaustion test

Saudi / Hormuz disruption remains severe

But Sep14:
WTI almost +5% intraday
settled only +1.3%

If WTI <100:
bad-news exhaustion

If WTI >105:
supply shock re-acceleration

#TSO #US10Y #WTI #NASDAQ #USDJPY #BTC #Fed #BOJ
```

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-15,20260915_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,70,80,,EVENT,94,91,98,68,77,91,GCZ26_reclaim_above_4400_or_clean_break_below_4300_after_Fed_required,GCZ26_4300_4352_4400_US10Y_DXY_Fed_1d_3d,partially_verified
2026-09-15,20260915_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,73,72,,EVENT,75,88,94,72,76,70,manage_existing_20260912_sell_until_80850_or_verified_ETF_CME_reversal,BTC_76450_77600_79200_80850_ETF_CME_Fed_1d_3d,partially_verified
2026-09-15,20260915_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,77,68,,MIXED,76,86,91,75,78,72,ETH_hold_above_2600_with_confirmed_ETF_inflow_required,ETH_2480_2543_2600_ETF_ETHBTC_Fed_1d_3d,partially_verified
2026-09-15,20260915_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,95,88,,EVENT,98,99,99,92,94,97,WTI_above_105_or_below_100_with_supply_context_required_before_new_signal,WTI_100_101.39_105_Hormuz_EastWest_Fed_1d_3d,verified
2026-09-15,20260915_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,84,66,,EVENT,89,95,98,82,86,94,manage_existing_sell_until_156.20_156.40_or_BOJ_repricing_reversal,USDJPY_152.5_154.36_155_156.2_Fed_BOJ_1d_3d,verified
2026-09-15,20260915_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,71,79,,RISK_OFF,88,90,97,69,79,92,ESZ26_reaction_to_US10Y_5pct_and_Fed_required,ESZ26_7660_7708_7720_US10Y_WTI_Fed_1d_3d,partially_verified
2026-09-15,20260915_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,82,75,,RISK_OFF,92,93,98,81,84,94,manage_existing_NQU26_sell_and_wait_for_NQZ26_postFed_price_discovery,NQU26_28750_29300_29620_NQZ26_29100_29600_1d_3d,partially_verified
2026-09-15,20260915_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,68,73,,EVENT,87,90,95,66,75,91,Fed_confirmed_break_below_99_or_above_100_required,DXY_99_99.41_100_US10Y_USDJPY_Fed_1d_3d,verified
2026-09-15,20260915_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,93,88,,EVENT,99,99,99,92,94,99,postFed_hold_above_5.00_or_reversal_below_4.90_required,US10Y_4.90_4.96_5.01_WTI_NQ_Fed_1d_3d,verified
2026-09-15,20260915_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,65,78,,RISK_OFF,82,82,96,64,73,85,VIX_break_above_20_or_return_below_15.5_with_equity_confirmation_required,VIX_15.5_17.18_20_ES_NQ_Fed_1d_3d,verified
```

## TSO_LOG JSON

```json
[
  {"date":"2026-09-15","signal_id":"20260915_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":70,"no_trade_score":80,"risk_pct":null,"regime":"EVENT","ems":94,"ffs":91,"cds":98,"ias":68,"cbs":77,"mes":91,"invalidation":"GCZ26_reclaim_above_4400_or_clean_break_below_4300_after_Fed_required","verification_target":"GCZ26_4300_4352_4400_US10Y_DXY_Fed_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-15","signal_id":"20260915_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":73,"no_trade_score":72,"risk_pct":null,"regime":"EVENT","ems":75,"ffs":88,"cds":94,"ias":72,"cbs":76,"mes":70,"invalidation":"manage_existing_20260912_sell_until_80850_or_verified_ETF_CME_reversal","verification_target":"BTC_76450_77600_79200_80850_ETF_CME_Fed_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-15","signal_id":"20260915_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":77,"no_trade_score":68,"risk_pct":null,"regime":"MIXED","ems":76,"ffs":86,"cds":91,"ias":75,"cbs":78,"mes":72,"invalidation":"ETH_hold_above_2600_with_confirmed_ETF_inflow_required","verification_target":"ETH_2480_2543_2600_ETF_ETHBTC_Fed_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-15","signal_id":"20260915_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":95,"no_trade_score":88,"risk_pct":null,"regime":"EVENT","ems":98,"ffs":99,"cds":99,"ias":92,"cbs":94,"mes":97,"invalidation":"WTI_above_105_or_below_100_with_supply_context_required_before_new_signal","verification_target":"WTI_100_101.39_105_Hormuz_EastWest_Fed_1d_3d","verified_status":"verified"},
  {"date":"2026-09-15","signal_id":"20260915_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":84,"no_trade_score":66,"risk_pct":null,"regime":"EVENT","ems":89,"ffs":95,"cds":98,"ias":82,"cbs":86,"mes":94,"invalidation":"manage_existing_sell_until_156.20_156.40_or_BOJ_repricing_reversal","verification_target":"USDJPY_152.5_154.36_155_156.2_Fed_BOJ_1d_3d","verified_status":"verified"},
  {"date":"2026-09-15","signal_id":"20260915_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":71,"no_trade_score":79,"risk_pct":null,"regime":"RISK_OFF","ems":88,"ffs":90,"cds":97,"ias":69,"cbs":79,"mes":92,"invalidation":"ESZ26_reaction_to_US10Y_5pct_and_Fed_required","verification_target":"ESZ26_7660_7708_7720_US10Y_WTI_Fed_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-15","signal_id":"20260915_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":82,"no_trade_score":75,"risk_pct":null,"regime":"RISK_OFF","ems":92,"ffs":93,"cds":98,"ias":81,"cbs":84,"mes":94,"invalidation":"manage_existing_NQU26_sell_and_wait_for_NQZ26_postFed_price_discovery","verification_target":"NQU26_28750_29300_29620_NQZ26_29100_29600_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-15","signal_id":"20260915_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":68,"no_trade_score":73,"risk_pct":null,"regime":"EVENT","ems":87,"ffs":90,"cds":95,"ias":66,"cbs":75,"mes":91,"invalidation":"Fed_confirmed_break_below_99_or_above_100_required","verification_target":"DXY_99_99.41_100_US10Y_USDJPY_Fed_1d_3d","verified_status":"verified"},
  {"date":"2026-09-15","signal_id":"20260915_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":93,"no_trade_score":88,"risk_pct":null,"regime":"EVENT","ems":99,"ffs":99,"cds":99,"ias":92,"cbs":94,"mes":99,"invalidation":"postFed_hold_above_5.00_or_reversal_below_4.90_required","verification_target":"US10Y_4.90_4.96_5.01_WTI_NQ_Fed_1d_3d","verified_status":"verified"},
  {"date":"2026-09-15","signal_id":"20260915_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":65,"no_trade_score":78,"risk_pct":null,"regime":"RISK_OFF","ems":82,"ffs":82,"cds":96,"ias":64,"cbs":73,"mes":85,"invalidation":"VIX_break_above_20_or_return_below_15.5_with_equity_confirmation_required","verification_target":"VIX_15.5_17.18_20_ES_NQ_Fed_1d_3d","verified_status":"verified"}
]
```

本日の最大の観察点は、**US10Yがついに5%を突破したのに、NQが日中安値からかなり戻したこと**です。これは単純な「金利高＝NASDAQを売ればよい」という局面ではないことを示します。同時にWTIも最悪級の供給ニュースに対して高値を大きく削りました。今日はこの2つの**悪材料への価格反応低下**を重く見て、新規ポジションは作らず、既存USDJPY SELL・NASDAQ SELL・BTC SELLの検証を優先します。
