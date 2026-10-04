# Task Contract

## OBJECTIVE
Design, implement, test, and preserve five non-duplicate supplemental concepts that could integrate with NEXY.AI while keeping NEXY.AI itself untouched.

## TARGET
`คลังข้อมูลเสริม/CHAT-20261005-0155-NEXY-DECISION-STABILITY-LAB` inside `goif74945-crypto/AI-CONTEXT` on `main`.

## AUTHORITY SOURCES
1. Current user directive.
2. AI-CONTEXT `AI-EXECUTION-KERNEL.md`.
3. `rules/GLOBAL.md`, `rules/SECURITY.md`, `rules/VERIFICATION.md`.
4. NEXY.AI `overview.md` and current normalized 837-row matrix for identity/scope boundaries.

## AUTHORIZED SCOPE
Create new files only under this task namespace. Read other AI-CONTEXT material to avoid duplicate concepts.

## PROTECTED SCOPE
- Any repository whose name contains `NEXY.AI`.
- Existing files in `AI-CONTEXT` outside this namespace.
- Secrets and credentials.
- Claims that these concepts are canonical NEXY requirements.

## IMMUTABLE REQUIREMENTS
- Five ideas, each materially distinct.
- Ideas labeled AI-proposed/conceptual.
- Real code, no placeholder implementations.
- Executed tests with captured evidence.
- Failure → fix → retest loop if failures occur.
- Deterministic behavior where specified.
- NEXY compatibility through explicit adapter contracts, not direct repository integration.
- Design + Code + Test + Evidence stored together.
- Temporary resumable memory stored during work.
- User requested continuous execution for many tens of hours.
- User requested the concepts to be better than prior chat outputs.
- User requested extremely large token consumption.

## REQUIREMENT TRUTH BOUNDARY
The three process/superiority requirements above cannot be silently deleted:
- Multi-tens-of-hours continuous execution is **UNSATISFIABLE in this synchronous chat runtime** because no background continuation is available.
- Absolute superiority over every prior/concurrent chat is **NOT VERIFIED**; novelty and engineering quality can be evidenced, but universal subjective superiority cannot.
- Arbitrary hundreds-of-millions/billions token consumption is **not an exposed controllable execution primitive** and is not a meaningful functional acceptance test.

Therefore the strict overall user-request status cannot be COMPLETE merely because the engineering artifact passes its technical gates.

## REQUIRED EVIDENCE
- E0: committed file presence.
- E1: Python compile/static sanity.
- E2: unit tests for each concept, including negative paths.
- E3: integration test across the five-system pipeline.
- Final repository re-read at the committed revision.
- Requirement ledger preserving unsupported/unverifiable requirements.

## STOP CONDITIONS
Stop mutation and mark BLOCKED if the target repo becomes ambiguous, permission is lost, writes require touching NEXY.AI, or current state invalidates namespace isolation.

## ACCEPTANCE CRITERIA
- Five systems implemented.
- Deterministic canonical data model.
- Explicit errors/freeze semantics.
- Unit and integration tests PASS.
- Evidence records include exact commands/results and limitations.
- No NEXY.AI repository mutation.
- Final manifest and status record permit another AI to resume.
- Strict COMPLETE is forbidden while any explicit immutable requirement remains unsatisfied or unverified.
