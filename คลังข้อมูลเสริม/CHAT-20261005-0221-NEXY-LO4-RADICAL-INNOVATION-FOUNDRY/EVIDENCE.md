# Verification Evidence

Classification: `EXECUTED REFERENCE-LAB EVIDENCE`
Actual NEXY runtime/deployment evidence: `NOT VERIFIED`

## Evidence classes
- E1 compile/static: PASS.
- E2 unit/adversarial: PASS.
- E2 stress: PASS in the recorded local environment.
- E3 integrated five-system reference pipeline: PASS.
- E5 actual NEXY runtime: NOT_VERIFIED.
- E6 deployment: NOT_VERIFIED.

## Reproducible command
```bash
./verify.sh
```

## Fresh verified results
- `COMPILE_PASS`
- `STATIC_GUARD_PASS banned_imports=0 banned_calls=0`
- `Ran 31 tests ... OK`
- seeded fuzz loop: 250 iterations inside unit suite
- `STRESS_PROBE_PASS surprise_dims=20000 alternatives=10000 relaxation_candidates=18 regret_actions=5000 option_choices=5000`
- `DEMO_DETERMINISM_PASS`

## Tested invariants
- nonzero SBC drift at USER_LAW/CANON freezes
- MRPE cannot relax USER_LAW/CANON/non-relaxable constraints
- MRPE bound overflow fails closed
- REP excludes illegal actions before regret-baseline calculation
- irreversible actions without explicit human gate are blocked
- OPC rejects unknown future-option IDs and hard-constraint-failing choices
- tested permutations produce identical fingerprints
- integrated result remains Lo4 and requires external promotion authority

## Failure → correction → re-verification
Two useful defects were found during execution.

1. Stress harness initially supplied `SurprisePolicy(total_budget=10^12)`, violating the engine’s explicit maximum `10^9`. Root cause was invalid test input. The harness was corrected to `10^9`, still above the synthetic workload requirement, and the entire verification sequence was rerun successfully.

2. An earlier manifest design included a live verification log while that log was still being appended, which could produce a stale digest. The rule was corrected to exclude the live log and the manifest itself. Verification was rerun.

These failures are preserved because hiding them would make the evidence worse, not prettier.

## Claim boundary
Stress results prove successful execution at the stated synthetic sizes in the local reference environment. They are not production SLAs, do not prove current NEXY integration, and do not establish deployment readiness.
