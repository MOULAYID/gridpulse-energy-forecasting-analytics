import csv
from pathlib import Path

import pytest

from gridpulse.storage.postgres import parse_csv


def write_csv(tmp_path: Path, records: list[dict[str, str]]) -> Path:
    file = tmp_path / "sample.csv"
    with file.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(
            output, fieldnames=["timestamp_utc", "demand_mw", "data_status", "source"]
        )
        writer.writeheader()
        writer.writerows(records)
    return file


def row(**overrides):
    record = {
        "timestamp_utc": "2025-01-01T00:00:00+00:00",
        "demand_mw": "51000.0",
        "data_status": "D",
        "source": "RTE eco2mix-national-cons-def",
    }
    return record | overrides


def test_reads_valid_rows(tmp_path):
    records = parse_csv(write_csv(tmp_path, [row()]))
    assert len(records) == 1
    assert records[0]["demand_mw"] == 51000.0


@pytest.mark.parametrize(
    "invalid",
    [
        {"timestamp_utc": "2025-01-01T00:00:00"},
        {"timestamp_utc": "2025-01-01T00:15:00+00:00"},
        {"demand_mw": "-2"},
        {"demand_mw": "nan"},
        {"demand_mw": "inf"},
        {"source": ""},
    ],
)
def test_rejects_bad_rows(tmp_path, invalid):
    with pytest.raises(ValueError):
        parse_csv(write_csv(tmp_path, [row(**invalid)]))


def test_rejects_duplicate_rows(tmp_path):
    with pytest.raises(ValueError, match="duplicate"):
        parse_csv(write_csv(tmp_path, [row(), row()]))
