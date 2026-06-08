# Model State Safety Gate

Model State Safety Gate は、`propose_model_state_updates.py` が生成した重み更新提案を、人間が確認する前に機械的に安全監査するための仕組みです。

## 目的

この監査は、危険・過大・データ不足の提案を検出し、Dashboardとartifactで分かるようにするために使います。

監査は以下を出力します。

- `results/model_state_proposal_audit.json`
- `results/model_state_proposal_audit.csv`
- `reports/model_state/YYYY-MM-DD_model_state_proposal_audit.md`

## 監査ルール

主なチェックは以下です。

- `apply_automatically=true` が含まれる提案は critical blocked
- `abs(proposed_delta) > max_allowed_delta` は blocked
- `confidence_level=insufficient_data` なのに non-hold または deltaありなら blocked
- `sample_count < 5` なのに non-hold なら warning
- `proposal_strength=strong` なのに根拠が弱い場合は warning

## audit_status

監査結果は以下のいずれかです。

- `passed`: 明確なブロック・警告なし
- `warning`: 人間確認が特に必要な提案あり
- `blocked`: 反映してはいけない提案あり
- `unavailable`: 提案データが未取得

## 重要な安全条件

この監査は、自動反映を許可するものではありません。

- `weights.json` は更新しません
- `weights_json_updated` は常に `false`
- `requires_human_review` は常に `true`
- 実売買は行いません
- 発注は行いません
- XMや証券会社の操作は行いません

`audit_status=blocked` の場合、その提案は絶対に反映しないでください。

`audit_status=warning` の場合も、人間が根拠と相場環境を確認するまで反映しないでください。
