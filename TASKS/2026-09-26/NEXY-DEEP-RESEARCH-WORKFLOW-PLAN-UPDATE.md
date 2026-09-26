# NEXY Deep Research Workflow Plan — User Update

TASK_ID: NEXY-DEEP-RESEARCH-WORKFLOW-PLAN-UPDATE
DATE: 2026-09-26
SOURCE: Direct user instruction
STATUS: ACTIVE_WORKFLOW_GUIDANCE

## Updated Deep Research workflow

1. รวบรวมเอกสารต้นทางและ repository ทั้งหมดที่เกี่ยวข้อง
2. อ่านและแยกข้อผูกพันจากทุก source specification
3. ตรวจความครบถ้วนและความสอดคล้องระหว่าง SPEC↔CODE↔TEST↔EVIDENCE
4. ตรวจเทียบ implementation กับเอกสารภายนอกที่เชื่อถือได้
5. สรุปผล พบข้อบกพร่อง และจัดลำดับแผนแก้ไขตาม dependency

## Operational interpretation for NEXY

- Source collection must include the authoritative NEXY design source, current repository state, AI-CONTEXT registries, tests, and evidence.
- Source obligations must be extracted before implementation completeness is judged.
- Traceability must distinguish source truth, code truth, test execution, and evidence freshness.
- External references validate technology/framework/security behavior only and must not override NEXY source requirements.
- Findings and remediation must be ordered by dependency and evidence-backed; unsupported guesses are forbidden.

## Persistence note

This record captures the user's updated workflow as project task guidance. It does not itself prove audit completion, implementation correctness, or release readiness.
