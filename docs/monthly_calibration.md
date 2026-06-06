# 月次較正

月次較正は、Tactical Swing OS の過去約1か月分の `SIGNALS` と `EVALUATIONS` を集計し、翌月の暫定方針と重み変更案を確認するためのレビューです。

このフェーズでは、`models/weights.json` を自動更新しません。現在は評価データがまだ少ないため、成績に偶然の偏りが入りやすく、少数サンプルで売買ロジックや重みを自動変更すると判断が不安定になります。

当面は、月次レポートに「提案」として小さな変更幅だけを出します。closed評価が30〜50件以上たまってから、本格的な較正や自動適用の可否を検討します。

## 出力ファイル

- `reports/monthly/YYYY-MM-DD_monthly_calibration.md`
- `results/monthly_calibration.csv`
- `results/monthly_calibration.json`
- `models/weights.json`

## 見方

- `月次サマリー`: 全体の勝率、R損益、翌月モードを確認します。
- `資産別較正`: どの資産が相対的に良いか、悪いかを確認します。
- `Rank別較正`: A/B/NO_TRADE の判定が期待通りに働いているかを確認します。
- `Side別較正`: LONG/SHORT/NONE の偏りを確認します。
- `重み変更案`: あくまで提案です。`models/weights.json` は自動更新されません。

この処理は分析と仮想評価の集計だけを行います。実売買、発注、XM操作、Google Sheetsへの書き込み、GitHub Actionsからのgit pushは行いません。
