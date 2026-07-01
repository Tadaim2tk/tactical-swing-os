# Shadow Weights（Phase 29.1）— 学習ループの第一接続

- 実装: `src/shadow_weights.py`（`generate_signal.py` の main から毎日呼ばれる。単体CLIも可）
- 入力: `models/approved_weights.json`（人間承認済み weights のみ読込）+ `results/signals.csv`
- 出力: `results/shadow_weighted_signals.csv|json` / `results/shadow_weight_impact_summary.json` /
  `reports/model_state/shadow_weight_impact.md` / `data/shadow_weight_comparisons.csv`（累積台帳・git追跡）
- テスト: `src/test_shadow_weights.py` + `src/test_adversarial_review.py` の境界テスト
- 根拠: [governance_reform_2026-07.md](governance_reform_2026-07.md) §2 #4/#5/#6

## 目的

`models/weights.json` が生成側に一度も読み込まれない**開ループ**を閉じる。学習した知見
（weights候補）がシグナル生成に **shadow** で流れ込み、base との差分が毎日記録される。

```
models/approved_weights.json（人間承認PRで更新）
   └─ generate_signal.py main()
        ├─ results/signals.csv          ← 実推奨（従来どおり・変更なし）
        └─ shadow_weights.run()
             ├─ results/shadow_weighted_signals.csv   ← base vs weighted 差分
             ├─ reports/model_state/shadow_weight_impact.md ← 昇格判断材料
             └─ data/shadow_weight_comparisons.csv    ← 累積台帳（daily_cycleがcommit）
```

## 二段階の人間承認

| 段階 | 内容 | 承認 |
|---|---|---|
| shadow承認 | 候補weightsを `approved_weights.json` に反映し比較を開始 | 人間PRマージ |
| active昇格 | weighted を実推奨に反映（未実装・将来の別PR） | 人間PRマージ（比較30件以上の材料を添付） |

shadow の**自動計算・記録**そのものは承認不要（governance §2 #4）。
`status != "approved"` / 欠損 / 破損 の weights は読み込まず、正直なステータス
（`not_approved` / `missing` / `invalid`）を summary とレポートに出す。

## weighted の計算（post-hoc 再構成）

`signals.csv` の保存済みコンポーネント（trend/momentum/volatility/risk_penalty/
entry_quality/direction_confidence/rr）から、`generate_signal` と同一の式・閾値で再構成する:

- `weighted_setup = clamp(0.35·w_t·trend + 0.35·w_m·momentum + 0.20·w_v·vol − 0.20·w_r·risk + 10)`
  （SHORT は trend/momentum を 100−x に反転。generate_signal と同じ規約）
- rank 裁定は本体と同一閾値（A: setup≥75/entry≥65/conf≥65/risk<60/rr≥1.5、B: 60/50/50/1.5）
- `weighted_strength = clamp((setup·0.5 + conf·0.3 + entry·0.2) × asset_w × rank_w·global_rank_w × side_w)`

**差分は「weights=1 で再構成した base」と比較する**（丸め誤差による偽差分を排除。
identity weights なら厳密にゼロ差分）。保存値との食い違いは `reconstruction_mismatch`
として別途カウントし隠さない。

**base side=NONE の行は weighted でも復活しない**: NONE はハードゲート（risk≥80 /
トレンド不明瞭 / 低ATR / データ不足）による除外で、重み以前の判断。entry水準も無い。

## 監査との関係（誤検知防止）

shadow 成果物は必ず携行する: `shadow_mode=true` / `affects_live_recommendation=false` /
`weights_json_updated=false` / `patch_applied=false` / `apply_automatically=false` /
`requires_human_approval=true`（=active昇格の承認）。

Adversarial Review は `check_shadow_weight_boundary` でこれを読む:
- 上記の組合せ → **正当な shadow 記録**（違反ではない・有効ソースにカウント）
- `affects_live_recommendation=true` や `weights_json_updated=true` を主張 → **blocked**
- `shadow_mode` フラグ欠落 → warning（区別不能な成果物）

## 台帳と昇格判断

`data/shadow_weight_comparisons.csv` に日次1行（date × weights_version で重複排除）。
daily_cycle が **data/ 配下のみ**の追記コミットで永続化（governance §2 #6。src/docs/.github
への自動pushは引き続き禁止）。

累積 actionable 比較数が **30 件以上**で `promotion_sample_ready=true` となり、
`shadow_weight_impact.md` が昇格判断の材料（rank変化数・Δstrength分布・再構成不一致）を
提示する。判断・昇格は人間。

## 初期状態（v0-identity）

出荷時の approved weights は **identity（全1.0）ベースライン**。weighted == base が構成上
成立し、差分ゼロは正常（false green ではなく設計どおりの基準線）。非identity候補は
`models/weight_versions/` にスナップショットを置く人間承認PRで昇格させる。

## 安全条件

- 実推奨（`results/signals.csv` の既存列）は一切変更しない。実売買・発注なし。
- weights の active 昇格（実推奨への反映）は人間承認PRが必須（不可侵）。
- shadow層の失敗はシグナル生成を止めない（soft-fail）。
