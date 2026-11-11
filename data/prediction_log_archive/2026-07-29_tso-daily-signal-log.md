<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-07-29 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 13661 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026年7月29日

利用価格は主に**7月28日の米国市場終値・CME遅延値・7月29日朝の暗号資産価格**です。完全な同時刻スナップショットではないため、各行の検証状態を分けています。

## 1. 本日の結論

**新規A級候補：なし**

**新規B級監視候補**

- GOLD：3995～4025への押し目買い
- NASDAQ：反発後の戻り売り。ただし本日のFOMC前には新規執行しない

**前回からの仮想ポジション管理**

- GOLD買い：Entry帯へ到達。ほぼ建値圏
- NASDAQ売り：Entry成立とみなし、含み益方向。TP1接近

**本日の新規NO_TRADE**

BTC、ETH、WTI、USDJPY、SPX、DXY、US10Y、VIX。

7月28日の米国株は、ダウが1.29%上昇、S&P500が0.37%上昇した一方、NASDAQは0.04%高にとどまりました。AI・半導体株から非テクノロジー株への資金移動が続いています。citeturn391369news81turn391369news82

本日はFOMCの政策発表を控えています。市場は据え置きを中心に見ていますが、利上げ確率も約3割残っており、発表前の新規ポジションは原則0.25%以下、または見送りとします。citeturn924916news45turn924916news47

---

## 2. 前回判断の簡易検証

### GOLD：`20260728_GOLD_LONG_B-PULLBACK`

前回条件：

- Entry：4035～4065
- SL：3940
- TP1：4175
- TP2：4260

7月28日の米金先物は4038.70ドル付近まで下落し、清算値も4036.30ドル前後でした。したがって、**Entry帯に到達し、4035～4040付近で仮想約定した**と扱います。citeturn664520news36turn664520news38

- Entry：成立
- 推定約定価格：4038
- SL：未到達
- TP1・TP2：未到達
- 推定MFE：約+0.1R未満
- 推定MAE：約0.1R未満
- 現状：ほぼ建値圏
- 判断：継続。ただしFOMC前に追加しない

金価格はドル高と利上げ警戒で一週間ぶりの安値圏へ下落しています。短期的には弱いものの、4030～4000ドル近辺の支持確認余地があります。citeturn664520news36turn664520news37

### NASDAQ：`20260728_NASDAQ_SHORT_B-REVERSAL`

前回条件：

- Entry：28600～28720
- SL：29150
- TP1：27950
- TP2：27400

前回提示時の基準値は28600台であり、Entry帯内だったため**28620付近で仮想約定**と扱います。その後、CMEのNQ先物は一時27684.50、別の遅延表示では28078.25まで下落しました。citeturn924916search3turn924916search19

- Entry：成立
- 推定約定価格：28620
- SL：未到達
- TP1：一時到達した可能性が高い
- 推定MFE：約+1.5R
- 推定MAE：精密値未確認
- 現状：利益方向
- 判断：新規追加禁止。既存仮想ポジションは5営業日時間決済ルールを維持

半導体株ではMicron、AMD、Applied Materialsなどが大幅下落し、AI投資の採算性と中国勢の競争力が売り材料になっています。citeturn391369news82turn391369news85

---

## 3. 市場全体の前提

### 判定：中立。ただし内部は明確なセクターローテーション

指数全体では極端なリスクオフではありません。S&P500とダウは上昇し、VIXも18台へ低下しました。一方、半導体・AI関連株が売られ、資金は生活必需品、資本財、景気敏感株などへ移っています。citeturn391369news81turn391369news82turn664520search0

重要なのは、現在の市場が単純な「株高」ではない点です。

- 原油安と金利低下：株式全体には追い風
- AI・半導体の収益性懸念：NASDAQには逆風
- FOMC：全資産にイベントギャップリスク
- 大型テクノロジー決算：NASDAQの方向を短時間で反転させ得る
- ドル円163円台：介入リスクが高い

したがって、本日は**指数方向よりも、NASDAQ弱・非テクノロジー株優位という内部構造を重視**します。

---

## 4. 10資産別判断

### GOLD

米金先物は4038.70ドル、清算値は4036.30ドル前後まで下落しました。ドル指数が101.35付近を維持し、FOMCでの利上げ可能性が残ることが重荷です。citeturn664520news36turn664520news38turn924916news43

前回の買いEntryは成立しましたが、FOMC前なので追加はしません。

**判断：既存B級継続、新規は押し目監視のみ**

---

### BTC

BTCは63903ドル付近で、日中高値64713ドル、安値62772ドルです。citeturn391369finance0

直近では65000ドルを維持できず、FOMC前のポジション縮小が出ています。Bitcoin ETFは7月中旬以降改善傾向が報じられていますが、2026年通算では依然として大幅な流出超過です。citeturn391369search8turn391369search16

当日ETFフローとCME basisの完全確認がないため、MESは48とします。

**判断：NO_TRADE**

---

### ETH

ETHは1624.95ドル付近です。citeturn391369finance1

BTCが下落する局面でETH独自の相対強度は確認できません。BTCよりも流動性と情報確認度が低く、FOMC前にリスクを取る根拠が不足しています。

**判断：NO_TRADE**

---

### WTI

CMEのWTI先物は81.32ドル、別の同日遅延値では78.03ドルまで下落しました。時刻差が大きいため、基準値は79～81ドルとします。citeturn924916search5turn924916search17

米国とイランの緊張緩和により、供給途絶プレミアムが急速に剥落しています。米10年債利回りも4.604%まで低下しました。citeturn924916news45

方向は下ですが、すでに短期間で大幅下落しているため、追随売りは過去の失敗モードに該当します。

**判断：NO_TRADE**

---

### USDJPY

ドル指数は101.35付近、円は40年来の安値圏にあり、日本当局は介入姿勢を改めて示しています。citeturn924916news43turn664520news35

米金利は低下していますが、日米金利差は依然大きく、売りにも買いにも非対称なイベントリスクがあります。

**判断：NO_TRADE**

---

### SPX

ES先物は7月28日の遅延値で7469.75付近です。citeturn664520search14

S&P500はテクノロジー株の弱さを他セクターが吸収しています。市場の広がりはNASDAQより良好ですが、FOMC直前なので新規買いの期待値は高くありません。

**判断：NO_TRADE**

---

### NASDAQ

NQ先物は28078付近で、別時点では27684.50まで下落しました。citeturn924916search3turn924916search19

半導体株の急落と、中国のAI・半導体技術進展への警戒がNASDAQの相対的弱さを生んでいます。citeturn391369news81turn391369news82

前回の売りシグナルは有効ですが、すでに大きく下落しているため新規追随はしません。

**判断：既存B級売り継続、新規NO_TRADE**

---

### DXY

ドル指数は101.35付近です。FOMC据え置きなら短期的なドル売り、予想外の利上げまたは強いタカ派発言ならドル上昇が想定されます。citeturn924916news43turn924916news44

方向よりイベントギャップの寄与が大きいため、通常のテクニカル優位が機能しにくい状態です。

**判断：NO_TRADE**

---

### US10Y

米10年債利回りは4.604%まで低下しました。原油安と地政学リスク緩和がインフレ懸念を後退させています。citeturn924916news45

4.60%は重要な分岐点ですが、FOMCで再び4.70%方向へ跳ねる可能性があります。

**判断：NO_TRADE**

---

### VIX

Cboeの7月28日表示ではVIXは18.24、別の終値系列では18.04です。citeturn664520search0turn664520search4

株式市場全体のパニックは後退していますが、FOMCと大型決算の前としては低すぎる水準でもありません。

**判断：NO_TRADE**

---

## 5. A級候補

**なし**

GOLDはEntry成立後ですが、CBS・MAE条件が不足しています。NASDAQ売りは方向性が機能したものの、すでに下落が進み、現在値からの新規RRが悪化しています。

---

## 6. B級監視候補

### GOLD押し目買い

- signal_id：`20260729_GOLD_LONG_B-PULLBACK`
- Entry：3995～4025
- SL：3900
- TP1：4140
- TP2：4225
- RR：1.25
- win_prob：0.60
- expected_r：0.42
- risk_pct：0.25
- MAE想定：0.31R
- 時間決済：5営業日
- 無効化：3900割れ、US10Yが4.75%超へ反発
- A級昇格：FOMC後に4025以上を維持、US10Yが4.55%以下、CBS75以上

### NASDAQ戻り売り

- signal_id：`20260729_NASDAQ_SHORT_B-REVERSAL`
- Entry：28250～28400
- SL：28950
- TP1：27650
- TP2：27100
- RR：1.13
- win_prob：0.58
- expected_r：0.36
- risk_pct：0.25
- MAE想定：0.38R
- 時間決済：5営業日
- 無効化：28950超、大型決算後の上方ギャップ定着
- A級昇格：FOMC後に28000を割り、VIX20超、戻りが28250以下で止まること

**FOMC発表前は新規執行しません。**

---

## 7. 触らない資産

- BTC：MES50未満、65000ドル維持失敗
- ETH：独立した強さなし
- WTI：急落後で売り追随禁止
- USDJPY：介入と金利差が衝突
- SPX：指数は堅いがイベント前
- DXY：FOMCの二方向ギャップ
- US10Y：4.60%分岐点で政策発表待ち
- VIX：方向性よりイベント保険需要が支配

---

## 8. 後日検証ポイント

1. GOLDの前回買いが3940のSLを回避できるか
2. NASDAQ売りがTP1の27950を終値ベースで達成するか
3. NQがFOMC後に28000を割るか、28500を回復するか
4. BTCが62772ドル安値を維持できるか
5. WTIが78ドルを割るか、82ドルを回復するか
6. US10Yが4.60%を明確に割るか
7. DXYが101を割るか、102へ上昇するか
8. VIXが20を超えるか、17台へ低下するか

---

## 9. Obsidian保存用Observation Draft

```markdown
# 2026-07-29 指数安定とNASDAQ内部崩れの併存

Type: 一般市場Observation

## Summary

米国株全体は安定したが、AI・半導体株の売りが続き、NASDAQは相対的に弱い。
原油と米長期金利の低下は株式全体を支えた一方、FOMCと大型テクノロジー決算が新規ポジションを抑制している。
前回のGOLD買いはEntry成立、NASDAQ売りは利益方向に進んだと評価する。

## Observation

- BTCは63903ドル、日中安値62772ドル。
- ETHは1624.95ドル。
- GOLD先物は4036～4039ドル。
- WTIは約78～81ドル。
- ES先物は約7469.75。
- NQ先物は約27685～28078。
- DXYは約101.35。
- US10Yは約4.604%。
- VIXは約18.0～18.2。
- AI・半導体株から非テクノロジー株への資金移動が継続。

## Evaluation

A級候補なし。
GOLDとNASDAQをB級監視とするが、FOMC前の新規執行は禁止。
前回NASDAQ売りはTP1接近または一時到達の可能性が高い。
WTIは方向が下でも急落後の追随を禁止する。

## Interpretation

市場全体の指数だけを見ると安定しているが、内部ではAI・半導体株の評価修正が進んでいる。
原油安・金利低下による支援と、AI投資採算への疑念が同時に存在するため、SPXとNASDAQの乖離が続きやすい。

## Later Review

- FOMC後のNQ28000
- GOLD3940と4025
- US10Y4.60%
- BTC62772
- WTI78
- DXY101
- VIX20

## Tags

#TSO #MarketObservation #NASDAQ #GOLD #FOMC #Semiconductors #SectorRotation
```

---

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-07-29,20260729_GOLD_LONG_B-PULLBACK,GOLD,BUY,B,PULLBACK,3995,4025,3900,4140,4225,1.25,0.60,0.42,67,66,38,0.25,WEAK_PULLBACK,64,58,63,65,71,61,3900_break_or_US10Y_above_4.75,5d_close_MFE_MAE_and_FOMC_reaction,verified
2026-07-29,20260729_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,53,46,79,,WEAK_NEUTRAL,54,43,48,51,55,48,mes_below_50_and_65000_rejection,BTC_62772_65000_ETF_flow_and_5d_close,verified
2026-07-29,20260729_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,44,39,82,,WEAK,47,40,44,45,49,39,no_independent_relative_strength,ETH_BTC_ratio_and_5d_close,partially_verified
2026-07-29,20260729_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,77,39,86,,SHOCK_DOWNTREND,68,60,78,55,62,64,post_shock_momentum_chase_risk,WTI_78_break_or_82_recovery_and_5d_close,partially_verified
2026-07-29,20260729_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,66,44,85,,STRONG_UP_INTERVENTION_RISK,63,58,59,46,60,57,intervention_and_FOMC_gap_risk,USDJPY_post_FOMC_BOJ_and_5d_close,partially_verified
2026-07-29,20260729_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,61,54,71,,ROTATION_BULLISH,62,57,61,63,65,58,FOMC_and_earnings_gap_risk,ES_post_FOMC_and_5d_close,verified
2026-07-29,20260729_NASDAQ_SHORT_B-REVERSAL,NASDAQ,SELL,B,REVERSAL,28250,28400,28950,27650,27100,1.13,0.58,0.36,69,67,42,0.25,BEARISH_ROTATION,66,53,68,65,70,57,28950_break_or_earnings_up_gap_hold,5d_close_MFE_MAE_FOMC_and_earnings,partially_verified
2026-07-29,20260729_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,58,47,76,,EVENT_DEPENDENT,62,57,53,50,58,55,FOMC_two_way_gap_risk,DXY_101_or_102_break_and_5d_close,verified
2026-07-29,20260729_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,61,51,74,,YIELD_EASING,63,60,58,55,61,60,FOMC_policy_repricing,US10Y_4.55_or_4.70_break_and_5d_close,verified
2026-07-29,20260729_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,55,46,72,,EVENT_PREMIUM,59,53,62,60,61,54,no_clean_direction_before_FOMC,VIX_17_or_20_break_and_5d_close,verified
```

## TSO_LOG JSON

```json
[
  {"date":"2026-07-29","signal_id":"20260729_GOLD_LONG_B-PULLBACK","asset":"GOLD","side":"BUY","rank":"B","type":"PULLBACK","entry_low":3995,"entry_high":4025,"sl":3900,"tp1":4140,"tp2":4225,"rr":1.25,"win_prob":0.60,"expected_r":0.42,"tq_score":67,"opp_score":66,"no_trade_score":38,"risk_pct":0.25,"regime":"WEAK_PULLBACK","ems":64,"ffs":58,"cds":63,"ias":65,"cbs":71,"mes":61,"invalidation":"3900_break_or_US10Y_above_4.75","verification_target":"5d_close_MFE_MAE_and_FOMC_reaction","verified_status":"verified"},
  {"date":"2026-07-29","signal_id":"20260729_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":53,"opp_score":46,"no_trade_score":79,"risk_pct":null,"regime":"WEAK_NEUTRAL","ems":54,"ffs":43,"cds":48,"ias":51,"cbs":55,"mes":48,"invalidation":"mes_below_50_and_65000_rejection","verification_target":"BTC_62772_65000_ETF_flow_and_5d_close","verified_status":"verified"},
  {"date":"2026-07-29","signal_id":"20260729_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":44,"opp_score":39,"no_trade_score":82,"risk_pct":null,"regime":"WEAK","ems":47,"ffs":40,"cds":44,"ias":45,"cbs":49,"mes":39,"invalidation":"no_independent_relative_strength","verification_target":"ETH_BTC_ratio_and_5d_close","verified_status":"partially_verified"},
  {"date":"2026-07-29","signal_id":"20260729_WTI_NONE_NO_TRADE","asset":"WTI","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":77,"opp_score":39,"no_trade_score":86,"risk_pct":null,"regime":"SHOCK_DOWNTREND","ems":68,"ffs":60,"cds":78,"ias":55,"cbs":62,"mes":64,"invalidation":"post_shock_momentum_chase_risk","verification_target":"WTI_78_break_or_82_recovery_and_5d_close","verified_status":"partially_verified"},
  {"date":"2026-07-29","signal_id":"20260729_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":66,"opp_score":44,"no_trade_score":85,"risk_pct":null,"regime":"STRONG_UP_INTERVENTION_RISK","ems":63,"ffs":58,"cds":59,"ias":46,"cbs":60,"mes":57,"invalidation":"intervention_and_FOMC_gap_risk","verification_target":"USDJPY_post_FOMC_BOJ_and_5d_close","verified_status":"partially_verified"},
  {"date":"2026-07-29","signal_id":"20260729_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":61,"opp_score":54,"no_trade_score":71,"risk_pct":null,"regime":"ROTATION_BULLISH","ems":62,"ffs":57,"cds":61,"ias":63,"cbs":65,"mes":58,"invalidation":"FOMC_and_earnings_gap_risk","verification_target":"ES_post_FOMC_and_5d_close","verified_status":"verified"},
  {"date":"2026-07-29","signal_id":"20260729_NASDAQ_SHORT_B-REVERSAL","asset":"NASDAQ","side":"SELL","rank":"B","type":"REVERSAL","entry_low":28250,"entry_high":28400,"sl":28950,"tp1":27650,"tp2":27100,"rr":1.13,"win_prob":0.58,"expected_r":0.36,"tq_score":69,"opp_score":67,"no_trade_score":42,"risk_pct":0.25,"regime":"BEARISH_ROTATION","ems":66,"ffs":53,"cds":68,"ias":65,"cbs":70,"mes":57,"invalidation":"28950_break_or_earnings_up_gap_hold","verification_target":"5d_close_MFE_MAE_FOMC_and_earnings","verified_status":"partially_verified"},
  {"date":"2026-07-29","signal_id":"20260729_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":58,"opp_score":47,"no_trade_score":76,"risk_pct":null,"regime":"EVENT_DEPENDENT","ems":62,"ffs":57,"cds":53,"ias":50,"cbs":58,"mes":55,"invalidation":"FOMC_two_way_gap_risk","verification_target":"DXY_101_or_102_break_and_5d_close","verified_status":"verified"},
  {"date":"2026-07-29","signal_id":"20260729_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":61,"opp_score":51,"no_trade_score":74,"risk_pct":null,"regime":"YIELD_EASING","ems":63,"ffs":60,"cds":58,"ias":55,"cbs":61,"mes":60,"invalidation":"FOMC_policy_repricing","verification_target":"US10Y_4.55_or_4.70_break_and_5d_close","verified_status":"verified"},
  {"date":"2026-07-29","signal_id":"20260729_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":null,"entry_high":null,"sl":null,"tp1":null,"tp2":null,"rr":null,"win_prob":null,"expected_r":null,"tq_score":55,"opp_score":46,"no_trade_score":72,"risk_pct":null,"regime":"EVENT_PREMIUM","ems":59,"ffs":53,"cds":62,"ias":60,"cbs":61,"mes":54,"invalidation":"no_clean_direction_before_FOMC","verification_target":"VIX_17_or_20_break_and_5d_close","verified_status":"verified"}
]
```
