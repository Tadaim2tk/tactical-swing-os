# 仕様凍結: 統計ガード (過学習ブレーキ)

- status: **active (frozen)**
- spec_id: SPEC-SG-001
- frozen_at: 2026-06-10 (JST)
- 実装: `src/stat_guards.py`
- 適用箇所: `build_monthly_calibration.py` / `audit_model_state_proposals.py` / `build_weights_patch.py`

## 1. 目的

少数サンプルへの過剰適合(過学習)による重み変更を機械的に遮断する。
憲章ルールの実装である:

- 憲章7「Active昇格条件: 勝率で昇格しない。最低30サンプル。それ未満はWatching固定」
- 憲章8「最大評価指標: 勝率ではない。MAE改善・破滅回避・Sharpe優先」

## 2. 凍結された閾値

| 定数 | 値 | 意味 |
|---|---|---|
| `MIN_SAMPLES_WEIGHT_CHANGE` | 30 | 重み変更提案に必要な最低closed評価数 |
| `SIGNIFICANCE_ALPHA` | 0.05 | 一標本t検定(両側, H0: mean(R)=0)の有意水準 |
| `MIN_SHARPE_FOR_INCREASE` | 0.5 | 増加(攻撃方向)提案に追加要求するSharpe比下限 |

## 3. ゲート規則

1. closedサンプル数 n < 30 → 変更提案禁止(「データ不足」)。監査では非hold提案を **blocked**。
2. n >= 30 でも p >= 0.05 → 変更提案禁止(「統計的有意性なし」)。
3. **増加提案**: 有意性に加えて Sharpe > 0.5 を要求。
4. **減少提案**: 有意性のみ要求。Sharpe閾値は課さない。
   - 理由: 損失が統計的に確認された場合はRuin回避を優先し、即時に格下げ方向へ動けるべき。過学習への警戒は攻撃方向にのみ非対称に適用する。
5. reason文字列には n / win_rate / average_r / sharpe / p値 を必ず記録する(後日監査のため)。

## 4. 技術的制約

- **scipy禁止**。requirements.txt にscipyは含まれず、GitHub Actions上で壊れるため。
- t検定のp値は標準ライブラリのみで計算する(正則化不完全ベータ関数による正確なStudent's t分布)。実装と数値検証は `stat_guards.py` / `test_stat_guards.py`。

## 5. データ隔離に関する注記

本仕様凍結(2026-06-10)以前に出力された `proposed_weight_change` を含む較正結果は
`pre_specification` 扱いとし、正式な重み判断に使用しない。

## 6. 変更手続き

本仕様の閾値変更は、変更前後の成績を混在させないため、新しいspec_idの発行と
本ドキュメントの更新履歴への追記を必須とする。
