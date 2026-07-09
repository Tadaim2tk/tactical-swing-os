"""Sheets workbook grid maintenance (Issue #83) — 空グリッドの刈り込み専用。

workbook「Tactical Swing OS Log」が 1,000万セル上限に達し EVALUATIONS 同期が
失敗している。原因の大半は「データの無い巨大グリッド」(行/列だけ確保されたタブ)
であることが多いため、本スクリプトは**データを一切消さずに**各タブのグリッドを
データ実在範囲+マージンへ resize して空セルを解放する。

安全設計:
- タブの削除・行データの削除は絶対にしない(非破壊 resize のみ)
- 縮小のみ(拡大しない)。データ実在範囲より小さくは絶対にしない
- 既定は DRY-RUN(計画の表示のみ)。適用は環境変数 TRIM_APPLY=true のときだけ
- タブ別の before/after と解放セル数を results/sheets_maintenance_report.json に出力
- 刈り込み後も上限に近い場合は「データ実在セルが多いタブ」を名指しで報告し、
  削除するかどうかは人間判断(Issue #83)に委ねる
"""
from __future__ import annotations

import json
import os
from pathlib import Path

RESULTS_DIR = Path("results")
MARGIN_ROWS = 20
MIN_ROWS = 50
WORKBOOK_CELL_LIMIT = 10_000_000


def data_extent(values: list[list[str]]) -> tuple[int, int]:
    """get_all_values() の結果からデータ実在範囲 (rows, cols) を返す。"""
    rows = len(values)
    cols = max((len(r) for r in values), default=0)
    return rows, cols


def plan_resize(row_count: int, col_count: int, data_rows: int, data_cols: int) -> tuple[int, int] | None:
    """縮小プラン (target_rows, target_cols) を返す。縮小余地が無ければ None。

    データ実在範囲を下回るサイズには絶対にしない(非破壊保証)。
    """
    target_rows = max(data_rows + MARGIN_ROWS, MIN_ROWS)
    target_cols = max(data_cols, 1)
    target_rows = min(target_rows, row_count)  # 拡大しない
    target_cols = min(target_cols, col_count)
    if target_rows >= row_count and target_cols >= col_count:
        return None
    return target_rows, target_cols


def main() -> int:
    apply = os.getenv("TRIM_APPLY", "").strip().lower() == "true"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    from sync_to_sheets import get_client, open_spreadsheet
    client = get_client()
    if client is None:
        print("error: GOOGLE_SERVICE_ACCOUNT_JSON / GOOGLE_SHEET_ID が未設定")
        return 1
    spreadsheet = open_spreadsheet(client)

    report = {"mode": "apply" if apply else "dry_run", "worksheets": [],
              "total_cells_before": 0, "total_cells_after_planned": 0, "cells_freed_planned": 0}

    for ws in spreadsheet.worksheets():
        rows_before, cols_before = ws.row_count, ws.col_count
        cells_before = rows_before * cols_before
        try:
            values = ws.get_all_values()
        except Exception as exc:  # noqa: BLE001 - 読めないタブは触らない
            report["worksheets"].append({"title": ws.title, "error": f"read failed: {type(exc).__name__}",
                                         "cells_before": cells_before, "action": "skipped"})
            report["total_cells_before"] += cells_before
            report["total_cells_after_planned"] += cells_before
            continue
        data_rows, data_cols = data_extent(values)
        plan = plan_resize(rows_before, cols_before, data_rows, data_cols)
        entry = {
            "title": ws.title,
            "grid_before": f"{rows_before}x{cols_before}",
            "cells_before": cells_before,
            "data_extent": f"{data_rows}x{data_cols}",
        }
        report["total_cells_before"] += cells_before
        if plan is None:
            entry.update({"action": "no_trim_needed", "cells_after": cells_before})
            report["total_cells_after_planned"] += cells_before
        else:
            tr, tc = plan
            cells_after = tr * tc
            entry.update({"grid_after": f"{tr}x{tc}", "cells_after": cells_after,
                          "cells_freed": cells_before - cells_after,
                          "action": "resized" if apply else "would_resize"})
            report["total_cells_after_planned"] += cells_after
            if apply:
                try:
                    ws.resize(rows=tr, cols=tc)
                except Exception as exc:  # noqa: BLE001 - 失敗は正直に記録して続行
                    entry["action"] = f"resize_failed: {type(exc).__name__}"
                    report["total_cells_after_planned"] += cells_before - cells_after  # 戻す
        report["worksheets"].append(entry)

    report["cells_freed_planned"] = report["total_cells_before"] - report["total_cells_after_planned"]
    report["still_near_limit"] = report["total_cells_after_planned"] > WORKBOOK_CELL_LIMIT * 0.9
    # データ実在セルが大きいタブ(刈り込みでは減らない側)の上位を人間向けに列挙
    heavy = sorted(
        (w for w in report["worksheets"] if "data_extent" in w),
        key=lambda w: w.get("cells_after", 0), reverse=True)[:5]
    report["heaviest_tabs_after_trim"] = [
        {"title": w["title"], "cells_after": w.get("cells_after", 0), "data_extent": w["data_extent"]}
        for w in heavy]

    (RESULTS_DIR / "sheets_maintenance_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"mode={report['mode']} tabs={len(report['worksheets'])}")
    print(f"total cells: {report['total_cells_before']:,} -> {report['total_cells_after_planned']:,} "
          f"(freed {report['cells_freed_planned']:,})")
    for w in report["worksheets"]:
        line = f"  {w['title']}: {w.get('grid_before','?')} data={w.get('data_extent','?')} -> {w.get('action')}"
        if "cells_freed" in w:
            line += f" (free {w['cells_freed']:,})"
        print(line)
    if report["still_near_limit"]:
        print("warning: 刈り込み後も上限の90%超。データ実在の大きいタブは人間判断で整理が必要 (Issue #83):")
        for h in report["heaviest_tabs_after_trim"]:
            print(f"  - {h['title']} ({h['cells_after']:,} cells, data {h['data_extent']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
