# Initial data contracts (design, subject to source verification)

## Electricity consumption (target)
- `timestamp_utc`: timezone-aware UTC observation time (hourly granularity after aggregation).
- `demand_mw`: nonnegative measured power in MW.
- `source`, `retrieved_at_utc`, `source_status`: lineage and revision/finality metadata.
- Uniqueness: (source, timestamp_utc, granularity). Do not infer that measurements are energy totals.

## Weather covariates
- `timestamp_utc`, `region_or_station_id`, `temperature_c`, `wind_speed`, `source`.
- Keep weather observation vs archived forecast distinct with `forecast_issued_at_utc` when applicable.
- Spatial matching/aggregation strategy must be documented before modeling.

## Forecast outputs
- `model_name`, `model_version`, `issued_at_utc`, `target_at_utc`, `horizon_hours`
- `prediction_mw`, optional `lower_mw`/`upper_mw`, `interval_level`, `run_id`
- Preserve multiple forecast vintages, never overwrite historical predictions.
- Evaluate forecasts only against an actual target that has subsequently arrived.

## Acceptance checks
Complete hourly UTC timeline over the expected coverage; no duplicate natural keys; correct units; valid timezone; explicit missingness report and source freshness. Do not impute raw missing values silently.
