# NEXY Incident Semantics Drift — 2026-09-24

- Audit run: `AUDIT-NEXY-FULL-20260924-01`
- Target: `goif74945-crypto/NEXY.AI-@84484d8108fe1dee186450c0d36c26d360b2596e`
- Cause: incident persistence/schema does not encode DOC-C multiple-failure priority/secondary semantics and does not constrain primary incident error codes to canonical `ErrorCode`.
- Violations: DOC-C paragraphs 7519-7527, 8006-8016, 8952-8956.
- Impact: later lower-priority failure can replace primary failure evidence; noncanonical strings can enter incident evidence.
- Findings: `F-NEXY-REAUDIT-N-INCIDENT-PRIORITY-001`, `F-NEXY-REAUDIT-N-INCIDENT-ERRORCODE-002`.
- Fix status: not attempted; implementation mutation remains forbidden during full-audit gate.
- Prevention: canonical ErrorCode validation at incident boundary; deterministic priority arbitration; secondary failure persistence; negative/replay tests.
- Regression requirement: repeated competing failures must preserve the highest-priority primary and retain all lower-priority failures as secondary evidence.
