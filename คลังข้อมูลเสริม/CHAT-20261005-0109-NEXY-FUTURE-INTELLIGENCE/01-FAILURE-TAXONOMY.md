# Failure Taxonomy for Autonomous AI Systems

Purpose: provide stable names for failures so future NEXY.AI audits, tests, telemetry and incident reviews can refer to the same concepts.

## F01 Authority inversion
A lower-authority source overrides a higher-authority requirement.
Detection: trace every decision to source + authority rank.
Required response: stop mutation, surface conflict, restore authoritative requirement.

## F02 Silent scope expansion
Agent adds major work not required for objective completion.
Detection: deliverable has no mapping to requirement ledger.
Response: quarantine unrequested work.

## F03 Silent scope reduction
Hard requirement is omitted, softened or reinterpreted.
Detection: bidirectional requirement-to-evidence coverage.
Response: mark incomplete; restore missing requirement.

## F04 Assumption laundering
An assumption is later presented as fact.
Detection: provenance tag disappears across transformations.
Response: propagate FACT/ASSUMPTION/UNKNOWN state end-to-end.

## F05 Evidence-class mismatch
Evidence exists but cannot prove the claim. Example: source inspection used to claim runtime behavior.
Detection: claim type vs evidence type validator.
Response: acquire runtime/test evidence or mark NOT_VERIFIED.

## F06 Completion hallucination
Agent declares success before acceptance criteria are demonstrated.
Detection: completion requires explicit evidence bundle.
Response: downgrade status.

## F07 Stale-context execution
Agent acts on superseded project state.
Detection: freshness metadata, commit/ref identity, timestamp or version checks.
Response: refresh authoritative state before mutation.

## F08 Cross-task contamination
Knowledge or artifacts from one task are mistaken for another task's authority.
Detection: namespace/task IDs and provenance.
Response: isolate contexts.

## F09 Partial-success masking
A successful substep hides a failed overall objective.
Detection: objective-level gate independent of tool-call success.
Response: continue loop or report incomplete.

## F10 Tool-success overtrust
Tool returns success but resulting state is wrong or absent.
Detection: read-after-write or independent verification.
Response: verify postcondition, not API acknowledgement.

## F11 Irreversible mutation without gate
High-impact action occurs without required approval or rollback strategy.
Detection: mutation risk classifier.
Response: freeze before action.

## F12 Retry amplification
Repeated retries worsen state, cost, rate limits, or duplication.
Detection: bounded retries + failure fingerprint.
Response: change strategy after repeated identical failure.

## F13 Non-idempotent replay
Resuming a task repeats writes that should occur once.
Detection: operation keys / durable checkpoints.
Response: reconcile before replay.

## F14 Hidden dependency failure
Task appears local but depends on unavailable service/data/credential.
Detection: dependency inventory before execution.
Response: BLOCKED with exact missing dependency.

## F15 Validation theater
Checks exist but do not exercise the claimed behavior.
Detection: mutation testing, negative tests, counterexamples.
Response: strengthen oracle.

## F16 Ambiguous success oracle
No deterministic definition of correct result.
Detection: acceptance criterion cannot produce PASS/FAIL.
Response: define oracle before execution.

## F17 Context overflow loss
Critical constraint disappears as context grows.
Detection: compact immutable contract reloaded at checkpoints.
Response: externalize durable state.

## F18 Conflicting truths
Repo, docs, runtime, user specification disagree.
Detection: truth-source matrix.
Response: do not silently merge; label CONFLICT.

## F19 Unsafe fallback
Missing data causes fabricated placeholder/default behavior.
Detection: explicit missing-data tests.
Response: fail closed where truth matters.

## F20 Regression by local optimization
A fix improves one metric while violating another requirement.
Detection: regression suite tied to requirement ledger.
Response: rollback or redesign.

### Severity
S0 informational; S1 local recoverable; S2 objective-threatening; S3 data/compatibility risk; S4 irreversible/security-critical.

### Minimum incident record
failure_id, task_id, timestamp, trigger, observed_state, expected_state, authority_sources, evidence, blast_radius, reversibility, correction, verification, residual_risk.
