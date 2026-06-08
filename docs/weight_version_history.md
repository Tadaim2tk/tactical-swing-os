# Weight Version History

Weight Version History は、Weights Patch候補やProposal Adoption Trackingの結果を長期追跡するための履歴レイヤーです。

このPhaseでは `weights.json` を更新しません。patchも適用しません。現在Versionは初期運用として `v1` に固定し、将来の明示承認付き更新に備えて、どのProposalが候補・保留・承認・却下・ブロック状態にあるかを記録します。

## 目的

Phase 15までで、Model State提案からWeights Patch候補を作り、人間レビューと採用追跡を行う流れができました。

Weight Version History は、その結果をVersion単位で見返せるようにするための分析用ビューです。

## 入力

- `results/proposal_adoption_tracking.json`
- `results/weights_patch_review.json`
- `results/model_state_update_proposals.json`
- `models/weights.json`

入力が存在しない場合でもworkflowは落ちません。履歴行は空になり、summaryでは `review_status=unavailable` として出力します。

## 出力

- `results/weight_version_history.csv`
- `results/weight_version_history.json`
- `results/weight_version_history_summary.json`
- `reports/model_state/YYYY-MM-DD_weight_version_history.md`

## adoption_status

履歴上の状態は以下に正規化されます。

- `tracked`: 追跡対象
- `held`: 保留
- `candidate`: 人間承認候補
- `approved`: 人間が採用判断したもの
- `rejected`: 却下
- `blocked`: 安全上ブロック

Proposal Adoption Trackingの `pending_review` は `candidate`、`accepted` は `approved` として履歴化されます。

## Version管理

現在の運用では `weights.json` を更新しないため、`current_version` は `v1` 固定です。

将来Phaseで人間承認付きのapplyを実装する場合、Version ID、適用日時、採用Proposal、変更理由、安全監査結果をこの履歴に追加していく想定です。

## Safety

- `weights.json` は自動更新しません
- patchは適用しません
- `generate_signal.py` は自動変更しません
- Google Sheetsへの書き込みは行いません
- 実売買・発注・XM操作は行いません
- すべてのweight変更はHuman Approvalが前提です
