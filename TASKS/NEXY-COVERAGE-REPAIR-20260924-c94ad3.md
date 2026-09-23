TASK_ID: NEXY-COVERAGE-REPAIR-20260924-c94ad3
title: Railway runtime validation and API coverage repair
mode: EXECUTE / CROSS_CONTINUE
scope: goif74945-crypto/NEXY.AI- astra/omega-full-spec-convergence
observed_head_before: 8ee2ccfc06e592177610a7e3c10db2cecfa4f512
repair_commit: c94ad368773ba57dd9490286e6cca696fc3ec8a1
railway_previous_deployment: 4cf474bd-03ec-4ea3-97e9-da403885cf5e
previous_runtime_results:
  npm_ci: PASS
  prisma_generate: PASS
  typecheck: PASS
  contract: PASS
  integration: PASS
  full: PASS
  coverage_measurement: PASS
  coverage_check: FAIL
  doc_c: PASS
  web_build: PASS
proof:
  - full suite: 86 files / 635 tests passed
  - coverage api: lines 64.62 statements 63.43 functions 72.33 branches 56.11, threshold 85 all metrics
  - core/law/judge coverage gates PASS
  - DOC-C static gate PASS
  - web build compiled successfully
coverage_hotspots:
  - packages/api/storage-control.ts ~0.5% statements
  - packages/api/cold-snapshot.ts ~1.53% statements
  - packages/api/owner-recovery.ts ~6.59% statements
actions:
  - added tests/coverage/owner-recovery-control-plane.test.ts
  - added tests/coverage/cold-snapshot-control-plane.test.ts
  - added tests/coverage/storage-control-plane.test.ts
  - did not lower thresholds or exclude source from coverage
current_railway_deployment: 2027f4a6-2ab7-467e-a0c2-2cee621efd44
current_status: BUILDING
final_status: PARTIAL_VALIDATION_REPAIR_IN_PROGRESS
next_actions:
  - inspect current deployment gate markers
  - fix any proven test/source defect
  - verify API coverage >=85 under lines/statements/functions/branches
trace_id: NEXY-COVERAGE-REPAIR-20260924-c94ad3
hash: HASH_UNAVAILABLE
