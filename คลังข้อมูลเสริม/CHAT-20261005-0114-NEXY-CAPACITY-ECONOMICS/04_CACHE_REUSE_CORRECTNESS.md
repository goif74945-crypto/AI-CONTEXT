# Cache and Reuse Correctness Contract

> Classification: AI_PROPOSAL. Not a claim that NEXY.AI currently implements caching.

## 1. Objective

Allow safe reuse of expensive results without converting stale, unauthorized, differently scoped, or weakly evidenced outputs into apparent truth.

The default rule is:

[
reuse_allowed iff identity_match land authority_match land freshness_valid land evidence_sufficient land policy_compatible
]

A textual similarity match is never sufficient.

## 2. Cacheable object

A reusable artifact SHOULD carry this envelope:

| Field | Purpose |
|---|---|
| artifact_digest | Hash of canonical payload |
| producer_version | Exact producing component/version |
| input_identity | Canonical digest of normalized inputs |
| authority_set | Source identities and authority levels |
| policy_digest | Governing rules at creation |
| task_contract_digest | Scope and required evidence |
| environment_digest | Relevant model/tool/runtime configuration |
| created_at_source | Trusted time source or UNKNOWN |
| freshness_policy | Expiry/invalidation rule |
| evidence_manifest | Evidence references and statuses |
| sensitivity | Data-handling class |
| tenant_scope | Authorized reuse boundary |
| determinism_class | deterministic, bounded-nondeterministic, nondeterministic |
| dependency_vector | Version/digest of dependent objects |
| negative_result | Whether this is a failure/absence result |

Missing identity-critical metadata makes the artifact non-reusable.

## 3. Cache key

A logical cache key SHOULD be built from canonicalized, length-delimited fields:

[
K=H(namespace | schema_version | input_identity | authority_set | policy_digest | environment_digest | task_contract_digest)
]

Requirements:

- unambiguous canonical encoding;
- domain-separated hash namespace;
- explicit schema version;
- stable ordering for sets;
- normalized locale/encoding where applicable;
- secrets excluded from user-visible metadata;
- tenant and authorization scope included before lookup.

Do not key only on prompt text, URL, filename, or user-visible task title.

## 4. Reuse decision state machine

States:

- MISS: no candidate exists;
- CANDIDATE: identity key matched;
- VALIDATING: policy, authority, freshness, and evidence checked;
- HIT_STRONG: exact contract and evidence match;
- HIT_DERIVED: safe transformation exists with lineage;
- STALE: invalidated by time/dependency/version;
- FORBIDDEN: authorization/sensitivity mismatch;
- CORRUPT: digest or schema validation failed;
- UNKNOWN: required metadata unavailable.

Only HIT_STRONG or an explicitly permitted HIT_DERIVED may feed a completion claim.

## 5. Freshness models

Choose per datum:

1. immutable-by-content: valid while digest and authority remain accepted;
2. version-bound: valid only for exact repository/config/model version;
3. event-invalidated: invalidated by declared dependency change;
4. TTL-bound: valid for a documented duration;
5. request-current: must be refreshed for each decision;
6. non-cacheable: authorization, high volatility, or missing provenance forbids reuse.

TTL is not proof of freshness. It is a policy limit.

## 6. Negative caching

Failures and “not found” responses may be cached only with:

- short, explicit lifetime;
- dependency identity;
- distinction between authoritative absence, transient failure, permission denial, and rate limit;
- no conversion of UNKNOWN into absence;
- retry-after semantics when supplied.

A permission error cached as “object does not exist” is a correctness defect.

## 7. Evidence-aware reuse

Evidence has a scope. Reuse is invalid if the new claim is stronger than the cached proof.

Examples:

- a static parse result cannot prove runtime behavior;
- a test at commit A cannot prove commit B;
- a source snapshot from date D cannot prove a current-state claim after its freshness window;
- a proposal document cannot prove implementation.

The consumer must compare required evidence class with the evidence manifest before reuse.

## 8. Authorization and isolation

Cache lookup and response filtering must enforce:

- tenant isolation;
- principal authorization;
- purpose limitation;
- sensitivity policy;
- deletion/retention requirements;
- least-privilege access to source artifacts.

Authorization must occur before a hit is disclosed, including timing or metadata that could reveal existence.

## 9. Stampede and concurrency control

For concurrent identical misses:

- use single-flight per exact key;
- bound waiters;
- propagate cancellation carefully;
- do not let one tenant's authorization result authorize another;
- allow stale-while-revalidate only for artifact classes whose policy permits it;
- maintain generation/version checks to prevent late writers from replacing newer values.

Recommended write rule: compare expected generation, then commit atomically; otherwise discard and re-evaluate.

## 10. Partial-result caching

Partial results require:

- completed requirement set;
- missing requirement set;
- explicit PARTIAL status;
- evidence manifest per completed part;
- resumable dependency/version information.

A partial artifact must never be served as COMPLETE solely because it exists in cache.

## 11. Invalidation matrix

| Change | Required invalidation |
|---|---|
| canonical input changes | Exact dependent entries |
| authority hierarchy changes | Entries relying on changed authority |
| policy digest changes | Entries governed by incompatible policy |
| evidence requirement increases | Entries below new evidence floor |
| repository/runtime version changes | Version-bound entries |
| permission revoked | Principal/tenant-scoped entries immediately |
| schema changes | Migrate with proof or invalidate |
| dependency becomes UNKNOWN | Block reuse unless policy defines safe behavior |

## 12. Cache poisoning defenses

- verify payload digest on read;
- validate producer identity and schema;
- reject untrusted metadata;
- partition untrusted and trusted results;
- never promote an artifact merely because it is frequently reused;
- cap object size and decompression ratio;
- record lineage for derived artifacts;
- audit abnormal hit-rate and key-collision patterns.

## 13. Metrics

Track by artifact class:

- eligible lookups;
- strong hit rate;
- derived hit rate;
- stale rejection rate;
- authorization rejection rate;
- corrupt entry rate;
- false-hit incidents;
- avoided resource cost;
- validation cost;
- recompute cost;
- age at reuse;
- evidence-floor rejection rate.

High hit rate is not success if false-hit probability rises.

## 14. Verification suite

Minimum scenarios:

1. identical input and contract → HIT_STRONG;
2. same text, different authority set → MISS/FORBIDDEN;
3. same input, newer repository revision → STALE;
4. expired current-state result → STALE;
5. lower evidence than requested → reject reuse;
6. tenant mismatch → FORBIDDEN without existence disclosure;
7. corrupted payload → CORRUPT and quarantine;
8. concurrent miss burst → one authorized computation per key;
9. late writer after invalidation → discarded;
10. cached timeout → not converted to authoritative absence;
11. partial result → remains PARTIAL;
12. policy change → incompatible entry invalidated.

## 15. Acceptance properties

- every served hit has traceable provenance;
- cache key covers semantic and authority identity;
- authorization precedes disclosure;
- stale and corrupt results fail closed;
- cache behavior is observable without exposing sensitive payloads;
- invalidation behavior is deterministic for the same event sequence;
- cache savings never replace required evidence.

Status: SPECIFICATION_COMPLETE; IMPLEMENTATION_NOT_VERIFIED.
