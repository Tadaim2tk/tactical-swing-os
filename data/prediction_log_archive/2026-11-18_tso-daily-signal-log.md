<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-11-18 07:00 JST -->
<!-- transport: Complete original read_thread message c4330f5c-d577-4a2c-b3fd-8748ad72cfc0; raw markdown -->
<!-- archived_at: 2026-11-17T23:02:07Z / chars: 12982 / 値は無修正 -->

# Tactical Swing OS 日次判断 — 2026年11月18日（水）

実行モデル：GPT-6
基準時刻：2026-11-18 06:56 JST
本日の市場の主役：**NASDAQ**
市場レジーム：**RISK\_OFF / EVENT**

## 1\. 本日の結論

**A級0件、B級6件、NO\_TRADE4件。**

本日の方向性は株式・暗号資産の下落継続、ドルの相対的な強さを基本シナリオとする。最も注目するのはNASDAQの戻り売り、次いでSPXとETHの戻り売り。

ただし、米国株は既に大幅に下落しており、VIXも急上昇している。方向性の強さと新規参加の期待値は区別する。

| 優先 | 資産 | 判断 | expected\_r |
|--------|--------|--------|--------|
| 1 | NASDAQ | B・SELL | \+0.40R |
| 2 | SPX | B・SELL | \+0.34R |
| 3 | ETH | B・SELL | \+0.31R |
| 4 | GOLD | B・SELL | \+0.29R |
| 5 | DXY | B・BUY | \+0.23R |
| 6 | USDJPY | B・SELL | \+0.18R |

B+観察候補はNASDAQ、SPX、ETHの3件。いずれもA級への自動昇格は行わない。

通常リスクは1件0.25%、日次合計0.50%。相関の強いNASDAQとSPXを同時に選ぶ場合、同じ株式下落リスクへの集中として扱う。

**データ上の制限：** 11月17日の価格・市場情報を新規取得した。10資産すべてに参照基準があるが、日足ATR10の厳密な再計算、過去signal\_idの完全照合、一部の先物限月・ETFフロー確認が未完了。EntryとSLは暫定モデル値であり、全行をpartially\_verifiedとする。

## 2\. 前回判断の簡易検証

前回までの方向あり判断について、完全なsignal\_id台帳と個別invalidation水準を取得できなかった。このため、過去の判断に対して推測でfiredやnot\_firedを付けない。

市場価格としては、11月17日にES先物が7358.00、NQ先物が27102.25まで下落した。一方、VIXは26.96へ上昇。株式下落シナリオには整合的な値動きだが、過去の個別シグナルの勝敗を意味しない。citeturn382236search0turn567438view0turn382236search2

`invalidation_check: 対象signal_id未照合（過去台帳の取得不足により個別判定保留）`

これは指定形式の完全な判定行ではない。最新1件ずつのsignal\_idを確認できていないため、架空のIDを補わず未完了として記録する。

## 3\. 市場全体の前提

### 11月17日の主要参照値

| 資産 | 参照価格 | 系列 |
|--------|--------|--------|
| GOLD | 3890.92 | COMEX 2026年12月限 |
| BTC | 約63749 | BTC/USD現物 |
| ETH | 約1787 | ETH/USD現物 |
| WTI | 86.01 | WTI先物・報道上の清算値 |
| USDJPY | 約159.28 | USD/JPY |
| SPX | 7358.00 | ES 2026年12月限 |
| NASDAQ | 27102.25 | NQ 2026年12月限 |
| DXY | 103.43 | ドル指数 |
| US10Y | 約5.10% | 米10年国債利回り |
| VIX | 26.96 | Cboe VIX指数 |

出典：金・株価指数先物・VIX・為替の履歴データ、暗号資産の現物履歴、Reutersおよび債券市場報道。取得元ごとに日次区切りや更新時刻が異なる。citeturn532961search3turn455798search2turn382236search1turn532961news49turn455798search8turn382236search0turn567438view0turn455798search3turn532961news55turn382236search2

主要な市場材料は次のとおり。

- 米国株式はAI関連の不透明感と金融引き締め懸念から下落。S&amp;P500現物指数は11月17日に約1%下落した。citeturn532961news53turn532961news52
- 米10年債利回りは5.10%付近。高金利環境がグロース株・金・暗号資産の重荷となっている。citeturn532961news55turn532961news51
- WTIは中東のタンカー攻撃と供給懸念で上昇。需給見通しと地政学的供給ショックが衝突している。citeturn532961news49turn532961news50
- 11月18日は米FOMC議事要旨が重要なイベントリスク。金利・ドル・株式の短期的な方向転換に注意する。citeturn532961news51turn455798news51

## 4\. 10資産別判断

以下の価格帯は11月17日を基準にした暫定水準。ATR10は前日までの10日足を使う規則だが、今回の全系列について完全なOHLC検算を終えていない。SLが1×ATR10以上であることは最終未検証である。

| 資産 | 判断 | Entry | SL | TP1 | RR |
|--------|--------|--------|--------|--------|--------|
| GOLD | B SELL | 3890–3920 | 4010 | 3725 | 1.714 |
| BTC | NO\_TRADE | — | — | — | — |
| ETH | B SELL | 1820–1870 | 2040 | 1550 | 1.513 |
| WTI | NO\_TRADE | — | — | — | — |
| USDJPY | B SELL | 159.20–159.60 | 160.50 | 157.10 | 2.091 |
| SPX | B SELL | 7400–7480 | 7720 | 6960 | 1.714 |
| NASDAQ | B SELL | 27300–27700 | 29000 | 25000 | 1.667 |
| DXY | B BUY | 103.20–103.50 | 102.50 | 105.00 | 1.941 |
| US10Y | NO\_TRADE | — | — | — | — |
| VIX | NO\_TRADE | — | — | — | — |

RRはEntry中点とSL・TP1から再計算済み。

### GOLD

12月限GCZ26を固定基準とする。ドル高・高金利環境による下押しを基本とするが、地政学的な安全資産需要が反対方向に作用する。3890–3920への戻りを売り方向で監視。MAE想定0.35R。4010超えでシナリオ失効。FOMC議事要旨が主要イベントリスク。

### BTC

**NO\_TRADE。** BTC/USD現物は約63749ドルで、下落基調が継続。ETFフローとCME建玉・basisの当日確認が不十分で、MES43と評価する。売り方向の構造は認識するが、BTC固有の運用条件を満たさない。citeturn455798search2turn532961news57

### ETH

**B SELL。** 11月17日参照値は約1787ドル。戻り売りの監視帯1820–1870、SL2040、TP1 1550。MAE想定0.31R。BTCの急反発やETHの2040超えが失効条件。暗号資産市場全体のショートカバーに注意。

### WTI

**NO\_TRADE。** 86.01ドルを参照。中東の供給障害による急騰と、供給回復期待による反落が併存している。供給ショック直後のmomentum追随を避ける規則を適用する。citeturn532961news49turn532961news50

### USDJPY

**B SELL。** 160円付近からの反落を想定する逆張り寄りの判断。159.20–159.60を監視帯、SL160.50、TP1 157.10。MAE想定0.36R。米金利再上昇と円売り再開が主要リスク。判断日の終値までに帯へ到達しなければ終値成行という既存規則を適用する。

### SPX

**B SELL。** ES12月限7358.00を基準とする。7400–7480への戻りを売り方向で監視。SL7720、TP1 6960。MAE想定0.29R。FOMC議事要旨やAI関連材料による急反発に注意。

### NASDAQ

**B SELL・本日の最優先観察。** NQ12月限27102.25を基準とする。27300–27700を監視帯、SL29000、TP1 25000。MAE想定0.28R。既存の終値成行参加規則を適用し、Entry未到達による不参加確率はexpected\_rから控除しない。

### DXY

**B BUY。** 103.43付近を基準とする。103.20–103.50で買い方向を監視。SL102.50、TP1 105.00。MAE想定0.34R。FOMC議事要旨を受けたドル売りが主要リスク。

### US10Y

**NO\_TRADE。** 5.10%付近。高水準にあるものの、株安に伴う安全資産買いと金融引き締め見通しが反対方向に働いている。利回り方向の優位性が不足する。

### VIX

**NO\_TRADE。** 26.96まで急上昇。株式市場の不安定化を示す重要な観測指標だが、急上昇後の平均回帰リスクが大きく、新規方向判断は見送る。

## 5\. A級候補

**該当なし。**

NASDAQはCBS74、EMS67、expected\_r +0.40Rであり、A級のCBS75・expected\_r +0.45Rに届かない。

方向性が強いという理由だけでA級へ昇格させず、B級として記帳する。

## 6\. B級監視候補

B+観察候補はNASDAQ、SPX、ETH。3資産ともCBS70以上、EMS60以上、RR1.5以上、較正後参考win\_prob0.50以上を満たす。

| 資産 | CBS | EMS | RR | 生win\_prob |
|--------|--------|--------|--------|--------|
| NASDAQ | 74 | 67 | 1.667 | 0.56 |
| SPX | 73 | 65 | 1.714 | 0.55 |
| ETH | 70 | 63 | 1.513 | 0.54 |

GOLD、DXY、USDJPYもB級として記帳する。B級であることと、同時に全件へ資金を配分することは別である。

## 7\. 触らない資産

BTC、WTI、US10Y、VIXの4資産。

BTCはETF/CME確認不足、WTIは供給ショック、US10Yは方向の競合、VIXは急上昇後の不安定性を主因とする。

## 8\. 後日検証ポイント

1. NASDAQの戻り売りが5営業日の時間決済でプラスになるか。
2. NASDAQとSPXの相関を考慮した場合、どちらが高い実現Rを残すか。
3. ETHの売り方向がBTCより明確な結果を示すか。
4. GOLDの12月限において4010超えのinvalidationが発動するか。
5. FOMC議事要旨後にドル・金利・株式の方向関係が変化するか。
6. 1×ATR10の下限を実際の日足OHLCで再確認し、暫定SLの適合性を確定する。

## 9\. Obsidian保存用Observation Draft

```markdown
# TSO Observation 2026-11-18

model: GPT-6
market_leader: NASDAQ
regime: RISK_OFF / EVENT
gold_contract: GCZ26
source_date: 2026-11-17
verification: partially_verified

## Hypothesis
米国株の下落圧力が継続する。
NASDAQとSPXの戻り売りを優先観察する。
ETHも弱いが暗号資産のショートカバーに注意する。

## Signals
A: 0
B: 6
NO_TRADE: 4
B_plus: NASDAQ, SPX, ETH

## Execution
risk_per_B: 0.25%
daily_risk_cap: 0.50%
time_exit: 5_business_days
ATR10_rule: 1x_minimum
ATR10_validation: pending

## Outstanding
previous_signal_invalidation: unresolved
historical_signal_ids: not_retrieved
ETF_CME_flow: incomplete
```

## 10\. TSO\_LOG

CSVは固定28列、10資産10行。全データ行27カンマを検算済み。B級のRRもEntry中点から計算済み。

### CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-11-18,20261118_GOLD_SELL_PULLBACK,GOLD,SELL,B,PULLBACK,3890,3920,4010,3725,3600,1.714,0.53,0.29,67,66,35,0.25,EVENT,62,55,61,57,69,61,GCZ26_above_4010,GCZ26_daily_OHLC_ATR10,partially_verified
2026-11-18,20261118_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,65,48,81,,RISK_OFF,51,38,59,42,58,43,ETF_CME_confirmation_missing,BTCUSD_spot_ETF_CME,partially_verified
2026-11-18,20261118_ETH_SELL_PULLBACK,ETH,SELL,B,PULLBACK,1820,1870,2040,1550,1430,1.513,0.54,0.31,70,65,38,0.25,RISK_OFF,63,49,62,55,70,54,ETHUSD_above_2040,ETHUSD_daily_OHLC_ATR10,partially_verified
2026-11-18,20261118_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,52,38,85,,EVENT,35,40,37,30,39,44,Hormuz_supply_shock,CL_futures_OHLC_inventory,partially_verified
2026-11-18,20261118_USDJPY_SELL_REVERSAL,USDJPY,SELL,B,REVERSAL,159.2,159.6,160.5,157.1,156.1,2.091,0.51,0.18,62,59,48,0.25,EVENT,58,52,58,49,64,54,USDJPY_above_160.5,USDJPY_daily_OHLC_ATR10,partially_verified
2026-11-18,20261118_SPX_SELL_PULLBACK,SPX,SELL,B,PULLBACK,7400,7480,7720,6960,6800,1.714,0.55,0.34,73,69,33,0.25,RISK_OFF,65,58,65,58,73,65,ESZ26_above_7720,ESZ26_daily_OHLC_ATR10,partially_verified
2026-11-18,20261118_NASDAQ_SELL_PULLBACK,NASDAQ,SELL,B,PULLBACK,27300,27700,29000,25000,24000,1.667,0.56,0.4,77,73,29,0.25,EVENT,67,59,66,57,74,66,NQZ26_above_29000,NQZ26_daily_OHLC_ATR10,partially_verified
2026-11-18,20261118_DXY_BUY_PULLBACK,DXY,BUY,B,PULLBACK,103.2,103.5,102.5,105.0,105.8,1.941,0.52,0.23,65,59,44,0.25,MIXED,59,55,56,53,65,59,DXY_below_102.5,DXY_daily_OHLC_ATR10,partially_verified
2026-11-18,20261118_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,49,38,71,,MIXED,46,48,42,40,48,50,yield_direction_mixed,US10Y_yield_daily,partially_verified
2026-11-18,20261118_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,59,39,82,,EVENT,43,45,44,33,46,53,VIX_spike_event,VIX_cash_index_daily,partially_verified
```

### JSON

```json
[
  {"date":"2026-11-18","signal_id":"20261118_GOLD_SELL_PULLBACK","asset":"GOLD","side":"SELL","rank":"B","type":"PULLBACK","entry_low":3890,"entry_high":3920,"sl":4010,"tp1":3725,"tp2":3600,"rr":1.714,"win_prob":0.53,"expected_r":0.29,"tq_score":67,"opp_score":66,"no_trade_score":35,"risk_pct":0.25,"regime":"EVENT","ems":62,"ffs":55,"cds":61,"ias":57,"cbs":69,"mes":61,"invalidation":"GCZ26_above_4010","verification_target":"GCZ26_daily_OHLC_ATR10","verified_status":"partially_verified"},
  {"date":"2026-11-18","signal_id":"20261118_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":65,"opp_score":48,"no_trade_score":81,"risk_pct":"","regime":"RISK_OFF","ems":51,"ffs":38,"cds":59,"ias":42,"cbs":58,"mes":43,"invalidation":"ETF_CME_confirmation_missing","verification_target":"BTCUSD_spot_ETF_CME","verified_status":"partially_verified"},
  {"date":"2026-11-18","signal_id":"20261118_ETH_SELL_PULLBACK","asset":"ETH","side":"SELL","rank":"B","type":"PULLBACK","entry_low":1820,"entry_high":1870,"sl":2040,"tp1":1550,"tp2":1430,"rr":1.513,"win_prob":0.54,"expected_r":0.31,"tq_score":70,"opp_score":65,"no_trade_score":38,"risk_pct":0.25,"regime":"RISK_OFF","ems":63,"ffs":49,"cds":62,"ias":55,"cbs":70,"mes":54,"invalidation":"ETHUSD_above_2040","verification_target":"ETHUSD_daily_OHLC_ATR10","verified_status":"partially_verified"},
  {"date":"2026-11-18","signal_id":"20261118_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":52,"opp_score":38,"no_trade_score":85,"risk_pct":"","regime":"EVENT","ems":35,"ffs":40,"cds":37,"ias":30,"cbs":39,"mes":44,"invalidation":"Hormuz_supply_shock","verification_target":"CL_futures_OHLC_inventory","verified_status":"partially_verified"},
  {"date":"2026-11-18","signal_id":"20261118_USDJPY_SELL_REVERSAL","asset":"USDJPY","side":"SELL","rank":"B","type":"REVERSAL","entry_low":159.2,"entry_high":159.6,"sl":160.5,"tp1":157.1,"tp2":156.1,"rr":2.091,"win_prob":0.51,"expected_r":0.18,"tq_score":62,"opp_score":59,"no_trade_score":48,"risk_pct":0.25,"regime":"EVENT","ems":58,"ffs":52,"cds":58,"ias":49,"cbs":64,"mes":54,"invalidation":"USDJPY_above_160.5","verification_target":"USDJPY_daily_OHLC_ATR10","verified_status":"partially_verified"},
  {"date":"2026-11-18","signal_id":"20261118_SPX_SELL_PULLBACK","asset":"SPX","side":"SELL","rank":"B","type":"PULLBACK","entry_low":7400,"entry_high":7480,"sl":7720,"tp1":6960,"tp2":6800,"rr":1.714,"win_prob":0.55,"expected_r":0.34,"tq_score":73,"opp_score":69,"no_trade_score":33,"risk_pct":0.25,"regime":"RISK_OFF","ems":65,"ffs":58,"cds":65,"ias":58,"cbs":73,"mes":65,"invalidation":"ESZ26_above_7720","verification_target":"ESZ26_daily_OHLC_ATR10","verified_status":"partially_verified"},
  {"date":"2026-11-18","signal_id":"20261118_NASDAQ_SELL_PULLBACK","asset":"NASDAQ","side":"SELL","rank":"B","type":"PULLBACK","entry_low":27300,"entry_high":27700,"sl":29000,"tp1":25000,"tp2":24000,"rr":1.667,"win_prob":0.56,"expected_r":0.4,"tq_score":77,"opp_score":73,"no_trade_score":29,"risk_pct":0.25,"regime":"EVENT","ems":67,"ffs":59,"cds":66,"ias":57,"cbs":74,"mes":66,"invalidation":"NQZ26_above_29000","verification_target":"NQZ26_daily_OHLC_ATR10","verified_status":"partially_verified"},
  {"date":"2026-11-18","signal_id":"20261118_DXY_BUY_PULLBACK","asset":"DXY","side":"BUY","rank":"B","type":"PULLBACK","entry_low":103.2,"entry_high":103.5,"sl":102.5,"tp1":105.0,"tp2":105.8,"rr":1.941,"win_prob":0.52,"expected_r":0.23,"tq_score":65,"opp_score":59,"no_trade_score":44,"risk_pct":0.25,"regime":"MIXED","ems":59,"ffs":55,"cds":56,"ias":53,"cbs":65,"mes":59,"invalidation":"DXY_below_102.5","verification_target":"DXY_daily_OHLC_ATR10","verified_status":"partially_verified"},
  {"date":"2026-11-18","signal_id":"20261118_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":49,"opp_score":38,"no_trade_score":71,"risk_pct":"","regime":"MIXED","ems":46,"ffs":48,"cds":42,"ias":40,"cbs":48,"mes":50,"invalidation":"yield_direction_mixed","verification_target":"US10Y_yield_daily","verified_status":"partially_verified"},
  {"date":"2026-11-18","signal_id":"20261118_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":59,"opp_score":39,"no_trade_score":82,"risk_pct":"","regime":"EVENT","ems":43,"ffs":45,"cds":44,"ias":33,"cbs":46,"mes":53,"invalidation":"VIX_spike_event","verification_target":"VIX_cash_index_daily","verified_status":"partially_verified"}
]
```

**本日の最終判断：NASDAQの売り方向を第一候補として継続観察。** A級への昇格はせず、B級6件を記録する。翌朝は価格更新に加えて、過去signal\_idのinvalidation照合とATR10の確定が重要な検証作業となる。
