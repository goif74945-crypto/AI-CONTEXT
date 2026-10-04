# Future Assurance Synthesis
Status: AI-PROPOSED CONCEPT
Work ID: NEXY-FAL-20261005-0113-ICT

## Agent admission and quarantine
Do not treat model identity as capability proof. Maintain a time-bounded Agent Passport containing provider/model identity, capability classes, allowed tool scopes, prohibited actions, schema conformance, reliability window, failure signatures, evidence freshness and quarantine state.

Lifecycle: UNSEEN -> BENCHMARKING -> LIMITED -> ADMITTED -> DEGRADED -> QUARANTINED -> RETIRED.

Quarantine triggers include fabricated tool execution, repeated schema violation, authority violation, correctness-affecting silent truncation, anomalous disagreement and provider behavior changes that invalidate evidence. Re-admission requires root-cause classification, targeted regression, clean benchmark evidence, limited scope and observation.

## Provenance graph protocol
Nodes: SOURCE, CLAIM, REQUIREMENT, DECISION, ARTIFACT, TEST, EVIDENCE, INCIDENT, PROPOSAL, SUPERSESSION.
Edges: DERIVED_FROM, VERIFIED_BY, CONTRADICTS, SUPERSEDES, IMPLEMENTS, TESTS, BLOCKS, DEPENDS_ON, EXPIRES_WITH.
Minimum metadata: stable id, truth class, authority rank, source locator, observation time, version/hash when available, freshness policy, dependencies, conflict state and redaction class.

Freshness is claim-specific. Conflicting nodes remain visible even when authority selects an operational winner. Never store secrets or hidden chain-of-thought as provenance.

## Determinism and replay
Determinism should be defined over relevant state rather than raw text alone.

Proposed Decision Capsule:
- normalized request
- authority snapshot ids
- policy/version ids
- relevant state hashes
- tool contracts
- agent passport ids
- external observation timestamps
- side-effect ledger
- final adjudication record

Replay modes: exact, semantic, counterfactual and incident replay. Equivalent relevant state should preserve authority winner, scope boundary, freeze decision, required evidence class and side-effect permission. If dependencies cannot be reconstructed, exact replay is NOT_VERIFIED.

## Recovery and continuity
Verified checkpoints, not conversational memory, are the recovery boundary.

Checkpoint contract:
task id, objective, authoritative inputs, protected scope, completed claims/evidence, in-flight side effects, unresolved conflicts, next safe action, invalidation triggers and source/version hashes.

Side-effect ledger:
INTENT -> PRECONDITION -> ACTION_ID -> OBSERVED_RESULT -> POSTCONDITION -> COMPENSATION.

An unknown postcondition after interruption freezes replay until idempotency or actual state is established.

## Compatibility futures
Compatibility dimensions include schema, API, policy, provider/model, tool semantics, storage, event ordering, user-visible behavior, evidence format and audit lineage.

Change classes:
C0 additive/no semantic change
C1 backward-compatible extension
C2 migration required
C3 dual-run required
C4 breaking/authority-sensitive
C5 irreversible/high-risk

Shadow Contract before adopting a provider/model/tool/schema:
replay representative corpus; compare structural decisions; measure disagreement; classify changed failure semantics; test rollback; preserve old evidence interpretation; define cutover/abort thresholds.

## Experiment promotion gates
Lifecycle:
IDEA -> HYPOTHESIS -> EXPERIMENT_SPEC -> SANDBOX_EVIDENCE -> CANDIDATE -> SHADOW -> LIMITED -> ELIGIBLE_FOR_SPEC_REVIEW.

This lab cannot promote itself into canonical NEXY specification.

G0 clarity: falsifiable hypothesis, owner, scope, forbidden outcomes.
G1 safety: trust boundary, abuse cases, blast radius, rollback.
G2 oracle: verifiable expected result.
G3 evidence: evidence class matches claim.
G4 regression: existing invariants preserved.
G5 compatibility: migration and rollback classified.
G6 operations: observability, incident signature, recovery.
G7 authority: authorized human/spec process explicitly accepts promotion.

## Assurance scorecard
A score never replaces hard gates.

Hard gates: authority integrity, protected-scope integrity, critical security, required evidence, destructive-action authorization and recovery viability.

Diagnostic dimensions 0-4:
contract completeness; evidence freshness; negative-path coverage; replayability; recovery confidence; provenance completeness; provider independence; observability; compatibility readiness; human control clarity.

0 unknown; 1 documented only; 2 static/sandbox evidence; 3 integrated evidence; 4 target-runtime evidence appropriate to the claim.

A high average cannot compensate for a failed hard gate.

## AI-proposed future systems
All items below are UNVALIDATED concepts.

1. Evidence Compiler: compile requirements and claims into machine-checkable evidence plans.
2. Counterfactual Judge: vary policy/state deliberately to expose brittle decisions.
3. Authority Diff: semantic diff for changes to precedence, permissions, freeze behavior and destructive authority.
4. Failure Genome: compose incident fault genes to regenerate failure families.
5. Agent Immune System: detect passport deviation and quarantine capability classes.
6. Provenance Garbage Collector: remove redundant derived artifacts only while preserving lineage and retention obligations.
7. Decision Time Machine: replay historical decision capsules against historical and current policy.
8. Unknown Budget: make critical UNKNOWN/NOT_VERIFIED accumulation visible without pretending it is safe.
9. Side-Effect Escrow: stage high-impact action intent before execution for policy, deduplication and postcondition checks.
10. Spec Promotion Firewall: generated design cannot enter canonical spec without provenance, tests, conflict scan, compatibility classification and authorized promotion.
11. Capability Prediction Market: non-financial scoring of agent routing predictions against real evidence.
12. Semantic Blast-Radius Mapper: map which requirements, tests, policies, evidence and recovery procedures become stale after a contract change.

## Research experiments
E1: Measure whether structural replay detects policy drift earlier than end-to-end regression alone.
E2: Compare provider routing by marketing identity versus capability passport.
E3: Inject false tool-success responses and measure postcondition detection.
E4: Simulate interrupted side effects and test duplicate-action prevention.
E5: Introduce contradictory provenance and verify authority resolution without lineage deletion.
E6: Run shadow migration across schema versions and measure evidence invalidation.
E7: Evaluate whether Failure Genome mutations discover regressions missed by exact incident replay.
E8: Measure calibration between agent self-confidence and evidence-backed success.
E9: Test whether Unknown Budget correlates with incident discovery rate.
E10: Validate blast-radius mapping against manually traced dependency impact.

## Stop conditions
Freeze promotion when authority conflicts, side effects are unbounded, a critical claim has no valid oracle, required evidence is unavailable, rollback is missing for high-impact changes, or provenance is insufficient to reproduce the decision.

## Boundary
Nothing in this file proves current NEXY implementation behavior. It is future assurance research only.
