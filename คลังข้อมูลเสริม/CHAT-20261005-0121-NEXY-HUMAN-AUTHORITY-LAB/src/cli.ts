import { readFile } from "node:fs/promises";
import { evaluateScenario } from "./engine.js";
import type { Scenario } from "./types.js";

async function main(): Promise<void> {
  const input = process.argv[2];
  if (!input) {
    process.stderr.write("Usage: node dist/src/cli.js <scenario.json>\n");
    process.exitCode = 2;
    return;
  }

  try {
    const raw = await readFile(input, "utf8");
    const scenario = JSON.parse(raw) as Scenario;
    const result = evaluateScenario(scenario);
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    process.stderr.write(`Evaluation failed: ${message}\n`);
    process.exitCode = 1;
  }
}

await main();
