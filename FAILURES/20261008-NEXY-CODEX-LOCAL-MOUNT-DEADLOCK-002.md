# Failure Record

FAILURE_ID: 20261008-NEXY-CODEX-LOCAL-MOUNT-DEADLOCK-002
CONTEXT: Prior Codex cycle ended without product mutation because the repository was not locally mounted and no runner was available.
FAILED_APPROACH: Treating local checkout availability as if it were equivalent to repository write capability.
CAUSE: Write capability and runner capability were not modeled independently.
RECOVERY: Re-query current remote GitHub write permission and use the authorized remote write surface for source-integrity repairs that do not require a local runner.
BOUNDARY: Runtime verification still requires a real runner and must remain unverified until executed.
PREVENTION: Separate capability states and keep blockers subsystem-local.
STATUS: RECORDED
