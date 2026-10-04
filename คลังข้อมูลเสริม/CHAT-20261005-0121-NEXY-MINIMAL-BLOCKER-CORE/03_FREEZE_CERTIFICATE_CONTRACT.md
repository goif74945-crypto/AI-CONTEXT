# Freeze Certificate Contract v0.1.0

**Status:** `AI-PROPOSED / EXPERIMENTAL`

## Input contract

Required top-level fields:

- `schema_version`: exactly `1.0`;
- `certificate_id`: caller identity for this evaluation;
- `target.name`;
- `target.revision` when evidence freshness is revision-bound;
- `evidence`: non-empty map;
- `gate`: one supported monotone operator.

Optional `metadata` is preserved as inert JSON.

### Evidence leaf

Required:

- `status`: `PASS | FAIL | PARTIAL?` is **not accepted** in v0.1.0. The engine deliberately accepts only `PASS | FAIL | BLOCKED | NOT_VERIFIED | UNKNOWN | CONFLICT` because PARTIAL at a leaf is ambiguous without a declared decomposition.

Optional:

- `required_class` and `observed_class`: `E0_PRESENCE`..`E7_PHYSICAL`;
- `target_revision` and `observed_revision`;
- `repair_cost` >= 0;
- `repair_kind`: `EVIDENCE | IMPLEMENTATION | AUTHORITY | DEPENDENCY | REVIEW | OTHER`;
- `remediation`.

### Why leaf PARTIAL is rejected

A composite gate can be partially satisfied, but an atomic leaf marked PARTIAL hides what part passed and what part did not. The correct representation is to decompose it into multiple leaves and combine them explicitly.

That design is intentionally stricter than general AI-CONTEXT status vocabulary.

## Output contract

Key fields:

- `status`: root compact status;
- `decision`: `ALLOW` only when root status is PASS, else `FREEZE`;
- `status_summary`: effective leaf counts;
- `unsatisfied_evidence`;
- `minimal_repair_sets`;
- `recommended_repair_set`;
- `primary_blocker_core`;
- `recommendation_guarantee`;
- `explanation_tree`;
- `evaluation.node_count`;
- `evaluation.repair_sets_truncated`;
- `certificate_sha256`.

## Evidence downgrade law

`PASS` is provisional until freshness/class constraints validate.

```text
PASS + insufficient class      -> NOT_VERIFIED
PASS + missing required class  -> NOT_VERIFIED
PASS + stale revision          -> NOT_VERIFIED
PASS + missing bound revision  -> NOT_VERIFIED
```

No rule upgrades a non-PASS leaf automatically.

## Certificate law

`certificate_sha256 = SHA256(canonical_json(certificate_body_without_certificate_sha256))`

This seal proves deterministic content identity of the generated certificate body. It does not prove authenticity of the upstream facts.

## Repair-set law

A repair set means:

> Under the monotone model and current gate structure, making every evidence leaf in this set PASS is sufficient to make the selected gate path pass, assuming all other current PASS leaves remain PASS.

It does **not** mean:

- those repairs are physically/organizationally possible;
- no hidden requirement exists outside the modeled gate;
- the repair can be performed safely;
- the set is globally cheapest if enumeration was truncated;
- project authority permits bypassing other requirements.

## Versioning law

Any change to:

- accepted statuses;
- evidence downgrade semantics;
- gate logic;
- minimal-set semantics;
- canonicalization/hash scope;
- output field meaning

requires a version review and should normally increment engine/schema version.
