# tactical-swing-os

Tactical Swing OS — AIの意味ベクトル的な文章判断能力（ナラティブ評価）を従来のテクニカル分析に
組み込み、記録と自己改善を繰り返して**スイングトレードの予測精度を高める**シグナル研究ツール。
実売買・発注は行わない（これは手段の制約であって、「予測精度で勝つための道具」という目的は
変わらない）。最終判断と発注は人間が行う。

## はじめに読む

- **運用手順**: [docs/operations_runbook.md](docs/operations_runbook.md) — 毎朝の確認順序・ステータスの読み方・異常時の一次対応
- **ガバナンス改定 2026-07**: [docs/governance_reform_2026-07.md](docs/governance_reform_2026-07.md) — ルールの keep / relax / delete 対照表
- **フェーズ進捗**: [docs/phase_status.md](docs/phase_status.md)
- **公開Dashboard**: https://tadaim2tk.github.io/tactical-swing-os/

## 主KPI

**予測精度の改善**（Brier / prediction calibration / net R）。
EVALUATIONS 蓄積件数は精度計算の分母となる補助指標であり、それ自体は成果ではない。

## 安全インバリアント（不可侵）

実売買なし / 発注なし / XM・証券会社操作なし / Secretsをログ・Dashboardに出さない /
lookahead防止（`source_published_at_utc <= signal_cutoff_utc`）/
weightsの**本採用（active昇格）は人間承認（PRマージ）必須** / false green を作らない。

shadow weights の自動計算・記録は許可（実推奨には影響しない）。
`generate_signal.py` の通常PRフローでの改修・weights読込機構の追加は普通の開発であり、
禁止されるのは「実行時の自己書き換え」のみ。詳細は運用手順書 §6 と
[governance_reform_2026-07.md](docs/governance_reform_2026-07.md) を参照。
