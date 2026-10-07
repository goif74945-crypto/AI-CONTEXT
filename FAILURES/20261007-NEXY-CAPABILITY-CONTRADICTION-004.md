# Failure — NEXY CI Dispatch Capability Contradiction

FAILURE_ID: FAILURE-20261007-NEXY-CAPABILITY-CONTRADICTION-004
TASK_ID: 20261007-NEXY-CAPABILITY-CONTRADICTION-004
STATUS: OPEN
SEVERITY: BLOCKING
DETECTED_UTC: 2026-10-07T16:04:52Z

## Evidence

Status snapshots reported:

- product `read_only=false`
- product `gateway_write_policy=ALLOW`
- runtime `read_only_repository_count=0`

The actual authorized dispatch call returned:

- `REPOSITORY_READ_ONLY`
- HTTP 403
- repository: `goif74945-crypto/NEXY.AI-`
- operation: `ci_dispatch`

## Root cause classification

Gateway capability/state inconsistency or stale policy propagation. The exact internal cause is UNKNOWN; no assumption is permitted.

## Safety consequence

CI dispatch is not available in practice. Because the locked command requires write and CI capabilities before product edits, the repair remains blocked. No product write probe was attempted after the dispatch contradiction, and no alternate backend was used.

## Clearance

Make the capability response and operation gate consistent. A successful authorized diagnostic dispatch is required before starting product TDD.
