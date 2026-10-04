# CFPC-20 Architecture

Classification: Lo4 AI-PROPOSED / EXPERIMENTAL / NON-CANONICAL / NON-GOVERNING.

## Purpose
CFPC is an advisory proof layer for proposal computational feasibility. It answers a narrower question than a resource allocator: given a declared worst-case workload and deterministic symbolic bounds, can the proposal prove that all required resource surfaces stay within explicit budgets without weakening verification or authority?

It never promotes, mutates Canon/Law/Core/JUDGE, schedules workers, or claims runtime measurements.

## 20 mechanisms
1. **Input Size Vector Binder** — every symbolic variable must bind to an explicit bounded input dimension.
2. **Complexity Expression Validator** — accepts only a deliberately small nonnegative polynomial grammar with bounded term/exponent counts.
3. **Q64 Coefficient Conformance Gate** — coefficients use checked signed Q64.64 and authoritative negative coefficients are rejected.
4. **Monotonicity Witness** — supported nonnegative polynomial bounds are certified monotone over nonnegative workloads.
5. **Worst-Case Workload Binder** — validates dimension identities/counts/ranges and rejects unbounded declarations.
6. **CPU Work Upper-Bound Verifier** — proves declared CPU work does not exceed budget.
7. **Peak Memory Upper-Bound Verifier** — proves peak memory bound.
8. **Durable State Growth Verifier** — bounds persistent state growth.
9. **Evidence Growth Verifier** — bounds proof/evidence material so verification cannot create unbounded storage pressure.
10. **Fan-Out Amplification Verifier** — bounds expansion into child tasks/agents.
11. **Retry Multiplication Verifier** — bounds retry-induced work amplification.
12. **Queue Pressure Verifier** — bounds queued work accumulation.
13. **Serialization Growth Verifier** — bounds encoded proposal/evidence output size.
14. **External Call Ceiling Verifier** — bounds network/provider calls without authorizing them.
15. **Verification Work Preservation Verifier** — required verification steps must remain present; optimization cannot silently remove proof obligations.
16. **Budget Dominance Analyzer** — hard non-compensatory bound <= budget check.
17. **Bound Composition Engine** — deterministic composition of independent polynomial bounds with explicit term caps.
18. **Fail-Closed Degradation Contract Verifier** — any over-budget state must freeze rather than skip verification/evidence/authority checks.
19. **Canon/Authority Non-Interference Gate** — proposals requesting Canon mutation, Core mutation or automatic promotion freeze regardless of resource score.
20. **Feasibility Certificate Builder** — canonical deterministic record + SHA-256 certificate over exact identity, workload, resource policy, assumptions, verification obligations, degradation contract, evaluated bounds, checks and verdict.

## Numeric model
All quantitative coefficients, evaluated bounds and budgets are signed Q64.64 represented by checked signed-i128 semantics. Intermediate multiplication uses a wider signed-256 domain and narrows only after explicit range checks. IEEE-754 is not part of authoritative scoring or bounds.

## Deliberate grammar limitation
CFPC v0.1 supports finite sums of nonnegative monomials with named nonnegative integer dimensions and exponents 0..8. This is intentionally less expressive than arbitrary code. The benefit is that monotonicity and deterministic evaluation are inspectable. Logarithmic, amortized, probabilistic, recursive and data-dependent bounds are OUT OF SCOPE for v0.1 and must return NOT_VERIFIED/FREEZE rather than being guessed.

## Integration boundary
A future NEXY adapter could feed CFPC a proposal identity, exact source/spec hashes, worst-case size vector, resource budget policy and required verification step IDs. CFPC returns only a proof packet. External JUDGE/Human authority decides whether the packet matters. No CFPC output is a release token.
