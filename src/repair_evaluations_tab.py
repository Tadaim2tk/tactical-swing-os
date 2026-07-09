"""EVALUATIONS タブの列爆発(5,951列)の検査と修復 (Issue #83 根本対応)。

症状: EVALUATIONS のヘッダが 5,951 列に肥大し、1行 append するたびに 5,951 セルを
消費して workbook を上限へ押し上げていた。

安全設計:
- REPAIR_APPLY 未設定 = 検査のみ: ヘッダ構成(正規列/ゴミ列のパターン・件数)と
  修復プランを表示して終了
- REPAIR_APPLY=true: 正規列のデータだけを退避 -> タブを正規サイズで作り直し -> 復元。
  実データ(正規列の値)は1セルも失わない。作業前に旧タブを EVALUATIONS_BACKUP_<ts>
  として複製してから置換する(ロールバック可能)
- 正規列 = results/evaluations.csv のスキーマ(現行コードが書く列)との正規化名一致
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

RESULTS_DIR = Path("results")


def legit_columns() -> list[str]:
    """現行 evaluate_signal が出力する正規の列名リスト。"""
    import evaluate_signal
    import pandas as pd
    base = evaluate_signal.base_result(pd.Series({"signal_id": "x"}))
    return list(base.keys())


def classify_header(header: list[str], legit: list[str]) -> dict:
    from sync_to_sheets import normalize_column_name
    legit_norm = {normalize_column_name(c) for c in legit}
    keep_idx, junk = [], []
    seen = set()
    for i, col in enumerate(header):
        norm = normalize_column_name(col)
        if norm in legit_norm and norm not in seen:
            keep_idx.append(i)
            seen.add(norm)
        else:
            junk.append(col)
    return {"keep_idx": keep_idx, "junk_count": len(junk), "junk_samples": junk[:15],
            "missing_legit": sorted(legit_norm - seen)}


def main() -> int:
    apply = os.getenv("REPAIR_APPLY", "").strip().lower() == "true"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    from sync_to_sheets import get_client, open_spreadsheet
    client = get_client()
    if client is None:
        print("error: 認証情報なし")
        return 1
    ss = open_spreadsheet(client)
    ws = ss.worksheet("EVALUATIONS")
    values = ws.get_all_values()
    if not values:
        print("EVALUATIONS is empty; nothing to repair")
        return 0
    header, data = values[0], values[1:]
    legit = legit_columns()
    plan = classify_header(header, legit)

    print(f"header columns: {len(header)} / legit keep: {len(plan['keep_idx'])} / junk: {plan['junk_count']}")
    print(f"junk samples: {plan['junk_samples']}")
    print(f"missing legit columns (再同期で自動補完される): {plan['missing_legit'][:10]}")
    print(f"data rows: {len(data)}")

    report = {"mode": "apply" if apply else "inspect", "header_cols": len(header),
              "keep_cols": len(plan["keep_idx"]), "junk_cols": plan["junk_count"],
              "junk_samples": plan["junk_samples"], "data_rows": len(data)}
    (RESULTS_DIR / "evaluations_repair_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if not apply:
        print("inspect only (REPAIR_APPLY=true で修復実行)")
        return 0

    # --- 修復 ---
    keep = plan["keep_idx"]
    new_header = [header[i] for i in keep]
    new_rows = [[(r[i] if i < len(r) else "") for i in keep] for r in data]
    # 空行(正規列に値が1つも無い行)は落とす
    new_rows = [r for r in new_rows if any(str(c).strip() for c in r)]

    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M")
    backup_title = f"EVALUATIONS_BACKUP_{ts}"
    ws.duplicate(new_sheet_name=backup_title)
    print(f"ok: backup created: {backup_title}")

    ss.del_worksheet(ws)
    new_ws = ss.add_worksheet(title="EVALUATIONS", rows=max(len(new_rows) + 50, 100), cols=max(len(new_header), 1))
    new_ws.update("A1", [new_header] + new_rows, value_input_option="RAW")
    print(f"ok: EVALUATIONS rebuilt: {len(new_rows)} rows x {len(new_header)} cols "
          f"(was {len(data)} x {len(header)})")
    print(f"note: 問題なければ {backup_title} タブは後で削除してよい")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
