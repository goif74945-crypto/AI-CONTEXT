# Test / Requirement Matrix

| Requirement | Evidence |
|---|---|
| Commutative unordered writes may PASS | `test_commutative_additions_are_confluent` |
| Divergent writes FAIL with two schedules | `test_unordered_sets_produce_divergence_witness` |
| Explicit dependency can serialize | `test_dependency_serializes_divergent_writes` |
| Order-sensitive precondition FAIL | `test_order_sensitive_precondition_is_failure` |
| Intermediate invariant violation FAIL | `test_intermediate_invariant_violation_fails_even_if_later_action_could_repair` |
| Invalid cycle/missing dependency FREEZE | cycle + missing dependency tests |
| Exact cap exhaustion FREEZE | state/transition limit tests |
| Reachable type error FAIL | `test_runtime_type_error_is_decisive_plan_failure` |
| Path-prefix conflicts detected | `test_parent_child_paths_conflict` |
| Input action order does not alter report | input-order determinism + oracle permutation tests |
| Ambiguous operation fields rejected | copy/set irrelevant-field regression tests |
| Floating point rejected | `test_float_values_freeze_for_cross_runtime_determinism` |
| State merging remains exact | 64-program brute-force oracle |
| Large schedule collapse is exact | 10-action test: 10! schedules -> 1024 states / 5120 transitions |
| CLI status maps to exit codes | five CLI tests |
| Python syntax/importability | compileall E1 |

## Regression history
An adversarial schema test exposed that the initial validator accepted irrelevant fields on effect objects. Two new tests failed before the repair. The validator was tightened and those tests now pass. This is preserved as evidence that negative-path validation was not assumed from code presence.
