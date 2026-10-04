# Requirement and Evidence Ledger

All IDs below are **lab proposal requirements**, not canonical NEXY.AI requirements.

| ID | Requirement | Evidence | Status |
|---|---|---|---|
| R-001 | Default policy blocks resources targeting repo names containing `NEXY.AI` | tests 13, 37 | PASS E2 |
| R-002 | Canonical serialization independent of object key order | test 1 | PASS E2 |
| R-003 | Unsafe/non-integral JS numbers rejected from canonical identity | test 2 | PASS E2 |
| R-004 | Policy hash binds canonicalized policy material | tests 35, 36, 46 | PASS E2 |
| R-005 | Caller action permutations preserve plan identity | tests 4, 41 | PASS E2 |
| R-006 | Dependency graph rejects invalid/cyclic structure | tests 10, 11 + static inspection | PASS/PARTIAL coverage |
| R-007 | Independent actions produce deterministic waves | test 5 | PASS E2 |
| R-008 | Same-resource side effects require dependency order | tests 6-9 | PASS E2 |
| R-009 | `NONE` cannot hide declared/resource side effects | tests 14, 42 | PASS E2 |
| R-010 | non-`NONE` requires declared operation + side-effecting access | tests 15, 43 | PASS E2 |
| R-011 | Mutated resources require preconditions under default policy | test 16 | PASS E2 |
| R-012 | Preconditions cannot target undeclared resources | test 44 | PASS E2 |
| R-013 | Preflight exact hash state required | tests 27, 28 | PASS E2 |
| R-014 | Preflight observation set must be exact | tests 29, 30 | PASS E2 |
| R-015 | Post-compile plan tamper invalidates preflight | test 38 | PASS E2 |
| R-016 | Configured effect classes require idempotency | tests 17, 18 | PASS E2 |
| R-017 | Mutations require valid reversibility metadata | test 19 | PASS E2 |
| R-018 | Reversible mutations require rollback | test 20 | PASS E2 |
| R-019 | Rollback coverage equals mutated-resource set | test 21 | PASS E2 |
| R-020 | Rollback effect class must be policy-legal | test 45 | PASS E2 |
| R-021 | Irreversible actions default-denied and approval-gated if enabled | tests 22-24 | PASS E2 |
| R-022 | Risk/effect policy boundaries fail closed | tests 25, 26 | PASS E2 |
| R-023 | Compensation order is reverse topological | test 31 | PASS E2 |
| R-024 | Unknown/irreversible completed actions block compensation | tests 32, 33 | PASS E2 |
| R-025 | Plan tamper invalidates compensation | test 39 | PASS E2 |
| R-026 | Structural NEXY adapter requires no NEXY source import | test 34 + source inspection | PASS E1/E2 |
| R-027 | Default max-action boundary is 256/257 | test 40 | PASS E2 |
| R-028 | Compiled artifacts deeply frozen | test 47 | PASS E2 |
| R-029 | Strict TypeScript validation | `npm run typecheck` | PASS E1 |
| R-030 | Full suite passes after final source mutation | `npm run verify`, 47/47 | PASS E1/E2 |
| R-031 | Tested source archive reconstructs and re-verifies | clean restore + 47/47 | PASS E0/E1/E2 |
| R-032 | NEXY repo receives no mutation from this task | tool-action audit | PASS for this session's actions |

## Evidence ceiling

No row claims E3 integration, E4 E2E, E5 runtime durability, E6 deployment or E7 physical proof.
