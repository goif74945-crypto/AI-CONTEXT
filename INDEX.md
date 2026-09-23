# AI-CONTEXT — Canonical Entry Index

## BOOT HERE

For any substantial task, read in this order:

1. [Portable AI Bootstrap](./AI-BOOTSTRAP.md) — smallest handoff for a new model/session
2. [AI Execution Kernel](./AI-EXECUTION-KERNEL.md)
3. [Work Router](./WORK-ROUTER.md)
4. Relevant global rules under [rules/](./rules/)
5. Target project/context entrypoint
6. Only the workflows/schemas/evidence needed for the task

**Do not load the whole repository by default.**
Use progressive context loading.

---

## Core operating rules

- [Global rules](./rules/GLOBAL.md)
- [AI behavior](./rules/AI-BEHAVIOR.md)
- [Memory law](./rules/MEMORY.md)
- [Security & mutation boundary](./rules/SECURITY.md)
- [Verification & evidence law](./rules/VERIFICATION.md)

---

## Workflows

- [Project start](./workflows/project-start.md)
- [Implementation / repair](./workflows/implementation.md)
- [Repository audit](./workflows/repository-audit.md)
- [Verification](./workflows/verification.md)
- [Research](./workflows/research.md)
- [System design](./workflows/system-design.md)
- [Artifact creation](./workflows/artifact-creation.md)
- [Debugging](./workflows/debugging.md)
- [Long-context ingestion](./workflows/long-context-ingestion.md)
- [Memory/context update](./workflows/memory-update.md)

---

## Machine-readable contracts

- [Context](./schema/context.schema.json)
- [Decision](./schema/decision.schema.json)
- [Evidence](./schema/evidence.schema.json)
- [Memory](./schema/memory.schema.json)
- [Project](./schema/project.schema.json)
- [Skill](./schema/skill.schema.json)
- [Task Contract](./schema/task-contract.schema.json)
- [Execution Record](./schema/execution-record.schema.json)
- [Requirement Ledger](./schema/requirement-ledger.schema.json)

Ready-to-fill examples:
- [Templates](./templates/README.md)

---

## Projects

- [Project index](./projects/INDEX.md)
- [NEXY.AI context](./projects/NEXY.AI/overview.md)
- [NEXY.AI deep source context](./projects/NEXY.AI/deep/INDEX.md)

When working on NEXY.AI, do not treat the 215-entry registry as the total atomic system count. Use the deep context and authority boundaries.

---

## Skills

- [Skills registry entry](./skills/README.md)
- [Imported skills index](./skills/IMPORTED-SKILLS-INDEX.md)
- [Import/provenance manifest](./skills/IMPORT-MANIFEST.md)

Skills are capabilities, not automatic authority. Their output must still obey the Execution Kernel and verification rules.

---

## Operational data planes

Load only when relevant:

- `TASKS/` — task/execution records
- `CASES/` — reusable cases
- `FAILURES/` — failure patterns
- `LEDGER/` — ledger/history records
- `audit/` — audits/evidence
- `memory/` — durable memory
- `task-records/` — task lineage
- `user/` — user-scoped context
- `projects/` — project truth/context

---

## Core mental model

```text
REQUEST
  ↓
AI-BOOTSTRAP / AI-EXECUTION-KERNEL
  ↓
WORK-ROUTER
  ↓
PROJECT CONTEXT + REAL STATE
  ↓
TASK CONTRACT
  ↓
WORKFLOW(S)
  ↓
MUTATION / CREATION
  ↓
VERIFICATION + EVIDENCE
  ↓
EXECUTION RECORD
  ↓
DURABLE CONTEXT UPDATE
```

The repository is designed so a different model can resume work without depending on hidden reasoning from the previous model.
