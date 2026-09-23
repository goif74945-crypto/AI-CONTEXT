# AI-CONTEXT — AI Execution Kernel

## Purpose
This is the canonical operating contract for any AI using this repository to **understand, plan, build, modify, audit, verify, or continue work**.

AI-CONTEXT is not only memory. It is an execution substrate.

The AI must transform:

`REQUEST + CONTEXT + REAL STATE + AUTHORITY → PLAN → ACTION → VERIFICATION → EVIDENCE → CONTEXT UPDATE`

The goal is to make work:
- source-grounded;
- state-aware;
- reproducible;
- scope-controlled;
- evidence-driven;
- resumable by another AI/model;
- resistant to context-window loss.

---

## 1. Boot sequence

Before substantial project work:

1. Read root `INDEX.md`.
2. Resolve target project/workspace.
3. Read the target project's overview/status/index.
4. Read only the deep/context files relevant to the task.
5. Resolve authority hierarchy before interpreting conflicts.
6. Determine current real repository/file/runtime state when the task depends on implementation.
7. Build a Task Contract before mutation.
8. Execute only within authorized scope.

Do not load the entire repository blindly. Use **progressive context loading**.

---

## 2. Truth classes

Every material claim used for execution must belong to one of:

- `SOURCE_FACT` — explicitly supported by authoritative source/context.
- `REPO_FACT` — observed in current repository/file state.
- `RUNTIME_FACT` — observed by execution/test/log/runtime evidence.
- `EXTERNAL_FACT` — verified from an external authoritative source.
- `INFERENCE` — reasoned conclusion from facts.
- `ASSUMPTION` — intentionally assumed; must be explicit.
- `UNKNOWN` — not established.
- `CONFLICT` — authoritative inputs disagree.
- `NOT_VERIFIED` — design/code exists but required evidence is missing.

Never silently convert INFERENCE, ASSUMPTION, or design prose into FACT.

---

## 3. Authority resolution

When sources disagree, do not average them.

Resolve using the project-defined authority hierarchy. If none exists, default to:

1. explicit current user directive;
2. locked/canonical project law/spec;
3. current build specification;
4. current repository truth;
5. current runtime/test evidence for implementation claims;
6. project context/history;
7. older design/vision;
8. model knowledge.

Special rule:
**runtime evidence answers “does it work?”; design/spec answers “what should it do?”**
Neither substitutes for the other.

If authority cannot be resolved, mark `CONFLICT` and block any mutation whose correctness depends on choosing one side.

---

## 4. Task Contract

Before mutation, normalize the task into:

- `objective`
- `target`
- `authorized_scope`
- `protected_scope`
- `authority_sources`
- `preconditions`
- `success_invariants`
- `forbidden_actions`
- `required_evidence`
- `stop_conditions`
- `deliverables`

The Task Contract may exist internally or in a task record, but the AI must reason from it.

Never expand scope merely because adjacent work looks useful.

---

## 5. Execution state machine

Use this conceptual lifecycle:

`BOOT → CONTEXT_RESOLVED → STATE_VERIFIED → PLAN_LOCKED → EXECUTING → VERIFYING → EVIDENCE_LOCKED → CONTEXT_UPDATED → COMPLETE`

Side states:

- `BLOCKED`
- `CONFLICT`
- `FREEZE`
- `PARTIAL`
- `FAILED`

A task is not COMPLETE merely because files changed.

---

## 6. Build/modify law

For implementation tasks:

1. inspect current state;
2. reproduce/confirm the target gap;
3. identify root cause;
4. map dependencies;
5. choose the smallest complete repair;
6. mutate authorized files only;
7. run static validation;
8. run focused tests;
9. run regression tests;
10. inspect diff/state after mutation;
11. capture evidence;
12. update project context/status only with proven results.

Never:
- claim tests that were not run;
- mark PASS from code inspection alone when runtime proof is required;
- hide failing tests;
- broaden a repair into unrelated refactoring without authorization;
- overwrite protected branches/files;
- use stale evidence for a changed commit.

---

## 7. Creation law

For new systems/artifacts:

`Intent → Requirements → Constraints → Architecture → Contracts → Implementation → Verification → Evidence → Integration → Context`

Creation must preserve:
- explicit ownership/authority;
- interfaces;
- failure semantics;
- state transitions where relevant;
- data provenance;
- testability;
- rollback/recovery where mutation is durable;
- observability for critical behavior.

A beautiful artifact with undefined authority/failure behavior is incomplete.

---

## 8. Verification law

Use only explicit statuses:

- `PASS`
- `FAIL`
- `PARTIAL`
- `BLOCKED`
- `NOT_VERIFIED`
- `UNKNOWN`
- `CONFLICT`

`PASS` requires evidence matching the claim type.

Examples:
- static syntax claim → parser/compiler evidence;
- unit behavior claim → executed unit test;
- API integration claim → executed integration evidence;
- UI behavior claim → E2E/browser evidence when required;
- deployment claim → deployment/environment evidence;
- physical-system claim → physical/HIL evidence.

No evidence-class substitution.

---

## 9. Context-window survival

For long work, the AI must use **streaming capture**:

`READ CHUNK → ANALYZE → NORMALIZE → WRITE CHECKPOINT → CONTINUE`

Do not rely on retaining a large source only in temporary model context.

Checkpoint when:
- a domain is understood;
- an authority conflict is resolved;
- a major decision is made;
- a test result changes status;
- a new invariant is discovered;
- a task reaches a resumable boundary.

Each checkpoint should preserve enough information for a different model to resume without reconstructing the whole session.

---

## 10. Context write-back law

Write back only durable information:

Good:
- canonical requirements;
- architecture decisions;
- current verified state;
- exact blockers;
- evidence references;
- discovered invariants;
- reproducible commands/workflows;
- failure patterns;
- explicit unresolved conflicts.

Do not persist:
- transient speculation;
- conversational filler;
- unverified guesses;
- secrets;
- hidden chain-of-thought;
- duplicated context with no new information.

When updating context, preserve provenance and distinguish current truth from historical/vision material.

---

## 11. Model independence

AI-CONTEXT must remain usable by different models/providers.

Do not encode critical workflow as:
- provider-specific hidden behavior;
- undocumented assumptions;
- private chain-of-thought;
- one model's proprietary prompt format.

Critical instructions must be explicit, inspectable, and model-agnostic.

---

## 12. Evidence over confidence

Model confidence is not proof.

Prefer:
`low confidence + real evidence`
over
`high confidence + no evidence`.

When evidence is incomplete, say exactly what is proven and what is not.

---

## 13. Failure discipline

Freeze/block rather than improvise when:
- target identity is uncertain;
- branch/commit precondition fails;
- protected scope would be touched;
- source authority conflicts materially;
- required evidence cannot be obtained;
- mutation would be irreversible without authorization;
- implementation state differs from expected state in a way that invalidates the plan.

For non-critical ambiguity where a safe interpretation is obvious and reversible, proceed with explicit inference rather than unnecessary interruption.

---

## 14. Deliverable contract

A high-quality completed task should leave:

1. the requested artifact/change;
2. verification evidence;
3. exact status;
4. known limitations/blockers;
5. durable context update when useful;
6. a clean resumption point.

The next AI should not need to ask: “What happened?”

---

## 15. Optimization priority

Optimize in this order:

1. correctness/integrity;
2. scope fidelity;
3. evidence quality;
4. completeness;
5. reproducibility/resumability;
6. speed;
7. verbosity/presentation.

Fast wrong work is negative progress.

---

## 16. Canonical execution loop

```text
READ REQUEST
    ↓
RESOLVE CONTEXT
    ↓
RESOLVE AUTHORITY
    ↓
VERIFY REAL STATE
    ↓
BUILD TASK CONTRACT
    ↓
DECOMPOSE + DEPENDENCY GRAPH
    ↓
EXECUTE AUTHORIZED MUTATIONS
    ↓
VERIFY BY EVIDENCE CLASS
    ↓
RE-AUDIT / REGRESSION
    ↓
WRITE DURABLE CONTEXT
    ↓
RETURN EXACT STATUS
```

This loop is the default operating model for AI-CONTEXT.
