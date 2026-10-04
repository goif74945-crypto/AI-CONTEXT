# Test & Publication Evidence — NEXY Chrono Integrity Lab

## Target

`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0141-NEXY-CHRONO-INTEGRITY-LAB`

## Evidence boundary

This record proves the standalone reference prototype and the identity of its published executable files. It does **not** prove actual NEXY integration, trusted distributed time, production authentication/session behavior, operational clock-fault tolerance, or deployment readiness.

## E1 — Compile/static syntax

Command:

```text
PYTHONPATH=src python -m compileall -q src tests examples
```

Observed: exit code 0.  
Status: `PASS`.

The compile step was rerun after publication-identity normalization of the test file.

## E2 — Unit/boundary/randomized behavior

Command:

```text
PYTHONPATH=src python -m unittest discover -s tests -v
```

Latest observed result after normalization:

```text
Ran 42 tests in 0.022s
OK
```

Coverage families:

- exact timeout boundary and 1ns-before boundary;
- activation boundary;
- clock-ID mismatch;
- monotonic epoch mismatch;
- monotonic rollback;
- positive and negative wall-vs-monotonic divergence;
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

Observed:

- state: `VALID`
- reason: `OK`
- elapsed monotonic: `60000000000 ns`
- elapsed wall: `60000000000 ns`
- wall/monotonic delta: `0`
- remaining: `240000000000 ns`
- envelope fingerprint: `2d382539b0fa34d0b774e3e8df82f4ec597aec5953a948ae2b8fbd5fe1c0c921`

Status: `PASS`.

## Exact executable publish identities

After a fetch-back comparison, the test file was found to differ from the locally retained test source by one trailing newline. No logic differed, but byte identity is an explicit invariant, so this was treated as `FAIL`, not ignored.

Correction:
- local exact-set was normalized to the already-published byte representation;
- compile/test/demo were rerun;
- 42/42 remained PASS;
- the new exact local Git blob identity now matches GitHub.

Final exact identities:

| File | SHA-256 exact bytes | Git blob SHA-1 | Fetch-back |
|---|---|---|---|
| `src/nexy_chrono_integrity.py` | `d60d4d70f484349a0131d55130ab21c67b9a611a282f3c53f3af7ccd795abf8f` | `33477fe7af548b45a120b8f3db68e533783ef33c` | PASS |
| `tests/test_chrono_integrity.py` | `dac54621536f08d36bea27e07aa435f6daaf64d489c8cf0fa86a5da71b79a1bc` | `b831cde8a85f583668e29a5d9fe66d761bc3ddc4` | PASS |
| `pyproject.toml` | `e3290a0eb4293e15cf0316c3e29740495aa0e800c6b1b4dab3cf6a67b5dd5a7d` | `a3438cb2f2a74659de5e5fbeca1418c7921b3996` | PASS |
| `examples/demo.py` | `0d0330fef2ca3a1f60cac6f3c7461aa7eba518b99c607f276da3206f27514020` | `b62687e762a7c62076ff7029935064455da57b8e` | PASS |

## Publication commit lineage observed

Initial additive commits:

- source: `9f0426ea5eb9e6df5f1219577f3b928092789993`
- tests: `ac9dbb4a794d51e8da88afc03c491584d82d47ad`
- package metadata: `4dafffba409fbff25d7aba7066985312ab57054a`
- demo: `20cac053790becc41f9f9a29afdbf076e5d25bd0`
- temporary memory: `81fd7c6438a1a2cb9f7ad0b62bb708145200651b`
- initial evidence record: `1a42a58086a23b2599c088e3762bf7ed109a5993`

The repository was under concurrent writes from other sessions. Two contents-API operations returned HTTP 409 branch-race conflicts. Recovery was fail-safe: no force update was used; HEAD was refreshed; writes were retried only for this workstream's unique paths.

## Protected-scope evidence

Every mutation tool call in this workstream targeted only:

`goif74945-crypto/AI-CONTEXT`

No mutation tool call targeted a repository whose name contains `NEXY.AI`.

Status: `PASS` for the mutation boundary of this workstream.

## Evidence classes not established

- E3 NEXY integration: `NOT_VERIFIED`
- E4 actual NEXY end-to-end user flow: `NOT_VERIFIED`
- E5 real target-runtime clock fault behavior: `NOT_VERIFIED`
- E6 deployment: `NOT_VERIFIED`
