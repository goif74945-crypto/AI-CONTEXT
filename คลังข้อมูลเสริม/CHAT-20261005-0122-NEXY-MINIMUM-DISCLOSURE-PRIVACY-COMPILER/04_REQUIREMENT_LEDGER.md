# Requirement Ledger

| ID | Requirement | Authority | Implementation | Evidence target | Status |
|---|---|---|---|---|---|
| NMD-001 | Exact non-empty purpose required | AI_PROPOSED + zero-guess alignment | `TaskRequest.validate` | E2 | PASS_LOCAL |
| NMD-002 | Recipient trust UNKNOWN freezes | AI_PROPOSED + fail-closed alignment | `Recipient.validate` | E2 | PASS_LOCAL |
| NMD-003 | Non-required fields omitted | AI_PROPOSED minimum disclosure | `_decide_field` | E2 | PASS_LOCAL |
| NMD-004 | Purpose mismatch freezes | AI_PROPOSED purpose binding | `_decide_field` | E2 | PASS_LOCAL |
| NMD-005 | Credential values never disclosed | AI-CONTEXT security alignment | credential branch + bundle builder | E2 | PASS_LOCAL |
| NMD-006 | External-model SECRET always freezes | AI_PROPOSED strict boundary | secret branch | E2 | PASS_LOCAL |
| NMD-007 | Private external disclosure requires explicit consent | AI_PROPOSED + human authority alignment | private branch | E2 | PASS_LOCAL |
| NMD-008 | Sensitive external disclosure prefers transform | AI_PROPOSED privacy minimization | transform path | E2 | PASS_LOCAL |
| NMD-009 | Retention clamped to lower bound of request/policy | AI_PROPOSED lifecycle control | `_decision` | E2 | PASS_LOCAL |
| NMD-010 | Raw payload excluded from plan/fingerprint | AI_PROPOSED data minimization | compile/build separation | E2 | PASS_LOCAL |
| NMD-011 | Frozen plan cannot produce bundle | AI_PROPOSED fail-closed | `build_bundle` | E2 | PASS_LOCAL |
| NMD-012 | Canonical output independent of rule order | NEXY deterministic target | sort + canonical JSON | E2 | PASS_LOCAL |
| NMD-013 | Duplicate field rules freeze | AI_PROPOSED ambiguity control | compile preconditions | E2 | PASS_LOCAL |
| NMD-014 | Runtime tokenization key required for TOKENIZE | AI_PROPOSED secret separation | `_transform` | E2 | PASS_LOCAL |
| NMD-015 | No NEXY.AI repository mutation | explicit user constraint | execution boundary | E0/repo audit | PENDING_COMMIT_AUDIT |
| NMD-016 | No current-build promotion claim | authority boundary | docs/status labels | E0/review | PENDING_COMMIT_AUDIT |

`PASS_LOCAL` means the isolated reference implementation has matching local E2 evidence. It does **not** mean NEXY current-product behavior is proven.
