# Task Contract

## OBJECTIVE
Build five strong, distinct, executable companion concepts for future NEXY.AI consideration, validate them, and persist Design + Code + Test + Evidence in AI-CONTEXT only.

## REQUIRED OUTPUT
1. Five concept designs.
2. Reference code for all five.
3. Tests including negative/adversarial behavior.
4. Evidence record.
5. NEXY.AI compatibility audit based on read-only current repository inspection.
6. Temporary/durable session memory.

## AUTHORIZED_SCOPE
`goif74945-crypto/AI-CONTEXT` only, under `คลังข้อมูลเสริม/NCAF-20261005-0154-TH-01/`.

## PROTECTED_SCOPE
Any repository with `NEXY.AI` in its name. Read-only inspection is permitted. Mutation is forbidden.

## IMMUTABLE REQUIREMENTS
- Do not silently reduce requirements.
- Do not claim canonical adoption.
- Fail closed on invalid contract inputs.
- Deterministic behavior for identical inputs.
- No external runtime dependency in reference lab.
- Preserve explicit authority boundaries.
- Produce reproducible evidence.

## ACCEPTANCE CRITERIA
- All five modules have defined purpose, invariants, interfaces, failure semantics, tests, and integration limits.
- Python compilation succeeds.
- Focused + regression tests all pass.
- At least one cross-module smoke path succeeds.
- Negative paths cover malformed/unsafe/conflicting states.
- GitHub write is verified by re-fetching files from AI-CONTEXT.

## STOP CONDITIONS
Stop/mark BLOCKED on repository identity ambiguity, protected-scope mutation requirement, unresolved authority conflict, or inability to verify writes/tests.
