# Ablation Evaluation（Phase 29.3）— 3系統の同一cohort比較

- 実装: `src/evaluate_ablation.py`（validation_suite / dashboard workflow で毎回実行）
- 出力: `results/ablation_cohort.csv`（行単位） / `results/ablation_comparison.csv` /
  `results/ablation_comparison_summary.json` / `reports/ablation/*_ablation_comparison.md`
- テスト: `src/test_evaluate_ablation.py`
- 根拠: [governance_reform_2026-07.md](governance_reform_2026-07.md) Phase 29.3

## 目的

「テキスト（ナラティブ）情報は予測精度に寄与しているか」を主KPI（Brier / calibration /
net R）で継続測定する。3系統（arm）を**完全に同一の cohort**（同じ日×資産×ホライズン、
同じ結果窓）で比較する — 系統ごとに母集団を変えない。

| arm | 予測の作り方 |
|---|---|
| `technical_only` | 各日 d 以前のバーだけで `generate_signal.build_row` を再構成（既存ロジックの as-of 版）。prob = win_prob |
| `text_narrative_only` | Narrative Memory の類似局面検索のみ。top-5 類似日のうち**結果窓が d までに閉じたもの**の類似度加重平均リターンで向きを決定。prob = 加重方向一致率 |
| `technical_plus_text` | テクニカルの向きをテキストが確認/棄却する決定的ルール（下記） |

## 合成ルール（v0・決定的）

- テクニカルが NONE → NONE
- テキストのテクニカル方向確率 `p_text_dir`（同方向: text prob / 逆方向: 1−prob / 向きなし: 0.5）
- `p_text_dir < 0.35` → **見送り**（強い不一致）
- それ以外 → side=テクニカル、prob = (tech_prob + p_text_dir) / 2

## 指標（arm × horizon 5/10/20営業日）

hit率 / avg R（R = 方向つきリターン ÷ 1.2×ATR14。generate_signal の SL 基準と同一）/
net R（`cost_model` 経由。**unconfigured の間は net=gross を正直表示**）/ Brier /
calibration slope / MFE / MAE（Rユニット・経路ベース）/ Sharpe /
**DSR**（`stat_guards.deflated_sharpe_ratio`、n_trials=3系統の多重検定として deflate）。

## lookahead 防止

- テクニカル再構成・ATR・類似検索の TF-IDF fit はすべて各日 d **以前**のデータのみ
- テキスト系統は「d 時点で結果が確定した類似日」だけを方向決定に使用（バー位置で機械判定）
- 結果窓未確定・risk 不定の行は **arm 非依存に全系統で除外**（cohort 対称性を壊さない）

## 正直な状態表示

- `n_actionable >= 30` の行のみ `status=ok`（判断材料）。未満は `insufficient_data`
- cohort が作れない間（局面文書 6日未満 / 価格履歴なし）も `insufficient_data`
- **実装はデータを待たない**: news_narratives が日次で memory を積むと、
  ~2週間で cohort が生まれ、同じコマンドで自動的に数字が出る

## 安全条件

分析・比較専用。実推奨・signal score には未接続（`connected_to_signal_score=false`）。
実売買・発注なし。weights.json / generate_signal.py（実行時）変更なし。
テキスト層を signal へ接続する将来判断は、この ablation の `status=ok` な比較結果と
人間承認PRを経る。

## 改善判定（arm 対比較 / 2026-07-02 司令 B-2 指示で閾値を先行固定）

`compare_arms()` が「semantic類似が予測に効いている」のか「似た説明が見つかっただけ」なのかを
同一 (日,資産,ホライズン) ペアの R 差分で分離する。判定閾値（固定済み・変更は人間PR）:

| verdict | 条件 |
|---|---|
| `improves` | n_pairs>=30 かつ 符号検定 p<=0.05 かつ 平均R差>0 かつ 勝ち>負け |
| `degrades` | n_pairs>=30 かつ 符号検定 p<=0.05 かつ 平均R差<0 |
| `no_significant_difference` | n_pairs>=30 で上記に該当せず |
| `insufficient_data` | n_pairs<30（小標本では判定しない） |

- 符号検定は正確二項（両側・純stdlib）。tie は除外。t検定 p も参考表示。
- 出力: `results/ablation_arm_comparison.csv` + summary json の `arm_comparison` + レポート§3。
- text 層を signal score へ接続する将来判断は `improves` 判定 + 人間承認PRを経る。
