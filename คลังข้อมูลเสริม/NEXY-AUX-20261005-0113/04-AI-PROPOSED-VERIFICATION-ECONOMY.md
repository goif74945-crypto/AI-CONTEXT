# AI-PROPOSED CONCEPT — Verification Economy & Proof Scheduling
Status: PROPOSAL / RESEARCH MODEL

## Motivation
Verification is not free. Large systems can waste time rerunning irrelevant proof or, worse, skip expensive proof and overclaim confidence.
AI_PROPOSED_CONCEPT: schedule evidence work from risk + invalidation dependency, while never lowering mandatory evidence required by authority.

## Hard invariant
Optimization may choose WHEN/WHAT ORDER to verify, never redefine the minimum evidence class required for a claim.

## Inputs
- changed artifacts and dependency closure
- claim criticality
- required evidence class
- historical failure density
- security/safety relevance
- blast radius
- evidence cost/time
- proof freshness
- environment availability
- unresolved conflicts
- nondeterminism indicators

## Priority model
Conceptual score only:
Priority = MandatoryGate + Criticality + ChangeImpact + FailureRisk + Staleness + ConflictWeight - ReuseEligibility.
Weights must be policy-controlled and versioned. Mandatory gates cannot be outscored.

## Proof reuse
Reuse only when:
- exact applicable subject revision or proven unaffected dependency slice
- environment constraints still match
- verifier/toolchain compatibility holds
- fixtures remain valid
- no policy change invalidates the proof
- freshness requirement holds

## Verification DAG
Represent tests/evidence jobs as a DAG:
cheap static prerequisites → unit → integration → E2E → runtime/deploy.
Fail fast only where downstream proof would be meaningless. Preserve skipped reason explicitly.

## Negative-path quota
Critical claims require explicit negative-path coverage. Suggested categories:
invalid input, permission denial, timeout, dependency failure, duplicate/idempotency, rollback/recovery, injection/abuse, stale evidence, conflicting authority.

## Adaptive verification
HYPOTHESIS: historical failures can prioritize additional tests, but cannot suppress canonical mandatory tests.
Example: repeated idempotency regressions increase priority of duplicate-delivery tests.

## Budget exhaustion behavior
If required proof cannot fit available execution budget:
status must remain NOT_VERIFIED/BLOCKED/PARTIAL as applicable.
Never convert “not tested because expensive” into PASS.

## Anti-gaming rules
- model confidence has zero proof weight
- code volume has zero proof weight
- previous PASS does not survive relevant invalidation
- number of agents agreeing is not evidence class
- synthetic mock success cannot prove deployment
- benchmark score cannot prove policy compliance

## Outputs
VerificationPlan:
claim set; required classes; ordered jobs; dependencies; estimated cost; mandatory/optional flag; reuse decision + justification; invalidation references; stop conditions.

VerificationResult:
job identity; exact revision/environment; result; artifacts; limitations; downstream claims updated.

## Research questions
- Can dependency-sliced proof reuse be sound enough for large monorepos?
- How should environment fingerprints be normalized?
- What proof types need expiry independent of code change?
- How should nondeterministic external providers affect evidence freshness?
- How to prove that the scheduler itself never suppresses mandatory gates?

## Promotion gate
Formal policy for mandatory gates, deterministic scheduler behavior, property tests, adversarial budget tests, and auditability of every skip/reuse decision.
