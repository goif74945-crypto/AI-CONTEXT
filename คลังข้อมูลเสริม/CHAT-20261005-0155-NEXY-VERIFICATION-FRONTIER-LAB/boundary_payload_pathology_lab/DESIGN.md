# Boundary Payload Pathology Lab (BPPL) — Design

Status: **AI-PROPOSED / EXPERIMENTAL / NON-CANONICAL**

## Objective
Provide a strict deterministic JSON boundary that rejects payload ambiguity and resource-pathology cases before data enters higher-level control logic.

## Threat / failure boundary
Ordinary JSON parsing can accept inputs whose semantics become dangerous after downstream normalization or interpretation. BPPL explicitly checks:
- duplicate raw object keys;
- distinct keys that collide under Unicode NFC normalization;
- non-finite JSON extensions such as `NaN`/`Infinity`;
- excessive structural depth;
- excessive total node count;
- excessive numeric magnitude;
- unsupported in-memory value types during canonicalization.

## Inputs and outputs
- `strict_loads(text, limits) -> value` parses hostile/untrusted JSON text.
- `canonical_json(value, limits) -> str` emits normalized, sorted, compact JSON.
- `Limits` explicitly bounds depth, nodes, and numeric magnitude.

## Invariants
1. Ambiguous duplicate/colliding keys fail closed.
2. Canonicalization is deterministic for accepted values.
3. Canonicalization normalizes keys using NFC and rechecks collisions.
4. Resource limits are explicit and enforced both after parse and before canonical serialization.
5. Non-finite numbers never enter canonical output.

## Failure model
All semantic boundary violations raise `BoundaryPayloadError`; wrong API type (`strict_loads` input not `str`) raises `TypeError`. Parser recursion/JSON syntax failures are normalized into `BoundaryPayloadError` with no silent repair.

## NEXY integration proposal
BPPL can sit at an adapter/API boundary before any authority-bearing parser or policy evaluation. It is not a replacement for application schema validation. A future adapter should apply project-specific byte-size and schema limits before/after this generic structural layer.

## Evidence plan
E2 tests cover duplicate keys, Unicode collision, non-finite numeric extensions, depth/numeric limits, and deterministic canonical order. E3 lab integration round-trips a distilled failure witness back through the strict boundary.

## Known limitations
- Python's JSON decoder still allocates the parsed object before `max_nodes` is checked; a production ingress needs an independent byte limit and possibly streaming parsing.
- NFC is one selected normalization policy, not a universal identifier policy.
- This prototype validates structure, not project-specific schemas or authorization.
