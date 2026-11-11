<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-14 07:00 JST -->
<!-- transport: /backend-api/conversation (raw markdown, Bearer=/api/auth/session) -> Blob file with TSO_DAILY delimiter -> tools/archive_gpt_prose.py -->
<!-- archived_at: 2026-09-15T03:04:24Z / chars: 17020 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-09-14

**使用モデル：GPT-5.6 Sol**  
**本日の市場の主役：WTI**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**crypto_grounds: etf=有, cme=無**  
**expected_r_basis: subjective** — 本日は新規方向あり判断を発行しないため、当日LOGの`expected_r`は空欄。既存シグナルでは未約定、5営業日時間決済、早期invalidationを含むsubjective基準を継続します。

**invalidation_check: 20260904_WTI_BUY_PULLBACK=unknown, 20260905_WTI_BUY_PULLBACK=unknown, 20260906_WTI_BUY_PULLBACK=unknown, 20260907_WTI_BUY_PULLBACK=unknown, 20260908_WTI_BUY_PULLBACK=unknown, 20260908_USDJPY_SELL_PULLBACK=not_fired, 20260909_WTI_BUY_PULLBACK=unknown, 20260909_USDJPY_SELL_PULLBACK=not_fired, 20260911_NASDAQ_SELL_PULLBACK=unknown, 20260912_BTC_SELL_PULLBACK=not_fired**

`unknown`を多用した理由は明確です。**本日の実行時刻は米東部時間9月13日18:01前後で、CME/NYMEXの週明け取引開始直後**です。新規Web取得は実施しましたが、WTI・GC・ES・NQの取得ページはまだ9月11日終値を表示しており、今週初値を確認できません。価格条件を含むinvalidationを「たぶん大丈夫」で`not_fired`にはしません。一方USDJPYは9月13日17:57 ET時点で**153.48**、BTCは17:25 ET時点で**77408**を取得できているため、この2系列は現在値を用いて判定しています。citeturn286673view3turn979268view0

9/4・9/5・9/6・9/7起点のWTI判断は、Labor Day後の9/8・9/9・9/10・9/11・9/14で**本日が5営業日窓の最終確認日**です。今週初値が確認できないため、最終判定は`unknown`のまま閉じる可能性があります。

## 1. 本日の結論

**新規A級：0件**  
**新規B級：0件**  
**新規B+：0件**

**10資産すべて新規NO_TRADE**です。

昨日との最大の変化は、週末のWTI強気材料がさらに悪化したことです。Reutersによれば、ドローン攻撃を受けたサウジの東西パイプラインは依然停止中で、この迂回ルートは約400万bpdを処理しており、停止が長引けば**世界供給の約4%が追加で脅かされる**可能性があります。Yanbu在庫も5～7日で逼迫する可能性が指摘されています。さらにオマーンで予定されていた海上安全協議は延期され、ホルムズ正常化も確認できていません。citeturn893009news32turn893009news35

urlReuters：サウジ東西パイプライン停止（2026-09-13）turn893009news32

これはWTI BUY材料として非常に強い一方、**まさに供給ショック直後のmomentum追随を禁止すべき局面**です。金曜のWTI10月限は100.05ドル清算、高値104.46、安値98.48でした。週明け価格をまだ取得できていない以上、新規Entry・SLを推測で作りません。citeturn355854view0

BTCは77408ドル。9/12 SELLのEntry 79200–79800からさらに離れており、ここからSELLするのは追随です。ETHは2513.67ドル。9/11のETFフローはBTCが**-13.29Mドル**で4営業日連続流出、ETHは集計会社間に差はあるものの明確な純流入でした。BTCとETHで機関需給が分岐しています。citeturn979268view0turn979268view1turn934435search0turn934435search2turn934435search3

## 2. 前回判断の簡易検証

昨日9/13は新規方向あり判断を発行していないため、管理対象は主に**20260912_BTC_SELL_PULLBACK**と**20260911_NASDAQ_SELL_PULLBACK**です。

BTC SELLは、

**Entry 79200–79800 / SL 80850 / TP1 76450 / TP2 74800**

でした。シグナル発行後の9/12価格は取得系列で高値約77303ドル、現在は77408ドルであり、**Entry帯は未到達**です。BTCは正しい方向へ進んでいますが取引にはなっていません。ETFも9/11は再流入ではなく-13.29Mドルの流出だったため、需給invalidationも発火していません。citeturn131541search7turn979268view0turn934435search0

したがって、

**20260912_BTC_SELL_PULLBACK = ORDER_NOT_FILLED / THESIS_ALIVE / not_fired**

です。

NASDAQ SELLは、

**Entry 29300–29400 / SL 29620 / TP1 28750**

で、9/11のNQU26は高値29500.25、安値29040.50、清算29387。金曜までの範囲ではSL未到達です。citeturn286673view1

ただし本日07:00 JSTに週明けGlobexが再開している一方、取得可能なNQU26ページはまだ金曜値です。そのため**現在時点のinvalidationはunknown**とします。ここは推測しません。

また今日は株価指数先物のロール移行期です。金曜時点でESZ26は7727.25清算、NQZ26は29684.25清算でした。既存9/11 NASDAQ SELLのinvalidationは**発行時と同じNQU26で最後まで判定**し、新規の日次観察は12月限への出来高移行も併せて確認します。citeturn254141view0turn185365view0

## 3. 市場全体の前提

総合regimeは**EVENT**です。

週明けは中央銀行イベントと中東供給ショックが重なります。米10年債利回りは金曜に一時**4.979%**まで上昇し、5%目前。9月16日のFedについて市場は25bp利上げを約85～87%織り込んでいます。BOJも9月17～18日の会合で1.25%への25bp利上げが中心予想です。citeturn453090news17turn509500news21turn509500news32turn893009news38

円については追加材料があります。CFTCデータで投機筋の円ポジションが、9月8日終了週に**2月以来初めてネットロング**へ転換しました。USDJPYも日曜17:57 ETで153.48と、既存SELLシナリオの156.20/156.40から十分下です。citeturn893009news34turn286673view3

GoldはGCZ26の金曜清算が**4408.90**、日中レンジ4333.0～4444.9。高金利だけなら弱いはずですが、中東悪化による安全資産需要が同時に働くため単純SELLにはしません。citeturn355854view1

VIXはCboe公式で9月11日**15.84**。株式市場は金曜時点ではパニックを解除していました。しかし、その後にサウジ供給網への新しい攻撃が追加されたため、金曜VIXだけを使って月曜もRISK_ONとは判断しません。citeturn893009search0

## 4. 10資産別判断

| 資産 | 新規判断 | 基準・理由 |
|---|---|---|
| GOLD | **NO_TRADE** | GCZ26金曜4408.9。金利高 vs 地政学safe-haven |
| BTC | **NO_TRADE / 既存SELL管理** | 77408。Entryより下、追わない |
| ETH | **NO_TRADE** | 2513.7。ETF流入は強いが2600未確認 |
| WTI | **NO_TRADE / 既存BUY管理** | 金曜100.05＋週末供給悪化。週明け価格待ち |
| USDJPY | **NO_TRADE / 既存SELL管理** | 153.48。円ロング転換＋BOJ期待 |
| SPX | **NO_TRADE** | ESロール＋週明け価格未取得 |
| NASDAQ | **NO_TRADE / 既存SELL管理** | NQロール＋既存SLの現在判定不可 |
| DXY | **NO_TRADE** | 金曜99.10。Fedタカ派でも円高継続 |
| US10Y | **NO_TRADE** | 金曜4.97%近辺。Fed直前＋5%攻防 |
| VIX | **NO_TRADE** | 金曜15.84。週末ショックをまだ反映していない |

DXYは金曜99.10、日中98.97～99.37でした。citeturn286673view2

## 5. A級候補

**なし。**

WTIのCBS/EMSは非常に高く評価できますが、A級とは「方向確率が高い」だけではありません。**実際に入れるEntryが存在すること**が必要です。

現状は金曜100.05に対し、週末に供給リスクがさらに悪化。もし週明けWTIが104～108へギャップした場合、そこを買うと供給ショックmomentum追随になります。逆に100以下なら、悪材料に対する反応低下が疑われます。

どちらの場合も**価格形成を見る前のBUYはA級になりません**。

BTC SELLも同様です。79500中点の既存シグナルに対して現在77408なので、新規SELLは約2100ドル不利です。

## 6. B級監視候補

**新規B級：なし。**

既存で重点監視するのは3系統です。

**BTC SELL**は79200–79800への戻りがない限り何もしません。TP1の76450まで残り約958ドルですが、ここから売っても元のRRは得られません。

**NASDAQ SELL**はNQU26の29620が既存価格invalidationです。現在の週明けNQを取得できていないため、今日のinvalidationは`unknown`。取得できた金曜高値29500.25までは未発火でした。citeturn286673view1

**WTI BUY群**は方向仮説そのものは週末ニュースで強まりました。しかし今日は9/4～9/7シグナル群の5営業日最終日でもあるため、新しいBUYを追加して検証窓をリセットするより、既存判断を最後まで独立評価する方を優先します。

## 7. 触らない資産

最優先で触らないのは**WTIの寄り付き追随**です。

Reutersによれば停止した東西パイプラインは約400万bpdを迂回輸送していた重要経路です。しかもホルムズ側も正常化していません。材料だけ見れば強烈なBUYですが、だからこそ価格には大きなギャップが入り得ます。citeturn893009news32turn893009news35

NASDAQも寄り付きSELLはしません。金曜はNQが反発しており、さらに今日は9月→12月限のロールが重なるため、寄り直後の値動きには**マクロ方向とロール差**が混ざります。

USDJPYも153.48からはSELLを追いません。円投機筋はネットロングへ転じており、方向仮説はむしろ強化されていますが、既存Entry 154.8～155.6から大幅に進んだ位置です。citeturn893009news34turn286673view3

ETHはBTCより需給が良いものの、ETFフローの9/11集計が**+49.3Mと+216Mでデータ会社間に大きな差**があります。方向として「流入」は採用できますが、強度は較正不能なのでBUYにはしません。citeturn934435search2turn934435search3

## 8. 後日検証ポイント

今日もっとも価値が高いのは、**週末の極端なWTI強気ニュースに対する価格反応**です。

週明けで、

**WTI >104.46 + US10Y >5.00 + NQ下落**

なら、`oil → inflation → yields → growth equities` の伝播仮説を強く支持します。

逆に、

**東西パイプライン停止継続なのにWTI <=100**

なら、材料の悪化に対して価格が上がらない「bad news exhaustion」です。これは既存WTI BUY仮説を終了方向へ再評価する重要な兆候になります。

USDJPYは、

**US10Y >5%でもUSDJPY <154**

なら、BOJ引き締め・円キャリー解消・円ロング転換が米金利差より強いことをさらに支持します。

BTCは明確です。

**76450到達 → 20260912 SELLのTP1**  
**80850突破 → fired**  
**ETF再流入＋80k回復 → 価格SL前でも需給仮説を再評価**

NASDAQは既存NQU26シグナルについて、

**29620超 → fired**  
**28750到達 → TP1**

です。ロール後のNQZ26水準をそのまま29620と比較しないことが重要です。

## 9. Obsidian保存用 Observation Draft

```markdown
# 2026-09-14 Saudi Pipeline Shock / Fed Week

Model:
GPT-5.6 Sol

Market protagonist:
WTI

Gold reference:
COMEX Dec-2026 / GCZ26

Equity futures:
existing NASDAQ signal remains NQU26
new observation begins monitoring NQZ26 / ESZ26 roll

crypto_grounds:
etf=有
cme=無

expected_r_basis:
subjective

Reason:
no new directional signal today.
Existing signals keep non-fill,
early invalidation,
and 5-business-day time exit assumptions.

## Data limitation

Execution time:
07:01 JST

CME/NYMEX reopen:
just occurred

Fresh WTI / GC / ES / NQ delayed quote:
not yet available

Do not infer first print.

## Regime

EVENT

## Latest verified prices

WTI Oct:
100.05 Friday settle
Friday high 104.46
Friday low 98.48

GCZ26:
4408.90 Friday settle

USDJPY:
153.48
Sep13 17:57 ET

BTC:
77408
Sep13 17:25 ET

ETH:
2513.67
Sep13 17:16 ET

DXY:
99.10 Friday

US10Y:
~4.97
Friday peak 4.979

VIX:
15.84 Friday

ESU26:
7659.50 settle

ESZ26:
7727.25 settle

NQU26:
29387.00 settle

NQZ26:
29684.25 settle

## Weekend oil event

Saudi East-West pipeline:
offline after drone attack

Approx rerouted flow:
~4 mbpd

Risk:
up to ~4% of global oil supply threatened
if outage persists

Hormuz:
not normalized

Oman maritime talks:
postponed

## Policy week

Fed:
Sep16
hike probability ~85-87%

BOJ:
Sep17-18
25bp hike to 1.25% consensus

JPY speculative position:
net long for first time since Feb

## Invalidation check

20260904_WTI_BUY_PULLBACK=unknown
20260905_WTI_BUY_PULLBACK=unknown
20260906_WTI_BUY_PULLBACK=unknown
20260907_WTI_BUY_PULLBACK=unknown

Reason:
fresh Monday WTI price unavailable.
Today = final 5-business-day check.

20260908_WTI_BUY_PULLBACK=unknown
20260908_USDJPY_SELL_PULLBACK=not_fired
20260909_WTI_BUY_PULLBACK=unknown
20260909_USDJPY_SELL_PULLBACK=not_fired
20260911_NASDAQ_SELL_PULLBACK=unknown
20260912_BTC_SELL_PULLBACK=not_fired

## Existing BTC SELL

Entry:
79200-79800

SL:
80850

TP1:
76450

TP2:
74800

Current:
77408

Status:
ORDER_NOT_FILLED
THESIS_ALIVE
NO_CHASE

## Existing NASDAQ SELL

Contract:
NQU26

Entry:
29300-29400

SL:
29620

TP1:
28750

Friday high:
29500.25

Monday open:
not yet verified

Status:
UNKNOWN current invalidation

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

## Primary test

If:
WTI >104.46
US10Y >5.00
NQ weak

supports:
oil -> inflation -> yields -> growth weakness

If:
WTI <=100
despite Saudi pipeline outage

watch:
bad-news exhaustion
possible WTI thesis endgame

#TSO #WTI #NASDAQ #BTC #USDJPY #US10Y #Fed #BOJ
```

## 10. TSO_LOG CSVとJSON

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-14,20260914_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,66,83,,EVENT,92,93,98,62,76,90,GCZ26_reopen_reaction_to_pipeline_shock_and_US10Y_5pct_required,GCZ26_4333_4408.9_4445_US10Y_WTI_Fed_1d_3d,partially_verified
2026-09-14,20260914_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,80,67,,MIXED,79,89,94,77,80,72,manage_existing_20260912_sell_until_80850_or_ETF_CME_reversal,BTC_76450_77408_79500_80850_ETF_CME_1d_3d,partially_verified
2026-09-14,20260914_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,75,68,,MIXED,75,88,92,74,78,74,ETH_2600_hold_with_reconciled_ETF_flow_and_BTC_stability_required,ETH_2480_2514_2600_ETF_ETHBTC_1d_3d,partially_verified
2026-09-14,20260914_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,96,94,,EVENT,98,99,99,93,95,98,fresh_Monday_price_and_EastWest_pipeline_status_required_before_new_entry,WTI_98.48_100.05_104.46_EastWest_Hormuz_1d_3d,partially_verified
2026-09-14,20260914_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,85,68,,EVENT,89,95,98,84,86,95,manage_existing_sell_until_156.20_156.40_or_BOJ_repricing_reversal,USDJPY_152.89_153.48_155_156.2_Fed_BOJ_1d_3d,verified
2026-09-14,20260914_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,72,82,,EVENT,87,90,97,70,79,92,ES_roll_and_Monday_reopen_price_discovery_required,ESU26_7659.5_ESZ26_7727.25_WTI_US10Y_1d_3d,partially_verified
2026-09-14,20260914_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,83,78,,EVENT,90,93,98,81,83,94,manage_existing_NQU26_sell_until_29620_or_macro_invalidation,NQU26_28750_29387_29620_NQZ26_roll_WTI_US10Y_1d_3d,partially_verified
2026-09-14,20260914_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,61,84,,EVENT,87,90,95,58,72,90,Fed_repricing_break_below_98.7_or_above_99.5_required,DXY_98.7_99.10_99.5_US10Y_USDJPY_Fed_1d_3d,partially_verified
2026-09-14,20260914_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,91,86,,EVENT,99,98,99,89,92,99,sustained_break_above_5.00_or_reversal_below_4.85_required,US10Y_4.85_4.979_5.00_WTI_NQ_Fed_1d_3d,partially_verified
2026-09-14,20260914_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,63,84,,EVENT,78,84,95,62,72,84,Monday_reopen_reclaim_above_18_or_hold_below_15_required,VIX_15_15.84_18_ES_NQ_WTI_1d_3d,partially_verified
```

```json
[
  {"date":"2026-09-14","signal_id":"20260914_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":66,"no_trade_score":83,"risk_pct":null,"regime":"EVENT","ems":92,"ffs":93,"cds":98,"ias":62,"cbs":76,"mes":90,"invalidation":"GCZ26_reopen_reaction_to_pipeline_shock_and_US10Y_5pct_required","verification_target":"GCZ26_4333_4408.9_4445_US10Y_WTI_Fed_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-14","signal_id":"20260914_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":80,"no_trade_score":67,"risk_pct":null,"regime":"MIXED","ems":79,"ffs":89,"cds":94,"ias":77,"cbs":80,"mes":72,"invalidation":"manage_existing_20260912_sell_until_80850_or_ETF_CME_reversal","verification_target":"BTC_76450_77408_79500_80850_ETF_CME_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-14","signal_id":"20260914_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":75,"no_trade_score":68,"risk_pct":null,"regime":"MIXED","ems":75,"ffs":88,"cds":92,"ias":74,"cbs":78,"mes":74,"invalidation":"ETH_2600_hold_with_reconciled_ETF_flow_and_BTC_stability_required","verification_target":"ETH_2480_2514_2600_ETF_ETHBTC_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-14","signal_id":"20260914_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":96,"no_trade_score":94,"risk_pct":null,"regime":"EVENT","ems":98,"ffs":99,"cds":99,"ias":93,"cbs":95,"mes":98,"invalidation":"fresh_Monday_price_and_EastWest_pipeline_status_required_before_new_entry","verification_target":"WTI_98.48_100.05_104.46_EastWest_Hormuz_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-14","signal_id":"20260914_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":85,"no_trade_score":68,"risk_pct":null,"regime":"EVENT","ems":89,"ffs":95,"cds":98,"ias":84,"cbs":86,"mes":95,"invalidation":"manage_existing_sell_until_156.20_156.40_or_BOJ_repricing_reversal","verification_target":"USDJPY_152.89_153.48_155_156.2_Fed_BOJ_1d_3d","verified_status":"verified"},
  {"date":"2026-09-14","signal_id":"20260914_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":72,"no_trade_score":82,"risk_pct":null,"regime":"EVENT","ems":87,"ffs":90,"cds":97,"ias":70,"cbs":79,"mes":92,"invalidation":"ES_roll_and_Monday_reopen_price_discovery_required","verification_target":"ESU26_7659.5_ESZ26_7727.25_WTI_US10Y_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-14","signal_id":"20260914_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":83,"no_trade_score":78,"risk_pct":null,"regime":"EVENT","ems":90,"ffs":93,"cds":98,"ias":81,"cbs":83,"mes":94,"invalidation":"manage_existing_NQU26_sell_until_29620_or_macro_invalidation","verification_target":"NQU26_28750_29387_29620_NQZ26_roll_WTI_US10Y_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-14","signal_id":"20260914_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":61,"no_trade_score":84,"risk_pct":null,"regime":"EVENT","ems":87,"ffs":90,"cds":95,"ias":58,"cbs":72,"mes":90,"invalidation":"Fed_repricing_break_below_98.7_or_above_99.5_required","verification_target":"DXY_98.7_99.10_99.5_US10Y_USDJPY_Fed_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-14","signal_id":"20260914_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":91,"no_trade_score":86,"risk_pct":null,"regime":"EVENT","ems":99,"ffs":98,"cds":99,"ias":89,"cbs":92,"mes":99,"invalidation":"sustained_break_above_5.00_or_reversal_below_4.85_required","verification_target":"US10Y_4.85_4.979_5.00_WTI_NQ_Fed_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-14","signal_id":"20260914_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":63,"no_trade_score":84,"risk_pct":null,"regime":"EVENT","ems":78,"ffs":84,"cds":95,"ias":62,"cbs":72,"mes":84,"invalidation":"Monday_reopen_reclaim_above_18_or_hold_below_15_required","verification_target":"VIX_15_15.84_18_ES_NQ_WTI_1d_3d","verified_status":"partially_verified"}
]
```

今日のポイントは**「新しいデータを取りに行ったが、CME週明け開始1分後なので価格の遅延配信がまだ追いついていない」ことを、無理に推測で埋めなかったこと**です。USDJPYとCryptoには新値がありますが、WTI/NQの既存invalidationについては現在値を確認できないため`unknown`にしました。方向面ではサウジ供給網の悪化でWTI強気材料がさらに増していますが、新規BUYは価格形成確認後でなければTSOルール違反です。
