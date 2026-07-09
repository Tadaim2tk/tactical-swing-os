# Daily Log Ingestion（Phase 29.7）— ChatGPT 日次出力の検証付き取込

- 実装: `src/ingest_daily_log.py`（取込・全経路共通）/ `scripts/tso_daily_gpt.sh`（ターミナルGPT生成）/
  `prompts/tso_daily_signal_log.md`（出力契約プロンプト）
- テスト: `src/test_ingest_daily_log.py`
- 原則: 設計書 §6「全判断採点の原則」— 取込は広く・警告は正直に・黙って捨てない

## 3つの経路（併用可・origin 列で成績を経路別比較できる）

### 経路1: ChatGPT アプリの出力を貼って取込（現行運用の置き換え・最小変更）

ChatGPT の日次レポートを丸ごとファイルに貼る（```csv ブロックを自動抽出する。整形不要）:

```bash
pbpaste > inbox/2026-07-10.md          # クリップボードから（または手で貼る）
python src/ingest_daily_log.py --file inbox/2026-07-10.md --origin chatgpt_app
# プレビュー確認後:
python src/ingest_daily_log.py --file inbox/2026-07-10.md --origin chatgpt_app --apply
```

Claude セッション内なら「これ取り込んで」と貼るだけでよい（Claude が同コマンドを実行する）。

### 経路2: ターミナル GPT（codex exec）で生成 → 検証 → 取込

codex CLI（ChatGPT アカウント認証済み・web検索有効）で日次ログを生成:

```bash
./scripts/tso_daily_gpt.sh
# -> inbox/YYYY-MM-DD_daily_log_gpt.md 生成 + dry-run プレビューまで自動
# 内容確認後に --apply（human-in-the-loop を維持。自動 apply はしない）
```

プロンプトは `prompts/tso_daily_signal_log.md`（出力契約: 必ず既定ヘッダの csv ブロックを含む）。
ChatGPT アプリ側の会話メモリは引き継がれないため、**品質は経路別比較で検証してから**
主経路を決める（下記）。

### 経路3: Claude によるブラウザ読み取り（スポット確認用）

Claude Code セッションで「ChatGPT のタブを読んで取り込んで」と依頼すれば、
Chrome 拡張経由で開いているチャットからレポートを読み取り、経路1と同じ検証付き取込を行う。
（常用ではなく、貼り忘れ時の回収・照合用）

## 取込時の検証（ingest_daily_log.py）

- 3形式自動判別: markdown 中の ```csv ブロック / 生CSV（ヘッダ有無両対応）/ JSON配列
- 全行に verdict: `append` / `skip_duplicate`（既存 signal_id）/ `reject`（date不正・ID空のみ。理由表示）
- 警告（記録は許可・人間に見せる）: 未知 asset / enum 外 side・rank / entry・SL 不整合 /
  **記録水準が実価格と桁違い**（6/9 NASDAQ の QQQ 水準事故を入口で検知）
- 既定 dry-run。`--apply` で追記し、遡及採点（score_prediction_log）まで自動実行
- `origin` 列（chatgpt_app / gpt_terminal / manual）を台帳に付与

## 経路の優劣はデータで決める

origin 列 × `data/prediction_log_scores.csv` により、**「ChatGPT アプリの判断」と
「ターミナル GPT の判断」の予測成績（勝率・R・Brier 相当）を経路別に比較できる**。
n が溜まるまで両方走らせ、統計ゲート（n>=30）を満たしてから主経路を人間が決める。

## 安全条件

- 取込は台帳（data/signal_log.csv）への追記のみ。ライブ評価ループの真実源にはしない
- codex 実行は read-only サンドボックス。自動 apply はしない（人間確認を挟む）
- 実売買・発注なし。signal score 未接続
