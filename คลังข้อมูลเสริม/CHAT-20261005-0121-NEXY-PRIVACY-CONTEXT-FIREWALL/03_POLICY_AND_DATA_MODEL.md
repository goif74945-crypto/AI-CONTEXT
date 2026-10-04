# Policy and Data Model

## Classification vocabulary

Ordered from least to most restrictive in this reference:

1. `PUBLIC`
2. `INTERNAL`
3. `PERSONAL`
4. `SENSITIVE`
5. `SECRET`
6. `CREDENTIAL`

The ordering is a policy primitive, not a universal legal taxonomy.

## Context envelope

Required decision inputs:
- `policy_version`: policy identity expected by the caller;
- `purpose`: one admitted task purpose;
- `destination`: destination/profile ID;
- `decision_time`: timezone-aware ISO-8601 timestamp;
- `required_fields`: field IDs actually required for task execution;
- `fields`: candidate context fields.

Each field carries:
- `id`;
- `value`;
- `classification`;
- `purposes`;
- `allowed_destinations`;
- `retention_seconds`.

`allowed_destinations: ["*"]` is supported as an explicit wildcard. Absence is not treated as wildcard.

## Destination profile

A destination must declare:
- `id`;
- `boundary`: `LOCAL` or `EXTERNAL`;
- `allowed_purposes`;
- `max_classification`;
- `max_retention_seconds`;
- `can_retain`.

The supplied profile must match the envelope destination ID. PCF does not discover destinations dynamically.

## Policy

The policy defines:
- `version`;
- `known_purposes`;
- `default_retention_seconds`;
- `max_retention_seconds`;
- `deny_external_classifications`.

The current example policy denies `SECRET` and `CREDENTIAL` on external boundaries. This is a lab default, not canonical NEXY law.

## Minimum-disclosure rule

A field can only enter the payload if all applicable checks pass and the field is in `required_fields`.

A candidate field that is not required is pruned even if it would otherwise be safe. This is deliberate data minimization rather than merely sensitivity filtering.

## Retention leases

For an admitted field:

```text
if destination.can_retain == false:
    effective_ttl = 0
else:
    effective_ttl = min(
        field.retention_seconds or policy.default_retention_seconds,
        policy.max_retention_seconds,
        destination.max_retention_seconds,
    )
```

The lease contains only field ID, TTL, and deterministic expiry. A TTL is an authorization bound, not evidence that a provider actually deleted data. Provider-side deletion requires separate operational evidence.

## Decision receipts

Receipts use HMAC-SHA256 over canonical JSON:
- sorted object keys;
- compact separators;
- UTF-8;
- NaN/Infinity rejected.

The key must be at least 32 bytes and is never serialized into the output.

HMAC proves that a party with the key produced/authorized the recorded decision material. It does not prove that the destination obeyed the decision after receipt.

## Freeze privacy

The freeze receipt material contains field metadata but not field `value`. The serialized FREEZE result likewise does not expose denied values. This prevents an absurd class of audit system where the security log helpfully republishes the secret it blocked.
