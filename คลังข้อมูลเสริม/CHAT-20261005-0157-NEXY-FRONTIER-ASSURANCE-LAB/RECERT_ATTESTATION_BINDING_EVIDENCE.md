# RECERT State and Policy Attestation Binding Evidence

Status: `PASS` for the bounded standalone reference slice described below.

## Target and Scope

- Repository: `goif74945-crypto/AI-CONTEXT`
- Branch target observed before persistence: `main`
- Parent revision: `f3553a1eba1a1653227095c8cb56e468675be8d7`
- Tested persisted code revision: `9cdef2dd5f51cd2da647ce912399ef5f1313fece`
- Tested tree: `e6a736ce10197cb7a57404888600e1ff7e7a893a`
- Runtime: Python `3.12.14`
- Verification timestamp: `2026-10-06T05:23:29Z`
- Write scope: this mission root only
- Classification: AI-proposed experimental reference, not canon and not a
  NEXY.AI implementation or deployment

## Verified Gap

A fresh executable reproduction assessed three different RECERT inputs:

1. before/after `{"epoch": 1}` with default exact policies;
2. before/after `{"epoch": 2}` with default exact policies; and
3. before/after `{"epoch": 1}` with explicit `PRESENT` policies.

All three returned `CERTIFIED` and the identical result hash:

```text
3492f3c1c847157c2eace3c188ea0b40fe43978c263f282fcf95bc3e9c5f4e31
state_collision True
policy_collision True
```

The prior certificate therefore proved the comparison outcome but did not
identify the state/policy inputs that produced it.

Supplemental scans found general certificate policy-binding and before/after
hashing work but no exact RECERT dual-certifier state-plus-policy binding. This
slice deepens RECERT and leaves the concept count at five.

## TDD Evidence

Initial standalone RED:

```text
python3 -m unittest -v test_recert_attestation_binding.py
ERROR: ModuleNotFoundError: No module named 'recert_attestation_binding'
```

Composed integration RED after adding the contract to the test request:

```text
python3 -m unittest -v test_frontier_composed_assurance.py
Ran 21 tests
FAILED (errors=21)
cause: unexpected keyword argument 'recovery_attestation'
```

Role Court remediation RED:

```text
test_list_and_tuple_states_have_distinct_bindings
FAIL: list and tuple state hashes were identical
```

The repair introduced type-tagged state commitments while preserving the base
RECERT comparison semantics.

## Fresh Verification

Focused suite after remediation:

```text
python3 -m unittest -q \
  test_recert_attestation_binding.py test_frontier_composed_assurance.py
Ran 37 tests in 0.061s
OK
```

Pre-persistence verification:

```text
python3 -m py_compile *.py
python3 -m unittest discover -s . -p 'test_*.py' -q
Ran 170 tests in 0.116s
OK
git diff --check
exit 0
```

Post-persistence verification used a detached worktree at exact commit
`9cdef2dd5f51cd2da647ce912399ef5f1313fece`:

```text
python3 -m py_compile *.py
python3 -m unittest discover -s . -p 'test_*.py' -q
Ran 170 tests in 0.118s
OK
git diff --check
exit 0
```

Evidence classes: E1 compile, E2 positive/negative/adversarial/determinism, and
E3 integration with collision-safe RECERT and the five-gate composed pipeline.

## Persisted Byte Binding

The five persisted files were fetched from the exact tested commit as base64
and compared with the local tested bytes. Every comparison returned `true`.

- Design blob: `156746f8d45fb82b8d5786f4b96502b7a03d50f7`
- Binding code blob: `9414d390619e84c1409366f0c3c7c48b3d5f431f`
- Binding test blob: `a6e93bd563602ccacec5bd32de4b646c34ca9aeb`
- Composed integration code blob: `63cabf7b0be089f84721358b8f403fe54ae977ed`
- Composed integration test blob: `44664784642509aa4eb661c56fe16d20785c599e`

## Verification and Persistence Corrections

The first exact duplicate-scan exclusion glob omitted the leading supplemental
directory, so it included this mission's new design file. The corrected glob
excluded the complete mission path and returned no exact external match.

During the initial five-blob persistence loop, the connector response for the
composed test file did not expose a blob SHA. The file was submitted again as a
single explicit blob operation, returning
`44664784642509aa4eb661c56fe16d20785c599e`; subsequent exact base64 readback
matched the tested local bytes. No branch ref was advanced until all five blob
SHAs were present.

## Role Court Record

- Execution mode: `LOGICAL_ISOLATION`
- Specification Prosecutor: confirmed an unverified RECERT evidence dimension,
  not a new assurance concept.
- Architect: selected an outer binding adapter so existing recovery comparison
  semantics remain independently visible.
- Security/Resource review: required finite built-in snapshots, cycle checks,
  immutable policy snapshots, canonical leaves, and no raw-state disclosure.
- Adversary: exposed generic JSON normalization collapsing list and tuple state
  commitments; a RED test and type-tagged record repair closed it.
- Regression Guardian: full mission suite passed before persistence and again
  from the exact persisted code commit.
- Truth Sentinel: evidence supports standalone E1/E2/E3 behavior only; caller
  identity authenticity, live snapshot atomicity, deployment, and adoption are
  not claimed.
- Judge: `PASS` for this bounded continuation slice.

## Limitations

This evidence does not prove live NEXY.AI compatibility, production operation,
deployment, snapshot authenticity, atomic capture, revision provenance, or
universal safety. Contract identity fields remain caller-supplied assertions.
GitHub readback proves persistence of compared bytes, not runtime deployment.
