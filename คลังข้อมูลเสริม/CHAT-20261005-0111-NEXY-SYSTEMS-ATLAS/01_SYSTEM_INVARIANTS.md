# NEXY Future System Invariants
## Purpose
Properties that should remain true across implementations, models, vendors, tools, and UI generations.

## Invariants
I-01 Authority monotonicity: lower-authority evidence never silently overwrites higher-authority evidence. Test contradictory ranked sources. Violation => freeze claim + conflict record.
I-02 Evidence-addressable claims: consequential claims carry evidence IDs, derivation, time/version, and FACT/INFERENCE/ASSUMPTION/UNKNOWN/NOT_VERIFIED.
I-03 Scope conservation: no major expansion without authorization; no silent requirement reduction.
I-04 Side-effect isolation: read, propose, stage, execute, verify are distinct capability states.
I-05 Idempotent recovery: replay cannot duplicate irreversible effects.
I-06 Explicit incompleteness: missing evidence cannot become synthetic completion.
I-07 Compatibility before optimization: external contracts require migration evidence before change.
I-08 Verification independence: critical writes are re-read from authoritative state.
I-09 Temporal correctness: freshness-sensitive claims carry validity/freshness constraints.
I-10 Bounded autonomy: authority, scope, reversibility, cost, and risk budgets bound actions.

Production gate: every subsystem states enforced invariants, tests, and violation behavior.
