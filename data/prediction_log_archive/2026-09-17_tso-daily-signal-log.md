<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-09-17 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-09-21T12:59:52Z / chars: 16201 / 値は無修正 -->

# TSO Daily Signal Log v2 — 2026-09-17

**使用モデル：GPT-5.6 Sol**  
**本日の市場の主役：USDJPY**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**crypto_grounds: etf=有, cme=有**  
**expected_r_basis: subjective** — 本日の唯一の方向あり判断WTI BUYでは、二点分布の素の期待値約+0.67Rから、未約定確率・供給正常化ヘッドライン・5営業日時間決済を織り込み、`expected_r=0.48`まで引き下げています。

**invalidation_check: 20260912_BTC_SELL_PULLBACK=not_fired**

9月16日のFOMCではFedが25bp利上げし、政策金利を**3.75–4.00%**へ引き上げました。18人中16人が年内少なくとももう1回の利上げを見込んでいます。米10年債は約**5.00%**、DXYは**100.31**、USDJPYは**156.31**までドル高方向へ反応しました。citeturn231282view1turn168443view0

urlReuters：9月16日のFOMCと市場反応turn231282view0  
urlReuters：9月16日のWTI市場turn231282view2  
urlReuters：9月18日のBOJ見通しturn255659news13

## 1. 本日の結論

**A級：0件**  
**B級：1件 — WTI BUY_PULLBACK**  
**B+：0件**  
**新規の実取引：現時点ではNO_TRADE**

今日の重要な変化は、FOMCそのものより**FOMCに対する価格反応**です。

Fedは明確にタカ派でした。利上げは全会一致で、追加利上げも示唆。それでもNQZ26は一時29,227.5まで下げた後、約**29,462**まで回復しました。9月16日の日次では+0.74%です。ESZ26も遅延値で約7,680付近まで戻しています。citeturn558057search2turn548440search2

つまり昨日までの

**WTI高 → 金利高 → NASDAQ下**

という連鎖のうち、**金利高までは成立したがNASDAQの下落持続が弱かった**。

これはかなり重要です。NASDAQ SELLを新たに重ねる根拠は弱くなりました。

一方WTIは105.83から**102.43ドルへ3.2%下落**。サウジがオマーン経由の供給を増やしたことで供給懸念が一部緩和しましたが、Yanbu積み出し停止とHormuzの極端に少ない船舶通過は継続しています。citeturn231282view2

したがって、WTIは初めて**「ショック追随BUY」ではなく「押し目BUYを待てる価格構造」**になりました。

---

## 2. 前回判断の簡易検証

### 20260909_USDJPY_SELL_PULLBACK

既存条件：

**Entry 154.80–155.40**  
**SL 156.20**  
**TP1 152.50**

FOMC後、USDJPYは**156.31**まで上昇しました。citeturn168443view0

したがって、

**20260909_USDJPY_SELL_PULLBACK = fired**

です。

これは昨日が5営業日確認の最終日だったため、非常にきれいな教師データになります。

方向仮説は、

**BOJ利上げ期待 → 円高**

でしたが、最終日に

**Fedの追加利上げ示唆 → 米金利・ドル上昇**

が勝ちました。

このシグナルは本日から未決着リストから除外します。

ただし明日9月18日はBOJです。Reutersによると利上げ先は**1.25%**が中心予想で、追加利上げ経路まで市場が注目しています。citeturn255659news13turn255659news19

つまりUSDJPYは**旧SELL仮説が失敗した直後に、新しいBOJ仮説を作り直す必要がある状態**です。

### 20260909_WTI_BUY_PULLBACK

9月16日のWTIは102.43ドルで、既存失効水準を大きく上回っています。citeturn231282view2

したがって最終日は、

**not_fired / 5営業日満了**

です。

方向仮説としては成功。ただしEntry91ドル台まで戻らなかったため、実取引としては未約定です。

### 20260912_BTC_SELL_PULLBACK

既存：

**Entry 79200–79800**  
**SL 80850**  
**TP1 76450：到達済み**  
**TP2 74800：未到達**

CME BTCの9月16日は、

**高値76545  
安値75040  
終値付近75852**

でした。citeturn727698search0

TP2の74800までは届いていません。

ETFは最新完成データの9月15日に**-450.4Mドル**と大幅流出。前日の+159.9Mドルを完全に反転しました。citeturn596770search0

したがって、

**ETF/CME反転によるinvalidationは発生していない**  
**80850価格invalidationも未発生**

なので、

**20260912_BTC_SELL_PULLBACK=not_fired**

です。

このシグナルはまだ5営業日窓内です。

---

## 3. 市場全体の前提

総合regimeは**EVENT / MIXED**です。

FOMC結果は明確にタカ派でした。Fedは25bp利上げ、さらに年内追加利上げを示唆。10年債利回りは約5.00%、2年債は4.738%まで上昇しました。citeturn168443view0

しかし株式の反応は単純ではありません。

現物ではS&P500が-0.45%、Nasdaq Compositeはほぼ横ばいでした。citeturn231282view0

さらにNQZ26は日中安値29,227から29,400台へ戻しています。citeturn558057search2

これは、

**悪材料は成立したのに、NASDAQがそれほど下がらない**

という価格反応です。

TSOではこの場合、ニュースより価格を優先します。

DXYは100.31へ上昇、USDJPYは156.31。Gold現物は4263ドルまで下落しました。GCZ26は遅延系列で約4323ドルが確認できますが、COMEXの通常清算時刻とFOMC発表時刻がずれているため、GOLDは`partially_verified`とします。citeturn168443view0turn727698search1

WTIは102.43ドル。サウジはOmanのSohar沖でship-to-ship輸送を開始し供給懸念を一部緩和しましたが、Hormuz通過船は火曜日わずか4隻、10日平均18隻を大幅に下回ります。citeturn231282view2

Cryptoは引き続き弱いです。

BTCは約75.7k、CMEは約75.8k。ETHは約2400、CME ETHも2396付近。BTC ETFは-450.4Mドル、ETH ETFも約-142Mドルでした。citeturn596770news45turn727698search0turn231282search3turn596770search3

---

## 4. 10資産別判断

| 資産 | 本日判断 | コメント |
|---|---|---|
| GOLD | **NO_TRADE** | Fedタカ派で下だが既に急落後。追わない |
| BTC | **NO_TRADE / 既存SELL管理** | TP1済み、TP2未到達 |
| ETH | **NO_TRADE** | ETF流出＋弱いが既に下落済み |
| WTI | **B BUY_PULLBACK** | 初めて押し目Entryを定義可能 |
| USDJPY | **NO_TRADE** | 旧SELL fired。明日BOJ |
| SPX | **NO_TRADE** | Fed後もESが戻しており方向不明瞭 |
| NASDAQ | **NO_TRADE** | Fedタカ派でもNQが強く戻した |
| DXY | **NO_TRADE** | 100突破後。BOJ前に追わない |
| US10Y | **NO_TRADE** | 5%到達済み。追随は期待値低い |
| VIX | **NO_TRADE** | 約18前後、警戒域だがパニックではない |

VIXは9月16日にデータ元間で約18.0～18.4と差があります。Cboe公式ページの13:53 ET時点では16.75とFOMC前の値だったため、`partially_verified`にします。citeturn542184search2turn542184news22turn542184search0

---

## 5. A級候補

**なし。**

WTIは数値上かなりA級へ近いです。

新シグナル：

**20260917_WTI_BUY_PULLBACK**

Entry：**100.80–101.60**  
中点：**101.20**  
SL：**98.90**  
TP1：**105.20**  
TP2：**108.00**

RR：

\[
(105.20-101.20)/(101.20-98.90)=1.74
\]

生win_prob：**0.61**

二点分布なら約**+0.67R**ですが、

- Entryまで戻らない可能性
- Oman経由輸送拡大
- 外交・供給正常化ニュース
- 5営業日での時間決済

を織り込んで、

**expected_r = 0.48**

としました。

想定MAE：**約0.23R**

CBS87、EMS89なので、シグナル品質だけならA条件に近い。

それでもAにしない理由は**実行側の最小ロット損失を確実に確認できていないため**です。

したがって今日は**B監視**です。

---

## 6. B級監視候補

### WTI BUY_PULLBACK — B

**Entry 100.80–101.60**  
**SL 98.90**  
**TP1 105.20**  
**TP2 108.00**  
**RR 1.74**  
**win_prob 0.61**  
**expected_r 0.48**  
**risk_pct 0.25%**

現在102.43なので、**成行では買いません**。citeturn231282view2

101ドル台まで戻した場合だけ評価します。

特に、

**WTI 101付近  
＋ Hormuz依然制約  
＋ Saudi/Oman代替輸送が完全正常化していない**

という組み合わせならEntry品質はかなり改善します。

逆に98.90を割れば、今回の供給ショックの価格プレミアムが本格的に剥落したと見ます。

**B+にはしません。** XMで実際に使う銘柄の最小ロット×SL距離による実損が3,000円以内かを、この実行では確定できないためです。端末仕様で3,000円以内を確認できた場合のみ実取引候補です。

---

## 7. 触らない資産

最も触らないのは**USDJPY**です。

昨日のSELL仮説は156.20を突破して明確に失効しました。しかし、その直後に明日はBOJです。

BOJは1.25%への利上げが中心予想です。citeturn255659news13

今156.31でBUYするとFed後のドル上昇を追うことになり、SELLするとBOJ結果を先回りすることになります。

どちらも悪い。

NASDAQも今日は触りません。

昨日まで私は下方向を比較的強く見ていました。しかし、**Fedが実際に利上げし追加利上げまで示したのにNQが安値から反発した**。

これは仮説に都合の悪いデータなので重く扱います。

NQ SELLの確信度は一段下げます。

Goldも同様です。タカ派Fedに対する下落自体は予想通りですが、発表後に既に大きく動いています。新規SELLは追随になります。

---

## 8. 後日検証ポイント

第一は**NASDAQの耐性**です。

FOMC後、

**US10Y ≈5%  
DXY >100  
Fed追加利上げ示唆**

なのにNQZ26は29,400台へ戻しました。citeturn168443view0turn558057search2

今後、

**NQ >29600**

なら、「高金利でもgrowth株を売れない」状態がかなり強くなります。

逆に、

**NQ <29200**

なら今回の反発が一時的だったと判断します。

第二はUSDJPY。

旧SELLはfiredしました。

明日のBOJで、

**1.25%利上げ＋追加利上げ示唆なのにUSDJPY >156**

なら円高仮説をかなり弱めます。

逆に、

**USDJPY <154.40**

ならFOMC後のドル高をBOJが全て巻き戻したことになります。

第三はWTI。

**100.8–101.6へ押すが供給問題継続**

なら本日のBシグナルが約定候補。

**98.90割れ**

なら失効です。

第四はBTC。

9/15のETF-450MドルとCME75k台を踏まえると、現在は既存SELL仮説を支持しています。citeturn596770search0turn727698search0

**74800到達 → TP2**  
**80850突破 → fired**

です。

---

## 9. Obsidian保存用 Observation Draft

```markdown
# 2026-09-17 Post-FOMC Absorption / BOJ Next

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

WTI two-point raw EV:
~0.67R

WTI adjusted expected_r:
0.48R

Adjustment:
unfilled probability
supply-normalization headlines
5-business-day exit
geopolitical gap risk

## FOMC

Fed:
+25bp

Target:
3.75%-4.00%

Vote:
unanimous

SEP:
16/18 see at least one more hike this year

US10Y:
~5.00%

DXY:
100.31

USDJPY:
156.31

## Key surprise

Hawkish Fed did NOT create sustained Nasdaq selloff.

NQZ26:
low ~29227
rebounded to ~29462

Interpretation:
bad macro news increasingly absorbed by growth equities

Reduce confidence in simple:
oil -> yields -> NQ sell
chain.

## WTI

Settle:
102.43

Previous:
105.83

Reason for pullback:
Saudi supply via Oman
smaller US inventory draw

But:
Yanbu loading suspended
Hormuz traffic still extremely constrained

New B signal:
20260917_WTI_BUY_PULLBACK

Entry:
100.80-101.60

Mid:
101.20

SL:
98.90

TP1:
105.20

TP2:
108.00

RR:
1.74

win_prob:
0.61

expected_r:
0.48

MAE expected:
0.23R

Risk:
0.25%

Execution:
NO_TRADE until XM minimum-lot SL loss <= JPY3000 verified

## USDJPY old signal

20260909_USDJPY_SELL_PULLBACK

SL:
156.20

Post-FOMC:
156.31

Result:
FIRED

Remove from active invalidation list.

## BTC existing signal

20260912_BTC_SELL_PULLBACK

Entry:
79200-79800

TP1:
76450 reached

TP2:
74800 not reached

CME Sep16:
~75852
low ~75040

ETF Sep15:
-450.4m

invalidation:
not_fired

## Active invalidation

20260912_BTC_SELL_PULLBACK=not_fired

## BOJ

Date:
2026-09-18

Consensus:
hike to 1.25%

Primary test:
BOJ guidance vs Fed hawkishness

USDJPY <154.40:
yen side wins

USDJPY >156 after hawkish BOJ:
yen thesis weakens materially

## Today

A:
NONE

B:
WTI BUY_PULLBACK

B+:
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

#TSO #FOMC #BOJ #WTI #USDJPY #NASDAQ #BTC
```

## 10. TSO_LOG CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-09-17,20260917_GOLD_NONE_NO_TRADE,GOLD,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,79,83,,EVENT,94,93,99,76,82,94,post_FOMC_GCZ26_reclaim_4375_or_break_4250_with_yield_confirmation_required,GCZ26_4250_4323_4375_US10Y_DXY_1d_3d,partially_verified
2026-09-17,20260917_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,84,77,,RISK_OFF,86,94,97,82,84,82,manage_existing_20260912_sell_until_80850_or_verified_ETF_CME_reversal,BTC_74800_75800_79200_80850_ETF_CME_1d_3d,partially_verified
2026-09-17,20260917_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,82,79,,RISK_OFF,84,92,96,80,82,80,ETH_reclaim_2475_or_break_2350_with_ETF_CME_confirmation_required,ETH_2350_2400_2475_ETF_CME_1d_3d,partially_verified
2026-09-17,20260917_WTI_BUY_PULLBACK,WTI,BUY,B,PULLBACK,100.80,101.60,98.90,105.20,108.00,1.74,0.61,0.48,99,89,44,0.25,EVENT,89,96,95,86,87,92,WTI_below_98.90_or_verified_Saudi_Hormuz_supply_normalization,WTI_98.90_101.20_105.20_108_Oman_Hormuz_1d_3d_5d,verified
2026-09-17,20260917_USDJPY_NONE_NO_TRADE,USDJPY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,90,91,,EVENT,96,97,99,89,90,98,BOJ_Sep18_guidance_required_after_156.20_invalidation,USDJPY_154.40_156.31_157_BOJ_1d_3d,verified
2026-09-17,20260917_SPX_NONE_NO_TRADE,SPX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,98,76,78,,MIXED,88,91,97,74,79,91,ESZ26_break_below_7600_or_hold_above_7700_postFed_required,ESZ26_7600_7680_7700_US10Y_VIX_1d_3d,partially_verified
2026-09-17,20260917_NASDAQ_NONE_NO_TRADE,NASDAQ,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,88,72,,MIXED,91,94,98,86,86,94,NQZ26_failure_below_29200_or_sustained_reclaim_above_29600_required,NQZ26_29200_29462_29600_US10Y_VIX_1d_3d,partially_verified
2026-09-17,20260917_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,84,75,,EVENT,92,94,98,81,84,96,BOJ_reaction_break_below_99.80_or_hold_above_100.50_required,DXY_99.80_100.31_100.50_USDJPY_BOJ_1d_3d,verified
2026-09-17,20260917_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,99,91,82,,EVENT,98,98,99,89,92,99,postFed_hold_above_5.05_or_reversal_below_4.90_required,US10Y_4.90_5.00_5.05_NQ_GOLD_1d_3d,verified
2026-09-17,20260917_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,97,72,76,,MIXED,85,84,96,70,74,86,VIX_close_above_20_or_return_below_16_required,VIX_16_18_20_ES_NQ_1d_3d,partially_verified
```

### TSO_LOG JSON

```json
[
{"date":"2026-09-17","signal_id":"20260917_GOLD_NONE_NO_TRADE","asset":"GOLD","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":99,"opp_score":79,"no_trade_score":83,"risk_pct":"","regime":"EVENT","ems":94,"ffs":93,"cds":99,"ias":76,"cbs":82,"mes":94,"invalidation":"post_FOMC_GCZ26_reclaim_4375_or_break_4250_with_yield_confirmation_required","verification_target":"GCZ26_4250_4323_4375_US10Y_DXY_1d_3d","verified_status":"partially_verified"},
{"date":"2026-09-17","signal_id":"20260917_BTC_NONE_NO_TRADE","asset":"BTC","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":99,"opp_score":84,"no_trade_score":77,"risk_pct":"","regime":"RISK_OFF","ems":86,"ffs":94,"cds":97,"ias":82,"cbs":84,"mes":82,"invalidation":"manage_existing_20260912_sell_until_80850_or_verified_ETF_CME_reversal","verification_target":"BTC_74800_75800_79200_80850_ETF_CME_1d_3d","verified_status":"partially_verified"},
{"date":"2026-09-17","signal_id":"20260917_ETH_NONE_NO_TRADE","asset":"ETH","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":98,"opp_score":82,"no_trade_score":79,"risk_pct":"","regime":"RISK_OFF","ems":84,"ffs":92,"cds":96,"ias":80,"cbs":82,"mes":80,"invalidation":"ETH_reclaim_2475_or_break_2350_with_ETF_CME_confirmation_required","verification_target":"ETH_2350_2400_2475_ETF_CME_1d_3d","verified_status":"partially_verified"},
{"date":"2026-09-17","signal_id":"20260917_WTI_BUY_PULLBACK","asset":"WTI","side":"BUY","rank":"B","type":"PULLBACK","entry_low":"100.80","entry_high":"101.60","sl":"98.90","tp1":"105.20","tp2":"108.00","rr":"1.74","win_prob":"0.61","expected_r":"0.48","tq_score":99,"opp_score":89,"no_trade_score":44,"risk_pct":"0.25","regime":"EVENT","ems":89,"ffs":96,"cds":95,"ias":86,"cbs":87,"mes":92,"invalidation":"WTI_below_98.90_or_verified_Saudi_Hormuz_supply_normalization","verification_target":"WTI_98.90_101.20_105.20_108_Oman_Hormuz_1d_3d_5d","verified_status":"verified"},
{"date":"2026-09-17","signal_id":"20260917_USDJPY_NONE_NO_TRADE","asset":"USDJPY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":99,"opp_score":90,"no_trade_score":91,"risk_pct":"","regime":"EVENT","ems":96,"ffs":97,"cds":99,"ias":89,"cbs":90,"mes":98,"invalidation":"BOJ_Sep18_guidance_required_after_156.20_invalidation","verification_target":"USDJPY_154.40_156.31_157_BOJ_1d_3d","verified_status":"verified"},
{"date":"2026-09-17","signal_id":"20260917_SPX_NONE_NO_TRADE","asset":"SPX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":98,"opp_score":76,"no_trade_score":78,"risk_pct":"","regime":"MIXED","ems":88,"ffs":91,"cds":97,"ias":74,"cbs":79,"mes":91,"invalidation":"ESZ26_break_below_7600_or_hold_above_7700_postFed_required","verification_target":"ESZ26_7600_7680_7700_US10Y_VIX_1d_3d","verified_status":"partially_verified"},
{"date":"2026-09-17","signal_id":"20260917_NASDAQ_NONE_NO_TRADE","asset":"NASDAQ","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":99,"opp_score":88,"no_trade_score":72,"risk_pct":"","regime":"MIXED","ems":91,"ffs":94,"cds":98,"ias":86,"cbs":86,"mes":94,"invalidation":"NQZ26_failure_below_29200_or_sustained_reclaim_above_29600_required","verification_target":"NQZ26_29200_29462_29600_US10Y_VIX_1d_3d","verified_status":"partially_verified"},
{"date":"2026-09-17","signal_id":"20260917_DXY_NONE_NO_TRADE","asset":"DXY","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":99,"opp_score":84,"no_trade_score":75,"risk_pct":"","regime":"EVENT","ems":92,"ffs":94,"cds":98,"ias":81,"cbs":84,"mes":96,"invalidation":"BOJ_reaction_break_below_99.80_or_hold_above_100.50_required","verification_target":"DXY_99.80_100.31_100.50_USDJPY_BOJ_1d_3d","verified_status":"verified"},
{"date":"2026-09-17","signal_id":"20260917_US10Y_NONE_NO_TRADE","asset":"US10Y","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":99,"opp_score":91,"no_trade_score":82,"risk_pct":"","regime":"EVENT","ems":98,"ffs":98,"cds":99,"ias":89,"cbs":92,"mes":99,"invalidation":"postFed_hold_above_5.05_or_reversal_below_4.90_required","verification_target":"US10Y_4.90_5.00_5.05_NQ_GOLD_1d_3d","verified_status":"verified"},
{"date":"2026-09-17","signal_id":"20260917_VIX_NONE_NO_TRADE","asset":"VIX","side":"NONE","rank":"NO_TRADE","type":"NO_TRADE","entry_low":"","entry_high":"","sl":"","tp1":"","tp2":"","rr":"","win_prob":"","expected_r":"","tq_score":97,"opp_score":72,"no_trade_score":76,"risk_pct":"","regime":"MIXED","ems":85,"ffs":84,"cds":96,"ias":70,"cbs":74,"mes":86,"invalidation":"VIX_close_above_20_or_return_below_16_required","verification_target":"VIX_16_18_20_ES_NQ_1d_3d","verified_status":"partially_verified"}
]
```

今日の一番重要な学習は、**USDJPY SELLが最終日にきちんと失効したことと、タカ派FOMCにもかかわらずNASDAQが下げを維持できなかったこと**です。ニュース仮説より価格反応を優先するなら、昨日まで強かったNASDAQ SELLの確信度は下げるべきです。

一方WTIは105ドル台から102ドル台へ戻り、初めて「追いかけずに押し目を待つ」というTSO本来の形が作れるようになりました。今日はこの1本だけを方向ありBとして残します。
