FAILURE_ID: NEXY-COVERAGE-REPAIR-20260924-c94ad3
context: current-head Railway validation
cause: API coverage threshold failure
proof: check:coverage exit=1 with api lines=64.62%, statements=63.43%, functions=72.33%, branches=56.11%; threshold=85% for every metric
non_failures:
  - typecheck, contract, integration, full, DOC-C, web build passed on 8ee2ccfc
repair: added runtime coverage tests for storage-control, cold-snapshot, owner-recovery
status: REPAIR_DEPLOYMENT_BUILDING
trace_id: NEXY-COVERAGE-REPAIR-20260924-c94ad3
