# TASK CONTRACT — ECPC-20

## OBJECTIVE
Create and verify an isolated Lo4 reference system named **NEXY Evolution Compatibility Proof Compiler (ECPC-20)** with exactly 20 executable concepts/modules that make future NEXY schema/API/event/WAL/evidence contract evolution safer without granting AI authority over Canon.

## REQUIRED OUTPUT
- 20 designed + implemented + executed modules.
- Signed-128 carrier / Q64.64 checked arithmetic with no IEEE-754 decision path.
- Deterministic canonical serialization/hashing.
- Tests including normal, edge, negative, overflow, determinism, and cross-version cases.
- NEXY read-only integration contract.
- Evidence bundle + hash manifest.
- EPC vote governance/validation files.
- Durable execution memory.

## INPUTS / AUTHORITY
1. Current user directive.
2. NEXY canonical source law/build hierarchy captured in AI-CONTEXT.
3. AI-CONTEXT execution/security/verification rules.
4. Read-only current NEXY.AI- repository state.
5. Existing AI-CONTEXT supplemental work for semantic collision detection.

## IN SCOPE
Only new files under:
- `คลังข้อมูลเสริม/CHAT-20261005-0310-NEXY-LO4-EVOLUTION-COMPAT-Q64-20/**`
- `คลังข้อมูลเสริม/VOTES/**` for this task's EPC framework/records.

## OUT OF SCOPE / PROTECTED
- Any mutation to `goif74945-crypto/NEXY.AI-` or any repository whose name contains `NEXY.AI`.
- Canon/DOC-B/DOC-C promotion.
- Production deployment.
- Claims that isolated tests prove NEXY integration/runtime/deployment.

## IMMUTABLE REQUIREMENTS
- Lo4 proposals have zero Canon authority.
- CORE/JUDGE remain final authority.
- SWARM/AI/Human auxiliary proposal layers may not directly change Core state or bypass verification.
- Q64.64 authoritative calculations use BigInt fixed-point; binary floating point is forbidden for decisions.
- Signed i128 output range is checked. Overflow/invalid arithmetic fails closed in this lab.
- UNKNOWN/WIP/INSUFFICIENT_EVIDENCE is never sufficient CUT rationale.
- CUT means archive/reject/supersede, not physical deletion.
- Vote score cannot override Canon/LAW/JUDGE.
- One CHAT_ID may consume KEEP once and CUT once for its entire lifetime.
- Existing vote records are append-only; correction uses revision/evidence, never retroactive rewrite.

## ACCEPTANCE CRITERIA
- `tsc --noEmit` or equivalent E1 static proof PASS.
- Full executed test suite E2 PASS after final source bytes.
- Deterministic repeated report bytes/hash match.
- 20/20 modules have at least one positive and one adverse/edge proof path.
- No source file uses numeric literals with decimal/exponent as authoritative Q64 inputs.
- No NEXY repo mutation performed.
- Published AI-CONTEXT bytes are read back and match local manifest or exact expected hash.
- Final audit lists exact limitations and does not call NEXY integration verified.

## STOP CONDITIONS
Freeze publication/promotion if target identity changes, protected repo mutation would be required, unresolved authority conflict would make design illegal, or tested bytes cannot be proven equal to published bytes.
