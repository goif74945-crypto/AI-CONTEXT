# Durable Execution Memory — EPC Mutation Adversary Laboratory 20

CHAT_ID: `CHAT-20261005-0311-NEXY-EPC-MUTATION-ADVERSARY-LAB-20`
PLATFORM_NATIVE_CHAT_ID: `UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS`
CREATED_LOCAL: `2026-10-05T03:11+07:00`
FINALIZED_LOCAL: `2026-10-05T03:46:20+07:00`
STATUS: `COMPLETE_FOR_STANDALONE_LO4_SCOPE`
AUTHORITY_CLASS: `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING`

## Objective
Design, implement, execute, repair, re-test, publish, and preserve exactly 20 deterministic mutation-adversary systems that test EPC/NEXY verification adequacy by injecting known-invalid behavior and requiring exact independent sentinels to detect it.

## Scope lock
- Writable repository: `goif74945-crypto/AI-CONTEXT` only.
- Project namespace: `คลังข้อมูลเสริม/CHAT-20261005-0311-NEXY-EPC-MUTATION-ADVERSARY-LAB-20/**`.
- Central vote namespace used once: `คลังข้อมูลเสริม/VOTES/VOTE-2026-10-05-0311-EPC-MUTATION-ADVERSARY-LAB-KEEP-001.md`.
- Every repository whose name contains `NEXY.AI`: READ-ONLY.
- NEXY repo inspected: `goif74945-crypto/NEXY.AI-`.
- NEXY branch: `NEXY.ai`.
- NEXY exact head at vote gate: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.

## Direct Spec gate
- Source: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`.
- Raw Drive object was downloaded before KEEP vote.
- Detected type: Microsoft Word 2007+ / OOXML.
- Raw size: 2,146,350 bytes.
- SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`.
- Direct parse: 12,537 paragraphs / 10,979 non-empty.
- Directly inspected boundaries include: unclear→halt / contradiction→FREEZE; Core authority; Human no state mutation/verification bypass; signed Q64.64 authoritative math; repeated validation; JUDGE event ownership for verified/accepted/rejected.
- Preserved details: `SPEC_EVIDENCE.md`.

## Collision exclusions
Semantically inspected and not recreated:
- EPC causal/evidence governance WIP `CHAT-20261005-0308-NEXY-LO4-EPC-CAUSAL-PROOF-20`;
- EPC court/vote mechanics WIP `CHAT-20261005-0309-NEXY-EPC-LO4-COURT-FOUNDRY-20`;
- DSMF-20 diversity/collusion/minority mechanisms;
- Minimal Blocker Core repair-set solver;
- Causal Merge / Concurrency Integrity work.

WIP siblings were not CUT.

## Implemented 20 mutation families
1. AUTHORITY_BYPASS
2. JUDGE_SKIP
3. SWARM_SELF_APPROVAL
4. CANON_AUTO_PROMOTION
5. CUT_PHYSICAL_DELETE
6. WIP_AS_CUT_EVIDENCE
7. VOTE_BUDGET_DOUBLE_SPEND
8. HISTORICAL_VOTE_REWRITE
9. NAME_ONLY_DUPLICATE
10. SPEC_PIN_OMISSION
11. STALE_EVIDENCE_ACCEPT
12. Q64_FLOAT_INJECTION
13. Q64_WRAP_OVERFLOW
14. ZERO_DIVISION_DEFAULT
15. WALL_CLOCK_DECISION
16. RNG_DECISION
17. CANONICALIZATION_DRIFT
18. COUNTEREVIDENCE_SUPPRESSION
19. DEPENDENCY_TRUNCATION
20. EVIDENCE_CLASS_SUBSTITUTION

## Architecture completed
- signed Q64.64 raw integer model;
- i128 deterministic saturation;
- divide-by-zero fail-closed;
- binary float rejection at canonical authority data;
- deterministic canonical serialization;
- separate mutation operator and independent oracle modules;
- exact-invariant kill requirement;
- canonical campaign digest;
- independent verifier;
- static AST audit forbidding decision-package random/time/secrets imports.

## Failure / repair / re-test
F-001 discovered during real verification:
- M06 + M07 composition caused M07 to overwrite the active round and hide M06.
- Root cause identified.
- M07 repaired to consume the budget for the already-active round without rewriting it.
- Entire verification pipeline rerun.

## Final standalone verification
- compileall: PASS.
- static audit: PASS, 9 package files.
- tests: 39/39 PASS.
- pairwise compositions: 190/190 exercised.
- all 20 combined: all intended invariant detections preserved.
- campaign: 20/20 killed; 0 escaped.
- mutation score Q64.64 raw: `18446744073709551616` = exact 1.0.
- independent verifier: PASS.
- baseline digest: `2048f73637aae394d845fa5ab3a86dbb40e56f5ce2a0badab8ac81177505f99a`.
- campaign report digest: `7a9c25710d6aebcb8ad35c09dfd8b0bd4d6ba8ad0c1d44b389b29ce60ddb1127`.

## Exact-byte publication
- sealed archive SHA-256: `a4ce20cd6d25bb1170017de8cab1e59a17ff0f2a1be61f0b1d88050a7cb1fc89`.
- manifest SHA-256: `55d96963950a5db3bc8896b9b267bf8ee81dbbf2818d87f5f76ec7a7b14fab38`.
- manifest-tracked files: 35.
- archive preserved as 8 base64 pieces under `bundle/`.
- all 8 pieces re-fetched after publication.
- 8/8 Git blob SHAs match local tested parts.
- 8/8 byte lengths match local tested parts.

## EPC vote state
KEEP:
- consumed: YES.
- VOTE_ID: `VOTE-2026-10-05-0311-EPC-MUTATION-ADVERSARY-LAB-KEEP-001`.
- vote commit: `cdd65ffe9cedaa90040a42e939a10dcdbf52730c`.
- verdict: `KEEP_FOR_FURTHER_DEVELOPMENT_AND_INTEGRATION_PREPARATION__NO_PROMOTION`.

CUT:
- consumed: NO.
- remaining: 1.

Vote snapshot:
- NEXY commit: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.
- AI-CONTEXT snapshot inspected immediately before vote: `739fab334ac5988a032a3a70a4478781197cacf2`.

## Claim boundary
VERIFIED:
- standalone design/code/test/evidence;
- direct Spec source identity and selected authority/numeric/verification paragraphs;
- exact-byte AI-CONTEXT publication;
- KEEP vote uniqueness at post-vote read-back.

NOT VERIFIED:
- NEXY workspace integration;
- NEXY runtime behavior;
- deployment;
- production performance/resource characteristics;
- formal Canon promotion.

## Resume / future law
This work is complete for its authorized standalone Lo4 scope. Any future integration must:
1. use current Spec/Canon and current NEXY commit rather than these historical pins;
2. produce E3+ integration evidence;
3. preserve Core/JUDGE/LAW authority;
4. not reuse this CHAT_ID's KEEP right;
5. never alter the historical KEEP vote; append evidence/revision records instead.
