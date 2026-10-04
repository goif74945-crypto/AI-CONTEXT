# Task Contract

## OBJECTIVE
Produce five AI-proposed systems that are useful to NEXY.AI, materially distinct from existing supplemental work, implemented as deterministic reference code, tested, and stored only in AI-CONTEXT.

## REQUIRED OUTPUT
For each concept: DESIGN, runnable reference implementation, unit tests, evidence record. For the workstream: collision audit, session memory, final audit, manifest.

## INPUTS / AUTHORITY
1. Current user directive.
2. AI-CONTEXT `AI-EXECUTION-KERNEL.md`, `INDEX.md`, `WORK-ROUTER.md`.
3. NEXY.AI `overview.md` and current normalized 837-row matrix boundaries.
4. Current contents of `คลังข้อมูลเสริม` for collision avoidance.

## CONSTRAINTS
- Do not mutate any repository whose name contains `NEXY.AI`.
- Everything here is `AI_PROPOSAL / NON_GOVERNING` unless authoritative sources separately promote it.
- Standard-library-only Python reference implementations.
- Fail closed on malformed or ambiguous critical state.
- Do not claim deployment, integration, or production security.

## ACCEPTANCE CRITERIA
- Five distinct concepts exist.
- Each has architecture/invariants/failure model/integration boundary.
- Each has executable tests with positive and negative paths.
- All tests pass in a clean local Python run.
- Evidence files contain command + observed result.
- Final repository write touches only the authorized AI-CONTEXT path.

## STOP CONDITIONS
Stop and mark BLOCKED if target repository identity changes, protected scope would be touched, or writes cannot be verified.
