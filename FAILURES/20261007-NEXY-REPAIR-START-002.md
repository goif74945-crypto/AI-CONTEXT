# Failure — NEXY Repair Start Permission Gate

FAILURE_ID: FAILURE-20261007-NEXY-REPAIR-START-002
TASK_ID: 20261007-NEXY-REPAIR-START-002
DETECTED_UTC: 2026-10-07T14:10:59Z
CLASS: CAPABILITY / PERMISSION_BOUNDARY
STATUS: OPEN
SEVERITY: BLOCKING

## Failing precondition

The authorized product repository is configured read-only:

- repository: `goif74945-crypto/NEXY.AI-`
- branch: `NEXY.ai`
- observed HEAD: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- `read_only=true`
- `gateway_write_policy=DENY`

The gateway's GitHub permission probe reports pull/push/admin=true, but this does not override the configured read-only product policy.

## Consequence

The first product TDD RED step cannot be started because creating a regression test would require a product write. CI dispatch cannot be used as a substitute or bypass. There is no implementation failure diagnosis yet; the blocker is before code mutation.

## Integrity decision

- Product write attempted: NO
- Product CI dispatch attempted: NO
- Alternate/raw backend used: NO
- Branch changed: NO
- Product files changed: NO
- PASS_100 claimed: NO

## Required clearance

An authorized gateway configuration must change product write and CI dispatch to ALLOW for `NEXY.ai`. After clearance, re-query status and start from a newly frozen product HEAD; do not reuse a stale target or this blocked checkpoint as product evidence.
