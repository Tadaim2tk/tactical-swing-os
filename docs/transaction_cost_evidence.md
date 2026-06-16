# Transaction Cost Evidence (Phase 26)

- 設定ファイル: `config/cost_model.json`
- 実装: `src/cost_model.py`（証拠ガード + 検証）
- 表示: Dashboard の `Transaction Cost Model` セクション
- 前提仕様: [SPEC_TRANSACTION_COST.md](SPEC_TRANSACTION_COST.md)（SPEC-TC-001）

## 目的

ネットR評価を「研究上、現実寄り」にするための**証拠フレーム**。実コスト数値そのものは
**人間が出典付きで記入**する（AIは捏造しない）。Phase 26 では値ではなく、出典メタ・
機械的ガード・表示・docs の「枠」を整える。

ブローカー操作・口座情報・API・Secrets は一切扱わない。

## 証拠主義の機械的強制

**`source` が未設定（空 / `unconfigured` / `placeholder` / `none` / `tbd`）のコストは、
値が非ゼロでも net R 計算に採用されない（無視される）。** これにより、出典のない数値が
黙って評価へ混入することを防ぐ（`src/cost_model.py` の `is_sourced` / `cost_in_price`）。

Dashboard はこの状態を可視化する:
- `unsourced_nonzero` > 0 → 「証拠主義違反」警告（出典なしの非ゼロコストが無視されている）
- `missing_provenance` > 0 → 出典はあるが取得日/責任者が欠落

## 記入方法（人間の作業）

`config/cost_model.json` の各アセットに、出典付きで記入する。

| フィールド | 内容 | 例 |
|---|---|---|
| `spread` | 往復スプレッド（price単位＝建値と同じ通貨/ポイント） | `30.0` |
| `commission_round_turn` | 1往復手数料（price換算） | `0.0` |
| `swap_per_bar` | 1バー保有あたりスワップ/金利（price、正でコスト） | `1.5` |
| `source` | **出典**。実測ログ名 or 公開仕様の参照 | `"XMTrading published spec (BTCUSD)"` |
| `source_date` | 取得日 `YYYY-MM-DD` | `"2026-06-16"` |
| `source_type` | `measured`（実測） / `published_spec`（公開仕様） | `"published_spec"` |
| `responsibility` | この数値の更新責任者 | `"主任研究員"` |

記入後、`_meta.status` を `configured`（または部分設定なら任意のラベル）に更新する。

### 出典の方針

- **measured**: 自分の取引/デモ口座で実測したスプレッド等。ログ名・日付を source に。
- **published_spec**: ブローカーが公開している契約仕様（スプレッド表・スワップ表）。
  参照URL/ページ名と取得日を記録する。**口座操作・発注は不要**。
- 出典が confidence 低い場合は `source_type` を明示し、Dashboard で区別できる。

## 検証

`cost_model.validate_cost_model()` が以下を列挙する:
- `unsourced_nonzero_cost`: 非ゼロだが出典なし（採用されず無視）
- `missing_source_date` / `missing_responsibility`: 出典はあるがメタ欠落

## 安全条件

- 実売買なし / 発注なし / XM・証券会社操作なし / API・Secrets なし
- ネットR はあくまで**研究用の補正**。`weights.json` / `generate_signal.py` は変更しない
- AI は値を捏造しない。値は人間が出典付きで記入する
