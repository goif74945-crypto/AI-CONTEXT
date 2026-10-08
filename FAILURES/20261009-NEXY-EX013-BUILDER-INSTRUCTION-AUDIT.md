# FAILURE 20261009-NEXY-EX013-BUILDER-INSTRUCTION-AUDIT
STATUS: OPEN_BLOCKERS_REQUIRING_BUILDER_EXECUTION
FAILED_OBSERVATION: Historical EX012 on connected Windows runner ran 911 Vitest contract+coverage cases; 6 tests failed.
RUNNER_RUST: cargo missing for 2, whether rustc missing for 2 not independently confirmed; alternative authorized connected Linux/Rust runner discovery required.
CURRENT_HEAD: attestation child process returned exit1 in 2 fixtures; implementation-vs-Windows environment not established.
CI: latest exact HEAD 37811868233 completed failure at Product 90fac4835788e867559858fc92d093ded3dcb1eb, inspected job 113430495465 had steps=[] and runner_name empty, root cause UNKNOWN.
DO_NOT: change tests/assertions/spec to make green; skip Rust; reclassify env missing as product pass; fake DOC-E release or broad suite PASS.
RESOLUTION_GATE: actual command, stderr/stdout, environment, source blobs, isolated RED/GREEN, current HEAD, test/commit readback.
ALTERNATE: independently testable DOC-C issue/queue boundary when isolated Postgres+Redis genuinely available. Avoid production services or chargeable provisioning without approval.
NO_PRODUCTS_CHANGED_BY_THIS_AUDITOR: TRUE.
