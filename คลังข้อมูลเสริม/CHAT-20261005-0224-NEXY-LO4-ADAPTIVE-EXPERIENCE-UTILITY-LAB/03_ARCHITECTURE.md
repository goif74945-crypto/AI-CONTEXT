# Architecture

## Authority boundary
ICF is an advisory Lo4 research layer. It can compute proposal-selection and pilot-planning evidence, but it has **zero authority** to:

- alter User Law;
- alter NEXY LAW/JUDGE release semantics;
- promote a proposal into Canon;
- mutate NEXY.AI;
- deploy a feature;
- turn a pilot into production automatically.

## Pipeline

### Stage 1 — IURS
Input: proposal utility intervals by explicit objectives, exact Q64.64 weights, protected minima, maximum tolerated worst-case regret.

Output: `SELECT`, `HOLD`, or `FREEZE`.

Important invariant: a candidate violating a protected objective at its conservative lower bound cannot compensate using gains on other objectives.

### Stage 2 — COMET
Input: candidate base value, already-selected ideas, explicit pairwise overlap evidence.

Output: retained marginal value or `COLLISION`/`FREEZE`.

Important invariant: missing overlap evidence never silently means zero overlap.

### Stage 3 — SCTE
Input: declared change surfaces and explicit burden weights.

Output: total and normalized structural complexity tax plus `PASS`/`REJECT`/`FREEZE`.

Important invariant: complexity is charged separately from benefit so a visually impressive feature cannot hide migration/rollback/public-contract burden inside one opaque score.

### Stage 4 — DCPX
Input: conservative value/cost/complexity per candidate, domains, dependencies, conflicts, complete pairwise overlap evidence and portfolio policy.

Output: exact bounded best feasible portfolio or `HOLD`/`FREEZE`.

Important invariant: the reference algorithm enumerates all subsets up to `max_items` for at most 18 candidates. It does not pretend a heuristic is an optimum.

### Stage 5 — RIVP
Input: one reversible pilot proposal and explicit risk/option-value policy.

Output: `PLAN`, `HOLD`, or `REJECT` with treatment/control budgets. Only `PLAN` carries rollback and stop-rule identifiers.

Important invariant: irreversible effects are invalid by construction.

## Integration result
`run_innovation_capital_flow` composes the five systems and emits a deterministic fingerprint. The integration status can reach `READY_FOR_BOUNDED_PILOT_REVIEW`, never `CANON`, `DEPLOYED`, or `APPROVED`.

## Determinism
Core decision functions depend only on explicit function inputs. They do not read wall-clock time, network state, environment variables, random state, filesystem state or model output directly.
