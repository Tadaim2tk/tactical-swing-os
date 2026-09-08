"""GPT本文にしかない観察項目を追記型台帳へ記録する（changelog(15)）。

LOG28列は不変（append-only契約）なので、本文の1行申告はサイドカーへ残す。

- expected_r_basis: expected_r が主観か二点分布式か。**A級条件が expected_r>=0.45 なので、
  同じ列に別の量が混ざると同じ判断が通ったり落ちたりする**
  （2026-09-04 WTI: rr=2.89 win_prob=0.57 申告0.39 / 式なら1.2173。0.45を挟んで反対側）
- invalidation_check: **まだ決着していない方向あり判断すべて**について invalidation が
  発動したか。判断は最長5営業日オープンなので、初日だけ聞くと2〜5日目の崩壊
  （まさに測りたいもの）を取りこぼす(#157 Codex P1)。
  invalidation は191/193行に書かれているのに発動記録が無く、
  **実際の手仕舞い基準(シナリオ崩壊)が当たっていたかを測れなかった**

usage:
  python tools/record_signal_extras.py basis 2026-09-07 two_point
  python tools/record_signal_extras.py invalidation 2026-09-07 "20260906_WTI_BUY_PULLBACK=not_fired,20260906_GOLD_BUY_REVERSAL=fired"

第4引数で生成経路を指定する(既定 chatgpt_app)。同じプロンプトを
scripts/tso_daily_gpt.sh のターミナル経路でも使うため、決め打ちにすると provenance が
壊れ、経路別の比較・監査ができなくなる(#157 Codex P2)。
  python tools/record_signal_extras.py basis 2026-09-07 two_point gpt_terminal
"""
from __future__ import annotations

import csv
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

BASIS_PATH = Path("data/expected_r_basis.csv")
INVAL_PATH = Path("data/invalidation_checks.csv")
LEDGER_PATH = Path("data/signal_log.csv")
WINDOW_BUSINESS_DAYS = 5  # prompts/tso_daily_signal_log.md の「5営業日を過ぎるまで毎日聞き直す」
BASIS_VOCAB = {"subjective", "two_point"}
SOURCE_VOCAB = {"chatgpt_app", "gpt_terminal", "manual"}  # ingest_daily_log の origin と揃える
INVAL_VOCAB = {"fired", "not_fired", "unknown"}
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _check_date(token: str) -> str:
    try:
        date.fromisoformat(token)
    except ValueError:
        raise SystemExit(f"日付が ISO 形式でない: '{token}'")
    return token


def _read(path: Path) -> list[dict]:
    return list(csv.DictReader(path.open(encoding="utf-8"))) if path.exists() else []


def _append(path: Path, fields: list[str], rows: list[dict], key: tuple[str, ...]) -> int:
    seen = {tuple(r[k] for k in key) for r in _read(path)}
    # 投入分の中の重複も弾く(#157 Codex P2)。seen をディスク上のキーだけにしていると、
    # 1行に同じ signal_id が fired と not_fired で2回現れた場合に両方通り、
    # 矛盾した (check_date, signal_id) が append-only 台帳に書かれる。
    # そうなると再実行しても両方「既存」になり、通常の手順では直せない。
    new = []
    for r in rows:
        k = tuple(r[x] for x in key)
        if k in seen:
            continue
        seen.add(k)
        new.append(r)
    if not new:
        print("already recorded; append-only台帳のため上書きしない")
        return 0
    first = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if first:
            w.writeheader()
        w.writerows(new)
    return len(new)


def _business_days_since(start: str, end: str) -> int:
    """start の翌日から end までの平日数。祝日は考慮しない(米国休場日も1日と数える)。

    多く数える側に振れるので窓は早く閉じ、警告は出過ぎない方へ倒れる。
    暗号資産は土日も動くが、契約側の窓が全資産一律「5営業日」なのでそれに合わせる。
    """
    a, b = date.fromisoformat(start), date.fromisoformat(end)
    n, cur = 0, a
    while cur < b:
        cur += timedelta(days=1)
        if cur.weekday() < 5:
            n += 1
    return n


def _undeclared_open(check_date: str, declared: set[str]) -> list[str]:
    """台帳上まだ窓の内側にある方向あり判断のうち、過去に fired と記録されておらず、
    今回の申告にも含まれていない signal_id を返す。

    これが空でないと、その判断は「発動しなかった」のか「聞かれなかった」のかが
    区別できない。invalidation_check は発動率を測るための列なので、分母が黙って
    縮むと数字そのものが意味を失う(2026-09-09に実際に3件漏れた)。

    同じ check_date で既に記録済みの signal_id は申告済みとして扱う。漏れた分だけを
    追記する運用(runbook 1d)で、2回目の実行が1回目の申告を漏れ扱いしないため。

    判定は台帳と本ファイルだけで閉じる。採点表(result_5d)を使うと、UTC同日ラベルの
    バーを確定扱いしない防御(#137 Codex P2)のぶん窓が実際より長く見え、
    朝の取込時に決着済みのものまで警告に出る。
    """
    history = _read(INVAL_PATH)
    fired = {r["signal_id"] for r in history if r.get("invalidation_fired") == "fired"}
    # 同じ check_date で既に記録済みのものも「申告済み」に数える(#161 Codex P2)。
    # runbook の手順は「漏れた分だけ聞き直して追記する」なので、2回目の実行では
    # declared に1回目の分が入らない。ここを見ないと、追記のたびに前回申告済みの
    # 側が「漏れ」として出て、警告が逆さまになる。
    declared = declared | {r["signal_id"] for r in history if r.get("check_date") == check_date}
    out = []
    for r in _read(LEDGER_PATH):
        sid = (r.get("signal_id") or "").strip()
        day = (r.get("date") or "").strip()
        if (r.get("side") or "").strip().upper() not in {"BUY", "SELL", "LONG", "SHORT"}:
            continue
        if not day or day >= check_date:
            continue          # 当日ぶんはまだ確認しようがない
        if _business_days_since(day, check_date) > WINDOW_BUSINESS_DAYS:
            continue          # 窓が閉じた
        if sid in fired or sid in declared:
            continue
        out.append(sid)
    return out


def main() -> int:
    if len(sys.argv) < 4:
        print(__doc__)
        return 1
    kind, day, value = sys.argv[1], _check_date(sys.argv[2]), sys.argv[3]
    source = sys.argv[4] if len(sys.argv) > 4 else "chatgpt_app"
    if source not in SOURCE_VOCAB:
        raise SystemExit(f"source: '{source}' は閉じた語彙にない。許容 {sorted(SOURCE_VOCAB)}")

    if kind == "basis":
        if value not in BASIS_VOCAB:
            raise SystemExit(f"expected_r_basis: '{value}' は閉じた語彙にない。許容 {sorted(BASIS_VOCAB)}")
        n = _append(BASIS_PATH, ["date", "expected_r_basis", "source", "recorded_at"],
                    [{"date": day, "expected_r_basis": value, "source": source, "recorded_at": NOW}],
                    ("date",))
        print(f"recorded basis: {day} -> {value}" if n else "")
        return 0

    if kind == "invalidation":
        rows = []
        for part in value.split(","):
            part = part.strip()
            if not part:
                continue
            if "=" not in part:
                raise SystemExit(f"書式違反: '<signal_id>=fired|not_fired|unknown' が必要 ('{part}')")
            sid, verdict = (x.strip() for x in part.split("=", 1))
            if verdict not in INVAL_VOCAB:
                raise SystemExit(f"{sid}: '{verdict}' は閉じた語彙にない。許容 {sorted(INVAL_VOCAB)}")
            if not sid:
                raise SystemExit("signal_id が空")
            prev = {r["signal_id"]: r["invalidation_fired"] for r in rows}
            if sid in prev and prev[sid] != verdict:
                # 同じ行の中で矛盾している。先勝ちで黙って通すと、どちらが本当か
                # 分からない値が append-only 台帳に入る(#157 Codex P2)。全体を弾く。
                raise SystemExit(
                    f"{sid} が同じ行に矛盾する値で2回現れている: "
                    f"'{prev[sid]}' と '{verdict}'。どちらが正しいか確認して出し直すこと")
            rows.append({"check_date": day, "signal_id": sid, "invalidation_fired": verdict,
                         "source": source, "recorded_at": NOW})
        if not rows:
            raise SystemExit("記録する項目が無い")
        missing = _undeclared_open(day, {r["signal_id"] for r in rows})
        n = _append(INVAL_PATH, ["check_date", "signal_id", "invalidation_fired", "source", "recorded_at"],
                    rows, ("check_date", "signal_id"))
        for r in rows[:n]:
            print(f"recorded invalidation: {r['signal_id']} -> {r['invalidation_fired']}")
        if missing:
            print(f"!! 申告漏れ: 未決着の方向あり判断 {len(missing)} 件が今回の申告に無い: "
                  + ", ".join(missing), file=sys.stderr)
            print("   発動したのか聞かれなかったのかが区別できない。"
                  "GPT側の取りこぼしなら出し直すこと。", file=sys.stderr)
        return 0

    raise SystemExit(f"未知の種別: '{kind}'（basis か invalidation）")


if __name__ == "__main__":
    raise SystemExit(main())
