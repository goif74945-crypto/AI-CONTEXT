# NEXY Clarification Optimizer Lab — Mission State

Status: EXECUTING
Created: 2026-10-05T01:20+07:00
Storage: goif74945-crypto/AI-CONTEXT
Authorized write scope: this directory only
Protected scope: every repository whose name contains "NEXY.AI"; all existing sibling work under คลังข้อมูลเสริม

## Session identity
- Platform immutable chat/conversation ID: UNKNOWN — not exposed by the available toolset.
- Durable session reference (local project identifier, NOT a platform chat ID): CHAT-20261005-0120-NEXY-CLARIFICATION-OPTIMIZER

## Objective
Design and build an additive, testable reference system that computes the smallest deterministic clarification set required to unblock an execution contract when material unknowns remain, without guessing missing intent.

## Authority
1. Current explicit user directive.
2. AI-CONTEXT/AI-EXECUTION-KERNEL.md.
3. projects/NEXY.AI canonical context and current 837-row normalization boundary.
4. Existing supplemental work, used only for de-duplication.

## Scope lock
IN SCOPE:
- new design/specification, reference implementation, tests, fixtures, validation evidence, and future-adoption notes inside this directory;
- additive-only work;
- AI-proposed concepts clearly marked as proposals.

OUT OF SCOPE / PROTECTED:
- modifying any repository whose name contains "NEXY.AI";
- changing existing AI-CONTEXT canonical NEXY project files;
- claiming this proposal is current NEXY implementation;
- inventing implementation/runtime evidence;
- copying secrets or personal data.

## Non-duplication finding
Existing supplemental work already covers semantic contracts, specification compilation, epistemic control, evidence graphs, counterfactual impact, knowledge decay, assurance, capacity economics, and long-horizon reliability.
This mission is intentionally orthogonal: optimize the human clarification boundary after ambiguity is detected, minimizing operator burden while preserving no-guess and human-authority rules.

## Proposed system
Working name: NEXY Clarification Optimizer (NCO)
Truth class: AI_PROPOSAL / NOT_CURRENT_REQUIREMENT

Core idea:
Ambiguity detection remains upstream. NCO receives explicit unresolved variables and dependency/coverage relationships, then deterministically chooses a minimal legal set of clarification questions. It never infers missing answers.

## Acceptance criteria
- deterministic output for equivalent canonical input;
- no guessed answer generation;
- only blocking unresolved variables influence release;
- chosen questions cover every blocking variable or return BLOCKED with uncovered proof;
- stable tie-breaking;
- machine-readable decision trace;
- tests cover normal, redundant-question, dependency, uncovered, cycle/invalid, and determinism cases;
- reference code executes successfully in an isolated local test environment before completion is claimed.

## Execution state
COMPLETED:
- Read AI-CONTEXT index and execution kernel.
- Read NEXY overview, requirements, product/human-control context, current source matrix.
- Enumerated supplemental knowledge tree (350 entries) to avoid duplicate mission selection.
- Compared against semantic-contract and spec-compiler proposals.

IN PROGRESS:
- Formal algorithm and data contract.
- Reference implementation and tests.

NEXT:
1. Write specification.
2. Implement deterministic optimizer.
3. Run tests locally.
4. Correct failures.
5. Persist code/tests/evidence.
6. Read back every persisted file and final-audit.

## Stop conditions
FREEZE if a write would touch protected scope, if a required file path collides with existing content, or if verification evidence cannot be obtained.


## Checkpoint CP-01 — 2026-10-05
Persistence: durable read-after-write verified for 01_SPEC.md.
Local reference implementation state: NOT YET PERSISTED.
Local executed evidence:
- unittest suite: 13 tests PASS.
- deterministic exhaustive-oracle cross-check: 250 generated problems PASS.
- validated behaviors: READY/no-blocker, multi-blocker cover, exact minimum total cost, canonical tie-break, uncovered blocker BLOCKED, cost-budget BLOCKED, input validation, order-invariant SHA-256 fingerprint.
Evidence limitation:
- tests were executed in the session's local container, not GitHub Actions.
- code must still be persisted and read back before repository-level completion.
Next legal action:
- add JSON/CLI boundary and additional metamorphic/scale tests, then persist implementation + tests + evidence.
