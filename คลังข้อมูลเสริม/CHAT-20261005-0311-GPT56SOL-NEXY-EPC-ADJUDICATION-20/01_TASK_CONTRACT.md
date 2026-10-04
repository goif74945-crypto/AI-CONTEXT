# Task Contract — EPC Verified Adjudication Calculus 20

## OBJECTIVE
Produce a standalone, deterministic, evidence-gated EPC adjudication package with exactly 20 distinct Lo4 mechanisms that extends rather than duplicates Proposal Forge, can later be adapted to NEXY, and cannot acquire NEXY authority by itself.

## REQUIRED OUTPUT
Design + source + tests + exact execution evidence + hashes + integration contract + vote schema/eligibility record + final audit, all stored in the unique AI-CONTEXT namespace for this chat.

## INPUTS / AUTHORITY
1. Current user directive and EPC vote law.
2. NEXY-IGNIS canonical source identity and source-normalized context.
3. DOC-B/DOC-C authority interpretation in AI-CONTEXT.
4. Exact read-only NEXY.AI repository state used for compatibility evidence.
5. AI-CONTEXT execution/security/verification rules.
6. Existing supplemental systems only as collision/evolution evidence.

## ACCEPTANCE CRITERIA
- Exactly 20 named mechanisms, each with purpose, authority boundary, I/O, failure semantics, and integration mapping.
- Checked signed Q64.64 implementation with explicit i128-range checks and fail-closed overflow/divide-by-zero.
- No IEEE-754 values in authoritative decision structures or calculations.
- Hard gates non-compensatory.
- Deterministic canonical serialization/hash/replay behavior.
- Executable one-KEEP/one-CUT entitlement rule; DEFER/WIP does not spend rights.
- WIP/UNKNOWN cannot produce CUT.
- CUT disposition is non-destructive.
- Court cannot create a NEXY state transition, release token, Canon mutation, or promotion mutation.
- Tests cover malformed evidence, stale anchors, duplicate/correlated evidence, contradictions, unresolved rebuttals, vote replay/double-spend, Q64 boundaries, overflow, divide-by-zero, canonical order, determinism, CUT/WIP prohibition, non-override, and persistence invariants.
- Full TypeScript typecheck passes under strict compiler settings.
- Full local test suite passes against the exact persisted/tested source set.
- Source manifest hashes exact tested files.
- GitHub read-back confirms persisted text equals tested text for all published files or records an exact limitation.
- Protected NEXY.AI repository mutation count by this mission remains zero.

## FORBIDDEN
- NEXY.AI mutation of any kind.
- Automatic promotion or state mutation.
- Hidden randomness/time/network/filesystem order in adjudication.
- Float decision math.
- Lowering tests/requirements to obtain green status.
- Claiming runtime/deployment integration from standalone tests.
- Consuming KEEP/CUT vote rights without user-law evidence requirements.

## REQUIRED EVIDENCE
E0 persisted artifact presence; E1 strict TypeScript compile/static scans; E2 unit/property/negative/replay tests; E3 standalone package integration flow. NEXY runtime integration/deployment remains NOT_VERIFIED unless separately executed under explicit authority.
