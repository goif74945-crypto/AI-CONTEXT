# 04 — Semantic Entropy Guard (SEG)

Status: **AI-PROPOSED REFERENCE SYSTEM — ADVISORY ONLY**

Purpose: preserve disagreement information that ordinary consensus may erase by measuring structured decision coverage and normalized entropy per semantic dimension.

Implementation: `../src/semantic-entropy-guard.ts`
Tests: `../tests/run-tests.ts`
Evidence: `../EVIDENCE.md`

Key invariants: at least two independent workers; duplicate workers rejected; missing decisions reduce coverage; critical low-coverage/high-entropy dimensions may request advisory FREEZE; ordering does not change the result.

Numeric limitation: current standalone implementation uses JavaScript floating point. Authoritative NEXY promotion would require canonical fixed-point/Q64.64 migration and fresh proof.
