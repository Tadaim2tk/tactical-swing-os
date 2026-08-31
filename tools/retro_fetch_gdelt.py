"""遡及市場コーパス: ニュース層の一度きり取得 (SPEC-RNC-001)。

GDELT DOC 2.0 API (公開・キー不要) から、市場関連の英語見出しを日次で取得する。
- 一度きりの過去データ取得。レートは約1.2秒/リクエストに抑える
- 再開可能: 出力に既にある日付はスキップ
- 取得は広く(選別は読む側): 上位30件/日をそのまま保存
出力: data/retro/news_gdelt.csv (date, seendate, title, domain, url)
provenance: retrospective_derived
"""
from __future__ import annotations

import csv
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

OUT = Path("data/retro/news_gdelt.csv")
START = date(2021, 8, 30)
END = date(2026, 8, 30)
QUERY = ('(markets OR stocks OR "federal reserve" OR inflation OR treasury OR '
         'oil OR gold OR bitcoin OR nasdaq) sourcelang:eng')
MAX_PER_DAY = 30
SLEEP_SEC = 5.5  # GDELTの実運用上の礼儀(約5秒/リクエスト)。1.2秒では throttle された実測あり
RETRIES = 3
UA = "tso-retro-corpus/1.0 (one-time historical research fetch)"


def fetch_day(d: date) -> list[dict]:
    start = d.strftime("%Y%m%d") + "000000"
    end = d.strftime("%Y%m%d") + "235959"
    params = {
        "query": QUERY, "mode": "artlist", "format": "json",
        "maxrecords": str(MAX_PER_DAY), "sort": "hybridrel",
        "startdatetime": start, "enddatetime": end,
    }
    url = "https://api.gdeltproject.org/api/v2/doc/doc?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode("utf-8", errors="replace"))
    rows = []
    for a in data.get("articles", []):
        rows.append({
            "date": d.isoformat(),
            "seendate": a.get("seendate", ""),
            "title": (a.get("title") or "").replace("\n", " ").strip()[:300],
            "domain": a.get("domain", ""),
            "url": a.get("url", ""),
        })
    return rows


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    done: set[str] = set()
    if OUT.exists():
        with open(OUT, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                done.add(row["date"])
    new_file = not OUT.exists()
    fields = ["date", "seendate", "title", "domain", "url", "fetched_at", "provenance"]
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    n_days = 0
    with open(OUT, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if new_file:
            w.writeheader()
        d = START
        while d <= END:
            key = d.isoformat()
            if key in done:
                d += timedelta(days=1)
                continue
            rows = None
            for attempt in range(RETRIES):
                try:
                    rows = fetch_day(d)
                    break
                except Exception as e:  # noqa: BLE001 - throttle/一時失敗はバックオフして再試行
                    print(f"warn {key} try{attempt+1}: {e}", file=sys.stderr)
                    time.sleep(30 * (attempt + 1))
            if rows is None:
                # この日は諦めて続行(doneに入らないので、後日の再実行で自然に埋まる)
                d += timedelta(days=1)
                continue
            for row in rows:
                row["fetched_at"] = fetched_at
                row["provenance"] = "retrospective_derived"
                w.writerow(row)
            f.flush()
            n_days += 1
            if n_days % 50 == 0:
                print(f"[{n_days}] {key} rows={len(rows)}")
            time.sleep(SLEEP_SEC)
            d += timedelta(days=1)
    print(f"done: +{n_days} days -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
