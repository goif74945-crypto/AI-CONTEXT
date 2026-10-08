# Execution 009 CROSS
Product start/frozen source HEAD: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
Control initial HEAD: 11123ddb31c674db720812904f84b03cae4b93a4
Canonical DOCX SHA previously established: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7.
| Work | Proof |
|---|---|
| Source HEAD | exact NEXY.ai 44bcb... direct GitHub + remote clean clone |
| 3 candidate patch SHA | individual A/B/C git apply --check, apply, reverse, blob identity |
| A mock candidate | real module imported with own test, GREEN 9/9 |
| B mock candidate | real module imported with own test, GREEN 9/9 |
| C mock candidate | real module imported with own test, GREEN 10/10 |
| Real PG/Redis | NOT_RUN due absent Docker/PG/Redis, no endpoint configured |
| New executable harness | scripts importable, local fail-closed preflight verified; tsconfig typecheck exit0 |
| Cage contract | baseline expected RED 1 fail/1 pass, candidate GREEN 2/2, still no seccomp runtime proof |
| Release | NOT_AUTHORIZED |
| 98 row matrix | 98 distinct IDs, 15 scoped observations, 83 not reassessed |
