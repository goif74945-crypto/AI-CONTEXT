# Performance and Invariants

## Complexity

Let `n` be candidate fields and `r` be required field IDs.

- field canonical ordering: `O(n log n)`;
- per-field policy checks: `O(n)` apart from Python list membership costs;
- required-field resolution: bounded by field/index construction plus membership checks;
- memory: `O(n)` for decisions/payload/leases.

For large context manifests, production evolution should normalize purpose/destination/classification sets into hash-backed structures after validating their canonical representation. The reference favors clarity and deterministic behavior over micro-optimization.

## Determinism invariants

Given equal normalized envelope/profile/policy/key:
- decision is equal;
- violations are equal and stably ordered by processing rules;
- field decisions and leases are equal;
- receipt digest is equal.

Changing an admitted payload value changes the ALLOW receipt.

Reordering fields without changing their semantics produces the same decision artifacts because fields are processed by stable ID order.

## Privacy invariants

- FREEZE implies `payload == null`.
- denied field values are not included in FREEZE receipt material.
- a field absent from `required_fields` cannot appear in ALLOW payload.
- an unknown classification cannot be admitted.
- external classes denied by policy cannot be admitted.
- destination ceiling cannot be exceeded.
- retention cannot exceed caller request, policy maximum, or destination maximum.
- a non-retaining destination receives TTL 0.

## Authority invariants

- policy version must match exactly;
- destination identity must match exactly;
- purpose must be known to policy and admitted by destination;
- receipt authority requires a minimum-strength caller key;
- policy/profile data must be canonical-JSON-compatible.

## Operational invariant proposed for future integration

A future NEXY provider call should be structurally impossible unless it carries an ALLOW decision/receipt bound to the exact projection and destination. This lab does not implement that integration gate.
