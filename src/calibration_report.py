from __future__ import annotations

"""月次較正レポートのレンダリング層。

build_monthly_calibration.py から抽出(SPEC-RD-001適用時のモジュール分割)。
"""

import json

import pandas as pd

import stat_guards


def markdown_table(df: pd.DataFrame, empty: str = "_該当なし_") -> str:
    if df.empty:
        return empty
    view = df.fillna("").astype(str)
    headers = list(view.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in view.iterrows():
        lines.append("| " + " | ".join(str(row[col]).replace("|", "\\|") for col in headers) + " |")
    return "\n".join(lines)


def render_monthly_report(
    *,
    conclusion: str,
    log: pd.DataFrame,
    evaluation_meta: dict,
    asset_table: pd.DataFrame,
    rank_table: pd.DataFrame,
    side_table: pd.DataFrame,
    regime_table: pd.DataFrame,
    narrative_table: pd.DataFrame,
    narrative_note: str,
    divergence_note: str,
    mode: str,
    risk: float,
    summary: str,
    data_warning: str,
    reason_memo: str,
    strong_positive_reasons: pd.DataFrame,
    strong_negative_reasons: pd.DataFrame,
    payload: dict,
) -> str:
    return f"""# Tactical Swing OS Monthly Calibration

## 1. 月次結論

{conclusion}

## 2. 月次サマリー

{markdown_table(log)}

評価データソース: {evaluation_meta["evaluation_source"]} / latest_evaluations_available: {evaluation_meta["latest_evaluations_available"]} / fallback_used: {evaluation_meta["fallback_used"]}

## 3. 資産別較正

{markdown_table(asset_table)}

## 4. Rank別較正

{markdown_table(rank_table)}

## 5. Side別較正

{markdown_table(side_table)}

## 6. レジーム別較正 (SPEC-RD-001)

{markdown_table(regime_table)}

- decayed_avg_r: 半減期{stat_guards.DECAY_HALF_LIFE_DAYS}日の指数減衰加重平均R(直近の成績ほど重い)
- effective_n: 減衰後の実効サンプル数
- decay_divergence: True = 全期間平均と直近加重平均の符号が逆。レジームシフトの兆候として人間が確認すること

{divergence_note}

## 7. ナラティブ信頼性 (SPEC-NQ-001)

{markdown_table(narrative_table)}

- 整合判定はシグナル発生時点に記録された値のみを使用(追記専用・後知恵バイアス防止)
- 重み変更提案はSPEC-SG-001と同一ゲート(n>=30, p<0.05, 増加はSharpe>0.5)に従う

{narrative_note}

## 8. 翌月の暫定モード

- next_month_mode: {mode}
- max_daily_risk_pct: {risk}

## 9. 重み変更案

{summary}

## 10. 据え置き理由

weights.jsonは初期値のまま据え置きます。今回の出力は提案のみで、自動更新は行いません。

## 11. データ不足の注意

{data_warning}

## 12. Reason Code較正メモ

{reason_memo}

### strong_positive reason_codes

{markdown_table(strong_positive_reasons)}

### strong_negative reason_codes

{markdown_table(strong_negative_reasons)}

## 13. MONTHLY_CALIBRATION_LOG CSV

```csv
{log.to_csv(index=False).strip()}
```

## 14. MONTHLY_CALIBRATION_LOG JSON

```json
{json.dumps([payload], ensure_ascii=False, indent=2)}
```
"""
