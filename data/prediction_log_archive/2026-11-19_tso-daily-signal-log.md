<!-- source: ChatGPT会話「TSO Daily Signal Log v2」定時実行 2026-11-19 07:00 JST -->
<!-- transport: Complete original read_thread message e00b440f-1529-4d34-a9df-d74ac9ad9622; raw markdown -->
<!-- archived_at: 2026-11-18T22:59:38Z / chars: 10901 / 値は無修正 -->

# Tactical Swing OS — 2026-11-19（木）日次判断

実行モデル: GPT-6
本日の市場の主役: GOLD
運用モード: 通常寄り防御
市場レジーム: RISK\_OFF / MIXED
データ基準: 2026-11-18米国市場、11月19日日本時間早朝時点で取得できた情報

## 1\. 本日の結論

**A級候補0件、B級監視候補4件、NO\_TRADE 6件。**

本日はドル高・米長期金利高・商品安を中心に判断する。方向性が比較的明確なのはGOLDの下落、NASDAQの戻り売り、USDJPYの上昇だが、いずれもA級に必要なATR10の確定検証が未完了である。

| 資産 | 判断 | 優先度 | 主な根拠 |
|--------|--------|--------|--------|
| GOLD | SELL / B | 1 | ドル高・金利高・金先物急落 |
| NASDAQ | SELL / B | 2 | 高金利とハイテク株の不安定さ |
| USDJPY | BUY / B | 3 | ドル優位、ただし円買い介入リスク |
| SPX | SELL / B | 4 | 株式市場の広範な弱さ |
| BTC | NO\_TRADE | — | 下落基調、ETF/CME検証不足 |
| ETH | NO\_TRADE | — | 独立した強い方向性を確認できず |
| WTI | NO\_TRADE | — | 急落後の供給要因・反発リスク |
| DXY | NO\_TRADE | — | 上昇方向だが価格系列の検証不足 |
| US10Y | NO\_TRADE | — | 高水準だが新規参加水準未確定 |
| VIX | NO\_TRADE | — | 方向性と短期変動の不一致 |

本日のB級は監視帯を定義した方向あり判断として記帳する。A級への昇格は行わない。

## 2\. 前回判断の簡易検証

前回の方向あり判断の原本と、各signal\_idに対応するinvalidation水準を今回の実行では取得できなかった。そのため、前日までの最新signal\_idを正確に特定できず、個別のfired判定は保留する。

`invalidation_check:` 対象signal\_id未取得（個別判定未実施）

これは発動なしを意味しない。前回判断の検証は未完了であり、過去の判断が消滅したものとして扱わない。

11月18日の市場では、GOLDの12月限が約3,743ドルまで下落し、ドル指数は約103.7、VIXは24.56付近だった。前日の売買判断がこれらの変動を捉えたかどうかは、過去のEntry・SL・invalidationとの照合が必要である。citeturn541219search5turn669567news5turn669567news7

## 3\. 市場全体の前提

11月18日の米国市場では、S&amp;P500現物が0.23%下落、NASDAQ総合が0.42%上昇、ダウ平均が1.11%下落した。市場全体が一様に売られたわけではなく、セクター間の分化が大きい。citeturn669567news5turn669567news7

GOLDはCOMEX 2026年12月限（GCZ26）を固定基準とする。11月18日の履歴価格は3,743.32ドル、日中安値3,731.60ドル。別データでは3,742.80ドル付近で整合している。citeturn541219search5turn541219search9

USDJPYは11月18日の参照値159.40〜159.42円。BTCは同日米東部時間朝に約64,100ドルと報じられ、株価指数先物に対して相対的に弱かった。citeturn541219search0turn541219search1turn669567news1

米10年債利回りは5.1%前後の高水準にあり、ドル高と合わせて金や高PER株の逆風になっている。citeturn669567news10turn669567news19

**データ上の制約\:** 10資産すべての同時刻価格と、判断日前10営業日の日足OHLCを完全には取得できていない。以下のB級水準は観測価格を起点とした暫定監視値であり、ATR10実測値を満たすことが確認済みの正式な注文水準ではない。推測値と観測値を区別する。

## 4\. 10資産別判断

### GOLD — SELL / B

- 参照系列: COMEX GCZ26、12月限
- 基準価格: 約3743
- Entry: 3770〜3800
- SL: 3940
- TP1: 3540、TP2: 3440
- RR: 1.63
- 主観win\_prob: 0.54
- expected\_r: +0.30R
- MAE想定: 0.45R
- CBS: 73、EMS: 61

ドル高・高金利・金の急落が売り方向を支持する。ただし11月18日に大きく下げた直後であり、短期的な買い戻しが入りやすい。反発局面を監視する。

SL距離155ドルは暫定値。ATR10実測値との比較が未完了のためA級にしない。invalidationは3940超え。

### BTC — NO\_TRADE

- 参照系列: BTC/USD現物
- 参考価格: 約64100（11月18日米東部時間朝）
- MES: 43
- CBS: 55

BTCは10月高値から大きく下落しており、basis tradeの収益性低下も報じられている。ETFフローとCME建玉の最新整合確認が不足するため、売り方向の可能性は残るが、今回はNO\_TRADEとする。citeturn669567news1

### ETH — NO\_TRADE

ETH/USD現物を対象とする。独立した価格構造とBTCに対する相対強弱を確認できていない。BTCの下落を機械的にETHの売り判断へ転用しない。

### WTI — NO\_TRADE

WTI先物を対象とする。11月18日は原油先物にも強い売り圧力が見られたが、供給ニュースと期近限月の価格構造を確認できていない。急落直後のmomentum追随は避ける。citeturn669567news5turn669567news7

### USDJPY — BUY / B

- 基準価格: 159.42
- Entry: 159.10〜159.50
- SL: 157.60
- TP1: 162.00、TP2: 163.00
- RR: 1.43
- 主観win\_prob: 0.53
- expected\_r: +0.26R
- MAE想定: 0.40R
- CBS: 71、EMS: 62

ドル高方向を優先。ただし159円台後半から160円台は日本当局の介入警戒が強まりやすい領域とみなし、上昇継続を無条件には想定しない。

判断日の終値までにEntry帯へ到達しない場合は終値成行参加という既存規則を維持する。ただし、その場合の実際のRRは約定価格で再計算する。invalidationは157.60割れ。

### SPX — SELL / B

- 参照系列: ES先物指数
- Entry: 7350〜7390
- SL: 7550
- TP1: 7070、TP2: 6900
- RR: 1.88
- 主観win\_prob: 0.51
- expected\_r: +0.27R
- MAE想定: 0.46R
- CBS: 68、EMS: 58

米株全体の弱さを監視する。ただしESの正確な11月18日終値・ATR10は未検証で、価格帯は暫定。invalidationは7550超え。

### NASDAQ — SELL / B

- 参照系列: NQZ26先物指数
- 参考価格: 27254.50（11月18日15:19 UTC時点）
- Entry: 27200〜27500
- SL: 28400
- TP1: 25500、TP2: 24800
- RR: 1.85
- 主観win\_prob: 0.53
- expected\_r: +0.33R
- MAE想定: 0.42R
- CBS: 72、EMS: 63

高金利とハイテク株の変動拡大を背景に戻り売りを優先する。一方、NVIDIA決算後の値動きで短期反発が起きており、方向の確信はA級に届かない。NQ先物価格を使用し、NASDAQ総合やQQQで代用していない。citeturn541219search4turn669567news3

終値成行参加規則は維持する。invalidationは28400超え。

### DXY — NO\_TRADE

ドル指数先物は103.72付近まで上昇した。方向は上向きだが、DXY指数本体と先物の水準差を混同しないため、今回の新規判断は見送る。citeturn669567news5

### US10Y — NO\_TRADE

米10年債利回りは5.1%前後。高金利レジームは継続しているが、上昇余地と反落リスクのバランスが不明瞭。利回り%系列で評価する。

### VIX — NO\_TRADE

VIXは24.56付近で、11月18日は約3.5%低下した。株式市場の不安定さが残る一方、VIX自体の短期方向性は明確ではない。citeturn669567news5turn669567news7

## 5\. A級候補

本日は0件。

理由は方向性が存在しないからではない。GOLD・NASDAQ・USDJPYには方向の見立てがあるが、ATR10下限、MAE、イベントリスクを含むA級条件の検証が未完了であるため、B級として継続記帳する。

## 6\. B級監視候補

| 資産 | Side | Entry中点 | SL | TP1 | RR | expected\_r |
|--------|--------|--------|--------|--------|--------|--------|
| GOLD | SELL | 3785 | 3940 | 3540 | 1.63 | \+0.30 |
| NASDAQ | SELL | 27350 | 28400 | 25500 | 1.85 | \+0.33 |
| USDJPY | BUY | 159.30 | 157.60 | 162.00 | 1.43 | \+0.26 |
| SPX | SELL | 7370 | 7550 | 7070 | 1.88 | \+0.27 |

RRはすべてEntry中点・SL・TP1から再計算した。

B+観察候補は0件。GOLDとNASDAQはCBSが70以上だが、EMSが60以上でも較正後勝率とその他条件を含む総合評価ではB+として確定しない。

## 7\. 触らない資産

BTC、ETH、WTI、DXY、US10Y、VIXの6資産。

BTCとETHは暗号資産市場の構造確認、WTIは供給要因、DXYは指数系列、US10Yは利回り方向、VIXは短期の反転リスクが主な未解決事項。

## 8\. 後日検証ポイント

1. GOLDの12月限が3731付近の安値を更新するか、それとも3800以上へ反発するか。
2. NASDAQの戻りが27500を超えて定着するか。
3. USDJPYが160円台を突破するか、介入警戒で反落するか。
4. BTCが株式市場の反発に追随できるか。
5. B級4件について、実測ATR10と暫定SL距離の差を検証する。
6. 前回signal\_idの取得とinvalidation判定を復旧する。

## 9\. Obsidian保存用Observation Draft

```markdown
---
date: 2026-11-19
system: Tactical Swing OS
model: GPT-6
regime: RISK_OFF
market_leader: GOLD
a_count: 0
b_count: 4
no_trade_count: 6
verification: partial
---

# Observation 2026-11-19

米長期金利高・ドル高が商品と株式に圧力。

GOLD 12月限の急落が中心的な市場変化。
NASDAQは高金利とハイテク株の不安定さを背景に戻り売り監視。
USDJPYはドル高方向だが介入リスクが制約。

B: GOLD SELL / NASDAQ SELL / USDJPY BUY / SPX SELL
A: なし
NO_TRADE: BTC ETH WTI DXY US10Y VIX

重要な検証欠損:
- ATR10の10営業日OHLC完全取得
- 前回signal_idとinvalidation水準
- BTC ETF/CME最新データ
- 全資産の同時刻価格
```

## 10\. TSO\_LOG — CSV / JSON

以下は10資産固定の本日記録。B級の価格・スコア・確率はモデル推定であり、未検証のATR10を実測済みとして扱っていない。

### CSV

```csv
date,signal_id,asset,side,rank,type,entry_low,entry_high,sl,tp1,tp2,rr,win_prob,expected_r,tq_score,opp_score,no_trade_score,risk_pct,regime,ems,ffs,cds,ias,cbs,mes,invalidation,verification_target,verified_status
2026-11-19,20261119_GOLD_SELL_PULLBACK,GOLD,SELL,B,PULLBACK,3770,3800,3940,3540,3440,1.58,0.54,0.30,70,74,32,0.25,RISK_OFF,61,65,68,59,73,67,GCZ26_above_3940,GCZ26_ATR10,partially_verified
2026-11-19,20261119_BTC_NONE_NO_TRADE,BTC,NONE,NO_TRADE,NO_TRADE,,,,,,,,,48,45,78,,RISK_OFF,44,43,52,40,55,43,BTC_ETF_CME_unconfirmed,BTCUSD_spot,partially_verified
2026-11-19,20261119_ETH_NONE_NO_TRADE,ETH,NONE,NO_TRADE,NO_TRADE,,,,,,,,,42,40,82,,RISK_OFF,40,42,45,39,46,40,ETH_structure_unconfirmed,ETHUSD_spot,unverified
2026-11-19,20261119_WTI_NONE_NO_TRADE,WTI,NONE,NO_TRADE,NO_TRADE,,,,,,,,,47,43,79,,MIXED,45,48,44,38,49,42,WTI_supply_and_contract_unconfirmed,WTI_futures,partially_verified
2026-11-19,20261119_USDJPY_BUY_PULLBACK,USDJPY,BUY,B,PULLBACK,159.10,159.50,157.60,162.00,163.00,1.59,0.53,0.26,66,69,37,0.25,MIXED,62,60,65,54,71,60,USDJPY_below_157.60,USDJPY_ATR10,partially_verified
2026-11-19,20261119_SPX_SELL_PULLBACK,SPX,SELL,B,PULLBACK,7350,7390,7550,7070,6900,1.67,0.51,0.27,62,64,42,0.25,RISK_OFF,58,57,60,49,68,55,ES_above_7550,ES_futures_ATR10,unverified
2026-11-19,20261119_NASDAQ_SELL_PULLBACK,NASDAQ,SELL,B,PULLBACK,27200,27500,28400,25500,24800,1.76,0.53,0.33,68,72,35,0.25,RISK_OFF,63,62,65,55,72,59,NQZ26_above_28400,NQZ26_ATR10,partially_verified
2026-11-19,20261119_DXY_NONE_NO_TRADE,DXY,NONE,NO_TRADE,NO_TRADE,,,,,,,,,55,50,68,,MIXED,54,57,53,48,59,55,DXY_index_futures_basis_unconfirmed,DXY_index,partially_verified
2026-11-19,20261119_US10Y_NONE_NO_TRADE,US10Y,NONE,NO_TRADE,NO_TRADE,,,,,,,,,51,46,73,,RISK_OFF,49,53,50,45,54,51,US10Y_direction_unconfirmed,US10Y_yield_pct,partially_verified
2026-11-19,20261119_VIX_NONE_NO_TRADE,VIX,NONE,NO_TRADE,NO_TRADE,,,,,,,,,43,39,81,,MIXED,41,44,42,37,46,43,VIX_direction_unconfirmed,VIX_index,partially_verified
```

**CSV算術訂正\:** 上のCSVのRR値が本文表と一致していないため、Entry中点を用いた正しい値はGOLD 1.58、USDJPY 1.59、SPX 1.67、NASDAQ 1.76である。本文表のRR 1.63、1.43、1.88、1.85は誤りであり、CSVを正とする。

計算式はそれぞれ、GOLD 245/155、USDJPY 2.70/1.70、SPX 300/180、NASDAQ 1850/1050。

### JSON

```json
{
  "date": "2026-11-19",
  "model": "GPT-6",
  "market_leader": "GOLD",
  "regime": "RISK_OFF",
  "risk_mode": "normal_defensive",
  "max_daily_risk_pct": 0.50,
  "gold_contract": "GCZ26",
  "data_status": "partial",
  "atr10_verified": false,
  "previous_invalidation_status": "not_evaluated_missing_signal_records",
  "summary": {
    "A": 0,
    "B": 4,
    "NO_TRADE": 6
  },
  "signals": [
    {
      "signal_id": "20261119_GOLD_SELL_PULLBACK",
      "asset": "GOLD",
      "side": "SELL",
      "rank": "B",
      "entry_low": 3770,
      "entry_high": 3800,
      "sl": 3940,
      "tp1": 3540,
      "tp2": 3440,
      "rr": 1.58,
      "win_prob": 0.54,
      "expected_r": 0.30,
      "risk_pct": 0.25,
      "cbs": 73,
      "ems": 61,
      "verified_status": "partially_verified"
    },
    {
      "signal_id": "20261119_BTC_NONE_NO_TRADE",
      "asset": "BTC",
      "side": "NONE",
      "rank": "NO_TRADE"
    },
    {
      "signal_id": "20261119_ETH_NONE_NO_TRADE",
      "asset": "ETH",
      "side": "NONE",
      "rank": "NO_TRADE"
    },
    {
      "signal_id": "20261119_WTI_NONE_NO_TRADE",
      "asset": "WTI",
      "side": "NONE",
      "rank": "NO_TRADE"
    },
    {
      "signal_id": "20261119_USDJPY_BUY_PULLBACK",
      "asset": "USDJPY",
      "side": "BUY",
      "rank": "B",
      "entry_low": 159.10,
      "entry_high": 159.50,
      "sl": 157.60,
      "tp1": 162.00,
      "tp2": 163.00,
      "rr": 1.59,
      "win_prob": 0.53,
      "expected_r": 0.26,
      "risk_pct": 0.25,
      "cbs": 71,
      "ems": 62,
      "verified_status": "partially_verified"
    },
    {
      "signal_id": "20261119_SPX_SELL_PULLBACK",
      "asset": "SPX",
      "side": "SELL",
      "rank": "B",
      "entry_low": 7350,
      "entry_high": 7390,
      "sl": 7550,
      "tp1": 7070,
      "tp2": 6900,
      "rr": 1.67,
      "win_prob": 0.51,
      "expected_r": 0.27,
      "risk_pct": 0.25,
      "cbs": 68,
      "ems": 58,
      "verified_status": "unverified"
    },
    {
      "signal_id": "20261119_NASDAQ_SELL_PULLBACK",
      "asset": "NASDAQ",
      "side": "SELL",
      "rank": "B",
      "entry_low": 27200,
      "entry_high": 27500,
      "sl": 28400,
      "tp1": 25500,
      "tp2": 24800,
      "rr": 1.76,
      "win_prob": 0.53,
      "expected_r": 0.33,
      "risk_pct": 0.25,
      "cbs": 72,
      "ems": 63,
      "verified_status": "partially_verified"
    },
    {
      "signal_id": "20261119_DXY_NONE_NO_TRADE",
      "asset": "DXY",
      "side": "NONE",
      "rank": "NO_TRADE"
    },
    {
      "signal_id": "20261119_US10Y_NONE_NO_TRADE",
      "asset": "US10Y",
      "side": "NONE",
      "rank": "NO_TRADE"
    },
    {
      "signal_id": "20261119_VIX_NONE_NO_TRADE",
      "asset": "VIX",
      "side": "NONE",
      "rank": "NO_TRADE"
    }
  ]
}
```

### 最終チェック

- 10資産の記録: 10件
- A級: 0件
- B級: 4件
- NO\_TRADE: 6件
- GOLD基準限月: GCZ26
- RR算術: CSV値を正として確認
- ATR10: 未検証
- 前回invalidation: 未検証
- CSV固定列: 28列構成で出力
- 記録継続: 実施

本日はGOLDの下落を最重要観察対象とし、NASDAQ・USDJPY・SPXを補助的な方向あり判断として記帳した。A級を無理に作らず、B級4件の継続検証を優先する。
