# Tactical Swing OS — Phase Status

> 本体repo側のフェーズ進捗ミラー。spec repo の Phase Status はこれと同期する。
> 最終更新: 2026-06-16（Phase 24 完了時点）

## サマリー

研究OSの「最初の鼓動」（毎日のデータ取得→シグナル→評価サイクル）は稼働済み。
その上に**分析レイヤー**・**監査網**・**計器の健全性**が積み上がり、データ蓄積
フェーズの観測基盤が整った状態。

到達点の3層:
- **計器**: 各分析レイヤー（calibration / reliability / cost / portfolio 等）
- **監査網**: Narrative Lookahead Audit / Adversarial Review
- **計器の健全性**: Data Health / Freshness

KPI は EVALUATIONS 蓄積件数（目標: 100 → 300 → 1000）。

---

## 基盤フェーズ（本セッション以前に確立）

GitHub Actions による自動デイリーサイクルとして稼働済み:

- Layer 1-3: 9資産のデータ取得 → シグナル生成（generate_signal.py）
- Layer 4-6: T+N bars の実データによる仮想成績採点（evaluate_signal.py / reevaluate）
- Layer 7+: Reason Code 分析、AI Feedback、Rule/Model State 提案、Safety Audit、
  Weights Patch 提案・レビュー、Proposal Adoption Tracking、Weight Version History、
  Meta Learning、Auto Calibration、Human Override Analytics、Portfolio Layer、Datetime Audit
- Google Sheets read/write 同期、Weekly / Monthly レビュー

仕様凍結（基盤）:
- **SPEC-SG-001** 統計ガード（過学習ブレーキ: n>=30, t検定 p<0.05, 増加はSharpe>0.5）— active(frozen)
- **SPEC-RD-001** レジーム較正と忘却（time decay 半減期90日）— active(frozen)
- **SPEC-NQ-001** ナラティブ×クオンツ（Welch検定）— active(frozen)

---

## 本セッションで追加・完了したフェーズ

| Phase | 内容 | Spec | PR | 状態 |
|---|---|---|---|---|
| — | Prediction Calibration（Brier / BSS） | SPEC-BC-001 | [#48](https://github.com/Tadaim2tk/tactical-swing-os/pull/48) | ✅ |
| — | Deflated Sharpe Ratio（多重検定補正） | SPEC-DSR-001 | [#49](https://github.com/Tadaim2tk/tactical-swing-os/pull/49) | ✅ |
| — | Transaction Cost（ネットR評価） | SPEC-TC-001 | [#50](https://github.com/Tadaim2tk/tactical-swing-os/pull/50) | ✅ |
| — | Integration Reconciliation（4レイヤーをDashboard/Validationへ統合） | — | [#51](https://github.com/Tadaim2tk/tactical-swing-os/pull/51) | ✅ |
| — | Dashboard Modularization（io/summaries/render/build分割） | — | [#52](https://github.com/Tadaim2tk/tactical-swing-os/pull/52) | ✅ |
| — | Post-modularization fix（`__main__`脱落の修正） | — | [#53](https://github.com/Tadaim2tk/tactical-swing-os/pull/53) | ✅ |
| 22 | Narrative Lookahead Audit（未来情報混入監査） | — | [#54](https://github.com/Tadaim2tk/tactical-swing-os/pull/54) | ✅ |
| 23 | Adversarial Review Agent（提案の横断敵対監査） | — | [#55](https://github.com/Tadaim2tk/tactical-swing-os/pull/55) | ✅ |
| 24 | Data Health / Freshness（計器の鮮度ガード） | — | [#56](https://github.com/Tadaim2tk/tactical-swing-os/pull/56) | ✅ |
| 25 | Operational Runbook & Spec Sync | — | （本PR） | 🔄 |

---

## 今後の候補・未実装

- **Cross Asset Regime Engine（Phase 28.0: SPEC 先行起草済 / 本体未実装）**: 資産横断の市場
  環境（レジーム）を分類する将来レイヤー。評価データ不足での「それっぽい判断器」化を避けるため
  本体はデータ蓄積後に実装し、それまでは非活性ゲート（closed評価>=30・複数資産分散・監査passed/許容warning等）
  で `insufficient_data` を出す前提。設計は [SPEC_CROSS_ASSET_REGIME.md](SPEC_CROSS_ASSET_REGIME.md)
  （SPEC-CAR-001, draft / deferred）。前提仕様 SPEC-RD-001。
- **実コスト設定**: `config/cost_model.json` に XMTrading の実測スプレッド/手数料/スワップを
  source付きで記入 → ネットR が有効化（現状 status=unconfigured）
- **辞書拡充**: Narrative Lookahead / Adversarial Review のキーワード・過信表現辞書を
  運用しながら調整
- **LLMベース敵対エージェント**: 現在ルールベースの Adversarial Review に、LLMによる
  反証エージェントを後フェーズで追加（要 API キー・課金、要 lookahead 監査の前段）
- **EVALUATIONS 蓄積**: 実データが溜まると Data Health が healthy へ、各統計ゲートが本格稼働

---

## 確認手順

日々の運用・異常時対応は [operations_runbook.md](operations_runbook.md) を参照。
