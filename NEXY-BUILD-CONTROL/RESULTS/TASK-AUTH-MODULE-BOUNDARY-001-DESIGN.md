# TASK-AUTH-MODULE-BOUNDARY-001 — Authority-safe design result

CHAT_ID: C-SOL-20261005-1921-V8
TASK_ID: TASK-AUTH-MODULE-BOUNDARY-001
STATUS: DESIGN_COMPLETE / SOURCE_MUTATION_BLOCKED
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SOURCE_TREE_SHA: e7f603d06db6475a4d72f5d0aed752213d17eb16

## FACT

1. FINAL VERDICT assigns DOC-B = SYSTEM LAW, DOC-C = BUILD SPEC, and states build obligation comes from DOC-C only.
2. FINAL_DOC_C_PRIMARY_INDEX pins Final DOC-C to raw paragraphs 9886-10499.
3. The module dependency section named "4.2 Allowed Dependency Shape" is raw paragraph 8525, inside the pre-FINAL execution pack 8095-9829.
4. Final DOC-C section 4.2 is "Route Matrix" at paragraph 10038.
5. Final DOC-B paragraphs 9846-9885 do not contain a module dependency graph.
6. Current integration script scripts/check-module-boundaries.ts is blob 08f19abd16db69646cc0d3fd7e58b1cdc345d677.
7. Implementation commit 1c3ce5d2dd0e305b82c1140e904759f8ea56d6d3 is an ancestor of integration SHA 608426cb30398b1f3461866f7079d2a435c96b96; the boundary script and its routing test blobs remain unchanged.
8. package.json makes check:doc-c execute check:boundaries.
9. deploy.yml executes check:doc-c.
10. e7-queue.yml executes lint, whose package script also executes check:boundaries.
11. exact-head-evidence.yml executes both lint and check:doc-c.

## INVALID ORACLE

The proposition "Final DOC-C §4.2 permits only API->AUTH/API->CORE, therefore API->LAW must fail" is not supported by Final DOC-C. Those edges come from historical paragraph 8525 material.

This does not prove API->LAW is safe. It proves only that the cited Final-DOC-C oracle is invalid.

## SAFE DESIGN

A source repair must not guess the missing authority. The permitted design space is:

A. FINAL-DOC-C gate:
- check:doc-c must report only obligations derived from locked Final DOC-C.
- Historical module edges must not be described or accepted as Final-DOC-C requirements.

B. Boundary hardening gate:
- scripts/check-module-boundaries.ts may remain only if a current non-DOC-C authority or evidence-backed hardening policy explicitly justifies the enforced relation.
- Its required allowed/forbidden set must be derived from that authority, not copied forward merely because the historical pack once contained it.
- If retained as hardening, label evidence and failures accordingly.

C. Test oracle:
- module-boundary-routing tests may prove classifier mechanics such as longest-root mapping.
- They may not claim Final-DOC-C semantic acceptance for an edge set absent from Final DOC-C.
- F-B71C4E8D-01's runtime reproduction remains a valid observation of current checker behavior, but its Final-DOC-C expected result is stale.

D. Gate wiring:
- Do not remove boundary enforcement from all CI as a reflexive repair.
- First decide its valid authority; then wire it under the correct gate name and evidence class.
- Never weaken or widen architecture rules based on inference alone.

## ACCEPTANCE AFTER UNBLOCK

- Locked-primary authority mapping proves every enforced boundary rule has an active source.
- check:doc-c contains no historical-only obligation.
- Focused tests distinguish classifier mechanics from authority semantics.
- Exact candidate SHA/tree executes check:doc-c and any separately authorized hardening gate.
- Review confirms no protected-upstream mutation and no unrelated architecture rewrite.

## BLOCKER

INC-BRANCH-NAMESPACE-001 prevents the mandated worker prefix NEXY.AI-Test-AI/work/<TASK_ID> from coexisting with refs/heads/NEXY.AI-Test-AI. No source mutation is performed by this task until branch policy is authoritatively resolved.
