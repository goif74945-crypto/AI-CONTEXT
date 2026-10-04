const MASK64 = (1n << 64n) - 1n;
const FNV_PRIME = 1099511628211n;
const SEEDS = [
  14695981039346656037n,
  1099511628211n ^ 0x9e3779b97f4a7c15n,
  0xcbf29ce484222325n ^ 0xd6e8feb86659fd93n,
  0x84222325cbf29ce4n ^ 0xa0761d6478bd642fn,
] as const;

export function canonical(value: unknown): string {
  if (value === null) return 'null';
  if (typeof value === 'bigint') return JSON.stringify(value.toString(10));
  if (typeof value === 'string' || typeof value === 'boolean') return JSON.stringify(value);
  if (typeof value === 'number') {
    if (!Number.isSafeInteger(value)) throw new Error('CANONICAL_NUMBER_MUST_BE_SAFE_INTEGER');
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) return '[' + value.map(canonical).join(',') + ']';
  if (typeof value === 'object') {
    const obj = value as Record<string, unknown>;
    return '{' + Object.keys(obj).sort().map((key) => JSON.stringify(key) + ':' + canonical(obj[key])).join(',') + '}';
  }
  throw new Error('CANONICAL_VALUE_UNSUPPORTED');
}

function fnv64(text: string, seed: bigint): bigint {
  let h = seed & MASK64;
  for (let i = 0; i < text.length; i += 1) {
    h ^= BigInt(text.charCodeAt(i));
    h = (h * FNV_PRIME) & MASK64;
  }
  return h;
}

/** Deterministic 256-bit identity fingerprint. Not a cryptographic integrity primitive. */
export function fingerprint(value: unknown): string {
  const text = canonical(value);
  return SEEDS.map((seed) => fnv64(text, seed).toString(16).padStart(16, '0')).join('');
}
