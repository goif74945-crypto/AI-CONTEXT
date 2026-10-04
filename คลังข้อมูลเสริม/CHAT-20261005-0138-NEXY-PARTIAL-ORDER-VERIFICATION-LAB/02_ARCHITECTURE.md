# NPOVL Architecture and Algorithm Contract

Classification: **AI_PROPOSED / ADVISORY / NOT_CURRENT_NEXY_REQUIREMENT**

## 1. Objective

Reduce redundant concurrent verification schedules while preserving one representative for every trace-equivalence class defined by an explicit, conservative, static independence relation.

The system is useful only as a subordinate verification-planning primitive. It has no authority to approve a result, release a build, mutate NEXY state, or weaken mandatory evidence.

## 2. Inputs

A model contains:

- a finite set of uniquely identified actions;
- an acyclic `depends_on` relation;
- exact resource tokens in `reads` and `writes`;
- per-action `effects_complete` and `opaque` flags;
- model-level `dependency_declarations_complete` attestation;
- verification-level `trace_invariant_under_declared_independence` attestation;
- explicit search and output limits.

Resource identity is exact-string identity in v1. Wildcards, aliases, hierarchical resources and semantic equivalence are intentionally unsupported because silently interpreting them would make independence unsafe.

## 3. Static independence relation

Let action `a` have read set `R(a)` and write set `W(a)`. Let `HB(a,b)` mean that `a` is a transitive declared prerequisite of `b`.

`I(a,b)` is true only if:

- `a != b`;
- neither action is opaque;
- both actions assert complete effect declarations;
- neither `HB(a,b)` nor `HB(b,a)` holds;
- `W(a) ∩ W(b) = ∅`;
- `W(a) ∩ R(b) = ∅`;
- `W(b) ∩ R(a) = ∅`.

This relation is symmetric and irreflexive by construction. It is intentionally an under-approximation of semantic commutativity. False dependence costs performance; false independence can cost correctness, so the design chooses the former.

If an action has unknown effects, v1 does **not** reject the whole model. That action is conservatively dependent with every other action. If the dependency graph itself is declared incomplete, reduction is blocked because hidden causal precedence could invalidate reordered schedules.

## 4. Trace equivalence

Two legal linearizations are considered equivalent when one can be transformed into the other by repeatedly swapping adjacent actions related by `I`.

For exact audit, each complete trace is mapped to an independent class signature: for every unordered **dependent** action pair, record their observed relative order. Equal signatures represent the same static Mazurkiewicz-style class under this model.

`canonical_trace_key()` separately constructs a dependent-order graph from a trace and returns its lexicographically smallest topological ordering. The exact audit intentionally does not use canonicalization as its only oracle; class signatures are computed independently so a canonicalization defect cannot trivially certify itself.

## 5. Reduced exploration

The reference kernel implements a classic static sleep-set exploration:

1. compute all currently enabled actions in deterministic lexical order;
2. skip actions in the inherited sleep set;
3. choose an enabled action;
4. retain only sleeping actions that commute with the chosen action;
5. recurse;
6. add the chosen action to the local sibling sleep set.

This removes many schedules that differ only by commuting choices. It is **not** claimed to be optimal POR. Research literature explicitly shows that non-optimal POR methods can still explore exponentially many redundant schedules in some systems, so NPOVL reports its POR node count and exposes strict search budgets rather than pretending the state-explosion problem has been abolished.

## 6. Two verification modes

### 6.1 `EXACT_CROSS_CHECK`

`analyze_model()`:

- validates the model;
- checks reduction preconditions;
- counts legal linear extensions with memoized subset-state DP;
- blocks if exact full-trace count exceeds `max_full_traces`;
- runs sleep-set POR;
- exhaustively enumerates all legal traces within the bound;
- computes exact class signatures and representative class signatures;
- returns `FAIL/POR_CLASS_COVERAGE_MISMATCH` if the two sets differ.

This mode is evidence-heavy and deliberately bounded.

### 6.2 `PLAN_ONLY`

`plan_model()`:

- validates the same safety preconditions;
- attempts exact trace counting subject to `max_states`;
- if counting exceeds that metric budget, returns `full_trace_count: null` plus `FULL_TRACE_COUNT_OMITTED_STATE_LIMIT` but may continue;
- runs the reduced exploration under the separate `max_por_nodes` and `max_representatives` budgets;
- rejects duplicate representative class signatures.

The metric count is not allowed to become a hidden precondition for sound plan generation.

## 7. Safety limits and failure law

| Condition | Behavior |
|---|---|
| malformed schema / missing dependency / cycle | validation failure |
| dependency completeness not attested | `BLOCKED` |
| property trace invariance not attested | `BLOCKED` |
| exact full-trace audit exceeds limit | `BLOCKED` in exact mode |
| DP trace-count state budget exceeded | count omitted in plan-only; reduction may continue |
| POR search node budget exceeded | `BLOCKED` |
| representative budget exceeded | `BLOCKED` |
| exact oracle and POR classes disagree | `FAIL` |
| opaque/incomplete action effects | no inferred independence involving that action |

No mode silently truncates a representative set and then calls it complete.

## 8. Determinism

- action IDs, dependencies, reads and writes are normalized and sorted;
- input action order is non-semantic;
- enabled choices are lexically sorted;
- output dictionaries use canonical JSON ordering;
- model and output identities use SHA-256 over canonical JSON;
- no RNG is used;
- the core package has no network calls or subprocess execution.

CLI file I/O is an adapter boundary, not core decision logic.

## 9. Soundness obligations

The reduction is only intended to preserve a verification claim if all of the following hold:

**O1 — Dependency completeness.** Declared causal dependencies cover every ordering constraint relevant to legal execution.

**O2 — Effect conservatism.** Any effect omitted from `reads/writes` must force `effects_complete=false` or `opaque=true`; otherwise an undeclared conflict can produce false independence.

**O3 — Resource identity correctness.** Equal real resources must map to equal resource tokens before NPOVL sees the model.

**O4 — Trace-invariant verification property.** The verifier must not distinguish schedules solely by reordering action pairs declared independent. NPOVL requires an explicit attestation but cannot prove this property for an arbitrary downstream verifier.

**O5 — Static-action semantics.** Actions occur at most once in a model and the independence relation is state-independent. Dynamic creation, retries, loop iterations and state-dependent commutativity are outside v1.

**O6 — Class coverage.** For bounded exact audit, every exhaustive dependent-order class must have a reduced representative. The implemented oracle checks this directly.

## 10. Complexity

Let `n` be the number of actions.

- dependency closure and independence table are polynomial in `n` for the static model;
- exact topological-trace enumeration is necessarily proportional to the number of legal linearizations;
- exact subset-state trace counting can visit up to `2^n` states;
- sleep-set POR can still be exponential and is not advertised as optimal;
- output size is at least proportional to the number of trace classes that must be represented.

The implementation therefore treats budgets as correctness boundaries, not merely performance knobs.

## 11. Compatibility boundary for NEXY

A future adapter could map an already-authorized NEXY verification DAG into NPOVL's neutral action model, use the returned representative plan to schedule **tests**, and return evidence to the existing authority path. The adapter must not:

- let NPOVL choose policy or User Law;
- let NPOVL waive a required verification class;
- treat a reduced plan as proof of execution;
- infer effects from model-generated text;
- bypass CORE/JUDGE authority;
- call the AI proposal a current NEXY requirement without an explicit authoritative adoption decision.

## 12. Verification strategy used in this lab

- TDD RED evidence recorded before source implementation.
- Unit and negative tests for conflict semantics, DAG validation, limits and determinism.
- Exhaustive generated small-model comparison across 1,184 model instances.
- Independent test-side brute-force permutation oracle across another 256 four-action models using plan-only mode, intentionally bypassing the engine's exhaustive-audit helper.
- Fixture contracts for PASS, conservative dependence, BLOCKED, invalid and large-plan behavior.
- 20-run byte-level deterministic replay check.
- Compile and coverage execution.

This evidence verifies the reference implementation within its finite model and tested corpus. It is not E3+ integration/runtime/deployment evidence for NEXY.AI.
