# Counterfactual Change Graph
Status: AI-PROPOSED CONCEPT — NOT CURRENT NEXY REQUIREMENT

A deterministic graph for answering: if X changes, what requirements, claims, tests, evidence, interfaces and releases may become invalid?

ChangeNode fields: stable_id, object_type, authority_class, version/hash, provenance, inbound_dependencies, outbound_dependencies, invariants, evidence_refs, invalidation_rules, rollback_anchor.

Object types include REQUIREMENT, LAW, POLICY, CONTRACT, API, SCHEMA, MODULE, MODEL_PROVIDER, PROMPT, TOOL, DATASET, TEST, EVIDENCE, DEPLOYMENT, UI_FLOW, MIGRATION.

Typed edges: REQUIRES, IMPLEMENTS, VERIFIES, DEPENDS_ON, CONSTRAINS, SUPERSEDES, DERIVES_FROM, DEPLOYS, RENDERS, READS, WRITES, TRUSTS, FALLS_BACK_TO. Every edge has HARD/SOFT/INFORMATIONAL strength, condition, source, freshness rule and propagation policy.

ChangeEvent = target + before_hash + candidate_hash + reason + authority + semantic_delta + requested_scope. UNKNOWN target identity or authority freezes evaluation.

Propagation: seed changed node; traverse HARD edges first; apply typed invalidation; mark DIRECT/TRANSITIVE/CONDITIONAL effects; stop at proven isolation boundaries; compute evidence staleness; generate verification and rollback obligations.

Output: blast radius, stale evidence, compatibility boundaries, E0-E7 obligations, unsafe unknowns, rollback anchor, and SAFE_TO_EVALUATE / FREEZE_NEEDS_EVIDENCE / CONFLICT.

Invariant: missing dependency coverage becomes UNKNOWN, never "safe".
