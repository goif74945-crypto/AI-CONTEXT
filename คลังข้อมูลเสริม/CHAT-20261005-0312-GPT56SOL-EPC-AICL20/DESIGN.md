# MMCRC20 Design

## Authority boundary

MMCRC20 is Lo4 advisory logic. Its output can only be `QUALIFIED_FOR_EXTERNAL_REVIEW` or `FREEZE_NOT_QUALIFIED`. Neither output authorizes NEXY state mutation or promotion. The qualification capsule hard-codes `authority_mutation_allowed=false` and `promotion_allowed=false`.

## Grounded NEXY surface

At NEXY commit `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`, `packages/swarm/adapters/types.ts` defines a canonical external AgentAdapter with identity/provider/schema, supported modes, deterministic capability, criticality, timeout, max context, execute, cancel, and healthcheck. `base.ts` supplies shared adapter semantics and caps current-build admitted input at 8192. `agent-response.ts` treats provider responses as untrusted and fails closed on malformed canonical response/evidence data. OpenAI, Gemini, and Anthropic adapters are concrete provider boundaries.

## Twenty mechanisms

01 Adapter Contract Completeness Gate — hard-fails missing/invalid canonical adapter fields or operations.
02 Provider Identity Integrity Binder — prevents silent provider identity substitution.
03 Mode Set Equivalence Gate — proves required fast/strict/audit coverage.
04 Context Ceiling Compatibility — rejects a provider ceiling below the NEXY admission bound.
05 Timeout Budget Compatibility — rejects provider timeouts exceeding the canonical budget.
06 Criticality Consistency Gate — preserves critical/non-critical failure semantics.
07 Health Classification Parity — replays status→HEALTHY/DEGRADED/UNHEALTHY classification.
08 Cancellation Contract Gate — requires exercised acknowledgement and no post-cancel side effect.
09 Structured Response Shape Gate — requires answer/reasoning/evidence/confidence and exact confidence domain.
10 Evidence Provenance Preservation — validates IDs, source class, SHA-256, anchors, normalization version and Q64 confidence.
11 Confidence Domain Consistency — keeps captured provider confidence inside exact Q64 [0,1].
12 Canonical Response Equivalence — compares schema, semantic digest and parse state across providers.
13 Truncation Boundary Probe — requires below/at/above context-boundary fixtures.
14 Provider Error Taxonomy Normalizer — maps timeout/schema/HTTP failure states into provider-neutral deterministic codes.
15 Retry Safety Classifier — permits retries only for retryable errors when the operation is explicitly idempotent.
16 Failover Eligibility Gate — requires at least two healthy compatible substitutes.
17 Model Identity Drift Binder — freezes unapproved model identifier changes.
18 Cross-Provider Behavioral Differential — compares semantic/parse/evidence/answer/reasoning behavior.
19 Q64 Resilience Scorecard — advisory weighted score only.
20 Qualification Capsule Compiler — seals baseline/spec/gates/score/replay identity and enforces non-compensatory hard gates.

## Numeric and determinism law

Decision-relevant quantities use checked signed Q64.64 on a signed 128-bit carrier with 256-bit checked intermediates. Overflow, divide-by-zero and invalid ranges fail closed. Canonical replay framing is length-prefixed before SHA-256. Network, wall clock, randomness, filesystem ordering and floating-point scores cannot affect a verdict.

Mechanism 19 cannot cancel failures in mechanisms 01–18. Any failed hard gate makes mechanism 20 emit `FREEZE_NOT_QUALIFIED`.

## Scope exclusions

This project intentionally does not implement provider SDK calls, tool-call semantics, streaming semantics, production billing, provider marketing context-window claims, live provider health, JUDGE decisions, Canon promotion, or NEXY repository changes. Those require separate authority and runtime evidence.
