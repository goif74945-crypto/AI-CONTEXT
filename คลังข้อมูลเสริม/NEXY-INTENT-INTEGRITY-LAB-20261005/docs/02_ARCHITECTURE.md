# 02 — Proposed Architecture

**Classification:** AI-PROPOSED CONCEPT / ADVISORY ONLY

## Logical flow

```text
Human directive / authoritative spec
        |
        v
Intent Contract Builder
        |
        +--> Canonicalizer --> SHA-256 Contract Digest
        |
        v
Execution Proposal
        |
        v
Intent Guard
  |     |      |      |
  |     |      |      +--> Truth-class checks
  |     |      +---------> Evidence floor checks
  |     +----------------> Requirement coverage
  +----------------------> Repository + scope/protected boundary
        |
        +--> PASS
        +--> REVIEW
        +--> FREEZE + findings
```

A separate transition guard compares contract revisions:

```text
Base Contract + Candidate Contract + Optional Exact Approval
                    |
                    v
             Transition Guard
                    |
          semantic change IDs
                    |
       PASS / REVIEW / FREEZE
```

## Components

### Canonicalizer
Normalizes Unicode to NFC, normalizes line endings, sorts object keys, sorts string arrays, and sorts arrays of ID-bearing objects by ID.

Design goal: prevent non-semantic ordering differences from generating false contract identities.

Risk: some arrays may become order-sensitive in future domains. If that happens, canonicalization rules must become schema-aware rather than applying the current generic list policy.

### Contract validator
Rejects malformed data before evaluation. It checks required object shape, duplicate IDs, duplicate string entries, known evidence classes, valid requirement kinds, and acceptance-criterion references.

### Proposal guard
Evaluates a proposed execution plan against the contract. It does not execute mutations. It returns findings only.

### Transition guard
Computes deterministic semantic changes between two validated contracts. Each change receives an exact ID such as:

- `objective:main`
- `requirement.remove:REQ-001`
- `scope.in_scope.add:another/**`

An approval must name the exact change IDs it authorizes.

### CLI
Provides reproducible local evaluation without network access or third-party dependencies.

## Future production requirements if ever adopted

The current prototype is intentionally insufficient for production. A production design would need, at minimum:

- cryptographically authenticated approval identity;
- replay protection and nonce/timestamp strategy;
- schema-version migration law;
- path normalization aligned with the actual execution environment;
- repository identity binding, not only path patterns;
- signed contract/evidence envelopes;
- agent/workflow identity and delegation lineage;
- partial-order evidence semantics rather than a simplistic global ranking;
- policy conflict resolution with authoritative law;
- tamper-evident audit storage;
- runtime integration tests and adversarial fuzzing.

## Performance model

For a contract with `R` requirements, `C` criteria, `P` touched paths, and `K` claims, the prototype is approximately:

- validation/indexing: `O(R + C + K)`;
- path matching: `O(P * patterns)`;
- canonicalization: dominated by sorting, roughly `O(N log N)` for set-like collections;
- hashing: linear in canonical serialized size.

This is suitable for small control-plane contracts. It is not designed to hash entire repositories or massive source documents.
