# Architecture and engineering conventions

## Objective and scope
Start with **French national hourly demand**, weather covariates and one-day-ahead predictions. Keep the design modular but a **single deployable Python package**; no microservices.

## Data flow
1. **Source adapters** fetch RTE consumption and Open-Meteo observations/forecasts, handling pagination, retries, rate limits and provenance.
2. **Raw layer** preserves source responses, retrieval timestamps, versions and units. Ingestion is idempotent by natural source key.
3. **Staging/quality** parses timestamps into UTC, aligns weather and demand resolution, validates gaps/duplicates, marks provisional readings and flags anomalies without silently filling observations.
4. **Analytical marts** expose hourly demand, weather predictors, generation mix (later) and dimensions for BI.
5. **Forecasting** trains baselines, uses rolling-origin chronological evaluation, persists models externally and predictions in SQL (issue time, target time, horizon, model version, intervals).
6. **Power BI** reads curated marts, actuals, model metrics and historical predictions. Start with Import mode and explicit refresh; avoid requiring a live database for portfolio viewers.

## Source-of-truth / layers
- PostgreSQL schemas: `raw`, `staging`, `marts`, `ml` (planned; not provisioned yet).
- Repository code is versioned. Operational data, credentials, caches and serialized models are not.
- SQL is used for stable, testable transformations; Python is used for API ingestion and models.
- Notebook code is exploratory; production logic belongs in `src/gridpulse`.

## Time series integrity
- Store timestamps in UTC as timezone-aware datetimes; present Europe/Paris reporting times with explicit DST handling.
- Use explicit units: demand power MW vs energy MWh; never sum MW readings as if they are MWh.
- Forecast evaluation must simulate prediction cutoff. Weather **actuals** cannot be used as predictors for future periods in retrospective backtests; use archived forecasts or a documented alternative.
- Split by time; benchmark against seasonal naive. Preserve model version and feature provenance.

## Development standards
- Python 3.11+, typed functions, focused tests, Ruff, README and architecture decisions.
- Changes via branches and pull requests; CI checks lint and tests.
- Secrets in env/secret stores; only `.env.example` goes to Git.
- Prefer clear error handling, structured logs and deterministic CLI jobs over premature orchestration platforms.

## Architecture decisions
See `docs/decisions/`. This design intentionally starts as a monorepo and is extended one tested vertical slice at a time.
