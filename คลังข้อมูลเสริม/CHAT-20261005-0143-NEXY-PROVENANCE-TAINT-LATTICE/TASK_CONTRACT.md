# TASK CONTRACT

## OBJECTIVE
Create a new, non-duplicative, high-value experimental subsystem for future NEXY.AI compatibility that prevents provenance/authority/evidence laundering across chained AI/tool transformations.

## TARGET
`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0143-NEXY-PROVENANCE-TAINT-LATTICE`

## AUTHORITY SOURCES
1. Current user directive.
2. AI-CONTEXT AI Execution Kernel and global rules.
3. AI-CONTEXT NEXY.AI overview for compatibility principles.
4. Current observed AI-CONTEXT repository state.
5. Executed local test evidence.

## AUTHORIZED SCOPE
- Create new files only under the target folder in AI-CONTEXT.
- Read AI-CONTEXT broadly enough to avoid collision and preserve compatibility.
- Run local isolated tests against the created reference implementation.

## PROTECTED SCOPE
- Any repository whose name contains `NEXY.AI`.
- Existing unrelated AI-CONTEXT supplemental project files.
- Canonical NEXY requirements/specification.

## SUCCESS INVARIANTS
- A derived artifact cannot silently acquire stronger authority/evidence than its lineage proves.
- Unknown/untrusted/conflicted/stale lineage propagates deterministically.
- Verification receipts are bound to exact artifact identity and cannot be replayed on modified artifacts.
- Release decisions are deterministic and return explicit ALLOW or FREEZE with stable reason codes.
- Implementation has no third-party runtime dependency.
- Negative-path tests cover trust laundering, receipt mismatch/replay, unknown origins, conflicts, staleness, and mixed-authority merges.
- Design is explicitly labeled AI-PROPOSED CONCEPT.

## REQUIRED EVIDENCE
- E0: files present in AI-CONTEXT.
- E1: Python compilation/static import succeeds.
- E2: executed unit tests for invariants and negative paths.
- Repository re-read after writes.
- Final evidence record with exact commands and observed results.

## FORBIDDEN ACTIONS
- Mutating NEXY.AI.
- Claiming production deployment/integration.
- Hiding failing tests.
- Adding unrelated project scope.

## STOP CONDITIONS
- Protected-scope mutation would be required.
- Material conflict with current authoritative NEXY law.
- Test failures remain unresolved.
- Repository write verification fails.

## DELIVERABLES
- README
- DESIGN
- REQUIREMENT_LEDGER
- Python package source
- Test suite
- test/evidence log
- resumable execution state
- AI-proposed future integration notes
