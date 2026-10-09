# AI.AI | Independent critique, innovation, and tested-code workspace

Repository: goif74945-crypto/AI-CONTEXT. Existing branch: main. Authorized write prefix: AI.AI/ only.

This is a separate workspace for reviewing the AI.AI agent product, proposing system improvements, and delivering test-proven code. It is NOT product source. Historical records under PROJECTS/AI.AI remain untouched.

## Mandatory rules for EVERY contributing chat

1. Read CONSTITUTION.md, REGISTRY.md, all related proposals, and the actual AI.AI source/revision before doing anything.
2. Every chat must deliver BOTH (a) a distinct, evidence-backed criticism of an AI.AI defect/gap and (b) a distinct system improvement or repair with working source/patch and reproducible positive/negative tests.
3. Search and compare all registered criticism signatures, semantic effects, fingerprints, and impacted code before claiming uniqueness. A renamed duplicate is rejected.
4. All product modifications are forbidden here; code is staged ONLY under AI.AI/PROPOSALS/. Patches are applied solely to isolated test copies.
5. DO NOT change any directory named โค้ดโปรเจคปัจจุบัน or its contents, wherever that directory exists. Do not touch PROJECTS/AI.AI, NEXY.AI-, any other repository, branches, settings, or secrets.
6. Pin source SHA/ZIP hash and actual test logs, mark mocks as MOCKED and blocked hardware tests as BLOCKED. Never assert success without runtime proof.
7. Recheck current main HEAD and registry before every commit. Use one atomic commit and expected-HEAD guard, reject clashes, verify GitHub read-back.

### Structure

- CONSTITUTION.md: authoritative limits, evidence criteria and stop conditions.
- REGISTRY.md: registered criticism/idea signatures and acceptance states.
- TEMPLATES/SUBMISSION.md: new-chat requirements.
- PROPOSALS/AAI-YYYYMMDD-NNN-slug/: independently tested integration patch, tests and evidence for one unique contribution.
- tools/validate_catalog.py: offline SHA/path/field collision check, not a substitute for semantic review or E2E tests.

### Initial contribution

AAI-20261009-001-file-read-integrity fixes proven silent result truncation of file.read on AI.AI v0.2.0. 117/117 Python tests passed on a COPY of the v0.2.0 sources. This proposal is TESTED_ON_PINNED_REVISION, not product-merged or certified compatible with v0.3.0.

Historical AI-CONTEXT PROJECTS/AI.AI reports document a later v0.3.0 local build; do NOT infer its source contents from the v0.2.0 ZIP.
