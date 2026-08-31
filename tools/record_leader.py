"""日次の「本日の市場の主役」申告(GPT本文の1語)を追記型台帳へ記録する。

changelog(13)の観察項目。LOG28列は不変のため、本文にしか存在しない主役申告を
route-3取込時にここへ1行残す(10月月次でコーパスの機械判定LEADER_V1と一致率を比較する)。
usage: python tools/record_leader.py 2026-09-01 NASDAQ [source]
"""
from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

PATH = Path("data/leader_observations.csv")


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    date, leader = sys.argv[1], sys.argv[2]
    source = sys.argv[3] if len(sys.argv) > 3 else "chatgpt_app"
    rows = list(csv.DictReader(open(PATH, encoding="utf-8"))) if PATH.exists() else []
    if any(r["date"] == date for r in rows):
        print(f"already recorded for {date}; append-only台帳のため上書きしない")
        return 1
    with open(PATH, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=["date", "leader_claimed", "source", "recorded_at"]).writerow({
            "date": date, "leader_claimed": leader.upper(), "source": source,
            "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
    print(f"recorded: {date} -> {leader.upper()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
