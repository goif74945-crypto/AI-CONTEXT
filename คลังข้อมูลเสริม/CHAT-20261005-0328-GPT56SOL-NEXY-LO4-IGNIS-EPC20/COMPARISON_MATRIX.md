# COMPARISON_MATRIX

| Group | Nearest current/prior mechanism | Architecture | Determinism | Canon fit | Evidence | Security | Failure containment | Integration cost | Maintainability | Novelty | Verification | Runtime usefulness | User value | Operational risk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S01/S03/S05 | prechecks/scope governance | narrow pure verifier + | + | + | E2 | + | + | medium | + | PARTIAL | local | + | + | low |
| S02 | queue telemetry/retry | exact Q64 metric + | + | + | E2 | = | = | medium | + | PARTIAL | local | ? telemetry | + | low |
| S04/S14 | retry/idempotency | additive = | + | + | E2 | + | + | low-medium | + | PARTIAL | local | + | + | low |
| S06/S07/S15 | auth/session/rate controls | truth audit + | + | + | E2 | + | + | medium | + | PARTIAL | local | + | + | low |
| S08/S09/S10/S18 | envelope/UI truth | user-truth focus + | + | + | E2 | = | + | medium | + | PARTIAL | local | + | + | low |
| S11 | current secret provider | weaker runtime, defense-in-depth only | + | + | E2 | = | + | low | + | PARTIAL | local | CI useful | = | low |
| S12 | artifact export | inventory coverage + | + | + | E2 | + | + | medium | = | PARTIAL | local | ? | + | medium |
| S13 | capability registry/calibration | orthogonal = | + | + | E2 | = | + | medium | + | PARTIAL | local | + | + | low |
| S16 | audit hash chain | correlation compiler orthogonal | + | + | E2 | = | + | low | + | PARTIAL | local | + | + | low |
| S17 | owner cancel | post-cancel witness + | + | + | E2 | + | + | medium-high | = | PARTIAL | local | ? | + | medium |
| S19 | evidence capsule/LBCC | ref-loss check orthogonal | + | + | E2 | = | + | medium | + | UNKNOWN | local | + | + | low |
| S20 | release reasons/stability work | fixed order proposal + | + | governance needed ? | E2 | = | + | low | + | PARTIAL | local | + | + | low |

**SUPERIORITY = NOT_VERIFIED.** Narrow tested advantages do not prove global superiority over NEXY or other Lo4 systems.
