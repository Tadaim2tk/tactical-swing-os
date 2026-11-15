<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-11-16 07:00 JST -->
<!-- transport: Complete original read_thread message f654ec69-f34c-4be5-9c78-542857792040; raw markdown -->
<!-- archived_at: 2026-11-15T23:06:13Z / chars: 12444 / 値は無修正 -->

# Tactical Swing OS v2 — 2026年11月16日（月）

実行モデル：GPT-6
評価時刻：日本時間 07:00頃
本日の市場の主役：**BTC**
市場レジーム：MIXED（暗号資産はRISK\_OFF）
運用モード：通常寄り防御

## 1\. 本日の結論

**A級0件、B級4件、NO\_TRADE 6件。**

週末の暗号資産急落とドル高・米金利上昇が主要テーマです。BTCは週末に一時61,946ドルまで下落したとの報道があり、その後65,000ドル近辺へ反発しています。Coinbaseの取得時表示は65,045ドル付近でした。ただし、表示価格の厳密な取得時刻は確定できません。citeturn720914news8turn720914news4

本日の方向判断は、GOLD売り、ETH売り、WTI売り、USDJPY買いです。前日までの方向性を機械的に継続したのではなく、WTIについては供給余剰の新しい材料を踏まえてB級に変更します。

| 優先 | 資産 | 判断 | RR | expected\_r |
|--------|--------|--------|--------|--------|
| 1 | USDJPY | B BUY | 1.615 | \+0.34R |
| 2 | ETH | B SELL | 1.500 | \+0.27R |
| 3 | GOLD | B SELL | 1.647 | \+0.26R |
| 4 | WTI | B SELL | 1.571 | \+0.17R |

B+観察候補はUSDJPYのみです。CBS72、EMS63、RR1.615、較正後参考勝率0.54で条件を満たします。

**重要な制限：** 今回も10本分の完全な日足OHLCを取得できず、ATR10下限の実測検証は未完了です。したがって、B級の価格計画は暫定値であり、A級は認定しません。これは方向判断を停止する理由ではなく、執行前に残る検証項目です。

## 2\. 前回判断の簡易検証

11月15日のGOLD SELL、ETH SELL、および11月14日のBTC SELL、USDJPY BUYを、各資産の最新の方向あり判断として確認します。

| signal\_id | 無効化水準 | 今回の判定 |
|--------|--------|--------|
| 20261115\_GOLD\_SELL\_PULLBACK | 4050超 | not\_fired |
| 20261114\_BTC\_SELL\_PULLBACK | 74500超 | unknown |
| 20261115\_ETH\_SELL\_PULLBACK | 2100超 | unknown |
| 20261114\_USDJPY\_BUY\_PULLBACK | 158.30割れ | unknown |

GOLDは日曜日に通常のCOMEX取引がなく、確認した11月13日の高値3927.20も4050未満です。ただし週明け取引再開後の価格は未照合です。その他3資産は、判断日以降の連続した高値・安値が不足しているため、終値だけから発動なしとは確定しません。

`invalidation_check: 20261115_GOLD_SELL_PULLBACK=not_fired, 20261114_BTC_SELL_PULLBACK=unknown, 20261115_ETH_SELL_PULLBACK=unknown, 20261114_USDJPY_BUY_PULLBACK=unknown`

なお、11月15日のGOLDのnot\_firedは、確認可能な休場期間に限定した暫定判定です。

## 3\. 市場全体の前提

今回、新規に市場データと金融ニュースを検索しました。米国市場は日本時間月曜日の早朝にあたり、取引所・商品によって取引再開状況が異なります。

| 資産 | 取得基準値 | 時点・品質 |
|--------|--------|--------|
| GOLD | 3886.30 | COMEX 2026年12月限、11/13終値 |
| BTC | 約65045 | Coinbase取得時表示、時刻未確定 |
| ETH | 約1761 | 11/14報道値、直近値未確認 |
| WTI | 88.56 | 11/13清算値 |
| USDJPY | 159.70前後 | 11/13終盤、日銀17時中心159.85 |
| SPX（ES） | 7632 | 11/13米国早朝の先物値 |
| NASDAQ（NQ） | 28423 | 11/13米国早朝の先物値 |
| DXY | 103.26 | 11/13米国早朝 |
| US10Y | 5.10% | 11/12米国取引時間 |
| VIX | 18.35 | 11/13米国早朝 |

GOLDは2026年12月限（GCZ26）を継続基準とします。11月13日終値3886.30ドル、当日の値幅3871.10～3927.20ドルという報告を確認しました。citeturn720914news5

WTIはReutersによる11月13日の清算値88.56ドルを採用します。世界的な供給余剰見通しが下押し材料ですが、中東の輸送・供給リスクは依然として残っています。citeturn698973news33

USDJPYは日銀の11月13日公表資料で17時時点159.84～159.86円、Bloombergの米国時間終盤で159.7円前後です。160円近辺では日本当局の為替介入リスクがあります。citeturn698973search38turn698973search4turn698973news35

ESとNQは先物そのものの価格ですが、11月13日の早朝参考値であり、金曜日の最終清算値ではありません。現物指数やQQQを代用していません。citeturn698973search2

## 4\. 10資産別判断

| 資産 | 判断 | 根拠 |
|--------|--------|--------|
| GOLD | B SELL | 4000ドル割れ、下落基調継続。ただし反発余地あり |
| BTC | NO\_TRADE | 急落後の反発、ETF・CME根拠不足、MES39 |
| ETH | B SELL | 2000ドル割れ、BTCより弱い相対推移 |
| WTI | B SELL | IEAの供給余剰見通し、週間下落 |
| USDJPY | B BUY | 米金利・ドル高基調。ただし160円近辺の介入警戒 |
| SPX | NO\_TRADE | 先物の最終清算値と直近値幅未確認 |
| NASDAQ | NO\_TRADE | AI関連株の不安定さ、NQ最新価格未確認 |
| DXY | NO\_TRADE | ドル高方向だが押し目構造の定量確認不足 |
| US10Y | NO\_TRADE | 金利上昇方向だが直近OHLC不足 |
| VIX | NO\_TRADE | リスクオフと指数水準の関係が不安定 |

## 5\. A級候補

該当なし。

B級4件のうち、USDJPYがA級に最も近いですが、CBS72、EMS63、expected\_r0.34で基準未達です。加えてATR10実測検証が未完了です。

## 6\. B級監視候補

| 項目 | USDJPY BUY | ETH SELL | GOLD SELL | WTI SELL |
|--------|--------|--------|--------|--------|
| Entry低 | 159.30 | 1780 | 3860 | 88.00 |
| Entry高 | 159.70 | 1840 | 3900 | 90.00 |
| SL | 158.20 | 2070 | 4050 | 96.00 |
| TP1 | 161.60 | 1420 | 3600 | 78.00 |
| TP2 | 162.50 | 1300 | 3450 | 74.00 |
| RR | 1.615 | 1.500 | 1.647 | 1.571 |
| win\_prob | 0.54 | 0.52 | 0.53 | 0.50 |
| expected\_r | \+0.34 | \+0.27 | \+0.26 | \+0.17 |
| 想定MAE | 0.35R | 0.48R | 0.45R | 0.55R |
| risk\_pct | 0.25% | 0.25% | 0.25% | 0.25% |

RRはEntry中点とSL・TP1から再計算しています。

USDJPYはドル高の継続を想定しますが、160円近辺での為替介入が最大のイベントリスクです。判断日終値までにEntry帯へ来ない場合の終値成行参加規則は維持します。未到達による不参加確率はexpected\_rから控除していません。

ETHは週末の急落でBTCより弱い動きを示したことから、戻り売りを継続します。BTCの急反発に連動して2070ドルを超えればシナリオを無効化します。

GOLDは4000ドルを回復できない限り戻り売り優位とみます。ただし、金利低下やドル安による急反発には注意します。

WTIは供給余剰見通しによる下落方向を採用しますが、中東情勢による供給ショックで96ドルを超える場合は無効化します。供給ショック直後のmomentum追随は行いません。

4件のリスクを単純合計すると1.00%となるため、同日にすべて参加することはできません。最大日次リスク0.50%を優先します。

## 7\. 触らない資産

BTC、SPX、NASDAQ、DXY、US10Y、VIXの6資産をNO\_TRADEとします。

BTCは下落方向の見立て自体を否定しません。しかし、週末の急落と反発で短期的な価格構造が変わり、ETFフロー・CME建玉・basisの照合も不足しています。MES39のため、新規シグナルは見送ります。

NASDAQについては弱気材料があるものの、NQ先物の最新値とATR10が未確認です。現物指数で価格計画を代用せず、今回は方向あり判断を新規記帳しません。

## 8\. 後日検証ポイント

1. BTCが週末安値61946ドルを再び割るか、65564ドルを上回って定着するか。
2. ETHが2000ドルを回復できるか、戻り売りが優勢となるか。
3. USDJPYが160円台を定着させるか、日本当局の介入警戒で反転するか。
4. GOLD12月限が4000ドルを回復するか。
5. WTIの供給余剰見通しが中東情勢によって覆るか。
6. 全方向あり判断のATR10と、5営業日後の時間決済Rを検証する。

## 9\. Obsidian保存用Observation Draft

```markdown
# TSO Observation — 2026-11-16

model: GPT-6
market_leader: BTC
regime: MIXED
mode: normal_defensive

## Summary
A: 0
B: 4
NO_TRADE: 6

## Directional hypotheses
- USDJPY BUY B: dollar strength, intervention risk
- ETH SELL B: crypto weakness
- GOLD SELL B: below 4000
- WTI SELL B: supply surplus

## Risk
- Per B trade: 0.25%
- Daily aggregate maximum: 0.50%
- Time exit: 5 business days
- TP1/TP2: reference targets

## Unverified
- Complete ATR10 OHLC
- Latest ES/NQ settlements
- Full ETF/CME/basis evidence
- Historical intraday invalidation paths

## Next review
- Reconcile ATR10 and SL distances
- Recheck latest invalidation signals
- Observe Monday futures session
- Measure 5-day realized R
```

## 10\. TSO\_LOG CSVとJSON

以下は固定28列、10資産10行の記録です。NO\_TRADEの価格・確率・expected\_r・risk\_pctは空欄としています。RRは中点から計算し、小数第3位に丸めています。数値スコアはモデルの主観評価です。

### CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-11-16,20261116_GOLD_SELL_PULLBACK,GOLD,SELL,B,PULLBACK,3860,3900,4050,3600,3450,1.647,0.53,0.26,63,66,38,0.25,RISK_OFF,61,57,58,53,68,57,above_4050,GCZ26_ATR10,partially_verified
2026-11-16,20261116_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,45,47,82,,RISK_OFF,48,43,44,42,55,39,ETF_CME_incomplete,BTCUSD_spot,partially_verified
2026-11-16,20261116_ETH_SELL_PULLBACK,ETH,SELL,B,PULLBACK,1780,1840,2070,1420,1300,1.5,0.52,0.27,60,65,39,0.25,RISK_OFF,59,52,53,49,66,45,above_2070,ETHUSD_ATR10,partially_verified
2026-11-16,20261116_WTI_SELL_PULLBACK,WTI,SELL,B,PULLBACK,88,90,96,78,74,1.571,0.5,0.17,54,56,52,0.25,EVENT,55,50,46,42,61,49,above_96,CL_contract_ATR10,partially_verified
2026-11-16,20261116_USDJPY_BUY_PULLBACK,USDJPY,BUY,B,PULLBACK,159.3,159.7,158.2,161.6,162.5,1.615,0.54,0.34,66,70,34,0.25,EVENT,63,58,56,51,72,60,below_158.2,USDJPY_ATR10,partially_verified
2026-11-16,20261116_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,49,45,72,,MIXED,50,46,44,43,53,45,reference_ATR_pending,ES_futures_OHLC,partially_verified
2026-11-16,20261116_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,53,50,69,,MIXED,53,48,45,44,57,46,reference_ATR_pending,NQ_futures_OHLC,partially_verified
2026-11-16,20261116_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,58,55,60,,MIXED,59,54,51,48,64,56,reference_ATR_pending,DXY_OHLC,partially_verified
2026-11-16,20261116_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,53,48,66,,MIXED,56,51,48,44,58,52,reference_ATR_pending,US10Y_OHLC,partially_verified
2026-11-16,20261116_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,42,36,78,,MIXED,44,42,39,36,46,41,reference_ATR_pending,VIX_OHLC,partially_verified
```

### JSON

```json
[
  {"date":"2026-11-16","signal_id":"20261116_GOLD_SELL_PULLBACK","asset":"GOLD","side":"SELL","rank":"B","type":"PULLBACK","entry_low":3860,"entry_high":3900,"sl":4050,"tp1":3600,"tp2":3450,"rr":1.647,"win_prob":0.53,"expected_r":0.26,"tq_score":63,"opp_score":66,"no_trade_score":38,"risk_pct":0.25,"regime":"RISK_OFF","ems":61,"ffs":57,"cds":58,"ias":53,"cbs":68,"mes":57,"invalidation":"above_4050","verification_target":"GCZ26_ATR10","verified_status":"partially_verified"},
  {"date":"2026-11-16","signal_id":"20261116_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":45,"opp_score":47,"no_trade_score":82,"risk_pct":null,"regime":"RISK_OFF","ems":48,"ffs":43,"cds":44,"ias":42,"cbs":55,"mes":39,"invalidation":"ETF_CME_incomplete","verification_target":"BTCUSD_spot","verified_status":"partially_verified"},
  {"date":"2026-11-16","signal_id":"20261116_ETH_SELL_PULLBACK","asset":"ETH","side":"SELL","rank":"B","type":"PULLBACK","entry_low":1780,"entry_high":1840,"sl":2070,"tp1":1420,"tp2":1300,"rr":1.5,"win_prob":0.52,"expected_r":0.27,"tq_score":60,"opp_score":65,"no_trade_score":39,"risk_pct":0.25,"regime":"RISK_OFF","ems":59,"ffs":52,"cds":53,"ias":49,"cbs":66,"mes":45,"invalidation":"above_2070","verification_target":"ETHUSD_ATR10","verified_status":"partially_verified"},
  {"date":"2026-11-16","signal_id":"20261116_WTI_SELL_PULLBACK","asset":"WTI","side":"SELL","rank":"B","type":"PULLBACK","entry_low":88,"entry_high":90,"sl":96,"tp1":78,"tp2":74,"rr":1.571,"win_prob":0.5,"expected_r":0.17,"tq_score":54,"opp_score":56,"no_trade_score":52,"risk_pct":0.25,"regime":"EVENT","ems":55,"ffs":50,"cds":46,"ias":42,"cbs":61,"mes":49,"invalidation":"above_96","verification_target":"CL_contract_ATR10","verified_status":"partially_verified"},
  {"date":"2026-11-16","signal_id":"20261116_USDJPY_BUY_PULLBACK","asset":"USDJPY","side":"BUY","rank":"B","type":"PULLBACK","entry_low":159.3,"entry_high":159.7,"sl":158.2,"tp1":161.6,"tp2":162.5,"rr":1.615,"win_prob":0.54,"expected_r":0.34,"tq_score":66,"opp_score":70,"no_trade_score":34,"risk_pct":0.25,"regime":"EVENT","ems":63,"ffs":58,"cds":56,"ias":51,"cbs":72,"mes":60,"invalidation":"below_158.2","verification_target":"USDJPY_ATR10","verified_status":"partially_verified"},
  {"date":"2026-11-16","signal_id":"20261116_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":49,"opp_score":45,"no_trade_score":72,"risk_pct":null,"regime":"MIXED","ems":50,"ffs":46,"cds":44,"ias":43,"cbs":53,"mes":45,"invalidation":"reference_ATR_pending","verification_target":"ES_futures_OHLC","verified_status":"partially_verified"},
  {"date":"2026-11-16","signal_id":"20261116_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":53,"opp_score":50,"no_trade_score":69,"risk_pct":null,"regime":"MIXED","ems":53,"ffs":48,"cds":45,"ias":44,"cbs":57,"mes":46,"invalidation":"reference_ATR_pending","verification_target":"NQ_futures_OHLC","verified_status":"partially_verified"},
  {"date":"2026-11-16","signal_id":"20261116_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":58,"opp_score":55,"no_trade_score":60,"risk_pct":null,"regime":"MIXED","ems":59,"ffs":54,"cds":51,"ias":48,"cbs":64,"mes":56,"invalidation":"reference_ATR_pending","verification_target":"DXY_OHLC","verified_status":"partially_verified"},
  {"date":"2026-11-16","signal_id":"20261116_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":53,"opp_score":48,"no_trade_score":66,"risk_pct":null,"regime":"MIXED","ems":56,"ffs":51,"cds":48,"ias":44,"cbs":58,"mes":52,"invalidation":"reference_ATR_pending","verification_target":"US10Y_OHLC","verified_status":"partially_verified"},
  {"date":"2026-11-16","signal_id":"20261116_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":42,"opp_score":36,"no_trade_score":78,"risk_pct":null,"regime":"MIXED","ems":44,"ffs":42,"cds":39,"ias":36,"cbs":46,"mes":41,"invalidation":"reference_ATR_pending","verification_target":"VIX_OHLC","verified_status":"partially_verified"}
]
```

**記録結果：10資産すべて出力、各CSV行28列。** A級0件、B級4件、NO\_TRADE 6件です。今回の最大の未完了事項は、ATR10の実測照合と過去4件のinvalidationの完全判定です。これらを未確認として残し、方向判断と日次台帳の継続を優先しました。
