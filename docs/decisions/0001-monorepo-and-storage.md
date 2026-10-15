# ADR 0001: Small Python monorepo with PostgreSQL

**Status:** Accepted (initial design)

## Context
The project must demonstrate ingestion, analytical SQL, forecasting and Power BI while remaining easy to run and explain.

## Decision
Use one installable `src/gridpulse` Python package; organize by bounded responsibilities. Adopt PostgreSQL for curated analytics and forecast history in Phase 2. Store Power BI PBIP/TMDL as text where supported.

## Consequences
Easy local development, unit tests and CI. No unnecessary microservices. Database and orchestration are introduced only when the first API client and contract are proven.
