# Task Contract

## OBJECTIVE
Design and implement 20 novel, deterministic, Q64.64-based Lo4 information-acquisition systems useful to NEXY, with code, tests and evidence, while never mutating any repository whose name contains `NEXY.AI`.

## REQUIRED OUTPUT
- 20 implemented concepts.
- Checked Q64.64 substrate.
- Design, code, tests, evidence and failure history.
- NEXY compatibility analysis based on read-only source inspection.
- Temporary execution memory.
- EPC-compatible candidate record, without automatic Canon promotion.

## INPUT / AUTHORITY
1. User instruction in this chat.
2. Authoritative source document: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา(20260929-184432).docx`.
3. AI-CONTEXT retrieval snapshot: `REFERENCES/NEXY/2026-10-04/04-NEXY-IGNIS-source.txt`.
4. Read-only NEXY source at inspected revision `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.
5. Existing AI-CONTEXT Lo4 work used for semantic collision avoidance.

## IMMUTABLE REQUIREMENTS
- Never write to `goif74945-crypto/NEXY.AI-`.
- Lo4 cannot override Canon/LAW/JUDGE/CORE.
- AI output is proposal-only.
- Q64.64 is authoritative numeric representation.
- No binary floating-point in authoritative computation.
- Deterministic ordering/ties; no clocks, randomness or locale semantics.
- Fail closed on invalid schema, overflow, impossible ratio or authority escalation.
- No completion claim without evidence.

## IN SCOPE
Standalone reference implementation, tests, deterministic example, build definition, static audit, evidence, integration proposal, EPC evaluation metadata.

## OUT OF SCOPE
NEXY runtime integration, deployment, migration, production release, Canon changes, LAW changes, JUDGE changes, CORE state changes, UI changes, database changes.

## ACCEPTANCE CRITERIA
- All 20 concepts have executable implementation surfaces.
- Strict GCC build passes with warnings-as-errors.
- Clang ASan/UBSan run passes.
- Tests cover all concepts plus arithmetic, determinism and authority boundaries.
- Replay output is byte deterministic across repeated runs and inspected compilers.
- Static audit rejects float/clock/random/locale/authority-escalation API patterns.
- All known failures are recorded and reverified.
- Package never claims NEXY integration or Canon promotion.

## STOP CONDITIONS
Stop and report NOT VERIFIED rather than guess if authoritative source identity, target revision, verification result or promotion authority is unavailable.
