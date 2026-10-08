import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";

// EX009 source contract, not a Linux namespace/seccomp runtime attestation.
// Fail on the observed Linux bwrap=false direct-spawn downgrade.
describe("EX009 protected Linux cage fail-closed source fence", () => {
  it("rejects missing bwrap before protected guest process launch", () => {
    const source = readFileSync("packages/phase-f/lo3/cage.ts", "utf8");
    const linux = source.slice(
      source.indexOf("async function runLinuxCgroupSeccomp("),
      source.indexOf("// ── macOS backend:"),
    );
    expect(linux.length).toBeGreaterThan(500);
    const availability = linux.indexOf("const useBwrap    = await bwrapAvailable();");
    const denial = linux.indexOf('throw new CageError(id, "SPAWN_FAILED", "CAGE_OS_ISOLATION_UNAVAILABLE");');
    const direct = linux.indexOf("spawn(trustedCommand.executable, args");
    expect(availability).toBeGreaterThanOrEqual(0);
    expect(denial).toBeGreaterThan(availability);
    expect(direct).toBeGreaterThan(denial);
  });
  it("does not conflate written JSON with installed seccomp", () => {
    const source = readFileSync("packages/phase-f/lo3/cage.ts", "utf8");
    const linux = source.slice(
      source.indexOf("async function runLinuxCgroupSeccomp("),
      source.indexOf("// ── macOS backend:"),
    );
    const merelyWritten = linux.includes("await writeFile(seccompFile, seccompJson");
    const actuallyInstalled = /--seccomp|seccomp_load|seccomp_export_bpf|prctl\s*\(/.test(linux);
    expect(merelyWritten && !actuallyInstalled).toBe(true);
    // This assertion documents an UNRESOLVED SECURITY GAP, not a security PASS.
  });
});
