<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-19 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-21T12:59:52Z / chars: 20434 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-09-19

**使用モデル：GPT-5.6 Sol**  
**本日の市場の主役：USDJPY**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**データ基準：2026年9月18日米国市場終了後。土曜日のため、FX・先物・株式は金曜終値／最終遅延値、Cryptoのみ週末取引継続。**  
**crypto_grounds: etf=有, cme=有** — BTC ETFの最新確定値は9月17日の約+159.5Mドル。9月18日分は07:00 JST時点で確定確認できず。CME BTC/ETHは9月18日データを確認。citeturn708243search0turn772773search0turn772773search1  
**expected_r_basis: subjective** — 新規USDJPY BUYの二点分布EVは約+0.66Rですが、為替介入リスク、rate check、週末ギャップ、Entry未到達確率を織り込み`expected_r=0.43`へ下方調整します。

**invalidation_check: 20260917_WTI_BUY_PULLBACK=not_fired, 20260919_USDJPY_BUY_PULLBACK=not_fired**

`20260912_BTC_SELL_PULLBACK`は9月18日に最終的に**fired**となったため、本日から未決着リストから除外します。詳細は後述します。

---

## 1. 本日の結論

**新規A級：0件**  
**新規B級：1件 — USDJPY BUY_PULLBACK**  
**B+観察候補：USDJPY BUY_PULLBACK**  
**既存ポジション：WTI BUYをHOLD**  
**その他8資産：NO_TRADE**

今日最大の変化はBOJです。

BOJは政策金利を**1.00%→1.25%**へ引き上げましたが、決定は7対2。さらに市場が期待していたほど次回利上げへの強いガイダンスが出ず、円は逆に売られました。USDJPYは一時**158.05**まで上昇。その後、日本当局によるrate check報道を受けて上昇幅を縮め、Reuters最終付近では約**156.73**でした。citeturn713953view0turn615919search2

これは昨日設定した検証条件、

**「BOJが1.25%へ利上げしてもUSDJPY >156.50なら、新しいUSDJPY BUY仮説を検討」**

が実際に成立した形です。

ただし158円を追いかけて買うのではありません。

新規シグナルは、

**20260919_USDJPY_BUY_PULLBACK**

Entry：**156.00–156.50**  
SL：**155.20**  
TP1：**158.20**  
TP2：**159.60**  
RR：**1.86**  
win_prob：**0.58**  
expected_r：**0.43**  
risk_pct：**0.25%**

です。

標準的なXM Standard口座で0.01lot=1,000USDという前提なら、Entry中点156.25→SL155.20の損失は概算**約1,050円＋スプレッド/滑り**で、3,000円制約内です。XM Standardの最小0.01lot・1lot=100,000通貨という仕様とも整合します。citeturn620212search0

したがって**B+観察候補**とします。

ただし今日は土曜なので、実際のFX新規執行はありません。月曜に156.00–156.50へ戻った場合のみ候補で、**157円台後半を成行追いするシグナルではありません。**

---

## 2. 前回判断の簡易検証

### `20260912_BTC_SELL_PULLBACK`

最終結果を更新します。

既存条件は、

**Entry 79200–79800**  
**SL / invalidation 80850**  
**TP1 76450**  
**TP2 74800**

でした。

9月15日のCME BTCは安値**74925**まで低下しているため、

**Entry到達 → TP1到達 → TP2は125ドル届かず**

でした。citeturn772773search0

しかし9月18日に相場が完全反転しました。

CME BTCは、

**Open 76397  
High 81545  
Low 76247  
Close 約81320**

まで上昇。80850を明確に突破しています。ReutersでもBitcoin現物は約**+5.9%、81,000ドル**と報じられています。citeturn772773search0turn351485news26

したがって最終評価は、

**ENTRY_REACHED  
→ TP1_REACHED  
→ TP2_NOT_REACHED  
→ FINAL_DAY_INVALIDATION_FIRED**

です。

これはかなり有用な教師データです。

単純な「SELL失敗」ではありません。

**方向は最初に正しく、約3,000ドル下落してTP1へ到達。その後、最終日に価格構造が反転してinvalidationが発動した**

というケースです。

今回のinvalidation設計はかなり意味があります。TP2まで固執していた場合、利益がほぼ全て戻る経路でした。

本日からこのsignal_idは`invalidation_check`対象外です。

---

### `20260917_WTI_BUY_PULLBACK`

ユーザー実取引：

**Entry：約101.19**  
**SL：98.90**  
**TP：105.20**

9月18日のWTIは**100.30ドル**で清算、前日比-1.58%。中国がイランへフーシ派によるサウジ攻撃抑制を働きかけたとの報道が供給プレミアムを削りました。citeturn713953view1

一方で、

**Hormuz通過commodity vessels：4隻  
10日平均：約16隻**

と物流は正常化していません。

Saudi East-West Pipelineも3つのポンプ施設が損傷し、修理時期は依然不透明。Saudi Aramcoが一部欧州顧客への10月供給を停止したとの報道もあります。citeturn713953view1

つまり、

**価格はBUYに不利**
ですが、
**根本の供給制約はまだ消えていない**

状態です。

金曜安値も報道ベースでは約99.4ドルで、SL98.90には到達していません。citeturn265953news54

したがって、

**ENTRY_FILLED / SL_NOT_REACHED / TP_NOT_REACHED / invalidation=not_fired**

です。

現状の主観勝率は、発行時0.61から**約0.51～0.54**まで低下させます。

**HOLD。ただし追加BUYは禁止。SL98.90も広げません。**

---

## 3. 市場全体の前提

今の市場はかなり特殊です。

**中央銀行：タカ派**  
**US10Y：約5%**  
**WTI：100ドル超**  
なのに、  
**NASDAQ・Crypto・Goldがかなり強い**

という構造になっています。

米10年債利回りは9月18日に**4.995%付近**まで戻りました。それでもS&P500は+0.17%、Nasdaq Compositeは+0.40%。VIXは**14.81**まで低下しています。citeturn707341news19turn718920search0

つまり市場は、

**金利5% = 自動的にrisk-off**

ではなくなっています。

特にGrowth/Cryptoの耐性がかなり強い。

NQZ26はデータ提供元間で終盤値に若干差がありますが、約**29,700前後**。9月15日の29,100台から大きく回復しています。citeturn138736search0turn265953search7

Bitcoinはさらに顕著で、CMEが約81.3k、Reuters現物が約81k。ETFフローも9月15・16日の大幅流出から9月17日に+159.5Mドルへ反転しました。citeturn708243search0turn772773search0turn351485news26

Goldも強いです。

GCZ26は複数ソースで約**4420～4425ドル**、Reutersの米金先物清算値は**4424.90ドル**。米金利5%・ドル指数100超にもかかわらず上昇しています。citeturn701097search2turn351485news24

したがって今日の総合regimeは、

**MIXED。ただしリスク資産内部にはRISK_ONがかなり残っている**

とします。

urlReuters：BOJ後のドル円とrate checkturn713953view0  
urlReuters：9月18日のWTI市場turn713953view1  
urlReuters：9月18日の米株市場turn713953view2  
urlReuters：9月18日のGold市場turn713953view4

---

## 4. 10資産別判断

| 資産 | 本日判断 | 評価 |
|---|---|---|
| **GOLD** | **NO_TRADE** | GCZ26約4425。金利5%でも強いが4439付近まで上昇済み。追わない |
| **BTC** | **NO_TRADE** | 現物約81k、CME約81.3k。旧SELLはfired。ただし+6%後を追わない |
| **ETH** | **NO_TRADE** | CME約2612、現物も2600付近まで回復。1日で急伸したため追わない |
| **WTI** | **既存BUY HOLD / 新規NO_TRADE** | 100.30。供給正常化は未完、ただし仮説確信度低下 |
| **USDJPY** | **B BUY_PULLBACK / B+観察** | BOJ後の円売りを押し目で取る |
| **SPX** | **NO_TRADE** | ESZ26約7700前後。金利上昇と低VIXが拮抗 |
| **NASDAQ** | **NO_TRADE** | NQZ26約29700。強いが戻り後を追わない |
| **DXY** | **NO_TRADE** | 約100.4。強いがUSDJPYの方がテーマが明瞭 |
| **US10Y** | **NO_TRADE** | 約4.995%。5%付近の双方向リスク大 |
| **VIX** | **NO_TRADE** | 14.81。risk-onだが既に低下済み |

ETHはCME先物で9月18日に**約2612.5、+6.6%**まで上昇しています。citeturn772773search1

VIX 14.81はCboe由来データとも整合しています。citeturn718920search0turn718920search1

---

## 5. A級候補

**なし。**

最もAに近いのはUSDJPY BUYです。

数値条件は、

**CBS 84**  
**EMS 78**  
**RR 1.86**  
**win_prob 0.58**

と十分です。

二点分布なら、

\[
0.58\times1.86-0.42\approx+0.66R
\]

あります。

それでもAにしない最大理由が**介入リスク**です。

日本当局は金曜にrate checkを実施したと報じられています。これは実際の市場介入に先行することがある行動です。USDJPYも158.05から156円台へ押し戻されました。citeturn713953view0

したがって想定MAEを**約0.28R**と見積もり、A条件の`<=0.25R`を外します。

さらに週末ギャップもあります。

よって**B+止まり**です。

---

## 6. B級監視候補

### `20260919_USDJPY_BUY_PULLBACK` — B / B+

**Entry：156.00–156.50**  
**中点：156.25**  
**SL：155.20**  
**TP1：158.20**  
**TP2：159.60**

RR：

\[
(158.20-156.25)/(156.25-155.20)
=1.86
\]

**win_prob：0.58**  
**expected_r：0.43**  
**risk_pct：0.25%**

根拠は3つです。

第一に、Fedは利上げ＋追加利上げ方向。

第二に、BOJ自身も利上げしたにもかかわらず、**円が買われなかった**。

第三に、7対2の反対票と明確な次回利上げ時期の欠如を市場が相対的にdovishと解釈しました。ReutersによるとUSDJPYは158.05まで上昇しています。citeturn713953view0turn615919search2

これはかなり強い価格反応です。

ただし、158円で買うのではなく、

**156.0–156.5まで押しても155.2を割らない**

ことを確認して参加します。

**157.20以上で始まった場合は成行追い禁止。**

また、

**実際の為替介入が確認された場合**
または
**155.20を明確に割った場合**

はinvalidationです。

XM Standardの0.01lotなら、概算SL損失は約1,050円なので、3,000円実損制約も満たします。citeturn620212search0

なお現在WTIで0.25%リスクが残っているため、USDJPYを実際に約定させれば、

**WTI 0.25% + USDJPY 0.25% = 0.50%**

で現在の日次/ポートフォリオ上限に到達します。

したがってその場合、他の新規シグナルには参加しません。

---

## 7. 触らない資産

特に**BTC、ETH、NASDAQ**を追いかけません。

BTCは約76kから81kへ1日で約6%上昇。CME高値も81,545です。citeturn772773search0

方向だけなら、昨日までのSELLから明確に**上方向へ評価を変更**します。

しかし、

**「上方向へ評価変更」≠「今から81kで買う」**

です。

これはTSOでこれまで利益につながっている部分そのものです。

次にBTCを見るなら、

**79.0～79.8kへ押して維持**
または
**82.3k前後を突破→押し目形成**

を待ちます。

ETHも同じで、CMEが一日で約+6.6%。今からBUYするとmomentum追随です。citeturn772773search1

NASDAQも強さ自体は評価しますが、NQは既に29,700付近まで戻しています。金利5%という逆風も残るため、今日はBUYシグナルを出しません。

---

## 8. 後日検証ポイント

### USDJPY

最重要です。

**156.00–156.50へ押して反発**
なら、本日BシグナルのEntry成立。

**158.20**
ならTP1。

**159.60**
ならTP2。

一方、

**155.20割れ**
または
**実際の円買い介入**

なら即`fired`です。

また、158円を再突破しても成行で追いません。

---

### WTI

現状100.30。

**98.90 → SL / fired**

です。

ただしSL前でも、

**East-West Pipeline半分以上復旧確認**
＋
**Hormuz通過船が10～15隻程度へ継続回復**

となれば、物理供給仮説のinvalidation候補です。

現時点ではHormuzは4隻対10日平均16隻なので、まだそこまで正常化していません。citeturn713953view1

逆に、

**WTI >102.5～103**
＋
供給障害継続

なら、今回の100ドル近辺が押し目だった可能性が高まります。

TP105.20は維持します。

---

### BTC

今回の大反転は重要です。

9月12日SELLは、

**79k台SELL**
→
**74.9k**
→
**81.5k**

というかなり大きな往復になりました。

今後、

**82.3k前後を突破・維持**
＋
**ETFフローがプラス継続**
＋
**CMEも80k超維持**

なら、新しいBTC BUY仮説候補です。

反対に79kを再び割るなら、今回の上昇がshort squeeze中心だった可能性を再検討します。

---

### NASDAQ

ここも重要。

**US10Y ≈5%なのにNQ >29600を維持**

していること自体が強いです。

来週、

**NQ >30000**
＋
**VIX <16**

なら、金利高耐性がかなり強いと評価します。

逆に、

**NQ <29400**
＋
**US10Y >5.05**

ならrisk-on評価を撤回します。

---

### GOLD

GCZ26は4420～4425。

**4440～4450を明確に突破**
すれば、金利高にもかかわらずGold BUYが成立する非常に強い価格反応になります。

逆に4370割れなら、現在の反発はshort-covering中心だった可能性が高まります。

---

## 9. Obsidian保存用 Observation Draft

```markdown
# 2026-09-19 BOJ Disappointment / USDJPY Repricing / BTC Reversal

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

Risk assets:
RISK_ON pockets

Rates:
still restrictive

Oil:
EVENT / physical disruption not resolved

## BOJ

Rate:
1.00 -> 1.25%

Vote:
7-2

Key surprise:
two dissenters
no sufficiently hawkish near-term guidance

USDJPY:
high 158.05
late ~156.73

Japan:
rate check reported

Interpretation:
BOJ hike failed to strengthen JPY.

Previous test:
USDJPY >156.50 after hike

Result:
TRIGGERED

## New signal

20260919_USDJPY_BUY_PULLBACK

Rank:
B

B+ observation:
YES

Entry:
156.00-156.50

Mid:
156.25

SL:
155.20

TP1:
158.20

TP2:
159.60

RR:
1.86

win_prob:
0.58

raw two-point EV:
~0.66R

subjective expected_r:
0.43R

Adjustment:
intervention risk
rate-check signal
weekend gap
unfilled probability

MAE estimate:
0.28R

Risk:
0.25%

Approx XM Standard 0.01-lot SL loss:
~JPY1050 + spread/slippage

Do not chase above:
157.20

Invalidation:
USDJPY <155.20
OR confirmed FX intervention
OR clear BOJ hawkish repricing

## WTI existing trade

20260917_WTI_BUY_PULLBACK

User actual:
Entry ~101.19
SL 98.90
TP 105.20

Sep18 settle:
100.30

Status:
HOLD

Current subjective win probability:
~0.51-0.54

Physical market:
Hormuz vessels 4
10d avg ~16

East-West pipeline:
three pumping stations damaged
repair timeline uncertain

China-Iran diplomatic effort:
bearish oil premium

invalidation:
not_fired

Do not add.
Do not widen SL.

## BTC previous signal final

20260912_BTC_SELL_PULLBACK

Entry:
79200-79800

TP1:
76450 reached

TP2:
74800

CME Sep15 low:
74925

Sep18 CME:
high 81545
close ~81320

SL / invalidation:
80850

Final:
TP1_REACHED
TP2_NOT_REACHED
FINAL_DAY_INVALIDATION_FIRED

Interpretation:
initial direction correct
late reversal correctly detected by invalidation

Remove from active list.

## Crypto

BTC spot:
~81000

CME BTC:
~81320

Latest completed BTC ETF flow:
Sep17 +159.5m

Sep18 ETF:
not finalized at report time

ETH:
~2600

CME ETH:
~2612.5

Do not chase either asset after ~6% daily move.

## Markets

WTI:
100.30

GCZ26:
~4425

USDJPY:
~156.7

DXY:
~100.4

US10Y:
~4.995%

NQZ26:
~29700

ESZ26:
~7700

VIX:
14.81

## Active invalidation

20260917_WTI_BUY_PULLBACK=not_fired
20260919_USDJPY_BUY_PULLBACK=not_fired

## New signals

A:
NONE

B:
USDJPY BUY_PULLBACK

B+:
USDJPY BUY_PULLBACK

Existing:
WTI BUY active

#TSO #USDJPY #BOJ #WTI #BTC #NASDAQ #GOLD
```

---

# 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-19,20260919_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,86,74,,MIXED,82,86,94,84,84,78,wait_for_GCZ26_break_4450_or_failure_below_4370_before_new_signal,GCZ26_4370_4425_4450_DXY_US10Y_1d_3d,verified
2026-09-19,20260919_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,92,90,,RISK_ON,88,89,97,90,91,82,do_not_chase_after_6pct_move_wait_79k_retest_or_82.3k_break_confirmation,BTC_79000_79800_81000_82300_ETF_CME_1d_3d,partially_verified
2026-09-19,20260919_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,85,86,,RISK_ON,80,86,94,85,83,72,do_not_chase_after_large_daily_move_wait_for_retest_or_new_CME_ETF_confirmation,ETH_2500_2570_2610_2700_ETF_CME_1d_3d,partially_verified
2026-09-19,20260919_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,88,94,,EVENT,82,94,95,84,84,90,manage_existing_20260917_BUY_SL98.90_TP105.20_no_add,WTI_98.90_100.30_101.19_103_105.20_Hormuz_pipeline_1d_3d,verified
2026-09-19,20260919_USDJPY_BUY_PULLBACK,USDJPY,BUY,B,PULLBACK,156.00,156.50,155.20,158.20,159.60,1.86,0.58,0.43,99,92,48,0.25,EVENT,78,95,98,91,84,94,USDJPY_below_155.20_or_confirmed_MOF_intervention_or_clear_BOJ_hawkish_repricing,USDJPY_155.20_156.25_158.20_159.60_DXY_US10Y_MOF_1d_3d_5d,verified
2026-09-19,20260919_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,80,78,,MIXED,70,82,93,79,78,82,wait_for_ESZ26_pullback_or_clean_break_with_US10Y_confirmation,ESZ26_7650_7700_7750_US10Y_VIX_1d_3d,partially_verified
2026-09-19,20260919_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,89,73,,MIXED,76,86,95,88,86,86,wait_for_NQ_pullback_or_break_30000_without_chasing,NQZ26_29400_29600_29700_30000_US10Y_VIX_1d_3d,partially_verified
2026-09-19,20260919_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,86,82,,EVENT,82,92,96,83,84,92,prefer_USDJPY_expression_wait_for_DXY_hold_above_100_or_failure_below_99.7,DXY_99.7_100.4_101_USDJPY_US10Y_1d_3d,partially_verified
2026-09-19,20260919_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,89,87,,MIXED,90,94,98,88,90,96,wait_for_sustained_break_above_5.05_or_rejection_below_4.90,US10Y_4.90_4.995_5.05_GOLD_NQ_DXY_1d_3d,verified
2026-09-19,20260919_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,78,87,,RISK_ON,68,84,94,74,76,80,wait_for_VIX_reclaim_16.5_or_hold_below_15_with_equity_confirmation,VIX_14.81_15_16.5_ES_NQ_1d_3d,verified
```

### TSO_LOG JSON

```json
[
  {
    "date":"2026-09-19",
    "signal_id":"20260919_GOLD_NONE_NO_TRADE",
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
    "no_trade_score":74,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":82,
    "ffs":86,
    "cds":94,
    "ias":84,
    "cbs":84,
    "mes":78,
    "invalidation":"wait_for_GCZ26_break_4450_or_failure_below_4370_before_new_signal",
    "verification_target":"GCZ26_4370_4425_4450_DXY_US10Y_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-19",
    "signal_id":"20260919_BTC_NONE_NO_TRADE",
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
    "opp_score":92,
    "no_trade_score":90,
    "risk_pct":null,
    "regime":"RISK_ON",
    "ems":88,
    "ffs":89,
    "cds":97,
    "ias":90,
    "cbs":91,
    "mes":82,
    "invalidation":"do_not_chase_after_6pct_move_wait_79k_retest_or_82.3k_break_confirmation",
    "verification_target":"BTC_79000_79800_81000_82300_ETF_CME_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-09-19",
    "signal_id":"20260919_ETH_NONE_NO_TRADE",
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
    "no_trade_score":86,
    "risk_pct":null,
    "regime":"RISK_ON",
    "ems":80,
    "ffs":86,
    "cds":94,
    "ias":85,
    "cbs":83,
    "mes":72,
    "invalidation":"do_not_chase_after_large_daily_move_wait_for_retest_or_new_CME_ETF_confirmation",
    "verification_target":"ETH_2500_2570_2610_2700_ETF_CME_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-09-19",
    "signal_id":"20260919_WTI_NONE_NO_TRADE",
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
    "opp_score":88,
    "no_trade_score":94,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":82,
    "ffs":94,
    "cds":95,
    "ias":84,
    "cbs":84,
    "mes":90,
    "invalidation":"manage_existing_20260917_BUY_SL98.90_TP105.20_no_add",
    "verification_target":"WTI_98.90_100.30_101.19_103_105.20_Hormuz_pipeline_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-19",
    "signal_id":"20260919_USDJPY_BUY_PULLBACK",
    "asset":"USDJPY",
    "side":"BUY",
    "rank":"B",
    "type":"PULLBACK",
    "entry_low":156.00,
    "entry_high":156.50,
    "sl":155.20,
    "tp1":158.20,
    "tp2":159.60,
    "rr":1.86,
    "win_prob":0.58,
    "expected_r":0.43,
    "tq_score":99,
    "opp_score":92,
    "no_trade_score":48,
    "risk_pct":0.25,
    "regime":"EVENT",
    "ems":78,
    "ffs":95,
    "cds":98,
    "ias":91,
    "cbs":84,
    "mes":94,
    "invalidation":"USDJPY_below_155.20_or_confirmed_MOF_intervention_or_clear_BOJ_hawkish_repricing",
    "verification_target":"USDJPY_155.20_156.25_158.20_159.60_DXY_US10Y_MOF_1d_3d_5d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-19",
    "signal_id":"20260919_SPX_NONE_NO_TRADE",
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
    "tq_score":98,
    "opp_score":80,
    "no_trade_score":78,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":70,
    "ffs":82,
    "cds":93,
    "ias":79,
    "cbs":78,
    "mes":82,
    "invalidation":"wait_for_ESZ26_pullback_or_clean_break_with_US10Y_confirmation",
    "verification_target":"ESZ26_7650_7700_7750_US10Y_VIX_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-09-19",
    "signal_id":"20260919_NASDAQ_NONE_NO_TRADE",
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
    "opp_score":89,
    "no_trade_score":73,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":76,
    "ffs":86,
    "cds":95,
    "ias":88,
    "cbs":86,
    "mes":86,
    "invalidation":"wait_for_NQ_pullback_or_break_30000_without_chasing",
    "verification_target":"NQZ26_29400_29600_29700_30000_US10Y_VIX_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-09-19",
    "signal_id":"20260919_DXY_NONE_NO_TRADE",
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
    "opp_score":86,
    "no_trade_score":82,
    "risk_pct":null,
    "regime":"EVENT",
    "ems":82,
    "ffs":92,
    "cds":96,
    "ias":83,
    "cbs":84,
    "mes":92,
    "invalidation":"prefer_USDJPY_expression_wait_for_DXY_hold_above_100_or_failure_below_99.7",
    "verification_target":"DXY_99.7_100.4_101_USDJPY_US10Y_1d_3d",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-09-19",
    "signal_id":"20260919_US10Y_NONE_NO_TRADE",
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
    "opp_score":89,
    "no_trade_score":87,
    "risk_pct":null,
    "regime":"MIXED",
    "ems":90,
    "ffs":94,
    "cds":98,
    "ias":88,
    "cbs":90,
    "mes":96,
    "invalidation":"wait_for_sustained_break_above_5.05_or_rejection_below_4.90",
    "verification_target":"US10Y_4.90_4.995_5.05_GOLD_NQ_DXY_1d_3d",
    "verified_status":"verified"
  },
  {
    "date":"2026-09-19",
    "signal_id":"20260919_VIX_NONE_NO_TRADE",
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
    "opp_score":78,
    "no_trade_score":87,
    "risk_pct":null,
    "regime":"RISK_ON",
    "ems":68,
    "ffs":84,
    "cds":94,
    "ias":74,
    "cbs":76,
    "mes":80,
    "invalidation":"wait_for_VIX_reclaim_16.5_or_hold_below_15_with_equity_confirmation",
    "verification_target":"VIX_14.81_15_16.5_ES_NQ_1d_3d",
    "verified_status":"verified"
  }
]
```

今日の核心は2点です。

**USDJPYでは、昨日設定した「BOJ利上げ後でも156.50超ならBUY仮説」という検証条件が実際に成立しました。** ただしrate checkまで出ているので、158円を追わず156.00–156.50だけを狙うB+です。

もう一つはBTCです。`20260912_BTC_SELL_PULLBACK`は**TP1まで正しく取った後、最終日に80850を上抜いてinvalidation fired**となりました。これは「SLまで固執せず、シナリオ反転を検出する」という現在のTSO設計を検証する上でかなり価値のあるサンプルです。

WTIは100.30まで下がりましたが、HormuzとSaudi pipelineの物理制約がまだ正常化していないため、**101.19 BUY / SL98.90 / TP105.20はHOLD**とします。追加はしません。
