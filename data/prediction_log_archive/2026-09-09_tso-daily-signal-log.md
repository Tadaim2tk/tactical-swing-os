<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-09 07:00 JST -->
<!-- transport: DOM innerText -> Blob download -> tools/archive_gpt_prose.py -->
<!-- archived_at: 2026-09-08T22:34:36Z / chars: 16278 / 値は無修正 -->

TSO Daily Signal Log v2
TSO Daily Signal Log v2 — 2026-09-09

使用モデル：GPT-5.6 Sol
本日の市場の主役：WTI
GOLD基準限月：COMEX 2026年12月限
crypto_grounds: etf=有, cme=有
expected_r_basis: subjective
Entry未到達、成行追随禁止、PPI/CPI前の早期撤退、5営業日の時間決済を織り込むため、単純な win_prob*rr-(1-win_prob) より低く評価します。

invalidation_check: 20260903_WTI_BUY_PULLBACK=not_fired, 20260904_WTI_BUY_PULLBACK=not_fired, 20260904_NASDAQ_BUY_PULLBACK=not_fired, 20260905_WTI_BUY_PULLBACK=not_fired, 20260906_WTI_BUY_PULLBACK=not_fired, 20260907_WTI_BUY_PULLBACK=not_fired, 20260908_WTI_BUY_PULLBACK=not_fired, 20260908_USDJPY_SELL_PULLBACK=not_fired

基準は9月8日米国市場終了まで＋9月9日06:58 JST時点で取得できた最新情報です。WTIは9月8日に93.03ドルで清算し、6月以来の高値圏。米10年債利回りは4.791%、DXYは98.80、USDJPYは154.13、VIXは15.29。BTCは約78.3k、ETHは約2.49kです。
CoinCodex
+6
Reuters
+6
Investing.com
+6

BTC/ETHについては、ETFは9月4日までの完成データを取得でき、BTC +174.6Mドル、ETH +25.9Mドル。9月8日欄は現時点で未反映のため0.0表示を確定フローとは扱いません。CME Bitcoin futuresも取得できましたが、ページ上の最新trade dateは9月4日で、BTC先物OI 20,906、Micro BTC OI 37,458と鮮度が不足しています。したがって etf=有, cme=有 ですが、両方とも今日の価格判断への寄与は限定的です。
Farside Investors
+2
Farside Investors
+2

1. 本日の結論

A級：0件

B級：WTI BUY、USDJPY SELL

このうちUSDJPYはB+観察候補です。WTIは方向信頼度こそ高いものの、9月8日に94ドル台まで吹き上がり、供給ショック直後の過熱状態なのでB止まりとします。

NO_TRADE：GOLD、BTC、ETH、SPX、NASDAQ、DXY、US10Y、VIX

昨日の市場で最も重要だったのは、WTI上昇が実際に金利・株へ伝播したことです。Houthiによるサウジのエネルギー施設攻撃を受けWTIは93.03ドルへ上昇し、米10年金利は一時4.814%。S&P500は**-0.58%、Nasdaq Compositeは-0.32%**でした。一方、VIXは15台にとどまり、全面的なパニックにはなっていません。
Investing.com
+3
Reuters
+3
The Wall Street Journal
+3

したがって、

WTI↑ → US10Y↑ → 株に逆風

というこれまでの仮説は再び支持されました。

ただしNASDAQは崩れてはいません。NQ Sep-26はデータ提供元間で9月8日終値に29,508～29,687程度の差があり、参照系列の厳密な終値を完全には確定できないため、本日はpartially_verifiedとして方向を出しません。NASDAQ総合指数をNQ行の代用には使用していません。
Investing.com
+1

2. 前回判断の簡易検証
20260908_WTI_BUY_PULLBACK → かなり良好

前回は、

Entry 91.20–92.00
SL 89.50
TP1 97.00

でした。

9月8日のWTI日中安値はデータ提供元で91.83、高値は94.73。Reuters清算値は93.03です。つまりEntry帯には実際に入っており、その後2ドル以上上昇しました。
Investing.com Nigeria
+1

したがって前回は、

ENTRY_REACHED / POSITIVE_MFE / TP1_NOT_REACHED

と評価できます。

SL89.50は割れず、ホルムズ・中東供給リスクも正常化していません。

invalidation = not_fired

です。

これは今回かなり良い教師データです。方向だけ当たりではなく、押し目Entryまで実際に戻ってから上昇しました。

20260908_USDJPY_SELL_PULLBACK → 方向成功、未約定

前回：

Entry 155.00–155.60
SL 156.40
TP1 152.80

9月8日のUSDJPYは高値154.42、安値152.89、終値154.13。Entry155円台には戻りませんでした。
Investing.com

したがって、

THESIS_SUCCESS / ORDER_NOT_FILLED

です。

ここは追わなかったことが重要です。一時152.89まで円高が進んでおり、154円以下で新規SELLしていたらリスクリワードが急速に悪化していました。

156.40も到達していないため、

invalidation = not_fired

です。

過去の未決着シグナル

9月3日以降のWTI BUY群は、いずれも88～90ドル台のinvalidationを割らず、TP1が95.5～97ドルに集中しています。9月8日の高値は94.73なので、まだTP到達前・invalidation未発動として追跡継続です。
Investing.com Nigeria

9月4日のNASDAQ BUYは、

Entry 29350–29500 / SL29100 / TP1 30150
invalidation = NQ<29100 または US10Y>4.82

でした。

9月8日のNQは取得可能な系列で安値約29400台、US10Y高値は4.814%。したがってぎりぎりですがinvalidation未発動です。
Investing.com
+1

この古いNASDAQ BUYはまだ5営業日の検証期間内なので残します。

3. 市場全体の前提

本日の総合regimeはEVENTです。

現在の市場には、相反する3本の力があります。

第一は原油です。Houthiによるサウジのエネルギー施設攻撃で一部施設の稼働が停止し、WTIは93.03ドル、Brentは97.92ドルまで上昇しました。Reutersによれば中東産原油輸出は戦争前の約18mbpdから約11mbpdまで減少しています。一方で代替ルートや非OPEC増産が効いているため、100ドルを明確に超えてはいません。
Reuters
+1

第二は金利です。米10年金利は4.79%前後で、9月8日には4.814%まで上昇。原油高と強い雇用統計がFedの利上げ観測を約60%まで押し上げています。
Investing.com
+1

第三が円です。通常なら米金利高はUSDJPYを押し上げますが、今回は逆で、円は一時152.89まで上昇。BOJの次回25bp利上げ確率はReuters報道で約**97%**まで上がっており、キャリートレードの巻き戻しが米金利要因を上回っています。
Reuters
+1

このため市場構造は、

WTI：上方向
US10Y：上方向圧力
NASDAQ：耐えているが追い買い不適
GOLD：地政学より金利が優勢
JPY：独自に強い

と判断します。

なお次の大イベントは、BLS公式日程でPPIが9月10日08:30 ET、CPIが9月11日08:30 ET。日本時間はいずれも21:30です。
Bureau of Labor Statistics
+1

4. 10資産別判断
資産	判定	短期判断
GOLD	NO_TRADE	戦争でも上がれず、金利が支配
BTC	NO_TRADE	ETFはプラスだが78k台、CME根拠が古い
ETH	NO_TRADE	BTCより相対強いが独立BUYには不足
WTI	B BUY	91.8–92.5への押し限定
USDJPY	B+ SELL	154.8–155.4への戻り限定
SPX	NO_TRADE	原油・金利逆風＋PPI/CPI前
NASDAQ	NO_TRADE	古いBUY仮説は生存、新規は待つ
DXY	NO_TRADE	円高で98.8、方向の純度不足
US10Y	NO_TRADE	CPI/PPIで直接再価格形成
VIX	NO_TRADE	15台で警戒は限定的
5. A級候補

なし。

WTIはCBS/EMSだけならA級水準ですが、

expected_r 0.42 < 0.45
MAE想定 0.31R > 0.25R

なので不合格。

USDJPYも、

CBS79 / EMS75

と良好ですが、

expected_r 0.38
MAE 0.29R

なのでAにはしません。

PPI・CPI直前であることもA級を抑える理由です。

6. B級監視候補
WTI — B BUY / PULLBACK ONLY

最新確定基準：93.03。9月8日は一時94.73まで上昇しています。
Reuters
+1

Entry 91.80–92.50
SL 90.20
TP1 97.00
TP2 100.00

Entry中点 = 92.15
SL距離 = 92.15 - 90.20 = 1.95
TP1距離 = 97.00 - 92.15 = 4.85

RR = 4.85 / 1.95 = 2.49

再計算一致。

win_prob 0.59
較正参考 0.62
expected_r 0.42 subjective
MAE想定 0.31R
CBS 86
EMS 81
risk_pct 0.25%

二点分布なら 0.59×2.49 - 0.41 ≒ 1.06R ですが、これは現実の運用期待値として過大です。Entryへ再び押す確率、95ドル近辺での早期利確、PPI/CPI前の撤退、急な停戦・供給正常化ニュースを含めて0.42Rとします。

執行は、

91.8–92.5：BUY候補
92.5–93.5：5分足で押し止まり確認必須
94以上：NO_CHASE

です。

方向予測が当たり続けているからといってEntryを94へ引き上げません。

USDJPY — B+観察候補 / SELL PULLBACK

最新終値参考：154.13。9月8日安値は152.89です。
Investing.com
+1

Entry 154.80–155.40
SL 156.20
TP1 152.50
TP2 151.20

Entry中点 = 155.10
SL距離 = 156.20 - 155.10 = 1.10
TP1距離 = 155.10 - 152.50 = 2.60

RR = 2.60 / 1.10 = 2.36

再計算一致。

win_prob 0.59
較正参考 0.62
expected_r 0.38 subjective
MAE想定 0.29R
CBS 79
EMS 75
risk_pct 0.25%

0.01 lot＝1000USDの一般的なFX契約仕様を前提にすると、1.10円のSL幅は概算約1100円の損失です。したがってXMで0.01 lotが実際に選択可能なら、3000円制約内としてB+数値条件を満たします。口座上の最小ロット・契約仕様は発注画面で最終確認が必要です。

ただし現在154円台なので、今SELLする判断ではありません。

155円近辺まで戻れば売りを検討し、152円台へそのまま走れば

THESIS_SUCCESS / ORDER_NOT_FILLED

で終了して構いません。

7. 触らない資産

BTCは現時点で最も判断が難しい資産です。9月3日+730.8M、9月4日+174.6MとETF需要はかなり強かった一方、BTC価格は9月8日に78.3k前後まで下がっています。ETF需要に価格が応えていません。
Farside Investors
+1

これは現在、

FLOW bullish / PRICE bearish-neutral

です。

CMEの最新取得データも9月4日までなので、MESを58に留め、NO_TRADEとします。

ETHは約2490ドルで、ETH/BTC比率は9月初旬から上昇しています。9月8日のETH/BTCは約0.0318で、BTCより相対的には強いです。
CoinMarketCap
+1

ただしBTCが78kへ落ちている環境でETHだけ独立BUYするほどのedgeではありません。

GOLDも重要です。Reutersによる9月8日のCOMEX12月限は約4430.10ドルまで下落しました。原油高・地政学悪化にもかかわらず金が弱いので、依然として金利/Fed > safe havenです。
Reuters

NASDAQは売りません。原油高・金利上昇下でもNasdaq Compositeの下落は-0.32%程度に留まり、半導体の一部はむしろ強かったためです。
Reuters

しかし新規BUYもPPI/CPI前には出しません。

8. 後日検証ポイント

今日は4つに絞ります。

まずWTI。過去のBUY群のTP1は95.5～97ドルに集中しています。9月8日の高値94.73はその直前です。95.5到達なら9月3日・4日シグナルから順次決着として記録できます。

次にNASDAQ。9月4日のBUYシグナルのinvalidation条件はNQ<29100 or US10Y>4.82。US10Yは9月8日に4.814まで来ています。あと数bpです。4.82を明確に突破した時に、NQが同時に崩れるかが非常に価値のある検証になります。
Investing.com

第三にUSDJPY。米10年金利4.79%でもUSDJPYが155を回復できないなら、BOJ・キャリー巻き戻しという円固有要因の支配をさらに強く認定します。

最後にBTC。ETFの9月8日確定フローが更新された際、

ETF流入 + BTC<78k

ならdistribution/潜在供給圧力を重くする。

逆に、

ETF流入 + BTC>80k回復

なら再度BUY監視へ戻します。

9. Obsidian保存用 Observation Draft
Markdown
# 2026-09-09 Oil Shock Reaches Rates, Yen Decouples

Model:
GPT-5.6 Sol

Market protagonist:
WTI

Gold reference:
COMEX Dec-2026

crypto_grounds:
etf=有
cme=有

ETF freshness:
latest completed flow = Sep 4
Sep 8 provisional row not usable yet

CME freshness:
latest accessible BTC futures trade date = Sep 4

expected_r_basis:
subjective

Reason:
non-fill probability
no-chase execution
early exit before PPI/CPI
5-business-day time exit

## Regime
EVENT

## Core market data

WTI:
93.03 settle
Sep8 high ~94.73
Sep8 low ~91.83

US10Y:
4.791 close
4.814 high

DXY:
98.80

USDJPY:
154.13
high 154.42
low 152.89

VIX:
15.29

BTC:
~78300

ETH:
~2490

Gold Dec:
~4430 Reuters late-session reference

ES Sep26:
~7698

NQ Sep26:
~29500-29700
provider discrepancy
partially_verified

## Previous signal validation

20260908_WTI_BUY_PULLBACK:
entry reached
positive MFE
TP1 not reached
invalidation not fired

20260908_USDJPY_SELL_PULLBACK:
direction correct
order not filled
invalidation not fired

## Outstanding invalidations

20260903_WTI_BUY_PULLBACK = not_fired
20260904_WTI_BUY_PULLBACK = not_fired
20260904_NASDAQ_BUY_PULLBACK = not_fired
20260905_WTI_BUY_PULLBACK = not_fired
20260906_WTI_BUY_PULLBACK = not_fired
20260907_WTI_BUY_PULLBACK = not_fired
20260908_WTI_BUY_PULLBACK = not_fired
20260908_USDJPY_SELL_PULLBACK = not_fired

## Today

A:
NONE

B:
WTI BUY PULLBACK

B+ observation:
USDJPY SELL PULLBACK

WTI:
Entry 91.80-92.50
SL 90.20
TP1 97.00
TP2 100.00
RR 2.49
win_prob 0.59
expected_r 0.42 subjective

USDJPY:
Entry 154.80-155.40
SL 156.20
TP1 152.50
TP2 151.20
RR 2.36
win_prob 0.59
expected_r 0.38 subjective

NO_TRADE:
GOLD
BTC
ETH
SPX
NASDAQ
DXY
US10Y
VIX

## Next events

Sep10:
US PPI

Sep11:
US CPI

Primary research chain:
WTI
-> inflation expectations
-> US10Y
-> NQ / Gold

Secondary chain:
BOJ repricing
-> carry unwind
-> JPY strength

#TSO #WTI #USDJPY #US10Y #NASDAQ #BTC
10. TSO_LOG CSV / JSON
csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-09,20260909_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,46,86,,EVENT,82,86,94,44,67,85,GC_Dec_4500_reclaim_with_US10Y_decline_required,GOLD_Dec_4400_4500_US10Y_DXY_PPI_CPI_1d_3d,verified
2026-09-09,20260909_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,61,78,,EVENT,68,88,90,56,68,58,80000_reclaim_with_fresh_ETF_or_CME_confirmation_required,BTC_78000_80000_82000_ETF_CME_PPI_CPI_1d_3d,partially_verified
2026-09-09,20260909_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,96,64,70,,EVENT,70,84,86,63,71,63,BTC_stabilization_and_ETH_2550_hold_required,ETH_2450_2550_ETHBTC_ETF_BTC_1d_3d,partially_verified
2026-09-09,20260909_WTI_BUY_PULLBACK,WTI,BUY,B,PULLBACK,91.80,92.50,90.20,97.00,100.00,2.49,0.59,0.42,99,90,37,0.25,EVENT,81,94,99,86,86,91,90.20_break_or_verified_Gulf_supply_deescalation,WTI_91.8_94.7_97_Hormuz_Saudi_PPI_CPI_1d_3d_5d,verified
2026-09-09,20260909_USDJPY_SELL_PULLBACK,USDJPY,SELL,B,PULLBACK,154.80,155.40,156.20,152.50,151.20,2.36,0.59,0.38,99,84,42,0.25,EVENT,75,90,95,83,79,90,156.20_break_or_BOJ_hike_repricing_reversal,USDJPY_152.9_155_156.2_BOJ_US10Y_DXY_1d_3d_5d,verified
2026-09-09,20260909_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,97,52,80,,RISK_OFF,72,80,91,51,68,79,ES_stabilization_with_US10Y_below_4.75_required,ES_7650_7750_WTI_US10Y_VIX_PPI_CPI_1d_3d,partially_verified
2026-09-09,20260909_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,94,67,73,,MIXED,76,89,91,68,75,84,NQ_below_29100_or_US10Y_above_4.82_changes_bias,NQ_29100_29750_US10Y_WTI_semis_PPI_CPI_1d_3d,partially_verified
2026-09-09,20260909_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,95,48,84,,MIXED,82,86,88,45,67,84,clear_break_below_98.5_or_above_99.5_required,DXY_98.5_99.5_US10Y_USDJPY_PPI_CPI_1d_3d,verified
2026-09-09,20260909_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,72,94,,EVENT,94,97,99,70,83,96,PPI_CPI_confirmed_break_below_4.70_or_above_4.82_required,US10Y_4.70_4.82_WTI_NQ_GOLD_PPI_CPI_1d_3d,verified
2026-09-09,20260909_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,43,85,,MIXED,70,71,91,48,67,73,VIX_break_above_17_with_equity_confirmation_required,VIX_15_17_ES_NQ_WTI_PPI_CPI_1d_3d,verified
JSON
[
  {"date":"2026-09-09","signal_id":"20260909_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":46,"no_trade_score":86,"risk_pct":null,"regime":"EVENT","ems":82,"ffs":86,"cds":94,"ias":44,"cbs":67,"mes":85,"invalidation":"GC_Dec_4500_reclaim_with_US10Y_decline_required","verification_target":"GOLD_Dec_4400_4500_US10Y_DXY_PPI_CPI_1d_3d","verified_status":"verified"},
  {"date":"2026-09-09","signal_id":"20260909_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":61,"no_trade_score":78,"risk_pct":null,"regime":"EVENT","ems":68,"ffs":88,"cds":90,"ias":56,"cbs":68,"mes":58,"invalidation":"80000_reclaim_with_fresh_ETF_or_CME_confirmation_required","verification_target":"BTC_78000_80000_82000_ETF_CME_PPI_CPI_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-09","signal_id":"20260909_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":96,"opp_score":64,"no_trade_score":70,"risk_pct":null,"regime":"EVENT","ems":70,"ffs":84,"cds":86,"ias":63,"cbs":71,"mes":63,"invalidation":"BTC_stabilization_and_ETH_2550_hold_required","verification_target":"ETH_2450_2550_ETHBTC_ETF_BTC_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-09","signal_id":"20260909_WTI_BUY_PULLBACK","asset":"WTI","side":"BUY","rank":"B","type":"PULLBACK","entry_low":91.80,"entry_high":92.50,"sl":90.20,"tp1":97.00,"tp2":100.00,"rr":2.49,"win_prob":0.59,"expected_r":0.42,"tq_score":99,"opp_score":90,"no_trade_score":37,"risk_pct":0.25,"regime":"EVENT","ems":81,"ffs":94,"cds":99,"ias":86,"cbs":86,"mes":91,"invalidation":"90.20_break_or_verified_Gulf_supply_deescalation","verification_target":"WTI_91.8_94.7_97_Hormuz_Saudi_PPI_CPI_1d_3d_5d","verified_status":"verified"},
  {"date":"2026-09-09","signal_id":"20260909_USDJPY_SELL_PULLBACK","asset":"USDJPY","side":"SELL","rank":"B","type":"PULLBACK","entry_low":154.80,"entry_high":155.40,"sl":156.20,"tp1":152.50,"tp2":151.20,"rr":2.36,"win_prob":0.59,"expected_r":0.38,"tq_score":99,"opp_score":84,"no_trade_score":42,"risk_pct":0.25,"regime":"EVENT","ems":75,"ffs":90,"cds":95,"ias":83,"cbs":79,"mes":90,"invalidation":"156.20_break_or_BOJ_hike_repricing_reversal","verification_target":"USDJPY_152.9_155_156.2_BOJ_US10Y_DXY_1d_3d_5d","verified_status":"verified"},
  {"date":"2026-09-09","signal_id":"20260909_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":97,"opp_score":52,"no_trade_score":80,"risk_pct":null,"regime":"RISK_OFF","ems":72,"ffs":80,"cds":91,"ias":51,"cbs":68,"mes":79,"invalidation":"ES_stabilization_with_US10Y_below_4.75_required","verification_target":"ES_7650_7750_WTI_US10Y_VIX_PPI_CPI_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-09","signal_id":"20260909_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":94,"opp_score":67,"no_trade_score":73,"risk_pct":null,"regime":"MIXED","ems":76,"ffs":89,"cds":91,"ias":68,"cbs":75,"mes":84,"invalidation":"NQ_below_29100_or_US10Y_above_4.82_changes_bias","verification_target":"NQ_29100_29750_US10Y_WTI_semis_PPI_CPI_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-09","signal_id":"20260909_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":95,"opp_score":48,"no_trade_score":84,"risk_pct":null,"regime":"MIXED","ems":82,"ffs":86,"cds":88,"ias":45,"cbs":67,"mes":84,"invalidation":"clear_break_below_98.5_or_above_99.5_required","verification_target":"DXY_98.5_99.5_US10Y_USDJPY_PPI_CPI_1d_3d","verified_status":"verified"},
  {"date":"2026-09-09","signal_id":"20260909_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":72,"no_trade_score":94,"risk_pct":null,"regime":"EVENT","ems":94,"ffs":97,"cds":99,"ias":70,"cbs":83,"mes":96,"invalidation":"PPI_CPI_confirmed_break_below_4.70_or_above_4.82_required","verification_target":"US10Y_4.70_4.82_WTI_NQ_GOLD_PPI_CPI_1d_3d","verified_status":"verified"},
  {"date":"2026-09-09","signal_id":"20260909_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":43,"no_trade_score":85,"risk_pct":null,"regime":"MIXED","ems":70,"ffs":71,"cds":91,"ias":48,"cbs":67,"mes":73,"invalidation":"VIX_break_above_17_with_equity_confirmation_required","verification_target":"VIX_15_17_ES_NQ_WTI_PPI_CPI_1d_3d","verified_status":"verified"}
]

本日の実運用で最も形が良いのはUSDJPYの戻り売りです。ただし154円台からは追わず、155円近辺への戻りがなければ見送ります。WTIは前日の押し目シグナルが実際に機能しましたが、94ドル台まで上昇した後なので、新規は91ドル後半～92ドル前半への再押しだけです。PPI・CPI前なので、この2本を同時に取る場合でも**0.25%＋0.25%=日次上限0.50%**を超えない運用を維持します。
