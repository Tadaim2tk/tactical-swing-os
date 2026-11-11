<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-25 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-26T09:12:02Z / chars: 17506 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-09-25

**使用モデル：GPT-5.6 Sol**  
**本日の市場の主役：US10Y**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**データ基準：2026年9月24日米国市場終了後〜9月25日06:57 JST。ES/NQ/BTC/ETHは遅延値・直近値を含む。**

**crypto_grounds: etf=有, cme=有** — Farsideの確定済み最新行は9月23日で、BTC ETF **+346.9Mドル**、ETH ETF **+104.5Mドル**。9月24日行は今朝時点で未確定表示です。CME BTCは9月24日 **84322.5、安値82857**、CME ETHは **2668.5、安値2630** を確認しました。citeturn311340view0turn438101search0turn561667search1turn561667search2

**expected_r_basis: subjective** — 本日は新規方向シグナルを発行しません。既存`20260924_BTC_BUY_PULLBACK`の発行時`expected_r=0.40`は書き換えず、今日の管理判断では金利上昇・ドル高・実測MAE拡大を別途反映します。

**invalidation_check: 20260924_BTC_BUY_PULLBACK=unknown**

厳密に`unknown`とします。BTC/USDの価格SL **82500**自体は未到達ですが、CMEは一時83000を割りました。一方、複合失効条件のもう片方である**9月24日のETFフロー反転有無がFarsideでまだ確定していない**ためです。推測で`fired`にも`not_fired`にもしません。

9月24日の最大の変化は、米10年債利回りがさらに上昇して**5.196%**と2007年以来の高水準へ達したことです。WTIもHouthiによるサウジ攻撃を受け**94.61ドル、+2.7%**。一方、S&P500は-0.02%、Nasdaqは+0.01%とほぼ横ばいに耐えました。つまり金利・原油ショックはさらに悪化したのに、株式は前日のようには崩れていません。citeturn461430view1turn461430view2turn461430view0

---

## 1. 本日の結論

**新規A級：0件**  
**新規B級：0件**  
**既存B：BTC BUY_PULLBACK — Entry到達済み、失効判定はunknown**  
**新規実取引：NO_TRADE**

今日はいったん**ポジション追加をしない**判断です。

昨日のBTCシグナル、

**Entry 83800–84600  
SL 82500  
TP1 87400  
TP2 90200**

は実際にEntry帯へ入りました。その後BTC現物は**約82875**まで下落し、CMEも**82857**まで下げた後、84k台へ回復しています。citeturn857113search1turn561667search1

中点84200を基準にすると実測MAEは、

\[
(84200-82875)/(84200-82500)
\approx0.78R
\]

です。

発行時想定の**0.29Rを大幅に超えました**。

したがって、シグナル自体は価格SLに達していませんが、**質は昨日より明確に低下**しています。実取引している場合でも、**追加BUYは禁止、SL82500は広げない**とします。

一方、株式は意外に耐えています。米10年債が5.196%まで上がってもS&P500はほぼ横ばいで、VIXもCboe直近値で**15.41**にとどまっています。これは「5%金利＝即risk-off」という単純な関係がまだ成立していないことを示します。citeturn668580search0turn461430view0

---

## 2. 前回判断の簡易検証

### `20260924_BTC_BUY_PULLBACK`

発行値：

**Entry 83800–84600**  
**Mid 84200**  
**SL 82500**  
**TP1 87400**  
**TP2 90200**  
**RR 1.88**  
**win_prob 0.55**  
**expected_r 0.40**

9月24日のBTC現物は概ね**84.4k付近で開始後、82.9k近辺まで下落し、その後84k台へ回復**。現在値も約84.1kです。CMEでは**Open 84370 / High 84922 / Low 82857 / Close 84322.5**という系列を確認しています。citeturn857113search5turn561667search1

結果：

**ENTRY_TOUCHED**  
**SL_NOT_REACHED**  
**TP1_NOT_REACHED**  
**MAE ≈0.78R**  
**invalidation=unknown**

ここが今日の最重要検証です。

昨日の問題は方向そのものより、**MAE想定を大幅に過小評価したこと**です。

一方、ETF需要は9月23日まで非常に強く、BTC ETFは**5営業日連続流入、最新確定+346.9Mドル**。ETH ETFも+104.5Mドルでした。citeturn311340view0turn438101search0

したがって「金利ショックでCryptoの需要構造まで完全崩壊した」とまではまだ言えません。

### Trump–Xi会談

市場を大きく動かすほどの突破口はありませんでした。

米中は11月期限だった貿易休戦を**2か月延長**しましたが、関税、レアアース、農産品、技術規制といった主要問題は先送りです。短期的にはtrade-war再燃を避けたためプラスですが、恒久的なrisk-on材料ではありません。citeturn579201view0

---

## 3. 市場全体の前提

現在のクロスアセットは、

**WTI ↑  
US10Y ↑  
DXY ↑  
Gold ↓  
BTC 横ばい〜弱含み  
SPX/NASDAQ surprisingly resilient**

です。

米10年債は**5.196%**、30年債も2004年以来の高水準。Fedの10月追加利上げ確率は約7割まで上昇しています。citeturn461430view1

DXYは**101.28**、一時101.39で2か月高値。USDJPYも約**158.8**です。citeturn461430view4turn668580search8

Gold Decemberは**4298ドル**で清算。高金利、ドル高、原油高による追加利上げ懸念が重石です。citeturn461430view3

WTIは**94.61ドル**。サウジはTaif・Yanbuを狙った6発のHouthi弾道ミサイルを迎撃。一方で米国とIranはHormuz再開を含む段階的合意を模索しており、油価は日中高値からは押し戻されました。citeturn461430view2

ESZ26は遅延値で約**7766**、NQZ26は約**30680**。S&P現物は7704.13、Nasdaq現物26939.37でほぼ横ばいでした。citeturn514109search8turn514109search11turn461430view0

今日9月25日は米耐久財受注、Michigan消費者信頼感確報、複数Fed当局者発言があります。特にインフレ期待が高止まりすれば、5.2%近辺の米金利がさらに上へ走る可能性があります。citeturn921026news32turn921026search7

総合regimeは**EVENT / MIXED**です。

---

## 4. 10資産別判断

| 資産 | 本日判断 | 評価 |
|---|---|---|
| **GOLD** | **NO_TRADE** | GCZ26 4298。下向きだが4235近辺に支持候補があり、今からSELLは遅い。citeturn461430view3 |
| **BTC** | **既存B管理 / 新規NO_TRADE** | 約84.1k。Entry到達、SL未達、MAE0.78R。ETF9/24未確定。 |
| **ETH** | **NO_TRADE** | spot約2665–2690、CME2668.5。BTCより相対的に弱い。citeturn857113search6turn561667search2 |
| **WTI** | **NO_TRADE** | 94.61。Houthi攻撃で+2.7%だがHormuz交渉あり。momentum追随禁止。 |
| **USDJPY** | **NO_TRADE** | 約158.8。ドル優位だが160接近ほど介入非対称リスク増大。 |
| **SPX** | **NO_TRADE** | ES約7766。5.2%金利でも崩れないが、今は方向優位より耐性観察。 |
| **NASDAQ** | **NO_TRADE** | NQ約30680。金利逆風の割に耐えるが、買いにも売りにも非対称性不足。 |
| **DXY** | **NO_TRADE** | 101.28。上方向は明確だが4日続伸・2か月高値で追わない。 |
| **US10Y** | **NO_TRADE** | 5.196%。主役だが2日間の急騰後を追わない。 |
| **VIX** | **NO_TRADE** | 15.41。上昇しているが恐怖相場ではなく、単独trade edgeなし。citeturn668580search0 |

---

## 5. A級候補

**なし。**

最も明確なトレンドは、

**US10Y上昇**
と
**DXY上昇**
です。

しかし両方とも既に急伸しています。

10年債利回りは2日で大きく上昇し5.196%、DXYも101.28で2か月高値です。ここから追うとイベント反転を最も受けやすい場所になります。citeturn461430view1turn461430view4

BTCも昨日よりAから遠ざかりました。

発行時のA不合格理由はMAE想定0.29Rでしたが、実際には**0.78Rまで逆行**しました。この時点で少なくとも短期エントリー品質については、昨日の評価が楽観的でした。

---

## 6. B級監視候補

**新規Bなし。**

既存のみです。

### `20260924_BTC_BUY_PULLBACK`

**Entry：83800–84600**  
**SL：82500**  
**TP1：87400**  
**TP2：90200**  
**RR：1.88**

現在の管理評価：

**研究シグナル：継続**  
**invalidation：unknown**  
**追加BUY：禁止**  
**SL拡大：禁止**

ETF側は9月23日まで、

**BTC +346.9Mドル**  
**ETH +104.5Mドル**

とプラスが続いています。Farsideの9月24日行は未入力なので、今日ここを0とみなしてはいけません。citeturn311340view0turn438101search0

また、外部の暫定集計では9月24日もBTC/ETH ETFへの流入継続を示すデータがありますが、TSOの正式invalidation判定にはまだ採用しません。citeturn932257search0

実取引済みであれば、**82500をそのままSLとして維持**します。

---

## 7. 触らない資産

特に**WTI、USDJPY、US10Y、GOLD**です。

WTIは一日+2.7%。Houthi攻撃という供給ショック直後なので、BUYはTSOルール上追えません。同時にHormuz再開交渉が進めば数ドル単位の急反落もあり得ます。citeturn461430view2

USDJPYは158円後半。金利差だけならBUYですが、日本当局によるrate checkが出た後の水準であり、160へ近づくほど上昇余地と介入テールリスクのバランスが悪くなります。

Goldは下方向が整っていますが、4298からReutersが指摘する4235支持まで約63ドルしかありません。ここでSELLして通常のSLを置くとRRが悪い。戻りを待つべきです。citeturn461430view3

US10Yも5.196%で追わない。今日の耐久財やMichiganで弱い数字が出れば、5%台前半から急低下するリスクがあります。

---

## 8. 後日検証ポイント

### BTC

現在唯一の未解決方向判断です。

**82500 → price invalidation / fired**  
**87400 → TP1**  
**90200 → TP2**

それとは別に、

**CME <83000**
＋
**ETFフロー反転**

の組み合わせもinvalidationです。

CMEはすでに一時**82857**まで入っているため、9月24日のETFフローが確定した時点で必ず再判定します。citeturn561667search1

そして今回の較正ポイントは、

**予想MAE 0.29R → 実測約0.78R**

です。

BTCの次回BUY_PULLBACKでは、急騰直後＋金利上昇局面のMAE見積もりをかなり広く取る必要があります。

### NASDAQ / SPX

非常に重要です。

**US10Y 5.196%**
にもかかわらず、

**S&P -0.02%  
Nasdaq +0.01%**

でした。citeturn461430view0turn461430view1

今日も10年債が5.15〜5.25%にいてNQが30500以上を維持するなら、**米株の高金利耐性は想定以上に強い**という新しいObservationになります。

逆に、

**NQ <30300  
ES <7700  
VIX >17**

が揃えば、遅れて金利ショックが株へ伝播したと判断します。

### GOLD

**4235付近**が第一支持。

ここを明確に割り、DXY>101、US10Y>5.15が続けば、次はSELL_PULLBACKを作りやすくなります。

逆に4325–4350を回復するなら、金利ショック売りは一旦終息です。

### WTI

**96超**
ならSaudi攻撃プレミアムの定着。

**92割れ**
ならHormuz交渉・供給正常化が再び優勢。

現在94.61は中間地点なので新規なし。

### USDJPY

**159.50–160**
は新しい観察領域。

ここまで上がって日本当局の追加rate checkや実介入がなければ、介入閾値に対する市場認識自体の変更を疑います。

---

## 9. Obsidian保存用 Observation Draft

```markdown
# 2026-09-25 US10Y 5.20 / BTC Deep MAE / Equity Resilience

Model:
GPT-5.6 Sol

Market protagonist:
US10Y

Gold reference:
COMEX Dec-2026 / GCZ26

crypto_grounds:
etf=有
cme=有

expected_r_basis:
subjective

## Regime

EVENT / MIXED

## Main macro state

US10Y:
5.196%
highest since 2007

DXY:
101.28
2-month high

USDJPY:
~158.8

WTI:
94.61
+2.7%

GCZ26:
4298

VIX:
15.41

SPX cash:
7704.13
-0.02%

Nasdaq Composite:
26939.37
+0.01%

ESZ26 delayed:
~7766

NQZ26 delayed:
~30680

Interpretation:

Rates and oil worsened materially,
but equities did not break.

This is important resilience evidence.

## Trump-Xi

Trade truce:
extended only 2 months

New deadline:
Jan 10

No durable agreement on:
tariffs
rare earths
technology
agriculture

Interpretation:
short-term tail risk reduced
structural uncertainty remains.

## BTC active signal

20260924_BTC_BUY_PULLBACK

Entry:
83800-84600

Mid:
84200

SL:
82500

TP1:
87400

TP2:
90200

RR:
1.88

Sep24 spot low:
~82875

Sep24 CME:
close 84322.5
low 82857

Status:
ENTRY_TOUCHED
SL_NOT_REACHED
TP_NOT_REACHED

Expected MAE at issue:
0.29R

Observed MAE:
~0.78R

Key learning:
MAE materially underestimated.

ETF latest completed:
BTC Sep23 +346.9m
ETH Sep23 +104.5m

Sep24 Farside row:
not finalized

Invalidation:
UNKNOWN

Reason:
CME temporarily lost 83000
but ETF-flow reversal condition cannot yet be verified.

Do not add.
Do not widen SL.

## Crypto

BTC spot:
~84100

ETH spot:
~2665-2690

CME BTC:
84322.5

CME ETH:
2668.5

ETF demand remains supportive through Sep23,
but macro liquidity pressure is worsening.

## Oil

Houthi missiles:
6 intercepted targeting Taif / Yanbu

WTI:
94.61

US-Iran:
phased Hormuz reopening discussions ongoing

Interpretation:
event-driven two-way risk
NO_TRADE

## Gold

GCZ26:
4298

Macro:
bearish

But:
near 4235 support
poor chase RR

NO_TRADE

## Sep25 events

US durable goods
Michigan sentiment / inflation expectations
Fed speakers

Main question:
can US10Y remain near 5.2% without breaking NQ/SPX?

## Active invalidation

20260924_BTC_BUY_PULLBACK=unknown

## New signals

A:
NONE

B:
NONE

Existing:
BTC BUY_PULLBACK active / unresolved

#TSO #US10Y #BTC #NASDAQ #WTI #GOLD #USDJPY
```

---

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-25,20260925_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,91,89,,EVENT,90,95,98,88,88,96,wait_for_GCZ26_break_4235_or_rebound_4325_4350_before_new_signal,GCZ26_4235_4298_4325_4350_DXY_US10Y_1d_3d,verified
2026-09-25,20260925_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,94,67,,EVENT,82,92,97,89,85,88,manage_existing_20260924_BUY_entry_touched_SL82500_unchanged_invalidation_unknown_pending_Sep24_ETF_flow,BTC_82500_82857_84100_84322.5_87400_ETF_CME_US10Y_1d_3d,partially_verified
2026-09-25,20260925_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,86,88,,MIXED,76,89,95,83,82,84,prefer_existing_BTC_expression_wait_for_ETH_hold_2630_or_reclaim_2750,ETH_2630_2668.5_2750_ETF_CME_US10Y_1d_3d,verified
2026-09-25,20260925_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,96,98,,EVENT,97,99,99,95,94,99,do_not_chase_Houthi_supply_shock_wait_for_break_above_96_or_failure_below_92,WTI_92_94.61_96_Houthi_Yanbu_Hormuz_USIran_1d_3d,verified
2026-09-25,20260925_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,94,95,,EVENT,92,97,99,93,90,98,do_not_chase_158_8_wait_for_intervention_response_or_pullback_below_157_5,USDJPY_157.5_158.8_159.5_160_MOF_DXY_US10Y_1d_3d,partially_verified
2026-09-25,20260925_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,91,91,,MIXED,88,94,98,88,87,96,wait_for_ES_break_below_7700_or_hold_above_7750_despite_US10Y_5.2,ESZ26_7700_7750_7766_7785_US10Y_VIX_1d_3d,partially_verified
2026-09-25,20260925_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,93,90,,MIXED,88,95,98,91,89,96,wait_for_NQ_break_below_30300_or_hold_above_30500_with_US10Y_near_5.2,NQZ26_30300_30500_30680_30820_US10Y_VIX_1d_3d,partially_verified
2026-09-25,20260925_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,94,91,,EVENT,94,97,99,93,92,98,do_not_chase_two_month_high_wait_for_pullback_100.7_101_or_clean_hold_above_101.5,DXY_100.7_101_101.28_101.5_US10Y_Fed_1d_3d,verified
2026-09-25,20260925_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,99,94,,EVENT,99,99,99,98,98,99,do_not_chase_5.196_wait_for_hold_above_5.25_or_rejection_below_5.10_after_US_data,US10Y_5.10_5.196_5.25_DurableGoods_UMich_NQ_GOLD_1d_3d,verified
2026-09-25,20260925_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,87,90,,EVENT,82,92,97,84,84,91,wait_for_VIX_break_above_17_or_return_below_14.5_with_ES_NQ_confirmation,VIX_14.5_15.41_17_ES_NQ_US10Y_1d_3d,verified
```

### TSO_LOG JSON

```json
[
  {"date":"2026-09-25","signal_id":"20260925_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":91,"no_trade_score":89,"risk_pct":null,"regime":"EVENT","ems":90,"ffs":95,"cds":98,"ias":88,"cbs":88,"mes":96,"invalidation":"wait_for_GCZ26_break_4235_or_rebound_4325_4350_before_new_signal","verification_target":"GCZ26_4235_4298_4325_4350_DXY_US10Y_1d_3d","verified_status":"verified"},
  {"date":"2026-09-25","signal_id":"20260925_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":94,"no_trade_score":67,"risk_pct":null,"regime":"EVENT","ems":82,"ffs":92,"cds":97,"ias":89,"cbs":85,"mes":88,"invalidation":"manage_existing_20260924_BUY_entry_touched_SL82500_unchanged_invalidation_unknown_pending_Sep24_ETF_flow","verification_target":"BTC_82500_82857_84100_84322.5_87400_ETF_CME_US10Y_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-25","signal_id":"20260925_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":86,"no_trade_score":88,"risk_pct":null,"regime":"MIXED","ems":76,"ffs":89,"cds":95,"ias":83,"cbs":82,"mes":84,"invalidation":"prefer_existing_BTC_expression_wait_for_ETH_hold_2630_or_reclaim_2750","verification_target":"ETH_2630_2668.5_2750_ETF_CME_US10Y_1d_3d","verified_status":"verified"},
  {"date":"2026-09-25","signal_id":"20260925_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":96,"no_trade_score":98,"risk_pct":null,"regime":"EVENT","ems":97,"ffs":99,"cds":99,"ias":95,"cbs":94,"mes":99,"invalidation":"do_not_chase_Houthi_supply_shock_wait_for_break_above_96_or_failure_below_92","verification_target":"WTI_92_94.61_96_Houthi_Yanbu_Hormuz_USIran_1d_3d","verified_status":"verified"},
  {"date":"2026-09-25","signal_id":"20260925_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":94,"no_trade_score":95,"risk_pct":null,"regime":"EVENT","ems":92,"ffs":97,"cds":99,"ias":93,"cbs":90,"mes":98,"invalidation":"do_not_chase_158_8_wait_for_intervention_response_or_pullback_below_157_5","verification_target":"USDJPY_157.5_158.8_159.5_160_MOF_DXY_US10Y_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-25","signal_id":"20260925_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":91,"no_trade_score":91,"risk_pct":null,"regime":"MIXED","ems":88,"ffs":94,"cds":98,"ias":88,"cbs":87,"mes":96,"invalidation":"wait_for_ES_break_below_7700_or_hold_above_7750_despite_US10Y_5.2","verification_target":"ESZ26_7700_7750_7766_7785_US10Y_VIX_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-25","signal_id":"20260925_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":93,"no_trade_score":90,"risk_pct":null,"regime":"MIXED","ems":88,"ffs":95,"cds":98,"ias":91,"cbs":89,"mes":96,"invalidation":"wait_for_NQ_break_below_30300_or_hold_above_30500_with_US10Y_near_5.2","verification_target":"NQZ26_30300_30500_30680_30820_US10Y_VIX_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-25","signal_id":"20260925_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":94,"no_trade_score":91,"risk_pct":null,"regime":"EVENT","ems":94,"ffs":97,"cds":99,"ias":93,"cbs":92,"mes":98,"invalidation":"do_not_chase_two_month_high_wait_for_pullback_100.7_101_or_clean_hold_above_101.5","verification_target":"DXY_100.7_101_101.28_101.5_US10Y_Fed_1d_3d","verified_status":"verified"},
  {"date":"2026-09-25","signal_id":"20260925_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":99,"no_trade_score":94,"risk_pct":null,"regime":"EVENT","ems":99,"ffs":99,"cds":99,"ias":98,"cbs":98,"mes":99,"invalidation":"do_not_chase_5.196_wait_for_hold_above_5.25_or_rejection_below_5.10_after_US_data","verification_target":"US10Y_5.10_5.196_5.25_DurableGoods_UMich_NQ_GOLD_1d_3d","verified_status":"verified"},
  {"date":"2026-09-25","signal_id":"20260925_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":87,"no_trade_score":90,"risk_pct":null,"regime":"EVENT","ems":82,"ffs":92,"cds":97,"ias":84,"cbs":84,"mes":91,"invalidation":"wait_for_VIX_break_above_17_or_return_below_14.5_with_ES_NQ_confirmation","verification_target":"VIX_14.5_15.41_17_ES_NQ_US10Y_1d_3d","verified_status":"verified"}
]
```

今日の最重要な学習は、**BTCの方向仮説がまだ完全には壊れていない一方、発行時のMAE想定0.29Rに対して実際は約0.78Rまで逆行したこと**です。次回以降、急騰直後かつ米金利上昇局面のCrypto押し目BUYでは、Entry品質・MAE較正を厳しくする必要があります。

また、**US10Yが5.2%近辺まで上昇しても米株がほぼ横ばいだったこと**も重要です。今日の米指標後もNQ/ESが崩れなければ、「高金利耐性」はかなり強いObservationになります。
