# Design Contract — Deterministic Interleaving Verifier

## 1. Purpose
Provide an exact bounded model checker for declarative multi-action plans so future NEXY-style orchestration can detect schedule-dependent behavior before treating a concurrent plan as deterministic.

## 2. Non-goals
- Not a thread scheduler.
- Not a transaction executor.
- Not a replacement for the existing Side-Effect Transaction Lab.
- Not a context-drift/revalidation planner.
- Not proof of real NEXY runtime concurrency.
- Not a linearizability checker for arbitrary programs.
- Not a theorem prover over unbounded state.
- Not a source-code interpreter.

## 3. Authority
The verifier owns only the semantics of its declared DSL and report format. It does not own business ordering authority. If two unordered actions conflict, the verifier may identify the pair but must not choose which should win.

## 4. Core state machine
`LOAD -> VALIDATE -> NORMALIZE -> STATIC_CONFLICT_ANALYSIS -> EXACT_STATE_EXPLORATION -> COUNTEREXAMPLE | CONFLUENCE -> REPORT`

Fail-closed side transitions:
- validation ambiguity -> `FREEZE_INVALID_INPUT`;
- state/transition budget exhaustion -> `FREEZE_LIMIT`;
- input read/JSON/output error -> `FREEZE_IO_OR_JSON` at CLI boundary.

## 5. Model
A plan contains:
- canonical initial JSON object state;
- mandatory atomic actions;
- dependency edges between actions;
- action preconditions;
- deterministic effects;
- global invariants;
- exact exploration limits.

### Atomicity assumption
Each action is atomic with respect to interleaving. If a real operation exposes intermediate externally visible states, it must be decomposed into multiple modeled actions. Treating a non-atomic real operation as atomic can create a false PASS and is therefore an integration error.

## 6. Deterministic data restrictions
Canonical state permits JSON objects/arrays plus strings, booleans, null, and integers. Floating point is rejected to avoid cross-runtime representation and arithmetic ambiguity. Object keys are strings. Paths use non-root JSON Pointer-style strings.

## 7. Exact state-space reduction
Naive schedule enumeration grows as `n!` for `n` unordered actions.

The engine instead stores a node as:
`K = (sorted(completed_action_ids), canonical_json(state))`

Two histories with the same K are future-equivalent because:
1. enabled actions depend only on completed dependencies;
2. every action transition is a deterministic function of state;
3. invariants are deterministic functions of state;
4. no hidden clock/random/network/environment input exists.

Therefore the engine may merge them without losing a distinct reachable future state. This is exact reduction, not sampling.

Observed regression case: 10 commuting actions represent `10! = 3,628,800` full schedules but collapse to 1,024 unique states and 5,120 explored transitions.

## 8. PASS proof obligation
PASS requires all of the following:
- valid acyclic dependency graph;
- exact exploration completed before caps;
- every reached enabled mandatory action satisfied its preconditions;
- every action effect evaluated deterministically;
- every reached post-action state satisfied every invariant;
- exactly one canonical terminal state existed.

A static conflict does not automatically fail. Two actions may conflict syntactically yet commute semantically, such as integer additions.

## 9. FAIL proof obligation
A single reproducible counterexample is sufficient for FAIL:
- mandatory action precondition can become false;
- effect is not executable on a reachable state;
- invariant is violated;
- two complete schedules yield distinct terminal states.

Complete exploration is not required after a decisive counterexample because the universal safety/confluence claim is already disproved.

## 10. Static conflict analysis
For unordered action pairs, the verifier reports path-prefix-aware:
- write/write overlap;
- left-write/right-read overlap;
- left-read/right-write overlap.

Dependencies suppress a pair from the unordered conflict list when one transitively orders the other.

Static conflict output is diagnostic evidence only, not a substitute for dynamic state exploration.

## 11. Divergence witness
When two terminal states differ, output contains:
- `schedule_a` and `schedule_b`;
- both final states;
- deterministic structural state diff;
- first conflicting unordered pair whose relative order differs, when one is identifiable.

The report explicitly refuses to choose a serialization direction without external authority.

## 12. Security boundary
Input values are data only. The verifier never:
- executes strings;
- imports user-selected modules;
- spawns processes;
- calls network services;
- reads environment/secrets;
- performs filesystem mutation in core logic.

The CLI reads one JSON file and optionally writes one report file.

## 13. Evolution law
New operations must define:
- exact deterministic semantics;
- read/write footprint derivation;
- invalid-state behavior;
- schema branch;
- positive/negative tests;
- oracle or regression evidence where applicable.

No operation may be added merely as a passthrough to arbitrary code.
