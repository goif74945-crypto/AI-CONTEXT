# NEXY.AI — NEW NORMAL CHAT EXECUTION HANDOFF 006
SYSTEM: NEXY::NORMAL-CHAT-SELF-EXECUTING-REPAIR-AND-AUDIT-V1

## MODE
ทำ / EXECUTE_NOW / CROSS / NORMAL_CHAT_ONLY / ENGINEERING / FAIL_CLOSED / NO_GUESS / NO_FAKE_PASS / EXACT_HEAD_FENCED / CONTINUE_READY_WORK

## ขอบเขตและเป้าหมาย
คุณคือแชท ChatGPT ใหม่ที่ต้องลงมือทำงาน NEXY.AI ด้วยตัวเองผ่านเครื่องมือที่มีสิทธิ์ใช้จริง ห้ามมอบหมายงานกลับให้ Codex ห้ามหยุดเพียงแผน/ACK ห้ามอ้างว่าควบคุม Work, Cloud Browser, VS Code, เครื่องทดสอบ, แชทอื่น หรือระบบต่าง ๆ ได้ ถ้าไม่มีเครื่องมือจริง จงหาทางที่ได้รับอนุญาตอื่นและลงมือในส่วน READY ต่อในรอบคำตอบเดียว

มีแชทอื่นทำงานร่วมกันอยู่: CROSS. ใช้ handoff นี้เป็นข้อมูลประวัติตั้งต้นที่ต้องตรวจสอบกับ GitHub ใหม่ก่อนอ้างข้อเท็จจริงปัจจุบัน. ไม่สมมติว่าอ่านเนื้อหาหรือ state ของแชทอื่นได้.

## แหล่งและสาขาที่อนุญาต
Product repo: goif74945-crypto/NEXY.AI-
Product branch: NEXY.ai เท่านั้น
Observed live product HEAD ณ ตอนสร้าง handoff:
44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
AI-CONTEXT repo: goif74945-crypto/AI-CONTEXT
AI-CONTEXT branch: main
Observed AI-CONTEXT HEAD ก่อนเขียน handoff: bdf4161c622eac689cc22ec97c744a764df94a91

Authoritative specification:
แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx
Required SHA-256:
b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

Source evidence already persisted and read back:
AI-CONTEXT/EVIDENCE/20261008-NEXY-SPEC-AUTHORITY-RESOLUTION-004.md
AI-CONTEXT/EVIDENCE/20261008-NEXY-DOCB-DOCC-TSA-QUEUE-TTL-CLAUSES-005.md
AI-CONTEXT/EVIDENCE/20261008-NEXY-CONTINUOUS-REPAIR-EXECUTION-003.tsv
AI-CONTEXT/TASKS/20261008-NEXY-CONTINUOUS-REPAIR-EXECUTION-003.md

ไฟล์ DOCX ไบนารีจากอีกแชทไม่ได้หมายความว่าแชทใหม่นี้เปิดได้จริง; ถ้าเปิดไม่ได้ให้ใช้ extraction เฉพาะข้อความและ locator ที่ยืนยันไว้เท่านั้นและ mark ส่วนที่จำเป็นต้องอ่านเต็มว่า UNAVAILABLE. ห้ามอ้างว่าแชทนี้ rehash ไบนารีเองถ้าไม่ได้ทำ.

## ขั้นตอน 1: LIVE SNAPSHOT ก่อนแก้
1. ตรวจสิทธิ์ repository และอ่าน HEAD สดของ NEXY.ai กับ AI-CONTEXT/main
2. อ่าน commit หลัง 8b406a63f10aa1424225a80453393af2e4cb78b5 รวมถึง commit
   44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
   ชื่อ fix(auth,sandbox): enforce OTAC single use and trusted runtime mounts.
3. Diff ที่ตรวจจาก GitHub ขณะทำ handoff แสดง 5 ไฟล์เปลี่ยน: packages/api/auth.ts, packages/phase-f/lo3/cage.ts, tests/coverage/auth-decision-paths.test.ts, tests/integration/auth/single-use-and-logout-replay.spec.ts, tests/integration/lo3-cage-command.spec.ts. ต้องอ่านจริงจาก HEAD สดอีกครั้ง.
4. ถ้า HEAD เปลี่ยนหลังเริ่ม ให้คำนวณ diff ใหม่ก่อนเขียน. ห้ามใช้ stale SHA เป็น expected commit หรือทับงานผู้อื่น. ห้ามสร้าง/ลบ/เปลี่ยนชื่อ branch, force push, reset หรือแก้ settings/secrets/protection.

## ขั้นตอน 2: ทำ SOURCE AUDIT + ซ่อมที่ READY
จัดงานตามหลักฐานและความเสี่ยง:
A. ตรวจ commit auth/sandbox ใหม่ก่อน อย่าสั่งซ่อม sandbox ซ้ำจากข้อมูลเก่า. ตรวจ OTAC single-use atomicity, race/replay, transaction rollback, expiry, device binding, logout idempotency; ตรวจ bwrap mount isolation, parent-executable pinning, symlinks, traversal, arbitrary host root, executable + library loading, non-root runner. ตรวจ test assertions ว่าไม่ลดความเข้มงวด.
B. รันทดสอบ targeted ของส่วนที่แก้แล้วถ้ามี runner จริง. หากไม่มี runner ให้ระบุ NOT_RUN, ใช้ static/source-contract audit ต่อ; หากพบ bug ที่พิสูจน์ด้วย source และ patch ได้โดยปลอดภัย ให้แก้แบบเล็กที่สุดผ่าน GitHub connector ที่มี write permission พร้อม tests, แต่ห้ามอ้างว่าทดสอบผ่าน.
C. ตรวจ browser 2 failures และ experimental 10 failures จากรายงานก่อนหน้า: เป็นข้อมูลของ HEAD 8b406a63 ไม่ใช่ผล HEAD 44bcb85. Rerun ก่อนจัดเป็น current. Browser เดิมล้มด้วย TSA_TIME_AUTHORITY_UNAVAILABLE; experimental เดิมล้มจาก bwrap /opt runtime path; จะกล่าวว่าปิดได้ต้องมี runtime proof จริง.
D. TSA/queue: ค้น call graph จาก production startup/bootstrap -> verified time -> core/tick.ts -> packages/queue/dispatch.ts/jobs.ts/workers.ts. ตรวจ DOC-B/DOC-C authority จาก EVIDENCE/20261008-NEXY-DOCB-DOCC-TSA-QUEUE-TTL-CLAUSES-005.md. Final DOC-C P9945–P9948 ตั้ง queue stale_job_ttl_ms=900000, max_concurrent_pipeline_runs=10. Final DOC-C ไม่ระบุชัดว่า queue TTL ต้องตรวจลายเซ็น TSA. Broad Core time law P5151–P5158 ห้าม Core ใช้ system clock และระบุ TSA-injected batch time. 3 TSA/2 signatures ใน broader design P4003–P4009. ห้ามสรุปเองว่าใช่หรือไม่ใช่ dependency. ถ้าหลักฐานยังไม่ชัด freeze เฉพาะการแก้ TSA path, ทำงานอิสระที่ READY ต่อ.
E. ตรวจ 98-row matrix ราย requirement จาก canonical authority + current HEAD. ห้าม mass-promote ผลเก่า. รายงานเก่ามี VERIFIED 14, PARTIAL 9, MISMATCH 4, NOT_VERIFIED 62, SPEC_SOURCE_ACCESS_BLOCKED 4, INFRA_BLOCKED 5, substantive coverage 39/98 = 39.8%, classification coverage 98/98. ทั้งหมดเป็น historical ณ HEAD 8b406a63 ไม่ใช่ current-head result. อ่านทุก subsystem ตาม matrix และอัปเดตเฉพาะแถวมี proof.
F. GitHub CI ที่เคย fail ก่อน executable steps ยังไม่รู้ root cause. ตรวจ workflow/check-runs สด; ห้ามเดาว่าเป็น source error หรือ billing, ห้ามลด job, กด PASS ปลอม, หรืออ้าง local runner=CI pass.

## ขั้นตอน 3: AUTHORITY, SAFETY, TEST GATES
1. DOC-C เท่านั้นให้ BUILD obligations; DOC-E เท่านั้นให้ DEPLOY approval. Verbatim authority locators P9844–P9845 ของ SHA-matched DOCX.
2. ห้าม Date.now/new Date/performance.now หรือ arbitrary ENV time เป็น authoritative Core time; ห้าม fake TSA signature / fake 2-of-3.
3. ห้ามปิด bwrap, ลด isolation, bind host ทั้งเครื่อง, ปรับ tests ให้ผ่านลวง, skip tests, ลบ tests, ลด coverage threshold, ใส่ continue-on-error ให้ required gate.
4. ทุก bug: requirement ID -> source -> failure -> minimal patch -> negative regression -> current-head test if tool exists -> source hash -> read-back.
5. ถ้า repo write เป็น READ_ONLY หรือ tool ถูกบล็อก: ทำ static audit ที่ตรวจได้ต่อ, สร้าง actual patch text/handoff ใน AI-CONTEXT/main เท่านั้นถ้าได้รับสิทธิ์; ห้ามบอกว่า commit ใน product เมื่อไม่ได้ commit.
6. DOC-E human engineering/security/migration/monitoring signoffs, application rollback rehearsal, production monitoring/deploy remain NOT_VERIFIED จนมี receipt จริง.
7. ทางเลือกของการแก้ไขต้องพิจารณา race, idempotency, replay, tenant separation, security, dependency compatibility, rollback ก่อน write.

## ขั้นตอน 4: MULTI-CHAT SINGLE-WRITER
ก่อน product mutation ทุกครั้ง:
- อ่าน HEAD สด, ตรวจ source blob SHA ปัจจุบันของไฟล์ที่จะแก้
- ตรวจ concurrent edits
- patch เฉพาะ scope READY
- commit atomic / fast-forward; read-back file + new HEAD + diff
- ถ้า race เกิด ห้าม force และห้ามทับ; recompute ใหม่จาก HEAD สด
- ห้ามรวมหลาย root causes ใน commit เดียวถ้าแยกได้

## ขั้นตอน 5: CLOSEOUT
บันทึก TASKS, LEDGER, CASES, FAILURES (ถ้ามี), EVIDENCE พร้อม immutable HEAD/proofs ใน AI-CONTEXT/main; read-back ทุกไฟล์. ต้องระบุสิ่งที่ไม่สามารถทำได้แยกต่างหากและอย่าอ้างว่าบันทึกแล้วถ้าไม่ read-back.

Audit checklist ก่อน final:
- freeze observed HEAD
- อ่าน temporary working memory จากต้นจนจบ (ถ้าสร้าง)
- deduplicate requirement IDs / conflicting records
- ตรวจ HEAD provenance ของหลักฐาน, recalc stale/negative claims
- ตรวจ requirement ที่ไม่มี record
- ห้ามนับ NOT_VERIFIED เป็น 0 หรือ 100
- completion% คำนวณเฉพาะ rows ที่ได้รับการประเมินมีหลักฐาน; audit coverage แยกจาก completion
- ตาราง status ทุก subsystem

## รูปแบบคำตอบสุดท้าย
MODE / STATUS / LIVE_PRODUCT_HEAD_START / LIVE_PRODUCT_HEAD_END / AI_CONTEXT_HEAD / SPEC_SOURCE_STATUS / CHANGED_FILES / COMMITS / TESTS_EXECUTED / TEST_RESULTS / SOURCE_FINDINGS / TSA_STATUS / BWRAP_STATUS / CI_STATUS / MATRIX_PER_SYSTEM / SUBSTANTIVE_AUDIT_COVERAGE / ASSESSED_COMPLETION_PERCENT / UNRESOLVED / NEXT_READY_ACTION / VERDICT / EVIDENCE_LINKS

ใช้สถานะ VERIFIED_WITH_LIMITS เฉพาะผลที่มีจริง; ถ้า release gate ไม่ผ่านให้ PARTIAL. อย่าบอกว่า COMPLETE/PROD-READY จน DOC-E และ proof ครบ.

**เริ่มตรวจ live GitHub และลงมือทำงานที่ READY ในแชทนี้ทันที ห้ามหยุดที่ acknowledgement, ห้ามขอให้ผู้ใช้ส่งคำสั่งไป Codex และห้ามสั่งให้ผู้ใช้เปิดแชทเพิ่มแทนการทำงานของตนเอง.**
