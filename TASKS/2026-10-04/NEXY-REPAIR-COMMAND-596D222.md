# NEXY TARGETED REPAIR COMMAND — 596D222

SYSTEM: NEXY::TARGETED-REPAIR-EXECUTOR-V1
CHAT_ID=NEXY-REPAIR-596D222
MODE=EXECUTE/CROSS

PROJECT=NEXY.AI / NEXY-IGNIS
REPOSITORY=goif74945-crypto/NEXY.AI-
ONLY_BRANCH=NEXY.ai
AI_CONTEXT=goif74945-crypto/AI-CONTEXT
AUTHORITATIVE_SPEC=แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx
AUTHORITATIVE_SPEC_SHA256=b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
VERIFIED_BASELINE_HEAD=596d2225676ea978dc0ccf22e34a597949104f79

MISSION:
แก้เฉพาะระบบที่มีหลักฐานยืนยันว่าต้องแก้หรือยังไม่สมบูรณ์จาก audit ล่าสุด โดยแก้โค้ดจริง รันเทสจริง สร้างหลักฐานจริง และอัปเดต AI-CONTEXT ตาม HEAD ใหม่ ห้ามประกาศ 100% หากยังมีข้อใด NOT_VERIFIED/BLOCKED/FAIL

STRICT RULES:
1. ห้ามสร้าง branch ใหม่ ใช้ NEXY.ai เท่านั้น
2. ก่อนแก้ให้ตรวจ HEAD ปัจจุบัน ถ้าเปลี่ยนจาก VERIFIED_BASELINE_HEAD ให้ทำ semantic revalidation ของ target ที่เกี่ยวข้องก่อนลงมือ
3. ห้ามแก้ authoritative spec เพื่อให้โค้ดผ่าน
4. ห้ามลดความเข้มของ test, assertion, gate, security check หรือ determinism check เพื่อทำให้ CI เขียว
5. ห้าม skip/disable test ที่ fail
6. ห้ามใช้ fallback ที่ขัดสเป็ก
7. ห้ามเปลี่ยนระบบนอก scope ถ้าไม่จำเป็นต่อ dependency ที่พิสูจน์ได้
8. ทุกการแก้ต้องผูก source -> claim -> code diff -> test -> evidence
9. ถ้าหาสาเหตุไม่เจอ ให้สถานะ UNKNOWN/BLOCKED ห้ามเดา
10. ห้ามเรียกงานว่า complete/release-ready จน exact-head tests และ release evidence ผ่านจริง

TARGET-01 — Runtime determinism
KNOWN EVIDENCE:
- packages/core/tick.ts blob baseline: 92ce2ae30a74d767013b322dd0d7aceb3fedd8b0
- currentTick() เป็น authoritative clock path
- baseline ใช้ process.hrtime.bigint() ที่บรรทัด 41, 58, 108, 139
- authoritative spec: Core cannot read system clock
- allowed: TSA-injected batch time only
- forbidden: Date.now / system_time / monotonic_clock

REPAIR:
- เอา dependency ต่อ process.hrtime.bigint() และ system/monotonic clock ออกจาก authoritative Core clock path
- เวลา authoritative ต้องมาจาก source ที่สเป็กอนุญาตจริง เช่น TSA-injected batch time / deterministic logical state ตามที่ canonical design กำหนด
- ห้ามแทนด้วย Date.now(), performance.now(), new Date(), process.hrtime(), OS timer หรือ time source อื่นที่เป็น nondeterministic
- รักษา deterministic replay: input/spec/canon/event stream เดิมต้องให้ tick/state เดิม
- ตรวจ callers ของ currentTick() ทั้งหมดและแก้ contract อย่างมีหลักฐาน ห้าม patch แค่บรรทัดเดียวแล้วทิ้ง behavior พัง

REQUIRED TESTS:
- identical injected batch/event time -> identical tick sequence
- replay/restart -> identical tick/state output
- forbidden clock source in authoritative core -> gate ต้อง fail
- valid deterministic injected clock -> gate/test ต้อง pass

TARGET-02 — Runtime enforcement
KNOWN EVIDENCE:
- scripts/check-static-determinism.ts baseline blob: 478c50115761d8f41d53383785531e7f8b19990b
- checker ตรวจ localeCompare / Math.random / Date.now / process.hrtime / process.hrtime.bigint
- แต่ baseline scan แค่ packages/phase-f/game ผ่าน GAME_ROOT

REPAIR:
- ขยาย static determinism enforcement ให้ครอบคลุม authoritative runtime paths ที่สเป็กกำหนด โดยอย่างน้อยต้องตรวจ packages/core
- หา authoritative roots จาก repo/spec จริงก่อนสร้าง scope สุดท้าย
- แยก runtime production paths ออกจาก tests/scripts/generated/vendor ด้วยกติกาที่ตรวจสอบย้อนกลับได้
- ห้าม hardcode exemption เพื่อซ่อน violation
- checker ต้องจับ violation ใน packages/core/tick.ts แบบ baseline ได้จริง
- error output ต้องระบุ path, rule, offending construct และผล FAIL ชัดเจน

REQUIRED TESTS:
- negative fixture ที่มี process.hrtime.bigint() ใน authoritative core -> FAIL
- negative fixture ที่มี Date.now/Math.random ใน authoritative deterministic path -> FAIL
- approved non-authoritative boundary ตามสเป็ก -> PASS เฉพาะเมื่อมี explicit rule
- repo scan หลังแก้ -> ไม่มี unapproved deterministic violation

TARGET-03 — Test / CI gate
KNOWN EVIDENCE AT BASELINE HEAD:
- run 37202785747 Exact HEAD test evidence -> failure
- run 37202785787 NEXY CI / Deploy Gate -> failure
- run 37202785862 Layer8 Cargo lock evidence -> failure
- run 37202785871 Six-system exact HEAD evidence -> failure
- baseline ไม่มี newer rerun ที่ผ่าน
- root cause ของ zero-step failures ยัง UNKNOWN

REPAIR:
- ตรวจ workflow YAML, workflow/job configuration, repository scripts, dependency/install/build commands และ logs ที่เข้าถึงได้
- ถ้า GitHub log ไม่พอ ให้ reproduce command จริงใน workspace ตาม package manager/toolchain ของ repo
- แก้เฉพาะ root cause ที่พิสูจน์ได้
- ห้ามตีความ workflow failure เป็น assertion failure ถ้าไม่มี log ยืนยัน
- หลัง commit ใหม่ ให้รัน canonical build/test/typecheck/integration/determinism/security gates ที่ repo กำหนดจริง
- จากนั้นสร้าง exact-head CI evidence ที่ผูกกับ HEAD ใหม่

ACCEPTANCE:
- required exact-head workflow/gates ต้อง conclusion=success จริง
- job steps/logs ต้องอ่านตรวจสอบได้
- ไม่มี skipped release-critical gate โดยไม่มีเหตุผลจาก spec
- ถ้ายังมี infra/permission limitation ให้ BLOCKED และบอกหลักฐาน ห้ามปลอม PASS

TARGET-04 — Exact-head deployment evidence
REPAIR:
- ทำหลัง TARGET-01..03 ผ่านเท่านั้น
- สร้าง evidence/attestation ที่ผูกกับ HEAD ใหม่ ไม่ใช้ผลเทสจาก commit เก่า
- อย่างน้อยต้องบันทึก: repository, branch, exact HEAD SHA, workflow run IDs, job IDs, build/test results, artifact identities/digests ถ้ามี, timestamp source, unresolved blockers
- deployment/release gate ต้อง reject stale evidence
- ถ้าไม่มี deployment environment หรือ permission จริง ให้ BLOCKED ไม่ใช่ SUCCESS

TARGET-05 — G14 Toolchain / Game WebGPU runtime
KNOWN EVIDENCE:
- packages/phase-f/game/runtime/webgpu.ts baseline blob: 73773fa3a309d5dae0240fbf1dcdce9cc88aefb6
- file ระบุเองว่า WebGPU pipeline เป็น stub
- file ระบุ production จะ submit draw calls ผ่าน WebGPU แต่ปัจจุบันเป็น in-process simulation

REPAIR:
- อ่าน requirement G14/WebGPU จาก authoritative spec แบบ 1:1 ก่อนเขียนโค้ด
- implement เฉพาะ behavior ที่สเป็กกำหนดจริง
- ถ้าสเป็กกำหนด WebGPU จริง ให้สร้าง real WebGPU integration path จริง ไม่ใช่เปลี่ยนชื่อ stub
- capability detection / initialization / shader handling / device failure ต้องสะท้อนสถานะจริง
- nondeterministic GPU result ห้ามกลายเป็น authoritative canonical state ถ้าสเป็กไม่ได้อนุญาต
- simulation/fallback จะเก็บไว้ได้เฉพาะเมื่อสเป็กอนุญาตชัดเจน และต้องรายงานว่าเป็น mode ใด
- ถ้า CI environment ไม่มี WebGPU ให้ใช้ test strategy ที่พิสูจน์ integration contract ได้ และแยก hardware execution evidence เป็น BLOCKED จนมีของจริง ห้ามอ้างว่าทดสอบ GPU จริงถ้าไม่ได้รัน

OPEN RISKS — ห้ามรีบแก้โดยเดา
ไฟล์/ระบบที่มี localeCompare ใน L1o, Lo3, Sovereign canon seal, Global Anchor ยังเป็น NOT_VERIFIED risk
ขั้นตอน:
1. อ่าน exact spec requirement เรื่อง lexicographic/canonical ordering
2. พิสูจน์ว่า localeCompare ให้ผล host/locale dependent ที่ขัด requirement หรือไม่ใน path นั้น
3. ถ้าขัดจริง ให้เปลี่ยนเป็น canonical deterministic comparator และเพิ่ม regression test
4. ถ้ายังพิสูจน์ไม่ได้ คง NOT_VERIFIED ห้ามนับ FAIL/PASS

EXECUTION ORDER:
A. Freeze HEAD + dirty state + spec identity
B. Revalidate target evidence ถ้า HEAD เปลี่ยน
C. Fix TARGET-01 Runtime determinism
D. Fix TARGET-02 Runtime enforcement
E. Run focused deterministic tests
F. Diagnose/fix TARGET-03 CI gate
G. Run full canonical test/build/typecheck/security/determinism suite
H. Fix/complete TARGET-05 G14 WebGPU ตาม exact spec
I. Re-run full regression
J. Produce TARGET-04 exact-head evidence
K. Re-audit changed files against spec
L. Update AI-CONTEXT
M. Read-back AI-CONTEXT และ Final Gate

MANDATORY VALIDATION:
- use actual package scripts/toolchain from repository; do not invent command names
- typecheck
- unit tests
- integration/contract tests
- deterministic/static gate
- replay/idempotency tests where applicable
- security tests where affected
- production build
- exact-head GitHub Actions
- regression of directly dependent systems
- no test deletion/weakening
- no unrelated refactor

EVIDENCE FORMAT FOR EACH CHANGE:
REQ/SPEC:
SOURCE LOCATION:
OLD BEHAVIOR:
NEW BEHAVIOR:
FILES:
COMMIT:
TEST COMMAND:
EXIT CODE:
RESULT:
ARTIFACT/RUN ID:
NEGATIVE TEST:
REGRESSION:
UNRESOLVED:
VERDICT:

AI-CONTEXT WRITE REQUIRED:
หลังจบ ไม่ว่าจะ SUCCESS/PARTIAL/FAILED/BLOCKED ให้เขียนและ read-back:
- TASKS
- CASES
- FAILURES ถ้ามี
- LEDGER

ต้องบันทึก:
old HEAD
new HEAD
spec hash
changed paths
claims/proofs
commands + exit codes
workflow run IDs/jobs
artifacts
successes/failures
unresolved
risks
rollback
final status

FINAL GATE:
จะตอบ VERIFIED_WITH_LIMITS หรือ COMPLETE ได้เฉพาะเมื่อ:
- Runtime determinism ตรงสเป็ก
- Runtime enforcement จับ violation ใน authoritative Core ได้
- required exact-head CI ผ่านจริง
- release/deployment evidence ผูก HEAD ใหม่
- G14 requirement ที่อยู่ใน scope ไม่มี stub ที่ขัดสเป็ก
- regression ผ่าน
- ไม่มี critical UNKNOWN
- AI-CONTEXT write + read-back ผ่าน

ถ้าข้อใดไม่ผ่าน:
STATUS=PARTIAL หรือ FREEZE/BLOCKED
ห้ามรายงาน 100%
