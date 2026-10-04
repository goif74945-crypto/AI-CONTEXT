# AI-PROPOSED CONCEPT — Failure Atlas & Freeze Semantics
Status: PROPOSAL / ADVISORY / NOT CURRENT REQUIREMENT

SOURCE_FACT: NEXY favors explicit freeze over guessing or unsafe continuation.
AI_PROPOSED_CONCEPT: standardize failures as typed machine-actionable records.

## Failure classes
INPUT_INVALID; INPUT_AMBIGUOUS; AUTHORITY_CONFLICT; POLICY_DENIED; EVIDENCE_MISSING; EVIDENCE_CONFLICT; DEPENDENCY_UNAVAILABLE; DEPENDENCY_UNTRUSTED; TOOL_FAILURE; MODEL_FAILURE; TIMEOUT; RESOURCE_EXHAUSTION; CONCURRENCY_CONFLICT; STATE_CORRUPTION; SECURITY_VIOLATION; PROVENANCE_BREAK; NONDETERMINISM_DETECTED; VERIFICATION_FAILURE; DEPLOYMENT_MISMATCH; PHYSICAL_SAFETY_TRIP.

Dimensions:
- severity S0..S4
- recoverability: RETRY_SAFE / RETRY_WITH_BACKOFF / REQUIRES_NEW_EVIDENCE / REQUIRES_HUMAN_AUTHORITY / REQUIRES_ROLLBACK / NON_RECOVERABLE_IN_SESSION
- blast radius: OPERATION / TASK / SESSION / PROJECT / TENANT / DEPLOYMENT / PHYSICAL_SYSTEM

## FreezeRecord
freeze_id; trigger; violated_invariant; observed_facts; unknowns; affected_scope; prohibited_next_actions; safe_read_only_actions; evidence_refs; recovery_preconditions; authority_required_to_unfreeze; audit_lineage.

## Freeze laws proposed
1. Freeze smallest safe scope.
2. Escalate blast radius only with evidence.
3. Read-only diagnosis can continue unless integrity/security risk forbids it.
4. Retry is a controlled state transition, never silent continuation.
5. Unfreeze requires proof that the triggering invariant is restored.
6. A model cannot waive higher authority.
7. Failure rendering must not leak secrets.

## State machine
ACTIVE→DETECTED→CLASSIFIED→CONTAINED/FROZEN→DIAGNOSING→RECOVERY_PROPOSED→RECOVERY_AUTHORIZED→RECOVERY_EXECUTING→REVERIFYING→RESTORED.
Side states: BLOCKED_EXTERNAL, ESCALATED, ABORTED, PERMANENTLY_DENIED.

Forbidden:
- DETECTED→ACTIVE without evidence
- FROZEN→RESTORED without re-verification
- POLICY_DENIED→EXECUTING by blind retry
- SECURITY_VIOLATION→cleanup that destroys forensic lineage

## Retry policy
Deterministic validation failure: 0 blind retries.
Transient network timeout: bounded backoff.
Auth denial: 0 retries without changed authority.
Rate limit: obey authoritative retry signal.
Malformed AI worker output: bounded regeneration under same contract, then freeze.
Evidence conflict: no retry until conflict-resolution plan exists.

## Chaos catalog
kill verifier mid-commit; reorder/duplicate tool responses; replay stale evidence; semantically wrong but schema-valid model output; late dependency success after timeout; conflicting authority; write succeeds but ack lost; clock jump; disk full; duplicate queue delivery; network partition; low-authority worker attempts PASS promotion.

Expected: explicit deterministic state, bounded effects, no hidden success.

## Metrics
freeze_rate_by_class; time_to_classify; time_to_verified_recovery; false_unfreeze_count(target 0); stale_evidence_rejections; retry_budget_exhaustion; repeated_failure_signature; blast_radius_escalations.

## Promotion gate
Canonical mapping + deterministic transition table + ownership + negative-path tests + security review + compatibility proof with existing freeze semantics.
