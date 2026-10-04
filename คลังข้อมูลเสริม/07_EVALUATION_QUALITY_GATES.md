# Evaluation & Quality Gates

## Matrix
ทุก capability: requirement_id, scenario, expected_behavior, failure_scenarios, evidence_source, environment, pass_rule.

## Classes
Contract; invariant; metamorphic; differential; adversarial; longitudinal; recovery tests.

## AI Evaluation
task correctness; requirement coverage; groundedness; tool-action accuracy; false completion; scope violation; unsafe mutation attempts; recovery quality; latency/cost budget.
คะแนนเฉลี่ยไม่พอ ต้องมี hard gates สำหรับ catastrophic failure.

## Release Gates
G0 artifact exists
G1 static validation
G2 unit/contract
G3 integration
G4 E2E critical path
G5 negative/failure path
G6 security
G7 performance/capacity
G8 rollback/recovery
G9 evidence audit

Critical release ห้ามข้าม gate ที่เกี่ยวข้องโดยไม่มี explicit waiver + risk owner.

## Regression
bug สำคัญที่เคยเกิดควรถูกแปลงเป็น reproducible regression test หรือ machine-checkable invariant.

## Flaky Tests
rerun-until-green ไม่ใช่หลักฐาน pass. บันทึก flaky rate, root cause และ owner.
