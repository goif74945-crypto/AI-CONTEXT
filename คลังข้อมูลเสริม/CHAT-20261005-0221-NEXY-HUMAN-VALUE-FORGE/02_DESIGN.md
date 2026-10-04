# Architecture — NEXY Human Value Forge

> **Lo4 / AI-PROPOSED / NON-CANONICAL**

## Purpose
Add a deterministic, proof-aware human-value layer that can sit around future NEXY candidate plans without changing NEXY authority. It formalizes five questions that are usually left vague: what did the operator explicitly expect, how surprising is a candidate relative to that contract, which verified plan minimizes declared worst-case regret, which alternatives are Pareto-efficient under explicit utility dimensions, and whether declared satisfaction criteria are actually proven.

## Pipeline
```text
explicit operator/task contract
        |
        v
Expectation Envelope Compiler (EEC)
        |
        +--> Surprise Delta Governor (SDG) --> ALLOW / WARN / FREEZE
        |
verified legal candidate plans
        +--> Regret-Bounded Planner (RBP) --> SELECT / FREEZE / BLOCKED
        |
        +--> Utility Frontier Selector (UFS) --> PARETO SET + explicit-priority selection
        |
observed outcome + evidence
        +--> Satisfaction Proof Contract (SPC) --> PASS / FAIL / NOT_VERIFIED
```

## Invariants
- User-declared hard limits dominate optimization.
- `expected` is not the same as `allowed`: an allowed but unexpected action may WARN; a forbidden/out-of-envelope action FREEZEs.
- RBP never invents probabilities. It uses an explicit scenario/loss matrix only.
- UFS never invents weights. Selection requires an explicit priority order; otherwise it returns the frontier.
- SPC never equates sentiment prediction with proof. Satisfaction means declared criteria met under declared evidence statuses.
- Canonical serialization and sorted identifiers make results stable across input ordering.
- No module can promote itself into NEXY Canon.

## Failure semantics
- contradictory expectation contract -> exception before evaluation;
- missing scenario loss -> `BLOCKED`;
- no eligible legal+verified plan -> `BLOCKED`;
- regret threshold exceeded -> `FREEZE`;
- missing utility metric -> explicit contract error;
- unresolved satisfaction evidence -> `NOT_VERIFIED`;
- hard expectation violation -> `FREEZE`.

## Security / trust boundary
Input is data only. The package executes no subprocess, network, filesystem mutation, repository write, or provider action. Strings are treated as identifiers, not instructions.

## Future NEXY integration
Use adapters from a real NEXY Task Contract / candidate action / proof record into these immutable data structures. NEXY LAW/JUDGE remains authoritative. The forge can supply advisory/gating signals only after formal promotion.
