<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-20 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-21T12:59:52Z / chars: 16556 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-09-20

**使用モデル：GPT-5.6 Sol**  
**本日の市場の主役：WTI**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**データ基準：2026年9月18日米国終値＋9月19日週末ニュース＋9月20日06:57 JST時点のBTC/ETH。日曜のため非Crypto資産は休場。**  
**crypto_grounds: etf=有, cme=有** — 9/18のBTC ETFはFarsideの現時点集計で少なくとも+324.6Mドル、ETH ETFは+29.4Mドル。BTC側は一部ファンド欄が未反映なので総額だけ`partially_verified`扱いです。citeturn340546search0turn340546search1  
**expected_r_basis: subjective** — 本日の新規方向シグナルは0件。既存WTIとUSDJPYは発行済み値を変更せず、未約定確率・イベントギャップ・介入/地政学リスクを含むsubjective基準を維持します。

**invalidation_check: 20260917_WTI_BUY_PULLBACK=not_fired, 20260919_USDJPY_BUY_PULLBACK=not_fired**

今朝の最大の新情報は、**土曜日にサウジへのHouthi攻撃が再び激化したこと**です。Reuters映像ではリヤド空港付近で炎と黒煙が確認され、Houthi側はYanbuのAramco施設も攻撃したと主張しました。サウジ連合側はYanbu攻撃を阻止したとしていますが、損害の有無は明らかにしていません。つまり、WTIの既存BUY仮説に対しては**週末に再び上方向の供給リスクが追加された**一方、実際の生産・輸出被害はまだ未確認です。citeturn119244view0

urlReuters：9月19日のサウジ・Houthi攻撃turn119244view0  
urlReuters：9月18日のWTI市場turn351381view1  
urlReuters：BOJ後のドル円・rate checkturn351381view0  
urlFarside：Bitcoin ETF flowsturn340546search0

## 1. 本日の結論

**新規A級：0件**  
**新規B級：0件**  
**既存B：WTI BUYを継続HOLD**  
**既存B+監視：USDJPY BUY_PULLBACKを月曜まで待機**  
**本日新規実取引：NO_TRADE**

日曜なので、ここで無理に新しい方向シグナルを作る意味はありません。

むしろ今朝は、**既存WTI BUYにとって週末ニュースが有利に変化した**ことが重要です。

金曜のWTI清算値は**100.30**。その時点では中国がIranにHouthi攻撃抑制を求めたことが弱材料でしたが、その翌日に実際の攻撃が再びリヤド・Yanbu方面へ拡大しました。Hormuzも金曜時点で通過commodity vesselが4隻、10日平均約16隻と依然異常な低水準です。citeturn351381view1turn119244view0

したがって既存実取引、

**Entry：約101.19**  
**SL：98.90**  
**TP：105.20**

はそのまま。

**HOLD / SLを広げない / 追加BUYもしない**です。

USDJPYは前日B+、

**Entry 156.00–156.50  
SL 155.20  
TP1 158.20  
TP2 159.60**

を維持しますが、金曜高値158.05のあとrate checkで156.725まで戻されています。月曜に157円台後半で始まっても追いません。citeturn351381view0

---

## 2. 前回判断の簡易検証

### `20260917_WTI_BUY_PULLBACK`

金曜終値はWTI **100.30**。SL98.90には未到達です。Saudi East-West Pipelineは3つのポンプ施設損傷が確認され、復旧時期には依然幅があり、Hormuzも正常化していません。citeturn351381view1

さらに土曜にはHouthi側がYanbuのAramco施設への攻撃を主張。サウジ側は阻止したとしていますが、同時にリヤド空港付近では実際に煙と炎が確認されています。citeturn119244view0

したがって、

**ENTRY_FILLED / SL_NOT_REACHED / TP_NOT_REACHED / invalidation=not_fired**

です。

金曜終了時点では主観勝率を約0.51–0.54まで落としていましたが、週末攻撃を織り込むと**約0.56–0.59程度へ再上方修正**します。

ただしこれは月曜のギャップを見ていない段階の評価です。週明けにWTIがほとんど反応しなければ、この上方修正は取り消します。

### `20260919_USDJPY_BUY_PULLBACK`

これは土曜発行なので、**まだ市場で約定機会そのものがありません**。

金曜のUSDJPYはBOJ後に158.05まで上昇し、その後rate check報道で156.725付近まで押し戻されました。BOJは1.25%へ利上げしましたが7対2で、市場は追加利上げへの確信を弱めました。citeturn351381view0

したがって、

**UNFILLED / invalidation=not_fired**

です。

実際の円買い介入は確認されていません。

---

## 3. 市場全体の前提

金曜終了時点ではrisk assetはかなり強いです。

NQZ26の9月18日清算値は**29917.25**、高値29993.25。ESZ26は**7712.50**。NQはほぼ30000まで戻しました。citeturn477802search3turn719247search4

一方で米10年債利回りは**4.996%**。つまり「10年債5%近辺でもNASDAQが崩れない」という価格構造が続いています。citeturn972933search1

VIXは**14.81**まで低下。金曜時点の市場は明確に恐怖を織り込んでいませんでした。citeturn972933search7

Goldは基準のGCZ26で**4415.90**。ここは前日の約4425という近似より、今回再取得した同一限月の終値4415.90を基準値として採用します。高値は4439.60でした。citeturn719247search5

DXY系は約**99.94**、US10Yは約5%。つまり金利・ドルは強いままですがGold・NASDAQ・Cryptoがそれに耐えています。citeturn972933search4turn972933search1

Cryptoは週末も強さを維持しています。BTC/USDは約**81.0–81.3k**、ETH/USDは約**2620–2630**。9月18日のCME側でもBTCはかなり強く、ETH futuresは**2643.5**まで上昇しました。citeturn415739search3turn415739search4turn828579search0turn828579search5

ただしBTC・ETHとも金曜に一気に上げた後で、CMEのRSIもかなり高いので、ここから追うのはTSO向きではありません。citeturn828579search0turn828579search2

総合regimeは**MIXED / EVENT**。金曜までのrisk-onと、土曜に追加されたSaudi地政学リスクが衝突しています。

---

## 4. 10資産別判断

| 資産 | 本日判断 | 見方 |
|---|---|---|
| GOLD | **NO_TRADE** | GCZ26 4415.90。週末地政学で上ギャップ候補だが追わない |
| BTC | **NO_TRADE** | 約81.3k。ETF改善＋CME強いが急騰後 |
| ETH | **NO_TRADE** | 約2.62k。CME強いが急伸後 |
| WTI | **既存BUY HOLD / 新規NO_TRADE** | 100.30。週末Saudi攻撃で上方向リスク再増加 |
| USDJPY | **既存B+待機 / 新規NO_TRADE** | 156.725。介入警戒が強い |
| SPX | **NO_TRADE** | ESZ26 7712.5。月曜ギャップを待つ |
| NASDAQ | **NO_TRADE** | NQZ26 29917.25。30000直前を追わない |
| DXY | **NO_TRADE** | 約99.94。ドル強含みだがUSDJPYの介入要因がノイズ |
| US10Y | **NO_TRADE** | 4.996%。5%近辺で双方向 |
| VIX | **NO_TRADE** | 14.81。週末戦争ヘッドライン未反映 |

---

## 5. A級候補

**なし。**

方向だけなら、今朝一番強くなったのは**WTI上**です。

ただし新規でWTIを買う判断ではありません。

理由は、金曜100.30で閉じた後に週末の攻撃が出ており、月曜に103–105へギャップして始まる可能性があります。そこで新規BUYすると**供給ショック直後のmomentum追随**になります。

既存101.19 BUYを持っている現在は、むしろ新しいリスクを追加せず既存ポジションの優位性を使う局面です。

---

## 6. B級監視候補

**新規Bなし。**

継続監視は2件です。

### WTI — 既存B、実約定済み

**Entry 101.19  
SL 98.90  
TP 105.20  
RR 1.75**

週末ニュースはBUY側に有利。

ただし月曜、

**102.5–103超で開始**
なら、供給リスク再価格付けを確認。

**100付近のまま**
なら、週末ニュースが市場にほぼ評価されなかったという重要な弱気シグナルです。

**98.90割れ**
ならfired。

### USDJPY — 既存B+、未約定

**Entry 156.00–156.50  
SL 155.20  
TP1 158.20  
TP2 159.60  
RR 1.86**

月曜にEntry帯へ戻る場合だけ候補。

**157.20以上で始まるなら追わない**。

さらにrate check直後なので、通常のB+よりも実行時の介入ヘッドライン確認を重く見ます。Reutersはrate checkを「介入前の予備的措置」と説明しています。citeturn351381view0

---

## 7. 触らない資産

特に**BTC・ETH・NASDAQ・GOLD**を追いません。

BTCは75k台から81k台へ急反発し、9/18のETFフローも再びプラス。方向自体は上へ変化していますが、83k付近には既存の抵抗帯があります。今から81k台を買うより、**79.5–80.2kの押し**か、**83k超を抜いてからの押し直し**を待つ方がTSO的です。ETFフローはFarsideで9/18プラスを確認できます。citeturn340546search0turn415739search3

ETHも同じで、CME futuresは9/18に約+7.9%。この位置はEntryではなく観察地点です。citeturn828579search5

NASDAQもNQZ26が30000直前まで来ています。しかも週末のSaudi攻撃は金曜価格に入っていません。上方向を追うにも、下方向を先回りするにも条件が悪いです。

---

## 8. 後日検証ポイント

最優先は**月曜WTIの初動**です。

土曜の攻撃を受けて、

**WTI >103でギャップ**
なら、週末ニュースが供給プレミアムとして明確に再評価されたことになります。

**100前後でほぼ無反応**
なら、Houthi攻撃への市場感応度が低下している可能性があります。

**98.90割れ**
なら既存BUYは即firedです。

USDJPYは、

**156.00–156.50 → Entry候補**  
**155.20割れ → fired**  
**157.20超開始 → 追わない**  
**158再接近＋日本当局追加警告 → 介入リスク上昇**

です。

BTCは、

**79.5–80.2k押し止まり**
ならBUY再検討。

**83k超維持**
ならbreakout後の押し目候補。

逆に79k割れなら、金曜の上昇がshort squeeze主体だった可能性を再評価します。

NASDAQは、

**NQ >30000維持＋VIX <16**
なら、5%金利耐性はかなり強い。

**NQ <29600＋VIX >16.5**
なら週末地政学リスクがrisk-onを壊したと判断します。

---

## 9. Obsidian保存用 Observation Draft

```markdown
# 2026-09-20 Weekend Saudi Escalation / WTI Gap Risk

Model:
GPT-5.6 Sol

Market protagonist:
WTI

Gold reference:
COMEX Dec-2026 / GCZ26

crypto_grounds:
etf=有
cme=有

expected_r_basis:
subjective

## Weekend status

Sunday
Non-crypto markets closed.

Use:
Sep18 closes
Sep19 Saudi/Houthi news
Sep20 crypto spot

## Main new event

Sep19:
Houthi attacks escalated against Saudi Arabia.

Reuters:
flames and black smoke near Riyadh airport

Houthis claimed:
Yanbu Aramco facility attacked

Saudi coalition:
Yanbu attack foiled
damage unclear

Interpretation:
WTI existing BUY thesis strengthened
but confirmed production/export damage not yet available.

## WTI existing trade

20260917_WTI_BUY_PULLBACK

Actual:
Entry ~101.19
SL 98.90
TP 105.20

Sep18 WTI:
100.30

Current status:
HOLD

invalidation:
not_fired

Current subjective win probability:
~0.56-0.59

Reason for uplift:
new weekend Saudi attacks
Hormuz still constrained
East-West pipeline repair uncertain

Do not add.
Do not widen SL.

Monday test:

WTI >103 gap:
supply premium repriced

WTI ~100:
weekend attacks largely ignored

WTI <98.90:
FIRED

## USDJPY existing pending signal

20260919_USDJPY_BUY_PULLBACK

Entry:
156.00-156.50

SL:
155.20

TP1:
158.20

TP2:
159.60

RR:
1.86

Friday:
high 158.05
late 156.725

Rate check:
reported

Status:
UNFILLED
not_fired

Do not chase >157.20.

## Friday reference

GCZ26:
4415.90

ESZ26:
7712.50 settlement

NQZ26:
29917.25 settlement

US10Y:
4.996%

DXY:
~99.94

VIX:
14.81

WTI:
100.30

## Crypto

BTC spot:
~81.0-81.3k

ETH spot:
~2620-2630

BTC ETF Sep18:
at least +324.6m on current Farside table
some fields incomplete

ETH ETF Sep18:
+29.4m

CME:
strong momentum
overbought technical state

Do not chase.

## Active invalidation

20260917_WTI_BUY_PULLBACK=not_fired
20260919_USDJPY_BUY_PULLBACK=not_fired

## New signals

A:
NONE

B:
NONE

Existing:
WTI BUY active
USDJPY BUY_PULLBACK pending

#TSO #WTI #USDJPY #BTC #Saudi #Hormuz #NASDAQ
```

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-20,20260920_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,88,86,,EVENT,85,90,97,88,87,84,wait_for_Monday_GCZ26_reaction_to_Saudi_escalation_and_US10Y_DXY_confirmation,GCZ26_4372.65_4415.90_4439.60_US10Y_DXY_Monday_gap,verified
2026-09-20,20260920_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,90,88,,RISK_ON,87,91,96,90,90,88,do_not_chase_81k_after_6pct_move_wait_for_79.5k_80.2k_retest_or_83k_break_hold,BTC_79500_80200_81300_83000_ETF_CME_weekend_1d_3d,partially_verified
2026-09-20,20260920_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,87,89,,RISK_ON,84,89,95,88,86,84,do_not_chase_post_surge_wait_for_2550_2580_retest_or_2670_break_hold,ETH_2550_2580_2625_2670_ETF_CME_weekend_1d_3d,partially_verified
2026-09-20,20260920_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,95,99,,EVENT,93,99,99,95,94,98,manage_existing_20260917_BUY_SL98.90_TP105.20_weekend_Saudi_attack_no_add,WTI_98.90_100.30_101.19_105.20_Yanbu_Riyadh_Hormuz_Monday_gap,verified
2026-09-20,20260920_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,92,97,,EVENT,82,95,99,92,86,96,manage_existing_20260919_BUY_PULLBACK_155.20_or_confirmed_intervention_fires_no_weekend_chase,USDJPY_155.20_156.00_156.50_156.725_158.05_MOF_Monday_open,verified
2026-09-20,20260920_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,85,90,,MIXED,75,84,96,84,82,86,wait_for_ESZ26_Monday_gap_and_hold_above_7675_or_failure_after_Saudi_escalation,ESZ26_7675_7712.50_7739.25_US10Y_VIX_Monday_gap,verified
2026-09-20,20260920_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,90,88,,MIXED,80,88,96,90,88,88,wait_for_NQZ26_Monday_reaction_no_chase_near_30k_after_weekend_geopolitical_escalation,NQZ26_29648_29917.25_29993.25_30000_US10Y_VIX_Monday_gap,verified
2026-09-20,20260920_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,84,92,,EVENT,82,92,96,84,83,92,wait_for_DXY_and_USDJPY_Monday_open_after_BOJ_rate_check_and_geopolitical_gap,DXY_99.88_99.94_100.31_USDJPY_US10Y_Monday_open,partially_verified
2026-09-20,20260920_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,88,90,,MIXED,90,94,98,88,89,95,wait_for_Monday_break_above_5.05_or_rejection_below_4.90_after_weekend_energy_news,US10Y_4.90_4.996_5.05_WTI_GOLD_NQ_Monday,verified
2026-09-20,20260920_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,82,90,,EVENT,74,89,97,80,80,90,wait_for_Monday_VIX_gap_reclaim_above_16.5_or_hold_below_15_after_Saudi_attack,VIX_14.80_14.81_15.63_16.5_ES_NQ_Monday_gap,verified
```

### TSO_LOG JSON

```json
[
  {"date":"2026-09-20","signal_id":"20260920_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":88,"no_trade_score":86,"risk_pct":null,"regime":"EVENT","ems":85,"ffs":90,"cds":97,"ias":88,"cbs":87,"mes":84,"invalidation":"wait_for_Monday_GCZ26_reaction_to_Saudi_escalation_and_US10Y_DXY_confirmation","verification_target":"GCZ26_4372.65_4415.90_4439.60_US10Y_DXY_Monday_gap","verified_status":"verified"},
  {"date":"2026-09-20","signal_id":"20260920_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":90,"no_trade_score":88,"risk_pct":null,"regime":"RISK_ON","ems":87,"ffs":91,"cds":96,"ias":90,"cbs":90,"mes":88,"invalidation":"do_not_chase_81k_after_6pct_move_wait_for_79.5k_80.2k_retest_or_83k_break_hold","verification_target":"BTC_79500_80200_81300_83000_ETF_CME_weekend_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-20","signal_id":"20260920_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":87,"no_trade_score":89,"risk_pct":null,"regime":"RISK_ON","ems":84,"ffs":89,"cds":95,"ias":88,"cbs":86,"mes":84,"invalidation":"do_not_chase_post_surge_wait_for_2550_2580_retest_or_2670_break_hold","verification_target":"ETH_2550_2580_2625_2670_ETF_CME_weekend_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-20","signal_id":"20260920_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":95,"no_trade_score":99,"risk_pct":null,"regime":"EVENT","ems":93,"ffs":99,"cds":99,"ias":95,"cbs":94,"mes":98,"invalidation":"manage_existing_20260917_BUY_SL98.90_TP105.20_weekend_Saudi_attack_no_add","verification_target":"WTI_98.90_100.30_101.19_105.20_Yanbu_Riyadh_Hormuz_Monday_gap","verified_status":"verified"},
  {"date":"2026-09-20","signal_id":"20260920_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":92,"no_trade_score":97,"risk_pct":null,"regime":"EVENT","ems":82,"ffs":95,"cds":99,"ias":92,"cbs":86,"mes":96,"invalidation":"manage_existing_20260919_BUY_PULLBACK_155.20_or_confirmed_intervention_fires_no_weekend_chase","verification_target":"USDJPY_155.20_156.00_156.50_156.725_158.05_MOF_Monday_open","verified_status":"verified"},
  {"date":"2026-09-20","signal_id":"20260920_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":85,"no_trade_score":90,"risk_pct":null,"regime":"MIXED","ems":75,"ffs":84,"cds":96,"ias":84,"cbs":82,"mes":86,"invalidation":"wait_for_ESZ26_Monday_gap_and_hold_above_7675_or_failure_after_Saudi_escalation","verification_target":"ESZ26_7675_7712.50_7739.25_US10Y_VIX_Monday_gap","verified_status":"verified"},
  {"date":"2026-09-20","signal_id":"20260920_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":90,"no_trade_score":88,"risk_pct":null,"regime":"MIXED","ems":80,"ffs":88,"cds":96,"ias":90,"cbs":88,"mes":88,"invalidation":"wait_for_NQZ26_Monday_reaction_no_chase_near_30k_after_weekend_geopolitical_escalation","verification_target":"NQZ26_29648_29917.25_29993.25_30000_US10Y_VIX_Monday_gap","verified_status":"verified"},
  {"date":"2026-09-20","signal_id":"20260920_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":84,"no_trade_score":92,"risk_pct":null,"regime":"EVENT","ems":82,"ffs":92,"cds":96,"ias":84,"cbs":83,"mes":92,"invalidation":"wait_for_DXY_and_USDJPY_Monday_open_after_BOJ_rate_check_and_geopolitical_gap","verification_target":"DXY_99.88_99.94_100.31_USDJPY_US10Y_Monday_open","verified_status":"partially_verified"},
  {"date":"2026-09-20","signal_id":"20260920_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":88,"no_trade_score":90,"risk_pct":null,"regime":"MIXED","ems":90,"ffs":94,"cds":98,"ias":88,"cbs":89,"mes":95,"invalidation":"wait_for_Monday_break_above_5.05_or_rejection_below_4.90_after_weekend_energy_news","verification_target":"US10Y_4.90_4.996_5.05_WTI_GOLD_NQ_Monday","verified_status":"verified"},
  {"date":"2026-09-20","signal_id":"20260920_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":82,"no_trade_score":90,"risk_pct":null,"regime":"EVENT","ems":74,"ffs":89,"cds":97,"ias":80,"cbs":80,"mes":90,"invalidation":"wait_for_Monday_VIX_gap_reclaim_above_16.5_or_hold_below_15_after_Saudi_attack","verification_target":"VIX_14.80_14.81_15.63_16.5_ES_NQ_Monday_gap","verified_status":"verified"}
]
```

今日の更新で最も重要なのは、**WTIの既存BUYが金曜には弱く見えたものの、土曜のSaudi攻撃再激化でシナリオ根拠が再び強まったこと**です。ただしYanbuの実害はまだ確認されていないので、勝率を極端に引き上げる段階ではありません。

月曜のWTI初値がこの週末ニュースをどう評価するかが、今回のポジションの最大の検証になります。
