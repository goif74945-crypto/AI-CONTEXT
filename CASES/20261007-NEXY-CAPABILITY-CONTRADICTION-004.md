# Case — NEXY Gateway Capability Contradiction

CASE_ID: CASE-20261007-NEXY-CAPABILITY-CONTRADICTION-004
TASK_ID: 20261007-NEXY-CAPABILITY-CONTRADICTION-004
STATUS: BLOCKED_WITH_RESUME
OPENED_UTC: 2026-10-07T16:04:52Z

## Reproduction

1. Query runtime and product status for `goif74945-crypto/NEXY.AI-` / `NEXY.ai`.
2. Observe `read_only=false` and `gateway_write_policy=ALLOW`.
3. Dispatch `omega-runner-diagnostic.yml` at product HEAD `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.

## Observed failure

The authorized gateway returns:

- code: `REPOSITORY_READ_ONLY`
- HTTP status: 403
- operation: `ci_dispatch`
- allowed operations: runtime_status, repo_catalog, repo_status, repo_read, repo_search, repo_diff, ci_status, open_vscode

## Expected

The status probe and the actual operation gate must agree. The locked command requires both product write and CI dispatch to be explicitly usable before code changes.

## Decision

Capability is ambiguous and CI dispatch is operationally denied. Fail closed. No product mutation is safe or valid under the exact-head acceptance contract.
