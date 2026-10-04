# Design — NEXY Correlation-Aware Consensus Guard (CACG)

**Status:** AI-PROPOSED / NON-AUTHORITY / NOT PRODUCTION INTEGRATED.

## Objective
Prevent false confidence when agents share provider/model/retrieval/tool dependencies.

## Algorithm
Canonicalize votes; build transitive correlation components over shared dependency domains using union-find; apply evidence floor; let each correlated component count once at its strongest eligible trust weight; internal component disagreement abstains; require weighted quorum and a minimum number of independent supporting components.

## Invariants
Deterministic fingerprint; correlated clones cannot inflate weight; missing dependency provenance rejects; ties/insufficient independence/material correlated disagreement freeze.

## Complexity
Approximately O(V α(V)+D) plus canonical sorting.

## Future NEXY boundary
Candidate after SWARM worker judgments and before JUDGE/release. Dependency provenance must be authoritative. CACG never becomes final authority.

## Limits
Caller metadata is not self-proving; production adoption needs signed/fresh dependency provenance.

## Security boundary
No network access, credential handling, repository mutation, production side effect, or NEXY law override occurs in the reference engine. A future adapter must validate provenance and authorization.
