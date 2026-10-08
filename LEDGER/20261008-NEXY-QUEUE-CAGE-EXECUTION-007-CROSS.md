# LEDGER 20261008-NEXY-QUEUE-CAGE-EXECUTION-007-CROSS
Product HEAD at source audit: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
Control PREWRITE HEAD: b8b11254dc1c5a4091de883ec35fbd7a4d70df85
DOCX SHA256 locally computed: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

| ID | Evidence depth | New verdict |
|--|--|--|
| QUEUE-02 | SOURCE + EXECUTABLE MODEL (not db) | MISMATCH-RISK, unpatched |
| QUEUE-03 | SOURCE retry-policy 3888169fc88784c999c31ff0f19ad673ba0e0f11 | PARTIAL, default deny/allowlist observed, races untested |
| QUEUE-04 | DOC-C + config in Handoff 006 | SOURCE VERIFIED WITH LIMITS |
| QUEUE-05 | jobs.ts + workers.ts source | PARTIAL, worker guard present, no Redis execution proof |
| QUEUE-06 | tick.ts + producer/worker source | DEPENDENCY BLOCKED, no signed-time test |
| EXP-05 | cage.ts source | SECURITY GAP RISK, runtime not tested |
| GATE-03 | current-head Actions run IDs | CI FAILED (cause unknown) |
| GATE-06 | DOC-E signoffs | NOT_VERIFIED |
| AUTH-01 | locally SHA256-matched DOCX | SOURCE VERIFIED |
All other requirements: do not mass promote, exact existing matrix historical. Current assessed_completion_percent: NOT_COMPUTABLE. Substantive coverage new head not globally validated.
