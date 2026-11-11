<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-08-31 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 14054 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026年8月31日

基準時点は**8月31日07:01 JST**。ちょうどCME Globexの週初オープン時刻に当たり、NQ/ES/GC/CLの新セッション価格はまだ安定した取得値が出ていません。そのため金曜清算値＋週末BTC/ETH＋週末ニュースを使用し、該当系列を`partially_verified`とします。CME先物は日曜18:00 ETから再開します。citeturn1search0turn1search5

週末に**重大な新情報**があります。8月30日、米軍がホルムズ海峡に機雷を敷設する準備をしていたとされるイラン・ララク島のミサイル発射設備を攻撃しました。米軍によるイラン攻撃としては7月末以来で、イラン革命防衛隊は報復を表明しています。citeturn2news20turn2news21

これにより、昨日の「月曜まで確認待ち」から状況が変わりました。

## 1. 本日の結論

**A級：0件**

**B+観察候補：WTI BUY**

**B級：なし**

**NO_TRADE：GOLD、BTC、ETH、USDJPY、SPX、NASDAQ、DXY、US10Y、VIX**

最大の変更は**WTI**です。

金曜WTIは83.40まで下落していましたが、これは「ホルムズ海峡の部分正常化・合意期待」が地政学プレミアムを削っていたためでした。実際、WTIは週間4%以上下落しています。citeturn2news10

しかし週末、

**正常化期待 → 米軍攻撃 → イラン報復表明**

へイベント構造が反転しました。

したがってWTIはSELLではなく**BUY監視**へ変更します。ただし供給ショック直後なので、ユーザールール通り**月曜寄りの急騰を成行追随しません**。

BTCは週末約**78225**、ETHは約**2457**。どちらも従来Entry帯ですが、金利＋地政学という二重のrisk-off要因があるためBUYを再開しません。citeturn0news9turn0news4

---

## 2. 前回判断の簡易検証

### BTC NO_TRADE → **妥当**

8月28日80268 → 29日77821 → 30日78225。

週末は78k近辺で下げ止まりましたが、80kを回復できていません。citeturn0news9

昨日の判断は、

**Entry 77000–79000到達  
しかしCME/ETF確認なし → 買わない**

でした。

結果として少なくとも現時点まで「押し目を逃した」というほどの上昇はなく、待機は妥当です。

### ETH NO_TRADE → **妥当**

ETHは28日2511 → 29日2442 → 30日2457。citeturn0news4

2380–2460の旧Entry帯にはありますが、明確な反転確認はありません。

### NASDAQ NO_TRADE → **判断継続**

金曜NQ Sepは**29491.75**、安値29436.25。citeturn1search4

NASDAQのAI earnings仮説そのものはまだ否定しません。しかし金曜はWarsh発言で利上げ確率が35%から約57～58%へ上昇し、NASDAQ総合は0.52%下落しました。citeturn0news89turn1news59

そこへ週末のIran escalationが追加されています。

したがって本日朝のNQを先回りBUYする理由はありません。

### WTI NO_TRADE → **回避成功**

金曜WTIは83.40。市場には「ホルムズ再開合意があるかもしれない」という期待がありました。citeturn2news10

ところが週末に米軍攻撃が発生。

つまり金曜にWTI SELLを作っていた場合、典型的な**週末gap risk**を受ける局面でした。

NO_TRADEは非常に良い回避でした。

---

## 3. 市場全体の前提

本日のRegimeは、

**`IRAN_REESCALATION / HORMUZ_SUPPLY_PREMIUM_RETURN / HAWKISH_FED / CRYPTO_RISK_OFF_RESILIENCE_TEST / AI_THESIS_RATE_PRESSURED`**

です。

マクロ側ではWarsh発言によるFed再評価が残っています。9月25bp利上げ確率は約57～58%。米2年債は4.22%台から4.30～4.35%へ、10年債も4.69%前後へ上昇しました。citeturn0news90turn0news91

そこへ地政学ショックが重なりました。

イラン側は8月29日時点でもホルムズ海峡を掌握しているとの立場を維持し、米国への譲歩を示していませんでした。citeturn2news0turn2news1

そして30日の米軍攻撃後、報復を明言。citeturn2news20turn2news21

したがって今日は、

**金利上昇リスク  
＋原油供給リスク  
＋地政学risk-off**

です。

株式・cryptoを積極的に買う環境ではありません。

一方、米国はベネズエラ産原油を利用してSPRを補充する方針を発表しており、中期的には原油上昇を抑える材料もあります。citeturn2news23

だからWTIもAにはしません。

---

## 4. 10資産別判断

| 資産 | 判定 | 本日 |
|---|---|---|
| GOLD | **NO_TRADE** | 地政学BUY vs 金利・ドルSELL |
| BTC | **NO_TRADE** | 78k支持確認待ち |
| ETH | **NO_TRADE** | 2450近辺、BTC確認待ち |
| WTI | **B+ BUY** | gap追随せず押し限定 |
| USDJPY | **NO_TRADE** | 金利差 vs risk-off円＋介入 |
| SPX | **NO_TRADE** | 二重イベント |
| NASDAQ | **NO_TRADE** | AI仮説生存、金利＋Iran逆風 |
| DXY | **NO_TRADE** | Fed＋safe haven上昇を追わない |
| US10Y | **NO_TRADE** | Warsh後の再価格形成 |
| VIX | **NO_TRADE** | 本日は重要確認系列 |

---

## 5. A級候補

**なし。**

WTIは方向信頼度だけならかなり上昇しましたが、

**供給ショック直後のmomentum追随禁止**

に抵触します。

また、米国・イラン双方の一報で数ドル単位の逆方向gapがあり得ます。

したがってA昇格はしません。

NASDAQについても、

**AI thesis = ALIVE  
immediate BUY thesis = PAUSED**

を維持します。

---

## 6. B級監視候補

### WTI — **B+ BUY / PULLBACK ONLY**

基準となる金曜終値は83.40。citeturn2news10

**Entry 83.50–85.00  
SL 80.50  
TP1 90.00  
TP2 94.00  
RR 約1.83  
win_prob 0.61  
較正参考 0.64  
expected_r 0.43  
MAE想定 0.29R  
risk_pct 0.25%**

CBS **79**  
EMS **78**  
MES **82**

とします。

ただし重要な執行条件があります。

**月曜openが86～88などへgap upした場合、このEntryを上へ追従させません。**

83.5–85.0へ戻らなければ、

**THESIS_SUCCESS / ORDER_NOT_FILLED**

を許容します。

今回の上方向根拠は単なるheadlineではありません。米軍攻撃対象が「ホルムズ海峡へ機雷を敷設する準備をしていた設備」とされており、原油輸送そのものに直接関係します。citeturn2news20

一方、ベネズエラ供給・SPR政策と外交再開余地が上値抑制要因です。citeturn2news23

したがってAではなくB+です。

XM最小ロットでSL到達時の想定実損が3000円以内なら実取引候補。超える場合のみ**実取引NO_TRADE**です。

---

## 7. 触らない資産

本日は特に**NASDAQとGOLDの逆張りBUYを避けます。**

GOLDは本来なら地政学リスクで買われやすいですが、金曜にはWarsh発言によるドル・金利上昇で3%以上急落し、COMEX Decemberは4529.90まで低下しました。citeturn0news86

つまり現在は、

**Iran escalation → GOLD BUY  
Fed tightening → GOLD SELL**

という強い説明変数同士の衝突です。

NASDAQも同じで、

**Nvidia/AI → BUY  
US10Y/Fed/Iran → SELL**

です。

こういう日には方向を無理に決めません。

BTCについても78kだから安いとは扱いません。80k回復＋CME再開後の価格形成を見るまでNO_TRADEです。

---

## 8. 後日検証ポイント

今日は非常に重要です。

最優先で記録するのは、

**WTI Friday 83.40  
→ Weekend US strike  
→ Monday open**

です。

これはTSOの「週末headline gap」の教師データになります。

WTIがgap upして85超を維持するなら、供給プレミアム再構築を支持。

逆に83.40を割るなら、

**市場は攻撃よりHormuz正常化・Venezuela供給を重視**

したことになります。

NASDAQでは、

**NQ 29436（金曜安値）**

を最重要水準とします。citeturn1search4

ここを守り、US10Yが4.7%近辺から上がらなければBUY仮説はまだ再起動可能。

BTCは、

**77000維持  
→ 80000回復  
→ 81200突破**

の順で評価します。

今週はさらに米雇用統計、JOLTS、ADP、ISMがあり、Fedの9月判断に直接影響します。citeturn1news63

したがって今週は「Warsh発言を経済データが追認するか」がNASDAQ・GOLD・DXY・US10Y共通の主要検証テーマです。

---

## 9. Obsidian保存用Observation Draft

```markdown
# 2026-08-31 Iran Re-escalation / Monday Open

## Regime
IRAN_REESCALATION
HORMUZ_SUPPLY_PREMIUM_RETURN
HAWKISH_FED
CRYPTO_RISK_OFF_RESILIENCE_TEST
AI_THESIS_RATE_PRESSURED

## Weekend critical event
2026-08-30:
US forces struck Iranian missile launchers on Larak Island.

US rationale:
launchers reportedly preparing to deploy sea mines into Strait of Hormuz.

Iran:
retaliation promised.

This is first known US strike on Iran since late July.

## Friday reference
WTI:
83.40

NQ Sep:
29491.75
Friday low:
29436.25

US10Y:
~4.69%

Fed Sep hike probability:
~57-58%

Gold Dec:
4529.90

## Weekend crypto
BTC:
~78225

ETH:
~2457

## Main interpretation
Friday Hormuz-normalization premium compression is challenged by weekend escalation.

WTI:
NO_TRADE -> B+ BUY PULLBACK

Do not chase Monday gap.

If price gaps above entry:
THESIS_SUCCESS / ORDER_NOT_FILLED is acceptable.

## Signals
A:
NONE

B+:
WTI BUY

B:
NONE

NO_TRADE:
GOLD
BTC
ETH
USDJPY
SPX
NASDAQ
DXY
US10Y
VIX

## Verification
WTI Monday gap
NQ 29436
US10Y 4.70
BTC 77000 / 80000 / 81200
VIX reaction

#TSO #WTI #Iran #Hormuz #NASDAQ #BTC
```

## 10. TSO_LOG CSV / JSON

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-08-31,20260831_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,96,48,81,,FED_IRAN_GOLD_CONFLICT,81,87,94,46,68,84,US10Y_DXY_decline_or_gold_reclaim_required,GOLD_DXY_US10Y_Iran_1d_3d,partially_verified
2026-08-31,20260831_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,62,73,,BTC_78K_MACRO_GEOPOLITICAL_CONFLICT,68,81,88,59,70,58,77000_hold_and_CME_80000_reclaim_required,BTC_77000_80000_81200_CME_ETF_1d_3d,partially_verified
2026-08-31,20260831_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,96,57,76,,ETH_2450_RISK_OFF_CONFIRMATION_WAIT,65,78,87,55,67,56,BTC_confirmation_and_ETH_2500_reclaim_required,ETH_2380_2500_BTC_CME_1d_3d,partially_verified
2026-08-31,20260831_WTI_BUY_PULLBACK,WTI,BUY,B,PULLBACK,83.50,85.00,80.50,90.00,94.00,1.83,0.61,0.43,99,84,38,0.25,HORMUZ_SUPPLY_PREMIUM_REESCALATION,78,84,96,82,79,82,80.50_break_or_durable_Hormuz_normalization,WTI_85_90_Hormuz_US_Iran_1d_3d_5d,partially_verified
2026-08-31,20260831_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,95,35,91,,FED_RISKOFF_INTERVENTION_CONFLICT,82,86,97,32,63,84,post_open_yield_yen_confirmation_required,USDJPY_DXY_US10Y_Iran_1d_3d,partially_verified
2026-08-31,20260831_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,92,43,84,,HAWKISH_FED_GEOPOLITICAL_RISK,75,77,92,43,67,74,ES_hold_after_Monday_open_required,ES_US10Y_VIX_Iran_1d_3d,partially_verified
2026-08-31,20260831_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,97,54,80,,AI_THESIS_FED_IRAN_PRESSURE,78,84,94,54,71,78,NQ_29436_hold_and_US10Y_stabilization_required,NQ_29436_US10Y_DXY_VIX_semis_1d_3d,partially_verified
2026-08-31,20260831_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,94,40,89,,FED_SAFE_HAVEN_DOLLAR_SUPPORT,84,87,91,39,70,85,post_open_dollar_consolidation_required,DXY_US10Y_Iran_1d_3d,partially_verified
2026-08-31,20260831_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,97,39,93,,HAWKISH_FED_GEOPOLITICAL_DURATION_CONFLICT,89,92,94,36,73,89,post_open_yield_direction_confirmation_required,US10Y_4.70_DXY_NQ_1d_3d,partially_verified
2026-08-31,20260831_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,95,49,82,,WEEKEND_GEOPOLITICAL_VOL_REPRICING,72,69,96,54,68,71,VIX_Monday_open_equity_confirmation_required,VIX_NQ_ES_Iran_1d_3d,partially_verified
```

```json
[
{"date":"2026-08-31","signal_id":"20260831_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":96,"opp_score":48,"no_trade_score":81,"risk_pct":null,"regime":"FED_IRAN_GOLD_CONFLICT","ems":81,"ffs":87,"cds":94,"ias":46,"cbs":68,"mes":84,"invalidation":"US10Y_DXY_decline_or_gold_reclaim_required","verification_target":"GOLD_DXY_US10Y_Iran_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-31","signal_id":"20260831_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":62,"no_trade_score":73,"risk_pct":null,"regime":"BTC_78K_MACRO_GEOPOLITICAL_CONFLICT","ems":68,"ffs":81,"cds":88,"ias":59,"cbs":70,"mes":58,"invalidation":"77000_hold_and_CME_80000_reclaim_required","verification_target":"BTC_77000_80000_81200_CME_ETF_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-31","signal_id":"20260831_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":96,"opp_score":57,"no_trade_score":76,"risk_pct":null,"regime":"ETH_2450_RISK_OFF_CONFIRMATION_WAIT","ems":65,"ffs":78,"cds":87,"ias":55,"cbs":67,"mes":56,"invalidation":"BTC_confirmation_and_ETH_2500_reclaim_required","verification_target":"ETH_2380_2500_BTC_CME_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-31","signal_id":"20260831_WTI_BUY_PULLBACK","asset":"WTI","side":"BUY","rank":"B","type":"PULLBACK","entry_low":83.50,"entry_high":85.00,"sl":80.50,"tp1":90.00,"tp2":94.00,"rr":1.83,"win_prob":0.61,"expected_r":0.43,"tq_score":99,"opp_score":84,"no_trade_score":38,"risk_pct":0.25,"regime":"HORMUZ_SUPPLY_PREMIUM_REESCALATION","ems":78,"ffs":84,"cds":96,"ias":82,"cbs":79,"mes":82,"invalidation":"80.50_break_or_durable_Hormuz_normalization","verification_target":"WTI_85_90_Hormuz_US_Iran_1d_3d_5d","verified_status":"partially_verified"},
{"date":"2026-08-31","signal_id":"20260831_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":95,"opp_score":35,"no_trade_score":91,"risk_pct":null,"regime":"FED_RISKOFF_INTERVENTION_CONFLICT","ems":82,"ffs":86,"cds":97,"ias":32,"cbs":63,"mes":84,"invalidation":"post_open_yield_yen_confirmation_required","verification_target":"USDJPY_DXY_US10Y_Iran_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-31","signal_id":"20260831_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":92,"opp_score":43,"no_trade_score":84,"risk_pct":null,"regime":"HAWKISH_FED_GEOPOLITICAL_RISK","ems":75,"ffs":77,"cds":92,"ias":43,"cbs":67,"mes":74,"invalidation":"ES_hold_after_Monday_open_required","verification_target":"ES_US10Y_VIX_Iran_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-31","signal_id":"20260831_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":97,"opp_score":54,"no_trade_score":80,"risk_pct":null,"regime":"AI_THESIS_FED_IRAN_PRESSURE","ems":78,"ffs":84,"cds":94,"ias":54,"cbs":71,"mes":78,"invalidation":"NQ_29436_hold_and_US10Y_stabilization_required","verification_target":"NQ_29436_US10Y_DXY_VIX_semis_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-31","signal_id":"20260831_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":94,"opp_score":40,"no_trade_score":89,"risk_pct":null,"regime":"FED_SAFE_HAVEN_DOLLAR_SUPPORT","ems":84,"ffs":87,"cds":91,"ias":39,"cbs":70,"mes":85,"invalidation":"post_open_dollar_consolidation_required","verification_target":"DXY_US10Y_Iran_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-31","signal_id":"20260831_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":97,"opp_score":39,"no_trade_score":93,"risk_pct":null,"regime":"HAWKISH_FED_GEOPOLITICAL_DURATION_CONFLICT","ems":89,"ffs":92,"cds":94,"ias":36,"cbs":73,"mes":89,"invalidation":"post_open_yield_direction_confirmation_required","verification_target":"US10Y_4.70_DXY_NQ_1d_3d","verified_status":"partially_verified"},
{"date":"2026-08-31","signal_id":"20260831_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":95,"opp_score":49,"no_trade_score":82,"risk_pct":null,"regime":"WEEKEND_GEOPOLITICAL_VOL_REPRICING","ems":72,"ffs":69,"cds":96,"ias":54,"cbs":68,"mes":71,"invalidation":"VIX_Monday_open_equity_confirmation_required","verification_target":"VIX_NQ_ES_Iran_1d_3d","verified_status":"partially_verified"}
]
```

**本日の核心はWTIです。** 金曜までの「ホルムズ正常化期待」が週末の米軍攻撃で明確に傷つきました。ただし、この材料を見て月曜寄りを追いかけるのはTSOルール違反です。**83.50–85.00までの押しが来た場合だけB+として参加し、gapで走れば取り逃しを許容**します。 memcite
