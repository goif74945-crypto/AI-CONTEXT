# Future Proposals

Everything in this file is `PROPOSAL_AI`. Nothing here is a current NEXY requirement.

## P1 — Source Matrix Adapter
Build a read-only adapter that converts authoritative rows from the current normalized requirement matrix into CIGE requirement nodes and maps implementation/test/evidence identifiers from verified repository metadata. Reject rows that cannot be mapped exactly.

## P2 — Evidence Freshness Sealing
Bind each evidence node to:
- code/spec revision;
- graph digest;
- test identity/version;
- environment identity where applicable.
A change that reaches that evidence node marks it stale until matching evidence is regenerated.

## P3 — Minimal Validation Set Optimization
When many tests cover overlapping paths, compute a deterministic minimal or policy-weighted validation frontier while preserving mandatory critical tests. This must never reduce required evidence without a formally declared coverage model.

## P4 — Change Budget Policy
Add a governed maximum blast radius by risk class. If a supposedly narrow change impacts an unexpectedly large fraction of critical nodes, FREEZE for explicit review instead of proceeding automatically.

## P5 — Cross-Version Compatibility Graph
Represent versioned contracts as separate nodes and calculate whether a change breaks current consumers, migration tools, historical replay, or rollback targets.

## P6 — Incident Learning Without Auto-Authority
Use past verified incidents to propose missing graph edges or tests, but keep suggestions outside canonical state until human/project authority approves them. No model-generated edge becomes authoritative automatically.

## P7 — Graph Provenance Proof
Attach provenance to each node/edge: source spec anchor, repository path/commit, generated mapping version, and verification status. This prevents a correct algorithm from operating on an untrustworthy graph.

## P8 — Policy-Specific Edge Classes
Split generic `uses/depends_on` into governed classes such as runtime, schema, auth, security, persistence, UI truth, and release-policy dependency. This enables risk-weighted impact without relying on natural-language interpretation.
