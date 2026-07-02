# Tactical Swing OS — Operational Runbook

> このドキュメントは「研究OSを毎日どう運用・確認するか」の一次手順書です。
> コードの仕様ではなく、人間（主任研究員）が迷わず運用するための背骨です。

## 0. 最重要前提（毎回思い出すこと）

本システムの目的は「**AIの意味ベクトル的な文章判断能力を従来のテクニカル分析に組み込み、
ナラティブ評価を記録し、自己改善を繰り返してスイングトレードの予測精度を高める**」こと。
実売買・発注をしないのは手段の制約であって、「予測精度で勝つための道具」という目的は
変わらない（2026-07 ガバナンス改定で目的を復元。[governance_reform_2026-07.md](governance_reform_2026-07.md)）。

- **実売買・発注・XM/証券会社操作はしない**（不可侵）。Dashboard・レポート・提案は分析出力。
- weights の**本採用（active昇格）は人間承認（PRマージ）必須**。shadow weights の自動計算・
  記録は日次で行ってよい（実推奨には影響しない）。
- 主KPI は**予測精度の改善**（Brier / prediction calibration / net R）。EVALUATIONS 蓄積件数は
  精度計算の分母となる補助指標であり、それ自体は成果ではない。
- 統計的な**採用判断**はデータを待つが、**実装はデータを待たない**。shadow / inactive で先に
  実装し、データが揃い次第ゲートが自動で開く構造を標準とする。
- 監査・ガード・健全性レイヤーは既に十分にある。**新しいガードの追加は、既存ゲートを
  1つ緩和・統合するのとセットでのみ可**（アンチ停滞ルール）。

---

## 1. 自動実行スケジュール（JST）

GitHub Actions が毎日この順で走る（UTC cron を JST 換算）。

| 時刻(JST) | workflow | 役割 |
|---|---|---|
| 06:50 | news_narratives | ニュース取得・ナラティブ分類 |
| 06:55 | daily_cycle | 市場取得 → シグナル生成 → 評価 → レポート → Sheets同期 |
| 07:05 | reevaluate_pending | 未決着シグナルの継続再評価 |
| 07:10 | **dashboard** | 全レイヤー生成 → **Dashboard公開(GitHub Pages)** |
| 07:20 | narrative_lookahead_audit | ナラティブの未来情報混入監査 |
| 07:30 | adversarial_review | 提案レイヤーの横断敵対監査 |
| 土 12:10 | weekly_review | 週次レビュー |
| 1日 12:30 | monthly_calibration | 月次較正 |

> dashboard workflow は内部で各監査も再生成してから公開するため、07:10 時点の
> Dashboard は自己完結している。07:20/07:30 の単独監査workflowは追加のartifact生成。

確認は基本 **公開Dashboard** を見る: https://tadaim2tk.github.io/tactical-swing-os/

---

## 2. 毎朝の確認順序（上から順に5分）

Dashboard を開いて、**この順番**で見る。上ほど「土台の健全性」、下ほど「中身」。

1. **Data Health / Freshness** — まず計器自体が健全か。
   - `health_status` を見る → §3.1 の解釈表へ。
   - `critical/degraded` なら attention_layers を確認し、§4 の一次対応へ。
2. **System Health** — datetime監査（タイムゾーン整合）。
3. **Adversarial Review** — 提案に危険兆候がないか（`review_status`）→ §3.3。
4. **Narrative Lookahead Audit** — ニュース/AI要約に未来情報混入がないか → §3.2。
5. **Audit Report** — 統合状態（PASS/WARNING）。
6. **Prediction Calibration / Narrative Reliability** — AIの確信度・ナラティブの統計的価値。
7. **本日のシグナル概要 / 評価概要 / 資産別成績** — 当日の中身。
8. **週次・月次モード** — 攻撃/通常/防御モードと日次リスク上限。
9. **安全上の注意** — 毎回最後に再確認（これは実売買ではない）。

> 原則: **土台(1〜5)が赤いまま中身(6〜8)を読まない。** 古い/空のデータを
> 正常だと思って読むのが最大の事故源（偽passed / false-fresh と同じ思想）。

---

## 3. ステータスの読み方

### 3.1 Data Health `health_status`

| status | 意味 | 行動 |
|---|---|---|
| `healthy` | 全レイヤー fresh | そのまま中身を読んでよい |
| `watch` | unknown_age または future_timestamp あり | 時刻系の軽い異常。§4へ |
| `degraded` | stale または empty あり | 古い/空のレイヤーがある。中身は割引いて読む |
| `critical` | missing または unavailable あり | 土台データ欠損。**中身を鵜呑みにしない**。§4へ |

> `critical` は「失敗」ではなく「正直な状態表示」。データ蓄積前は critical が普通。
> 重要なのは *criticalだと分かっていること*。

レイヤー別 status: `fresh / stale / empty / missing / unavailable / unknown_age / future_timestamp`
（監査系は0件でも `fresh`＝allow_empty。詳細は [dashboard_health.md](dashboard_health.md)）

### 3.2 Narrative Lookahead Audit `audit_status`

| status | 意味 | 行動 |
|---|---|---|
| `passed` | 未来情報混入なし | OK |
| `warning` | キーワード/評価結果語の混入疑い | 人間が時間軸を確認 |
| `high_risk` | 未来日付の材料が事前ナラティブに混入 | 当該材料を除外 |
| `blocked` | 複数の重大混入 | ナラティブ層を一旦使わない |
| `unavailable` | 監査対象が無い | データ蓄積待ち |

### 3.3 Adversarial Review `review_status`

| status | 意味 | 行動 |
|---|---|---|
| `passed` | 危険兆候なし | OK |
| `warning` | サンプル不足の強提案/過剰最適化/矛盾/過信表現 | 人間が精査 |
| `high_risk` | 高リスクpatch等 | 採用前に個別精査 |
| `blocked` | **自動適用/weights更新/patch適用の痕跡** | 即時に原因停止（§4最優先） |
| `unavailable` | 提案が無い/全て空 | データ蓄積待ち（passedではない＝偽passed防止） |

### 3.4 共通

すべての提案・監査行に `requires_human_approval=true` / `weights_json_updated=false` /
`generate_signal_updated=false` が立っていること。**ここが false/true で崩れていたら異常。**

---

## 4. 異常時の一次対応表

| 症状 | 想定原因 | 一次対応 |
|---|---|---|
| Data Health `critical`、core(signals/evaluations) が `missing` | 市場取得失敗 or daily_cycle未実行 | daily_cycle workflow のログ確認。fetch_market失敗ならRSS/API側。再実行 |
| 多数レイヤーが `stale` | dashboard/validation workflow が失敗で止まった | 直近の workflow run を確認、再実行 |
| レイヤーが `future_timestamp` | 生成側の時計/タイムゾーン異常 | 該当スクリプトの timestamp 生成（time_utils）を確認 |
| Adversarial Review `blocked` | weights_json_updated / patch_applied / apply_automatically が true | **最優先**。どのレイヤーが自動適用したか特定し停止。憲章違反 |
| Narrative Lookahead `high_risk/blocked` | ニュース/AI要約に未来情報混入 | 当該ナラティブを採用判断から除外。辞書/source分類を見直す |
| Audit Report `WARNING` | datetime不整合や評価欠損 | reports/audit の最新mdを読む |
| Dashboard workflow が `Upload Pages artifact` で失敗 | 生成物が出ていない（過去の `__main__`脱落のような） | Build dashboard ステップが実ファイルを出したかログ確認 |
| validation suite が赤 | いずれかのスクリプトが例外 | Step Summary の missing 項目を特定し、該当スクリプトをローカル実行 |

> 共通原則: **「赤い＝壊れた」ではなく「赤い＝正直に異常を表示できている」**。
> 偽の緑（false healthy / false passed / false fresh）の方が危険。

---

## 5. 役割分担（Claude / Codex / 人間）

| 主体 | 役割 |
|---|---|
| **Claude (実装AI)** | 仕様に沿って実装・テスト・ドキュメント。各フェーズで**セルフ敵対監査**(ワークフロー)を回し、自分の書いたコードのバグを潰す。PR作成まで |
| **Codex (レビューAI)** | GitHub上でPRレビュー。スコープ・安全条件・P2級の穴(偽passed等)を指摘 |
| **人間 (主任研究員)** | 研究上の最終判断。PRマージの可否、workflow手動実行、Pages確認、weights/rules/proposals の採否を研究上レビュー。AIは監査される対象であり、人間が監査機。**実資金判断・発注・証券会社操作は Tactical Swing OS の範囲外であり、このworkflowには含めない**（人間の最終判断は本プロジェクト内での発注許可を意味しない） |

ワークフロー（毎フェーズ共通）:
1. 人間が Codex 由来の仕様/方針を提示
2. Claude が実装 → テスト → セルフ敵対監査 → PR
3. Codex がレビュー（P2指摘あれば Claude が同一PRで修正）
4. 人間がマージ判断
5. マージ後、Validation Suite / Dashboard を手動実行 → Pages確認
6. 問題なければ次フェーズ

---

## 6. 安全インバリアント（2026-07 改定。対照表: [governance_reform_2026-07.md](governance_reform_2026-07.md)）

### 不可侵（今後も絶対に変えない）

- 実売買なし / 発注なし / XM・証券会社操作なし
- Secrets を ログ/Dashboard に出さない
- lookahead 防止: `source_published_at_utc <= signal_cutoff_utc` を満たさない文章情報を
  シグナルに使わない
- weights の**本採用（active昇格）は人間承認（PRマージ）必須**
- false green を作らない（`insufficient_data` 等の正直な状態表示を維持）
- 既存テストを黙って削除しない（仕様変更に伴う修正・更新は可）

### 改定済み（旧ルール → 新ルール）

- 「weights.json 自動更新なし」→ **shadow weights の自動計算・記録は許可**。
  active への昇格のみ人間承認。提案・較正・監査の `requires_human_approval=true` は不変
  （shadow 計算は「適用」ではなく「記録」であり、実推奨に影響しない）。
- 「generate_signal.py 自動変更なし」→ 禁止されるのは**実行時の自己書き換え**のみ。
  通常のPRフローによる改修・リファクタ・weights読込機構の追加は普通の開発。
- 「GitHub Actions から git push しない」→ `src / docs / .github` への自動pushは引き続き禁止。
  **`results / reports / data` 配下へのデータ追記コミットのみ Actions bot に許可**
  （学習ループの日次出力の永続化経路）。
- Google Sheets への新規書き込み追加は引き続きしない（永続化は上記 Actions データコミットで行う）。

---

## 7. 関連ドキュメント

- 仕様凍結: [SPEC_STATISTICAL_GUARDS.md](SPEC_STATISTICAL_GUARDS.md) / [SPEC_DEFLATED_SHARPE.md](SPEC_DEFLATED_SHARPE.md) / [SPEC_REGIME_DECAY.md](SPEC_REGIME_DECAY.md) / [SPEC_NARRATIVE_QUANT.md](SPEC_NARRATIVE_QUANT.md) / [SPEC_PREDICTION_CALIBRATION.md](SPEC_PREDICTION_CALIBRATION.md) / [SPEC_TRANSACTION_COST.md](SPEC_TRANSACTION_COST.md)
- レイヤー解説: [dashboard.md](dashboard.md) / [dashboard_health.md](dashboard_health.md) / [narrative_lookahead_audit.md](narrative_lookahead_audit.md) / [adversarial_review.md](adversarial_review.md) / [validation_suite.md](validation_suite.md)
- フェーズ進捗: [phase_status.md](phase_status.md)
