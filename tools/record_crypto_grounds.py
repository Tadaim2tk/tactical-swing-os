"""日次のcrypto根拠有無(GPT本文の`crypto_grounds:`行)を追記型台帳へ記録する。

changelog(14)の観察項目。BTCは見送り72%・ETHは83%だが、その見送りが
「根拠が無くて棄権した」のか「根拠はあるが見送った」のかが台帳から区別できなかった。
LOG28列は不変のため、本文にしかない申告をroute-3取込時にここへ1行残す。

**内生化を避けるための注意**: この列は根拠の有無の記録であって、根拠を揃えることを
促す装置ではない。「有=良い」として集計してはいけない（B+印がスコアの内生化で
無意味化した件と同型のリスク。research_bplus_2026-09-01）。

usage: python tools/record_crypto_grounds.py 2026-09-04 有 無 [source]
       python tools/record_crypto_grounds.py 2026-09-04 yes no
"""
from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

PATH = Path("data/crypto_grounds_observations.csv")
FIELDS = ["date", "etf_grounds", "cme_grounds", "source", "recorded_at"]
TRUE = {"有", "yes", "y", "true", "1", "present"}
FALSE = {"無", "no", "n", "false", "0", "absent"}


def parse(token: str, label: str) -> str:
    t = token.strip().lower()
    if t in {x.lower() for x in TRUE}:
        return "present"
    if t in {x.lower() for x in FALSE}:
        return "absent"
    raise SystemExit(f"{label}: '{token}' は閉じた語彙(有/無)ではない。推測で埋めない。")


def main() -> int:
    if len(sys.argv) < 4:
        print(__doc__)
        return 1
    date = sys.argv[1]
    etf = parse(sys.argv[2], "etf")
    cme = parse(sys.argv[3], "cme")
    source = sys.argv[4] if len(sys.argv) > 4 else "chatgpt_app"
    rows = list(csv.DictReader(PATH.open(encoding="utf-8"))) if PATH.exists() else []
    if any(r["date"] == date for r in rows):
        print(f"already recorded for {date}; append-only台帳のため上書きしない")
        return 1
    new = not PATH.exists()
    with PATH.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow({"date": date, "etf_grounds": etf, "cme_grounds": cme, "source": source,
                    "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
    print(f"recorded: {date} etf={etf} cme={cme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
