<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-08-07 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 12780 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026年8月7日

データは**8月6日米国市場終了後～8月7日07:00 JST**を基準に新規取得した。本日は特に重要で、米雇用統計が**今夜21:30 JST（8:30 ET）**に発表される。米労働省も7月雇用統計の8月7日8:30 ET公表を明記している。citeturn0search61

結論から言えば、**A級は0件。B級はGOLD BUY、SPX BUY、NASDAQ BUY。ただし雇用統計前なので、新規執行は原則0.25%以下、NASDAQはXM最小ロット問題が残るため実質監視中心**とする。

## 1. 本日の結論

市場は「上昇トレンド崩壊」ではなく、**最高値圏でのイベント待ち**に入った。

8月6日のS&P500は7710.03（-0.18%）、NASDAQ総合は26348.35（-0.06%）、Dowは-0.85%。WTIは逆に+2.75%の77.29ドルへ反発した。citeturn2view0

重要なのは、NASDAQが前日の-0.83%からさらに崩れなかったこと。一方で値上がり銘柄より値下がり銘柄がNYSEで1.57倍、NASDAQでも1.38倍多く、内部の強さは指数ほど良くない。citeturn2view0

したがって、

**トレンド：株式上  
短期モメンタム：中立化  
イベントリスク：極めて高い**

と判定する。

本日は**「良い方向を見つける日」より「雇用統計前に悪いリスクを取らない日」**である。

---

# 2. 前回判断の簡易検証

### GOLD B級BUY → **方向成功**

前回Entryは4190～4240。

COMEX金先物（12月限）は8月5日に**4305.20**で決済し、+3.7%。現物も4253.36、日中高値4264.93まで上昇した。50日線4160も上抜いた。citeturn2view4

したがって方向判定は明確に成功。

ただしEntry帯から離れた後なら追わない。

**評価：DIRECTION_SUCCESS**

### SPX B級BUY

前回ES監視Entry7650～7690。

S&P500現物は7710.03。高値圏を維持しているが、TSO参照系列はESなので現物価格でFILL判定はしない。citeturn2view0

**評価：VALID / NO_CONFIRMED_FILL**

### NASDAQ B級BUY

NASDAQ総合は-0.06%とほぼ横ばい。citeturn2view0

NQ系列のEntry到達を十分検証できないためFILL判定しない。

ただし8月4日のA級方向成功後、NASDAQが大きく崩れていないため、中期方向仮説はまだ生きている。

---

# 3. 市場全体の前提

本日のRegimeは

**`PRE_NFP / HIGH_EVENT_RISK / EQUITY_UPTREND / OIL_HEADLINE_VOLATILITY`**

とする。

昨日の米新規失業保険申請は19.9万件。市場予想20.2万件を下回った。7月の人員削減計画も前年同月比46%減、2年ぶり低水準だった。さらにQ2労働生産性は年率+1.4%と予想+0.6%を上回った。citeturn2view1

つまり雇用市場には現時点で**急激な崩壊シグナルはない**。

今夜の市場予想は、

**NFP +8万人  
失業率 4.2%**

付近。citeturn2view1

ここから大きく外れると、金利・ドル・GOLD・NASDAQが同時に動く。

またWTIが一日で+2.75%反発した理由は、イラン議会委員会が米国・イスラエル等の「敵対国」船舶のホルムズ海峡通航を禁止する法案を検討しているとの報道。citeturn2view0

したがってWTIは引き続き**通常のテクニカル商品として扱わない**。

---

# 4. 10資産別判断

**GOLD — B / BUY PULLBACK。** 50日線突破、ドル安・金利低下という構造は良好。ただし8月5日の+3.7%急騰後なのでAにはしない。COMEX基準の新Entryを**4210～4260、SL4050、TP1 4430、TP2 4580**とする。citeturn2view4

**BTC — NO_TRADE。** BTCは8月6日時点で約64394ドル。株式リスクオンに参加できず65000以下でレンジが続いている。30日インプライド・ボラティリティも36%まで低下しており、CoinDeskも低ボラを低リスクと誤認すべきではないと指摘している。citeturn2view2 MES=47。規定によりNO_TRADE。

**ETH — NO_TRADE。** 約1900ドルで、保有者全体の実現価格約2450ドルを下回る。大口の蓄積は見られる一方、CryptoQuantは底形成前にもう一段の下落余地を警戒している。citeturn2view3

**WTI — NO_TRADE。** 77.29、+2.75%。前日の急落から今度は急反発。citeturn2view0 完全にHormuz headline regime。売らない、買わない。

**USDJPY — NO_TRADE。** 雇用統計で米金利経路が直接再評価される。さらに直近には米国による円買い介入という異例の要因もある。今朝ポジションを作るRRではない。

**SPX — B / BUY PULLBACK。** ES基準Entry **7630～7680、SL7460、TP1 7860、TP2 7980**。株式トレンドは維持。ただしbreadth悪化＋NFP前なので0.25%。

**NASDAQ — B / BUY PULLBACK。** NQ基準Entry **28900～29200、SL28050、TP1 30250、TP2 31000**。AI/成長株の構造的優位は維持するが、個別決算ではAppLovin -19.7%、Datadog -19%など高バリュエーション銘柄への選別が強まっている。citeturn2view0

**DXY — NO_TRADE。** 今夜のNFPそのものがドルの方向決定イベント。事前ポジションの期待値は低い。

**US10Y — NO_TRADE。** 失業保険申請は強かったが、雇用統計次第で4.5～4.7%帯のどちらにも動き得る。イベント前に金利方向を固定しない。citeturn2view1

**VIX — NO_TRADE。** 株式breadth悪化はVIX上昇材料だが、指数そのものは最高値近辺。VIXを売買するより、今夜のNFP後のES/NQ確認指標として使用する。

---

# 5. A級候補

**0件。**

GOLDはCBS・EMSだけならA候補まで来ているが、急騰後のEntry効率とNFPイベントリスクによってMAE想定が0.25Rを超える。

NASDAQ/SPXも同様。

**NFP直前というだけで機械的NO_TRADEにはしないが、A級条件を満たしていないものをAへ格上げしない。**

---

# 6. B級監視候補

| 優先 | 資産 | Entry | SL | TP1 | win_prob | expected_r |
|---|---:|---:|---:|---:|---:|---:|
| 1 | GOLD BUY | 4210–4260 | 4050 | 4430 | 0.64 | 0.44 |
| 2 | SPX BUY | 7630–7680 | 7460 | 7860 | 0.59 | 0.37 |
| 3 | NASDAQ BUY | 28900–29200 | 28050 | 30250 | 0.58 | 0.36 |

GOLDが今日も首位。

ただし**21:30 JSTの雇用統計を跨ぐ新規なら0.25%上限**。

NASDAQについては、以前確認したXM最小ロットでは広いSLを使うと損失額が1万円超だったため、同様なら分析上Bでも実売買は `LOT_CONSTRAINT / NO_TRADE`。SPXは同条件で約3000円だったため実行可能性が相対的に高い。memcite

---

# 7. 触らない資産

最優先は**WTI**。

75ドル台への急落→77.29への+2.75%反発という状態で、Hormuz関連報道一つで方向が変わる。citeturn2view0

次にBTC/ETH。

BTCは株式上昇に追随せず65000以下。ETHは1900近辺で実現価格2450を大幅に下回る。citeturn2view2turn2view3

これは「安いから買う」局面ではなく、**底形成を確認する局面**。

---

# 8. 後日検証ポイント

本日は非常に良い検証日になる。

最優先で保存するのは、

**NFP発表前価格 → +1h → 米国終値 → +1d → +3d**

のGOLD、ES、NQ、DXY、US10Y。

さらに8月4日のNASDAQ A級について、5営業日MFE/MAEまで追跡する。

GOLDについては8月6日B級が方向成功したため、**「B級発行→翌日も継続→Entry追随禁止」がどの程度機会損失を生むか**も記録する。

---

# 9. Obsidian保存用Observation Draft

```markdown
# 2026-08-07 NFP前・GOLD優位継続

## Market

S&P500 7710.03 -0.18%
NASDAQ Composite 26348.35 -0.06%
WTI 77.29 +2.75%

US initial claims 199k
Forecast 202k

Q2 productivity +1.4%
Forecast +0.6%

NFP consensus approximately +80k
Unemployment 4.2%

## Regime

PRE_NFP
HIGH_EVENT_RISK
EQUITY_UPTREND
OIL_HEADLINE_VOLATILITY

## Signals

A: NONE

B:
GOLD BUY 4210-4260
SPX BUY 7630-7680
NASDAQ BUY 28900-29200

NO_TRADE:
BTC
ETH
WTI
USDJPY
DXY
US10Y
VIX

## Previous

GOLD B:
DIRECTION_SUCCESS

SPX B:
VALID / NO_CONFIRMED_FILL

NASDAQ B:
VALID

2026-08-04 NASDAQ A:
Direction SUCCESS
Execution NO_TRADE / BROKER_MIN_LOT_RISK

## Event

2026-08-07 21:30 JST
US Employment Situation

## Verification

NFP pre-event -> +1h -> close -> +1d -> +3d

#TSO #NFP #GOLD #NASDAQ #SPX
```

# 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-08-07,20260807_GOLD_LONG_B-PULLBACK,GOLD,BUY,B,PULLBACK,4210,4260,4050,4430,4580,1.16,0.64,0.44,91,72,39,0.25,GOLD_BREAKOUT_PRE_NFP,76,74,79,77,76,71,4050_break_or_NFP_yield_spike,COMEX_GOLD_NFP_US10Y_DXY_5d,verified
2026-08-07,20260807_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,55,42,86,,LOW_VOL_EQUITY_RELATIVE_WEAKNESS,53,45,61,45,53,47,mes_below_50_and_65000_failure,BTC_65000_ETF_CME_post_NFP,partially_verified
2026-08-07,20260807_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,54,46,82,,CAPITULATION_UNCONFIRMED_BOTTOM,55,48,64,50,55,49,below_realized_price_without_floor_confirmation,ETH_1900_2450_realized_price_ETF_flow,partially_verified
2026-08-07,20260807_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,94,28,97,,HORMUZ_HEADLINE_VOLATILITY,77,70,96,29,54,66,headline_reversal_risk_dominates_signal,WTI_Hormuz_legislation_5d,verified
2026-08-07,20260807_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,69,37,88,,PRE_NFP_INTERVENTION_DISTORTED,61,62,78,39,55,57,NFP_and_intervention_binary_risk,USDJPY_NFP_US10Y_post_event,partially_verified
2026-08-07,20260807_SPX_LONG_B-PULLBACK,SPX,BUY,B,PULLBACK,7630,7680,7460,7860,7980,1.02,0.59,0.37,82,64,48,0.25,EQUITY_UPTREND_PRE_NFP,69,68,74,69,71,65,7460_break_or_NFP_yield_VIX_shock,ES_preNFP_1h_1d_3d_MFE_MAE,partially_verified
2026-08-07,20260807_NASDAQ_LONG_B-PULLBACK,NASDAQ,BUY,B,PULLBACK,28900,29200,28050,30250,31000,1.10,0.58,0.36,85,62,51,0.25,AI_UPTREND_PRE_NFP_SELECTION,68,67,76,73,72,64,28050_break_or_tech_breadth_failure,NQ_preNFP_1h_1d_3d_MFE_MAE,partially_verified
2026-08-07,20260807_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,72,31,91,,PRE_NFP_BINARY_DOLLAR,64,65,79,34,57,61,NFP_directly_reprices_dollar,DXY_preNFP_1h_1d_3d,partially_verified
2026-08-07,20260807_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,79,34,91,,PRE_NFP_RATE_REPRICING,68,73,82,37,61,69,NFP_directly_reprices_rate_path,US10Y_preNFP_1h_1d_3d,partially_verified
2026-08-07,20260807_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,72,38,84,,PRE_EVENT_VOLATILITY,64,61,76,54,60,60,NFP_volatility_expansion_risk,VIX_preNFP_postNFP_ES_NQ,partially_verified
```

## JSON

```json
[
{"date":"2026-08-07","signal_id":"20260807_GOLD_LONG_B-PULLBACK","asset":"GOLD","side":"BUY","rank":"B","type":"PULLBACK","entry_low":4210,"entry_high":4260,"sl":4050,"tp1":4430,"tp2":4580,"rr":1.16,"win_prob":0.64,"expected_r":0.44,"tq_score":91,"opp_score":72,"no_trade_score":39,"risk_pct":0.25,"regime":"GOLD_BREAKOUT_PRE_NFP","ems":76,"ffs":74,"cds":79,"ias":77,"cbs":76,"mes":71,"invalidation":"4050_break_or_NFP_yield_spike","verification_target":"COMEX_GOLD_NFP_US10Y_DXY_5d","verified_status":"verified"},
{"date":"2026-08-07","signal_id":"20260807_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":55,"opp_score":42,"no_trade_score":86,"risk_pct":null,"regime":"LOW_VOL_EQUITY_RELATIVE_WEAKNESS","ems":53,"ffs":45,"cds":61,"ias":45,"cbs":53,"mes":47,"invalidation":"mes_below_50_and_65000_failure","verification_target":"BTC_65000_ETF_CME_post_NFP","verified_status":"partially_verified"},
{"date":"2026-08-07","signal_id":"20260807_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":54,"opp_score":46,"no_trade_score":82,"risk_pct":null,"regime":"CAPITULATION_UNCONFIRMED_BOTTOM","ems":55,"ffs":48,"cds":64,"ias":50,"cbs":55,"mes":49,"invalidation":"below_realized_price_without_floor_confirmation","verification_target":"ETH_1900_2450_realized_price_ETF_flow","verified_status":"partially_verified"},
{"date":"2026-08-07","signal_id":"20260807_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":94,"opp_score":28,"no_trade_score":97,"risk_pct":null,"regime":"HORMUZ_HEADLINE_VOLATILITY","ems":77,"ffs":70,"cds":96,"ias":29,"cbs":54,"mes":66,"invalidation":"headline_reversal_risk_dominates_signal","verification_target":"WTI_Hormuz_legislation_5d","verified_status":"verified"},
{"date":"2026-08-07","signal_id":"20260807_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":69,"opp_score":37,"no_trade_score":88,"risk_pct":null,"regime":"PRE_NFP_INTERVENTION_DISTORTED","ems":61,"ffs":62,"cds":78,"ias":39,"cbs":55,"mes":57,"invalidation":"NFP_and_intervention_binary_risk","verification_target":"USDJPY_NFP_US10Y_post_event","verified_status":"partially_verified"},
{"date":"2026-08-07","signal_id":"20260807_SPX_LONG_B-PULLBACK","asset":"SPX","side":"BUY","rank":"B","type":"PULLBACK","entry_low":7630,"entry_high":7680,"sl":7460,"tp1":7860,"tp2":7980,"rr":1.02,"win_prob":0.59,"expected_r":0.37,"tq_score":82,"opp_score":64,"no_trade_score":48,"risk_pct":0.25,"regime":"EQUITY_UPTREND_PRE_NFP","ems":69,"ffs":68,"cds":74,"ias":69,"cbs":71,"mes":65,"invalidation":"7460_break_or_NFP_yield_VIX_shock","verification_target":"ES_preNFP_1h_1d_3d_MFE_MAE","verified_status":"partially_verified"},
{"date":"2026-08-07","signal_id":"20260807_NASDAQ_LONG_B-PULLBACK","asset":"NASDAQ","side":"BUY","rank":"B","type":"PULLBACK","entry_low":28900,"entry_high":29200,"sl":28050,"tp1":30250,"tp2":31000,"rr":1.10,"win_prob":0.58,"expected_r":0.36,"tq_score":85,"opp_score":62,"no_trade_score":51,"risk_pct":0.25,"regime":"AI_UPTREND_PRE_NFP_SELECTION","ems":68,"ffs":67,"cds":76,"ias":73,"cbs":72,"mes":64,"invalidation":"28050_break_or_tech_breadth_failure","verification_target":"NQ_preNFP_1h_1d_3d_MFE_MAE","verified_status":"partially_verified"},
{"date":"2026-08-07","signal_id":"20260807_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":72,"opp_score":31,"no_trade_score":91,"risk_pct":null,"regime":"PRE_NFP_BINARY_DOLLAR","ems":64,"ffs":65,"cds":79,"ias":34,"cbs":57,"mes":61,"invalidation":"NFP_directly_reprices_dollar","verification_target":"DXY_preNFP_1h_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-07","signal_id":"20260807_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":79,"opp_score":34,"no_trade_score":91,"risk_pct":null,"regime":"PRE_NFP_RATE_REPRICING","ems":68,"ffs":73,"cds":82,"ias":37,"cbs":61,"mes":69,"invalidation":"NFP_directly_reprices_rate_path","verification_target":"US10Y_preNFP_1h_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-07","signal_id":"20260807_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":72,"opp_score":38,"no_trade_score":84,"risk_pct":null,"regime":"PRE_EVENT_VOLATILITY","ems":64,"ffs":61,"cds":76,"ias":54,"cbs":60,"mes":60,"invalidation":"NFP_volatility_expansion_risk","verification_target":"VIX_preNFP_postNFP_ES_NQ","verified_status":"partially_verified"}
]
```

**今日のポイントはGOLDです。** 昨日のB級BUYは方向成功しましたが、今夜の雇用統計前に急騰を追う必要はありません。株指数も同じで、**8月4日のNASDAQ A級で確認できた方向選別能力を維持しつつ、今日はイベント前の価格追随をしない**運用を優先します。citeturn2view4turn2view0
