# TEMP SESSION STATE — NEXY Authority-Preserving Causal Merge Lab

status: IN_PROGRESS
date: 2026-10-05
project_local_work_id: CHAT-20261005-0140-NEXY-CAUSAL-MERGE-LAB
platform_chat_id: UNKNOWN
platform_chat_id_note: Current toolset does not expose an immutable ChatGPT conversation ID. Do not invent one.

## Objective
Create a standalone, experimental, deterministic causal merge/reference implementation that can later integrate with NEXY.AI without modifying any repository whose name contains NEXY.AI.

## Mutable scope
- goif74945-crypto/AI-CONTEXT
- path: คลังข้อมูลเสริม/CHAT-20261005-0140-NEXY-CAUSAL-MERGE-LAB/**

## Protected scope
- Every repository whose name contains NEXY.AI: READ/ANALYZE ONLY.
- Existing supplemental projects outside this project folder are read-only for this task unless a final index/provenance update is strictly needed.
- No secrets/credentials/PII.

## Verified starting facts
- AI-CONTEXT default branch: main.
- Supplemental folder already exists.
- NEXY implementation repository observed read-only: goif74945-crypto/NEXY.AI-, canonical branch NEXY.ai.
- NEXY uses TypeScript/Vitest and strict TypeScript settings in its current repository.
- AI-CONTEXT search returned zero direct hits for CRDT, vector clock, Lamport, causal consistency, replica, concurrent edit, and distributed state terminology at inspection time. This is search evidence, not proof of absolute conceptual absence.

## Locked design direction
Experimental proposal: authority-preserving deterministic causal merge fabric for multi-agent/session state.
- No last-write-wins.
- No model-generated conflict winner.
- Causally ordered updates may supersede predecessors.
- Concurrent divergent writes to the same semantic key freeze with a deterministic conflict certificate.
- Concurrent commuting writes merge deterministically.
- Tamper, causal gaps, invalid authority, malformed clocks, and policy violations fail closed.
- External authority mapping is configuration; this lab must not invent NEXY canonical authority law.

## Planned artifacts
- DESIGN.md
- REQUIREMENT_LEDGER.md
- INTEGRATION_CONTRACT.md
- FAILURE_MODEL.md
- src/*.ts
- tests/*.test.ts
- package.json / tsconfig.json
- TEST_EVIDENCE.md
- FINAL_AUDIT.md
- README.md
- 00_SESSION_STATE.md updated at resumable checkpoints

## Verification target
E1 static TypeScript compilation + E2 executed unit/property-style tests in isolated local environment. NEXY integration/runtime/deployment remain NOT_VERIFIED because protected NEXY repositories will not be mutated.

## Next action
Implement locally, run compile/tests, repair failures, then persist verified artifacts and evidence into this folder.
