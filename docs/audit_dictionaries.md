# Audit Dictionaries (Externalization & Tuning)

- 設定: `config/audit_dictionaries.json`
- 実装: `src/audit_dictionaries.py`（ローダー + 語境界マッチャー）
- 利用: `audit_narrative_lookahead.py` / `audit_adversarial_review.py` / `classify_news_narratives.py`
- テスト: `src/test_audit_dictionaries.py`

## 目的

ルールベース監査の語彙辞書を**コードから config へ外部化**し、運用しながら育てられる
ようにする。今回のスコープは **データ駆動の重み調整ではなく**、カバレッジ拡充・
誤検知低減・例ロックである（EVALUATIONS 蓄積後にデータ駆動の調整へ進む）。

## 何を外部化したか

| セクション | キー | 利用先 |
|---|---|---|
| `narrative_lookahead` | `future_keywords_en` / `future_keywords_ja` / `outcome_terms` | Narrative Lookahead Audit |
| `adversarial_review` | `overconfidence_terms_ja` / `overconfidence_terms_en` | Adversarial Review |
| `news_narrative` | テーマ別 `*_news_score` キーワード（risk_on/risk_off/geopolitical/inflation 等） | News Narrative |

## マッチャー（誤検知低減）

`audit_dictionaries.match_terms(text, terms)`:
- **英語（ASCII）語は語境界マッチ**。`"certain win"` は `"uncertain win"` に当たらず、
  `"war"` は `"warning"` / `"reward"` / `"toward"` に当たらない。
- **日本語は部分一致**（語境界が無いため）。`"引け後"` は文中で従来どおり一致。
- 大文字小文字無視、結果は重複排除・ソート。

実装は `(?<![a-z0-9]) term (?![a-z0-9])` の正規表現で、ASCII語にのみ実効的な境界を課す。

## 安全フォールバック

`config/audit_dictionaries.json` が**欠損・破損・部分定義**でも、
`src/audit_dictionaries.py` の `DEFAULTS` へトップレベルキー単位でフォールバックする。
空リスト指定も無効として DEFAULTS を採用。既存挙動を壊さない。

## チューニング方法（運用）

`config/audit_dictionaries.json` を編集して語彙を追加/調整する。**コード変更不要**。
- 英語の短い汎用語は誤検知を招きやすいので、可能なら複数語フレーズを使う。
- 追加後は `src/test_audit_dictionaries.py` のラベル付き例（true positive / true negative）に
  ケースを足して挙動をロックする。

## 安全条件

- 分析・監査専用。`weights.json` / `generate_signal.py` は変更しない。
- LLM API・有料APIの新規利用なし。実売買・発注・Sheets書き込みなし。
- データ駆動の重み調整は本フェーズの範囲外（EVALUATIONS 蓄積後）。
