# NIAF-20 Temporary Execution Memory

- WORK_CODE: `CHAT-20261005-0309-NEXY-LO4-NIAF-Q64-20`
- PLATFORM_NATIVE_CHAT_ID: `UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS`
- AUTHORITY: `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING`
- WRITABLE_REPO: `goif74945-crypto/AI-CONTEXT`
- WRITABLE_NAMESPACE: `คลังข้อมูลเสริม/CHAT-20261005-0309-NEXY-LO4-NIAF-Q64-20/**`
- FORBIDDEN_MUTATION: every repository whose name contains `NEXY.AI`
- NEXY_READ_BASELINE: `goif74945-crypto/NEXY.AI-@9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- NEXY_BRANCH: `NEXY.ai`
- IGNIS_SOURCE_SHA256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
- IGNIS_EXTRACT_BLOB_SHA: `30b0c179670a836af61923b4b85ae89f3a40d8dc`

## Objective
Build 20 deterministic Q64.64 information-acquisition proposal subsystems that fill the gap between `WAIT_FOR_DATA_CLARITY` and acquisition of the most useful clarifying evidence/question, without gaining authority over CORE/JUDGE/LAW.

## Hard invariants
1. AI proposal only. No state mutation, release, promotion, verification bypass, or Canon override.
2. No binary floating-point in authoritative computation.
3. No wall-clock, randomness, locale ordering, environmental nondeterminism.
4. Checked signed Q64.64 arithmetic. Overflow/divide-by-zero must fail explicitly.
5. Deterministic bytewise ordering and deterministic tie-breaks.
6. Unknown/WIP cannot be silently promoted to truth.
7. All integration claims with NEXY remain `NOT_VERIFIED` until separately authorized and tested against target NEXY revision.
8. EPC KEEP and CUT rights are each single-use for this work code. No retroactive vote edits.

## Novelty/collision pivots rejected
- Counterfactual/causal simulation: overlap with existing counterfactual labs + Human Agency Lab.
- Consensus correlation/independence: overlap with NCIF/NEIK/correlation quorum work.
- Semantic contract/drift: overlap with semantic contract lab.
- Preference/human-agency governance: overlap with HICF/Human Agency Lab.
- Proof planning/compiler: overlap with Lo4 Proof Compiler Lab.

## Selected capability gap
NEXY CIRL already resolves explicit intent and returns `WAIT_FOR_DATA_CLARITY` for ambiguity/conflict. NIAF-20 proposes a deterministic pre-governance planner for what clarification/evidence to acquire, whether acquisition is worth its burden/privacy/latency/irreversibility cost, and when to stop asking and package a freeze recommendation.

## 20 concepts
C01 Epistemic Entropy Ledger
C02 Marginal Information Gain
C03 Value-of-Information Scorer
C04 User Burden Budget
C05 Privacy Cost Meter
C06 Latency Budget Meter
C07 Irreversibility Risk Guard
C08 Ambiguity Partition Resolver
C09 Question Novelty Filter
C10 Answer Sensitivity Ranker
C11 Missing Variable Impact Ranker
C12 Evidence Conflict Probe Ranker
C13 Exact Probe Portfolio Optimizer
C14 Stop-or-Ask Frontier
C15 Explicit-Tick Staleness Decay
C16 Evidence Saturation Detector
C17 Calibration Loss Tracker
C18 Batch Query Composer
C19 Fallback Freeze Evidence Packager
C20 Acquisition Envelope Compiler

## Verified state
- Q64.64 substrate: IMPLEMENTED / VERIFIED.
- Main C01-C20: IMPLEMENTED / VERIFIED.
- Tests: 29/29 PASS.
- Q64 identity iterations: 20,001 PASS.
- Portfolio property iterations: 2,000 PASS.
- Clang 17 ASan/UBSan: PASS.
- Deterministic replay: 50/50 same SHA-256.
- GCC/Clang canonical output: byte-identical.
- Static audit: PASS.
- F-001..F-005: repaired and full regression passed.
- Sealed archive SHA-256: `24e9ffd24bd61fa20adcbda10d36075bb76a784cc006e5dfe6bb3ec9c5d4c5b5`.
- GitHub transport read-back: 4/4 part blob identities matched the source bytes.
- NEXY runtime integration: NOT_VERIFIED / NOT_PERFORMED.
- Canon promotion: NOT_PERFORMED.

This file is an execution-memory checkpoint. The sealed bundle contains the earlier pre-publication checkpoint as historical evidence.
