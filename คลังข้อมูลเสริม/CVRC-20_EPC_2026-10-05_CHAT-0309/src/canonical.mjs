import { createHash } from "node:crypto";

function normalize(value) {
  if (typeof value === "bigint") return { $bigint: value.toString(10) };
  if (Array.isArray(value)) return value.map(normalize);
  if (value && typeof value === "object") {
    const out = {};
    for (const key of Object.keys(value).sort()) out[key] = normalize(value[key]);
    return out;
  }
  if (typeof value === "number" && !Number.isFinite(value)) throw new TypeError("non-finite numbers are forbidden in canonical evidence");
  return value;
}
export function canonicalJson(value) { return JSON.stringify(normalize(value)); }
export function sha256Canonical(value) { return createHash("sha256").update(canonicalJson(value), "utf8").digest("hex"); }
export function sortedUnique(values) { return [...new Set(values)].sort((a,b)=>(a<b?-1:a>b?1:0)); }
export function setContainsAll(supersetValues, subsetValues) {
  const superset = new Set(supersetValues);
  return subsetValues.every(value => superset.has(value));
}
export function setIsSubset(subsetValues, supersetValues) {
  const superset = new Set(supersetValues);
  return subsetValues.every(value => superset.has(value));
}
