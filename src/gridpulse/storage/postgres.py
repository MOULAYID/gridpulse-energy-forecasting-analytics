"""PostgreSQL persistence for validated RTE observations."""

from __future__ import annotations

import csv
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import create_engine, text

from gridpulse.config import Settings

UPSERT_SQL = text(
    """
    INSERT INTO staging.electricity_demand
        (timestamp_utc, source, demand_mw, data_status)
    VALUES (:timestamp_utc, :source, :demand_mw, :data_status)
    ON CONFLICT (source, timestamp_utc) DO UPDATE SET
        demand_mw = EXCLUDED.demand_mw,
        data_status = EXCLUDED.data_status,
        loaded_at_utc = now()
    WHERE
        staging.electricity_demand.demand_mw IS DISTINCT FROM EXCLUDED.demand_mw
        OR staging.electricity_demand.data_status IS DISTINCT FROM EXCLUDED.data_status
    """
)


def parse_csv(path: Path) -> list[dict[str, Any]]:
    """Validate a complete CSV before making any database changes."""
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, datetime]] = set()
    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        expected = {"timestamp_utc", "demand_mw", "data_status", "source"}
        if reader.fieldnames is None or set(reader.fieldnames) != expected:
            raise ValueError(f"Unexpected CSV columns: {reader.fieldnames}")
        for index, record in enumerate(reader, start=2):
            try:
                timestamp = datetime.fromisoformat(record["timestamp_utc"])
                demand = float(record["demand_mw"])
                source = record["source"].strip()
            except (TypeError, ValueError, KeyError) as exc:
                raise ValueError(f"Invalid data on CSV line {index}") from exc
            if timestamp.tzinfo is None or timestamp.utcoffset() != UTC.utcoffset(None):
                raise ValueError(f"CSV line {index}: timestamp must be UTC")
            if (
                timestamp.minute not in (0, 30)
                or timestamp.second != 0
                or timestamp.microsecond != 0
            ):
                raise ValueError(f"CSV line {index}: unexpected half-hour timestamp")
            if not (0 <= demand < float("inf")):
                raise ValueError(f"CSV line {index}: demand must be finite and nonnegative")
            if not source:
                raise ValueError(f"CSV line {index}: source is empty")
            key = (source, timestamp)
            if key in seen:
                raise ValueError(f"CSV line {index}: duplicate source/timestamp")
            seen.add(key)
            rows.append(
                {
                    "timestamp_utc": timestamp,
                    "demand_mw": demand,
                    "data_status": record["data_status"] or None,
                    "source": source,
                }
            )
    return rows


def load_demand(csv_path: Path, schema_path: Path, database_url: str | None = None) -> int:
    """Initialize staging schema, then atomically upsert validated observations."""
    rows = parse_csv(csv_path)
    ddl = schema_path.read_text(encoding="utf-8")
    engine = create_engine(database_url or Settings().database_url, pool_pre_ping=True)
    try:
        with engine.begin() as connection:
            # SQL file contains three fixed statements. Never load arbitrary user SQL here.
            for statement in ddl.split(";"):
                if statement.strip():
                    connection.execute(text(statement))
            if rows:
                connection.execute(UPSERT_SQL, rows)
    finally:
        engine.dispose()
    return len(rows)
