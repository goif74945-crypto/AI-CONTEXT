# Context & Data Integrity

## Data Envelope
ข้อมูลสำคัญควรห่อ metadata:
value
source
source_type
observed_at
valid_from
valid_until (ถ้ามี)
environment
version
authority
confidence
verification_state

## Conflict Resolution
เมื่อข้อมูลขัดกัน:
1. ห้ามเลือกค่าที่ชอบ
2. ระบุ conflict
3. เทียบ authority
4. เทียบ freshness
5. เทียบ environment/version
6. หา direct evidence
7. หากยังตัดสินไม่ได้ -> UNKNOWN/STOP

## Provenance Graph
Derived fact ต้องย้อนกลับได้:
claim -> transformation -> source claims -> source artifacts

Transformation ควรบันทึก logic/version หากมีผลต่อผลลัพธ์

## Freshness Classes
F0 immutable/historical
F1 slow-changing
F2 release-changing
F3 operational
F4 real-time

ยิ่ง class สูง TTL และ verification window ต้องสั้นลง

## Cache Integrity
cache key ต้องรวม dimensions ที่เปลี่ยน meaning ของข้อมูล
cache invalidation ต้องมี owner
stale-while-revalidate ต้องไม่ใช้กับข้อมูลที่ stale แล้วก่อ security/financial/destructive impact โดยไม่มี guard

## Schema Evolution
เพิ่ม field: พิจารณา optionality/default semantics
ลบ field: ต้องตรวจ consumer
rename: ถือเป็น remove+add หากไม่มี compatibility layer
semantic change: ถือเป็น breaking แม้ type เดิม
enum expansion: consumer ที่ exhaustive อาจพัง

## Unknown Registry
UNKNOWN ไม่ใช่ failure แต่เป็น state ที่ต้องบริหาร:
id
question
impact
blocking?
owner/source_to_check
resolution evidence
status
