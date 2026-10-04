# Design, Security, Verification, and Integration Contract

**Authority:** AI-PROPOSED advisory research. It does not override NEXY source/spec.

## Source alignment
`FACT_PROJECT` recorded in AI-CONTEXT:
- NEXY is a deterministic control/authority system and prefers a legal verified output or freeze/silence over guessing.
- Locked-source context describes canonical binary WAL encoding with fixed schema/endian, length framing, and SHA-256.
- Locked-source context forbids floating point in Core and specifies signed 128-bit canonical arithmetic in that branch.
- Replay/state behavior must not depend on incidental ordering; divergence freezes.
- Evidence classes remain separate from source/design claims.

`PROPOSAL` in this lab: NCW1 tags/layout, NFC admission, UTF-8 key byte ordering, JSON duplicate handling, resource defaults, and hash domain.

## Architecture
`untrusted JSON -> raw-size gate -> strict JSON parser -> semantic validator -> NCW1 encoder -> domain-separated SHA-256`

Inbound wire: `NCW1 -> total-size gate -> strict decoder -> canonical-order validation -> semantic value`.

Core is stateless and takes only explicit input + explicit immutable policy. No clock, RNG, network, filesystem, process, environment, or database I/O is used by the core module.

## NCW1 wire
Magic: ASCII `NCW1`. Exactly one root value; trailing bytes reject.

| Tag | Meaning | Payload |
|---:|---|---|
| 0x00 | null | none |
| 0x01 | false | none |
| 0x02 | true | none |
| 0x03 | signed i128 | 16-byte two's-complement big-endian |
| 0x04 | string | u32 big-endian length + strict UTF-8 NFC bytes |
| 0x05 | list | u32 count + values |
| 0x06 | map | u32 count + key length/key bytes/value |

Map keys are strings and must be in strictly increasing raw UTF-8 byte order. Integers are limited to `[-2^127, 2^127-1]`. Float values are forbidden. Non-NFC text is rejected rather than silently rewritten.

Hash: `SHA-256(b"NEXY-CANONICAL-WIRE-LAB-v1\\0" || NCW1_BYTES)`.

## Failure model
Fail closed on: duplicate JSON keys, NFC-equivalent key collisions, float/NaN/Infinity, i128 overflow, unsupported type collapse, invalid/non-NFC Unicode, bad magic, unknown tag, truncation, non-canonical map order, duplicate wire keys, trailing data, depth/item/string/raw-JSON/total-wire resource limits.

No fallback parser, best-effort repair, normalization rewrite, last-key-wins policy, or lossy coercion exists.

## Security limits
Explicit byte/depth/count limits reduce obvious resource abuse, but production DoS resistance is NOT_VERIFIED. The import scan is E1 evidence against a named set of common side-effect modules, not a formal non-interference proof. Constant-time behavior, signing/authentication, persistence durability, sandbox containment, and deployment security are out of scope.

## Requirement/evidence summary
- equivalent map order -> byte/hash identity: PASS E2
- i128 boundaries/float rejection: PASS E2
- strict duplicate/collision detection: PASS E2
- malformed/noncanonical wire rejection: PASS E2
- golden format vectors: PASS E2
- no listed core side-effect imports: PASS E1
- cross-language equivalence: NOT_VERIFIED
- cross-architecture equivalence: NOT_VERIFIED
- NEXY production/WAL compatibility: NOT_VERIFIED

## Future NEXY integration gate
Preferred lowest-risk adoption is **test-only oracle** against an existing authoritative codec. Production adoption, if ever authorized, requires all of:
1. resolve authoritative current NEXY format/schema;
2. independent cross-language byte/hash conformance;
3. x86_64/arm64/runtime conformance;
4. hostile complexity/load evidence;
5. explicit version/evolution/rollback law;
6. persistence/replay proof if used for durable state;
7. expanded differential parser/fuzz evidence;
8. exact-commit integration evidence at the required class.

Passing this isolated lab does not authorize copying it into NEXY.AI.
