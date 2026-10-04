# Proposed NEXY Integration Contract

**Status: AI_PROPOSAL / NON_GOVERNING / NOT INTEGRATED.**

This lab does not mutate the NEXY.AI implementation repository. The following are proposed hook boundaries only.

## Composition order

```text
Normalized user/task state
  -> MCAE (only when multiple normalized evidence claims disagree)
  -> CPAC (only for actions that require explicit purpose-bound consent)
  -> existing NEXY LAW/RBAC/authority gates
  -> EMCR (choose among already-admitted interchangeable model workers)
  -> action/execution path
  -> IVS (after an implementation/config change, schedule impacted proofs)
  -> existing evidence ledger/JUDGE/release gates
  -> CDHC (when a resumable task must move to another trusted device/agent context)
```

## Ownership boundaries
- MCAE owns only normalized-claim arbitration. It does not extract modalities or override authoritative LAW.
- CPAC owns only matching explicit consent grants. It does not authenticate, authorize, or delegate.
- EMCR owns only empirical ranking among candidates already admitted by superior policy.
- IVS owns only test scheduling from supplied dependency/coverage metadata. It does not certify coverage or test outcomes.
- CDHC owns only capsule minimization/integrity/expiry/target binding. It does not distribute keys or provide confidentiality.

## Fail-closed composition
Any `FREEZE`, `BLOCK`, `CONFLICT`, or unmet superior NEXY policy prevents downstream execution. `ALLOW` from a supplemental component is never sufficient by itself to authorize a real NEXY action.

## Promotion gate
Before any production adoption, authoritative NEXY requirements must explicitly promote the concept, assign owners/interfaces, map it to the current build matrix, implement adapters, execute integration/E2E/security tests at the exact NEXY revision, and record deployment evidence where applicable.
