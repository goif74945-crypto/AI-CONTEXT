# Design Audit

## Strengths
- narrow surface area;
- deterministic by construction rather than by convention;
- typed fail-closed semantics;
- explicit resource bounds;
- no implicit clock/random/environment dependence;
- domain-separated identity;
- reusable conformance vectors;
- integration is deliberately deferred rather than silently assumed.

## Deliberate trade-offs
- rejecting floats is less convenient but removes a major cross-runtime ambiguity class;
- NFC normalization changes byte identity for canonically equivalent Unicode strings, so normalized-key collisions must be rejected;
- default ±(2^53−1) integer range is narrower than Python integers but safer for TypeScript/JavaScript interoperability;
- materializing canonical text costs O(n) memory; a future streaming port can improve memory usage only if exact output bytes remain unchanged.

## Risks
- a future consumer may wrongly treat a hash as proof of truth or authenticity;
- Unicode normalization can be unsuitable for domains where code-point distinction is semantically meaningful;
- cross-language key ordering must use Unicode scalar order explicitly, not host-language default sort;
- changing format semantics in place would invalidate stored identities.

## Decision
Keep NDIK experimental and standalone. The prototype is useful as a future compatibility primitive, but adoption should require independent cross-runtime conformance evidence.
