#!/usr/bin/env node
import fs from "node:fs";
import { analyzeTranslation } from "./index.js";

const inputPath = process.argv[2];
if (!inputPath) {
  process.stderr.write("Usage: node src/cli.js <translation-contract.json>\n");
  process.exit(2);
}

try {
  const contract = JSON.parse(fs.readFileSync(inputPath, "utf8"));
  const report = analyzeTranslation(contract);
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  process.exit(report.decision === "PASS" ? 0 : 3);
} catch (error) {
  process.stderr.write(`${error instanceof Error ? error.stack : String(error)}\n`);
  process.exit(2);
}
