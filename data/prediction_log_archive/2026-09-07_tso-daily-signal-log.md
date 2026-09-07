<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-07 07:00 JST -->
<!-- transport: DOM innerText -> Blob download -> tools/archive_gpt_prose.py -->
<!-- archived_at: 2026-09-07T22:09:52Z / chars: 13228 / 値は無修正 -->

TSO Daily Signal Log v2 — 2026-09-07

使用モデル：GPT-5.6 Sol
本日の市場の主役：WTI
GOLD基準限月：COMEX 2026年12月限
crypto_grounds: etf=有, cme=無
expected_r_basis: subjective — 方向成立後も5営業日以内の時間決済・Entry未到達・週末/祝日ギャップによる不参加を織り込み、単純な二点分布式より低く評価。
invalidation_check: 20260906_WTI_BUY_PULLBACK=not_fired

データ基準は9月7日06:58 JST前後。本日は米国のLabor Dayで、NYSE・Nasdaq・米債市場は休場です。したがってES/NQ/US10Y/VIX等は9月4日の最終値を基準にし、週末に発生した情報を新たに反映しました。
Kiplinger

週末の最大の追加材料は、米・イランのタンカー攻撃に続き、イランがホルムズ海峡付近に新たな「exclusion zone」を設ける方針を表明したことです。さらにOPEC+は9月6日、10月の生産政策を変更しないと決定しました。
AP News
+1

1. 本日の結論

A級：0件

B級：WTI BUY

B+：0件

NO_TRADE：GOLD、BTC、ETH、USDJPY、SPX、NASDAQ、DXY、US10Y、VIX

昨日から判断の中心は変わりませんが、WTI BUY仮説はさらに強化です。

理由は、

タンカー直接攻撃
→ イラン exclusion zone
→ ホルムズ実効通航能力への懸念
→ OPEC+追加増産なし

という組み合わせです。
AP News
+1

ただしこれは同時に、TSOが最も避けるべき供給ショック直後のmomentum追随でもあります。

したがって結論はかなり明確です。

WTIが90–91ドルへ押すならBUY監視。
94～100ドルへ飛んだ場合は追わない。

金曜WTIは91.48ドル。Reutersによれば米10年債利回りは4.78%、S&P500 -0.38%、Nasdaq -0.29%、ドル指数+0.21%、現物金-1.2%でした。
Reuters

2. 前回判断の簡易検証

前日の唯一の方向あり判断は、

20260906_WTI_BUY_PULLBACK

でした。

Entry 90.00–91.00
SL 88.50
TP1 96.50
TP2 100.00

日曜だったため、通常のWTI先物でEntry/SL/TPの約定判定はまだできません。

一方、シナリオのinvalidationは、

88.50割れ、または確認可能な米イラン緊張緩和＋ホルムズ正常化

でした。

週末にはむしろ逆に、イランが新しいexclusion zoneを発表し、米・イラン双方によるタンカー攻撃が続いています。したがって、

invalidation_check: 20260906_WTI_BUY_PULLBACK=not_fired

です。
AP News
+1

前回仮説はALIVE / STRENGTHENED / NOT_FILLED_YETと記録します。

3. 市場全体の前提

総合regimeは引き続きEVENTです。

金曜のマクロ側では、米8月雇用者数が**+162k、予想+56k**。これを受け米10年債は一時4.78%へ上昇し、9月Fed利上げ確率は一時65%、その後57%程度まで低下しました。
Reuters

終値近辺は、

US10Y 4.77–4.78%
DXY 約99.2
VIX 約14.5
USDJPY 約156.25

です。
Hyperdash
+2
Twelve Data
+2

つまり金融市場はまだ全面的なRISK_OFFではありません。

ところがエネルギー側では状況が悪化しています。

イランは事実上閉鎖状態だったホルムズ海峡について新たな排除区域を設ける意向を示しました。APによれば、戦前は同海峡を約2000万bpdが通過していました。
AP News

さらに9月6日のOPEC+会合は10月の生産政策を据え置き。戦争によって実際の生産が目標を下回っているため、名目生産枠より物流障害の方が重要になっています。
Reuters

したがって現在の因果仮説は、

Hormuz → WTI → inflation → US10Y → NASDAQ/GOLD

です。

火曜日の米市場再開で、この伝播が実際に発生するかを検証します。

4. 10資産別判断
資産	判定	要点
GOLD	NO_TRADE	金利上昇と地政学需要が衝突
BTC	NO_TRADE	ETF需要は強いが80k攻防、CME更新なし
ETH	NO_TRADE	BTC方向確認待ち
WTI	B BUY	90–91押し限定
USDJPY	NO_TRADE	Fedタカ派 vs BOJ/円safe haven
SPX	NO_TRADE	火曜ギャップ確認待ち
NASDAQ	NO_TRADE	金利上昇リスク、SELL確信も不足
DXY	NO_TRADE	NFP後ドル高を追わない
US10Y	NO_TRADE	CPI＋原油ショック観察系列
VIX	NO_TRADE	金曜14.5、火曜再価格形成待ち
5. A級候補

なし。

WTIはCBS 88、EMS 84まで上げます。

しかしA級条件のうち、

MAE想定 <=0.25R

を満たしません。

今回は週末イベントを跨いだ供給ショックであり、最初の値動きが大きくなりやすいため、MAE想定を0.31Rとします。

またXM最小ロットでの実損3000円以内も、この時点では契約仕様をリアルタイム確認できていません。

したがってAへは上げません。

6. B級監視候補
WTI — B BUY / PULLBACK ONLY

金曜基準：91.48

Entry：90.00–91.00
SL：88.50
TP1：96.50
TP2：100.00

Entry中点 = 90.50

SL距離：

90.50 − 88.50 = 2.00

TP1距離：

96.50 − 90.50 = 6.00

したがって、

RR = 6.00 / 2.00 = 3.00

再計算一致。

win_prob：0.62
較正参考：0.65
expected_r：0.46
MAE想定：0.31R
CBS：88
EMS：84
risk_pct：0.25%

単純なtwo_pointなら、

0.62×3 − 0.38 = 1.48R

になります。

しかしこれは今回のexpected_rとしては過大です。Entryまで押さず未約定になる確率、急騰後に追わず参加しないケース、5営業日時間決済でTP1前に降りるケースを含め、subjective expected_r=0.46とします。

方向としてはかなり強い。

ただし注文ルールは昨日以上に厳格です。

90–91 → BUY候補
91–92 → 5分足確認後のみ
93以上 → NO_CHASE
94以上 → 実取引NO_TRADE

です。

なおB+数値条件自体はCBS/EMS/RR/win_probで満たしますが、XM最小ロット損失を確認できていないためB+認定は保留します。

7. 触らない資産

特にBTC・NASDAQ・GOLDです。

BTCは9月4日の米スポットETFに約174.6Mドルの純流入がありました。前日の約730.8Mドルからは減速したものの、流入自体は継続しています。
CryptoRank

一方、金曜終盤のBTCは約79,817ドルでした。
Hyperdash

つまり、

ETF demand = positive
price response = mediocre

です。

週末の現在値について複数の高品質現物ソースを十分整合できず、CMEも祝日前で新しい確認材料がありません。

したがってMESは65としますが、NO_TRADEを維持します。

NASDAQは金曜の強いNFPでもNasdaq総合が-0.29%程度にとどまり、株式自体の耐性はあります。
Reuters

しかしTSO参照系列はNQです。Nasdaq総合をNQ価格として代用しません。

火曜にNQが開いた際、

WTI↑ + US10Y↑ + NQ↓

が出るかを見るのが先です。

GOLDも同様です。金曜現物は約4419ドルまで下落しましたが、TSOの基準はCOMEX 2026年12月限です。
Reuters

休日中に別系列でEntryを作らず、GC12月限の再開を待ちます。

8. 後日検証ポイント

今回最も重要なのはWTI価格そのものより二次伝播です。

火曜に以下を記録します。

Case A

WTI >94
US10Y >4.80
NQ下落
GOLD伸びない

→ oil inflation shock仮説を強く支持

Case B

WTI >94
US10Y <4.75
NQ上昇
GOLD上昇

→ 地政学ショックとして処理され、金融引締め経路は弱い。

Case C

WTI <91

→ exclusion zone・タンカー攻撃にもかかわらず市場が供給障害を限定的と判断。

さらに今回はOPEC+据え置きが追加されました。
Reuters

したがって、WTIが上がらない場合の情報量はかなり大きいです。

「これだけ強いニュースでも上がらない」こと自体が弱気シグナルになります。

9. Obsidian保存用 Observation Draft
Markdown
# 2026-09-07 Hormuz Exclusion Zone Before Labor Day

Model:
GPT-5.6 Sol

Market protagonist:
WTI

Gold reference:
COMEX Dec-2026

crypto_grounds:
etf=有
cme=無

expected_r_basis:
subjective

invalidation_check:
20260906_WTI_BUY_PULLBACK=not_fired

## Regime
EVENT

## Friday references

WTI:
91.48

US10Y:
4.77-4.78

DXY:
~99.2

USDJPY:
~156.25

VIX:
~14.5

BTC:
~79800 Friday reference

## Weekend developments

US strikes three Iranian oil tankers.

Iran attacks tankers and US-linked vessels.

Iran announces planned exclusion zone near Strait of Hormuz.

OPEC+ keeps October production policy unchanged.

## Core hypothesis

Hormuz disruption
-> WTI
-> inflation expectations
-> US10Y
-> NQ / GOLD

## Decision

A:
NONE

B:
WTI BUY PULLBACK

Entry:
90.00-91.00

SL:
88.50

TP1:
96.50

TP2:
100.00

RR:
3.00

win_prob:
0.62

expected_r:
0.46 subjective

MAE:
0.31R

NO CHASE:
>=93

## NO_TRADE

GOLD
BTC
ETH
USDJPY
SPX
NASDAQ
DXY
US10Y
VIX

## Key test

Tuesday US reopening.

Observe whether:
WTI up
-> US10Y up
-> NQ down

#TSO #WTI #Hormuz #US10Y #NASDAQ #GOLD
10. TSO_LOG CSV / JSON
csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-07,20260907_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,96,51,80,,EVENT,80,85,94,49,69,86,GC_Dec_reopen_and_US10Y_direction_confirmation_required,GOLD_Dec_US10Y_DXY_WTI_Tuesday_1d_3d,partially_verified
2026-09-07,20260907_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,94,73,68,,EVENT,71,89,90,69,75,65,CME_confirmation_and_sustained_80000_82000_reclaim_required,BTC_78000_80000_82000_ETF_CME_Tuesday_1d_3d,partially_verified
2026-09-07,20260907_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,91,64,72,,EVENT,68,83,88,60,70,66,BTC_confirmation_and_ETH_relative_strength_required,ETH_BTC_ETF_CME_Tuesday_1d_3d,partially_verified
2026-09-07,20260907_WTI_BUY_PULLBACK,WTI,BUY,B,PULLBACK,90.00,91.00,88.50,96.50,100.00,3.00,0.62,0.46,99,93,31,0.25,EVENT,84,93,99,90,88,91,88.50_break_or_verified_deescalation_and_Hormuz_normalization,WTI_91.48_93_96.5_Hormuz_exclusion_US10Y_1d_3d_5d,partially_verified
2026-09-07,20260907_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,97,43,88,,EVENT,86,89,94,42,66,89,Fed_BOJ_relative_policy_and_safe_haven_direction_confirmation_required,USDJPY_155_157_DXY_US10Y_BOJ_1d_3d,verified
2026-09-07,20260907_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,91,52,81,,EVENT,73,79,92,51,68,79,ES_reopen_after_Hormuz_weekend_confirmation_required,ES_WTI_US10Y_VIX_Tuesday_1d_3d,partially_verified
2026-09-07,20260907_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,92,65,76,,EVENT,77,87,94,64,74,84,NQ_reopen_and_US10Y_oil_transmission_confirmation_required,NQ_WTI_US10Y_VIX_Tuesday_1d_3d,partially_verified
2026-09-07,20260907_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,94,50,83,,EVENT,84,87,91,48,69,86,DXY_break_confirmation_after_US_reopen_required,DXY_99.2_US10Y_WTI_CPI_1d_3d,verified
2026-09-07,20260907_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,79,95,,EVENT,95,97,99,76,85,96,post_holiday_yield_response_to_WTI_and_inflation_risk_required,US10Y_4.75_4.80_WTI_NQ_GOLD_Tuesday_1d_3d,verified
2026-09-07,20260907_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,95,57,81,,EVENT,73,70,94,61,70,74,VIX_reopen_confirmation_with_ES_NQ_and_WTI_required,VIX_14.5_ES_NQ_WTI_Tuesday_1d_3d,verified
JSON
[
{"date":"2026-09-07","signal_id":"20260907_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":96,"opp_score":51,"no_trade_score":80,"risk_pct":null,"regime":"EVENT","ems":80,"ffs":85,"cds":94,"ias":49,"cbs":69,"mes":86,"invalidation":"GC_Dec_reopen_and_US10Y_direction_confirmation_required","verification_target":"GOLD_Dec_US10Y_DXY_WTI_Tuesday_1d_3d","verified_status":"partially_verified"},
{"date":"2026-09-07","signal_id":"20260907_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":94,"opp_score":73,"no_trade_score":68,"risk_pct":null,"regime":"EVENT","ems":71,"ffs":89,"cds":90,"ias":69,"cbs":75,"mes":65,"invalidation":"CME_confirmation_and_sustained_80000_82000_reclaim_required","verification_target":"BTC_78000_80000_82000_ETF_CME_Tuesday_1d_3d","verified_status":"partially_verified"},
{"date":"2026-09-07","signal_id":"20260907_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":91,"opp_score":64,"no_trade_score":72,"risk_pct":null,"regime":"EVENT","ems":68,"ffs":83,"cds":88,"ias":60,"cbs":70,"mes":66,"invalidation":"BTC_confirmation_and_ETH_relative_strength_required","verification_target":"ETH_BTC_ETF_CME_Tuesday_1d_3d","verified_status":"partially_verified"},
{"date":"2026-09-07","signal_id":"20260907_WTI_BUY_PULLBACK","asset":"WTI","side":"BUY","rank":"B","type":"PULLBACK","entry_low":90.0,"entry_high":91.0,"sl":88.5,"tp1":96.5,"tp2":100.0,"rr":3.0,"win_prob":0.62,"expected_r":0.46,"tq_score":99,"opp_score":93,"no_trade_score":31,"risk_pct":0.25,"regime":"EVENT","ems":84,"ffs":93,"cds":99,"ias":90,"cbs":88,"mes":91,"invalidation":"88.50_break_or_verified_deescalation_and_Hormuz_normalization","verification_target":"WTI_91.48_93_96.5_Hormuz_exclusion_US10Y_1d_3d_5d","verified_status":"partially_verified"},
{"date":"2026-09-07","signal_id":"20260907_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":97,"opp_score":43,"no_trade_score":88,"risk_pct":null,"regime":"EVENT","ems":86,"ffs":89,"cds":94,"ias":42,"cbs":66,"mes":89,"invalidation":"Fed_BOJ_relative_policy_and_safe_haven_direction_confirmation_required","verification_target":"USDJPY_155_157_DXY_US10Y_BOJ_1d_3d","verified_status":"verified"},
{"date":"2026-09-07","signal_id":"20260907_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":91,"opp_score":52,"no_trade_score":81,"risk_pct":null,"regime":"EVENT","ems":73,"ffs":79,"cds":92,"ias":51,"cbs":68,"mes":79,"invalidation":"ES_reopen_after_Hormuz_weekend_confirmation_required","verification_target":"ES_WTI_US10Y_VIX_Tuesday_1d_3d","verified_status":"partially_verified"},
{"date":"2026-09-07","signal_id":"20260907_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":92,"opp_score":65,"no_trade_score":76,"risk_pct":null,"regime":"EVENT","ems":77,"ffs":87,"cds":94,"ias":64,"cbs":74,"mes":84,"invalidation":"NQ_reopen_and_US10Y_oil_transmission_confirmation_required","verification_target":"NQ_WTI_US10Y_VIX_Tuesday_1d_3d","verified_status":"partially_verified"},
{"date":"2026-09-07","signal_id":"20260907_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":94,"opp_score":50,"no_trade_score":83,"risk_pct":null,"regime":"EVENT","ems":84,"ffs":87,"cds":91,"ias":48,"cbs":69,"mes":86,"invalidation":"DXY_break_confirmation_after_US_reopen_required","verification_target":"DXY_99.2_US10Y_WTI_CPI_1d_3d","verified_status":"verified"},
{"date":"2026-09-07","signal_id":"20260907_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":79,"no_trade_score":95,"risk_pct":null,"regime":"EVENT","ems":95,"ffs":97,"cds":99,"ias":76,"cbs":85,"mes":96,"invalidation":"post_holiday_yield_response_to_WTI_and_inflation_risk_required","verification_target":"US10Y_4.75_4.80_WTI_NQ_GOLD_Tuesday_1d_3d","verified_status":"verified"},
{"date":"2026-09-07","signal_id":"20260907_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":95,"opp_score":57,"no_trade_score":81,"risk_pct":null,"regime":"EVENT","ems":73,"ffs":70,"cds":94,"ias":61,"cbs":70,"mes":74,"invalidation":"VIX_reopen_confirmation_with_ES_NQ_and_WTI_required","verification_target":"VIX_14.5_ES_NQ_WTI_Tuesday_1d_3d","verified_status":"verified"}
]

本日は**「WTIを買う日」ではなく「WTIの押しだけを待つ日」**という区別が重要です。米市場が休場しているため、週末のホルムズ悪化を株・金利市場がまだ価格形成していません。火曜の再開でWTI→US10Y→NQ/GOLDの伝播が確認できれば、次の日次判断ではNASDAQやGOLDにも方向ありシグナルが出る可能性があります。
AP News
+1
