CREATE SCHEMA IF NOT EXISTS marts;

CREATE OR REPLACE VIEW marts.hourly_demand AS
SELECT
    source,
    date_trunc('hour', timestamp_utc AT TIME ZONE 'UTC') AT TIME ZONE 'UTC' AS hour_utc,
    COUNT(*)::integer AS observations,
    AVG(demand_mw)::double precision AS avg_demand_mw,
    MIN(demand_mw) AS min_demand_mw,
    MAX(demand_mw) AS peak_demand_mw,
    CASE WHEN COUNT(*) = 2
         THEN SUM(demand_mw) * 0.5
         ELSE NULL END AS energy_mwh,
    COUNT(*) = 2 AS is_complete_hour
FROM staging.electricity_demand
GROUP BY source, date_trunc('hour', timestamp_utc AT TIME ZONE 'UTC') AT TIME ZONE 'UTC';

CREATE OR REPLACE VIEW marts.daily_demand AS
SELECT
    source,
    (hour_utc AT TIME ZONE 'UTC')::date AS date_utc,
    COUNT(*)::integer AS hours_with_data,
    COUNT(*) FILTER (WHERE is_complete_hour)::integer AS complete_hours,
    SUM(observations)::integer AS observations,
    AVG(avg_demand_mw) FILTER (WHERE is_complete_hour) AS avg_complete_hour_demand_mw,
    MAX(peak_demand_mw) AS peak_demand_mw,
    CASE WHEN COUNT(*) = 24 AND BOOL_AND(is_complete_hour)
         THEN SUM(energy_mwh)
         ELSE NULL END AS energy_mwh,
    COUNT(*) = 24 AND BOOL_AND(is_complete_hour) AS is_complete_day
FROM marts.hourly_demand
GROUP BY source, (hour_utc AT TIME ZONE 'UTC')::date;

CREATE OR REPLACE VIEW marts.demand_quality AS
WITH limits AS (
    SELECT source, MIN(timestamp_utc) AS first_utc, MAX(timestamp_utc) AS last_utc
    FROM staging.electricity_demand
    GROUP BY source
), expected AS (
    SELECT limits.source, slot_utc
    FROM limits
    CROSS JOIN LATERAL generate_series(
        limits.first_utc, limits.last_utc, interval '30 minutes'
    ) AS slot_utc
)
SELECT
    e.source,
    COUNT(*)::integer AS expected_half_hours_between_bounds,
    COUNT(d.timestamp_utc)::integer AS observed_half_hours_between_bounds,
    (COUNT(*) - COUNT(d.timestamp_utc))::integer AS missing_half_hours_between_bounds,
    ROUND((100.0 * COUNT(d.timestamp_utc) / NULLIF(COUNT(*), 0))::numeric, 2)
        AS completeness_pct_between_bounds
FROM expected e
LEFT JOIN staging.electricity_demand d
    ON d.source = e.source AND d.timestamp_utc = e.slot_utc
GROUP BY e.source;
