# Context Integrity Protocol

Problem: autonomous systems fail when correct facts are mixed with stale, inferred, cross-task, or lower-authority material.

## Every durable statement should conceptually carry
value; status (FACT/ASSUMPTION/UNKNOWN/CONFLICT); source; authority; observed_at; scope; freshness; supersedes/superseded_by.

## Truth partitions
SPEC_TRUTH: what must be true.
REPO_TRUTH: what source currently contains.
RUNTIME_TRUTH: what execution currently demonstrates.
EXTERNAL_TRUTH: verified outside facts.
HYPOTHESIS: reasoned but unverified.
Never collapse these partitions.

## Context loading
Load minimum sufficient authority first, then relevant project state, then task evidence. Avoid dumping entire repositories into context merely because tokens exist. More tokens can increase contradiction and retrieval noise. Human civilization has already demonstrated that possessing more paperwork does not automatically produce wisdom.

## Conflict algorithm
1. Identify statements that cannot simultaneously hold.
2. Tag source and authority.
3. Determine whether scopes/times differ.
4. If authority resolves conflict, select authoritative statement and retain conflict history.
5. If not resolvable, mark CONFLICT and block dependent irreversible action.

## Checkpoint contract
task_id; objective; immutable_constraints; completed_verified; in_progress; blockers; evidence_refs; mutations_done; next_exact_action; regression_state; context_version.

## Contamination defense
Never import another task's conclusions as authority without re-validating scope, freshness and source.
