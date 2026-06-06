# Tactical Swing OS Dashboard

Tactical Swing OS Dashboard は、日次シグナル、仮想評価、資産別成績、Reason Code分析、Rule Update Proposalを1つのHTMLで確認するための読み取り専用レポートです。

画面の主要な見出し、カード、テーブル列、注意文は日本語表示です。`reason_codes`、`proposal_type`、`target_name` など一部の内部分析コードは、ログとの照合をしやすくするため英語コードのまま残ります。

## 目的

ダッシュボードは、毎日のartifactやGoogle Sheetsに蓄積された結果を人間が確認しやすい形にまとめます。実売買、発注、XM操作、Google Sheetsへの書き込み、`weights.json` の自動更新、`generate_signal.py` の自動変更は行いません。

## データソース

GitHub Actionsで `GOOGLE_SERVICE_ACCOUNT_JSON` と `GOOGLE_SHEET_ID` が設定されている場合は、Google Sheetsの次のシートを読み込みます。

- `MARKET_SNAPSHOT`
- `SIGNALS`
- `EVALUATIONS`

Secretsが未設定、またはSheets読み込みに失敗した場合は、ローカルのCSV/JSONへfallbackします。

- `results/market_snapshot.csv`
- `results/signals.csv`
- `results/evaluations.csv`
- `results/weekly_review.csv`
- `results/monthly_calibration.csv`
- `results/reason_code_analysis.csv`
- `results/rule_update_proposals.csv`
- 対応するJSONファイル

週次・月次・Reason Code・Rule Proposalは、現時点では主にローカルartifactを参照します。runner上に該当ファイルがない場合、そのセクションは「データなし」と表示されます。

## 表示セクション

- `System Status`: 読み込んだ行数、最新レポート日付、データソース
- `Daily Signal Overview`: 最新日のA/B/NO_TRADE件数とシグナル一覧
- `Evaluation Overview`: 勝率、R損益、missed opportunityなどの評価要約
- `Asset Performance`: 資産別のsignal数、評価数、R損益
- `Reason Code Performance`: positive / negative / insufficient data の理由コード
- `No Trade Reason Analysis`: NO_TRADE理由ごとの暫定評価
- `Rule Update Proposals`: ルール更新提案一覧
- `Weekly / Monthly Mode`: 翌週・翌月モードとリスク上限
- `Safety Notes`: 自動売買ではないことの確認

## Rule Update Proposalの扱い

Rule Update Proposalは提案ログとして表示するだけです。`apply_automatically` は `false` 前提で表示し、ダッシュボード生成時に `weights.json` や `generate_signal.py` を変更しません。

## Artifact確認方法

1. GitHubの対象リポジトリを開く
2. `Actions` タブを開く
3. `Tactical Swing OS dashboard` を選ぶ
4. `Run workflow` で手動実行する
5. 成功したrunのartifactから `reports/dashboard/index.html` と `reports/dashboard/dashboard_summary.json` を確認する

## GitHub Pages版の確認方法

GitHub Pagesを使うと、artifact zipをダウンロードせずにブラウザから直接ダッシュボードを確認できます。

1. GitHubの対象リポジトリを開く
2. `Settings` → `Pages` を開く
3. `Build and deployment` の `Source` が `GitHub Actions` になっていることを確認する
4. `Actions` タブで `Tactical Swing OS dashboard` を手動実行、または定期実行を待つ
5. 成功したrunの `deploy-pages` 結果、または `Settings` → `Pages` に表示されるURLから開く

Pagesへ公開される対象は `reports/dashboard` ディレクトリです。`reports/dashboard/index.html` がPagesのルートで開かれ、`dashboard_summary.json` も同じ場所に配置されます。

## GitHub Pages公開時の注意

GitHub Pagesはリポジトリ設定によってpublicに閲覧できる状態になる可能性があります。そのため、ダッシュボードにはSecrets、APIキー、サービスアカウントJSON、個人口座情報、取引口座番号、実資金量、発注情報、ブローカー操作情報を表示しない設計にしています。

現在のダッシュボードは、`SIGNALS`、`EVALUATIONS`、Reason Code分析、Rule Update Proposalなどの分析結果のみを表示します。Google Sheetsからの読み込みは行いますが、Google Sheetsへの書き込みは行いません。

公開URLを共有する場合は、表示内容が研究用の分析結果だけであることを確認してください。このダッシュボードは実売買や発注のための画面ではありません。

## 注意

このダッシュボードは分析・監査・レビュー用です。実売買判断には人間の確認が必要です。Sheets読み込みはサービスアカウントの権限やヘッダー状態に依存するため、読み込みに失敗した場合はローカルCSV/JSONのfallback結果になります。
