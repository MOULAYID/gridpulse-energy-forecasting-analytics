# Roadmap

## Phase 0 — Foundation
- [x] Repository structure, package, architecture documentation and CI

## Phase 1 — First real data
- [x] RTE paginated API client, UTC normalization, exports and unit tests
- [ ] Verify successful live historical download and review QA output locally

## Phase 2 — Local database (current)
- [x] PostgreSQL Docker service and initial SQL table
- [x] Validated CSV loader with repeatable upserts
- [x] Unit tests for malformed, missing, duplicate and nonfinite values
- [ ] Run ingestion/loader twice locally and verify duplicate prevention
- [ ] Add database integration test and fuller raw/staging lineage
- [ ] Add hourly marts and coverage audit

## Phase 3 — Descriptive Power BI
- [ ] Connect Power BI Desktop to PostgreSQL
- [ ] Star schema, measures and executive overview

## Phase 4 — Forecasting
- [ ] Weather covariates and archived forecasts
- [ ] Seasonal baseline, SARIMAX, XGBoost and rolling-origin evaluation

## Phase 5 — Operations and publication
- [ ] Scheduling, monitoring, docs, portfolio demo and final report
