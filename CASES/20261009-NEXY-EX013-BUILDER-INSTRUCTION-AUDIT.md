# CASE 20261009-NEXY-EX013-BUILDER-INSTRUCTION-AUDIT
CATEGORY: CORRECTNESS/TOOLCHAIN/RELEASE_GATE
STATUS: OPEN_UNDER_BUILDER_REPAIR
EVIDENCE: EX012 broad test run 905/911 success and 6 failures on Product law-commit HEAD: 2 cargo ENOENT, 2 Tier-depth compile failures with null exit/undefined stderr, 2 current-head-attestation fixture child status=1.
ROOT_CAUSE_CLASSES: cargo tool absent is observed for two; rustc absence is a HYPOTHESIS for Tier-depth until result.error/version reproduced; attestation is UNKNOWN (must capture child stderr/stdout before patch).
CONSTITUTIONAL_RISK: tests are required semantic boundaries (Rust authority, max Tier5, immutable current-head provenance). Lowering tests or inserting fallback fake PASS would invalidate audit.
FIX_ORIENTED_ACTION: use connected authorized runner via Remote Desktop Commander, GitHub or legitimate other plugin, prove failures and recover capability, minimal source-targeted repairs only where actual defect, then re-run against exact current HEAD. Commit only safe verified source and regression, then independent audit.
CONTROL_PATH: COMMANDS/20261009-NEXY-NORMAL-CHAT-EXECUTION-013-BUILDER.md.
EVIDENCE_CHAIN: source -> failure reproduction -> root cause -> minimally diff -> RED/GREEN -> regression -> commit+readback -> independent auditor.
