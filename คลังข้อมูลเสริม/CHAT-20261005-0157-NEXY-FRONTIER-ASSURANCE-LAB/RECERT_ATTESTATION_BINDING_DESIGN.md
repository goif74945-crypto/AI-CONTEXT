# RECERT State and Policy Attestation Binding Design

Status: `AI_PROPOSED_EXPERIMENTAL_NOT_CANON`

## Purpose

Deepen the existing RECERT concept at an unverified evidence boundary: a
recovery decision must identify the exact before state, after state, recovery
policies, and comparison identity that produced it.

This slice adds no sixth concept. It wraps the collision-safe RECERT adapter and
is also integrated into the existing five-gate composed reference pipeline.

## Confirmed Gap

Fresh reproduction showed that all three of these materially different inputs
returned `CERTIFIED` with the identical RECERT result hash
`3492f3c1c847157c2eace3c188ea0b40fe43978c263f282fcf95bc3e9c5f4e31`:

- before/after `{"epoch": 1}` under default exact policies;
- before/after `{"epoch": 2}` under default exact policies; and
- before/after `{"epoch": 1}` under explicit `PRESENT` policies.

The existing result binds verdicts and mismatches, but a successful comparison
has no mismatch payload and therefore does not identify which state/policy was
assessed. A consumer cannot distinguish certificates for different recovery
inputs.

Repository-wide supplemental inspection found generic certificate and
before/after hashing systems. None binds this mission's concrete RECERT
dual-certifier decision to both recovery states and both policy dialects. This
is an exact RECERT evidence repair, not a new general certificate concept.

## Contract

`RecoveryAttestationContract` declares four non-empty identities:

- `attestation_id`;
- `incident_id`;
- `before_revision`; and
- `after_revision`.

`RecertAttestationBindingAssurance.assess` performs this sequence:

1. validate the attestation contract;
2. snapshot both states into finite built-in structures;
3. reject custom mappings, cycles, unsupported leaves, and non-finite floats;
4. snapshot the original dot-path policy and pointer-safe policy;
5. hash the contract, both type-tagged states, and both canonical policies;
6. build a single `binding_hash` over those five hashes;
7. run `RecertPathIntegrityAssurance` against the exact snapshots; and
8. bind the base decision hash and binding hashes into the final result hash.

Hashing uses type-tagged state records so semantically distinct Python
containers such as `list` and `tuple` cannot collapse to the same generic JSON
array commitment. The adapter does not expose raw state values in its result.

## Failure Semantics

- Invalid contract, unbounded/custom mapping behavior, cyclic input, mutable
  policy container types, unsupported values, or non-finite floats raise the
  mission's `FreezeError` before certification.
- A base RECERT failure remains `FREEZE` with the original reason, original
  certifier output, pointer-safe certifier output, and complete binding.
- A passing base comparison becomes `CERTIFIED` only with all binding hashes.
- The composed pipeline converts rejected binding inputs into its existing
  structured `RECERT_INPUT_REJECTED` freeze path.

The adapter does not authenticate caller-provided revision or incident IDs and
does not prove that snapshots were captured atomically from a live runtime.

## Verification Plan

- Positive: certified decisions expose contract/state/policy/base/final hashes.
- Negative: empty identities, custom mappings, mutable policy container types,
  cycles, and unsupported leaves fail closed.
- Adversarial: shuffled mappings are deterministic; caller mutation after
  assessment cannot rewrite the result; list/tuple inputs remain distinct.
- Gap regression: different passing states and different passing policies keep
  the old base-hash collision but produce distinct binding/final hashes.
- Integration: path-integrity failures retain their reason and the composed
  pipeline carries the RECERT binding into its own result hash.
- Regression: compile every mission Python file and execute the complete
  mission test suite from the exact persisted revision.

## Authority and Limitations

This is a standalone reference artifact inside the supplemental mission root.
It does not establish NEXY.AI adoption, compatibility, runtime integration,
deployment, production readiness, snapshot authenticity, or canonical status.
Claims are limited to the exact committed bytes and executed E1/E2/E3 evidence
recorded for this experimental slice.
