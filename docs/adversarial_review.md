# Adversarial Review (Phase 23)

- 実装: `src/audit_adversarial_review.py`
- テスト: `src/test_adversarial_review.py`
- workflow: `.github/workflows/adversarial_review.yml`（毎日 07:30 JST / 手動）

## 目的

AI Feedback / Rule Proposal / Model State Proposal / Weights Patch / Auto Calibration など、蓄積済みの「提案・要約」を**横断レビュー**し、危険な兆候を検出する**ルールベースの敵対的監査層**。新しい予測ロジックではなく、憲章「AIは監査される対象」「過剰最適化への自動ブレーキ」の上に載る。

LLMは使わず、まずはルールベースで実装している（LLM API導入は後フェーズ）。

## 検出観点

| # | finding_category | 内容 |
|---|---|---|
| 1 | `insufficient_sample_strong` | サンプル不足（<30）なのに strong 提案。半数未満なら high_risk |
| 2 | `auto_apply_violation` / `weights_update_violation` / `generate_signal_violation` | `apply_automatically=true`(high_risk) / `weights_json_updated=true`・`patch_applied=true`・`generate_signal_updated=true`(blocked) |
| 3 | `overfitting_risk` | 増加方向の提案が低サンプル/低信頼で出ている |
| 3b | `weak_evidence_strong_claim` / `high_patch_risk` | 最低条件未達なのに強い / patch_risk_level=high |
| 4 | `lookahead_contamination` | Narrative Lookahead Audit が warning 以上 → ナラティブ由来提案への波及警告 |
| 5 | `overconfidence_language` | 「絶対」「必ず」「guaranteed」等の過信表現 |
| 6 | `cross_layer_contradiction` | 同一targetに増加と減少の提案が混在 |

## severity と review_status

- severity: `info` < `warning` < `high_risk` < `blocked`
- review_status は `blocked > high_risk > warning > passed(提案あり/findingなし) > unavailable(提案なし)` の優先順位

## 出力

- `results/adversarial_review.csv` / `.json`
- `results/adversarial_review_summary.json`
- `reports/audit/YYYY-MM-DD_adversarial_review.md`

## 安全条件

- 監査結果は**提案・警告のみ**。`weights.json` / `generate_signal.py` は一切変更しない（各 finding に `weights_json_updated=false` / `generate_signal_updated=false`）。
- `requires_human_approval` は常に `true`。最終判断は人間が行う。
- **LLM API・有料API新規利用なし**（蓄積済みCSV/JSONのみ読む）。
- Google Sheets書き込みなし。実売買・発注なし。

## Dashboard / Validation Suite 統合

- Dashboard に `Adversarial Review` セクション（review_status / 件数 / 違反数 / max_severity + blocked/high_risk/warning 詳細）。
- Validation Suite と Dashboard workflow の両方で毎回生成・検証する。
