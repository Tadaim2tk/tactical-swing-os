# JP One-Share Swing Ledger — 運用ガイド

- 実装: `src/jp_swing_ledger.py` / `src/jp_swing_evaluate.py` / `src/jp_one_share_cost.py` / `src/jp_calendar.py` / `src/jp_adversarial_checklist.py`
- 入力: `data/jp_swing_signals.csv`（仮説台帳）/ `data/jp_swing_pass_log.csv`（見送りログ）
- 出典: `config/jp_cost_model.json`（ワン株コスト・証拠主義）
- 関連spec: JP-LEDGER-001 / JP-EVAL-001 / JP-COST-001 / JP-CAL-001 / JP-ADV-001

## 何のためのものか

JP個別株スイング仮説の **記録・検証・振り返り台帳**。実売買・発注・証券会社操作は一切しない。
研究上の仮説ライフサイクル（採用・見送り・約定・評価）を残し、後知恵バイアスなく学習する。

> **これは実売買判断ではない**。Ledger に書いた仮説は発注命令ではない。
> 実際の発注は Tactical Swing OS の範囲外（人間が自分の判断で行う）。

## 設計の核心：4日付分離（lookahead防止）

| 列 | 意味 |
|---|---|
| `decision_date` | 仮説を形成した日。**これ以降の情報は使ってはいけない**（事後情報の混入禁止） |
| `intended_order_date` | 注文予定日（標準: `decision_date` の翌営業日。`src/jp_calendar.py` で計算） |
| `assumed_execution_date` | 想定約定日（標準: `intended_order_date` の翌営業日 = `decision_date + 2営業日`） |
| `actual_execution_date` | 実際の約定日（約定後に記入） |

**lookahead 防止の前提**: `decision_date` 時点で知り得ない情報（後日の値動き・後発の発表）を、
narrative や falsifier に書き込まない。日付順序（decision ≤ intended ≤ assumed）はバリデータが検査する。

## 毎日の運用ループ

### ステップ1: 仮説検討 → adversarial checklist で採否判定

```python
import jp_adversarial_checklist as adv

# 各 CheckItem(ADV-JP-001 …) に対し、 "pass" / "fail" / "n/a" で回答
answers = {"ADV-JP-001": "pass", "ADV-JP-002": "fail", ...}

decision = adv.adoption_decision(answers)
# decision["decision"] は次のいずれか:
#   "adopt_eligible"     — 採用条件を満たす
#   "pass_recommended"   — high fail 2件以上 → 見送り推奨
#   "blocked"            — critical fail 1件でも → 採用禁止
#   "insufficient_data"  — 未回答3件以上 → 全項目に答えてから再判断
```

「答えられない」は「見送り推奨」を意味する（false-confidence rule）。
チェックリスト全文は `adv.checklist_text()` で取得。

### ステップ2: 採用 → `jp_swing_signals.csv` に1行追記

最低限の必須フィールド（`validate_signal_row` が検査）:

| 必須 | 説明 |
|---|---|
| `hypothesis_id` | 一意ID（例: `2026-06-16-7203`） |
| `decision_date` | 仮説を形成した日 |
| `intended_order_date` | 注文予定日 |
| `assumed_execution_date` | 想定約定日 |
| `ticker` | yfinance 形式（例: `7203.T`） |
| `narrative` | 仮説の中身（決定日時点の情報のみ） |
| `falsifier` | **仮説崩壊条件**（必須、事前に決める） |
| `horizon_days` | `10` / `20` / `30` のいずれか |
| `confidence_pct` | 0〜100 |
| `status` | `pending` / `open` / `closed` |

`catalyst_type` は `{theme, order_backlog, pricing_power, structural_change, earnings_beat, margin_improvement, other}`、
`falsifier_type` は `{price, fundamental, catalyst, timing, market_regime}`。
列定義の全体は `src/jp_swing_ledger.py` の SIGNAL_COLUMNS を参照。

### ステップ3: 見送り → `jp_swing_pass_log.csv` に1行追記

採用しなかった検討も**学習資産として記録**する。後日 followup で再評価。

### ステップ4: 検証CLI（読み取り専用）で入力ミスをチェック

```bash
python src/jp_swing_ledger.py
```

出力例:
```
Signals:  3 rows loaded from data/jp_swing_signals.csv
Pass log: 1 rows loaded from data/jp_swing_pass_log.csv
[signals] 1 行に問題があります:
  row 2 2026-06-16-7203
    - falsifier が未記入です。事前に仮説崩壊条件を決めてください。
[pass_log] OK — 0 件の問題
```

問題があれば exit code 1。CIや pre-commit でも使える。
**ネットワーク無し・読み取り専用。発注・broker操作は一切行わない。**

オプション:
- `--signals PATH` 仮説CSVのパス（デフォルト `data/jp_swing_signals.csv`）
- `--pass-log PATH` 見送りログのパス（デフォルト `data/jp_swing_pass_log.csv`）

### ステップ5: 約定後の評価（`jp_swing_evaluate`）

約定後、`actual_execution_date` を記入してから評価:

```python
import jp_swing_evaluate as ev

# 1仮説の評価(yfinance で OHLCV を取得して MFE/MAE/outcome を判定)
result = ev.evaluate_signal(signal_row, ohlcv=None)  # ohlcv=None なら yfinance 自動取得

# 全仮説のサマリー
summary = ev.summarize(signals_df)
```

`outcome_type` (A〜F) は補助的な自動推定で、最終的な `thesis_correct / timing_correct / execution_degraded` は**人間が判断して記入**（機械的に決定できない領域は人間に残す）。

## 安全条件（全フェーズ不変）

- 実売買なし / 発注なし / XM・証券会社・SBI・楽天・マネックス操作なし
- API キー・口座情報・Secrets を扱わない
- `weights.json` / `generate_signal.py` 変更なし
- Google Sheets への新規書き込みなし
- yfinance は **過去 OHLCV データ取得のみ**（発注機能は使わない）
- 検証CLI は読み取り専用（CSVを書き換えない）
- `data/jp_swing_*.csv` への記入は **人間の手動編集**（バッチ自動生成しない）

## False-confidence rule（憲章の継承）

- 「答えられない」「データ不足」→ **採用しない / 不明扱い**
- outcome が判定できない → `open_unresolved`（passed にしない）
- adversarial checklist の critical fail 1件で **採用禁止**
- decision_date 以降の情報は narrative に書かない

## 関連ドキュメント

- 全体運用: [operations_runbook.md](operations_runbook.md)
- 安全境界: [SPEC_TRANSACTION_COST.md](SPEC_TRANSACTION_COST.md) / [transaction_cost_evidence.md](transaction_cost_evidence.md)
- Spec repo: SAFETY_RULES.md / PHASE_STATUS.md
