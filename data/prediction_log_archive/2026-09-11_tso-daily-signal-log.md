<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-11 07:00 JST -->
<!-- transport: DOM innerText -> Blob download -> tools/archive_gpt_prose.py -->
<!-- archived_at: 2026-09-13T09:02:19Z / chars: 15976 / 値は無修正 -->

TSO Daily Signal Log v2
TSO Daily Signal Log v2 — 2026-09-11

使用モデル：GPT-5.6 Sol
本日の市場の主役：WTI
GOLD基準限月：COMEX 2026年12月限（GCZ26）
ES/NQ参照：比較継続のため本日は9月限 ESU26 / NQU26。9月10日がロール日で出来高移行中のため、両系列は partially_verified 扱い。 
ExpectancyIQ

crypto_grounds: etf=有, cme=有
expected_r_basis: subjective — 本日のNASDAQ SELLは、CPI前の未約定確率、CPIでの逆方向ギャップ、5営業日時間決済、シナリオ崩壊時の早期撤退を織り込み、TP1/SLだけの二点分布より低く評価します。

invalidation_check: 20260903_NASDAQ_BUY_PULLBACK=unknown, 20260903_WTI_BUY_PULLBACK=not_fired, 20260904_WTI_BUY_PULLBACK=not_fired, 20260905_WTI_BUY_PULLBACK=not_fired, 20260906_WTI_BUY_PULLBACK=not_fired, 20260907_WTI_BUY_PULLBACK=not_fired, 20260908_WTI_BUY_PULLBACK=not_fired, 20260908_USDJPY_SELL_PULLBACK=not_fired, 20260909_WTI_BUY_PULLBACK=not_fired, 20260909_USDJPY_SELL_PULLBACK=not_fired

9月3日NASDAQは元のinvalidation条件を現在の台帳断片から確定できないため、値動きから推測せずunknownです。9月3日分は本日が5営業日後の最終確認日。9月2日分は昨日で5営業日の窓を終了したため、本日の行から外しています。WTI群は価格側の既知の失効水準を大幅に上回り、供給正常化も起きていません。USDJPY SELL群も156.20/156.40を超えず、むしろBOJの升委員が追加・場合によっては速い利上げの必要性に言及しているためnot_firedです。
Reuters
+1

データ基準は2026年9月10日米国取引終了～9月11日07:00 JST前後です。8月PPIは前月比**+0.4%、前年比+5.4%**。前年比はReuters調査の5.3%をやや上回りました。今夜9月11日21:30 JSTには8月CPIが発表されます。
アメリカ合衆国労働省
+2
Boursorama
+2

1. 本日の結論

A級：0件

B級：NASDAQ SELL / PULLBACK 1件

B+：0件

NO_TRADE：GOLD、BTC、ETH、WTI、USDJPY、SPX、DXY、US10Y、VIX

今日の変化は明確です。WTIは9月10日にさらに6%以上上昇して102.48ドルで清算、Brentは107.63ドル。米10年債利回りも約**4.94～4.96%**まで上昇しました。S&P500は-0.58%、Nasdaqは-0.65%、金先物は-1.2%。これまで観察してきた

WTI上昇 → インフレ懸念 → US10Y上昇 → Growth株圧迫

が一段はっきりしました。
Reuters
+2
The Wall Street Journal
+2

ただし、WTIを102ドルから買う判断ではありません。これは明確な供給ショック追随になるので新規はNO_TRADEです。

一方NASDAQは、9月4日のBUYシナリオが金利条件で先にfiredした後も、油価・PPI・長期金利がさらに悪化しました。そこで今日は初めて逆方向のSELLをB級監視として新規発行します。ただし現在値を売らず、NQの戻りを待ちます。

2. 前回判断の簡易検証

昨日は新規方向あり判断を発行していないため、検証対象は既存シグナルです。

WTIは9月9日の96.05ドルから、9月10日に102.48ドルまでさらに上昇しました。Iran/Houthi関連のタンカー攻撃と紅海・ホルムズ双方の物流障害が悪化し、OPECの8月産出量も戦争・輸出停止等で約64万bpd減少したとReutersは報じています。既存BUY仮説は方向面では大幅に進展しています。
Reuters

したがって9/3～9/9の既存WTI BUY群は、既知の価格失効水準にも達しておらず、供給正常化もありません。すべてnot_firedを維持します。

USDJPYは9月10日に一時円安方向へ戻し、Reuters終盤値は154.32円前後。それでも9/8シグナルの156.40、9/9シグナルの156.20には遠く、BOJ追加利上げ観測も後退していません。
Reuters
+1

よって、

20260908_USDJPY_SELL_PULLBACK=not_fired
20260909_USDJPY_SELL_PULLBACK=not_fired

です。

9月3日NASDAQ BUYだけは、元のinvalidation文を確定できないためunknownのまま最終日を迎えます。ここは9月4日NASDAQのUS10Y>4.82条件を流用しません。

3. 市場全体の前提

総合regimeはEVENTです。

8月PPIは前年比5.4%へ加速しました。エネルギー価格は前月比4.2%上昇し、特にディーゼルは24.1%上昇。市場の9月Fed利上げ確率は約70%へ上昇しています。
AP News
+1

同時に原油市場では、Iran/Houthiを巡る船舶攻撃、ホルムズ海峡の低通航、Mocha港を含む紅海側の障害が重なり、WTIは102.48、Brentは107.63まで上昇しました。
Reuters

米10年債は約4.94～4.96%。5%が目前です。
The Wall Street Journal
+1

DXYはPPI後に99.06まで上昇。一方USDJPYは154円台にとどまり、ドル全面高というより「米金利高＋円独自の強さ」という状態です。
Reuters

Goldは米金利上昇に負け、米金先物は4407.30ドルで清算。TSOの基準はGCZ26で、Reutersのアクティブ米金先物価格を12月限の基準近似として使います。現物は4355.85ドルまで下落しました。
Reuters

CryptoはBTC現物が概ね77.9～78.3k。CME BTC先物は9月10日に約78.1～78.5kで、現物に対して小幅プレミアムですが、取得時点が完全一致していないのでbasis自体は定量評価しません。
Investing.com
+2
Investing.com Nigeria
+2

BTC ETFは9月8日-46.6M、9月9日約-120Mと2営業日連続流出。ETH ETFは最新取得値で+34.75Mの流入が確認できます。BTCの機関需給は9月初旬より明確に鈍化しています。
LCX
+1

4. 10資産別判断
資産	判定	今日の読み
GOLD	NO_TRADE	金利SELL優勢だがCPI前＋地政学反発リスク
BTC	NO_TRADE	78k近辺、ETF流出、CMEは小幅premium
ETH	NO_TRADE	約2.42k、ETF流入でも価格弱い
WTI	NO_TRADE	102.48、方向は強いが完全なNO_CHASE
USDJPY	NO_TRADE	既存SELL仮説管理。154台から新規コピーしない
SPX	NO_TRADE	ESU26下落、CPI前で追いSELLしない
NASDAQ	B SELL	NQU26戻り売りのみ
DXY	NO_TRADE	99.06、CPI前のドル追随禁止
US10Y	NO_TRADE	約4.94～4.96%、5%直前＋CPI
VIX	NO_TRADE	Cboe遅延値17.06、まだパニック域ではない

Cboeの9月10日遅延データではVIXは17.06、前日終値16.46から+0.60でした。
Cboe Global Markets

NQU26は取得できた遅延系列で約29176、当日レンジ約29043～29508。日次判定はStrong Sell。ESU26も約7610台まで下落し、当日安値7585.5が確認されています。
Investing.com Australia
+1

5. A級候補

なし。

NASDAQ SELLは方向条件だけならかなり良くなっています。

CBS 82
EMS 88
RR 2.22

ですが、

expected_r 0.39 < 0.45
MAE想定 0.31R > 0.25R

なのでA級条件を満たしません。

さらに今夜21:30 JSTのCPIがあります。CPIが弱ければUS10Yが4.8%方向へ急低下し、NQが大きく反発する可能性があるため、A級には上げません。

6. B級監視候補
NASDAQ — B SELL / PULLBACK ONLY

参照系列：NQU26
最新遅延参考：約29176。日中安値約29043。
Investing.com Australia

Entry：29300–29400
SL：29620
TP1：28750
TP2：28350

Entry中点：

29350

SL距離：

29620 − 29350 = 270

TP1距離：

29350 − 28750 = 600

したがって、

RR = 600 / 270 = 2.22

再計算一致です。

win_prob：0.58
較正後参考：0.61
expected_r：0.39 subjective
MAE想定：0.31R
risk_pct：0.25%
CBS：82
EMS：88
MES：92

二点分布なら、

0.58 × 2.22 - 0.42 = 0.87R

ですが、これをLOGには使いません。

CPI前なので、Entryまで戻らない未約定、CPI直後の上方向ギャップ、TP1前の時間決済、金利急低下時の早期撤退を織り込み0.39Rとします。

現在29100台なので今からSELLしません。

29300–29400への戻りのみ監視です。

29620超なら、短期下降シナリオは崩れたと扱います。

また、US10Yが4.80%未満へ急低下し、同時にWTIも100ドルを割って安定する場合は、価格SL前でもマクロシナリオの崩壊を疑います。

XM最小ロット時の想定実損を今回確定できていないため、数値上のCBS/EMS/RR/win_probを満たしてもB+には認定しません。発注画面で3000円以内を確認できない場合は実取引NO_TRADEです。

7. 触らない資産

最も触らないのはWTIです。

102.48ドルまで1日で6%以上上昇しています。方向の主観確率が高くても、ここからBUYすることはTSOの「供給ショック直後のmomentum追随禁止」に正面から反します。
Reuters

次がUS10Yです。5%近辺まで上がりましたが、今夜のCPI一つで10～20bp規模の逆行があり得ます。

GOLDもSELL方向の材料は揃っていますが、すでに1日で1%以上下落し、同時に中東戦争によるsafe-haven需要があります。金利だけを見て追いSELLはしません。

USDJPYは新規シグナルを増やさず、9/8・9/9 SELLの管理に任せます。BOJの升委員は9月10日、物価が加速すればより速い利上げが必要になり得ると述べており、円高仮説自体は崩れていません。
Reuters

8. 後日検証ポイント

第一はNASDAQの方向転換です。

9月4日BUYがUS10Y>4.82で先にfiredし、その後10年債は4.94～4.96まで上昇しました。今日初めてNQ SELLを新規発行しました。

これで今後、

US10Y高止まり → NQ 28750到達

なら、「金利invalidationが旧BUYを早く切り、新しいSELLへ移行する」という設計が機能したことになります。

逆にCPI後、

US10Y <4.80 + NQ >29620

となれば、今日のSELLはfiredです。これも良い教師データです。

第二はWTI100ドル定着です。

9月10日の102.48は一時的なニューススパイクなのか、戦争による新しい価格帯なのかを判別します。Reutersは今回を「persistently disrupted oil market」へ移行した可能性のある局面として報じています。
Reuters

第三はBTCのETF乖離です。

9月3～4日の大規模ETF流入でも82kを維持できず、その後ETFは2営業日連続流出、BTCも78k近辺です。

BTC <77500 + ETF流出継続
→ distribution仮説強化。

BTC >80000 + ETF再流入 + CME premium維持
→ BUY再評価。

第四はUSDJPYの金利離れ。

US10Yが5%近辺なのにUSDJPYが155～156へ戻れないなら、BOJ利上げ・円キャリー解消・国内回帰という円固有ファクターをさらに重くします。

9. Obsidian保存用 Observation Draft
Markdown
# 2026-09-11 Oil Above 100, NQ Bias Flips

Model:
GPT-5.6 Sol

Market protagonist:
WTI

Gold reference:
COMEX Dec-2026 / GCZ26

Equity futures reference:
ESU26
NQU26

Note:
Sep10 is equity futures roll date.
Keep Sep contracts for continuity today.
partially_verified because volume is migrating.

crypto_grounds:
etf=有
cme=有

expected_r_basis:
subjective

Reason:
CPI event risk
non-fill probability
early scenario exit
5-business-day time exit

## Regime
EVENT

## Macro

US PPI Aug:
MoM +0.4%
YoY +5.4%

Reuters consensus YoY:
5.3%

Next:
US CPI
Sep11 08:30 ET
Sep11 21:30 JST

## Market

WTI:
102.48 settle

Brent:
107.63 settle

US10Y:
~4.94-4.96%

DXY:
~99.06

USDJPY:
~154.32

Gold futures:
~4407.30
GCZ26 reference approximation

VIX:
~17.06 delayed

BTC:
~77.9-78.3k

ETH:
~2425

CME BTC:
~78.1-78.5k

NQU26:
~29176 delayed
range ~29043-29508

ESU26:
~7610s delayed
low ~7585.5

## Crypto flow

BTC ETF:
Sep8 -46.6m
Sep9 ~-120m

ETH ETF:
latest accessible +34.75m

## Outstanding invalidation

20260903_NASDAQ_BUY_PULLBACK=unknown
20260903_WTI_BUY_PULLBACK=not_fired
20260904_WTI_BUY_PULLBACK=not_fired
20260905_WTI_BUY_PULLBACK=not_fired
20260906_WTI_BUY_PULLBACK=not_fired
20260907_WTI_BUY_PULLBACK=not_fired
20260908_WTI_BUY_PULLBACK=not_fired
20260908_USDJPY_SELL_PULLBACK=not_fired
20260909_WTI_BUY_PULLBACK=not_fired
20260909_USDJPY_SELL_PULLBACK=not_fired

Sep3 signals:
final invalidation-check day.

Sep2 signals:
5-business-day window completed yesterday.

## Today

A:
NONE

B:
NASDAQ SELL PULLBACK

NASDAQ:
Entry 29300-29400
SL 29620
TP1 28750
TP2 28350
RR 2.22
win_prob 0.58
expected_r 0.39 subjective
MAE 0.31R
risk_pct 0.25

NO CHASE:
current NQ near 29100s

B+:
NONE
XM minimum-lot loss not verified.

NO_TRADE:
GOLD
BTC
ETH
WTI
USDJPY
SPX
DXY
US10Y
VIX

## Primary research chain

Middle East supply disruption
-> WTI >100
-> inflation
-> US10Y near 5%
-> NQ pressure

## Secondary research chain

BOJ tightening
-> carry unwind
-> JPY strength
despite high US10Y

#TSO #WTI #NASDAQ #US10Y #USDJPY #CPI
10. TSO_LOG CSVとJSON
csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-11,20260911_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,66,79,,EVENT,92,91,98,64,76,88,CPI_reaction_and_GCZ26_4450_reclaim_or_4300_break_required,GCZ26_4300_4407_4450_US10Y_DXY_CPI_1d_3d,partially_verified
2026-09-11,20260911_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,55,84,,EVENT,70,85,90,52,65,58,80000_reclaim_with_ETF_reinflow_and_CME_confirmation_required,BTC_77500_80000_83000_ETF_CME_CPI_1d_3d,partially_verified
2026-09-11,20260911_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,97,57,80,,MIXED,68,82,88,56,67,59,BTC_stabilization_and_ETH_2500_reclaim_required,ETH_2400_2500_BTC_ETF_CPI_1d_3d,partially_verified
2026-09-11,20260911_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,92,88,,EVENT,96,98,99,90,92,96,pullback_below_100_or_verified_supply_deescalation_required_before_new_entry,WTI_100_102.48_105_Hormuz_RedSea_CPI_1d_3d,verified
2026-09-11,20260911_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,79,68,,EVENT,85,93,98,78,82,92,existing_sell_signals_manage_until_156.20_156.40_or_BOJ_repricing_reversal,USDJPY_152.5_154.3_156_BOJ_US10Y_CPI_1d_3d,verified
2026-09-11,20260911_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,65,81,,RISK_OFF,90,89,97,64,77,90,ESU26_reclaim_above_7665_with_US10Y_below_4.85_required,ESU26_7585_7615_7665_US10Y_WTI_CPI_1d_3d,partially_verified
2026-09-11,20260911_NASDAQ_SELL_PULLBACK,NASDAQ,SELL,B,PULLBACK,29300,29400,29620,28750,28350,2.22,0.58,0.39,99,84,47,0.25,RISK_OFF,88,91,98,84,82,92,NQU26_above_29620_or_US10Y_below_4.80_with_WTI_below_100,NQU26_29300_29620_28750_US10Y_WTI_CPI_1d_3d_5d,partially_verified
2026-09-11,20260911_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,97,57,78,,EVENT,86,88,94,55,70,88,CPI_confirmed_break_below_98.5_or_above_99.5_required,DXY_98.5_99.06_99.5_US10Y_CPI_1d_3d,verified
2026-09-11,20260911_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,86,74,,EVENT,98,97,99,85,90,99,CPI_confirmed_break_below_4.80_or_sustained_above_5.00_required,US10Y_4.80_4.95_5.00_WTI_NQ_GOLD_CPI_1d_3d,verified
2026-09-11,20260911_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,68,76,,EVENT,85,82,96,69,76,86,VIX_sustained_above_20_or_return_below_16_with_equity_confirmation_required,VIX_16_17.06_20_ES_NQ_CPI_1d_3d,partially_verified
JSON
[
  {"date":"2026-09-11","signal_id":"20260911_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":66,"no_trade_score":79,"risk_pct":null,"regime":"EVENT","ems":92,"ffs":91,"cds":98,"ias":64,"cbs":76,"mes":88,"invalidation":"CPI_reaction_and_GCZ26_4450_reclaim_or_4300_break_required","verification_target":"GCZ26_4300_4407_4450_US10Y_DXY_CPI_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-11","signal_id":"20260911_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":55,"no_trade_score":84,"risk_pct":null,"regime":"EVENT","ems":70,"ffs":85,"cds":90,"ias":52,"cbs":65,"mes":58,"invalidation":"80000_reclaim_with_ETF_reinflow_and_CME_confirmation_required","verification_target":"BTC_77500_80000_83000_ETF_CME_CPI_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-11","signal_id":"20260911_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":97,"opp_score":57,"no_trade_score":80,"risk_pct":null,"regime":"MIXED","ems":68,"ffs":82,"cds":88,"ias":56,"cbs":67,"mes":59,"invalidation":"BTC_stabilization_and_ETH_2500_reclaim_required","verification_target":"ETH_2400_2500_BTC_ETF_CPI_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-11","signal_id":"20260911_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":92,"no_trade_score":88,"risk_pct":null,"regime":"EVENT","ems":96,"ffs":98,"cds":99,"ias":90,"cbs":92,"mes":96,"invalidation":"pullback_below_100_or_verified_supply_deescalation_required_before_new_entry","verification_target":"WTI_100_102.48_105_Hormuz_RedSea_CPI_1d_3d","verified_status":"verified"},
  {"date":"2026-09-11","signal_id":"20260911_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":79,"no_trade_score":68,"risk_pct":null,"regime":"EVENT","ems":85,"ffs":93,"cds":98,"ias":78,"cbs":82,"mes":92,"invalidation":"existing_sell_signals_manage_until_156.20_156.40_or_BOJ_repricing_reversal","verification_target":"USDJPY_152.5_154.3_156_BOJ_US10Y_CPI_1d_3d","verified_status":"verified"},
  {"date":"2026-09-11","signal_id":"20260911_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":65,"no_trade_score":81,"risk_pct":null,"regime":"RISK_OFF","ems":90,"ffs":89,"cds":97,"ias":64,"cbs":77,"mes":90,"invalidation":"ESU26_reclaim_above_7665_with_US10Y_below_4.85_required","verification_target":"ESU26_7585_7615_7665_US10Y_WTI_CPI_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-11","signal_id":"20260911_NASDAQ_SELL_PULLBACK","asset":"NASDAQ","side":"SELL","rank":"B","type":"PULLBACK","entry_low":29300,"entry_high":29400,"sl":29620,"tp1":28750,"tp2":28350,"rr":2.22,"win_prob":0.58,"expected_r":0.39,"tq_score":99,"opp_score":84,"no_trade_score":47,"risk_pct":0.25,"regime":"RISK_OFF","ems":88,"ffs":91,"cds":98,"ias":84,"cbs":82,"mes":92,"invalidation":"NQU26_above_29620_or_US10Y_below_4.80_with_WTI_below_100","verification_target":"NQU26_29300_29620_28750_US10Y_WTI_CPI_1d_3d_5d","verified_status":"partially_verified"},
  {"date":"2026-09-11","signal_id":"20260911_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":97,"opp_score":57,"no_trade_score":78,"risk_pct":null,"regime":"EVENT","ems":86,"ffs":88,"cds":94,"ias":55,"cbs":70,"mes":88,"invalidation":"CPI_confirmed_break_below_98.5_or_above_99.5_required","verification_target":"DXY_98.5_99.06_99.5_US10Y_CPI_1d_3d","verified_status":"verified"},
  {"date":"2026-09-11","signal_id":"20260911_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":86,"no_trade_score":74,"risk_pct":null,"regime":"EVENT","ems":98,"ffs":97,"cds":99,"ias":85,"cbs":90,"mes":99,"invalidation":"CPI_confirmed_break_below_4.80_or_sustained_above_5.00_required","verification_target":"US10Y_4.80_4.95_5.00_WTI_NQ_GOLD_CPI_1d_3d","verified_status":"verified"},
  {"date":"2026-09-11","signal_id":"20260911_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":68,"no_trade_score":76,"risk_pct":null,"regime":"EVENT","ems":85,"ffs":82,"cds":96,"ias":69,"cbs":76,"mes":86,"invalidation":"VIX_sustained_above_20_or_return_below_16_with_equity_confirmation_required","verification_target":"VIX_16_17.06_20_ES_NQ_CPI_1d_3d","verified_status":"partially_verified"}
]

今日の実運用上のポイントは、WTIの強さを新規BUYに変換しないことと、NASDAQは29100台を追ってSELLせず、29300～29400への戻りだけを見ることです。今夜のCPIでUS10Yが5%を突破するか4.8%台へ戻るかが、次の5営業日シナリオを大きく分けます。
