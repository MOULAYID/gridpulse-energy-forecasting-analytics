"""Normalize RTE demand observations and summarize data quality."""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from typing import Any

from gridpulse.ingestion.rte import timestamp_utc


def normalize(
    records: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Keep valid half-hour demand rows; never interpolate or silently invent demand."""
    clean: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    seen: set[datetime] = set()
    for raw in records:
        counts["raw_records"] += 1
        try:
            ts = timestamp_utc(str(raw["date_heure"]))
        except (KeyError, TypeError, ValueError):
            counts["invalid_timestamp"] += 1
            continue
        # Historical dataset may include 15/45-minute auxiliary rows without consumption.
        if ts.minute not in (0, 30) or ts.second != 0:
            counts["off_grid_timestamp"] += 1
            continue
        if ts in seen:
            counts["duplicate_timestamp"] += 1
            continue
        seen.add(ts)
        demand = raw.get("consommation")
        if isinstance(demand, bool) or not isinstance(demand, (int, float)):
            counts["missing_or_invalid_demand"] += 1
            continue
        if demand < 0:
            counts["negative_demand"] += 1
            continue
        clean.append(
            {
                "timestamp_utc": ts.isoformat(),
                "demand_mw": demand,
                "data_status": raw.get("nature"),
                "source": "RTE eco2mix-national-cons-def",
            }
        )
    clean.sort(key=lambda r: r["timestamp_utc"])
    counts["valid_records"] = len(clean)
    if clean:
        from datetime import timedelta

        first = datetime.fromisoformat(clean[0]["timestamp_utc"])
        last = datetime.fromisoformat(clean[-1]["timestamp_utc"])
        expected = int((last - first) / timedelta(minutes=30)) + 1
        counts["missing_half_hours_between_first_last"] = expected - len(clean)
    return clean, dict(counts)
