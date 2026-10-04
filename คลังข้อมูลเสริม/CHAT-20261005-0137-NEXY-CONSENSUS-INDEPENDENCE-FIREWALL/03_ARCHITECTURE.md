# NCIF Reference Architecture

**Classification:** EXPERIMENTAL / AI-PROPOSED

## 1. Trust model

All input is untrusted contract data. The caller supplies:

- a claim identifier;
- evidence nodes with stable IDs, kind, source identity, parent lineage, and optional correlation keys;
- actor votes with stance, evidence references, and optional vote-level correlation keys;
- a consensus policy.

NCIF validates structure but **does not authenticate these assertions**. A malicious caller can lie about provenance unless an upstream signed/verified provenance system exists.

## 2. Core data objects

### EvidenceNode

- `evidence_id`
- `kind`
- `source_identity`
- `parents[]`
- `correlation_keys[]`

Root evidence has no parents. Derived evidence inherits roots/correlation keys through the DAG.

### Vote

- `actor_id`
- `stance`: `SUPPORT | OPPOSE | ABSTAIN`
- `evidence_ids[]`
- `correlation_keys[]`

Only one vote per actor is accepted in reference v1.

### ConsensusPolicy

- `min_support_groups` default `2`
- `max_opposition_groups` default `0`
- `require_single_root_resilience` default `false`

These defaults are prototype policy, not NEXY canon.

## 3. Validation stage

Reject as contract errors:

- non-object root input;
- missing/empty claim ID;
- malformed evidence/vote arrays;
- unsupported evidence kind or vote stance;
- duplicate evidence ID;
- duplicate actor vote;
- vote reference to unknown evidence;
- invalid policy value.

Fail as `FREEZE` rather than contract exception when the structure is syntactically representable but provenance is unsafe to interpret:

- missing evidence parent;
- evidence lineage cycle;
- SUPPORT or OPPOSE without evidence.

## 4. Iterative provenance propagation

Evidence edges are `parent → child`.

The engine uses deterministic Kahn topological processing with a heap-sorted ready queue. For each node it propagates:

- set of root evidence IDs;
- set of correlation-key digests inherited from ancestors.

This avoids recursive lineage traversal and therefore avoids binding valid lineage depth to Python's recursion limit. The local stress audit exercises 5,000 levels; that does not prove arbitrary/unbounded depth.

## 5. Privacy-preserving correlation tokens

The engine internally needs equality tokens for source identity and declared correlation keys. Result diagnostics must not echo those raw values by default.

Reference v1 therefore uses domain-separated SHA-256-based tokens:

```text
key:<sha256(canonical({kind:"key",value:...}))>
source:<sha256(canonical({kind:"source",value:...}))>
```

Root evidence IDs remain visible because they are explicit provenance references. Hashing reduces accidental disclosure; it is **not encryption**, and low-entropy values may still be guessable by dictionary attack.

## 6. Vote view

Each non-abstaining vote is transformed into:

- direct evidence IDs;
- propagated root IDs;
- tokens from root IDs;
- digested root source identities;
- inherited evidence correlation keys;
- vote-level correlation keys.

Distinct evidence objects that declare the same root `source_identity` therefore remain correlated even if their evidence IDs differ.

## 7. Independence grouping

For each stance independently:

1. create a disjoint-set item for each actor;
2. associate each provenance token with its first actor;
3. union later actors that share a token;
4. emit deterministic connected components.

This intentionally collapses transitive bridges. If A shares a key with B and B shares another key with C, A/B/C are one group even if A and C have no direct common token.

## 8. Cross-stance conflict

If SUPPORT and OPPOSE groups depend on the same root evidence, the engine adds `SHARED_ROOT_STANCE_CONFLICT` and freezes. This is an interpretation conflict over common provenance, not independent corroboration.

## 9. Decision policy

Reference rules:

- support independence groups below threshold → `FREEZE`;
- opposition groups above allowed threshold → `FREEZE`;
- unsafe lineage or evidence-less material vote → `FREEZE`;
- optional root-removal resilience failure → `FREEZE`;
- otherwise → `CONSENSUS_CANDIDATE`.

A candidate is deliberately not named PASS/VERIFIED/FINAL.

## 10. Single-root resilience

When enabled, remove every support vote dependent on each root, one root at a time, then recompute support independence groups. The minimum surviving group count must still satisfy policy.

This tests concentration/brittleness. It does not model all common-mode failures because undeclared causal links remain invisible.

## 11. Determinism

The core has no designed source of nondeterminism from:

- clock;
- random generator;
- filesystem/network access;
- environment lookup;
- model/provider call;
- hidden retry/fallback.

Input ordering is normalized by sorted traversal and canonical fingerprinting. Executed permutation tests cover vote-order invariance for bounded fixtures.

## 12. Integration boundary

Conceptual future placement:

```text
SWARM workers/verifiers
        ↓
 signed/verified evidence provenance layer
        ↓
 NCIF independence analysis
        ↓
 candidate independence receipt
        ↓
 CORE / JUDGE policy + truth adjudication
        ↓
 release boundary
```

NCIF must remain advisory below JUDGE. It must never convert “independent enough” into “true.”
