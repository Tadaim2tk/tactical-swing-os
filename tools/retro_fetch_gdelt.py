"""遡及市場コーパス: ニュース層の一度きり取得 (SPEC-RNC-001)。

GDELT DOC 2.0 API (公開・キー不要) から市場関連の英語見出しを取得する。
v2 (2026-08-31): 日単位→週単位窓へ変更。初版の日単位・1.2秒間隔は throttle され、
その後は1リクエスト約3分の減速サーブとなった実測を受け、リクエスト数を1/7にした。
記事の日付は各記事の seendate から復元するので日次の粒度は保たれる。

- 一度きりの過去データ取得。間隔8秒・読み取りは長めに待つ(減速サーブ耐性)
- 再開可能: 完了済みの週を data/retro/.gdelt_weeks_done に記録
- 取得は広く(選別は読む側): 週120件をそのまま保存。URLで重複排除
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
DONE = Path("data/retro/.gdelt_weeks_done")
START = date(2021, 8, 30)  # 月曜
END = date(2026, 8, 30)
QUERY = ('(markets OR stocks OR "federal reserve" OR inflation OR treasury OR '
         'oil OR gold OR bitcoin OR nasdaq) sourcelang:eng')
MAX_PER_WEEK = 120
SLEEP_SEC = 8.0
RETRIES = 3
TIMEOUT = 420  # 減速サーブ(実測~3分/件)を待ち切る
UA = "tso-retro-corpus/1.1 (one-time historical research fetch, weekly windows)"


def fetch_week(week_start: date) -> list[dict]:
    week_end = week_start + timedelta(days=6)
    params = {
        "query": QUERY, "mode": "artlist", "format": "json",
        "maxrecords": str(MAX_PER_WEEK), "sort": "hybridrel",
        "startdatetime": week_start.strftime("%Y%m%d") + "000000",
        "enddatetime": week_end.strftime("%Y%m%d") + "235959",
    }
    url = "https://api.gdeltproject.org/api/v2/doc/doc?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        data = json.loads(r.read().decode("utf-8", errors="replace"))
    rows = []
    for a in data.get("articles", []):
        seen = str(a.get("seendate", ""))
        if len(seen) >= 8 and seen[:8].isdigit():
            d_iso = f"{seen[0:4]}-{seen[4:6]}-{seen[6:8]}"
        else:
            d_iso = week_start.isoformat()
        rows.append({
            "date": d_iso,
            "seendate": seen,
            "title": (a.get("title") or "").replace("\n", " ").strip()[:300],
            "domain": a.get("domain", ""),
            "url": a.get("url", ""),
        })
    return rows


def fetch_single_day(d: date, max_records: int = 30) -> list[dict]:
    params = {
        "query": QUERY, "mode": "artlist", "format": "json",
        "maxrecords": str(max_records), "sort": "hybridrel",
        "startdatetime": d.strftime("%Y%m%d") + "000000",
        "enddatetime": d.strftime("%Y%m%d") + "235959",
    }
    url = "https://api.gdeltproject.org/api/v2/doc/doc?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        data = json.loads(r.read().decode("utf-8", errors="replace"))
    rows = []
    for a in data.get("articles", []):
        seen = str(a.get("seendate", ""))
        rows.append({
            "date": d.isoformat(), "seendate": seen,
            "title": (a.get("title") or "").replace("\n", " ").strip()[:300],
            "domain": a.get("domain", ""), "url": a.get("url", ""),
        })
    return rows


def main_daily() -> int:
    """日次深掘り(週次完了後の第2段。4日予算・応答時間ログ=ペナルティ解除メーター)。"""
    days_done_path = Path("data/retro/.gdelt_days_done")
    done: set[str] = set(days_done_path.read_text().split()) if days_done_path.exists() else set()
    seen_urls: set[str] = set()
    if OUT.exists():
        with open(OUT, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                seen_urls.add(row.get("url", ""))
    fields = ["date", "seendate", "title", "domain", "url", "fetched_at", "provenance"]
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    n = 0
    new_file = not OUT.exists() or OUT.stat().st_size == 0  # 単独起動でもヘッダを書く(#130 Codex P2)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        if new_file:
            w.writeheader()
        d = START
        while d <= END:
            key = d.isoformat()
            if key in done:
                d += timedelta(days=1)
                continue
            rows = None
            t0 = time.time()
            for attempt in range(RETRIES):
                try:
                    rows = fetch_single_day(d)
                    break
                except Exception as e:  # noqa: BLE001
                    print(f"warn {key} try{attempt+1}: {e}", file=sys.stderr, flush=True)
                    time.sleep(60 * (attempt + 1))
            if rows is None:
                d += timedelta(days=1)
                continue
            n_new = 0
            for row in rows:
                if row["url"] in seen_urls:
                    continue
                seen_urls.add(row["url"])
                row["fetched_at"] = fetched_at
                row["provenance"] = "retrospective_derived"
                w.writerow(row)
                n_new += 1
            f.flush()
            with open(days_done_path, "a", encoding="utf-8") as df:
                df.write(key + "\n")
            n += 1
            print(f"[daily {n}] {key}: +{n_new} rows ({time.time()-t0:.0f}s)", flush=True)
            time.sleep(7.0)
            d += timedelta(days=1)
    print(f"daily done: +{n} days -> {OUT}")
    return 0


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    done_weeks: set[str] = set()
    if DONE.exists():
        done_weeks = set(DONE.read_text(encoding="utf-8").split())
    seen_urls: set[str] = set()
    if OUT.exists():
        try:
            with open(OUT, newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    seen_urls.add(row.get("url", ""))
        except Exception:  # noqa: BLE001
            pass
    new_file = not OUT.exists() or OUT.stat().st_size == 0
    fields = ["date", "seendate", "title", "domain", "url", "fetched_at", "provenance"]
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    n_weeks = 0
    with open(OUT, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        if new_file:
            w.writeheader()
        wk = START
        while wk <= END:
            key = wk.isoformat()
            if key in done_weeks:
                wk += timedelta(days=7)
                continue
            rows = None
            t0 = time.time()
            for attempt in range(RETRIES):
                try:
                    rows = fetch_week(wk)
                    break
                except Exception as e:  # noqa: BLE001
                    print(f"warn {key} try{attempt+1}: {e}", file=sys.stderr)
                    time.sleep(60 * (attempt + 1))
            if rows is None:
                wk += timedelta(days=7)  # doneに入れない=再実行で埋まる
                continue
            n_new = 0
            for row in rows:
                if row["url"] in seen_urls:
                    continue
                seen_urls.add(row["url"])
                row["fetched_at"] = fetched_at
                row["provenance"] = "retrospective_derived"
                w.writerow(row)
                n_new += 1
            f.flush()
            with open(DONE, "a", encoding="utf-8") as df:
                df.write(key + "\n")
            n_weeks += 1
            print(f"[{n_weeks}] week {key}: +{n_new} rows ({time.time()-t0:.0f}s)", flush=True)
            time.sleep(SLEEP_SEC)
            wk += timedelta(days=7)
    print(f"done: +{n_weeks} weeks -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main_daily() if "--daily" in sys.argv else main())
