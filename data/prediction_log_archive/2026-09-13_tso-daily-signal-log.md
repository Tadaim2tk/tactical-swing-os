<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-13 07:00 JST -->
<!-- transport: DOM innerText -> Blob download -> tools/archive_gpt_prose.py -->
<!-- archived_at: 2026-09-13T09:02:19Z / chars: 18818 / 値は無修正 -->

TSO Daily Signal Log v2
TSO Daily Signal Log v2 — 2026-09-13

使用モデル：GPT-5.6 Sol
本日の市場の主役：WTI
GOLD基準限月：COMEX 2026年12月限（GCZ26）
ES/NQ参照系列：ESU26 / NQU26（9月限。ロール期のため先物2系列は partially_verified）
crypto_grounds: etf=有, cme=有
expected_r_basis: subjective — 本日は新規方向あり判断を発行しないため当日TSO_LOGのexpected_rは空欄。既存BTC/NASDAQシグナルの管理では、未約定、5営業日時間決済、マクロinvalidation、週末ヘッドラインを織り込む従来のsubjective基準を維持します。

invalidation_check: 20260904_WTI_BUY_PULLBACK=not_fired, 20260905_WTI_BUY_PULLBACK=not_fired, 20260906_WTI_BUY_PULLBACK=not_fired, 20260907_WTI_BUY_PULLBACK=not_fired, 20260908_WTI_BUY_PULLBACK=not_fired, 20260908_USDJPY_SELL_PULLBACK=not_fired, 20260909_WTI_BUY_PULLBACK=not_fired, 20260909_USDJPY_SELL_PULLBACK=not_fired, 20260911_NASDAQ_SELL_PULLBACK=not_fired, 20260912_BTC_SELL_PULLBACK=not_fired

本日は日曜朝なので、WTI、GC、ES、NQ、米債、VIXなど通常の非暗号資産市場はまだ週末休場中です。CMEの通常商品は日曜17:00 CTから再開する一方、暗号資産先物は24/7取引へ移行しているため、BTC/ETHだけが週末中も新しい価格情報を形成しています。したがって非暗号資産は9月11日金曜確定値＋9月12日までの新しいニュース、Cryptoは9月13日07:00 JST直前の週末価格を使います。
CME Group
+1

1. 本日の結論

新規A級：0件
新規B級：0件
B+新規：0件

本日の10資産TSO_LOGはすべて新規NO_TRADEです。

ただしこれは「方向感がない」という意味ではありません。既存判断では、

BTC：SELL仮説継続
NASDAQ：SELL仮説継続・やや圧迫
WTI：BUY仮説群は依然生存
USDJPY：SELL仮説群は依然生存

です。

今日、新しいsignal_idを増やさない最大の理由は週明けのWTI価格形成前だからです。

9月11日のWTIは102ドル台から100.05ドルへ反落しましたが、週間では約9%上昇しました。ところが市場終了後の9月12日、サウジアラビアが東西原油パイプラインをドローン攻撃後に一時停止したとReutersが報じました。このパイプラインはホルムズ海峡を迂回する主要ルートで、能力は最大約500万bpdです。さらに月曜のオマーン協議についても、イラン側は「署名済みのホルムズ合意は想定していない」としており、別報では直ちに海峡を再開する内容でもないとされています。
Reuters
+2
Reuters
+2

つまり、

金曜終値100.05ドル
＋ 週末に供給リスク悪化
＋ 月曜の即時正常化期待は弱い

です。

これはWTI上方向の材料ですが、月曜寄り前に推測価格で新しいBUYを作るのは「供給ショック追随禁止」に反するため、今日はNO_TRADEにします。

BTCは現在およそ77250～77350ドル。昨日のSELL Entry 79200–79800には戻らず、そのまま下側にあります。したがって既存仮説は良い方向へ進んでいますが、77000ドル台からSELLを追う理由はありません。
CoinMarketCap
+1

2. 前回判断の簡易検証
20260912_BTC_SELL_PULLBACK

昨日：

Entry 79200–79800
SL 80850
TP1 76450
TP2 74800

現在BTC/USDは約77300ドルです。24時間ではほぼ横ばいですが、Entry帯には戻っていません。
CoinMarketCap
+1

したがって、

ORDER_NOT_FILLED / THESIS_MOVING_CORRECT_DIRECTION / TP1_NOT_REACHED / invalidation=not_fired

です。

ETF面でも9月11日のBTC現物ETFは約**-13.29Mドルで、規模は前3日より大幅に縮小したものの4営業日連続の純流出**でした。したがって昨日のinvalidationに含めた「fresh ETF reinflow」は発生していません。
KuCoin
+1

またBTC現物も80850を回復していないため、

20260912_BTC_SELL_PULLBACK=not_fired

と確定します。

20260911_NASDAQ_SELL_PULLBACK

既存設定：

Entry 29300–29400
SL 29620
TP1 28750
TP2 28350

NQU26の9月11日レンジは29120.75～29500.25、終値近辺は約29390～29400でした。従ってEntry到達後に反発しましたが、SL29620は未到達です。
Investing.com Nederland
+1

マクロinvalidationは、

US10Y <4.80% かつ WTI <100ドル

という組み合わせでした。

金曜は10年債利回りが一時4.979%、終盤約4.93%で、WTIも100.05ドルです。どちらも条件を満たしません。
Reuters
+1

したがって、

20260911_NASDAQ_SELL_PULLBACK=not_fired

です。

ただし金曜はS&P500 +0.86%、Nasdaq +0.96%と株式が反発し、VIXも15.59まで低下したため、SELL仮説の価格側の質は悪化しています。
Reuters
+1

WTI既存BUY群

9/4～9/9のWTI BUY群については、週末に先物価格の新しい約定はありません。

一方、価格失効水準は金曜100.05ドルから大きく下にあり、供給正常化どころか週末にサウジ東西パイプライン停止とホルムズ即時再開否定が追加されました。
Reuters
+1

したがって対象7件をすべてnot_firedとします。

USDJPY既存SELL群

9月11日のUSDJPYはデータ元で若干差がありますが、概ね153.5～153.7円で終了し、9/8シグナルの156.40、9/9シグナルの156.20には達していません。Reutersも金曜、円が約0.45%上昇して153.69付近になったと報じています。
Reuters
+1

BOJについてもReuters調査では9月18日に1.25%への25bp利上げが中心予想です。
Reuters

したがって両方ともnot_firedです。

3. 市場全体の前提

総合regimeはEVENTです。

現在の市場を整理すると、

WTI：約100ドル＋週末供給リスク再悪化
US10Y：約4.93%、一時4.979%
Fed：9月16日25bp利上げ確率約87%
BOJ：9月18日25bp利上げが中心予想
株式：金曜は反発
VIX：15.59へ低下
BTC：約77.3kで弱い
ETH：約2530でBTCより相対的に強い

という組み合わせです。Fedの利上げ織り込みは8月CPI後に約87%へ上昇しています。
The Wall Street Journal
+1

金曜だけを見ると、WTIが102.48から100.05へ下がったことで株式の安心感が戻り、S&P500とNasdaqはともに反発しました。しかし土曜にサウジの主要迂回パイプライン停止が追加されたため、金曜の株高をそのまま月曜へ延長できるかは疑問です。
Reuters
+2
Reuters
+2

これは週明けの重要な自然実験になります。

Case 1：WTIギャップ高 → US10Y再び5% → NQ反落
なら、これまで観察してきた

oil → inflation → yields → growth stocks

が再度成立します。

逆に、

WTIが上がってもUS10Y/NQが反応しない

なら、市場が供給ショックを一時的・既織り込みと判断し始めた可能性があります。

Goldは金曜、米金先物が4408.90ドル。強いCPIと高金利にもかかわらず前日から反発しました。
Reuters

USDJPYは円高、DXYは約99.1でほぼ横ばい。米金利が高いにもかかわらずドル全面高ではありません。DXYは金曜約99.11、円はReutersで153.69近辺でした。
Reuters
+1

Cryptoでは明確な分岐があります。BTC ETFは9月11日まで4日連続流出ですが、ETH ETFは複数データ会社で純流入が確認されています。ただしETHの9月11日フローは集計元によって約+49M～+216Mドルとかなり差があるため、方向は「流入」で採用しても金額は未確定扱いにします。
コインスタッツ
+2
Biturai
+2

ETH/USDは現在約2532ドル、BTC/USDは約77300ドルです。ETHは24時間で約3%上昇しており、BTCより相対的に強いですが、まだ新規BUYを発行するほど価格構造が明瞭ではありません。
CoinMarketCap
+1

4. 10資産別判断
資産	本日	判断
GOLD	NO_TRADE	GCZ26 4408.9。金利高とsafe haven反発が拮抗
BTC	NO_TRADE / 既存SELL管理	約77.3k。79200–79800まで戻らず追わない
ETH	NO_TRADE	約2532。ETF流入は強いが集計差あり
WTI	NO_TRADE / 既存BUY管理	100.05金曜終値＋週末供給悪化。月曜ギャップ待ち
USDJPY	NO_TRADE / 既存SELL管理	153円台。Fed/BOJ両方利上げ局面
SPX	NO_TRADE	ESU26約7613。金曜株高と週末原油悪化が衝突
NASDAQ	NO_TRADE / 既存SELL管理	NQU26約29390。29620までは仮説生存
DXY	NO_TRADE	約99.1。Fedタカ派でも円高
US10Y	NO_TRADE	約4.93%、5%直前
VIX	NO_TRADE	15.59。金曜は警戒後退

VIXのCboe公式遅延値は9月11日時点で**15.59、前日比-12.61%**です。
Cboe Global Markets

ESU26は遅延系列で約7613、NQU26は約29390台。NASDAQ総合やQQQをNASDAQ行の価格へ代用していません。
Tiger Brokers
+1

5. A級候補

なし。

今もっとも強い方向材料を持つのはWTIですが、価格が閉じているためEntryを定義できません。

週末ニュースだけから仮に101～103ドルでBUY Entryを作ると、月曜のギャップを推測しているだけになり、SL幅を通常より広げない・供給ショックを追わないというTSOルールに反します。

BTC SELLは既存シグナルの方向性が機能していますが、77.3kから新しくSELLすれば、昨日の79500中点に対して約2200ドル悪い価格です。

したがってA級判定以前にEntry品質で失格です。

6. B級監視候補

新規B級：なし。

ただし既存B級を2件重点監視します。

既存 BTC SELL — 20260912_BTC_SELL_PULLBACK

Entry 79200–79800
SL 80850
TP1 76450
TP2 74800

現在約77300なのでNO_CHASEです。
CoinMarketCap

昨日のEntry中点79500から現在値まで既に約-2200ドル進んでおり、ここで新しいSELLを作るとRRが大幅に劣化します。

今後79200–79800へ戻れば既存シグナルだけを評価し直します。

ただしETF流出が9月11日に-13Mドルまで縮小しているため、昨日よりSELLの需給優位は若干弱くなりました。
KuCoin

既存 NASDAQ SELL — 20260911_NASDAQ_SELL_PULLBACK

Entry 29300–29400
SL 29620
TP1 28750
TP2 28350

NQU26は金曜に約29500まで反発したものの29620未到達。
Investing.com Nederland

週末のサウジ供給障害はSELL仮説にとって再び追い風ですが、月曜寄りでNQをSELL追随しません。

見るべきは、

WTI再上昇
＋ US10Y 5%突破
＋ NQが29500を回復できない

という組み合わせです。

逆に、

NQ >29620

なら既存シグナルをfiredにします。

7. 触らない資産

最優先はWTIの月曜ギャップ追随です。

土曜に「ホルムズの代替ルート」であるサウジ東西パイプラインが停止したため、月曜寄りでは価格が大きく飛ぶ可能性があります。しかしその場合、ニュース自体は極めて強くてもEntryは悪いです。Reutersによれば同パイプラインは最大500万bpdを運べる重要ルートです。
Reuters

また月曜にはオマーン主導の協議があります。現時点では署名合意や即時ホルムズ再開は期待されていませんが、外交ヘッドライン一つで原油のリスクプレミアムが数ドル消える可能性もあります。
Reuters
+1

したがってWTIは、

上なら追わない
下なら供給正常化か単なる利確かを確認する

の二段構えです。

NASDAQも同様で、週末ニュースだけで既存SELLを増やしません。

ETHは興味深いですが、新規BUYも見送ります。BTC ETFが4日連続流出する一方、ETH ETFは流入しており相対需給は良好です。しかしETHフローの金額に集計差がある上、Fed会合直前なので、2530付近からのBUYに十分な非対称性はまだありません。
KuCoin
+2
コインスタッツ
+2

8. 後日検証ポイント

最重要は週末WTIショックを月曜市場がどう処理するかです。

サウジ東西パイプライン停止という材料にもかかわらず、

WTI <=100

なら非常に重要です。

これは「悪材料が増えても上がらない」状態であり、WTI既存BUY仮説の終盤を示す可能性があります。

逆に、

WTI >103
US10Y >5.00
NQ <29100

なら、oil-inflation-yield-equity伝播モデルをかなり強く支持します。

二番目はNASDAQ SELL。

金曜株価は反発しましたが、NQは29620を抜けていません。月曜に原油高にもかかわらず29620を突破すれば、金利・原油SELL仮説よりAI/企業収益側が強いと評価できます。

三番目はBTC。

現在約77300なので、昨日のSELLは方向としては良好です。
CoinMarketCap

BTC <76450
→ TP1到達、SELL仮説支持。

BTC >80850
→ fired。

BTC ETFが再流入へ転換＋BTC 80k回復
→ 価格SL前でも需給invalidationを再評価します。

四番目はETH/BTCです。

BTC ETFが流出なのにETH ETFが流入している状態が続き、ETHが2580～2600を維持するなら、次回はETH単独BUYまたはETH/BTC relative-strength観察を強めます。

最後が中央銀行です。

Fedは9月16日、BOJは9月18日に政策判断を予定し、市場はFed25bp利上げを約87%、Reuters調査ではBOJも25bp利上げが中心です。
The Wall Street Journal
+1

したがって今週は、通常の

US10Y↑ → USDJPY↑

が崩れる可能性が高い週です。

9. Obsidian保存用 Observation Draft
Markdown
# 2026-09-13 Weekend Supply Shock Before Monday Reopen

Model:
GPT-5.6 Sol

Market protagonist:
WTI

Gold reference:
COMEX Dec-2026 / GCZ26

Equity futures:
ESU26
NQU26

crypto_grounds:
etf=有
cme=有

expected_r_basis:
subjective

Today:
No new directional signal.

Reason:
non-crypto markets closed
Monday oil gap risk
existing BTC/NQ directional signals already active
no-chase discipline

## Regime
EVENT

## Friday references

WTI:
100.05 settle

Gold Dec:
4408.90

US10Y:
~4.93 close area
intraday high ~4.979

DXY:
~99.1

USDJPY:
~153.5-153.7

VIX:
15.59

ESU26:
~7613

NQU26:
~29390
Friday high ~29500

## Weekend crypto

BTC:
~77300

ETH:
~2532

BTC ETF Sep11:
~-13.29m
4th consecutive outflow day

ETH ETF Sep11:
positive flow
provider disagreement on amount

## Weekend oil development

Saudi East-West pipeline:
temporarily shut after drone attack

Pipeline capacity:
up to ~5 mbpd

Hormuz:
no immediate reopening agreed

Monday Oman meeting:
no signed Hormuz deal expected yet

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
20260912_BTC_SELL_PULLBACK=not_fired

## Existing directional signals

BTC SELL:
Entry 79200-79800
SL 80850
TP1 76450
TP2 74800

Current:
~77300

Status:
ORDER_NOT_FILLED
THESIS_MOVING_CORRECT_DIRECTION
NO_CHASE

NASDAQ SELL:
Entry 29300-29400
SL 29620
TP1 28750
TP2 28350

Status:
ENTRY_REACHED
ALIVE
UNDER_PRESSURE

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

## Monday primary test

Saudi pipeline shutdown
+ no immediate Hormuz reopening

-> WTI gap?

If:
WTI >103
US10Y >5.00
NQ <29100

supports:
oil -> inflation -> yields -> growth equity weakness

If:
WTI <=100 despite weekend shock

possible exhaustion / bad-news-is-priced test

## Policy week

Fed:
Sep16
hike probability ~87%

BOJ:
Sep18
25bp hike consensus

#TSO #WTI #BTC #NASDAQ #US10Y #USDJPY
10. TSO_LOG CSVとJSON
csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-13,20260913_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,65,82,,EVENT,90,91,98,63,75,89,GCZ26_break_below_4350_or_reclaim_above_4450_with_US10Y_confirmation_required,GCZ26_4350_4409_4450_US10Y_DXY_Fed_1d_3d,verified
2026-09-13,20260913_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,79,68,,MIXED,78,88,94,76,80,77,manage_existing_20260912_sell_until_80850_or_ETF_CME_reversal,BTC_76450_77300_79500_80850_ETF_CME_1d_3d,verified
2026-09-13,20260913_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,72,71,,MIXED,74,85,91,70,76,70,ETF_flow_source_reconciliation_and_2580_2600_hold_required,ETH_2480_2532_2600_ETF_ETHBTC_1d_3d,partially_verified
2026-09-13,20260913_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,94,90,,EVENT,97,99,99,91,94,97,Monday_gap_and_Hormuz_EastWest_pipeline_status_required_before_new_entry,WTI_98_100.05_103_EastWest_Hormuz_Oman_1d_3d,verified
2026-09-13,20260913_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,81,69,,EVENT,87,94,98,81,84,93,manage_existing_sell_until_156.20_156.40_or_BOJ_repricing_reversal,USDJPY_153.5_155_156.2_Fed_BOJ_1d_3d,verified
2026-09-13,20260913_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,67,78,,MIXED,84,88,96,67,77,89,ES_reopen_and_US10Y_5pct_response_required,ESU26_7585_7613_7665_WTI_US10Y_1d_3d,partially_verified
2026-09-13,20260913_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,78,73,,MIXED,87,91,98,75,80,92,manage_existing_20260911_sell_until_29620_or_macro_invalidation,NQU26_28750_29390_29620_WTI_US10Y_1d_3d,partially_verified
2026-09-13,20260913_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,58,82,,EVENT,86,89,95,55,71,89,Fed_repricing_break_below_98.7_or_above_99.5_required,DXY_98.7_99.1_99.5_US10Y_Fed_BOJ_1d_3d,verified
2026-09-13,20260913_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,88,80,,EVENT,98,98,99,86,91,99,sustained_break_above_5.00_or_reversal_below_4.85_required,US10Y_4.85_4.93_5.00_WTI_NQ_Fed_1d_3d,verified
2026-09-13,20260913_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,56,85,,MIXED,73,80,93,55,69,79,reopen_reclaim_above_18_or_hold_below_15_required,VIX_15_15.59_18_ES_NQ_WTI_1d_3d,verified
JSON
[
  {
    "date":"2026-09-13",
    "signal_id":"20260913_GOLD_NONE_NO_TRADE",
    "asset":"GOLD",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":99,
    "opp_score":65,
    "no_trade_score":82,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":90,
    "ffs":91,
    "cds":98,
    "ias":63,
    "cbs":75,
    "mes":89,
    "invalidation":"GCZ26_break_below_4350_or_reclaim_above_4450_with_US10Y_confirmation_required",
    "verification_target":"GCZ26_4350_4409_4450_US10Y_DXY_Fed_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-13",
    "signal_id":"20260913_BTC_NONE_NO_TRADE",
    "asset":"BTC",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":99,
    "opp_score":79,
    "no_trade_score":68,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":78,
    "ffs":88,
    "cds":94,
    "ias":76,
    "cbs":80,
    "mes":77,
    "invalidation":"manage_existing_20260912_sell_until_80850_or_ETF_CME_reversal",
    "verification_target":"BTC_76450_77300_79500_80850_ETF_CME_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-13",
    "signal_id":"20260913_ETH_NONE_NO_TRADE",
    "asset":"ETH",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":98,
    "opp_score":72,
    "no_trade_score":71,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":74,
    "ffs":85,
    "cds":91,
    "ias":70,
    "cbs":76,
    "mes":70,
    "invalidation":"ETF_flow_source_reconciliation_and_2580_2600_hold_required",
    "verification_target":"ETH_2480_2532_2600_ETF_ETHBTC_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-09-13",
    "signal_id":"20260913_WTI_NONE_NO_TRADE",
    "asset":"WTI",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":99,
    "opp_score":94,
    "no_trade_score":90,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":97,
    "ffs":99,
    "cds":99,
    "ias":91,
    "cbs":94,
    "mes":97,
    "invalidation":"Monday_gap_and_Hormuz_EastWest_pipeline_status_required_before_new_entry",
    "verification_target":"WTI_98_100.05_103_EastWest_Hormuz_Oman_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-13",
    "signal_id":"20260913_USDJPY_NONE_NO_TRADE",
    "asset":"USDJPY",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":99,
    "opp_score":81,
    "no_trade_score":69,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":87,
    "ffs":94,
    "cds":98,
    "ias":81,
    "cbs":84,
    "mes":93,
    "invalidation":"manage_existing_sell_until_156.20_156.40_or_BOJ_repricing_reversal",
    "verification_target":"USDJPY_153.5_155_156.2_Fed_BOJ_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-13",
    "signal_id":"20260913_SPX_NONE_NO_TRADE",
    "asset":"SPX",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":98,
    "opp_score":67,
    "no_trade_score":78,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":84,
    "ffs":88,
    "cds":96,
    "ias":67,
    "cbs":77,
    "mes":89,
    "invalidation":"ES_reopen_and_US10Y_5pct_response_required",
    "verification_target":"ESU26_7585_7613_7665_WTI_US10Y_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-09-13",
    "signal_id":"20260913_NASDAQ_NONE_NO_TRADE",
    "asset":"NASDAQ",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":99,
    "opp_score":78,
    "no_trade_score":73,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":87,
    "ffs":91,
    "cds":98,
    "ias":75,
    "cbs":80,
    "mes":92,
    "invalidation":"manage_existing_20260911_sell_until_29620_or_macro_invalidation",
    "verification_target":"NQU26_28750_29390_29620_WTI_US10Y_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-09-13",
    "signal_id":"20260913_DXY_NONE_NO_TRADE",
    "asset":"DXY",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":98,
    "opp_score":58,
    "no_trade_score":82,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":86,
    "ffs":89,
    "cds":95,
    "ias":55,
    "cbs":71,
    "mes":89,
    "invalidation":"Fed_repricing_break_below_98.7_or_above_99.5_required",
    "verification_target":"DXY_98.7_99.1_99.5_US10Y_Fed_BOJ_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-13",
    "signal_id":"20260913_US10Y_NONE_NO_TRADE",
    "asset":"US10Y",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":99,
    "opp_score":88,
    "no_trade_score":80,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":98,
    "ffs":98,
    "cds":99,
    "ias":86,
    "cbs":91,
    "mes":99,
    "invalidation":"sustained_break_above_5.00_or_reversal_below_4.85_required",
    "verification_target":"US10Y_4.85_4.93_5.00_WTI_NQ_Fed_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-13",
    "signal_id":"20260913_VIX_NONE_NO_TRADE",
    "asset":"VIX",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":99,
    "opp_score":56,
    "no_trade_score":85,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":73,
    "ffs":80,
    "cds":93,
    "ias":55,
    "cbs":69,
    "mes":79,
    "invalidation":"reopen_reclaim_above_18_or_hold_below_15_required",
    "verification_target":"VIX_15_15.59_18_ES_NQ_WTI_1d_3d",
    "verified_status":"verified"
  }
]

本日は**「方向を当てにいく日」より「月曜の価格形成を待つ日」**です。週末の情報だけならWTIの上方向材料は金曜より明確に強くなりましたが、それこそ追随を禁止すべき局面です。BTCは既存SELL仮説に対して77300ドルまで進んでいるため新しいSELLを重ねず、NASDAQも29620の既存invalidationをそのまま維持します。月曜の最重要観察は、これだけ供給ニュースが悪化してもWTIが103ドルを超えられるかです。超えられない場合は、強気材料そのものより「悪材料への価格反応低下」を重視します。
