# NEXY Future Engineering Knowledge Pack
Execution ID: NEXY-SUPPLEMENT-20261005-0111-TH
Status: ADVISORY / DURABLE CONTEXT
Date: 2026-10-05

## Scope Lock
Mutation target: AI-CONTEXT only.
Every repository whose name contains NEXY.AI is protected from mutation in this execution.
This document is not authoritative NEXY.AI specification. It is reusable engineering knowledge subordinate to current user directives and canonical project specifications.

## 1. Contract & Invariant Graph
Represent critical engineering truth as graph nodes: REQUIREMENT, INVARIANT, INTERFACE, STATE, EVIDENCE, RISK, OWNER, VERSION.
Edges: REQUIRES, SATISFIES, PROVES, CONTRADICTS, SUPERSEDES, DEPENDS_ON, EMITS, CONSUMES, MUST_NOT_TOUCH, INVALIDATES, COMPATIBLE_WITH.

Laws:
1. Every critical requirement maps to one or more invariants.
2. Every VERIFIED invariant has current evidence.
3. Evidence bound to a stale revision cannot prove changed implementation.
4. SUPERSEDES preserves history.
5. CONTRADICTS invokes authority resolution.
6. MUST_NOT_TOUCH is a hard execution boundary.
7. Interface changes trigger consumer and compatibility traversal.

Minimal invariant record:
```yaml
id: INV-...
statement: ...
authority_ref: ...
scope: []
preconditions: []
counterexamples: []
evidence_class: static|unit|integration|e2e|runtime|physical
evidence_refs: []
invalidated_by: []
version_range: ...
status: UNKNOWN|PROPOSED|VERIFIED|VIOLATED|SUPERSEDED
```

High-value queries include: unproven requirements, stale evidence, interfaces without compatibility contracts, risks without failure-injection cases, and claims depending on advisory sources.

## 2. Truth & Provenance Ledger
Material claim tuple:
`<claim_id, claim, truth_class, source_identity, source_revision, observed_at, authority_rank, scope, freshness, verification_state>`

Truth classes follow AI-EXECUTION-KERNEL: SOURCE_FACT, REPO_FACT, RUNTIME_FACT, EXTERNAL_FACT, INFERENCE, ASSUMPTION, UNKNOWN, CONFLICT, NOT_VERIFIED.

Non-conversion laws:
- INFERENCE does not become fact by repetition.
- AI-generated committed text is not project authority by location alone.
- REPO_FACT proves repository state, not runtime behavior.
- test-code existence is not test-execution evidence.
- build success is not deployment-health evidence.
- old runtime evidence cannot prove a changed revision without proven equivalence.

Recommended evidence identity:
`hash(subject_revision + environment + procedure + result_digest)`.

Evidence records should preserve procedure, environment, timestamps, exit/result state, output digest, artifacts, verifier type, and blind spots.

Freshness is claim-specific. Runtime health and architectural law cannot share one global TTL.

Derived claims expose dependencies. When a dependency becomes stale or violated, the derived claim is downgraded.

## 3. Deterministic Verification Matrix
Evidence class must match claim class.

| Claim | Minimum evidence | Invalid substitute |
|---|---|---|
| syntax/schema valid | parser/compiler execution | visual inspection |
| function behavior | focused executed test | function exists |
| cross-service contract | integration execution | mocks only |
| UI workflow | browser/E2E evidence | screenshot only |
| deployment healthy | target environment probe | build success |
| migration safe | forward + rollback rehearsal | migration file |
| authorization enforced | positive + negative tests | middleware existence |
| idempotency | repeated execution + state comparison | docs |
| recovery works | injected failure + recovery proof | recovery code |
| protected scope untouched | diff/audit evidence | intention |

Regression lattice:
R0 static
R1 changed unit
R2 direct contracts
R3 dependency neighborhood
R4 workflow/E2E
R5 adversarial/security
R6 deployment/canary

Evidence invalidates when subject revision, environment contract, material fixture, dependency boundary, verifier procedure, or authoritative requirement changes.

## 4. Failure Injection & Recovery Corpus
Fault families:
- Data: malformed, missing, duplicate, out-of-order, stale, conflicting, oversized.
- Dependency: timeout, partial response, rate limit, expired auth, schema drift, semantic-invalid success.
- Storage: write conflict, partial write, lag, cache corruption, unavailable primary, rollback failure.
- Agent/tool: wrong tool, wrong target, repeated side effect, evidence-capture failure, context loss, retrieved instruction injection.
- Runtime: cold start, unhealthy instance, mixed-version fleet, config mismatch, missing secret, DNS/network failure.

Every case defines detection, containment, visible semantics, retry eligibility, idempotency, rollback/compensation, evidence, terminal state, data-integrity assertion, and resumption state.

A recovery case passes only when an allowed terminal state is reached AND forbidden side effects are proven absent.

Severity:
S0 informational
S1 degraded
S2 workflow failure
S3 integrity/security risk
S4 destructive/cross-boundary risk

S3/S4 injection requires isolated authorized environments.

## 5. Compatibility & Evolution Matrix
Change dimensions: API, events, persisted state, prompt/policy contract, tool contract, config, model/provider behavior, evidence schema, topology.

Compatibility classes:
C0 no observable change
C1 additive/backward compatible
C2 negotiated version/capability
C3 migration required
C4 breaking coordinated cutover

For each material change record producer version, consumer version, data version, compatibility class, fallback, rollback, migration proof, removal date.

Expand/contract:
1. tolerant consumer
2. verify consumer
3. new producer behavior
4. mixed-version observation
5. migrate data
6. remove old behavior only with bounded usage evidence
7. retain rollback until destructive boundary

Model upgrades count as dependency upgrades even if API schema is unchanged. Re-evaluate authority adherence, tool selection, forbidden action rate, structured output, recovery, latency/cost envelope, and retrieval sensitivity.

FREEZE breaking changes when consumer inventory, rollback, current evidence, recovery, or authority is undefined.

## 6. Autonomous Agent Handoff
Handoff packet fields:
execution_id, objective, authoritative_inputs, protected_scope, target_revision, completed, in_progress, blockers, decisions_with_evidence, changed_artifacts, verification_executed, verification_missing, known_failures, next_exact_action, stop_conditions.

Resume algorithm:
1. read packet
2. re-fetch target revision
3. detect drift
4. invalidate dependent evidence/decisions if drift matters
5. reconstruct minimum context
6. continue exact next action
7. never repeat mutation merely because hidden reasoning is unavailable

Checkpoint on authority resolution, architecture lock, mutation batch, test phase, failure, blocker transition, context pressure, or external state change.

Concurrent agents must re-fetch before write and avoid semantic last-writer-wins behavior.

## 7. Unknown & Research Registry
Preserve unknowns rather than filling them with plausible prose.

Priority should consider impact × uncertainty × reuse × irreversibility / verification cost.

High-value unknowns:
1. authoritative vs historical NEXY contracts
2. runtime claims tied to exact revisions
3. cross-component invariants lacking executable tests
4. undocumented schema consumers
5. untested recovery paths
6. environment-specific deployment assumptions
7. non-idempotent agent/tool actions
8. evidence freshness invalidation coverage
9. behavior changes from model/provider upgrades
10. historical COMPLETE/PASS claims lacking matching evidence class

Research record:
```yaml
research_id:
question:
why_it_matters:
authority_needed:
safe_sources: []
forbidden_assumptions: []
verification_method:
expected_artifact:
status: UNKNOWN|IN_PROGRESS|VERIFIED|BLOCKED
```

Research order: exact project evidence, current implementation/evidence, official sources, verified external sources, inference last.

## 8. Long-Run Execution State
CURRENT STATE: initial durable pack created for this execution.
COMPLETED: architecture of contract graph, truth ledger, verification matrix, failure corpus, compatibility model, handoff protocol, unknown registry.
IN PROGRESS: deeper read-only NEXY inventory and mapping are intentionally not claimed without repository evidence.
BLOCKED: none for this artifact; future NEXY mutations remain prohibited without explicit authorization.
NEXT ACTION: future agents may extend this pack with read-only evidence maps tied to exact revisions.
VERIFICATION STATUS: artifact requires fetch-back after commit before COMPLETE can be claimed.

## 9. Stop Conditions
FREEZE when target identity is uncertain, protected scope would be mutated, authority conflicts materially, evidence required for a critical claim is unavailable, irreversible action lacks approval, or repository state drift invalidates the plan.

## 10. Anti-Patterns
- treating token count or elapsed hours as quality
- generating duplicate documents to simulate progress
- equating file count with coverage
- claiming tests from test-file existence
- treating screenshots as behavioral proof
- stale PASS after revision change
- hiding partial failures inside aggregate success
- making AI-CONTEXT advisory prose override project authority

## 11. Future Extension Packs
- read-only contract inventory with exact revision provenance
- invariant-to-test coverage graph
- evidence freshness checker specification
- incident-to-eval conversion pipeline
- compatibility risk scorer
- deterministic side-effect audit format
- context poisoning adversarial corpus
- mixed-version deployment verification playbook

The design goal is not maximal text. It is durable leverage: future agents should be able to prove more, guess less, and resume work without reconstructing history.
