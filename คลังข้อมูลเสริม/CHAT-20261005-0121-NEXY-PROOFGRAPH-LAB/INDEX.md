# NEXY ProofGraph Lab — Local Index

> **AI-PROPOSED / EXPERIMENTAL / NOT CANON**

Load only what the current task needs.

## Entry points

- [README](./README.md) — purpose, scope and CLI usage.
- [Design](./DESIGN.md) — architecture, invariants, failure model and security boundary.
- [Requirement ledger](./REQUIREMENT-LEDGER.md) — requirement → implementation → evidence mapping.
- [Task contract](./TASK-CONTRACT.json) — mutation boundary and acceptance contract.
- [AI-proposed future concepts](./AI-PROPOSED-CONCEPTS.md) — non-canonical future ideas.
- [Session checkpoint](./SESSION-CHECKPOINT.md) — resumable execution state.
- [Execution record](./EXECUTION-RECORD.json) — stable execution ID, chat-ID availability status, and evidence summary.
- [Non-duplication note](./NON-DUPLICATION-NOTE.md) — boundary against concurrently-created sibling labs.
- [Local test evidence](./evidence/LOCAL-TEST-REPORT.md) — executed sandbox evidence.
- [Repository write evidence](./evidence/REPOSITORY-WRITE-REPORT.md) — verified GitHub insertion and protected-scope audit.

## Machine interfaces

- [Scan result schema](./schemas/scan-result.schema.json)
- [Truth-lock schema](./schemas/truth-lock.schema.json)
- [Link graph schema](./schemas/link-graph.schema.json)
- [NEXY context policy](./policy/nexy-context-policy.json)

## Source

Python package: `src/nexy_proofgraph/`  
Tests: `tests/`
