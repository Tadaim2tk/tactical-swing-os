# Weights Patch Review

Weights Patch Review は、Weights Patch候補を人間が採用判断しやすいように分類するための確認レイヤーです。

このレイヤーは `weights.json` を更新しません。patchを適用せず、承認補助用のCSV/JSON/Markdownだけを生成します。

## 出力

- `results/weights_patch_review.csv`
- `results/weights_patch_review.json`
- `results/weights_patch_review_summary.json`
- `reports/model_state/YYYY-MM-DD_weights_patch_review.md`

## review_decision

- `candidate`: 最低条件を満たした承認検討候補
- `hold`: weak候補、sample_count不足、データ不足などによる保留
- `reject`: delta不正、対象不明、max_allowed_delta欠損などによる却下
- `blocked`: 安全監査blocked、またはpatch_applied=trueなど安全条件違反

`candidate` でも自動適用はしません。人間がチェックリストを確認し、別フェーズで明示承認するまで `weights.json` は変わりません。

## recommended_next_action

- `wait_for_more_data`: 追加データを待つ
- `manual_review`: 人間による精査が必要
- `no_action`: 今回は対応しない

現段階では、weak候補やsample_count不足の候補が多い場合、`wait_for_more_data` が自然です。

## 人間チェックリスト

- 対象weight pathは妥当か
- sample_countは十分か
- avg_r / win_rate は実用的か
- 提案deltaは過大ではないか
- 直近相場の一時的偏りではないか
- 同じ方向の提案が複数重なりすぎていないか
- 実売買に使う前にバックテストまたは紙上検証するか

## 安全条件

- `weights.json` は自動更新しない
- `patch_applied=false`
- `requires_human_approval=true`
- Google Sheetsへの書き込みなし
- 実売買なし
- 発注なし
- XM操作なし
- `generate_signal.py` の自動変更なし
- Actionsからgit pushなし
