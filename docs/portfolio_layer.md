# Portfolio Layer

Portfolio Layerは、Tactical Swing OSが生成した市場データ、シグナル、最新評価、Meta Learning、Auto Calibration Candidates、Human Override Analyticsなどを読み取り、ポートフォリオ全体としての配分候補を作る分析レイヤーです。

このレイヤーは資産別の売買シグナルを直接発注に変換しません。出力するのは、各資産の`allocation_score`、`portfolio_weight_candidate`、`confidence`、`risk_class`などの研究用候補だけです。

## 入力

- `results/market_snapshot.csv/json`
- `results/signals.csv/json`
- `results/latest_evaluations.csv/json`
- `results/meta_learning.csv/json`
- `results/auto_calibration_candidates.csv/json`
- `results/human_override_analytics.csv/json`
- `results/proposal_impact.csv/json`が存在する場合は補助的に利用

入力が欠けていても処理は継続し、fallbackとして固定資産ユニバースに対する保守的な候補を生成します。

## 出力

- `results/portfolio_layer.csv`
- `results/portfolio_layer.json`
- `results/portfolio_layer_summary.json`
- `reports/portfolio/YYYY-MM-DD_portfolio_layer.md`

Summaryにはcandidate assets、defensive assets、offensive assets、cash candidate、average confidence、portfolio concentration、risk concentration、recommended exposureを出力します。

## Dashboard

Dashboardには`Portfolio Layer`セクションが追加されます。

表示項目は、top allocation candidates、risk concentration、recommended exposure、cash ratio candidateです。配分候補の上位資産を確認できますが、これは実際の売買指示ではありません。

## 安全条件

- weights.jsonは更新しません
- patchは適用しません
- generate_signal.pyは変更しません
- Google Sheetsへの書き込みは行いません
- 実売買・発注・XM操作は行いません
- 自動リバランスは行いません
- すべての候補は人間承認が必須です
