# NEXY EPC Scientific Falsification & Replication Chamber (SFRC-20)

**Status:** Lo4 experimental proposal only. Non-canonical. Non-governing. No NEXY runtime authority.

SFRC-20 is a standalone deterministic TypeScript package that evaluates whether a proposed NEXY innovation's **claimed benefit** survives a locked scientific protocol before the proposal is even considered for formal promotion review.

It does not vote proposals into Canon. It does not mutate CORE/JUDGE/LAW state. It does not write to NEXY.AI. Its strongest positive output is an **advisory science packet marked `eligibleForJudgeReview=true` and `canPromote=false`**.

## Why this exists

Existing EPC work already covers court mechanics, causal/evidence governance, adversarial integration testing, and evolutionary integration ecology. SFRC-20 deliberately attacks a different failure mode: a proposal can look excellent because its evaluator changed the metric after seeing results, inspected repeatedly until a favorable point appeared, ignored null results, failed to separate intervention from confounders, or reproduced only in the creator's own environment.

SFRC-20 converts benefit claims into preregistered engineering hypotheses and requires:

- locked hypothesis, primary metric, outcome window, inspection checkpoints and multiplicity budget;
- baseline and control/treatment pairing;
- declared confounders and isolated intervention surface;
- signed checked Q64.64 effect calculations;
- perturbation robustness;
- independent replication by distinct actors;
- cross-environment replication;
- append-only preservation of null/negative results;
- regression-to-mean checks;
- explicit falsification witnesses;
- conservative replication synthesis;
- advisory-only review packet construction.

## The 20 systems

1. Hypothesis Contract Compiler
2. Preregistration Seal
3. Baseline Snapshot Binder
4. Paired Trial Planner
5. Confounder Declaration Gate
6. Intervention Isolation Gate
7. Outcome Window Locker
8. Metric Invariance Guard
9. Sequential Peeking Guard
10. Multiplicity Budget Guard
11. Q64 Effect Magnitude Engine
12. Robustness Envelope Engine
13. Replication Protocol Compiler
14. Independent Replication Ledger
15. Cross-Environment Replication Matrix
16. Null Result Preservation Vault
17. Regression-to-Mean Guard
18. Falsification Witness Extractor
19. Replication Evidence Synthesizer
20. Promotion Science Packet Builder

## Run locally

```bash
npm run check
```

The package has no runtime npm dependencies. TypeScript is compiled with strict settings. The included test runner currently exercises 50 deterministic unit/property/negative/integration checks.

## Integration shape

Treat SFRC-20 as an adapter/shadow verifier upstream of formal promotion review:

```text
Lo4 proposal + claimed benefit
       |
       v
SFRC-01..19 experimental validity pipeline
       |
       v
SFRC-20 Promotion Science Packet
       |  authority=ADVISORY_ONLY, canPromote=false
       v
Existing NEXY evidence / LAW / JUDGE / Human promotion process
```

There is deliberately no function that commits, deploys, promotes, changes Canon, changes the NEXY FSM, calls a network, reads wall-clock time, or uses randomness.

## Evidence

See `EVIDENCE.md` and the exact tested bundle under `bundle/`.
