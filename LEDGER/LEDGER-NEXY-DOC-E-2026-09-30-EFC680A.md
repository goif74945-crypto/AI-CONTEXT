# LEDGER-NEXY-DOC-E-2026-09-30-EFC680A

| id | source | claim | proof | deps | risk | status | confidence | freshness |
|---|---|---|---|---|---|---|---|---|
| L1 | GitHub NEXY.ai branch | canonical tested HEAD is efc680a5846dcd6a49ad5e49bc53ec6e8cdd4e98 | branch/ref + Railway source binding | GitHub + Railway | low | VERIFIED | 1.00 | current-at-campaign |
| L2 | GitHub source fetch | DOC-E contract corruption existed at prior HEAD 541421ab | malformed bytes inside TypeScript expression | repository file content | S4 | VERIFIED | 1.00 | current-at-fix |
| L3 | GitHub commit | corruption/test contradiction repaired | commit bd817650267acea64f21aa631d49076c5e7d201a | Git object | medium | VERIFIED_SOURCE_CHANGE | 1.00 | current |
| L4 | GitHub Actions | GitHub hosted runner did not execute first steps | run 36602881913, job 109524417528, steps=null, logs_url=null | Actions API | S4 | VERIFIED_ENV_BLOCK | 1.00 | historical |
| L5 | Railway | exact source identity is bound to validation deployment | deployment 7ad09354-83a2-4ef7-a084-c6404c675d7e + ::NEXY_HEAD::efc680... | Railway build log | high | VERIFIED | 1.00 | current-at-campaign |
| L6 | Railway raw build log | node/npm toolchain executed | node_setup exit=0; Node v22.23.2; npm 10.9.8 | Railway build | medium | VERIFIED | 1.00 | current-at-campaign |
| L7 | Railway raw build log | dependency install passed | npm_ci exit=0; 405 packages; 0 vulnerabilities | Railway build | medium | VERIFIED | 1.00 | current-at-campaign |
| L8 | Railway raw build log | typecheck passed | ::NEXY_GATE_END::typecheck::exit=0 | Railway build | high | VERIFIED | 1.00 | current-at-campaign |
| L9 | Railway raw build log | contract tests passed | ::NEXY_GATE_END::contract::exit=0 | Railway build | high | VERIFIED | 1.00 | current-at-campaign |
| L10 | Railway raw build log | integration tests passed | ::NEXY_GATE_END::integration::exit=0 | Railway build | high | VERIFIED | 1.00 | current-at-campaign |
| L11 | Railway raw build log | full test suite passed | ::NEXY_GATE_END::full::exit=0; 114 files / 844 tests shown in suite output | Railway build | high | VERIFIED | 1.00 | current-at-campaign |
| L12 | Railway raw build log | coverage run and thresholds passed | coverage exit=0; coverage_check exit=0; API 93.44/Core 95.73/Law 100/Judge 97.39 lines | Railway build | high | VERIFIED | 1.00 | current-at-campaign |
| L13 | Railway raw build log | DOC-C static gate passed | doc_c exit=0 + static check ALL PASS | Railway build | high | VERIFIED | 1.00 | current-at-campaign |
| L14 | Railway raw build log | production web build passed | web_build exit=0 | Railway build | high | VERIFIED | 1.00 | current-at-campaign |
| L15 | Railway raw build log | base validation overall passed | ::NEXY_VALIDATION_OVERALL::0 | all preceding gates | high | VERIFIED_BASE_GATES | 1.00 | current-at-campaign |
| L16 | design authority + repo | DOC-E release remains unauthorized | E1-E12 current evidence pack not complete and E11 real signoff absent | design source | S4 | VERIFIED | 1.00 | current |
| L17 | docs/evidence/current | committed E1-E12 markdown is stale | namespace README binds to SHA 0d0d82bdc7d04ef8248f310d106cf5e4c1dd7a3d | repo content | S4 | VERIFIED_STALE | 1.00 | current |
