# Data Health / Freshness (Phase 24)

- 実装: `src/dashboard_summaries.py`（`data_health_summary` / `assess_layer` / `parse_generated_at`）
- 表示: `src/dashboard_render.py`（`Data Health / Freshness` セクション）
- テスト: `src/test_dashboard_health.py`

## 目的

レイヤーが大量に増えた今、最大のリスクは「分析が壊れる」ことより**「古い/空のデータを正常だと思って読む」**ことである。偽passed問題（Adversarial Review の `count_sources_present`）と同じ思想で、Dashboard 全体に **freshness guard** を敷く。

各分析レイヤーについて、最終生成時刻・行数・想定更新間隔から鮮度を判定し、一目で「どの分析が古い/空/正常か」を見えるようにする。

## レイヤー別ステータス

| status | 意味 |
|---|---|
| `fresh` | 想定間隔内に生成され、データあり |
| `stale` | 生成時刻が想定間隔(threshold_hours)を超過 |
| `empty` | 生成時刻はあるが行数0（rows_expected レイヤー） |
| `missing` | 生成時刻も行数も無い（一度も生成されていない） |
| `unavailable` | summary が明示的に unavailable（対象データ不足） |
| `unknown_age` | 行はあるが生成時刻が取れず鮮度判定不能 |
| `future_timestamp` | 生成時刻が明確に未来(> 1h)。時計/タイムゾーン異常の検知。軽微なクロックスキュー(<1h)は許容して fresh |

- 想定更新間隔: daily=36h / 評価=48h / weekly≈204h / monthly≈840h
- **`allow_empty`**: 監査系レイヤー（`adversarial_review` 等、0件=「異常なし」が正常）は行数0でも生成時刻が新しければ `fresh` とする。0件を `empty`(degraded) と誤判定しない

## 全体 health_status

- `critical`: missing または unavailable が1つでもある（core データ欠損）
- `degraded`: stale または empty がある
- `watch`: unknown_age または future_timestamp がある
- `healthy`: 全レイヤー fresh

`attention_layers` に stale/empty/missing/unavailable/future_timestamp のレイヤー名を列挙する。

> **鮮度 ≠ 成熟度**: Data Health はレイヤーの**鮮度**を見る。評価が「新しいが、まだ決着0件
> （蓄積中）」という状態は鮮度の劣化ではなく**成熟度**の問題であり、`evaluation_summary` の
> `evaluation_maturity`（no_signals / accumulating / active）として別途・正直に併記する。
> `fresh` を「結果が出ている」と誤読しないこと。詳細は
> [evaluation_cohort_maturity.md](evaluation_cohort_maturity.md)。

## タイムスタンプの扱い

`parse_generated_at` が `... UTC` / `... JST` / `YYYY-MM-DD` を naive UTC に正規化する（JSTは-9時間してUTC化）。`now` は `now_utc()` を渡し、両者を naive UTC で比較する。

## 安全条件

- 表示・分析専用。`weights.json` / `generate_signal.py` は一切変更しない（summary に `weights_json_updated=false` / `generate_signal_updated=false`）。
- `requires_human_approval=true`。新規出力ファイル・新規workflowなし（`dashboard_summary.json` に `data_health_summary` キーとして埋め込み、既存の dashboard / validation_suite で生成・検証）。
