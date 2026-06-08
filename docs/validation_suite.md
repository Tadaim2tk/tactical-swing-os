# Validation Suite

`Tactical Swing OS validation suite` は、PRマージ後や大きな変更後に主要な分析パイプラインをまとめて確認するための手動実行workflowです。

## 目的

個別のworkflowを何度も手動実行せずに、以下の処理が一通り通るかを確認します。

- 市場データ取得
- ニュース取得とニュースナラティブ分類
- pending signalの再評価
- latest evaluations生成
- AI feedback生成
- weekly review生成
- monthly calibration生成
- reason code analysis生成
- rule update proposals生成
- model state update proposals生成
- dashboard生成

## 実行方法

1. GitHubの `Actions` タブを開く
2. `Tactical Swing OS validation suite` を選ぶ
3. `Run workflow` を押す
4. 実行完了後、Step Summaryとartifactを確認する

## 確認できる成果物

workflowは以下をartifactとして保存します。

- `reports/**/*.md`
- `reports/dashboard/index.html`
- `reports/dashboard/dashboard_summary.json`
- `reports/model_state/*.md`
- `results/*.csv`
- `results/*.json`

Step Summaryには、主要なCSV/JSON/HTMLが生成されたかどうかが表示されます。

## 安全条件

このworkflowは検証専用です。

- Google Sheetsへの書き込みは行いません
- `sync_to_sheets.py` は実行しません
- `reevaluate_pending_signals.py` に `--write-sheets` は付けません
- 実売買は行いません
- 発注は行いません
- XMや証券会社の操作は行いません
- `weights.json` は自動更新しません
- `generate_signal.py` は自動変更しません
- GitHub Actionsからgit pushしません

Google Sheetsからの読み込みは、蓄積データを使った分析確認のために許可しています。

## Dashboard Pagesについて

このworkflowはDashboard HTMLをartifactとして生成しますが、GitHub Pagesへのdeployは行いません。

GitHub Pages上の表示を更新したい場合は、別途 `Tactical Swing OS dashboard` workflowを実行してください。

## ニュース取得について

ニュース取得は外部RSSに依存します。RSS側の遅延や一時的な失敗があっても、validation suite全体は続行します。その場合、Step Summaryやログでwarningを確認してください。
