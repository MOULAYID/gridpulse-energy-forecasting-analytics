# Phase 1 — Download and inspect real RTE data

RTE source: [éCO2mix national consolidated/final](https://odre.opendatasoft.com/explore/dataset/eco2mix-national-cons-def/information/).
API uses Opendatasoft Explore v2.1 records endpoint.

## Windows PowerShell
```powershell
git clone https://github.com/MOULAYID/gridpulse-energy-forecasting-analytics.git
cd gridpulse-energy-forecasting-analytics
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m gridpulse.ingestion.cli --start 2025-01-01 --end 2025-01-08
```

The end date is **exclusive**. The tool writes:
- `data/raw/rte_<start>_<end>.jsonl` — unmodified API rows.
- `data/processed/rte_<start>_<end>.csv` — clean half-hourly demand (MW).
- `data/processed/rte_<start>_<end>_quality.json` — QA summary.

Source responses are historical and may be corrected retroactively. The raw extract is a snapshot, not a revision-proof log. The script filters non-half-hour timestamps and invalid demand from the clean layer, but preserves them in raw. It does not interpolate missing values. Current QA gap counts refer only to gaps **between first/last retained rows**; boundary coverage checks will be added later.

## PostgreSQL via Docker Desktop
```powershell
docker compose up -d postgres
docker compose ps
```
The database is ready for Phase 2; **the Phase 1 CLI does not load it yet**. Credentials in `compose.yaml` are deliberately local-only placeholders; do not deploy this compose file publicly. Stop locally using `docker compose down` (keep volume) or `docker compose down -v` (delete local data).

## Source caveats
RTE records are supplied at half-hour frequency, not hourly. Historical data can include auxiliary 15/45-minute records with null demand. Store UTC timestamps; do not confuse MW (instantaneous/interval power) with MWh (energy). Only aggregate into hourly values deliberately in a later phase.

RTE also publishes `prevision_j1` and `prevision_j` forecast fields. We will analyze these as optional documented benchmarks later, without assuming availability or issue timestamps per observation.

## Validation acceptance criteria
1. CLI exits successfully for one historical week.
2. Raw JSONL and clean CSV files are non-empty.
3. Quality JSON reports counts and does not conceal missing or off-grid records.
4. `python -m pytest -q` and `ruff check src tests` pass.

**This document describes local steps; we have not run live API download inside the user’s Windows machine.**
