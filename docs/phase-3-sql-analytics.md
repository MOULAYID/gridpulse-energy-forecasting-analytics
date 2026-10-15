# SQL analytics layer — Power BI preparation

## Build views (Git Bash)
```bash
git pull origin chore/phase-0-project-foundation
source .venv/Scripts/activate
python -m gridpulse.storage.marts_cli

docker compose exec postgres psql -U gridpulse -d gridpulse -c "SELECT * FROM marts.demand_quality;"
docker compose exec postgres psql -U gridpulse -d gridpulse -c "SELECT date_utc, observations, complete_hours, peak_demand_mw, round(energy_mwh::numeric, 1) AS energy_mwh FROM marts.daily_demand ORDER BY date_utc;"
docker compose exec postgres psql -U gridpulse -d gridpulse -c "SELECT count(*) AS hourly_rows, count(*) FILTER (WHERE is_complete_hour) AS complete_hours FROM marts.hourly_demand;"
```

The expected results for a completely populated 7-day UTC window are: **336** observed half-hour periods, **168** complete hours and **7** complete days. Validate actual results rather than assuming completeness from the total count alone.

## Measurement definitions
- `demand_mw`: observed power, MW, at 30-minute frequency.
- `avg_demand_mw`: arithmetic mean of two half-hourly readings, MW, when both exist.
- `peak_demand_mw`: maximum observed half-hour demand during the period, MW.
- `energy_mwh`: approximate half-hour integration (`0.5 h * sum(MW)`). Only reported when complete. Interpret as an estimate depending on RTE's interval semantics; do not call the sum of MW an energy total.
- Date grouping: **UTC**, not local French civil days. A later Power BI calendar model will handle Europe/Paris daylight-saving rules explicitly.

## Caveats
- Views track source coverage **between first/last stored observations only**, not unobserved boundary slots.
- Missing half-hour periods result in incomplete hours and days, where total energy is NULL.
- Daily averages include only complete hours.
- The first report can connect to these three views using Power BI Desktop **Import** mode with the PostgreSQL connector.
- For a portfolio-ready trend model, ingest several months or years before evaluating seasonality or forecasting; seven days only validate the pipeline.
