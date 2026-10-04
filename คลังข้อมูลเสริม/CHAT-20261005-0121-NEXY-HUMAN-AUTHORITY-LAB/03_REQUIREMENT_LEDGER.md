# Requirement Ledger

Classification: LAB-INTERNAL / AI_PROPOSED_CONCEPT unless marked SOURCE_CONSTRAINT.

| ID | Type | Requirement | Implementation | Evidence target | Current lab status |
|---|---|---|---|---|---|
| HAI-001 | SOURCE_CONSTRAINT | Frozen state must not be visually masked | `evaluatePresentation` | E2 | PASS |
| HAI-002 | SOURCE_CONSTRAINT | UI must not fabricate success | `evaluatePresentation` | E2 | PASS |
| HAI-003 | SOURCE_CONSTRAINT | Visible does not imply executable | `computeDisclosure` + presentation check | E2 | PASS |
| HAI-004 | SOURCE_CONSTRAINT | Missing material information must not be guessed | material-field gate | E2 | PASS |
| HAI-005 | SOURCE_CONSTRAINT | External use is explicit | `allow_external` gate | E2 | PASS |
| HAI-006 | PROPOSAL | Mutation must map to an explicit required outcome ID | objective-alignment gate | E2 | PASS |
| HAI-007 | PROPOSAL | Material questions are aggregated into one interruption | `materialQuestions` | E2 | PASS |
| HAI-008 | PROPOSAL | Interruption budget exhaustion freezes unresolved work | action evaluator | E2 | PASS |
| HAI-009 | PROPOSAL | Irreversible consent binds to exact contract and action hashes | consent gate | E2 | PASS |
| HAI-010 | PROPOSAL | Stale/mismatched consent freezes | consent gate | E2 | PASS |
| HAI-011 | PROPOSAL | Protected scope overrides allowed scope | scope gate | E2 | PASS |
| HAI-012 | PROPOSAL | Progressive disclosure is role/mode/state derived | `computeDisclosure` | E2 | PASS |
| HAI-013 | PROPOSAL | Required PASS without evidence stays NOT_VERIFIED | `evaluateAcceptance` | E2 | PASS |
| HAI-014 | PROPOSAL | Trace checker detects unnecessary/repeated interruptions | `evaluateTrace` | E2 | PASS |
| HAI-015 | PROPOSAL | Canonical hashing ignores object-key insertion order | `canonicalJson` | E2 | PASS |
| HAI-016 | PROPOSAL | Engine performs no network/model/time/randomness calls | source/static inspection | E1 | PASS for current source |
| HAI-017 | PROPOSAL | Fixture corpus contains >=20 distinct adversarial cases | fixtures + validator | E1 | PASS |
| HAI-018 | PROPOSAL | Runtime NEXY integration is not claimed | docs/final audit | E0 | PASS |
| HAI-019 | ADOPTION_GATE | Upstream role/state provenance must be authenticated before production use | not implemented | E3+ | NOT_VERIFIED |
| HAI-020 | ADOPTION_GATE | Full current requirement compatibility must be mapped before promotion | not performed | source audit | NOT_VERIFIED |
| HAI-021 | ADOPTION_GATE | Real user-study benefit must be established without authority regressions | not performed | experiment | NOT_VERIFIED |
| HAI-022 | ADOPTION_GATE | Accessibility and localization behavior must be tested | not performed | E4/usability | NOT_VERIFIED |

## Authority note

Rows labeled SOURCE_CONSTRAINT are interpretations of existing NEXY context used to constrain this lab. They are not a claim that this reference code is the canonical implementation of those source requirements.
