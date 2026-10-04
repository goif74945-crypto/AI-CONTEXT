# Architecture

## Components

### `canonical.py`
Stable UTF-8 JSON canonicalization and SHA-256 identity. Rejects unsupported values and non-standard numbers.

### `model.py`
Typed immutable authority references, events and capsules. Normalizes authority ordering and derives capsule identity.

### `builder.py`
Creates hash-linked events and seals a capsule without injecting time/randomness.

### `replay.py`
Two-stage verification:
1. integrity: authority fingerprint, contiguous sequence, previous-hash chain, event hash;
2. semantics: strict event state machine and terminal proof rules.

### `diff.py`
Compares project identity, authority fingerprint, terminal state, event kinds and payload digests. This is structural divergence detection, not semantic-equivalence proof.

### `receipt.py`
Generates a payload-minimized user/UI trust receipt after successful replay. It includes hashes, counts and terminal state but excludes raw request/tool/output bodies.

### `io.py` / `cli.py`
JSON plan compilation and operator-facing commands. Plans may use `$AUTHORITY_FINGERPRINT` and `$AUTO` placeholders that are replaced deterministically during compilation.

## Data flow

```text
UNHASHED PLAN
  -> normalize authority refs
  -> authority fingerprint
  -> append event + previous hash
  -> event hash chain
  -> capsule id
  -> integrity verification
  -> deterministic semantic replay
  -> trust receipt / structural diff
```

## Complexity

For `n` events:
- build: O(n) hash work;
- integrity verify: O(n);
- semantic replay: O(n);
- diff: O(min(n,m)) plus divergence output;
- tool-intent lookup: average O(1) per event using a dictionary.

The current JSON representation is memory-resident. A future NDJSON/streaming format could reduce verification memory to O(1) event state plus bounded open-tool state.

## Determinism boundary

The capsule identity intentionally excludes hidden time, environment, machine identity and random values. If a caller wants those facts recorded, it must supply them explicitly as payload data, making them visible inputs rather than hidden behavior.
