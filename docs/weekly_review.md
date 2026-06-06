# 週次レビュー

`src/build_weekly_review.py` は、直近の `results/signals.csv`、`results/evaluations.csv`、`results/market_snapshot.csv` を読み、週次レビューを生成します。

出力:

- `reports/weekly/YYYY-MM-DD_weekly_review.md`
- `results/weekly_review.csv`
- `results/weekly_review.json`

デフォルトでは実行日を含む過去7日を集計します。期間を固定したい場合は次のように指定できます。

```bash
python src/build_weekly_review.py --start 2026-06-01 --end 2026-06-07
```

この処理は分析と仮想評価の集計だけを行います。実売買、発注、XM操作、GitHub Actionsからのgit pushは行いません。
