# NCIF Future Integration Proposal

**Classification:** AI-PROPOSED / NON-GOVERNING / NOT IMPLEMENTED IN NEXY.AI

## Integration objective

Insert an evidence-independence check between multi-agent evidence collection and final JUDGE adjudication without changing NEXY authority semantics.

## Proposed flow

```text
Directive / Task Contract
        ↓
SWARM work + independent verification plan
        ↓
Evidence records with authenticated provenance
        ↓
NCIF adapter builds bounded evidence DAG + votes
        ↓
NCIF result
  ├─ FREEZE → JUDGE receives blocker/trace
  └─ CONSENSUS_CANDIDATE → JUDGE continues normal truth/policy checks
```

## Required production contracts before adoption

1. **Authenticated evidence identity** — stable IDs bound to signed/verified provenance rather than caller prose.
2. **Source identity ontology** — canonical identity rules for documents, tool calls, datasets, runtime traces, repositories and model outputs.
3. **Correlation authority** — who may assert dataset/provider/context/tool common-cause keys and how disputes are resolved.
4. **Revision binding** — every source identity must bind to exact version/hash/time where material.
5. **Policy authority** — thresholds and resilience requirements come from project law/config, not UI/requester convenience.
6. **Bounded admission** — max nodes, edges, votes, key count and string length before evaluation.
7. **Audit receipt** — persist decision fingerprint, policy identity, evidence graph identity and exact engine version.
8. **JUDGE semantics** — `CONSENSUS_CANDIDATE` only satisfies an independence precondition; it cannot satisfy truth correctness alone.
9. **NPRG handshake** — planner-level independent verifier selection and result-level evidence independence should be complementary, not conflated.
10. **Privacy contract** — raw provenance metadata access is restricted; diagnostics expose only necessary references/digests.

## Suggested compatibility adapter

Future adapter interface, conceptual only:

```text
build_ncif_payload(task_id, claim_id, evidence_records, agent_findings)
    -> NCIFInput

evaluate_consensus(NCIFInput, governed_policy)
    -> NCIFReceipt

judge(task_state, evidence, ncif_receipt)
    -> existing JUDGE decision path
```

No code in this lab assumes an actual NEXY API route or database schema.

## Adoption gates

- G1: authoritative architecture review approves role/boundary.
- G2: source-identity and correlation ontologies defined.
- G3: schema adapter tested against real NEXY evidence objects.
- G4: abuse tests prove fake duplicate sources do not inflate group count.
- G5: false-correlation/DoS scenarios have controlled review path.
- G6: performance budgets established with production-sized graphs.
- G7: privacy review validates diagnostic leakage boundary.
- G8: JUDGE integration E3 tests prove candidate cannot bypass normal truth/law gates.
- G9: E4 critical workflow proves human-visible freeze reason without false success.
- G10: exact-revision E5/E6 proof required before operational/deployment claims.
