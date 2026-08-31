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

## 出力契約 v2（2026-07-15）— 採点で実際に起きた事故への対応

採点済み台帳のレビュー（2026-07-15、n=131）で以下の欠陥が判明し、
`prompts/tso_daily_signal_log.md` を**全経路共通の契約 v2** に改定した。
ChatGPT アプリ側のプロジェクト指示も v2 の内容に差し替えること（アプリ側の旧指示が
残っていると同じ事故が再発する）。

| 事故 | 件数 | v2 での対応 |
|---|---|---|
| ETH が価格系列外で採点不能（invalid_data） | 10 | ETH をユニバースに追加（fetch_market.py: ETH-USD）。既存10行は次回採点で自動回復 |
| NASDAQ を QQQ 水準（700台）で記帳 → scale_mismatch | 6 | 資産ごとの参照系列・桁の目安表を契約に明記（NASDAQ = NQ 先物 29,000 前後） |
| asset=NONE の行が混入 → 採点不能 | 2 | asset=NONE 禁止。「何もない日」は全資産 NO_TRADE 行で表現 |
| QQQ 等リスト外資産の行 | 1 | ユニバース10資産に固定。リスト外は本文のみ |
| actionable 行の entry/sl 欠落（ETH 6/21 など） | 1+ | A/B 行の必須項目リストを明記（欠けると「記録が死ぬ」と警告） |
| NO_TRADE 行の ems 等スコア欠落 | 13 | NO_TRADE 行もスコア6種+no_trade_score+regime を必須化 |
| 日次ブロックの欠測（7/8 など） | — | 全資産 NO_TRADE の日も csv ブロック省略禁止を明記 |

経路1（アプリ貼り付け）・経路2（gpt_terminal）とも同一契約。signal_id は台帳の既存形式
`YYYYMMDD_ASSET_SIDE_TYPE` に統一（旧 TSO-YYYYMMDD-NNN 連番は廃止）。

## 主役申告の記録（2026-09-01 changelog(13)）

route-3 取込の際、GPT本文の「本日の市場の主役」1語を追記型台帳へ記録する（LOG28列は不変のため本文からの転記が必要。10月月次でコーパスの機械判定LEADER_V1との一致率を比較する）:

```
python tools/record_leader.py <日付> <資産名>
```

記録先: data/leader_observations.csv（append-only、同日重複は拒否）。
