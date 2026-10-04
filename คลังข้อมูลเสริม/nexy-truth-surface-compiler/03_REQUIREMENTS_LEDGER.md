# Requirements Ledger

| ID | Requirement | Type | Evidence target | Current prototype status |
|---|---|---|---|---|
| NXTS-R001 | Same normalized input produces byte-stable semantic output | Determinism | unit test | PASS in local validation |
| NXTS-R002 | Claim list order must not change output | Determinism | unit test | PASS in local validation |
| NXTS-R003 | Material UNKNOWN blocks release | Truth integrity | unit test | PASS in local validation |
| NXTS-R004 | Material CONFLICT blocks release | Truth integrity | unit test | PASS in local validation |
| NXTS-R005 | Material NOT_VERIFIED blocks release | Truth integrity | unit test | PASS in local validation |
| NXTS-R006 | Material fact without evidence reference blocks release | Evidence boundary | unit test | PASS in local validation |
| NXTS-R007 | Unknown status fails closed | Compatibility/failure | unit test | PASS in local validation |
| NXTS-R008 | INTERNAL/SENSITIVE text is not exposed as public content | Information boundary | unit test | PASS in local validation |
| NXTS-R009 | Common API/JWT-looking tokens are redacted from public text | Defense in depth | unit test | PASS in local validation |
| NXTS-R010 | Output includes tamper-detecting deterministic digest | Integrity | unit test | PASS in local validation |
| NXTS-R011 | RELEASE/FREEZE CLI outcomes have machine-usable exit codes | Tooling | subprocess test | PASS in local validation |
| NXTS-R012 | Compiler must not become an authority source | Architecture | design review only | NOT_VERIFIED in any integration |
| NXTS-R013 | Production redaction must prevent all relevant secret leakage | Security | adversarial DLP tests | NOT_VERIFIED / prototype explicitly insufficient |
| NXTS-R014 | Live NEXY integration must preserve current authority/order semantics | Compatibility | exact-head integration/E2E | NOT_VERIFIED / not attempted |
