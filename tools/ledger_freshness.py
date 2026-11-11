#!/usr/bin/env python3
"""台帳（data/signal_log.csv）が毎日増えているかを見る。

取込の経路（ChatGPT → 台帳）は外の道具に依存していて、黙って止まる。2026-10-28 のレポートから
Codex が ChatGPT の本文を読めなくなり、11/3〜11/9 は取込が止まったのに夜間ジョブは緑のままだった。
売買頻度の監視（tools/throughput_watch.py）は台帳の最終日を基準に数えるので、台帳が止まると
一緒に止まって何も言わない。ここは「今日」を基準に数える。

    python tools/ledger_freshness.py                  # 状態を出す（exit 0）
    python tools/ledger_freshness.py --fail-on-alert  # ALERT なら exit 2

判定（today は JST の暦日。ChatGPT の日次は土日も出る）:

    遅れ = today − 台帳の最終日
    遅れ 1日以下   OK     06:55 JST の夜間ジョブ時点では、前日分まで入っていれば正常
    遅れ 2日       WARN   1日ぶん取り込めていない（次の回が拾えば戻る。取込は欠けた日をまとめて入れる）
    遅れ 3日以上   ALERT  2日続けて取り込めていない = 経路が壊れている
    台帳が読めない・日付が1つも無い   ALERT

観測だけ。提案・配分・採用に入る数は変えない。
"""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JST = timezone(timedelta(hours=9))
WARN_DAYS = 2
ALERT_DAYS = 3


def jst_today(now: datetime | None = None) -> date:
    """JST の暦日。now は tz 付き（テスト用）。"""
    now = now or datetime.now(timezone.utc)
    return now.astimezone(JST).date()


def last_ledger_date(path: Path) -> date | None:
    """台帳の1列目（date）の最大値。読めない行は数えない。ファイルが無い・日付が無いなら None。"""
    if not path.exists():
        return None
    last = None
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.reader(fh):
            if not row:
                continue
            try:
                d = datetime.strptime(row[0].strip(), "%Y-%m-%d").date()
            except ValueError:
                continue                      # ヘッダ・壊れた行
            if last is None or d > last:
                last = d
    return last


def evaluate(last: date | None, today: date, warn_days: int = WARN_DAYS, alert_days: int = ALERT_DAYS) -> dict:
    if last is None:
        return {"status": "ALERT", "last_date": "", "today": today.isoformat(), "lag_days": None,
                "reason": "台帳が読めないか、日付の入った行が1つも無い"}
    lag = (today - last).days
    if lag >= alert_days:
        status, reason = "ALERT", f"台帳が {lag} 日前で止まっている（{lag - 1} 日ぶん取り込めていない）"
    elif lag >= warn_days:
        status, reason = "WARN", f"台帳が {lag} 日前（{lag - 1} 日ぶん取り込めていない。次の回が拾えば戻る）"
    else:
        status = "OK"
        reason = "前日分まで入っている" if lag == 1 else ("当日分まで入っている" if lag == 0 else "台帳の最終日が今日より先")
    return {"status": status, "last_date": last.isoformat(), "today": today.isoformat(), "lag_days": lag, "reason": reason}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger", type=Path, default=ROOT / "data" / "signal_log.csv")
    ap.add_argument("--today", help="YYYY-MM-DD（既定: いまの JST の暦日）")
    ap.add_argument("--warn-days", type=int, default=WARN_DAYS)
    ap.add_argument("--alert-days", type=int, default=ALERT_DAYS)
    ap.add_argument("--fail-on-alert", action="store_true", help="ALERT なら exit 2")
    args = ap.parse_args(argv)

    today = datetime.strptime(args.today, "%Y-%m-%d").date() if args.today else jst_today()
    res = evaluate(last_ledger_date(args.ledger), today, args.warn_days, args.alert_days)
    lag = "" if res["lag_days"] is None else res["lag_days"]
    print(f"status={res['status']} last_date={res['last_date']} today={res['today']} lag_days={lag}")
    print(res["reason"])
    if res["status"] == "ALERT":
        print("確認する順: (1) Claude の定期タスク「TSO 日次取込」の実行履歴（承認待ちで止まっていないか）"
              " (2) Claude アプリが開いているか (3) Chrome が ChatGPT にログイン済みか"
              " (4) ChatGPT の定時タスクが出力しているか。docs/operations_runbook.md §1g")
    return 2 if (args.fail_on_alert and res["status"] == "ALERT") else 0


if __name__ == "__main__":
    sys.exit(main())
