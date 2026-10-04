# Task Contract

## Objective
Create a novel, future-useful NEXY supplemental project in AI-CONTEXT without modifying any NEXY.AI repository. The project must include design, implementation, executed tests, failure handling, verification evidence, and durable resume context.

## Target
`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0121-NEXY-TRUST-UX-CONTRACT-LAB`

## Authorized scope
- Read AI-CONTEXT project/spec context.
- Read NEXY project context and existing supplemental inventory.
- Create new additive files under the target folder in AI-CONTEXT.
- Build/test a standalone reference implementation in an isolated local sandbox before persistence.

## Protected scope
- Any repository whose name contains `NEXY.AI`.
- Existing supplemental projects from other chats.
- Canonical NEXY project truth outside this new advisory folder.
- Secrets, credentials, tokens, PII.

## Authority sources
1. Explicit current user directive.
2. `AI-EXECUTION-KERNEL.md`.
3. `rules/GLOBAL.md`, `rules/SECURITY.md`, `rules/VERIFICATION.md`.
4. NEXY project context under `projects/NEXY.AI/`.
5. Existing supplemental inventory for deduplication only.

## Preconditions
- AI-CONTEXT is writable.
- Target folder does not already exist.
- No NEXY.AI mutation is required.

## Success invariants
- New work is clearly labeled AI-PROPOSED where not source-derived.
- UI/presentation is never treated as authority.
- FREEZE/STOP cannot be rendered as success.
- Pending/loading cannot imply success.
- STABLE alone cannot imply releaseability.
- Role-based visibility never claims backend authorization.
- Same input + same role produces the same reference output.
- Unknown material state fails closed rather than being guessed.

## Required evidence
- E0: persisted files exist in AI-CONTEXT.
- E1: Python code compiles; JSON artifacts parse.
- E2: executed unit tests cover positive and negative behavior.
- Final persistence re-read from GitHub.

## Forbidden actions
- Modify NEXY.AI code, branches, issues, PRs, workflows, settings, or files.
- Claim NEXY runtime implementation from this lab.
- Promote proposal text into canonical requirement.
- Claim browser/E2E/deployment evidence that was not run.

## Stop conditions
- Target repository identity becomes ambiguous.
- Existing folder collision is detected.
- Mutation would escape target folder.
- Authoritative NEXY source conflicts with a proposed invariant in a way that cannot be resolved.

## Deliverables
Executable reference model + tests + schema + source alignment + temporary memory + validation report + final audit.
