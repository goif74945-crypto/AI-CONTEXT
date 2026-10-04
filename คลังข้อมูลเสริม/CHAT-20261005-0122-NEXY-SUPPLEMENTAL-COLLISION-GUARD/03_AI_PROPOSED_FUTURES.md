# AI-Proposed Future Extensions

Every item in this document is:

`AI_PROPOSED / NOT_CURRENT_NEXY_REQUIREMENT / NOT_IMPLEMENTED_IN_V1`

These are design options only. They must not be described as existing NEXY behavior or shipped Collision Guard capability.

## F1 — Responsibility Capsule Protocol

Require every new supplemental project to expose a tiny machine-readable capsule:
- objective;
- responsibility boundary;
- explicit non-goals;
- key nouns/verbs;
- dependencies;
- authority class;
- expected outputs.

Collision Guard could compare capsules rather than mining arbitrary prose. This would reduce noise from implementation details and make intent-level comparison more reproducible.

Adoption gate: a capsule schema must be accepted by AI-CONTEXT governance before it is treated as authoritative input.

## F2 — Two-stage semantic advisory

After deterministic lexical screening, an optional embedding or LLM stage could inspect only the top lexical candidates and propose semantic similarities/differences.

Hard rule: semantic model output remains `ADVISORY`. It cannot independently delete, merge, or block a project. Any hard gate must expose deterministic facts or require explicit human/project-authority judgment.

## F3 — Concurrent Work Lease Registry

Create short-lived, append-only leases for active supplemental project responsibility areas. A new chat would preflight active leases before creating a directory.

Potential benefit: catches collisions before enough files exist for content-based comparison.

Risk: stale leases can become false blockers. Any design needs TTL, owner/session identity, renewal semantics, crash expiry, and no-force takeover rules.

## F4 — Novelty Delta Requirement

For `HIGH_OVERLAP`, require a candidate to persist an explicit delta capsule:
- what existing project already does;
- what new responsibility remains uncovered;
- why extending the existing project is insufficient;
- what outputs will not overlap.

This turns overlap from a warning into a design-quality prompt while preserving human authority.

## F5 — Coverage Heatmap

Build a graph of supplemental responsibility areas and show clusters that are over-invested versus uncovered. This could guide future research toward genuinely orthogonal work rather than whatever naming pattern is fashionable that hour.

Constraint: “uncovered” must never be inferred from filename absence alone. It requires a declared bounded taxonomy or capsule coverage denominator.

## F6 — Semantic Drift Watch

A project may start distinct and later drift into another project’s responsibility. A periodic read-only comparison could flag increasing overlap across revisions.

Required evidence before adoption:
- stable project snapshots;
- false-positive benchmark;
- deterministic drift metric or explicitly advisory model stage;
- no automatic destructive remediation.

## F7 — Merge Recommendation Planner

For proven duplicate workstreams, generate a **non-mutating** merge plan that identifies unique artifacts and conflicts.

This planner must never execute delete/move/history-rewrite operations. Those remain separately authorized actions with their own verification requirements.

## F8 — Multilingual Tokenization Adapter

V1 treats contiguous Thai text coarsely. A future pluggable tokenizer could provide Thai/other-language word segmentation.

Adoption rule: tokenization version must be recorded in fingerprints because changing token boundaries can change scores and invalidate comparisons.

## F9 — Benchmark Corpus

Create a curated labeled corpus of:
- exact duplicates;
- renamed duplicates;
- high-overlap extensions;
- merely related projects;
- orthogonal projects;
- adversarial keyword stuffing.

Use it to tune thresholds with precision/recall evidence instead of anecdotal examples. Until such a corpus exists, v1 thresholds remain engineering defaults validated only by the included fixtures.

## F10 — Collision Receipt in Project Creation Workflow

A future AI-CONTEXT project-start workflow could require a read-only Collision Guard receipt before creating a new supplemental directory.

The receipt should record:
- root snapshot identity;
- candidate capsule hash;
- top matches;
- risk classification;
- reviewer/user override if applicable.

This is the highest-value integration direction, but it should happen only after the guard is benchmarked against real historical projects. Otherwise the tool risks becoming bureaucracy with a JSON accent.
