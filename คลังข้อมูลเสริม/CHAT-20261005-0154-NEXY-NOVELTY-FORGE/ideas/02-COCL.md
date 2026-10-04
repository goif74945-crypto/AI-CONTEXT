# 02 — Counterfactual Outcome Credit Ledger (COCL)

Status: **AI-PROPOSED REFERENCE SYSTEM — NOT CAUSAL PROOF**

Purpose: attribute a supplied outcome-delta across a bounded set of actions using an exact complete-coalition Shapley-style accounting model.

Implementation: `../src/causal-credit.ts`
Tests: `../tests/run-tests.ts`
Evidence: `../EVIDENCE.md`

Key invariants: complete `2^n` coalition table; bounded action count; deterministic action ordering; contribution conservation residual is exposed; result is labeled `COUNTERFACTUAL_CONTRIBUTION_NOT_CAUSAL_PROOF`.

Failure model: incomplete/non-finite counterfactual tables or duplicate action IDs fail closed.
