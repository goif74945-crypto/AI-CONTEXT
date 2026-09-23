LEDGER_ID: NEXY-COVERAGE-REPAIR-20260924-c94ad3
claim: runtime validation now executes on Railway against the target private branch.
proof: Railway deployment metadata and gate logs.
status: VERIFIED

claim: 8ee2ccfc validation passed npm_ci, prisma_generate, typecheck, contract, integration, full suite, coverage measurement, DOC-C, and web build.
proof: NEXY_GATE_END markers exit=0; full suite 86 files/635 tests passed.
status: VERIFIED

claim: coverage_check failed because API domain is below 85% under all four metrics.
proof: Railway check:coverage output lines=64.62 statements=63.43 functions=72.33 branches=56.11; exit=1.
status: VERIFIED

claim: repair commit c94ad368 adds focused runtime tests without weakening thresholds.
proof: GitHub commit contains three new tests under tests/coverage and no check-coverage threshold changes.
status: VERIFIED_STATIC

claim: repair validation is not complete yet.
proof: Railway deployment 2027f4a6-2ab7-467e-a0c2-2cee621efd44 status BUILDING at last check.
status: VERIFIED_AT_TIMESTAMP
trace_id: NEXY-COVERAGE-REPAIR-20260924-c94ad3
