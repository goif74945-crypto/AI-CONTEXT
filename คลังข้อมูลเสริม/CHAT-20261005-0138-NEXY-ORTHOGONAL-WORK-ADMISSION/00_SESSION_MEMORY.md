# Session Memory — NEXY Orthogonal Work Admission Engine

- workspace_chat_tag: `CHAT-20261005-0138-NEXY-ORTHOGONAL-WORK-ADMISSION`
- actual_chat_platform_id: UNKNOWN / not exposed by the host
- started_local_time: `2026-10-05T01:38+07:00`
- repository: `goif74945-crypto/AI-CONTEXT`
- initial_main_head_observed: `fefa24ddaaa758277572e275bc6834b5aebdf487`
- persistence_mode: DURABLE_RESUMABLE after verified read-back
- phase: PLAN_LOCKED
- project_status: AI_PROPOSED_FUTURE_CONCEPT
- NEXY.AI repositories: READ-ONLY / NO MUTATION
- writable_scope: only this project directory inside AI-CONTEXT

## Objective
Build a standalone, deterministic reference system that prevents new AI/project work from silently duplicating existing work. It accepts structured work manifests, canonicalizes them, computes stable fingerprints, compares declared facets with integer-only overlap scoring, and returns an auditable admission verdict.

## Why this gap was selected
The supplemental vault currently contains many concurrent project directories. Existing NEXY context already covers command/path collision, verified reuse, proof systems, and many semantic/authority labs, but no directly named deterministic novelty/orthogonality admission layer for new supplemental work was found in the repository tree inspection.

## Core invariants
1. No mutation of any repository whose name contains `NEXY.AI`.
2. No claim that this proposal is a current NEXY build requirement.
3. Deterministic output for identical manifest/catalog input.
4. Integer-only scoring in the canonical decision path.
5. Exact duplicate must never be admitted as novel.
6. Missing required facets fails closed.
7. File-system scans are lexicographically ordered and symlinks are not followed.
8. Every admission result carries algorithm/version/catalog provenance.

## Planned deliverables
- design + source alignment + integration contract
- machine-readable manifest schema
- TypeScript reference implementation with no runtime dependencies
- CLI
- fixtures and tests
- E1/E2/E3 evidence
- final audit + resume state

## Current state
COMPLETED:
- AI-CONTEXT bootstrap / execution kernel / work router / global security & verification rules read.
- NEXY overview, deep index, constitutional locks, current 837-row matrix summary read.
- supplemental repository tree inspected for overlap.
- project idea selected as AI-proposed future concept.

IN PROGRESS:
- reference implementation and verification.

BLOCKED:
- none.

NEXT ACTION:
- build locally in isolated workspace; compile; run unit/integration/negative tests; only then persist code/evidence here.
