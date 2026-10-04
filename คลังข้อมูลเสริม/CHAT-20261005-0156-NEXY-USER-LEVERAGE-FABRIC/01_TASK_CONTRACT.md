# Task Contract — NEXY User Leverage Fabric

## OBJECTIVE

Create five non-duplicative, high-value, executable supplemental concepts that could later work with NEXY.AI while keeping NEXY.AI itself untouched.

## AUTHORITY

1. Explicit current user directive.
2. AI-CONTEXT `AI-EXECUTION-KERNEL.md`.
3. AI-CONTEXT global/security/verification rules.
4. Current NEXY project context in AI-CONTEXT.
5. This lab's AI-authored design, only where it does not conflict with higher authority.

## IN SCOPE

- create new artifacts only under this lab directory;
- design five distinct concepts;
- implement executable deterministic reference code;
- run static/unit/integration-style local verification;
- preserve design, code, tests, evidence and resumable state;
- document how each concept could integrate with NEXY without claiming that integration exists.

## OUT OF SCOPE / PROTECTED

- any mutation to a repository whose name contains `NEXY.AI`;
- modification, rename, deletion or consolidation of sibling supplemental projects;
- promotion of these concepts into the current 837-row NEXY build matrix;
- production deployment;
- hidden network/model dependency in verdict paths;
- secrets or credentials;
- claiming user adoption or real-world benefit without evidence.

## IMMUTABLE REQUIREMENTS

- Missing material inputs fail closed.
- Deterministic semantics must produce stable structural results.
- A result may not grant authority it does not own.
- No engine may auto-execute NEXY actions.
- No engine may rewrite canonical NEXY truth.
- Protected repository scope is never mutated.
- Local PASS claims require executed evidence.
- Proposed product value remains a hypothesis until measured.

## ACCEPTANCE CRITERIA

1. Five clearly distinct responsibilities are defined.
2. Each responsibility has executable code, positive tests and negative-path tests.
3. Static compilation succeeds.
4. All tests pass after final code changes.
5. A single demo exercises all five engines.
6. Deterministic replay produces byte-identical demo output.
7. Novelty audit explains overlap boundaries against relevant existing supplemental projects.
8. Repository persistence is read-back verified.
9. No NEXY.AI mutation occurs.

## REQUIRED EVIDENCE

- E0: files exist in the authorized AI-CONTEXT path and can be fetched back.
- E1: Python compile/static import evidence.
- E2: executed test suite.
- E3-local: one package-level demo invoking all five engines; this is not NEXY integration.
- E3+ NEXY runtime integration: `NOT_VERIFIED`.

## STOP CONDITIONS

Freeze affected work if target identity changes, target path collides, protected mutation becomes necessary, tests remain failing, or repository persistence cannot be verified.
