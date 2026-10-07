# Failure — NEXY Exact-Head Test Runner Unavailable

FAILURE_ID: FAILURE-20261007-NEXY-RAILWAY-DIAGNOSTIC-005
TASK_ID: 20261007-NEXY-RAILWAY-DIAGNOSTIC-005
STATUS: OPEN
SEVERITY: BLOCKING
DETECTED_UTC: 2026-10-07T16:19:21Z

## Facts

- Current target product HEAD: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.
- Railway failures available are from `6769b725e46753ce5af58a972c005894065f38da` and `dd9e691e346e97701877ad6e2e5ff5642ca1b068`.
- Neither deployment is exact-head evidence for `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.
- Repo Code Bridge `ci_dispatch` returned HTTP 403 `REPOSITORY_READ_ONLY`.
- No fresh exact-head Railway deployment was started.

## Consequence

The current test failures identify historical defects but cannot safely drive a Product patch without inspecting the exact current source and running a new RED test on the target HEAD. The required execution path remains blocked.

## Clearance

Restore a consistent authorized write/CI capability. Then run tests against a newly frozen HEAD and tie every result to that SHA.
