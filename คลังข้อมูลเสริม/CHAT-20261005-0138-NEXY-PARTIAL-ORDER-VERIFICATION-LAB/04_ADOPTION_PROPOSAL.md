# AI-Proposed NEXY Adoption Boundary

**Classification: AI_PROPOSED. This is not a current NEXY requirement, implementation claim, or deployment claim.**

## Proposed value

Use NPOVL as an offline or pre-execution **verification-plan compiler** when a NEXY workflow already has an explicit DAG and trustworthy action-effect metadata. The benefit is not “run fewer tests at any cost.” The benefit is “avoid rerunning schedules that are provably the same under an explicitly constrained equivalence model.”

Potential product value:

- lower latency for concurrent verification plans;
- less duplicate tool/worker execution;
- smaller evidence bundles with explicit class provenance;
- deterministic reproduction of why one schedule represented another;
- conservative fallback when effects are opaque;
- measurable reduction ratio without moving authority out of CORE/JUDGE.

## Proposed adapter contract

Input adapter responsibilities:

1. resolve an authoritative finite work DAG;
2. normalize every external/state resource into stable collision-safe resource IDs;
3. declare all causal dependencies;
4. set `effects_complete=false` for any action whose side effects are not statically bounded;
5. set `opaque=true` for dynamic tools whose interference cannot be modeled safely;
6. identify whether the downstream assertion is trace-invariant under the proposed independence relation;
7. select evidence-appropriate search budgets.

NPOVL responsibilities:

1. validate/freeze on invalid model structure;
2. construct only conservative static independence;
3. produce deterministic representatives and class IDs;
4. expose omitted metrics and search-limit failures explicitly;
5. never emit a release/approval decision.

Downstream verifier responsibilities:

1. execute every representative actually required by the plan;
2. bind resulting evidence to source/model identity;
3. reject stale evidence if the DAG/effects/property contract changes;
4. preserve NEXY's existing authority and release gates.

## Adoption gates

Do not integrate unless all are satisfied:

- **G1 Effect provenance:** action read/write declarations have a machine-checkable source and freshness identity.
- **G2 Alias safety:** resource aliasing/canonicalization is proven sufficient for the target domain.
- **G3 Property contract:** the reduced verification property is formally or independently justified as trace-invariant.
- **G4 Differential validation:** representative plans are compared against exhaustive or trusted POR baselines over a domain-specific corpus.
- **G5 Failure injection:** unknown effects, stale DAGs, conflict under-declaration and limit exhaustion all fail conservatively.
- **G6 Authority isolation:** NPOVL cannot approve, release, mutate policy, or silently lower a required evidence class.
- **G7 Version pinning:** model schema, algorithm revision and adapter revision are included in evidence identity.
- **G8 Observability:** reduction ratio, POR nodes, blockers and plan digest are recorded.
- **G9 Rollback:** disabling NPOVL restores the unreduced verification path without changing correctness semantics.
- **G10 No current-state claim:** integration status remains NOT_VERIFIED until actual integration evidence exists.

## Rejection criteria

Reject this proposal for a target workflow if effects are dynamic and cannot be conservatively modeled, if verification depends on the exact order of otherwise independent actions, or if the cost of proving effect completeness exceeds the work saved by reduction.
