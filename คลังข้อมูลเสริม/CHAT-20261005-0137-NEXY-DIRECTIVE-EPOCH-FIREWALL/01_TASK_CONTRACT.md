# 01 — Task Contract

## Objective
Create an additive, standalone R&D subsystem in AI-CONTEXT that can prevent stale autonomous actions after a newer operator directive supersedes their authority, while remaining compatible in principle with NEXY's deterministic/freeze-oriented control model.

## Target
`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0137-NEXY-DIRECTIVE-EPOCH-FIREWALL/`

## Authority sources
1. Explicit current user directive.
2. `AI-EXECUTION-KERNEL.md`, `WORK-ROUTER.md` and repository rules.
3. NEXY project context in `projects/NEXY.AI/` for design alignment only.
4. Executed tests for implementation claims in this standalone reference project.

## Authorized scope
- Add files only under this project folder in AI-CONTEXT.
- Design a new AI-proposed system.
- Implement a standalone reference core.
- Build tests, adversarial validation, fixtures, benchmark and evidence.

## Protected scope
- Every repository whose name contains `NEXY.AI`.
- Existing supplemental projects belonging to other sessions.
- Any production deployment or live NEXY data.

## Preconditions
- AI-CONTEXT is the confirmed target repository.
- Project path did not exist before creation.
- Existing supplemental tree was inspected to reduce duplicate work.
- Required NEXY context and repository execution rules were read.

## Success invariants
- Prepared actions cannot silently inherit authority from a newer directive.
- REPLACE/NARROW/REVOKE invalidate old prepared-action epochs.
- NARROW cannot expand action authority.
- Tampered payloads cannot pass the commit gate.
- Irreversible writes require an exact approval binding.
- Every protocol attempt needed to reconstruct state is journaled.
- Replay verifies journal integrity and reproduces final state.
- No NEXY.AI repository is mutated.

## Required evidence
- E1: Python compilation/static syntax proof.
- E2: executed unit tests for protocol invariants and negative paths.
- E3: fixture-driven multi-step protocol flow plus deterministic replay.
- Additional stress evidence: deterministic randomized trials.
- Local benchmark as performance observation only, not production proof.

## Forbidden behavior
- Natural-language intent inference inside the deterministic core.
- Silent rebasing of a prepared action onto a newer directive.
- Treating a hash binding as authentication/signature proof.
- Claiming this proposal is current NEXY implementation.
- Writes outside the authorized AI-CONTEXT folder.

## Stop conditions
- Any required step would mutate a protected repository.
- Required authority becomes ambiguous or conflicting.
- A PASS claim lacks matching executed evidence.
- The reference design would require guessing a current NEXY API/schema.
