# NEXY Multi-Principal Authority Lattice (MPAL)

**Status:** `AI_PROPOSED / EXPERIMENTAL / REFERENCE_IMPLEMENTATION / NOT_CURRENT_NEXY_REQUIREMENT / NOT_RUNTIME_PROOF`

MPAL is supplemental NEXY.AI research for deterministic joint authority across multiple human principals in future team, enterprise, or high-impact workflows.

> Given a versioned authority policy, a request, and approval/veto receipts, is the legal state `ALLOW`, `DENY`, `PENDING`, or `FREEZE`?

MPAL does **not** modify NEXY.AI, replace current RBAC, create current product requirements, or prove that any NEXY runtime implements this behavior.

## Why this may matter
Future multi-user NEXY deployment can create valid but partial authority across Owner, Security, Finance, Operator, etc. A machine-checkable joint-authority contract can answer who had authority, which gate is missing, and why execution is blocked without asking AI to decide which human “wins.”

Examples include Security + Operations release quorum, Owner + Finance payout, Security veto, maker-checker separation, stale approval invalidation, and contradiction freezing.

## Reference implementation
- `mpal_engine.py` — policy validator/evaluator + CLI.
- `model_check.py` — bounded exhaustive fixture checker.
- `fixtures/` — policy/request/approval examples.
- `tests/test_mpal_engine.py` — unit + negative-path tests.

## MPAL operational states
These are not AI-CONTEXT verification statuses:
- `ALLOW`: all configured authority gates satisfied.
- `DENY`: policy-defined negative authorization/veto.
- `PENDING`: legal request still lacks current approvals.
- `FREEZE`: authority evidence is malformed, stale, contradictory, ambiguous, or integrity-breaking.

## Key invariants
1. Policy version binds request and receipts.
2. Receipts bind canonical request SHA-256.
3. Approval order cannot change legal decision.
4. Duplicate identical receipts do not count twice.
5. Contradictory receipts freeze.
6. Self-approval can be forbidden.
7. Veto is explicit policy, never AI inference.
8. Unknown actions deny rather than invent rules.
9. Unsatisfiable quorum is rejected/frozen.
10. AI output never creates human authority.

## Pre-write evidence
- Python compilation: PASS.
- Unit/negative tests: 49/49 PASS.
- engine coverage: 90%; total measured coverage: 94%.
- bounded exhaustive model: 256 vectors; all configured invariants PASS.

These results apply only to this standalone prototype.

## Navigation
`00_EXECUTION_STATE.md`, `01_TASK_CONTRACT.md`, `02_SOURCE_ALIGNMENT.md`, `03_ARCHITECTURE.md`, `04_POLICY_PROTOCOL.md`, `05_SECURITY_FAILURE_MODEL.md`, `06_EXPERIMENTAL_FUTURE_EXTENSIONS.md`, `07_VERIFICATION_EVIDENCE.md`, and final `99_FINAL_AUDIT.md`.
