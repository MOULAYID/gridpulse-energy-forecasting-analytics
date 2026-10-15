"""Create reproducible analytical views for Power BI."""

from __future__ import annotations

import argparse
from pathlib import Path

from sqlalchemy import create_engine, text

from gridpulse.config import Settings


def main() -> None:
    parser = argparse.ArgumentParser(description="Create GridPulse PostgreSQL analytical views")
    parser.add_argument(
        "--sql",
        type=Path,
        default=Path(__file__).resolve().parents[3] / "sql/marts/001_demand_views.sql",
    )
    args = parser.parse_args()
    if not args.sql.is_file():
        parser.error(f"SQL file not found: {args.sql}")
    engine = create_engine(Settings().database_url, pool_pre_ping=True)
    try:
        with engine.begin() as connection:
            for statement in args.sql.read_text(encoding="utf-8").split(";"):
                if statement.strip():
                    connection.execute(text(statement))
    finally:
        engine.dispose()
    print("Created or updated marts.hourly_demand, marts.daily_demand, marts.demand_quality")


if __name__ == "__main__":
    main()
