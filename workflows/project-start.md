# WORKFLOW — PROJECT START

## Goal
Resolve enough context to begin work correctly without loading unrelated material.

## Procedure
1. Read root `INDEX.md` and `AI-EXECUTION-KERNEL.md`.
2. Identify exact project/target.
3. Read project index/overview/status.
4. Load only relevant architecture/requirements/deep files.
5. Resolve authority order.
6. Inspect current repository/file/runtime state if freshness matters.
7. Identify protected branches/paths and explicit no-touch zones.
8. Normalize request into a Task Contract.
9. Build initial dependency map.
10. Start execution only after preconditions hold.

## Task Contract template
- objective:
- target:
- branch/ref:
- expected_head:
- authority_sources:
- authorized_scope:
- protected_scope:
- preconditions:
- success_invariants:
- required_evidence:
- stop_conditions:
- deliverables:

## Stop conditions
Do not mutate if:
- target repository/branch is ambiguous;
- expected HEAD mismatch invalidates task;
- authoritative sources conflict materially;
- protected scope would be touched;
- required permission/credential is absent.

## Output of this workflow
A locked task boundary and a reproducible starting state.
