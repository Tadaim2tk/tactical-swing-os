<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-16 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-21T12:59:52Z / chars: 18119 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-09-16

**使用モデル：GPT-5.6 Sol**  
**本日の市場の主役：WTI**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**データ基準：2026年9月15日米国市場終了〜9月16日06:59 JST**  
**crypto_grounds: etf=有, cme=有**  
**expected_r_basis: subjective** — 本日は新規方向あり判断を発行しないため、当日LOGの`expected_r`は空欄。既存判断では、5営業日時間決済、未約定確率、FOMCイベント、シナリオ崩壊時の早期撤退を含むsubjective基準を維持します。

**invalidation_check: 20260909_WTI_BUY_PULLBACK=not_fired, 20260909_USDJPY_SELL_PULLBACK=not_fired, 20260912_BTC_SELL_PULLBACK=unknown**

9/9の2件は**本日が5営業日後の最終確認日**です。9/11 NASDAQ SELLは、実取引が約定後に含み益となり、利益側へ移動したSLでプラス決済済みとの申告があるため、未決着リストから除外しました。

BTCだけ`unknown`なのは、価格側の`BTC > 80850`は明確に未発火ですが、もう一つの条件`fresh_ETF_reinflow_with_CME_reclaim`について、9/14にBTC ETFが**+159.9Mドルへ再流入**した一方、「CME reclaim」の数値閾値を元シグナルで定義していなかったためです。CME BTCは9/14高値79,760、9/15終値77,495で、80kを明確に奪回した形ではありませんが、定義されていない条件をこちらで後付けせず`unknown`とします。citeturn488422search0turn488422search2

## 1. 本日の結論

**新規A級：0件**  
**新規B級：0件**  
**新規B+：0件**  
**10資産すべて新規NO_TRADE**

今日は方向感がないからではなく、**FOMC直前なので良い方向と良い取引を分離**します。

9月15日のWTIは**105.83ドル**まで上昇し、Brentは108.75ドル。サウジYanbuでの積み出し停止、東西パイプライン障害、Libyaの3油田停止など、供給側はむしろ悪化しています。citeturn385372news33

米10年債利回りは一時**5.041%**と2007年以来の高水準、終盤も約5.00%。DXYは約99.63。USDJPYも155円を一時突破しました。citeturn385372view2turn385372view3

株式はS&P500 -0.45%、Nasdaq -0.78%。NQZ26も9/15は**29229**まで下落しました。citeturn385372view1turn923802search8

ただしFOMC声明は**9月16日14:00 ET＝9月17日03:00 JST**、会見は03:30 JSTです。市場は約94〜95%の確率で25bp利上げを織り込んでいます。citeturn579742search0turn385372view1

urlFederal Reserve：2026年9月FOMC日程turn579742search0  
urlReuters：9月15日の原油市場turn385372news33  
urlReuters：米10年債5%突破と為替turn385372view2

したがって、**WTI BUY、債券SELL、NASDAQ SELL、Gold SELLをFOMC直前に追いかけることはしません。**

また、TSO上の**予約Entry待ちは現時点で0件**へ修正します。理由は次節のBTC再検証です。

## 2. 前回判断の簡易検証

### 重要修正：20260912_BTC_SELL_PULLBACK

設定は、

**Entry 79200–79800  
SL 80850  
TP1 76450  
TP2 74800**

でした。

これまで「Entry未到達」と扱っていましたが、今回新規取得したBTC/USD日次データでは、**9月14日の高値が79,550〜79,600ドル**でした。Entry帯79,200〜79,800へ明確に入っています。citeturn897055search3turn897055search4

さらに9月15日は、

**BTC/USD安値：約75,057〜75,605**  
**CME BTC終値：77,495**  
**Reuters記事中：約75,320**

まで下落しています。citeturn897055search3turn897055search4turn488422search2turn385372view2

したがってTSO検証上は、前日の

**ORDER_NOT_FILLED**

を訂正して、

**ENTRY_REACHED / TP1_REACHED / TP2_NOT_REACHED**

です。

TP1は76450なので、日中安値75k台で到達しています。

これは重要な訂正です。**TSO上のBTC予約指値はもう「約定待ち」ではありません。**

ただし、実際のXM等の注文が約定していたかはユーザーから申告されていないため、これはあくまで**TSOシグナルの価格経路上の判定**です。

invalidation自体は前述のETF/CME条件が曖昧なので、本日は`unknown`を維持します。

### 20260911_NASDAQ_SELL_PULLBACK

これは実取引結果が確定しています。

**Entry：約定  
→ 含み益  
→ SLを利益側へ変更  
→ 変更後SLにヒット  
→ プラス決済  
→ 想定利益のおよそ半分**

したがって、

**CLOSED_PROFIT / EARLY_EXIT_BY_ADJUSTED_SL**

として扱い、今日から`invalidation_check`対象外です。

研究上は「方向は合っていたが、利益保護SLで5営業日の方向エッジを途中で切った」というケースとして残します。

### 20260909_WTI_BUY_PULLBACK

既存Entryは91.80–92.50でしたが、9/15 WTIは105ドル台まで上昇。供給正常化も起きておらず、むしろYanbu積み出し停止やLibya供給障害が追加されています。citeturn385372news33

したがって、

**ORDER_NOT_FILLED / THESIS_STRONGLY_CORRECT_DIRECTION / not_fired**

です。

本日で5営業日確認を終了します。

### 20260909_USDJPY_SELL_PULLBACK

設定：

**Entry 154.80–155.40  
SL 156.20  
TP1 152.50**

9/15のUSDJPYは**154.40〜155.23**程度で推移し、Entry帯には入っていますが156.20には到達していません。citeturn923802search1turn923802search2

BOJは9月18日に1.25%への25bp利上げが中心予想で、円高側の政策仮説もまだ消えていません。citeturn153565news2

したがって、

**ENTRY_REACHED / SL_NOT_REACHED / not_fired**

です。

これも本日が5営業日後の最終確認日です。

## 3. 市場全体の前提

本日の総合regimeは**EVENT / RISK_OFF寄り**です。

上流は依然、

**中東供給障害  
→ WTI 105.83  
→ インフレ期待  
→ US10Y 5.0%  
→ Fed利上げ  
→ Growth株・Crypto圧力**

です。

WTIは9/15に4%以上上昇して105.83ドル。サウジが一部欧州向けカーゴをキャンセルし、Yanbu積み出しも停止したとReutersが報じています。citeturn385372news33

米10年債は5.041%まで上昇し、終盤も5%近辺。Fed利上げ確率は94〜95%です。citeturn385372view2turn385372view3

Goldはこの環境で弱く、Reutersの米金先物は**4332.80ドル**。GCZ26の別データでは**4337ドル前後**なので、方向は一致していますが数ドルの差があり`partially_verified`とします。citeturn385372news32turn986753search4

DXYは99.63近辺。USDJPYは155円前後で、Fed利上げ期待によるドル高がBOJ利上げ期待を一時的に上回っています。citeturn385372view2

ESZ26は**7666前後**、NQZ26は**29229前後**。NQは9/14の29449からさらに下落しました。citeturn700491search7turn923802search8

Cryptoも弱いです。BTC/USDはデータ時点差がありますが約**75.3k〜76.0k**、ETH/USDは概ね**2.40〜2.43k**。CME BTCは77,495、CME ETHは2,411.5で終了しています。citeturn385372view2turn897055search3turn897055search2turn488422search2turn488422search6

一方でBTC ETFは9/14に+159.9Mドルへ反転しており、**価格下落に対してETF需要は完全には崩れていません**。これはBTC SELLを新しく追加しない理由の一つです。citeturn488422search0

VIXは公式EOD更新が遅れていますが、最新のイントラデイ参照は**17.5前後**。20超のパニックではないものの、15台前半の静かな市場でもありません。citeturn324048search0

## 4. 10資産別判断

| 資産 | 本日判断 | 基準値・判断 |
|---|---|---|
| GOLD | **NO_TRADE** | GCZ26 約4337。SELL方向だがFOMC直前で追わない |
| BTC | **NO_TRADE** | 約75.3–76.0k。既存SELLはTP1到達、追加SELL禁止 |
| ETH | **NO_TRADE** | 約2.40–2.43k。下落したがETF需給との乖離あり |
| WTI | **NO_TRADE** | 105.83。供給ショック追随禁止 |
| USDJPY | **NO_TRADE** | 約155.1。既存SELL最終日、FOMC→BOJ待ち |
| SPX | **NO_TRADE** | ESZ26約7666。FOMC直前 |
| NASDAQ | **NO_TRADE** | NQZ26約29229。既存実取引は決済済み |
| DXY | **NO_TRADE** | 約99.63。利上げほぼ織り込み済み |
| US10Y | **NO_TRADE** | 約5.00%、高値5.041。5%突破を追わない |
| VIX | **NO_TRADE** | 約17.5。FOMC前の中間域 |

特にNASDAQについては、**QQQやNASDAQ Compositeを価格参照に使っていません**。今日の行はNQZ26です。citeturn923802search8

## 5. A級候補

**なし。**

方向確信だけなら、

**WTI BUY**  
**US10Y上昇**  
**NASDAQ SELL**  
**GOLD SELL**

の4つはかなり強いです。

しかしA級条件は方向の強さだけではなく、

**Entry品質  
RR  
MAE  
イベントリスク  
実損制約**

を満たす必要があります。

FOMCまで約20時間しかない現在、新規ポジションを作ると、通常の5営業日スイングではなく**FOMC結果への賭け**になります。

特にWTIは105ドル超を買えば供給ショック追随、US10Yは5%超を追えば金利上昇追随、NQを29200台で売れば既に2日下落後の追随です。

すべてEntry品質でA級失格です。

## 6. B級監視候補

**新規B級：なし。**

既存で見るのは2件だけです。

`20260909_USDJPY_SELL_PULLBACK`は本日最終日。

**Entry 154.80–155.40  
SL 156.20  
TP1 152.50**

現在約155.1なのでEntry帯内です。ただしFOMCの直後にBOJも控えるため、新しいUSDJPY SELLを追加しません。

`20260912_BTC_SELL_PULLBACK`は、今回の再取得で**Entry到達＋TP1到達**へ修正されました。

**Entry 79200–79800  
SL 80850  
TP1 76450 ← 到達済み  
TP2 74800 ← 未到達**

現在値付近からさらにSELLを重ねるのは完全な追随なので禁止です。

また、以前「唯一の予約約定待ち」としたBTCについても、価格履歴を再検証した結果、**TSO上では予約待ちではなくEntry到達済み**です。

## 7. 触らない資産

今日は特に**WTI、US10Y、NASDAQ、GOLD**を触りません。

WTIは105.83。供給障害は本物ですが、ここで買うとニュースを見てから買うことになります。citeturn385372news33

US10Yは5.04%まで到達しました。利上げがほぼ織り込まれた状態なので、FOMCで25bp上げても利回りが逆に低下する「事実売り」は十分あり得ます。

NASDAQも同じです。金利5%・原油106ドル・FOMC利上げという悪材料はかなり価格に入っています。NQZ26は9/15だけで0.75%下落しています。citeturn923802search8

GOLDは高金利・ドル高で弱いですが、FOMCが想定ほどタカ派でなければ、金利低下と地政学需要が同時に入る可能性があります。

つまり今日は、**方向を当ててもエントリーの期待値が悪い日**です。

## 8. 後日検証ポイント

最優先はFOMC後の**US10Yの反応**です。

Federal Reserveの公式日程では、政策声明は9月16日14:00 ET、会見は14:30 ETです。citeturn579742search0

25bp利上げ後に、

**US10Y >5.05維持  
＋ NQZ26 <29000**

なら、今回の利上げが単なる織り込み済みではなく、新しい引き締め局面として価格形成されていると判断します。

逆に、

**US10Y <4.90  
＋ NQZ26 >29500**

なら、「利上げは既に十分織り込まれていた」というシナリオを支持します。

第二はWTI。

現在105.83なので、

**108〜110定着**

なら供給ショックが新しい価格帯へ移行。

一方、

**供給障害継続なのに103以下へ戻る**

ならbad-news exhaustionを疑います。

第三はUSDJPY。

FOMC後にドル金利が上がっても、

**USDJPYが156.20を突破できない**

なら、9/9 SELLのinvalidation設計はかなり良かったと評価できます。

その後9月18日のBOJで1.25%利上げが実現するかも重要です。Reuters調査では利上げが中心予想です。citeturn153565news2

第四はBTC。

今回、非常に重要な教師データが得られました。

**9/12 SELL発行  
→ 9/14 Entry到達  
→ 9/15 TP1到達**

です。

一方で同時期にETFは+159.9Mドルへ再流入しました。citeturn488422search0

つまり、

**ETFフロー改善 ≠ 短期価格反転**

だった可能性があります。

ここは今後、ETF単独でinvalidationにするのではなく、価格/CME confirmationとのAND条件を数値で定義すべき候補です。

特に今回の`CME reclaim`には**数値閾値がなかったためinvalidation判定がunknownになった**ので、研究上の改善点として残します。

## 9. Obsidian保存用 Observation Draft

```markdown
# 2026-09-16 Pre-FOMC / Oil 106 / BTC TP1 Hit

Model:
GPT-5.6 Sol

Market protagonist:
WTI

Gold reference:
COMEX Dec-2026 / GCZ26

Equity futures:
ESZ26
NQZ26

crypto_grounds:
etf=有
cme=有

expected_r_basis:
subjective

Today:
NO NEW DIRECTIONAL SIGNAL

Reason:
FOMC in ~20 hours
oil supply shock already extended
US10Y already at 5%
NQ already sold off
no-chase rule

## Regime

EVENT
RISK_OFF bias

## Market

WTI:
105.83 Reuters settle

Brent:
108.75

US10Y:
~5.00
intraday high 5.041

DXY:
~99.63

USDJPY:
~155.1
intraday high ~155.23

GCZ26:
~4337
Reuters US gold futures ~4332.8
partially_verified

ESZ26:
~7666

NQZ26:
~29229

VIX:
~17.5 delayed/intraday

BTC spot:
~75.3-76.0k

CME BTC:
77495

ETH spot:
~2.40-2.43k

CME ETH:
2411.5

## Crypto flow

BTC ETF Sep14:
+159.9m

ETF flow reversed positive
but BTC price subsequently fell.

## Important correction

20260912_BTC_SELL_PULLBACK

Entry:
79200-79800

Sep14 BTC high:
~79550-79600

Therefore:
ENTRY_REACHED

Sep15 BTC low:
~75057-75605

TP1:
76450

Therefore:
TP1_REACHED

TP2:
74800
NOT reached

Previous ORDER_NOT_FILLED classification:
CORRECTED

## NASDAQ actual trade

20260911_NASDAQ_SELL_PULLBACK

Actual:
ENTRY_FILLED
moved SL into profit
stopped out at profit
realized approximately half of planned profit

Status:
CLOSED_PROFIT
EARLY_EXIT_BY_ADJUSTED_SL

Remove from invalidation_check.

## Invalidation

20260909_WTI_BUY_PULLBACK=not_fired
20260909_USDJPY_SELL_PULLBACK=not_fired
20260912_BTC_SELL_PULLBACK=unknown

Sep9 signals:
final check day.

BTC unknown reason:
price invalidation not fired
ETF reinflow occurred
"CME reclaim" threshold was not numerically defined

## Pending entry orders

TSO pending-entry candidates:
0

BTC was previously listed as pending,
but historical recheck shows Entry band was reached Sep14.

## FOMC

Sep16 14:00 ET
Sep17 03:00 JST

Market:
~94-95% probability of 25bp hike

## BOJ

Sep18
25bp hike to 1.25% consensus

## Primary test

Post-FOMC:

If:
US10Y >5.05
NQZ26 <29000

supports:
new tightening / risk-off regime

If:
US10Y <4.90
NQZ26 >29500

supports:
hike already priced

## Oil test

WTI >108-110:
supply shock re-acceleration

WTI <103 while disruption persists:
bad-news exhaustion

#TSO #FOMC #WTI #US10Y #NASDAQ #BTC #USDJPY
```

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-16,20260916_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,78,86,,EVENT,96,94,99,75,81,95,post_FOMC_GCZ26_reclaim_above_4380_or_break_below_4290_with_yield_confirmation_required,GCZ26_4290_4337_4380_US10Y_DXY_FOMC_1d_3d,partially_verified
2026-09-16,20260916_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,82,78,,RISK_OFF,84,92,96,80,82,79,post_FOMC_BTC_reclaim_79500_or_break_74800_with_ETF_CME_confirmation_required,BTC_74800_76450_76000_79500_80850_ETF_CME_FOMC_1d_3d,partially_verified
2026-09-16,20260916_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,76,82,,RISK_OFF,82,90,95,73,78,76,post_FOMC_ETH_reclaim_2500_2600_or_break_2350_required,ETH_2350_2410_2500_2600_ETF_CME_FOMC_1d_3d,partially_verified
2026-09-16,20260916_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,97,92,,EVENT,99,99,99,94,96,99,post_FOMC_pullback_below_103_or_clean_hold_above_108_required_before_new_signal,WTI_103_105.83_108_110_Yanbu_Hormuz_FOMC_1d_3d,verified
2026-09-16,20260916_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,86,79,,EVENT,92,96,99,84,88,96,post_FOMC_then_BOJ_reaction_required_before_new_signal,USDJPY_152.5_155.1_156.2_FOMC_BOJ_1d_3d,verified
2026-09-16,20260916_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,80,86,,RISK_OFF,93,92,98,78,83,95,post_FOMC_ESZ26_break_below_7600_or_reclaim_above_7720_required,ESZ26_7600_7666_7720_US10Y_WTI_FOMC_1d_3d,partially_verified
2026-09-16,20260916_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,86,87,,RISK_OFF,95,94,99,84,87,96,post_FOMC_NQZ26_break_below_29000_or_reclaim_above_29500_required,NQZ26_29000_29229_29500_US10Y_WTI_FOMC_1d_3d,partially_verified
2026-09-16,20260916_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,74,82,,EVENT,91,92,97,71,78,94,post_FOMC_break_below_99.0_or_above_100.0_required,DXY_99_99.63_100_US10Y_USDJPY_FOMC_1d_3d,verified
2026-09-16,20260916_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,96,92,,EVENT,99,99,99,94,96,99,post_FOMC_hold_above_5.05_or_reversal_below_4.90_required,US10Y_4.90_5.00_5.041_NQ_GOLD_WTI_FOMC_1d_3d,verified
2026-09-16,20260916_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,70,81,,RISK_OFF,87,85,97,69,76,89,post_FOMC_break_above_20_or_return_below_16_required,VIX_16_17.5_20_ES_NQ_FOMC_1d_3d,partially_verified
```

### TSO_LOG JSON

```json
[
  {"date":"2026-09-16","signal_id":"20260916_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":78,"no_trade_score":86,"risk_pct":null,"regime":"EVENT","ems":96,"ffs":94,"cds":99,"ias":75,"cbs":81,"mes":95,"invalidation":"post_FOMC_GCZ26_reclaim_above_4380_or_break_below_4290_with_yield_confirmation_required","verification_target":"GCZ26_4290_4337_4380_US10Y_DXY_FOMC_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-16","signal_id":"20260916_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":82,"no_trade_score":78,"risk_pct":null,"regime":"RISK_OFF","ems":84,"ffs":92,"cds":96,"ias":80,"cbs":82,"mes":79,"invalidation":"post_FOMC_BTC_reclaim_79500_or_break_74800_with_ETF_CME_confirmation_required","verification_target":"BTC_74800_76450_76000_79500_80850_ETF_CME_FOMC_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-16","signal_id":"20260916_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":76,"no_trade_score":82,"risk_pct":null,"regime":"RISK_OFF","ems":82,"ffs":90,"cds":95,"ias":73,"cbs":78,"mes":76,"invalidation":"post_FOMC_ETH_reclaim_2500_2600_or_break_2350_required","verification_target":"ETH_2350_2410_2500_2600_ETF_CME_FOMC_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-16","signal_id":"20260916_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":97,"no_trade_score":92,"risk_pct":null,"regime":"EVENT","ems":99,"ffs":99,"cds":99,"ias":94,"cbs":96,"mes":99,"invalidation":"post_FOMC_pullback_below_103_or_clean_hold_above_108_required_before_new_signal","verification_target":"WTI_103_105.83_108_110_Yanbu_Hormuz_FOMC_1d_3d","verified_status":"verified"},
  {"date":"2026-09-16","signal_id":"20260916_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":86,"no_trade_score":79,"risk_pct":null,"regime":"EVENT","ems":92,"ffs":96,"cds":99,"ias":84,"cbs":88,"mes":96,"invalidation":"post_FOMC_then_BOJ_reaction_required_before_new_signal","verification_target":"USDJPY_152.5_155.1_156.2_FOMC_BOJ_1d_3d","verified_status":"verified"},
  {"date":"2026-09-16","signal_id":"20260916_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":80,"no_trade_score":86,"risk_pct":null,"regime":"RISK_OFF","ems":93,"ffs":92,"cds":98,"ias":78,"cbs":83,"mes":95,"invalidation":"post_FOMC_ESZ26_break_below_7600_or_reclaim_above_7720_required","verification_target":"ESZ26_7600_7666_7720_US10Y_WTI_FOMC_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-16","signal_id":"20260916_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":86,"no_trade_score":87,"risk_pct":null,"regime":"RISK_OFF","ems":95,"ffs":94,"cds":99,"ias":84,"cbs":87,"mes":96,"invalidation":"post_FOMC_NQZ26_break_below_29000_or_reclaim_above_29500_required","verification_target":"NQZ26_29000_29229_29500_US10Y_WTI_FOMC_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-16","signal_id":"20260916_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":74,"no_trade_score":82,"risk_pct":null,"regime":"EVENT","ems":91,"ffs":92,"cds":97,"ias":71,"cbs":78,"mes":94,"invalidation":"post_FOMC_break_below_99.0_or_above_100.0_required","verification_target":"DXY_99_99.63_100_US10Y_USDJPY_FOMC_1d_3d","verified_status":"verified"},
  {"date":"2026-09-16","signal_id":"20260916_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":96,"no_trade_score":92,"risk_pct":null,"regime":"EVENT","ems":99,"ffs":99,"cds":99,"ias":94,"cbs":96,"mes":99,"invalidation":"post_FOMC_hold_above_5.05_or_reversal_below_4.90_required","verification_target":"US10Y_4.90_5.00_5.041_NQ_GOLD_WTI_FOMC_1d_3d","verified_status":"verified"},
  {"date":"2026-09-16","signal_id":"20260916_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":70,"no_trade_score":81,"risk_pct":null,"regime":"RISK_OFF","ems":87,"ffs":85,"cds":97,"ias":69,"cbs":76,"mes":89,"invalidation":"post_FOMC_break_above_20_or_return_below_16_required","verification_target":"VIX_16_17.5_20_ES_NQ_FOMC_1d_3d","verified_status":"partially_verified"}
]
```

今日の主要な更新は2つです。**BTC SELLは再取得した9/14高値を確認するとEntry帯へ到達しており、9/15にはTP1まで到達していたため、従来の「予約約定待ち」判定を訂正**します。そしてNASDAQ実取引はユーザー申告どおり利益決済済みなので、未決着invalidationから除外しました。

今日の新規売買を0件にする最大の理由は、**約20時間後にFOMCがあり、WTI106ドル・10年債5%・NQ29200という現在地からポジションを追うと、5営業日スイングではなくイベントトレードになるため**です。
