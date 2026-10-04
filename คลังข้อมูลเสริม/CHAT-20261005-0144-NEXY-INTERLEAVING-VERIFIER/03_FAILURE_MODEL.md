# Failure Model

| Code / decision | Verification status | Meaning | Recovery |
|---|---|---|---|
| `CONFLUENT` | PASS | Complete bounded state space converges and preserves invariants | Candidate for higher-level integration testing |
| `DIVERGENT_TERMINAL_STATE` | FAIL | Two legal schedules end in different canonical states | Add/resolve ordering authority or redesign operations |
| `PRECONDITION_FAILURE` | FAIL | A mandatory action becomes unrunnable on a reachable schedule | Strengthen dependencies or redesign precondition/plan |
| `INVARIANT_VIOLATION` | FAIL | Initial or reachable post-action state violates invariant | Fix action semantics/order/invariant contract |
| `EXECUTION_MODEL_ERROR` | FAIL | Valid DSL operation cannot execute on reachable state type/path | Fix model/state/action contract |
| `FREEZE_INVALID_INPUT` | NOT_VERIFIED | Invalid schema, unknown field/op, missing dependency, cycle, nondeterministic value class | Correct model; do not infer result |
| `FREEZE_LIMIT` | NOT_VERIFIED | Exact state/transition budget exhausted before proof | Increase cap, partition model, or add justified ordering constraints |
| `FREEZE_IO_OR_JSON` | NOT_VERIFIED | CLI could not read/parse/write | Correct I/O; rerun |

## Important distinction
`FAIL` means the verifier has a counterexample. `FREEZE` means it cannot legally make the requested proof claim.

## Anti-patterns explicitly rejected
- random schedule sampling presented as race proof;
- stopping exploration at cap and returning PASS;
- silently choosing an order to hide divergence;
- ignoring failed mandatory preconditions;
- checking only final state while allowing intermediate invariant violations;
- treating static conflict absence as a confluence proof;
- allowing arbitrary code callbacks inside the transition model.
