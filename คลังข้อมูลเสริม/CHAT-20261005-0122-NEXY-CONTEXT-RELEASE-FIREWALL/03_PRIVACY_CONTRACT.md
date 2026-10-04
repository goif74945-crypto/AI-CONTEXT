# CRF Privacy / Information-Flow Contract

Classification: AI_PROPOSED_CONCEPT

## P0 — Default deny by non-selection
A context field that is not explicitly listed in `required_keys` or `optional_keys` is outside the release candidate set and must never cross the boundary.

## P1 — Explicit consumer and purpose
No wildcard consumer and no inferred purpose exist in the reference contract.

## P2 — Policy ceiling
Field sensitivity above the policy ceiling is denied unless a valid trusted declassification grant lowers that exact field for that exact consumer/purpose/time window.

## P3 — Compartment monotonicity
A request may ask only for compartments allowed by policy. A field may cross only when all its compartments are present in the request's allowed compartment set.

## P4 — Derived sensitivity monotonicity
For derived data:
`declared_sensitivity >= max(source_sensitivity)`

No implicit sanitization exemption exists.

## P5 — Derived compartment monotonicity
For derived data:
`declared_compartments ⊇ union(source_compartments)`

## P6 — Derived purpose non-broadening
Treat an empty source purpose set as unrestricted. For all restricted sources, calculate the intersection of allowed purposes. A derived field may narrow that set but may never broaden it or erase the restriction.

## P7 — Atomic required release
If one required key cannot legally be released, the firewall returns `FROZEN` with an empty payload.

## P8 — Optional minimization
A blocked/missing optional key is omitted and cannot make another key more permissive.

## P9 — No blocked-value diagnostics
Receipt/decision records contain metadata and reason codes only. They must not include blocked field values or individual blocked-value hashes.

## P10 — Canonical reproducibility
Contract and receipt fingerprints use deterministic canonical JSON and SHA-256. Map insertion order must not alter the resulting hashes.

## P11 — No caller-created authority
A DeclassificationGrant is inert unless its exact canonical digest already exists in the trusted grant registry.

## P12 — Grant specificity
A valid grant is bound to:
- grant id;
- field key;
- source sensitivity;
- target sensitivity;
- authority id;
- consumer id;
- purpose;
- not-before/not-after window;
- reason code.

## P13 — Expiry
Expired ContextField data is unusable at the release boundary.

## P14 — Provenance presence
Every field must carry non-empty provenance. Provenance is metadata evidence, not automatic proof that the value is correct.

## P15 — Model independence
The reference engine contains no model call, prompt, embedding, provider SDK, or probabilistic decision.

## P16 — Status discipline
Reference release status is exactly:
- `RELEASED`
- `FROZEN`

Structural/policy contract violations raise validation errors and must be handled as non-release by an integrating authority layer.

## P17 — Evidence boundary
Passing this lab's E1/E2 tests proves only the reference implementation behaviors exercised by those tests. It does not prove NEXY integration, production privacy, transport security, provider retention guarantees, or deployment security.
