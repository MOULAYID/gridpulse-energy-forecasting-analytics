from datetime import date

import httpx
import pytest

from gridpulse.ingestion.rte import RTEAPIError, daily_windows, fetch_window
from gridpulse.quality.rte import normalize


def test_daily_windows_exclusive():
    assert list(daily_windows(date(2025, 1, 1), date(2025, 1, 3))) == [
        (date(2025, 1, 1), date(2025, 1, 2)),
        (date(2025, 1, 2), date(2025, 1, 3)),
    ]


def test_paginated_api():
    calls = []

    def handler(request):
        calls.append(dict(request.url.params))
        offset = int(request.url.params["offset"])
        entries = [
            {"date_heure": "2025-01-01T00:00:00+00:00", "consommation": 50000},
            {"date_heure": "2025-01-01T00:30:00+00:00", "consommation": 51000},
            {"date_heure": "2025-01-01T01:00:00+00:00", "consommation": 52000},
        ]
        return httpx.Response(200, json={"total_count": 3, "results": entries[offset:offset + 2]})

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        result = fetch_window(client, date(2025, 1, 1), date(2025, 1, 2), limit=2)
    assert len(result) == 3
    assert [v["offset"] for v in calls] == ["0", "2"]
    assert "date_heure" in calls[0]["where"]


def test_missing_and_irregular_records():
    rows = [
        {"date_heure": "2025-01-01T00:00:00+00:00", "consommation": 50000},
        {"date_heure": "2025-01-01T00:15:00+00:00", "consommation": None},
        {"date_heure": "2025-01-01T00:30:00+00:00", "consommation": None},
        {"date_heure": "2025-01-01T01:00:00+00:00", "consommation": 52000},
        {"date_heure": "2025-01-01T01:00:00+00:00", "consommation": 52000},
    ]
    clean, report = normalize(rows)
    assert len(clean) == 2
    assert report["off_grid_timestamp"] == 1
    assert report["missing_or_invalid_demand"] == 1
    assert report["duplicate_timestamp"] == 1
    assert report["missing_half_hours_between_first_last"] == 1


def test_malformed_api_response():
    with httpx.Client(
        transport=httpx.MockTransport(lambda _: httpx.Response(200, json={"oops": []}))
    ) as client:
        with pytest.raises(RTEAPIError):
            fetch_window(client, date(2025, 1, 1), date(2025, 1, 2))
