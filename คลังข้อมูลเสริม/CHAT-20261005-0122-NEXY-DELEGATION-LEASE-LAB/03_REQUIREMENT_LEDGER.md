# 03 — Requirement Ledger

Status below refers only to this standalone reference prototype, not NEXY production.

| ID | Requirement | Prototype location | Evidence | Status |
|---|---|---|---|---|
| DL-001 | Lease binds to exact plan hash | `canonical.py`, `policy.py` | E2 | PASS |
| DL-002 | Changed plan blocks execution | `evaluate_action` | E2 | PASS |
| DL-003 | Resource out-of-scope blocks | `evaluate_action` | E2 | PASS |
| DL-004 | Verb out-of-scope blocks | `evaluate_action` | E2 | PASS |
| DL-005 | Effect out-of-scope blocks | `evaluate_action` | E2 | PASS |
| DL-006 | High-impact action needs explicit second gate | `evaluate_action` | E2 | PASS |
| DL-007 | Expired lease blocks | `evaluate_action` | E2 | PASS |
| DL-008 | Not-yet-active lease blocks | `evaluate_action` | E2 | PASS |
| DL-009 | Revoked lease blocks | `revoke`, `evaluate_action` | E2 | PASS |
| DL-010 | Action budget is finite | `LeaseState`, `evaluate_action` | E2 | PASS |
| DL-011 | Cost budget is finite | `LeaseState`, `evaluate_action` | E2 | PASS |
| DL-012 | Evaluation does not mutate counters | `evaluate_action` | E1/E2 | PASS |
| DL-013 | Frozen decision cannot be committed | `commit_allowed_action` | E2 | PASS |
| DL-014 | Child lease cannot broaden verbs/effects | `derive_child_lease` | E2 | PASS |
| DL-015 | Child lease cannot exceed budget/expiry | `derive_child_lease` | E2 | PASS |
| DL-016 | Child cannot introduce high-impact authority | `derive_child_lease` | E2 | PASS |
| DL-017 | Unproven wildcard containment rejects | `_resource_scope_is_subset` | E2 | PASS |
| DL-018 | Policy version mismatch blocks | `evaluate_action` | E2 | PASS |
| DL-019 | Same inputs yield same tested decision | unit test loop | E2 | PASS |
| DL-020 | Destination changes are drift | `diff_plans` | E2 | PASS |
| DL-021 | Journal detects chain tampering | `journal.py` | E2 | PASS |
| DL-022 | Provider-specific resource aliases cannot bypass scope | not implemented | E3/E4 security | NOT_VERIFIED |
| DL-023 | Evaluation + accounting atomic under concurrency | not implemented | E3/E5 | NOT_VERIFIED |
| DL-024 | Lease issuance cryptographically attributable | not implemented | E3 security/auth | NOT_VERIFIED |
| DL-025 | Revocation propagates across distributed executors | not implemented | E3/E5 | NOT_VERIFIED |
| DL-026 | Real NEXY RBAC/LAW integration preserves restrictions | no NEXY mutation | E3/E4 | NOT_VERIFIED |
| DL-027 | UX reduces prompts without unsafe approvals | no study | usability/evals | NOT_VERIFIED |
| DL-028 | Deployment behavior is safe | no deployment | E6 | NOT_VERIFIED |

A PASS here means the named reference behavior was executed with matching local evidence. It does not promote the proposal into NEXY law.
