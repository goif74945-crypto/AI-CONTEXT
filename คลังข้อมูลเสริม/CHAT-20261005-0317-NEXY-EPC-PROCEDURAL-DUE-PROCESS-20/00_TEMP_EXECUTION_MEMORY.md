# Temporary Execution Memory — NEXY EPC Procedural Due-Process & Severability 20

**Durable work code / CHAT_ID:** `CHAT-20261005-0317-NEXY-EPC-PROCEDURAL-DUE-PROCESS-20`
**Platform-native ChatGPT conversation ID:** `UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS`
**Started:** `2026-10-05T03:17+07:00`
**Status:** `IN_PROGRESS`
**Classification:** `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING`

## Objective
Design, implement, execute, repair, retest, and preserve exactly 20 deterministic Q64.64-compatible **procedural due-process** systems for the proposed NEXY Evolutionary Proposal Court (EPC). This project does not build another vote engine, promotion engine, causal proof engine, proposal forge, integration simulator, mutation forge, or jurisprudence counterexample suite. It focuses on whether an EPC review process itself is fair, explicit, severable, reviewable, and evidence-bound before any authorized external authority considers a vote or promotion.

## Scope lock
WRITABLE:
- `goif74945-crypto/AI-CONTEXT`
- branch `main`
- only `คลังข้อมูลเสริม/CHAT-20261005-0317-NEXY-EPC-PROCEDURAL-DUE-PROCESS-20/**`
- one append-only KEEP receipt under `คลังข้อมูลเสริม/VOTES/**` only after executable evidence is sufficient.

READ-ONLY / PROTECTED:
- every repository whose name contains `NEXY.AI`
- observed implementation repo: `goif74945-crypto/NEXY.AI-`
- branch: `NEXY.ai`
- exact inspected commit: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`

FORBIDDEN:
- any NEXY.AI mutation;
- Canon/Law/Core/JUDGE/SWARM authority escalation;
- automatic promotion;
- physical deletion as CUT semantics;
- WIP/UNKNOWN/INSUFFICIENT_EVIDENCE as sufficient CUT cause;
- binary floating-point in authoritative project metrics;
- hidden wall-clock/random/network/filesystem-order influence;
- retroactive vote rewrite;
- claiming NEXY runtime integration from isolated tests.

## Authoritative evidence pins already inspected
- Canon source bytes retrieved from Drive object titled `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.txt`, whose raw bytes are Microsoft Word OOXML.
- Canon/spec SHA-256 independently computed locally: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`.
- Spec paragraphs 571-584: JUDGE is deterministic final adjudicator; SWARM compares/votes but has no decision authority; CORE/JUDGE hold authority.
- Spec paragraph 2838: AGENT propose only, SWARM debate only, VERIFY validates evidence, CORE decides; Canon writes require CORE approval + verification + version bump.
- Spec paragraphs 9858-9863: CORE may decide/validate/verify/enforce/freeze/kill; LAW may block; JUDGE may evaluate; SWARM may work; Human layer may suggest/warn/guide attention only and may not change Core state.
- Spec paragraph 4273: `FROZEN / READ-ONLY / COURT-EXPORT-ONLY` appears as an explicit consolidated-state mode.
- Spec paragraphs 6770-6775: signed 128-bit fixed point, Q64.64, authoritative math fixed128, no mixed precision in that numeric scope.
- NEXY exact-head `packages/core/vnext-state-matrix.ts`: boot/execute owned by CORE; agents_done by SWARM; verified/accepted/rejected by JUDGE.
- NEXY exact-head `core-kernel/src/engine/fixed128_math.rs`: signed i128 Q64.64 and fail-closed overflow/divide-by-zero via freeze.

## Collision boundary
Concurrent/earlier EPC work already owns:
- causal/evidence governance, vote-right ledger, WIP gate, freshness, promotion readiness, duplicate proof, court dossier;
- generic EPC proposal court/Q64 mechanisms;
- Court Foundry voting mechanics and immutable ballot lineage;
- evolutionary ecology/integration science;
- adversarial integration proof;
- adversarial mutation testing;
- jurisprudence/counterexample generation;
- cross-version refinement/equivalence proof.

Commit-message collision searches returned no observed active project whose primary axis is:
`standing`, `admissibility`, `burden of proof`, `rebuttal`, `dissent`, `recusal`, `severability`, `minimal remedy`, `precedent`, `ex parte`, `reason-giving`, or `estoppel`.
This is bounded repository evidence, not a universal novelty proof.

## Frozen 20-system surface
1. **STAND64 — Proposal Standing Declaration Gate**
2. **ADMIT64 — Evidence Admissibility Contract**
3. **BURDEN64 — Risk-Weighted Proof Burden Scheduler**
4. **NOTICE64 — Material Change Notice Auditor**
5. **OBJECTION64 — Objection Preservation Ledger**
6. **REBUT64 — Rebuttal Sufficiency Matrix**
7. **DISSENT64 — Dissent Capsule Compiler**
8. **RECUSAL64 — Evaluator Conflict/Recusal Advisory Graph**
9. **SEVER64 — Claim Severability Analyzer**
10. **REMEDY64 — Minimal Remedy Scope Compiler**
11. **PARITY64 — Symmetric Evidence-Standard Auditor**
12. **PRECITE64 — Precedent Citation Integrity Checker**
13. **NONBIND64 — Precedent Non-Binding Guard**
14. **APPEAL64 — Evidence-Delta Appeal Gate**
15. **EXPARTE64 — Hidden-Evidence Symmetry Detector**
16. **REASON64 — Reason-Giving Completeness Checker**
17. **SCOPE64 — Defect-to-Disposition Scope Validator**
18. **CONSIST64 — Cross-Revision Position Consistency Auditor**
19. **HEARING64 — Procedural Record Completeness Gate**
20. **DUEPROCESS64 — Non-Governing Procedural Readiness Orchestrator**

## Numeric law
- All quantitative project metrics use signed checked Q64.64.
- Carrier is Python `int` constrained explicitly to signed-i128 range.
- Binary `float` is forbidden in authoritative project paths.
- Overflow, divide-by-zero, malformed ratios, invalid ranges, duplicate IDs, and structurally incomplete critical inputs fail closed with explicit errors.

## Procedural law
- This package may return `PROCEDURALLY_READY`, `DEFER`, or specific advisory defects only.
- It never returns NEXY `accepted`/`rejected`, never emits a Core transition, never promotes.
- Historical EPC vote records remain immutable.
- Prior precedent is informational only and can never override current Spec/Canon/LAW/JUDGE evidence.
- Unresolved critical objections block procedural readiness but do not automatically justify CUT.
- Claim severability is conservative: unknown dependency edges couple claims rather than silently isolating them.
- Global CUT scope requires proof that defects reach the non-severable essential core; localized severable defects are insufficient by themselves.

## Verification plan
E1 — Python compile/static AST checks:
- compileall
- AST scan forbidding `float` calls and float literals in court core
- deterministic ordering audit

E2 — executable tests:
- unit tests for Q64.64
- positive + adverse tests for all 20 systems
- boundary/overflow/divide-by-zero tests
- randomized-but-seeded integer property checks where deterministic seed is explicit and test-only

E3 — integration/determinism:
- full synthetic hearing flow
- repeated canonical report byte equality
- subprocess test from clean extracted package
- exact tested-byte SHA-256 manifest

## Vote budget
KEEP remaining: 1
CUT remaining: 1
DEFER/WIP: unlimited and non-consuming.
No round is consumed until Spec + NEXY code + current AI-CONTEXT + Design + Code + Test + Evidence are sufficient.

## Current state
COMPLETED:
- Canon/spec raw bytes obtained and SHA-256 verified.
- Relevant Canon authority and numeric paragraphs inspected.
- NEXY exact commit inspected read-only for event ownership and Q64.64.
- Current AI-CONTEXT active EPC landscape collision-scanned.
- Orthogonal procedural-due-process axis selected.
- 20-system surface frozen.

IN_PROGRESS:
- standalone Python package and tests.

NEXT:
- create local isolated package;
- execute RED/GREEN/refactor/failure-repair loop;
- seal evidence;
- refresh AI-CONTEXT collision/head;
- publish exact tested bytes;
- GitHub read-back;
- evaluate one KEEP round only if evidence remains sufficient.

## Resume rule
Refresh AI-CONTEXT HEAD and NEXY HEAD first, re-read this file, preserve scope and collision boundaries, and never infer PASS from file presence or from work performed by another chat.
