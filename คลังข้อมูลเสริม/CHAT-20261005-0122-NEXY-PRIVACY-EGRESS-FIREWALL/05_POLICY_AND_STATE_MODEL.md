# Policy & State Model

**Status:** AI-PROPOSED

## Sensitivity lattice

`PUBLIC < INTERNAL < PERSONAL < SENSITIVE < SECRET`

This is an engineering classification proposal, not a legal taxonomy. Projects may need domain-specific classes and multiple orthogonal labels rather than a single linear sensitivity score.

## Recipient classes

- `LOCAL_TRUSTED`: stays inside a trusted execution boundary.
- `EXTERNAL_MODEL`: third-party or otherwise external model boundary.
- `CONNECTOR`: application/service connector boundary.
- `EXPORT`: user/system export beyond the current trusted control plane.

A recipient class is not an identity. The exact recipient string remains mandatory for per-recipient policy binding.

## Default policy flags

- `external_sensitive_requires_consent = true`
- `forbid_secret_external_egress = true`
- `sensitive_requires_explicit_recipient_binding = true`

Policy flags are included in a deterministic fingerprint so receipts can be linked to the decision configuration. The fingerprint is not proof that the policy was authorized.

## Consent grant lifecycle

`ISSUED -> ACTIVE -> EXPIRED | REVOKED`

A grant may authorize exactly one item/purpose/recipient tuple for its active interval. Production design may support scoped bundles, but any bundling must remain inspectable and bounded.

### Wave 07 exact-batch consent proposal

`ConsentBundleGrant` is AI-PROPOSED/NON-GOVERNING. It binds:
- one non-empty grant ID;
- one exact request ID;
- one exact purpose;
- one exact recipient;
- one expiry/revocation state;
- one `frozenset` containing at least two item IDs.

For an active bundle matching the current request/purpose/recipient, its item set must equal the full set of items in that request that require consent. Under-scoped and over-scoped active bundles FREEZE with `BUNDLE_SCOPE_NOT_EXACT`; the evaluator does not infer partial consent. Multiple active bundles, duplicate grant IDs, or valid single-item grants overlapping the bundle FREEZE as ambiguous authority. Expired, revoked, or binding-mismatched bundles are inert and lead to ordinary `ASK`/redaction behavior.

This contract validates deterministic structured metadata only. It does not authenticate the grant issuer, prove human comprehension, or establish legal consent.

## Evaluation state machine

```text
RECEIVED
  -> VALIDATING
      -> FREEZE
      -> EVALUATING
          -> BLOCK
          -> ASK
          -> REDACT
          -> ALLOW
```

Terminal states do not auto-transition. A new grant, corrected metadata, changed recipient, or changed purpose creates a **new evaluation** and new receipt.

## Reason-code discipline

Reason codes are stable machine-facing semantics, not user-facing prose. User interfaces should map them to concise explanations without exposing hidden policy internals or raw values.

## Required versus optional

`required=True` means the caller asserts the task cannot be correctly executed without this item. It does **not** grant permission. A required item that is forbidden blocks or asks; it is never smuggled through because the task wants it.
