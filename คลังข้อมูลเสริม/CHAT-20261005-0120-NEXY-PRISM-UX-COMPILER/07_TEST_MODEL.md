# NEXY::PRISM Verification Model

## Evidence classes
- E0: artifact/file presence.
- E1: Python compilation/static syntax.
- E2: executed unit and exhaustive invariant tests.

No E3/E4/E5/E6 claim is made because this has not been integrated into NEXY runtime, UI, or deployment.

## Focused coverage
Verified stable result; backend deny non-escalation; FREEZE operator denial; OWNER recovery; non-recoverable freeze; auditor config denial; irreversible typed confirmation; critical-risk truth floor; unverified non-finality; contradictory release fail-closed; STOP diagnostics; deterministic fingerprints.

## Exhaustive cross-product
- 8 system states
- 5 roles
- 7 evidence statuses
- 8 requested actions
- 4 risk levels
- 3 detail preferences
- 2 backend-authorization values
- 2 release-authorization values
- 2 recoverable values
- 2 irreversible values

Total: **430,080 deterministic scenarios**.

Each plan is validated for authorization non-escalation, finality prerequisites, FREEZE/STOP visibility, action legality, typed confirmation, blocked-state detail floor, release prerequisites, and fingerprint replay determinism.
