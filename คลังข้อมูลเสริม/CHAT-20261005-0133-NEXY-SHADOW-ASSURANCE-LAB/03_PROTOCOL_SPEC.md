# Shadow Decision Record Protocol

**Classification: AI-PROPOSED compatibility protocol.**

Each JSONL line is one object with:

- `case_id`: stable comparison identity;
- `input_fingerprint`: hash/identity of normalized input, not raw input;
- `revision`: exact candidate/stable revision identity;
- `policy_fingerprint`: exact governing policy snapshot identity;
- `authority_chain`: ordered precedence list;
- `outcome`: `RELEASE | FREEZE | STOP`;
- `action`: required only for RELEASE and forbidden for FREEZE/STOP;
- `required_evidence_classes`: exact classes required for this decision;
- `evidence[]`: `{class, ref, revision}`;
- `safety_labels[]`: compact invariants/tags that must not silently disappear.

## Comparison rules

1. Different input fingerprint -> `INPUT_MISMATCH`, stop pair comparison.
2. Different policy fingerprint -> `POLICY_DRIFT`, blocking until rebaselined under authority.
3. Stable authority chain must remain an exact prefix of candidate authority chain.
4. Candidate evidence with `evidence.revision != candidate.revision` -> `STALE_EVIDENCE`.
5. Required classes must have matching evidence objects; evidence-class substitution is not inferred.
6. Candidate cannot remove baseline required evidence classes.
7. Stable FREEZE/STOP -> candidate RELEASE -> `FREEZE_BYPASS`.
8. RELEASE -> RELEASE with changed action -> `ACTION_DIVERGENCE`.
9. Candidate removal of stable safety labels -> `SAFETY_LABEL_REGRESSION`.
10. Different candidate records sharing one case ID -> `NONDETERMINISTIC_CANDIDATE`.

## Deliberate conservatism

Some divergences may eventually be authorized and correct, but this prototype refuses to invent authorization. The intended workflow is: detect -> explain -> establish new authority/baseline -> re-run.
