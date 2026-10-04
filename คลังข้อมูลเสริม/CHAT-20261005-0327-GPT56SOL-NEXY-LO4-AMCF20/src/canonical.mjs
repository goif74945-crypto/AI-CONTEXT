import { createHash } from "node:crypto";

function norm(value) {
  if (value === null || typeof value === "string" || typeof value === "boolean") return value;
  if (typeof value === "bigint") return {"$bigint": value.toString(10)};
  if (Array.isArray(value)) return value.map(norm);
  if (typeof value === "object") {
    const out = {};
    for (const key of Object.keys(value).sort()) {
      if (value[key] === undefined) throw new Error("CANONICAL_UNDEFINED_FORBIDDEN");
      out[key] = norm(value[key]);
    }
    return out;
  }
  throw new Error("CANONICAL_TYPE_FORBIDDEN");
}
export function canonicalJson(value) { return JSON.stringify(norm(value)); }
export function sha256Canonical(value) { return createHash("sha256").update(canonicalJson(value),"utf8").digest("hex"); }
export function sha256Text(value) { if(typeof value!=="string") throw new Error("TEXT_REQUIRED"); return createHash("sha256").update(value,"utf8").digest("hex"); }
