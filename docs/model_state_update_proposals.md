# Model State Update Proposals

`propose_model_state_updates.py` は、Tactical Swing OS の `model_state` / `weights` を将来どう調整するべきかを、構造化された提案として出力するための分析スクリプトです。

## 目的

`latest_evaluations`、reason code分析、rule update proposals、月次較正、AI Feedbackをもとに、以下のような更新候補を生成します。

- asset別のweight調整候補
- side別のbias調整候補
- rank別のconfidence調整候補
- setup type別のweight調整候補
- reason_code別のweight / penalty調整候補
- narrative別のweight調整候補

出力は以下です。

- `results/model_state_update_proposals.csv`
- `results/model_state_update_proposals.json`
- `results/model_state_update_summary.json`
- `reports/model_state/YYYY-MM-DD_model_state_update_proposals.md`

## latest_evaluationsを使う理由

`EVALUATIONS` と `PENDING_REEVALUATIONS` はappend-onlyの履歴として蓄積されます。分析時に古い評価と最新の再評価が混在すると、同じ `signal_id` を二重に数える可能性があります。

そのため、model state更新提案では `results/latest_evaluations.csv` を優先して使います。これは各 `signal_id` について最新の評価状態をまとめた分析用ビューです。

## weights.jsonを自動更新しない理由

`models/weights.json` は現在の基準重みとして読み取りますが、このスクリプトは絶対に自動更新しません。

理由は以下です。

- まだサンプル数が少ないカテゴリが多い
- 相場環境に依存した一時的な成績の可能性がある
- 自動反映すると過学習や過剰最適化が起きやすい
- 実運用前には人間による確認が必要

このPhaseでは「どの重みを、なぜ、どれくらい変える候補があるか」を提案するだけです。

## 保守的なdelta制限

提案deltaは `sample_count` によって上限を制限します。

- `sample_count < 5`: `max_allowed_delta = 0`
- `sample_count 5〜9`: `max_allowed_delta = 0.03`
- `sample_count 10〜19`: `max_allowed_delta = 0.05`
- `sample_count >= 20`: `max_allowed_delta = 0.08`

データ不足のときは `confidence_level = insufficient_data`、`proposal_direction = hold`、`proposed_delta = 0` になります。

## 判定方針

基本ルールは以下です。

- `avg_r > 0.25` かつ `win_rate > 0.55`: increase候補
- `avg_r < -0.15` または `win_rate < 0.40`: decrease候補
- それ以外: hold

ただし、提案deltaは必ず `max_allowed_delta` の範囲内にクリップされます。

## apply_automatically

すべての提案で `apply_automatically=false` です。

Dashboardにもこの値を表示し、自動適用されないことを明示します。

## 今後のPhase

今後のPhaseでは、十分な評価件数が蓄積したあとに、人間承認を前提として `weights.json` へ反映する仕組みを検討できます。

ただし、その場合も以下を守ります。

- 実売買は行わない
- 発注は行わない
- XMや証券会社の操作は行わない
- 反映前に人間が提案内容を確認する

## 安全条件

この仕組みは研究・分析用です。

- Google Sheetsへの書き込みは行いません
- `weights.json` は自動更新しません
- `generate_signal.py` は自動変更しません
- 実売買・発注・XM操作は行いません
