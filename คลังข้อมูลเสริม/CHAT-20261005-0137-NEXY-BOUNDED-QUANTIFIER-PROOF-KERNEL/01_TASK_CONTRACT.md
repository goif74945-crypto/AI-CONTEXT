# Task Contract — NEXY Bounded Quantifier Proof Kernel

## OBJECTIVE
Design, implement, test, and document an isolated reference kernel that evaluates evidence-backed quantified claims without modifying NEXY.AI.

## AUTHORITY
1. Current user directive.
2. AI-CONTEXT execution kernel and rules.
3. NEXY.AI project context for compatibility principles only.
4. Current files created in this lab.
5. Executed test evidence.

## IN SCOPE
- Pure deterministic claim evaluator.
- Quantifiers: ALL, NONE, EXACTLY, AT_LEAST, AT_MOST.
- Explicit domain provenance and completeness.
- Revision-bound evidence freshness.
- Lower/upper-bound proof calculus for unresolved evidence.
- Fail-closed output for malformed/unproven claims.
- CLI adapter, schemas/examples, unit/integration tests, evidence and integration notes.

## PROTECTED / OUT OF SCOPE
- Any mutation to repositories whose names contain NEXY.AI.
- Any claim that BQPK is already part of NEXY.AI.
- Deployment, production integration, authentication, database, UI, provider orchestration.
- Editing unrelated AI-CONTEXT paths.

## IMMUTABLE REQUIREMENTS
- AI_PROPOSED / NON_AUTHORITATIVE label must remain visible.
- Core evaluator must not use clock, randomness, filesystem, network, database, process state, or environment state.
- Same JSON-compatible input must produce the same structural result.
- Only PASS may emit action RELEASE; every other status emits FREEZE.
- No PASS from search failure, missing evidence, stale evidence, or unbounded universal/exact upper bound.
- Evidence truth itself is outside this kernel; BQPK validates proof shape, coverage, freshness, and quantifier entailment.

## ACCEPTANCE CRITERIA
- Test-first RED observed before production implementation.
- Core tests cover positive, refutation, incomplete, stale, duplicate, extra-member, anti-vacuity, threshold, determinism, and unresolved cases.
- Full local suite passes.
- Python compile/static import check passes.
- CLI JSON-in/JSON-out integration check passes.
- Final files are read back from AI-CONTEXT.
- NEXY.AI protected scope remains untouched by this mission.

## STOP CONDITIONS
- Required work would mutate NEXY.AI.
- Target identity becomes ambiguous.
- AI-CONTEXT write authority disappears.
- Verification cannot distinguish intended behavior from an assumption.
