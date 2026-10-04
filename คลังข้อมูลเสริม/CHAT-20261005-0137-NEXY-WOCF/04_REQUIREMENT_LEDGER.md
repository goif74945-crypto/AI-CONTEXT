# Requirement Ledger

| ID | Requirement | Implementation | Evidence target | Final status |
|---|---|---|---|---|
| WOCF-R01 | Validate proposal structure | `WorkstreamManifest.from_mapping` | E2 unit | see validation report |
| WOCF-R02 | Reject unsafe/dot-traversal paths | path normalizer | E2 unit | see validation report |
| WOCF-R03 | Keep writes inside namespace by default | manifest validation | E2 unit | see validation report |
| WOCF-R04 | Block protected repository names by policy | evaluator policy check | E2 unit/CLI | see validation report |
| WOCF-R05 | Block workstream ID collision | evaluator | E2 unit | see validation report |
| WOCF-R06 | Block namespace ancestry overlap | path overlap | E2 unit | see validation report |
| WOCF-R07 | Block write-set ancestry overlap | write collision engine | E2 unit | see validation report |
| WOCF-R08 | Block exclusive-resource collision | evaluator | E2 unit | see validation report |
| WOCF-R09 | Detect exact duplicate concept fingerprint | canonical SHA-256 | E2 unit | see validation report |
| WOCF-R10 | Deterministic lexical overlap warning/freeze | lexical overlap | E2 unit | see validation report |
| WOCF-R11 | Read overlap alone must not block | read paths excluded from blockers | E2 unit | see validation report |
| WOCF-R12 | Malformed catalog fails closed | payload evaluator | E2 unit | see validation report |
| WOCF-R13 | Same inputs produce same structured result | canonicalization + sorting | E2 unit | see validation report |
| WOCF-R14 | Catalog ordering does not change result | sorted normalized catalog | E2 unit | see validation report |
| WOCF-R15 | CLI emits machine-readable result and freeze exit code | CLI | E2 CLI/unit | see validation report |
| WOCF-R16 | No external model/runtime dependency | stdlib-only core | E1 | see validation report |
| WOCF-R17 | No NEXY.AI repository mutation | task scope + repository evidence | E0 repo audit | see final audit |
