from __future__ import annotations

from datetime import datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo
except ModuleNotFoundError:  # pragma: no cover - local Python 3.8 compatibility.
    ZoneInfo = None


JST = ZoneInfo("Asia/Tokyo") if ZoneInfo else timezone(timedelta(hours=9), "JST")
UTC = ZoneInfo("UTC") if ZoneInfo else timezone.utc


def now_utc() -> datetime:
    return datetime.now(UTC)


def now_jst() -> datetime:
    return datetime.now(JST)


def format_jst(dt: datetime | None = None) -> str:
    dt = dt or now_jst()
    return dt.astimezone(JST).strftime("%Y-%m-%d %H:%M:%S JST")


def format_utc(dt: datetime | None = None) -> str:
    dt = dt or now_utc()
    return dt.astimezone(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")


def legacy_utc_iso(dt: datetime | None = None) -> str:
    dt = dt or now_utc()
    return dt.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S")
