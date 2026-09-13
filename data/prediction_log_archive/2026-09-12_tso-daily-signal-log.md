<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-12 07:00 JST -->
<!-- transport: DOM innerText -> Blob download -> tools/archive_gpt_prose.py -->
<!-- archived_at: 2026-09-13T09:02:19Z / chars: 15197 / 値は無修正 -->

TSO Daily Signal Log v2
TSO Daily Signal Log v2 — 2026-09-12

使用モデル：GPT-5.6 Sol
本日の市場の主役：WTI
GOLD基準限月：COMEX 2026年12月限（GCZ26）
crypto_grounds: etf=有, cme=有
expected_r_basis: subjective — 本日のBTC SELLは、週末の未約定確率、中東ヘッドラインによる急反転、5営業日時間決済、価格が先に走った場合のNO_CHASEを織り込み、単純なTP1/SL二点分布より低く評価します。

invalidation_check: 20260904_WTI_BUY_PULLBACK=not_fired, 20260905_WTI_BUY_PULLBACK=not_fired, 20260906_WTI_BUY_PULLBACK=not_fired, 20260907_WTI_BUY_PULLBACK=not_fired, 20260908_WTI_BUY_PULLBACK=not_fired, 20260908_USDJPY_SELL_PULLBACK=not_fired, 20260909_WTI_BUY_PULLBACK=not_fired, 20260909_USDJPY_SELL_PULLBACK=not_fired, 20260911_NASDAQ_SELL_PULLBACK=not_fired

9/3起点の方向あり判断は9/11で5営業日窓を終えたため本日から外しています。9/4〜9/7はLabor Dayを営業日に数えないため、まだ窓内です。

9/11のNQ SELLについては、NQU26が高値29500.25、終盤29420.75前後で、SL 29620には届いていません。US10Yも4.80%未満へ低下せず、WTIも99ドル台ではなく100.05ドルで清算したため、マクロ側の複合invalidationも未発動です。
Investing.com Italia
+2
Reuters
+2

1. 本日の結論

A級：0件

B級：BTC SELL / PULLBACK 1件

B+：0件

NO_TRADE：GOLD、ETH、WTI、USDJPY、SPX、NASDAQ、DXY、US10Y、VIX

昨日のCPIは前月比**+0.4%、Fedの9月利上げ確率は約87〜90%まで上昇しました。それでも米株は反発し、S&P500 +0.86%、Nasdaq +0.96%。一方、10年債利回りは5%近辺まで上昇した後にやや低下し、WTIも102.48から100.05**へ反落しました。つまり「インフレ悪化＝即全面RISK_OFF」にはなっていません。
Reuters
+3
Reuters
+3
Reuters
+3

その中で相対的に弱いのがBTCです。米スポットBTC ETFは9/8、9/9、9/10と3営業日連続流出で、9/10は約**-282.7Mドル**。CME BTC先物の9/11価格も約77.3kで弱く、週末現物は概ね78k台です。ETF需要とCMEの両方が短期的に逆風なので、本日はBTCだけ戻り売りをB級で新規発行します。
CoinGecko
+3
Gokhshtein
+3
SmallDrift
+3

2. 前回判断の簡易検証

前日の新規方向ありは、

20260911_NASDAQ_SELL_PULLBACK

でした。

設定は、

Entry 29300–29400
SL 29620
TP1 28750
TP2 28350

9/11のNQU26は安値29040.50、高値29500.25、終盤29420.75前後。したがってEntry帯には到達していますが、その後上方向へ振れ、SL手前まで戻しました。
Investing.com Italia

結果は現時点で、

ENTRY_REACHED / TP_NOT_REACHED / SL_NOT_REACHED / UNDER_PRESSURE

です。

CPI後に米株現物が大きく反発したため、昨日のSELLシナリオは方向面でやや悪化しました。ただしNQU26 29620を越えていないため、ルール上はまだnot_firedです。

WTI BUY群については、9/11にWTIが102ドル台から100.05へ反落しました。ただし下落理由はホルムズ正常化ではなく、一時的な外交協議報道によるリスクプレミアム縮小で、実際の供給障害・船舶攻撃・Saudi供給低下は残っています。したがって既存の供給正常化系invalidationは発動していません。
Reuters

USDJPYは9/11に概ね154.3〜154.4円。9/8の156.40、9/9の156.20という失効水準には達していません。BOJは9/17–18会合で1.25%への25bp利上げが有力とReutersが報じており、円高仮説の政策根拠も残っています。
Myfxbook.com
+1

3. 市場全体の前提

総合regimeはEVENTです。

8月CPIは前月比+0.4%。コアCPIも市場予想を上回り、Fedの9月利上げ確率は約85〜90%へ上昇しました。
Reuters
+1

一方、10年債利回りは一時**約5%**まで上昇した後、Reuters基準で4.93%前後まで反落。別系列の日次データでは4.97%近辺なので、US10Yは今日はpartially_verifiedとします。どちらにせよ4.8%台前半へは戻っていません。
Reuters
+1

WTIは100.05ドル。前日の102.48から反落しましたが、週間では8%以上上昇。Saudi供給は8月に6mbpdまで低下し、Hormuz通航も大幅に減少しています。
Reuters

Gold 12月限の基準値は4408.90ドル。強いCPIにもかかわらず金は1%以上戻しており、4300〜4400台で短期的な底固めが出始めています。
Reuters

DXYは約99.06、USDJPYは約154.3〜154.4。米金利が5%近辺でもドル全面高にはなっておらず、特に円はBOJ引き締め観測で独自に強い状態です。
Investing.com Canada
+2
Reuters
+2

VIXはCboe公式遅延値で15.59まで低下。前日17.84から大きく下がっており、株式市場は少なくとも金曜時点ではパニック状態ではありません。
Cboe Global Markets

4. 10資産別判断
資産	判定	基準・判断
GOLD	NO_TRADE	GCZ26 4408.9。金利高と底固めが衝突
BTC	B SELL	79.2–79.8kへの戻り限定
ETH	NO_TRADE	約2.44–2.48k、独立edge不足
WTI	NO_TRADE	100.05。既存BUY管理のみ
USDJPY	NO_TRADE	約154.3、既存SELL管理
SPX	NO_TRADE	ESU26約7615、金曜反発で方向不純
NASDAQ	NO_TRADE	既存SELL継続、追加発行なし
DXY	NO_TRADE	約99.06、Fed/BOJの綱引き
US10Y	NO_TRADE	約4.93–4.97%、5%攻防
VIX	NO_TRADE	15.59、警戒後退

ESU26は9/11遅延値で約7614.75。NQU26は約29420.75。現物S&P500やNasdaq Compositeを先物行へ代用していません。
Investing.com UK
+1

Cryptoは週末のWebスナップショットでBTC約78.3k前後、ETH約2.45k前後。ETFは9/11分を確定値として取得できていないため、ETF根拠は最新確認可能な9/10分までです。CME BTCは9/11データを取得できています。
CoinGecko
+2
CoinGecko
+2

5. A級候補

なし。

BTC SELLは、

CBS 79
EMS 76
RR 2.26

で形は悪くありません。

ただし、

expected_r 0.38 < 0.45
MAE想定 0.30R > 0.25R

なのでA級条件を満たしません。

また土日の中東ヘッドラインでBTCが突然リスクオン・オフへ振れる可能性があり、通常営業日のセットアップよりギャップリスクが高いです。

6. B級監視候補
BTC — B SELL / PULLBACK

参照：BTC/USD現物

週末参考：約78.3k。CME Sep-26は9/11に約77.3k。米ETFは9/10まで3営業日連続流出です。
CoinGecko
+2
Investing.com Canada
+2

Entry：79200–79800
SL：80850
TP1：76450
TP2：74800

Entry中点：

79500

SL距離：

80850 − 79500 = 1350

TP1距離：

79500 − 76450 = 3050

したがって、

RR = 3050 / 1350 = 2.26

再計算一致です。

win_prob：0.58
較正後参考：0.61
expected_r：0.38 subjective
MAE想定：0.30R
risk_pct：0.25%
CBS：79
EMS：76
MES：74

単純two_pointでは、

0.58 × 2.26 − 0.42 = 0.89R

ですが、これを採用しません。

79.2–79.8kまで戻らない未約定、週末中東ヘッドライン、ETF 9/11確定値未取得、5営業日以内の早期撤退を織り込み0.38Rとします。

執行は、

78k台前半からの成行SELL：しない
79.2–79.8k：戻り売り監視
80.85k超：invalidation
76.45k：TP1参考

です。

数値上はB+条件のCBS/EMS/RR/win_probを満たしますが、XM最小ロット時の実損を今日の外部データから確定できないためB+にはしません。最小ロットでSL損失が3000円を超える場合は、シグナル自体はBでも実取引NO_TRADEです。

7. 触らない資産

WTIは最重要です。102.48から100.05へ下がりましたが、これは供給構造が正常化したとはまだ言えません。外交協議報道だけで100ドルまで戻るということは、今後もヘッドライン一つで数ドル動く状態です。新規BUYもSELLも避けます。
Reuters

NASDAQも追加SELLしません。昨日のB SELLはEntry帯に到達した後、金曜の株式反発によって逆行しています。新しいSELLを重ねると同一仮説の重複リスクになります。

GOLDは金利がほぼ5%なのに4400ドル台へ戻した点が重要です。ここでSELLすると「高金利だから下がる」という単一ファクターに依存しすぎます。
Reuters
+1

USDJPYも既存SELLがあるので追加発行しません。FedとBOJがともに来週利上げ方向という珍しい局面で、154円台は金利差だけでは説明しにくくなっています。
Reuters
+1

8. 後日検証ポイント

最優先は昨日のNASDAQ SELLです。

NQU26はEntry 29300–29400へ入った後、29500近くまで反発しました。月曜以降、

29620超 → fired

なら、CPI後の株反発を過小評価したシグナルだったと判定できます。

逆に、

US10Y高止まり + NQ 28750

なら、金曜反発は単なる戻りだったと評価します。

次がWTIです。

WTI <100 + Hormuz外交合意進展

なら、既存BUY群のマクロinvalidationを再評価します。

一方、

100維持 → 105再突破

なら、供給ショックが新しい価格帯へ定着した可能性が高まります。

BTCについては、

ETF再流入 + BTC >80850

なら本日のSELLはfired。

ETF流出継続 + BTC <76450

なら、9月初旬の大規模ETF流入後に需給がdistributionへ移行した仮説を支持します。

来週はFedが9/15–16、BOJが9/17–18。Fedは約9割の利上げ確率、BOJも25bp利上げが有力なので、US10YとUSDJPYが同方向に動くとは限らない週になります。
Reuters
+1

9. Obsidian保存用 Observation Draft
Markdown
# 2026-09-12 BTC Weakness vs Friday Equity Rebound

Model:
GPT-5.6 Sol

Market protagonist:
WTI

Gold reference:
COMEX Dec-2026 / GCZ26

crypto_grounds:
etf=有
cme=有

ETF freshness:
latest confirmed = Sep10
BTC ETF = about -282.7m
3 consecutive outflow sessions

CME freshness:
Sep11 BTC futures available
~77.3k

expected_r_basis:
subjective

Reason:
weekend headline risk
non-fill probability
ETF Sep11 not confirmed
5-business-day time exit

## Regime
EVENT

## Market

WTI:
100.05 settle

Gold Dec:
4408.90

US10Y:
~4.93-4.97
near 5%

DXY:
~99.06

USDJPY:
~154.3-154.4

VIX:
15.59 Cboe delayed

ESU26:
~7615

NQU26:
~29421
Sep11 high ~29500
low ~29040

BTC spot:
~78.3k

ETH:
~2.45k

## Outstanding invalidation

20260904_WTI_BUY_PULLBACK=not_fired
20260905_WTI_BUY_PULLBACK=not_fired
20260906_WTI_BUY_PULLBACK=not_fired
20260907_WTI_BUY_PULLBACK=not_fired
20260908_WTI_BUY_PULLBACK=not_fired
20260908_USDJPY_SELL_PULLBACK=not_fired
20260909_WTI_BUY_PULLBACK=not_fired
20260909_USDJPY_SELL_PULLBACK=not_fired
20260911_NASDAQ_SELL_PULLBACK=not_fired

## Previous signal

20260911_NASDAQ_SELL_PULLBACK

Entry:
29300-29400

Entry reached:
YES

SL 29620:
NOT reached

TP1 28750:
NOT confirmed after entry

Status:
ALIVE / UNDER_PRESSURE

## Today

A:
NONE

B:
BTC SELL PULLBACK

BTC:
Entry 79200-79800
SL 80850
TP1 76450
TP2 74800
RR 2.26
win_prob 0.58
expected_r 0.38 subjective
MAE 0.30R
risk_pct 0.25

B+:
NONE
minimum-lot loss not verified

NO_TRADE:
GOLD
ETH
WTI
USDJPY
SPX
NASDAQ
DXY
US10Y
VIX

## Research

Friday divergence:

hot CPI
+ US10Y near 5%
but
SPX / Nasdaq rally
VIX falls

while:

BTC ETF outflows
+ weak CME BTC
+ spot below 80k

Potential crypto relative weakness.

#TSO #BTC #NASDAQ #WTI #US10Y #USDJPY
10. TSO_LOG CSV / JSON
csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-12,20260912_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,62,80,,EVENT,90,90,97,60,74,88,GCZ26_break_below_4350_or_reclaim_above_4450_with_US10Y_confirmation_required,GCZ26_4350_4409_4450_US10Y_DXY_1d_3d,verified
2026-09-12,20260912_BTC_SELL_PULLBACK,BTC,SELL,B,PULLBACK,79200,79800,80850,76450,74800,2.26,0.58,0.38,98,82,44,0.25,MIXED,76,88,92,80,79,74,BTC_spot_above_80850_or_fresh_ETF_reinflow_with_CME_reclaim,BTC_76450_79500_80850_ETF_CME_1d_3d_5d,partially_verified
2026-09-12,20260912_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,97,61,77,,MIXED,70,84,88,59,69,61,BTC_direction_and_ETH_2500_reclaim_or_2400_break_required,ETH_2400_2450_2500_BTC_ETF_1d_3d,partially_verified
2026-09-12,20260912_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,88,84,,EVENT,94,97,99,84,89,95,verified_Hormuz_deescalation_or_clean_reclaim_above_103_required_before_new_signal,WTI_98_100.05_103_Hormuz_supply_1d_3d,verified
2026-09-12,20260912_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,80,69,,EVENT,86,93,98,79,82,92,manage_existing_sell_until_156.20_156.40_or_BOJ_repricing_reversal,USDJPY_153_154.4_156.2_BOJ_Fed_1d_3d,verified
2026-09-12,20260912_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,66,78,,MIXED,84,87,95,65,76,88,ESU26_breakout_above_7665_or_failure_below_7585_required,ESU26_7585_7615_7665_US10Y_VIX_1d_3d,partially_verified
2026-09-12,20260912_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,78,70,,MIXED,88,91,98,76,80,92,existing_20260911_sell_managed_until_NQU26_29620_or_macro_invalidation,NQU26_28750_29421_29620_US10Y_WTI_1d_3d,partially_verified
2026-09-12,20260912_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,55,82,,EVENT,86,88,94,52,69,88,clear_break_below_98.7_or_above_99.5_required,DXY_98.7_99.06_99.5_Fed_BOJ_1d_3d,verified
2026-09-12,20260912_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,85,76,,EVENT,98,97,99,83,88,99,sustained_break_above_5.00_or_reversal_below_4.85_required,US10Y_4.85_4.95_5.00_WTI_NQ_GOLD_1d_3d,partially_verified
2026-09-12,20260912_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,58,83,,MIXED,74,78,92,56,69,78,VIX_reclaim_above_18_or_hold_below_15_required,VIX_15_15.59_18_ES_NQ_1d_3d,verified
JSON
[
  {"date":"2026-09-12","signal_id":"20260912_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":62,"no_trade_score":80,"risk_pct":null,"regime":"EVENT","ems":90,"ffs":90,"cds":97,"ias":60,"cbs":74,"mes":88,"invalidation":"GCZ26_break_below_4350_or_reclaim_above_4450_with_US10Y_confirmation_required","verification_target":"GCZ26_4350_4409_4450_US10Y_DXY_1d_3d","verified_status":"verified"},
  {"date":"2026-09-12","signal_id":"20260912_BTC_SELL_PULLBACK","asset":"BTC","side":"SELL","rank":"B","type":"PULLBACK","entry_low":79200,"entry_high":79800,"sl":80850,"tp1":76450,"tp2":74800,"rr":2.26,"win_prob":0.58,"expected_r":0.38,"tq_score":98,"opp_score":82,"no_trade_score":44,"risk_pct":0.25,"regime":"MIXED","ems":76,"ffs":88,"cds":92,"ias":80,"cbs":79,"mes":74,"invalidation":"BTC_spot_above_80850_or_fresh_ETF_reinflow_with_CME_reclaim","verification_target":"BTC_76450_79500_80850_ETF_CME_1d_3d_5d","verified_status":"partially_verified"},
  {"date":"2026-09-12","signal_id":"20260912_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":97,"opp_score":61,"no_trade_score":77,"risk_pct":null,"regime":"MIXED","ems":70,"ffs":84,"cds":88,"ias":59,"cbs":69,"mes":61,"invalidation":"BTC_direction_and_ETH_2500_reclaim_or_2400_break_required","verification_target":"ETH_2400_2450_2500_BTC_ETF_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-12","signal_id":"20260912_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":88,"no_trade_score":84,"risk_pct":null,"regime":"EVENT","ems":94,"ffs":97,"cds":99,"ias":84,"cbs":89,"mes":95,"invalidation":"verified_Hormuz_deescalation_or_clean_reclaim_above_103_required_before_new_signal","verification_target":"WTI_98_100.05_103_Hormuz_supply_1d_3d","verified_status":"verified"},
  {"date":"2026-09-12","signal_id":"20260912_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":80,"no_trade_score":69,"risk_pct":null,"regime":"EVENT","ems":86,"ffs":93,"cds":98,"ias":79,"cbs":82,"mes":92,"invalidation":"manage_existing_sell_until_156.20_156.40_or_BOJ_repricing_reversal","verification_target":"USDJPY_153_154.4_156.2_BOJ_Fed_1d_3d","verified_status":"verified"},
  {"date":"2026-09-12","signal_id":"20260912_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":66,"no_trade_score":78,"risk_pct":null,"regime":"MIXED","ems":84,"ffs":87,"cds":95,"ias":65,"cbs":76,"mes":88,"invalidation":"ESU26_breakout_above_7665_or_failure_below_7585_required","verification_target":"ESU26_7585_7615_7665_US10Y_VIX_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-12","signal_id":"20260912_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":78,"no_trade_score":70,"risk_pct":null,"regime":"MIXED","ems":88,"ffs":91,"cds":98,"ias":76,"cbs":80,"mes":92,"invalidation":"existing_20260911_sell_managed_until_NQU26_29620_or_macro_invalidation","verification_target":"NQU26_28750_29421_29620_US10Y_WTI_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-12","signal_id":"20260912_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":55,"no_trade_score":82,"risk_pct":null,"regime":"EVENT","ems":86,"ffs":88,"cds":94,"ias":52,"cbs":69,"mes":88,"invalidation":"clear_break_below_98.7_or_above_99.5_required","verification_target":"DXY_98.7_99.06_99.5_Fed_BOJ_1d_3d","verified_status":"verified"},
  {"date":"2026-09-12","signal_id":"20260912_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":85,"no_trade_score":76,"risk_pct":null,"regime":"EVENT","ems":98,"ffs":97,"cds":99,"ias":83,"cbs":88,"mes":99,"invalidation":"sustained_break_above_5.00_or_reversal_below_4.85_required","verification_target":"US10Y_4.85_4.95_5.00_WTI_NQ_GOLD_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-12","signal_id":"20260912_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":58,"no_trade_score":83,"risk_pct":null,"regime":"MIXED","ems":74,"ffs":78,"cds":92,"ias":56,"cbs":69,"mes":78,"invalidation":"VIX_reclaim_above_18_or_hold_below_15_required","verification_target":"VIX_15_15.59_18_ES_NQ_1d_3d","verified_status":"verified"}
]

本日の新規判断はBTCの戻り売り1本のみです。重要なのは78k台から追わず、ETF流出・CME弱含みが続いたまま79.2–79.8kへ戻った場合だけ売りを検討することです。NASDAQは昨日のSELLがEntry到達後に逆行しているため、新規を重ねず既存シグナルの29620だけを監視します。
