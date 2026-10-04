# Task Contract

## Objective
Create five materially distinct, NEXY-compatible, AI-proposed progressive-delivery safety systems with executable reference code, adversarial tests, integration proof, non-duplication evidence, and durable resumable state.

## Target
- Repository: `goif74945-crypto/AI-CONTEXT`
- Branch: `main`
- Write root: `คลังข้อมูลเสริม/CHAT-20261005-0157-NEXY-VERIFIED-PROGRESSIVE-DELIVERY-FABRIC/`

## Authorized scope
- Create new files only under the write root.
- Read AI-CONTEXT project/rules/adjacent supplemental work for authority and collision analysis.
- Execute authored code/tests in an isolated local container.
- Persist test/evidence artifacts whose provenance is explicit.

## Protected scope
- Any repository whose name contains `NEXY.AI`.
- Existing files outside the mission root.
- Canonical NEXY law/spec.
- Production/deployment state.
- Secrets/credentials.

## Immutable requirements
1. Exactly five named systems, each explicitly `AI_PROPOSED_CONCEPT / EXPERIMENTAL / NOT_CANON`.
2. Deterministic results for equal normalized inputs.
3. Fail closed on malformed, stale, conflicting, or materially insufficient evidence.
4. No model/network/subprocess execution from core library code.
5. No claim that NEXY.AI currently implements these systems.
6. No silent relaxation of NEXY authority, evidence, freeze, privacy, or safety semantics.
7. Positive, negative, adversarial, determinism, and cross-engine integration tests.
8. Exact tested source/test content must be persisted and read back.
9. Design + Code + Test + Evidence must remain together under this mission root.

## Concepts
- C1 CohortLock: stable deterministic cohort assignment under versioned rollout policy.
- C2 TraceDelta: compare canonical behavioral traces and block unapproved semantic drift.
- C3 BlastBudget: enforce explicit maximum user/execution exposure and hard criticality limits.
- C4 EvidenceCohesion: prove evidence belongs to one exact release/cohort/policy/time window.
- C5 PromotionMachine: state machine STAGED → CANARY → EXPAND → FULL or FREEZE/ROLLBACK, driven only by valid receipts.

## Required evidence
- E0: durable file presence + read-back.
- E1: `python -m compileall` and import validation on exact authored source.
- E2: executed `unittest` suite including negative/adversarial cases.
- E3: executed end-to-end library integration across all five engines.
- Determinism: repeated execution and canonical hash equality.
- Scope audit: created paths remain under mission root; no NEXY.AI repository mutation.

## Acceptance criteria
- Five callable engines exist independently.
- At least 30 executed assertions/tests across focused + integration coverage.
- Core invalid inputs deterministically produce explicit exceptions/blocks rather than permissive defaults.
- Integration scenario demonstrates safe promotion and at least one forced FREEZE.
- All executed tests pass after repairs.
- Evidence records include command, environment, observed result, and limitations.
- Persisted tested artifacts match locally computed SHA-256 digests.

## Completion law
STATUS COMPLETE is legal only after exact persisted files are read back and hash-matched to the tested local files, with no blocking test or scope finding.
