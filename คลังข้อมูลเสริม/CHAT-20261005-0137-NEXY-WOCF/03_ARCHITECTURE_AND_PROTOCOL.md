# Architecture and Protocol

## Data flow

```text
PROPOSAL MANIFEST
      |
      v
STRUCTURAL VALIDATION -----> invalid ----------> FREEZE
      |
      v
POLICY TARGET CHECK --------> protected --------> FREEZE
      |
      v
CATALOG NORMALIZATION ------> invalid catalog --> FREEZE
      |
      v
HARD COLLISION ENGINE
  - ID
  - namespace ancestry
  - write-set ancestry
  - exclusive resources held by ACTIVE/IN_PROGRESS workstreams
  - exact concept fingerprint
      |
      v
LEXICAL OVERLAP ENGINE
  - tag Jaccard (65%)
  - objective token Jaccard (30%)
  - differentiator Jaccard (5%)
      |
      v
DETERMINISTIC FINDING SORT + HASHES
      |
      +--> blocker present -> FREEZE
      +--> warning only    -> WARN
      +--> no findings     -> ALLOW
```

## Authority boundary
WOCF is **admission advice for a workstream scheduler/control plane**, not execution authority. A future NEXY integration could require `ALLOW` before creating a new supplemental workstream, but canonical authority must remain in NEXY CORE/LAW/JUDGE or equivalent governing layer.

## Path semantics
All write paths are normalized relative POSIX-style paths. Absolute paths and dot traversal are rejected. By default, every declared write path must stay inside the declared namespace. Ancestor/descendant overlap counts as a collision because the manifest does not encode file-vs-directory ownership strongly enough to safely relax it.

## Determinism contract
For identical normalized proposal, catalog, and policy:
- decision is identical;
- findings and ordering are identical;
- proposal/catalog/policy hashes are identical;
- no timestamps appear in core output.

## Concurrency semantics
WOCF itself is a snapshot evaluator. It does not solve atomic reservation. A production scheduler would need an atomic sequence:

`READ CATALOG VERSION -> EVALUATE -> COMPARE-AND-SWAP RESERVATION`

If catalog version changes between evaluation and reservation, evaluation is stale and must be rerun. This lab intentionally does not fake that distributed guarantee.

## Security boundary
Input manifests are untrusted data. The engine executes no manifest-provided code and performs no network operations. Repository-protection matching is policy input rather than a hard-coded NEXY rule.

## Failure model
- malformed proposal: FREEZE;
- malformed catalog entry: FREEZE because completeness of collision analysis is compromised;
- protected target: FREEZE;
- collision/high overlap: FREEZE;
- moderate overlap: WARN;
- no issues: ALLOW.
