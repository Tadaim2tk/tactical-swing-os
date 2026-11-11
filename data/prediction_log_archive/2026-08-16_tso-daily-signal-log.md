<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-08-16 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 14958 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026年8月16日

本日は日曜日です。**ES、NQ、COMEX金、WTI、DXY、米10年債、VIXには8月14日（金）以降の通常セッション更新がないため、金曜終値をアンカー**とします。BTC/ETHのみ8月16日朝の現物を新規取得しました。

BTCは**63102ドル**、本日レンジ62749～63121。ETHは**1624.95ドル**です。BTCは金曜日にも米指標の軟化へほとんど反応せず64,000ドルを回復できず、ETFからの資金流出も続いているとの報道があります。citeturn635868finance0turn635868finance1turn680761news18

8月14日のアンカーは、S&P500 7785.76（-0.17%）、NASDAQ総合26729.16（-0.28%）。米小売売上高は前月比-0.6%、ミシガン消費者信頼感は51.0へ低下しました。WTIは82.40、DXYは99.67、VIXは14.25、COMEX金先物は4437.30でした。citeturn635868search73turn635868search24turn936033news34turn936033news32turn936033search5turn936033search3

## 1. 本日の結論

**A級：0件。**

**B級：NASDAQ BUY、SPX BUY、GOLD BUY。**

**B+観察候補：0件。**

**NO_TRADE：BTC、ETH、WTI、USDJPY、DXY、US10Y、VIX。**

本日から月次較正ルールを全面適用します。その結果、前日までより**RRを厳しく再計算**しています。

分析順位は、

**NASDAQ B > SPX B > GOLD B**

です。

ただし、実取引順位は別です。

NASDAQは以前XMで確認した際、最小ロットでも広いSLでは損失が1万円を超えていたため、新基準の約1500円を大幅に超えます。SPXも以前の実測では約3000円規模でした。したがって、**現時点の契約仕様が同じなら両方とも「シグナル成立・実取引NO_TRADE」**です。memcite

GOLDもXM最小ロットで今回の130ドル程度のSL幅を置いた場合の円建て実損を今朝は直接検証できていないため、B+へ上げません。

つまり今日は実質、

**「買い方向を3資産監視するが、週末かつ実執行条件未達なので注文なし」**

です。

---

# 2. 前回判断の簡易検証

### NASDAQ B

昨日は前々日のA級が、

**Entry 29850–30100 → NQ安値30028.5 → Entry成立 → 正のMFE**

まで確認済みでした。

土曜日から日曜日にかけてNQ市場は閉じているため、新しい評価はありません。

**判定：OPEN / NO_NEW_SESSION**

8月14日のA級自体については引き続き5営業日評価対象です。

### SPX B

同じく週末でES更新なし。

8月14日には監視Entryへ到達しており、仮説はまだ失効していません。

**判定：OPEN / NO_NEW_SESSION**

### GOLD B

COMEXも新しいセッションなし。

金曜の米金先物は4437.30で+0.4%。ドル安が金を支えました。citeturn936033search3

**判定：DIRECTION_VALID / NO_NEW_SESSION**

### BTC NO_TRADE

BTCは昨日約62856から今朝63102まで小反発しましたが、依然64,000ドル未満です。citeturn635868finance0

しかも金曜日には、軟調な米経済指標にもかかわらずBTCの反応が弱く、ETF流出継続が需要面の逆風として指摘されました。citeturn680761news18

**NO_TRADE判断を維持します。**

---

# 3. 市場全体の前提

本日のRegimeは、

**`WEEKEND_GROWTH_SCARE / LOW_VOL_EQUITY_RESILIENCE / OIL_GEOPOLITICAL_PREMIUM / CRYPTO_RELATIVE_WEAKNESS`**

とします。

現在は二つのマクロ連鎖が衝突しています。

一方では、

**小売売上-0.6%  
＋消費者信頼感51.0  
＋雇用弱化  
→ Fed追加利上げ圧力低下**

です。小売売上は予想外の減少、消費者信頼感も55.2から51.0へ悪化しました。citeturn635868search73turn635868search24

反対側には、

**WTI 82.40  
＋Hormuz/イラン情勢  
＋高い長期金利  
→ インフレ・term premium圧力**

があります。WTIは8月14日に82.40まで上昇し、Brentも88.52。Reutersはタンカー攻撃と和平交渉停滞を主因として挙げています。citeturn936033news34

それでもVIXは**14.25**と非常に低く、株式市場は景気減速をまだ本格的なrecession shockとして価格付けしていません。citeturn936033search5

今後の重要な判定軸は引き続き、

**bad news = lower rates = equity positive**

から、

**bad news = recession = equity negative**

へ切り替わるかです。

---

# 4. 10資産別判断

| 資産 | 判定 | 要点 |
|---|---|---|
| GOLD | **B BUY** | ドル軟化・景気懸念は追い風、原油・長期金利は逆風 |
| BTC | **NO_TRADE** | 63102、64k回復失敗＋ETF需要弱化 |
| ETH | **NO_TRADE** | 1624.95、独自モメンタム不足 |
| WTI | **NO_TRADE** | Hormuz headline regime |
| USDJPY | **NO_TRADE** | 160接近・介入/BOJリスク |
| SPX | **B BUY** | 高値トレンド維持、景気減速リスク増 |
| NASDAQ | **B BUY** | AIトレンド維持、景気・Oil条件はA未満 |
| DXY | **NO_TRADE** | 99.67、弱いが追随SELLの優位性不足 |
| US10Y | **NO_TRADE** | 景気減速vs原油・財政term premium |
| VIX | **NO_TRADE** | 14.25、ショートRR不良 |

USDJPYは金曜日に159円台で、160円という介入警戒水準へ再接近しています。ReutersはBOJが9月にも追加利上げする可能性を市場が意識していると報じています。citeturn936033search10turn936033news32

BTCについては**MES=43**へさらに引き下げます。価格が63k近辺で、株式Risk-onへの参加が弱いだけでなく、金曜日にはETF流出継続まで確認されたためです。citeturn680761news18

---

# 5. A級候補

**0件です。**

NASDAQはもっとも近いですが、

**CBS 79  
EMS 72  
RR 1.55  
win_prob 0.61  
expected_r 0.42  
MAE想定 0.28R**

と評価。

RRは新基準を満たしましたが、

**expected_r < 0.45  
MAE > 0.25R**

なのでA不合格です。

さらにXM最小ロットで約1500円以内という**執行条件も満たさない可能性が極めて高い**ため、分析スコアだけでAへ上げません。

---

# 6. B級監視候補

### 1位 NASDAQ — BUY PULLBACK

**Entry 29850–30100  
SL 29150  
TP1 31250  
TP2 32100  
RR 1.55  
win_prob 0.61  
expected_r 0.42  
MAE 0.28R  
risk_pct 0.25%**

CBS=79、EMS=72。

定量面ではB+のCBS/EMS/RR/win_prob条件を満たします。

しかし**XM最小ロット実損≤1500円を満たさないためB+不成立・実取引NO_TRADE**です。

---

### 2位 SPX — BUY PULLBACK

**Entry 7740–7780  
SL 7620  
TP1 7980  
TP2 8110  
RR 1.57  
win_prob 0.59  
expected_r 0.39  
MAE 0.30R  
risk_pct 0.25%**

CBS=76、EMS=69。

こちらも定量スコアだけならB+候補ですが、以前XMで確認した約3000円規模の想定損失が現在も同程度なら、新しい1500円基準を超えます。

**B / 実取引NO_TRADE。**

---

### 3位 GOLD — BUY PULLBACK

**Entry 4320–4380  
SL 4220  
TP1 4560  
TP2 4690  
RR 1.62  
win_prob 0.58  
expected_r 0.36  
MAE 0.32R  
risk_pct 0.25%**

CBS=72、EMS=67。

金曜は金先物4437.30まで上昇しています。citeturn936033search3

RRは1.5を超えますが、price confirmationはNASDAQ/SPXより弱く、XM実損条件も未検証。

**通常B**とします。

---

# 7. 触らない資産

最優先は**WTI**です。

WTIは金曜日に82.40へ上昇。背景はタンカー攻撃、Hormuz情勢、米・イラン交渉停滞です。citeturn936033news34

これは引き続き、

**上昇したからBUY  
→ 和平報道で急落  
→ 下落したからSELL  
→ 攻撃報道で急騰**

となり得る環境です。

TSOの通常スイング対象から外します。

BTCも明確なNO_TRADE。今朝63102まで小反発しても、**64k回復・MES>=50・ETF/CME確認**の条件が揃っていません。citeturn635868finance0turn680761news18

---

# 8. 後日検証ポイント

最重要は**8月14日NASDAQ A級**の継続追跡です。

今回は現行Entryモデルで実際に約定帯へ到達したため、

**Entry到達 → 24h → 3営業日 → 5営業日**

についてMFE/MAEを確定します。

同時に8月15日から導入した月次較正の効果も新たに記録します。

特に、

**Signal rank  
→ RRフィルター  
→ XM最小ロットフィルター  
→ 実取引可否**

を分離します。

これによって今後、

> A判定精度は高いが、XMの商品仕様では資金サイズに対して実行できない

という問題を**モデル精度の問題と誤認しない**ようにします。

BTCでは、8月上旬のETF大量流入後に今週流出へ転じ、価格も65k→62～63kへ低下した一連を `FLOW_REVERSAL` の教師データとして残します。金曜日のBTCは64k回復に失敗し、ETF流出が継続していると報じられています。citeturn680761news18

---

# 9. Obsidian保存用Observation Draft

```markdown
# 2026-08-16 Monthly Calibration Applied / Weekend

## Market anchors

BTC:
63102

ETH:
1624.95

Friday:
S&P500 7785.76
NASDAQ Composite 26729.16
Gold futures 4437.30
WTI 82.40
DXY 99.67
VIX 14.25
USDJPY ~159

## Macro

US July retail sales:
-0.6%

Michigan sentiment:
51.0

1y inflation expectations:
4.3%

## Regime

WEEKEND_GROWTH_SCARE
LOW_VOL_EQUITY_RESILIENCE
OIL_GEOPOLITICAL_PREMIUM
CRYPTO_RELATIVE_WEAKNESS

## Monthly calibration first full application

A requirements additionally include:

RR >= 1.2
prefer >= 1.5

SL distance <= 2x TP1 distance

XM minimum-lot expected loss <= ~1500 JPY

Result today:

A: NONE

B:
NASDAQ
SPX
GOLD

B+:
NONE

Reason:

NASDAQ:
quantitative B+ conditions pass,
but broker loss constraint fails.

SPX:
quantitative B+ conditions pass,
but previous broker loss approximately 3000 JPY
> 1500 JPY limit.

GOLD:
RR passes,
but expected_r and MAE weak
and broker loss unverified.

## Crypto

BTC remains around 63k.

64k recovery failure.
ETF outflows reported.
MES lowered to 43.

NO_TRADE.

## Research

Separate:

signal quality
risk/reward quality
broker executability
actual trade outcome

Do not classify broker constraint
as forecasting failure.

#TSO #NASDAQ #SPX #GOLD #BTC #MonthlyCalibration
```

# 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-08-16,20260816_GOLD_BUY_PULLBACK,GOLD,BUY,B,PULLBACK,4320,4380,4220,4560,4690,1.62,0.58,0.36,86,65,48,0.25,WEEKEND_GROWTH_SCARE_GOLD_HEDGE,67,73,78,65,72,68,4220_break_or_DXY_US10Y_oil_reacceleration,GOLD_Monday_entry_24h_3d_5d_MFE_MAE_broker_loss,partially_verified
2026-08-16,20260816_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,81,29,94,,CRYPTO_ETF_OUTFLOW_RELATIVE_WEAKNESS,51,44,79,31,49,43,64000_failure_and_ETF_outflows_keep_MES_below_50,BTC_60k_64k_65k_ETF_CME_flow_3d_5d,verified
2026-08-16,20260816_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,86,23,96,,ETH_SEVERE_RELATIVE_WEAKNESS,44,47,83,26,42,36,ETH_lacks_independent_price_and_flow_confirmation,ETH_1600_1800_ETHBTC_ETF_3d_5d,partially_verified
2026-08-16,20260816_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,97,24,99,,HORMUZ_HEADLINE_SUPPLY_RISK,83,72,98,23,58,71,headline_supply_reversals_dominate_technical_edge,WTI_80_85_Hormuz_Monday_gap_3d_5d,verified
2026-08-16,20260816_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,89,30,95,,USDJPY_160_INTERVENTION_BOJ_RISK,72,74,92,29,63,68,160_intervention_and_BOJ_hike_risk_limit_RR,USDJPY_160_BOJ_DXY_US10Y_3d_5d,partially_verified
2026-08-16,20260816_SPX_BUY_PULLBACK,SPX,BUY,B,PULLBACK,7740,7780,7620,7980,8110,1.57,0.59,0.39,91,69,44,0.25,WEEKEND_RECORD_HIGH_GROWTH_SCARE,69,73,80,74,76,70,7620_break_or_VIX_recession_oil_yield_repricing,ES_Monday_entry_24h_3d_5d_MFE_MAE_broker_loss,partially_verified
2026-08-16,20260816_NASDAQ_BUY_PULLBACK,NASDAQ,BUY,B,PULLBACK,29850,30100,29150,31250,32100,1.55,0.61,0.42,94,74,39,0.25,WEEKEND_AI_UPTREND_GROWTH_SCARE,72,76,82,82,79,72,29150_break_or_growth_recession_VIX_yield_repricing,NQ_Monday_entry_Aug14_A_24h_3d_5d_MFE_MAE_broker_loss,partially_verified
2026-08-16,20260816_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,80,39,84,,WEAK_DATA_SOFT_DOLLAR_OIL_OFFSET,71,72,80,41,65,68,oil_inflation_or_long_yield_rebound_restores_dollar,DXY_100_US10Y_WTI_3d_5d,verified
2026-08-16,20260816_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,91,36,91,,GROWTH_SCARE_FISCAL_OIL_CONFLICT,75,82,91,37,68,77,growth_slowdown_conflicts_with_fiscal_and_oil_term_premium,US10Y_4.60_4.70_WTI_growth_3d_5d,partially_verified
2026-08-16,20260816_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,85,29,92,,EXTREME_LOW_VOL_MACRO_GEOPOLITICAL_RISK,66,61,88,47,63,60,VIX_expansion_despite_shallow_equity_drawdown,VIX_14_15_ES_NQ_Monday_gap_3d_5d,verified
```

## JSON

```json
[
{"date":"2026-08-16","signal_id":"20260816_GOLD_BUY_PULLBACK","asset":"GOLD","side":"BUY","rank":"B","type":"PULLBACK","entry_low":4320,"entry_high":4380,"sl":4220,"tp1":4560,"tp2":4690,"rr":1.62,"win_prob":0.58,"expected_r":0.36,"tq_score":86,"opp_score":65,"no_trade_score":48,"risk_pct":0.25,"regime":"WEEKEND_GROWTH_SCARE_GOLD_HEDGE","ems":67,"ffs":73,"cds":78,"ias":65,"cbs":72,"mes":68,"invalidation":"4220_break_or_DXY_US10Y_oil_reacceleration","verification_target":"GOLD_Monday_entry_24h_3d_5d_MFE_MAE_broker_loss","verified_status":"partially_verified"},
{"date":"2026-08-16","signal_id":"20260816_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":81,"opp_score":29,"no_trade_score":94,"risk_pct":null,"regime":"CRYPTO_ETF_OUTFLOW_RELATIVE_WEAKNESS","ems":51,"ffs":44,"cds":79,"ias":31,"cbs":49,"mes":43,"invalidation":"64000_failure_and_ETF_outflows_keep_MES_below_50","verification_target":"BTC_60k_64k_65k_ETF_CME_flow_3d_5d","verified_status":"verified"},
{"date":"2026-08-16","signal_id":"20260816_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":86,"opp_score":23,"no_trade_score":96,"risk_pct":null,"regime":"ETH_SEVERE_RELATIVE_WEAKNESS","ems":44,"ffs":47,"cds":83,"ias":26,"cbs":42,"mes":36,"invalidation":"ETH_lacks_independent_price_and_flow_confirmation","verification_target":"ETH_1600_1800_ETHBTC_ETF_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-16","signal_id":"20260816_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":97,"opp_score":24,"no_trade_score":99,"risk_pct":null,"regime":"HORMUZ_HEADLINE_SUPPLY_RISK","ems":83,"ffs":72,"cds":98,"ias":23,"cbs":58,"mes":71,"invalidation":"headline_supply_reversals_dominate_technical_edge","verification_target":"WTI_80_85_Hormuz_Monday_gap_3d_5d","verified_status":"verified"},
{"date":"2026-08-16","signal_id":"20260816_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":89,"opp_score":30,"no_trade_score":95,"risk_pct":null,"regime":"USDJPY_160_INTERVENTION_BOJ_RISK","ems":72,"ffs":74,"cds":92,"ias":29,"cbs":63,"mes":68,"invalidation":"160_intervention_and_BOJ_hike_risk_limit_RR","verification_target":"USDJPY_160_BOJ_DXY_US10Y_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-16","signal_id":"20260816_SPX_BUY_PULLBACK","asset":"SPX","side":"BUY","rank":"B","type":"PULLBACK","entry_low":7740,"entry_high":7780,"sl":7620,"tp1":7980,"tp2":8110,"rr":1.57,"win_prob":0.59,"expected_r":0.39,"tq_score":91,"opp_score":69,"no_trade_score":44,"risk_pct":0.25,"regime":"WEEKEND_RECORD_HIGH_GROWTH_SCARE","ems":69,"ffs":73,"cds":80,"ias":74,"cbs":76,"mes":70,"invalidation":"7620_break_or_VIX_recession_oil_yield_repricing","verification_target":"ES_Monday_entry_24h_3d_5d_MFE_MAE_broker_loss","verified_status":"partially_verified"},
{"date":"2026-08-16","signal_id":"20260816_NASDAQ_BUY_PULLBACK","asset":"NASDAQ","side":"BUY","rank":"B","type":"PULLBACK","entry_low":29850,"entry_high":30100,"sl":29150,"tp1":31250,"tp2":32100,"rr":1.55,"win_prob":0.61,"expected_r":0.42,"tq_score":94,"opp_score":74,"no_trade_score":39,"risk_pct":0.25,"regime":"WEEKEND_AI_UPTREND_GROWTH_SCARE","ems":72,"ffs":76,"cds":82,"ias":82,"cbs":79,"mes":72,"invalidation":"29150_break_or_growth_recession_VIX_yield_repricing","verification_target":"NQ_Monday_entry_Aug14_A_24h_3d_5d_MFE_MAE_broker_loss","verified_status":"partially_verified"},
{"date":"2026-08-16","signal_id":"20260816_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":80,"opp_score":39,"no_trade_score":84,"risk_pct":null,"regime":"WEAK_DATA_SOFT_DOLLAR_OIL_OFFSET","ems":71,"ffs":72,"cds":80,"ias":41,"cbs":65,"mes":68,"invalidation":"oil_inflation_or_long_yield_rebound_restores_dollar","verification_target":"DXY_100_US10Y_WTI_3d_5d","verified_status":"verified"},
{"date":"2026-08-16","signal_id":"20260816_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":91,"opp_score":36,"no_trade_score":91,"risk_pct":null,"regime":"GROWTH_SCARE_FISCAL_OIL_CONFLICT","ems":75,"ffs":82,"cds":91,"ias":37,"cbs":68,"mes":77,"invalidation":"growth_slowdown_conflicts_with_fiscal_and_oil_term_premium","verification_target":"US10Y_4.60_4.70_WTI_growth_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-16","signal_id":"20260816_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":85,"opp_score":29,"no_trade_score":92,"risk_pct":null,"regime":"EXTREME_LOW_VOL_MACRO_GEOPOLITICAL_RISK","ems":66,"ffs":61,"cds":88,"ias":47,"cbs":63,"mes":60,"invalidation":"VIX_expansion_despite_shallow_equity_drawdown","verification_target":"VIX_14_15_ES_NQ_Monday_gap_3d_5d","verified_status":"verified"}
]
```

**8月16日の最大の変更は月次較正です。** 方向分析としてはNASDAQ・SPX・GOLDを引き続き買い監視できますが、RRだけでなく**XM最小ロットで約1500円以内**という執行ゲートを通すと、現状では実際に注文すべき候補はありません。

これはシグナルを弱くしたのではなく、**「予測精度」と「現在の資金量・ブローカー仕様で安全に取引できるか」を明確に分離した**結果です。
