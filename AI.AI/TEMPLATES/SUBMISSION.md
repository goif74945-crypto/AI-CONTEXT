# Mandatory submission structure for every AI.AI chat

1. Read CONSTITUTION.md and REGISTRY.md; enumerate all sibling proposals and get current AI-CONTEXT/main HEAD.
2. Pin the real AI.AI target source revision and ZIP SHA-256. Check PROJECTS/AI.AI records, but do not confuse them with present source.
3. Write a **new** evidence-backed criticism: path/function, bad input/output, expected contract, severity, tests and source pin.
4. Write a **new** system idea/repair: design, API, permissions, threat model, failure modes, compatibility and objective acceptance tests.
5. Compare both criticisms and ideas semantically against all existing proposals. Never duplicate a chat's problem/effect even under a new name.
6. Create PROPOSALS/<AAI-id>-<slug>/manifest.json, README.md, integration.patch including tests, TEST_EVIDENCE.md. No placeholder code. No changes to โค้ดโปรเจคปัจจุบัน.
7. In a TEMPORARY COPY at exact pinned revision: git apply --check integration.patch; git apply integration.patch; run focused AND all product tests; collect real outputs and hashes.
8. Run python AI.AI/tools/validate_catalog.py --root AI.AI. Static PASS is NOT proof of runtime tests or semantic uniqueness.
9. Recheck AI-CONTEXT/main HEAD, sibling claims, protected paths; commit atomically with expected HEAD, then read-back. On conflict, reevaluate, never force-overwrite.
10. Set TESTED_ON_PINNED_REVISION only when tests actually passed. Set MERGE_READY only when verified against CURRENT AI.AI product source; do not claim product integration until an authorized product merge is proven.
