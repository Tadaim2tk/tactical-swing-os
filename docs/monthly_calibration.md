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

## 月初の手順（2026-11-09 固定。10月はこの3つが全部抜けた）

GPT 判断の月次較正（`docs/monthly_calibration_YYYY-MM.md`）は、上の機械側レポートとは別物。手順を一つの入口にまとめた。

```bash
python tools/monthly_calibration_run.py --docs     # 先月。遡及コーパス延長 → 数値 → 草稿
```

1. `tools/retro_build_market.py --extend` で遡及コーパス（主役の機械判定）を先月末まで延ばす。
2. `tools/analysis/monthly_calib.py --month YYYY-MM` が、毎月同じ物差しで数値を出す
   （売買頻度 / SL率・SL幅÷ATR10・併走 atr_floor / regime / 主役 / 週次 crypto / invalidation の時系列 /
   併走観測 / win_prob 較正 / 介入の前後14日）。
3. 草稿を `reports/monthly/YYYY-MM_calibration_draft.md` と `docs/monthly_calibration_YYYY-MM.md`（無いときだけ）に書く。
   **数値の採否・ルール変更は書かない。** 「決定待ち」は人間が埋める。

誰が回すか: GitHub Actions `monthly_calibration.yml`（毎月1日 12:30 JST）が草稿を artifact に出す。
docs への PR は Codex の月次自動化 `tso`（毎月1日 12:30）が同じコマンドを回して作る（本文は人間が設定。
2026-10-01・11-01 は本文が仮置きのまま走って何もしていなかった）。自動化の本文は `--extend --docs` で呼ぶ。
延長は既定で行うので `--extend` は明示用の別名（2026-11-11 までは未定義の旗で、そのまま 12/1 を迎えると
exit 2 で草稿が出なかった）。ChatGPT 側の月次タスク
「較正する短期スイングモデル」は 2026-11-09 時点で有効一覧に無い（一時停止または削除）。

