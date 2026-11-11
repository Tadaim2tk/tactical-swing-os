<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-27 07:00 JST -->
<!-- transport: Codex read_thread; message df63c218-4f1b-4690-84bf-d2cac406ee85; truncated=false -->
<!-- archived_at: 2026-09-27T10:04:24Z / chars: 19287 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-09-27

**使用モデル：GPT-5.6 Sol**  
**本日の市場の主役：USDJPY**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**データ基準：2026年9月25日米国市場の最終値＋9月26日週末Crypto。日曜日のため、Crypto以外は金曜終値を使用。**

**crypto_grounds: etf=有, cme=有** — 9月25日の米BTC現物ETFは**+134.5Mドル**、ETH ETFは**約+87Mドル**。BTC ETFは7営業日連続流入となり、9月21–25日の5日間だけでも約**+2.39Bドル**でした。CME BTCは金曜に安値83885、高値85742を確認しています。:chatgpt-content-reference{index="0"}

**expected_r_basis: subjective** — 本日の新規方向シグナルは0件。既存`20260924_BTC_BUY_PULLBACK`の発行時`expected_r=0.40`は変更しません。現在の管理評価ではETF流入継続をプラス、85k上で定着できない価格反応・US10Y 5.18%台・実測MAEの大きさをマイナスとして織り込んでいます。

**invalidation_check: 20260924_BTC_BUY_PULLBACK=not_fired**

週末BTCは約**84.0–84.2k**、土曜の確認レンジは概ね**83.18k–85.25k**で、SL82500には到達していません。:chatgpt-content-reference{index="1"}

---

## 1. 本日の結論

**新規A級：0件**  
**新規B級：0件**  
**既存B：BTC BUY_PULLBACK — 継続 / not_fired**  
**新規実取引：NO_TRADE**

今日は新規ポジションを作りません。

最も重要な更新は、**金曜最終値を取り直すと、前回朝時点よりUSDJPYの円高反応がかなり大きかった**ことです。

USDJPYは金曜に**159.00近辺から156.94まで低下し、最終は約157.29**。日本側が弱い円を「問題」と明示し、米側も「強い円が望ましい」との方向性を示したことで、口先介入が実際の価格へ効きました。:chatgpt-content-reference{index="2"}

つまり、

**高いUS10Y → 単純にUSDJPY上**

という構造に、かなり明確な政策上限が入り始めています。

一方BTCは、ETF流入が7営業日継続しているにもかかわらず**85kを定着して突破できていない**のが少し気になります。9月21–25日のBTC ETF流入は約2.39Bドルですが、BTCは週末84k前後で停滞しています。これは機関買いが弱いというより、**84–85k付近の既存売り・利確供給がかなり厚い**可能性を示します。:chatgpt-content-reference{index="3"}

したがって既存BTCは、

**HOLD相当 / 追加BUYなし / SL82500変更なし**

です。

---

## 2. 前回判断の簡易検証

### `20260924_BTC_BUY_PULLBACK`

発行条件：

**Entry：83800–84600**  
**Mid：84200**  
**SL：82500**  
**TP1：87400**  
**TP2：90200**  
**RR：1.88**  
**win_prob：0.55**  
**expected_r：0.40**

9月25日のCME BTCは、

**Low 83885  
High 85742  
Close 約85390**

まで回復しました。週末現物はその後84k前後へ戻っています。:chatgpt-content-reference{index="4"}

したがって現時点の経路は、

**ENTRY_REACHED  
→ 深いMAE  
→ 85k台へ回復  
→ TP1未達  
→ 週末84kへ再調整**

です。

SL82500は未到達。

また、9月25日のETFフローは**+134.5Mドル**で、ETF側の需要反転も起きていません。:chatgpt-content-reference{index="5"}

よって、

**`20260924_BTC_BUY_PULLBACK=not_fired`**

を維持します。

ただし管理上の主観勝率は、発行時0.55に対して現在は**約0.52**まで少し下げます。

理由は、ETF流入が非常に強い割に価格が85kを定着できていないためです。

これは弱気転換ではありませんが、**買い需要と売り供給が拮抗している**ことを示します。

---

## 3. 市場全体の前提

金曜はrisk-offではなく、むしろ**軽いrisk normalization**でした。

S&P500現物は**7743.41、+0.51%**、Nasdaq Compositeは**27068.72、+0.48%**。ESZ26も約**7805.75**まで上昇しました。VIXは前日の15.67から**14.87**へ低下しています。:chatgpt-content-reference{index="6"}

NASDAQ参照のNQ系も金曜は反発し、Micro NQ Dec-26では**30812.5、高値30998.5、安値30680**を確認しています。NQZ26と価格軸は同じですが、今回取得はMicro契約との照合を含むためNASDAQ行は`partially_verified`とします。:chatgpt-content-reference{index="7"}

US10Yは依然極端に高く、金曜終値は概ね**5.17–5.18%**。一時5.225%まで上昇しました。株式がこの金利でも上昇できたことは、今週の重要なObservationです。:chatgpt-content-reference{index="8"}

DXYは金曜**100.97、-0.32%**。高金利にもかかわらずドルが一服したのは、原油低下と円高方向の政策圧力が影響しています。:chatgpt-content-reference{index="9"}

GoldはGCZ26で**4320.50**。前日4298から反発しましたが、高金利が残るためまだ明確なBUYではありません。:chatgpt-content-reference{index="10"}

WTIは**92.41、-2.33%**。米国とイランの協議でHormuz再開期待が強まり、Saudi/Houthi供給不安のプレミアムを一部打ち消しました。:chatgpt-content-reference{index="11"}

総合regimeは**MIXED**です。

特に来週は米雇用・インフレ関連データがFedの追加利上げ観測を左右するため、US10Y・DXY・NASDAQの関係が再び中心になります。:chatgpt-content-reference{index="12"}

[9月25日の米株終値](https://finance.yahoo.com/markets/stocks/articles/major-us-stock-indexes-fared-202006753.html?utm_source=chatgpt.com)  
[9月25日のWTI市場背景](https://www.reuters.com/business/energy/talk-us-export-ban-diesel-deepens-us-crude-futures-discount-global-benchmark-2026-09-25/?utm_source=chatgpt.com)  
[来週の米雇用・金利見通し](https://economictimes.indiatimes.com/markets/us-stocks/news/wall-street-week-ahead-jobs-report-inflation-data-to-test-us-rate-path-economic-strength/articleshow/134497643.cms?utm_source=chatgpt.com)

---

## 4. 10資産別判断

| 資産 | 本日判断 | 評価 |
|---|---|---|
| **GOLD** | **NO_TRADE** | GCZ26 4320.5。4290台から反発したがUS10Y 5.18%が重い。:chatgpt-content-reference{index="16"} |
| **BTC** | **既存B継続 / 新規NO_TRADE** | 約84.0–84.2k。ETFは+134.5Mだが85k上を定着できず。:chatgpt-content-reference{index="17"} |
| **ETH** | **NO_TRADE** | 約2680–2690。ETFは+87MだがBTCより価格構造が弱い。:chatgpt-content-reference{index="18"} |
| **WTI** | **NO_TRADE** | 92.41。Hormuz和平期待とSaudi供給リスクが衝突。:chatgpt-content-reference{index="19"} |
| **USDJPY** | **NO_TRADE** | 約157.29。156.94まで急落し政策上限が明確化。:chatgpt-content-reference{index="20"} |
| **SPX** | **NO_TRADE** | ESZ26約7805.75。金利高でも強いが金曜反発後を追わない。:chatgpt-content-reference{index="21"} |
| **NASDAQ** | **NO_TRADE** | NQ系約30812.5。高金利耐性あり。ただし31000直前。:chatgpt-content-reference{index="22"} |
| **DXY** | **NO_TRADE** | 100.97。金曜に-0.32%、上昇モメンタム一服。:chatgpt-content-reference{index="23"} |
| **US10Y** | **NO_TRADE** | 約5.184%。依然主役級だが急騰後を追わない。:chatgpt-content-reference{index="24"} |
| **VIX** | **NO_TRADE** | 14.87。risk-off否定材料。:chatgpt-content-reference{index="25"} |

---

## 5. A級候補

**なし。**

最もAに近いのはNASDAQの押し目BUYですが、今日は日曜で先物価格形成がなく、金曜は30,800台まで既に戻っています。

さらに来週は米雇用統計・インフレデータがFed追加利上げ観測を左右します。US10Yが5.18%という状態では、NASDAQは方向よりも**金利耐性の検証段階**です。:chatgpt-content-reference{index="26"}

BTCもAではありません。

ETF需要は強い一方、週末の価格が85kを突破できていません。Aに必要な「価格反応まで含めた強さ」はまだ不足しています。

---

## 6. B級監視候補

**新規B級：なし。**

既存のみです。

### `20260924_BTC_BUY_PULLBACK`

**Entry：83800–84600**  
**SL：82500**  
**TP1：87400**  
**TP2：90200**  
**RR：1.88**  
**発行時win_prob：0.55**  
**現在管理参考：≈0.52**  
**risk_pct：0.25%**

ETF側は、

**9/21 +999M  
9/22 +714.7M  
9/23 +346.9M  
9/24 +190.7M  
9/25 +134.5M**

と流入自体は継続しています。:chatgpt-content-reference{index="27"}

ただし流入額は日ごとに縮小し、BTCは85kを明確に抜けていません。

このため評価は、

**需要：強い**  
**価格反応：やや弱い**

です。

現在は新規B+ではありません。

既存ポジションの管理だけにします。

**追加BUY禁止。SL82500維持。**

---

## 7. 触らない資産

今日は特に**USDJPY、WTI、BTC追加BUY、US10Y**です。

USDJPYは金利だけなら上方向ですが、金曜に159円近辺から157円台へ急落しました。日本・米国双方から「円安が望ましくない」というメッセージが出たため、158～160円の上側は明確にpolicy-risk zoneです。:chatgpt-content-reference{index="28"}

WTIも触りません。

木曜94.61から金曜92.41へ一気に反落し、Hormuz和平交渉だけで2%以上動いています。一方、中東の物理的輸送制約は完全解消していません。:chatgpt-content-reference{index="29"}

BTCも追加しません。

7営業日ETFが流入しているのに85kを抜けられない状態でポジションを増やすと、**「強い材料があるのに価格が伸びない」局面を買い増す**ことになります。

US10Yも5.18%で方向を追いません。

来週の雇用データが強ければ5.25%以上へ走る可能性がありますが、弱ければ5.0%台前半まで急低下する余地もあります。:chatgpt-content-reference{index="30"}

---

## 8. 後日検証ポイント

### BTC

現在唯一の未決着シグナルです。

**82500 → fired**  
**87400 → TP1**  
**90200 → TP2**

価格とは別に、

**CME <83000**
＋
**ETF純流出**

が揃えば早期invalidation。

週末安値は約83180で、まだ82500には届いていません。:chatgpt-content-reference{index="31"}

新しい重要ポイントは**85k**です。

ETF流入が続いているのに、

**BTC <85kが続く**
なら、売り供給の強さを示します。

逆に、

**85k突破 → 87.4k突破**
なら、ETF需要が価格へ再び素直に反映され始めたと判断します。

---

### USDJPY

今回かなり重要です。

**159近辺 → 156.94**

まで円高へ動きました。:chatgpt-content-reference{index="32"}

月曜以降、

**158.5を再奪回できない**
なら、政策上限が効き始めた可能性があります。

**156.5割れ**
なら、USDJPYの中期regimeを「単純ドル高」から変更する必要があります。

反対に、

**158.5超へすぐ復帰**
なら、金利差の力が政策警戒を再び上回ったことになります。

---

### NASDAQ

NQ系金曜高値は約**30998.5**。:chatgpt-content-reference{index="33"}

したがって、

**31000突破・維持**
＋
**US10Y <=5.20**
なら新BUY候補。

**30650–30700へ押して反発**
でもBUY_PULLBACK候補。

**30300割れ**
なら高金利耐性仮説を弱めます。

---

### SPX

ESZ26は約7805.75で終了。

**7750–7780**
を押し目支持として観察。

**7700割れ**
＋
**VIX >17**
ならrisk-off。

逆に7800台を維持しVIX15以下なら、株式の高金利耐性は相当強いと評価します。

---

### GOLD

GCZ26は4320.50。

**4350回復**
なら4300付近が支持化。

**4280割れ**
なら再びSELL優勢。

ただしUS10Yが5.10を割る場合はGold SELLの優位性を低下させます。

---

### WTI

**90割れ**
ならHormuz正常化期待優勢。

**95超**
なら供給プレミアム再拡大。

現在92.41はその中間なのでNO_TRADEです。

---

## 9. Obsidian保存用 Observation Draft

```markdown
# 2026-09-27 Yen Policy Ceiling / BTC ETF Absorption

Model:
GPT-5.6 Sol

Market protagonist:
USDJPY

Gold reference:
COMEX Dec-2026 / GCZ26

crypto_grounds:
etf=有
cme=有

expected_r_basis:
subjective

## Regime

MIXED

## Friday final-data corrections

GCZ26:
4320.50

WTI:
92.41

USDJPY:
157.29
Friday low:
156.94

ESZ26:
~7805.75

NQ / MNQ Dec-26:
~30812.5

DXY:
100.97

US10Y:
~5.184%

VIX:
14.87

Important:
Friday final closes are more risk-normalizing than the earlier intraday snapshot.

## USDJPY

Previous:
~158.8 area

Friday:
high near 159
low 156.94
close ~157.29

Drivers:
Japan publicly says weak yen is problematic
US side discusses desirability of stronger yen

Interpretation:
policy ceiling around 159-160 became materially stronger

Do not chase USDJPY BUY.

Tests:
158.5 reclaim = yield differential still dominant
156.5 break = regime change candidate

## BTC active

20260924_BTC_BUY_PULLBACK

Entry:
83800-84600

SL:
82500

TP1:
87400

TP2:
90200

RR:
1.88

Issue win_prob:
0.55

Current management estimate:
~0.52

Status:
not_fired

Weekend:
~84000-84200

Saturday range:
~83180-85250

ETF Sep25:
+134.5m

ETF Sep21-25:
~+2.39bn

Observation:
very strong ETF demand
but BTC unable to sustain >85000

Interpretation:
institutional demand remains real
but 84-85k seller supply is substantial

Do not add.

## Equity resilience

S&P500 Friday:
+0.51%

Nasdaq:
+0.48%

ES:
~7806

NQ:
~30813

VIX:
14.87

US10Y:
~5.18%

Key question:
can NQ break 31000 with yields still above 5.1%?

## Oil

WTI:
92.41

Friday:
-2.33%

Driver:
US-Iran / Hormuz reopening talks

Counter-risk:
Saudi/Houthi attacks
tight physical freight

NO_TRADE

## Week ahead

US jobs
inflation
Fed repricing

Primary chain:
jobs/inflation
-> US10Y
-> DXY
-> NQ/SPX
-> BTC/Gold

## Active invalidation

20260924_BTC_BUY_PULLBACK=not_fired

## New signals

A:
NONE

B:
NONE

Existing:
BTC BUY_PULLBACK active

#TSO #USDJPY #BTC #US10Y #NASDAQ #WTI #GOLD
```

---

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-27,20260927_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,86,90,,MIXED,83,92,97,82,83,92,wait_for_GCZ26_reclaim_4350_or_break_4280_with_US10Y_confirmation,GCZ26_4289.2_4320.5_4350_US10Y_DXY_1d_3d,verified
2026-09-27,20260927_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,95,60,,MIXED,85,94,98,92,88,94,manage_existing_20260924_BUY_SL82500_TP87400_not_fired_no_add,BTC_82500_83180_84200_85000_87400_ETF_CME_1d_3d_5d,partially_verified
2026-09-27,20260927_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,85,87,,MIXED,78,90,95,83,82,88,wait_for_ETH_hold_2600_or_reclaim_2750_and_prefer_existing_BTC_expression,ETH_2600_2685_2750_ETF_CME_1d_3d,partially_verified
2026-09-27,20260927_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,94,96,,EVENT,94,99,99,91,91,98,wait_for_WTI_break_below_90_or_reclaim_above_95_after_Hormuz_negotiations,WTI_Nov26_90_92.41_95_USIran_Hormuz_Houthi_1d_3d,verified
2026-09-27,20260927_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,96,97,,EVENT,97,99,99,96,93,99,policy_ceiling_strengthened_wait_for_158.5_reclaim_or_156.5_break_before_new_signal,USDJPY_156.5_156.94_157.29_158.5_159_MOF_US_1d_3d,verified
2026-09-27,20260927_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,92,84,,RISK_ON,84,94,98,89,88,95,wait_for_ES_pullback_7750_7780_or_failure_below_7700_with_VIX_confirmation,ESZ26_7700_7748.5_7780_7805.75_7835_US10Y_VIX_1d_3d,verified
2026-09-27,20260927_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,95,83,,RISK_ON,88,95,98,94,93,96,wait_for_NQ_break_hold_above_31000_or_pullback_30650_30700_without_chasing,NQZ26_30300_30650_30680_30812.5_31000_US10Y_VIX_1d_3d,partially_verified
2026-09-27,20260927_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,89,88,,MIXED,86,94,97,86,86,95,wait_for_DXY_reclaim_101.3_or_break_below_100.7_with_US10Y_USDJPY_confirmation,DXY_100.7_100.97_101.3_US10Y_USDJPY_1d_3d,verified
2026-09-27,20260927_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,98,94,,EVENT,99,99,99,97,97,99,do_not_chase_5.18_wait_for_break_above_5.25_or_rejection_below_5.10_before_new_signal,US10Y_5.10_5.184_5.225_5.25_NQ_GOLD_DXY_1d_3d,verified
2026-09-27,20260927_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,80,90,,RISK_ON,70,87,95,75,76,84,wait_for_VIX_reclaim_above_16.5_or_hold_below_14.5_with_ES_NQ_confirmation,VIX_14.68_14.87_16.5_ES_NQ_1d_3d,verified
```

### TSO_LOG JSON

```json
[
  {
    "date":"2026-09-27",
    "signal_id":"20260927_GOLD_NONE_NO_TRADE",
    "asset":"GOLD",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":99,
    "opp_score":86,
    "no_trade_score":90,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":83,
    "ffs":92,
    "cds":97,
    "ias":82,
    "cbs":83,
    "mes":92,
    "invalidation":"wait_for_GCZ26_reclaim_4350_or_break_4280_with_US10Y_confirmation",
    "verification_target":"GCZ26_4289.2_4320.5_4350_US10Y_DXY_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-27",
    "signal_id":"20260927_BTC_NONE_NO_TRADE",
    "asset":"BTC",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":99,
    "opp_score":95,
    "no_trade_score":60,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":85,
    "ffs":94,
    "cds":98,
    "ias":92,
    "cbs":88,
    "mes":94,
    "invalidation":"manage_existing_20260924_BUY_SL82500_TP87400_not_fired_no_add",
    "verification_target":"BTC_82500_83180_84200_85000_87400_ETF_CME_1d_3d_5d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-09-27",
    "signal_id":"20260927_ETH_NONE_NO_TRADE",
    "asset":"ETH",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":98,
    "opp_score":85,
    "no_trade_score":87,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":78,
    "ffs":90,
    "cds":95,
    "ias":83,
    "cbs":82,
    "mes":88,
    "invalidation":"wait_for_ETH_hold_2600_or_reclaim_2750_and_prefer_existing_BTC_expression",
    "verification_target":"ETH_2600_2685_2750_ETF_CME_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-09-27",
    "signal_id":"20260927_WTI_NONE_NO_TRADE",
    "asset":"WTI",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":99,
    "opp_score":94,
    "no_trade_score":96,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":94,
    "ffs":99,
    "cds":99,
    "ias":91,
    "cbs":91,
    "mes":98,
    "invalidation":"wait_for_WTI_break_below_90_or_reclaim_above_95_after_Hormuz_negotiations",
    "verification_target":"WTI_Nov26_90_92.41_95_USIran_Hormuz_Houthi_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-27",
    "signal_id":"20260927_USDJPY_NONE_NO_TRADE",
    "asset":"USDJPY",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":99,
    "opp_score":96,
    "no_trade_score":97,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":97,
    "ffs":99,
    "cds":99,
    "ias":96,
    "cbs":93,
    "mes":99,
    "invalidation":"policy_ceiling_strengthened_wait_for_158.5_reclaim_or_156.5_break_before_new_signal",
    "verification_target":"USDJPY_156.5_156.94_157.29_158.5_159_MOF_US_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-27",
    "signal_id":"20260927_SPX_NONE_NO_TRADE",
    "asset":"SPX",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":99,
    "opp_score":92,
    "no_trade_score":84,
    "risk_pct":null,
    "regime":"RISK_ON",
    "ems":84,
    "ffs":94,
    "cds":98,
    "ias":89,
    "cbs":88,
    "mes":95,
    "invalidation":"wait_for_ES_pullback_7750_7780_or_failure_below_7700_with_VIX_confirmation",
    "verification_target":"ESZ26_7700_7748.5_7780_7805.75_7835_US10Y_VIX_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-27",
    "signal_id":"20260927_NASDAQ_NONE_NO_TRADE",
    "asset":"NASDAQ",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":99,
    "opp_score":95,
    "no_trade_score":83,
    "risk_pct":null,
    "regime":"RISK_ON",
    "ems":88,
    "ffs":95,
    "cds":98,
    "ias":94,
    "cbs":93,
    "mes":96,
    "invalidation":"wait_for_NQ_break_hold_above_31000_or_pullback_30650_30700_without_chasing",
    "verification_target":"NQZ26_30300_30650_30680_30812.5_31000_US10Y_VIX_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-09-27",
    "signal_id":"20260927_DXY_NONE_NO_TRADE",
    "asset":"DXY",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":99,
    "opp_score":89,
    "no_trade_score":88,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":86,
    "ffs":94,
    "cds":97,
    "ias":86,
    "cbs":86,
    "mes":95,
    "invalidation":"wait_for_DXY_reclaim_101.3_or_break_below_100.7_with_US10Y_USDJPY_confirmation",
    "verification_target":"DXY_100.7_100.97_101.3_US10Y_USDJPY_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-27",
    "signal_id":"20260927_US10Y_NONE_NO_TRADE",
    "asset":"US10Y",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":99,
    "opp_score":98,
    "no_trade_score":94,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":99,
    "ffs":99,
    "cds":99,
    "ias":97,
    "cbs":97,
    "mes":99,
    "invalidation":"do_not_chase_5.18_wait_for_break_above_5.25_or_rejection_below_5.10_before_new_signal",
    "verification_target":"US10Y_5.10_5.184_5.225_5.25_NQ_GOLD_DXY_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-27",
    "signal_id":"20260927_VIX_NONE_NO_TRADE",
    "asset":"VIX",
    "side":"NONE",
    "rank":"NO_TRADE",
    "type":"NO_TRADE",
    "entry_low":null,
    "entry_high":null,
    "sl":null,
    "tp1":null,
    "tp2":null,
    "rr":null,
    "win_prob":null,
    "expected_r":null,
    "tq_score":99,
    "opp_score":80,
    "no_trade_score":90,
    "risk_pct":null,
    "regime":"RISK_ON",
    "ems":70,
    "ffs":87,
    "cds":95,
    "ias":75,
    "cbs":76,
    "mes":84,
    "invalidation":"wait_for_VIX_reclaim_above_16.5_or_hold_below_14.5_with_ES_NQ_confirmation",
    "verification_target":"VIX_14.68_14.87_16.5_ES_NQ_1d_3d",
    "verified_status":"verified"
  }
]
```

本日の最大の観察点は2つです。

第一に、**BTCはETF流入が非常に強いのに85kを突破しきれない**。既存BUYはまだ壊れていませんが、買い需要に対する価格反応は期待ほど強くありません。

第二に、**USDJPYは高金利にもかかわらず159円近辺から157円台へ急反落**しました。日米双方の円安牽制が実際に市場へ効き始めており、来週は「US10Y」と並んでUSDJPYの政策上限が重要なクロスアセット変数になります。
