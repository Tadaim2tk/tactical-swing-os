# Google Sheets 自動保存セットアップ

Tactical Swing OS は、GitHub Actions で生成した `market_snapshot`、`signals`、`evaluations` を Google Sheets に追記できます。

この同期は任意機能です。GitHub Secrets に `GOOGLE_SERVICE_ACCOUNT_JSON` と `GOOGLE_SHEET_ID` が両方設定されている場合だけ実行されます。未設定の場合は `Sheets sync skipped` と表示して正常終了します。

## 1. Google Cloud で Service Account を作る

1. Google Cloud Console を開きます。
2. 対象プロジェクトを選びます。まだ無い場合は新しいプロジェクトを作成します。
3. `IAM と管理` から `サービス アカウント` を開きます。
4. `サービス アカウントを作成` を押します。
5. 名前を入力します。例: `tactical-swing-os-sheets`
6. 作成を完了します。ロールは最小構成で問題ありません。Google Sheet 側で個別に編集権限を付与します。

## 2. Google Sheets API を有効化する

1. Google Cloud Console の `API とサービス` を開きます。
2. `ライブラリ` を開きます。
3. `Google Sheets API` を検索します。
4. `有効にする` を押します。

## 3. サービスアカウント JSON を取得する

1. 作成したサービスアカウントを開きます。
2. `キー` タブを開きます。
3. `鍵を追加` から `新しい鍵を作成` を選びます。
4. キーのタイプは `JSON` を選びます。
5. ダウンロードされた JSON ファイルの全文を GitHub Secrets に保存します。

## 4. 保存先 Google Sheet を作る

1. Google Sheets で新しいスプレッドシートを作成します。
2. URL から Spreadsheet ID を控えます。

例:

```text
https://docs.google.com/spreadsheets/d/<ここがGOOGLE_SHEET_ID>/edit
```

同期時に以下のシートが必要に応じて作成されます。

- `MARKET_SNAPSHOT`
- `SIGNALS`
- `EVALUATIONS`
- `WEEKLY_REVIEW`
- `MONTHLY_CALIBRATION`
- `PARAMETERS`

## 5. サービスアカウントに編集権限を付与する

1. サービスアカウント JSON 内の `client_email` を確認します。
2. 保存先 Google Sheet の `共有` を開きます。
3. `client_email` のメールアドレスを追加します。
4. 権限を `編集者` にします。

この共有を忘れると、GitHub Actions から Google Sheet を開けません。

## 6. GitHub Secrets を設定する

GitHub リポジトリで以下を設定します。

1. `Settings` を開きます。
2. `Secrets and variables` から `Actions` を開きます。
3. `New repository secret` を押します。
4. 以下の2つを追加します。

| Secret名 | 値 |
| --- | --- |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | サービスアカウント JSON ファイルの全文 |
| `GOOGLE_SHEET_ID` | 保存先 Google Spreadsheet ID |

## 7. Actions を手動実行して保存確認する

1. GitHub の `Actions` タブを開きます。
2. `Tactical Swing OS daily cycle` を選びます。
3. `Run workflow` を押します。
4. branch は `main` を選びます。
5. 実行ログで `Sync to Google Sheets` が成功していることを確認します。
6. Google Sheet に `MARKET_SNAPSHOT`、`SIGNALS`、`EVALUATIONS` が追記されていることを確認します。
7. artifact も引き続き保存されていることを確認します。

## 安全条件

- 実売買はしません。
- 発注はしません。
- XM 操作はしません。
- GitHub Actions から git commit / git push はしません。
- Google Sheets には生成済み CSV の内容だけを追記します。
