# GridPulse — Energy Forecasting & Analytics

End-to-end portfolio project for **French electricity demand analytics and forecasting**, using public electricity and weather APIs, Python, PostgreSQL, machine learning and Power BI.

> **Status:** Phase 0 — repository foundation. Forecasts, pipelines and dashboards are not implemented yet.

## Project goals
- Ingest documented public electricity and weather data reproducibly.
- Validate completeness, timestamps, units and data quality before analysis.
- Model reliable analytical data in PostgreSQL for Power BI.
- Compare one-day-ahead forecasts against seasonal-naive baselines using leakage-safe chronological backtests.
- Monitor predictions, uncertainty and data freshness in an interactive report.

## Planned architecture
```text
RTE + Open-Meteo APIs
        |
        v
Python ingestion + validation
        |
        v
PostgreSQL: raw -> staging -> marts
        |                     ^
        v                     |
Feature engineering -> backtesting / model training -> stored forecasts
        |
        +--------------------------> Power BI semantic model + reports
```

See [architecture](docs/architecture.md), [project roadmap](docs/roadmap.md) and [data contracts](docs/data-contracts.md).

## Getting started (Phase 0)
Requires Python 3.11+.

```bash
git clone https://github.com/MOULAYID/gridpulse-energy-forecasting-analytics.git
cd gridpulse-energy-forecasting-analytics
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest
```

Copy `.env.example` to `.env` when configuring the database later. Do not commit `.env` or API credentials.

## Repository layout
- `src/gridpulse/`: reusable Python package (ingestion, quality, transformations, forecasting).
- `sql/`: PostgreSQL DDL and analytic SQL.
- `powerbi/`: Power BI project files and DAX documentation when implemented.
- `tests/`: unit and integration tests.
- `docs/`: architecture, contracts, decisions, roadmap and results.
- `notebooks/`: exploration only; reusable logic goes in `src/`.
- `data/`: local raw/interim/processed data; excluded from Git.

## Engineering principles
Time zones are explicit (UTC in storage, Europe/Paris only for reporting), forecasts have an **issue time** and a **target time**, and backtests never read observations or weather forecasts that were unavailable at prediction time.

## License
MIT (see `LICENSE`). Data sources remain subject to their own terms and attribution requirements.
