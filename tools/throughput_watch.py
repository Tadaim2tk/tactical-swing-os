#!/usr/bin/env python3
"""売買頻度の監視（throughput watch）。

何を見るか
---------
台帳 ``data/signal_log.csv`` から2つの数を取る。

* **注文 (orders)**: rank が A か B の行。朝に指値を出す対象になった行。
* **見立て (ideas)**: 資産×方向の並びの「始まり」。同じ資産・同じ方向の A/B 行が
  3日以内の間隔で続いていれば同じ見立ての再発行とみなし、1本と数える。
  8月は78行の注文が8本の見立てだった（同じ WTI BUY を毎日書き直していた）。
  注文の数だけを見ると、記帳の仕方が変わっただけで崖に見える。見立ての数が
  本当の「試行回数」に近い。

直近 ``--window`` 日（既定14日）を、その前の ``--baseline`` 日（既定56日）と
台帳日あたりの率で比べる。

判定
----
* ``ALERT``: 見立てが窓の中で ``--alert-ideas`` 本未満（既定3本。14日で2本以下＝週1本以下）、
  または注文も見立ても基準の半分以下。
* ``WARN`` : 注文か見立てのどちらかが半分以下、または見立てが ``--warn-ideas`` 本未満（既定4本）。
* ``OK``   : それ以外。
* ``INSUFFICIENT_DATA``: 窓の中に台帳の日付が半分も無い（取込が止まっている）。
* 基準期間に台帳日が窓の長さぶん無いときは率の比較を諦め、床だけで判定する
  （``note`` に ``no_baseline``）。

試行回数が足りないと、期待値が高くても収束する前に相場の性質が変わる。
2026-09-14 の週から 2026-11-02 まで、この崖を誰も数えていなかった（人間の指摘で判明）。
この道具は観測だけを行い、提案・配分・採用に入る数は一切変えない。

使い方
------
    python tools/throughput_watch.py                       # 台帳の最終日を基準に判定し、CSVと報告を書く
    python tools/throughput_watch.py --check-only          # 何も書かない
    python tools/throughput_watch.py --history             # 毎日の判定を遡って出す（最初の ALERT 日が分かる）
    python tools/throughput_watch.py --fail-on-alert       # ALERT なら終了コード 2（CI 用）
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from throughput_metrics import *  # noqa: E402,F401,F403  (定義は src/throughput_metrics.py に一つだけ置く)
from throughput_metrics import (  # noqa: E402
    INTERVENTIONS_PATH, LEDGER_PATH, OUT_CSV, REPORT_PATH, alert_episodes, append_csv, evaluate, history,
    intervention_table, load_ledger, previous_status, render_report, weekly_table,
)


# --------------------------------------------------------------------------- CLI
def parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ledger", type=Path, default=LEDGER_PATH)
    p.add_argument("--as-of", help="判定の基準日。既定は台帳の最終日")
    p.add_argument("--window", type=int, default=14)
    p.add_argument("--baseline", type=int, default=56)
    p.add_argument("--alert-ideas", type=int, default=3, help="窓の中の見立てがこれ未満で ALERT（既定3＝14日で2本以下）")
    p.add_argument("--warn-ideas", type=int, default=4, help="窓の中の見立てがこれ未満で WARN（既定4）")
    p.add_argument("--out-csv", type=Path, default=OUT_CSV)
    p.add_argument("--report", type=Path, default=REPORT_PATH)
    p.add_argument("--interventions", type=Path, default=INTERVENTIONS_PATH)
    p.add_argument("--check-only", action="store_true", help="CSV・報告を書かない")
    p.add_argument("--report-only", action="store_true", help="報告は書くが CSV には追記しない（dashboard 用）")
    p.add_argument("--history", action="store_true", help="毎日の判定を遡って標準出力へ出す")
    p.add_argument("--fail-on-alert", action="store_true", help="ALERT なら終了コード 2")
    p.add_argument("--transition-file", type=Path, help="前回 ALERT でなく今回 ALERT のとき、このファイルを作る（CI の通知用）")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    ledger = load_ledger(args.ledger)
    if ledger.empty:
        print("ledger is empty", file=sys.stderr)
        return 1
    as_of = pd.Timestamp(args.as_of) if args.as_of else ledger["date"].max()
    if args.history:
        h = history(ledger, args.window, args.baseline, args.alert_ideas, args.warn_ideas)
        print(h.to_csv(index=False))
        print("alert_episodes=" + ";".join(f"{a}..{b}" for a, b in alert_episodes(h)), file=sys.stderr)
        return 0
    res = evaluate(ledger, as_of, args.window, args.baseline, args.alert_ideas, args.warn_ideas)
    h = history(ledger, args.window, args.baseline, args.alert_ideas, args.warn_ideas, until=as_of)
    if not h.empty and str(h["as_of"].iloc[-1]) == str(res["as_of"]) and h["status"].iloc[-1] != res["status"]:
        # WARN が続いて ALERT に上がった場合。history 側の判定を正とする。
        res["status"] = h["status"].iloc[-1]
        res["notes"].append(h["note"].iloc[-1].split("; ")[-1])
    report = render_report(res, ledger, alert_episodes(h), intervention_table(ledger, args.interventions), weekly_table(ledger))
    print(report)
    prev = previous_status(args.out_csv, res["as_of"])
    transition = res["status"] == "ALERT" and prev != "ALERT"
    print(f"\nstatus={res['status']} previous={prev} new_alert={transition}")
    if not args.check_only:
        if not args.report_only:
            append_csv(res, ledger, args.out_csv)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report, encoding="utf-8")
        if args.transition_file and transition and not args.report_only:
            args.transition_file.parent.mkdir(parents=True, exist_ok=True)
            args.transition_file.write_text(f"{res['as_of']} {res['status']}\n", encoding="utf-8")
    if args.fail_on_alert and res["status"] == "ALERT":
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
