import { createHash } from 'node:crypto';

function normalize(value: unknown): unknown {
  if (typeof value === 'bigint') {
    return { $bigint: value.toString(10) };
  }
  if (Array.isArray(value)) {
    return value.map(normalize);
  }
  if (value !== null && typeof value === 'object') {
    const source = value as Record<string, unknown>;
    const out: Record<string, unknown> = {};
    for (const key of Object.keys(source).sort()) {
      const child = source[key];
      if (child !== undefined) out[key] = normalize(child);
    }
    return out;
  }
  return value;
}

export function canonicalJson(value: unknown): string {
  return JSON.stringify(normalize(value));
}

export function sha256Canonical(value: unknown): string {
  return createHash('sha256').update(canonicalJson(value), 'utf8').digest('hex');
}

export function stableActionId(value: unknown): string {
  return `act_${sha256Canonical(value).slice(0, 24)}`;
}
