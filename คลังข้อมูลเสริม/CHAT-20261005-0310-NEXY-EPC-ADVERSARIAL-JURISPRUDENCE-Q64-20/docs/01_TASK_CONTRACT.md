# Task Contract

## OBJECTIVE
Build a reusable Lo4 EPC adversarial-procedure reference implementation with exactly twenty distinct mechanisms, deterministic Q64.64 quantitative policy, strong negative paths, and a NEXY-compatible review-only adapter.

## AUTHORIZED_SCOPE
- Read current NEXY source and source snapshots for compatibility evidence.
- Read current AI-CONTEXT and neighboring Lo4/EPC work for semantic collision checks.
- Build/test locally in an isolated workspace.
- Write only a new additive namespace under `AI-CONTEXT/คลังข้อมูลเสริม/`.

## PROTECTED_SCOPE
- Any mutation of any repository whose name contains `NEXY.AI`.
- Canon, LAW, Core state, JUDGE state, SWARM-owned state, production/runtime state.
- Other chats' work namespaces.
- Credentials/secrets.

## IMMUTABLE_REQUIREMENTS
1. Exactly twenty court organs.
2. Lo4 advisory status only.
3. Q64.64 bigint for authoritative numeric metrics; no IEEE-754 decision scoring.
4. Deterministic semantic canonicalization independent of input ordering/presentation metadata.
5. External policy authority for burdens/thresholds.
6. Fail closed on malformed identities, impossible causal order, invalid policy, forbidden archive deletion, and authority-boundary violation.
7. CUT semantics are reversible archive/reject/supersede, not physical deletion.
8. WIP/UNKNOWN/INSUFFICIENT_EVIDENCE are never transformed into destructive CUT justification.
9. No automatic promotion or Canon/Core mutation.
10. NEXY adapter emits `REVIEW_ONLY` for `EXTERNAL_JUDGE` review.
11. Real compilation/tests/replay/package evidence required before a verified local-reference claim.
12. KEEP/CUT vote rounds must not be consumed unless all vote preconditions are actually evidenced.

## ACCEPTANCE_CRITERIA
- 20 named mechanisms map to executable functions.
- strict TypeScript build succeeds;
- no-float/random/wall-clock authoritative-source gate succeeds;
- positive, negative, adversarial and deterministic replay tests pass;
- NEXY adapter refuses unpinned target/spec identities and cannot encode mutation authority;
- evidence/logs and source hashes preserved;
- protected NEXY repo mutation count from this task remains zero.
