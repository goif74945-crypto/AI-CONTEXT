import test from "node:test";
import assert from "node:assert/strict";
import { analyzeTranslation } from "../src/index.js";

function codes(report) {
  return report.issues.map((entry) => entry.code);
}

test("PASS: preserves prohibition, canonical tokens, number, placeholder and URL across EN→TH", () => {
  const report = analyzeTranslation({
    source: "The OWNER must not release FREEZE incident 42 without verification. Keep {incident_id} and https://example.com/run/42 unchanged.",
    target: "OWNER ต้องไม่เผยแพร่เหตุการณ์ FREEZE หมายเลข 42 โดยไม่มีการตรวจสอบ คง {incident_id} และ https://example.com/run/42 ไว้เหมือนเดิม",
    sourceLanguage: "en",
    targetLanguage: "th"
  });
  assert.equal(report.decision, "PASS");
  assert.equal(report.blockerCount, 0);
});

test("PASS: preserves obligation EN→TH", () => {
  const report = analyzeTranslation({
    source: "The OWNER must verify artifact 5.",
    target: "OWNER ต้องตรวจสอบอาร์ติแฟกต์ 5",
    sourceLanguage: "en",
    targetLanguage: "th"
  });
  assert.equal(report.decision, "PASS");
});

test("PASS: preserves prohibition TH→EN", () => {
  const report = analyzeTranslation({
    source: "OPERATOR ห้ามเปลี่ยน FREEZE เป็น PASS",
    target: "OPERATOR must not change FREEZE to PASS.",
    sourceLanguage: "th",
    targetLanguage: "en"
  });
  assert.equal(report.decision, "PASS");
});

test("FREEZE: number drift", () => {
  const report = analyzeTranslation({
    source: "Retry limit must be 5 before FREEZE.",
    target: "ขีดจำกัดการลองใหม่ต้องเป็น 6 ก่อน FREEZE",
    sourceLanguage: "en",
    targetLanguage: "th"
  });
  assert.equal(report.decision, "FREEZE");
  assert.ok(codes(report).includes("E_NUMBER_MISMATCH"));
});

test("FREEZE: placeholder removed", () => {
  const report = analyzeTranslation({
    source: "OWNER must inspect {artifact_id}.",
    target: "OWNER ต้องตรวจสอบอาร์ติแฟกต์",
    sourceLanguage: "en",
    targetLanguage: "th"
  });
  assert.equal(report.decision, "FREEZE");
  assert.ok(codes(report).includes("E_PLACEHOLDER_MISMATCH"));
});

test("FREEZE: canonical FREEZE token removed", () => {
  const report = analyzeTranslation({
    source: "The system must enter FREEZE.",
    target: "ระบบต้องหยุดการทำงาน",
    sourceLanguage: "en",
    targetLanguage: "th"
  });
  assert.equal(report.decision, "FREEZE");
  assert.ok(codes(report).includes("E_CANONICAL_TOKEN_MISMATCH"));
});

test("FREEZE: permission escalated into obligation", () => {
  const report = analyzeTranslation({
    source: "The OPERATOR may export the report.",
    target: "OPERATOR ต้องส่งออกรายงาน",
    sourceLanguage: "en",
    targetLanguage: "th"
  });
  assert.equal(report.decision, "FREEZE");
  assert.ok(codes(report).includes("E_MODALITY_MISMATCH"));
});

test("FREEZE: obligation weakened into recommendation", () => {
  const report = analyzeTranslation({
    source: "The OWNER must verify the result.",
    target: "OWNER ควรตรวจสอบผลลัพธ์",
    sourceLanguage: "en",
    targetLanguage: "th"
  });
  assert.equal(report.decision, "FREEZE");
  assert.ok(codes(report).includes("E_MODALITY_MISMATCH"));
});

test("FREEZE: prohibition polarity lost", () => {
  const report = analyzeTranslation({
    source: "The OWNER must not delete the audit record.",
    target: "OWNER ต้องลบบันทึกการตรวจสอบ",
    sourceLanguage: "en",
    targetLanguage: "th"
  });
  assert.equal(report.decision, "FREEZE");
  assert.ok(codes(report).includes("E_MODALITY_MISMATCH"));
  assert.ok(codes(report).includes("E_NEGATION_MISMATCH"));
});

test("FREEZE: negation added", () => {
  const report = analyzeTranslation({
    source: "The OWNER must approve the result.",
    target: "OWNER ต้องไม่อนุมัติผลลัพธ์",
    sourceLanguage: "en",
    targetLanguage: "th"
  });
  assert.equal(report.decision, "FREEZE");
  assert.ok(codes(report).includes("E_NEGATION_MISMATCH"));
});

test("FREEZE: URL drift", () => {
  const report = analyzeTranslation({
    source: "Open https://example.com/a and verify it.",
    target: "เปิด https://example.com/b และตรวจสอบ",
    sourceLanguage: "en",
    targetLanguage: "th"
  });
  assert.equal(report.decision, "FREEZE");
  assert.ok(codes(report).includes("E_URL_MISMATCH"));
});

test("FREEZE: email drift", () => {
  const report = analyzeTranslation({
    source: "Send to ops@example.com.",
    target: "ส่งไปที่ owner@example.com",
    sourceLanguage: "en",
    targetLanguage: "th"
  });
  assert.equal(report.decision, "FREEZE");
  assert.ok(codes(report).includes("E_EMAIL_MISMATCH"));
});

test("FREEZE: hash drift", () => {
  const a = "a".repeat(64);
  const b = "b".repeat(64);
  const report = analyzeTranslation({
    source: `Artifact hash is ${a}.`,
    target: `แฮชอาร์ติแฟกต์คือ ${b}`,
    sourceLanguage: "en",
    targetLanguage: "th"
  });
  assert.equal(report.decision, "FREEZE");
  assert.ok(codes(report).includes("E_IDENTIFIER_MISMATCH"));
});

test("FREEZE: UUID drift", () => {
  const report = analyzeTranslation({
    source: "Run 123e4567-e89b-12d3-a456-426614174000.",
    target: "รัน 123e4567-e89b-12d3-a456-426614174001",
    sourceLanguage: "en",
    targetLanguage: "th"
  });
  assert.equal(report.decision, "FREEZE");
  assert.ok(codes(report).includes("E_IDENTIFIER_MISMATCH"));
});

test("FREEZE: backtick identifier drift", () => {
  const report = analyzeTranslation({
    source: "Use `directive_id`.",
    target: "ใช้ `directiveId`",
    sourceLanguage: "en",
    targetLanguage: "th"
  });
  assert.equal(report.decision, "FREEZE");
  assert.ok(codes(report).includes("E_IDENTIFIER_MISMATCH"));
});

test("FREEZE: protected literal is removed", () => {
  const report = analyzeTranslation({
    source: "The legal state is CORE::LOCKED.",
    target: "สถานะทางกฎหมายถูกล็อก",
    sourceLanguage: "en",
    targetLanguage: "th",
    protectedLiterals: ["CORE::LOCKED"]
  });
  assert.equal(report.decision, "FREEZE");
  assert.ok(codes(report).includes("E_PROTECTED_LITERAL_MISMATCH"));
});

test("PASS: repeated protected literal count preserved", () => {
  const report = analyzeTranslation({
    source: "X means X.",
    target: "X หมายถึง X",
    sourceLanguage: "en",
    targetLanguage: "th",
    protectedLiterals: ["X"]
  });
  assert.equal(report.decision, "PASS");
});

test("FREEZE: repeated protected literal count changes", () => {
  const report = analyzeTranslation({
    source: "X means X.",
    target: "X หมายถึงค่า",
    sourceLanguage: "en",
    targetLanguage: "th",
    protectedLiterals: ["X"]
  });
  assert.equal(report.decision, "FREEZE");
  assert.ok(codes(report).includes("E_PROTECTED_LITERAL_MISMATCH"));
});

test("FREEZE: empty source", () => {
  const report = analyzeTranslation({source: "", target: "ข้อความ", sourceLanguage: "en", targetLanguage: "th"});
  assert.equal(report.decision, "FREEZE");
  assert.ok(codes(report).includes("E_EMPTY_SOURCE"));
});

test("FREEZE: empty target", () => {
  const report = analyzeTranslation({source: "Text", target: "", sourceLanguage: "en", targetLanguage: "th"});
  assert.equal(report.decision, "FREEZE");
  assert.ok(codes(report).includes("E_EMPTY_TARGET"));
});

test("PASS: Unicode NFC normalization prevents false protected-literal mismatch", () => {
  const decomposed = "Cafe\u0301";
  const composed = "Café";
  const report = analyzeTranslation({
    source: decomposed,
    target: composed,
    sourceLanguage: "en",
    targetLanguage: "en",
    protectedLiterals: [composed]
  });
  assert.equal(report.decision, "PASS");
});

test("fingerprint is deterministic across repeated execution", () => {
  const contract = {
    source: "OWNER must not change FREEZE incident 42.",
    target: "OWNER ต้องไม่เปลี่ยนเหตุการณ์ FREEZE 42",
    sourceLanguage: "en",
    targetLanguage: "th"
  };
  const fingerprints = new Set(Array.from({length: 100}, () => analyzeTranslation(contract).fingerprint));
  assert.equal(fingerprints.size, 1);
});

test("issue ordering is deterministic", () => {
  const report = analyzeTranslation({
    source: "OWNER must not send 5 to ops@example.com at https://example.com/a using {id} and FREEZE.",
    target: "OWNER ต้องส่ง 6 ไป owner@example.com ที่ https://example.com/b โดยใช้ {other} และ PASS",
    sourceLanguage: "en",
    targetLanguage: "th"
  });
  const sorted = [...codes(report)].sort();
  assert.deepEqual(codes(report), sorted);
});

test("policy override can add canonical token without mutating default policy", () => {
  const contract = {source: "LockA", target: "ล็อก", sourceLanguage: "en", targetLanguage: "th"};
  const custom = analyzeTranslation(contract, {canonicalTokens: ["LockA"]});
  assert.equal(custom.decision, "FREEZE");
  const ordinary = analyzeTranslation(contract);
  assert.equal(ordinary.decision, "PASS");
});

test("report explicitly labels proposal as not adopted", () => {
  const report = analyzeTranslation({source: "Text", target: "ข้อความ", sourceLanguage: "en", targetLanguage: "th"});
  assert.equal(report.proposalStatus, "AI_PROPOSED_CONCEPT_NOT_ADOPTED");
});


test("FREEZE: technical unit drift despite identical number", () => {
  const report = analyzeTranslation({
    source: "Timeout must be 500 ms.",
    target: "เวลาหมดอายุต้องเป็น 500 s",
    sourceLanguage: "en",
    targetLanguage: "th"
  });
  assert.equal(report.decision, "FREEZE");
  assert.ok(codes(report).includes("E_UNIT_MISMATCH"));
});

test("PASS: localized semantic unit preserves meaning", () => {
  const report = analyzeTranslation({
    source: "Timeout must be 5 seconds.",
    target: "เวลาหมดอายุต้องเป็น 5 วินาที",
    sourceLanguage: "en",
    targetLanguage: "th"
  });
  assert.equal(report.decision, "PASS");
});

test("FREEZE: unsupported target language is never treated as verified", () => {
  const report = analyzeTranslation({
    source: "OWNER must verify FREEZE incident 5.",
    target: "OWNER doit vérifier l’incident FREEZE 5.",
    sourceLanguage: "en",
    targetLanguage: "fr"
  });
  assert.equal(report.decision, "FREEZE");
  assert.ok(codes(report).includes("E_UNSUPPORTED_TARGET_LANGUAGE"));
});
