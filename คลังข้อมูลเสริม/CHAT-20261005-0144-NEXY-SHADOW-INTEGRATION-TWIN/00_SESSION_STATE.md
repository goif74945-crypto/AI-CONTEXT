# Temporary Session State — NEXY Shadow Integration Twin

status: IN_PROGRESS
started_at_ict: 2026-10-05T01:44:00+07:00
project_local_chat_id: CHAT-20261005-0144-NEXY-SHADOW-INTEGRATION-TWIN
platform_chat_id: UNKNOWN_NOT_EXPOSED_TO_AGENT
repository: goif74945-crypto/AI-CONTEXT
branch: main
observed_prewrite_head: 2b433f70099ee8484101f6ca2b700503ef4acf5b
classification: AI_PROPOSED_FUTURE_CONCEPT / REFERENCE_IMPLEMENTATION / NOT_NEXY_CANON / NOT_NEXY_INTEGRATED

## Objective
Build a standalone deterministic pre-integration conformance harness that can later sit beside NEXY.AI. It accepts a candidate adapter manifest plus sandbox-produced execution traces, checks explicit protocol and authority invariants, detects replay divergence and hidden side effects, and emits a hash-bound admission witness or fail-closed rejection.

## Scope lock
Writable:
- only this project directory in AI-CONTEXT.

Protected:
- every repository whose name contains NEXY.AI: READ ONLY / NO MUTATION.
- all sibling supplemental project directories: READ ONLY.
- no credentials, secrets, deployment mutation, PRs, branches, settings or workflows outside this project.

## Grounded design facts
- NEXY treats models/adapters as workers, not authority.
- Current context separates design, implementation and runtime evidence.
- DOC-C context defines AgentAdapter-style provider independence, explicit health states, timeouts/cancel, freeze semantics, validation boundaries, no automatic retry by default, and evidence before release.
- Deep source design emphasizes deterministic admission, explicit capability boundaries, no hidden network/dynamic escalation, and fail-closed behavior.
- Existing supplemental work already covers work-orthogonality admission, effect contracts, verified reuse, concurrency/causal merge and tool-contract drift; this project must not duplicate them.

## Current state
COMPLETED:
- AI-CONTEXT bootstrap/kernel/router/rules loaded.
- NEXY overview and selected deep compatibility/admission/determinism context loaded.
- supplemental root enumerated for collision review.
- direct search for shadow integration / differential trace / adapter certification returned no hits.
- local Node.js v22.16.0 and TypeScript 5.8.3 availability verified.

IN_PROGRESS:
- architecture, schemas, implementation and deterministic test suite.

BLOCKED:
- none.

NEXT:
- implement locally, run E1/E2/E3 verification, repair all failures, publish tested bytes, re-read from GitHub and bind evidence to commit/file identity.

## Stop conditions
- any required write to a NEXY.AI repository;
- semantic collision with an existing project discovered later;
- material authority conflict;
- inability to produce required static/unit/CLI evidence.
