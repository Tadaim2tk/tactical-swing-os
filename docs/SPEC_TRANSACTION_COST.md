# 仕様凍結: 取引コストモデル (ネットR評価)

- status: **active (frozen)**
- spec_id: SPEC-TC-001
- frozen_at: 2026-06-15 (JST)
- 実装: `src/cost_model.py` / `config/cost_model.json`
- 適用箇所: `src/evaluate_signal.py`

## 1. 目的

仮想評価の **グロスR**(スプレッド・手数料・スワップを無視した理論値)を、
実戦の **ネットR**(コスト控除後)へ変換する。XMTradingで10万円から実資金を
運用する段階では、「紙の上の勝ち筋」と「実際に資金が増える筋」を分離する必要がある。

LLM/自動売買研究で最大の落とし穴は執行コストを無視した成績である
(arXiv:2606.08285 "Execution Assumptions and Reproducibility")。

## 2. 証拠主義の遵守

憲章「証拠主義: source/timestamp の無いデータは仮説扱い」に従い、
**コストは出典(source)なしには採用しない**。

- `config/cost_model.json` の初期値は全アセット0。よって初期状態では
  **ネットR = グロスR**(完全な後方互換)。
- 実測スプレッド等を `source` 付きで記入して初めてコストが効く。
- 各評価行に `cost_source` を記録し、`unconfigured` か実ブローカー由来かを監査可能にする。

## 3. コスト式

| フィールド | 単位 | 意味 |
|---|---|---|
| `spread` | price | 往復スプレッド(Entry/Exitの不利約定の合計) |
| `commission_round_turn` | price | 1往復あたり手数料(price換算) |
| `swap_per_bar` | price | 1バー保有あたりのスワップ/金利(正でコスト) |

```
cost_price = spread + commission_round_turn + swap_per_bar * bars_held
cost_r     = cost_price / risk_per_unit          (risk = |entry - SL|)
r_result_net = r_result_gross - cost_r           (コストは常に減算)
```

- price単位は各アセットの建値と同一(USDJPY=円、BTC=米ドル、指数=ポイント)。
- `risk_per_unit <= 0`(評価不能)ではコスト0。
- closed評価(SL/TP1/TP2)にのみ適用。no_trade/no_entry/openはネット=グロス。

## 4. 出力列 (evaluations)

| 列 | 意味 |
|---|---|
| `r_result` | グロスR(従来通り。後方互換のため意味を変えない) |
| `cost_r` | 適用したコスト(R単位) |
| `r_result_net` | ネットR = グロス − コスト |
| `cost_source` | コスト定義の出典(`unconfigured` / ブローカー名) |

## 5. 設計判断の記録

- `r_result` の意味は変えない。既存の全下流(月次較正・統計ゲート等)は
  当面グロスを参照し続ける。ネットへの切替は「真実の定義の変更」であり、
  別途レビューの上で意図的に行う(本仕様の範囲外)。
- `swap_per_bar` は保有バー数に比例。bars_held はEntry到達バーから決済バーまで。
- 追加依存なし(標準ライブラリのみ)。

## 6. 次のステップ (本仕様の範囲外)

1. ユーザーがXMTradingの実測コストを `config/cost_model.json` に source 付きで記入。
2. 月次較正・統計ゲートの判定を `r_result_net` ベースへ切り替えるかを別途決定。
