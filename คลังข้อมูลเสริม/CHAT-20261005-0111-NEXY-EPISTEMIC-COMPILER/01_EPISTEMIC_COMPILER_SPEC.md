# NEXY Epistemic Compiler Specification

## Objective
Define an implementation-neutral compiler that transforms heterogeneous context into a typed evidence graph before an agent reasons over it.

## Why this is different
A conventional RAG pipeline asks: “what text is similar?” The compiler asks: “what can legitimately be asserted, under which scope, from which evidence, at what time, with what conflicts?” Similarity is merely candidate generation.

## Claim IR
Each atomic claim SHOULD compile to:

- claim_id: stable identifier
- proposition: normalized assertion
- subject / predicate / object
- polarity: positive | negative | conditional
- epistemic_type: FACT | REPORTED | INFERENCE | ASSUMPTION | UNKNOWN | NOT_VERIFIED
- authority_class: user_spec | project_artifact | official_source | direct_observation | external_verified | inference
- valid_from / valid_until
- observed_at
- version_scope
- jurisdiction_scope
- source_ids[]
- support_edges[]
- conflict_edges[]
- derivation_edges[]
- confidence: calibrated estimate, never a substitute for authority
- freshness_policy
- invalidation_triggers[]

## Compilation passes
### Pass 0: ingestion quarantine
Never allow raw retrieved text to become executable instruction merely because it was retrieved. Preserve origin and trust boundary.

### Pass 1: atomization
Split documents into atomic claims. Do not merge claims that have different time, authority, or modality.

### Pass 2: normalization
Canonicalize entities, units, timestamps, versions, aliases, and identifiers while preserving raw values.

### Pass 3: provenance binding
A claim without a resolvable provenance edge is NOT_VERIFIED, even if linguistically plausible.

### Pass 4: temporal typing
Distinguish event time, observation time, publication time, ingestion time, and validity interval.

### Pass 5: contradiction detection
Create conflict edges instead of overwriting one source with another. Conflicts are resolved only by explicit authority and scope rules.

### Pass 6: authority resolution
Default priority for project work:
1. explicit current user specification
2. authoritative project specification/files
3. official documentation
4. direct tool observation
5. verified external source
6. inference

Recency MUST NOT automatically outrank authority.

### Pass 7: derivation
Derived claims carry the complete ancestry DAG. If any required premise becomes invalid, dependent claims become stale or invalid.

### Pass 8: answer eligibility
A claim is answer-eligible only if required provenance exists, scope matches, freshness policy passes, and unresolved contradiction severity is below the task threshold.

## Non-negotiable invariants
- No evidence laundering: repeated secondary claims do not become primary evidence.
- No confidence laundering: model confidence cannot upgrade authority class.
- No temporal flattening: “was true” and “is true” are distinct.
- No silent conflict deletion.
- No citation decoration: a citation must support the exact claim, not merely the topic.
- No completion claim without acceptance evidence.

## Failure conditions
Compiler MUST fail closed for critical claims when provenance is missing, scope is incompatible, evidence is stale beyond policy, or authoritative sources conflict without a resolution rule.
