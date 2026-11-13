<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-11-14 07:00 JST -->
<!-- transport: Complete original read_thread message 206bdce9-eee4-480e-9acc-0f659df96629; raw markdown -->
<!-- archived_at: 2026-11-13T22:56:42Z / chars: 11208 / 値は無修正 -->

# Tactical Swing OS v2 — 2026年11月14日（土）

実行モデル: GPT-6
本日の市場の主役: **NASDAQ**
市場レジーム: **RISK\_OFF（株式・暗号資産）／MIXED（市場全体）**

## 1\. 本日の結論

米国11月13日（金）の取引終了後を基準に、10資産を評価した。

**A級0件、B級4件、NO\_TRADE 6件。**

週明けに向けて優先するのは、USDJPYの押し目買いとGOLDの戻り売り。BTCとETHにも下方向の見立てを残す。ただし、BTC・ETHは週末も取引されるため、株式市場が閉まっている間の価格変動に注意する。

| 優先 | 資産 | 判断 | RR | expected\_r |
|--------|--------|--------|--------|--------|
| 1 | USDJPY | B / BUY | 1.667 | \+0.35R |
| 2 | GOLD | B / SELL | 1.636 | \+0.29R |
| 3 | BTC | B / SELL | 1.500 | \+0.31R |
| 4 | ETH | B / SELL | 1.650 | \+0.23R |

B+観察候補はBTC、USDJPY。いずれもCBS・EMS・RR・較正後参考勝率の条件を満たす。ただし、ATR10の厳密な検証が未完了のため、価格水準は暫定評価である。

通常リスクは1件0.25%、日次合計0.50%。相関するGOLD・BTC・ETHの同時参加は合計リスクを考慮する。

## 2\. 前回判断の簡易検証

11月13日までの過去シグナルについて、前日までの方向あり判断の最新signal\_idとinvalidation水準を完全には取得できなかった。そのため、過去判断の発動・未発動を推測で確定しない。

11月13日の市場では、S&amp;P500現物が0.4%安、NASDAQ総合が0.9%安。一方、週間では主要株価指数が上昇した。日次の下落だけを根拠に、週間の反発局面が終了したとは判断できない。citeturn761572news37turn761572news33

`invalidation_check: 20261113以前の個別signal_idは未取得のため照合保留`

これは過去シグナルの発動判定を完了したという意味ではない。最新1件／資産の規則に従った検証には、過去のTSO\_LOGと判断日以降のOHLC照合が必要である。

## 3\. 市場全体の前提

11月13日の市場では、AI関連株への不透明感、米金利上昇、ドル高が同時に観測された。Reutersは米国株の下落とドル指数の19カ月ぶり高値を報じている。citeturn761572news34turn761572news33

| 指標 | 取得した参考値 | 時点・注意 |
|--------|--------|--------|
| GOLD | 3879.70 | 11/13先物清算値。12月限との厳密な照合未完了 |
| BTC/USD | 約68526 | 11/13報道値 |
| ETH/USD | 約1951 | 11/13報道値 |
| WTI | 約89.09 | 11/13報道値。別報道と不一致 |
| USDJPY | 約159.86 | 11/13日足 |
| SPX現物参考 | 7561.67 | ES先物への代用は禁止 |
| NASDAQ総合参考 | 25136.27 | NQ先物への代用は禁止 |
| DXY | 約103.37 | 11/13報道値 |
| US10Y | 約5.154% | 11/13報道値 |
| VIX | 約18.81 | 11/13報道値 |

参考資料: citeturn761572news36turn761572news0turn908638search8turn908638news38

**データ品質上の注意\:** ES・NQの正規先物価格は確認できず、現物指数を代用していない。WTIは情報源間で価格の不整合があり、方向判断を保留した。GOLDの基準限月はCOMEX 2026年12月限（GCZ26）とするが、今回取得した清算値の限月照合は未完了である。

ATR10についても、前日までの10本の完全なOHLCを取得できた資産は限定的である。B級のSLはボラティリティを考慮した暫定水準であり、全件について1×ATR10以上を数値的に証明できたわけではない。A級を認定しない理由の一つである。

## 4\. 10資産別判断

| 資産 | 判断 | 根拠 |
|--------|--------|--------|
| GOLD | B SELL | 週間下落が大きく、ドル高・金利上昇が逆風 |
| BTC | B SELL | 70000割れ、ETF資金流出報道、リスク回避 |
| ETH | B SELL | BTCに連動した下落、独立した強材料不足 |
| WTI | NO\_TRADE | 価格系列の不一致、供給要因の影響 |
| USDJPY | B BUY | ドル高基調、159円台を維持 |
| SPX | NO\_TRADE | 週間反発と日次下落が混在、ES未確認 |
| NASDAQ | NO\_TRADE | AI関連株下落、NQ先物の基準値未確認 |
| DXY | NO\_TRADE | 上昇方向だがATR・押し目水準未確認 |
| US10Y | NO\_TRADE | 金利上昇だが日足変動幅未確認 |
| VIX | NO\_TRADE | 株価下落に対して指数水準は限定的 |

### B級の価格計画

| 資産 | Entry帯 | SL | TP1 / TP2 | 想定MAE |
|--------|--------|--------|--------|--------|
| GOLD SELL | 3890–3910 | 4010 | 3720 / 3630 | 0.45R |
| BTC SELL | 68800–70200 | 74500 | 62000 / 58500 | 0.40R |
| ETH SELL | 1950–2010 | 2180 | 1650 / 1500 | 0.50R |
| USDJPY BUY | 159.35–159.65 | 158.30 | 161.50 / 162.30 | 0.35R |

すべてモデルによる暫定価格計画。RRはEntry帯中点から再計算済み。TP1・TP2は参考水準であり、基本決済は5営業日。

NASDAQ、BTC、USDJPYに適用される終値成行参加規則については、方向あり判断のBTC・USDJPYに引き続き適用する。ただし本日は土曜日であり、BTC以外の通常の平日終値執行とは市場条件が異なる。

## 5\. A級候補

**該当なし。**

USDJPYはCBS73、EMS64、expected\_r0.35でA級基準未達。BTCはCBS70、EMS62、expected\_r0.31。GOLDはCBS69、EMS61、expected\_r0.29。

いずれも方向判断を消す理由にはならないため、B級として記帳する。

## 6\. B級監視候補

USDJPYは159.35–159.65への押し目を中心に観察する。158.30割れをシナリオ崩壊水準とする。ドル高が継続する一方、160円付近では急激な円高反転に注意する。

GOLDは3900近辺への戻りを想定する。4010超えで売りシナリオを無効化。金利低下とドル安が同時進行する場合は早期再評価する。

BTCは70000近辺の回復が定着しない場合の下落継続を想定。74500超えで無効化する。ETF流出の報道は確認できたが、CME建玉・basisの完全照合は未完了。citeturn908638news38

ETHは1980近辺への戻り売りを想定し、2180超えで無効化。BTCとの高い相関を考慮し、両方のシグナルを独立した機会として過大評価しない。

## 7\. 触らない資産

WTI、SPX、NASDAQ、DXY、US10Y、VIX。

NASDAQは市場の主役と判断する一方、NQ先物の正しい基準値を取得できていないため、現物指数の水準を使って売買価格を設定しない。WTIも供給ショックに対する追随を避け、限月を確定してから再評価する。

## 8\. 後日検証ポイント

1. USDJPYが160円付近で反転するか、それともドル高が継続するか。
2. GOLDが3900近辺への戻り後に再下落するか。
3. BTCが70000を回復・維持できるか。
4. NASDAQのAI関連株売りが広範な株式市場に波及するか。
5. B級4件のATR10下限、週明けの価格ギャップ、5営業日後の実現Rを再計算する。

## 9\. Obsidian保存用Observation Draft

```markdown
# TSO Observation — 2026-11-14

model: GPT-6
market_leader: NASDAQ
regime: MIXED
market_bias: RISK_OFF
A_signals: 0
B_signals: 4
NO_TRADE: 6

## Hypothesis
米金利上昇とドル高が株式・暗号資産に逆風。
ただし株式市場は週間で反発しており、下落トレンド再開は未確定。

## Directional signals
- GOLD SELL B
- BTC SELL B
- ETH SELL B
- USDJPY BUY B

## Data limitations
- GCZ26限月照合未完了
- ES/NQ先物の正規清算値未確認
- WTI価格系列不一致
- ATR10厳密計算未完了
- 過去signal_id照合未完了

## Next review
週明けの先物市場再開、BTC週末価格、ドル円160円付近の反応。
```

## 10\. TSO\_LOG CSV / JSON

固定28列、10資産10行。CSVの各データ行は27カンマであることを確認した。スコア・確率・expected\_rは主観推定値であり、価格の検証状態とは区別する。

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-11-14,20261114_GOLD_SELL_PULLBACK,GOLD,SELL,B,PULLBACK,3890,3910,4010,3720,3630,1.636,0.51,0.29,63,67,35,0.25,RISK_OFF,61,57,58,60,69,59,above_4010,GCZ26_settlement,partially_verified
2026-11-14,20261114_BTC_SELL_PULLBACK,BTC,SELL,B,PULLBACK,68800,70200,74500,62000,58500,1.5,0.52,0.31,62,68,32,0.25,RISK_OFF,62,57,54,58,70,53,above_74500,BTCUSD_spot_and_ETF_flow,partially_verified
2026-11-14,20261114_ETH_SELL_PULLBACK,ETH,SELL,B,PULLBACK,1950,2010,2180,1650,1500,1.65,0.5,0.23,58,61,40,0.25,RISK_OFF,57,51,50,55,64,48,above_2180,ETHUSD_spot,partially_verified
2026-11-14,20261114_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,40,32,83,,EVENT,45,40,37,33,42,41,WTI_contract_conflict,CL_contract_settlement,unverified
2026-11-14,20261114_USDJPY_BUY_PULLBACK,USDJPY,BUY,B,PULLBACK,159.35,159.65,158.3,161.5,162.3,1.667,0.53,0.35,68,70,29,0.25,MIXED,64,62,57,60,73,61,below_158.30,USDJPY_OHLC,partially_verified
2026-11-14,20261114_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,48,38,74,,RISK_OFF,51,48,44,42,52,46,ES_settlement_missing,ESZ26_settlement,unverified
2026-11-14,20261114_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,55,49,68,,RISK_OFF,55,48,45,46,58,48,NQ_settlement_missing,NQZ26_settlement,unverified
2026-11-14,20261114_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,57,52,62,,MIXED,56,52,50,51,61,52,DXY_ATR_missing,DXY_index_OHLC,partially_verified
2026-11-14,20261114_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,52,43,72,,EVENT,53,49,47,45,55,49,US10Y_ATR_missing,US10Y_yield,partially_verified
2026-11-14,20261114_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,42,31,81,,MIXED,44,43,39,38,45,42,VIX_ATR_missing,VIX_index,partially_verified
```

```json
[
  {"date":"2026-11-14","signal_id":"20261114_GOLD_SELL_PULLBACK","asset":"GOLD","side":"SELL","rank":"B","type":"PULLBACK","entry_low":3890,"entry_high":3910,"sl":4010,"tp1":3720,"tp2":3630,"rr":1.636,"win_prob":0.51,"expected_r":0.29,"tq_score":63,"opp_score":67,"no_trade_score":35,"risk_pct":0.25,"regime":"RISK_OFF","ems":61,"ffs":57,"cds":58,"ias":60,"cbs":69,"mes":59,"invalidation":"above_4010","verification_target":"GCZ26_settlement","verified_status":"partially_verified"},
  {"date":"2026-11-14","signal_id":"20261114_BTC_SELL_PULLBACK","asset":"BTC","side":"SELL","rank":"B","type":"PULLBACK","entry_low":68800,"entry_high":70200,"sl":74500,"tp1":62000,"tp2":58500,"rr":1.5,"win_prob":0.52,"expected_r":0.31,"tq_score":62,"opp_score":68,"no_trade_score":32,"risk_pct":0.25,"regime":"RISK_OFF","ems":62,"ffs":57,"cds":54,"ias":58,"cbs":70,"mes":53,"invalidation":"above_74500","verification_target":"BTCUSD_spot_and_ETF_flow","verified_status":"partially_verified"},
  {"date":"2026-11-14","signal_id":"20261114_ETH_SELL_PULLBACK","asset":"ETH","side":"SELL","rank":"B","type":"PULLBACK","entry_low":1950,"entry_high":2010,"sl":2180,"tp1":1650,"tp2":1500,"rr":1.65,"win_prob":0.5,"expected_r":0.23,"tq_score":58,"opp_score":61,"no_trade_score":40,"risk_pct":0.25,"regime":"RISK_OFF","ems":57,"ffs":51,"cds":50,"ias":55,"cbs":64,"mes":48,"invalidation":"above_2180","verification_target":"ETHUSD_spot","verified_status":"partially_verified"},
  {"date":"2026-11-14","signal_id":"20261114_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":40,"opp_score":32,"no_trade_score":83,"risk_pct":"","regime":"EVENT","ems":45,"ffs":40,"cds":37,"ias":33,"cbs":42,"mes":41,"invalidation":"WTI_contract_conflict","verification_target":"CL_contract_settlement","verified_status":"unverified"},
  {"date":"2026-11-14","signal_id":"20261114_USDJPY_BUY_PULLBACK","asset":"USDJPY","side":"BUY","rank":"B","type":"PULLBACK","entry_low":159.35,"entry_high":159.65,"sl":158.3,"tp1":161.5,"tp2":162.3,"rr":1.667,"win_prob":0.53,"expected_r":0.35,"tq_score":68,"opp_score":70,"no_trade_score":29,"risk_pct":0.25,"regime":"MIXED","ems":64,"ffs":62,"cds":57,"ias":60,"cbs":73,"mes":61,"invalidation":"below_158.30","verification_target":"USDJPY_OHLC","verified_status":"partially_verified"},
  {"date":"2026-11-14","signal_id":"20261114_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":48,"opp_score":38,"no_trade_score":74,"risk_pct":"","regime":"RISK_OFF","ems":51,"ffs":48,"cds":44,"ias":42,"cbs":52,"mes":46,"invalidation":"ES_settlement_missing","verification_target":"ESZ26_settlement","verified_status":"unverified"},
  {"date":"2026-11-14","signal_id":"20261114_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":55,"opp_score":49,"no_trade_score":68,"risk_pct":"","regime":"RISK_OFF","ems":55,"ffs":48,"cds":45,"ias":46,"cbs":58,"mes":48,"invalidation":"NQ_settlement_missing","verification_target":"NQZ26_settlement","verified_status":"unverified"},
  {"date":"2026-11-14","signal_id":"20261114_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":57,"opp_score":52,"no_trade_score":62,"risk_pct":"","regime":"MIXED","ems":56,"ffs":52,"cds":50,"ias":51,"cbs":61,"mes":52,"invalidation":"DXY_ATR_missing","verification_target":"DXY_index_OHLC","verified_status":"partially_verified"},
  {"date":"2026-11-14","signal_id":"20261114_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":52,"opp_score":43,"no_trade_score":72,"risk_pct":"","regime":"EVENT","ems":53,"ffs":49,"cds":47,"ias":45,"cbs":55,"mes":49,"invalidation":"US10Y_ATR_missing","verification_target":"US10Y_yield","verified_status":"partially_verified"},
  {"date":"2026-11-14","signal_id":"20261114_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":42,"opp_score":31,"no_trade_score":81,"risk_pct":"","regime":"MIXED","ems":44,"ffs":43,"cds":39,"ias":38,"cbs":45,"mes":42,"invalidation":"VIX_ATR_missing","verification_target":"VIX_index","verified_status":"partially_verified"}
]
```

**本日の記録結果\:** 10資産すべて記帳。方向あり4件、A級0件。未確認の先物価格やATR10を確定値として扱わず、週明けの再検証対象として残した。
