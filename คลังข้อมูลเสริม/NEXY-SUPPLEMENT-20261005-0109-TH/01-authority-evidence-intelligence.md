# Authority & Evidence Intelligence
Status: ADVISORY DESIGN

## New failure class: authority substitution
An agent can cite a true sentence that is wrong for the decision because it is stale, advisory, scoped elsewhere, or backed by the wrong evidence class.

## Claim Provenance Graph
Store material claims as:
claim_id; proposition; truth_class; authority_class; source_locator; source_revision; effective_scope; effective_time; supersession; dependencies; required_evidence_class; observed_evidence; verification_status; freshness_policy; promotion_state.

Relations:
REQUIRES / IMPLEMENTS / PROVES / CONTRADICTS / SUPERSEDES / DERIVES_FROM / NARROWS / EXCLUDES / DEPENDS_ON.

## Authority-aware retrieval
A query must carry target revision/environment and truth domain: design, implementation, runtime, deployment, physical.
Return supporting claims AND strongest disqualifiers:
- superseding spec
- explicit exclusion/deferment
- failing evidence
- stale revision
- wrong environment
- advisory-only source
- evidence-class mismatch

This "negative retrieval" is a defense against confirmation bias.

## Evidence lattice
Evidence is typed, not a single confidence number:
SOURCE_SPEC; STATIC_CODE; TYPECHECK; UNIT_RUNTIME; CONTRACT_RUNTIME; INTEGRATION_RUNTIME; E2E_BROWSER; SECURITY_DYNAMIC; LOAD_PERFORMANCE; DEPLOYMENT_ENVIRONMENT; EXTERNAL_PROVIDER; PHYSICAL_HIL.
No class automatically substitutes for another.

## Proof-carrying completion
Serialize each important completion claim with authority, target revision, required evidence, observed evidence, gaps, status and replay instructions.

## Dependency-directed invalidation
Invalidate evidence when its source/dependency/authority/environment changes. Do not blindly keep PASS across revisions.

## Critical contradiction budget
Critical mutation: unresolved authority contradictions = zero allowed.
Exploratory research may retain contradictions only when isolated from mutation authority.

## Falsification tests
1. stale README conflicts with DOC-C -> reject README authority.
2. old-commit PASS -> current claim becomes NOT_VERIFIED.
3. deployment evidence alone -> must not imply implementation PASS.
4. equal-authority unresolved conflict -> mutation blocks as CONFLICT.
