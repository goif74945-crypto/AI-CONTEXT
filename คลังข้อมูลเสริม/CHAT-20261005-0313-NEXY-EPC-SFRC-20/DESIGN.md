# SFRC-20 Architecture and Design

## 1. Design class
`Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING`

SFRC-20 is a **benefit-claim falsification layer**, not a proposal generator, JUDGE replacement, vote authority, deployment gate, or integration executor.

## 2. Core invariant
A proposal is never considered experimentally supported merely because a score improved. A support claim requires a locked hypothesis, locked measurement contract, controlled intervention, complete preregistered observation surface, robustness evidence, independent replication, and no unresolved falsification/null evidence. The final output is only a packet for existing authority to inspect.

## 3. Trust and authority boundary
```text
UNTRUSTED / EXPERIMENTAL
Lo4 candidate + claimed benefit
         |
         v
SFRC scientific pipeline
         |
         v
ADVISORY packet only
         |
--------- authority boundary --------------------------------
         v
NEXY LAW / evidence gates / JUDGE / authorized Human process
```
SFRC cannot cross the boundary itself.

## 4. Determinism contract
The implementation uses canonical key ordering and explicit lexical ordering; SHA-256 domain separation; signed Q64.64 represented by BigInt restricted to signed-i128 range; stable string IDs and exact lowercase SHA-256 identities; no locale collation; no randomness; no time source; no network source; and no binary floating-point decision math.

Structural counts/indexes may use ordinary integer language constructs; authoritative effect/robustness values are Q64.64.

## 5. Numeric failure law
`src/q64.ts` rejects result outside signed i128 range, divide by zero, invalid unit interval where required, and negation of signed-i128 minimum. The standalone package throws a typed `FailClosedError`. It does not claim to invoke NEXY's actual FSM freeze because it is deliberately not integrated into NEXY runtime.

## 6. Twenty-system pipeline
1. **SFRC-01 Hypothesis Contract Compiler**: locks candidate ID, claim, metric, direction, effect floor, invariants, confounders and allowed intervention paths into a deterministic hypothesis hash.
2. **SFRC-02 Preregistration Seal**: locks metric hashes, scenarios, outcome window, checkpoints, multiplicity budget, robustness spread and replication count before results.
3. **SFRC-03 Baseline Snapshot Binder**: binds baseline metrics to source commit, environment, metric definition and evidence identity.
4. **SFRC-04 Paired Trial Planner**: creates exactly one control/treatment pair for every preregistered scenario and rejects identical artifacts.
5. **SFRC-05 Confounder Declaration Gate**: fails any detected undeclared confounder.
6. **SFRC-06 Intervention Isolation Gate**: fails when changed paths exceed allowed intervention surface or external mutation lacks evidence.
7. **SFRC-07 Outcome Window Locker**: rejects observations outside the locked ordinal window; empty evidence produces DEFER.
8. **SFRC-08 Metric Invariance Guard**: rejects post-hoc metric-definition changes.
9. **SFRC-09 Sequential Peeking Guard**: only preregistered inspection/stopping checkpoints are legal and history must be monotonic.
10. **SFRC-10 Multiplicity Budget Guard**: enforces preregistered claim count and rejects duplicate claim identities.
11. **SFRC-11 Q64 Effect Magnitude Engine**: requires exact scenario coverage and computes direction-adjusted mean, median and conservative minimum effect in Q64.64.
12. **SFRC-12 Robustness Envelope Engine**: computes perturbation-group effects and conservative min/max/spread so weak perturbations cannot be averaged away.
13. **SFRC-13 Replication Protocol Compiler**: binds replication protocol to preregistration, metric, scenarios, effect floor, direction and originator.
14. **SFRC-14 Independent Replication Ledger**: append-only experiment record requiring unique replication IDs and actor identities; originator cannot count as independent replicator.
15. **SFRC-15 Cross-Environment Replication Matrix**: requires passing replication evidence in every explicitly required environment.
16. **SFRC-16 Null Result Preservation Vault**: hash-chained append-only NULL/NEGATIVE results; duplicate experiment identities rejected.
17. **SFRC-17 Regression-to-Mean Guard**: requires at least three repeated baselines and effect exceeding both floor and observed baseline drift.
18. **SFRC-18 Falsification Witness Extractor**: selects deterministic canonical first invariant violation; no checks means DEFER, not PASS.
19. **SFRC-19 Replication Evidence Synthesizer**: conservative minimum replication effect and non-compensatory failure; too few replications DEFER.
20. **SFRC-20 Promotion Science Packet Builder**: requires critical gates and emits `authority="ADVISORY_ONLY"` with compile-time literal `canPromote=false`.

## 7. Failure states
Malformed input fails closed; absent non-critical evidence DEFERs where meaningful; missing critical evidence during packet build fails closed; contradictions FAIL; insufficient replications DEFER; failed replication FAIL; unresolved same-hypothesis null/negative result blocks review eligibility; promotion is impossible through the public SFRC packet type.

## 8. Conservative minima
Minimum effects are intentionally used at critical boundaries. High performance in easy scenarios must not compensate for failure in a required scenario/environment. This is aligned with non-compensatory control logic.

## 9. Persistence model
The core library is pure except two explicit append-only in-memory ledgers: `IndependentReplicationLedger` and `NullResultPreservationVault`. Neither writes disk, network or NEXY state. A future adapter may persist immutable records in an authorized store but must preserve hashes and authority boundaries.

## 10. Promotion path
SFRC proves only experimental validity of a claim. It does not prove complete Canon compatibility, all integration security, deployment readiness, full runtime correctness, or authority to merge/promote.
