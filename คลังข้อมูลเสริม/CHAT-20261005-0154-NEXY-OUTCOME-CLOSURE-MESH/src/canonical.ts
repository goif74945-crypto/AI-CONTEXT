export type CanonicalPrimitive = null | boolean | number | string;
export type CanonicalValue = CanonicalPrimitive | readonly CanonicalValue[] | { readonly [key: string]: CanonicalValue };

export function compareText(a: string, b: string): number {
  return a < b ? -1 : a > b ? 1 : 0;
}

export function sortedUnique(values: readonly string[]): string[] {
  return [...new Set(values)].sort(compareText);
}

export function hasDuplicates(values: readonly string[]): boolean {
  return new Set(values).size !== values.length;
}

export function isNonBlank(value: string): boolean {
  return value.trim().length > 0;
}

export function stableStringify(value: CanonicalValue): string {
  if (value === null || typeof value === "boolean" || typeof value === "string") {
    return JSON.stringify(value);
  }
  if (typeof value === "number") {
    if (!Number.isFinite(value)) throw new TypeError("Non-finite numbers are not canonical");
    return Object.is(value, -0) ? "0" : JSON.stringify(value);
  }
  if (Array.isArray(value)) {
    return `[${value.map((entry) => stableStringify(entry)).join(",")}]`;
  }
  const objectValue = value as { readonly [key: string]: CanonicalValue };
  const keys = Object.keys(objectValue).sort(compareText);
  return `{${keys.map((key) => `${JSON.stringify(key)}:${stableStringify(objectValue[key]!)}`).join(",")}}`;
}

/**
 * Deterministic FNV-1a style 64-bit fingerprint over UTF-16 code-unit bytes.
 * This is intentionally a non-cryptographic identity fingerprint. It must not
 * be used as a security hash or evidence-integrity digest.
 */
export function fingerprint64(value: CanonicalValue): string {
  const text = stableStringify(value);
  let hash = 0xcbf29ce484222325n;
  const prime = 0x100000001b3n;
  const mask = 0xffffffffffffffffn;
  for (let index = 0; index < text.length; index += 1) {
    const unit = text.charCodeAt(index);
    hash ^= BigInt(unit & 0xff);
    hash = (hash * prime) & mask;
    hash ^= BigInt((unit >>> 8) & 0xff);
    hash = (hash * prime) & mask;
  }
  return hash.toString(16).padStart(16, "0");
}
