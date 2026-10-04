# Integration Proposal for NEXY.AI

> **PROPOSAL ONLY. NOT CURRENT NEXY BUILD LAW. NO NEXY.AI CODE WAS MODIFIED.**

## Proposed placement

```text
Directive / Plan Candidate
          |
          +--> C1 Contract Composition Gate
          |
          +--> C2 Emergent Capability Risk Gate
          |
          v
   Existing NEXY LAW / CORE / SWARM / JUDGE pipeline
          |
          +--> C3 Evidence Portability Gate before proof reuse
          |
          +--> C4 Correction Contract emission after authorized human correction
          |
          +--> C5 Failure Distillation for stable incident/eval signatures
```

## Required integration work before adoption
1. Map literal contracts in C1 to authoritative typed NEXY component contracts.
2. Bind C2 taint/capability labels to versioned AgentAdapter/tool contracts with evidence.
3. Define authoritative C3 portability dimensions per evidence/claim type; do not use one global policy for all claims.
4. Place C4 behind explicit correction authorization, evidence confirmation, provenance, and revocation/supersession governance.
5. Bind C5 oracle to deterministic replay or exact-version test receipts whenever possible.
6. Add TypeScript/Next.js-compatible adapters if current DOC-C implementation requires them.
7. Run actual NEXY integration/unit/E2E tests at exact revision before making any runtime claim.

## Adoption order
Recommended research order:
1. C3, because stale/misapplied evidence can corrupt all downstream completion claims.
2. C2, because cross-tool composition creates risk not visible in per-tool admission.
3. C1, once stable typed contracts exist.
4. C5, to accelerate diagnosis/evals for C1/C2/JUDGE/LAW failures.
5. C4, only after correction authority/provenance lifecycle is fully specified.

This order is an AI proposal, not authority.
