# Roadmap

## Phase 0 — Foundation
- [x] Repository structure, package, architecture documentation and CI

## Phase 1 — First real data
- [x] RTE paginated API client, UTC normalization, exports and unit tests
- [x] Local historical download and successful ingestion (user verified for Jan 1–7 2025)

## Phase 2 — Local database
- [x] PostgreSQL Docker service and initial SQL table
- [x] Validated CSV loader with idempotent upserts
- [x] 336 observations stored Jan 1–7 2025 (user verified)
- [ ] Repeat import and verify no row-count increase
- [ ] Add database integration tests, formal migration tooling and raw source lineage

## Phase 3 — Power BI preparation
- [x] Add reproducible hourly, daily and quality SQL views
- [ ] Run SQL views locally and validate complete hours/days
- [ ] Ingest enough history for meaningful KPI trend comparisons
- [ ] Connect Power BI Desktop and build executive overview

## Phase 4 — Forecasting
- [ ] Weather covariates, archived forecasts and calendar features
- [ ] Seasonal baseline, SARIMAX, XGBoost and rolling-origin evaluation

## Phase 5 — Operations and publication
- [ ] Scheduling, model monitoring, documentation, portfolio demo and final report
