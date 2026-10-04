export type JsonPrimitive = null | boolean | number | string;
export type JsonValue = JsonPrimitive | readonly JsonValue[] | { readonly [key: string]: JsonValue };

export class ContractError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ContractError";
  }
}

export function assertNonEmpty(value: string, label: string): string {
  if (value.trim().length === 0) throw new ContractError(`${label} must be non-empty`);
  return value;
}

export function assertSafeInt(value: number, label: string, min = 0): number {
  if (!Number.isSafeInteger(value) || value < min) {
    throw new ContractError(`${label} must be a safe integer >= ${min}`);
  }
  return value;
}

export function canonicalize(value: JsonValue): string {
  if (value === null) return "null";
  if (typeof value === "boolean") return value ? "true" : "false";
  if (typeof value === "number") {
    if (!Number.isSafeInteger(value)) throw new ContractError("canonical numbers must be safe integers");
    return String(Object.is(value, -0) ? 0 : value);
  }
  if (typeof value === "string") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map((item) => canonicalize(item)).join(",")}]`;
  const record = value as { readonly [key: string]: JsonValue };
  return `{${Object.keys(record).sort().map((key) => `${JSON.stringify(key)}:${canonicalize(record[key]!)}`).join(",")}}`;
}

export function fnv1a64(text: string): string {
  let hash = 0xcbf29ce484222325n;
  const prime = 0x100000001b3n;
  for (const codePoint of text) {
    const bytes = new TextEncoder().encode(codePoint);
    for (const byte of bytes) {
      hash ^= BigInt(byte);
      hash = BigInt.asUintN(64, hash * prime);
    }
  }
  return hash.toString(16).padStart(16, "0");
}

export function fingerprint(value: JsonValue): string {
  return fnv1a64(canonicalize(value));
}

export function stableUnique(values: readonly string[], label: string): readonly string[] {
  const seen = new Set<string>();
  for (const value of values) {
    assertNonEmpty(value, label);
    if (seen.has(value)) throw new ContractError(`${label} contains duplicate value ${value}`);
    seen.add(value);
  }
  return [...seen].sort();
}

export function checkedAdd(a: bigint, b: bigint, cap: bigint, label: string): bigint {
  const out = a + b;
  if (out > cap) throw new ContractError(`${label} exceeds configured analysis cap`);
  return out;
}

export function checkedMul(a: bigint, b: bigint, cap: bigint, label: string): bigint {
  const out = a * b;
  if (out > cap) throw new ContractError(`${label} exceeds configured analysis cap`);
  return out;
}
