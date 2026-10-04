# 07 — Requirement / Evidence Ledger

| ID | Requirement | Authority | Implementation | Evidence | Status |
|---|---|---|---|---|---|
| DEF-R01 | New accepted directive establishes a logical epoch | AI proposal | `engine.apply` | unit tests | PASS |
| DEF-R02 | Replace invalidates prepared old-epoch action | user objective + proposal | `apply` + `commit_gate` | unit + fixture | PASS |
| DEF-R03 | Narrow cannot expand action authority | proposal invariant | `apply` NARROW | negative unit | PASS |
| DEF-R04 | Revoke blocks old work | proposal invariant | `apply` REVOKE | unit | PASS |
| DEF-R05 | Exact payload tamper is detected | security invariant | action digest recomputation | negative unit | PASS |
| DEF-R06 | Duplicate event ID cannot substitute content | idempotency invariant | event ID -> digest registry | negative unit | PASS |
| DEF-R07 | Irreversible action requires exact approval binding | user-safety proposal | `expected_approval_binding` + gate | unit | PASS |
| DEF-R08 | Journal detects tamper | replay/integrity invariant | hash chain | negative unit | PASS |
| DEF-R09 | Replay reproduces commit-induced FREEZE | recovery invariant | full protocol journal replay | unit | PASS |
| DEF-R10 | Stale action never ALLOWs under randomized mutation trials | stress invariant | adversarial validator | 5,000 deterministic trials | PASS |
| DEF-R11 | Standalone code has valid Python syntax | build integrity | all Python modules | compileall | PASS |
| DEF-R12 | Proposed integration does not claim current NEXY implementation | authority boundary | docs/status labels | artifact inspection | PASS |
| DEF-R13 | No repository whose name contains NEXY.AI is mutated | explicit user prohibition | write target lock | GitHub write target/audit | PASS for actions performed in this session |
| DEF-R14 | Production atomic gate-to-side-effect race is solved | future adoption requirement | not implemented | none | NOT_VERIFIED |
| DEF-R15 | Cryptographic operator approval is enforced | future adoption requirement | not implemented | none | NOT_VERIFIED |
| DEF-R16 | Distributed epoch consistency is proven | future adoption requirement | not implemented | none | NOT_VERIFIED |
