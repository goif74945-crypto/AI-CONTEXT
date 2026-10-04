# Future NEXY Integration Contract

Status: `DESIGN CONTRACT ONLY / NEXY INTEGRATION NOT_VERIFIED`

## Adapter boundary
A future NEXY adapter may map existing verified/authorized state into these scorers. The adapter must convert external numeric inputs to decimal strings, integers or exact ratios before Q64 construction. Binary floats are forbidden.

## Required envelope
Each invocation should carry, outside the numeric core:
- `trace_id`;
- `system_id` (one of the 20 IDs);
- input provenance references;
- authority class of each source;
- current policy/version identifiers;
- Q64 raw/canonical values;
- output score;
- limitations/UNKNOWN flags.

## Authority
Outputs are `ADVISORY_SCORE`. They may rank options only after existing NEXY LAW/JUDGE has established which options are legal. An illegal/unverified option cannot become legal because it scores highly.

## Failure semantics
- malformed/unit-domain input -> fail closed with explicit error;
- zero denominator/capacity/cost where invalid -> fail;
- overflow -> fail;
- unresolved authoritative conflict -> adapter must FREEZE before calling this layer if the score would depend on choosing a side;
- missing material input -> UNKNOWN/FREEZE in adapter, never fabricated zero.

## Determinism contract
For identical normalized inputs, code version and policy weights, raw outputs and rank order must be identical.

## Non-claims
This standalone E3 does not prove Next.js/TypeScript adapters, queue behavior, database behavior, production runtime, deployment, or physical systems.
