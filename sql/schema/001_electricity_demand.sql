-- Phase 2: validated half-hour electricity power observations.
-- Store UTC time with timestamptz. Do not impute missing values in this table.
CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.electricity_demand (
    timestamp_utc TIMESTAMPTZ NOT NULL,
    source TEXT NOT NULL,
    demand_mw DOUBLE PRECISION NOT NULL CHECK (demand_mw >= 0),
    data_status TEXT,
    loaded_at_utc TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (source, timestamp_utc)
);

CREATE INDEX IF NOT EXISTS electricity_demand_time_idx
    ON staging.electricity_demand (timestamp_utc);
