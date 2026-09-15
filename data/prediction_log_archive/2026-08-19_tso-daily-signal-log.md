<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-08-19 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 14476 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026年8月19日

データ基準は**8月18日米国市場終了後～8月19日07:00 JST前後**。本日は前日までの押し目買い局面から一段変化しました。NASDAQは-1.33%、S&P500は-0.69%。特に半導体株の下落が大きく、フィラデルフィア半導体指数は約-5%。WTIは84.94ドル、米30年債利回りは一時5.337%と2007年以来の高水準に達しました。citeturn949563search37turn830069news19turn382453news38

さらに**本日8月19日14:00 ET（日本時間20日03:00）に7月28–29日FOMC議事要旨**が公表されます。Fed公式カレンダーで確認済みです。7月会合は9対3で3.50–3.75%据え置きでした。citeturn983433search0turn983433search1turn983433search4

## 1. 本日の結論

**A級：0件。**

**B+：0件。**

**新規B級：0件。**

今日は**10資産すべて新規NO_TRADE**とします。

これは防御的に丸めたのではなく、昨日まで存在した押し目BUYのクロスアセット前提が明確に悪化したためです。

特に、

**WTI高止まり  
＋長期金利高止まり  
＋NASDAQ自身の下落加速  
＋半導体-5%  
＋FOMC議事要旨前**

という組み合わせでは、NASDAQ/SPXを新規BUYするには確認不足。一方、ここからSELLすると「既に発生した下落への追随」になるため、SELLも見送ります。citeturn949563search37turn830069news19

したがって今日の判断は、

**「前日までのBUYポジションはSL・時間決済ルールで管理、新規建てはしない」**

です。

---

## 2. 前回判断の簡易検証

### SPX B+ BUY — **ENTRY_REACHED / 逆行中 / SL未到達**

前回：

**Entry 7740–7785  
SL 7630**

8月18日のES9月限は概ね**7710台まで下落**。現物S&P500は7691.76、-0.69%でした。ESの確認値でも7714.5付近が観測されています。citeturn949563search14turn949563news44

したがって、

**ENTRY_REACHED  
MAE_EXPANDED  
SL_NOT_REACHED**

です。

前日までの正のMFEから逆行へ変わりました。

ここは重要な教師データです。

### NASDAQ B BUY — **ENTRY_REACHED / 大幅逆行 / SL未到達**

前回：

**Entry 29880–30120  
SL 29200**

NQは18日に約**29550付近**まで下落し、NASDAQ現物も-1.33%。半導体株の下落が特に大きくなりました。citeturn949563search14turn949563search37

したがって、

**ENTRY_REACHED  
MAE_EXPANDED  
SL_NOT_REACHED  
THESIS_WEAKENED**

です。

まだ29200を割ったと確認していないので、後からSTOP扱いにはしません。

### GOLD B BUY — **ENTRY_REACHED / 方向失敗**

前回：

**Entry 4380–4430  
SL 4260**

金先物は18日に大幅反落。Reutersでは12月限4420.60、別のCOMEX限月では4366.00決済が確認され、限月差があります。いずれにせよ金は約1.1–1.6%下落しました。citeturn830069news17turn382453news41

**ENTRY_REACHED  
1D_DIRECTION_FAIL  
SL_NOT_CONFIRMED**

と評価します。

### WTI NO_TRADE — **成功**

WTIは84.94まで上昇。Brentは91.02。米・イランの和平期待後退とHormuz問題が主因です。citeturn130916news49

BUY方向は出ましたが、供給ショック後を追わないルール通りです。

**SUCCESSFUL_AVOIDANCE**

を継続します。

---

## 3. 市場全体の前提

本日のRegimeは、

**`TERM_PREMIUM_SHOCK / OIL_INFLATION / TECH_DELEVERAGING / FOMC_MINUTES_AHEAD`**

へ変更します。

昨日までの重要な研究テーマだった、

**weak macro → lower yields → Growth positive**

が、かなり明確に機能しなくなっています。

18日の米経済指標自体は強くありません。住宅着工は-12.4%、鉱工業生産も+0.2%程度でした。それでも長期金利は一時10年4.748%、30年5.337%まで上昇しました。citeturn949563news41turn949563news45

つまり今は、

**景気が弱い  
↓  
Fed利上げ期待は低下**

している一方、

**Oil inflation  
＋財政赤字  
＋国債供給  
＋AI企業の巨額債券発行  
→ term premium上昇**

が長期金利を押し上げています。citeturn382453news37turn830069news21

この変化はNASDAQにとって非常に重要です。

---

## 4. 10資産別判断

| 資産 | 本日 | 判断理由 |
|---|---|---|
| GOLD | **NO_TRADE** | 金利上昇に負けてprice confirmation悪化 |
| BTC | **NO_TRADE** | 64560まで戻るがMES<50 |
| ETH | **NO_TRADE** | 約1625、独自強度なし |
| WTI | **NO_TRADE** | 84.94、供給ショック追随禁止 |
| USDJPY | **NO_TRADE** | 長期金利・BOJ・介入要因が衝突 |
| SPX | **NO_TRADE** | 既存BUYは管理、新規押し目買い停止 |
| NASDAQ | **NO_TRADE** | 半導体急落＋高金利。SELL追随もしない |
| DXY | **NO_TRADE** | 金利とFed期待が逆方向 |
| US10Y | **NO_TRADE** | 4.708、直前の急騰を追わない |
| VIX | **NO_TRADE** | 15.84付近まで上昇、まだSELL/BUY双方RR不足 |

BTCは現在約**64560ドル**まで戻っています。citeturn130916finance0 ただし65kの明確な上抜けではなく、ETF/CME需給の継続確認も十分ではないためMES=49。ルール通りNO_TRADEです。

ETHは約**1624.95ドル**で、BTC反発への追随すら確認できないため弱いままです。citeturn130916finance1

VIXはCboeで18日に**15.84**付近まで上昇しています。citeturn382453search7 ただし17～20超への本格的なボラティリティブレイクではありません。

---

## 5. A級候補

**0件。**

A基準に最も遠ざかったのはNASDAQです。

昨日：

**CBS 77 / EMS 70**

から、本日は、

**CBS 61 / EMS 58**

まで引き下げます。

理由は単なる1日の下落ではありません。

**NQ price action  
＋ semiconductor breadth  
＋ Oil  
＋ long yields**

の4要素が同時に悪化したためです。citeturn949563search37turn830069news19

---

## 6. B級監視候補

**本日は新規0件。**

ここは意図的です。

SPX/NASDAQは既存BUYシグナルがまだSLまで到達していないため、そのポジションを新しいBUYシグナルで重ねません。

逆にSELLについても、NASDAQが一日で-1.33%、半導体が約-5%下落した後なので、今日からSELLすると**momentum chase**になりやすい。citeturn949563search37

再びB候補へ戻す条件は、

**SPX：ESが7630を割らず反発＋VIX17未満＋US10Y低下**

**NASDAQ：NQ29200を維持＋半導体安定＋US10Y4.65以下方向**

**GOLD：4360近辺を維持＋US10Y低下＋金自身の反発**

です。

---

## 7. 触らない資産

最優先は**WTI**。

WTIは84.94、Brent91.02。IranはHormuzに関する強硬姿勢を維持し、米国側も現在の交渉継続を否定しています。citeturn130916news49

これは依然、

**Headline → gap → reversal**

の市場です。

次にNASDAQの新規SELL。

方向だけなら昨日から弱気ですが、**売るなら昨日以前であって、-1.3%下落と半導体-5%を確認した後ではない**と判断します。

---

## 8. 後日検証ポイント

今日の最重要検証は、8月14日NASDAQ A級です。

あのA判定は、

**Entry成立 → 正のMFE → 数営業日後に大きく逆行**

という形になりました。

5営業日終了時に必ず、

**最大MFE  
最大MAE  
TP到達有無  
SL到達有無  
5日時間決済リターン**

を確定します。

特に研究価値が高いのは、

**「良いA級を、何営業日保有すべきだったか」**

です。

方向判定そのものと出口設計を分離して評価します。

また18日の市場で、**弱い経済指標にもかかわらず長期金利が上昇した**ことを新regime候補として記録します。これは今後のNASDAQスコアリングに直接影響する可能性があります。citeturn949563news41turn382453news37

本日深夜03:00 JSTのFOMC議事要旨では、

**US10Y / DXY / NQ / ES / GOLD / VIX**

の発表直前→+30分→+1h→米国翌終値を記録対象とします。Fed公式に8月19日14:00 ET公表です。citeturn983433search1

---

## 9. Obsidian保存用Observation Draft

```markdown
# 2026-08-19 Term Premium Shock / New Entries Suspended

## Market

S&P500:
7691.76
-0.69%

NASDAQ Composite:
26289.71
-1.33%

Semiconductor Index:
~ -5%

WTI:
84.94

Brent:
91.02

US10Y:
4.708% close area
intraday ~4.748%

US30Y:
intraday 5.337%

VIX:
~15.84

BTC:
~64560

ETH:
~1625

Gold:
sharp decline
contract-dependent close ~4366-4421

## Regime

TERM_PREMIUM_SHOCK
OIL_INFLATION
TECH_DELEVERAGING
FOMC_MINUTES_AHEAD

## Key regime observation

Weak macro data no longer guarantees lower long yields.

Housing / industrial data soft

but:

oil inflation
+
fiscal supply
+
AI corporate bond issuance
+
global bond selloff

-> long yields remain elevated

-> Nasdaq valuation pressure

## Previous signals

SPX B+:
ENTRY_REACHED
MAE_EXPANDED
SL_NOT_REACHED

NASDAQ B:
ENTRY_REACHED
MAE_EXPANDED
THESIS_WEAKENED
SL_NOT_REACHED

GOLD B:
ENTRY_REACHED
1D_DIRECTION_FAIL

WTI NO_TRADE:
SUCCESSFUL_AVOIDANCE

## New signals

A:
NONE

B+:
NONE

B:
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

## Policy

Do not add to existing SPX/NQ longs.

Do not chase Nasdaq downside after:
Nasdaq -1.33%
Semis ~-5%

Wait for structure confirmation.

## Event

2026-08-19 14:00 ET
FOMC Minutes

Track:
US10Y
DXY
NQ
ES
GOLD
VIX

#TSO #NASDAQ #SPX #US10Y #WTI #FOMC
```

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-08-19,20260819_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,91,38,84,,TERM_PREMIUM_GOLD_PRICE_FAILURE,58,71,84,45,62,66,gold_price_confirmation_failed_under_high_long_yields,GOLD_4360_US10Y_FOMC_1d_3d,partially_verified
2026-08-19,20260819_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,70,48,76,,BTC_64K_RECOVERY_UNCONFIRMED,59,56,67,49,58,49,65000_break_and_sustained_ETF_CME_confirmation_required,BTC_65k_ETF_CME_FOMC_3d_5d,partially_verified
2026-08-19,20260819_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,87,22,97,,ETH_EXTREME_RELATIVE_WEAKNESS,43,46,85,24,41,35,ETH_independent_strength_required,ETH_1600_1800_ETHBTC_3d_5d,partially_verified
2026-08-19,20260819_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,18,99,,HORMUZ_SUPPLY_SHOCK_HIGH_OIL,87,76,99,17,56,75,headline_gap_risk_and_supply_shock_momentum,WTI_85_90_Hormuz_FOMC_3d_5d,verified
2026-08-19,20260819_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,91,30,94,,GLOBAL_YIELD_BOJ_INTERVENTION_CONFLICT,74,77,93,29,62,70,US_Japan_yields_and_intervention_risk_conflict,USDJPY_160_BOJ_US10Y_FOMC_3d,partially_verified
2026-08-19,20260819_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,89,42,82,,EQUITY_PULLBACK_TERM_PREMIUM_SHOCK,62,69,84,49,66,65,new_long_requires_ES_7630_hold_and_yield_VIX_stabilization,ES_7630_VIX17_US10Y_FOMC_1d_3d,verified
2026-08-19,20260819_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,97,31,94,,TECH_DELEVERAGING_LONG_YIELD_SHOCK,58,65,93,36,61,62,new_long_requires_NQ29200_hold_and_semiconductor_yield_stabilization,NQ_29200_SOX_US10Y_FOMC_1d_3d,verified
2026-08-19,20260819_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,84,38,86,,FED_EXPECTATION_TERM_PREMIUM_CONFLICT,71,75,86,39,64,70,FOMC_minutes_can_break_dollar_yield_divergence,DXY_100_US10Y_FOMC_30m_1h_1d,partially_verified
2026-08-19,20260819_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,25,97,,FISCAL_TERM_PREMIUM_GLOBAL_BOND_STRESS,84,88,97,24,73,84,confirmed_yield_reversal_below_4.60_required,US10Y_4.60_4.75_FOMC_30m_1h_1d,verified
2026-08-19,20260819_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,87,39,84,,VOL_EXPANSION_NOT_YET_BREAKOUT,71,66,87,48,66,65,VIX_above_17_with_ES_NQ_structure_break_confirms_risk_off,VIX_17_ES_NQ_FOMC_1d_3d,verified
```

### JSON

```json
[
{"date":"2026-08-19","signal_id":"20260819_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":91,"opp_score":38,"no_trade_score":84,"risk_pct":null,"regime":"TERM_PREMIUM_GOLD_PRICE_FAILURE","ems":58,"ffs":71,"cds":84,"ias":45,"cbs":62,"mes":66,"invalidation":"gold_price_confirmation_failed_under_high_long_yields","verification_target":"GOLD_4360_US10Y_FOMC_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-19","signal_id":"20260819_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":70,"opp_score":48,"no_trade_score":76,"risk_pct":null,"regime":"BTC_64K_RECOVERY_UNCONFIRMED","ems":59,"ffs":56,"cds":67,"ias":49,"cbs":58,"mes":49,"invalidation":"65000_break_and_sustained_ETF_CME_confirmation_required","verification_target":"BTC_65k_ETF_CME_FOMC_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-19","signal_id":"20260819_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":87,"opp_score":22,"no_trade_score":97,"risk_pct":null,"regime":"ETH_EXTREME_RELATIVE_WEAKNESS","ems":43,"ffs":46,"cds":85,"ias":24,"cbs":41,"mes":35,"invalidation":"ETH_independent_strength_required","verification_target":"ETH_1600_1800_ETHBTC_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-19","signal_id":"20260819_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":18,"no_trade_score":99,"risk_pct":null,"regime":"HORMUZ_SUPPLY_SHOCK_HIGH_OIL","ems":87,"ffs":76,"cds":99,"ias":17,"cbs":56,"mes":75,"invalidation":"headline_gap_risk_and_supply_shock_momentum","verification_target":"WTI_85_90_Hormuz_FOMC_3d_5d","verified_status":"verified"},
{"date":"2026-08-19","signal_id":"20260819_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":91,"opp_score":30,"no_trade_score":94,"risk_pct":null,"regime":"GLOBAL_YIELD_BOJ_INTERVENTION_CONFLICT","ems":74,"ffs":77,"cds":93,"ias":29,"cbs":62,"mes":70,"invalidation":"US_Japan_yields_and_intervention_risk_conflict","verification_target":"USDJPY_160_BOJ_US10Y_FOMC_3d","verified_status":"partially_verified"},
{"date":"2026-08-19","signal_id":"20260819_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":89,"opp_score":42,"no_trade_score":82,"risk_pct":null,"regime":"EQUITY_PULLBACK_TERM_PREMIUM_SHOCK","ems":62,"ffs":69,"cds":84,"ias":49,"cbs":66,"mes":65,"invalidation":"new_long_requires_ES_7630_hold_and_yield_VIX_stabilization","verification_target":"ES_7630_VIX17_US10Y_FOMC_1d_3d","verified_status":"verified"},
{"date":"2026-08-19","signal_id":"20260819_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":97,"opp_score":31,"no_trade_score":94,"risk_pct":null,"regime":"TECH_DELEVERAGING_LONG_YIELD_SHOCK","ems":58,"ffs":65,"cds":93,"ias":36,"cbs":61,"mes":62,"invalidation":"new_long_requires_NQ29200_hold_and_semiconductor_yield_stabilization","verification_target":"NQ_29200_SOX_US10Y_FOMC_1d_3d","verified_status":"verified"},
{"date":"2026-08-19","signal_id":"20260819_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":84,"opp_score":38,"no_trade_score":86,"risk_pct":null,"regime":"FED_EXPECTATION_TERM_PREMIUM_CONFLICT","ems":71,"ffs":75,"cds":86,"ias":39,"cbs":64,"mes":70,"invalidation":"FOMC_minutes_can_break_dollar_yield_divergence","verification_target":"DXY_100_US10Y_FOMC_30m_1h_1d","verified_status":"partially_verified"},
{"date":"2026-08-19","signal_id":"20260819_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":25,"no_trade_score":97,"risk_pct":null,"regime":"FISCAL_TERM_PREMIUM_GLOBAL_BOND_STRESS","ems":84,"ffs":88,"cds":97,"ias":24,"cbs":73,"mes":84,"invalidation":"confirmed_yield_reversal_below_4.60_required","verification_target":"US10Y_4.60_4.75_FOMC_30m_1h_1d","verified_status":"verified"},
{"date":"2026-08-19","signal_id":"20260819_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":87,"opp_score":39,"no_trade_score":84,"risk_pct":null,"regime":"VOL_EXPANSION_NOT_YET_BREAKOUT","ems":71,"ffs":66,"cds":87,"ias":48,"cbs":66,"mes":65,"invalidation":"VIX_above_17_with_ES_NQ_structure_break_confirms_risk_off","verification_target":"VIX_17_ES_NQ_FOMC_1d_3d","verified_status":"verified"}
]
```

**8月19日は「何も新規に取らない」がシグナルです。** とくにNASDAQは、これまで機能してきた「弱い景気→金利低下→Growth買い」が長期金利のterm-premium上昇によって壊れ始めた可能性があります。citeturn382453news37turn830069news21

既存のSPX/NASDAQ BUYについてはまだSL到達を確認していないため機械的に撤退判定はしませんが、**追加BUYは停止**。今夜のFOMC議事要旨後にUS10Y・NQ・VIXがどう組み合わさるかを次の再参入判定に使います。citeturn983433search1
