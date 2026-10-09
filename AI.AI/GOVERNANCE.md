# AI.AI / Multi-Chat Engineering Constitution v1.0
STATUS: ACTIVE for new work under AI-CONTEXT/AI.AI; does not override higher-priority user authority.
AS-OF: 2026-10-09
SCOPE: AI-CONTEXT/AI.AI/** on branch main ONLY.
REPO EXCLUSIONS: NEVER mutate NEXY.AI-, its branches, GitHub settings, or any files outside the new AI.AI/** root.
CURRENT PRODUCT REFERENCE: AI.AI local v0.4.0, product commit 95741bede86405685a022633df03a2c39ce7fc4c (NOT a verified remote GitHub AI.AI commit).

## RULES / กฎบังคับ
1. AI.AI/** เป็นพื้นที่ตรวจวิจารณ์ AI.AI, เสนอแนวคิดระบบใหม่ และส่งมอบ Implementation ที่รันจริงพร้อมหลักฐาน ไม่ใช้เป็นพื้นที่ประกาศความสำเร็จโดยไม่มีการทดสอบ
2. ทุกแชทต้องระบุ VERSION ที่ใช้ตรวจ, exact source revision และ CHAT_ID ที่ไม่ซ้ำตั้งแต่ต้น, พร้อม IN_SCOPE/OUT_OF_SCOPE. หากไม่เห็นเวอร์ชันล่าสุดจริงให้ใช้ VERSION_UNVERIFIED และห้ามแอบอ้าง
3. ทุกแชทต้องเสนออย่างน้อยหนึ่ง (a) ข้อวิจารณ์ที่มี source locator/reproduction และ (b) แนวคิดใหม่ที่แก้ปัญหานั้น มีผลเชิงวิศวกรรมที่วัดได้
4. ก่อนเริ่ม ต้องค้นหารหัส/ชื่อ/semantic fingerprint ของแนวคิดใน INDEX.md และทุกเวอร์ชัน; หากซ้ำ => REJECT_DUPLICATE. GitHub create-file-only สำหรับ claim filename ช่วยป้องกันแชทแย่งชื่อ; semantic uniqueness ยังต้องตรวจเอง ห้ามอ้างว่ารับประกันไม่ซ้ำ 100%
5. แนวคิดที่รับเข้าได้ต้องมี COMPLETE SOURCE (ไม่ใช่ pseudo-code, stub, TODO หรือ placeholder), TESTS, exact test invocation/outputs, Integration Contract, regression impact, threat/edge cases. หากไม่มีหลักฐานครบ = CANDIDATE_UNVERIFIED, ห้ามกล่าวว่านำเข้าพร้อมใช้งาน
6. ทุกการเสนอ patch ต้องจำกัดเฉพาะไฟล์ที่อนุญาต, ระบุ exact target version/HEAD, dependency, import path, rollback, tests. ห้ามเปลี่ยนข้อกำหนดเดิมและห้ามลดจำนวนการทดสอบให้ผ่านง่ายขึ้น
7. โฟลเดอร์ 'โค้ดโปรเจคปัจจุบัน' ถูก PROTECTED: ห้าม overwrite, edit, delete, rename, move ไฟล์ที่มีอยู่ หรือแก้ snapshot เดิมโดยเด็ดขาด. การเพิ่ม snapshot ของเวอร์ชันใหม่ทำได้แบบ create-only เฉพาะเมื่อไม่ชนของเดิมและยืนยัน source integrity. หากมีความขัดแย้งหรือต้องแก้ข้อมูลเก่าให้ FREEZE + ออก finding ไปยังเวอร์ชันใหม่แทน
8. Versioning: ผลงานอยู่ใน /AI.AI/versions/vX.Y.Z/; ห้ามสร้างเวอร์ชันใหม่เพียงเพราะเสนอแนวคิด. เพิ่ม version directory เมื่อมี source version ใหม่ที่ตรวจรับได้เท่านั้น; ถ้าเวอร์ชันเดิมมีแล้วให้สร้างไฟล์เอกสาร/แนวคิดใหม่ที่ชื่อไม่ชน โดยไม่แก้ไฟล์ที่มีอยู่
9. Code snapshots: เก็บ complete source ทุกเวอร์ชันภายใต้ /AI.AI/โค้ดโปรเจคปัจจุบัน/vX.Y.Z/ แบบ immutable และ /AI.AI/versions/vX.Y.Z/ มี manifest กับหลักฐาน. ถ้ายังไม่อัปโหลด source ครบ ต้องระบุ SNAPSHOT_INCOMPLETE ไม่ใช้คำว่า FULL
10. Every review records explicit FACT / ASSUMPTION / UNKNOWN / FAILURE. Tests classify PASS/FAIL/BLOCKED/NOT_RUN; only real source + runtime evidence may be labeled PASS. E2E physical device cannot be claimed from mocks.
11. One writer per path. Before writing requery main HEAD; commit append-only, verify read-back and record exact Git commit+blob SHAs. Conflict or insufficient authority => stop that mutation and report BLOCKED, continue other independent tasks.
12. Never copy secrets, tokens, private screen data, personal files, credentials or dependency artifacts into version snapshots. No mass exfiltration. Require explicit user approval for destructive and external side-effect actions.
13. Any change request that modifies protected existing source, a NEXY.AI- repository, or other teams' files is OUT_OF_SCOPE and forbidden unless the owner explicitly overrides for that exact resource.
14. Completion: criticism documented; new concept unique against scanned registry; complete code published; negative/positive tests executed; matching source/HEAD and read-back proofs; compatibility gate; version manifest; no unsupported claims. Otherwise status PARTIAL.

## Submission required paths for each CHAT_ID
/AI.AI/versions/vX.Y.Z/reviews/<CHAT_ID>.md
/AI.AI/versions/vX.Y.Z/ideas/<CHAT_ID>.md
/AI.AI/versions/vX.Y.Z/implementation/<CHAT_ID>/ai_ai/*.py
/AI.AI/versions/vX.Y.Z/implementation/<CHAT_ID>/tests/*.py
/AI.AI/versions/vX.Y.Z/evidence/<CHAT_ID>.md

## Release gate
Code from this collaboration folder is a tested merge candidate; it becomes actual AI.AI release code ONLY after applying to the real product repo at its exact HEAD and passing product acceptance & device-specific validation. Never confuse staging evidence with installed production.
