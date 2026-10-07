# Failure Record — Stale Builder Command Deadlock Patterns

FAILURE_ID: 20261008-NEXY-GPT56-SOL-COMMAND-AUDIT-001
CONTEXT: Previous NEXY builder command design.
CAUSES:
1. hard-locked stale branch assumptions
2. global stop when CI/write gateway denied
3. single-tool dependency
4. conflation of infrastructure failure with code failure
5. strict RED-before-write even for structural fixes without runner
6. historical evidence promoted too easily
7. no concurrency branch/HEAD recheck before every mutation
FAILED_APPROACH: Treat product write + CI dispatch + one gateway as one global precondition.
RECOVERY: V4 splits capabilities, localizes blockers, routes across independently authorized tools, and requires live branch/head readback.
BOUNDARY: Permission denial is never bypassed; only independently authorized tools may be used.
PREVENTION: 28-round adversarial prompt audit and final live-state recheck.
STATUS: MITIGATED_IN_V4