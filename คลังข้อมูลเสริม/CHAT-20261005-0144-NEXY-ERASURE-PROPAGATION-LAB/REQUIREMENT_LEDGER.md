# Requirement Ledger

Legend: PASS means verified within this standalone reference scope. NOT VERIFIED means the claim needs production/integration evidence.

| ID | Requirement | Status | Evidence |
|---|---|---|---|
| ER-001 | Work is novel relative to existing supplemental deletion backlog | PASS | Selected open R-020 deletion semantics / propagation gap |
| ER-002 | Store work under AI-CONTEXT/คลังข้อมูลเสริม only | PASS | PR #53 merge + post-merge 17/17 exact blob read-back |
| ER-003 | Do not modify any repository whose name contains NEXY.AI | PASS | NEXY repository was read-only compatibility evidence source |
| ER-004 | Code compatible with observed NEXY architecture | PASS | INTEGRATION.md bound to exact NEXY snapshot |
| ER-005 | Separate soft delete from physical erase | PASS | tests + planner |
| ER-006 | Preserve immutable audit history | PASS | APPEND_AUDIT_TOMBSTONE invariant |
| ER-007 | Legal/retention holds block destructive erase | PASS | tests |
| ER-008 | Do not mutate other principals exclusive data | PASS | CROSS_OWNER_MUTATION freeze |
| ER-009 | Shared derivative preserves unrelated owners | PASS | REBUILD_SHARED_DERIVED tests |
| ER-010 | External erasure cannot be claimed locally | PASS | PENDING_EXTERNAL + receipt |
| ER-011 | Missing/dangling/cyclic provenance fails closed | PASS | tests |
| ER-012 | Plan identity deterministic | PASS | graph-order invariance tests |
| ER-013 | Completion requires evidence for every action | PASS | receipt verifier tests |
| ER-014 | Frozen plan explicitly denies execution | PASS | executionAuthorized=false tests |
| ER-015 | Strict source typecheck | PASS | tsc exit 0 |
| ER-016 | Regression suite after final changes | PASS | 36/36 tests |
| ER-017 | Persisted critical suite executable | PASS | 12/12 local run before persistence + exact persisted test blob |
| ER-018 | Production physical erasure proven | NOT VERIFIED | out of standalone scope |
| ER-019 | Backups/replicas erased | NOT VERIFIED | future integration work |
| ER-020 | External providers actually erase data | NOT VERIFIED | requires provider receipts |
| ER-021 | Durable mission checkpoint exists | PASS | STATE.md |
| ER-022 | Future concepts clearly marked AI-proposed | PASS | FUTURE_IDEAS.md |
| ER-023 | Persisted bytes match verified deliverables | PASS | 17/17 main read-back exact Git blob SHA match |
