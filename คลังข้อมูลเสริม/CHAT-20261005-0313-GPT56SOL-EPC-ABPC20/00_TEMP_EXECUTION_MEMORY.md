# TEMP EXECUTION MEMORY — NEXY EPC Atomic Ballot Publication & Concurrency Fabric 20

CHAT_ID: CHAT-20261005-0313-GPT56SOL-EPC-ABPC20
PLATFORM_NATIVE_CHAT_ID: UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS
STATUS: IN_PROGRESS
AUTHORITY_CLASS: Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING
START_CONTEXT_LOCAL: 2026-10-05T03:13:00+07:00

## OBJECTIVE
Design, implement, execute, repair, re-test, and preserve exactly 20 deterministic systems that make concurrent EPC proposal/vote publication safe under a shared Git-backed AI-CONTEXT ledger. Prevent vote-right double spending, stale-head publication, partial evidence publication, ballot rewriting, namespace collision, and race-dependent outcomes while remaining advisory and incapable of mutating NEXY.AI or Canon.

## SCOPE LOCK
WRITABLE:
- goif74945-crypto/AI-CONTEXT branch main
- ONLY คลังข้อมูลเสริม/CHAT-20261005-0313-GPT56SOL-EPC-ABPC20/**
- append-only คลังข้อมูลเสริม/VOTES/** only when justified by EPC vote law

PROTECTED READ-ONLY:
- every repository whose name contains NEXY.AI
- goif74945-crypto/NEXY.AI- branch NEXY.ai
- exact inspected commit 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43

FORBIDDEN:
- any NEXY.AI mutation
- Canon/LAW/CORE/JUDGE state mutation
- SWARM/AI/Human authority escalation
- auto-promotion
- physical deletion as CUT
- editing another chat namespace
- rewriting historical ballots
- last-writer-wins court decisions
- floating-point authoritative math
- random/wall-clock-dependent decision logic
- unverified completion claims

## AUTHORITATIVE INPUT PINS
SPEC_ID: แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx
SPEC_SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SPEC_EXTRACT: REFERENCES/NEXY/2026-10-04/04-NEXY-IGNIS-source.txt
SPEC_EXTRACT_GIT_BLOB_SHA: 30b0c179670a836af61923b4b85ae89f3a40d8dc
NORMALIZED_REQUIREMENT_ROWS: 837
NEXY_COMMIT_SHA: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
NEXY_FIXED128_BLOB_SHA: e0e1d4b3fa47d40ac9b30ae14ea8b7ae0ac58313
NEXY_VNEXT_STATE_MATRIX_BLOB_SHA: 27e1281fba330784cc3bf2c30e9e1e82f951479b
NEXY_DIALOG_SANDBOX_BLOB_SHA: 39e508783c23120dc0daa6ffe4db2c181137daf2

## VERIFIED AUTHORITY FACTS
- SWARM is labor/debate, not final authority.
- verified/accepted/rejected product-level events are JUDGE-owned in inspected NEXY code.
- Human/auxiliary layers may not mutate Core state or bypass verification.
- authoritative numeric logic uses signed Q64.64/fixed128 semantics with fail-closed boundaries.
- lower layers cannot override Canon/LAW.
- EPC remains advisory until external formal promotion.

## USER EPC VOTE LAW
- one CHAT_ID may consume KEEP once total and CUT once total
- old vote result immutable; revision evidence does not renew entitlement
- Spec + real NEXY code + current AI-CONTEXT required before voting
- UNKNOWN/WIP/INSUFFICIENT_EVIDENCE cannot justify CUT
- duplicate claims require semantic evidence
- CUT = archive/rejected/superseded, never physical deletion
- scores/votes cannot override Canon/LAW or auto-promote

## COLLISION BOUNDARY
Concurrent EPC work already covers adjudication, vote semantics, causal proof, ecology, jurisprudence, due process, falsification/replication, mutation/counterexamples, interop, phase-boundary analysis, active evidence acquisition, and temporal proof.
Older generic concurrency work covers bounded schedule confluence and generic side-effect transaction planning.
ABPC20 is narrowly different: shared Git-backed EPC publication transactionality, one-time ballot entitlement isolation, evidence-snapshot pinning, and race-safe central VOTES semantics.

## FROZEN 20-SYSTEM SURFACE
01 Head Snapshot Binder
02 Compare-and-Swap Publish Gate
03 CHAT_ID Namespace Lease Validator
04 KEEP Entitlement Single-Spend Guard
05 CUT Entitlement Single-Spend Guard
06 Cross-Round Independence Guard
07 Ballot Identity Canonicalizer
08 Append-Only Ballot Immutability Guard
09 Evidence Snapshot Pin Binder
10 Candidate Artifact Atomicity Checker
11 Vote/Artifact Two-Phase Publish Planner
12 Stale-Head Rebase Safety Classifier
13 Concurrent Duplicate Ballot Detector
14 ABA Revision Epoch Guard
15 Idempotency Receipt Compiler
16 Partial-Publication Recovery Planner
17 Cross-Chat Write-Set Isolation Auditor
18 Deterministic Conflict Freeze Resolver
19 Q64 Contention/Conflict Risk Envelope
20 Atomic Publication Qualification Gate

## NUMERIC LAW
All quantitative advisory metrics use checked signed Q64.64 in a signed-i128 domain. No binary floating point. Overflow/range/division errors fail closed. Scores never grant authority or consume vote rights.

## EXECUTION LOOP
INSPECT -> LOCK -> IMPLEMENT -> FORMAT -> COMPILE -> UNIT -> PROPERTY -> INTERLEAVING -> NEGATIVE -> DETERMINISM -> HASH -> PUBLISH -> READBACK -> VOTE-EVALUATE -> FINAL AUDIT

## CURRENT STATE
COMPLETED:
- AI-CONTEXT and active EPC corpus inspected
- NEXY/spec compatibility inspected read-only
- collision scan completed
- ABPC20 axis and 20-system surface frozen

IN_PROGRESS:
- standalone Rust implementation and test corpus

BLOCKED:
- none

NEXT:
- build isolated Rust crate
- execute/fix/retest
- publish exact tested bytes and evidence
- GitHub read-back + hash comparison
- KEEP only if evidence sufficient; CUT remains unused absent evidence

VERIFICATION_STATUS:
- grounding PASS
- NEXY write actions NONE
- implementation NOT_VERIFIED
- publication THIS CHECKPOINT ONLY
