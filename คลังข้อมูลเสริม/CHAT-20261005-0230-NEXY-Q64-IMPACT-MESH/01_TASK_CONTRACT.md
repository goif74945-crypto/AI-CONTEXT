# Task Contract — NEXY Q64 Impact Mesh

Classification: Lo4_AI_PROPOSAL_ONLY / NON_GOVERNING / REFERENCE_IMPLEMENTATION

## OBJECTIVE
Design, implement, test, and persist twenty new deterministic advisory engines that quantify action economics, accumulated impact, reversibility, fairness, concentration, staleness, resource margins, and exit costs for possible future NEXY use.

## REQUIRED OUTPUT
- exact signed Q64.64 arithmetic kernel;
- 20 independently testable engines;
- deterministic suite/orchestrator without execution authority;
- positive, negative, property, integration, stress, and static-Q64 tests;
- AI-proposed design document and collision audit;
- adapter/integration contract for NEXY-facing use without direct integration;
- failure/fix/retest log;
- evidence, hashes, manifest, final audit, and resumable execution memory.

## IN SCOPE
Standalone code and evidence under this namespace only.

## OUT OF SCOPE
- mutation of any repository whose name contains NEXY.AI;
- Canon promotion;
- production deployment;
- provider/network/model calls;
- inferring user permissions or evidence quality;
- auto-executing recommendations.

## ACCEPTANCE CRITERIA
1. All 20 engines have materially distinct responsibilities.
2. All quantitative calculations use signed Q64.64.
3. No float literals exist in production quantitative modules.
4. Deterministic replay is byte-identical under different PYTHONHASHSEED values.
5. Invalid input paths are tested and fail closed.
6. Integration demo exercises all 20 engines.
7. Stress/property tests cover arithmetic and engine invariants.
8. Source/test files compile.
9. Exact committed artifacts are re-read from GitHub.
10. No protected repository mutation occurs.

## STOP CONDITIONS
Freeze affected work if target identity becomes ambiguous, protected-scope mutation is required, tests cannot be made green without weakening requirements, or evidence cannot be persisted/read back.

## Truth Boundary
Passing this lab proves only the isolated reference implementation. It does not prove NEXY runtime integration, production security, user benefit, deployment readiness, or Canon eligibility.
