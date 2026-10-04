# 20 Executable Lo4 Concepts

All concepts are **PROPOSAL**. Higher score always means a healthier promotion candidate. Every result is UnitQ64 `[0,1]`.

| # | Concept ID | Purpose | Core mechanism |
|---:|---|---|---|
| 1 | `requirement-lock` | Prevent attractive work from outrunning the actual objective | clarity + inverse assumption ratio + canon alignment |
| 2 | `evidence-reliability` | Distinguish broad-but-stale proof from fresh, diverse, provenance-complete proof | coverage×freshness + diversity + provenance |
| 3 | `contradiction-resilience` | Measure whether disagreement is visible and survivable | inverse contradiction×agent-disagreement pressure + observability + evidence |
| 4 | `scope-integrity` | Detect innovation that has escaped the authorized surface | inverse scope distance + inverse change surface + clarity |
| 5 | `canon-compatibility` | Score interoperability without granting authority | canon alignment×interface compatibility + reproducibility |
| 6 | `regression-containment` | Prefer experiments that can fail without damaging adjacent behavior | inverse regression risk + reversibility + rollback readiness |
| 7 | `failure-visibility` | Reward failures that are diagnosable rather than silent | observability + provenance + test coverage |
| 8 | `reproducibility` | Prevent host-specific or dependency-specific illusions of success | deterministic reproducibility + dependency stability + provenance |
| 9 | `safety-utility-balance` | Stop high utility from compensating for weak safety | hard minimum of safety/user value plus multiplicative balance |
| 10 | `novelty-discipline` | Allow radical ideas only when uncertainty and scope are controlled | novelty + inverse uncertainty + inverse scope distance + evidence |
| 11 | `assumption-firewall` | Make hidden assumptions expensive | inverse assumption ratio + evidence + provenance |
| 12 | `dependency-survivability` | Prefer candidates that remain stable under dependency churn | dependency stability + rollback + reproducibility |
| 13 | `blast-radius-control` | Quantify whether a candidate can be isolated and reversed | inverse change surface + reversibility + rollback |
| 14 | `agent-consensus-quality` | Reject shallow consensus that comes from low diversity or poor proof | inverse disagreement + diversity/evidence/contradiction guard |
| 15 | `test-priority-fitness` | Reward candidates whose high-risk paths are actually testable | coverage + inverse regression risk + observability |
| 16 | `promotion-readiness` | Combine hard preconditions that should not be averaged away | canon×safety×reproducibility hard product + tests + evidence + reversibility |
| 17 | `user-value-preservation` | Ensure innovation still solves the user's stated job | user value×requirement clarity + safety + reversibility |
| 18 | `quarantine-readiness` | Ensure an experiment can be isolated when promotion is denied | rollback + observability + reversibility |
| 19 | `uncertainty-burndown` | Measure whether execution is actually reducing unknowns | inverse uncertainty + evidence×freshness + inverse assumptions |
| 20 | `future-adaptability` | Prefer interfaces that can evolve without destroying compatibility | interface compatibility + dependency stability + reversibility + bounded novelty |

## Why these are implemented as a mesh

No single score is allowed to tell the whole story. The 20-dimensional vector lets reviewers see *why* a candidate failed. A feature can have high user value and still be rejected for safety; it can be safe and still be quarantined because evidence is weak; it can be novel and still fail scope integrity.

That avoids the classic aggregate-score catastrophe where one excellent dimension hides one existentially bad dimension.

## Critical rejection floors

The engine currently treats these as catastrophic floors:

- safety-utility-balance < 0.50
- reproducibility < 0.80
- canon-compatibility < 0.60
- requirement-lock < 0.50

Those floors cause `REJECT` regardless of average.

## Mandatory review gates

A candidate cannot become eligible for review unless all of these pass:

- requirement-lock >= 0.80
- evidence-reliability >= 0.75
- canon-compatibility >= 0.85
- regression-containment >= 0.80
- reproducibility >= 0.95
- safety-utility-balance >= 0.80
- promotion-readiness >= 0.85
- overall average >= 0.85

Thresholds are proposal values, not Canon.
