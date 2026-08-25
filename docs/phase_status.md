# Tactical Swing OS — Phase Status

> 本体repo側のフェーズ進捗ミラー。spec repo の Phase Status は後でまとめて同期する。
> 最終更新: 2026-07-02（Phase 29 学習ループ閉鎖 着手 / 主KPIを予測精度に復元）

## サマリー

研究OSの「最初の鼓動」（毎日のデータ取得→シグナル→評価サイクル）は稼働済み。
その上に**分析レイヤー**・**監査網**・**計器の健全性**が積み上がり、データ蓄積
フェーズの観測基盤が整った状態。

到達点の3層:
- **計器**: 各分析レイヤー（calibration / reliability / cost / portfolio 等）
- **監査網**: Narrative Lookahead Audit / Adversarial Review
- **計器の健全性**: Data Health / Freshness

KPI は EVALUATIONS 蓄積件数（目標: 100 → 300 → 1000）。

**現在地（2026-07-02）**: 観測装置・監査網は十分に整備済み（PR #48〜#69）。一方で
**学習ループ本体（学習した知見がシグナル生成へ流れ込む経路）が未着工**であり、
`models/weights.json` は `generate_signal.py` に一度も読み込まれていない開ループだった。
2026-07 の軌道修正ミッション（[governance_reform_2026-07.md](governance_reform_2026-07.md)）により、
主KPIを**予測精度の改善**に復元し、**Phase 29: 学習ループ閉鎖**を進行中。
「評価データ蓄積待ち」は既定路線から外す — 統計的な採用判断はデータを待つが、
**実装はデータを待たない**（shadow / inactive で先に作り、データが揃い次第ゲートが自動で開く）。

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
| 27.x | JP-EVAL-001 rev2（jp_swing_evaluate スキーマ整合 + lag cost attribution） | — | [#68](https://github.com/Tadaim2tk/tactical-swing-os/pull/68) | ✅ |
| — | Dashboard 投資判断ファースト日本語レイアウト（バナー + 4ティア） | — | [#69](https://github.com/Tadaim2tk/tactical-swing-os/pull/69) | ✅ |
| 27.3 | JP Market Context Bridge（TSO 市場コンテキストを point-in-time feature store として保存 / 判断は未活性） | [SPEC-JMCB-001](SPEC_JP_MARKET_CONTEXT_BRIDGE.md) | — | 🔄 (a のみ完了) |
| 27.3-a | 日次スナップショット `data/market_context_daily.csv` 生成（蓄積開始。データを待たない） | SPEC-JMCB-001 | — | ✅ |
| 27.3-b | JP 側の参照列追加 + lookahead 結合規則 + 監査登録 | SPEC-JMCB-001 | — | ⏳ |
| 27.3-c | Ablation 検証（jp_technical_only vs jp_plus_market_context）→ ゲート判断 | SPEC-JMCB-001 | — | ⏳ (JP closed 30件待ち) |

---

## 進行中: Phase 29 — 学習ループ閉鎖（軌道修正ミッション 2026-07）

目的の復元。「学習した知見がシグナル生成に（shadowで）流れ込む閉ループが動く」ことのみを
成果とする。**安全装置の追加は成果に数えない。** 詳細: [governance_reform_2026-07.md](governance_reform_2026-07.md)

| Step | 内容 | 状態 |
|---|---|---|
| 29.0 | ガバナンス改革（README / runbook §0・§6 / 本表の改定 + 対照表新設） | 🔄 本PR |
| 29.1 | Approved Weights → Shadow Mode 接続（`generate_signal.py` に承認済みweights読込。出力は base / weighted 併記、実推奨は base のまま。日次差分レポート） | ⏳ |
| 29.2 | Narrative Memory v0（意味ベクトル層。embedding + TF-IDFフォールバック。類似局面検索を表示のみで導入） | ⏳ |
| 29.3 | Ablation 評価フレーム（technical_only / text_narrative_only / technical_plus_text の3系統比較） | ⏳ |
| 29.4 | 最小観測ループを1周実行（観測→事前ナラティブ→評価→類似検索→教訓） | ⏳ |

---

## 今後の候補・未実装

- **Phase 28.1+ Cross Asset Regime Engine 本体**: SPEC-CAR-001（[SPEC_CROSS_ASSET_REGIME.md](SPEC_CROSS_ASSET_REGIME.md)）
  に基づく本体実装。統計的な**採用**は非活性ゲート（closed評価>=30・複数資産分散>=4・観測>=20日・
  Data Health 非critical非degraded・必須入力 fresh・監査 passed/許容warning・cost未設定なら net-R 不使用）
  が開くまで `insufficient_data` を出すが、**実装自体は Phase 29 完了後に shadow / inactive で
  先行してよい**（実装はデータを待たない）。
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
