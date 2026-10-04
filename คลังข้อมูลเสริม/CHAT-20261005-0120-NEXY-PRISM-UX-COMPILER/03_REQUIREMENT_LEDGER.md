# NEXY::PRISM Requirement Ledger

| ID | Requirement | Rationale | Implementation | Evidence |
|---|---|---|---|---|
| PRISM-R01 | Backend deny must never become UI allow | NEXY auth/UI truth boundary | `_decide_action` | E2 unit + matrix |
| PRISM-R02 | Final only when backend release=true, state=STABLE, evidence=PASS | DOC-C release/UI truth | `_trust_label`, `_decide_action` | E2 |
| PRISM-R03 | FREEZE must visibly remain FREEZE | DOC-C/D freeze law | `_banner`, disclosures | E2 |
| PRISM-R04 | STOP allows diagnostic read only | fail-safe presentation | `_decide_action` | E2 |
| PRISM-R05 | Compact preference cannot hide required risk/truth | UI truth | `_required_detail_floor` | E2 |
| PRISM-R06 | Irreversible action requires typed confirmation | fail-safe UX | `_confirmation` | E2 |
| PRISM-R07 | Auditor/public/system surfaces do not gain mutation controls | authority preservation | role surface map | E2 |
| PRISM-R08 | Contradictory release facts fail closed | zero-guess principle | `_detect_conflicts` | E2 |
| PRISM-R09 | Same input -> same plan/fingerprint | deterministic direction | canonical JSON + SHA-256 | E2 |
| PRISM-R10 | Mandatory truth independent of optional detail | progressive disclosure | `_mandatory_disclosures` | E2 |
| PRISM-R11 | Existing NEXY.AI repos untouched | user scope | isolated AI-CONTEXT path | final inspection |
| PRISM-R12 | Concept not silently added to 837-row build denominator | authority boundary | explicit classification | E0 |

This ledger is for the standalone prototype only and does not promote PRISM into DOC-C or the current normalized NEXY matrix.
