#!/usr/bin/env node
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { auditRuntimeSnapshot } from "./audit.mjs";
import { compileContract } from "./compiler.mjs";
import { canonicalPretty } from "./canonicalize.mjs";
import { normalizeAndValidateManifest, assertObservedCommitRefIfSha } from "./validate-manifest.mjs";

async function loadJson(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

async function writeText(path, content) {
  await mkdir(dirname(path), { recursive: true });
  await writeFile(path, content, "utf8");
}

function usage() {
  return [
    "Usage:",
    "  node src/cli.mjs validate <manifest.json>",
    "  node src/cli.mjs compile <manifest.json> <output-dir>",
    "  node src/cli.mjs snapshot <manifest.json> <output.json>",
    "  node src/cli.mjs audit <manifest.json> <observed-snapshot.json> [report.json]",
  ].join("\n");
}

async function main(argv) {
  const [command, ...args] = argv;
  if (command === "validate" && args.length === 1) {
    const manifest = await loadJson(resolve(args[0]));
    assertObservedCommitRefIfSha(manifest);
    const result = normalizeAndValidateManifest(manifest);
    process.stdout.write(canonicalPretty({
      status: "PASS",
      contractId: result.normalized.contractId,
      contractVersion: result.normalized.contractVersion,
      semanticFingerprint: result.semanticFingerprint,
      manifestFingerprint: result.manifestFingerprint,
    }));
    return 0;
  }
  if (command === "compile" && args.length === 2) {
    const manifestPath = resolve(args[0]);
    const outputDir = resolve(args[1]);
    const manifest = await loadJson(manifestPath);
    assertObservedCommitRefIfSha(manifest);
    const compiled = compileContract(manifest);
    await Promise.all([
      writeText(resolve(outputDir, "contract.normalized.json"), compiled.normalizedManifest),
      writeText(resolve(outputDir, "contract.generated.ts"), compiled.typescript),
      writeText(resolve(outputDir, "contract.generated.rs"), compiled.rust),
      writeText(resolve(outputDir, "contract.snapshot.json"), compiled.runtimeSnapshot),
      writeText(resolve(outputDir, "contract.fixtures.json"), compiled.fixtures),
      writeText(resolve(outputDir, "compile-evidence.json"), canonicalPretty({
        status: "PASS",
        source: manifestPath,
        semanticFingerprint: compiled.semanticFingerprint,
        manifestFingerprint: compiled.manifestFingerprint,
      })),
    ]);
    process.stdout.write(canonicalPretty({ status: "PASS", outputDir, semanticFingerprint: compiled.semanticFingerprint }));
    return 0;
  }
  if (command === "snapshot" && args.length === 2) {
    const manifest = await loadJson(resolve(args[0]));
    const compiled = compileContract(manifest);
    await writeText(resolve(args[1]), compiled.runtimeSnapshot);
    process.stdout.write(canonicalPretty({ status: "PASS", output: resolve(args[1]), semanticFingerprint: compiled.semanticFingerprint }));
    return 0;
  }
  if (command === "audit" && (args.length === 2 || args.length === 3)) {
    const manifest = await loadJson(resolve(args[0]));
    const observed = await loadJson(resolve(args[1]));
    const report = auditRuntimeSnapshot(manifest, observed);
    const reportText = canonicalPretty(report);
    if (args[2]) await writeText(resolve(args[2]), reportText);
    process.stdout.write(reportText);
    return report.pass ? 0 : 2;
  }
  process.stderr.write(`${usage()}\n`);
  return 64;
}

try {
  const exitCode = await main(process.argv.slice(2));
  process.exitCode = exitCode;
} catch (error) {
  const payload = {
    status: "FAIL",
    error: error instanceof Error ? error.message : String(error),
    code: error && typeof error === "object" && "code" in error ? error.code : "UNEXPECTED_ERROR",
  };
  process.stderr.write(canonicalPretty(payload));
  process.exitCode = 1;
}
