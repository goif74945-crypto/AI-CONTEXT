# Security and Failure Model

Classification: `AI_PROPOSED_LO4_ONLY`

## Trust assumptions
All external payloads are untrusted. Concept IDs, numeric strings, arrays, dependency references, labels, and weights must be validated before use.

## Threats addressed in v1
- binary floating-point drift in authoritative domain scoring;
- overflow/underflow-style silent corruption at Q64 boundaries;
- divide by zero;
- malformed numeric strings;
- duplicate agent/node identities;
- dependency cycles and dangling dependency references;
- correlated-agent false consensus;
- stale evidence represented as fresh evidence;
- deterministic tie instability;
- hidden network/model dependency;
- dynamic code execution in concept modules;
- accidental self-promotion of experimental work.

## Controls
- BigInt Q64.64 with signed-128 range checks;
- nearest-even deterministic rounding;
- static forbidden-pattern gate for concept modules;
- no network path in the reference engine;
- no eval/dynamic Function;
- canonical sorting and content digest;
- explicit FREEZE semantics;
- independent exact-rational oracle vectors;
- adversarial and property-style tests;
- replay stress across all concepts.

## Failure classification
`INPUT/Q64 failures`: converted to deterministic FREEZE with reason codes.

`Unexpected implementation exceptions`: not hidden. They fail the process/test so a bug cannot quietly become a business-domain FREEZE with plausible-looking output.

`Benchmark slowdown`: not a correctness failure by itself. Benchmark throughput is observational and environment-specific.

`NEXY integration absence`: explicit `NOT_VERIFIED`, never inferred from standalone PASS.

## Known residual risk
- formula quality remains a design hypothesis until domain-reviewed;
- Q64 prevents a class of numeric ambiguity, not bad models or bad thresholds;
- SHA-256 integrity IDs are not signatures/authentication;
- Node runtime and OS isolation are outside this project;
- denial-of-service from excessively large JSON payloads needs an integrating boundary limit;
- no E5/E6/E7 evidence exists for production/deployment/physical behavior.
