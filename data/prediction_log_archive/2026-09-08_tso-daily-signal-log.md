<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-08 07:00 JST -->
<!-- transport: DOM innerText -> Blob download -> tools/archive_gpt_prose.py -->
<!-- archived_at: 2026-09-07T22:09:52Z / chars: 14410 / 値は無修正 -->

TSO Daily Signal Log v2 — 2026-09-08

使用モデル：GPT-5.6 Sol
本日の市場の主役：WTI
GOLD基準限月：COMEX 2026年12月限（GCZ26）
crypto_grounds: etf=有, cme=無
expected_r_basis: subjective — 5営業日の時間決済、Entry未到達、イベント前後の途中撤退を織り込み、単純なTP1/SL二点分布より低く評価。
invalidation_check: 20260907_WTI_BUY_PULLBACK=not_fired

基準時点は2026年9月8日07:00 JST前後。米Labor Day明けで、ES/NQ/米債はちょうど通常セッション再開へ移る時間帯のため、安定した新セッション価格がまだ不足しています。そのため株・VIX・US10Yは9月4日の確定値と休日中の先物情報を組み合わせ、partially_verifiedとします。

WTIは休日取引中に92.65ドルまで上昇し、一時93.29ドル。COMEX金12月限は約4456～4461ドル、USDJPYは154.4前後、BTCは約79185ドル、ETHは約2489ドルです。
CoinMarketCap
+5
DAWN
+5
Reuters
+5

1. 本日の結論

A級：0件

B級：WTI BUY、USDJPY SELL

B+：0件

NO_TRADE：GOLD、BTC、ETH、SPX、NASDAQ、DXY、US10Y、VIX

昨日までの最大テーマだったWTI上昇は継続しました。金曜91.48ドルから休日取引で92.65ドル、一時93.29ドルまで上昇。米・イランによる船舶攻撃、ホルムズ海峡の通航低迷、湾岸エネルギー施設への脅威が継続しています。
Reuters
+2
Reuters
+2

ただし重要なのは、昨日の90–91ドルEntryを上へ追従させないことです。93ドル台は既に短期過熱域に近く、RSI過熱と93.64付近の抵抗も観測されています。
Investing.com 香港

もう一つ、本日初めて方向ありへ戻すのがUSDJPY SELLです。ドル円は金曜156円台から休日中に一時154.05、直近154.4前後まで低下。BOJ利上げ観測、円キャリー巻き戻し、資金還流観測が、強い米雇用統計によるドル高圧力を上回っています。
Reuters
+1

ただし154円台を成行SELLするのではなく、155円台への戻り売り限定です。

2. 前回判断の簡易検証

前日の唯一の方向あり判断は、

20260907_WTI_BUY_PULLBACK

でした。

前回：

Entry 90.00–91.00
SL 88.50
TP1 96.50
TP2 100.00

休日取引ではWTIが一時91.03付近まで下がった後、92.65、一時93.29へ上昇しました。取得できた高品質データだけでは90.00–91.00への明確な約定を確認できないため、

FILL = unknown

とします。
Euronext
+1

一方、invalidation条件だった

88.50割れ、または明確な米イラン緊張緩和＋ホルムズ正常化

はいずれも確認されていません。

むしろ米・イランは船舶への攻撃を継続し、イランは湾岸エネルギー資産への報復能力を警告。ホルムズ通航の10日平均は1日10隻まで低下しています。
Reuters
+1

したがって、

invalidation_check: 20260907_WTI_BUY_PULLBACK=not_fired

です。

方向仮説はSUCCESS寄り / ALIVEと評価します。

3. 市場全体の前提

本日の総合regimeはEVENTです。

現在の構造は、

WTI↑
＋ 米金利高止まり
＋ Fed利上げ観測約60%
＋ しかしDXYは伸びず
＋ 円は急騰
＋ BTCは80kを維持できない

です。

強い8月雇用統計を受け、9月Fed利上げ確率は約60%へ上昇。これがGoldを圧迫し、COMEX12月限は休日中に約4456ドルまで下落しました。
Reuters

一方で、ドル円は一時154.05。米金利要因だけならドル高になるはずなのに、円高が勝っています。
Reuters

これは重要で、今のUSDJPYでは、

US rates < BOJ repricing + carry unwind + yen repatriation

になっている可能性が高い。

株については、米現物市場が休日だったためまだ十分な検証がありません。休日中のS&P/Nasdaq先物は方向感が乏しく、アジアでは日韓の半導体株がかなり強く推移しました。
AP News
+1

したがってNASDAQについては、WTI高だからSELLとも、AI半導体が強いからBUYともまだ決めません。

4. 10資産別判断
資産	判定	短期評価
GOLD	NO_TRADE	GCZ26約4460、金利圧力 vs 地政学
BTC	NO_TRADE	ETF強いが79k、CME根拠なし
ETH	NO_TRADE	2.49k、BTC確認待ち
WTI	B BUY	91.2–92.0への押し限定
USDJPY	B SELL	155円台への戻り限定
SPX	NO_TRADE	ES再開後確認待ち
NASDAQ	NO_TRADE	NQ再開直後、AI強度と金利が衝突
DXY	NO_TRADE	強いNFPでも伸び鈍化
US10Y	NO_TRADE	CPI前＋原油インフレ
VIX	NO_TRADE	米現物再開後の反応待ち
5. A級候補

なし。

最も近いのはWTIです。

本日WTIは、

CBS 87
EMS 83
expected_r 0.44
MAE想定 0.30R

とします。

CBS・EMSは十分ですが、

expected_r >= 0.45
MAE <= 0.25R

をわずかに満たしません。

何より既に金曜から10%以上上昇したイベント相場です。ニュース一本で2～3ドルの逆行も十分あり得ます。

USDJPYも方向性は強まりましたが、5営業日で約3%以上円高が進んだ後なのでAには不適切です。

6. B級監視候補
WTI — B BUY / PULLBACK

現在参考：約92.65。
Reuters

Entry 91.20–92.00
SL 89.50
TP1 97.00
TP2 100.00

Entry中点 = 91.60
SL距離 = 91.60 − 89.50 = 2.10
TP1距離 = 97.00 − 91.60 = 5.40

RR = 5.40 / 2.10 = 2.57

再計算一致。

win_prob 0.60
較正参考 0.63
expected_r 0.44
MAE想定 0.30R
risk_pct 0.25%
CBS 87 / EMS 83 / MES 90

two_pointなら、

0.60 × 2.57 − 0.40 = 1.14R

ですが、これをLOGには使いません。

本日は91.2–92.0へ押さず上昇してしまう未約定確率、93ドル超から追わないケース、ニュース反転による早期撤退、5営業日の時間決済を織り込みsubjective 0.44Rとします。

執行ルールは、

91.2–92.0 → BUY候補
92.0–93.0 → 5分足反転確認必須
93.0以上 → NO_CHASE
94.0以上 → 実取引NO_TRADE

です。

93.29まで既に試したため、「方向が当たっているからEntryを上げる」は禁止します。
DAWN

USDJPY — B SELL / PULLBACK

現在参考：約154.4。一時154.05。
Reuters

Entry 155.00–155.60
SL 156.40
TP1 152.80
TP2 151.50

Entry中点 = 155.30
SL距離 = 156.40 − 155.30 = 1.10
TP1距離 = 155.30 − 152.80 = 2.50

RR = 2.50 / 1.10 = 2.27

再計算一致。

win_prob 0.57
較正参考 0.60
expected_r 0.34
MAE想定 0.32R
risk_pct 0.25%
CBS 75 / EMS 72 / MES 86

円は5営業日で約3.4%上昇し、BOJの次回利上げを約80%織り込むとの市場観測も出ています。
フィナンシャル・タイムズ

ただし154円台を売ると短期的には完全な追随です。

したがって、

154台 → NO_CHASE
155.0–155.6 → SELL監視
156.4超 → 仮説失効

とします。

WTIとUSDJPYを両方実行する場合は**0.25%＋0.25%=日次上限0.50%**なので、3本目は追加しません。

XM最小ロットで3000円以内かを今回の外部データから確定できないため、両方ともB+認定は保留です。

7. 触らない資産

特にBTC・GOLD・NASDAQです。

BTCは米スポットETFが9月4日までの週に約9.87億ドル純流入。機関需要そのものは明確に強いです。
HedgeCo
+1

ところが現在BTCは約79185ドル。9月3日に81k超へ上昇した後、再び80kを割っています。
CoinMarketCap

したがって、

ETF FLOW = bullish
PRICE = weak/neutral
CME = unavailable

です。

MESは60台を維持しますが、ユーザールールに従ってNO_TRADE。

ETHも約2489ドルまで戻していますが、BTCほどETF需要が強くなく、BTCが80～82kを取り戻す前に独立BUYするedgeは薄いです。
CoinMarketCap
+1

GOLDはさらに興味深く、戦争が悪化しているのにGCZ26は約4460ドル。12月限は休日セッションで4481.3高値、4430.4安値を記録しています。
FXEmpire

安全資産需要よりFed・金利要因がまだ強い。

NASDAQは逆に、休日中の日本・韓国で半導体株が大幅高でした。
AP News

だからこそ、NQをWTIだけでSELLするのも危険です。米国再開後の価格を確認します。

8. 後日検証ポイント

本日から最も重要なのは、昨日まで待っていた米国市場の再価格形成です。

第一の検証は、

WTI 92～93
→ US10Yが4.80超へ行くか

です。

ここで、

WTI↑ + US10Y↑ + NQ↓

なら、これまで研究してきた

WTI → inflation → US10Y → NQ

をさらに支持します。

逆に、

WTI >93
US10Y <4.75
NQ >29600

なら、原油高よりAI・Fed期待の方が株価を支配していると判断します。

第二はUSDJPYです。

一時154.05まで円高が進んだのに、

米金利上昇でも155を回復できない

なら、円側の独自ファクターが相当に強い。

逆に156.40を超えて戻れば、今回の円高は休日薄商い＋ポジション解消の寄与が大きかったとしてSELL仮説を失効させます。

第三はBTC。

ETFへの約9.9億ドル週間流入にもかかわらず80k未満という乖離があります。
HedgeCo

ETF positive + BTC >82000
→ 需給仮説を再強化。

ETF positive + BTC <78000
→ 潜在売り圧力を重く評価。

9. Obsidian保存用 Observation Draft
Markdown
# 2026-09-08 US Reopen After Labor Day

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

Reason:
Entry non-fill probability,
5-day time exit,
event-driven early exit,
and no-chase rules included.

invalidation_check:
20260907_WTI_BUY_PULLBACK=not_fired

## Regime
EVENT

## Current references

WTI:
~92.65
holiday high ~93.29

Gold Dec:
~4456-4461

USDJPY:
~154.4
holiday low ~154.05

BTC:
~79185

ETH:
~2489

US10Y:
Friday 4.784%

ES:
Friday/holiday reference ~7722

NQ:
Friday/holiday reference ~29565

VIX:
Friday reference ~15.24

## WTI

Previous thesis:
ALIVE

Previous invalidation:
NOT FIRED

New setup:
BUY PULLBACK

Entry:
91.20-92.00

SL:
89.50

TP1:
97.00

TP2:
100.00

RR:
2.57

win_prob:
0.60

expected_r:
0.44 subjective

No chase:
>=93

## USDJPY

New directional setup:
SELL PULLBACK

Current:
~154.4

Entry:
155.00-155.60

SL:
156.40

TP1:
152.80

TP2:
151.50

RR:
2.27

win_prob:
0.57

expected_r:
0.34 subjective

Do not chase 154.

## Crypto divergence

BTC ETF weekly:
~+986.7m

BTC price:
below 80k

Interpretation:
institutional flow strong,
price response weak.

CME evidence:
not available in today's judgment.

## Research test

US market reopens.

Primary chain:
WTI
-> US10Y
-> NQ / GOLD

Secondary:
BOJ repricing
-> JPY
-> USDJPY / carry trades

A:
NONE

B:
WTI BUY PULLBACK
USDJPY SELL PULLBACK

NO_TRADE:
GOLD
BTC
ETH
SPX
NASDAQ
DXY
US10Y
VIX

#TSO #WTI #USDJPY #US10Y #NASDAQ #BTC #Gold
10. TSO_LOG CSV / JSON
csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-08,20260908_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,49,83,,EVENT,81,85,92,47,68,84,GCZ26_4500_reclaim_with_US10Y_decline_required,GOLD_Dec_4430_4500_US10Y_DXY_WTI_1d_3d,verified
2026-09-08,20260908_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,74,69,,EVENT,70,89,89,69,74,63,CME_confirmation_and_80000_82000_reclaim_required,BTC_78000_80000_82000_ETF_CME_1d_3d,partially_verified
2026-09-08,20260908_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,96,64,72,,EVENT,68,83,86,60,70,65,BTC_confirmation_and_ETH_2550_reclaim_required,ETH_2450_2550_BTC_ETF_CME_1d_3d,partially_verified
2026-09-08,20260908_WTI_BUY_PULLBACK,WTI,BUY,B,PULLBACK,91.20,92.00,89.50,97.00,100.00,2.57,0.60,0.44,99,91,34,0.25,EVENT,83,92,98,87,87,90,89.50_break_or_verified_Hormuz_deescalation,WTI_91.2_93_97_Hormuz_US10Y_1d_3d_5d,verified
2026-09-08,20260908_USDJPY_SELL_PULLBACK,USDJPY,SELL,B,PULLBACK,155.00,155.60,156.40,152.80,151.50,2.27,0.57,0.34,99,80,48,0.25,EVENT,72,86,92,79,75,86,156.40_break_or_BOJ_hawkish_repricing_reversal,USDJPY_154_155.3_152.8_BOJ_US10Y_DXY_1d_3d_5d,verified
2026-09-08,20260908_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,91,57,77,,EVENT,73,79,91,56,69,78,ES_post_holiday_price_discovery_required,ES_WTI_US10Y_VIX_1d_3d,partially_verified
2026-09-08,20260908_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,94,68,71,,EVENT,77,88,92,69,75,84,NQ_post_holiday_hold_with_US10Y_confirmation_required,NQ_29565_WTI_US10Y_semis_1d_3d,partially_verified
2026-09-08,20260908_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,95,48,84,,EVENT,83,86,88,47,68,84,US_reopen_and_CPI_direction_confirmation_required,DXY_98.8_100_US10Y_CPI_1d_3d,partially_verified
2026-09-08,20260908_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,78,94,,EVENT,94,96,98,75,84,95,post_holiday_break_below_4.70_or_above_4.85_required,US10Y_4.70_4.85_WTI_NQ_GOLD_1d_3d,partially_verified
2026-09-08,20260908_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,94,52,81,,EVENT,71,69,91,57,69,72,VIX_post_holiday_equity_confirmation_required,VIX_14_17_ES_NQ_WTI_1d_3d,partially_verified
JSON
[
{"date":"2026-09-08","signal_id":"20260908_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":49,"no_trade_score":83,"risk_pct":null,"regime":"EVENT","ems":81,"ffs":85,"cds":92,"ias":47,"cbs":68,"mes":84,"invalidation":"GCZ26_4500_reclaim_with_US10Y_decline_required","verification_target":"GOLD_Dec_4430_4500_US10Y_DXY_WTI_1d_3d","verified_status":"verified"},
{"date":"2026-09-08","signal_id":"20260908_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":74,"no_trade_score":69,"risk_pct":null,"regime":"EVENT","ems":70,"ffs":89,"cds":89,"ias":69,"cbs":74,"mes":63,"invalidation":"CME_confirmation_and_80000_82000_reclaim_required","verification_target":"BTC_78000_80000_82000_ETF_CME_1d_3d","verified_status":"partially_verified"},
{"date":"2026-09-08","signal_id":"20260908_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":96,"opp_score":64,"no_trade_score":72,"risk_pct":null,"regime":"EVENT","ems":68,"ffs":83,"cds":86,"ias":60,"cbs":70,"mes":65,"invalidation":"BTC_confirmation_and_ETH_2550_reclaim_required","verification_target":"ETH_2450_2550_BTC_ETF_CME_1d_3d","verified_status":"partially_verified"},
{"date":"2026-09-08","signal_id":"20260908_WTI_BUY_PULLBACK","asset":"WTI","side":"BUY","rank":"B","type":"PULLBACK","entry_low":91.20,"entry_high":92.00,"sl":89.50,"tp1":97.00,"tp2":100.00,"rr":2.57,"win_prob":0.60,"expected_r":0.44,"tq_score":99,"opp_score":91,"no_trade_score":34,"risk_pct":0.25,"regime":"EVENT","ems":83,"ffs":92,"cds":98,"ias":87,"cbs":87,"mes":90,"invalidation":"89.50_break_or_verified_Hormuz_deescalation","verification_target":"WTI_91.2_93_97_Hormuz_US10Y_1d_3d_5d","verified_status":"verified"},
{"date":"2026-09-08","signal_id":"20260908_USDJPY_SELL_PULLBACK","asset":"USDJPY","side":"SELL","rank":"B","type":"PULLBACK","entry_low":155.00,"entry_high":155.60,"sl":156.40,"tp1":152.80,"tp2":151.50,"rr":2.27,"win_prob":0.57,"expected_r":0.34,"tq_score":99,"opp_score":80,"no_trade_score":48,"risk_pct":0.25,"regime":"EVENT","ems":72,"ffs":86,"cds":92,"ias":79,"cbs":75,"mes":86,"invalidation":"156.40_break_or_BOJ_hawkish_repricing_reversal","verification_target":"USDJPY_154_155.3_152.8_BOJ_US10Y_DXY_1d_3d_5d","verified_status":"verified"},
{"date":"2026-09-08","signal_id":"20260908_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":91,"opp_score":57,"no_trade_score":77,"risk_pct":null,"regime":"EVENT","ems":73,"ffs":79,"cds":91,"ias":56,"cbs":69,"mes":78,"invalidation":"ES_post_holiday_price_discovery_required","verification_target":"ES_WTI_US10Y_VIX_1d_3d","verified_status":"partially_verified"},
{"date":"2026-09-08","signal_id":"20260908_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":94,"opp_score":68,"no_trade_score":71,"risk_pct":null,"regime":"EVENT","ems":77,"ffs":88,"cds":92,"ias":69,"cbs":75,"mes":84,"invalidation":"NQ_post_holiday_hold_with_US10Y_confirmation_required","verification_target":"NQ_29565_WTI_US10Y_semis_1d_3d","verified_status":"partially_verified"},
{"date":"2026-09-08","signal_id":"20260908_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":95,"opp_score":48,"no_trade_score":84,"risk_pct":null,"regime":"EVENT","ems":83,"ffs":86,"cds":88,"ias":47,"cbs":68,"mes":84,"invalidation":"US_reopen_and_CPI_direction_confirmation_required","verification_target":"DXY_98.8_100_US10Y_CPI_1d_3d","verified_status":"partially_verified"},
{"date":"2026-09-08","signal_id":"20260908_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":78,"no_trade_score":94,"risk_pct":null,"regime":"EVENT","ems":94,"ffs":96,"cds":98,"ias":75,"cbs":84,"mes":95,"invalidation":"post_holiday_break_below_4.70_or_above_4.85_required","verification_target":"US10Y_4.70_4.85_WTI_NQ_GOLD_1d_3d","verified_status":"partially_verified"},
{"date":"2026-09-08","signal_id":"20260908_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":94,"opp_score":52,"no_trade_score":81,"risk_pct":null,"regime":"EVENT","ems":71,"ffs":69,"cds":91,"ias":57,"cbs":69,"mes":72,"invalidation":"VIX_post_holiday_equity_confirmation_required","verification_target":"VIX_14_17_ES_NQ_WTI_1d_3d","verified_status":"partially_verified"}
]

本日の更新で重要なのは二つです。WTIは前日の上方向仮説を確認したものの、93ドル台では既に追う価値が低下していること。もう一つは、強い米雇用統計にもかかわらずUSDJPYが154円台まで下落し、円側のBOJ・キャリー巻き戻し要因が明確に米金利要因を上回り始めたことです。今日はWTIの押し目とUSDJPYの戻りだけを監視し、米市場再開直後のNQ/GOLDは先回りしません。
Reuters
+1
