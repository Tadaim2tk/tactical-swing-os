# Narrative Lookahead Audit

- 実装: `src/audit_narrative_lookahead.py`
- テスト: `src/test_narrative_lookahead.py`
- workflow: `.github/workflows/narrative_lookahead_audit.yml`（毎日 07:20 JST / 手動）

## 目的

ニュースナラティブやAIフィードバックなどの文章系分析に、**未来情報・評価後情報・結果情報**が混入していないかを監査する。新しい予測ロジックではなく、**研究プロセスの時間軸汚染を防ぐ補助レイヤー**である。

憲章の実装:
- 「後知恵バイアスこそ最大の敵」「結果を見てから理由を作ることが最も危険」
- 「AIは監査される対象」（AUDIT-001: AIが結果から逆算した事故の再発防止）

## 何を監査するか

| 観点 | 内容 |
|---|---|
| 1. 時系列 | 文章の日時（headline published / generated_at）が分析対象時点（signal_date）より後でないか |
| 2. 未来キーワード | 「引け後」「after the close」など結果判明後でないと書けない表現 |
| 3. 評価結果混入 | `outcome` / `r_multiple` / `loss_sl` 等が**事前材料**に混入していないか |
| 4. source separation | `pre_signal_news` / `post_signal_news` / `evaluation_feedback` / `retrospective_analysis` / `unknown_timing` に分類 |
| 5. risk level | `passed` / `warning` / `high_risk` / `blocked` / `unavailable` |

**評価結果を「振り返り」として使うのは許可**される（AIフィードバック等）。問題は「当日の事前材料」と混同する場合のみ警告する。

## risk level の判定

- 事前材料ソース（news）で `narrative日時 > signal日時` → **high_risk**（未来日付参照）
- 未来情報キーワード検出 → **warning** 以上
- 事前材料ソースに評価結果語が混入 → **warning**
- 上記が複数重なる → **blocked**
- 比較材料が無い → **unavailable**

## 出力

- `results/narrative_lookahead_audit.csv`
- `results/narrative_lookahead_audit.json`
- `results/narrative_lookahead_audit_summary.json`
- `reports/narrative/YYYY-MM-DD_narrative_lookahead_audit.md`

`audit_status` は `blocked > high_risk > warning > unavailable(total=0) > passed` の優先順位で決まる。

## 安全条件

- 監査結果は**提案・警告のみ**。`weights.json` / `generate_signal.py` は一切変更しない（各行に `weights_json_updated=false` / `generate_signal_updated=false` を記録）。
- `requires_human_approval` は常に `true`。最終判断は人間が行う。
- **LLM API・有料ニュースAPIは新規利用しない**。蓄積済みCSV/JSONのみを読む。
- Google Sheetsへの書き込みなし。実売買・発注なし。

## Dashboard / Validation Suite 統合

- Dashboard に `Narrative Lookahead Audit` セクションを表示（status / 件数 / max score / 詳細テーブル）。
- Validation Suite と Dashboard workflow の両方で毎回生成・検証する。
