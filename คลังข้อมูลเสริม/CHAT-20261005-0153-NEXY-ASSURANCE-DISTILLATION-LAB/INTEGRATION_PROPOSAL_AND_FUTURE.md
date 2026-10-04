# Integration Proposal and Future Ideas

## Status
Everything in this file is **AI-PROPOSED**. Nothing here is promoted into current NEXY law or implementation.

## Potential future integration points

### CED
After a verifier/test fails, an authorized adapter could distill the failing structured input before storing it in the Vault or displaying a developer-facing witness. CORE/JUDGE remains authoritative.

### MUCF
When CIRL/CLE or a planning layer produces a finite explicit candidate set with incompatible constraints, MUCF could explain the smallest conflicting constraint subset instead of returning a vague “no solution”.

### EFRP
Before reusing cached proof/evidence, an adapter could run EFRP against current versions and evidence dependencies. A FREEZE result means revalidation is required; it does not itself authorize reruns or mutations.

### SECL
Documentation/spec CI could lint structured examples against machine-readable rules so user-facing docs do not drift away from actual contracts.

### VRPP
A freeze/recovery UX could ask VRPP for an evidence-gated route back to a declared safe state. The output is a plan only; ECL/Safety/authority layers must separately authorize and execute each transition.

## Adoption gate
No system should be integrated merely because this standalone prototype passes unit tests. Adoption requires:
1. authoritative NEXY adapter contracts;
2. mapping to actual NEXY state/evidence schemas;
3. E3 integration tests;
4. E4 user-flow tests where user-facing;
5. abuse/resource testing;
6. regression against current NEXY requirements;
7. explicit promotion decision by project authority.

## Additional future-only concepts
1. **Counterexample Corpus Curator** — deduplicate and cluster verified failure witnesses without hiding distinct root causes.
2. **Constraint Negotiation Preview** — show which constraints could be relaxed and the exact authority needed, without auto-relaxing them.
3. **Proof Refresh Budgeter** — rank stale evidence refresh work under explicit cost/time ceilings while never treating deferred evidence as valid.
4. **Executable Documentation Coverage Map** — map rule IDs to examples/tests and expose unillustrated or untested laws.
5. **Recovery Plan Sensitivity Analyzer** — show which missing evidence item would change the safe recovery frontier.

These five secondary ideas are proposals only and are not implemented in this mission.
