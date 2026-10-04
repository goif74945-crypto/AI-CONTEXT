# Recovery Playbook

## Universal loop
Detect → classify → contain → inspect evidence → choose smallest safe correction → execute → verify correction → regression check → resume objective.

## Recovery classes
R1 transient external: bounded retry with backoff.
R2 invalid input: correct input only with evidence.
R3 stale state: refresh and reconcile.
R4 conflict: freeze dependent mutation.
R5 partial mutation: determine actual state before replay.
R6 corrupted artifact: restore from verified source/rollback.
R7 permission/auth: block and request required authorization; never bypass.
R8 unknown root cause: increase observability; do not random-walk mutations.

## Retry budget
Retries must be bounded and keyed by failure fingerprint. Identical failures without new information should not consume infinite attempts.

## Rollback gate
Before risky mutation, know:
- what changes,
- how to detect success,
- how to detect partial success,
- rollback mechanism,
- data that cannot be restored.

## Resume safety
A checkpoint must distinguish "planned", "attempted", "succeeded", and "verified". Only verified state is safe to assume after interruption.

## Escalation
Escalate when action is irreversible, authority is unresolved, credentials are required, data loss is possible, or repeated recovery attempts do not change evidence.
