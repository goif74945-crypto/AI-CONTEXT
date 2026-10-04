# TEMP EXECUTION MEMORY — CTIAF-20

WORK_CODE: CHAT-CTIAF20-GPT56SOL-20261005
PLATFORM_NATIVE_CHAT_ID: UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS
STATUS: IN_PROGRESS
AUTHORITY_CLASS: Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING

## OBJECTIVE
Design, implement, execute, repair, re-test, and preserve exactly 20 deterministic Q64.64-compatible mechanisms under **NEXY Canonical Text & Identifier Ambiguity Firewall (CTIAF-20)**. The lab detects representation ambiguity and spoofing at text/identifier boundaries before data is trusted by future NEXY adapters.

## SCOPE LOCK
WRITABLE TARGET:
- goif74945-crypto/AI-CONTEXT
- branch main
- only path prefix: คลังข้อมูลเสริม/CHAT-CTIAF20-GPT56SOL-20261005/**
- optional unique append-only vote receipt under คลังข้อมูลเสริม/VOTES/** only after evidence sufficiency

PROTECTED / READ-ONLY:
- every repository whose name contains NEXY.AI
- observed repo goif74945-crypto/NEXY.AI-
- branch NEXY.ai
- exact observed head 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43

FORBIDDEN:
- any mutation to NEXY.AI-
- Canon/LAW/Core/JUDGE/SWARM state mutation or automatic promotion
- physical deletion as CUT
- UNKNOWN/WIP as CUT cause
- binary floating point in authoritative CTIAF scoring
- hidden randomness, wall-clock or network dependency in deterministic decisions
- claims of NEXY production integration without matching evidence

## DIRECT SPEC EVIDENCE
SPEC_ID: แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx
SPEC_SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
- p2580: MIXED/AMBIGUOUS -> INVALID.
- p2654+: unclear/conflicting authority freezes rather than guessing.
- p6440: Text normalized (UTF-8 canonical).
- p6441: No locale-dependent formatting.
- p6451-6455: AI output must pass validation and must not inject runtime entropy.
- p7160-7163: INVALID_DIRECTIVE / EMPTY_INPUT / AMBIGUOUS_INPUT error taxonomy.
- p7383-7400: runtime validation mandatory at all external/internal boundaries.
- p8072-8075: queue payload validates before enqueue and consume; invalid payload maps to SCHEMA_VIOLATION and may freeze.

## CURRENT NEXY CODE EVIDENCE
- core-kernel/src/api/payload_parser.rs at 9e615b... is strict binary parser with zero partial accepts and Q64.64 confidence.
- core-kernel/src/engine/fixed128_math.rs uses signed i128 Q64.64 and fail-closed/freeze arithmetic.
- packages/phase-f/universe/capability-declaration.ts exposes bounded capabilities including NETWORK_EGRESS; CTIAF does not replace capability governance.
- packages/phase-f/lo2/refinement.ts uses bigint Q64.64 and experimental-only candidate governance; CTIAF does not replace Lo2/EPC promotion logic.

## COLLISION EXCLUSIONS
Observed existing AI-CONTEXT work already covers privacy egress minimization, provenance/context taint, localization integrity, accessibility integrity, capacity/admission, generic EPC governance, strategyproofness, causal/evidence governance, mutation/counterexample systems, phase boundaries, compatibility, context compaction and human deliberation. Searches for homoglyph/confusable/bidirectional/unicode-security/canonical-text-identifier found no commit hits. This is low-overlap evidence, not proof of global uniqueness.

## FROZEN 20 MECHANISMS
1. UTF Canonical Form Gate
2. Noncharacter & Invalid Scalar Guard
3. Invisible Control Quarantine
4. Bidirectional Control Firewall
5. Zero-Width Mutation Detector
6. Mixed-Script Identifier Gate
7. High-Risk Confusable Skeleton Mapper
8. Visual Identifier Collision Detector
9. Canonical Case-Fold Collision Gate
10. Whitespace Canonicalization Guard
11. Line-Break Canonicalization Guard
12. Percent-Decoding Ambiguity Detector
13. Double-Decoding Guard
14. Path Segment Canonicalizer
15. Dot-Segment Traversal Guard
16. URL Authority Canonicalization Gate
17. JSON Key Canonical Collision Detector
18. Numeric Lexeme to Q64 Canonicalizer
19. Canonical Text Digest Binder
20. Ambiguity Proof Bundle Compiler

## TDD / VERIFICATION LAW
- RED must be observed before production implementation.
- GREEN requires strict TypeScript compile + executed tests.
- Each mechanism requires positive and adverse/edge coverage.
- Deterministic replay must produce byte-identical canonical reports/hashes.
- Q64 overflow/div-by-zero/noncanonical numeric lexemes fail closed.
- No-float/no-random/no-wall-clock source audit.
- Published bytes must be read back and matched before any final PASS.

## VOTE BUDGET
KEEP_REMAINING: 1
CUT_REMAINING: 1
DEFER/WIP/INSUFFICIENT_EVIDENCE: no round consumed
No vote will be cast before exact Spec + NEXY + current AI-CONTEXT evidence and implementation evidence are sufficient.

## NEXT
1. Write failing tests first.
2. Run RED and preserve raw log.
3. Implement Q64 + 20 mechanisms.
4. Compile/test/fix until green.
5. Run adversarial/determinism/property source audits.
6. Produce design/integration/evidence/final audit.
7. Publish only into AI-CONTEXT namespace.
8. Read back exact GitHub bytes and re-verify hashes.
