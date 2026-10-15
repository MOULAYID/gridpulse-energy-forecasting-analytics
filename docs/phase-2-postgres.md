# Phase 2 — Local PostgreSQL persistence

## Prerequisites
- Docker Desktop running with Linux containers.
- Git Bash Python virtual environment activated.
- Phase 1 succeeded and generated a cleaned RTE CSV.

## Commands (Git Bash)
```bash
git pull origin chore/phase-0-project-foundation
source .venv/Scripts/activate
python -m pip install -e ".[dev]"
python -m pytest -q
python -m ruff check src tests

docker compose up -d postgres
docker compose ps
cp .env.example .env
python -m gridpulse.storage.cli --csv data/processed/rte_2025-01-01_2025-01-08.csv

docker compose exec postgres psql -U gridpulse -d gridpulse -c "SELECT count(*) AS observations, min(timestamp_utc), max(timestamp_utc) FROM staging.electricity_demand;"
```

Run the same `python -m gridpulse.storage.cli` command twice. Row count must **not** increase. Existing observations will only update when their recorded values change.

## Schema
`staging.electricity_demand` stores validated half-hourly power (MW). Its composite primary key is (source, timestamp_utc). The SQL table schema is tracked at `sql/schema/001_electricity_demand.sql`.

## Limitations & next improvements
- This phase imports a previously validated local CSV, not a scheduled ingestion job.
- The original JSONL is retained locally but not yet persisted to a PostgreSQL raw schema.
- DDL is intentionally minimal; formal versioned migration tooling is planned after the first database slice.
- Only local credentials are provided; production credential management is out of scope.
- A real PostgreSQL integration test and source-level coverage audit are next.
- Power BI comes after SQL time aggregation and the first analytics mart.
