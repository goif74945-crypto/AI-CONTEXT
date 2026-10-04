# Design — Five AI-Proposed NEXY-Compatible Assurance Systems

## Authority boundary
The following five systems are **AI-PROPOSED CONCEPTS**, not current NEXY requirements. NEXY source context is used only for compatibility constraints: evidence-first behavior, no material guessing, fail/freeze on insufficient proof, deterministic structural results, explicit authority, bounded execution, provenance, and separation of design from runtime evidence.

## 1. Counterexample Distiller (CED)
Purpose: turn a large failing structured case into a smaller reproducible witness.

Input:
- \`case\`: JSON object/list;
- \`interesting_when\`: declarative predicate set;
- \`protected_paths\`: JSON Pointers whose values must survive reduction;
- optional \`max_nodes\`.

Output:
- PASS plus reduced case and content hashes, or FREEZE when baseline is not interesting/contract invalid.

Invariants:
- baseline must reproduce before reduction;
- protected paths cannot disappear or change;
- deterministic key/order traversal;
- no arbitrary code execution;
- bounded input size.

Limitation: current reducer is greedy structural minimization, not a proof of globally smallest nested JSON witness.

## 2. Minimal Unsat Constraint Core Finder (MUCF)
Purpose: explain why no supplied candidate can satisfy all explicit constraints.

Input:
- finite candidate objects;
- predicate constraints with stable IDs;
- explicit maximum constraint bound.

Output:
- PASS plus feasible candidate indices, or FREEZE with a minimal-cardinality unsatisfiable constraint core.

Invariants:
- no invented candidate universe;
- duplicate/invalid constraints reject;
- deterministic core ordering;
- hard combinatorial bounds.

Limitation: proof is relative to the supplied finite candidate set.

## 3. Evidence Freshness Revalidation Planner (EFRP)
Purpose: stop stale evidence from silently proving a changed system.

Input:
- explicit \`now\`;
- current dependency/spec versions;
- evidence artifacts with observation timestamp, max age, captured versions, and evidence DAG dependencies.

Output:
- PASS when all evidence remains valid, or FREEZE with stale reasons and topological revalidation order.

Invalidation reasons include:
- TTL_EXPIRED;
- OBSERVED_IN_FUTURE;
- VERSION_CHANGED;
- UNKNOWN_CURRENT_VERSION;
- UPSTREAM_STALE.

Invariants:
- no ambient system clock;
- timezone required;
- cycles reject;
- upstream invalidation propagates.

## 4. Spec Example Conformance Linter (SECL)
Purpose: catch documentation/examples that teach behavior inconsistent with declared machine-readable rules.

Input:
- rule set;
- PASS/FREEZE examples.

Output:
- PASS or FAIL with example IDs and failed rule IDs.

Invariants:
- declarative predicate vocabulary only;
- duplicate IDs reject;
- bounded examples/rules;
- contradictions are explicit, never silently repaired.

Limitation: prose-only requirements must first be converted into an authoritative machine-readable rule representation.

## 5. Verified Recovery Path Planner (VRPP)
Purpose: produce an explainable recovery route from a frozen/unsafe state to a declared safe state.

Input:
- finite states;
- current state;
- safe states;
- transitions;
- required evidence per transition;
- available evidence;
- maximum steps.

Output:
- PASS with shortest deterministic path, or FREEZE when no provable safe route exists.

Invariants:
- planner does not execute actions;
- unknown states/duplicate transitions reject;
- missing prerequisite evidence disables the transition;
- bounded BFS;
- lexicographic deterministic tie-break with alternate shortest paths exposed.

Limitation: safety is only as complete as the supplied FSM, transition preconditions, and evidence declarations.

## Shared security model
- Python standard library only.
- No network access in core.
- No subprocess/eval/exec/randomness in decision engines.
- CLI uses deterministic JSON serialization.
- Invalid external inputs fail closed.
- Limits protect obvious state/candidate explosion.
- External/NEXY integration remains a separate future adapter boundary requiring E3/E4+ evidence.
