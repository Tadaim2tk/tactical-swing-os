# tactical-swing-os

Trade Training AI — AI自身の判断能力を監査し継続的に改善する**研究OS**。
売買シグナル生成器でも自動売買botでもない。最終判断と発注は人間が行う。

## はじめに読む

- **運用手順**: [docs/operations_runbook.md](docs/operations_runbook.md) — 毎朝の確認順序・ステータスの読み方・異常時の一次対応
- **フェーズ進捗**: [docs/phase_status.md](docs/phase_status.md)
- **公開Dashboard**: https://tadaim2tk.github.io/tactical-swing-os/

## 安全インバリアント

実売買なし / 発注なし / weights.json自動更新なし / generate_signal.py自動変更なし /
すべての提案は `requires_human_approval=true`。詳細は運用手順書 §6 を参照。
