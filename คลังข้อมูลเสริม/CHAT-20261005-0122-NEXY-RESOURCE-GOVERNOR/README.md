# NEXY Proof-Preserving Resource Governor Lab

**Status:** AI-PROPOSED / reference implementation only  
**Canonical NEXY status:** NOT PROMOTED  
**NEXY.AI implementation/runtime/deployment:** NOT_VERIFIED

This isolated supplemental lab explores deterministic allocation of AI workers/verifiers under hard capability, privacy, evidence, independence, token, cost, and latency constraints.

The central rule is deliberately boring and strict: **optimization may choose among legal plans; it may not make an illegal plan legal.** If the required plan cannot fit the available resources, the reference governor returns `FREEZE` rather than silently weakening verification, privacy, or authority.

## Why this is distinct

The existing supplemental Verification Economy work schedules proof jobs. This lab instead allocates **execution resources and model/agent roles** while treating proof requirements as non-negotiable constraints. It is therefore adjacent but not a duplicate.

## Reference properties

- deterministic lexicographic ranking;
- integer-only price arithmetic;
- explicit data-clearance gating;
- quarantine/inactive-agent rejection;
- capability and context-window gating;
- risk-driven independent-verifier enforcement;
- hard token/cost/latency budgets;
- evidence capability floors;
- elimination trace for every rejected candidate/pair retained within configured diagnostic bounds;
- successful allocation remains `NOT_VERIFIED` until real evidence is executed.

## Files

- `01_TASK_CONTRACT.md` — objective, scope, acceptance criteria.
- `02_ARCHITECTURE.md` — modules, authority, state and deterministic ordering.
- `03_REQUIREMENT_LEDGER.md` — requirement-to-evidence map.
- `04_CONTRACTS.md` — human-readable contract semantics.
- `contracts/resource-governor.schema.json` — machine-readable proposal contract.
- `src/models.py`, `src/governor.py`, `src/serde.py` — deterministic Python reference implementation split into contracts, planner and mapping boundary.
- `tests/test_governor.py` — unit/adversarial tests.
- `tests/test_properties.py` — fixed-seed property-style invariant regression.
- `fixtures/scenarios.json` — reusable scenario corpus.
- `benchmarks/benchmark_governor.py` — reproducible synthetic scale benchmark.
- `05_FAILURE_MODEL.md` — fail/freeze semantics.
- `06_INTEGRATION_PROPOSAL.md` — non-governing NEXY integration concept.
- `07_RESEARCH_BACKLOG.md` — experiments required before any promotion.
- `08_VALIDATION_REPORT.md` — executed evidence for this lab.
- `09_FINAL_AUDIT.md` — scope/boundary/completion audit.

No file in this lab claims that NEXY.AI currently implements this design.
