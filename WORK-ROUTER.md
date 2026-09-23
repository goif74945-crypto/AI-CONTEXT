# AI-CONTEXT — Work Router

Use this file after `AI-EXECUTION-KERNEL.md` to choose the smallest workflow set that can complete the request.

## Route table

| User intent | Primary workflow | Add when needed |
|---|---|---|
| Start/continue a project | `workflows/project-start.md` | memory-update |
| Implement/repair code/system | `workflows/implementation.md` | debugging, verification |
| Audit a repository/spec | `workflows/repository-audit.md` | verification |
| Verify a claim | `workflows/verification.md` | repository-audit |
| Research a topic/problem | `workflows/research.md` | system-design |
| Design architecture/product/system | `workflows/system-design.md` | research, verification |
| Create a finished artifact | `workflows/artifact-creation.md` | system-design |
| Debug a failure | `workflows/debugging.md` | implementation, verification |
| Ingest a very large source | `workflows/long-context-ingestion.md` | memory-update |
| Update durable context | `workflows/memory-update.md` | verification |

## Composition rule
Workflows are composable. Typical high-value chains:

### Build from idea
`PROJECT START → RESEARCH → SYSTEM DESIGN → ARTIFACT CREATION / IMPLEMENTATION → VERIFICATION → MEMORY UPDATE`

### Repair existing system
`PROJECT START → DEBUGGING → IMPLEMENTATION → VERIFICATION → MEMORY UPDATE`

### Full audit and convergence
`PROJECT START → REPOSITORY AUDIT → DEFECT GRAPH → IMPLEMENTATION → VERIFICATION → RE-AUDIT → MEMORY UPDATE`

### Large document/spec ingestion
`LONG-CONTEXT INGESTION → COVERAGE MAP → CONFLICT MAP → MEMORY UPDATE`

## Router law
Do not run every workflow for every task.
Choose based on required evidence and artifact type.

## Escalation
If a workflow discovers a materially different task class, route explicitly rather than silently changing the mission.
