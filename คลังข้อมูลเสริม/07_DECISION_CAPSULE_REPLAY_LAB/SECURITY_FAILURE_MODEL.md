# Security & Failure Model

Status: AI PROPOSAL, prototype scope only.

## Threats covered by v0.1

- event payload tampering -> event hash mismatch;
- event insertion/deletion/reordering -> sequence or hash-chain mismatch;
- authority reference mutation -> authority fingerprint mismatch;
- fake capsule identifier -> load-time capsule-id mismatch;
- tool result without legal intent -> replay rejection;
- tool result bound to altered intent -> intent-digest mismatch;
- execution after FREEZE -> replay rejection;
- PASS without verification -> replay rejection;
- raw secret exposure through trust receipt -> receipt omits event/output payloads by design.

## Threats not solved

- SHA-256 keyless integrity is tamper-evident only when trusted original identities exist; it is not a signature.
- A malicious producer can generate a self-consistent false capsule.
- The prototype does not authenticate actors or tools.
- It does not enforce OS/network/process sandboxing.
- It does not prove external evidence is truthful.
- It does not encrypt sensitive payloads at rest.
- It does not solve distributed concurrency or cross-machine ordering.

## Fail-closed behavior

Invalid schema, hashes, chain, state transitions, terminal proof or output digest cause explicit failure. There is no hidden repair, guessed action, auto-skip or silent PASS.

## Recommended future hardening

AI PROPOSAL:
- signature envelope with key rotation and verifier identity;
- external evidence binding by content hash + evidence class;
- NDJSON streaming verifier;
- explicit redaction policy and encrypted payload compartment;
- capability-policy binding for each TOOL_INTENT;
- monotonic execution sequence from a trusted coordinator;
- signed public receipt for portable verification.
