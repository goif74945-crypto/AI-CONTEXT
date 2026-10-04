# Verification & Test Architecture
Map tests to risks/contracts, not only a pyramid.
Layers: static, unit, property, contract, integration, end-to-end, migration, resilience, security, performance, production synthetic/telemetry.
Acceptance map: requirement_id -> verification_method -> evidence -> result.
Negative tests: unauthorized mutation rejected; malformed input rejected; duplicates do not duplicate side effects; stale version cannot overwrite; expired credential rejected; unsupported enum rejected; missing dependency explicitly fails/degrades.
Regression gate: preserve/reproduce defect; identify cause; failing test where practical; apply fix; pass test; pass adjacent critical paths.
Zero discovered tests is not evidence of a passing suite.
