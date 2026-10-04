# 03 — Verification Value Scheduler (VVS)

Status: **AI-PROPOSED REFERENCE SYSTEM — ADVISORY PLANNER**

Purpose: allocate a finite verification budget across claims while preserving mandatory evidence-class obligations before optional value optimization.

Implementation: `../src/verification-value-scheduler.ts`
Tests: `../tests/run-tests.ts`
Evidence: `../EVIDENCE.md`

Key invariants: required evidence class is never downgraded; impossible mandatory proof returns `BLOCKED`; mandatory spend exceeding budget returns `BLOCKED`; optional selection is deterministic and budget-bounded.

Compatibility boundary: this is a claim/evidence portfolio planner, not a replacement for NEXY Lo3's tester/verifier agent ladder or LAW/JUDGE authority.
