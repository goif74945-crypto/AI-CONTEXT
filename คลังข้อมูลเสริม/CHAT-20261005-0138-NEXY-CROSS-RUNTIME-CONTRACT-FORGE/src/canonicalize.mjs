import { createHash } from "node:crypto";
import { fail } from "./errors.mjs";

const DANGEROUS_KEYS = new Set(["__proto__", "prototype", "constructor"]);

export function assertJsonSafe(value, path = "$") {
  if (value === null) return;
  const kind = typeof value;
  if (kind === "string" || kind === "boolean") return;
  if (kind === "number") {
    if (!Number.isFinite(value)) fail("NON_JSON_NUMBER", "number must be finite", path);
    return;
  }
  if (kind !== "object") {
    fail("NON_JSON_VALUE", `unsupported JSON value type ${kind}`, path);
  }
  if (Array.isArray(value)) {
    for (let index = 0; index < value.length; index += 1) {
      assertJsonSafe(value[index], `${path}[${index}]`);
    }
    return;
  }
  const proto = Object.getPrototypeOf(value);
  if (proto !== Object.prototype && proto !== null) {
    fail("NON_PLAIN_OBJECT", "objects must have Object.prototype or null prototype", path);
  }
  for (const key of Object.keys(value)) {
    if (DANGEROUS_KEYS.has(key)) {
      fail("DANGEROUS_KEY", `reserved key ${JSON.stringify(key)} is forbidden`, `${path}.${key}`);
    }
    assertJsonSafe(value[key], `${path}.${key}`);
  }
}

export function canonicalize(value) {
  assertJsonSafe(value);
  return canonicalizeSafe(value);
}

function canonicalizeSafe(value) {
  if (value === null || typeof value !== "object") return value;
  if (Array.isArray(value)) return value.map(canonicalizeSafe);
  const output = Object.create(null);
  for (const key of Object.keys(value).sort()) {
    output[key] = canonicalizeSafe(value[key]);
  }
  return output;
}

export function canonicalStringify(value) {
  return JSON.stringify(canonicalize(value));
}

export function canonicalPretty(value) {
  return `${JSON.stringify(canonicalize(value), null, 2)}\n`;
}

export function sha256Hex(value) {
  const bytes = typeof value === "string" ? value : canonicalStringify(value);
  return createHash("sha256").update(bytes, "utf8").digest("hex");
}
