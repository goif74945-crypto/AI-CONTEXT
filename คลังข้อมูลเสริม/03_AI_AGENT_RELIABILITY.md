# AI Agent Reliability

## Agent Contract
Agent ที่ทำงาน production ต้องแยก:
Objective
Authority
Scope
Inputs
Constraints
Immutable rules
Required behavior
Forbidden behavior
Evidence
Failure conditions
Stop conditions
Output schema

## Reliability Hazards
1. Goal drift: เปลี่ยนโจทย์ระหว่างทำ
2. Scope creep: เพิ่มงานโดยไม่ได้รับอนุญาต
3. Premature completion: tool สำเร็จหนึ่งครั้งแล้วจบ
4. Evidence laundering: เปลี่ยน inference เป็น fact
5. Retry mutation: ทำ write ซ้ำ
6. Context collision: ใช้ข้อมูลคนละ project/version
7. Silent fallback: ลด requirement เมื่อทำไม่ได้
8. Tool hallucination: อ้าง action ที่ไม่ได้ execute
9. Stale authority: ใช้ spec เก่าทับ spec ใหม่
10. Partial-state blindness: ไม่ตรวจผลหลัง mutation

## Execution State Machine
UNDERSTAND -> INSPECT -> PLAN -> EXECUTE -> VERIFY
failure -> DIAGNOSE -> MINIMAL_FIX -> REVERIFY
success -> FINAL_AUDIT -> COMPLETE

ห้ามข้าม VERIFY สำหรับ mutation หรือ deliverable สำคัญ

## Tool Safety
ก่อน write:
- resolve exact target
- confirm authority
- inspect current state
- calculate intended delta
- identify rollback
- execute smallest mutation
- read-after-write
- validate invariant

## Idempotency
Agent action ควรมี deterministic identity เมื่อเป็นไปได้ เช่น operation key / target+desired-state hash เพื่อแยก retry จากงานใหม่

## Context Isolation
ข้อมูลทุกชิ้นควรมี namespace:
project
environment
version/ref
source
timestamp
authority_level

ห้าม merge context ต่าง namespace โดย implicit assumption

## Stop Conditions
STOP เมื่อ:
- target ambiguous
- write authority absent
- destructive action ไม่มี approval
- spec conflict unresolved
- required secret/credential unavailable
- evidence ต่ำกว่าที่ acceptance criterion ต้องการ

## Useful Metrics
task_success_rate
verified_completion_rate
false_completion_rate
rollback_rate
tool_error_rate
retry_duplication_rate
requirement_coverage
unknown_resolution_rate
mean_steps_to_verified_completion
