# NEXY Evolutionary Proposal Court (EPC) — KEEP Vote

VOTE_ID: `VOTE-2026-10-05-0311-EPC-MUTATION-ADVERSARY-LAB-KEEP-001`
CHAT_ID: `CHAT-20261005-0311-NEXY-EPC-MUTATION-ADVERSARY-LAB-20`
ROUND: `KEEP`
TIMESTAMP: `2026-10-05T03:44:48+07:00`

SPEC_ID: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
SPEC_HASH: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
NEXY_REPO: `goif74945-crypto/NEXY.AI-`
NEXY_BRANCH: `NEXY.ai`
NEXY_COMMIT_SHA: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
AI_CONTEXT_COMMIT_SHA: `739fab334ac5988a032a3a70a4478781197cacf2`

CANDIDATE_ID: `EPC-MUTATION-ADVERSARY-LAB-20`
CANDIDATE_PATH: `คลังข้อมูลเสริม/CHAT-20261005-0311-NEXY-EPC-MUTATION-ADVERSARY-LAB-20`

STATUS_BEFORE: `STANDALONE_VERIFIED_LO4_NON_CANONICAL`
VERDICT: `KEEP_FOR_FURTHER_DEVELOPMENT_AND_INTEGRATION_PREPARATION__NO_PROMOTION`

## SPEC_EVIDENCE

Direct raw-source read was completed before this vote.

- Raw Drive object was detected as Microsoft Word 2007+ / OOXML despite a misleading `.txt` Drive filename.
- Raw bytes: 2,146,350.
- Direct SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`.
- Direct DOCX parse: 12,537 paragraphs / 10,979 non-empty.
- Paragraph 2654: unclear execution must halt; contradiction freezes instead of being silently resolved.
- Paragraph 2657: Core alone may decide / validate / verify / lock / freeze / kill / commit to Vault.
- Paragraphs 2658-2660: AI is worker/verification machinery and stage failure halts the chain.
- Paragraph 2662: Human Layer may not mutate state, override decisions, or bypass verification.
- Paragraphs 6771-6775: signed 128-bit fixed-point, Q64.64, authoritative math fixed128, no mixed precision.
- Paragraphs 8487-8494: validation is required repeatedly through API/CORE/queue/worker/SWARM/JUDGE/LAW/VAULT boundaries.
- Paragraphs 8546-8551: forbidden dependency edges include SWARM → VAULT and JUDGE → CORE.
- Paragraphs 8626-8633: execute = CORE; agents_done = SWARM; verified/accepted/rejected = JUDGE.
- Paragraphs 9858-9863: authority lock restated; Human Layer may not change Core state.

## CODE_EVIDENCE

Read-only NEXY code at `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43` was inspected before the vote.

- `packages/phase-f/game/numeric-law.ts`, blob `62ec68ae19ec5554c7c357d5f9cae2838d1dba01`: Q64.64 / i128 saturation / div-zero fail-closed.
- `packages/judge/candidate.ts`, blob `eb9e261006c6496c78256d0ad1b287425cd2a8e8`: JUDGE revalidates SWARM candidate boundary.
- `packages/intelligence/trinity.ts`: proposer/verifier/feedback/publisher authority separation; implicit override false.
- `packages/swarm/pipeline.ts`: release must remain JUDGE_PENDING or freeze at the Trinity boundary.
- `packages/phase-f/sovereign/versioning-law.ts`: explicit ratification/deploy gates.

Candidate implementation evidence:
- sealed archive SHA-256: `a4ce20cd6d25bb1170017de8cab1e59a17ff0f2a1be61f0b1d88050a7cb1fc89`;
- manifest SHA-256: `55d96963950a5db3bc8896b9b267bf8ee81dbbf2818d87f5f76ec7a7b14fab38`;
- 35 manifest-tracked design/code/test/evidence files;
- compileall PASS;
- static AST determinism audit PASS over 9 package files;
- 39/39 unit/adversarial tests PASS;
- all `C(20,2)=190` pairwise mutation compositions exercised;
- all 20 combined preserve exact intended invariant detections;
- mutation campaign 20 killed / 20, 0 escaped;
- mutation score Q64.64 raw `18446744073709551616` = exact 1.0;
- independent campaign verifier PASS;
- baseline digest `2048f73637aae394d845fa5ab3a86dbb40e56f5ce2a0badab8ac81177505f99a`;
- campaign report digest `7a9c25710d6aebcb8ad35c09dfd8b0bd4d6ba8ad0c1d44b389b29ce60ddb1127`.

Failure/recovery evidence:
- initial suite found one composition defect between M06 and M07;
- root cause identified as M07 overwriting the active vote round;
- smallest correction preserved the active round and consumed the matching vote budget instead;
- the complete verification pipeline was rerun and passed.

## AI_CONTEXT_EVIDENCE

Current AI-CONTEXT state was read before this vote.

High-overlap work was semantically inspected and excluded:
- `CHAT-20261005-0308-NEXY-LO4-EPC-CAUSAL-PROOF-20`: causal/evidence governance WIP;
- `CHAT-20261005-0309-NEXY-EPC-LO4-COURT-FOUNDRY-20`: court/vote mechanics WIP;
- Deterministic Swarm Mechanism Fabric 20: diversity/collusion/minority mechanisms;
- Minimal Blocker Core: deterministic blocker/repair-set work;
- Authority-Preserving Causal Merge / Concurrency Integrity: merge/vector-clock/mutation scheduling.

Those WIP candidates were not CUT.

Current bounded search found no direct matches for `mutation testing`, `mutant kill`, `mutation score`, or `verification adequacy mutant`.

Publication proof:
- 8 base64 archive parts are stored under the candidate path;
- all 8 parts were re-fetched from AI-CONTEXT;
- every observed Git blob SHA and byte length matched the locally tested bundle part exactly.

## ARCHITECTURE_FIT

`HIGH_FOR_ADVISORY_LO4`.

The lab is deliberately external/advisory. It tests verification adequacy and does not become a state owner, publisher, promotion gate, JUDGE replacement, LAW replacement, or CORE replacement.

## CANON_COMPATIBILITY

`HIGH_FOR_STANDALONE_SCOPE / INTEGRATION_NOT_VERIFIED`.

The candidate encodes known-invalid adversaries around authority, Q64.64, evidence freshness, deterministic identity and verification boundaries. It has no mechanism that can change Canon.

## NOVELTY

`HIGH_WITHIN_INSPECTED_AI_CONTEXT_SCOPE`.

Novelty is supported by semantic exclusion of the nearest projects and zero direct search hits for mutation-testing terminology at the vote checkpoint. This is bounded evidence, not a universal uniqueness claim.

## OVERLAP

`LOW_TO_MODERATE_AND_INTENTIONAL`.

It references the same Canon invariants that other EPC work must enforce, but its implementation goal is orthogonal: measure whether tests/verifiers detect injected violations rather than implement court mechanics, causal proof, merge, or proposal promotion.

## IMPLEMENTATION_VALUE

`HIGH`.

The package is executable, deterministic, sealed, independently checkable, and structured for later adapter work.

## VERIFICATION_VALUE

`VERY_HIGH_FOR_STANDALONE_E1_E2`.

The project directly measures test adequacy and caught a defect in its own mutation infrastructure before finalization.

## SECURITY_IMPACT

`POSITIVE_ASSURANCE_ONLY / NO_PRIVILEGED_RUNTIME_ACTION`.

It creates adversarial fixtures for testing but has no authority-bearing runtime path and performs no NEXY production mutation.

## DETERMINISM_IMPACT

`POSITIVE`.

Q64.64 raw scoring, canonical serialization, no decision RNG, no decision wall clock, exact digesting, and replay-oriented tests reduce hidden nondeterminism in the proposed verification surface.

## MAINTENANCE_COST

`MODERATE`.

Twenty mutation contracts and their exact-invariant oracle must be updated when authoritative boundaries evolve. The catalog and independent oracle intentionally make those changes explicit.

## CONFLICTS

No proven Canon conflict in the standalone design.

Unresolved integration question: exact future NEXY adapter surface and evidence class required for E3+ integration proof.

## DUPLICATES

No semantic duplicate was proven in the inspected current AI-CONTEXT scope.

Name similarity alone was explicitly rejected as duplicate evidence.

## DEPENDENCIES

- current authoritative NEXY Spec / Canon interpretation;
- current NEXY authority and numeric boundaries;
- Python standard library for the standalone reference;
- future NEXY adapter/integration harness for E3+ evidence;
- AI-CONTEXT evidence and vote lineage.

## FACT

- NEXY remained read-only during this work.
- Exact direct Spec bytes were read and hash-matched.
- 20 mutation families exist in the sealed candidate.
- 39 tests passed after the repair.
- 190 pairwise mutant combinations were exercised.
- 20/20 campaign mutants were killed by their exact expected invariant.
- 8/8 published bundle parts match the locally tested pieces by Git blob identity and size.
- This KEEP vote cannot promote the candidate.

## ASSUMPTION

- A future NEXY adapter can consume equivalent canonical scenario/evidence structures without weakening current authority boundaries. This is a design assumption only and is not required for the standalone PASS.

## UNKNOWN

- Exact integration point into a future NEXY revision.
- E3/E4/E5 behavior against the real NEXY workspace/runtime.
- Production resource/performance characteristics.
- Whether Canon will ever approve/promotion-select this proposal.

## REASON

KEEP is justified because the candidate is materially distinct from inspected sibling work, implements all 20 planned adversaries, found and repaired a real semantic defect, has exact-byte publication evidence, aligns with direct Spec authority/numeric boundaries, and has unusually high verification utility without claiming state authority.

## COUNTERARGUMENT

A 20/20 mutation score can be misleading if the mutation corpus is too synthetic, if the independent oracle shares the same mistaken assumptions, or if real NEXY integration exposes behaviors absent from the standalone model. The package therefore must not be promoted based on this vote or E1/E2 results alone.

## FINAL_JUSTIFICATION

`KEEP` means retain, develop, combine where useful, and prepare for future formal integration evidence. It does **not** mean Canon acceptance, release approval, state mutation, or automatic promotion.

KEEP right consumed for this CHAT_ID: `YES`.
CUT right consumed for this CHAT_ID: `NO`.
CUT right remaining: `1`.
