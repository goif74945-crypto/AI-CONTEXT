# Architecture

Mission Intent declares identity, objective, controlled domains/capabilities/deliverables, FILE/TREE write claims, protected claims, exclusive resources/authorities, start, finite lease expiry and status.

Canonicalizer applies Unicode NFKC + casefold to controlled tags, sorting/deduplication to set-like fields, UTC normalization to timestamps, and rejects wildcard/parent-traversal path ambiguity.

Hard collision engine checks write/write, write/protected, identity, exclusive resource and exclusive authority collisions. Any hard collision against an active incumbent => FREEZE.

Declared overlap engine uses integer Jaccard basis points with weights 35 domain / 25 capability / 25 deliverable / 15 objective tokens. Default thresholds: >=7600 with deliverable overlap => DECONFLICT; >=4000 => COEXIST; otherwise PROCEED.

Lease evaluator uses caller-supplied timezone-aware now. Only ACTIVE incumbents with leases covering now participate. Default maximum lease is 24h.

Decision sealer binds canonical candidate, sorted registry, UTC time, policy, comparisons and final decision into canonical JSON and SHA-256.

Trust boundary: NCMDE proves deterministic evaluation of declarations, not truthfulness of declarations. Production adoption needs authenticated registration, controlled vocabularies and atomic reservation semantics.