# Evidence & Verification Protocol

## หลัก
Completion เป็น claim ที่ต้องพิสูจน์ ไม่ใช่ความรู้สึกหลัง tool call สำเร็จหนึ่งครั้ง

## Evidence Hierarchy
E0: ไม่มีหลักฐาน
E1: reasoning/inference
E2: static artifact inspection
E3: automated test result
E4: runtime observation
E5: independent cross-check / end-to-end proof
E6: production-equivalent evidence พร้อม traceability

Critical claim ควรมี E3+ และ behavior สำคัญควรพยายามไป E4/E5

## Claim Ledger
สำหรับ claim สำคัญบันทึก:
CLAIM_ID
statement
required_evidence_level
actual_evidence
source
timestamp
environment
result
limitations

## Verification Layers
V1 Syntax/shape
V2 Static semantics
V3 Unit behavior
V4 Integration behavior
V5 End-to-end behavior
V6 Failure-path behavior
V7 Security behavior
V8 Performance under defined load
V9 Recovery/rollback
V10 Regression against frozen requirements

## Anti-False-Completion
ห้ามใช้สิ่งเหล่านี้เป็นหลักฐานเพียงอย่างเดียว:
- "ไฟล์ถูกสร้างแล้ว"
- "build ผ่าน"
- "ไม่มี exception"
- "UI เปิดได้"
- "agent บอกว่าสำเร็จ"
- "API ตอบ 200"
แต่ละอย่างพิสูจน์ได้เพียงบาง layer

## Negative Testing
ทุก critical flow ต้องคิดอย่างน้อย:
missing input
malformed input
stale data
duplicate request
timeout
dependency unavailable
partial write
permission denied
rate limit
schema mismatch
concurrent mutation
retry after unknown outcome

## Evidence Freshness
หลักฐานต้องระบุ environment/version/ref เมื่อมีผล หากระบบเปลี่ยนหลัง verification ให้ mark evidence เป็น potentially stale จน regression check ผ่าน

## Final Audit
ก่อน COMPLETE:
- requirement coverage = 100% ของ explicit critical requirements
- ไม่มี critical UNKNOWN ที่ถูกซ่อน
- artifact ที่อ้างถึงมีอยู่จริง
- verification สอดคล้องกับ claim
- known limitation ถูกเปิดเผย
