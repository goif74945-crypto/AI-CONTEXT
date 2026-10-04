# Failure & Freeze Intelligence
Status: ADVISORY DESIGN grounded in observed repository patterns

## Failure ontology by blocked authority
AUTHORITY_FAILURE: conflicting laws, unknown owner, unauthorized mutation.
EVIDENCE_FAILURE: missing/stale/wrong-class/non-reproducible proof.
STATE_FAILURE: illegal transition, corrupt state, version mismatch.
IDENTITY_FAILURE: target/repo/environment/actor ambiguity.
SECURITY_FAILURE: replay, credential misuse, injection, abuse.
DETERMINISM_FAILURE: multiple legal outcomes, unstable ordering, hidden nondeterminism.
CAPABILITY_FAILURE: provider/tool/resource unavailable.
INTEGRITY_FAILURE: hash/signature/audit-chain mismatch.
EXTERNAL_REALITY_FAILURE: provider/runtime/deployment drift.
PHYSICAL_SAFETY_FAILURE: sensor/actuator/safety-controller uncertainty.

## Freeze vector
A freeze record should be able to state:
domain; violated_invariant; blocking_layer; primary_error_code; recoverability; required_recovery_authority; required_new_evidence; invalidated_evidence; safe_read_actions; forbidden_mutations; retry_policy; escalation_path.

## Recovery is proof, not retry
Exit freeze only after root cause is identified/bounded, invariant restored, stale evidence invalidated, required proof regenerated, authority validated, and regression surface checked.

## Freeze-storm control
Potential future mechanism: incident equivalence key = hash(project + target_revision + invariant + blocking_layer + normalized_root_cause).
Coalesce derivative incidents while preserving affected-task links.

## Pre-mortem execution
Before high-impact mutation, predeclare likely freeze classes, stop signals, required evidence and rollback/recovery. Failure handling then becomes controlled rather than improvised.

Promotion: none. Existing authorized NEXY incident semantics remain authoritative.
