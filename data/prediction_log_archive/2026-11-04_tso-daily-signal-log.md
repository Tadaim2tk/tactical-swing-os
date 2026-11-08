<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-11-04 07:00 JST -->
<!-- transport: ChatGPT conversation JSON (公式エクスポート conversations.json または /backend-api/conversation) -> tools/archive_gpt_prose.py --from-chatgpt-export -->
<!-- archived_at: 2026-11-08T22:30:38Z / chars: 19357 / 値は無修正 -->

# Tactical Swing OS — Daily Signal Log v2
<text color="secondary" size="sm">2026年11月4日（水）07:03 JST基準</text>

**使用モデル：GPT-6**  
**本日の市場の主役：NASDAQ**  
**総合regime：EVENT**  
**GOLD基準限月：COMEX 2026年12月限（GCZ26）**  
**WTI基準限月：NYMEX 2026年12月限（CLZ26）**

**crypto_grounds: etf=有, cme=有**  
**expected_r_basis: subjective**

今回のexpected_rは5営業日の時間決済、途中失効、イベント前の早期撤退を考慮した主観値です。NASDAQ・USDJPYについては承認済みの終値成行参加規則を適用し、Entry未到達による不参加確率を減点していません。

## 1. 本日の結論

<grid columns={3} gap={2}>
  <grid-item>
    <box border radius="lg" padding={3} gap={1}>
      <text color="secondary" size="xs">新規A級</text>
      <title size="2xl" tabularNums>0件</title>
    </box>
  </grid-item>
  <grid-item>
    <box border radius="lg" padding={3} gap={1}>
      <text color="secondary" size="xs">新規B級</text>
      <title size="2xl" tabularNums>6件</title>
    </box>
  </grid-item>
  <grid-item>
    <box border radius="lg" padding={3} gap={1}>
      <text color="secondary" size="xs">うちB+</text>
      <title size="2xl" tabularNums>3件</title>
    </box>
  </grid-item>
</grid>

本日はGOLD、ETH、WTI、USDJPY、SPX、NASDAQについて**方向ありのB級判断を記帳**します。BTC、DXY、US10Y、VIXはNO_TRADEです。

最も注目するのは、11月3日の米国市場でNASDAQ100先物が前日の大幅下落から約1.04%反発したことです。反発しても中期的な下落構造が直ちに解消されたわけではなく、SELL方向の監視を継続する根拠があります。<Cite ref="turn823697view0"/>

また、11月3日改定の**SL幅1×ATR10以上**を今回の6件すべてに適用しました。以前の0.5ATR近辺の狭いSLには戻していません。

各B級の理論リスクは0.25%。6件をすべて同時執行すると日次上限0.50%を超えるため、執行する判断は相関を考慮して選択する必要があります。ロット数・損失金額は人間側の管理事項として、シグナル判定の失格条件にしていません。

## 2. 前回判断の簡易検証

11月3日のTSO_LOGは10資産すべてNO_TRADEでした。追加の方向あり判断はありませんでした。

継続対象は10月30日のNASDAQ SELLです。

| 項目 | 発行時固定値 |
|---|---:|
| signal_id | `20261030_NASDAQ_SELL_PULLBACK` |
| Entry | 29640–29740 |
| SL | 29870 |
| TP1 / TP2 | 29120 / 28850 |
| 失効条件 | 4時間足終値29830超 |

11月2日のNQZ26高値は28891.25、11月3日の高値は28448.75でした。いずれも失効水準29830を下回っているため、この2日間の4時間足について失効は**not_fired**です。<Cite ref="turn823697view0"/>

ただし、過去レポートの`TP2_BEFORE_ENTRY / NOT_FILLED`分類には重要な監査上の問題があります。

**9月9日に承認されたNASDAQの終値成行参加規則を反映すると、10月30日のEntry帯未到達は、単純な未約定とは扱えません。** 10月30日終値参考28534.00で成行参加する規則だったためです。

この時点ではTP1の29120をすでに下回っており、元のTP1はSELLの利益目標として機能しません。したがって、旧シグナルの執行評価は`FALLBACK_MARKET_ENTRY / TP1_ALREADY_PASSED / EXECUTION_REVIEW_REQUIRED`として監査対象にします。

過去ログの発行値は変更せず、実際の注文・約定利益も未確認のまま残します。

**invalidation_check: 20261030_NASDAQ_SELL_PULLBACK=not_fired, 20261104_GOLD_SELL_PULLBACK=unknown, 20261104_ETH_SELL_PULLBACK=unknown, 20261104_WTI_SELL_PULLBACK=unknown, 20261104_USDJPY_BUY_PULLBACK=unknown, 20261104_SPX_SELL_PULLBACK=unknown, 20261104_NASDAQ_SELL_PULLBACK=unknown**

本日発行分の6件は、発行後の4時間足がまだないためunknownです。10月30日分は5営業日満了後の翌朝確認まで追跡します。

## 3. 市場全体の前提

### 最新10資産の価格

| 資産 | 基準値 | 参照日時・系列 | 検証 |
|---|---:|---|---|
| GOLD | 3930.75 | 11/3 GCZ26遅延日次 | 部分 |
| BTC | 約77610 | 11/3 BTC/USD現物 | 部分 |
| ETH | 約2291 | 11/3 ETH/USD Binance | 部分 |
| WTI | 95.96 | 11/3 CLZ26遅延日次 | 部分 |
| USDJPY | 158.73 | 11/3 米国時間夕方付近 | 部分 |
| SPX | 7609.75 | 11/3 ESZ26 | 部分 |
| NASDAQ | 28420.75 | 11/3 NQZ26 | 部分 |
| DXY | 101.87 | 11/3 ドル指数 | 部分 |
| US10Y | 約4.94% | 11/3 市場利回り | 部分 |
| VIX | 20.81 | 11/3 VIX指数 | 部分 |

GOLD、WTI、ES、NQは11月3日の取引終了付近の業者提供値を採用しました。正式清算値との差が残る可能性があるため、すべてpartially_verifiedです。<Cite refs={["turn756226view2","turn756226view3","turn823697view0","turn823697view1"]}/>

BTC・ETHは11月3日の現物参考値で、翌朝07:03 JSTとの完全な同時刻価格ではありません。USDJPY・DXY・VIXも取得できた最新の遅延参考値を使用しています。<Cite refs={["turn982168search4","turn137444view1","turn137444view0","turn756226view4","turn756226view5"]}/>

US10Yの約4.94%は市場利回りであり、米財務省の日次パー利回りとの確定照合は済んでいません。<Cite ref="turn378035news76"/>

### 主要な市場変化

<grid columns={2} gap={2}>
  <grid-item>
    <box border radius="lg" padding={3} gap={1}>
      <text color="secondary" size="xs">NQZ26・11月3日</text>
      <title size="xl" color="success">+1.04%</title>
      <text size="xs" color="secondary">急落後の反発</text>
    </box>
  </grid-item>
  <grid-item>
    <box border radius="lg" padding={3} gap={1}>
      <text color="secondary" size="xs">ESZ26・11月3日</text>
      <title size="xl" color="success">+0.47%</title>
      <text size="xs" color="secondary">ハイテク主導で回復</text>
    </box>
  </grid-item>
  <grid-item>
    <box border radius="lg" padding={3} gap={1}>
      <text color="secondary" size="xs">GCZ26・11月3日</text>
      <title size="xl" color="danger">-0.98%</title>
      <text size="xs" color="secondary">金利・原油変動を警戒</text>
    </box>
  </grid-item>
  <grid-item>
    <box border radius="lg" padding={3} gap={1}>
      <text color="secondary" size="xs">CLZ26・11月3日</text>
      <title size="xl" color="danger">-0.52%</title>
      <text size="xs" color="secondary">前日の急落後も不安定</text>
    </box>
  </grid-item>
</grid>

米国中間選挙の投票が11月3日に行われています。07:03 JSTの判断では、選挙結果を織り込んだ確定的な市場方向はまだ認定しません。

原油と長期金利の反発がインフレ警戒を残す一方、NASDAQは反発しています。市場全体は単純なRISK_ONでもRISK_OFFでもなく、イベント主導の分岐点と評価します。<Cite refs={["turn378035news74","turn378035news75"]}/>

### 暗号資産ETFとCME

| 日付 | BTC ETF | ETH ETF |
|---|---:|---:|
| 10/29 | +17.2M | -105.5M |
| 10/30 | -643.2M | -155.7M |
| 11/2 | **-398.6M** | **-139.7M** |
| 11/3 | 未集計 | 未集計 |

<caption>単位：百万米ドル。Farsideの11月3日行は未報告であり、0.0表示を実際のフローゼロとは解釈しません。<Cite refs={["turn720236view7","turn720236view8"]}/></caption>

CME先物価格・限月情報は参考材料として使用できました。一方、現物との同期basisと最新建玉変化は検証できていません。<Cite refs={["turn378035search5","turn140446view0"]}/>

## 4. 10資産別判断

| 資産 | 新規判断 | CBS | EMS | MES |
|---|---|---:|---:|---:|
| GOLD | B SELL | 72 | 59 | 85 |
| BTC | NO_TRADE | 66 | 45 | 43 |
| ETH | B SELL | 70 | 57 | 48 |
| WTI | B SELL | 72 | 50 | 98 |
| USDJPY | B BUY | 75 | 67 | 90 |
| SPX | B SELL | 73 | 63 | 88 |
| NASDAQ | B SELL | 78 | 63 | 92 |
| DXY | NO_TRADE | 66 | 58 | 79 |
| US10Y | NO_TRADE | 64 | 57 | 88 |
| VIX | NO_TRADE | 68 | 52 | 92 |

スコアは取得情報に基づく本日のモデル主観評価です。

**GOLD：** 3930.75ドル。4000ドルを回復できず、長期金利上昇と原油の反発が逆風です。戻りSELLのB級を記帳します。

**BTC：** 約77610ドル。ETFが2営業日連続で大幅流出となり、資金需給は弱いものの、現物は反発を試しています。MES43のためBTC固有ルールに従いNO_TRADEを優先します。

**ETH：** 約2291ドル。ETF流出が6営業日続き、2400ドルを下回る構造が続いています。戻りSELLをB級記帳しますが、取引所関連イベントで流動性リスクが残ります。

**WTI：** 95.96ドル。11月2日の7%超の急落後も戻りが弱く、SELL寄りです。ただし中東の供給関連ニュースで反転する可能性が高く、A級とは評価しません。

**USDJPY：** 158.73円。日銀会合後も円安方向へ戻り、米国債利回りの上昇が支えになっています。160円台への回復をBUY方向のB級で監視します。為替介入リスクは失効条件とは別に注視します。

**SPX：** ESZ26は7609.75。急落後の反発ですが、直近の上値構造は弱く、戻りSELLのB級です。

**NASDAQ：** NQZ26は28420.75。反発によるSELL Entry機会を監視します。既存10月30日シグナルとは別に、11月4日時点の1×ATR10幅で新しいB級を記帳します。

**DXY：** 101.87。反発はあるものの、ドル指数全体の上昇への移行は未確認でNO_TRADE。

**US10Y：** 約4.94%。利回り上昇方向ですが、利回り系列の日足ATRと実際の売買対象への変換を十分確認できておらずNO_TRADE。

**VIX：** 20.81。高い警戒水準は維持していますが、株価指数の反発に伴い前日から低下。指数自体の方向優位性は不十分でNO_TRADE。

## 5. A級候補

**本日のA級は0件です。**

USDJPYとNASDAQは相対的に有望ですが、USDJPYはexpected_r0.39R、MAE想定0.38R、NASDAQはexpected_r0.38R、MAE想定0.40Rです。

いずれもA級基準のexpected_r0.45以上、MAE0.25R以下を満たしません。イベントリスクが高い状況でもあるため、B級のまま維持します。

## 6. B級監視候補

<text color="secondary" size="sm">全6件のEntry・SL・TPは11月4日判断として固定。数値は各参照系列の価格単位です。</text>

| 資産 | Entry帯 | SL | TP1 | TP2 | RR |
|---|---:|---:|---:|---:|---:|
| GOLD SELL | 3950–3980 | 4070 | 3780 | 3680 | 1.761905 |
| ETH SELL | 2300–2330 | 2405 | 2170 | 2100 | 1.611111 |
| WTI SELL | 96.5–97.5 | 102 | 89.5 | 85 | 1.500000 |
| USDJPY BUY | 158.55–158.85 | 157.45 | 160.8 | 161.8 | 1.680000 |
| SPX SELL | 7630–7680 | 7780 | 7445 | 7290 | 1.680000 |
| NASDAQ SELL | 28500–28600 | 29300 | 27250 | 26600 | 1.733333 |

### 1×ATR10検証

過去10本の真の値幅を平均し、Entry帯の最もSLに近い端からでも1×ATR10以上の幅を確保しました。

| 資産 | ATR10 | SLまでの最短距離 | 判定 |
|---|---:|---:|---|
| GOLD | 82.10 | 90 | 適合 |
| ETH | 68.944 | 75 | 適合 |
| WTI | 4.27 | 4.50 | 適合 |
| USDJPY | 0.861 | 1.10 | 適合 |
| SPX | 95.075 | 100 | 適合 |
| NASDAQ | 679.00 | 700 | 適合 |

GOLD、WTI、USDJPY、ES、NQのATRは11月3日までの10営業日、ETHはUTCでの日足確定状況を考慮して11月2日までの10日間を使用しました。データ提供元の確定後修正によって小差が生じる可能性があります。

RRはすべてEntry中点から再計算しました。例えばNASDAQは中点28550、SL29300、TP1 27250なので、1300÷750＝1.733333です。

### 確率・期待値・B+判定

| 資産 | win_prob | expected_r | MAE想定 | B+ |
|---|---:|---:|---:|---|
| GOLD | 0.52 | +0.26R | 0.52R | — |
| ETH | 0.52 | +0.16R | 0.50R | — |
| WTI | 0.49 | +0.11R | 0.72R | — |
| USDJPY | 0.55 | +0.39R | 0.38R | 該当 |
| SPX | 0.53 | +0.28R | 0.44R | 該当 |
| NASDAQ | 0.54 | +0.38R | 0.40R | 該当 |

**B+観察候補：USDJPY BUY、SPX SELL、NASDAQ SELLの3件です。**

NASDAQとSPXは相関が高いため、両方のリスクを独立した機会として過大評価しません。USDJPYは相場の方向性が比較的独立していますが、米金利や中間選挙による共通リスクはあります。

各B級のinvalidationはCSV・JSONに個別記録しています。4時間足の失効条件が成立した場合、SL到達を待たずシナリオ崩壊として評価します。

## 7. 触らない資産

BTC、DXY、US10Y、VIXの4資産です。

BTCはMES43で固有の見送り条件に該当し、DXYはドル高への転換が未確定です。US10Yは方向性だけでなく取引参照系列とATRの検証不足、VIXは反発・再上昇の両方向が残っていることが主な理由です。

今回はイベントが近いという理由だけで方向判断を抑制していません。WTIやETHも、リスクを認識したうえでB級監視行を残しています。

## 8. 後日検証ポイント

本日からの重要な比較は、**旧0.5ATR近辺のSL設計と、新1×ATR10下限のSL設計による成績の違い**です。今後5営業日のMAE、MFE、失効、時間決済を分けて追跡します。

また、NASDAQ・USDJPYでは終値成行参加規則の適用状況を検証します。指値Entry帯に届かなかった場合でも、判断日の終値で参加する設計であり、従来の`TP_BEFORE_ENTRY`を自動的に「未約定」として処理しません。

イベント面では米中間選挙結果、11月4日のADP雇用関連統計、11月6日の米雇用統計を監視します。これらは本レポート時点で将来の発表として扱います。

## 9. Obsidian保存用 Observation Draft

```markdown
# TSO Observation — 2026-11-04

Model: GPT-6
Market protagonist: NASDAQ
Overall regime: EVENT

GOLD: GCZ26
WTI: CLZ26

crypto_grounds: etf=有, cme=有
expected_r_basis: subjective

New A: 0
New B: 6
B+: 3
Daily risk cap: 0.50%
Per B risk: 0.25%

## New B signals

GOLD SELL
ETH SELL
WTI SELL
USDJPY BUY
SPX SELL
NASDAQ SELL

## ATR10 minimum

GOLD: 82.10
ETH: 68.944
WTI: 4.27
USDJPY: 0.861
SPX: 95.075
NASDAQ: 679.00

All six SL widths >= 1x ATR10
measured even from the nearest Entry edge.

## Existing signal audit

20261030_NASDAQ_SELL_PULLBACK

Invalidation: not_fired

Previously reported:
TP2_BEFORE_ENTRY / NOT_FILLED

Audit correction:
Terminal market-entry rule applies.
Fallback close reference: 28534.00
TP1 was already passed at fallback entry.
Execution classification requires review.
No realized PnL confirmation.

## Crypto

BTC ETF Nov02: -398.6m
ETH ETF Nov02: -139.7m
Nov03 ETF: pending

## Research priorities

1. ATR10 1x SL versus previous narrow SL
2. Terminal market-entry execution validation
3. Daily B signal recurrence
4. Invalidation through fifth session and next morning
5. US election impact on index correlation

Sources:
https://www.investing.com/indices/nq-100-futures-historical-data
https://www.investing.com/indices/us-spx-500-futures-historical-data
https://www.investing.com/commodities/gold-historical-data
https://www.investing.com/commodities/crude-oil-historical-data
https://www.investing.com/currencies/usd-jpy-historical-data
https://farside.co.uk/btc/
https://farside.co.uk/eth/

#TSO #NASDAQ #ATR10 #BSignal
```

## 10. TSO_LOG — CSV / JSON

固定28列・10資産10行です。全6件のB級にEntry、SL、TP、RR、win_prob、expected_rを記録しました。

算術処理により28列構造、10資産の重複・欠落、全6件のRR、ATR10下限を確認しています。ファイル生成環境に接続できなかったためダウンロード用ファイルは作成せず、CSV・JSON全文をここに残します。

### CSV全文

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-11-04,20261104_GOLD_SELL_PULLBACK,GOLD,SELL,B,PULLBACK,3950,3980,4070,3780,3680,1.761905,0.52,0.26,68,72,,0.25,MIXED,59,88,86,65,72,85,GCZ26_4h_close_above_4050,GCZ26_20261103_3930.75_ATR10_82.10_prev10,partially_verified
2026-11-04,20261104_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,58,65,88,,EVENT,45,92,91,51,66,43,BTCUSD_76000_break_or_79000_reclaim,BTCUSD_spot_20261103_approx77610_ETF_20261102_m398.6_CME_Nov_ref,partially_verified
2026-11-04,20261104_ETH_SELL_PULLBACK,ETH,SELL,B,PULLBACK,2300,2330,2405,2170,2100,1.611111,0.52,0.16,65,70,,0.25,RISK_OFF,57,90,90,60,70,48,ETHUSD_4h_close_above_2380,ETHUSD_Binance_20261103_approx2291_ATR10_68.944_prev10,partially_verified
2026-11-04,20261104_WTI_SELL_PULLBACK,WTI,SELL,B,PULLBACK,96.5,97.5,102,89.5,85,1.5,0.49,0.11,63,76,,0.25,EVENT,50,98,93,60,72,98,CLZ26_4h_close_above_100.5,CLZ26_20261103_95.96_ATR10_4.27_prev10,partially_verified
2026-11-04,20261104_USDJPY_BUY_PULLBACK,USDJPY,BUY,B,PULLBACK,158.55,158.85,157.45,160.8,161.8,1.68,0.55,0.39,70,69,,0.25,EVENT,67,91,87,69,75,90,USDJPY_4h_close_below_157.8,USDJPY_20261103_approx158.73_ATR10_0.861_prev10,partially_verified
2026-11-04,20261104_SPX_SELL_PULLBACK,SPX,SELL,B,PULLBACK,7630,7680,7780,7445,7290,1.68,0.53,0.28,70,72,,0.25,RISK_OFF,63,92,89,66,73,88,ESZ26_4h_close_above_7730,ESZ26_20261103_7609.75_ATR10_95.075_prev10,partially_verified
2026-11-04,20261104_NASDAQ_SELL_PULLBACK,NASDAQ,SELL,B,PULLBACK,28500,28600,29300,27250,26600,1.733333,0.54,0.38,73,77,,0.25,RISK_OFF,63,94,93,71,78,92,NQZ26_4h_close_above_29100,NQZ26_20261103_28420.75_ATR10_679_prev10,partially_verified
2026-11-04,20261104_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,59,53,85,,MIXED,58,86,88,57,66,79,DXY_102.10_reclaim_or_101.43_break,DXY_index_20261103_101.87_not_DX_futures,partially_verified
2026-11-04,20261104_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,58,52,81,,EVENT,57,87,88,60,64,88,US10Y_5.00_reclaim_or_4.85_break,US10Y_20261103_market_yield_approx4.94_Treasury_par_unverified,partially_verified
2026-11-04,20261104_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,61,61,83,,EVENT,52,93,91,59,68,92,VIX_22.0_reclaim_or_19.0_break,VIX_index_20261103_20.81_Investing_cboe_series,partially_verified
```

### JSON全文

```json
[
  {
    "date":"2026-11-04",
    "signal_id":"20261104_GOLD_SELL_PULLBACK",
    "asset":"GOLD",
    "side":"SELL","rank":"B","type":"PULLBACK",
    "entry_low":3950,"entry_high":3980,"sl":4070,
    "tp1":3780,"tp2":3680,"rr":1.761905,
    "win_prob":0.52,"expected_r":0.26,
    "tq_score":68,"opp_score":72,"no_trade_score":null,
    "risk_pct":0.25,"regime":"MIXED",
    "ems":59,"ffs":88,"cds":86,"ias":65,"cbs":72,"mes":85,
    "invalidation":"GCZ26_4h_close_above_4050",
    "verification_target":"GCZ26_20261103_3930.75_ATR10_82.10_prev10",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-11-04",
    "signal_id":"20261104_BTC_NONE_NO_TRADE",
    "asset":"BTC",
    "side":"NONE","rank":"NO_TRADE","type":"NO_TRADE",
    "entry_low":null,"entry_high":null,"sl":null,
    "tp1":null,"tp2":null,"rr":null,
    "win_prob":null,"expected_r":null,
    "tq_score":58,"opp_score":65,"no_trade_score":88,
    "risk_pct":null,"regime":"EVENT",
    "ems":45,"ffs":92,"cds":91,"ias":51,"cbs":66,"mes":43,
    "invalidation":"BTCUSD_76000_break_or_79000_reclaim",
    "verification_target":"BTCUSD_spot_20261103_approx77610_ETF_20261102_m398.6_CME_Nov_ref",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-11-04",
    "signal_id":"20261104_ETH_SELL_PULLBACK",
    "asset":"ETH",
    "side":"SELL","rank":"B","type":"PULLBACK",
    "entry_low":2300,"entry_high":2330,"sl":2405,
    "tp1":2170,"tp2":2100,"rr":1.611111,
    "win_prob":0.52,"expected_r":0.16,
    "tq_score":65,"opp_score":70,"no_trade_score":null,
    "risk_pct":0.25,"regime":"RISK_OFF",
    "ems":57,"ffs":90,"cds":90,"ias":60,"cbs":70,"mes":48,
    "invalidation":"ETHUSD_4h_close_above_2380",
    "verification_target":"ETHUSD_Binance_20261103_approx2291_ATR10_68.944_prev10",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-11-04",
    "signal_id":"20261104_WTI_SELL_PULLBACK",
    "asset":"WTI",
    "side":"SELL","rank":"B","type":"PULLBACK",
    "entry_low":96.5,"entry_high":97.5,"sl":102,
    "tp1":89.5,"tp2":85,"rr":1.5,
    "win_prob":0.49,"expected_r":0.11,
    "tq_score":63,"opp_score":76,"no_trade_score":null,
    "risk_pct":0.25,"regime":"EVENT",
    "ems":50,"ffs":98,"cds":93,"ias":60,"cbs":72,"mes":98,
    "invalidation":"CLZ26_4h_close_above_100.5",
    "verification_target":"CLZ26_20261103_95.96_ATR10_4.27_prev10",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-11-04",
    "signal_id":"20261104_USDJPY_BUY_PULLBACK",
    "asset":"USDJPY",
    "side":"BUY","rank":"B","type":"PULLBACK",
    "entry_low":158.55,"entry_high":158.85,"sl":157.45,
    "tp1":160.8,"tp2":161.8,"rr":1.68,
    "win_prob":0.55,"expected_r":0.39,
    "tq_score":70,"opp_score":69,"no_trade_score":null,
    "risk_pct":0.25,"regime":"EVENT",
    "ems":67,"ffs":91,"cds":87,"ias":69,"cbs":75,"mes":90,
    "invalidation":"USDJPY_4h_close_below_157.8",
    "verification_target":"USDJPY_20261103_approx158.73_ATR10_0.861_prev10",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-11-04",
    "signal_id":"20261104_SPX_SELL_PULLBACK",
    "asset":"SPX",
    "side":"SELL","rank":"B","type":"PULLBACK",
    "entry_low":7630,"entry_high":7680,"sl":7780,
    "tp1":7445,"tp2":7290,"rr":1.68,
    "win_prob":0.53,"expected_r":0.28,
    "tq_score":70,"opp_score":72,"no_trade_score":null,
    "risk_pct":0.25,"regime":"RISK_OFF",
    "ems":63,"ffs":92,"cds":89,"ias":66,"cbs":73,"mes":88,
    "invalidation":"ESZ26_4h_close_above_7730",
    "verification_target":"ESZ26_20261103_7609.75_ATR10_95.075_prev10",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-11-04",
    "signal_id":"20261104_NASDAQ_SELL_PULLBACK",
    "asset":"NASDAQ",
    "side":"SELL","rank":"B","type":"PULLBACK",
    "entry_low":28500,"entry_high":28600,"sl":29300,
    "tp1":27250,"tp2":26600,"rr":1.733333,
    "win_prob":0.54,"expected_r":0.38,
    "tq_score":73,"opp_score":77,"no_trade_score":null,
    "risk_pct":0.25,"regime":"RISK_OFF",
    "ems":63,"ffs":94,"cds":93,"ias":71,"cbs":78,"mes":92,
    "invalidation":"NQZ26_4h_close_above_29100",
    "verification_target":"NQZ26_20261103_28420.75_ATR10_679_prev10",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-11-04",
    "signal_id":"20261104_DXY_NONE_NO_TRADE",
    "asset":"DXY",
    "side":"NONE","rank":"NO_TRADE","type":"NO_TRADE",
    "entry_low":null,"entry_high":null,"sl":null,
    "tp1":null,"tp2":null,"rr":null,
    "win_prob":null,"expected_r":null,
    "tq_score":59,"opp_score":53,"no_trade_score":85,
    "risk_pct":null,"regime":"MIXED",
    "ems":58,"ffs":86,"cds":88,"ias":57,"cbs":66,"mes":79,
    "invalidation":"DXY_102.10_reclaim_or_101.43_break",
    "verification_target":"DXY_index_20261103_101.87_not_DX_futures",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-11-04",
    "signal_id":"20261104_US10Y_NONE_NO_TRADE",
    "asset":"US10Y",
    "side":"NONE","rank":"NO_TRADE","type":"NO_TRADE",
    "entry_low":null,"entry_high":null,"sl":null,
    "tp1":null,"tp2":null,"rr":null,
    "win_prob":null,"expected_r":null,
    "tq_score":58,"opp_score":52,"no_trade_score":81,
    "risk_pct":null,"regime":"EVENT",
    "ems":57,"ffs":87,"cds":88,"ias":60,"cbs":64,"mes":88,
    "invalidation":"US10Y_5.00_reclaim_or_4.85_break",
    "verification_target":"US10Y_20261103_market_yield_approx4.94_Treasury_par_unverified",
    "verified_status":"partially_verified"
  },
  {
    "date":"2026-11-04",
    "signal_id":"20261104_VIX_NONE_NO_TRADE",
    "asset":"VIX",
    "side":"NONE","rank":"NO_TRADE","type":"NO_TRADE",
    "entry_low":null,"entry_high":null,"sl":null,
    "tp1":null,"tp2":null,"rr":null,
    "win_prob":null,"expected_r":null,
    "tq_score":61,"opp_score":61,"no_trade_score":83,
    "risk_pct":null,"regime":"EVENT",
    "ems":52,"ffs":93,"cds":91,"ias":59,"cbs":68,"mes":92,
    "invalidation":"VIX_22.0_reclaim_or_19.0_break",
    "verification_target":"VIX_index_20261103_20.81_Investing_cboe_series",
    "verified_status":"partially_verified"
  }
]
```

---

## 本日の総括

本日から採用した1×ATR10下限により、方向判断とSL設計を切り離して記録できるようになりました。

**新規A級0件、B級6件、B+観察候補3件。** 特にNASDAQ SELL、USDJPY BUY、SPX SELLを重点観察します。

従来の狭いSLを前提にせず、同時に方向が見えているB級をNO_TRADEへ落とさず記帳しています。ただし、発行数の増加だけでは改善を証明できないため、約定後のMAE・MFE、失効、5営業日時間決済と実現Rを後日検証します。

10資産分の28列TSO_LOGは、CSVとJSONの両形式で継続記録しました。
