# Architecture

## Boundary model

```text
untrusted JSON / runtime value
          |
          v
   strict acceptance gate
          |
          +--> reject duplicate keys / float / unsafe int / bad key / cycle / limits
          |
          v
 Unicode NFC normalization
          |
          v
 deterministic key ordering
          |
          v
 canonical UTF-8 bytes
          |
     +----+----+
     |         |
     v         v
 domain hash   deterministic envelope
                   |
                   v
          payload_hash + envelope_hash
```

## Modules

### `canonical.py`
Owns accepted types, normalization, ordering, bounds, serialization, strict JSON parsing, and domain-separated fingerprinting.

### `envelope.py`
Builds and verifies a strict proof-carrying envelope. Time is supplied by the caller, never read internally.

### `errors.py`
Defines machine-distinguishable failure classes so a future NEXY adapter can map failures to FREEZE/rejection states without parsing prose.

## Accepted data model
- `null` / Python `None`;
- boolean;
- integer within configured bounds, default ±(2^53−1);
- Unicode string normalized to NFC;
- ordered-independent object with string keys;
- ordered array/list.

Floats are forbidden. Exact decimal quantities should use an explicitly versioned tagged representation at a schema layer above NDIK.

## Deterministic ordering
Object keys are ordered by Unicode scalar-value sequence after NFC normalization. This is explicitly **NDIK-v1 behavior**, not a claim of RFC 8785 equivalence.

## Complexity
For total payload size `n` and object-key counts `k_i`:
- traversal/encoding is O(n);
- each object sorts keys O(k_i log k_i);
- total memory is O(n) in this reference implementation because text chunks are materialized;
- cycle detection is O(active container depth).

A future production port may stream scalar/array chunks and hash incrementally, but must preserve exactly the same byte contract.

## Failure semantics
Every rejected condition raises a typed exception. No invalid input is silently repaired. This makes future integration compatible with NEXY's freeze-over-guess direction.

## Trust boundary
NDIK is a deterministic encoding primitive only. It does not establish truth, authorization, safety, authenticity, or schema validity. A valid envelope can still contain a false claim; the hash proves consistency of bytes, not correctness of meaning.

## Evolution law
Any byte-level rule change requires a new format/domain version. Never change `NDIK-v1` semantics in place after adoption because doing so would silently invalidate stored identities.
