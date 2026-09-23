# NEXY.AI Observability Map

## Purpose
Per-current-build entity map of expected logs/metrics/traces/alerts/health/failure signatures.

## Truth boundary
The source requires monitoring of errors, resources, performance, security and AI decisions; DOC-C separates Event/Audit/Security/Freeze records; DOC-E requires exercised alerts for auth abuse, freeze, worker down, queue backlog, database failure and release-policy failure.

The source does **not** lock a complete per-system SLO/metric threshold set. Therefore:
- `slo = SOURCE_NOT_SPECIFIED` where no authoritative SLO is present.
- metric names in this registry are monitoring categories/navigation intelligence unless directly locked by source.
- runtime observability remains NOT_VERIFIED until evidence exists.

## Files
- `observability.jsonl` — 13 current-build entity records.
- `alerts.json` — source-required alert classes.
- `observability.schema.json`.
- `validation-report.md`.

## Critical rule
Having log/metric code does not prove alarms flow or trigger. DOC-E E8 requires exercised monitoring/alarm evidence.
