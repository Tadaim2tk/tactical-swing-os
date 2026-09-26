<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-22 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-26T09:12:02Z / chars: 17475 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-09-22

**使用モデル：GPT-5.6 Sol**  
**本日の市場の主役：NASDAQ**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**データ基準：2026年9月21日米国市場＋9月22日07:00 JST前後の遅延市場データ。ES/NQ等は遅延値を含む。**  
**crypto_grounds: etf=有, cme=有**  
**expected_r_basis: subjective** — 新規SPX BUY_PULLBACKは二点分布なら約`+0.68R`だが、前日大幅上昇後の反落、Entry未到達、9月24日の米中首脳会談、Fed再利上げリスクを織り込み`expected_r=0.40`へ下方調整。

**invalidation_check: 20260919_USDJPY_BUY_PULLBACK=not_fired, 20260922_SPX_BUY_PULLBACK=not_fired**

`20260917_WTI_BUY_PULLBACK`は、ユーザー実取引の**OILCash 98.90 SL到達により fired**。本日から未決着リストから除外します。

9月21日はクロスアセット構造がかなり明瞭に変化しました。WTIはOct限で**95.78ドル、-4.5%**、Nov限は**92.47ドル**まで低下。一方で10年債利回りは5%を割り、S&P500は+1.49%、Nasdaq Compositeは+2.26%で最高値更新。つまり直近までの「原油高→金利高→Growth圧迫」が逆回転しています。citeturn213769news0turn213769news72

urlReuters：9月21日の米株・金利・原油turn213769news0  
urlReuters：サウジ原油輸出の回復turn213769news72  
urlReuters：9月21日の金市場turn213769news71  
urlReuters：9月21日のUSDJPY・介入警戒turn511588news50

## 1. 本日の結論

**新規A級：0件**  
**新規B級：1件 — SPX BUY_PULLBACK**  
**B+観察候補：SPX BUY_PULLBACK**  
**既存B+：USDJPY BUY_PULLBACKは未約定のまま継続**  
**WTI既存BUY：損切り完了、FIRED**  
**その他7資産：NO_TRADE**

今日の方向感は明確に**RISK_ON**ですが、NASDAQ・BTC・ETHをそのまま追うのは遅いです。

そこでリスクオン仮説を表現するなら、NASDAQやBTCではなく、値幅が相対的に穏やかな**SPXの押し目だけを1本残す**のが適切と判断します。これは相関資産を同時に抱える問題も避けます。

新規：

**`20260922_SPX_BUY_PULLBACK`**

Entry：**7760–7780**  
中点：**7770**  
SL：**7730**  
TP1：**7850**  
TP2：**7910**  
RR：**2.00**  
win_prob：**0.56**  
expected_r：**0.40**  
MAE想定：**0.24R**  
risk_pct：**0.25%**

直近のESZ26遅延値はおよそ**7798**まで上昇しています。現在値を追わず、7760–7780までの押しだけを待ちます。citeturn102646search7

XMのUS500Cashは確認可能な実測仕様で**contract size=1、最小0.10lot**。40ポイントのSLなら概算損失は約4ドル、157円換算でも700円弱＋スプレッド程度なので、3,000円実損制約には十分収まります。citeturn867258search4

したがって**B+観察候補**です。

---

## 2. 前回判断の簡易検証

### `20260917_WTI_BUY_PULLBACK` — FIRED

実取引：

**Entry：約101.19  
SL：98.90  
TP：105.20**

ユーザー口座でSL到達を確認済みです。

さらに9月21日の市場でも、WTI Oct限は**95.78ドル**まで低下し、単なる瞬間的なSL狩りではなく、その後も下方向が継続しました。Nov限も92.47ドルです。citeturn213769news72

今回の反証はかなり明確です。

サウジはEast-West Pipelineの障害を抱えながらも、Hormuz経由の輸出を急増させました。Kpler推計で直近6日平均**約2.9mbpd**、8月の約0.7mbpdから大幅回復。9月20日だけでもRas Tanuraから7隻のVLCCへ約1,400万バレルを積載しています。citeturn213769news72

つまり今回の失敗要因は、

**「物理インフラ損傷」自体は正しく認識したが、代替輸送による実効供給回復を過小評価した**

ことです。

最終評価：

**ENTRY_FILLED → favorable excursion → thesis weakened → SL_REACHED → FIRED**

約**-1R**で終了です。

ここから即座にWTI SELLへ反転はしません。4%以上落ちた直後なので、次はNov限で戻りの構造を待ちます。

---

### `20260919_USDJPY_BUY_PULLBACK` — 継続

既存：

**Entry 156.00–156.50  
SL 155.20  
TP1 158.20  
TP2 159.60  
RR 1.86**

9月21日のUSDJPYはReuters時点で約**157.48**。BOJ利上げ後も円安方向が維持されていますが、日本当局のrate checkを受けた介入警戒も続いています。citeturn511588news50

月曜安値について複数データに若干差がありますが、確認できた系列では156.5を明確に下回っておらず、Entry約定を確定できません。

したがって、

**UNFILLED / invalidation=not_fired**

のまま維持します。

157円台で追いません。

---

## 3. 市場全体の前提

昨日の市場はかなり強いrisk-onです。

Nasdaq Compositeは**+2.26%**、S&P500は**+1.49%**。AI関連、特に半導体が先導し、Nasdaqは最高値を更新しました。WTI急落と10年債利回りの5%割れがGrowth株の逆風を同時に弱めています。citeturn213769news0turn213769news4

米10年債利回りは約**4.96%**。依然高いですが、「5%突破が続く」状態ではなくなりました。citeturn213769news77

DXYは逆に約**100.40**まで上昇。Fed追加利上げ観測がドルを支えています。USDJPYも約157.5なので、**株高＝全面的ドル安**ではありません。citeturn511588news50

Goldはこのドル高・利上げ観測に押され、米金先物は**4383.90ドル**、-0.9%。現物は4349.94ドルでした。citeturn213769news71

Cryptoはさらに強烈です。BTC/USDは約**85.9～86.5k**まで上昇し、CME Bitcoin Futuresも9月21日に**86395、高値86520**。前日比+6%超です。citeturn443792search2turn511588search1

ETH/USDも約**2730～2750**、CME Ether Futuresも約**2754**まで上昇。ETFフローは直近確定分でBTC、ETHとも再びプラスです。citeturn192842search1turn192842search2turn511588news52turn285903search0

VIXはCboeの9月21日15:03 ET遅延値で**14.66**。前日14.81からさらに低下しています。citeturn113844search0

総合regimeは**RISK_ON**です。

ただし、9月24日のTrump–Xi会談が控えており、米中・AI・中東問題が議題になる見通しです。5営業日持つTSOでは無視できないイベントリスクです。citeturn213769news0

---

## 4. 10資産別判断

| 資産 | 判断 | 今朝の評価 |
|---|---|---|
| GOLD | **NO_TRADE** | GCZ26基準。約4384付近。ドル高・Fed再利上げ観測 vs 地政学でMIXED |
| BTC | **NO_TRADE** | 約86k。ETF/CMEとも強いが一日+6%超、short squeeze後を追わない |
| ETH | **NO_TRADE** | 約2.74k。2,700突破は強いが急伸後 |
| WTI | **NO_TRADE** | 旧BUYはfired。Nov限約92.47。即SELLも追随になる |
| USDJPY | **既存B+待機** | 約157.5。156.00–156.50まで戻る場合のみ旧BUY候補 |
| SPX | **B BUY_PULLBACK / B+** | ESZ26約7798遅延値。7760–7780だけを買う |
| NASDAQ | **NO_TRADE** | NQZ26約30.2k～30.5k。強いが急伸後 |
| DXY | **NO_TRADE** | 約100.4。ドル高継続だが独立edge弱い |
| US10Y | **NO_TRADE** | 約4.96%。5%割れだがFed追加利上げ観測あり |
| VIX | **NO_TRADE** | 約14.66。risk-on確認材料だが既に低い |

NQZ26はデータ提供時点差があり、9月21日系列は約30,203、より遅い遅延値では約30,526まで確認できます。方向は明確に上ですが、正確な清算値を一本化できないためNASDAQ行は`partially_verified`とします。citeturn102646search6turn872640search4

---

## 5. A級候補

**なし。**

SPXは数値だけならかなり近いです。

\[
RR=(7850-7770)/(7770-7730)=2.00
\]

raw win_prob = **0.56**

二点分布なら、

\[
0.56\times2.00-0.44=+0.68R
\]

です。

しかし現在は既にS&P500 +1.49%、Nasdaq +2.26%上昇後です。

さらに、

- Entry未到達確率
- 大幅上昇翌日のmean reversion
- 9月24日Trump–Xi会談
- Fed追加利上げ観測

を織り込み、subjective expected_rは**0.40R**まで落とします。

A条件の`expected_r>=0.45`を満たさないので、**Aにはしません**。

---

## 6. B級監視候補

### `20260922_SPX_BUY_PULLBACK` — B / B+

**Entry：7760–7780**  
**Mid：7770**  
**SL：7730**  
**TP1：7850**  
**TP2：7910**  
**RR：2.00**  
**win_prob：0.56**  
**較正後参考：0.58**  
**expected_r：0.40**  
**MAE想定：0.24R**  
**risk_pct：0.25%**

根拠は、

**WTI急落 → インフレ圧力低下 → US10Y 5%割れ → Growth/AI株急騰 → VIX低下**

というクロスアセット整合です。

ただし7790～7800台で成行BUYはしません。

**7760–7780まで押すが、7730を割らない**場合だけ参加です。

XM最小0.10lotで40ポイントSLなら概算実損は700円未満＋スプレッド程度なので、3,000円制約を十分満たします。citeturn867258search4

したがって**B+観察候補**。

なおUSDJPYの既存0.25%シグナルもまだ生きています。両方が同日に約定すれば、

**SPX 0.25% + USDJPY 0.25% = 0.50%**

で上限到達です。その後は新規を取りません。

---

## 7. 触らない資産

特に**NASDAQ、BTC、ETH、WTI**を追いません。

NASDAQは方向としては最も強いです。NQZ26は30,000を突破し、AI株が先導しています。しかし一日で大きく上昇した後なので、新規BUYのEntry品質が悪い。citeturn213769news0turn872640search4

BTCも同様です。約81kから86kへ一気に上昇し、CMEも+6%超。ETF資金流入という実需根拠はありますが、同時にshort squeezeも大きく寄与しています。citeturn511588news52turn511588search1

ETHも2,700を突破しましたが、短期清算を伴った上昇です。ここはEntryではなく、**次の押しがどこで止まるかを見る場所**です。citeturn285903search4

WTIは逆方向。BUY仮説は明確に失敗しましたが、Oct限が一日4.5%下がった地点でSELLすると、今度は下落追随になります。

**損切り→即ドテンSELL**はしません。

---

## 8. 後日検証ポイント

SPXは、

**7760–7780へ押して反発 → Entry成立**  
**7730割れ → fired**  
**7850 → TP1**  
**7910 → TP2**

です。

NASDAQは**NQ 30,000台を維持できるか**が重要。30,000を割らず、US10Yも5%未満、VIX15未満なら「高金利でもGrowthを買う」regimeがかなり強いと判断します。

BTCは**83.2–84.0kへの押し**が次の重要地点です。そこを維持し、ETFフローもプラスならBUY候補を作り直せます。86.5kをそのまま追うことはしません。

ETHは**2,650–2,700**を支持化できるか。2,800突破後の押しでもよいです。

WTIは今日から新規観察軸を**Nov-26**へ切り替えます。

**94–95へ戻して失速**
ならSELL仮説候補。

逆に**96.5以上を回復**
なら今回の下落が行き過ぎだった可能性を再評価します。

USDJPYは既存通り、

**156.00–156.50 → Entry候補**  
**155.20 → fired**  
**158.20 → TP1**  
**実介入確認 → 価格にかかわらず再評価**

です。

---

## 9. Obsidian保存用 Observation Draft

```markdown
# 2026-09-22 Oil Down / AI Risk-On / SPX Pullback Candidate

Model:
GPT-5.6 Sol

Market protagonist:
NASDAQ

Gold reference:
COMEX Dec-2026 / GCZ26

crypto_grounds:
etf=有
cme=有

expected_r_basis:
subjective

## Regime

RISK_ON

## Main market change

WTI collapsed while equities and crypto rallied.

Sep21:
WTI Oct:
95.78
-4.51%

WTI Nov:
92.47

US10Y:
~4.96%

S&P500:
+1.49%

Nasdaq Composite:
+2.26%
record close

VIX:
~14.66 delayed

BTC:
~86k

ETH:
~2.74k

DXY:
~100.4

USDJPY:
~157.5

Gold futures:
~4383.9

Interpretation:

Previous chain:
WTI up
-> inflation up
-> yields up
-> growth pressure

reversed:

WTI down
-> inflation pressure lower
-> yields below 5%
-> AI / growth bid
-> VIX lower

## WTI previous signal

20260917_WTI_BUY_PULLBACK

Actual user:
Entry ~101.19
SL 98.90
TP 105.20

Result:
FIRED

Path:
ENTRY_FILLED
favorable excursion
thesis weakened
SL_REACHED

Approx:
-1R

Learning:
physical infrastructure damage was real
but effective Saudi supply recovery through Hormuz was underestimated.

Saudi Gulf exports:
~2.9m bpd recent average
vs ~0.7m bpd in August

Do not immediately reverse to SELL.

New WTI observation contract:
Nov-26

## USDJPY existing pending

20260919_USDJPY_BUY_PULLBACK

Entry:
156.00-156.50

SL:
155.20

TP1:
158.20

TP2:
159.60

Status:
UNFILLED
not_fired

Current:
~157.5

Do not chase.

## New SPX signal

20260922_SPX_BUY_PULLBACK

Rank:
B

B+:
YES

Entry:
7760-7780

Mid:
7770

SL:
7730

TP1:
7850

TP2:
7910

RR:
2.00

win_prob:
0.56

calibrated reference:
0.58

raw two-point EV:
0.68R

subjective expected_r:
0.40R

MAE:
0.24R

Risk:
0.25%

Expected XM minimum-lot loss:
well below JPY3000

Adjustments:
post-rally mean reversion
entry non-fill
Trump-Xi Sep24
Fed tightening risk

Invalidation:
ESZ26 below 7730
OR US10Y back above 5.05 with VIX repricing

## Risk cluster

SPX / NASDAQ / BTC / ETH:
same broad risk-on cluster

Use SPX only.

Do not stack NQ/BTC/ETH longs.

If USDJPY and SPX both fill:
total risk = 0.50%
no third trade.

## Active invalidation

20260919_USDJPY_BUY_PULLBACK=not_fired
20260922_SPX_BUY_PULLBACK=not_fired

## New signals

A:
NONE

B:
SPX BUY_PULLBACK

B+:
SPX BUY_PULLBACK

#TSO #SPX #NASDAQ #WTI #BTC #USDJPY
```

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-22,20260922_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,84,85,,MIXED,84,89,96,82,83,86,wait_for_GCZ26_reclaim_4420_or_break_4320_with_DXY_US10Y_confirmation,GCZ26_4320_4383.9_4420_DXY_US10Y_1d_3d,partially_verified
2026-09-22,20260922_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,94,90,,RISK_ON,88,92,98,92,93,92,do_not_chase_86k_short_squeeze_wait_for_83.2k_84k_retest_or_86.5k_break_retest,BTC_83200_84000_86000_86500_ETF_CME_1d_3d,verified
2026-09-22,20260922_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,89,88,,RISK_ON,84,90,96,89,88,87,do_not_chase_post_squeeze_wait_for_2650_2700_retest_or_2800_break_retest,ETH_2650_2700_2740_2800_ETF_CME_1d_3d,partially_verified
2026-09-22,20260922_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,93,99,,EVENT,94,99,99,93,94,98,previous_20260917_BUY_fired_at_OILCash_98.90_wait_for_new_Nov26_structure,WTI_Nov26_92.47_94_95_96.5_USIran_Saudi_exports_1d_3d,verified
2026-09-22,20260922_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,90,82,,EVENT,82,95,98,89,85,94,manage_existing_20260919_BUY_PULLBACK_155.20_or_confirmed_MOF_intervention_fires,USDJPY_155.20_156_156.50_157.48_158.20_MOF_1d_3d,verified
2026-09-22,20260922_SPX_BUY_PULLBACK,SPX,BUY,B,PULLBACK,7760,7780,7730,7850,7910,2.00,0.56,0.40,99,92,47,0.25,RISK_ON,74,91,96,89,88,89,ESZ26_below_7730_or_US10Y_above_5.05_with_VIX_risk_repricing,ESZ26_7730_7760_7780_7850_7910_US10Y_VIX_1d_3d_5d,partially_verified
2026-09-22,20260922_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,96,84,,RISK_ON,88,94,98,95,94,92,do_not_chase_NQZ26_after_large_move_wait_for_30000_support_or_clean_pullback,NQZ26_30000_30200_30500_US10Y_VIX_1d_3d,partially_verified
2026-09-22,20260922_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,84,82,,MIXED,80,92,95,82,83,90,wait_for_DXY_hold_above_100.5_or_break_below_99.8_with_rate_confirmation,DXY_99.8_100.4_100.5_US10Y_USDJPY_1d_3d,verified
2026-09-22,20260922_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,90,84,,MIXED,88,93,97,88,89,95,wait_for_US10Y_break_above_5.05_or_extend_below_4.90_with_oil_equity_confirmation,US10Y_4.90_4.96_5.05_WTI_NQ_GOLD_1d_3d,verified
2026-09-22,20260922_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,82,88,,RISK_ON,70,86,94,78,79,84,wait_for_VIX_reclaim_above_16_or_hold_below_14.5_with_ES_NQ_confirmation,VIX_14.5_14.66_16_ES_NQ_1d_3d,partially_verified
```

### TSO_LOG JSON

```json
[
  {"date":"2026-09-22","signal_id":"20260922_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":84,"no_trade_score":85,"risk_pct":null,"regime":"MIXED","ems":84,"ffs":89,"cds":96,"ias":82,"cbs":83,"mes":86,"invalidation":"wait_for_GCZ26_reclaim_4420_or_break_4320_with_DXY_US10Y_confirmation","verification_target":"GCZ26_4320_4383.9_4420_DXY_US10Y_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-22","signal_id":"20260922_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":94,"no_trade_score":90,"risk_pct":null,"regime":"RISK_ON","ems":88,"ffs":92,"cds":98,"ias":92,"cbs":93,"mes":92,"invalidation":"do_not_chase_86k_short_squeeze_wait_for_83.2k_84k_retest_or_86.5k_break_retest","verification_target":"BTC_83200_84000_86000_86500_ETF_CME_1d_3d","verified_status":"verified"},
  {"date":"2026-09-22","signal_id":"20260922_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":89,"no_trade_score":88,"risk_pct":null,"regime":"RISK_ON","ems":84,"ffs":90,"cds":96,"ias":89,"cbs":88,"mes":87,"invalidation":"do_not_chase_post_squeeze_wait_for_2650_2700_retest_or_2800_break_retest","verification_target":"ETH_2650_2700_2740_2800_ETF_CME_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-22","signal_id":"20260922_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":93,"no_trade_score":99,"risk_pct":null,"regime":"EVENT","ems":94,"ffs":99,"cds":99,"ias":93,"cbs":94,"mes":98,"invalidation":"previous_20260917_BUY_fired_at_OILCash_98.90_wait_for_new_Nov26_structure","verification_target":"WTI_Nov26_92.47_94_95_96.5_USIran_Saudi_exports_1d_3d","verified_status":"verified"},
  {"date":"2026-09-22","signal_id":"20260922_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":90,"no_trade_score":82,"risk_pct":null,"regime":"EVENT","ems":82,"ffs":95,"cds":98,"ias":89,"cbs":85,"mes":94,"invalidation":"manage_existing_20260919_BUY_PULLBACK_155.20_or_confirmed_MOF_intervention_fires","verification_target":"USDJPY_155.20_156_156.50_157.48_158.20_MOF_1d_3d","verified_status":"verified"},
  {"date":"2026-09-22","signal_id":"20260922_SPX_BUY_PULLBACK","asset":"SPX","side":"BUY","rank":"B","type":"PULLBACK","entry_low":7760,"entry_high":7780,"sl":7730,"tp1":7850,"tp2":7910,"rr":2.00,"win_prob":0.56,"expected_r":0.40,"tq_score":99,"opp_score":92,"no_trade_score":47,"risk_pct":0.25,"regime":"RISK_ON","ems":74,"ffs":91,"cds":96,"ias":89,"cbs":88,"mes":89,"invalidation":"ESZ26_below_7730_or_US10Y_above_5.05_with_VIX_risk_repricing","verification_target":"ESZ26_7730_7760_7780_7850_7910_US10Y_VIX_1d_3d_5d","verified_status":"partially_verified"},
  {"date":"2026-09-22","signal_id":"20260922_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":96,"no_trade_score":84,"risk_pct":null,"regime":"RISK_ON","ems":88,"ffs":94,"cds":98,"ias":95,"cbs":94,"mes":92,"invalidation":"do_not_chase_NQZ26_after_large_move_wait_for_30000_support_or_clean_pullback","verification_target":"NQZ26_30000_30200_30500_US10Y_VIX_1d_3d","verified_status":"partially_verified"},
  {"date":"2026-09-22","signal_id":"20260922_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":84,"no_trade_score":82,"risk_pct":null,"regime":"MIXED","ems":80,"ffs":92,"cds":95,"ias":82,"cbs":83,"mes":90,"invalidation":"wait_for_DXY_hold_above_100.5_or_break_below_99.8_with_rate_confirmation","verification_target":"DXY_99.8_100.4_100.5_US10Y_USDJPY_1d_3d","verified_status":"verified"},
  {"date":"2026-09-22","signal_id":"20260922_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":99,"opp_score":90,"no_trade_score":84,"risk_pct":null,"regime":"MIXED","ems":88,"ffs":93,"cds":97,"ias":88,"cbs":89,"mes":95,"invalidation":"wait_for_US10Y_break_above_5.05_or_extend_below_4.90_with_oil_equity_confirmation","verification_target":"US10Y_4.90_4.96_5.05_WTI_NQ_GOLD_1d_3d","verified_status":"verified"},
  {"date":"2026-09-22","signal_id":"20260922_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":98,"opp_score":82,"no_trade_score":88,"risk_pct":null,"regime":"RISK_ON","ems":70,"ffs":86,"cds":94,"ias":78,"cbs":79,"mes":84,"invalidation":"wait_for_VIX_reclaim_above_16_or_hold_below_14.5_with_ES_NQ_confirmation","verification_target":"VIX_14.5_14.66_16_ES_NQ_1d_3d","verified_status":"partially_verified"}
]
```

本日の最大の更新は、**WTI BUYを失敗として明確に閉じた一方、その原油急落そのものが株式・Cryptoのrisk-on条件を改善したこと**です。

ただしNASDAQ・BTC・ETHを同時に買えば、実質的には同じ「risk-on仮説」を重複保有することになります。そこで今日は**SPXの押し目1本だけをB+として残し、他のrisk-on資産は追わない**という構成にしています。
