<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-07-31 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-15T03:54:47Z / chars: 16077 / 値は無修正 -->

停止条件は定義されていません。前回、出力量を理由に停止した判断は明確な契約違反でした。今回は10資産のTSO_LOGまで完遂します。

# TSO Daily Signal Log v2 — 2026年7月31日

**基準時刻：2026年7月31日 8:28（日本時間）**

利用データは、主に7月30日の米国市場終値、同日清算値、7月31日朝の暗号資産価格です。ES・NQ・為替などは取得時刻が揃っていないため、該当資産を `partially_verified` としています。

## 1. 本日の結論

**新規A級候補：なし**

**B級監視候補**

- GOLD：上昇後の押し目買い
- NASDAQ：押し目買いへの転換監視。ただし現時点ではNO_TRADE

**本日の執行対象**

- 即時執行：なし
- 最大日次リスク：0%
- B級候補がEntry帯へ到達した場合のみ：0.25%

7月30日の米国株はMicrosoftの好決算を起点に急反発し、S&P500は1.7%、NASDAQは2.8%上昇しました。半導体指数も大幅反発しましたが、同時に米長期債利回りは高止まりし、30年債利回りは2007年以来の高水準に達しました。したがって、今回の株高は「全面的な金融環境改善」ではなく、主に大型AI銘柄の決算による集中反発と評価します。citeturn619252news66turn619252news68

GOLDはCOMEX先物が4100.10ドルで清算され、前日比1.58%上昇しました。前回のB級買いは利益方向ですが、現在値追随ではなく押し目を待ちます。citeturn619744news36

---

## 2. 前回判断の簡易検証

### GOLD：`20260730_GOLD_LONG_B-PULLBACK`

前回条件：

- Entry：4010～4040
- SL：3910
- TP1：4140
- TP2：4220
- 時間決済：5営業日

7月30日のCOMEX金先物は4100.10ドルで清算されました。前日の安値圏から反発したため、4010～4040での仮想約定は利益方向へ進んでいます。citeturn619744news36

暫定採点：

- 仮想約定：4025
- 7月30日清算値：4100.10
- 含み値幅：+75.10
- 1R：115
- 暫定MFE：約+0.65R
- 暫定MAE：精密な日中安値が揃わず未確定
- SL：未到達
- TP1：未到達
- 判定：**継続**
- 追加買い：禁止

現物金は一時4110ドル前後、Reuters確認値では4104.59ドルまで上昇しました。先物と現物で基準が異なるため、採点はCOMEX先物系列を優先します。citeturn619744news34turn619744news38

### NASDAQ：`20260730_NASDAQ_SHORT_B-PULLBACK`

前回条件：

- Entry：28080～28250
- SL：28800
- TP1：27450
- TP2：26900

7月30日はNASDAQ現物が2.8%上昇し、Microsoftは約15.5～16%上昇しました。前日の半導体・AI株下落を大きく巻き戻しています。citeturn619252news66turn619252news68

NQ先物の正確な日中高値を十分に確認できていないため、SL到達は断定しません。ただし、前回の戻り売り仮説は大幅に弱まりました。

- Entry：約定の可能性あり
- MFE：限定的だった可能性
- MAE：大きく悪化
- SL：到達有無は `unverified`
- 判断：**前回売りシグナルを取消**
- 新規売り：禁止

方向が一日で反転したため、前回NASDAQ売りは「構造的弱さを一日延長して読んだ誤差」として後日採点します。

---

## 3. 市場全体の前提

### 判定：中立からリスクオン寄り。ただし金利面は逆風

株式は強く反発しましたが、内部構造は完全には健全ではありません。

- S&P500：7437.63、前日比+1.7%
- NASDAQ：24122.18、前日比+2.8%
- Microsoftの急騰が指数上昇を大きく牽引
- MetaはAI設備投資負担への懸念で下落
- 30年債利回りは約5.21～5.24%へ上昇
- GOLDは4100ドル台へ反発
- WTIは83ドル台へ小幅下落
- VIXは20.66から18.31付近へ低下 citeturn619252news66turn619252news67turn619252news68turn619252search6

つまり、

**株式決算はリスクオン、債券市場はインフレ・財政リスク警戒**

という分裂状態です。

S&P500の反発は広く確認できますが、金利上昇が続けば、長期デュレーション資産であるNASDAQには再び逆風となります。そのため、株価の急反発をそのまま新しい上昇トレンドと断定しません。

---

## 4. 10資産別判断

### GOLD

COMEX金先物は4100.10ドルで清算され、現物金も4100～4110ドル台へ上昇しました。ドル安、弱めのインフレ指標、将来の利上げ確率低下が支援材料です。citeturn619744news34turn619744news36

ただし、米超長期金利は上昇しています。金にとって、ドル安は追い風、長期実質金利上昇は逆風です。

**判断：B級押し目買い**

- 現在値追随は禁止
- 4060～4090への押しを待つ
- 既存仮想買いは継続
- 新規リスクは0.25%

### BTC

BTCは約64847ドル、日中高値65040ドル、安値63540ドルです。citeturn619252finance0

NASDAQの反発に連動していますが、65000ドルを明確に上抜けてはいません。ETFフローとCME basisの当日情報も十分に揃っていません。

MESは49と評価します。

**判断：NO_TRADE**

65000ドル上抜けだけでは買わず、終値定着とETFフロー改善を待ちます。

### ETH

ETHは約1624.95ドルです。価格更新の高値・安値情報は不足しています。citeturn619252finance1

BTCが株式反発に反応している一方、ETHには独自の相対強度が確認できません。

**判断：NO_TRADE**

### WTI

WTIは7月30日に約1%下落し、83.59ドル付近まで低下したと報じられています。中東情勢は不安定ですが、タンカー輸送が継続しており、現時点で深刻な供給途絶は確認されていません。citeturn619252news68turn619744news40

供給不安と実際の物流継続が衝突しています。

**判断：NO_TRADE**

- 買い：ショック追随になる
- 売り：ヘッドライン反転に弱い
- 82ドル割れまたは87ドル回復まで待つ

### USDJPY

Reutersは7月30日に円が急反発し、日本当局による介入観測が強まったと報じています。ドル自体も約0.8%下落しました。citeturn619744news34turn619744news38

直前まで円は40年来の安値圏にあり、値動きが政策・介入ヘッドラインに左右される状態です。

**判断：NO_TRADE**

- ドル円買い：介入リスク
- ドル円売り：米金利高止まりに逆行
- 価格の同時刻確認が弱いため `partially_verified`

### SPX

S&P500現物は7437.63で終了しました。ES先物の7月30日夜間値は7488.50付近が確認されていますが、セッションと限月差があるため参考値です。citeturn619252news67turn619744search15

Microsoft一社の寄与が大きく、米長期金利上昇も残ります。

**判断：NO_TRADE**

上昇を否定はしませんが、急反発翌日の買い追随はRRが悪いため見送ります。

### NASDAQ

NASDAQ現物は2.8%上昇しました。Microsoftの決算とAI関連投資への安心感が主因で、半導体指数も約8%上昇しました。一方、Metaは設備投資負担への懸念で下落しており、AI銘柄すべてが同方向ではありません。citeturn619252news66turn619252news68

前回の戻り売り構造は無効化します。

**判断：NO_TRADE**

買いへ反転するには、Microsoft主導だけでなく、半導体と市場全体の上昇継続をもう1営業日確認します。

### DXY

Reutersによればドルは7月30日に下落し、円高も進みました。弱めのインフレ指標と将来の利上げ確率低下がドルを圧迫しました。citeturn619744news34turn619744news38

一方、長期債利回りは高く、ドル安と金利高が同時に起きています。

**判断：NO_TRADE**

DXYの正確な当日終値が十分に確認できないため `partially_verified` とします。

### US10Y

FREDで確認できる最新確定値は7月29日の4.67%です。7月30日は超長期債利回りが大きく上昇し、30年債は5.21～5.24%付近へ達しました。citeturn619744search13turn619252news66turn619252news68

10年債も高止まりしていると推定できますが、7月30日の確定値は未更新です。

**判断：NO_TRADE**

4.70%超の定着はNASDAQ・GOLDに逆風、4.60%割れは支援材料として監視します。

### VIX

Cboe表示ではVIXは7月30日に20.66から18.31付近へ低下しました。別欄では17.09という夜間値も表示されており、時間帯差があります。citeturn619252search6

恐怖指数は低下しましたが、前日の株安を完全に否定するほど低くはありません。

**判断：NO_TRADE**

VIXの低下をそのまま売るのではなく、株式反発の持続性確認に使用します。

---

## 5. A級候補

**なし**

GOLDは方向性が機能していますが、

- CBS：74
- EMS：68
- expected_r：0.44
- MAE想定：0.28R

と評価し、A級条件の `CBS>=75`、`expected_r>=0.45`、`MAE<=0.25R` を満たしません。

NASDAQは反発が強いものの、一日だけのMicrosoft主導相場で、追随買いのMAE想定が高いためA級にはしません。

---

## 6. B級監視候補

### GOLD押し目買い

- signal_id：`20260731_GOLD_LONG_B-PULLBACK`
- 方向：BUY
- Entry：4060～4090
- SL：3970
- TP1：4190
- TP2：4275
- RR：1.26
- win_prob：0.61
- expected_r：0.44
- risk_pct：0.25
- MAE想定：0.28R
- 時間決済：5営業日
- ロット制約：SL幅が広いため通常想定の約半分
- 無効化：3970割れ、DXY急反発、US10Yが4.80%超
- A級昇格：4090以上で反発定着、CBS75以上、expected_r0.45以上、MAE0.25R以下

### NASDAQ押し目買い監視

今回はTSO_LOG上のB級シグナルにはしません。

昇格監視条件：

- NQが前日上昇分の半分以上を維持
- 半導体指数の上昇継続
- VIXが18以下を維持
- 米10年債利回りが4.70%を超えない
- Microsoft以外にも上昇が拡大

条件が揃わないため、現段階ではNO_TRADEです。

---

## 7. 触らない資産

- **BTC**：65000ドル上抜け未確定、MES49
- **ETH**：独自の相対強度不足
- **WTI**：地政学ヘッドライン依存
- **USDJPY**：介入リスクと米金利高が衝突
- **SPX**：急反発翌日で追随RRが悪い
- **NASDAQ**：前回売りは取消だが、買い転換確認も一日不足
- **DXY**：ドル安と長期金利高の不整合
- **US10Y**：最新確定値の更新待ち
- **VIX**：急低下後で方向優位なし

---

## 8. 後日検証ポイント

1. GOLDが4060～4090へ押して反発するか
2. 前回GOLD買いがTP1の4140へ到達するか
3. NASDAQが前日の上昇を半分以上維持できるか
4. Microsoft以外へ買いが拡大するか
5. BTCが65000ドルを終値で超えるか
6. WTIが82ドルを割るか、87ドルを超えるか
7. US10Yが4.70%を維持するか
8. VIXが18以下へ定着するか
9. USDJPYの円高が実介入によるものか、ポジション解消か
10. DXY下落と長期金利上昇の不整合が解消するか

---

## 9. Obsidian保存用Observation Draft

```markdown
# 2026-07-31 Microsoft主導の急反発と長期金利上昇の併存

Type: 一般市場Observation

## Summary

7月30日の米国株はMicrosoftの好決算を受けて急反発し、S&P500は1.7%、NASDAQは2.8%上昇した。
一方、米超長期債利回りは2007年以来の高水準へ上昇し、金融環境が全面的に改善したわけではない。
GOLDは4100.10ドルへ上昇し、前回のB級買いは利益方向に進んだ。
NASDAQの前回戻り売り仮説は急反発によって弱まり、取消とする。

## Observation

- S&P500は7437.63。
- NASDAQは24122.18。
- Microsoftは約15.5～16%上昇。
- 半導体指数は約8%上昇。
- 30年債利回りは約5.21～5.24%。
- COMEX金先物は4100.10ドル。
- WTIは約83.59ドル。
- BTCは約64847ドル。
- ETHは約1624.95ドル。
- VIXは20.66から18.31付近へ低下。
- ドルは下落し、円は急反発した。

## Evaluation

A級候補なし。
GOLDをB級押し目買い監視とする。
NASDAQ売りは取消とし、買いへの転換にはもう1営業日の確認を必要とする。
BTCはMES49でNO_TRADE。
WTI、USDJPYはヘッドラインリスクが大きくNO_TRADE。

## Interpretation

株式の反発は強いが、Microsoft一社の寄与が大きく、債券市場はインフレ・財政リスクを警戒している。
株高と長期金利上昇が長く併存する場合、NASDAQの上昇持続性は低下する。
GOLDはドル安に支えられているが、長期金利上昇との綱引きが続く。

## Later Review

- GOLD4060～4090と4140
- NASDAQ反発維持
- 半導体市場の広がり
- BTC65000
- WTI82・87
- US10Y4.70
- VIX18
- USDJPY介入確認

## Tags

#TSO #MarketObservation #GOLD #NASDAQ #Microsoft #US10Y #VIX #WTI
```

---

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-07-31,20260731_GOLD_LONG_B-PULLBACK,GOLD,BUY,B,PULLBACK,4060,4090,3970,4190,4275,1.26,0.61,0.44,72,70,31,0.25,BULLISH_CONFLICTED,68,64,67,70,74,65,3970_break_or_DXY_rebound_or_US10Y_above_4.80,5d_close_MFE_MAE_4140_and_yield,verified
2026-07-31,20260731_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,59,55,73,,NEUTRAL_REBOUND,58,48,52,56,61,49,mes_below_50_and_65000_not_confirmed,BTC_65000_ETF_flow_CME_basis_and_5d_close,verified
2026-07-31,20260731_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,46,42,80,,WEAK_NEUTRAL,50,43,46,48,52,42,no_independent_relative_strength,ETH_BTC_ratio_and_5d_close,partially_verified
2026-07-31,20260731_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,70,43,84,,GEOPOLITICAL_VOLATILE,66,62,76,54,63,67,headline_risk_and_no_supply_confirmation,WTI_82_or_87_break_and_5d_close,partially_verified
2026-07-31,20260731_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,64,45,87,,INTERVENTION_VOLATILE,63,58,67,44,59,57,intervention_uncertainty_and_US_yield_support,intervention_confirmation_USDJPY_range_and_5d_close,partially_verified
2026-07-31,20260731_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,74,58,67,,EARNINGS_REBOUND_HIGH_YIELD,69,61,66,68,71,62,one_day_rebound_and_long_yield_risk,ES_rebound_retention_breadth_and_5d_close,verified
2026-07-31,20260731_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,82,62,69,,AI_EARNINGS_REBOUND,74,58,68,72,73,63,Microsoft_concentration_and_yield_risk,NQ_rebound_retention_SOXX_breadth_and_5d_close,partially_verified
2026-07-31,20260731_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,56,48,75,,DOLLAR_DOWN_YIELDS_UP,62,59,54,51,57,56,dollar_yield_divergence,DXY_level_US10Y_correlation_and_5d_close,partially_verified
2026-07-31,20260731_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,69,52,76,,HIGH_YIELD_TERM_PREMIUM,67,66,65,56,63,65,latest_confirmed_value_lag_and_long_end_selloff,US10Y_4.60_or_4.75_break_and_5d_close,partially_verified
2026-07-31,20260731_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,64,47,72,,VOLATILITY_NORMALIZING,61,55,68,65,64,57,post_rebound_volatility_compression,VIX_18_hold_or_20_recovery_and_5d_close,verified
```

## TSO_LOG JSON

```json
[
  {
    "date":"2026-07-31",
    "signal_id":"20260731_GOLD_LONG_B-PULLBACK",
    "asset":"GOLD",
    "side":"BUY",
    "rank":"B",
    "type":"PULLBACK",
    "entry_low":4060,
    "entry_high":4090,
    "sl":3970,
    "tp1":4190,
    "tp2":4275,
    "rr":1.26,
    "win_prob":0.61,
    "expected_r":0.44,
    "tq_score":72,
    "opp_score":70,
    "no_trade_score":31,
    "risk_pct":0.25,
    "regime":"BULLISH_CONFLICTED",
    "ems":68,
    "ffs":64,
    "cds":67,
    "ias":70,
    "cbs":74,
    "mes":65,
    "invalidation":"3970_break_or_DXY_rebound_or_US10Y_above_4.80",
    "verification_target":"5d_close_MFE_MAE_4140_and_yield",
    "verified_status":"verified"
  },
  {
    "date":"2026-07-31",
    "signal_id":"20260731_BTC_NONE_NO_TRADE",
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
    "tq_score":59,
    "opp_score":55,
    "no_trade_score":73,
    "risk_pct":null,
    "regime":"NEUTRAL_REBOUND",
    "ems":58,
    "ffs":48,
    "cds":52,
    "ias":56,
    "cbs":61,
    "mes":49,
    "invalidation":"mes_below_50_and_65000_not_confirmed",
    "verification_target":"BTC_65000_ETF_flow_CME_basis_and_5d_close",
    "verified_status":"verified"
  },
  {
    "date":"2026-07-31",
    "signal_id":"20260731_ETH_NONE_NO_TRADE",
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
    "tq_score":46,
    "opp_score":42,
    "no_trade_score":80,
    "risk_pct":null,
    "regime":"WEAK_NEUTRAL",
    "ems":50,
    "ffs":43,
    "cds":46,
    "ias":48,
    "cbs":52,
    "mes":42,
    "invalidation":"no_independent_relative_strength",
    "verification_target":"ETH_BTC_ratio_and_5d_close",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-07-31",
    "signal_id":"20260731_WTI_NONE_NO_TRADE",
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
    "tq_score":70,
    "opp_score":43,
    "no_trade_score":84,
    "risk_pct":null,
    "regime":"GEOPOLITICAL_VOLATILE",
    "ems":66,
    "ffs":62,
    "cds":76,
    "ias":54,
    "cbs":63,
    "mes":67,
    "invalidation":"headline_risk_and_no_supply_confirmation",
    "verification_target":"WTI_82_or_87_break_and_5d_close",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-07-31",
    "signal_id":"20260731_USDJPY_NONE_NO_TRADE",
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
    "tq_score":64,
    "opp_score":45,
    "no_trade_score":87,
    "risk_pct":null,
    "regime":"INTERVENTION_VOLATILE",
    "ems":63,
    "ffs":58,
    "cds":67,
    "ias":44,
    "cbs":59,
    "mes":57,
    "invalidation":"intervention_uncertainty_and_US_yield_support",
    "verification_target":"intervention_confirmation_USDJPY_range_and_5d_close",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-07-31",
    "signal_id":"20260731_SPX_NONE_NO_TRADE",
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
    "tq_score":74,
    "opp_score":58,
    "no_trade_score":67,
    "risk_pct":null,
    "regime":"EARNINGS_REBOUND_HIGH_YIELD",
    "ems":69,
    "ffs":61,
    "cds":66,
    "ias":68,
    "cbs":71,
    "mes":62,
    "invalidation":"one_day_rebound_and_long_yield_risk",
    "verification_target":"ES_rebound_retention_breadth_and_5d_close",
    "verified_status":"verified"
  },
  {
    "date":"2026-07-31",
    "signal_id":"20260731_NASDAQ_NONE_NO_TRADE",
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
    "tq_score":82,
    "opp_score":62,
    "no_trade_score":69,
    "risk_pct":null,
    "regime":"AI_EARNINGS_REBOUND",
    "ems":74,
    "ffs":58,
    "cds":68,
    "ias":72,
    "cbs":73,
    "mes":63,
    "invalidation":"Microsoft_concentration_and_yield_risk",
    "verification_target":"NQ_rebound_retention_SOXX_breadth_and_5d_close",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-07-31",
    "signal_id":"20260731_DXY_NONE_NO_TRADE",
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
    "tq_score":56,
    "opp_score":48,
    "no_trade_score":75,
    "risk_pct":null,
    "regime":"DOLLAR_DOWN_YIELDS_UP",
    "ems":62,
    "ffs":59,
    "cds":54,
    "ias":51,
    "cbs":57,
    "mes":56,
    "invalidation":"dollar_yield_divergence",
    "verification_target":"DXY_level_US10Y_correlation_and_5d_close",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-07-31",
    "signal_id":"20260731_US10Y_NONE_NO_TRADE",
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
    "tq_score":69,
    "opp_score":52,
    "no_trade_score":76,
    "risk_pct":null,
    "regime":"HIGH_YIELD_TERM_PREMIUM",
    "ems":67,
    "ffs":66,
    "cds":65,
    "ias":56,
    "cbs":63,
    "mes":65,
    "invalidation":"latest_confirmed_value_lag_and_long_end_selloff",
    "verification_target":"US10Y_4.60_or_4.75_break_and_5d_close",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-07-31",
    "signal_id":"20260731_VIX_NONE_NO_TRADE",
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
    "tq_score":64,
    "opp_score":47,
    "no_trade_score":72,
    "risk_pct":null,
    "regime":"VOLATILITY_NORMALIZING",
    "ems":61,
    "ffs":55,
    "cds":68,
    "ias":65,
    "cbs":64,
    "mes":57,
    "invalidation":"post_rebound_volatility_compression",
    "verification_target":"VIX_18_hold_or_20_recovery_and_5d_close",
    "verified_status":"verified"
  }
]
```
