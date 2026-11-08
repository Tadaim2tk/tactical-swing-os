#!/usr/bin/env python3
"""月次較正の手順を一つにまとめる（毎月1日。10月はこの3つが全部抜けた）。

  1. 遡及コーパスを対象月の末まで延長する（tools/retro_build_market.py --extend。失敗しても続行）
  2. 先月の数値を出す（tools/analysis/monthly_calib.py）
  3. 草稿を書く: reports/monthly/YYYY-MM_calibration_draft.md（常に）、
     --docs なら docs/monthly_calibration_YYYY-MM.md（**無いときだけ**。あれば .draft.md に書く）

決定は書かない。人間（または人間に頼まれた Claude）が草稿を読んで「決定待ち」を埋める。

    python tools/monthly_calibration_run.py                 # 先月、延長あり、reports だけ
    python tools/monthly_calibration_run.py --docs          # docs にも草稿
    python tools/monthly_calibration_run.py --month 2026-10 --no-extend
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "analysis"))
import monthly_calib  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--month", default=monthly_calib.default_month())
    ap.add_argument("--no-extend", action="store_true", help="遡及コーパスの延長を飛ばす（ネットワーク無し）")
    ap.add_argument("--docs", action="store_true", help="docs/monthly_calibration_YYYY-MM.md にも草稿を書く（既存なら .draft.md）")
    ap.add_argument("--root", type=Path, default=ROOT)
    args = ap.parse_args(argv)

    notes = []
    if not args.no_extend:
        r = subprocess.run([sys.executable, str(args.root / "tools" / "retro_build_market.py"), "--extend"],
                           cwd=args.root, capture_output=True, text=True)
        tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or [""]
        notes.append(f"retro extend rc={r.returncode}: {tail[0][:160]}")
        if r.returncode != 0:
            print("warning - retro extend failed; continuing with the existing corpus", file=sys.stderr)
    md, R = monthly_calib.build(args.root, args.month)
    rep = args.root / "reports" / "monthly" / f"{args.month}_calibration_draft.md"
    rep.parent.mkdir(parents=True, exist_ok=True)
    rep.write_text(md + "\n", encoding="utf-8")
    written = [rep]
    if args.docs:
        doc = args.root / "docs" / f"monthly_calibration_{args.month}.md"
        if doc.exists():
            doc = args.root / "docs" / f"monthly_calibration_{args.month}.draft.md"
            notes.append("docs に同月の文書が既にあるので .draft.md に書いた")
        doc.write_text(md + "\n", encoding="utf-8")
        written.append(doc)
    print(f"month={args.month}")
    for n in notes:
        print(n)
    for w in written:
        print(f"wrote {w.relative_to(args.root)}")
    if R.get("errors"):
        print("sections with errors:", R["errors"], file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
