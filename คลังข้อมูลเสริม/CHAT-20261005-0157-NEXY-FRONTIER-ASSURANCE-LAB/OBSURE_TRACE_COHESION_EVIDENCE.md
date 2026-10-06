# OBSURE Cross-Effect Trace Cohesion Evidence

Status: `PASS` for the bounded standalone reference slice described below.

## Target and Scope

- Repository: `goif74945-crypto/AI-CONTEXT`
- Branch target observed before persistence: `main`
- Parent revision: `deea71a27ff3ac03cc0d7b06715a2a11139f7e33`
- Tested persisted code revision: `d5a36fc8151fbbe5e05e48a55cb7bae47a318b77`
- Tested tree: `4271432023cbdc68382a729af325d7743545c124`
- Runtime: Python `3.12.14`
- Verification timestamp: `2026-10-06T04:24:59Z`
- Write scope: this mission root only
- Classification: AI-proposed experimental reference, not canon and not a
  NEXY.AI implementation or deployment

## Verified Gap

An executed reproduction passed two individually valid effect histories with
different trace/action identities to the prior `ObsureRuntimeAssurance`. It
returned `CERTIFIED / RUNTIME_CERTIFIED` with no issues. The new negative test
binds those histories to one contract and returns `FREEZE` for the splice.

The prior adapter also had no cross-effect causal contract. The new tests prove
that a child cannot start before a declared parent completes, including the
subtle case where a failed parent is incomplete until `COMPENSATION_RESULT`.

A repository-wide supplemental scan found generic rollback, reversibility, and
action-dependency systems, but no other artifact joining OBSURE's concrete
runtime events to one trace/action identity plus compensation-aware dependency
completion. This slice therefore deepens OBSURE and retains the mission's five
concepts rather than inventing a sixth.

## TDD Evidence

Initial standalone RED:

```text
python3 -m unittest -v test_obsure_trace_cohesion.py
Ran 14 tests
FAILED (14 errors: obsure_trace_cohesion module missing)
```

Initial composed-integration RED:

```text
python3 -m unittest -v test_frontier_composed_assurance.py
Ran 19 tests
FAILED (19 errors: trace_contract not accepted)
```

Role Court remediation RED for compensation completion:

```text
test_compensated_parent_must_finish_before_child_intent
expected FREEZE, observed CERTIFIED
```

The repair chooses `COMPENSATION_RESULT` as the parent completion phase when
the parent's expectation requires compensation.

Role Court remediation RED for mutable contract input:

```text
test_contract_snapshots_mutable_dependency_input
ERROR: KeyError: 'unknown'
```

The repair restricts the graph input to a built-in dictionary, validates it,
and snapshots it behind an immutable mapping during contract construction.

## Fresh Verification

Focused suite after all remediation:

```text
python3 -m unittest -q \
  test_obsure_trace_cohesion.py test_frontier_composed_assurance.py
Ran 35 tests in 0.053s
OK
```

Pre-persistence verification:

```text
python3 -m py_compile *.py
python3 -m unittest discover -s . -p 'test_*.py' -q
Ran 152 tests in 0.103s
OK
git diff --check
exit 0
```

Post-persistence verification used a detached worktree at exact commit
`d5a36fc8151fbbe5e05e48a55cb7bae47a318b77`:

```text
python3 -m py_compile *.py
python3 -m unittest discover -s . -p 'test_*.py' -q
Ran 152 tests in 0.100s
OK
git diff --check
exit 0
```

Evidence classes: E1 compile, E2 positive/negative/adversarial/determinism, and
E3 integration with base OBSURE and the five-gate composed pipeline.

## Persisted Byte Binding

The five persisted files were fetched from the exact tested commit as base64
and compared with the local tested bytes. Every comparison returned `true`.

- Design blob: `3f9a8e7025d80ae90a706a02fdbf77deef1e5e32`
- Cohesion code blob: `5da0b3e77f9a38b4f8f078bced3c985e2ea1fcd2`
- Cohesion test blob: `b835802631a57c7bfbccb376cfead164ce555f06`
- Composed integration code blob: `74ae71c50b66bef83823fe7259d06efe2958ec16`
- Composed integration test blob: `b2f77e4f1b549d612e2fce7342ee2dd418539505`

## Verification-Path Corrections

The first supplemental collision-search command was issued from the mission
directory while also naming the repository-relative supplemental path. It
failed because that path did not exist relative to the working directory. The
scan was rerun from the repository root and completed.

After the compensation repair, the first targeted unittest selector used a
nonexistent aggregate class name and produced an unittest loader error. The
selector was corrected to the actual `TraceCohesionNegativeTests` class; the
targeted test passed, followed by the 35-test focused suite and 152-test full
suite. This was a command-selection error, not a code behavior pass/fail.

## Role Court Record

- Execution mode: `LOGICAL_ISOLATION`
- Specification Prosecutor: confirmed an OBSURE dimension, not a new concept.
- Architect: selected a wrapper contract so the original per-effect certifier
  remains authoritative for its existing invariants.
- Security/Resource review: required finite built-in sequences, canonical
  witness values, exact effect coverage, acyclic dependencies, and immutable
  post-validation graph semantics.
- Adversary: exposed compensation-boundary ordering and caller mutation after
  validation; both received RED tests and repairs.
- Regression Guardian: full mission suite passed before persistence and again
  from the exact persisted code revision.
- Truth Sentinel: claims are limited to standalone E1/E2/E3 evidence at the
  bound bytes; no deployment, canonical, or NEXY.AI adoption claim.
- Judge: `PASS` for this bounded continuation slice.

## Limitations

This evidence does not prove live NEXY.AI compatibility, production operation,
deployment, telemetry authenticity, identifier provenance, distributed-clock
correctness, or universal safety. Trace/action identifiers and sequence numbers
remain caller-supplied assertions. GitHub content readback proves persistence of
the compared bytes, not runtime deployment.
