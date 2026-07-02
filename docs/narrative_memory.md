# Narrative Memory v0（Phase 29.2）— 意味ベクトル層の導入

- 実装: `src/build_narrative_memory.py` / `src/retrieve_similar_narratives.py` / `src/evaluate_narrative_similarity.py`
- ストア: `data/narrative_memory.csv`（git追跡。news_narratives workflow が data/ のみ追記コミット）
- 出力: `results/narrative_memory_summary.json` / `results/similar_narrative_cases.csv|json` /
  `results/similar_narrative_summary.json` / `results/narrative_similarity_evaluation.csv|json` /
  `reports/narrative/*_similar_narratives.md` / `*_narrative_similarity_evaluation.md`
- Dashboard: Tier ③「類似局面検索（Narrative Memory v0）」
- テスト: `src/test_narrative_memory.py`
- 根拠: [governance_reform_2026-07.md](governance_reform_2026-07.md) §2 #14 / Phase 29.2

## 目的

ニュース見出しを時刻フィールド付きの narrative record として蓄積し、
「**今日の局面は過去のどの局面に似ているか**」「**その類似局面の後、5/10/20営業日で
何が起きたか（実リターン）**」を毎日提示する。v0 は**表示・記録のみ**で
signal score には接続しない（`connected_to_signal_score=false`）。

## 必須時刻フィールド（lookahead 防止・不可侵 #3）

| フィールド | 意味 |
|---|---|
| `observed_at_utc` | 我々が情報を観測した時刻（news の fetched_at_utc） |
| `source_published_at_utc` | 情報源の公表時刻（欠損 = 検証不能 → 除外） |
| `ingested_at_utc` | memory への取込時刻 |
| `signal_cutoff_utc` | この record が材料になり得る最初のシグナル生成時刻（observed 以降の最初の 21:55 UTC = daily_cycle cron） |
| `allowed_for_signal` | `source_published_at_utc <= signal_cutoff_utc` を満たすときのみ true |

- `allowed=false` の record は store に残る（監査可能）が、検索からは**機械的に除外**。
- 公表 > cutoff は `cutoff_violation=true`。**lookahead audit が接続監視**:
  `allowed_with_violation_count > 0`（=除外の破れ）を検出したら high_risk を出す
  （`check_narrative_memory`）。正常時は findings なし。

## 検索（as-of・lookahead-safe）

- allowed record を `memory_date`（そのrecordが材料になるシグナル実行日）毎に連結して「局面文書」を作る。
- 基準日の文書 vs **基準日より前**の文書のみでコサイン類似度 → 上位5日。
- 各類似日の +5/10/20 営業日リターンを `data/raw` の実価格から付す
  （未来バー不足は `awaiting_horizon`、価格なしは `no_price_data` の正直表示）。
- 過去局面が5日分未満なら `insufficient_data`（**実装はデータを待たない**: 溜まれば自動で出る）。

## embedding provider（環境変数切替・フォールバック必須）

| 設定 | 挙動 |
|---|---|
| `TSO_EMBEDDING_PROVIDER=openai` + `OPENAI_API_KEY`（Actions secret） | OpenAI embeddings（`TSO_EMBEDDING_MODEL`、既定 text-embedding-3-small） |
| 未設定 / API失敗 | **TF-IDF ローカルフォールバック**（純numpy・依存追加なし・日本語は文字bigram）で必ず動く |

キー登録は人間タスク（Issue化済）。キーをログに出さない。

## 予測力の検証（evaluate_narrative_similarity）

過去の各局面日 d について top-1 類似日 s（d 以前のみから as-of 検索。TF-IDF も
d 以前の文書だけで fit = 未来語彙の混入なし）を取り、d と s の直後リターンの
**方向一致率**を資産×ホライズン別に集計。n>=30 で判断材料（それまで insufficient_data）。

## 安全条件

- signal score 未接続（v0）。実売買・発注なし。weights.json / generate_signal.py 変更なし。
- 将来 score へ接続する場合は ablation（Phase 29.3）の比較結果と人間承認PRを経る。
