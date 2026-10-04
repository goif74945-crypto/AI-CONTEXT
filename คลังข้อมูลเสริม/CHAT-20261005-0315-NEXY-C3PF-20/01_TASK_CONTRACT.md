# TASK CONTRACT — C3PF-20

## OBJECTIVE
Create a production-grade isolated Lo4 reference laboratory named **NEXY Context Conservation & Compaction Proof Fabric (C3PF-20)** containing exactly 20 executable mechanisms that determine whether a compacted/summarized context preserves the decision-critical semantics of its source context.

## REQUIRED OUTPUT
- Exactly 20 implemented mechanisms matching the frozen mechanism list in `00_TEMP_EXECUTION_MEMORY.md`.
- Deterministic canonical serialization and SHA-256 proof capsules.
- Signed-128 Q64.64 arithmetic implemented with BigInt only; no IEEE-754 decision arithmetic.
- Fail-closed overflow/division behavior.
- Normal, edge, adverse, overflow, determinism, repeated-compaction, shard-reunion, and mutation tests.
- Design document, integration contract, test evidence, manifest, and final audit.
- Append-only EPC vote record only after evidence is sufficient.
- No mutation of any repository whose name contains `NEXY.AI`.

## INPUTS / AUTHORITY
1. Current user directive.
2. Canon source `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx` and extracted Canon corpus.
3. Current `goif74945-crypto/AI-CONTEXT`.
4. Current read-only `goif74945-crypto/NEXY.AI-`.
5. Executed local test evidence generated from exact source bytes before publication.

## IN SCOPE
Only additive files under:
- `คลังข้อมูลเสริม/CHAT-20261005-0315-NEXY-C3PF-20/**`
- one unique append-only vote record under `คลังข้อมูลเสริม/VOTES/**` if KEEP or CUT is actually consumed.

## OUT OF SCOPE
- Editing/deleting/renaming/branching/committing to `NEXY.AI-` or any repository containing `NEXY.AI`.
- Replacing NEXY memory, CIRL, Context Sharding, Core, JUDGE, SWARM, VERIFY, or Canon.
- Production deployment.
- Automatic promotion.
- Claims that isolated tests establish production integration.

## IMMUTABLE RULES
- Lo4 output is proposal-only and non-canonical.
- CORE/JUDGE/LAW remain authoritative.
- AGENT proposes; SWARM debates; VERIFY validates; CORE decides.
- Human/auxiliary layers may not alter Core state or bypass verification.
- UNKNOWN/WIP/INSUFFICIENT_EVIDENCE cannot justify CUT.
- CUT is logical disposition only, not physical deletion.
- Vote scores cannot override Canon/LAW/JUDGE.
- Each CHAT_ID may consume KEEP once and CUT once for its lifetime.
- Existing vote records are append-only; corrections require revision/evidence records.
- A compaction proof must fail closed when a source obligation, authority rule, negative requirement, unresolved unknown, contradiction, evidence binding, or required continuation item is absent or materially weakened.
- Additions not grounded in source context are classified as hallucinated additions unless explicitly marked as proposal/non-authoritative.
- Q64.64 values use raw signed i128-compatible BigInt carriers. Overflow is an error, never saturation in this lab.
- Deterministic functions may not depend on wall clock, random number generators, object insertion order, locale, or floating-point math.

## ACCEPTANCE CRITERIA
- TypeScript static compilation PASS.
- Full executed test suite PASS after final source bytes.
- Repeated proof runs over identical inputs produce byte-identical canonical reports and identical hashes.
- 20/20 mechanisms have positive and adverse/edge test coverage.
- Multi-hop compaction can detect accumulated loss even when each individual hop loses only a small item.
- Shard reunion detects missing and duplicated anchors.
- Hallucinated additions are distinguishable from source-preserved claims.
- Q64.64 overflow/divide-by-zero tests fail closed.
- Published AI-CONTEXT source bytes are read back and hashes match the local tested manifest.
- Final audit records exact NEXY and AI-CONTEXT SHAs and known limitations.
- Zero writes to NEXY repositories.

## FAILURE CONDITIONS
- Any protected-repo mutation.
- Any silent requirement weakening.
- Any ungrounded Canon claim.
- Any binary floating-point value that affects a verdict.
- Any nondeterministic proof result.
- Any test failure.
- Any published/tested byte mismatch.
- Any vote performed before evidence reaches VERIFIED state.

## STOP CONDITIONS
Freeze publication or vote if:
- Canon/NEXY authority semantics conflict with the design.
- Current NEXY head materially changes the integration assumptions and cannot be re-audited.
- Source/test byte identity cannot be proven.
- A semantic collision shows C3PF is merely duplicating an existing stronger system.

## QUALITY GATE
[ ] Design frozen
[ ] 20 mechanisms implemented
[ ] E1 static compile PASS
[ ] E2 tests PASS
[ ] Determinism PASS
[ ] Overflow/fail-closed PASS
[ ] Multi-hop PASS
[ ] Shard reunion PASS
[ ] Collision audit PASS
[ ] Publication readback PASS
[ ] Vote evidence sufficient
