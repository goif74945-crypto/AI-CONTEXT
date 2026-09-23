CASE_ID: NEXY-COVERAGE-REPAIR-20260924-c94ad3
cause: validation infrastructure became functional and exposed a genuine API coverage gate failure.
impact: release validation remains failed despite functional correctness/build gates passing.
fix: expand runtime coverage across low-covered API control planes; preserve threshold authority.
prevention: keep exact gate markers and per-domain coverage reports in validation evidence.
status: OPEN_VALIDATION
trace_id: NEXY-COVERAGE-REPAIR-20260924-c94ad3
