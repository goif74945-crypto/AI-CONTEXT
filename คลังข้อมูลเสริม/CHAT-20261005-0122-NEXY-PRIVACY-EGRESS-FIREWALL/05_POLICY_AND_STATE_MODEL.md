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
