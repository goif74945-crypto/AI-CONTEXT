# Input Contract Schema (informal v0.1)

The executable parser in `interaction_contract/model.py` is the current reference for v0.1.

```json
{
  "contract_id": "string",
  "authorized_scopes": ["scope"],
  "protected_scopes": ["scope"],
  "directives": [
    {
      "id": "D1",
      "text": "human-readable directive",
      "kind": "requirement|constraint|forbidden|preference|acceptance",
      "criticality": "critical|high|normal|low",
      "scopes": ["scope"],
      "conflicts_with": ["D2"],
      "resolved": true
    }
  ],
  "events": [
    {
      "seq": 1,
      "actor": "assistant",
      "type": "clarification|action|evidence|completion|note",
      "directive_ids": ["D1"],
      "scopes": ["scope"],
      "assumptions": ["explicit assumption"],
      "outcome": "pass|fail|blocked|unknown|not_verified",
      "evidence_ref": "stable reference",
      "completion_status": "complete|incomplete|blocked|not_verified"
    }
  ]
}
```

## Important semantic boundary
`conflicts_with` is explicit data. The analyzer does not guess conflicts from text.

`authorized_scopes` is exact-match in v0.1. A future scope grammar must not be silently retrofitted because prefix/wildcard semantics can accidentally widen authority.
