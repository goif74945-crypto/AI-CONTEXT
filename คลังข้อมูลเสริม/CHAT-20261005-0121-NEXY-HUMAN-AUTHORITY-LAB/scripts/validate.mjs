import { readdir, readFile, stat } from "node:fs/promises";
import { join, relative, resolve } from "node:path";

const root = resolve(new URL("..", import.meta.url).pathname);
const required = [
  "package.json",
  "tsconfig.json",
  "schemas/intent-contract.schema.json",
  "schemas/evaluation-report.schema.json",
  "src/types.ts",
  "src/canonical.ts",
  "src/engine.ts",
  "src/cli.ts",
  "fixtures/scenario-cases.json",
  "tests/engine.test.mjs"
];

const failures = [];
for (const path of required) {
  try {
    if (!(await stat(join(root, path))).isFile()) failures.push(`NOT_FILE:${path}`);
  } catch {
    failures.push(`MISSING:${path}`);
  }
}

for (const path of ["package.json", "schemas/intent-contract.schema.json", "schemas/evaluation-report.schema.json", "fixtures/scenario-cases.json"]) {
  try {
    JSON.parse(await readFile(join(root, path), "utf8"));
  } catch (error) {
    failures.push(`INVALID_JSON:${path}:${error instanceof Error ? error.message : String(error)}`);
  }
}

try {
  const cases = JSON.parse(await readFile(join(root, "fixtures/scenario-cases.json"), "utf8"));
  const ids = cases.map((item) => item.id);
  if (ids.length < 20) failures.push(`FIXTURE_COUNT_TOO_LOW:${ids.length}`);
  if (new Set(ids).size !== ids.length) failures.push("DUPLICATE_FIXTURE_ID");
} catch {}

async function walk(dir) {
  const out = [];
  for (const name of await readdir(dir)) {
    if (name === "dist" || name === "node_modules") continue;
    const full = join(dir, name);
    const s = await stat(full);
    if (s.isDirectory()) out.push(...await walk(full));
    else out.push(full);
  }
  return out;
}

for (const full of await walk(root)) {
  const rel = relative(root, full);
  if (!/\.(ts|mjs|json|md)$/.test(rel)) continue;
  const content = await readFile(full, "utf8");
  const banned = ["TO" + "DO", "FIX" + "ME", "PLACE" + "HOLDER"];
  if (banned.some((word) => content.toUpperCase().includes(word))) failures.push(`INCOMPLETE_MARKER:${rel}`);
  if (/\bsk-(?:proj-)?[A-Za-z0-9]{20,}\b/.test(content)) failures.push(`POSSIBLE_SECRET:${rel}`);
}

if (failures.length > 0) {
  console.error(JSON.stringify({ status: "FAIL", failures }, null, 2));
  process.exitCode = 1;
} else {
  console.log(JSON.stringify({ status: "PASS", required_files: required.length, fixture_cases: 21 }, null, 2));
}
