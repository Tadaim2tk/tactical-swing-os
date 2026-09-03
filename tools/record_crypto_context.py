"""週次crypto文脈タスクの `CRYPTO_CTX,...` 行を追記型台帳へ記録する（changelog(14)）。

閉じた語彙をここで強制する。GPT本文の自由記述は採らない（規約: 閉じた値はルール側で
検証し、LLMには自由記述だけをさせる。SPEC-RNC-001 §監査の教訓4）。

usage: python tools/record_crypto_context.py "CRYPTO_CTX,2026-09-07,MACRO,INFLOW,CONTANGO,NONE,MEDIUM"
"""
from __future__ import annotations

import csv
import sys
from datetime import date, datetime, timezone
from pathlib import Path

PATH = Path("data/crypto_context_weekly.csv")
FIELDS = ["week_start", "driver", "etf_flow_dir", "cme_basis", "regulation_event",
          "confidence", "source", "recorded_at"]
VOCAB = {
    "driver": {"MACRO", "IDIOSYNCRATIC", "MIXED", "UNKNOWN"},
    "etf_flow_dir": {"INFLOW", "OUTFLOW", "FLAT", "UNKNOWN"},
    "cme_basis": {"CONTANGO", "BACKWARDATION", "FLAT", "UNKNOWN"},
    "regulation_event": {"NONE", "PROPOSAL", "ENFORCEMENT", "APPROVAL", "HEARING", "OTHER"},
    "confidence": {"HIGH", "MEDIUM", "LOW"},
}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    parts = [p.strip() for p in sys.argv[1].split(",")]
    if len(parts) != 7 or parts[0] != "CRYPTO_CTX":
        raise SystemExit(f"書式違反: CRYPTO_CTX + 6欄が必要 (受領 {len(parts)}欄)")
    week_start = parts[1]
    try:
        d = date.fromisoformat(week_start)
    except ValueError:
        raise SystemExit(f"week_start が ISO 日付でない: '{week_start}'")
    if d.weekday() != 0:
        raise SystemExit(f"week_start は月曜であること: {week_start} は {d.strftime('%A')}")
    row = dict(zip(FIELDS[1:6], parts[2:7]))
    for k, v in row.items():
        if v not in VOCAB[k]:
            raise SystemExit(f"{k}: '{v}' は閉じた語彙にない。許容値 {sorted(VOCAB[k])}")
    rows = list(csv.DictReader(PATH.open(encoding="utf-8"))) if PATH.exists() else []
    if any(r["week_start"] == week_start for r in rows):
        print(f"already recorded for {week_start}; append-only台帳のため上書きしない")
        return 1
    new = not PATH.exists()
    with PATH.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow({"week_start": week_start, **row, "source": "chatgpt_app",
                    "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
    print(f"recorded: {week_start} driver={row['driver']} conf={row['confidence']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
