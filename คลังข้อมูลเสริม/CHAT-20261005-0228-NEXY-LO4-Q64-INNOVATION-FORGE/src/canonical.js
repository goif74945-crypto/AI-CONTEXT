import { createHash } from 'node:crypto';
import { Q64 } from './q64.js';

function normalize(value) {
  if (value instanceof Q64) return value.toJSON();
  if (typeof value === 'bigint') return value.toString();
  if (Array.isArray(value)) return value.map(normalize);
  if (value && typeof value === 'object') {
    const out = {};
    for (const key of Object.keys(value).sort()) out[key] = normalize(value[key]);
    return out;
  }
  return value;
}

export function canonicalJson(value) {
  return JSON.stringify(normalize(value));
}

export function digest(value) {
  return createHash('sha256').update(canonicalJson(value)).digest('hex');
}
