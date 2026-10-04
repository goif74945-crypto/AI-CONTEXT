# Future NEXY Integration Contract

Classification: `PROPOSAL_BY_AI / NOT IMPLEMENTED IN NEXY`

## Proposed placement

```text
NEXY user authority / Task Contract
        |
        v
execution + tool/effect governance (existing/future NEXY mechanisms)
        |
        v
trusted observation adapter  <--- OUTSIDE OAF
        |
        +--> OAF OCC/ODV/OSF/BRG
                     |
              outcome verdict
                     |
              if remediation needed
                     v
                    ORP
                     |
              proposed repair set
                     |
                     v
          NEXY authority/JUDGE decides
```

## Input obligations for an adapter

An adapter MUST:
- bind the OAF contract to the exact authorized objective/task identity;
- provide observations with provenance and freshness appropriate to the claim;
- prevent lower-authority model output from rewriting the contract;
- map NEXY data into JSON without hidden defaults;
- distinguish unknown/unobservable fields from observed negative values;
- preserve user law and protected scopes.

## Output obligations

An adapter MUST treat:
- `PASS` as an outcome-evaluation result, **not automatic release/deploy authority**;
- `PARTIAL` as unmet soft outcomes requiring explicit policy/user handling;
- `FAIL` as observed contract violation;
- `FREEZE` as insufficient/invalid observation or malformed boundary state;
- ORP plan as a proposal requiring normal NEXY authorization and effect governance.

## Compatibility rules

- OAF never replaces `NEXY::JUDGE`.
- OAF never promotes experimental requirements into NEXY Canon.
- OAF does not collect secrets or require provider credentials.
- OAF contract hash should be bound into any future evidence capsule/receipt so outcome evidence cannot be replayed against a different objective.
- If NEXY semantics conflict with OAF proposal semantics, NEXY authority wins and OAF integration must freeze until adapted explicitly.
