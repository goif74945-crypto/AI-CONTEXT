# EVIDENCE RECORD

> Target: standalone AI-PROPOSED reference lab only. No NEXY.AI runtime/deployment claim.

## Environment

- Python: 3.13.5
- Implementation: CPython
- Platform observed: Linux-6.18.44-x86_64-with-glibc2.41
- Runtime path observed: `/opt/pyvenv/bin/python`
- Third-party runtime dependencies: none declared

## E1 — Static / compile evidence

Command:

```bash
python -W error -m compileall -q -f src tests examples bench
```

Observed: PASS, exit code 0, no warning promoted to error.

## E2 — Unit/property evidence

Command:

```bash
python -W error -m unittest discover -s tests -v
```

Observed:

```text
Ran 53 tests in 0.013s
OK
```

Coverage themes executed:
- authority non-promotion;
- assurance non-inflation;
- taint monotonicity;
- 64-step protected-taint chain;
- exact artifact binding;
- receipt content tamper detection;
- receipt expiration/future-time validation;
- idempotent same-input receipt replay and rejection after state change;
- stale/future release handling;
- deterministic reason ordering;
- evidence-class exact matching rather than numeric ordering;
- strict wire schema parsing;
- extra/missing field rejection;
- unknown taint/schema rejection;
- artifact/receipt round trips.

## Executed demonstration

Command:

```bash
python examples/demo.py
```

Observed behavior:
1. unverified candidate => `FREEZE` with `UNVERIFIED` + missing-assurance reasons;
2. exact verification receipt applied => `ALLOW` under the demo policy.

The demo was executed twice and byte-for-byte output comparison returned no diff.

## Local stress/performance probe

Command:

```bash
python bench/stress.py
```

Final observed run:

```text
transforms=20000
transform_seconds=0.378400
transforms_per_second=52854.17
decisions=50000
decision_seconds=0.414007
decisions_per_second=120770.92
final_artifact_id=078fed2edabca75b82c32b9443a3c539e3c08a625302202ac8ac786c961e017b
```

Interpretation: local reference-runtime evidence only. It is **not** a production SLA, deployment benchmark, or proof of NEXY.AI performance.

The deterministic final artifact ID matched the prior stress run even though timings changed.

## Placeholder audit

Command class:

```bash
grep -RInE '\b(TODO|FIXME|NotImplemented|PLACEHOLDER|placeholder)\b' src tests examples bench
```

Observed: no matches; audit command completed without finding placeholder markers.

## Source SHA-256 snapshot

```text
6c5b0450bbbfb49114d77b0777b93efc0d325e46dc42c13af056f08d0a7c907a  src/nexy_provenance_taint/__init__.py
8b2a03d2d0d1bd9856538393ffc131140616dd5e9b78aea1c78478e62b0cba69  src/nexy_provenance_taint/core.py
b4303ad9528687ce311d73d2188c0ddd5ad0bec7b31dcdcde8328778a3ae8500  src/nexy_provenance_taint/model.py
3291317baba0cd68700f7eb5bd1ec0f7023212a2a19985d1f7d0d8c57b601270  src/nexy_provenance_taint/wire.py
a8ba1a826ddfcaeace9e745ef6d6d37f8dfe3fddefa09f0bf4fb8fe8de5a4269  tests/test_lattice.py
43853edb50ab42ffd3f55a7063dc8b1cf89876b197ea0e9aafab24ee8ed7bc7a  tests/test_properties.py
e56dcb6e9b38221556f8d149fb1d89cc1423130ea55c7211d277f3cafc48e946  tests/test_wire.py
6dc2890b04f7ee2aed05dd69e57a5e91ab6cdd60b3c84e9cd1ad5d32ae38ace4  examples/demo.py
ef2908aa3370991b743e1a53b23e7757db2d6b59d35db3b9d0653e4121815001  bench/stress.py
38c3c330c264029ebd194c275db17a3bbb162aaac0d5ab6e89f4527b2e6b85ae  pyproject.toml
```

## Novelty/collision evidence

Before implementation, AI-CONTEXT repository search returned zero code-search hits for:
- `taint provenance authority`
- `trust laundering provenance`
- `provenance lattice`
- `authority laundering`
- `derived data provenance release`

This is evidence of no direct keyword collision in the searchable default branch, not a mathematical proof that no conceptual overlap exists anywhere.

## Protected-scope evidence

No mutation action was directed to a repository whose name contains `NEXY.AI`.
All durable writes for this task are under:

`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0143-NEXY-PROVENANCE-TAINT-LATTICE/`

## Evidence class limits

- E0/E1/E2: available for this lab.
- E3 integration with NEXY.AI: NOT VERIFIED / intentionally out of scope.
- E4 E2E NEXY user flow: NOT VERIFIED.
- E5 operational target runtime: NOT VERIFIED.
- E6 deployment: NOT VERIFIED.
