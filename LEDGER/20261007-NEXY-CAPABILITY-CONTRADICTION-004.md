# Ledger — NEXY Capability Contradiction

LEDGER_ID: LEDGER-20261007-NEXY-CAPABILITY-CONTRADICTION-004
TASK_ID: 20261007-NEXY-CAPABILITY-CONTRADICTION-004
TIMESTAMP_UTC: 2026-10-07T16:04:52Z
PARENT_AI_CONTEXT_HEAD: ee9ad9a561d64241fc93f3da37709b76cd070489
CHECKPOINT_COMMIT: b2d9626e89da4b9610114e308bf380c6913c7312

| Seq | Action | Evidence | Result |
|---:|---|---|---|
| 1 | Read latest command and blocked evidence | AI-CONTEXT/ee9ad9a561d64241fc93f3da37709b76cd070489 | Read; exact-head fail-closed rules apply |
| 2 | Re-query runtime | Repo Code Bridge runtime status | Runtime snapshot says no read-only repositories; backend READY |
| 3 | Re-query product | `NEXY.ai` | Snapshot says read_only=false, gateway ALLOW |
| 4 | Test actual CI capability | `ci_dispatch(omega-runner-diagnostic.yml, 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43)` | 403 REPOSITORY_READ_ONLY; dispatch denied |
| 5 | Resolve contradiction | Locked command | Actual denial is the blocker; no product edit |
| 6 | Persist task/case/failure/ledger/evidence | AI-CONTEXT/main commit b2d9626e89da4b9610114e308bf380c6913c7312 | Committed without force |
| 7 | Read-back gate | AI-CONTEXT/main after commit | To be checked in the final verification pass |

## Ruling

Ruling: actual operation denial overrides a permissive status snapshot — the cost if wrong is a delayed repair, which is safer than mutating a repository while CI/evidence capability is unproven.

## Gate

- Product branch exact: YES
- Product HEAD unambiguous: YES
- Authority hash exact: YES
- Product write capability: NOT PROVEN
- CI dispatch capability: NO
- Product mutation: NO
- PASS_100: NO
- Status: BLOCKED_WITH_RESUME
