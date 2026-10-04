CASE_ID: NEXY-TSA-PRODUCER-GAP-9E615B04
head: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
severity: S4 release/operational blocker for elapsed-time consumers
status: OPEN

proven:
- currentTsaBatchTimeMs() now correctly fails closed when no TSA batch is injected.
- LO2 heartbeat, resilience I/O windows, and queue stale-time validation consume TSA milliseconds rather than logical call-count ticks.
- repository-wide search for injectTsaBatchTime() returns packages/core/tick.ts plus tests only.
- no production/bootstrap/runtime injection caller was found.

impact:
- corrected consumers no longer silently manufacture elapsed milliseconds from logical calls.
- live elapsed-time operations require a real verified TSA injection binding; absent that, they can fail closed with TSA_BATCH_TIME_REQUIRED/TSA_TIME_AUTHORITY_UNAVAILABLE.

required_next:
- identify canonical TSA authority/provider contract from spec.
- bind authenticated/verified production injection at the correct authority boundary.
- prove stale/regression/replay behavior and ensure external time cannot enter canonical identity outside allowed contract.

verdict: PARTIAL_IMPROVED / INTEGRATION_NOT_COMPLETE
