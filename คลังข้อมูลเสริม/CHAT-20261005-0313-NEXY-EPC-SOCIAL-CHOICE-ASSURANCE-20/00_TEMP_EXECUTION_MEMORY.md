# TEMP EXECUTION MEMORY — NEXY EPC SOCIAL-CHOICE ASSURANCE 20

CHAT_ID: CHAT-20261005-0313-NEXY-EPC-SOCIAL-CHOICE-ASSURANCE-20
PLATFORM_NATIVE_CHAT_ID: UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS
STATUS: EXECUTING
CLASSIFICATION: Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING
CREATED_LOCAL: 2026-10-05T03:13:00+07:00

## OBJECTIVE
Design, implement, execute, repair, test, and preserve exactly 20 deterministic Q64.64 social-choice assurance mechanisms for NEXY Evolutionary Proposal Court (EPC). This layer is pre-vote/advisory only: it analyzes candidate-selection stability and manipulation risk but cannot cast KEEP/CUT, promote, mutate Canon, or mutate NEXY Core/JUDGE/LAW state.

## WRITABLE SCOPE
- goif74945-crypto/AI-CONTEXT
- branch main
- only path prefix: คลังข้อมูลเสริม/CHAT-20261005-0313-NEXY-EPC-SOCIAL-CHOICE-ASSURANCE-20/**
- shared vote path only if a later evidence-complete vote is actually cast

## PROTECTED SCOPE
- goif74945-crypto/NEXY.AI- and every repository whose name contains NEXY.AI: READ ONLY
- no branch/settings/workflow/issue/PR/code mutation in protected repositories

## BASELINE EVIDENCE
NEXY_REPO: goif74945-crypto/NEXY.AI-
NEXY_BRANCH: NEXY.ai
NEXY_COMMIT_SHA: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
NEXY_TREE_SHA: a809bc5f4cc2d8f806e500d1d3a09a4e66450c7c
AI_CONTEXT_REPO: goif74945-crypto/AI-CONTEXT
AI_CONTEXT_BRANCH: main
AI_CONTEXT_OBSERVED_HEAD_BEFORE_MEMORY: 0e77ed5e8ebc15cdd2c1eb2c06c941a9988d79bd
IGNIS_REFERENCE_PATH: REFERENCES/NEXY/2026-10-04/04-NEXY-IGNIS-source.txt
IGNIS_REFERENCE_BLOB_SHA: 30b0c179670a836af61923b4b85ae89f3a40d8dc
IGNIS_CANONICAL_SOURCE_SHA256_RECORDED: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
NORMALIZED_REQUIREMENT_ROWS_RECORDED: 837

## AUTHORITY FACTS VERIFIED
- USER LAW is above AI logic and must not be reinterpreted/bypassed.
- CORE is the state/decision authority.
- SWARM is debate/work, not decision authority.
- JUDGE owns verified/accepted/rejected events in the current VNext state matrix.
- Human/auxiliary layers cannot modify Core state or bypass verification.
- Contradiction or insufficient proof leads to FREEZE, not guess.
- Lo4 output is advisory until proof and formal promotion.
- Current NEXY contains Q64.64 bigint/i128 fixed-point surfaces; this task uses Q64.64 BigInt for all authoritative numeric mechanics.

## COLLISION BOUNDARY
Existing concurrent EPC work already covers vote-right ledger, WIP protection, semantic duplicate proof, promotion readiness, canon collision, evidence freshness, revision immutability, dossier compilation, causal proof, falsification, temporal consistency and generic Q64 court mechanics. This mission MUST NOT reimplement those.

Name-level corpus scan at the locked snapshot found zero paths containing:
social-choice, Condorcet, Schulze, Ranked Pairs, Smith Set, Kemeny, Borda, Copeland, pairwise-majority.

This is evidence of a likely gap, NOT proof of total semantic absence. Deeper comparison remains required.

## 20 TARGET MECHANISMS
1. Canonical Preference Witness Validator
2. Q64 Weighted Pairwise Majority Matrix
3. Condorcet Winner/Loser Detector
4. Majority-Cycle Strongly-Connected-Component Detector
5. Smith Set Extractor
6. Schwartz Set Extractor
7. Schulze Strongest-Path Ranking
8. Ranked-Pairs Acyclic Lock Ranking
9. Minimax Opposition Ranking
10. Copeland Pairwise Score
11. Weighted Borda Baseline
12. Bounded Exact Kemeny-Young Optimizer
13. Majority-Judgment Grade Aggregator
14. Pairwise Margin-of-Victory Analyzer
15. Leave-One-Witness-Out Sensitivity Audit
16. Explicit Clone-Group Sensitivity Audit
17. Sequential Agenda-Control Stress Simulator
18. Source-Weight Concentration / Coalition Capture Metric
19. Cross-Method Rank Discordance Analyzer
20. Social-Choice Stability Dossier Compiler

## IMMUTABLE RULES
- Input preference witnesses are evidence artifacts, NOT KEEP/CUT votes and consume no vote right.
- No mechanism may emit KEEP/CUT or promotion authority.
- Missing, malformed, ambiguous, or out-of-range critical evidence => INSUFFICIENT_EVIDENCE / failure, never guessed ranking.
- Deterministic ordering is lexicographic by explicit stable candidate IDs unless a method defines a stronger evidence-derived ordering; lexicographic order is tie representation only, never hidden preference.
- Binary floating point is forbidden in authoritative numeric paths.
- Q64.64 bounds/overflow/divide-by-zero fail closed.
- Exact Kemeny solver is bounded; oversized sets return unsupported/insufficient evidence rather than approximate silently.
- Clone groups must be explicit evidence; never inferred from names.
- Source identities must be explicit for concentration analysis.
- Outputs are advisory witnesses for CORE/JUDGE/Human formal review only.

## EXECUTION LOOP
INSPECT -> SPEC PIN -> NEXY READ-ONLY PIN -> COLLISION SCAN -> DESIGN -> IMPLEMENT -> UNIT -> PROPERTY -> ADVERSARIAL -> DETERMINISM -> FIX -> RE-TEST -> EVIDENCE -> PUBLISH -> READBACK -> FINAL AUDIT

## CURRENT STATE
COMPLETED:
- AI-CONTEXT current tree/corpus inspected
- concurrent EPC collision surface inspected
- IGNIS reference inspected
- current NEXY JUDGE/LAW/SWARM/state/Q64 surfaces inspected read-only
- social-choice gap selected

IN_PROGRESS:
- standalone dependency-free Node/ESM implementation using signed checked Q64.64 BigInt
- 20 mechanism design and tests

VOTE RIGHTS:
- KEEP: UNUSED
- CUT: UNUSED

VERIFICATION:
- protected NEXY mutations: 0
- implementation: NOT VERIFIED YET
