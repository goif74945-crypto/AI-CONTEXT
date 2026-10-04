# Test Evidence — Exact Publish Set

## Target

`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0141-NEXY-CHRONO-INTEGRITY-LAB`

## Evidence boundary

This evidence applies to the exact consolidated publish-set whose source/test hashes are listed below. It proves standalone Python semantics only. It does not prove NEXY integration, distributed trusted time, real authentication/session behavior, production runtime fault tolerance, or deployment readiness.

## E1 — Compile/static syntax

Command:

```text
PYTHONPATH=src python -m compileall -q src tests examples
```

Observed: exit code 0.  
Status: `PASS`.

## E2 — Unit/boundary/randomized behavior

Command:

```text
PYTHONPATH=src python -m unittest discover -s tests -v
```

Observed:

```text
Ran 42 tests in 0.020s
OK
```

Coverage families:

- exact timeout boundary and 1ns-before boundary;
- activation boundary;
- clock-ID mismatch;
- monotonic epoch mismatch;
- monotonic rollback;
- positive/negative wall-vs-monotonic divergence;
- parent/child deadline budget propagation;
- strict canonical serialization and fingerprints;
- deterministic replay;
- 1,000 randomized within-skew decision cases;
- 500 randomized above-skew freeze cases.

Status: `PASS`.

## E2 — Example

Command:

```text
PYTHONPATH=src python examples/demo.py
```

Observed semantic result:

- state: `VALID`
- reason: `OK`
- elapsed monotonic: `60000000000 ns`
- remaining: `240000000000 ns`
- wall/monotonic delta: `0`

Status: `PASS`.

## SHA-256 of exact executable publish files before repository publication

```text
0d0330fef2ca3a1f60cac6f3c7461aa7eba518b99c607f276da3206f27514020  examples/demo.py
e3290a0eb4293e15cf0316c3e29740495aa0e800c6b1b4dab3cf6a67b5dd5a7d  pyproject.toml
d60d4d70f484349a0131d55130ab21c67b9a611a282f3c53f3af7ccd795abf8f  src/nexy_chrono_integrity.py
547f6804e782027d39b888d0d6f303e6e9df1f7a502b76b9f52ef33d4c06e099  tests/test_chrono_integrity.py
```

## Repository evidence pending at time of this record

Publication is not considered fully verified until:
1. target folder exists on `main`;
2. all expected files fetch successfully;
3. critical Git blob identities match the locally tested bytes;
4. no repository with `NEXY.AI` in its name was mutated by this workstream.

E3+ remains `NOT_VERIFIED`.
