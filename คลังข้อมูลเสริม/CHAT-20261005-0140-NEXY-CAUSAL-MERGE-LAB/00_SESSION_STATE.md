# SESSION STATE — NEXY Authority-Preserving Causal Merge Lab

status: COMPLETE_FOR_STANDALONE_SCOPE
date: 2026-10-05
project_local_work_id: CHAT-20261005-0140-NEXY-CAUSAL-MERGE-LAB
platform_chat_id: UNKNOWN
platform_chat_id_note: Current toolset does not expose an immutable ChatGPT conversation ID. This value was not invented.

## Objective
Create a standalone experimental deterministic causal merge/reference implementation that can later integrate with NEXY.AI without modifying any repository whose name contains NEXY.AI.

## Mutable scope used
- goif74945-crypto/AI-CONTEXT
- คลังข้อมูลเสริม/CHAT-20261005-0140-NEXY-CAUSAL-MERGE-LAB/**

## Protected scope
Every repository whose name contains NEXY.AI remained READ/ANALYZE ONLY.

## Delivered
- deterministic causal merge design
- standalone TypeScript source and tests preserved losslessly in CODE_TEST_BUNDLE parts
- external authority/policy gate
- canonical SHA-256 operation, policy, state/frontier/history and conflict certificate identities
- causal gap/cycle/equivocation/tamper detection
- tombstones, CAS-style expected key digest, deterministic replay
- generic future NEXY adapter seam with no protected repo import
- design, integration contract, failure model, repair log, test evidence, future proposal backlog, final audit in DURABLE_RECORD.md

## Verification
- E1 strict TypeScript: PASS
- E1 Node16 compatibility configuration: PASS on local TypeScript 5.8.3
- E2 executable tests: 39/39 PASS
- sampled permutation convergence: 500 merge + 500 conflict permutations PASS
- 10,000 independent-operation stress path: PASS
- latest sandbox full verify observation: 2.56 s / 144368 KB max RSS
- E3 actual NEXY integration: NOT_VERIFIED
- E4-E6 runtime/deployment: NOT_VERIFIED
- exact NEXY TypeScript 6.x workspace validation: NOT_VERIFIED

## Durable integration rule
Current DOC-C context forbids direct SWARM -> VAULT. A future authorized integration must use an authorized CORE/VAULT path and preserve Vault previous_version optimistic concurrency. This lab must never become a worker persistence backdoor.

## Bundle integrity
Decoded CODE_TEST_BUNDLE.tar.gz SHA-256:
7f2e8d086f729597b0427ca7ea20949c7df7803a1745517644d8b89fafdea4ab

## Remaining
None for this standalone authorized scope. Production integration/formal verification/signatures/clock compaction/database concurrency/deployment remain separate future work requiring appropriate authorization and evidence.
