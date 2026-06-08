# Latest Evaluation View

`latest_evaluations` は、append-onlyで蓄積される `EVALUATIONS` と `PENDING_REEVALUATIONS` から、各 `signal_id` の最新評価だけを選ぶ分析用ビューです。

元データは削除・更新しません。履歴は履歴として残し、Dashboardなどの分析では最新ビューを優先して使います。

## 入力

優先順位は以下です。

1. Google Sheets の `EVALUATIONS` / `PENDING_REEVALUATIONS`
2. ローカルCSV fallback
   - `results/evaluations.csv`
   - `results/pending_reevaluations.csv`

Secretsが未設定、またはSheets読み込みに失敗した場合でも、ローカルCSV fallbackで実行します。

## 最新行の選び方

`signal_id` 単位で1行を採用します。空の `signal_id` は除外します。

時刻列は以下の優先順位で使います。

1. `reevaluation_at_jst`
2. `reevaluation_at_utc`
3. `evaluation_date`
4. `date`
5. 元の行順

同じ時刻の場合は、`PENDING_REEVALUATIONS` 由来の行を優先します。これは、再評価履歴のほうがより新しい検証結果になりやすいためです。

## 出力

以下を生成します。

- `results/latest_evaluations.csv`
- `results/latest_evaluations.json`
- `results/latest_evaluations_summary.json`
- `reports/evaluations/YYYY-MM-DD_latest_evaluations.md`

追加される主な列は以下です。

- `latest_selected_at_jst`
- `latest_selected_at_utc`
- `latest_source`
- `source_priority`
- `previous_rows_count`
- `has_reevaluation_history`
- `latest_reason`
- `is_latest_evaluation`

## Dashboard連携

Dashboardは評価データとして以下の優先順位を使います。

1. `results/latest_evaluations.csv`
2. `results/pending_reevaluations.csv`
3. `results/evaluations.csv` または Google Sheets `EVALUATIONS`

これにより、古いpending評価と新しいclosed評価が同じ分析内に混ざることを避けます。

Dashboard workflowでは、`build_dashboard.py` の前に `build_latest_evaluations.py` を実行します。失敗した場合でもDashboard生成は続行し、その場合は `最新評価ビュー未取得` と表示されます。

## Google Sheets書き込み

Phase 12.2 ではGoogle Sheetsへ書き込みません。出力はartifactとDashboard表示用です。

将来的には専用シート `LATEST_EVALUATIONS` を作り、最新ビューをGoogle Sheetsへ保存する案があります。ただし、現時点ではappend-only履歴である `PENDING_REEVALUATIONS` を主な永続ログとし、`LATEST_EVALUATIONS` は派生ビューとして扱います。

## 週次・月次・AI Feedback

将来的には、週次レビュー、月次較正、AI Feedbackも `latest_evaluations` を標準入力にする予定です。

Phase 12.2 ではDashboard統合を優先し、週次・月次側の既存挙動は大きく変えません。

## 安全条件

- 実売買は行いません。
- 自動発注は行いません。
- XMや証券会社を操作しません。
- `weights.json` は自動更新しません。
- `generate_signal.py` は自動変更しません。
- Actionsからgit pushしません。
- 既存の `SIGNALS` / `EVALUATIONS` / `PENDING_REEVALUATIONS` は削除・更新しません。
