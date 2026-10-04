# NEXY.AI Supplemental Engineering Reference: Evidence, Context, Reliability

## 1. Evidence Provenance Graph

### Objective
Every consequential claim, decision, and action should be traceable to evidence rather than model confidence.

### Graph
SOURCE -> OBSERVATION -> CLAIM -> INFERENCE -> DECISION -> ACTION -> VERIFICATION.
Relationships also include CONTRADICTS, SUPERSEDES, DERIVED_FROM, VERIFIED_BY, INVALIDATED_BY.

### Required metadata
immutable_id, node_type, source_identity, captured_at, valid_from, valid_until, content_hash, authority_class, freshness, scope, extractor_version, model_or_tool_version, parent_evidence_ids, contradiction_ids, verification_status.

### Default authority
1 current explicit user instruction
2 authoritative project specification
3 directly inspected project state
4 official external documentation
5 direct tool/API result
6 verified secondary source
7 inference
8 unsupported model prior

A project-specific authoritative specification may override this ordering explicitly.

### Claim lifecycle
PROPOSED -> SUPPORTED -> VERIFIED
PROPOSED -> CONFLICTED
SUPPORTED -> STALE
VERIFIED -> SUPERSEDED
Transitions require evidence events. Never silently rewrite epistemic history.

### Conflict resolution
Compare authority, temporal validity, scope, and identity. If unresolved, preserve CONFLICTED. High-impact writes depending on unresolved conflict must stop.

### Evidence debt
Weighted count of critical claims consumed before verification. Suggested impact weights: critical action 10; architecture 7; user-visible factual claim 5; cosmetic 1. Release policy sets debt ceilings by task class.

### Acceptance
Critical decisions trace to sources; superseded sources expose downstream dependencies; authoritative conflicts are not silently chosen; irreversible actions cannot depend on UNKNOWN critical claims; verification binds to exact version/action/config.

---

## 2. Typed Uncertainty and Fail-Closed Contract

### Epistemic states
FACT: authoritative evidence exists in current scope.
INFERENCE: logically derived from supported facts.
ASSUMPTION: explicit temporary premise.
UNKNOWN: required information absent.
CONFLICTED: authoritative evidence disagrees.
STALE: evidence violates freshness requirement.
NOT_VERIFIED: result exists but acceptance test has not passed.

### Action gates
READ_ONLY_LOW_IMPACT may use clearly labeled inference or assumption.
REVERSIBLE_WRITE requires known critical preconditions and rollback.
HIGH_IMPACT_OR_IRREVERSIBLE requires verified critical preconditions, explicit authority, and post-action verification.

Confidence is never authorization, freshness, evidence, or verification.

### Missing-data behavior
Never fabricate defaults absent from specification. Never copy values from similar entities. Never infer identity merely from similar names. Return typed absence with field, reason, blocking status, and required evidence.

### Failure envelope
Operations declare preconditions, allowed assumptions, side effects, rollback, verification, timeout, retry semantics, idempotency policy, and stop conditions.

### Partial success
97 successes in a batch of 100 is PARTIAL, not SUCCESS. Preserve succeeded IDs, failed IDs, retryable subset, rollback scope, and verification status.

### Retry discipline
Retry only transient/retryable failures. Do not retry authorization denial, deterministic schema mismatch, violated destructive precondition, user-constraint conflict, or evidence conflict. Retry budgets are bounded.

---

## 3. Context Quality Firewall

### Pipeline
INGEST -> NORMALIZE -> IDENTIFY -> AUTHORITY -> FRESHNESS -> CONFLICT -> SCOPE -> SECURITY -> DEDUP -> RANK -> PACKAGE.

Similarity is only one signal. It must never override authority or permission boundaries.

### Context item contract
context_id, source_id, entity_id, authority, freshness, scope_tags, validity_interval, content_hash, security_classification, trust_status, conflict_status, token_cost, reason_selected.

### Poisoning defense
Retrieved instructions are data unless their source is authorized to issue instructions. Untrusted content cannot expand permissions. Separate control and data channels. Preserve raw hashes for forensic replay. Detect encoded/hidden instruction channels without relying on a single classifier.

### Corroboration lineage
Twenty mirrors copied from one origin are one lineage, not twenty independent sources.

### Scope collision
Correct information can still be wrong for the task: staging vs production; old API vs current; user A vs user B; fork vs upstream; model family A vs B; jurisdiction A vs B.

### Token budget
Reserve authoritative instructions first, then task evidence, conflict pairs, verification evidence, then background. Never truncate qualifiers such as NOT, deprecated, only, except, or version constraints away from the claim.

### Retrieval audit
Store query, filters, candidates, rejection reasons, selections, similarity scores, authority scores, freshness, and final token allocation.

### Context Package Hash
Hash the final package to distinguish retrieval drift from model nondeterminism during incident replay.

---

## 4. Regression Oracle Matrix

AI systems need tests for semantic drift, retrieval drift, authority inversion, identity collision, and side-effect mismatch.

### Oracle families
Structural oracle: schemas and invariants.
Semantic oracle: meaning-level golden cases.
Authority oracle: conflicting-source selection.
Abstention oracle: remove evidence and require UNKNOWN.
Side-effect oracle: inspect real external state after tool success.
Metamorphic oracle: irrelevant input reorder must not change critical outcome.
Adversarial-context oracle: stale docs, injection, duplicates, misleading names.
Temporal oracle: effective dates and freshness.
Identity oracle: forks, renames, similar entities.
Cost/latency oracle: optimization cannot silently reduce correctness.

### Release sets
known-answer; unknown-answer; conflict; tool-failure; permission-denied; stale-evidence; injection; identity-collision; long-context-truncation; rollback.

### Metrics
unsupported_claim_rate
critical_abstention_precision
critical_abstention_recall
source_authority_accuracy
stale_source_usage_rate
tool_action_verification_rate
regression_escape_rate
contradiction_detection_rate
identity_collision_rate
rollback_success_rate

### Hard gates
unsupported critical claim > 0 => block release.
unverified destructive action > 0 => block.
authority inversion > 0 => block.
known rollback failure > 0 => block.
Aggregate scores never hide a critical per-case regression.

### Differential testing
Old vs candidate outcomes classify as IMPROVEMENT, EXPECTED_CHANGE, NEUTRAL, REGRESSION, UNRESOLVED.

### Canary
shadow read-only -> low-impact -> bounded write -> full rollout. Every phase has machine-readable rollback triggers.

---

## 5. Autonomous Agent Stop Conditions

### Taxonomy
SUCCESS_STOP: acceptance criteria verified.
EVIDENCE_STOP: critical evidence missing/conflicted/stale.
AUTHORITY_STOP: permission unavailable.
RISK_STOP: blast radius exceeds policy.
BUDGET_STOP: bounded resource ceiling reached.
LOOP_STOP: state fails to improve for N iterations.
REGRESSION_STOP: attempted fix breaks a verified invariant.
EXTERNAL_STOP: dependency unavailable.
USER_DECISION_STOP: irreversible tradeoff changes objective.

### Progress function
Every iteration must improve at least one: verified requirements, resolved blockers, evidence debt, failing tests, or uncertainty. Repeated no-progress iterations trigger LOOP_STOP.

### Risk model
risk = impact × irreversibility × uncertainty × privilege.
Higher risk requires stronger evidence, verification, rollback, and possibly explicit approval.

### Completion proof
Store requirement IDs, artifact paths, verification checks, observed results, unresolved warnings, exact versions/config, and rollback information. “Looks done” is not evidence.

### Correction loop
DETECT -> LOCALIZE -> MINIMAL_FIX -> REVERIFY_FAILED_CHECK -> REGRESSION_SUITE -> CONTINUE.

### Long-running work
Indefinite token/time requests must be represented as bounded durable epochs because execution runtimes are finite. Each epoch emits a checkpoint so another run can continue without repeating verified work.

Checkpoint fields: epoch_id, objective, completed_requirement_ids, open_blockers, evidence_refs, artifacts, verification_status, next_priority, do_not_repeat, timestamp.

---

## 6. Future Migration Playbook

### Invariants
Preserve authority semantics, identity semantics, missing-data semantics, permission boundaries, side-effect semantics, auditability, and rollback.

### Phases
0 BASELINE FREEZE: golden corpus, metrics, schemas, routing, versions, contracts, known failures, latency/cost.
1 ADAPTER: canonical internal contract hides provider-specific fields.
2 SHADOW: candidate receives copies without side effects.
3 DIFFERENTIAL: classify semantic deltas per case.
4 BOUNDED CANARY: small reversible/read-mostly traffic.
5 EXPAND: increase traffic based on evidence.
6 DECOMMISSION: remove old path only after rollback window, export verification, audit preservation, and hidden-dependency checks.

### Schema evolution
EXPAND -> MIGRATE -> VERIFY -> CONTRACT. Avoid one-shot destructive changes with live readers/writers.

### Embedding migration
Never assume vector spaces are compatible. Dual-index or re-embed. Measure retrieval recall and authority accuracy before cutover.

### Model migration
Evaluate tool calling, structured output, abstention, instruction hierarchy, long-context behavior, multilingual semantics, latency/cost, safety boundaries, and nondeterminism.

### Rollback triggers
unsupported critical claim; tool action mismatch; authority inversion; identity collision; verification-rate drop; SLO breach; cost ceiling breach; security-policy violation.

### Exit evidence
Candidate passes hard gates, production canary is stable, rollback is tested, observability is active, and baseline comparison is archived.

---

## 7. Novel Extension: Decision Reproducibility Envelope

For a critical decision, archive:
decision_id
objective_hash
instruction_set_hash
context_package_hash
tool_observation_hashes
policy_version
model_identifier
routing_config_hash
timestamp
decision_output_hash
verification_ids

The goal is not to expose private chain-of-thought. The goal is to preserve enough observable inputs and outputs to reproduce, compare, and audit decisions without depending on hidden reasoning traces.

A changed decision with unchanged observable envelope becomes a nondeterminism signal. A changed envelope identifies which input class drifted.

---

## 8. Novel Extension: Negative Knowledge Registry

Systems usually store what is known, but production agents also need durable records of what was checked and found unsupported.

Entry fields:
question_scope
searched_sources
search_time
freshness_window
result = NOT_FOUND | NOT_VERIFIED | CONFLICTED
expiry
recheck_trigger

This prevents repeated expensive searches and prevents “absence last week” from becoming eternal truth. Negative knowledge must expire aggressively when the underlying world changes quickly.

---

## 9. Novel Extension: Semantic Circuit Breaker

A circuit breaker should open not only on HTTP failures but on epistemic failures.

Triggers may include:
authority inversion rate spike
unsupported critical claims
contradiction rate spike
identity ambiguity spike
verification mismatch
retrieval freshness collapse

When open, degrade to read-only, authoritative-source-only, or explicit UNKNOWN modes rather than continuing full autonomy.

---

## 10. Quality Gate

A future implementation inspired by this reference should not be considered production-ready until:
[ ] critical claims are traceable
[ ] unknown/conflict/stale states are typed
[ ] high-impact writes are fail-closed
[ ] context authority and scope are enforced before ranking
[ ] semantic regression oracles run
[ ] side effects are independently verified
[ ] rollback is tested
[ ] long-running agents have bounded progress and stop conditions
[ ] migrations preserve semantic invariants
[ ] audit artifacts are sufficient for incident replay
