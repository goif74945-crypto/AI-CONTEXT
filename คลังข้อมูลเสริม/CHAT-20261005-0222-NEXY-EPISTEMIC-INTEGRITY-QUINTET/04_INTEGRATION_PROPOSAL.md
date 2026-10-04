# Future NEXY Integration Proposal

**Status:** PROPOSAL ONLY. No integration was performed.

Suggested future flow:

```text
Authoritative request/law/policy/evidence
        ↓
explicit normalization adapter
        ↓
ECOF + ACE + DMAG + PDZA + RKM
        ↓
AdvisoryIntegrityGate (READY | FREEZE)
        ↓
existing NEXY authority / verification / JUDGE boundary
```

## Promotion prerequisites
1. Map canonical NEXY claim/evidence identities without losing authority/provenance semantics.
2. Source DMAG dimensions and verdict order from authoritative policy, never examples.
3. Use PDZA only over exact bounded domains or explicitly label weaker sampling as non-exhaustive.
4. Bind RKM premise digests/authority epochs to canonical NEXY revisions and revocation semantics.
5. Define NEXY-to-ACE premise classes under authority; ACE itself cannot promote assumptions.
6. Keep READY below all existing execution authorization and JUDGE boundaries.

## Suggested adoption order
ACE audit/reporting → ECOF proof-graph validation → DMAG policy regression → PDZA offline policy audit → RKM verification planning.

Any promotion requires a separate authorized task, exact target revision, compatibility analysis, matching evidence class, regression/security evidence where applicable, and explicit approval.
