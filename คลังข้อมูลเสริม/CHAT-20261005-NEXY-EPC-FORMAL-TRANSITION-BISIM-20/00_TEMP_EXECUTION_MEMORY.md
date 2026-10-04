# TEMP EXECUTION MEMORY — NEXY EPC Formal Transition Safety & Bisimulation Calculus 20

CHAT_ID: `CHAT-20261005-NEXY-EPC-FORMAL-TRANSITION-BISIM-20`
PLATFORM_NATIVE_CHAT_ID: `UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS`
STATUS: `IN_PROGRESS`
CLASSIFICATION: `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING`

## Objective
Design, implement, execute, repair, re-test, and preserve exactly 20 deterministic Q64.64 formal-transition assurance mechanisms that can later act as a read-only proof adapter around NEXY state/authority contracts. The lab proves behavioral equivalence, refinement, authority noninterference, fail-closed reachability, invariant preservation, and adapter compatibility. It has zero power to promote, release, mutate Canon, or mutate NEXY runtime state.

## Scope lock
WRITABLE:
- `goif74945-crypto/AI-CONTEXT`
- branch `main`
- ONLY `คลังข้อมูลเสริม/CHAT-20261005-NEXY-EPC-FORMAL-TRANSITION-BISIM-20/**`
- one append-only KEEP receipt and one append-only CUT receipt under `คลังข้อมูลเสริม/VOTES/**` only when all EPC vote prerequisites are actually met.

READ-ONLY / PROTECTED:
- every repository whose name contains `NEXY.AI`
- observed implementation repo: `goif74945-crypto/NEXY.AI-`
- branch: `NEXY.ai`
- observed exact commit: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`

FORBIDDEN:
- any NEXY.AI mutation;
- Canon/Law/Core/JUDGE/SWARM state mutation or authority escalation;
- automatic promotion/release;
- physical deletion as CUT;
- WIP/UNKNOWN/INSUFFICIENT_EVIDENCE as sufficient CUT cause;
- binary floating point in authoritative proof/scoring paths;
- hidden randomness, wall clock, network state, filesystem order, or unspecified map order in proof results;
- PASS/COMPLETE without executed evidence.

## Grounded authority pins
AI_CONTEXT_OBSERVED_HEAD_BEFORE_THIS_CHAT: `1e2e4bc9beabfed8b8ebcc52ebea8dd55b581a84`
NEXY_REPO: `goif74945-crypto/NEXY.AI-`
NEXY_BRANCH: `NEXY.ai`
NEXY_COMMIT_SHA: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
SPEC_ID: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
SPEC_DRIVE_OBJECT_OBSERVED: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.txt`
SPEC_DRIVE_FILE_ID: `1JHv9vPv4OaK0cOHS1de-BftGoY3bX0qA`
SPEC_BYTES: `2146350`
SPEC_SHA256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
SPEC_CONTAINER: `ZIP/OOXML; word/document.xml present`
SPEC_NONEMPTY_PARAGRAPHS: `10979`

Direct source extraction in this chat verified the above SHA-256 from materialized Drive bytes. Relevant source facts include:
- Q64.64 is explicitly specified.
- the source defines NEXY as an executable constitutional state machine.
- deterministic state-machine requirements and invalid transitions are explicit.
- `verified`, `accepted`, and `rejected` are assigned to JUDGE in the executable state-machine material.
- SWARM is labor/debate, not final authority.
- contradiction/invalid states lead to FREEZE rather than silent guessing.

## Current implementation compatibility observations
At protected NEXY commit `9e615b04...`:
- `core-kernel/src/engine/fixed128_math.rs` uses signed i128 Q64.64.
- `packages/core/vnext-state-matrix.ts` assigns boot/execute to CORE, agents_done to SWARM, verified/accepted/rejected to JUDGE.
- `packages/queue/workers.ts` states LAW authorizes VERIFYING -> CONSENSUS and final output after JUDGE candidate metrics.
- `packages/judge/consensus.ts` fails closed when release authorization/evidence/threshold conditions fail.
- `packages/phase-f/lo2/runtime-coordinator.ts` keeps promotion fail-closed and evidence-gated.

## Collision exclusions
This mission does NOT recreate:
- EPC causal/evidence governance or vote-right ledgers;
- Court Foundry ballot/court mechanics;
- Evolutionary Ecology/integration/blast-radius work;
- Phase-Boundary cliff/hysteresis work;
- generic interleaving verification;
- proposal composition collision/order/resource analysis;
- mutation/adversary testing;
- strategyproof/social-choice voting;
- context-compaction proof.

Its distinct target is **formal behavioral equivalence and authority-preserving refinement of finite transition contracts**.

## Frozen 20-mechanism surface
1. State Contract Normalizer (SCN)
2. Explicit Strong Bisimulation Witness Checker (ESBWC)
3. Stutter-Projection Equivalence Checker (SPEC)
4. Visible Trace Prefix Inclusion Prover (VTPI)
5. Illegal Transition Witness Miner (ITWM)
6. Authority Ownership Preservation Checker (AOPC)
7. Protected-Event Noninterference Matrix (PENM)
8. Freeze-Dominance Reachability Prover (FDRP)
9. Stable-Gate Dominator Checker (SGDC)
10. Error-State Totality Checker (ESTC)
11. Event Determinism Fingerprint (EDF)
12. Canonical State Snapshot Codec (CSSC)
13. Contract Refinement Lattice Classifier (CRLC)
14. Semantic-Version Delta Classifier (SVDC)
15. Q64 Guard Equivalence Prover (QGEP)
16. Q64 Boundary Partition Generator (QBPG)
17. Invariant Inductiveness Checker (IIC)
18. Advisory-State Isolation Proof (ASIP)
19. Read-Only Adapter Compatibility Witness (RACW)
20. Formal Proof Capsule Compiler (FPCC)

## Numeric law
All decision-relevant quantities and guards use checked signed Q64.64 represented as signed i128 raw values. Overflow, invalid range, malformed guard, and divide-by-zero fail closed. Binary float is forbidden.

## Vote budget
- KEEP remaining: 1 / 1
- CUT remaining: 1 / 1
- DEFER / INSUFFICIENT_EVIDENCE / WIP consume neither.
- Historical votes are immutable; evidence revisions never restore a consumed round.
- Semantic duplication requires actual module/function/path evidence.
- Vote score cannot override Canon/Law/Core/JUDGE or auto-promote.

## Execution state
COMPLETED:
- AI-CONTEXT boot/kernel/rules/workflows read.
- protected NEXY repo/branch/head resolved and read-only authority surfaces inspected.
- canonical NEXY-IGNIS bytes fetched from Drive and independently SHA-256 verified.
- source OOXML parsed; relevant state/Q64/JUDGE/SWARM/freeze clauses located.
- concurrent supplemental collision scan performed.
- unique formal-transition surface frozen.

IN_PROGRESS:
- TDD implementation and executable proof suite.
- exact tested-byte manifest.
- publication/readback evidence.

NEXT:
- author RED tests;
- execute RED;
- implement all 20 mechanisms;
- run strict compile/unit/property/integration/determinism/negative tests;
- repair until green;
- publish Design + Code + Tests + Evidence;
- read back published bytes;
- evaluate exactly one KEEP round only if evidence is sufficient; leave CUT unused absent a proven cut candidate.

## Resume law
Refresh AI-CONTEXT HEAD and protected NEXY HEAD, re-read this file, and continue from the first non-PASS quality gate. Never infer completion from file presence and never mutate a repository whose name contains `NEXY.AI`.
