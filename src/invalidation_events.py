"""invalidation の発動記録を読む側。**発動日が分からない行を較正に渡さない。**

**きっかけ(#162 Codex P2)**: 2026-09-09 に5日ぶんをまとめて聞き直して回収した
`fired` 2件が、`check_date=2026-09-09` で台帳に入った。**その日に発動したのではない。**
実際にはその前の5営業日のどこかで壊れている。ところが行の形は「9/9に初めて発動を
観測した行」とまったく同じで、区別は runbook の散文にしか無かった。
`check_date >= 2026-09-09` で絞る較正コードは、この2件を拾って**偽の手仕舞い日**を付ける。

台帳が持つ3つの日付を混ぜない。
    check_date    **聞いた日**。台帳に載った日
    recorded_at   書き込んだ時刻
    fired_on      **発動した日**。分からなければ空

`fired_on` が空の `fired` 行は「発動したが、いつかは分からない」。
発動率の分子には数えてよいが、**手仕舞い日を要する較正には渡さない。**

既存行は書き換えない。当時 `fired_on` / `retrospective` を記録していなかった行は
空のままで、「不明」を意味する。あとから分かった訂正は
`data/invalidation_corrections.csv` に追記し、ここで重ねる。**訂正を元の行に
上書きしない。** どちらが観測でどちらが訂正かが読めなくなる。
"""
from __future__ import annotations

import csv
from pathlib import Path

INVAL_PATH = Path("data/invalidation_checks.csv")
CORRECTIONS_PATH = Path("data/invalidation_corrections.csv")
CORRECTABLE = ("fired_on", "retrospective")


def _read(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_checks(inval_path: Path = INVAL_PATH,
                corrections_path: Path = CORRECTIONS_PATH) -> list[dict]:
    """台帳に訂正を重ねて返す。元の値は `observed_<列名>` に残す。

    同じ (check_date, signal_id, field) に訂正が複数あれば、**後の行が勝つ**。
    追記型なので、直し直した履歴はファイルに残る。
    """
    rows = [dict(r) for r in _read(inval_path)]
    fixes: dict[tuple[str, str, str], str] = {}
    for c in _read(corrections_path):
        field = (c.get("field") or "").strip()
        if field not in CORRECTABLE:
            continue
        fixes[((c.get("check_date") or "").strip(),
               (c.get("signal_id") or "").strip(), field)] = (c.get("value") or "").strip()
    for r in rows:
        key = ((r.get("check_date") or "").strip(), (r.get("signal_id") or "").strip())
        for field in CORRECTABLE:
            r.setdefault(field, "")
            if (key[0], key[1], field) in fixes:
                r["observed_" + field] = r.get(field, "")
                r[field] = fixes[(key[0], key[1], field)]
    return rows


def fired_events(require_known_date: bool = True, **kw) -> list[dict]:
    """`fired` の行を返す。

    require_known_date=True（既定）では **`fired_on` が入っている行だけ**返す。
    手仕舞い日を使う較正はこちらを使うこと。`check_date` を発動日の代わりに
    しないこと。**聞いた日は発動した日ではない。**
    """
    out = []
    for r in load_checks(**kw):
        if (r.get("invalidation_fired") or "").strip() != "fired":
            continue
        if require_known_date and not (r.get("fired_on") or "").strip():
            continue
        out.append(r)
    return out


def undated_fired(**kw) -> list[dict]:
    """発動したが日付が分からない行。**除外した件数を黙って消さないために要る。**"""
    return [r for r in fired_events(require_known_date=False, **kw)
            if not (r.get("fired_on") or "").strip()]
