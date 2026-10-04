# Task Contract

## Objective
Create five increasingly useful Lo4 AI-proposed systems that can integrate conceptually with NEXY.AI without modifying any NEXY.AI repository, implement executable reference code, test it, preserve evidence, and store the complete work under `AI-CONTEXT/คลังข้อมูลเสริม/`.

## Target
- Repository: `goif74945-crypto/AI-CONTEXT`
- Branch: `main`
- Initial HEAD observed before local implementation: `d51b8329fde997d928886baa82c06aaf2994cd77`
- Refreshed pre-publish HEAD after concurrent AI-CONTEXT writes: `f87ec113a1d28d5f3735a1cc9c450d47dab5f9d8`
- Publish rule: preserve concurrent work by building on the newest observed HEAD; never force-update.
- Target folder: `คลังข้อมูลเสริม/CHAT-20261005-0222-NEXY-FORMAL-NOVELTY-5-SOL/`

## Authority sources
1. Current explicit user directive.
2. `AI-EXECUTION-KERNEL.md`.
3. `rules/GLOBAL.md`, `AI-BEHAVIOR.md`, `SECURITY.md`, `VERIFICATION.md`.
4. `projects/NEXY.AI/overview.md` and current 837-row source-normalization boundary.
5. Current AI-CONTEXT repository state.
6. AI proposal/inference.

## Authorized scope
- Read AI-CONTEXT and NEXY context needed for compatibility reasoning.
- Create new files under the target folder only.
- Implement isolated deterministic Python reference prototypes.
- Execute sandbox tests and record evidence.

## Protected scope
- No mutation to any repository whose name contains `NEXY.AI`.
- No edits to existing AI-CONTEXT files outside the new target folder.
- No canonical NEXY promotion.
- No production/deployment mutation.
- No secrets/credentials.

## Success invariants
- Exactly five clearly distinct concepts.
- Every concept labeled AI-proposed/non-canonical.
- Deterministic behavior for identical inputs.
- Explicit failure semantics.
- Negative-path tests included.
- Tests run for real; no simulated PASS claims.
- Final repository write verified by re-read/tree inspection.

## Required evidence
- E0: files exist in AI-CONTEXT at final commit.
- E1: Python compileall success.
- E2: executed unit/negative-path tests.
- Additional stress/determinism checks as supplemental runtime evidence.
- NEXY production integration remains NOT_VERIFIED.

## Stop conditions
- Any write would touch protected scope.
- Baseline branch moved before atomic publish and fast-forward assumptions become unsafe.
- Repository permission missing.
- Contradictory authority requires choosing an unauthorized interpretation.
