# Integration Proposal — Proposal Only

**Classification: `Lo4_AI_PROPOSAL_ONLY`. No Canon/build promotion is implied.**

A future authorized NEXY integration could place this suite before irreversible or trust-sensitive transitions:

```text
candidate change
  -> CAWT: counterfactual authority impact
  -> EDEL: proof/evidence freshness
  -> CCF: composed-capability risk
  -> SIMF: discover/falsify candidate invariants (advisory only)
  -> DRCDO: replay equivalence across execution implementations
  -> NEXY-authorized judge/promotion process
```

Recommended boundaries:
- CAWT consumes normalized authority rules and a curated decision-case corpus; it never writes policy.
- EDEL consumes exact subject versions/hashes and evidence metadata; it never upgrades evidence class.
- CCF consumes explicit capability manifests and forbidden privilege conjunctions; no hidden capability discovery is assumed.
- SIMF output must remain quarantined in an experimental/proposal plane until independently specified, reviewed, and promoted.
- DRCDO should bind exact policy/tool/input identities; nondeterministic model behavior requires either a deterministic envelope or a different equivalence contract.

## Promotion prerequisites
1. Map each prototype contract to an authorized NEXY requirement or approve a new requirement.
2. Implement adapters in an authorized branch outside this research folder.
3. Add exact-head integration tests against the real NEXY implementation.
4. Add E4/E5 evidence for user/runtime behavior where relevant.
5. Security review the capability and replay boundaries.
6. Obtain explicit formal promotion into Canon/build scope.
