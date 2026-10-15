# Roadmap

## Phase 0 — Foundation (this change)
- [x] Repository structure and typed Python package
- [x] Architecture and contracts documentation
- [x] Basic unit test and CI checks
- [ ] Verify local editable installation and CI run

## Phase 1 — First real data (next)
- [ ] Verify RTE dataset field names, coverage, API limits and license
- [ ] Implement one paginated API client + CLI and deterministic local sample
- [ ] Validate UTC timestamps, MW units, duplicates and time gaps
- [ ] Add mocked HTTP tests and source provenance

## Phase 2 — Storage and transformations
- [ ] Docker Compose PostgreSQL and migrations
- [ ] Raw/staging/mart tables and idempotent incremental loads
- [ ] Data validation and SQL tests

## Phase 3 — Descriptive Power BI
- [ ] Build semantic star schema, DAX measures and first report page

## Phase 4 — Weather and forecasting
- [ ] Integrate weather, archived forecasts and calendar features
- [ ] Seasonal-naive baseline, SARIMAX and XGBoost
- [ ] Rolling backtest, error metrics, prediction intervals and saved vintages

## Phase 5 — Operations and polish
- [ ] Scheduling, logging, freshness alerts, model monitoring and retraining
- [ ] Additional Power BI pages, reproducibility, demo, and case-study README
