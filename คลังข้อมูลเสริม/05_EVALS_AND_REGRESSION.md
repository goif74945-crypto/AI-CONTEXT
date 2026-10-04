# Agent / System Evals and Regression Architecture
Status: FACT_EXTERNAL + PROPOSAL
External baseline: Anthropic 2026 guidance emphasizes multi-turn/tool-using agent evals and building eval sets from real failures.

## Evaluation layers
L0 deterministic unit invariants
L1 contract tests
L2 integration tests
L3 workflow/agent trajectory tests
L4 adversarial/security tests
L5 release evidence validation
L6 production canary/observability

## What to score
Not only final answer:
- requirement satisfaction
- authority selection
- tool selection
- argument correctness
- side-effect correctness
- forbidden side effects
- evidence quality
- recovery behavior
- stop/freeze behavior
- latency/resource budget
- reproducibility

## Golden trajectory warning
Do not require one exact reasoning path when multiple legal paths exist.
Require invariants, allowed tool/action sets, terminal state and evidence.

## Failure-derived eval loop
1. capture real failure
2. minimize reproducible case
3. classify failure
4. add expected invariant
5. prove test fails before fix when feasible
6. apply fix
7. prove test passes
8. run adjacent regression set
9. preserve case permanently if high-value

## Mutation testing for authority
Generate variants:
- MUST -> SHOULD
- current -> superseded
- verified -> unverified
- exact SHA -> different SHA
- read-only -> write request
System should detect semantic authority changes rather than pattern-match words.

## Release comparison
Compare candidate vs baseline by failure class, not aggregate score only.
A +5% average that introduces one destructive authority regression is unacceptable.

## Eval dataset governance
Each case needs origin, date, requirement, expected result, severity, deterministic fixtures where possible, and retirement/supersession reason.
