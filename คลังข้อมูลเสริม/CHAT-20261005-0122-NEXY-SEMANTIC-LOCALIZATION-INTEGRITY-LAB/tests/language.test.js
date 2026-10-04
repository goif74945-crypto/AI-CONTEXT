import test from "node:test";
import assert from "node:assert/strict";
import { analyzeLanguageSemantics, compareNormativeSemantics } from "../src/language.js";

test("English must not is classified as prohibition without duplicate obligation", () => {
  const value = analyzeLanguageSemantics("OWNER must not delete it.", "en");
  assert.equal(value.normative.PROHIBITION, 1);
  assert.equal(value.normative.OBLIGATION, 0);
  assert.ok(value.negationCount > 0);
});

test("Thai ต้องไม่ is classified as prohibition without duplicate obligation", () => {
  const value = analyzeLanguageSemantics("OWNER ต้องไม่ลบ", "th");
  assert.equal(value.normative.PROHIBITION, 1);
  assert.equal(value.normative.OBLIGATION, 0);
  assert.ok(value.negationCount > 0);
});

test("EN obligation and TH obligation compare equal by semantic class", () => {
  const en = analyzeLanguageSemantics("OWNER must verify.", "en");
  const th = analyzeLanguageSemantics("OWNER ต้องตรวจสอบ", "th");
  assert.deepEqual(compareNormativeSemantics(en, th), []);
});

test("permission and obligation mismatch", () => {
  const en = analyzeLanguageSemantics("OWNER may export.", "en");
  const th = analyzeLanguageSemantics("OWNER ต้องส่งออก", "th");
  const mismatches = compareNormativeSemantics(en, th);
  assert.ok(mismatches.some((entry) => entry.class === "PERMISSION"));
  assert.ok(mismatches.some((entry) => entry.class === "OBLIGATION"));
});
