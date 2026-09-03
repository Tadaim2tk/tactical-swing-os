"""週次cryptoタスク(日曜20:30)の機械取込行を追記型台帳へ記録する（changelog(14)）。

受け付ける2行:
  CRYPTO_CTX,<week_start>,<driver>,<etf_flow_dir>,<cme_basis>,<regulation_event>,<confidence>,<prev_result>
  CRYPTO_PRED,<week_start>,<asset>,<direction>,<level>,<deadline>

閉じた語彙はここで強制する。GPT本文の自由記述は採らない
（規約: 閉じた値はルール側で検証し、LLMには自由記述だけをさせる。SPEC-RNC-001 §監査の教訓4）。

usage:
  python tools/record_crypto_context.py "CRYPTO_CTX,2026-08-31,MACRO,OUTFLOW,CONTANGO,PROPOSAL,MEDIUM,NONE"
  python tools/record_crypto_context.py "CRYPTO_PRED,2026-08-31,BTC,ABOVE,80000,2026-09-11"
複数行をまとめて渡してもよい（改行区切りの1引数）。
"""
from __future__ import annotations

import csv
import sys
from datetime import date, datetime, timezone
from pathlib import Path

CTX_PATH = Path("data/crypto_context_weekly.csv")
PRED_PATH = Path("data/crypto_predictions_weekly.csv")
CTX_FIELDS = ["week_start", "driver", "etf_flow_dir", "cme_basis", "regulation_event",
              "confidence", "prev_result", "source", "recorded_at"]
PRED_FIELDS = ["week_start", "asset", "direction", "level", "deadline", "source", "recorded_at"]
CTX_VOCAB = {
    "driver": {"MACRO", "IDIOSYNCRATIC", "MIXED", "UNKNOWN"},
    "etf_flow_dir": {"INFLOW", "OUTFLOW", "FLAT", "UNKNOWN"},
    "cme_basis": {"CONTANGO", "BACKWARDATION", "FLAT", "UNKNOWN"},
    "regulation_event": {"NONE", "PROPOSAL", "ENFORCEMENT", "APPROVAL", "HEARING", "OTHER"},
    "confidence": {"HIGH", "MEDIUM", "LOW"},
    "prev_result": {"HIT", "MISS", "DATA_PENDING", "NONE"},
}
PRED_VOCAB = {"asset": {"BTC", "ETH"}, "direction": {"ABOVE", "BELOW"}}
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def monday(token: str) -> str:
    try:
        d = date.fromisoformat(token)
    except ValueError:
        raise SystemExit(f"week_start が ISO 日付でない: '{token}'")
    if d.weekday() != 0:
        raise SystemExit(f"week_start は月曜であること: {token} は {d.strftime('%A')}")
    return token


def append(path: Path, fields: list[str], key: str, row: dict) -> bool:
    rows = list(csv.DictReader(path.open(encoding="utf-8"))) if path.exists() else []
    if any(all(r.get(k) == row[k] for k in key.split("+")) for r in rows):
        print(f"already recorded: {path.name} {row[key.split('+')[0]]}; append-only台帳のため上書きしない")
        return False
    new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if new:
            w.writeheader()
        w.writerow(row)
    return True


def handle(line: str) -> None:
    parts = [p.strip() for p in line.split(",")]
    kind = parts[0]
    if kind == "CRYPTO_CTX":
        if len(parts) != 8:
            raise SystemExit(f"CRYPTO_CTX は 8欄が必要（受領 {len(parts)}欄）: {line}")
        row = dict(zip(CTX_FIELDS[1:7], parts[2:8]))
        for k, v in row.items():
            if v not in CTX_VOCAB[k]:
                raise SystemExit(f"{k}: '{v}' は閉じた語彙にない。許容値 {sorted(CTX_VOCAB[k])}")
        if append(CTX_PATH, CTX_FIELDS, "week_start",
                  {"week_start": monday(parts[1]), **row, "source": "chatgpt_app", "recorded_at": NOW}):
            print(f"recorded ctx: {parts[1]} driver={row['driver']} prev={row['prev_result']}")
    elif kind == "CRYPTO_PRED":
        if len(parts) != 6:
            raise SystemExit(f"CRYPTO_PRED は 6欄が必要（受領 {len(parts)}欄）: {line}")
        asset, direction, level, deadline = parts[2], parts[3], parts[4], parts[5]
        for k, v in (("asset", asset), ("direction", direction)):
            if v not in PRED_VOCAB[k]:
                raise SystemExit(f"{k}: '{v}' は閉じた語彙にない。許容値 {sorted(PRED_VOCAB[k])}")
        try:
            float(level)
        except ValueError:
            raise SystemExit(f"level は数値のみ: '{level}'（単位や記号を書かない）")
        try:
            date.fromisoformat(deadline)
        except ValueError:
            raise SystemExit(f"deadline が ISO 日付でない: '{deadline}'")
        if append(PRED_PATH, PRED_FIELDS, "week_start+asset",
                  {"week_start": monday(parts[1]), "asset": asset, "direction": direction,
                   "level": level, "deadline": deadline, "source": "chatgpt_app", "recorded_at": NOW}):
            print(f"recorded pred: {parts[1]} {asset} {direction} {level} by {deadline}")
    else:
        raise SystemExit(f"未知の行種別: '{kind}'（CRYPTO_CTX か CRYPTO_PRED のみ）")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    for line in sys.argv[1].splitlines():
        if line.strip():
            handle(line.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
