"""Read historical French power demand from RTE's public Opendatasoft API."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any, Iterator

import httpx

API_URL = (
    "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/"
    "eco2mix-national-cons-def/records"
)


class RTEAPIError(RuntimeError):
    """Unexpected response or response contract from RTE."""


def daily_windows(start: date, end: date) -> Iterator[tuple[date, date]]:
    """Yield [start, end) calendar-day windows; end is exclusive."""
    if start >= end:
        raise ValueError("start must be before end (exclusive)")
    current = start
    while current < end:
        following = current + timedelta(days=1)
        yield current, following
        current = following


def fetch_window(
    client: httpx.Client,
    start: date,
    end: date,
    *,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Fetch all records for a UTC calendar window with bounded pagination.

    One day has far fewer than the Opendatasoft 10k offset cap.
    """
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")
    records: list[dict[str, Any]] = []
    offset = 0
    where = (
        f'date_heure >= "{start.isoformat()}T00:00:00Z" AND '
        f'date_heure < "{end.isoformat()}T00:00:00Z"'
    )
    while True:
        try:
            response = client.get(
                API_URL,
                params={
                    "where": where,
                    "order_by": "date_heure ASC",
                    "limit": limit,
                    "offset": offset,
                },
            )
            response.raise_for_status()
            payload = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise RTEAPIError(f"RTE request failed for {start} offset={offset}") from exc
        if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
            raise RTEAPIError("Unexpected RTE response: missing results list")
        page = payload["results"]
        if not all(isinstance(item, dict) for item in page):
            raise RTEAPIError("Unexpected RTE response: non-object record")
        records.extend(page)
        offset += len(page)
        total = payload.get("total_count")
        if total is not None and (not isinstance(total, int) or total < 0):
            raise RTEAPIError("Invalid total_count in RTE response")
        if not page and total is not None and offset < total:
            raise RTEAPIError("RTE pagination returned empty page prematurely")
        if len(page) < limit or (total is not None and offset >= total):
            break
    return records


def fetch_range(start: date, end: date) -> list[dict[str, Any]]:
    """Fetch [start,end) one day at a time, avoiding API deep offsets."""
    with httpx.Client(timeout=30, follow_redirects=True) as client:
        rows = [
            record
            for day_start, day_end in daily_windows(start, end)
            for record in fetch_window(client, day_start, day_end)
        ]
    return rows


def timestamp_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp has no UTC offset")
    return parsed.astimezone(timezone.utc)
