"""週次レビューの結果を追記型台帳へ残す（runbook §1c 対応）。

問題: 週次レビューは2系統あるのに、どちらも耐久的に残っていなかった。
- ChatGPT側(土12:00) → 会話のみ
- Actions側(土12:10) → results/weekly_review.csv も reports/weekly/*.md も .gitignore 済みで、
  実体は retention-days 指定の無いCI artifact だけ（既定90日で消える）

best_asset / next_week_mode / total_r は週次でしか作られないため、90日より前が
取り出せなくなっていた。監査P1-7と同じ構造。ここでは data/ 配下へ追記して永続化する。

規約:
- **append-only**。同じ week_start が既にあれば追記しない（上書きもしない）。
- したがってこの台帳は「**その週を最初に集計した土曜時点の観測**」であり、
  **最終成績台帳ではない**（監査 2026-09-06 の仕様確認事項）。実行時点では多くの判断が
  awaiting_horizon で、5日・10日の結果は後から確定する。同じ週の確定後の成績を
  ここへ残す経路は無い。最終成績が要るなら revision / as_of を持つ別設計にする必要がある。
  現状は「その時点で何が見えていたか」の記録として使う。
- 推測で埋めない。列が無ければ空欄のまま残す。
- data/ への追記のみ（governance_reform_2026-07 の範囲内）。

usage: python src/append_weekly_review_log.py [--apply]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

SRC = Path("results/weekly_review.csv")
LEDGER = Path("data/weekly_review_log.csv")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="実際に追記する（既定はdry-run）")
    args = ap.parse_args()

    if not SRC.exists():
        print(f"skip: {SRC} が無い（週次レビューが走っていない）")
        return 0
    new = pd.read_csv(SRC, dtype=str, keep_default_na=False)
    if new.empty or "week_start" not in new.columns:
        print(f"skip: {SRC} に week_start 列が無い（{list(new.columns)[:5]}）")
        return 0

    if LEDGER.exists():
        old = pd.read_csv(LEDGER, dtype=str, keep_default_na=False)
        seen = set(old["week_start"]) if "week_start" in old.columns else set()
    else:
        old, seen = pd.DataFrame(), set()

    add = new[~new["week_start"].isin(seen)]
    dup = len(new) - len(add)
    if add.empty:
        print(f"no new weeks (既存 {len(seen)}週 / 重複 {dup}行) — append-only台帳のため上書きしない")
        return 0

    for _, r in add.iterrows():
        print(f" + {r['week_start']}..{r.get('week_end','')}: signals={r.get('total_signals','')} "
              f"mode={r.get('next_week_mode','')} total_r={r.get('total_r','')}")
    if not args.apply:
        print(f"[dry-run] 追記候補 {len(add)}行。実行するには --apply")
        return 0

    # 列は和集合で保つ（週次レビュー側に列が増えても古い行を壊さない）
    merged = pd.concat([old, add], ignore_index=True) if not old.empty else add
    merged = merged.sort_values("week_start").reset_index(drop=True)
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(LEDGER, index=False)
    print(f"appended={len(add)} skipped_dup={dup} total={len(merged)} -> {LEDGER}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
