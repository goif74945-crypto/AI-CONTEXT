# Final Local Verification Summary

Captured against the final local FAAL source before AI-CONTEXT publication.

## Verdict

`LOCAL_VERIFICATION: PASS`

This is E1/E2/E3-local evidence only. It is not production/deployment proof.

## Executed checks

| Check | Observed result |
|---|---|
| Full unittest discovery | 71 tests, 0 failures/errors |
| Python compileall | exit 0 |
| Core AST policy audit | 8 files scanned, 0 findings |
| Deterministic replay | 30 checks PASS |
| Integrated bundle identity | `6b8b9791eec4f14e3cda14c9b4748c9d396a1adfb128c2a4d23fb22a8dd37d1a` |
| Adversarial matrix | 100 cases PASS |
| Mutation sensitivity | 5/5 mutations killed; 0 survivors |
| PYTHONHASHSEED replay | seeds 0, 1, 42, 999 all same identity and PASS |
| Secret-pattern scan | 0 matching bytes for configured patterns |
| Final exit matrix | all recorded checks exit 0 |

## TDD / remediation evidence

- Initial import RED recorded in `RED_IMPORT.txt`.
- Behavioral RED after API skeleton: 67 tests loaded, 48 failures + 9 errors.
- First implementation GREEN attempt left one swarm failure.
- Root cause fixed: absent tool/data metadata can no longer masquerade as independence.
- Resource-limit hardening was test-first: four new resource-bound tests observed failing before checks were added.
- Final suite after hardening/refactor: 71/71 PASS.
- First adversarial verifier contained a lexical-order assumption bug; verifier was fixed and 100-case matrix rerun PASS.

## Performance characterization

Raw data: `BENCHMARK_FINAL.json`.

Observed on this execution environment, not an SLA:
- uncertainty derive: 4,471 ns/call over 20,000 repeats;
- impact chain 500: 651,840 ns/call over 20 repeats;
- exact swarm 20 choose 6: 566,164,799 ns for one bounded worst-pool selection;
- FSM validate 100: 95,188 ns/call;
- FSM simulate 100: 122,867 ns/call;
- compress 1,000 exact duplicates: 2,405,664 ns/call.

## Remaining verification boundary before task completion

Remote publication to `goif74945-crypto/AI-CONTEXT` and exact read-back verification remain required before R11 can be PASS.
