# Architecture

## System model

The lab uses a fluid deterministic network-calculus model:

- arrival curve: `alpha(t) = b + r*t`;
- service curve: `beta(t) = R * max(0, t - T)`;
- stability/admissibility prerequisite: `R >= r`;
- conservative backlog upper bound: `B = b + r*T`;
- conservative delay upper bound: `D = T + b/R`;
- a chain of rate-latency services is represented by effective rate `min(R_i)` and total latency `sum(T_i)` for the fluid service-curve composition used here.

All arithmetic is performed on Q64.64 raw integers. Products/divisions that feed an upper bound use ceiling rounding so representational truncation cannot make the reported bound smaller than the fixed-point expression being enclosed.

## Pipeline

`explicit flow contract -> FLOWGUARD-64 -> QUEUEBOUND-64 / DEADLINE-64 -> CHAIN-64 -> optional SHAPER-64 -> advisory certificate`

SHAPER-64 never changes a service promise or NEXY law. It only proposes a stricter arrival envelope. If a requested deadline is below intrinsic service latency, it returns `IMPOSSIBLE`. If satisfying a target requires zero sustained rate, it returns `BLOCKED` rather than pretending useful throughput exists.

## Complexity
- FLOWGUARD-64: O(1) time, O(1) memory.
- QUEUEBOUND-64: O(1) time, O(1) memory.
- DEADLINE-64: O(1) time, O(1) memory.
- CHAIN-64: O(n) for n stages, O(n) only because the returned certificate preserves stage identities.
- SHAPER-64: O(1) time, O(1) memory.

## Trust boundaries
- arrival/service contracts must come from an authorized upstream source; the lab does not infer them from telemetry;
- fingerprints are deterministic identity aids, not signatures;
- runtime measurements, clock semantics, queue discipline and burst model validity are external assumptions that must be proven at integration time;
- packetization, scheduler-specific interference, stochastic traffic and multi-class contention are outside this reference model.
