# Future NEXY Integration Proposal

**Status: AI_PROPOSED / NOT_CURRENT_BUILD / NOT_IMPLEMENTED_IN_NEXY.AI**

The five engines are designed as narrow advisory/gating modules around existing NEXY authority boundaries. A future adoption path could be:

```text
User Directive
   |
   +--> GCG: does the proposed work graph earn every task against acceptance criteria?
   |
   +--> VCC: is there a policy-compliant capability chain capable of producing the target?
   |
   +--> SCTG: are candidate tool/dependency artifacts admissible under trust policy?
   |
   v
Existing NEXY admission / scheduler / execution / verification
   |
   v
Artifact produced and verified
   |
   +--> ACFG: is the artifact consumable by the declared destination?
   |
   v
VIEW / export / controlled handoff

MPC is orthogonal: it can generate a guided prerequisite path for a human operator before advanced capabilities are exposed.
```

## Adoption gates

No engine should be promoted merely because its standalone tests pass. Integration would require:

- authoritative interface mapping to current NEXY contracts;
- exact schema versioning;
- policy ownership decisions;
- real capability-registry ingestion tests for VCC;
- real artifact/export boundary tests for ACFG;
- dependency/package source-of-truth decisions for SCTG;
- UX/E2E tests for MPC;
- regression proof that no gate can bypass CORE/JUDGE/FREEZE semantics;
- deployment/runtime evidence at the exact integrated revision.

## Rollback principle

All five should be additive and bypassable only by an explicit authorized configuration that restores the prior NEXY path. None should rewrite canonical historical state during evaluation. That keeps experimental adoption reversible.
