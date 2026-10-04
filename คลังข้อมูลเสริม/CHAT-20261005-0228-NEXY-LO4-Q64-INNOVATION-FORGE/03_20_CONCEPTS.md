# Twenty Lo4 Concepts

All entries below are **AI-proposed Lo4 concepts only**. None is canonical NEXY law.

| # | Concept | Purpose | Key fail-closed condition |
|---:|---|---|---|
| 01 | Evidence Dispersion Governor | Measures aggregate evidence integrity and disagreement spread before downstream use. | Integrity too low or dispersion too high. |
| 02 | Proof Gain Scheduler | Ranks verification work by expected proof gain relative to cost and risk, then fits a budget. | No useful test fits the declared budget. |
| 03 | Uncertainty Budget Allocator | Allocates a finite uncertainty budget across stages with floors and deterministic residual correction. | Required floors exceed total budget or allocation invariant breaks. |
| 04 | Consensus Margin Auditor | Quantifies proof-weighted consensus margin across independent agents. | Duplicate agents, insufficient independence, or top-vs-second margin too small. |
| 05 | Capability Shadow Price Router | Selects a feasible worker/capability using success utility penalized by cost, latency, and risk. | No option satisfies hard bounds. |
| 06 | Temporal Freshness Gate | Decays evidence confidence by explicit age/TTL rather than pretending stale evidence remains current. | Effective confidence falls below threshold or temporal contract is invalid. |
| 07 | Decision Stability Envelope | Measures how far a selected score is from adversarial/uncertainty perturbation boundaries. | Stability margin is insufficient. |
| 08 | Degradation Ladder Planner | Chooses the highest-utility safe degraded operating level under capability loss. | No degraded level satisfies minimum safety. |
| 09 | Rollback Value Ranker | Ranks changes by expected rollback value using impact, reversibility, and detection delay. | Invalid decision inputs; otherwise produces deterministic ranking. |
| 10 | Constraint Pressure Map | Quantifies normalized pressure against hard resource/constraint limits. | Any hard limit is exceeded or invalid. |
| 11 | Determinism Drift Detector | Compares repeated quantitative observations against a strict drift budget. | Observed drift exceeds declared tolerance. |
| 12 | Model Trust Update | Updates bounded trust from prior trust and verified positive/negative evidence without granting authority. | Invalid evidence weights or trust contract. |
| 13 | Lo4 Promotion Proof Accumulator | Aggregates required evidence classes and quality for *eligibility for formal review only*. | Missing required evidence class or quality below threshold. |
| 14 | Failure Injection Priority Engine | Ranks failure scenarios by likelihood × impact × low detectability × low recovery ease. | Invalid bounded inputs. |
| 15 | Resource Saturation Forecaster | Extrapolates a bounded linear saturation trend over an explicit step horizon. | Forecast crosses freeze threshold or horizon is invalid. |
| 16 | Cross-Agent Independence Guard | Estimates ensemble independence from weighted overlap so correlated agents do not masquerade as consensus. | Independence below minimum or malformed/self pair. |
| 17 | Authority Gap Quantifier | Quantifies disagreement mass among assertions weighted by declared authority/confidence. | Conflict mass exceeds maximum allowed bound. |
| 18 | Audit Sampling Optimizer | Chooses highest risk×unknownness audit coverage per cost under a finite budget. | No audit item fits the budget. |
| 19 | Verification Frontier Compiler | Produces the ranked frontier of unmet evidence targets using deficit×impact/cost. | Returns FREEZE while verification gaps remain. |
| 20 | Dependency Confidence Firewall | Propagates confidence through a weighted dependency DAG so weak upstream proof cannot silently support a critical claim. | Cycle, missing dependency, duplicate node, or critical effective confidence below threshold. |

## Why these are a set instead of twenty isolated toys
The value is composability around one numeric truth surface. For example, C19 can identify the largest verification deficits, C02 can schedule proof work, C13 can evaluate evidence-class completeness, and C20 can ensure downstream critical claims do not exceed the confidence of their dependency chain. That sequence is exercised by `tests/integration-chain.test.js`.

## Promotion rule
A PASS from any module means only “this module's declared mathematical contract passed for this input.” It never means “NEXY should ship,” “the proposal is Canon,” or “release is authorized.”
