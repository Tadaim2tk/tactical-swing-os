# Evaluation Cohort Maturity（評価コホートの成熟待ち）— Phase 27.2

最大のリスクは「分析レイヤーが足りない」ことではなく、**最初の仮説コホートが評価へ
変換される瞬間を、ちゃんと観測できるか**である。評価0件・未決着だけの状態を `healthy`
と誤読しない（false green を出さない）ためのガイド。

## 評価ループの実体（どのファイルが正か）

durable な評価の蓄積は **Google Sheets の `SIGNALS` / `EVALUATIONS` ワークシート**、
ローカル/CI実行時の作業実体は **`results/`（gitignored）** にある。流れ:

```
data/raw/*.csv (fetch_market.py)
  └─ generate_signal.py        → results/signals.csv
        └─ reevaluate_pending_signals.py (evaluate_signal.py)
              → results/pending_reevaluations.csv
                    └─ build_latest_evaluations.py → results/latest_evaluations.csv
                          └─ evaluation_loader.load_evaluations_prefer_latest()
                                → dashboard / 各分析レイヤー
```

- 評価の記録は `results/evaluations.csv` と `results/latest_evaluations.csv`。
- **`data/signal_log.csv` / `data/verification_log.csv` は別系統の手動台帳であり、この
  ライブ評価ループには接続されていない**（`src/` のどこからも読み書きされない）。これらを
  評価のsinkだと誤解しないこと。verification の正は上記 `results/` 側である。
- ローカルで `data/raw` や `results/signals.csv` が空なら、評価0件は「壊れている」のでは
  なく「ライブ入力が無い/Sheets未接続」の正直な状態。

## 評価状態の区別（data_missing と awaiting_horizon）

`evaluate_signal.py` は、将来バーが無いケースを2つに**区別**する。取り違えると、若いだけの
シグナルを「データ欠損エラー(赤)」と誤表示してしまう。

| error_type | 意味 | OHLC | signal_date 以降のバー |
|---|---|---|---|
| `data_missing` | 価格データが本当に無い（asset未取得・空ファイル等） | 無し | — |
| `awaiting_horizon` | OHLCはあるが signal_date 以降のバーがまだ無い＝**ホライズン未到達（若い/蓄積中）** | 有り | 無し |
| `invalid_signal_date` | `signal_date` が不正/欠損で**評価位置を決められない入力不正**（若さではない） | — | — |

- trade(data_missing/awaiting_horizon): `status=pending` / `outcome=open_unresolved`（決着させない）。
- no_trade(data_missing/awaiting_horizon): `evaluation_status=skipped` / `outcome=no_trade`（正否は未確定）。
- **invalid_signal_date**: trade/no_trade とも `status=invalid` / `evaluation_status=skipped` /
  `outcome=invalid`。`signal_date is None`（パース不能/空）のとき future_bars が空になるが、これを
  `awaiting_horizon`（若い）と誤分類しないよう、ホライズン判定**より前**に弾く。
- ホライズン到達後にバーが揃えば、通常どおり `closed`（win_tp1/win_tp2/loss_sl）等へ進む。

## 評価成熟度（evaluation_maturity）

`dashboard_summaries.evaluation_summary` が、決着済み判断の有無から正直な成熟度を返す。
`dashboard_summary.json` の `evaluation_summary.evaluation_maturity` に格納され、Dashboard の
「評価概要」カードに表示される。

| maturity | 条件 | 読み方 |
|---|---|---|
| `no_signals` | 評価行が0件 | まだ何も評価対象が無い |
| `accumulating` | 行はあるが finalized（決着）=0 | **蓄積中**。pending / awaiting_horizon のみ。結果はまだ出ていない |
| `active` | finalized が1件以上 | 決着した判断がある |

- finalized = `win_tp1 / win_tp2 / loss_sl / no_trade_correct / no_trade_missed`。
- 併記される `awaiting_horizon` / `data_missing` / `invalid_signal_date` 件数で「なぜまだ蓄積中か」を切り分けられる。
- `invalid_signal_date`（入力不正）は finalized ではないため `active` を過剰に立てない。件数として可視化し、入力品質の問題を隠さない。

### Data Health（鮮度）との関係

Data Health（`data_health_summary`）は各レイヤーの**鮮度**を判定する別ガードである。
両者を**取り違えない**こと:

- `evaluations` / `latest_evaluations` レイヤーは `allow_empty` 無し → 行0なら `empty`(degraded)
  として正直に劣化表示される（鮮度の偽green防止は既に効いている）。
- 一方、若い（accumulating）状態を `health_status=degraded` に落とすのは**逆の偽り（false
  red）**。若さは想定内であり、パイプライン障害ではない。よって成熟度は health_status を
  汚さず、独立した `evaluation_maturity` として正直に併記する。

つまり: **「鮮度は fresh / 成熟度は accumulating」= データは新しいが決着はまだ、という二段の
正直さ**を同時に表示する（fresh を「結果が出ている」と誤読させない）。

## 安全条件

- 表示・評価専用。実売買・発注・XM/証券会社操作なし。
- `weights.json` / `generate_signal.py` を変更しない。
- 新規出力ファイル・新規 workflow を追加しない（既存の dashboard / validation_suite が生成・検証）。
- AIはコスト値や評価結果を捏造しない（証拠主義）。
