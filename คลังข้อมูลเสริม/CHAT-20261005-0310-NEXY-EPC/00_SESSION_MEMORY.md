# 00 — Session Memory / Mission Checkpoint

- mission_id: NEXY-EPC-2026-10-05-0310
- project_chat_id: CHAT-20261005-0310-NEXY-EPC
- platform_immutable_chat_id: UNKNOWN_NOT_EXPOSED_BY_CURRENT_TOOLSET
- classification: AI_PROPOSED_LO4 / NON_CANONICAL / NON_GOVERNING
- persistence_mode: DURABLE_RESUMABLE_IN_AI_CONTEXT
- current_phase: TDD_RED_CONFIRMED / IMPLEMENTATION_PENDING
- protected_repo: goif74945-crypto/NEXY.AI- (READ ONLY)
- writable_repo: goif74945-crypto/AI-CONTEXT
- writable_scope: คลังข้อมูลเสริม/CHAT-20261005-0310-NEXY-EPC/**
- central_vote_scope_authorized_later: คลังข้อมูลเสริม/VOTES/**

## Objective
Build NEXY Evolutionary Proposal Court (EPC) as a deterministic Lo4 advisory governance reference implementation with 20 implemented chamber concepts, Q64.64 authoritative scoring, append-only vote-right enforcement, WIP/UNKNOWN CUT protection, evidence-bound semantic duplicate proof, and an explicit non-authority boundary that prevents EPC from mutating or bypassing NEXY CORE/JUDGE/LAW.

## Authority baseline
- User directive in current conversation.
- AI-CONTEXT INDEX / AI-EXECUTION-KERNEL / GLOBAL / SECURITY / VERIFICATION.
- NEXY project context derived from NEXY-IGNIS canonical source SHA-256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7.
- Actual protected NEXY repository observed at branch NEXY.ai commit 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43.

## Source-grounded invariants
1. CORE owns authoritative execution state.
2. JUDGE owns verified/accepted/rejected product-level adjudication events.
3. SWARM/AI labor cannot mutate canonical state merely by consensus.
4. Authoritative numeric core uses signed i128 / Q64.64.
5. Core overflow is fail-closed/freeze; no wrap, silent saturation, or float authority.
6. EPC may recommend KEEP/CUT/DEFER eligibility but cannot promote into Canon.
7. CUT means archive/reject/supersede semantics only, never physical deletion.
8. WIP/UNKNOWN/insufficient evidence cannot be CUT merely for being incomplete.
9. Each CHAT_ID has one KEEP right and one CUT right for its lifetime.
10. Vote revisions may append evidence but never replenish vote rights or silently rewrite historical verdicts.

## Novelty boundary
Nearest inspected systems:
- NEXY-PROPOSAL-FORGE: validates/packages proposals, deterministic overlap/admission recommendations.
- NCIF: independent evidence-lineage/pseudo-consensus detection.
- Causal Merge Lab: causal conflict handling for state/Vault semantics.
- NEXY Evolution Atlas: execution/proof topology mapping.

EPC is deliberately NOT a replacement for those systems. Its primary domain is lifecycle governance of proposal evidence and irrevocable vote-right accounting after proposal packaging.

## TDD checkpoint
Local isolated source workspace: /mnt/data/nexy_epc_work
Observed RED command:
cmake -S . -B build-red -G Ninja -DCMAKE_BUILD_TYPE=Release && cmake --build build-red -j2

Observed RED result:
- CMake configure begins with GCC 14.2.
- Fails because src/q64.cpp does not yet exist.
- exit code: 1.
This is expected pre-implementation evidence.

## Exact next legal action
Implement the Q64.64 carrier and EPC/vote modules without weakening the existing tests, then run GCC/Clang builds, unit/property tests, sanitizer verification, deterministic replay, and exact-persisted-byte re-verification.

## Freeze conditions
- any required write to a repository whose name contains NEXY.AI;
- any design that lets EPC override Canon/LAW/JUDGE/CORE;
- unresolved authority contradiction;
- inability to produce execution evidence for a claimed PASS.
