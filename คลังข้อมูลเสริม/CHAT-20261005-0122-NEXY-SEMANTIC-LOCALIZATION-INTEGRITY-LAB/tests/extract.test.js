import test from "node:test";
import assert from "node:assert/strict";
import {
  extractCanonicalTokens,
  extractEmails,
  extractIdentifiers,
  extractNumbers,
  extractPlaceholders,
  extractUrls,
  extractUnits
} from "../src/extract.js";

test("extractNumbers preserves numeric lexemes and percentages", () => {
  assert.deepEqual(extractNumbers("5 10.5 99% -3 +4,000"), ["5", "10.5", "99%", "-3", "+4,000"]);
});

test("extractPlaceholders recognizes supported forms", () => {
  assert.deepEqual(extractPlaceholders("{id} {{name}} ${value} %s %d"), ["{id}", "{{name}}", "${value}", "%s", "%d"]);
});

test("extractUrls strips sentence punctuation", () => {
  assert.deepEqual(extractUrls("See https://example.com/a."), ["https://example.com/a"]);
});

test("extractEmails is case-normalized", () => {
  assert.deepEqual(extractEmails("OPS@Example.COM"), ["ops@example.com"]);
});

test("extractIdentifiers finds SHA-256, UUID, backtick and UPPER_SNAKE", () => {
  const sha = "a".repeat(64);
  const values = extractIdentifiers(`${sha} 123e4567-e89b-12d3-a456-426614174000 \`artifact_id\` CORE_LOCK`);
  assert.deepEqual(values, [sha, "123e4567-e89b-12d3-a456-426614174000", "`artifact_id`", "CORE_LOCK"]);
});

test("extractCanonicalTokens honors token boundaries", () => {
  assert.deepEqual(extractCanonicalTokens("FREEZE FREEZER PASS", ["FREEZE", "PASS"]), ["FREEZE", "PASS"]);
});


test("extractUnits maps EN and TH time units to semantic classes", () => {
  assert.deepEqual(extractUnits("5 seconds 500 ms 2 นาที"), ["SECOND", "MILLISECOND", "MINUTE"]);
});
