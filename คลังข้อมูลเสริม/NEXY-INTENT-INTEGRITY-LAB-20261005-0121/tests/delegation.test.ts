import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { compileManifest } from "../src/engine.ts";
import { createDelegationCapsule, verifyDelegationCapsule } from "../src/delegation.ts";

async function parent() {
  return compileManifest(await readFile(new URL("../examples/valid.iil", import.meta.url), "utf8")).contract;
}

async function request() {
  return JSON.parse(await readFile(new URL("../examples/delegation.valid.json", import.meta.url), "utf8"));
}

test("least-authority child delegation is admitted", async () => {
  const result = createDelegationCapsule(await parent(), await request());
  assert.equal(result.receipt.status, "ADMIT");
  assert.equal(result.receipt.findings.length, 0);
  assert.match(result.capsule.seal, /^sha256:[0-9a-f]{64}$/);
});

test("delegation seal is deterministic across repeated runs", async () => {
  const p = await parent();
  const r = await request();
  const seals = new Set(Array.from({ length: 500 }, () => createDelegationCapsule(p, r).capsule.seal));
  assert.equal(seals.size, 1);
});

test("delegation cannot introduce a new input", async () => {
  const p = await parent();
  const r = await request();
  r.inputs.push("Unreviewed internet source");
  const result = createDelegationCapsule(p, r);
  assert.equal(result.receipt.status, "FREEZE");
  assert.ok(result.receipt.findings.some((f) => f.code === "IIL_DELEGATION_INPUT_ESCALATION"));
});

test("delegation cannot invent a parent-unrequired output", async () => {
  const p = await parent();
  const r = await request();
  r.requiredOutputs.push("Production deployment");
  const result = createDelegationCapsule(p, r);
  assert.equal(result.receipt.status, "FREEZE");
  assert.ok(result.receipt.findings.some((f) => f.code === "IIL_DELEGATION_OUTPUT_ESCALATION"));
});

test("delegation cannot escape parent in-scope boundary", async () => {
  const p = await parent();
  const r = await request();
  r.inScope = ["another-repository/**"];
  const result = createDelegationCapsule(p, r);
  assert.equal(result.receipt.status, "FREEZE");
  assert.ok(result.receipt.findings.some((f) => f.code === "IIL_DELEGATION_SCOPE_ESCALATION"));
});

test("delegation cannot overlap protected/out-of-scope boundary", async () => {
  const p = await parent();
  const r = await request();
  r.inScope = ["goif74945-crypto/NEXY.AI-/src/**"];
  const result = createDelegationCapsule(p, r);
  assert.equal(result.receipt.status, "FREEZE");
  assert.ok(result.receipt.findings.some((f) => f.code === "IIL_DELEGATION_SCOPE_BOUNDARY_COLLISION"));
});

test("tampering inherited guardrail or authority freezes verification", async () => {
  const p = await parent();
  const created = createDelegationCapsule(p, await request()).capsule;
  const tampered = {
    ...created,
    forbidden: created.forbidden.filter((item) => item !== p.forbidden[0]),
    authorities: [...created.authorities].reverse(),
  };
  const result = verifyDelegationCapsule(p, tampered);
  assert.equal(result.receipt.status, "FREEZE");
  assert.ok(result.receipt.findings.some((f) => f.code === "IIL_DELEGATION_GUARDRAIL_REMOVED"));
  assert.ok(result.receipt.findings.some((f) => f.code === "IIL_DELEGATION_AUTHORITY_CHANGED"));
  assert.ok(result.receipt.findings.some((f) => f.code === "IIL_DELEGATION_SEAL_MISMATCH"));
});

test("unknown delegation request fields are rejected", async () => {
  const p = await parent();
  const r = { ...(await request()), privilegeOverride: true };
  assert.throws(() => createDelegationCapsule(p, r), /IIL_DELEGATION_UNKNOWN_FIELD/);
});
