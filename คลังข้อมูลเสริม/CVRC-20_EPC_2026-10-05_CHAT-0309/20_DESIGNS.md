# CVRC-20 Designs

All 20 systems are Lo4 AI proposals. None can override Canon, LAW, CORE, or JUDGE.

| ID | System | Proof obligation | Representative regression |
|---|---|---|---|
| CVRC01 | State Universe Preservation | canonical product states remain representable | FREEZE removed |
| CVRC02 | Trace Forward Simulation | every baseline legal lifecycle step remains simulatable | READY→RUNNING disappears |
| CVRC03 | Illegal Transition Non-Expansion | strict profile cannot legalize non-baseline product transitions | READY→STABLE added |
| CVRC04 | Event Owner Non-Widening | event authority cannot widen | API gains agents_done |
| CVRC05 | Guard Strength Monotonicity | baseline guards cannot be removed | release_policy_passed removed |
| CVRC06 | FREEZE/STOP Dominance | safety transitions cannot move to weaker destinations | error returns READY |
| CVRC07 | Recovery Authority Non-Widening | nonrecoverability and recovery actors cannot widen | HASH_DIVERGENCE becomes recoverable |
| CVRC08 | Release Policy Monotonicity | confidence/determinism/quorum/evidence minima cannot weaken | evidence_min drops |
| CVRC09 | Release Gate Preservation | mandatory release booleans remain mandatory | LAW prerelease gate removed |
| CVRC10 | RBAC Authority Non-Widening | permission role sets cannot expand | OPERATOR gains role management |
| CVRC11 | Module Boundary Non-Expansion | canonical forbidden dependency edges remain forbidden | JUDGE→CORE legalized |
| CVRC12 | Envelope Truth Preservation | required SystemEnvelope truth fields/states/statuses remain | trace_id removed |
| CVRC13 | Error Taxonomy No-Loss | API and VNext failure vocabulary cannot shrink | state violation code removed |
| CVRC14 | Numeric Scope Law Preservation | Q64 carrier and per-scope overflow/div0 semantics remain | Core FREEZE replaced by SATURATE |
| CVRC15 | Queue Safety Monotonicity | idempotency, producer/consumer validation, cancellation and retry defaults remain | default auto-retry enabled |
| CVRC16 | Vault Lineage Monotonicity | append-only/OCC/existing-revision obligations remain | overwrite allowed |
| CVRC17 | Adapter Contract Refinement | external AgentAdapter obligations remain | cancel method removed |
| CVRC18 | Evidence Contract Refinement | source/hash/verification/anchor/normalization provenance remains | verified field removed |
| CVRC19 | Obs/UI/Config Refinement | trace/incident linkage, UI truth, and config evolution obligations remain | UI may mask FREEZE |
| CVRC20 | Composite Promotion Court | aggregate 01–19 without acquiring authority | partial PASS misrepresented as promotion |

## Separation rule
A single proven gate failure cannot be averaged away by high scores from other gates. Q64.64 coverage/risk is evidence telemetry only.

## Integration rule
The composite emits `KEEP_CANDIDATE`, `REJECT`, or `DEFER`, with explicit:
- `authority = NONE`
- `canPromoteCanon = false`
- `canMutateCoreState = false`
- `canWriteVault = false`
- next authority: JUDGE/LAW/governance review.
