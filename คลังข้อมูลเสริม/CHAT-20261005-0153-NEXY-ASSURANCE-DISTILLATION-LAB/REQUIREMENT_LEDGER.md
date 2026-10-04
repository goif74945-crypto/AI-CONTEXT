# Requirement Ledger

| ID | Requirement | Authority | Implementation | Evidence | Status |
|---|---|---|---|---|---|
| R01 | Work only in AI-CONTEXT supplemental project folder | User directive | repository path boundary | final path/read-back | PASS when committed |
| R02 | Do not mutate any NEXY.AI repository | User directive | no NEXY tool mutation path used | operation audit | PASS |
| R03 | Produce five novel/non-duplicative concepts | User directive | CED/MUCF/EFRP/SECL/VRPP | repository search returned zero direct hits for selected concept phrases | PASS with limited novelty scope |
| R04 | Clearly label ideas as AI-proposed | User directive / truth separation | docs + session state | document inspection | PASS |
| R05 | Write real code | User directive | \`src/nexy_aqt/*\` | E0 + blob identity | PASS |
| R06 | Run tests and repair failures | User directive / verification law | unit/negative/CLI suites | 24/24 and 21/21 logs | PASS |
| R07 | Counterexample reduction preserves protected nested paths | design invariant | counterexample.py | negative/regression tests | PASS |
| R08 | Unsat analysis bounded and deterministic | design invariant | unsat_core.py | unit/bound tests | PASS |
| R09 | Stale/future/version-drift evidence cannot PASS | design invariant | freshness.py | unit/negative tests | PASS |
| R10 | Contradictory examples are surfaced | design invariant | example_linter.py | unit tests | PASS |
| R11 | Recovery paths require declared evidence | design invariant | recovery.py | positive/negative tests | PASS |
| R12 | CLI malformed input freezes | design invariant | cli.py | subprocess test | PASS |
| R13 | Deterministic no-hidden-network core | design invariant | all engine modules | source inspection + tests | PASS for reference code |
| R14 | Live NEXY integration works | future adoption requirement | none | E3/E4 against NEXY required | NOT_VERIFIED |
| R15 | Production performance/scalability | future adoption requirement | none | load/runtime evidence required | NOT_VERIFIED |
