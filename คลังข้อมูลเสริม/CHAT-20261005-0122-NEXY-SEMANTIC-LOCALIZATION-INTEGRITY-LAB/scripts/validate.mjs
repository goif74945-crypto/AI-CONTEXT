import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { analyzeTranslation, loadDefaultPolicy } from "../src/index.js";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const required = [
  "README.md",
  "00_SESSION_MEMORY.md",
  "01_TASK_CONTRACT.md",
  "02_CONCEPT_AND_SCOPE.md",
  "03_ARCHITECTURE.md",
  "04_INVARIANTS_AND_FAILURE_MODEL.md",
  "05_ADVERSARIAL_CORPUS_DESIGN.md",
  "06_ADOPTION_GATES.md",
  "07_FUTURE_AI_PROPOSALS.md",
  "08_REQUIREMENT_LEDGER.md",
  "IMPLEMENTATION_MANIFEST.json",
  "package.json",
  "config/default-policy.json",
  "schema/policy.schema.json",
  "schema/translation-contract.schema.json",
  "src/index.js",
  "src/extract.js",
  "src/language.js",
  "src/multiset.js",
  "src/policy.js",
  "src/cli.js",
  "tests/analyze.test.js",
  "tests/extract.test.js",
  "tests/language.test.js",
  "fixtures/pass-en-th.json",
  "fixtures/freeze-number-drift.json",
  "fixtures/freeze-authority-drift.json"
];

for (const relative of required) {
  const absolute = path.join(root, relative);
  if (!fs.existsSync(absolute)) throw new Error(`Required file missing: ${relative}`);
}

for (const relative of ["package.json", "config/default-policy.json", "schema/policy.schema.json", "schema/translation-contract.schema.json", "fixtures/pass-en-th.json", "fixtures/freeze-number-drift.json", "fixtures/freeze-authority-drift.json"]) {
  JSON.parse(fs.readFileSync(path.join(root, relative), "utf8"));
}

const policy = loadDefaultPolicy();
if (policy.mode !== "strict") throw new Error("Default policy must remain strict.");
if (new Set(policy.canonicalTokens).size !== policy.canonicalTokens.length) throw new Error("canonicalTokens must be unique.");
if (!policy.supportedLanguages.includes("en") || !policy.supportedLanguages.includes("th")) throw new Error("Reference lab must support EN and TH.");

const passFixture = JSON.parse(fs.readFileSync(path.join(root, "fixtures/pass-en-th.json"), "utf8"));
const freezeFixture = JSON.parse(fs.readFileSync(path.join(root, "fixtures/freeze-number-drift.json"), "utf8"));
if (analyzeTranslation(passFixture).decision !== "PASS") throw new Error("PASS fixture did not pass.");
if (analyzeTranslation(freezeFixture).decision !== "FREEZE") throw new Error("FREEZE fixture did not freeze.");

process.stdout.write(`VALIDATION_PASS required_files=${required.length} policy=${policy.policyVersion}\n`);
