<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-10 07:00 JST -->
<!-- transport: DOM innerText -> Blob download -> tools/archive_gpt_prose.py -->
<!-- archived_at: 2026-09-13T09:02:19Z / chars: 15104 / 値は無修正 -->

TSO Daily Signal Log v2
TSO Daily Signal Log v2 — 2026-09-10

使用モデル：GPT-5.6 Sol
本日の市場の主役：WTI
GOLD基準限月：COMEX 2026年12月限（GCZ26）
crypto_grounds: etf=有, cme=無
expected_r_basis: subjective — 本日は新規の方向あり判断を出さないため、当日LOGのexpected_rは空欄。既存シグナルの管理では、未約定・5営業日の時間決済・PPI/CPI前の早期撤退を含む従来のsubjective基準を維持します。

invalidation_check: 20260902_BTC_BUY_PULLBACK=unknown, 20260902_WTI_BUY_PULLBACK=not_fired, 20260903_NASDAQ_BUY_PULLBACK=unknown, 20260903_WTI_BUY_PULLBACK=not_fired, 20260904_NASDAQ_BUY_PULLBACK=fired, 20260904_WTI_BUY_PULLBACK=not_fired, 20260905_WTI_BUY_PULLBACK=not_fired, 20260906_WTI_BUY_PULLBACK=not_fired, 20260907_WTI_BUY_PULLBACK=not_fired, 20260908_WTI_BUY_PULLBACK=not_fired, 20260908_USDJPY_SELL_PULLBACK=not_fired, 20260909_WTI_BUY_PULLBACK=not_fired, 20260909_USDJPY_SELL_PULLBACK=not_fired

9/2 BTCと9/3 NASDAQは、こちらで現在参照できる履歴に元のinvalidation条件そのものが残っていないため、値動きから推測せずunknownとしました。逆に9/4 NASDAQは条件がNQ<29100 または US10Y>4.82と確認できており、9月9日に米10年債利回りが**4.8528%**まで上昇したため、明確にfiredです。
Reuters

9/2起点の2件は、Labor Dayを米市場営業日から除外すると本日が5営業日目の最終確認日として扱います。

1. 本日の結論

新規A級：0件
新規B級：0件
本日10資産すべて新規NO_TRADE

これは弱気だから全部見送るのではありません。むしろ現在は、

WTI上昇仮説：かなり強い
USDJPY下落仮説：かなり強い

一方で、両方ともすでに良いEntryから離れすぎたため、新しいsignal_idを増やしません。

WTIは9月9日に96.05ドルまで上昇し、Brentは101.21ドル。米10年債利回りも4.84%台へ上昇しました。米株はS&P500 -0.48%、Nasdaq -0.64%。原油ショックが金利・株へ伝播する経路がさらに確認されています。
Reuters
+1

一方USDJPYは153.65前後。米金利が上がっているにもかかわらず円高が継続しており、BOJ利上げ期待とキャリー解消が依然として米金利差を上回っています。
Reuters

そして本日最大の制約は、米8月PPIが9月10日08:30 ET＝日本時間21:30に発表されることです。翌9月11日にはCPIも控えます。
Bureau of Labor Statistics
+1

したがって今日は、既存WTI/USDJPYシグナルの管理日であって、新規Entryを増やす日ではないと判断します。

2. 前回判断の簡易検証
20260909_WTI_BUY_PULLBACK

前回：

Entry 91.80–92.50
SL 90.20
TP1 97.00
TP2 100.00

9月9日のWTIは最終的に96.05ドルまで上昇しました。ReutersではWTI +3.4%相当、Brent 101.21ドル。中東で米国とイラン双方によるタンカー攻撃が再開し、供給リスクはむしろ悪化しました。
Reuters
+1

今朝7時時点の前日中には、昨日朝の94.66付近から上方向へ進んでおり、91.80–92.50への新規再押しは確認できません。

したがって、

ORDER_NOT_FILLED / THESIS_CONTINUED_HIGHER / invalidation=not_fired

です。

ここで96ドルへEntryを引き上げるのは、TSOの「供給ショック追随禁止」に反します。

20260909_USDJPY_SELL_PULLBACK

前回：

Entry 154.80–155.40
SL 156.20
TP1 152.50
TP2 151.20

9月9日のUSDJPYは153円台で推移し、Reutersの最新値は153.65。別の日次系列でも9月9日高値は154円前後で、Entry 154.80には到達していません。
Reuters
+1

したがって、

ORDER_NOT_FILLED / THESIS_CONTINUED_LOWER / invalidation=not_fired

です。

方向は正しいですが、153円台から追って売る必要はありません。

重要な既存シグナル更新

20260904_NASDAQ_BUY_PULLBACKは本日fired。

元のinvalidationは、

NQ < 29100 または US10Y > 4.82

でした。

9月9日の米10年債利回りは一時**4.8528%**まで上昇。価格側のNQが29100を割っていなくても、OR条件なのでシナリオ失効です。
Reuters

これはかなり重要です。

NASDAQ価格が大崩れする前に、金利側のinvalidationが先に発火した

というデータになります。

3. 市場全体の前提

総合regimeはEVENTです。

現在の主要系列は、

中東供給障害
→ WTI 96.05
→ インフレ懸念
→ US10Y 4.84–4.85
→ 株式に圧力

です。

WTIは9月8日の93.03から9月9日には96.05へ上昇。Brentは101.21ドルで、Reutersによればホルムズ海峡を巡る輸送障害と新たなタンカー攻撃が主要因です。
Reuters
+1

金利側では10年債が4.84%台、別のReuters記事では一時4.8528%。米財務省が9月10日に最大60億ドルの10～20年債買い戻しを行う予定ですが、それでも長期金利上昇は止まっていません。
Reuters
+1

一方、Goldは興味深く、COMEX12月限が4458.80ドルで決済。前日の大幅安から反発しました。弱いドルと安全資産需要が金利上昇をある程度相殺しています。
Reuters

DXYは98.83前後でほぼ横ばい。USDJPYは153.65。つまり米金利高がそのままドル全面高にはつながっていません。
Reuters

VIXはCboeで16.24前後。恐怖は上昇していますが、20～30台のパニックにはまだ程遠いです。
Cboe

CryptoではBTCが約78.7k、ETHが約2510。9月8日の米スポットETFではBTCが**-46.65Mドル**、ETHが**-24.29Mドル**と、それまでの強い流入から一旦反転しました。
ODaily
+3
Investing.com
+3
Investing.com
+3

freshなCME basis/OIを今日の判断に使える品質では取得できなかったため、

crypto_grounds: etf=有, cme=無

としています。

4. 10資産別判断
資産	今日の新規判断	基準値・理由
GOLD	NO_TRADE	GCZ26 4458.8。PPI前、金利高と安全資産需要が衝突
BTC	NO_TRADE	約78.7k、ETF流出、CME fresh根拠なし
ETH	NO_TRADE	約2510、BTCより相対的に底堅いが独立edge不足
WTI	NO_TRADE	96.05。方向は上だが供給ショック追随禁止
USDJPY	NO_TRADE	153.65。SELL方向だがEntryから離れすぎ
SPX	NO_TRADE	ES Sep 約7660、PPI前＋金利高
NASDAQ	NO_TRADE	NQ Sep 約29.4–29.6k、旧BUY invalidation発火
DXY	NO_TRADE	98.83。米金利高でもドル全面高にならず
US10Y	NO_TRADE	4.84–4.85%。PPIで直接再価格形成
VIX	NO_TRADE	約16.2。上昇中だがまだ中程度

ES/NQについては現物S&P500やNasdaq Compositeを代用していません。NQ Sep-26の9月9日値はデータ提供元間に差があり、29,449～29,559程度の幅があるためpartially_verifiedとします。
Investing.com Nederland
+1

5. A級候補

なし。

特にWTIは方向確信だけならCBS/EMSともA級圏ですが、96ドルから新たに買うことと、91～92ドル台で買うことは全く別の取引です。

96.05から同じSLを維持すればSL距離が拡大し、2026-09-01改定の「SLを広げない」に抵触します。

USDJPYも同じで、153.6からSELLすると従来の156.2 SLまで2.5円以上あり、RRと実損制約が崩れます。

A条件以前にEntry品質で失格です。

6. B級監視候補

新規B級：なし。

ただし既存シグナルとしては引き続き、

WTI BUY系：管理継続
USDJPY SELL系：管理継続

です。

WTIは96ドルを追わず、既存Entryで約定していないものは未約定のままにします。

USDJPYも153円台では追いません。154円台後半への十分な戻しが出た場合でも、本日21:30のPPIを跨ぐ新規注文は原則見送る方がTSOのイベントリスク管理と整合します。

したがって今日は、過去シグナルを持っている場合の管理と検証のみです。

7. 触らない資産

最優先で触らないのはWTIの新規追随、USDJPYの新規追随、PPI直前のNASDAQ/GOLDです。

WTIは方向そのものは最も強いですが、Brentが100ドルを超え、WTIも96ドル。供給ショックのニュースを見てから買う段階ではありません。
The Wall Street Journal

USDJPYも同様で、9月初めの160円近辺から153円台まで既に約4%円高です。BOJ利上げ期待やキャリー巻き戻しという仮説は生存していますが、現在値からSELLすると「方向は合っているが取引は悪い」状態です。
Reuters
+1

Gold/NQは今夜のPPIで、US10Yが4.9%へ向かうのか、4.75%へ戻るのかによって期待値が大きく変わります。

今は先回りしません。

8. 後日検証ポイント

第一は、9/4 NASDAQ invalidationの先行性です。

US10Y >4.82で9/4 BUYシナリオがfiredしました。今後NQが29100方向へ下落するなら、「金利条件で早めに降りる」というinvalidation設計が機能した証拠になります。

逆にPPI後にUS10Yが急低下し、NQが再上昇するなら、4.82閾値が過敏だった可能性を検証します。

第二はWTIです。

WTIは96.05まで上昇しましたが、ここから100ドルへ向かうか、93～94へ戻るかを見る必要があります。
Reuters

とくにPPIが強く、

WTI高止まり + US10Y >4.85 + NQ下落

なら、ここ数日検証してきた

oil → inflation → yield → growth stocks

の伝播モデルをさらに支持します。

第三はUSDJPY。

US10Yが4.85%なのにUSDJPYが154を回復できない

状態は、円側の独自ファクターが強い証拠です。

PPIが強くても155円を回復できなければ、BOJ/キャリー解消仮説の信頼度を上げます。

第四はCrypto。

BTC ETFは9月8日に-46.65Mドルへ反転し、BTCも80kを回復できていません。
ODaily

BTC >80k + ETF再流入ならBUY監視へ戻す。

BTC <77.5k + ETF流出継続なら、9月3日の大規模流入後のdistribution仮説を強めます。

9. Obsidian保存用 Observation Draft
Markdown
# 2026-09-10 No New Signal Before PPI

Model:
GPT-5.6 Sol

Market protagonist:
WTI

Gold reference:
COMEX Dec-2026 / GCZ26

crypto_grounds:
etf=有
cme=無

expected_r_basis:
subjective

Today:
No new directional signal.
Existing WTI BUY and USDJPY SELL theses remain under validation.

## Regime
EVENT

## Market

WTI:
96.05

Brent:
101.21

Gold Dec:
4458.80 settle

US10Y:
~4.84
intraday ~4.8528

DXY:
~98.83

USDJPY:
~153.65

VIX:
~16.24

BTC:
~78.7k

ETH:
~2510

ES Sep:
~7660

NQ Sep:
~29.45k-29.56k
provider discrepancy
partially_verified

## Crypto flow

BTC ETF Sep8:
-46.65m

ETH ETF Sep8:
-24.29m

Fresh CME basis/OI:
not usable today

## Invalidation

20260902_BTC_BUY_PULLBACK=unknown
20260902_WTI_BUY_PULLBACK=not_fired
20260903_NASDAQ_BUY_PULLBACK=unknown
20260903_WTI_BUY_PULLBACK=not_fired
20260904_NASDAQ_BUY_PULLBACK=fired
20260904_WTI_BUY_PULLBACK=not_fired
20260905_WTI_BUY_PULLBACK=not_fired
20260906_WTI_BUY_PULLBACK=not_fired
20260907_WTI_BUY_PULLBACK=not_fired
20260908_WTI_BUY_PULLBACK=not_fired
20260908_USDJPY_SELL_PULLBACK=not_fired
20260909_WTI_BUY_PULLBACK=not_fired
20260909_USDJPY_SELL_PULLBACK=not_fired

Important:
Sep4 NQ BUY fired because US10Y > 4.82.

## Today decision

A:
NONE

B:
NONE NEW

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

## Event

Sep10 08:30 ET:
US PPI

Sep11 08:30 ET:
US CPI

## Research

Oil shock transmission remains:

WTI
-> inflation expectations
-> US10Y
-> NQ / Gold

JPY remains partially decoupled from US yields:

BOJ repricing
+ carry unwind
-> JPY strength

#TSO #WTI #USDJPY #US10Y #NASDAQ #PPI
10. TSO_LOG CSV / JSON
csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-10,20260910_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,63,76,,EVENT,88,87,96,61,74,86,PPI_reaction_and_GCZ26_4480_hold_required,GCZ26_4430_4480_US10Y_DXY_PPI_CPI_1d_3d,verified
2026-09-10,20260910_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,58,82,,MIXED,66,84,90,55,66,48,fresh_ETF_inflow_and_80000_82000_reclaim_required,BTC_77500_80000_82000_ETF_CME_PPI_CPI_1d_3d,partially_verified
2026-09-10,20260910_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,97,64,75,,MIXED,70,84,88,62,71,54,BTC_stabilization_and_ETH_2550_hold_required,ETH_2480_2550_BTC_ETF_PPI_CPI_1d_3d,partially_verified
2026-09-10,20260910_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,84,77,,EVENT,93,96,99,82,87,93,pullback_or_verified_supply_deescalation_required_before_new_entry,WTI_94_96_100_Hormuz_US10Y_PPI_CPI_1d_3d,verified
2026-09-10,20260910_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,78,72,,EVENT,82,92,97,79,81,91,154.5_retest_after_PPI_or_BOJ_repricing_reversal_required,USDJPY_152.5_154.5_155.5_BOJ_US10Y_PPI_CPI_1d_3d,verified
2026-09-10,20260910_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,96,54,84,,RISK_OFF,83,86,95,52,69,82,ES_stabilization_after_PPI_with_US10Y_below_4.80_required,ES_7600_7700_US10Y_WTI_VIX_PPI_CPI_1d_3d,partially_verified
2026-09-10,20260910_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,95,59,81,,MIXED,82,89,96,58,72,85,NQ_reassessment_after_US10Y_invalidation_and_PPI_required,NQ_29100_29600_US10Y_WTI_PPI_CPI_1d_3d,partially_verified
2026-09-10,20260910_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,49,86,,EVENT,84,88,93,45,68,86,PPI_break_below_98.5_or_above_99.5_required,DXY_98.5_99.5_US10Y_USDJPY_PPI_CPI_1d_3d,verified
2026-09-10,20260910_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,74,91,,EVENT,97,98,99,70,85,98,PPI_confirmed_break_below_4.75_or_above_4.90_required,US10Y_4.75_4.85_4.90_WTI_NQ_GOLD_PPI_CPI_1d_3d,verified
2026-09-10,20260910_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,60,78,,MIXED,78,80,94,61,72,80,VIX_break_above_17_with_equity_confirmation_required,VIX_16_17_20_ES_NQ_US10Y_PPI_CPI_1d_3d,verified
JSON
[
  {"date":"2026-09-10","signal_id":"20260910_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":63,"no_trade_score":76,"risk_pct":null,"regime":"EVENT","ems":88,"ffs":87,"cds":96,"ias":61,"cbs":74,"mes":86,"invalidation":"PPI_reaction_and_GCZ26_4480_hold_required","verification_target":"GCZ26_4430_4480_US10Y_DXY_PPI_CPI_1d_3d","verified_status":"verified"},
  {"date":"2026-09-10","signal_id":"20260910_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":58,"no_trade_score":82,"risk_pct":null,"regime":"MIXED","ems":66,"ffs":84,"cds":90,"ias":55,"cbs":66,"mes":48,"invalidation":"fresh_ETF_inflow_and_80000_82000_reclaim_required","verification_target":"BTC_77500_80000_82000_ETF_CME_PPI_CPI_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-10","signal_id":"20260910_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":97,"opp_score":64,"no_trade_score":75,"risk_pct":null,"regime":"MIXED","ems":70,"ffs":84,"cds":88,"ias":62,"cbs":71,"mes":54,"invalidation":"BTC_stabilization_and_ETH_2550_hold_required","verification_target":"ETH_2480_2550_BTC_ETF_PPI_CPI_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-10","signal_id":"20260910_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":84,"no_trade_score":77,"risk_pct":null,"regime":"EVENT","ems":93,"ffs":96,"cds":99,"ias":82,"cbs":87,"mes":93,"invalidation":"pullback_or_verified_supply_deescalation_required_before_new_entry","verification_target":"WTI_94_96_100_Hormuz_US10Y_PPI_CPI_1d_3d","verified_status":"verified"},
  {"date":"2026-09-10","signal_id":"20260910_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":78,"no_trade_score":72,"risk_pct":null,"regime":"EVENT","ems":82,"ffs":92,"cds":97,"ias":79,"cbs":81,"mes":91,"invalidation":"154.5_retest_after_PPI_or_BOJ_repricing_reversal_required","verification_target":"USDJPY_152.5_154.5_155.5_BOJ_US10Y_PPI_CPI_1d_3d","verified_status":"verified"},
  {"date":"2026-09-10","signal_id":"20260910_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":96,"opp_score":54,"no_trade_score":84,"risk_pct":null,"regime":"RISK_OFF","ems":83,"ffs":86,"cds":95,"ias":52,"cbs":69,"mes":82,"invalidation":"ES_stabilization_after_PPI_with_US10Y_below_4.80_required","verification_target":"ES_7600_7700_US10Y_WTI_VIX_PPI_CPI_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-10","signal_id":"20260910_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":95,"opp_score":59,"no_trade_score":81,"risk_pct":null,"regime":"MIXED","ems":82,"ffs":89,"cds":96,"ias":58,"cbs":72,"mes":85,"invalidation":"NQ_reassessment_after_US10Y_invalidation_and_PPI_required","verification_target":"NQ_29100_29600_US10Y_WTI_PPI_CPI_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-10","signal_id":"20260910_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":49,"no_trade_score":86,"risk_pct":null,"regime":"EVENT","ems":84,"ffs":88,"cds":93,"ias":45,"cbs":68,"mes":86,"invalidation":"PPI_break_below_98.5_or_above_99.5_required","verification_target":"DXY_98.5_99.5_US10Y_USDJPY_PPI_CPI_1d_3d","verified_status":"verified"},
  {"date":"2026-09-10","signal_id":"20260910_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":74,"no_trade_score":91,"risk_pct":null,"regime":"EVENT","ems":97,"ffs":98,"cds":99,"ias":70,"cbs":85,"mes":98,"invalidation":"PPI_confirmed_break_below_4.75_or_above_4.90_required","verification_target":"US10Y_4.75_4.85_4.90_WTI_NQ_GOLD_PPI_CPI_1d_3d","verified_status":"verified"},
  {"date":"2026-09-10","signal_id":"20260910_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":60,"no_trade_score":78,"risk_pct":null,"regime":"MIXED","ems":78,"ffs":80,"cds":94,"ias":61,"cbs":72,"mes":80,"invalidation":"VIX_break_above_17_with_equity_confirmation_required","verification_target":"VIX_16_17_20_ES_NQ_US10Y_PPI_CPI_1d_3d","verified_status":"verified"}
]

今日の重要点は、方向予測を新しいsignal_idへ機械的にコピーしないことです。WTI BUYとUSDJPY SELLは依然として生きていますが、現在価格で入り直すとEntry品質が悪化します。一方、9/4 NASDAQ BUYは価格SLを待たず、設計済みのUS10Y > 4.82で本日正式にfiredとなりました。今夜のPPI後にUS10Y・NQ・GCZ26がどう再価格形成するかが、次の方向あり判断の主要材料です。
