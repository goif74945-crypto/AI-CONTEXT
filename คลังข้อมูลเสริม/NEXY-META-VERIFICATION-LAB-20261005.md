# NEXY Meta Verification Lab

Status: ACTIVE / ADVISORY
Run ID: NEXY-MVL-20261005-0112-ICT
Chat ID: UNKNOWN — canonical ChatGPT conversation ID is not exposed to this runtime, so none is invented.
Created: 2026-10-05T01:12+07:00
Mutation boundary: AI-CONTEXT only. NEXY.AI repositories remain READ-ONLY.

## Objective
Create a divergent future-knowledge pack for NEXY focused on epistemic integrity, evidence freshness, adversarial verification, traceability, and long-horizon research.

## Authority facts observed
AI-CONTEXT requires progressive context loading, explicit truth classes, evidence matching, durable checkpoints, and no fake execution. Current NEXY source normalization uses 837 requirement rows; the historical 215 registry is deprecated/unreliable for current counts. Design, implementation, runtime behavior, and deployment evidence are separate truth domains.

# 1. Truth Lattice
Binary truth is insufficient. Represent material claim C as:
<subject,predicate,object,authority,revision,environment,time,evidence_class,evidence_ref,status,dependencies>.

Keep orthogonal axes: normative truth (should), structural truth (exists), behavioral truth (executed test), operational truth (runtime), deployment truth (artifact/environment), temporal truth (freshness), provenance truth (lineage). Never collapse these into a confidence percentage.

UNKNOWN means not established. NOT_VERIFIED means a candidate exists but required proof is missing. FAIL requires matching proof that actually failed.

Validation: synthetic claims mixing spec/source/test/runtime/deploy states must produce zero E0/E1-to-E4/E5/E6 substitutions and zero UNKNOWN-to-FAIL conversions without proof. Authority conflict must freeze dependent claims.

# 2. Evidence Decay
Evidence is bound to a proof context. Record claim, target revision, dependency fingerprint, environment fingerprint, evidence class, procedure/revision, result, timestamp, artifact hash, and limitations.

Hard invalidators include relevant source/config change, materially changed proof procedure, environment change for environment-sensitive claims, artifact mismatch, or broken provenance. External provider/policy drift requires review. Do not use a universal TTL; freshness is claim-specific.

Core rule: evidence remains current only while the relevant proof closure remains equivalent. If relevance cannot be established after a change, narrow status to NOT_VERIFIED rather than silently preserving PASS.

# 3. Counterfactual Verification
Happy-path proof can accidentally verify tests instead of requirements. For every critical invariant:
1 state invariant precisely;
2 identify enforcement mechanism;
3 construct minimal violating test world;
4 predict failure/freeze signal;
5 execute only in authorized disposable fixtures;
6 verify violation cannot PASS;
7 restore and rerun positive case.

Metamorphic laws:
- removing required evidence cannot preserve PASS;
- lowering evidence class cannot strengthen a claim;
- changing target revision without revalidation cannot preserve CURRENT_PASS;
- adding unresolved authority conflict cannot increase executability;
- corrupt provenance cannot remain sealed.

# 4. Uncertainty Budget
Track categorical uncertainty dimensions:
U_authority, U_input, U_state, U_evidence, U_dependency, U_time, U_scope.
Each = CLEAR / DEGRADED / BLOCKING.

Execution is allowed only if every uncertainty dimension capable of affecting correctness, authority, safety, or irreversibility is non-BLOCKING. DEGRADED is acceptable only when it cannot change required correctness and the output claim is narrowed accordingly.

Avoid fake “82% confidence.” It hides what is unknown and whether that uncertainty matters.

# 5. Agent Epistemic Attack Catalog
Defensive threat families:
authority laundering; evidence laundering; completion laundering; recency laundering; provenance stripping; scope smuggling; denominator manipulation; correlated-consensus laundering; tool-result shadowing; memory poisoning; failure suppression; ambiguity collapse.

Defenses: typed truth classes, authority labels, immutable evidence references, claim-to-proof mapping, revision binding, independent denominator source, scope ledger, negative-path verification, write-back filters, conflict-preserving summaries.

Multi-agent invariant: N agents sharing the same source are one correlated evidence lineage, not N independent confirmations. Eloquence never outranks direct tool evidence.

# 6. Requirement Coverage Graph
Observed current source denominator: 837 normalized requirement rows.

Node types: LAW, REQ, IMPL, TEST, EVID, ENV, RISK, DEC.
Edges:
LAW governs REQ;
REQ realized_by IMPL;
REQ verified_by TEST;
TEST produced EVID;
EVID bound_to revision/environment;
RISK challenged_by TEST;
DEC constrains REQ/IMPL.

Coverage states: UNMAPPED, MAPPED, STATIC_PROVEN, BEHAVIOR_PROVEN, DEPLOY_PROVEN, PHYSICAL_PROVEN, STALE, CONFLICT.

Denominator law: never publish a coverage percentage unless numerator and denominator share ontology and scope. “tests passed / 837” is invalid unless tests map to normalized rows with defined many-to-many semantics.

High-value gap queries: requirements without tests; tests without requirements; PASS evidence on stale revisions; deployment evidence lacking implementation lineage; high-risk requirements lacking negative paths; requirements governed by conflicting laws.

# 7. Long-Horizon Research Queue
This backlog intentionally exceeds a short session. It is continuation state, not a false claim of background execution.

A Epistemic integrity: truth-lattice corpus; stale-evidence benchmark; authority-conflict benchmark; UNKNOWN-vs-FAIL evaluation; claim/evidence mismatch detector.

B Verification science: proof-gate mutation testing; counterfactual generator; dependency-closure algorithm; environment fingerprints; reproducibility scorecard; flaky-proof quarantine.

C Multi-agent governance: correlated-consensus detection; adversarial judge benchmark; worker/judge separation; tool-result precedence; delegation provenance; partial-completion detection.

D Context engineering: retrieval contamination; stale-context eviction; authority-aware ranking; provenance-preserving compression; contradiction-preserving summaries; durable write-back validator.

E Traceability: semantic clustering of 837 rows; coverage edge schema; orphan requirement/test queries; scope-safe metrics; registry comparison without conflating ontologies.

F Failure economics: false-PASS vs false-FREEZE cost; risk-tiered evidence; reversible/irreversible action policy; evidence acquisition cost.

G Temporal truth: proof freshness; external drift; policy validity windows; historical replay; revision-aware cache invalidation.

H Human control: freeze explanations without hidden reasoning; evidence receipts; conflict presentation; uncertainty visualization; irreversible-action confirmation semantics.

DONE rule per research item: objective + authority + method + falsification + artifact + verification + limitations + durable index. Prioritize catastrophic false-PASS reduction before convenience.

# 8. Resumable Checkpoint
Current state: PARTIAL.
Completed: authority inspection; existing supplemental-folder inspection; this divergent knowledge pack design.
Known incident: initial multi-file GitHub contents write hit 409 because repository head changed concurrently. Recovery switched to a single additive artifact to reduce race risk. No NEXY.AI mutation was authorized or attempted.
Next continuation: build synthetic benchmark cases, machine-readable claim/evidence schemas, proof-invalidation fixtures, and authority-conflict corpus; verify each addition before promoting status.
Stop conditions: FREEZE on authority conflict, ambiguous mutation target, or any action that would mutate a NEXY.AI repository without explicit authorization.

## Acceptance criteria
This document is secondary/advisory only; it does not override NEXY law/spec/source. Proposals are not implementation facts. Any future COMPLETE claim requires re-fetching this artifact and verifying all promised deliverables.
