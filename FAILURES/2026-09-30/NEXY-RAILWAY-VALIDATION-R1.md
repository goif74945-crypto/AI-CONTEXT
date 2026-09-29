# FAILURE-NEXY-RAILWAY-VALIDATION-20260930

FAILURE_ID: FAILURE-NEXY-RAILWAY-VALIDATION-20260930
context: NEXY.AI exact-head Railway validation
cause:
- c8a6162... runner exported non-test NODE_ENV, causing test-only state reset denial and cascade.
- after that repair, Rust contract exposed missing cargo in the Railpack Node image.
failed_approach:
- relying on runtime environment to imply Vitest NODE_ENV
- Node-only Railpack image for a repository whose contract suite executes cargo
recovery:
- normalize NODE_ENV only in tests/setup/prisma-mock.ts
- add Rust via Railpack packages map
boundary:
- production reset guard remains denied outside test harness
- Rust test remains mandatory and was not skipped
prevention:
- validation image must include every tool invoked by contract tests
- exact-head evidence must bind SHA+tree, never reuse stale literals
evidence:
- deployment cfc320eb-c17c-4dd4-a487-23a7fe99ba72: 36 failed / 387 passed
- deployment 13320048-c6b4-4ef0-b126-975e0ed8e254: 1 failed / 422 passed; cargo ENOENT
- deployment 1839c67f-3cc9-48d1-832e-749e08dd377d: full suite 856/856 PASS observed before terminal deployment result
status: RECOVERING
