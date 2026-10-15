"""Load a previously validated RTE CSV into local PostgreSQL."""

from __future__ import annotations

import argparse
from pathlib import Path

from gridpulse.storage.postgres import load_demand


def main() -> None:
    parser = argparse.ArgumentParser(description="Load validated demand CSV to PostgreSQL")
    parser.add_argument("--csv", type=Path, required=True, help="Path to processed demand CSV")
    args = parser.parse_args()
    if not args.csv.is_file():
        parser.error(f"CSV does not exist: {args.csv}")
    schema = Path(__file__).resolve().parents[3] / "sql/schema/001_electricity_demand.sql"
    if not schema.is_file():
        parser.error(f"SQL schema file not found: {schema}")
    count = load_demand(args.csv, schema)
    print(f"Validated and upserted {count} observations into staging.electricity_demand")


if __name__ == "__main__":
    main()
