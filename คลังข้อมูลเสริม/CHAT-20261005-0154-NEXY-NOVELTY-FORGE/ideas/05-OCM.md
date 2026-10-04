# 05 — Observed Contract Miner (OCM)

Status: **AI-PROPOSED OFFLINE AUDIT TOOL — OBSERVATION IS NOT AUTHORITY**

Purpose: build a source-to-requirement observation ledger only from explicit machine-readable markers instead of guessing contracts from code or test names.

Implementation: `../src/observed-contract-miner.ts`
Tests: `../tests/run-tests.ts`
Evidence: `../EVIDENCE.md`

Marker: `@nexy-observed-contract {"requirementId":"REQ-X","behavior":"...","evidenceClass":"E2"}`

Key invariants: exact explicit marker only; source path and line retained; marker yields `NOT_VERIFIED`; absence yields `UNKNOWN`; conflicting duplicate observations yield `CONFLICT`; malformed markers are quarantined; every observation is stamped `OBSERVED_NON_AUTHORITY`.
