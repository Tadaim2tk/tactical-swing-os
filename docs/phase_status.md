# Tactical Swing OS — Phase Status

> 本体repo側のフェーズ進捗ミラー。spec repo の Phase Status は後でまとめて同期する。
> 最終更新: 2026-06-17（Phase 28.0 SPEC まで反映 / 既定路線は評価データ蓄積待ち）

## サマリー

研究OSの「最初の鼓動」（毎日のデータ取得→シグナル→評価サイクル）は稼働済み。
その上に**分析レイヤー**・**監査網**・**計器の健全性**が積み上がり、データ蓄積
フェーズの観測基盤が整った状態。

到達点の3層:
- **計器**: 各分析レイヤー（calibration / reliability / cost / portfolio 等）
- **監査網**: Narrative Lookahead Audit / Adversarial Review
- **計器の健全性**: Data Health / Freshness

KPI は EVALUATIONS 蓄積件数（目標: 100 → 300 → 1000）。

**現在地（2026-06-17）**: 観測装置側（評価ループの maturity / 状態分類、Dashboard の UTC 基準日統一）まで硬化済み。Cross Asset Regime Engine は **SPEC-only（本体未実装）**。能動的な大物実装は止め、既定路線は **評価データ蓄積待ち**（第1コホートの成熟を待つ）。

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

## 追加・完了したフェーズ（Phase 22〜28.0）

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
| 25 | Operational Runbook & Spec Sync | — | [#57](https://github.com/Tadaim2tk/tactical-swing-os/pull/57) | ✅ |
| — | Runbook: 人間ロールから実発注/broker操作を除外する文言修正 | — | [#58](https://github.com/Tadaim2tk/tactical-swing-os/pull/58) | ✅ |
| 26 | Transaction Cost Evidence Framework（証拠メタ / 未sourced非ゼロコストを net-R で無視） | SPEC-TC-001 | [#59](https://github.com/Tadaim2tk/tactical-swing-os/pull/59) | ✅ |
| 26.1 | Transaction Cost Evidence Validation Hardening（source_type / source_date 検証） | SPEC-TC-001 | [#60](https://github.com/Tadaim2tk/tactical-swing-os/pull/60) | ✅ |
| 27 | JP One-Share Swing Ledger（research-only 仮想台帳 / 4日付分離） | — | [#61](https://github.com/Tadaim2tk/tactical-swing-os/pull/61) | ✅ |
| — | Audit Dictionary Externalization（辞書を config 外部化・語境界マッチャー） | — | [#62](https://github.com/Tadaim2tk/tactical-swing-os/pull/62) | ✅ |
| 27.1 | JP Swing Ledger Operational Guide / 読み取り専用 validator CLI | — | [#63](https://github.com/Tadaim2tk/tactical-swing-os/pull/63) | ✅ |
| 27.2 | Evaluation Cohort Closure（awaiting_horizon / data_missing / invalid_signal_date / evaluation_maturity） | — | [#64](https://github.com/Tadaim2tk/tactical-swing-os/pull/64) | ✅ |
| 28.0 | Cross Asset Regime Engine **SPEC-only**（本体未実装 / deferred / inactive） | SPEC-CAR-001 | [#65](https://github.com/Tadaim2tk/tactical-swing-os/pull/65) | ✅ (SPEC) |
| — | Determinism cleanup（evaluation_summary / asset_performance が共有 UTC as_of） | — | [#66](https://github.com/Tadaim2tk/tactical-swing-os/pull/66) | ✅ |

---

## 今後の候補・未実装

- **評価データ蓄積待ち（現在の既定路線）**: 第1コホートが Sheets 上で成熟し clean closed
  evaluations が積み上がるのを待つ。KPI 100 → 300 → 1000。データが溜まると Data Health が
  healthy へ向かい、各統計ゲート（SG / DSR 等）が本格稼働する。「待つ」も正規の工程。
- **Phase 28.1+ Cross Asset Regime Engine 本体**: SPEC-CAR-001（[SPEC_CROSS_ASSET_REGIME.md](SPEC_CROSS_ASSET_REGIME.md)）
  に基づく本体実装。**非活性ゲート（closed評価>=30・複数資産分散>=4・観測>=20日・Data Health
  非critical非degraded・必須入力 fresh・監査 passed/許容warning・cost未設定なら net-R 不使用）
  達成後**に着手する。それまでは `insufficient_data` を出す（false-green を作らない）。
- **Phase 26.2 Evidence-backed Cost Configuration**: `config/cost_model.json` に XMTrading 実測
  コストを source / source_type / source_date / responsibility 付きで記入 → ネットR が有効化。
  **人間による出典付きコスト値入力待ち**（AI は値を捏造しない）。
- **spec repo 同期（後続候補）**: 本体 repo を正としてから、`tactical-swing-os-spec` の
  PHASE_STATUS / ROADMAP 等へ Phase 26〜28.0 をまとめて反映（二重更新のズレ回避のため後で一括）。
- **辞書拡充 / LLMベース敵対エージェント（更に後続）**: 運用しながらの辞書調整、ルールベース
  Adversarial Review への LLM 反証エージェント追加（要 API キー・課金、要 lookahead 監査の前段）。

---

## 確認手順

日々の運用・異常時対応は [operations_runbook.md](operations_runbook.md) を参照。
