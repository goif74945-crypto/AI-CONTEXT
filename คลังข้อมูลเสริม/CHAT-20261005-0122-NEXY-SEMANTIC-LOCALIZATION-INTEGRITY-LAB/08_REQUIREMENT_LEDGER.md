# Requirement Ledger

| ID | Requirement | Authority | Implementation | Evidence target | Status before repository integration |
|---|---|---|---|---|---|
| R01 | AI-CONTEXT only mutation | User | session path boundary | GitHub path audit | NOT_VERIFIED |
| R02 | No NEXY.AI repo mutation | User | execution boundary | tool/action audit | NOT_VERIFIED |
| R03 | Distinct from concurrent sibling labs | User | divergence inspection | repository searches/recent commits | PASS |
| R04 | Proposal clearly non-authoritative | AI-CONTEXT law | report/docs labels | tests + file inspection | PASS |
| R05 | Number preservation | Proposal | extractor/comparator | unit tests | PASS |
| R06 | Semantic unit preservation | Proposal | unit alias normalizer | unit tests | PASS |
| R07 | Placeholder preservation | Proposal | placeholder extractor | unit tests | PASS |
| R08 | URL/email preservation | Proposal | extractors | unit tests | PASS |
| R09 | Identifier preservation | Proposal | identifier extractor | unit tests | PASS |
| R10 | Canonical/protected token preservation | Proposal | token/literal checks | unit tests | PASS |
| R11 | Normative modality preservation | Proposal | EN/TH semantic rules | adversarial tests | PASS |
| R12 | Negation polarity preservation | Proposal | EN/TH negation rules | adversarial tests | PASS |
| R13 | Unsupported languages do not pass | Proposal + no-guess principle | strict unsupported-language block | negative test | PASS |
| R14 | Deterministic report fingerprint | Proposal + deterministic design target | stable canonicalization + SHA-256 | 100-run test | PASS |
| R15 | Dependency-free isolated execution | Design constraint | Node built-ins only | package inspection + run | PASS |
| R16 | Exact committed bytes pass tests | Verification law | post-commit reconstruction | E1/E2 rerun | NOT_VERIFIED |
| R17 | Final evidence and audit | User/AI-CONTEXT law | evidence docs | re-fetch | NOT_VERIFIED |
