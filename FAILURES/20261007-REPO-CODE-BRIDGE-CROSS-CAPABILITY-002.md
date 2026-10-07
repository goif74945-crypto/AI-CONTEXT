# FAILURES — 20261007-REPO-CODE-BRIDGE-CROSS-CAPABILITY-002

FAILURE_ID: FAILURE-20261007-RBC-STALE-HANDOFF-001
CONTEXT: Existing AI-CONTEXT task record was read at current AI-CONTEXT HEAD but contained an older product-access state and older AI-CONTEXT head.
CAUSE: Stale coordination record; no live-head refresh in that record.
IMPACT: False BLOCKED conclusion if reused.
RECOVERY: Re-queried live catalog, runtime, product status, product read/search, and VS Code URL; recorded reconciled evidence.
BOUNDARY: Coordination-data quality issue; not evidence of a product-repository failure.
PREVENTION: Every handoff must carry exact current HEAD/STATE and be independently refreshed.

FAILURE_ID: FAILURE-20261007-RBC-LOCAL-ROUTING-002
CONTEXT: First post-write verification wrapper referenced unavailable alias repo_status.
CAUSE: Tool-routing name mismatch.
IMPACT: Local wrapper failed before completing verification; no remote action occurred.
RECOVERY: Re-ran with repo_code_bridge_repo_status; AI-CONTEXT and product status plus evidence read-back succeeded.
BOUNDARY: Local orchestration error only.
PREVENTION: Resolve exact tool names from the live registry before composing calls.
STATUS: RECOVERED; retained for regression memory.
