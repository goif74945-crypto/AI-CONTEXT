# Autonomous Agent State Machine
INTAKE -> REQUIREMENT_LOCK -> INSPECT -> PLAN -> EXECUTE -> VERIFY -> (FIX -> REVERIFY)* -> FINAL_AUDIT -> COMPLETE.
Exceptional states: BLOCKED, CONFLICT, AUTH_REQUIRED, NOT_VERIFIED, ROLLBACK_REQUIRED.

## Transition rules
- No high-impact execution before requirement lock.
- VERIFY failure cannot transition directly to COMPLETE.
- Requirement conflict enters CONFLICT.
- Missing required authority enters AUTH_REQUIRED.
- FINAL_AUDIT evaluates the complete acceptance set, not merely the latest patch.
- COMPLETE is derived from evidence, never chosen as conversational wording.

## Compact execution state
CURRENT_STATE; OBJECTIVE; LOCKED_REQUIREMENTS; COMPLETED; IN_PROGRESS; BLOCKERS; NEXT_ACTION; LAST_VERIFIED_CHECKPOINT; REGRESSION_RISK.

## Ask-user stop conditions
Ask only when authority is insufficient, requirements materially conflict, irreversible high-impact action lacks authorization, required credential is unavailable, or ambiguity changes architecture/acceptance.

## Loop control
failure_fingerprint = class + target + verifier. Repeated identical failure without new evidence must change strategy or enter BLOCKED, not infinite retry.
