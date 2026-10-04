import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { dirname } from "node:path";
import { spawnSync } from "node:child_process";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, "..");
const CLI = resolve(ROOT, "src/cli.mjs");
const MANIFEST = resolve(ROOT, "examples/vnext-product-state.contract.json");

function run(args) {
  return spawnSync(process.execPath, [CLI, ...args], { cwd: ROOT, encoding: "utf8" });
}

test("CLI validate returns zero and PASS", () => {
  const result = run(["validate", MANIFEST]);
  assert.equal(result.status, 0, result.stderr);
  assert.equal(JSON.parse(result.stdout).status, "PASS");
});

test("CLI compile writes the complete deterministic artifact set", async () => {
  const out = await mkdtemp(join(tmpdir(), "nexy-xrcf-"));
  const result = run(["compile", MANIFEST, out]);
  assert.equal(result.status, 0, result.stderr);
  const expectedFiles = [
    "contract.normalized.json",
    "contract.generated.ts",
    "contract.generated.rs",
    "contract.snapshot.json",
    "contract.fixtures.json",
    "compile-evidence.json",
  ];
  for (const name of expectedFiles) {
    const body = await readFile(join(out, name), "utf8");
    assert.ok(body.length > 0, `${name} must not be empty`);
  }
});

test("CLI audit returns 0 for exact snapshot and 2 for drift", async () => {
  const out = await mkdtemp(join(tmpdir(), "nexy-xrcf-audit-"));
  assert.equal(run(["compile", MANIFEST, out]).status, 0);
  const snapshotPath = join(out, "contract.snapshot.json");
  const pass = run(["audit", MANIFEST, snapshotPath]);
  assert.equal(pass.status, 0, pass.stderr);
  assert.equal(JSON.parse(pass.stdout).status, "PASS");

  const drifted = JSON.parse(await readFile(snapshotPath, "utf8"));
  drifted.enums.vnext_actor = drifted.enums.vnext_actor.filter((x) => x !== "OWNER");
  const driftPath = join(out, "drifted.json");
  await writeFile(driftPath, `${JSON.stringify(drifted, null, 2)}\n`, "utf8");
  const fail = run(["audit", MANIFEST, driftPath]);
  assert.equal(fail.status, 2, fail.stderr);
  assert.equal(JSON.parse(fail.stdout).status, "FAIL");
});

test("CLI invalid manifest returns nonzero with machine-readable failure", async () => {
  const dir = await mkdtemp(join(tmpdir(), "nexy-xrcf-invalid-"));
  const invalidPath = join(dir, "invalid.json");
  await writeFile(invalidPath, JSON.stringify({ schemaVersion: 999 }), "utf8");
  const result = run(["validate", invalidPath]);
  assert.equal(result.status, 1);
  const payload = JSON.parse(result.stderr);
  assert.equal(payload.status, "FAIL");
  assert.equal(payload.code, "UNSUPPORTED_SCHEMA_VERSION");
});

test("generated TypeScript passes strict tsc when compiler is available", async (t) => {
  const version = spawnSync("tsc", ["--version"], { encoding: "utf8" });
  if (version.status !== 0) {
    t.skip("tsc is not available in this execution environment");
    return;
  }
  const out = await mkdtemp(join(tmpdir(), "nexy-xrcf-tsc-"));
  assert.equal(run(["compile", MANIFEST, out]).status, 0);
  const generated = join(out, "contract.generated.ts");
  const result = spawnSync("tsc", [
    "--noEmit",
    "--target", "ES2022",
    "--module", "Node16",
    "--moduleResolution", "Node16",
    "--strict",
    "--exactOptionalPropertyTypes",
    "--noUncheckedIndexedAccess",
    generated,
  ], { cwd: ROOT, encoding: "utf8" });
  assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`);
});
