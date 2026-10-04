# คลังข้อมูลเสริม — NEXY.AI Future Engineering Knowledge Base

สถานะ: ACTIVE
สร้างเมื่อ: 2026-10-05
ขอบเขต: คลังข้อมูลเสริมใน AI-CONTEXT เท่านั้น
ข้อห้ามถาวร: เอกสารชุดนี้ไม่อนุญาตให้ถือว่าตนเองมีสิทธิ์แก้ไข repository ที่ชื่อมี "NEXY.AI" เป็นส่วนประกอบ การอ่าน/วิเคราะห์เป็นคนละสิทธิ์กับการเขียน

## วัตถุประสงค์
สร้างฐานความรู้ที่ช่วยการพัฒนา NEXY.AI ในอนาคตโดยไม่ผูกกับ implementation ปัจจุบัน และไม่เดาข้อมูลที่ยังไม่มีหลักฐาน เน้นสิ่งที่ใช้เป็นกรอบตรวจสอบ ตัดสินใจ และป้องกัน regression ได้ในหลายรุ่นของระบบ

## Knowledge Domains
1. Architecture & Boundary Contracts
2. Evidence & Verification Engineering
3. AI Orchestration & Agent Reliability
4. Data Provenance & Context Integrity
5. Security & Trust Boundaries
6. Reliability, Failure Modes & Recovery
7. Evaluation & Quality Gates
8. Observability & Incident Knowledge
9. Performance & Capacity Reasoning
10. Product/System Evolution & Compatibility
11. Prompt/Policy Engineering
12. Research Backlog & Unknown Registry

## กฎคุณภาพ
- FACT ต้องมีหลักฐานหรือแหล่งอ้างอิงที่ตรวจย้อนกลับได้
- ASSUMPTION ต้องติดป้ายและห้ามใช้เป็น acceptance evidence
- UNKNOWN ต้องคงเป็น UNKNOWN จนกว่าจะตรวจได้
- NOT VERIFIED ห้ามเลื่อนสถานะเป็น VERIFIED ด้วยการอนุมาน
- ห้ามใช้ placeholder แล้วอ้างว่างานสมบูรณ์
- ทุกข้อเสนอเชิง architecture ต้องระบุ trade-off และ failure mode
- ทุก acceptance criterion สำคัญต้องมีวิธีพิสูจน์
- ข้อมูลที่ขึ้นกับเวลาให้ระบุวันที่ตรวจสอบ
- ห้ามคัดลอก secret, token, credential, PII หรือข้อมูลลับเข้าคลัง

## โครงสร้างไฟล์เริ่มต้น
- 00_INDEX.md — ดัชนีและกฎ
- 01_ARCHITECTURE_DECISION_FRAMEWORK.md — กรอบตัดสินใจสถาปัตยกรรม
- 02_EVIDENCE_VERIFICATION_PROTOCOL.md — โปรโตคอลหลักฐานและการยืนยันผล
- 03_AI_AGENT_RELIABILITY.md — ความน่าเชื่อถือของ agent/orchestration
- 04_CONTEXT_DATA_INTEGRITY.md — provenance, freshness, conflict handling
- 05_FAILURE_MODE_CATALOG.md — taxonomy ความล้มเหลว
- 06_SECURITY_TRUST_BOUNDARIES.md — security model เชิงระบบ
- 07_EVALUATION_QUALITY_GATES.md — eval และ release gates
- 08_OBSERVABILITY_INCIDENTS.md — telemetry และ incident learning
- 09_COMPATIBILITY_EVOLUTION.md — migration/compatibility strategy
- 10_RESEARCH_BACKLOG.md — สิ่งที่ยังต้องพิสูจน์
- CHAT_PROVENANCE.md — provenance ของงานชุดนี้

## Stop Conditions สำหรับ AI ที่ใช้คลังนี้
หยุดและขอหลักฐานเพิ่มเมื่อ:
- requirement ขัดกัน
- ต้องเดา schema/API/behavior ที่มีผลต่อ compatibility
- การกระทำจะเขียนไปยัง NEXY.AI โดยไม่มีคำสั่งชัดเจน
- ไม่มี evidence เพียงพอสำหรับ claim สำคัญ
- action เป็น irreversible/high-impact และไม่มี approval

เอกสารนี้เป็นฐานเสริม ไม่ใช่ authoritative specification ของ NEXY.AI หากขัดกับ requirement/spec ที่ผู้ใช้กำหนด ให้ requirement/spec นั้นมีอำนาจสูงกว่า
