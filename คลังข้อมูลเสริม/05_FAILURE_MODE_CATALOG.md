# Failure Mode Catalog

## Taxonomy
A Input failures; B State failures; C Dependency failures; D Concurrency failures; E Data integrity failures; F Authorization/security failures; G Resource/capacity failures; H Deployment/configuration failures; I AI/agent reasoning failures; J Observability failures; K Recovery failures.

## Canonical Failure Questions
ตรวจพบที่ boundary ไหน? blast radius เท่าไร? fail-open หรือ fail-closed? caller เห็น error แบบใด? retry safe หรือไม่? state หลัง failure แน่นอนหรือ unknown? มี partial side effect หรือไม่? recovery automated/manual? evidence ใดพิสูจน์ recovery? alert เกิดก่อนผู้ใช้พบหรือหลัง?

## Dangerous Patterns
### Unknown commit
request timeout หลังส่ง write ไป dependency: ห้าม assume failed; reconcile state ก่อน retry.
### Partial fan-out
หลาย downstream สำเร็จบางส่วน: ใช้ compensation หรือ durable workflow state.
### Poison message
bounded retry + quarantine/dead-letter + inspectability.
### Retry storm
ใช้ timeout budget, exponential backoff+jitter, retry budget, circuit breaking.
### Silent corruption
ป้องกันด้วย semantic invariants และ cross-field validation.
### Observability black hole
critical signals ควรมี independent health evidence.

## Failure Record
failure_id, trigger, preconditions, observable symptoms, hidden impact, detection, containment, recovery, prevention, verification, regression_test.
