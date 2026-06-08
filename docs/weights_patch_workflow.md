# Weights Patch Workflow

Weights Patch Proposal は、Model State更新提案から `weights.json` に対する差分候補を作るための仕組みです。

## 目的

`propose_model_state_updates.py` は「どの重みを、なぜ、どれくらい変えるべきか」という提案を作ります。

`build_weights_patch.py` は、その提案のうち安全監査を通過したものだけを、将来 `weights.json` に適用できるかもしれないpatch候補として整理します。

このPhaseでは、patch候補をファイルとして生成するだけです。

## 入力

- `models/weights.json`
- `results/model_state_update_proposals.json`
- `results/model_state_update_proposals.csv`
- `results/model_state_proposal_audit.json`
- `results/model_state_proposal_audit.csv`

## 出力

- `results/weights_patch_proposal.json`
- `results/weights_patch_proposal.csv`
- `results/weights_patch_summary.json`
- `reports/model_state/YYYY-MM-DD_weights_patch_proposal.md`

## Model State更新提案との違い

Model State更新提案は、成績に基づく重み調整の候補です。

Weights Patch Proposalは、その候補を `weights.json` の論理pathに変換したものです。たとえば以下のようなpathを出します。

- `asset_weights.BTC`
- `side_weights.LONG`
- `rank_weights.A`
- `setup_type_weights.A-Momentum`
- `reason_code_weights.trend_up`
- `narrative_weights.risk_on`

このpathは提案上の論理pathです。既存の `weights.json` 構造と完全一致しない場合があります。

## 採用条件

patch候補になるのは、以下をすべて満たす提案だけです。

- audit_status が `passed` または `warning`
- proposal単位の audit_result が `passed`
- `apply_automatically=false`
- `proposal_direction` が `increase` または `decrease`
- `proposed_delta != 0`
- `confidence_level != insufficient_data`
- `sample_count >= 5`
- `abs(proposed_delta) <= max_allowed_delta`

`audit_status=blocked` の場合、patch候補は生成しません。

## 安全条件

このworkflowは `weights.json` を更新しません。

- `weights_json_updated=false`
- `patch_applied=false`
- `requires_human_approval=true`
- `apply_automatically=false`

人間承認なしにpatchを適用してはいけません。

## 今後のPhase

将来のPhaseでは、人間が明示承認したpatchだけを適用する仕組みを検討できます。

ただし、その場合も実売買・発注・XM操作とは無関係です。Trading OSの研究用パラメータを更新するかどうかの判断に限定します。
