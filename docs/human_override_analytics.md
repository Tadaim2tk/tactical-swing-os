# Human Override Analytics

Human Override Analytics は、AI提案と人間判断の差分を分析し、どのような人間介入が有効だったかを可視化するための研究用レイヤーです。

このPhaseでは人間判断を評価するだけで、自動修正、自動適用、重み変更は行いません。

## 入力

以下の優先順位で読み込みます。

1. `results/proposal_adoption_tracking.json`
2. `results/weight_version_history.json`
3. `results/proposal_impact.json`
4. `results/meta_learning.json`
5. `results/auto_calibration_candidates.json`

JSONが存在しない場合は対応するCSVをfallbackとして読み込みます。入力が存在しない場合でもworkflowは失敗せず、空のanalytics成果物を生成します。

Phase17 `proposal_impact` が未生成の場合は、impact outcomeを `unknown` として扱います。Phase17が生成された後は、同じ `proposal_id` を使ってimpact結果を結合します。

## 出力

- `results/human_override_analytics.csv`
- `results/human_override_analytics.json`
- `results/human_override_analytics_summary.json`
- `reports/model_state/YYYY-MM-DD_human_override_analytics.md`

## 分析項目

- `proposal_id`
- `review_decision`
- `adoption_status`
- `override_type`
- `override_reason`
- `impact_status`
- `impact_score`

## override_type

- `accepted`
- `held`
- `rejected`
- `blocked`
- `unknown`

## Analytics

以下を集計します。

- 人間採用率
- 人間保留率
- 人間却下率
- 採用後改善率
- 採用後悪化率
- 保留後改善率
- 保留後悪化率

impactが未取得の場合は `unknown_outcome` として扱います。

## Dashboard

Dashboardには `Human Override Analytics` セクションを追加します。

表示内容:

- total overrides
- accepted
- held
- rejected
- blocked
- positive override
- negative override
- unknown outcome
- recommended next action

## 安全条件

- `weights.json` は更新しません
- patchは適用しません
- `generate_signal.py` は変更しません
- Google Sheetsへの書き込みは行いません
- 実売買・発注・XM操作は行いません
- `requires_human_approval=true`

このレイヤーは人間判断の分析だけを行うもので、自動適用や自動修正には使いません。
