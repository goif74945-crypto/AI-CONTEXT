# Architecture Decision Framework

## เป้าหมาย
ใช้ตัดสินใจ architecture โดยไม่ผูกกับ framework หรือ vendor และป้องกันการเลือกจากความชอบส่วนตัว

## Decision Record Contract
ทุกการตัดสินใจสำคัญควรบันทึก:
- Problem: ปัญหาที่ต้องแก้จริง
- Scope: ส่วนที่ได้รับผล
- Constraints: ข้อจำกัดที่ห้ามละเมิด
- Evidence: ข้อมูลที่พิสูจน์ได้
- Unknowns: สิ่งที่ยังไม่รู้
- Options: อย่างน้อยทางเลือกที่สมเหตุผล
- Trade-offs: latency, complexity, cost, security, operability, portability
- Failure modes: วิธีที่ทางเลือกนั้นล้มเหลว
- Reversibility: rollback/migration cost
- Decision: สิ่งที่เลือกและเหตุผล
- Validation: วิธีพิสูจน์ว่าการตัดสินใจถูกในระบบจริง
- Revisit trigger: เงื่อนไขที่ต้องเปิด decision ใหม่

## Boundary Rules
Boundary ที่ดีต้องมี contract ชัด:
Input -> Validation -> Processing -> Output -> Error semantics -> Observability

ห้ามพึ่ง implicit behavior ระหว่าง component สำคัญ หาก contract เปลี่ยนต้องประเมิน:
1. backward compatibility
2. forward compatibility
3. data migration
4. cache invalidation
5. retry/idempotency
6. security boundary
7. monitoring impact

## Coupling Test
ถามทุก dependency:
- ถ้าปลายทางหาย ระบบ fail แบบใด?
- timeout ถูกกำหนดหรือไม่?
- retry ทำให้ duplicate side effect หรือไม่?
- version mismatch ตรวจพบตรงไหน?
- schema drift ถูก reject หรือ silently accepted?
- มี circuit breaker/backpressure ที่เหมาะสมหรือไม่?
- สามารถ isolate failure ได้หรือไม่?

## Reversibility Classes
R0: เปลี่ยนกลับได้ทันที ไม่มี data mutation
R1: rollback ได้ด้วย config/deploy
R2: ต้อง migration ย้อนกลับ
R3: data semantics เปลี่ยนและ rollback ยาก
R4: irreversible/external commitment

R2-R4 ต้องการ evidence และแผน rollback/containment ที่ชัดก่อน execution

## Architecture Smells
- shared mutable state โดยไม่มี owner
- duplicated source of truth
- hidden cross-layer dependency
- retry โดยไม่มี idempotency
- cache โดยไม่มี invalidation contract
- async flow โดยไม่มี correlation ID
- schema ที่ field meaning เปลี่ยนตาม caller
- fallback ที่ซ่อน error จนระบบดูเหมือนปกติ
- authorization ที่ตรวจเฉพาะ UI
- success response ก่อน durable completion โดยไม่ประกาศ semantics

## Acceptance
Architecture proposal ไม่ผ่านถ้าไม่สามารถอธิบาย failure behavior, evidence, compatibility และ rollback ได้
