# 仕様凍結: ナラティブ×クオンツ統合 (Narrative Reliability Gate)

- status: **active (frozen)**
- spec_id: SPEC-NQ-001
- frozen_at: 2026-06-11 (JST)
- 実装: `src/build_narrative_reliability.py` / `src/export_narrative_alignment.py` /
  `src/build_monthly_calibration.py` (narrative_edge) / `src/stat_guards.py` (Welch検定)
- 前提仕様: SPEC-SG-001 (統計ガード) / SPEC-RD-001 (decay)

## 1. 目的

AIの文章分析能力(ニュースナラティブ分類)と従来のクオンツ監査ループを統合する。
原則: **AIの言語分析は、数字で信頼を勝ち取って初めて影響力を得る**。

## 2. 構成要素

### 2a. ナラティブ整合の時点記録 (export_narrative_alignment.py)
- シグナル発生時点のナラティブ整合判定(aligned / conflicted / neutral / insufficient_data)を
  `results/signal_narrative_alignment.csv` に **追記専用** で保存する。
- **最初の記録が正**。既存signal_idの行は決して上書き・再計算しない(後知恵バイアス防止)。
- score_market_context(旧score_narratives)に整合計算関数が無い環境では安全にスキップする(日次サイクルを止めない)。

### 2b. ナラティブ優位性検定 (narrative_edge, 月次較正)
- aligned群とconflicted群のR成績を **Welchの2標本t検定** (不等分散、Welch–Satterthwaite自由度)で比較。
- 両群とも n >= 30 (`MIN_SAMPLES_WEIGHT_CHANGE`) が揃うまで判定保留。
- 判定: `narrative_edge_confirmed` / `narrative_inverse`(警告: AI整合判定が有害) / `no_significant_edge` / `insufficient_data`
- Welch実装はscipy非依存・標準ライブラリのみ(数値検証: t=-2.0, df=8 → p=0.0805 でscipy基準値と一致)。

### 2c. ナラティブ別信頼性テーブル (build_narrative_reliability.py)
- ナラティブカテゴリ単位でclosed評価のRを集計し、SPEC-SG-001と同一ゲートを適用:
  - n < 30 → `insufficient_data`
  - p >= 0.05 → `unproven`
  - 有意 + mean > 0 + Sharpe > 0.5 → `strong_positive` (人間レビュー用の重み候補)
  - 有意 + mean < 0 → `strong_negative` (抑制候補)
- SPEC-RD-001のdecay統計(decayed_avg_r / effective_n / decay_divergence)を併記。
- 入力スキーマに寛容: ナラティブ成果物のファイル名・列名は候補リストで解決し、
  signal_id直結が無ければ (asset, date) で結合。入力欠如時はunavailable summaryを生成。

## 3. 安全原則

- 全出力は提案・分析のみ。weights.jsonは更新しない。requires_human_approval=true 固定。
- 凍結済み閾値(SPEC-SG-001)はそのまま参照する。本仕様で新しい閾値は導入しない。

## 4. 適用順序に関する注記

本仕様は2段階で適用可能: まず2cと2a(本PR)、次に2b(stat_guardsへのWelch追加と月次較正統合)。
2bが未適用の間も2a/2cは単独で完全に機能する。

## 5. 変更手続き

本仕様の変更は新spec_idの発行と本ドキュメント更新履歴への追記を必須とする。
