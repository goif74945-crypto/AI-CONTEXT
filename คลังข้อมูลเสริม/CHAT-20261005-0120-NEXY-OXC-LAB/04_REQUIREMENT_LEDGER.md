# OXC Requirement Ledger

Classification: **EXPERIMENTAL / AI-PROPOSED**

| ID | Requirement | Authority / rationale | Implementation | Evidence | Status |
|---|---|---|---|---|---|
| OXC-R01 | Presentation must not change Core truth | NEXY Human/UX authority boundary | SurfacePlan copies truth/state; no truth mutation API | unit + architecture review | PASS E2 |
| OXC-R02 | Presentation must not grant authority | NEXY visible ≠ editable ≠ executable; user directive | denial accumulator; backendAllowed gate | 576-case matrix + focused tests | PASS E2 |
| OXC-R03 | FREEZE must remain visible | NEXY UI truth/fail-safe design | mandatory FREEZE banner/signal | focused FREEZE test | PASS E2 |
| OXC-R04 | STOP must fail closed for write/recovery | proposal safety invariant | STOP denial rule | STOP negative-path test | PASS E2 |
| OXC-R05 | VIEW must remain read-only for mutate/recovery | NEXY mode semantics / proposal boundary | VIEW_MODE_READ_ONLY | focused test | PASS E2 |
| OXC-R06 | Preference must be presentation-only | Human Gravity imperfection firewall | preferences read only in disclosure/output presentation | pairwise + 36-combination metamorphic test | PASS E2 |
| OXC-R07 | Invalid contract values must not be guessed | AI-CONTEXT no silent guessing | runtime validators | invalid role/friction/state-list tests | PASS E2 |
| OXC-R08 | Duplicate action identity must be rejected | deterministic identity integrity | duplicate-id check | negative-path test | PASS E2 |
| OXC-R09 | Dangerous actions need monotonic friction | NEXY explicit-confirmation direction | max-friction compiler | critical irreversible test | PASS E2 |
| OXC-R10 | Core compiler must avoid hidden I/O/time/randomness | determinism / inspectability | pure TypeScript source | source/static inspection + tsc | PASS E1 for source property; runtime side-channel audit NOT PERFORMED |
| OXC-R11 | Exact source published must match tested source | evidence law | Git blob transfer | GitHub blob IDs == local git hash-object for 6 files | PASS E0/E1 lineage |
| OXC-R12 | Proposal must remain non-canonical until promotion | Memory law | labels throughout docs | document inspection | PASS E0 |
| OXC-R13 | NEXY implementation repo must remain unmodified | explicit user constraint | work confined to AI-CONTEXT | connector actions used only against AI-CONTEXT | PASS within observed tool history |
| OXC-R14 | Real UI/backend integration must be proven before production claim | verification law | integration plan only | no E3/E4 executed | NOT_VERIFIED |

## Status rule

PASS above applies only to the stated reference claim and evidence class. It does not imply NEXY production integration, UI E2E correctness or release readiness.
