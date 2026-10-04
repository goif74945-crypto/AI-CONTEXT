CASE_ID: NEXY-CLOCK-TIME-SEMANTICS-9C147261
head: 9c1472615d08af96188953fa17b855d8ac45ba31
severity: S3 correctness + release-blocking dependency
status: OPEN / CLOCK-SCOPE-FROZEN

source_claims:
- L9: Core cannot read system clock; allowed TSA-injected batch time only; Date.now/system_time/monotonic_clock forbidden.
- G19: authoritative layer uses invariant TSC only; no HPET; no wall clock; Tick = integer counter.

code_evidence:
- packages/core/tick.ts currentTick uses TSA floor when injected, otherwise recovered logical floor + ordinal/call sequence.
- repository search found injectTsaBatchTime production usage absent; occurrence is implementation + unit test only.
- packages/phase-f/lo2/federation.ts labels HEARTBEAT_TTL_MS=60000 and compares currentTick deltas as milliseconds.
- packages/phase-f/resilience/io-law.ts names windowMs and compares currentTick deltas to 1000/windowMs.
- existing LO2/I/O integration tests do not verify elapsed-window expiration against a deterministic injected time boundary.

verdict:
- old OS-clock access defect is resolved.
- exact clock-source compliance cannot be VERIFIED until spec scope conflict is resolved.
- millisecond-vs-call-counter consumer semantics remain a concrete correctness defect/risk.
