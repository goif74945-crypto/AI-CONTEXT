import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import {
  auditRuntimeSnapshot,
  buildExpectedRuntimeSnapshot,
  canonicalStringify,
  compileContract,
  compileRust,
  compileTypeScript,
  normalizeAndValidateManifest,
} from "../src/index.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, "..");
const example = JSON.parse(await readFile(resolve(ROOT, "examples/vnext-product-state.contract.json"), "utf8"));

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function minimalManifest() {
  return {
    schemaVersion: 1,
    contractId: "test.machine",
    contractVersion: "1.0.0",
    enums: [
      { name: "State", wireName: "state", members: [{ name: "A", wire: "A" }, { name: "B", wire: "B" }, { name: "Stop", wire: "STOP" }] },
      { name: "Event", wireName: "event", members: [{ name: "Go", wire: "go" }] },
      { name: "Actor", wireName: "actor", members: [{ name: "Core", wire: "CORE" }, { name: "Owner", wire: "OWNER" }] },
    ],
    stateMachines: [{
      name: "Machine",
      stateEnum: "State",
      eventEnum: "Event",
      actorEnum: "Actor",
      initialState: "A",
      terminalStates: ["STOP"],
      transitions: [{ from: "A", event: "go", to: "B", actors: ["CORE"], guards: ["ready"] }],
    }],
  };
}

test("example manifest validates and yields 64-hex fingerprints", () => {
  const result = normalizeAndValidateManifest(example);
  assert.match(result.semanticFingerprint, /^[0-9a-f]{64}$/);
  assert.match(result.manifestFingerprint, /^[0-9a-f]{64}$/);
  assert.notEqual(result.semanticFingerprint, result.manifestFingerprint, "provenance should affect manifest fingerprint but not semantic view");
});

test("semantic fingerprint is stable across non-semantic ordering changes", () => {
  const a = minimalManifest();
  const b = clone(a);
  b.enums.reverse();
  b.enums[0].members.reverse();
  b.stateMachines[0].transitions[0].actors.reverse();
  b.stateMachines[0].transitions[0].guards.reverse();
  const fa = normalizeAndValidateManifest(a).semanticFingerprint;
  const fb = normalizeAndValidateManifest(b).semanticFingerprint;
  assert.equal(fa, fb);
});

test("semantic fingerprint changes when a wire value changes", () => {
  const a = minimalManifest();
  const b = clone(a);
  b.enums.find((x) => x.name === "State").members.find((x) => x.name === "B").wire = "B2";
  b.stateMachines[0].transitions[0].to = "B2";
  assert.notEqual(
    normalizeAndValidateManifest(a).semanticFingerprint,
    normalizeAndValidateManifest(b).semanticFingerprint,
  );
});

test("validator rejects duplicate enum wire values", () => {
  const m = minimalManifest();
  m.enums[0].members.push({ name: "Duplicate", wire: "A" });
  assert.throws(() => normalizeAndValidateManifest(m), /DUPLICATE_ENUM_WIRE/);
});

test("validator rejects unknown enum references", () => {
  const m = minimalManifest();
  m.stateMachines[0].actorEnum = "MissingActor";
  assert.throws(() => normalizeAndValidateManifest(m), /UNKNOWN_ENUM_REFERENCE/);
});

test("validator rejects actor-aware non-deterministic transitions", () => {
  const m = minimalManifest();
  m.stateMachines[0].transitions.push({ from: "A", event: "go", to: "STOP", actors: ["CORE"], guards: ["ready"] });
  assert.throws(() => normalizeAndValidateManifest(m), /NON_DETERMINISTIC_TRANSITION/);
});

test("validator rejects exact duplicate transitions", () => {
  const m = minimalManifest();
  m.stateMachines[0].transitions.push(clone(m.stateMachines[0].transitions[0]));
  assert.throws(() => normalizeAndValidateManifest(m), /DUPLICATE_TRANSITION/);
});

test("validator rejects outbound transitions from terminal states", () => {
  const m = minimalManifest();
  m.stateMachines[0].transitions.push({ from: "STOP", event: "go", to: "A", actors: ["OWNER"], guards: [] });
  assert.throws(() => normalizeAndValidateManifest(m), /TERMINAL_OUTBOUND_TRANSITION/);
});

test("validator rejects dangerous prototype-related keys from parsed JSON", () => {
  const malicious = JSON.parse('{"schemaVersion":1,"contractId":"x.y","contractVersion":"1.0.0","enums":[],"stateMachines":[],"__proto__":{"polluted":true}}');
  assert.throws(() => normalizeAndValidateManifest(malicious), /DANGEROUS_KEY/);
  assert.equal({}.polluted, undefined);
});

test("validator rejects code-injection-shaped wire values", () => {
  const m = minimalManifest();
  m.enums[0].members[0].wire = 'A"; process.exit(1); //';
  assert.throws(() => normalizeAndValidateManifest(m), /STRING_FORMAT/);
});

test("compiler is byte-deterministic", () => {
  const first = compileContract(example);
  const second = compileContract(clone(example));
  assert.equal(first.typescript, second.typescript);
  assert.equal(first.rust, second.rust);
  assert.equal(first.runtimeSnapshot, second.runtimeSnapshot);
  assert.equal(first.fixtures, second.fixtures);
});

test("TypeScript generator emits contract identity and guarded transition API", () => {
  const output = compileTypeScript(example);
  assert.match(output, /CONTRACT_SEMANTIC_FINGERPRINT/);
  assert.match(output, /export function VNextLifecycleNext/);
  assert.match(output, /freeze_recovery_allowed/);
  assert.match(output, /readonly actors/);
});

test("Rust generator stays no_std and avoids allocation types", () => {
  const output = compileRust(example);
  assert.match(output, /#!\[no_std\]/);
  assert.match(output, /pub fn vnext_lifecycle_next/);
  assert.doesNotMatch(output, /\bstd::/);
  assert.doesNotMatch(output, /\bVec\b/);
  assert.doesNotMatch(output, /\bString\b/);
});

test("expected runtime snapshot self-audits PASS", () => {
  const snapshot = buildExpectedRuntimeSnapshot(example);
  const report = auditRuntimeSnapshot(example, snapshot);
  assert.equal(report.pass, true);
  assert.equal(report.status, "PASS");
  assert.deepEqual(report.diffs, []);
});

test("runtime snapshot audit fails closed on a missing enum member", () => {
  const snapshot = buildExpectedRuntimeSnapshot(example);
  snapshot.enums.vnext_state = snapshot.enums.vnext_state.filter((x) => x !== "FREEZE");
  const report = auditRuntimeSnapshot(example, snapshot);
  assert.equal(report.pass, false);
  assert.equal(report.status, "FAIL");
  assert.ok(report.diffs.some((x) => x.kind === "VALUE_MISMATCH" || x.kind === "MISSING_VALUE"));
});

test("runtime snapshot audit fails closed on unexpected fields", () => {
  const snapshot = buildExpectedRuntimeSnapshot(example);
  snapshot.unapproved = true;
  const report = auditRuntimeSnapshot(example, snapshot);
  assert.equal(report.pass, false);
  assert.ok(report.diffs.some((x) => x.kind === "UNEXPECTED_KEY" && x.path === "$.unapproved"));
});

test("normalization does not mutate caller input", () => {
  const input = minimalManifest();
  const before = canonicalStringify(input);
  normalizeAndValidateManifest(input);
  assert.equal(canonicalStringify(input), before);
});
