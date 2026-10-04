# Task Contract

## OBJECTIVE
Build exactly 20 executable Lo4 proposal systems for possible future NEXY Game/NCF integration. All decision-relevant fractional math uses exact signed Q64.64.

## TARGET
Repository: goif74945-crypto/AI-CONTEXT
Mutable path: คลังข้อมูลเสริม/CHAT-20261005-0230-NEXY-LO4-DETERMINISTIC-CREATIVE-WORLD-FABRIC/**

## PROTECTED
- No mutation to any repository whose name contains NEXY.AI.
- No mutation outside this mission folder.
- No Canon promotion.
- No production/deployment claim.
- No secrets.

## IMMUTABLE REQUIREMENTS
- Exactly 20 systems listed in 00_TEMP_MEMORY.md.
- Lo4_AI_PROPOSAL_ONLY status is preserved.
- Float is rejected at authoritative numeric boundaries.
- Equal canonical input yields equal canonical output.
- Inputs are bounded and validated.
- Impossible/unsafe states fail closed.
- No network/model/provider dependency in the reference package.
- Real tests must execute.
- Failures found during verification must be repaired and retested.
- Persist Design + Code + Tests + Evidence.
- Tested bytes must be bound to persisted bytes.

## ACCEPTANCE
E0: required files exist.
E1: compile/static syntax succeeds.
E2: all 20 systems have positive plus negative/boundary coverage and deterministic tests.
E3: at least one cross-fabric scenario passes.
Q64.64 rejects float and checked overflow.
Full regression suite returns zero failures.
Published executable/test files have Git blob SHA equal to locally tested Git blob SHA.
GitHub readback succeeds.

## FAILURE SEMANTICS
Malformed input -> validation error.
Overflow -> Q64 overflow error.
Unsafe/impossible proposal -> explicit rejection/freeze result.
Hard computation bound exceeded -> bounded-computation rejection.
Integration mismatch -> fail closed.
No silent fallback.

## TEST ORDER
1. Write tests.
2. Execute RED against missing package.
3. Implement shared Q64.64 and 20 systems.
4. Focused tests.
5. Negative/boundary tests.
6. Determinism tests.
7. Cross-fabric integration.
8. Full regression.
9. compileall.
10. Hash exact files.
11. Publish exact tested bytes.
12. Read back and compare identities.

## STOP CONDITIONS
Stop if protected scope would need mutation, authority conflicts materially, evidence cannot be produced, or tested/persisted identities diverge.

## PROMOTION LAW
Passing this isolated prototype does not make it NEXY Canon/current build/runtime. Promotion requires separate authorization and fresh integration evidence.
