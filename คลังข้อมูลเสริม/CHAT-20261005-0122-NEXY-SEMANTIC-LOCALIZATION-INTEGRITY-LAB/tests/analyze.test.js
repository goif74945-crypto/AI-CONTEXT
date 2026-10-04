import test from "node:test";
import assert from "node:assert/strict";
import { analyzeTranslation } from "../src/index.js";

const run=(source,target,sourceLanguage="en",targetLanguage="th",extra={},policy={})=>
  analyzeTranslation({source,target,sourceLanguage,targetLanguage,...extra},policy);
const codes=r=>r.issues.map(x=>x.code);
const pass=(name,args)=>test(`PASS: ${name}`,()=>assert.equal(run(...args).decision,"PASS"));
const freeze=(name,code,args)=>test(`FREEZE: ${name}`,()=>{const r=run(...args);assert.equal(r.decision,"FREEZE");assert.ok(codes(r).includes(code),`${code} missing: ${codes(r)}`)});

pass("EN→TH prohibition + protected structures",[
  "The OWNER must not release FREEZE incident 42 without verification. Keep {incident_id} and https://example.com/run/42 unchanged.",
  "OWNER ต้องไม่เผยแพร่เหตุการณ์ FREEZE หมายเลข 42 โดยไม่มีการตรวจสอบ คง {incident_id} และ https://example.com/run/42 ไว้เหมือนเดิม"
]);
pass("EN→TH obligation",["The OWNER must verify artifact 5.","OWNER ต้องตรวจสอบอาร์ติแฟกต์ 5"]);
pass("TH→EN prohibition",["OPERATOR ห้ามเปลี่ยน FREEZE เป็น PASS","OPERATOR must not change FREEZE to PASS.","th","en"]);
freeze("number drift","E_NUMBER_MISMATCH",["Retry limit must be 5 before FREEZE.","ขีดจำกัดการลองใหม่ต้องเป็น 6 ก่อน FREEZE"]);
freeze("placeholder removed","E_PLACEHOLDER_MISMATCH",["OWNER must inspect {artifact_id}.","OWNER ต้องตรวจสอบอาร์ติแฟกต์"]);
freeze("canonical FREEZE removed","E_CANONICAL_TOKEN_MISMATCH",["The system must enter FREEZE.","ระบบต้องหยุดการทำงาน"]);
freeze("permission escalated to obligation","E_MODALITY_MISMATCH",["The OPERATOR may export the report.","OPERATOR ต้องส่งออกรายงาน"]);
freeze("obligation weakened to recommendation","E_MODALITY_MISMATCH",["The OWNER must verify the result.","OWNER ควรตรวจสอบผลลัพธ์"]);
freeze("prohibition polarity lost","E_NEGATION_MISMATCH",["The OWNER must not delete the audit record.","OWNER ต้องลบบันทึกการตรวจสอบ"]);
freeze("negation added","E_NEGATION_MISMATCH",["The OWNER must approve the result.","OWNER ต้องไม่อนุมัติผลลัพธ์"]);
freeze("URL drift","E_URL_MISMATCH",["Open https://example.com/a and verify it.","เปิด https://example.com/b และตรวจสอบ"]);
freeze("email drift","E_EMAIL_MISMATCH",["Send to ops@example.com.","ส่งไปที่ owner@example.com"]);
freeze("hash drift","E_IDENTIFIER_MISMATCH",[`Artifact hash is ${"a".repeat(64)}.`,`แฮชอาร์ติแฟกต์คือ ${"b".repeat(64)}`]);
freeze("UUID drift","E_IDENTIFIER_MISMATCH",["Run 123e4567-e89b-12d3-a456-426614174000.","รัน 123e4567-e89b-12d3-a456-426614174001"]);
freeze("backtick identifier drift","E_IDENTIFIER_MISMATCH",["Use `directive_id`.","ใช้ `directiveId`"]);
freeze("protected literal removed","E_PROTECTED_LITERAL_MISMATCH",["The legal state is CORE::LOCKED.","สถานะทางกฎหมายถูกล็อก","en","th",{protectedLiterals:["CORE::LOCKED"]}]);
pass("protected literal multiplicity preserved",["X means X.","X หมายถึง X","en","th",{protectedLiterals:["X"]}]);
freeze("protected literal multiplicity drift","E_PROTECTED_LITERAL_MISMATCH",["X means X.","X หมายถึงค่า","en","th",{protectedLiterals:["X"]}]);
freeze("empty source","E_EMPTY_SOURCE",["","ข้อความ"]);
freeze("empty target","E_EMPTY_TARGET",["Text",""]);
pass("Unicode NFC equivalence",["Cafe\u0301","Café","en","en",{protectedLiterals:["Café"]}]);
freeze("technical unit drift","E_UNIT_MISMATCH",["Timeout must be 500 ms.","เวลาหมดอายุต้องเป็น 500 s"]);
pass("localized semantic unit",["Timeout must be 5 seconds.","เวลาหมดอายุต้องเป็น 5 วินาที"]);
freeze("unsupported target language","E_UNSUPPORTED_TARGET_LANGUAGE",["OWNER must verify FREEZE incident 5.","OWNER doit vérifier l’incident FREEZE 5.","en","fr"]);

test("fingerprint deterministic over 100 identical runs",()=>{
  const args=["OWNER must not change FREEZE incident 42.","OWNER ต้องไม่เปลี่ยนเหตุการณ์ FREEZE 42"];
  assert.equal(new Set(Array.from({length:100},()=>run(...args).fingerprint)).size,1);
});
test("issue ordering deterministic",()=>{
  const r=run("OWNER must not send 5 to ops@example.com at https://example.com/a using {id} and FREEZE.","OWNER ต้องส่ง 6 ไป owner@example.com ที่ https://example.com/b โดยใช้ {other} และ PASS");
  assert.deepEqual(codes(r),[...codes(r)].sort());
});
test("policy override does not mutate default",()=>{
  const args=["LockA","ล็อก"];
  assert.equal(run(...args,"en","th",{},{canonicalTokens:["LockA"]}).decision,"FREEZE");
  assert.equal(run(...args).decision,"PASS");
});
test("report keeps proposal non-authoritative",()=>assert.equal(run("Text","ข้อความ").proposalStatus,"AI_PROPOSED_CONCEPT_NOT_ADOPTED"));
