# Task Contract — NEXY Orthogonal Work Admission Engine

## OBJECTIVE
Create and verify a standalone future-concept reference implementation that can be integrated with NEXY workflows to detect exact/structural duplication and quantify orthogonality before expensive multi-agent work begins.

## TARGET
`คลังข้อมูลเสริม/CHAT-20261005-0138-NEXY-ORTHOGONAL-WORK-ADMISSION` in `goif74945-crypto/AI-CONTEXT`.

## AUTHORITY SOURCES
1. Current user directive in this conversation.
2. `AI-EXECUTION-KERNEL.md`.
3. `rules/GLOBAL.md`, `rules/AI-BEHAVIOR.md`, `rules/SECURITY.md`, `rules/VERIFICATION.md`.
4. `projects/NEXY.AI/overview.md`.
5. `projects/NEXY.AI/source-normalization/CURRENT-SYSTEM-FEATURE-BUILD-MATRIX.md`.
6. Relevant NEXY deep context, used only as design alignment, not implementation proof.

## AUTHORIZED_SCOPE
- Read AI-CONTEXT and NEXY context as needed.
- Create files only under this project directory in AI-CONTEXT.
- Run code/tests in an isolated local container.
- Store design, code, fixtures, tests, and evidence under this project directory.

## PROTECTED_SCOPE
- Every repository whose name contains `NEXY.AI`: NO WRITE / NO DELETE / NO BRANCH / NO COMMIT / NO PR / NO SETTINGS / NO WORKFLOW MUTATION.
- Existing files elsewhere in AI-CONTEXT: no modification unless strictly required; current plan requires none.
- Secrets/credentials: never persist.

## PRECONDITIONS
- AI-CONTEXT writable: observed through connected GitHub capability.
- Project directory name is unique at planning time.
- Node.js and TypeScript compiler are available locally for verification.

## SUCCESS_INVARIANTS
- Deterministic canonicalization and fingerprinting.
- Exact duplicate => `COLLISION`.
- High structural overlap => `COLLISION` or fail-closed review state according to locked thresholds.
- Materially distinct work => `ALLOW` only when required novelty criteria are met.
- Missing/invalid data => `INVALID`, never optimistic admission.
- No floating point in canonical scoring.
- Stable ordering independent of input array/path order.
- Result contains reason codes and catalog snapshot hash.
- CLI and library share the same engine implementation.
- No NEXY.AI repository mutation.

## REQUIRED_EVIDENCE
- E0: files present.
- E1: `tsc --noEmit` or equivalent successful compile/static check.
- E2: executed unit tests for canonicalization, scoring, exact duplicate, overlap thresholds, invalid input, ordering, and deterministic replay.
- E3: executed CLI integration scenario against fixture catalog.
- Negative tests: malformed input, duplicate IDs, symlink catalog entry, oversized manifest/catalog constraints where implemented.

## STOP_CONDITIONS
- Any required mutation would leave this project directory or enter a NEXY.AI repository.
- Current source authority materially conflicts with this concept.
- Required test evidence cannot be produced.
- Repository drift creates a path collision for the project directory.

## DELIVERABLES
- README
- session memory/checkpoints
- source-alignment note
- architecture/spec
- requirement ledger
- JSON schemas
- TypeScript source
- CLI
- fixtures
- tests
- test/evidence records
- final audit
- AI-proposed future concepts/extension backlog

## OUT OF SCOPE
- Integrating code into the NEXY.AI implementation repository.
- Deploying to production.
- Claiming current NEXY compliance.
- LLM semantic embeddings or nondeterministic similarity.
- Network calls during admission.
- Automatic deletion/merging of other chats' work.
