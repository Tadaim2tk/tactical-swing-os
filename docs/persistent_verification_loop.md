# Persistent Verification Loop

Tactical Swing OS の継続再評価ループは、過去に生成した SIGNALS のうち、まだ決着していない仮想評価を最新OHLCで再評価する仕組みです。

この機能は実売買ではありません。発注、XM操作、ブローカー操作、実資金管理は行いません。`weights.json` の自動更新や `generate_signal.py` の自動変更も行いません。

## 目的

日次の `evaluate_signal.py` は、その日に生成された `results/signals.csv` を評価します。一方で、Google Sheets 上には過去の SIGNALS / EVALUATIONS が蓄積されます。

`src/reevaluate_pending_signals.py` は、蓄積された過去シグナルから pending / open / no_entry / unresolved のものを拾い、最新の `data/raw/{ASSET}.csv` を使って再評価します。

## 入力

優先順位は以下です。

1. GitHub Secrets `GOOGLE_SERVICE_ACCOUNT_JSON` と `GOOGLE_SHEET_ID` がある場合、Google Sheets の `SIGNALS` / `EVALUATIONS` を読む
2. Sheetsが使えない場合、ローカルCSVへfallbackする
   - `results/signals.csv`
   - `results/evaluations.csv`

列名は正規化されます。`Signal ID`、`signal id`、`signal-id`、`signal_id` は同じ列として扱います。

## 再評価対象

以下は再評価対象です。

- `evaluation_status`: `pending`, `open`, `unresolved`, 空欄
- `outcome`: `open_unresolved`, `no_entry`, 空欄
- `status`: `pending`, `open`, `no_entry`, 空欄
- EVALUATIONSにまだ存在しないSIGNALS

以下は対象外です。

- `outcome`: `win_tp1`, `win_tp2`, `loss_sl`, `no_trade_correct`, `no_trade_missed`
- `status`: `closed`
- `evaluation_status`: `closed`

NO_TRADEは初期状態では再評価しません。必要な場合のみ `--include-no-trade` を指定します。

## 出力

以下を生成します。

- `results/pending_reevaluations.csv`
- `results/pending_reevaluations.json`
- `reports/reevaluation/YYYY-MM-DD_pending_reevaluation.md`

出力には既存の評価列に加えて、前回評価との差分確認用の列が入ります。

- `reevaluation_at_jst`
- `reevaluation_at_utc`
- `reevaluation_run_id`
- `previous_status`
- `previous_evaluation_status`
- `previous_outcome`
- `previous_r_multiple`
- `changed_status`
- `changed_outcome`
- `changed_r_multiple`
- `is_latest_evaluation`
- `source`

## Google Sheets書き込み

初期workflowでは Google Sheets へ書き込みません。artifactで結果を確認するだけです。

手動で `--write-sheets` を付けた場合のみ、`EVALUATIONS` へ append-only で追記します。既存行や元のSIGNALSは削除しません。

append-only運用では、同じ `signal_id` に複数の評価行が存在し得ます。そのため、週次レビュー、月次較正、AI Feedbackなどの分析側では、将来的に `reevaluation_at_utc`、`evaluation_date`、行順などを使って最新評価行を採用する必要があります。

将来的には `config/sheets_schema.json` に `results/pending_reevaluations.csv` → `PENDING_REEVALUATIONS` を追加し、EVALUATIONS本体とは別の監査ログとして同期する案もあります。

## workflow

`.github/workflows/reevaluate_pending.yml` は毎日 7:05 JST 相当に実行されます。

処理順は以下です。

1. 依存関係をインストール
2. `python src/fetch_market.py`
3. `python src/reevaluate_pending_signals.py --lookback-days 30 --horizon 10`
4. Markdown / CSV / JSON をartifact保存

初期workflowでは `--write-sheets` を付けません。

Dashboard workflowでも表示用に同じ再評価を試行します。失敗した場合でもDashboard生成は続行し、その場合は `Pending再評価未取得` と表示されます。

## 注意

- この仕組みは仮想評価専用です。
- 実売買、発注、XM操作は行いません。
- 価格データ欠損、休場、市場ごとのデータ更新差により、評価が遅れる場合があります。
- append-only運用では、分析時に最新評価行を選ぶ必要があります。
