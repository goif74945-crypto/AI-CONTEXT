# Integration Boundary

## Proposed placement
CAM is best treated as an auxiliary preflight/verification mesh around existing NEXY authority boundaries, not as a new authority layer.

Suggested conceptual flow:

`USER/DIALOG → ambiguity enumeration → ICG → context assembly → CNS → verification obligations → EAP → executed evidence → IEQE → execution checkpoint/handoff → REC → existing LAW/JUDGE release boundary`

## Non-bypass law
- ICG cannot decide law; it only proves convergence of already-admissible interpretations.
- CNS cannot authorize a context field; it only checks finite noninterference cases.
- EAP cannot downgrade evidence class or declare tests passed.
- IEQE cannot manufacture evidence; it only checks independence of supplied evidence records.
- REC cannot revive expired authority or stale target identity; those remain upstream freshness obligations.
- The integration coordinator returns `READY` only as **AI_PROPOSED_ADVISORY_PREFLIGHT_NOT_NEXY_JUDGE**.

## Data adapters required for a real NEXY integration
1. Adapter from NEXY intent/ambiguity representation to `Interpretation` + `DecisionSignature`.
2. Adapter from NEXY context router to finite `MutationSet` policies.
3. Adapter from requirement/evidence obligations to `ClaimNeed` and executable `Probe` catalog.
4. Adapter from handoff/checkpoint state to `ResumeState` critical/ephemeral partition.
5. Adapter from audit/test evidence provenance to `EvidenceRecord` producer, failure domains, and derivation graph.

These adapters are **not implemented against NEXY.AI in this mission** because that repository is protected by user instruction.
