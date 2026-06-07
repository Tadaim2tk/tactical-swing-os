from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path

import pandas as pd

from time_utils import JST, UTC, format_jst, format_utc, now_utc


CONFIG_PATH = Path("config/news_sources.json")
RESULTS_DIR = Path("results")
REPORTS_DIR = Path("reports/news")
OUTPUT_COLUMNS = [
    "fetched_at_jst",
    "fetched_at_utc",
    "source",
    "source_category",
    "title",
    "summary",
    "link",
    "published",
    "published_jst",
    "published_utc",
    "age_hours",
    "matched_assets",
    "raw_category",
]


@dataclass(frozen=True)
class NewsSource:
    name: str
    url: str
    category: str


ASSET_KEYWORDS = {
    "BTC": ["bitcoin", "crypto", "etf", "coinbase", "ether", "ethereum", "digital asset"],
    "GOLD": ["gold", "bullion", "safe haven"],
    "WTI": ["oil", "crude", "opec", "brent", "wti", "refinery", "tanker"],
    "USDJPY": ["dollar", "yen", "boj", "usd/jpy", "usdjpy", "fx", "greenback"],
    "SPX": ["stocks", "s&p", "s&p 500", "spx", "wall street", "earnings", "shares"],
    "NASDAQ": ["nasdaq", "tech", "chip", "ai stocks", "mega-cap", "megacap", "earnings"],
    "US10Y": ["yield", "yields", "treasury", "treasuries", "fed", "rates", "bond"],
    "DXY": ["dollar", "greenback", "fed", "rates", "treasury", "yields"],
    "VIX": ["vix", "volatility", "fear", "selloff", "risk-off"],
}


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", str(text or ""))
    return " ".join(text.split())


def parse_datetime(value: str) -> datetime | None:
    if not value:
        return None
    try:
        dt = parsedate_to_datetime(value)
    except (TypeError, ValueError, IndexError, OverflowError):
        try:
            dt = pd.to_datetime(value, errors="coerce", utc=True)
            if pd.isna(dt):
                return None
            return dt.to_pydatetime().astimezone(UTC)
        except (TypeError, ValueError):
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def text_of(element: ET.Element, names: list[str]) -> str:
    for name in names:
        found = element.find(name)
        if found is not None and found.text:
            return strip_html(found.text)
        for child in element:
            if child.tag.lower().endswith(name.lower()) and child.text:
                return strip_html(child.text)
    return ""


def link_of(element: ET.Element) -> str:
    direct = text_of(element, ["link"])
    if direct:
        return direct
    for child in element:
        if child.tag.lower().endswith("link"):
            href = child.attrib.get("href", "")
            if href:
                return href
    return ""


def category_of(element: ET.Element) -> str:
    cats = []
    for child in element:
        tag = child.tag.lower()
        if tag.endswith("category") or tag.endswith("subject"):
            value = child.text or child.attrib.get("term", "")
            if value:
                cats.append(strip_html(value))
    return "|".join(cats)


def item_elements(root: ET.Element) -> list[ET.Element]:
    items = [el for el in root.iter() if el.tag.lower().endswith("item")]
    if items:
        return items
    return [el for el in root.iter() if el.tag.lower().endswith("entry")]


def matched_assets_for(title: str, summary: str) -> str:
    text = f"{title} {summary}".lower()
    assets = []
    for asset, keywords in ASSET_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            assets.append(asset)
    return "|".join(assets)


def fetch_url(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "TacticalSwingOS/1.0 RSS reader"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def parse_feed(source: NewsSource, fetched_at: datetime, hours: int, timeout_seconds: int) -> tuple[list[dict], dict]:
    started = time.monotonic()
    print(f"news fetch start: {source.name} ({source.url})")
    try:
        raw = fetch_url(source.url, timeout=timeout_seconds)
        root = ET.fromstring(raw)
    except Exception as exc:  # noqa: BLE001 - one source should not break the run.
        elapsed = round(time.monotonic() - started, 2)
        print(f"warning: failed to fetch {source.name}: {exc}", file=sys.stderr)
        print(f"news fetch source done: {source.name} status=failed items=0 elapsed_seconds={elapsed}")
        return [], {
            "source": source.name,
            "status": "failed",
            "item_count": 0,
            "elapsed_seconds": elapsed,
            "reason": str(exc),
        }

    rows = []
    for item in item_elements(root):
        title = text_of(item, ["title"])
        if not title:
            continue
        summary = text_of(item, ["description", "summary", "content"])
        link = link_of(item)
        published_raw = text_of(item, ["pubDate", "published", "updated", "dc:date"])
        published_dt = parse_datetime(published_raw)
        age_hours = None
        if published_dt:
            age_hours = round((fetched_at - published_dt).total_seconds() / 3600, 2)
            if age_hours > hours:
                continue
        rows.append(
            {
                "fetched_at_jst": format_jst(fetched_at),
                "fetched_at_utc": format_utc(fetched_at),
                "source": source.name,
                "source_category": source.category,
                "title": title,
                "summary": summary,
                "link": link,
                "published": published_raw,
                "published_jst": format_jst(published_dt) if published_dt else "",
                "published_utc": format_utc(published_dt) if published_dt else "",
                "age_hours": age_hours if age_hours is not None else "",
                "matched_assets": matched_assets_for(title, summary),
                "raw_category": category_of(item),
            }
        )
    elapsed = round(time.monotonic() - started, 2)
    print(f"news fetch source done: {source.name} status=ok items={len(rows)} elapsed_seconds={elapsed}")
    return rows, {
        "source": source.name,
        "status": "ok",
        "item_count": len(rows),
        "elapsed_seconds": elapsed,
        "reason": "",
    }


def load_sources(path: Path = CONFIG_PATH) -> list[NewsSource]:
    if not path.exists():
        print(f"warning: news source config not found: {path}", file=sys.stderr)
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"warning: news source config is invalid: {exc}", file=sys.stderr)
        return []
    sources = []
    for row in payload.get("sources", []):
        name = str(row.get("name", "")).strip()
        url = str(row.get("url", "")).strip()
        category = str(row.get("category", "macro")).strip() or "macro"
        if name and url:
            sources.append(NewsSource(name=name, url=url, category=category))
    return sources


def dedupe_rows(rows: list[dict], max_items: int) -> list[dict]:
    out = []
    seen_titles = set()
    seen_links = set()
    for row in rows:
        title_key = str(row.get("title", "")).strip().lower()
        link_key = str(row.get("link", "")).strip().lower()
        if title_key and title_key in seen_titles:
            continue
        if link_key and link_key in seen_links:
            continue
        if title_key:
            seen_titles.add(title_key)
        if link_key:
            seen_links.add(link_key)
        out.append(row)
        if len(out) >= max_items:
            break
    return out


def fetch_status(metadata: dict) -> str:
    total = int(metadata.get("source_total_count", 0) or 0)
    success = int(metadata.get("source_success_count", 0) or 0)
    failed = int(metadata.get("source_failed_count", 0) or 0)
    skipped = int(metadata.get("source_skipped_count", 0) or 0)
    if total == 0:
        return "unavailable"
    if success == 0 and (failed or skipped):
        return "failed"
    if failed or skipped:
        return "partial"
    return "ok"


def write_outputs(rows: list[dict], fetched_at: datetime, metadata: dict) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    for col in OUTPUT_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    df = df[OUTPUT_COLUMNS]
    csv_path = RESULTS_DIR / "news_headlines.csv"
    json_path = RESULTS_DIR / "news_headlines.json"
    report_path = REPORTS_DIR / f"{fetched_at.astimezone(JST).strftime('%Y-%m-%d')}_news_headlines.md"
    df.to_csv(csv_path, index=False)
    metadata = dict(metadata)
    metadata["fetch_status"] = fetch_status(metadata)
    metadata["headline_count"] = int(len(df))
    json_path.write_text(
        json.dumps({"metadata": metadata, "headlines": df.to_dict(orient="records")}, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    lines = [
        "# Tactical Swing OS News Headlines",
        "",
        f"取得日時（JST）: {format_jst(fetched_at)}",
        f"取得日時（UTC）: {format_utc(fetched_at)}",
        f"ニュース取得ステータス: {metadata['fetch_status']}",
        f"取得成功ソース数: {metadata.get('source_success_count', 0)}",
        f"取得失敗ソース数: {metadata.get('source_failed_count', 0)}",
        f"スキップソース数: {metadata.get('source_skipped_count', 0)}",
        f"総所要秒数: {metadata.get('elapsed_seconds', 0)}",
        f"headline件数: {len(df)}",
        "",
        "## 見出し",
        "",
    ]
    if df.empty:
        lines.append("ニュース見出しは取得できませんでした。")
    else:
        for _, row in df.head(50).iterrows():
            assets = row.get("matched_assets", "") or "未分類"
            lines.append(f"- [{row.get('source', '')}] {row.get('title', '')} ({assets})")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"news headlines csv generated: {csv_path}")
    print(f"news headlines json generated: {json_path}")
    print(f"news headlines report generated: {report_path}")
    print(f"news fetch status: {metadata['fetch_status']}")
    print(f"news total fetched count: {len(df)}")
    print(f"news total elapsed seconds: {metadata.get('elapsed_seconds', 0)}")


def fetch_news(hours: int = 48, max_items: int = 100, timeout_seconds: int = 8, global_timeout_seconds: int = 60) -> pd.DataFrame:
    fetched_at = now_utc()
    started = time.monotonic()
    rows = []
    sources = load_sources()
    source_results = []
    for source in sources:
        elapsed = time.monotonic() - started
        if elapsed >= global_timeout_seconds:
            print(f"warning: global news fetch timeout reached; skipping {source.name}", file=sys.stderr)
            source_results.append(
                {
                    "source": source.name,
                    "status": "skipped",
                    "item_count": 0,
                    "elapsed_seconds": 0.0,
                    "reason": "global_timeout",
                }
            )
            continue
        source_rows, result = parse_feed(source, fetched_at, hours, timeout_seconds)
        rows.extend(source_rows)
        source_results.append(result)
    rows = dedupe_rows(rows, max_items)
    elapsed_seconds = round(time.monotonic() - started, 2)
    metadata = {
        "fetched_at_jst": format_jst(fetched_at),
        "fetched_at_utc": format_utc(fetched_at),
        "hours": hours,
        "max_items": max_items,
        "timeout_seconds": timeout_seconds,
        "global_timeout_seconds": global_timeout_seconds,
        "elapsed_seconds": elapsed_seconds,
        "source_total_count": len(sources),
        "source_success_count": sum(1 for item in source_results if item.get("status") == "ok"),
        "source_failed_count": sum(1 for item in source_results if item.get("status") == "failed"),
        "source_skipped_count": sum(1 for item in source_results if item.get("status") == "skipped"),
        "source_results": source_results,
    }
    write_outputs(rows, fetched_at, metadata)
    return pd.DataFrame(rows, columns=OUTPUT_COLUMNS)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch public RSS headlines for Tactical Swing OS.")
    parser.add_argument("--hours", type=int, default=48)
    parser.add_argument("--max-items", type=int, default=100)
    parser.add_argument("--timeout-seconds", type=int, default=8)
    parser.add_argument("--global-timeout-seconds", type=int, default=60)
    args = parser.parse_args()
    fetch_news(
        hours=max(1, args.hours),
        max_items=max(1, args.max_items),
        timeout_seconds=max(1, args.timeout_seconds),
        global_timeout_seconds=max(1, args.global_timeout_seconds),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
