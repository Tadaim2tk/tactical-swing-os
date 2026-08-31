# 仕様凍結: 予測キャリブレーション層 (Brier Score)

- status: **active (frozen)**
- spec_id: SPEC-BC-001
- frozen_at: 2026-06-11 (JST)
- 実装: `src/build_prediction_calibration.py`
- 前提仕様: SPEC-SG-001 (統計ガード)

## 1. 目的

AIの「自信」そのものを採点する。Rank A/Bが暗黙に主張する勝率(implied probability)と
実際の的中率を比較し、自信過剰(ハルシネーション傾向)を確率レベルで監査する。

## 2. 凍結された初期値

| Rank | implied probability (初期凍結値) |
|---|---|
| A | 0.55 |
| B | 0.45 |

- 変更は `config/rank_implied_probability.json` で人間が行う(モジュールは自動変更しない)。
- configが無い/不正な場合は上記デフォルトを使用。

## 3. 判定規則

- hit = (r_result > 0)。Rank別に hit_rate / calibration_gap = hit_rate − implied / Brier score を算出。
- 有意性: (hit_i − implied) の一標本t検定 (SPEC-SG-001の SIGNIFICANCE_ALPHA = 0.05)。
- n < 30 → `insufficient_data` (判定保留)。
- 有意かつ gap < 0 → `overconfident` (自信過剰)。implied引き下げ or Rank基準厳格化を人間レビュー。
- 有意かつ gap > 0 → `underconfident`。implied引き上げ or 基準緩和を人間レビュー。
- 非有意 → `well_calibrated`。

## 4. Brier Skill Score

- 基準Brier = 全体的中率を常に予測した場合のBrier(climatology)。
- BSS = 1 − BS / BS_ref。**BSS > 0 ならRank分けは情報量を持つ**(平均より良い予測)。

## 5. 安全原則

- 出力は採点・分析のみ。weights.jsonは更新しない。requires_human_approval=true 固定。
- 新しい閾値は導入しない(SG-001参照のみ)。implied値の更新は人間の承認事項。

## 6. 変更手続き

implied初期値・判定規則の変更は新spec_idの発行と本ドキュメント更新履歴への追記を必須とする。

## 追補 2026-08-31: 採点アンカー規約（監査P1-3対応）

- 台帳の `date` は JST 朝7時の**判断日**であり、市場バーの日付ではない。
- 遡及採点のアンカーは**判断時に既知の最後のバー**（信号日より前の直近バー、
  `searchsorted(side="left") - 1`）。同ラベルのバーは判断後に確定する未来情報のため
  アンカーに使わない。`fwd_return_1d` は「判断直後の第1セッション」のリターンを意味する。
- entry 到達判定・評価窓は**判断当日バーを含む**（旧実装は当日タッチを非検知
  = known-bias #9。修正で actionable 144行中 touched 89→109）。
- `append_scores` は情報量の降格（scored → awaiting_horizon / invalid_data）を禁止する。
  一過性のデータ障害で確定結果が消えた 2026-08-19 の実発生への恒久対策。
- 執行シミュレーションは信号日が価格窓より前の行を `data_window_expired` として
  約定探索しない（窓先頭バーへの誤アンカー禁止）。
- 本規約変更に伴い全622行を再採点した（B級5日勝率 70.8%→70.5%・n 113→122 で
  主要結論は不変。詳細は docs/audit_blindspots_2026-08-31.md）。
