# EXECUTION STATE — NEXY Privacy Context Firewall

- mission_id: CHAT-20261005-0121-NEXY-PRIVACY-CONTEXT-FIREWALL
- project_name: NEXY Privacy Context Firewall (PCF)
- proposal_class: AI_PROPOSED_SUPPLEMENTAL_CONCEPT
- persistence_mode: DURABLE_RESUMABLE
- repository: goif74945-crypto/AI-CONTEXT
- branch: main
- baseline_head_observed: 07a90db5e615bedfcf1b1c73024793a91889df3d
- phase: PLAN_LOCKED
- status: EXECUTING
- created_at: 2026-10-05T01:21:00+07:00

## Authority
1. Explicit current user directive.
2. AI-CONTEXT/AI-EXECUTION-KERNEL.md.
3. AI-CONTEXT rules, especially GLOBAL, SECURITY, VERIFICATION.
4. projects/NEXY.AI/overview.md and the current 837-row normalized matrix boundary.
5. External official references only as research support, never as NEXY project law.

## Scope lock

### IN SCOPE
- New files only under this mission folder.
- Privacy/data-minimization architecture useful to future NEXY integration.
- A standalone executable reference compiler/gate.
- Unit tests, fixtures, schemas, threat model, integration contract, verification evidence.
- AI-proposed future extensions clearly labeled as proposals.

### PROTECTED / OUT OF SCOPE
- Any mutation to any repository whose name contains NEXY.AI.
- Any mutation outside this mission folder in AI-CONTEXT.
- Claiming this proposal is an existing NEXY requirement or implemented NEXY behavior.
- Real secrets, credentials, private user data, production traffic, or production deployment.
- Legal/compliance certification claims.

## Current gap established
The current supplemental vault has extensive work on evidence, epistemic control, counterfactual reasoning, compatibility, resilience, long-horizon reliability, and knowledge lifecycle. Targeted repository scans found no existing privacy/data-minimization/retention/redaction project naming or direct topic hits. This establishes a useful orthogonal research/build direction, not proof that every historical file was semantically exhaustive.

## Objective
Build a deterministic Privacy Context Firewall that compiles a task context into the minimum provider/tool payload allowed by explicit data policy, or FREEZEs with machine-readable reasons.

## Planned core behaviors
- explicit data classification
- purpose-bound field admission
- deterministic minimum-disclosure projection
- provider/tool egress policy
- retention lease generation
- secret-safe audit receipts
- fail-closed handling for unknown classification/purpose/policy
- reproducible CLI and tests

## Work DAG
- W01 authority/gap verification: PASS
- W02 mission checkpoint creation: EXECUTING
- W03 test-first contract: PENDING
- W04 reference implementation: PENDING
- W05 schemas/fixtures: PENDING
- W06 unit/static verification: PENDING
- W07 adversarial/negative-path verification: PENDING
- W08 read-back + final audit: PENDING
- W09 completion certificate: PENDING

## Exact next legal action
Create test-first local reference package, observe RED for missing implementation, implement the smallest complete compiler, then run full unit/static verification before persisting the code set.

## Resume rule
On resume, read this file first, re-read 01_TASK_CONTRACT.md, verify current repository state, then continue from the first non-PASS work item. Do not touch other chat folders.
