# Evidence Invalidation & Freshness Model

> PROPOSAL_AI — แนวคิดที่เสนอโดย AI ยังไม่ใช่ข้อกำหนดจริงของ NEXY.AI

## Principle
Evidence proves a claim only under the conditions in which the evidence was produced. A relevant change can expire evidence without deleting the evidence artifact.

## Evidence tuple
Model evidence as:
E = (claim, subject_identity, source_identity, environment_identity, dependency_set, procedure, result, timestamp, toolchain_identity)

Evidence is CURRENT only when all validity-critical identities still match or an authoritative compatibility rule proves equivalence.

## Invalidation triggers
Re-verification should be considered when any of these change:
- requirement or policy meaning;
- implementation subject;
- dependency lock or compiler/runtime;
- schema/protocol;
- test oracle;
- fixture/data corpus;
- security boundary;
- permissions/authority;
- build flags/environment;
- deployment artifact;
- external provider contract;
- clock/randomness/I/O assumptions for deterministic paths.

## Invalidation states
- VALID_CURRENT: exact relevant identity is still current.
- VALID_BY_COMPATIBILITY_PROOF: identities differ but compatibility is explicitly proven.
- STALE: evidence predates a relevant change.
- PARTIALLY_STALE: only some claims remain supported.
- UNKNOWN: dependency relation cannot be established.
- CONFLICT: evidence sources disagree.
- REVOKED: known invalid evidence, retained only for history.

## Proof inheritance
PROPOSAL_AI: Evidence inheritance across commits/builds should be opt-in, not assumed. To inherit proof:
1. identify the exact claim;
2. prove the claim's dependency closure is unchanged;
3. prove test oracle/procedure unchanged or equivalently stronger;
4. prove environment differences irrelevant;
5. record the compatibility argument.

Failure of any step means rerun or NOT_VERIFIED.

## Negative evidence
Absence of a failure is not positive proof. Logs with no error, unchanged screenshots, or a green unrelated test cannot establish a claim outside their evidence class.

## Evidence debt
Track evidence debt as the set of impacted claims lacking current proof. A release decision should consume evidence debt explicitly, never hide it inside a generic PASS.

Suggested record:
- claim_id
- invalidated_by_change
- previous_evidence
- required_new_evidence_class
- current_status
- owner
- blocking/nonblocking rationale

## Security note
A security proof can become stale through transitive dependency changes even if application code is unchanged. Conversely, dependency freshness alone does not prove security.
