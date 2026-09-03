# 週次 crypto 文脈タスク（ChatGPTタスク "Weekly Sunday crypto-theme dashboard" の正本）

status: 2026-09-03 改定。**このタスクは元から存在し、元から週次（日曜）だった**。
人間の問い「Crypto market update: macro vs regulation dynamics っていらないのでは」で調べたところ、
その名前はこのタスクが生成した**会話スレッドの題名**であり、タスクは別名で存在していた。
廃止はせず、出力を台帳へ着地させる5)を追加した（changelog(14)）。

実行: **毎週日曜 20:30 JST**（変更なし）。取込は次回のroute-3で人間経由。
タスクID: `69356b19e87c819195526e7b6eb74d92`

---

## このタスクの既存の強み（1〜4は改定前から存在。壊さないこと）

1. 週末の主テーマとテーマスコア（0〜100）＋各スコアに根拠1行
2. BTC/ETHの週末センチメントスコア（0〜100）＋根拠1行
3. **月曜以降のレジーム予測を、起点価格と判定条件つきの反証可能な形で**
   （例: BTCが次の金曜終値までにXXを上回る/下回る）
4. **前回予測の自己採点**（的中/外れ/data_pending）

3)と4)の組み合わせは、TSOのGPTタスクの中で**唯一、週次ホライズンの反証可能な予測と
その自己採点を持つ**。日次タスクにも月次にも無い。これを削ると失われる。

「変化がない項目は変化なしと1行で済ませる／根拠を示せない精密風の数値は出さない」も既存規約。

## 追加した5)（機械取込用の2行）

```
CRYPTO_CTX,<まとめる週の月曜=実行日の6日前>,<driver>,<etf_flow_dir>,<cme_basis>,<regulation_event>,<confidence>,<prev_result>
CRYPTO_PRED,<同じ月曜>,<BTC|ETH>,<ABOVE|BELOW>,<水準の数値のみ>,<判定期限>
```

| 欄 | 取りうる値 | 意味 |
|---|---|---|
| driver | `MACRO` / `IDIOSYNCRATIC` / `MIXED` / `UNKNOWN` | 今週のcryptoを動かした主因はマクロ(DXY・金利・株)か、crypto固有(規制・ETF・清算)か |
| etf_flow_dir | `INFLOW` / `OUTFLOW` / `FLAT` / `UNKNOWN` | 現物ETFの週間フローの向き |
| cme_basis | `CONTANGO` / `BACKWARDATION` / `FLAT` / `UNKNOWN` | CME先物ベーシスの状態 |
| regulation_event | `NONE` / `PROPOSAL` / `ENFORCEMENT` / `APPROVAL` / `HEARING` / `OTHER` | 今週の規制イベントの型 |
| confidence | `HIGH` / `MEDIUM` / `LOW` | 上記4欄の確からしさ |
| prev_result | `HIT` / `MISS` / `DATA_PENDING` / `NONE` | 4)の自己採点結果を機械可読にしたもの |

`CRYPTO_PRED` は 3) の予測を機械可読にしたもの。
**UNKNOWN を選ぶことは失敗ではない**。取れなかったものを推測で埋める方が有害である。

取込: `tools/record_crypto_context.py` が語彙・月曜・重複を検証して
`data/crypto_context_weekly.csv` へ追記する。

## やらないこと

- **売買判断を書かない**。entry / SL / TP / rank / win_prob / ロットは日次タスク(07:00)の領分。
  ここに書くと同じ判断が2箇所に存在し、どちらが本物か分からなくなる。
- **日次タスクのBTC/ETH見送りを減らす目的で使わない**。根拠を揃えることが目的化すると、
  正直な棄権が作られた判断に化ける（B+印がスコアの内生化で無意味化した件と同型）。

## 検証設計（10月月次で見る）

- `prev_result` の的中率 — 3)の予測が当たっているか。**これが本命の検証**
- `driver=MACRO` と申告した週のBTC/ETHは、実際にDXY・US10Yとの相関が高かったか
- 自己申告 confidence と当否の対応（HIGHが当たっているか）
- 週次なので1年52件、独立クラスタもほぼ52件。日次より件数は少ないが
  疑似反復が無いぶん検定力はむしろ高い。
