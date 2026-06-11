# Auto Calibration Candidates

Auto Calibration Candidates は、Meta LearningやProposal Impactの結果から、将来検討できる重み変更候補を生成するための研究用レイヤーです。

このPhaseでは候補を作るだけで、`weights.json`、`model_state.json`、`generate_signal.py` は変更しません。patchも適用しません。

## 入力

入力は以下の優先順位で読みます。

1. `results/meta_learning.json`
2. `results/proposal_impact.json`
3. `results/proposal_adoption_tracking.json`
4. `results/weight_version_history.json`

JSONが存在しない場合は対応するCSVをfallbackとして読みます。入力がすべて存在しない場合でもworkflowは失敗せず、空のcandidate成果物を生成します。

## 出力

- `results/auto_calibration_candidates.csv`
- `results/auto_calibration_candidates.json`
- `results/auto_calibration_candidates_summary.json`
- `reports/model_state/YYYY-MM-DD_auto_calibration_candidates.md`

## Candidate分類

- `increase`: 将来の重み引き上げ候補
- `decrease`: 将来の重み引き下げ候補
- `hold`: 変更保留
- `insufficient_data`: データ不足
- `blocked`: ブロック扱い

`success_pattern` かつ positive impact のMeta Learning候補は `increase`、`failure_pattern` かつ negative impact の候補は `decrease` として扱います。サンプル数が少ない場合は `insufficient_data` とします。

## 安全設計

すべての出力で以下を固定します。

- `requires_human_approval=true`
- `patch_applied=false`
- `weights_json_updated=false`
- `generate_signal_updated=false`
- `apply_automatically=false`

このレイヤーは重み変更の提案候補を作るだけです。自動適用、実売買、発注、XM操作、Google Sheets書き込みは行いません。

## Dashboard

Dashboardには `Auto Calibration Candidates` セクションが表示されます。

表示内容:

- candidate count
- increase
- decrease
- hold
- blocked
- top confidence candidates
- recommended next action

## 運用

PRマージ後や大きな変更後はValidation Suiteを実行し、Auto Calibration CandidatesのCSV/JSON/Markdownがartifactに含まれていることを確認します。

Dashboard更新時にも候補生成を事前に実行しますが、失敗してもDashboard表示は継続します。その場合は候補欄が未取得になります。
