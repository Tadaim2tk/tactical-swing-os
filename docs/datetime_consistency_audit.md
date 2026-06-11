# Datetime Consistency Audit

Datetime Consistency Audit は、Validation Suiteの安定性を上げるために、日付型・時刻型・timezone境界の不安定要素を検出する品質確認レイヤーです。

この監査は分析用のチェックであり、取引判断や自動適用には使いません。

## 背景

`build_weekly_review.py` で `datetime.date` と `pandas.Timestamp` の比較が混在し、Validation Suite中に例外が発生するケースが確認されました。

Meta LearningやProposal Impactは期間集計に依存するため、日付処理の安定化を優先します。

## 監査対象

- `src/build_weekly_review.py`
- `src/build_monthly_calibration.py`
- `src/build_ai_feedback.py`
- `src/measure_proposal_impact.py`
- `src/build_meta_learning.py`
- `src/build_dashboard.py`
- `src/evaluation_loader.py`

対象ファイルが存在しない場合は、`missing_target` としてinfo記録します。監査workflow自体は失敗させません。

## 検出するもの

- `datetime.date` と `pandas.Timestamp` の比較混在
- timezone naiveな `datetime.now()` / `datetime.today()`
- timezoneを外す境界処理
- UTC/JSTの明示箇所
- 文字列日付変換

## 出力

- `results/datetime_audit.csv`
- `results/datetime_audit.json`
- `results/datetime_audit_summary.json`
- `reports/system/YYYY-MM-DD_datetime_audit.md`

## 推奨対応

- 期間比較は `pd.Timestamp(...).normalize()` に寄せる
- 現在時刻は `time_utils.now_utc()` / `time_utils.now_jst()` を使う
- JST/UTCの表示ラベルを明示する
- timezoneを外す場合は、その境界を意識して処理する

## Safety

- `weights.json` は更新しません
- patchは適用しません
- Google Sheetsへの書き込みは行いません
- 実売買・発注・XM操作は行いません
- `generate_signal.py` は変更しません
