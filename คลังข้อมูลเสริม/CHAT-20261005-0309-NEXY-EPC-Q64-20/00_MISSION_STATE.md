# NEXY Evolutionary Proposal Court (EPC) — Mission State

MISSION_ID: EPC-2026-10-05-0309-ICT-Q64-20
CHAT_ID: CHAT-20261005-0309-NEXY-EPC-Q64-20
PLATFORM_CHAT_ID: UNKNOWN_NOT_EXPOSED_BY_HOST
CREATED_AT: 2026-10-05T03:09:00+07:00
PERSISTENCE_MODE: DURABLE_RESUMABLE
STATE: AUTHORITY_SEALED
WORKSPACE: goif74945-crypto/AI-CONTEXT
WORKSPACE_BRANCH: main
WORKSPACE_BASELINE_SHA: 55469befc00844f14993c98c104a29c99dff7a0b
PROTECTED_REPOSITORY: goif74945-crypto/NEXY.AI-
PROTECTED_BRANCH: NEXY.ai
PROTECTED_BASELINE_SHA: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
PROTECTED_REPOSITORY_MODE: READ_ONLY

## Objective
Design, implement, test, and preserve a large Lo4 advisory governance system named **NEXY Evolutionary Proposal Court (EPC)** plus twenty novel EPC subsystems. The implementation must be deterministic, Q64.64-based, evidence-driven, reusable by NEXY.AI later, and must never obtain authority to mutate Canon/Core/JUDGE state or promote proposals automatically.

## Authority
1. Explicit user directive in the current conversation.
2. NEXY source law / current project context derived from the canonical NEXY-IGNIS source corpus.
3. Current NEXY implementation repository at the locked read-only SHA.
4. AI-CONTEXT execution/security/verification law.
5. Lo4 designs produced by this mission are advisory only.

## In Scope
- Read NEXY.AI source/spec context and implementation for compatibility evidence.
- Read current AI-CONTEXT supplemental work to reduce semantic duplication.
- Create a new additive-only EPC work folder under `คลังข้อมูลเสริม/`.
- Create twenty proposal-governance concepts/modules.
- Implement deterministic Q64.64 arithmetic and EPC logic in standalone code.
- Create extensive unit/property/negative/integration-style local tests.
- Run real local compilation/tests in an isolated workspace when toolchain exists.
- Persist design, code, test sources, raw test evidence, hashes, novelty/overlap analysis, integration guidance, vote schema, and resumable state.
- Create EPC vote records only according to the user's vote law.

## Protected / Out of Scope
- Any write, delete, rename, branch update, commit, PR, issue mutation, workflow mutation, setting change, or other state change in any repository whose name contains `NEXY.AI`.
- Automatic promotion into NEXY.AI.
- Core/JUDGE/LAW state mutation by EPC, SWARM, AI, human auxiliary layer, or this work.
- Physical deletion as the meaning of CUT.
- Claiming deployment, production integration, or NEXY runtime validation without evidence.

## Immutable EPC Laws
1. Lo4 output is proposal/advisory only until formal proof and promotion.
2. Canon/Law/JUDGE authority always outranks EPC scores or votes.
3. One CHAT_ID may cast at most one KEEP round and at most one CUT round over its lifetime.
4. Vote history is append-only. Revisions add evidence; they do not restore spent vote entitlement.
5. A vote requires real Spec + NEXY code + current AI-CONTEXT evidence.
6. UNKNOWN / WIP / INSUFFICIENT_EVIDENCE can never be sufficient reason for CUT.
7. Semantic duplication must be evidenced; name similarity alone is insufficient.
8. CUT defaults to ARCHIVE / REJECTED / SUPERSEDED semantics, never physical deletion.
9. No EPC output can automatically promote a candidate or change Core state.
10. Q64.64 arithmetic is signed 128-bit-domain fixed-point. Overflow/divide-by-zero/range violations fail closed.
11. Deterministic ordering uses explicit stable identifiers; no wall clock, randomness, filesystem iteration order, network state, or floating point may influence an authoritative EPC calculation.
12. Design != implementation != runtime != deployment.

## Required Vote Record Fields
VOTE_ID
CHAT_ID
ROUND = KEEP | CUT
TIMESTAMP
SPEC_ID / SPEC_HASH
NEXY_REPO
NEXY_BRANCH
NEXY_COMMIT_SHA
AI_CONTEXT_COMMIT_SHA
CANDIDATE_ID
CANDIDATE_PATH
STATUS_BEFORE
VERDICT
SPEC_EVIDENCE
CODE_EVIDENCE
AI_CONTEXT_EVIDENCE
ARCHITECTURE_FIT
CANON_COMPATIBILITY
NOVELTY
OVERLAP
IMPLEMENTATION_VALUE
VERIFICATION_VALUE
SECURITY_IMPACT
DETERMINISM_IMPACT
MAINTENANCE_COST
CONFLICTS
DUPLICATES
DEPENDENCIES
FACT
ASSUMPTION
UNKNOWN
REASON
COUNTERARGUMENT
FINAL_JUSTIFICATION

## Acceptance Criteria
- AC-01: Exactly 20 EPC concepts are documented with distinct purpose, authority boundary, inputs/outputs, failure behavior, and NEXY integration path.
- AC-02: Executable implementation exists and uses Q64.64 for quantitative court metrics.
- AC-03: No floating-point arithmetic in the deterministic court core.
- AC-04: Overflow, divide-by-zero, malformed metrics, duplicate vote use, WIP-CUT attempts, Canon-override attempts, and auto-promotion attempts fail closed.
- AC-05: Vote entitlement law is executable and tested.
- AC-06: CUT is modeled as non-destructive disposition only.
- AC-07: KEEP/CUT decisions cannot override Canon or cause promotion.
- AC-08: Real local compilation/tests are captured if the toolchain is available.
- AC-09: Negative/adversarial/property tests exist for critical invariants.
- AC-10: A source/commit/evidence manifest binds claims to exact baselines.
- AC-11: NEXY.AI protected repository remains unchanged by this mission.
- AC-12: Durable mission state and resume instructions are present.
- AC-13: A vote template and machine-readable vote contract are present.
- AC-14: Any actual KEEP/CUT vote is withheld unless required evidence, including the canonical source/spec evidence, is sufficient.
- AC-15: No claim of completion is made without read-back verification of persisted artifacts.

## Current Evidence
FACT:
- AI-CONTEXT main baseline observed at 55469befc00844f14993c98c104a29c99dff7a0b.
- NEXY.AI- branch NEXY.ai observed at 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43.
- NEXY project context identifies canonical source SHA-256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7.
- Current source matrix has 837 normalized requirement rows.
- NEXY constitutional context forbids floating point in Core and requires fixed/integer arithmetic with fail-closed overflow.
- Current Lo3 governor uses signed Q64.64 on bigint.
- Existing supplemental work includes Proposal Forge, formal novelty, innovation containment, and many Q64 laboratories. EPC therefore must not duplicate proposal generation.

UNKNOWN:
- The host does not expose the platform's internal conversation identifier.
- The canonical DOCX itself is not directly attached in this current conversation, but AI-CONTEXT contains normalized source context and recorded canonical source identity.

## Work DAG
W01 authority/baseline seal — PASS
W02 semantic collision scan — IN_PROGRESS
W03 EPC architecture + 20 concepts — PENDING
W04 deterministic Q64.64 core — PENDING
W05 20 court modules — PENDING
W06 unit/negative/property tests — PENDING
W07 local compile/test/fix loop — PENDING
W08 design/evidence packaging — PENDING
W09 vote protocol + template — PENDING
W10 persistence read-back + hash manifest — PENDING
W11 final protected-repo recheck — PENDING
W12 final audit/status — PENDING

## Stop / Freeze Conditions
- Any required step would mutate NEXY.AI-.
- Authority conflict makes a court rule ambiguous.
- The NEXY target identity changes materially and invalidates the locked baseline.
- A test failure cannot be repaired without weakening an immutable requirement.
- A requested KEEP/CUT verdict lacks sufficient spec/code/context evidence.
- Persistence write cannot be verified.

## Resume Rule
Resume from the latest verified checkpoint in this folder. Refresh both repository HEADs, mark stale evidence if baselines changed, and never infer that unfinished work continued in the background.
