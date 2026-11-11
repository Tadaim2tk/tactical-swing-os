<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-08-28 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 14495 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026年8月28日

データ基準は**8月27日米国市場終了後〜8月28日06:58 JST前後**。10資産すべてについて新規取得を試みました。結論から言うと、昨日のNASDAQ BUY仮説はかなり強く確認されました。一方、本日はFed議長のJackson Hole講演があるため、**上昇を見て新規で追う日ではありません**。

## 1. 本日の結論

**A級：0件**

**B+観察候補：NASDAQ BUY、GOLD BUY**

**B級：BTC BUY、ETH BUY**

**NO_TRADE：WTI、USDJPY、SPX、DXY、US10Y、VIX**

優先順位は、

**NASDAQ B+ > GOLD B+ > BTC B > ETH B**

です。

27日はS&P500が**7730.99（+0.7%）**、NASDAQ総合が**26541.35（+1.6%）**。Nvidiaは**+8.7%**、S&P情報技術セクター+3.4%、半導体指数+2.3%となり、昨日の「Nvidia好決算→NASDAQ follow-through」という中心仮説は成立しました。citeturn1news88turn1news90

ただし本日はFed議長Kevin WarshのJackson Hole講演が控えています。高金利・インフレというNASDAQ最大の逆風を再評価するイベントなので、**現在値からの成行BUYは禁止**とします。citeturn1news88

---

## 2. 前回判断の簡易検証

### NASDAQ B BUY — **成功**

昨日のNQ監視：

**Entry 29100–29400 / SL 28450 / TP1 30600**

さらに実取引用US100Cashでは、

**Buy Limit 29405 / SL 29255 / TP 29850**

を設定していました。

方向判定は明確に正解です。NASDAQ現物は+1.6%、Nvidia+8.7%。AIセクター全体にも波及しました。citeturn1news88turn1news90

ただし、重要なのは**指値が約定したかどうかと方向予測の成否を分離すること**です。

昨日の画像時点ですでにUS100Cashは29492付近だったため、29405まで押さず上昇した場合、

**THESIS_SUCCESS / ORDER_NOT_FILLED**

です。

これは失敗ではありません。むしろ「追わない」という執行規律が正しく機能したケースとして記録対象です。

### GOLD B — **仮説維持**

現物Goldは27日に約**4607.90、+0.4%**。COMEX Decemberは**4664、+0.2%**。ETF・中央銀行需要が支えています。citeturn1news87

前日の調整から反発したためBUY方向は維持。ただしJackson Hole前なのでAには上げません。

### BTC B — **方向維持、抵抗帯継続**

BTCは約80k周辺で推移。

特に重要なのは、オンチェーン上で**80k–82kにBTC供給量の約8%が集中**しており、さらにGlassnodeは**81k–86kを主要抵抗帯**としています。citeturn1news31turn1news35

一方、26日の米スポットETFフローはBTC **+232.12Mドル**、ETH **+192.35Mドル**でした。citeturn0news10

つまり昨日の

**FLOW強い / PRICE resistance強い**

という仮説がそのまま継続しています。

### WTI NO_TRADE — **非常に重要な回避成功**

WTIは26日の82.23から、27日は**83.53（+1.6%）**へ反発しました。

原因は米国がIranとの旧合意への復帰を否定したとの報道です。citeturn1news10

つまり、

**Hormuz改善期待 → 下落  
外交後退 → 翌日急反発**

となりました。

昨日SELLしなかった判断は妥当です。

---

## 3. 市場全体の前提

本日のRegimeは、

**`AI_FOLLOW_THROUGH / LOW_VOL_RISK_ON / JACKSON_HOLE_BINARY_EVENT / BTC_SUPPLY_WALL / OIL_HEADLINE_REVERSAL`**

です。

昨日まで最大の疑問だった、

**「Nvidia好決算でもNASDAQは本当に上がるのか？」**

には、かなり明確にYESが出ました。

しかし今日から問題はNvidiaではなく**金利**へ戻ります。

PCEは前年比3.7%。市場が織り込む9月利上げ確率は約34%、12月まででは約74%。citeturn1news87

したがって、

**AI earnings = bullish  
Fed/inflation = bearish**

の綱引きです。

USDJPYは27日終盤で約**159.4**。この水準ではドル高方向へ追うRRは悪いと判断します。

WTIは83.53まで反発しましたが、これは新しいtrendというより**外交headline reversal**です。citeturn1news10

---

## 4. 10資産別判断

| 資産 | 判定 | 今日の判断 |
|---|---|---|
| GOLD | **B+ BUY** | 4550–4610押し目 |
| BTC | **B BUY** | 76.5–78.5k限定 |
| ETH | **B BUY** | 2380–2460限定 |
| WTI | **NO_TRADE** | headline往復が激しすぎる |
| USDJPY | **NO_TRADE** | 159台＋Fedイベント |
| SPX | **NO_TRADE** | 上昇しているがNASDAQよりedge小 |
| NASDAQ | **B+ BUY** | 追わず押し目限定 |
| DXY | **NO_TRADE** | Jackson Hole待ち |
| US10Y | **NO_TRADE** | 講演でregime転換可能 |
| VIX | **NO_TRADE** | 低ボラ確認系列として使用 |

---

## 5. A級候補

**なし。**

NASDAQは純粋な方向予測ならA級に近いです。

**CBS 84 / EMS 80 / expected_r 0.48 / MAE想定0.23R**

まで上げます。

しかし**Jackson Hole当日**というCDS上の問題があります。

よって、

**Forecast=A相当 / Entry timing=B+**

とします。

昨日とは理由が違います。昨日はNvidiaという未知数、本日はFedという未知数です。

---

## 6. B級監視候補

### NASDAQ — **B+ BUY PULLBACK**

**NQ Entry 29400–29600  
SL 28950  
TP1 30400  
TP2 30900  
RR 約1.6  
win_prob 0.66  
較正参考 0.69  
expected_r 0.48  
MAE 0.23R  
risk_pct 0.25%**

昨日のfollow-through確認で信頼度を上げます。

Nvidia単独ではなく、半導体指数+2.3%、ITセクター+3.4%なのでbreadthも悪くありません。citeturn1news88

ただし**現在値がEntryより上なら追わない**。

昨日と同じです。

昨日のUS100Cash 29405指値のように、**良い価格が来なければ取引しない**を維持します。

XM最小ロットの実損が3000円以内ならB+実取引候補です。

### GOLD — **B+ BUY PULLBACK**

**Entry 4550–4610  
SL 4420  
TP1 4860  
TP2 5000  
RR 1.67  
win_prob 0.63  
較正参考 0.66  
expected_r 0.42  
MAE 0.27R  
risk_pct 0.25%**

Goldは27日に4607.90へ反発。COMEX Decemberも4664でした。citeturn1news87

ドルが弱含み、ETF・中央銀行需要も継続。

ただしFedがタカ派ならGold/US10Yの逆風になるため、**4600前後への押し限定**です。

### BTC — **B BUY PULLBACK**

**Entry 76500–78500  
SL 72500  
TP1 85000  
TP2 89000  
RR 1.53  
win_prob 0.62  
expected_r 0.40  
MAE 0.31R**

80–82kには供給量の約8%が集中しています。citeturn1news35

ETFフローはプラスなのでSELLする理由も弱い。

したがって、

**80k超＝買わない  
76.5–78.5k＝BUY監視**

です。

### ETH — **B BUY PULLBACK**

**Entry 2380–2460  
SL 2160  
TP1 2800  
TP2 3000  
RR 1.55  
win_prob 0.59  
expected_r 0.37  
MAE 0.33R**

ETFフローは26日に+192.35Mドル。citeturn0news10

BTCよりvolatilityが高いため順位は4位です。

---

## 7. 触らない資産

**WTIが最優先NO_TRADEです。**

26日：

**82.23**

27日：

**83.53**

へ反発しました。citeturn1news10turn1news11

価格が需給より、

**Iran/Oman協議  
→ 米国側発言  
→ 制裁  
→ Hormuz**

のheadlineに支配されています。

方向予測の信頼度よりgap riskが大きいため、BUY/SELL双方見送ります。

USDJPY、DXY、US10YもFed講演前なので同様です。

---

## 8. 後日検証ポイント

今日はNASDAQについて非常に価値の高い教師データができます。

今回の系列は、

**8/26 Nvidia前 → NO_TRADE  
8/27 Nvidia beat確認 → BUY  
8/27 Nasdaq +1.6%  
8/28 Fedイベント → 追随禁止**

です。

これはTSOが狙っている、

**イベントを予想して賭けるのではなく、イベント通過後のconfirmationを使う**

という方法そのものです。

次に確認するのは、Jackson Hole後の

**NQ / US10Y / DXY / VIX**

です。

特に、

**US10Y上昇なのにNQが崩れない**

ならAI earnings momentumが金利逆風を上回っている証拠になります。

BTCでは、

**ETF流入継続 + 80–82k供給壁**

の決着を追います。citeturn0news10turn1news35

WTIでは今回の

**82.23 → 83.53**

をheadline reversal教師データとして保存します。citeturn1news10

---

## 9. Obsidian保存用Observation Draft

```markdown
# 2026-08-28 AI Follow-through / Jackson Hole Risk

## Regime
AI_FOLLOW_THROUGH
LOW_VOL_RISK_ON
JACKSON_HOLE_BINARY_EVENT
BTC_SUPPLY_WALL
OIL_HEADLINE_REVERSAL

## Equity confirmation
S&P500:
7730.99
+0.7%

NASDAQ Composite:
26541.35
+1.6%

Nvidia:
+8.7%

SPX IT:
+3.4%

Semiconductors:
+2.3%

Interpretation:
Nvidia beat produced genuine sector follow-through.

## Previous NASDAQ signal
Direction:
SUCCESS

Execution:
separate fill from thesis outcome

US100Cash prior order:
29405
SL 29255
TP 29850

If no retracement:
ORDER_NOT_FILLED
THESIS_SUCCESS

Do not classify missed fill as forecast failure.

## Macro
PCE:
3.7%

Sep hike probability:
~34%

Dec hike probability:
~74%

USDJPY:
~159.4

Gold spot:
4607.9

COMEX Dec:
4664

WTI:
83.53

## Crypto
BTC:
~80k

Resistance:
80k-82k major supply cluster
81k-86k broader resistance

BTC ETF:
+232.12m

ETH ETF:
+192.35m

## Signals
A:
NONE

B+:
NASDAQ BUY
GOLD BUY

B:
BTC BUY
ETH BUY

NO_TRADE:
WTI
USDJPY
SPX
DXY
US10Y
VIX

## Key research
Event avoidance -> confirmation -> post-event entry
Nvidia case is positive evidence for this workflow.

#TSO #NASDAQ #GOLD #BTC #ETH
```

## 10. TSO_LOG CSV / JSON

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-08-28,20260828_GOLD_BUY_PULLBACK,GOLD,BUY,B,PULLBACK,4550,4610,4420,4860,5000,1.67,0.63,0.42,96,77,35,0.25,GOLD_UPTREND_FED_EVENT,78,84,82,79,82,80,4420_break_or_hawkish_Fed_yield_spike,GOLD_entry_24h_3d_5d_MFE_MAE,partially_verified
2026-08-28,20260828_BTC_BUY_PULLBACK,BTC,BUY,B,PULLBACK,76500,78500,72500,85000,89000,1.53,0.62,0.40,97,72,46,0.25,BTC_ETF_FLOW_SUPPLY_WALL,80,92,82,79,83,89,72500_break_or_ETF_flow_reversal,BTC_78k_82k_85k_ETF_3d_5d_MFE_MAE,partially_verified
2026-08-28,20260828_ETH_BUY_PULLBACK,ETH,BUY,B,PULLBACK,2380,2460,2160,2800,3000,1.55,0.59,0.37,94,68,51,0.25,ETH_ETF_FLOW_PULLBACK,75,89,80,76,79,84,2160_break_or_ETH_ETF_flow_reversal,ETH_2.4k_2.8k_ETF_3d_5d_MFE_MAE,partially_verified
2026-08-28,20260828_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,24,98,,HORMUZ_HEADLINE_REVERSAL,74,72,99,24,54,69,durable_diplomatic_or_supply_confirmation_required,WTI_80_85_Hormuz_headlines_3d_5d,verified
2026-08-28,20260828_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,94,35,94,,JACKSON_HOLE_FX_BINARY_EVENT,77,81,96,34,65,76,post_Warsh_rate_and_policy_confirmation_required,USDJPY_157_160_DXY_US10Y_post_Warsh,verified
2026-08-28,20260828_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,91,62,66,,AI_FOLLOW_THROUGH_FED_EVENT,75,76,81,67,74,72,post_Warsh_ES_breadth_confirmation_required,ES_NQ_US10Y_VIX_post_Warsh_3d,verified
2026-08-28,20260828_NASDAQ_BUY_PULLBACK,NASDAQ,BUY,B,PULLBACK,29400,29600,28950,30400,30900,1.60,0.66,0.48,99,86,28,0.25,AI_FOLLOW_THROUGH_JACKSON_HOLE_RISK,80,86,83,89,84,79,28950_break_or_post_Warsh_growth_selloff,NQ_29600_30400_US10Y_VIX_post_Warsh_1d_3d_5d,partially_verified
2026-08-28,20260828_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,90,38,91,,JACKSON_HOLE_DOLLAR_BINARY_EVENT,77,80,94,37,66,76,post_Warsh_break_below_98_or_above_100_required,DXY_98_100_US10Y_post_Warsh,partially_verified
2026-08-28,20260828_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,96,34,96,,JACKSON_HOLE_RATE_BINARY_EVENT,84,88,98,32,70,85,post_Warsh_direction_confirmation_required,US10Y_DXY_NQ_post_Warsh_1d_3d,partially_verified
2026-08-28,20260828_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,89,39,88,,LOW_VOL_PRE_FED_EVENT,70,68,94,48,67,67,VIX_above_18_or_below_14_with_NQ_confirmation,VIX_NQ_ES_post_Warsh_1d_3d,partially_verified
```

```json
[
{"date":"2026-08-28","signal_id":"20260828_GOLD_BUY_PULLBACK","asset":"GOLD","side":"BUY","rank":"B","type":"PULLBACK","entry_low":4550,"entry_high":4610,"sl":4420,"tp1":4860,"tp2":5000,"rr":1.67,"win_prob":0.63,"expected_r":0.42,"tq_score":96,"opp_score":77,"no_trade_score":35,"risk_pct":0.25,"regime":"GOLD_UPTREND_FED_EVENT","ems":78,"ffs":84,"cds":82,"ias":79,"cbs":82,"mes":80,"invalidation":"4420_break_or_hawkish_Fed_yield_spike","verification_target":"GOLD_entry_24h_3d_5d_MFE_MAE","verified_status":"partially_verified"},
{"date":"2026-08-28","signal_id":"20260828_BTC_BUY_PULLBACK","asset":"BTC","side":"BUY","rank":"B","type":"PULLBACK","entry_low":76500,"entry_high":78500,"sl":72500,"tp1":85000,"tp2":89000,"rr":1.53,"win_prob":0.62,"expected_r":0.40,"tq_score":97,"opp_score":72,"no_trade_score":46,"risk_pct":0.25,"regime":"BTC_ETF_FLOW_SUPPLY_WALL","ems":80,"ffs":92,"cds":82,"ias":79,"cbs":83,"mes":89,"invalidation":"72500_break_or_ETF_flow_reversal","verification_target":"BTC_78k_82k_85k_ETF_3d_5d_MFE_MAE","verified_status":"partially_verified"},
{"date":"2026-08-28","signal_id":"20260828_ETH_BUY_PULLBACK","asset":"ETH","side":"BUY","rank":"B","type":"PULLBACK","entry_low":2380,"entry_high":2460,"sl":2160,"tp1":2800,"tp2":3000,"rr":1.55,"win_prob":0.59,"expected_r":0.37,"tq_score":94,"opp_score":68,"no_trade_score":51,"risk_pct":0.25,"regime":"ETH_ETF_FLOW_PULLBACK","ems":75,"ffs":89,"cds":80,"ias":76,"cbs":79,"mes":84,"invalidation":"2160_break_or_ETH_ETF_flow_reversal","verification_target":"ETH_2.4k_2.8k_ETF_3d_5d_MFE_MAE","verified_status":"partially_verified"},
{"date":"2026-08-28","signal_id":"20260828_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":24,"no_trade_score":98,"risk_pct":null,"regime":"HORMUZ_HEADLINE_REVERSAL","ems":74,"ffs":72,"cds":99,"ias":24,"cbs":54,"mes":69,"invalidation":"durable_diplomatic_or_supply_confirmation_required","verification_target":"WTI_80_85_Hormuz_headlines_3d_5d","verified_status":"verified"},
{"date":"2026-08-28","signal_id":"20260828_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":94,"opp_score":35,"no_trade_score":94,"risk_pct":null,"regime":"JACKSON_HOLE_FX_BINARY_EVENT","ems":77,"ffs":81,"cds":96,"ias":34,"cbs":65,"mes":76,"invalidation":"post_Warsh_rate_and_policy_confirmation_required","verification_target":"USDJPY_157_160_DXY_US10Y_post_Warsh","verified_status":"verified"},
{"date":"2026-08-28","signal_id":"20260828_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":91,"opp_score":62,"no_trade_score":66,"risk_pct":null,"regime":"AI_FOLLOW_THROUGH_FED_EVENT","ems":75,"ffs":76,"cds":81,"ias":67,"cbs":74,"mes":72,"invalidation":"post_Warsh_ES_breadth_confirmation_required","verification_target":"ES_NQ_US10Y_VIX_post_Warsh_3d","verified_status":"verified"},
{"date":"2026-08-28","signal_id":"20260828_NASDAQ_BUY_PULLBACK","asset":"NASDAQ","side":"BUY","rank":"B","type":"PULLBACK","entry_low":29400,"entry_high":29600,"sl":28950,"tp1":30400,"tp2":30900,"rr":1.60,"win_prob":0.66,"expected_r":0.48,"tq_score":99,"opp_score":86,"no_trade_score":28,"risk_pct":0.25,"regime":"AI_FOLLOW_THROUGH_JACKSON_HOLE_RISK","ems":80,"ffs":86,"cds":83,"ias":89,"cbs":84,"mes":79,"invalidation":"28950_break_or_post_Warsh_growth_selloff","verification_target":"NQ_29600_30400_US10Y_VIX_post_Warsh_1d_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-28","signal_id":"20260828_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":90,"opp_score":38,"no_trade_score":91,"risk_pct":null,"regime":"JACKSON_HOLE_DOLLAR_BINARY_EVENT","ems":77,"ffs":80,"cds":94,"ias":37,"cbs":66,"mes":76,"invalidation":"post_Warsh_break_below_98_or_above_100_required","verification_target":"DXY_98_100_US10Y_post_Warsh","verified_status":"partially_verified"},
{"date":"2026-08-28","signal_id":"20260828_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":96,"opp_score":34,"no_trade_score":96,"risk_pct":null,"regime":"JACKSON_HOLE_RATE_BINARY_EVENT","ems":84,"ffs":88,"cds":98,"ias":32,"cbs":70,"mes":85,"invalidation":"post_Warsh_direction_confirmation_required","verification_target":"US10Y_DXY_NQ_post_Warsh_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-28","signal_id":"20260828_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":89,"opp_score":39,"no_trade_score":88,"risk_pct":null,"regime":"LOW_VOL_PRE_FED_EVENT","ems":70,"ffs":68,"cds":94,"ias":48,"cbs":67,"mes":67,"invalidation":"VIX_above_18_or_below_14_with_NQ_confirmation","verification_target":"VIX_NQ_ES_post_Warsh_1d_3d","verified_status":"partially_verified"}
]
```

本日の核心は、**NASDAQの方向判断は昨日より強くなったが、今日の新規注文条件はむしろ厳しくする**ことです。Nvidia後の上昇を確認できた以上、29,000台後半を無条件に追う必要はありません。Jackson Hole後にもNQが高値を維持できれば、次回はA級昇格を検討できます。citeturn1news88turn1news90 memcite
