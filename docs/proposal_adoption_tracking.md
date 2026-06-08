# Proposal Adoption Tracking

Proposal Adoption Tracking は、Weights Patch Review後の提案が人間レビューでどう扱われたかを追跡するためのレイヤーです。

このレイヤーは `weights.json` を更新しません。patchを適用せず、採用状態のCSV/JSON/Markdownだけを生成します。

## 入力

- `results/weights_patch_review.json`
- `results/weights_patch_review.csv`
- `results/weights_patch_proposal.json`
- `results/weights_patch_proposal.csv`
- `results/model_state_update_proposals.json`
- `results/model_state_update_proposals.csv`
- `config/proposal_adoption_decisions.json` または `config/proposal_adoption_decisions.csv`

手動判断ファイルは任意です。存在しない場合は、Weights Patch Reviewの `review_decision` から採用状態を自動導出します。

## 出力

- `results/proposal_adoption_tracking.csv`
- `results/proposal_adoption_tracking.json`
- `results/proposal_adoption_tracking_summary.json`
- `reports/model_state/YYYY-MM-DD_proposal_adoption_tracking.md`

## adoption_status

- `pending_review`: review_decision が `candidate` で、人間判断待ち
- `held`: review_decision が `hold`、または人間判断で保留
- `rejected`: review_decision が `reject`、または人間判断で却下
- `blocked`: review_decision が `blocked`、または安全上ブロック
- `accepted`: 人間が明示的に採用判断したもの
- `superseded`: 別提案に置き換えられたもの
- `unreviewed`: レビュー判定がまだないもの

## 手動判断ファイル

任意で以下のようなファイルを作成できます。

```json
{
  "decisions": [
    {
      "proposal_id": "20260609_asset_BTC_weight_adjustment",
      "human_decision": "accepted",
      "human_decision_date": "2026-06-09",
      "decision_reason": "sample_count and evidence quality are sufficient"
    }
  ]
}
```

許可される `human_decision` は以下です。

- `accepted`
- `held`
- `rejected`
- `superseded`
- `pending_review`
- `blocked`

## Safety

- `weights.json` は自動更新しません
- patchは適用しません
- `generate_signal.py` は自動変更しません
- Google Sheetsへの書き込みは行いません
- 実売買・発注・XM操作は行いません
- 採用判断はHuman Approvalが前提です
