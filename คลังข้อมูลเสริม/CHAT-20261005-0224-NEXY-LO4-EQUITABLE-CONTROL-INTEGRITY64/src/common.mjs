import { Q64, ensureQ64 } from './q64.mjs';

export function requireCount(value, label) {
  if (typeof value !== 'bigint' || value < 0n) throw new TypeError(`${label} must be a nonnegative bigint`);
  return value;
}

export function requirePositiveCount(value, label) {
  requireCount(value, label);
  if (value === 0n) throw new RangeError(`${label} must be > 0`);
  return value;
}

export function rate(numerator, denominator, label = 'rate') {
  const n = requireCount(numerator, `${label}.numerator`);
  const d = requirePositiveCount(denominator, `${label}.denominator`);
  if (n > d) throw new RangeError(`${label}: numerator exceeds denominator`);
  return Q64.fromRatio(n, d);
}

export function average(total, count, label = 'average') {
  const t = ensureQ64(total);
  const c = requirePositiveCount(count, `${label}.count`);
  if (t.lt(Q64.zero())) throw new RangeError(`${label}.total must be nonnegative`);
  return t.div(Q64.fromInt(c));
}

export function cohortRows(cohorts, minSample, metricFn) {
  if (!Array.isArray(cohorts) || cohorts.length < 2) throw new TypeError('at least two cohorts are required');
  const min = requirePositiveCount(minSample, 'minSample');
  const ids = new Set();
  const rows = [];
  for (const cohort of cohorts) {
    if (!cohort || typeof cohort.id !== 'string' || cohort.id.length === 0) throw new TypeError('cohort.id required');
    if (ids.has(cohort.id)) throw new TypeError(`duplicate cohort id: ${cohort.id}`);
    ids.add(cohort.id);
    const sample = requireCount(cohort.total, `${cohort.id}.total`);
    if (sample < min) return { status: 'INSUFFICIENT_SAMPLE', cohortId: cohort.id, rows: [] };
    rows.push(metricFn(cohort));
  }
  return { status: 'OK', rows };
}

export function rangeGap(values) {
  if (!Array.isArray(values) || values.length === 0) throw new TypeError('values required');
  let min = ensureQ64(values[0]);
  let max = min;
  for (const value of values.slice(1)) {
    const q = ensureQ64(value);
    min = min.min(q);
    max = max.max(q);
  }
  return { min, max, gap: max.sub(min) };
}

export function validateGapThreshold(value, label) {
  const q = ensureQ64(value);
  if (q.lt(Q64.zero()) || q.gt(Q64.one())) throw new RangeError(`${label} must be within [0,1]`);
  return q;
}
