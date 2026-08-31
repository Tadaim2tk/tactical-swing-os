# 週次レビュー

`src/build_weekly_review.py` は、週次レビューを生成します。

Phase 29以降、ChatGPT/GPTの日次判断は `data/signal_log.csv` に蓄積され、
`data/prediction_log_scores.csv` で全判断（A/B/NO_TRADE）を遡及採点します。
週次期間内にこの予測台帳の行がある場合、週次レビューは人間向けの主集計として
`data/signal_log.csv` / `data/prediction_log_scores.csv` を優先します。

予測台帳がない場合は従来通り、直近の `results/signals.csv`、
`results/evaluations.csv`、`results/market_snapshot.csv` を読みます。
Google Sheetsの `SIGNALS` / `EVALUATIONS` / `MARKET_SNAPSHOT` が利用できる場合は
そこから読み、Secrets未設定または読み込み失敗時はローカルCSVへfallbackします。

出力:

- `reports/weekly/YYYY-MM-DD_weekly_review.md`
- `results/weekly_review.csv`
- `results/weekly_review.json`

デフォルトでは実行日を含む過去7日を集計します。期間を固定したい場合は次のように指定できます。

```bash
python src/build_weekly_review.py --start 2026-06-01 --end 2026-06-07
```

この処理は分析と仮想評価の集計だけを行います。実売買、発注、XM操作、GitHub Actionsからのgit pushは行いません。
予測台帳を週次レビューに使う場合も、ライブシグナル評価へ接続せず、読み取り専用の集計として扱います。
