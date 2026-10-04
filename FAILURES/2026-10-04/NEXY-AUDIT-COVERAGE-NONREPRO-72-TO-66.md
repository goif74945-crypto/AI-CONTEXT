FAILURE_ID: NEXY-AUDIT-COVERAGE-NONREPRO-72-TO-66
status: OPEN / AUDIT-INTEGRITY
source_matrix: REFERENCES/NEXY/2026-10-04/NEXY_SPEC_CODE_AUDIT_ROWS_BA33C8F.csv
baseline_tree: 8a3ae328c1956c661bc2b1561de1a791a7856a7e
previous_claim: 72/301 inherited-current controls by immutable evidence identity
reproduction:
- strict exact evidence path resolver => 62
- exact path + resolvable directory/** expansion => 66
current_decision:
- use conservative mechanically reproducible 66/301 = 21.93%
- do not use 72/301 as current proof
impact:
- previous audit coverage figure is not independently reproducible from stored evidence under its stated method
prevention:
- persist exact row IDs + resolved evidence paths + blob SHAs + resolver version for every inherited row
