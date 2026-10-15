# Power BI

Store authored Power BI Project (PBIP) and TMDL source-controlled files here when the semantic model and report exist. Do not commit local caches, credentials, or large generated model data.

Planned report pages: Executive Overview, Forecast & Accuracy, Energy Mix, Demand Drivers, Data Quality.

Report data is sourced from PostgreSQL analytical marts and persisted forecast tables. DAX measures belong in the semantic model; heavy reshaping should happen upstream.
